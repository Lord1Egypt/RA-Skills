#!/usr/bin/env python3
# record.py - Record a skill invocation
# Usage: python3 record.py <skill_name> [scene] [outcome] [notes]

import json
import sys
import uuid
from datetime import datetime, timezone, timedelta

# Dynamic path resolution — works regardless of install location
from pathlib import Path; import sys; sys.path.insert(0, str(Path(__file__).parent))
from path_utils import get_usage_file, get_registry_file

GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
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

def main():
    if len(sys.argv) < 2:
        print(f"{RED}Error: skill name is required{NC}")
        print("Usage: python3 record.py <skill_name> [scene] [outcome] [notes]")
        sys.exit(1)

    skill_name = sys.argv[1]
    scene = sys.argv[2] if len(sys.argv) > 2 else "unknown"
    outcome = sys.argv[3] if len(sys.argv) > 3 else "success"
    notes = sys.argv[4] if len(sys.argv) > 4 else ""

    registry_file = get_registry_file()
    registry_data = load_json(registry_file)
    if registry_data:
        skill_names = {s["name"] for s in registry_data.get("skills", [])}
        if skill_name not in skill_names:
            print(f"{YELLOW}Warning: '{skill_name}' not found in {registry_file}{NC}")
            print(f"Add it with: bash add_skill.sh {skill_name} <category> <description>")

    usage_file = get_usage_file()
    usage_data = load_json(usage_file) or {"schema": "skill_usage_log:v1", "last_updated": "", "records": []}

    record_id = f"rec-{int(datetime.now().timestamp())}-{str(uuid.uuid4())[:4]}"
    timestamp = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%dT%H:%M:%S+08:00")

    new_entry = {
        "id": record_id,
        "skill": skill_name,
        "timestamp": timestamp,
        "scene": scene,
        "outcome": outcome,
        "notes": notes
    }

    usage_data["records"].append(new_entry)
    usage_data["last_updated"] = timestamp
    save_json(usage_file, usage_data)

    print(f"{GREEN}✓ Skill invocation recorded{NC}")
    print(f"  Skill: {skill_name}")
    print(f"  Scene: {scene}")
    print(f"  Time:  {timestamp}")
    print(f"  ID:    {record_id}")
    print(f"  Data:  {usage_file}")

if __name__ == "__main__":
    main()
