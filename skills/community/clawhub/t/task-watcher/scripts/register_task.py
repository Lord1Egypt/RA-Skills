#!/usr/bin/env python3
"""CLI tool to register a monitoring task with the watcher."""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

from models import CallbackTask, TaskState
from stores import JsonlTaskStore

DEFAULT_TASKS_FILE = os.path.expanduser(
    "~/.openclaw/shared-context/monitor-tasks/tasks.jsonl"
)


def main():
    parser = argparse.ArgumentParser(description="Register a monitoring task")
    parser.add_argument("--task-id", required=True, help="Unique task ID")
    parser.add_argument("--system", required=True, help="Target system (e.g., xiaohongshu, github)")
    parser.add_argument("--adapter", default="", help="Adapter name (auto-detected if empty)")
    parser.add_argument("--object-id", required=True, help="Target object ID (note_id, PR number, etc.)")
    parser.add_argument("--owner", default="main", help="Owner agent ID")
    parser.add_argument("--channel", default="discord", help="Reply channel")
    parser.add_argument("--reply-to", default="", help="Reply target (e.g., channel:ID)")
    parser.add_argument("--state", default="submitted", help="Initial state")
    parser.add_argument("--expires-hours", type=int, default=6, help="Hours until timeout")
    parser.add_argument("--tasks-file", default=DEFAULT_TASKS_FILE, help="Tasks JSONL file path")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    store = JsonlTaskStore(args.tasks_file)

    task = CallbackTask(
        task_id=args.task_id,
        owner_agent=args.owner,
        target_system=args.system,
        adapter=args.adapter,
        target_object_id=args.object_id,
        reply_channel=args.channel,
        reply_to=args.reply_to,
        current_state=args.state,
        expires_at=(datetime.now() + timedelta(hours=args.expires_hours)).isoformat(),
    )

    store.create(task)

    if args.json:
        print(json.dumps(task.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"Registered: {task.task_id}")
        print(f"  system: {task.target_system}")
        print(f"  object: {task.target_object_id}")
        print(f"  state: {task.current_state}")
        print(f"  expires: {task.expires_at}")


if __name__ == "__main__":
    main()
