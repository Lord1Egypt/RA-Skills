#!/usr/bin/env python3
import json
import os
from datetime import datetime

TODO_DIR = os.path.expanduser("~/.openclaw/workspace/memory/todo")
ITEMS_FILE = os.path.join(TODO_DIR, "items.json")
STATS_FILE = os.path.join(TODO_DIR, "stats.json")
ARCHIVE_FILE = os.path.join(TODO_DIR, "archive.json")

def write_json_if_missing(path, payload):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

def main():
    os.makedirs(TODO_DIR, exist_ok=True)

    write_json_if_missing(ITEMS_FILE, {
        "metadata": {
            "version": "3.0.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        },
        "items": {}
    })

    write_json_if_missing(STATS_FILE, {
        "total_items_created": 0,
        "total_items_completed": 0,
        "total_items_archived": 0,
        "total_projects_created": 0,
        "total_commitments_fulfilled": 0,
        "total_weight_released": 0,
        "total_minutes_completed": 0,
        "last_daily_sync_at": None,
        "last_weekly_review_at": None
    })

    write_json_if_missing(ARCHIVE_FILE, {
        "metadata": {
            "version": "3.0.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        },
        "items": {}
    })

    print("✓ Todo storage initialized")
    print(f"  {ITEMS_FILE}")
    print(f"  {STATS_FILE}")
    print(f"  {ARCHIVE_FILE}")

if __name__ == "__main__":
    main()
