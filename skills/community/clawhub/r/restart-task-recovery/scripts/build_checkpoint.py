#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: build_checkpoint.py <output-file>", file=sys.stderr)
        sys.exit(1)

    out = Path(sys.argv[1]).expanduser()
    raw = sys.stdin.read().strip()
    if not raw:
        print("Expected JSON on stdin", file=sys.stderr)
        sys.exit(2)

    data = json.loads(raw)
    sessions = data.get("sessions", [])
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append(f"# Restart checkpoint ({now})")
    lines.append("")

    for s in sessions:
        key = s.get("sessionKey", "unknown")
        agent = s.get("agentId", "unknown")
        goal = s.get("goal", "(fill)")
        done = s.get("lastDone", "(fill)")
        nxt = s.get("nextStep", "(fill)")
        blockers = s.get("blockers", "none")

        lines.append(f"## {key}")
        lines.append(f"- Agent: {agent}")
        lines.append(f"- Goal: {goal}")
        lines.append(f"- Last done: {done}")
        lines.append(f"- Next: {nxt}")
        lines.append(f"- Blockers: {blockers}")
        lines.append(
            f"- Resume message: Continue where you left off. Last completed: {done}. Next: {nxt}."
        )
        lines.append("")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(str(out))


if __name__ == "__main__":
    main()
