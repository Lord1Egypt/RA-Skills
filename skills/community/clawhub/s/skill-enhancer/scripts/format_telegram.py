#!/usr/bin/env python3
"""Phase 4 helper: format recommendations as a Telegram message.

Usage:
  python3 scripts/format_telegram.py --input PATH [--max-chars 4096]
"""

from __future__ import annotations

import json
import argparse
from datetime import date
from pathlib import Path


SEVERITY_EMOJI = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
SEVERITY_LABEL = {"green": "Safe refactors", "yellow": "Needs review", "red": "Informational"}


def format_digest(recommendations: list[dict], max_chars: int = 4096) -> str:
    if not recommendations:
        return f"📋 Weekly Skill Audit — {date.today().isoformat()}\n\nNo strong recommendations this week."

    by_severity: dict[str, list[dict]] = {"green": [], "yellow": [], "red": []}
    for rec in recommendations:
        sev = rec.get("severity", "red")
        by_severity.setdefault(sev, []).append(rec)

    lines = [f"📋 Weekly Skill Audit — {date.today().isoformat()}", ""]
    idx = 0

    for severity in ("green", "yellow", "red"):
        items = by_severity.get(severity, [])
        if not items:
            continue
        emoji = SEVERITY_EMOJI[severity]
        label = SEVERITY_LABEL[severity]
        lines.append(f"{emoji} {label} ({len(items)}):")
        for item in items:
            idx += 1
            title = item.get("title", "untitled")
            action = item.get("proposed_action", "")
            line = f"  {idx}. {title}"
            if action and severity == "green":
                line += f" → {action[:60]}"
            lines.append(line)
        lines.append("")

    lines.append('Reply with a number for details, or "approve 1,2" to greenlight.')

    message = "\n".join(lines)

    if len(message) > max_chars:
        truncated = message[: max_chars - 30]
        last_newline = truncated.rfind("\n")
        if last_newline > 0:
            truncated = truncated[:last_newline]
        message = truncated + "\n\n(truncated — reply for full details)"

    return message


def main() -> None:
    parser = argparse.ArgumentParser(description="Format recommendations for Telegram")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--max-chars", type=int, default=4096)
    args = parser.parse_args()

    recs = json.loads(args.input.read_text()) if args.input.exists() else []
    print(format_digest(recs, max_chars=args.max_chars))


if __name__ == "__main__":
    main()
