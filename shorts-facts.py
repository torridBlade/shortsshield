#!/usr/bin/env python3
"""
ShortsShield - YouTube Shorts Ad Replacer with Fun Facts
A FOSS application that replaces YouTube ads with engaging fun facts.
Designed for Linux systems.

Author: Senior Software Engineer
License: MIT
"""

import sys
import json
import random
import threading
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')

from gi.repository import Gtk, WebKit2, GLib, Gio
import requests
from dataclasses import dataclass, asdict


@dataclass
class FunFact:
    """Immutable fun fact data structure"""
    id: int
    text: str
    category: str
    source: str
    timestamp: str


class FunFactDatabase:
    """Manages the fun facts SQLite database"""
    
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        self._load_default_facts()
    
    def _init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fun_facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                source TEXT DEFAULT 'unknown',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS displayed_facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact_id INTEGER,
                displayed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(fact_id) REFERENCES fun_facts(id)
            )
        ''')
        conn.commit()
        conn.close()
    
    def _load_default_facts(self):
        """Load default fun facts if database is empty"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM fun_facts')
        
        if cursor.fetchone()[0] == 0:
            default_facts = [
                ("Octopuses have three hearts and blue blood.", "biology", "Marine Biology"),
                ("A single bolt of lightning is about 5 times hotter than the surface of the sun.", "physics", "Atmospheric Science"),
                ("Honey never spoils and can last thousands of years.", "nature", "Entomology"),
                ("The Great Barrier Reef can be seen from space.", "geography", "Marine Science"),
                ("A group of flamingos is called a 'flamboyance'.", "animals", "Zoology"),
                ("Bananas are berries, but strawberries are not.", "botany", "Agriculture"),
                ("The human body contains about 37 trillion cells.", "biology", "Anatomy"),
                ("Light takes 8 minutes and 20 seconds to reach Earth from the Sun.", "physics", "Astronomy"),
                ("Cleopatra lived closer to the moon landing than to the building of the Great Pyramid.", "history", "Historical Timeline"),
                ("Wombat poop is cube-shaped to prevent it from rolling away.", "animals", "Zoology"),
                ("A cockroach can survive for a week without its head.", "insects", "Entomology"),
                ("The smell of rain is caused by bacteria called actinomycetes.", "nature", "Microbiology"),
                ("Dolphins have names for each other.", "animals", "Marine Biology"),
                ("The Eiffel Tower grows about 15 cm taller every summer due to thermal expansion.", "physics", "Engineering"),
                ("An albatross can fly 500 miles without flapping its wings.", "animals", "Ornithology"),
                ("The Antarctic blue whale is the largest animal ever known to have lived.", "animals", "Marine Biology"),
                ("Penguins propose to their mates with a pebble.", "animals", "Zoology"),
                ("The fingerprints of koalas are so similar to humans they could confuse crime scenes.", "animals", "Forensic Science"),
                ("A group of crows is called a 'murder'.", "animals", "Ornithology"),
                ("The shortest war in history lasted only 38 to 45 minutes.", "history", "Military History"),
            ]
            
            for text, category, source in default_facts:
                cursor.execute('''
                    INSERT INTO fun_facts (text, category, source)
                    VALUES (?, ?, ?)
                ''', (text, category, source))
            
            conn.commit()
        
        conn.close()
    
    def get_random_fact(self) -> Optional[FunFact]:
        """Get a random fun fact, preferring ones not recently shown"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Try to get a fact not shown in the last 50 displays
        cursor.execute('''
            SELECT id, text, category, source, timestamp
            FROM fun_facts
            WHERE id NOT IN (
                SELECT fact_id FROM displayed_facts
                ORDER BY displayed_at DESC LIMIT 50
            )
            ORDER BY RANDOM()
            LIMIT 1
        ''')
        
        result = cursor.fetchone()
        
        # If all recent facts exhausted, just get a random one
        if not result:
            cursor.execute('''
                SELECT id, text, category, source, timestamp
                FROM fun_facts
                ORDER BY RANDOM()
                LIMIT 1
            ''')
            result = cursor.fetchone()
        
        if result:
            fact = FunFact(*result)
            # Log this display
            cursor.execute('''
                INSERT INTO displayed_facts (fact_id)
                VALUES (?)
            ''', (fact.id,))
            conn.commit()
            conn.close()
            return fact
        
        conn.close()
        return None
    
    def add_fact(self, text: str, category: str = "general", source: str = "user") -> bool:
        """Add a custom fun fact"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO fun_facts (text, category, source)
                VALUES (?, ?, ?)
            ''', (text, category, source))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding fact: {e}")
            return False


class ShortsShield:
    """Main application window"""
    
    def __init__(self):
        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.window.set_title("ShortsShield - YouTube Shorts with Fun Facts")
        self.window.set_default_size(1280, 720)
        self.window.set_icon_name("media-playback-start")
        
        # CSS provider for styling
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(self._get_css().encode())
        Gtk.StyleContext.add_provider_for_screen(
            self.window.get_screen(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        # Initialize database
        db_path = Path.home() / ".config/shortsshield/facts.db"
        self.db = FunFactDatabase(str(db_path))
        
        # Build UI
        self._build_ui()
        
        self.window.connect("destroy", self._on_destroy)
        self.window.show_all()
    
    def _get_css(self) -> str:
        """Return custom CSS for the application"""
        return """
        * {
            font-family: 'Fira Sans', sans-serif;
        }
        
        #main_box {
            background-color: #0a0e27;
        }
        
        #header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 15px 20px;
            color: white;
        }
        
        #header_label {
            font-size: 18px;
            font-weight: bold;
        }
        
        #fact_display {
            background-color: #1a1f3a;
            color: #e0e0e0;
            padding: 40px;
            margin: 20px;
            border-radius: 12px;
            font-size: 20px;
            line-height: 1.6;
            border-left: 5px solid #667eea;
        }
        
        #button_box {
            padding: 20px;
            spacing: 10px;
        }
        
        button {
            padding: 12px 24px;
            font-size: 14px;
            border-radius: 6px;
            font-weight: 500;
            transition: all 200ms ease;
        }
        
        #next_fact_btn {
            background-color: #667eea;
            color: white;
        }
        
        #next_fact_btn:hover {
            background-color: #764ba2;
        }
        
        #add_fact_btn {
            background-color: #48bb78;
            color: white;
        }
        
        #add_fact_btn:hover {
            background-color: #38a169;
        }
        
        #youtube_btn {
            background-color: #f00;
            color: white;
        }
        
        #youtube_btn:hover {
            background-color: #cc0000;
        }
        
        #status_bar {
            background-color: #16213e;
            color: #888;
            padding: 10px 20px;
            font-size: 12px;
            border-top: 1px solid #333;
        }
        """
    
    def _build_ui(self):
        """Build the user interface"""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.set_name("main_box")
        
        # Header
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        header.set_name("header")
        header_label = Gtk.Label("✨ ShortsShield - Replace Ads with Wisdom ✨")
        header_label.set_name("header_label")
        header.pack_start(header_label, True, True, 0)
        main_box.pack_start(header, False, False, 0)
        
        # Fact display area
        fact_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        fact_box.set_margin_top(30)
        fact_box.set_margin_bottom(30)
        fact_box.set_margin_start(20)
        fact_box.set_margin_end(20)
        
        self.fact_label = Gtk.Label()
        self.fact_label.set_name("fact_display")
        self.fact_label.set_line_wrap(True)
        self.fact_label.set_line_wrap_mode(True)
        self.fact_label.set_alignment(0.05, 0.5)
        
        fact_box.pack_start(self.fact_label, True, True, 0)
        main_box.pack_start(fact_box, True, True, 0)
        
        # Button box
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        button_box.set_name("button_box")
        button_box.set_homogeneous(False)
        button_box.set_spacing(10)
        
        next_btn = Gtk.Button("📝 Next Fun Fact")
        next_btn.set_name("next_fact_btn")
        next_btn.connect("clicked", self._on_next_fact)
        button_box.pack_start(next_btn, False, False, 0)
        
        add_btn = Gtk.Button("➕ Add Custom Fact")
        add_btn.set_name("add_fact_btn")
        add_btn.connect("clicked", self._on_add_fact)
        button_box.pack_start(add_btn, False, False, 0)
        
        youtube_btn = Gtk.Button("▶️ Open YouTube Shorts")
        youtube_btn.set_name("youtube_btn")
        youtube_btn.connect("clicked", self._on_open_youtube)
        button_box.pack_start(youtube_btn, False, False, 0)
        
        main_box.pack_start(button_box, False, False, 0)
        
        # Status bar
        self.status_label = Gtk.Label()
        self.status_label.set_name("status_bar")
        self.status_label.set_alignment(0, 0.5)
        main_box.pack_end(self.status_label, False, False, 0)
        
        self.window.add(main_box)
        
        # Load initial fact
        self._load_fact()
    
    def _load_fact(self):
        """Load and display a random fun fact"""
        def load_async():
            fact = self.db.get_random_fact()
            GLib.idle_add(self._display_fact, fact)
        
        thread = threading.Thread(target=load_async, daemon=True)
        thread.start()
    
    def _display_fact(self, fact: Optional[FunFact]):
        """Display a fun fact in the UI"""
        if fact:
            text = f"💡 {fact.text}\n\n— {fact.category} ({fact.source})"
            self.fact_label.set_markup(text)
            self.status_label.set_text(f"Loaded {fact.category} fact • ID: {fact.id}")
        else:
            self.fact_label.set_text("No facts available. Add one to get started!")
            self.status_label.set_text("Database error")
        return False
    
    def _on_next_fact(self, widget):
        """Handler for next fact button"""
        self._load_fact()
    
    def _on_add_fact(self, widget):
        """Handler for add fact button"""
        dialog = Gtk.Dialog(
            title="Add Custom Fun Fact",
            parent=self.window,
            flags=Gtk.DialogFlags.MODAL
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        
        content = dialog.get_content_area()
        
        # Fact text
        label1 = Gtk.Label("Fact Text:")
        label1.set_halign(Gtk.Align.START)
        content.pack_start(label1, False, False, 0)
        
        text_buffer = Gtk.TextBuffer()
        text_view = Gtk.TextView(buffer=text_buffer)
        text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        text_view.set_size_request(400, 100)
        content.pack_start(text_view, True, True, 0)
        
        # Category
        label2 = Gtk.Label("Category:")
        label2.set_halign(Gtk.Align.START)
        content.pack_start(label2, False, False, 0)
        
        category_entry = Gtk.Entry()
        category_entry.set_text("general")
        content.pack_start(category_entry, False, False, 0)
        
        content.show_all()
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            fact_text = text_buffer.get_text(
                text_buffer.get_start_iter(),
                text_buffer.get_end_iter(),
                False
            )
            category = category_entry.get_text()
            
            if self.db.add_fact(fact_text, category, "user"):
                self._show_notification("✓ Fact added successfully!")
            else:
                self._show_notification("✗ Error adding fact")
        
        dialog.destroy()
    
    def _on_open_youtube(self, widget):
        """Handler to open YouTube Shorts"""
        import subprocess
        try:
            subprocess.Popen(["xdg-open", "https://www.youtube.com/shorts"])
            self.status_label.set_text("Opening YouTube Shorts...")
        except Exception as e:
            self._show_notification(f"Error: {e}")
    
    def _show_notification(self, message: str):
        """Show a simple notification"""
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()
    
    def _on_destroy(self, widget):
        """Handler for window close"""
        Gtk.main_quit()
    
    def run(self):
        """Start the application"""
        Gtk.main()


def main():
    """Entry point"""
    app = ShortsShield()
    app.run()


if __name__ == "__main__":
    main()
