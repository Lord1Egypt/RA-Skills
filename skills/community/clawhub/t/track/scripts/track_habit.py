#!/usr/bin/env python3
"""Track habit completion."""
import json
import os
import uuid
import argparse
from datetime import datetime

TRACK_DIR = os.path.expanduser("~/.openclaw/workspace/memory/track")

def ensure_dir():
    os.makedirs(TRACK_DIR, exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description='Track habit')
    parser.add_argument('--habit', required=True, help='Habit name')
    parser.add_argument('--value', type=float, help='Tracked value')
    parser.add_argument('--unit', default='', help='Unit (minutes, count, etc)')
    
    args = parser.parse_args()
    
    entry_id = f"HABIT-{str(uuid.uuid4())[:6].upper()}"
    
    entry = {
        "id": entry_id,
        "habit": args.habit,
        "value": args.value,
        "unit": args.unit,
        "date": datetime.now().strftime('%Y-%m-%d'),
        "timestamp": datetime.now().isoformat()
    }
    
    habits_file = os.path.join(TRACK_DIR, "habits.json")
    data = {"entries": []}
    if os.path.exists(habits_file):
        with open(habits_file, 'r') as f:
            data = json.load(f)
    
    data['entries'].append(entry)
    
    ensure_dir()
    with open(habits_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Habit tracked: {args.habit}")
    if args.value:
        print(f"  Value: {args.value} {args.unit}")
    print(f"  Date: {entry['date']}")

if __name__ == '__main__':
    main()
