#!/usr/bin/env python3
"""
Smart Reminder Task State Manager

Deterministic JSON state management for smart-reminder tasks.
Actions: create, read, update-completion, delete, list, reset-week, config

Usage:
  python manage_tasks.py create <name> <cron_expr> <personality> [totalSessions] [channel] [sessionKey]
  python manage_tasks.py read <task_id>
  python manage_tasks.py list
  python manage_tasks.py complete <task_id> [true|false]
  python manage_tasks.py update <task_id> <field> <value>
  python manage_tasks.py delete <task_id>
  python manage_tasks.py reset-week
  python manage_tasks.py set-nickname <nickname>
  python manage_tasks.py get-nickname
  python manage_tasks.py config
"""

import json
import os
import sys
import uuid
from datetime import datetime, timezone, timedelta

STATE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "memory")
STATE_FILE = os.path.join(STATE_DIR, "smart-reminder-tasks.json")

def _ensure_state():
    os.makedirs(STATE_DIR, exist_ok=True)
    if not os.path.exists(STATE_FILE):
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"config": {}, "tasks": {}}, f, ensure_ascii=False, indent=2)
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        state = json.load(f)
    if "config" not in state:
        state["config"] = {}
    if "tasks" not in state:
        state["tasks"] = {}
    return state

def _save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def _short_id():
    return uuid.uuid4().hex[:8]

def _get_monday():
    now = datetime.now(timezone.utc) + timedelta(hours=8)
    monday = now - timedelta(days=now.weekday())
    return monday.strftime("%Y-%m-%d")

def _now_iso():
    now = datetime.now(timezone.utc) + timedelta(hours=8)
    return now.strftime("%Y-%m-%dT%H:%M:%S+08:00")

def cmd_create(args):
    if len(args) < 3:
        print("Usage: create <name> <cron_expr> <personality> [totalSessions] [channel] [sessionKey]")
        sys.exit(1)
    name = args[0]
    cron_expr = args[1]
    personality = args[2]
    total_sessions = int(args[3]) if len(args) > 3 and args[3] else None
    channel = args[4] if len(args) > 4 else None
    session_key = args[5] if len(args) > 5 else None
    state = _ensure_state()
    task_id = f"task_{_short_id()}"
    task = {
        "id": task_id,
        "name": name,
        "schedule": {"type": "cron", "expression": cron_expr, "tz": "Asia/Shanghai"},
        "personality": personality,
        "createdAt": _now_iso(),
        "enabled": True
    }
    if channel and session_key:
        task["delivery"] = {"channel": channel, "sessionKey": session_key}
    if total_sessions and total_sessions > 1:
        task["tracking"] = {
            "totalSessions": total_sessions,
            "completedSessions": 0,
            "weekStart": _get_monday(),
            "history": [],
            "sinceLastCompletion": 0
        }
    state["tasks"][task_id] = task
    _save_state(state)
    print(json.dumps(task, ensure_ascii=False, indent=2))
    return task_id

def cmd_read(args):
    if not args:
        print("Usage: read <task_id>")
        sys.exit(1)
    state = _ensure_state()
    task = state["tasks"].get(args[0])
    if not task:
        print(f"Task '{args[0]}' not found")
        sys.exit(1)
    print(json.dumps(task, ensure_ascii=False, indent=2))

def cmd_list(_):
    state = _ensure_state()
    if not state["tasks"]:
        print("No tasks.")
        return
    for tid, t in state["tasks"].items():
        tracking = ""
        if "tracking" in t:
            tr = t["tracking"]
            tracking = f" [{tr['completedSessions']}/{tr['totalSessions']}]"
        status = "✅" if t["enabled"] else "⏸️"
        print(f"  {status} {tid}: {t['name']} ({t['personality']}) {t['schedule']['expression']}{tracking}")

def cmd_complete(args):
    if len(args) < 2:
        print("Usage: complete <task_id> true|false")
        sys.exit(1)
    task_id, completed_str = args[0], args[1].lower()
    completed = completed_str == "true"
    state = _ensure_state()
    task = state["tasks"].get(task_id)
    if not task:
        print(f"Task '{task_id}' not found")
        sys.exit(1)
    today = _get_monday()
    if "tracking" not in task:
        if "history" not in task:
            task["history"] = []
        task["history"].append({"date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "completed": completed})
        _save_state(state)
        print(f"Logged {'completion' if completed else 'skip'} for single task {task_id}")
        return
    if task["tracking"]["weekStart"] != today:
        task["tracking"]["weekStart"] = today
        task["tracking"]["completedSessions"] = 0
        task["tracking"]["history"] = []
    if completed:
        task["tracking"]["completedSessions"] += 1
        task["tracking"]["sinceLastCompletion"] = 0
    else:
        task["tracking"]["sinceLastCompletion"] += 1
    task["tracking"]["history"].append({"date": _now_iso(), "completed": completed})
    _save_state(state)
    print(f"Updated {task_id}: completed={completed}, "
          f"progress={task['tracking']['completedSessions']}/{task['tracking']['totalSessions']}, "
          f"streakMissed={task['tracking']['sinceLastCompletion']}")

def cmd_update(args):
    if len(args) < 3:
        print("Usage: update <task_id> <field> <value>")
        sys.exit(1)
    task_id, field, value = args[0], args[1], args[2]
    state = _ensure_state()
    task = state["tasks"].get(task_id)
    if not task:
        print(f"Task '{task_id}' not found")
        sys.exit(1)
    if field in ("personality", "name", "enabled"):
        if field == "enabled":
            value = value.lower() == "true"
        task[field] = value
        _save_state(state)
        print(f"Updated {task_id}.{field} = {value}")
    else:
        print(f"Field '{field}' not updatable via CLI")

def cmd_delete(args):
    if not args:
        print("Usage: delete <task_id>")
        sys.exit(1)
    state = _ensure_state()
    if args[0] in state["tasks"]:
        del state["tasks"][args[0]]
        _save_state(state)
        print(f"Deleted {args[0]}")
    else:
        print(f"Task '{args[0]}' not found")

def cmd_reset_week(_):
    state = _ensure_state()
    today = _get_monday()
    count = 0
    for tid, task in state["tasks"].items():
        if "tracking" in task and task["tracking"]["weekStart"] != today:
            task["tracking"]["weekStart"] = today
            task["tracking"]["completedSessions"] = 0
            task["tracking"]["history"] = []
            count += 1
    if count:
        _save_state(state)
    print(f"Reset {count} tasks to week {today}")

def cmd_set_nickname(args):
    if not args:
        print("Usage: set-nickname <nickname>")
        sys.exit(1)
    state = _ensure_state()
    state["config"]["nickname"] = args[0]
    _save_state(state)
    print(f"Nickname set to: {args[0]}")

def cmd_get_nickname(_):
    state = _ensure_state()
    nick = state["config"].get("nickname")
    print(nick if nick else "(none)")

def cmd_config(_):
    state = _ensure_state()
    print(json.dumps(state["config"], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    commands = {
        "create": cmd_create,
        "read": cmd_read,
        "list": cmd_list,
        "complete": cmd_complete,
        "update": cmd_update,
        "delete": cmd_delete,
        "reset-week": cmd_reset_week,
        "set-nickname": cmd_set_nickname,
        "get-nickname": cmd_get_nickname,
        "config": cmd_config,
    }
    if cmd in commands:
        commands[cmd](args)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
