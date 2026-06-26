#!/usr/bin/env python3
import argparse
import os
import sys
import uuid
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_items, save_items, load_stats, save_stats
from lib.scoring import calculate_cognitive_weight

VALID_TYPES = ["task", "project", "commitment", "follow_up", "reminder"]
VALID_STATUS = ["todo", "in_progress", "waiting", "blocked", "done", "inbox"]
VALID_ENERGY = ["low", "medium", "high"]

def parse_csv(value):
    if not value:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]

def main():
    parser = argparse.ArgumentParser(description="Capture a new item")
    parser.add_argument("--title", required=True, help="Short title")
    parser.add_argument("--type", choices=VALID_TYPES, default="task")
    parser.add_argument("--status", choices=VALID_STATUS, default="todo")
    parser.add_argument("--energy", choices=VALID_ENERGY, default="medium")
    parser.add_argument("--tiny", action="store_true", help="2-5 minute low-friction task")
    parser.add_argument("--do_date", help="Planned date YYYY-MM-DD")
    parser.add_argument("--deadline", help="Must finish by YYYY-MM-DD")
    parser.add_argument("--duration_mins", type=int, help="Estimated duration")
    parser.add_argument("--project", help="Project ID or label")
    parser.add_argument("--depends_on", help="Comma-separated IDs")
    parser.add_argument("--waiting_for", help="Who/what this is waiting for")
    parser.add_argument("--commitment_to", help="Person/entity this commitment is for")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--notes", default="", help="Extra notes")

    args = parser.parse_args()

    now = datetime.now().isoformat()
    prefix_map = {
        "task": "TSK",
        "project": "PRJ",
        "commitment": "COM",
        "follow_up": "FLW",
        "reminder": "REM"
    }
    item_id = f"{prefix_map[args.type]}-{str(uuid.uuid4())[:4].upper()}"

    cognitive_weight = calculate_cognitive_weight(args.type, args.energy, args.tiny)

    item = {
        "id": item_id,
        "title": args.title,
        "type": args.type,
        "status": args.status,
        "created_at": now,
        "updated_at": now,
        "last_touched_at": now,
        "deadline": args.deadline,
        "do_date": args.do_date,
        "start_after": None,
        "energy": args.energy,
        "duration_mins": args.duration_mins,
        "tiny": bool(args.tiny),
        "project": args.project,
        "depends_on": parse_csv(args.depends_on),
        "waiting_for": args.waiting_for,
        "commitment_to": args.commitment_to,
        "hot_score": 100,
        "temperature": "hot",
        "cognitive_weight": cognitive_weight,
        "notes": args.notes,
        "tags": parse_csv(args.tags)
    }

    data = load_items()
    data["items"][item_id] = item
    save_items(data)

    stats = load_stats()
    stats["total_items_created"] += 1
    if args.type == "project":
        stats["total_projects_created"] += 1
    save_stats(stats)

    print(f"✅ Item Captured: [{item_id}]")
    print(f"   Title: {args.title}")
    print(f"   Type: {args.type}")
    print(f"   Mental weight offloaded: {cognitive_weight} units.")

if __name__ == "__main__":
    main()
