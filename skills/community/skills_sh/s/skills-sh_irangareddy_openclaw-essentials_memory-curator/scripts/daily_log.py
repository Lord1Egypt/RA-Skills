#!/usr/bin/env python3
"""
Create or append to today's daily log.

Usage:
    python daily_log.py --workspace ~/.openclaw/workspace --entry "Completed feature X"
    python daily_log.py --workspace ~/.openclaw/workspace --template
"""

import argparse
import os
from datetime import datetime
from pathlib import Path


def get_daily_log_path(workspace: Path) -> Path:
    """Get path to today's daily log."""
    memory_dir = workspace / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    return memory_dir / f"{today}.md"


def create_from_template(log_path: Path, workspace: Path) -> None:
    """Create today's log from template."""
    template_path = Path(__file__).parent.parent / "assets" / "templates" / "daily-log.md"

    today = datetime.now().strftime("%Y-%m-%d")
    weekday = datetime.now().strftime("%A")

    if template_path.exists():
        content = template_path.read_text()
        # Replace placeholders
        content = content.replace("{DATE}", today)
        content = content.replace("{WEEKDAY}", weekday)
    else:
        # Fallback template
        content = f"""# {today} ({weekday})

## Key Activities

-

## Decisions Made

-

## Learnings

-

## Context for Tomorrow

-
"""

    log_path.write_text(content)
    print(f"Created: {log_path}")


def append_entry(log_path: Path, entry: str, category: str = None) -> None:
    """Append entry to daily log."""
    if not log_path.exists():
        create_from_template(log_path, log_path.parent.parent)

    timestamp = datetime.now().strftime("%H:%M")

    if category:
        entry_text = f"\n## {category}\n\n- [{timestamp}] {entry}\n"
    else:
        entry_text = f"- [{timestamp}] {entry}\n"

    with open(log_path, 'a') as f:
        f.write(entry_text)

    print(f"Appended to: {log_path}")


def main():
    parser = argparse.ArgumentParser(description="Manage daily logs")
    parser.add_argument("--workspace", required=True, help="Agent workspace path")
    parser.add_argument("--entry", help="Entry to append")
    parser.add_argument("--category", help="Category for entry")
    parser.add_argument("--template", action="store_true", help="Create from template")
    parser.add_argument("--show", action="store_true", help="Show today's log")

    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser()
    log_path = get_daily_log_path(workspace)

    if args.template:
        create_from_template(log_path, workspace)
    elif args.entry:
        append_entry(log_path, args.entry, args.category)
    elif args.show:
        if log_path.exists():
            print(log_path.read_text())
        else:
            print(f"No log for today: {log_path}")
    else:
        print(f"Log path: {log_path}")
        print(f"Exists: {log_path.exists()}")


if __name__ == "__main__":
    main()
