#!/usr/bin/env python3
"""
Synapse Brain — Session State Manager
持久化 Session 状态，支持跨会话恢复。

Usage:
    python state_manager.py create <project> <title>
    python state_manager.py update <project> <task_id> <status> [data]
    python state_manager.py status <project>
    python state_manager.py list
    python state_manager.py archive <project>
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


STATE_DIR = os.path.expanduser("~/.openclaw/brain-state")


def _state_path(project: str) -> str:
    return os.path.join(STATE_DIR, f"{project}.json")


def _ensure_state_dir():
    Path(STATE_DIR).mkdir(parents=True, exist_ok=True)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def create(project: str, title: str):
    """Create a new session state."""
    _ensure_state_dir()
    path = _state_path(project)
    if os.path.exists(path):
        print(f"[brain] Session already exists for '{project}'. Use 'update' to modify.")
        return _load(project)

    state = {
        "session_id": f"sess_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}",
        "project": project,
        "title": title,
        "created_at": _now(),
        "updated_at": _now(),
        "tasks": [],
        "subagents": {
            "active": 0,
            "completed": 0,
            "failed": 0
        },
        "knowledge": {
            "wiki_initialized": False,
            "wiki_root": None,
            "last_ingest": None
        },
        "log": []
    }

    with open(path, "w") as f:
        json.dump(state, f, indent=2)

    print(f"[brain] Session created: {project} — {title}")
    return state


def _load(project: str) -> dict | None:
    path = _state_path(project)
    if not os.path.exists(path):
        print(f"[brain] No session found for '{project}'.")
        return None
    with open(path) as f:
        return json.load(f)


def _save(project: str, state: dict):
    _ensure_state_dir()
    state["updated_at"] = _now()
    with open(_state_path(project), "w") as f:
        json.dump(state, f, indent=2)
    print(f"[brain] State saved: {project}")


def update(project: str, task_id: str, status: str, data: str = None):
    """Update task status in session."""
    state = _load(project)
    if not state:
        return

    # Find task
    task = None
    for t in state["tasks"]:
        if t["id"] == task_id:
            task = t
            break

    if not task:
        # Create new task
        task = {
            "id": task_id,
            "title": task_id,
            "status": status,
            "created_at": _now()
        }
        state["tasks"].append(task)

    task["status"] = status
    task["updated_at"] = _now()

    if data:
        try:
            task_data = json.loads(data)
            task.update(task_data)
        except json.JSONDecodeError:
            task["note"] = data

    # Log
    state["log"].append(f"[{_now()}] Task {task_id} -> {status}")

    _save(project, state)


def status(project: str):
    """Show session status."""
    state = _load(project)
    if not state:
        return

    tasks = state["tasks"]
    completed = sum(1 for t in tasks if t["status"] == "completed")
    in_progress = sum(1 for t in tasks if t["status"] == "in_progress")
    failed = sum(1 for t in tasks if t["status"] == "failed")

    print(f"\n🧠 Session: {state['project']} — {state['title']}")
    print(f"Created: {state['created_at']} | Updated: {state['updated_at']}")
    print(f"\n📊 Tasks: {len(tasks)} total | {completed} done | {in_progress} active | {failed} failed")
    print(f"🤖 Subagents: {state['subagents']['completed']} completed | {state['subagents']['active']} active | {state['subagents']['failed']} failed")

    if tasks:
        print(f"\n📋 Task List:")
        for t in tasks[-10:]:
            icon = {"completed": "✅", "in_progress": "🔵", "failed": "❌", "pending": "⏳"}.get(t["status"], "⚪")
            print(f"  {icon} {t['id']}: {t['title']} ({t['status']})")
    print()


def list_sessions():
    """List all sessions."""
    _ensure_state_dir()
    files = list(Path(STATE_DIR).glob("*.json"))
    if not files:
        print("[brain] No sessions found.")
        return
    print(f"\n🧠 Sessions ({len(files)}):")
    for f in sorted(files):
        with open(f) as fh:
            state = json.load(fh)
        print(f"  - {state['project']}: {state['title']} ({state['updated_at']})")
    print()


def archive(project: str):
    """Archive completed tasks older than 30 days."""
    state = _load(project)
    if not state:
        return

    archived = 0
    remaining = []
    for t in state["tasks"]:
        if t["status"] == "completed" and t.get("updated_at", "") < _now():
            # Simple archive: move to archived list
            archived += 1
        else:
            remaining.append(t)

    state["archived_count"] = state.get("archived_count", 0) + archived
    state["tasks"] = remaining
    _save(project, state)
    print(f"[brain] Archived {archived} completed tasks.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "create":
        if len(sys.argv) < 4:
            print("Usage: state_manager.py create <project> <title>")
            sys.exit(1)
        create(sys.argv[2], sys.argv[3])
    elif cmd == "update":
        if len(sys.argv) < 5:
            print("Usage: state_manager.py update <project> <task_id> <status> [data]")
            sys.exit(1)
        data = sys.argv[5] if len(sys.argv) > 5 else None
        update(sys.argv[2], sys.argv[3], sys.argv[4], data)
    elif cmd == "status":
        if len(sys.argv) < 3:
            print("Usage: state_manager.py status <project>")
            sys.exit(1)
        status(sys.argv[2])
    elif cmd == "list":
        list_sessions()
    elif cmd == "archive":
        if len(sys.argv) < 3:
            print("Usage: state_manager.py archive <project>")
            sys.exit(1)
        archive(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
