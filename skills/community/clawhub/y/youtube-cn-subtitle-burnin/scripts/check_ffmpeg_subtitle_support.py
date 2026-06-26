#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import re
import shutil
import subprocess
import sys


def has_filter(ffmpeg: str, name: str) -> bool:
    result = subprocess.run([ffmpeg, "-hide_banner", "-filters"], check=False, text=True, capture_output=True)
    return result.returncode == 0 and re.search(rf"\b{name}\b", result.stdout) is not None


def candidate_ffmpegs(explicit: str | None) -> list[str]:
    candidates: list[str] = []
    if explicit:
        candidates.append(explicit)
    default = shutil.which("ffmpeg")
    if default:
        candidates.append(default)
    candidates.extend(
        [
            "/Users/daniel/Library/Application Support/bilibili/ffmpeg/ffmpeg",
            "/opt/homebrew/bin/ffmpeg",
            "/usr/local/bin/ffmpeg",
        ]
    )
    seen: set[str] = set()
    existing: list[str] = []
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if Path(candidate).exists() or shutil.which(candidate):
            existing.append(candidate)
    return existing


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether ffmpeg can burn subtitles.")
    parser.add_argument("--ffmpeg")
    args = parser.parse_args()

    checked = candidate_ffmpegs(args.ffmpeg)
    if not checked:
        print("FAIL: ffmpeg not found")
        return 1
    for ffmpeg in checked:
        ass = has_filter(ffmpeg, "ass")
        subtitles = has_filter(ffmpeg, "subtitles")
        drawtext = has_filter(ffmpeg, "drawtext")
        print(f"ffmpeg: {ffmpeg}")
        print(f"ass filter: {'yes' if ass else 'no'}")
        print(f"subtitles filter: {'yes' if subtitles else 'no'}")
        print(f"drawtext filter: {'yes' if drawtext else 'no'}")
        if ass or subtitles:
            print(f"PASS: use this ffmpeg for subtitle burn-in: {ffmpeg}")
            return 0
    print("FAIL: no checked ffmpeg can burn subtitle files with native filters")
    print("Fallback: use scripts/burn_subtitles_pil.py for frame-rendered hard subtitles")
    return 1


if __name__ == "__main__":
    sys.exit(main())
