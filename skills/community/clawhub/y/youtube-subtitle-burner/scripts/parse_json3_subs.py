#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Parse YouTube json3 auto-subtitles into sentence-level segments with accurate word-level timings.

Usage:
    uv run parse_json3_subs.py INPUT.json3 OUTPUT.json

Input: YouTube json3 subtitle file (downloaded with `yt-dlp --write-auto-subs --sub-format json3`)
Output: JSON array of {"start": float, "end": float, "text_zh_src": "English sentence"}

Why json3 and not VTT?
- YouTube VTT files use "rolling cues" that repeat previous text in each block.
  Parsing them directly loses the opening segment and causes subtitle desync (~2s delay).
- json3 contains word-level timestamps (tStartMs + tOffsetMs per word),
  giving millisecond-accurate timing from 0 seconds.
"""
import json
import re
import sys
import argparse


def parse_json3(filepath):
    """Extract word-level timings from json3 subtitle file."""
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    events = data.get("events", [])

    # Build word-level timeline
    all_words = []
    for ev in events:
        if "segs" not in ev:
            continue
        base_ms = ev["tStartMs"]
        for seg in ev["segs"]:
            text = seg.get("utf8", "").strip()
            if not text or text == "\n":
                continue
            offset = seg.get("tOffsetMs", 0)
            abs_time = (base_ms + offset) / 1000.0
            all_words.append({"time": abs_time, "word": text})

    if not all_words:
        print("ERROR: No word-level data found in json3 file", file=sys.stderr)
        sys.exit(1)

    # Dedupe (rolling cues repeat words)
    seen = set()
    unique = []
    for w in all_words:
        key = (round(w["time"], 1), w["word"])
        if key not in seen:
            seen.add(key)
            unique.append(w)

    unique.sort(key=lambda x: x["time"])

    # Group into sentence segments (~3-5 sec each)
    segments = []
    current_words = []
    current_start = None

    for w in unique:
        if current_start is None:
            current_start = w["time"]

        current_words.append(w["word"])
        elapsed = w["time"] - current_start
        combined = " ".join(current_words)

        # Flush on sentence end (>1.5s elapsed) or after 5 seconds
        if (combined.rstrip().endswith((".", "!", "?")) and elapsed > 1.5) or elapsed > 5:
            segments.append({
                "start": round(current_start, 2),
                "end": round(w["time"] + 0.3, 2),
                "text_zh_src": combined
            })
            current_words = []
            current_start = None

    # Flush remaining
    if current_words:
        segments.append({
            "start": round(current_start, 2),
            "end": round(unique[-1]["time"] + 0.3, 2),
            "text_zh_src": " ".join(current_words)
        })

    return segments


def main():
    parser = argparse.ArgumentParser(description="Parse YouTube json3 subtitles into segments")
    parser.add_argument("input", help="Input .json3 file")
    parser.add_argument("output", help="Output .json file")
    args = parser.parse_args()

    segments = parse_json3(args.input)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)

    print(f"Parsed {len(segments)} segments → {args.output}")
    print(f"First segment: {segments[0]['start']:.2f}s - {segments[0]['text_zh_src'][:60]}")
    print(f"Last segment ends: {segments[-1]['end']:.2f}s")


if __name__ == "__main__":
    main()
