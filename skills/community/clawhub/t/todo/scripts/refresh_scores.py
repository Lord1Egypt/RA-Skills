#!/usr/bin/env python3
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_items, save_items
from lib.scoring import calculate_hot_score, calculate_temperature

def main():
    data = load_items()
    items = data.get("items", {})

    updated = 0
    for item in items.values():
        created_at = item.get("created_at")
        last_touched_at = item.get("last_touched_at") or created_at
        if not created_at:
            continue

        try:
            item["hot_score"] = calculate_hot_score(created_at, last_touched_at)
            item["temperature"] = calculate_temperature(created_at, last_touched_at)
            item["updated_at"] = datetime.now().isoformat()
            updated += 1
        except ValueError:
            continue

    save_items(data)
    print(f"✓ Refreshed scores for {updated} item(s)")

if __name__ == "__main__":
    main()
