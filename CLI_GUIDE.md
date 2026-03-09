# ShortsShield CLI Usage Guide

The command-line interface allows you to manage your facts database without the GUI.

## Quick Reference

```bash
# List all facts
shortsshield-cli list

# Add a new fact
shortsshield-cli add "Your fact here" --category science

# Get a random fact
shortsshield-cli random

# View categories
shortsshield-cli categories

# Show statistics
shortsshield-cli stats

# Import from JSON
shortsshield-cli import facts.json

# Export to JSON
shortsshield-cli export backup.json

# Delete a fact (by ID)
shortsshield-cli delete 5
```

## Detailed Usage

### List Facts

Display all facts in the database:

```bash
$ shortsshield-cli list

📚 Found 23 fact(s)

┌─ [23] ANIMALS ─────────────────────────────
│ Penguins propose to their mates with a pebble.
└─ Source: Zoology | Added: 2024-03-09 10:30:45

┌─ [22] ANIMALS ─────────────────────────────
│ A group of crows is called a 'murder'.
└─ Source: Ornithology | Added: 2024-03-09 10:30:45
```

**Options**:
- `--category CATEGORY` - Filter by category
- `--limit N` - Show only first N facts

Examples:
```bash
# Show only biology facts
shortsshield-cli list --category biology

# Show first 5 facts
shortsshield-cli list --limit 5

# Show first 3 science facts
shortsshield-cli list --category science --limit 3
```

### Add a Fact

Add a new fun fact to the database:

```bash
$ shortsshield-cli add "Honey never spoils" --category biology

✅ Fact added successfully! (ID: 45)
```

**Syntax**:
```bash
shortsshield-cli add "FACT_TEXT" [--category CATEGORY] [--source SOURCE]
```

**Parameters**:
- `FACT_TEXT` (required) - The fact to add (use quotes for multi-word facts)
- `--category` (optional) - Category name (default: "general")
- `--source` (optional) - Where the fact comes from (default: "cli")

**Examples**:
```bash
# Basic fact
shortsshield-cli add "The Earth orbits the Sun"

# With category
shortsshield-cli add "Octopuses have three hearts" --category biology

# With source
shortsshield-cli add "Venus rotates backwards" --category astronomy --source nasa

# Complex fact
shortsshield-cli add "A single bolt of lightning is 5 times hotter than the sun" \
  --category physics --source weather-science
```

### Get Random Fact

Display a random fun fact from the database:

```bash
$ shortsshield-cli random

💡 The human nose can detect over 1 trillion different scents.

   Category: biology | Source: Rockefeller University (ID: 3)
```

Run this command multiple times to get different facts.

### View Categories

See all available categories and how many facts are in each:

```bash
$ shortsshield-cli categories

📂 Fact Categories:

  animals         ▓▓▓▓▓▓▓▓▓▓ 10
  biology         ▓▓▓▓▓ 5
  physics         ▓▓▓▓ 4
  astronomy       ▓▓▓ 3
  nature          ▓▓ 2
  history         ▓▓ 2
  general         ▓ 1
```

This helps you see what categories are available and how much content is in each.

### Show Statistics

Display database statistics:

```bash
$ shortsshield-cli stats

📊 ShortsShield Statistics

  Total Facts:      25
  Total Displays:   142
  Categories:       8
  Database Path:    /home/user/.config/shortsshield/facts.db
```

Useful for monitoring:
- How many facts you've added
- How often the app has been used
- Database storage location

### Import Facts from JSON

Bulk import facts from a JSON file:

```bash
# Use the included sample facts
shortsshield-cli import sample_facts.json

✅ Imported 25 fact(s) from sample_facts.json
```

**JSON Format**:
```json
[
  {
    "text": "Your fact here",
    "category": "science",
    "source": "Wikipedia"
  },
  {
    "text": "Another fact",
    "category": "animals",
    "source": "National Geographic"
  }
]
```

**Creating your own facts file**:
1. Create `my_facts.json`
2. Add array of fact objects
3. Run: `shortsshield-cli import my_facts.json`

### Export Facts to JSON

Save all facts to a JSON file for backup or sharing:

```bash
# Create a backup
shortsshield-cli export backup.json

✅ Exported 25 fact(s) to backup.json
```

**Use cases**:
- Backup before major changes
- Share facts with others
- Migrate to new computer
- Archive old facts

### Delete a Fact

Remove a fact from the database by ID:

```bash
# First, find the ID
shortsshield-cli list

# Then delete it
shortsshield-cli delete 5

✅ Fact 5 deleted.
```

**Finding IDs**:
- Run `shortsshield-cli list` to see fact IDs
- They appear in brackets: `[5]`

## Advanced Usage

### Create Themed Fact Collections

Organize facts by theme:

```bash
# Create a science facts file
cat > science_facts.json << 'EOF'
[
  {"text": "Fact 1", "category": "physics", "source": "Science Today"},
  {"text": "Fact 2", "category": "chemistry", "source": "Chemistry Journal"}
]
EOF

# Import them
shortsshield-cli import science_facts.json
```

### Backup & Restore

Create regular backups:

```bash
# Backup (daily)
shortsshield-cli export backup_$(date +%Y%m%d).json

# This creates: backup_20240309.json, backup_20240310.json, etc.
```

To restore:

```bash
# If you accidentally delete facts, import from backup
shortsshield-cli import backup_20240309.json
```

### Scripts & Automation

Use the CLI in bash scripts:

```bash
#!/bin/bash
# daily_fact.sh - Show a fact each day

echo "📚 Today's Fun Fact:"
shortsshield-cli random

# Add to cron for daily emails
# 0 9 * * * /path/to/daily_fact.sh | mail -s "Daily Fact" you@example.com
```

Create a cron job:

```bash
# Show a fact every morning at 9 AM
(crontab -l 2>/dev/null; echo "0 9 * * * shortsshield-cli random") | crontab -
```

### Data Analysis

Analyze your facts:

```bash
# Count facts by category
shortsshield-cli categories

# See most common categories
shortsshield-cli list | grep "┌─ \[" | awk '{print $NF}' | sort | uniq -c

# Total number of facts
shortsshield-cli stats | grep "Total Facts"
```

### Integration with Other Tools

```bash
# Show random fact and copy to clipboard (Linux)
shortsshield-cli random | xclip -selection clipboard

# Show random fact in a notification
shortsshield-cli random | notify-send -u normal "Fun Fact"

# Add fact from another program
echo "Interesting fact" | xargs shortsshield-cli add
```

## Troubleshooting

### Command not found

```bash
# Make sure you've installed it
pip3 install --user PyGObject requests

# Or run directly
python3 shortsshield-cli.py list
```

### Database errors

```bash
# Reset database (deletes all facts and history)
rm ~/.config/shortsshield/facts.db

# Run the app once to recreate it
shortsshield-cli list
```

### Import errors

```bash
# Check JSON syntax
python3 -m json.tool my_facts.json

# Verify format
cat my_facts.json | python3 -c "import sys, json; json.load(sys.stdin); print('Valid')"
```

## Tips & Tricks

1. **Add facts while thinking of them**:
   ```bash
   shortsshield-cli add "Remember this!"
   ```

2. **Organize by source**:
   ```bash
   shortsshield-cli add "Fact" --category science --source wikipedia
   shortsshield-cli add "Fact" --category science --source nasa
   ```

3. **Batch import educational content**:
   ```bash
   # Extract facts from a document and create JSON
   # Then: shortsshield-cli import facts.json
   ```

4. **Share collections**:
   ```bash
   # Export your favorite facts
   shortsshield-cli export my_collection.json
   # Send to a friend
   # Friend imports: shortsshield-cli import my_collection.json
   ```

5. **Keep it organized**:
   ```bash
   # Regularly check statistics
   shortsshield-cli stats
   
   # Remove duplicates/unwanted facts
   shortsshield-cli list | grep "ID\|Source"
   shortsshield-cli delete [ID]
   ```

## Help

Get help for any command:

```bash
shortsshield-cli --help
shortsshield-cli add --help
shortsshield-cli import --help
```

---

**Master the CLI to unlock the full power of ShortsShield!** 🎓
