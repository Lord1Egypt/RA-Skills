#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_items, save_items, load_stats, save_stats

VALID_STATUS = ["todo", "in_progress", "waiting", "blocked", "done", "inbox"]

def main():
    parser = argparse.ArgumentParser(description="Update an existing item")
    parser.add_argument("--id", required=True, help="Item ID")
    parser.add_argument("--status", choices=VALID_STATUS)
    parser.add_argument("--notes")
    parser.add_argument("--hot_score", type=int)
    args = parser.parse_args()

    data = load_items()
    items = data.get("items", {})

    if args.id not in items:
        print(f"Item not found: {args.id}")
        sys.exit(1)

    item = items[args.id]
    old_status = item.get("status")

    if args.status:
        item["status"] = args.status
    if args.notes is not None:
        item["notes"] = args.notes
    if args.hot_score is not None:
        item["hot_score"] = max(0, min(100, args.hot_score))

    item["updated_at"] = datetime.now().isoformat()
    item["last_touched_at"] = datetime.now().isoformat()

    save_items(data)

    if old_status != "done" and item.get("status") == "done":
        stats = load_stats()
        stats["total_items_completed"] += 1
        stats["total_weight_released"] += int(item.get("cognitive_weight", 0))
        stats["total_minutes_completed"] += int(item.get("duration_mins") or 0)
        if item.get("type") == "commitment":
            stats["total_commitments_fulfilled"] += 1
        save_stats(stats)

    print(f"✓ Updated {args.id}")
    print(f"  Status: {item.get('status')}")

if __name__ == "__main__":
    main()
