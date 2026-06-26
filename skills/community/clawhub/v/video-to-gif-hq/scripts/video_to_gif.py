#!/usr/bin/env python3
"""Convert a video clip to animated GIF or WebP using ffmpeg."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def die(message: str, code: int = 1) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(code)


def run(cmd: list[str]) -> None:
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        die(f"command failed with exit code {exc.returncode}: {' '.join(cmd)}", exc.returncode)


def require_ffmpeg() -> None:
    missing = [name for name in ("ffmpeg", "ffprobe") if shutil.which(name) is None]
    if missing:
        die("missing dependency on PATH: " + ", ".join(missing))


def scale_expr(width: int | None, height: int | None) -> str:
    if width and height:
        return f"scale={width}:{height}:flags=lanczos"
    if width:
        return f"scale={width}:-1:flags=lanczos"
    if height:
        return f"scale=-1:{height}:flags=lanczos"
    return "scale=iw:ih:flags=lanczos"


def base_input_args(args: argparse.Namespace) -> list[str]:
    cmd: list[str] = []
    # Seeking before -i is fast and adequate for GIF clipping. Users needing frame-perfect
    # starts can pass a short source clip or omit start and pre-trim separately.
    if args.start:
        cmd += ["-ss", args.start]
    cmd += ["-i", str(args.input)]
    if args.duration:
        cmd += ["-t", args.duration]
    elif args.end:
        cmd += ["-to", args.end]
    return cmd


def convert_gif(args: argparse.Namespace) -> None:
    filters = f"fps={args.fps},{scale_expr(args.width, args.height)}"
    with tempfile.TemporaryDirectory(prefix="video-to-gif-") as tmp:
        palette = Path(tmp) / "palette.png"
        run([
            "ffmpeg", "-y", *base_input_args(args),
            "-vf", f"{filters},palettegen=max_colors={args.max_colors}:stats_mode=diff",
            str(palette),
        ])
        run([
            "ffmpeg", "-y", *base_input_args(args), "-i", str(palette),
            "-lavfi", f"{filters} [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
            "-loop", str(args.loop),
            str(args.output),
        ])


def convert_webp(args: argparse.Namespace) -> None:
    filters = f"fps={args.fps},{scale_expr(args.width, args.height)}"
    run([
        "ffmpeg", "-y", *base_input_args(args),
        "-vf", filters,
        "-loop", str(args.loop),
        "-an", "-vsync", "0",
        "-quality", str(args.quality),
        str(args.output),
    ])


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a video clip to animated GIF or WebP.")
    parser.add_argument("input", type=Path, help="input video path, e.g. input.mp4")
    parser.add_argument("output", type=Path, help="output .gif or .webp path")
    parser.add_argument("--start", help="start time, e.g. 2.5 or 00:00:02.500")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--duration", help="clip duration, e.g. 4 or 00:00:04")
    group.add_argument("--end", help="end time, e.g. 8.5 or 00:00:08.500")
    parser.add_argument("--fps", type=float, default=12, help="frames per second (default: 12)")
    parser.add_argument("--width", type=int, help="output width, preserves aspect ratio if height omitted")
    parser.add_argument("--height", type=int, help="output height, preserves aspect ratio if width omitted")
    parser.add_argument("--output-format", choices=("gif", "webp"), help="override format inferred from output extension")
    parser.add_argument("--loop", type=int, default=0, help="loop count; 0 loops forever (default: 0)")
    parser.add_argument("--max-colors", type=int, default=256, help="GIF palette size 2-256 (default: 256)")
    parser.add_argument("--quality", type=int, default=75, help="WebP quality 0-100 (default: 75)")
    args = parser.parse_args()

    require_ffmpeg()
    if not args.input.exists():
        die(f"input not found: {args.input}")
    if args.fps <= 0:
        die("--fps must be > 0")
    if args.max_colors < 2 or args.max_colors > 256:
        die("--max-colors must be between 2 and 256")
    if args.quality < 0 or args.quality > 100:
        die("--quality must be between 0 and 100")

    output_format = args.output_format or args.output.suffix.lower().lstrip(".")
    if output_format not in {"gif", "webp"}:
        die("output extension must be .gif or .webp, or pass --output-format")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    if output_format == "gif":
        convert_gif(args)
    else:
        convert_webp(args)

    size = args.output.stat().st_size if args.output.exists() else 0
    print(f"wrote {args.output} ({size / 1024:.1f} KiB)")


if __name__ == "__main__":
    main()
