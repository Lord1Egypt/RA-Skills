#!/usr/bin/env python3
"""
Checkpoint manager for session-continuity skill.

Usage:
    python checkpoint.py save <name> [--task <task-summary>]
    python checkpoint.py list
    python checkpoint.py resume <name>
    python checkpoint.py delete <name>
    python checkpoint.py auto
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace")))
CHECKPOINT_DIR = WORKSPACE / "memory" / "checkpoints"

COMMANDS = ["save", "list", "resume", "delete", "auto"]


def get_session_state():
    """Read current SESSION-STATE.md for progress capture."""
    state_file = WORKSPACE / "SESSION-STATE.md"
    if state_file.exists():
        return state_file.read_text()
    return ""


def checkpoint_exists(name: str) -> bool:
    return (CHECKPOINT_DIR / f"{name}.md").exists()


def save_checkpoint(name: str, task: str = "") -> None:
    """Save a named checkpoint from current SESSION-STATE.md and recent context."""
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = CHECKPOINT_DIR / f"{name}.md"

    session_state = get_session_state()
    now = datetime.now().strftime("%Y-%m-%d %H:%M GMT+8")

    content = f"""# Checkpoint: {name}

**Created:** {now}
**Task:** {task or "Unnamed task"}

## Progress
<!-- Describe what was completed in this session -->

## Next Action
<!-- Exact next step: which file, which command -->

## Blockers
<!-- Concrete obstacles: errors, conflicts, pending decisions -->

## Key Decisions
<!-- Reasoning that led to current state -->

## Relevant Context
<!-- Files, paths, preferences needed to continue -->
"""

    out_file.write_text(content)
    print(f"✅ Checkpoint saved: {name}")
    print(f"   Path: {out_file}")


def list_checkpoints() -> None:
    """List all available checkpoints."""
    if not CHECKPOINT_DIR.exists():
        print("No checkpoints found.")
        return

    checkpoints = sorted(CHECKPOINT_DIR.glob("*.md"))
    if not checkpoints:
        print("No checkpoints found.")
        return

    print(f"{'Name':<30} {'Modified':<25} {'Summary'}")
    print("-" * 80)
    for cp in checkpoints:
        stat = cp.stat()
        mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
        content = cp.read_text()
        # Extract task from first line after frontmatter
        task_line = ""
        for line in content.split("\n"):
            if line.startswith("**Task:**"):
                task_line = line.replace("**Task:**", "").strip()
                break
        age = get_age(stat.st_mtime)
        print(f"{cp.stem:<30} {mtime:<25} ({age}) {task_line}")


def get_age(timestamp: float) -> str:
    """Return human-readable age."""
    delta = datetime.now().timestamp() - timestamp
    if delta < 60:
        return "just now"
    elif delta < 3600:
        return f"{int(delta/60)}m ago"
    elif delta < 86400:
        return f"{int(delta/3600)}h ago"
    else:
        return f"{int(delta/86400)}d ago"


def resume_checkpoint(name: str) -> None:
    """Print checkpoint content for review before resumption."""
    cp_file = CHECKPOINT_DIR / f"{name}.md"
    if not cp_file.exists():
        print(f"ERROR: No checkpoint named '{name}'")
        sys.exit(1)

    content = cp_file.read_text()
    stat = cp_file.stat()
    age = get_age(stat.st_mtime)

    print("=" * 60)
    print(f"📌 Checkpoint: {name} ({age})")
    print("=" * 60)
    print(content)
    print("=" * 60)
    print("Run with confirmation to execute from this point.")


def delete_checkpoint(name: str) -> None:
    """Delete a named checkpoint."""
    if name == "autosave":
        print("ERROR: Cannot delete autosave. Use a named checkpoint.")
        sys.exit(1)

    cp_file = CHECKPOINT_DIR / f"{name}.md"
    if not cp_file.exists():
        print(f"ERROR: No checkpoint named '{name}'")
        sys.exit(1)

    cp_file.unlink()
    print(f"✅ Deleted: {name}")


def auto_checkpoint() -> None:
    """Save autosave checkpoint."""
    session_state = get_session_state()
    if not session_state.strip():
        print("Nothing to autosave (SESSION-STATE.md is empty).")
        return

    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = CHECKPOINT_DIR / "autosave.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M GMT+8")

    # Simple autosave: copy current SESSION-STATE.md content
    content = f"""# Autosave

**Created:** {now}
**Auto-saved:** True

{session_state}
"""
    out_file.write_text(content)

    # Log to autosave log
    log_file = CHECKPOINT_DIR / "autosave-log.md"
    log_entry = f"- [{now}] autosave written\n"
    if log_file.exists():
        log_file.write_text(log_file.read_text() + log_entry)
    else:
        log_file.write_text(f"# Autosave Log\n{log_entry}")

    print(f"✅ Autosave written")


def usage():
    print(__doc__)
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        usage()

    cmd = sys.argv[1]
    if cmd not in COMMANDS:
        print(f"Unknown command: {cmd}")
        usage()

    if cmd == "list":
        list_checkpoints()
    elif cmd == "auto":
        auto_checkpoint()
    elif len(sys.argv) < 3:
        print(f"ERROR: '{cmd}' requires a name argument")
        sys.exit(1)
    elif cmd == "save":
        name = sys.argv[2]
        task = ""
        if len(sys.argv) > 4 and sys.argv[3] == "--task":
            task = sys.argv[4]
        save_checkpoint(name, task)
    elif cmd == "resume":
        resume_checkpoint(sys.argv[2])
    elif cmd == "delete":
        delete_checkpoint(sys.argv[2])


if __name__ == "__main__":
    main()