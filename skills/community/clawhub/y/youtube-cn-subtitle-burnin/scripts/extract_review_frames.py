#!/usr/bin/env python3
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def parse_time(value: str) -> float:
    value = value.strip()
    if re.fullmatch(r"\d+(\.\d+)?", value):
        return float(value)
    parts = value.split(":")
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    if len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    raise argparse.ArgumentTypeError(f"invalid time: {value}")


def get_duration(video: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            str(video),
        ],
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "ffprobe failed")
    return float(json.loads(result.stdout).get("format", {}).get("duration") or 0)


def format_name(seconds: float) -> str:
    seconds = max(0, int(round(seconds)))
    hh = seconds // 3600
    mm = (seconds % 3600) // 60
    ss = seconds % 60
    return f"{hh:02d}-{mm:02d}-{ss:02d}.jpg"


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract review screenshots from a video.")
    parser.add_argument("video", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--times", help="Comma-separated times, e.g. 00:00:12,00:31:07,01:17:16")
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        print("FAIL: ffmpeg and ffprobe are required")
        return 1
    if not args.video.exists():
        print(f"FAIL: missing video {args.video}")
        return 1

    duration = get_duration(args.video)
    if args.times:
        times = [parse_time(item) for item in args.times.split(",") if item.strip()]
    else:
        times = [12, max(0, duration / 2), max(0, duration - 60)]
    times = sorted({round(t, 3) for t in times if 0 <= t <= duration})
    if not times:
        print("FAIL: no valid screenshot times")
        return 1

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for seconds in times:
        output = args.out_dir / format_name(seconds)
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
    print(f"PASS: extracted {len(times)} screenshot(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
