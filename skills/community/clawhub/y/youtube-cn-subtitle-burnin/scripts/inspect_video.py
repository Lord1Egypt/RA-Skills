#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def run_ffprobe(path: Path) -> dict:
    if shutil.which("ffprobe") is None:
        raise SystemExit("ffprobe not found")
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(path),
        ],
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "ffprobe failed")
    return json.loads(result.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect final MP4 stream health.")
    parser.add_argument("video", type=Path)
    args = parser.parse_args()

    if not args.video.exists():
        print(f"FAIL: missing video {args.video}")
        return 1

    info = run_ffprobe(args.video)
    streams = info.get("streams", [])
    video_streams = [s for s in streams if s.get("codec_type") == "video"]
    audio_streams = [s for s in streams if s.get("codec_type") == "audio"]
    duration = float(info.get("format", {}).get("duration") or 0)
    issues: list[str] = []

    if duration <= 0:
        issues.append("duration is missing or zero")
    if not video_streams:
        issues.append("missing video stream")
    if not audio_streams:
        issues.append("missing audio stream")
    if video_streams:
        width = int(video_streams[0].get("width") or 0)
        height = int(video_streams[0].get("height") or 0)
        if width <= 0 or height <= 0:
            issues.append("video dimensions are missing")
    else:
        width = height = 0

    print(f"Video: {args.video}")
    print(f"Duration: {duration:.3f}s")
    print(f"Resolution: {width}x{height}")
    print(f"Video streams: {len(video_streams)}")
    print(f"Audio streams: {len(audio_streams)}")

    if issues:
        print(f"FAIL: {len(issues)} issue(s)")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("PASS: video has duration, video stream, audio stream, and dimensions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
