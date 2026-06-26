#!/usr/bin/env python3
"""
load_memory.py — Load agent memory at session start.

Returns a formatted string for injection into the system prompt.
Loads MEMORY.md + today's daily log + optionally yesterday's log.
"""

from datetime import date, timedelta
from pathlib import Path


def get_context(
    workspace: str = "~/.agent_workspace",
    max_memory_chars: int = 3000,
    load_yesterday: bool = True,
) -> str:
    root = Path(workspace).expanduser()
    parts = []

    memory_md = root / "MEMORY.md"
    if memory_md.exists():
        text = memory_md.read_text(encoding="utf-8")
        if len(text) > max_memory_chars:
            text = text[:max_memory_chars] + "\n...[MEMORY.md truncated]"
        parts.append(f"## Long-term memory (MEMORY.md)\n{text}")

    today_log = root / "memory" / f"{date.today()}.md"
    if today_log.exists():
        parts.append(f"## Today's log ({date.today()})\n{today_log.read_text(encoding='utf-8')}")

    if load_yesterday:
        yesterday = date.today() - timedelta(days=1)
        yesterday_log = root / "memory" / f"{yesterday}.md"
        if yesterday_log.exists():
            parts.append(f"## Yesterday's log ({yesterday})\n{yesterday_log.read_text(encoding='utf-8')}")

    if not parts:
        return ""

    header = f"[Agent memory — {len(parts)} source(s) loaded]\n"
    return header + "\n\n".join(parts)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--workspace", default="~/.agent_workspace")
    p.add_argument("--max-chars", type=int, default=3000)
    args = p.parse_args()
    print(get_context(args.workspace, args.max_chars))
