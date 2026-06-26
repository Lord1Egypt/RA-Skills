#!/usr/bin/env python3
from datetime import datetime
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_items, load_stats, save_stats

def main():
    items_data = load_items()
    stats = load_stats()

    items = list(items_data.get("items", {}).values())
    done_today = []

    today = datetime.now().date()
    for item in items:
        updated_at = item.get("updated_at")
        if item.get("status") == "done" and updated_at:
            try:
                if datetime.fromisoformat(updated_at).date() == today:
                    done_today.append(item)
            except ValueError:
                pass

    done_count = len(done_today)
    weight_today = sum(int(x.get("cognitive_weight", 0)) for x in done_today)
    minutes_today = sum(int(x.get("duration_mins") or 0) for x in done_today)

    print(f"Today you completed {done_count} item(s) and released {weight_today} unit(s) of mental weight.")
    print(f"Time cleared today: {minutes_today} min")
    print(f"Lifetime mental weight released: {stats.get('total_weight_released', 0)}")
    print()

    remaining = [x for x in items if x.get("status") in ["todo", "in_progress", "waiting"]]
    if remaining:
        print("Still in motion:")
        for item in remaining[:3]:
            print(f"- {item['title']} ({item['status']})")

    stats["last_daily_sync_at"] = datetime.now().isoformat()
    save_stats(stats)

if __name__ == "__main__":
    main()
