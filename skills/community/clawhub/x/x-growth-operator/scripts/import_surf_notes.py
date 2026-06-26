from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import utc_now_iso, write_json


ENTRY_RE = re.compile(
    r"\d+\)\s*时间：(?P<time>.+?)\n\s*内容：@(?P<handle>[A-Za-z0-9_]+)｜(?P<content>.+?)\n\s*链接：(?P<link>https://x\.com/[^\s]+)\n\s*评论：(?P<comment>.+?)(?=\n\d+\)|\Z)",
    re.S,
)


def infer_topics(text: str, comment: str) -> list[str]:
    combined = f"{text} {comment}".lower()
    candidates = [
        "ai",
        "agent",
        "coding agents",
        "local agent",
        "openclaw",
        "developer workflow",
        "automation",
    ]
    return [candidate for candidate in candidates if candidate in combined]


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert manual X surf notes into opportunities JSON.")
    parser.add_argument("--notes", required=True, help="Path to markdown notes file.")
    parser.add_argument("--output", default="data/opportunities_from_notes.json", help="Output JSON path.")
    args = parser.parse_args()

    raw = Path(args.notes).read_text(encoding="utf-8")
    items = []
    for index, match in enumerate(ENTRY_RE.finditer(raw), start=1):
        content = " ".join(match.group("content").split())
        comment = " ".join(match.group("comment").split())
        items.append({
            "id": f"notes-{index}",
            "source_account": match.group("handle"),
            "source_type": "manual-surf",
            "text": content,
            "url": match.group("link"),
            "posted_at": match.group("time").replace(" ", "T") + "+08:00",
            "likes": 0,
            "replies": 0,
            "reposts": 0,
            "quotes": 0,
            "views": 0,
            "growth_velocity": 0.3,
            "sentiment": "positive" if "值得跟" in comment else "neutral",
            "topics": infer_topics(content, comment),
            "operator_comment": comment,
        })

    payload = {
        "generated_at": utc_now_iso(),
        "source": "manual-surf-notes",
        "count": len(items),
        "items": items,
    }
    path = write_json(args.output, payload)
    print(f"Wrote {len(items)} opportunities to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
