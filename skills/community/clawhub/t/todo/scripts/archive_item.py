#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_items, save_items, load_archive, save_archive, load_stats, save_stats

def main():
    parser = argparse.ArgumentParser(description="Archive an item")
    parser.add_argument("--id", required=True, help="Item ID")
    args = parser.parse_args()

    data = load_items()
    items = data.get("items", {})

    if args.id not in items:
        print(f"Item not found: {args.id}")
        sys.exit(1)

    item = items.pop(args.id)
    item["archived_at"] = datetime.now().isoformat()

    archive = load_archive()
    archive["items"][args.id] = item
    save_archive(archive)
    save_items(data)

    stats = load_stats()
    stats["total_items_archived"] += 1
    save_stats(stats)

    print(f"✓ Archived {args.id}")
    print(f"  {item['title']}")

if __name__ == "__main__":
    main()
