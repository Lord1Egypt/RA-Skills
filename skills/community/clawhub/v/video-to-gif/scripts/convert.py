#!/usr/bin/env python3
"""Convert a video clip to GIF using ffmpeg."""

import argparse
import os
import shlex
import shutil
import subprocess
import sys


def ensure_ffmpeg_installed() -> bool:
    """Return True when both ffmpeg and ffprobe are available."""
    ffmpeg_path = shutil.which("ffmpeg")
    ffprobe_path = shutil.which("ffprobe")
    if ffmpeg_path and ffprobe_path:
        print("ffmpeg and ffprobe are available.")
        return True

    print("ffmpeg and ffprobe are required but were not found.")
    print("Please install ffmpeg first, then run this command again.")
    print("Example on macOS with Homebrew: brew install ffmpeg")
    return False


def convert_to_gif(
    input_path: str,
    output_path: str,
    fps: int = 15,
    width: int = 480,
    start: str = "0",
    duration: str = None,
) -> bool:
    """Convert video to GIF with ffmpeg."""
    if not os.path.exists(input_path):
        print(f"Error: input file does not exist: {input_path}")
        return False

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        start,
    ]

    if duration:
        cmd.extend(["-t", duration])

    cmd.extend(
        [
            "-i",
            input_path,
            "-vf",
            f"fps={fps},scale={width}:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
            "-loop",
            "0",
            output_path,
        ]
    )

    print(f"Running command: {' '.join(shlex.quote(c) for c in cmd)}")
    print("Converting...")

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Conversion succeeded.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed: {e.stderr}")
        return False


def get_file_info(file_path: str) -> dict:
    """Return output file metadata."""
    if not os.path.exists(file_path):
        return {}

    size = os.path.getsize(file_path)
    size_kb = size / 1024
    size_mb = size_kb / 1024
    size_str = f"{size_mb:.2f} MB" if size_mb >= 1 else f"{size_kb:.2f} KB"

    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height,r_frame_rate",
        "-of",
        "csv=s=,:p=0",
        file_path,
    ]

    dimensions = "unknown"
    frame_rate = "unknown"

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        info = result.stdout.strip().split(",")
        if len(info) >= 3:
            width, height = info[0], info[1]
            fps_num, fps_den = map(int, info[2].split("/"))
            frame_rate = f"{fps_num / fps_den:.2f}"
            dimensions = f"{width}x{height}"
    except Exception:
        pass

    return {
        "path": file_path,
        "size": size_str,
        "dimensions": dimensions,
        "frame_rate": frame_rate,
    }


def main():
    parser = argparse.ArgumentParser(description="Convert video to GIF.")
    parser.add_argument("input", help="Input video file path")
    parser.add_argument("output", help="Output GIF file path")
    parser.add_argument("--fps", type=int, default=15, help="Output frame rate (default: 15)")
    parser.add_argument(
        "--width", type=int, default=480, help="Output width in pixels (default: 480)"
    )
    parser.add_argument("--start", type=str, default="0", help="Start time (default: 0)")
    parser.add_argument("--duration", type=str, default=None, help="Clip duration")

    args = parser.parse_args()

    if not ensure_ffmpeg_installed():
        sys.exit(1)

    print("=" * 50)
    print("Video to GIF Converter")
    print("=" * 50)
    print(f"Input file: {args.input}")
    print(f"Output file: {args.output}")
    print(f"Frame rate: {args.fps} fps")
    print(f"Width: {args.width} px")
    print(f"Start time: {args.start}")
    if args.duration:
        print(f"Duration: {args.duration}")
    print("-" * 50)

    success = convert_to_gif(
        input_path=args.input,
        output_path=args.output,
        fps=args.fps,
        width=args.width,
        start=args.start,
        duration=args.duration,
    )

    if success:
        print("-" * 50)
        info = get_file_info(args.output)
        if info:
            print("Output file info:")
            print(f"  Path: {info['path']}")
            print(f"  Size: {info['size']}")
            print(f"  Dimensions: {info['dimensions']}")
            print(f"  Frame rate: {info['frame_rate']} fps")
        print("=" * 50)
        sys.exit(0)

    print("=" * 50)
    sys.exit(1)


if __name__ == "__main__":
    main()
