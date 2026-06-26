#!/usr/bin/env python3
# add_skill.py - Add or update a skill in the registry
# Usage: python3 add_skill.py <name> <category> <description> [installed]

import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from path_utils import get_registry_file, get_sample_registry_file, get_skill_dir

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
    if len(sys.argv) < 4:
        print("Usage: python3 add_skill.py <name> <category> <description> [installed]")
        sys.exit(1)

    name = sys.argv[1]
    category = sys.argv[2]
    desc = sys.argv[3]
    installed = sys.argv[4].lower() == "true" if len(sys.argv) > 4 else True

    registry_file = get_registry_file()
    data = load_json(registry_file)

    if data is None:
        # First run: check if sample data exists to initialize
        sample_file = get_sample_registry_file()
        sample_data = load_json(sample_file)
        if sample_data:
            data = sample_data
            print(f"Initializing registry from sample data...")
        else:
            data = {"schema": "skill_usage_tracker:v1", "last_updated": "", "skills": []}
            print(f"Creating new registry at {registry_file}")

    found = False
    for s in data.get("skills", []):
        if s["name"] == name:
            s["category"] = category
            s["description"] = desc
            s["installed"] = installed
            s["last_updated"] = "2026-03-28"
            found = True
            print(f"Updated existing skill: {name}")
            break

    if not found:
        data.setdefault("skills", []).append({
            "name": name,
            "installed": installed,
            "category": category,
            "description": desc,
            "use_cases": [],
            "install_date": "2026-03-28",
            "last_updated": "2026-03-28",
            "tags": [],
            "access_type": "route"  # default
        })
        print(f"Added new skill: {name}")

    data["last_updated"] = "2026-03-28T00:00:00+08:00"
    save_json(registry_file, data)
    print(f"Registry updated: {registry_file}")

if __name__ == "__main__":
    main()
