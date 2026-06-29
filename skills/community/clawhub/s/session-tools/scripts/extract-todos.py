#!/usr/bin/env python3
"""
Todo extractor - extracts TodoWrite items from a Claude session JSONL file.

Usage:
  extract-todos.py <project_name> <session_id> [--all]

Options:
  --all     Show all todo snapshots (not just the last one)

Output format:
  [completed] task content
  [in_progress] in-progress task
  [pending] pending task
"""

import json
import sys
from pathlib import Path


def extract_todos(project_name: str, session_id: str, show_all: bool = False):
    session_file = Path.home() / ".claude" / "projects" / project_name / f"{session_id}.jsonl"

    if not session_file.exists():
        print(f"Error: Session file not found: {session_file}", file=sys.stderr)
        sys.exit(1)

    snapshots = []

    with open(session_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if obj.get("type") != "assistant":
                    continue
                content = obj.get("message", {}).get("content", [])
                if not isinstance(content, list):
                    continue
                for item in content:
                    if (
                        isinstance(item, dict)
                        and item.get("type") == "tool_use"
                        and item.get("name") == "TodoWrite"
                    ):
                        todos = item.get("input", {}).get("todos", [])
                        if todos:
                            snapshots.append(todos)
            except (json.JSONDecodeError, Exception):
                continue

    if not snapshots:
        print("No TodoWrite items found in this session.")
        return

    if show_all:
        for i, snapshot in enumerate(snapshots, 1):
            print(f"\n--- Snapshot {i}/{len(snapshots)} ---")
            print_todos(snapshot)
    else:
        # Last snapshot (most recent state)
        print_todos(snapshots[-1])


def print_todos(todos: list):
    order = {"completed": 0, "in_progress": 1, "pending": 2}
    sorted_todos = sorted(todos, key=lambda t: order.get(t.get("status", "pending"), 3))

    for todo in sorted_todos:
        status = todo.get("status", "pending")
        content = todo.get("content", "")
        print(f"[{status}] {content}")


def main():
    if len(sys.argv) < 3:
        print("Usage: extract-todos.py <project_name> <session_id> [--all]")
        sys.exit(1)

    project_name = sys.argv[1]
    session_id = sys.argv[2]
    show_all = "--all" in sys.argv

    extract_todos(project_name, session_id, show_all)


if __name__ == "__main__":
    main()
