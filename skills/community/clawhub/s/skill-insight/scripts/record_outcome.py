#!/usr/bin/env python3
# record_outcome.py - Update the outcome of a previously recorded skill invocation
# Usage: python3 record_outcome.py <record_id> <success|failed|skipped> [notes]
#
# Examples:
#   python3 record_outcome.py rec-123456-abc4 success "completed successfully"
#   python3 record_outcome.py rec-123456-abc4 failed "API timeout after 30s"
#
# Also supports updating by skill name + scene (latest matching record):
#   python3 record_outcome.py --skill <name> --scene <scene> <outcome> [notes]

import json
import sys
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path; import sys; sys.path.insert(0, str(Path(__file__).parent))
from path_utils import get_usage_file

GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
CYAN = '\033[0;36m'
NC = '\033[0m'

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_by_id(usage_data, record_id, outcome, notes):
    """Update a specific record by its ID."""
    for r in usage_data["records"]:
        if r.get("id") == record_id:
            r["outcome"] = outcome
            if notes:
                r["notes"] = notes
            r["_outcome_updated_at"] = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%dT%H:%M:%S+08:00")
            return True, r.get("skill"), record_id
    return False, None, None

def update_by_skill_scene(usage_data, skill_name, scene_pattern, outcome, notes):
    """Update the latest record matching skill name and scene pattern."""
    found = None
    for r in reversed(usage_data["records"]):  # latest first
        if r.get("skill") == skill_name and scene_pattern.lower() in r.get("scene", "").lower():
            found = r
            break
    if found:
        found["outcome"] = outcome
        if notes:
            found["notes"] = notes
        found["_outcome_updated_at"] = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%dT%H:%M:%S+08:00")
        return True, found.get("skill"), found.get("id")
    return False, None, None

def main():
    parser = argparse.ArgumentParser(description="Update the outcome of a recorded skill invocation")
    parser.add_argument('--skill', type=str, help="Skill name (use with --scene)")
    parser.add_argument('--scene', type=str, help="Scene pattern to match")
    parser.add_argument('outcome', nargs='?', help="Outcome: success | failed | skipped")
    parser.add_argument('notes', nargs='?', help="Optional notes")
    args = parser.parse_args()

    if args.outcome not in ("success", "failed", "skipped", None):
        print(f"{RED}Error: outcome must be 'success', 'failed', or 'skipped'{NC}")
        print(f"Usage: python3 record_outcome.py <record_id> <outcome> [notes]")
        print(f"   or: python3 record_outcome.py --skill <name> --scene <pattern> <outcome> [notes]")
        sys.exit(1)

    usage_file = get_usage_file()
    usage_data = load_json(usage_file)
    if not usage_data:
        print(f"{RED}Error: usage data not found at {usage_file}{NC}")
        sys.exit(1)

    updated = False
    skill = None
    record_id = None

    if args.skill and args.scene and args.outcome:
        updated, skill, record_id = update_by_skill_scene(
            usage_data, args.skill, args.scene, args.outcome, args.notes or ""
        )
    elif len(sys.argv) >= 3 and not args.skill:
        # Positional: record_id outcome [notes]
        record_id = sys.argv[1]
        outcome = sys.argv[2]
        notes = sys.argv[3] if len(sys.argv) > 3 else ""
        updated, skill, record_id = update_by_id(usage_data, record_id, outcome, notes)
    else:
        print(f"{RED}Error: insufficient arguments{NC}")
        print(f"Usage: python3 record_outcome.py <record_id> <outcome> [notes]")
        print(f"   or: python3 record_outcome.py --skill <name> --scene <pattern> <outcome> [notes]")
        sys.exit(1)

    if updated:
        save_json(usage_file, usage_data)
        emoji = {"success": "📗", "failed": "📕", "skipped": "📙"}.get(args.outcome, "📋")
        print(f"{GREEN}✓ Outcome updated: {emoji} {skill} — {args.outcome}{NC}")
        print(f"  Record ID: {record_id}")
        if args.notes:
            print(f"  Notes: {args.notes}")
    else:
        print(f"{RED}✗ Record not found: {record_id or f'skill={args.skill}, scene={args.scene}'}{NC}")
        sys.exit(1)

if __name__ == "__main__":
    main()
