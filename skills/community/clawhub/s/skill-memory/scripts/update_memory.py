#!/usr/bin/env python3
"""
Skill Memory Update Script
技能记忆更新脚本

Usage:
  python update_memory.py --task "任务类型" --skill "技能名称" --params '{"key":"value"}' --scenario "场景描述"
  python update_memory.py --list
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

# Memory file location
MEMORY_FILE = Path(__file__).parent.parent / "references" / "memory.json"

def load_memory():
    """Load memory from file"""
    if not MEMORY_FILE.exists():
        return {"skills": [], "version": "1.0.0", "updated_at": None}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    """Save memory to file"""
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    memory["updated_at"] = datetime.now().isoformat()
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def find_entry(memory, task_type):
    """Find entry by task type"""
    for i, entry in enumerate(memory["skills"]):
        if entry["task_type"] == task_type:
            return i, entry
    return -1, None

def record_or_update(task_type, skill, params, scenario):
    """Record new entry or update existing one"""
    memory = load_memory()
    idx, entry = find_entry(memory, task_type)

    now = datetime.now().isoformat()

    if entry:
        # Entry exists, check if needs update
        needs_update = False

        # Check if params or scenario changed
        current_params = json.dumps(entry.get("parameters", {}), sort_keys=True)
        new_params = json.dumps(params, sort_keys=True)

        if current_params != new_params:
            entry["parameters"] = params
            needs_update = True

        if entry.get("scenario") != scenario:
            entry["scenario"] = scenario
            needs_update = True

        if needs_update:
            entry["updated_at"] = now
            print(f"✓ Updated: {task_type}")
        else:
            print(f"= No change: {task_type}")

        # Always increment usage count
        entry["usage_count"] = entry.get("usage_count", 0) + 1
        memory["skills"][idx] = entry
    else:
        # New entry
        new_entry = {
            "task_type": task_type,
            "skill": skill,
            "parameters": params,
            "scenario": scenario,
            "created_at": now,
            "updated_at": None,
            "usage_count": 1
        }
        memory["skills"].append(new_entry)
        print(f"+ Recorded: {task_type}")

    save_memory(memory)

def list_memory():
    """List all memory entries"""
    memory = load_memory()

    if not memory["skills"]:
        print("No skill memory entries yet.")
        return

    print(f"\n{'='*60}")
    print(f"Skill Memory (v{memory.get('version', '1.0.0')})")
    print(f"Last Updated: {memory.get('updated_at', 'N/A')}")
    print(f"{'='*60}\n")

    for i, entry in enumerate(memory["skills"], 1):
        print(f"[{i}] {entry['task_type']}")
        print(f"    Skill: {entry['skill']}")
        print(f"    Scenario: {entry.get('scenario', 'N/A')}")
        print(f"    Params: {json.dumps(entry.get('parameters', {}), ensure_ascii=False)}")
        print(f"    Usage: {entry.get('usage_count', 0)} times")
        if entry.get('updated_at'):
            print(f"    Updated: {entry['updated_at']}")
        else:
            print(f"    Created: {entry.get('created_at', 'N/A')}")
        print()

def main():
    parser = argparse.ArgumentParser(description="Skill Memory Update Tool")
    parser.add_argument("--task", "-t", help="Task type (任务类型)")
    parser.add_argument("--skill", "-s", help="Skill name (技能名称)")
    parser.add_argument("--params", "-p", default="{}", help="JSON parameters (参数JSON)")
    parser.add_argument("--scenario", "-c", default="", help="Usage scenario (使用场景)")
    parser.add_argument("--list", "-l", action="store_true", help="List all entries (列出所有记忆)")

    args = parser.parse_args()

    if args.list:
        list_memory()
        return

    if not args.task or not args.skill:
        print("Error: --task and --skill are required")
        print("Example: python update_memory.py --task '分析图片' --skill 'doubao-api-toolkit'")
        return

    try:
        params = json.loads(args.params)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON for --params: {args.params}")
        return

    record_or_update(args.task, args.skill, params, args.scenario)

if __name__ == "__main__":
    main()
