#!/usr/bin/env python3
"""
Apply speed change to a video file.

Uses FFmpeg's setpts (video) and atempo (audio) filters.

Usage:
    python speed_video.py input.mp4
    python speed_video.py input.mp4 -o output.mp4
    python speed_video.py input.mp4 --speed 1.5
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def check_has_audio(input_file: str) -> bool:
    """Check if input file has audio stream."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_streams", "-select_streams", "a",
        input_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return bool(data.get("streams"))


def speed_video(input_file: str, output_file: str, speed: float, has_audio_stream: bool) -> None:
    """Apply speed change using FFmpeg."""
    video_filter = f"setpts={1/speed}*PTS"

    if has_audio_stream:
        if 0.5 <= speed <= 2.0:
            audio_filter = f"atempo={speed}"
        else:
            tempos = []
            remaining = speed
            while remaining > 2.0:
                tempos.append("atempo=2.0")
                remaining /= 2.0
            while remaining < 0.5:
                tempos.append("atempo=0.5")
                remaining /= 0.5
            tempos.append(f"atempo={remaining}")
            audio_filter = ",".join(tempos)

        filter_complex = f"[0:v]{video_filter}[v];[0:a]{audio_filter}[a]"
        cmd = [
            "ffmpeg", "-y", "-i", input_file,
            "-filter_complex", filter_complex,
            "-map", "[v]", "-map", "[a]",
            output_file
        ]
    else:
        cmd = [
            "ffmpeg", "-y", "-i", input_file,
            "-vf", video_filter,
            "-an",
            output_file
        ]
    subprocess.run(cmd, capture_output=True, check=True)


def main():
    parser = argparse.ArgumentParser(
        description="Apply speed change to a video file."
    )
    parser.add_argument("input", help="Input video file path")
    parser.add_argument("-o", "--output", help="Output video file path (default: input_1.2x.mp4)")
    parser.add_argument(
        "-s", "--speed", type=float, default=1.2,
        help="Playback speed multiplier (default: 1.2)"
    )

    args = parser.parse_args()

    input_file = args.input
    if not os.path.isfile(input_file):
        print(f"Error: file not found: {input_file}")
        sys.exit(1)

    if args.speed <= 0:
        print("Error: speed must be positive")
        sys.exit(1)

    if args.output:
        output_file = args.output
    else:
        p = Path(input_file)
        output_file = str(p.with_stem(f"{p.stem}_{args.speed}x"))

    has_audio_stream = check_has_audio(input_file)
    print(f"Applying {args.speed}x speed to: {input_file}")
    speed_video(input_file, output_file, args.speed, has_audio_stream)
    print(f"Done! Output: {output_file}")


if __name__ == "__main__":
    main()
