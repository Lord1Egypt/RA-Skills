#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from prepare_youtube_transcript import write_srt


def cue_id(cue: dict[str, object], fallback: int) -> int:
    return int(cue.get("id", fallback))


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply numbered Chinese translations to cleaned cue JSON.")
    parser.add_argument("cue_json", type=Path)
    parser.add_argument("translation_cache", type=Path)
    parser.add_argument("--srt-out", type=Path, required=True)
    parser.add_argument("--force", action="store_true", help="Overwrite existing SRT output")
    args = parser.parse_args()

    cues = json.loads(args.cue_json.read_text(encoding="utf-8"))
    cache_data = json.loads(args.translation_cache.read_text(encoding="utf-8"))
    cache = {int(item["id"]): str(item["zh"]).strip() for item in cache_data}
    cue_ids = [cue_id(cue, index + 1) for index, cue in enumerate(cues)]
    missing = [item_id for item_id in cue_ids if item_id not in cache or not cache[item_id]]
    extra = sorted(set(cache) - set(cue_ids))
    if missing:
        print(f"FAIL: missing translation ids: {missing[:30]}")
        return 1
    if extra:
        print(f"FAIL: unexpected translation ids: {extra[:30]}")
        return 1
    for index, cue in enumerate(cues, 1):
        cue["zh"] = cache[cue_id(cue, index)]
    if args.srt_out.exists() and not args.force:
        print(f"FAIL: output already exists, choose a new version or pass --force: {args.srt_out}")
        return 1
    args.srt_out.parent.mkdir(parents=True, exist_ok=True)
    write_srt(cues, args.srt_out, "zh")
    print(f"PASS: wrote {len(cues)} translated cues to {args.srt_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
