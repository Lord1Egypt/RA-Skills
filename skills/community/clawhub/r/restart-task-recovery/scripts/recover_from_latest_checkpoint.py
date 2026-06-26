#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path
from datetime import datetime


def latest_checkpoint(root: Path):
    files = sorted(root.glob("*/*.md"))
    return files[-1] if files else None


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
        resume = fields.get("Resume message") or (
            f"Continue where you left off. Last completed: {fields.get('Last done', '(unknown)')}. Next: {fields.get('Next', '(unknown)')}."
        )
        items.append({"sessionKey": session_key, "message": resume})
    return items


def main():
    root = Path("memory/restart-checkpoints")
    cp = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else latest_checkpoint(root)
    if not cp or not cp.exists():
        print("No checkpoint file found", file=sys.stderr)
        sys.exit(1)

    items = parse_checkpoint(cp.read_text(encoding="utf-8"))

    out = {
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "checkpoint": str(cp),
        "count": len(items),
        "actions": [
            {
                "tool": "sessions_send",
                "params": {"sessionKey": i["sessionKey"], "message": i["message"]},
            }
            for i in items
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
