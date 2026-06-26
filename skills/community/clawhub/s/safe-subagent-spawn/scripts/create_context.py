#!/usr/bin/env python3
"""Create a new subagent context file.

Generates the initial context file with metadata, standing instructions,
background, and the first directive. Outputs the absolute path to stdout.
"""
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

# Default: sub-agents/ under the workspace root (derived from this script's location)
CONTEXT_DIR = Path(__file__).resolve().parent.parent.parent.parent / "sub-agents"

TASK_SLUG_RE = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")


def validate_task_slug(slug: str) -> str:
    """Validate task slug: a-z 0-9 hyphens, start/end alphanumeric, 1-48 chars."""
    if not slug or len(slug) > 48:
        print(f"Error: task slug must be 1-48 characters, got {len(slug)}.", file=sys.stderr)
        sys.exit(1)
    if not TASK_SLUG_RE.match(slug):
        print(
            f"Error: invalid task slug '{slug}'. "
            "Must contain only a-z, 0-9, and hyphens, and start/end with an alphanumeric character.",
            file=sys.stderr,
        )
        sys.exit(1)
    return slug


def build_context(task_slug: str, context_path: Path, background: str, directive: str | None, ts: str) -> str:
    lines = [
        f"# Subagent Context: {task_slug}",
        "",
        "## Metadata",
        f"- Created: {ts}",
        f"- Task: {task_slug}",
        f"- Context File: {context_path}",
        "",
        "## Standing Instructions",
        "- Do not self-append or modify this file. It is read-only context provided by the parent.",
        "- Do not spawn additional subagents inside this subagent. All delegation must come from the parent.",
        "",
        "## Background",
        background.strip(),
        "",
    ]
    if directive:
        lines.extend([
            "---",
            "",
            f"## Directive — Round 1 — {ts}",
            "",
            directive.strip(),
            "",
        ])
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Create a new subagent context file.")
    ap.add_argument("--task", required=True, help="Short task slug for the filename")
    ap.add_argument("--background", required=True, help="User request or relevant background")
    ap.add_argument("--directive", default=None, help="Instructions for the child agent (optional; omit to create context without an initial directive)")
    args = ap.parse_args()

    CONTEXT_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now().astimezone()
    slug = validate_task_slug(args.task)
    filename = f"{now.strftime('%Y%m%d-%H%M%S')}-{slug}.md"
    context_path = CONTEXT_DIR / filename

    content = build_context(slug, context_path, args.background, args.directive, now.isoformat())
    context_path.write_text(content, encoding="utf-8")

    print(str(context_path))


if __name__ == "__main__":
    main()
