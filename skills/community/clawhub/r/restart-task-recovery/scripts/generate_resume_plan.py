#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


def parse_checkpoint(text: str):
    blocks = re.split(r"\n## ", "\n" + text)
    items = []
    for b in blocks:
        b = b.strip()
        if not b:
            continue
        lines = b.splitlines()
        session_key = lines[0].strip()
        if session_key.startswith('#') or ':' not in session_key:
            continue
        fields = {}
        for ln in lines[1:]:
            m = re.match(r"-\s*([^:]+):\s*(.*)", ln.strip())
            if m:
                fields[m.group(1).strip()] = m.group(2).strip()
        msg = fields.get("Resume message") or (
            f"Continue where you left off. Last completed: {fields.get('Last done', '(unknown)')}. Next: {fields.get('Next', '(unknown)')}."
        )
        items.append(
            {
                "sessionKey": session_key,
                "agent": fields.get("Agent", "unknown"),
                "goal": fields.get("Goal", ""),
                "resumeMessage": msg,
            }
        )
    return items


def main():
    if len(sys.argv) < 2:
        print("Usage: generate_resume_plan.py <checkpoint.md> [out.json]", file=sys.stderr)
        sys.exit(1)

    cp = Path(sys.argv[1]).expanduser()
    out = Path(sys.argv[2]).expanduser() if len(sys.argv) > 2 else None

    text = cp.read_text(encoding="utf-8")
    items = parse_checkpoint(text)

    payload = {"count": len(items), "items": items}

    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(str(out))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
