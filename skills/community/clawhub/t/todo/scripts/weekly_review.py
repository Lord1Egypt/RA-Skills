#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_items, save_items, load_archive, save_archive, load_stats, save_stats

def archive_item(item_id, item):
    archive = load_archive()
    item["archived_at"] = datetime.now().isoformat()
    archive["items"][item_id] = item
    save_archive(archive)

def main():
    parser = argparse.ArgumentParser(description="Weekly review for cold items")
    parser.add_argument("--archive", help="Archive item by ID")
    parser.add_argument("--let_go", help="Let go of item by ID (archives with note)")
    parser.add_argument("--delay", help="Delay item by ID")
    parser.add_argument("--until", help="Delay target date YYYY-MM-DD")
    args = parser.parse_args()

    data = load_items()
    items = data.get("items", {})

    if args.archive:
        if args.archive not in items:
            print(f"Item not found: {args.archive}")
            sys.exit(1)
        item = items.pop(args.archive)
        archive_item(args.archive, item)
        save_items(data)

        stats = load_stats()
        stats["total_items_archived"] += 1
        stats["last_weekly_review_at"] = datetime.now().isoformat()
        save_stats(stats)

        print(f"✓ Archived {args.archive}")
        print(f"  {item['title']}")
        return

    if args.let_go:
        if args.let_go not in items:
            print(f"Item not found: {args.let_go}")
            sys.exit(1)
        item = items.pop(args.let_go)
        existing_notes = item.get("notes", "")
        note_prefix = "[Let go in weekly review]"
        item["notes"] = f"{note_prefix} {existing_notes}".strip()
        archive_item(args.let_go, item)
        save_items(data)

        stats = load_stats()
        stats["total_items_archived"] += 1
        stats["last_weekly_review_at"] = datetime.now().isoformat()
        save_stats(stats)

        print(f"✓ Let go of {args.let_go}")
        print(f"  {item['title']}")
        return

    if args.delay:
        if not args.until:
            print("Missing required argument: --until YYYY-MM-DD")
            sys.exit(1)
        if args.delay not in items:
            print(f"Item not found: {args.delay}")
            sys.exit(1)

        item = items[args.delay]
        item["do_date"] = args.until
        item["updated_at"] = datetime.now().isoformat()
        item["last_touched_at"] = datetime.now().isoformat()
        save_items(data)

        stats = load_stats()
        stats["last_weekly_review_at"] = datetime.now().isoformat()
        save_stats(stats)

        print(f"✓ Delayed {args.delay}")
        print(f"  {item['title']} -> {args.until}")
        return

    now = datetime.now()
    cold_items = []

    for item in items.values():
        touched = item.get("last_touched_at") or item.get("created_at")
        try:
            age_days = (now - datetime.fromisoformat(touched)).total_seconds() / 86400
            if age_days >= 30 and item.get("status") in ["todo", "in_progress", "waiting", "inbox"]:
                cold_items.append(item)
        except ValueError:
            continue

    if not cold_items:
        print("No cold items need special attention this week.")
    else:
        print("These items have been cold for 30+ days:")
        print("You can reactivate them, delay them to next month, archive them, or let them go.")
        print("Clearing them is not failure. It is how you make room for what matters now.")
        print()
        for item in cold_items[:10]:
            print(f"- {item['id']} | {item['title']} | status={item['status']}")

    stats = load_stats()
    stats["last_weekly_review_at"] = datetime.now().isoformat()
    save_stats(stats)

if __name__ == "__main__":
    main()
