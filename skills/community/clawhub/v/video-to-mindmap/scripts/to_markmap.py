#!/usr/bin/env python3
"""to_markmap — a LinkDigest digest (JSON on stdin) → Markdown that markmap draws as a mind map.

    python3 linkdigest.py "<video link>" --format json --depth transcript | python3 to_markmap.py > map.md
    npx markmap-cli map.md        # or paste map.md into https://markmap.js.org/repl

Long videos (8 minutes and up) carry a timed outline (`outline`: start, end,
title, summary lines); each section becomes a branch named with its time span,
its summary lines become leaves. A short video has no outline: its key points
become one layer of branches, and the file says so. Sections longer than
--max-minutes are marked, so a reader knows where to split by hand.

Standard library only. Exit 0 ok · 2 no usable JSON on stdin · 5 nothing to draw.
"""
from __future__ import annotations

import argparse
import json
import sys


def clock(sec: float) -> str:
    sec = int(sec or 0)
    h, m, s = sec // 3600, sec % 3600 // 60, sec % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def to_markmap(d: dict, max_minutes: float = 15) -> str:
    title = (d.get("title") or "Video").strip().replace("\n", " ")
    lines = [f"# {title}"]
    outline = d.get("outline") or []
    if outline:
        for sec in outline:
            start, end = float(sec.get("start") or 0), float(sec.get("end") or 0)
            long = end > start and (end - start) / 60 > max_minutes
            note = " (long section: split it by the transcript)" if long else ""
            lines.append(f"- `{clock(start)}–{clock(end)}` **{(sec.get('title') or '').strip()}**{note}")
            for point in sec.get("summary") or []:
                lines.append(f"  - {str(point).strip()}")
    else:
        points = [str(p).strip() for p in (d.get("key_points") or []) if str(p).strip()]
        if not points:
            return ""
        lines.append("- Key points (no timed outline: the video is under 8 minutes or was read before outlines existed)")
        lines.extend(f"  - {p}" for p in points)
    source = d.get("source_url") or d.get("url")
    if source:
        lines.append(f"- Source: {source}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="LinkDigest JSON (stdin) → markmap Markdown (stdout)")
    p.add_argument("--max-minutes", type=float, default=15, help="mark sections longer than this (default 15)")
    args = p.parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, ValueError):
        pass
    raw = sys.stdin.read()
    try:
        d = json.loads(raw)
    except json.JSONDecodeError:
        print("to_markmap: stdin is not JSON — run linkdigest.py with --format json", file=sys.stderr)
        return 2
    if not isinstance(d, dict):
        print("to_markmap: expected one digest object", file=sys.stderr)
        return 2
    md = to_markmap(d, args.max_minutes)
    if not md:
        print("to_markmap: the digest has neither an outline nor key points", file=sys.stderr)
        return 5
    sys.stdout.write(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
