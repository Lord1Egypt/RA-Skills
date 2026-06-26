#!/usr/bin/env python3
"""
Synapse Brain — Session Init
初始化新 Session 或恢复已有 Session。

Usage:
    python session_init.py new <project> <title>
    python session_init.py resume <project>
    python session_init.py auto <project>  # auto: resume if exists, else create
"""

import json
import os
import sys
from datetime import datetime, timezone

# Import state_manager functions
sys.path.insert(0, os.path.dirname(__file__))
from state_manager import create, status, _load, _ensure_state_dir


def resume(project: str) -> dict | None:
    """Resume an existing session."""
    state = _load(project)
    if not state:
        print(f"[brain] No session to resume for '{project}'.")
        return None

    # Check for interrupted tasks
    interrupted = [t for t in state["tasks"] if t["status"] == "in_progress"]
    if interrupted:
        print(f"[brain] Found {len(interrupted)} interrupted task(s):")
        for t in interrupted:
            print(f"  ⏸️ {t['id']}: {t['title']}")
        # Mark as waiting for user confirmation
        for t in interrupted:
            t["status"] = "interrupted"
            t["interrupted_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    print(f"\n🧠 Session resumed: {project}")
    status(project)
    return state


def auto_init(project: str, title: str) -> dict:
    """Auto: resume if session exists, else create new."""
    existing = _load(project)
    if existing:
        return resume(project) or create(project, title)
    return create(project, title)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "new":
        if len(sys.argv) < 4:
            print("Usage: session_init.py new <project> <title>")
            sys.exit(1)
        create(sys.argv[2], sys.argv[3])
    elif cmd == "resume":
        if len(sys.argv) < 3:
            print("Usage: session_init.py resume <project>")
            sys.exit(1)
        resume(sys.argv[2])
    elif cmd == "auto":
        if len(sys.argv) < 3:
            print("Usage: session_init.py auto <project> [title]")
            sys.exit(1)
        title = sys.argv[3] if len(sys.argv) > 3 else "Untitled"
        auto_init(sys.argv[2], title)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
