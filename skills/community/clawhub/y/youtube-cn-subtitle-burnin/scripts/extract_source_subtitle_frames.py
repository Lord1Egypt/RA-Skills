#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def get_duration(video: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", str(video)],
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "ffprobe failed")
    return float(json.loads(result.stdout).get("format", {}).get("duration") or 0)


def format_name(index: int, seconds: float) -> str:
    total = max(0, int(round(seconds)))
    hh = total // 3600
    mm = (total % 3600) // 60
    ss = total % 60
    return f"source-subtitle-check-{index:02d}-{hh:02d}-{mm:02d}-{ss:02d}.jpg"


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract source-video frames for checking existing burned-in subtitles before choosing subtitle layout.")
    parser.add_argument("video", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--count", type=int, default=5)
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        print("FAIL: ffmpeg and ffprobe are required")
        return 1
    if not args.video.exists():
        print(f"FAIL: missing video {args.video}")
        return 1

    duration = get_duration(args.video)
    if duration <= 0:
        print("FAIL: source video duration is missing or zero")
        return 1
    count = max(3, args.count)
    fractions = [0.08, 0.25, 0.5, 0.75, 0.92]
    if count != 5:
        fractions = [(index + 1) / (count + 1) for index in range(count)]
    times = [min(duration - 0.1, max(0, duration * fraction)) for fraction in fractions]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for index, seconds in enumerate(times, 1):
        output = args.out_dir / format_name(index, seconds)
        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                f"{seconds:.3f}",
                "-i",
                str(args.video),
                "-frames:v",
                "1",
                "-q:v",
                "2",
                str(output),
            ],
            check=False,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            print(result.stderr.strip())
            return 1
        print(f"wrote {output}")
    print(f"PASS: extracted {len(times)} source subtitle check frame(s)")
    print("Review these frames for existing hard subtitles before choosing bilingual mode.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
