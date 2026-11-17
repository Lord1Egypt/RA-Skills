#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在 references/ 里检索术语，返回命中行及其出处，避免整份读文件。

用法：
    python3 search_terms.py 悬停
    python3 search_terms.py "stagger" --limit 5
    python3 search_terms.py 弹簧 --file motion
    python3 search_terms.py 光照 --file three
    python3 search_terms.py 包豪斯 --file art
    python3 search_terms.py --list
    python3 search_terms.py 层级 --json
"""
import argparse
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(BASE, "references")

FILES = {
    "effect": "effect-catalog.md",
    "motion": "motion-vocabulary.md",
    "design": "design-vocabulary.md",
    "token": "motion-tokens.md",
    "platform": "platform-and-perf.md",
    "rubric": "review-rubric.md",
    "art": "art-direction.md",
    "gsap": "gsap-motion.md",
    "three": "threejs-3d.md",
    "p5": "p5js-creative-coding.md",
    "component": "premium-components.md",
}

LAYOUT_HINT = ("`**", "**`")


def load(only=None):
    entries = []
    for key, fn in FILES.items():
        if only and key != only:
            continue
        path = os.path.join(REF, fn)
        if not os.path.exists(path):
            continue
        section = ""
        with open(path, encoding="utf-8") as fh:
            for lineno, raw in enumerate(fh, 1):
                line = raw.rstrip("\n")
                if line.startswith("#"):
                    section = line.lstrip("#").strip()
                    continue
                text = line.strip()
                if not text or text.startswith("```"):
                    continue
                if text.startswith("|"):
                    if set(text) <= set("|-: "):
                        continue
                    cells = [c.strip() for c in text.strip("|").split("|")]
                    text = " · ".join(c for c in cells if c)
                entries.append(
                    {"file": key, "fn": fn, "section": section, "line": lineno, "text": text}
                )
    return entries


def score(text, tokens):
    low = text.lower()
    if not all(t in low for t in tokens):
        return 0
    s = sum(low.count(t) for t in tokens)
    # 命中词条名（**中文名** 或 `English`）权重最高
    for zh, en in re.findall(r"\*\*(.+?)\*\*|`(.+?)`", text):
        span = (zh or en).lower()
        if any(t in span for t in tokens):
            s += 4
    return s


def clip(text, tokens, width=110):
    low = text.lower()
    pos = min((low.find(t) for t in tokens if low.find(t) >= 0), default=0)
    if len(text) <= width:
        return text
    start = max(0, pos - width // 3)
    out = text[start:start + width]
    return ("…" if start else "") + out + "…"


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("query", nargs="*", help="检索词，可多个（多词为 AND）")
    ap.add_argument("--file", choices=sorted(FILES), help="只搜某个文件")
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--list", action="store_true", help="列出所有文件与章节")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    entries = load(args.file)

    if args.list:
        if args.json:
            print(json.dumps(entries, ensure_ascii=False, indent=1)[:2000])
            return
        cur = None
        for e in entries:
            if e["section"] and (cur != (e["fn"], e["section"])):
                cur = (e["fn"], e["section"])
                print(f"\n{e['fn']}  §{e['section']}")
        print(f"\n共 {len(entries)} 行可检索内容。")
        return

    if not args.query:
        ap.print_help()
        sys.exit(2)

    tokens = [t.lower() for t in args.query if t]
    hits = []
    for e in entries:
        s = score(e["text"], tokens)
        if s:
            hits.append((s, e))
    hits.sort(key=lambda x: (-x[0], x[1]["fn"], x[1]["line"]))

    if not hits:
        print(f"没找到「{' '.join(args.query)}」。试试更短的词，或加 --list 看有哪些章节。")
        sys.exit(1)

    top = hits[: args.limit]
    if args.json:
        print(json.dumps(
            [{"score": s, "file": e["fn"], "section": e["section"], "line": e["line"], "text": e["text"]}
             for s, e in top], ensure_ascii=False, indent=1))
        return

    for s, e in top:
        print(f"{e['fn']}  §{e['section']}  L{e['line']}")
        print("  " + clip(e["text"], tokens))
    if len(hits) > args.limit:
        print(f"\n…还有 {len(hits) - args.limit} 条，加 --limit 查看")


if __name__ == "__main__":
    main()
