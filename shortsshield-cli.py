#!/usr/bin/env python3
"""
ShortsShield CLI - Command-line interface for managing fun facts
Allows adding, listing, and managing facts without the GUI
"""

import sys
import json
import sqlite3
import argparse
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import textwrap


class ShortsShieldCLI:
    """Command-line interface for ShortsShield"""
    
    def __init__(self):
        self.db_path = Path.home() / ".config/shortsshield/facts.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _connect(self):
        """Connect to database"""
        return sqlite3.connect(self.db_path)
    
    def list_facts(self, category: str = None, limit: int = None):
        """List all facts, optionally filtered by category"""
        conn = self._connect()
        cursor = conn.cursor()
        
        if category:
            cursor.execute('''
                SELECT id, text, category, source, timestamp
                FROM fun_facts
                WHERE category = ?
                ORDER BY id DESC
            ''', (category,))
        else:
            cursor.execute('''
                SELECT id, text, category, source, timestamp
                FROM fun_facts
                ORDER BY id DESC
            ''')
        
        facts = cursor.fetchall()
        conn.close()
        
        if not facts:
            print("❌ No facts found.")
            return
        
        print(f"\n📚 Found {len(facts)} fact(s)\n")
        
        for idx, (fact_id, text, cat, source, ts) in enumerate(facts, 1):
            if limit and idx > limit:
                break
            
            print(f"┌─ [{fact_id}] {cat.upper()} ─────────────────────────────")
            wrapped = textwrap.fill(text, width=70)
            print(f"│ {wrapped}")
            print(f"└─ Source: {source} | Added: {ts}")
            print()
    
    def add_fact(self, text: str, category: str = "general", source: str = "cli"):
        """Add a new fact"""
        conn = self._connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO fun_facts (text, category, source)
                VALUES (?, ?, ?)
            ''', (text, category, source))
            conn.commit()
            fact_id = cursor.lastrowid
            print(f"✅ Fact added successfully! (ID: {fact_id})")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            conn.close()
    
    def delete_fact(self, fact_id: int):
        """Delete a fact by ID"""
        conn = self._connect()
        cursor = conn.cursor()
        
        # Check if exists
        cursor.execute('SELECT text FROM fun_facts WHERE id = ?', (fact_id,))
        fact = cursor.fetchone()
        
        if not fact:
            print(f"❌ Fact {fact_id} not found.")
            conn.close()
            return
        
        cursor.execute('DELETE FROM fun_facts WHERE id = ?', (fact_id,))
        cursor.execute('DELETE FROM displayed_facts WHERE fact_id = ?', (fact_id,))
        conn.commit()
        
        print(f"✅ Fact {fact_id} deleted.")
        conn.close()
    
    def get_random(self):
        """Get a random fact"""
        conn = self._connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, text, category, source
            FROM fun_facts
            ORDER BY RANDOM()
            LIMIT 1
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            fact_id, text, category, source = result
            print(f"\n💡 {text}")
            print(f"\n   Category: {category} | Source: {source} (ID: {fact_id})\n")
        else:
            print("❌ No facts available.")
    
    def get_categories(self):
        """List all fact categories"""
        conn = self._connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT category, COUNT(*) as count
            FROM fun_facts
            GROUP BY category
            ORDER BY count DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            print("❌ No facts found.")
            return
        
        print("\n📂 Fact Categories:\n")
        for category, count in results:
            bar_length = int(count / 2)
            bar = "▓" * bar_length
            print(f"  {category:15} {bar} {count}")
        print()
    
    def import_bulk(self, json_file: str):
        """Import facts from JSON file"""
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                data = [data]
            
            conn = self._connect()
            cursor = conn.cursor()
            
            count = 0
            for item in data:
                if isinstance(item, dict) and 'text' in item:
                    text = item['text']
                    category = item.get('category', 'general')
                    source = item.get('source', 'imported')
                    
                    cursor.execute('''
                        INSERT INTO fun_facts (text, category, source)
                        VALUES (?, ?, ?)
                    ''', (text, category, source))
                    count += 1
            
            conn.commit()
            conn.close()
            print(f"✅ Imported {count} fact(s) from {json_file}")
        
        except FileNotFoundError:
            print(f"❌ File not found: {json_file}")
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in {json_file}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def export_bulk(self, output_file: str):
        """Export all facts to JSON file"""
        conn = self._connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT text, category, source FROM fun_facts')
        facts = cursor.fetchall()
        conn.close()
        
        if not facts:
            print("❌ No facts to export.")
            return
        
        data = [
            {
                "text": text,
                "category": category,
                "source": source
            }
            for text, category, source in facts
        ]
        
        try:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✅ Exported {len(data)} fact(s) to {output_file}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def get_stats(self):
        """Show database statistics"""
        conn = self._connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM fun_facts')
        total_facts = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM displayed_facts')
        total_displays = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT category) FROM fun_facts')
        categories = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"\n📊 ShortsShield Statistics\n")
        print(f"  Total Facts:      {total_facts}")
        print(f"  Total Displays:   {total_displays}")
        print(f"  Categories:       {categories}")
        print(f"  Database Path:    {self.db_path}\n")


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description='ShortsShield CLI - Manage fun facts database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  shortsshield-cli list
  shortsshield-cli list --category science
  shortsshield-cli add "Octopuses have three hearts" --category biology
  shortsshield-cli random
  shortsshield-cli categories
  shortsshield-cli stats
  shortsshield-cli import facts.json
  shortsshield-cli export backup.json
  shortsshield-cli delete 5
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all facts')
    list_parser.add_argument('--category', help='Filter by category')
    list_parser.add_argument('--limit', type=int, help='Limit number of results')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new fact')
    add_parser.add_argument('text', help='Fact text')
    add_parser.add_argument('--category', default='general', help='Category')
    add_parser.add_argument('--source', default='cli', help='Source')
    
    # Delete command
    del_parser = subparsers.add_parser('delete', help='Delete a fact')
    del_parser.add_argument('id', type=int, help='Fact ID')
    
    # Random command
    subparsers.add_parser('random', help='Get a random fact')
    
    # Categories command
    subparsers.add_parser('categories', help='List fact categories')
    
    # Stats command
    subparsers.add_parser('stats', help='Show statistics')
    
    # Import command
    imp_parser = subparsers.add_parser('import', help='Import facts from JSON')
    imp_parser.add_argument('file', help='JSON file path')
    
    # Export command
    exp_parser = subparsers.add_parser('export', help='Export facts to JSON')
    exp_parser.add_argument('file', help='Output file path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = ShortsShieldCLI()
    
    if args.command == 'list':
        cli.list_facts(args.category, args.limit)
    elif args.command == 'add':
        cli.add_fact(args.text, args.category, args.source)
    elif args.command == 'delete':
        cli.delete_fact(args.id)
    elif args.command == 'random':
        cli.get_random()
    elif args.command == 'categories':
        cli.get_categories()
    elif args.command == 'stats':
        cli.get_stats()
    elif args.command == 'import':
        cli.import_bulk(args.file)
    elif args.command == 'export':
        cli.export_bulk(args.file)


if __name__ == '__main__':
    main()
