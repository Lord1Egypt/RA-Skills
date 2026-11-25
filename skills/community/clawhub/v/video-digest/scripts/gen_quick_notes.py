#!/usr/bin/env python3
"""gen_quick_notes.py — 从 video-digest 缓存批量生成 Quick 笔记骨架。

用法:
  python3 scripts/gen_quick_notes.py --exclude id1 id2 ... > notes_skeleton.json

输出 JSON: { video_id: { title, dur, channel, url, tldr_hint, sections:[{t,title}], gold:[{t,q}] } }
- sections 来自视频章节（无章节则按时长 6 等分）
- gold 取各章首句中最「观点性」的一句（启发式），供人工润色
"""
import argparse
import json
import os
import sys
import tempfile
from pathlib import Path


def parse_ts(line):
    try:
        parts = line[1:line.index("]")].split(":")
        return int(parts[0]) * 60 + int(parts[1]) + (int(parts[2]) if len(parts) > 2 else 0)
    except Exception:
        return None


def sec_str(total):
    return f"{total//60:02d}:{total%60:02d}"


def to_secs(v):
    if isinstance(v, (int, float)):
        return int(v)
    parts = str(v).split(":")
    secs = 0
    for p in parts:
        secs = secs * 60 + int(float(p or 0))
    return secs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=str(Path(tempfile.gettempdir()) / f"video-deep-reader-{os.geteuid()}"))
    ap.add_argument("--exclude", nargs="*", default=[])
    args = ap.parse_args()

    root = Path(args.cache)
    if not root.exists():
        sys.exit(f"cache not found: {root}")

    out = {}
    for meta_path in sorted(root.glob("*/*/meta.json")):
        meta = json.loads(meta_path.read_text())
        vid = meta["id"]
        if vid in args.exclude:
            continue
        tr = meta_path.parent / "transcript.txt"
        lines = tr.read_text().splitlines() if tr.exists() else []
        blocks = []
        for ln in lines:
            pos = parse_ts(ln)
            if pos is not None and "]" in ln:
                blocks.append((pos, ln[ln.index("]") + 1:].strip()))

        ch = meta.get("chapters") or []
        if ch:
            sections = [{"t": sec_str(to_secs(c["start"])), "title": c["title"]} for c in ch]
        else:
            dur = int(meta.get("duration") or 0)
            step = max(dur // 6, 60)
            sections = [{"t": sec_str(i * step), "title": f"Part {i+1}"} for i in range(6) if i * step < dur]

        gold = []
        keywords = ("the key", "the trick", "the secret", "i think", "the most", "remember",
                    "the point", "what matters", "lesson", "mistake", "actually", "turns out")
        for pos, txt in blocks:
            low = txt.lower()
            if any(k in low for k in keywords) and 40 < len(txt) < 160:
                gold.append({"t": sec_str(pos), "q": txt})
            if len(gold) >= 4:
                break
        if not gold and blocks:
            mid = blocks[len(blocks) // 2]
            gold = [{"t": sec_str(mid[0]), "q": mid[1][:150]}]

        first = " ".join(t for _, t in blocks[:6])[:220]
        out[vid] = {
            "title": meta["title"],
            "dur": meta.get("duration_str"),
            "channel": meta.get("channel"),
            "url": meta.get("url"),
            "tldr_hint": first,
            "sections": sections,
            "gold": gold,
        }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
