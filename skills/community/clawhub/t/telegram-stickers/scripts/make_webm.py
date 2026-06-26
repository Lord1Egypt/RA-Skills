#!/usr/bin/env python3
"""
make_webm.py — Convert a directory of PNG frames into a Telegram-ready video sticker (WebM).

Telegram video sticker requirements:
  - VP9 codec, 512x512, max 3 seconds, max 256KB, transparent background (yuva420p)

Usage:
    python3 make_webm.py <frames_dir> [output.webm] [--fps 24] [--duration 2.0]

<frames_dir> must contain files named frame_000.png, frame_001.png, ...
Output defaults to <frames_dir>.webm

After encoding, optionally uploads to tmpfiles.org and prints a direct download URL.
"""

import sys
import subprocess
import argparse
import json
import urllib.request
from pathlib import Path


def make_webm(
    frames_dir: str,
    output_path: str = None,
    fps: int = 24,
    duration: float = None,
    upload: bool = True,
) -> str:
    frames = Path(frames_dir)
    if output_path is None:
        output_path = str(frames.parent / f"{frames.name}.webm")

    # Count frames to auto-detect duration if not given
    frame_files = sorted(frames.glob("frame_*.png"))
    if not frame_files:
        print(f"ERROR: No frame_*.png files found in '{frames_dir}'")
        sys.exit(1)

    if duration is None:
        duration = len(frame_files) / fps

    if duration > 3.0:
        print(f"WARNING: Duration {duration:.2f}s exceeds 3s limit — Telegram will reject the sticker.")

    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", str(frames / "frame_%03d.png"),
        "-c:v", "libvpx-vp9",
        "-pix_fmt", "yuva420p",
        "-b:v", "400k",
        "-vf", "scale=512:512",
        "-an",
        "-t", str(duration),
        output_path,
    ]
    # NOTE: Do NOT add -loop 0 — that flag is for GIF, not WebM, and causes issues.

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("ffmpeg stderr:")
        print(result.stderr[-2000:])
        sys.exit(1)

    size_kb = Path(output_path).stat().st_size / 1024
    print(f"Output: {output_path} ({size_kb:.1f} KB)")
    if size_kb > 256:
        print("WARNING: File exceeds 256KB — Telegram may reject it. Try reducing duration or bitrate.")

    if upload:
        _upload(output_path)

    return output_path


def _upload(filepath: str):
    """Upload to tmpfiles.org and print a direct download URL."""
    print("Uploading to tmpfiles.org ...")
    try:
        with open(filepath, "rb") as f:
            data = f.read()

        boundary = "----FormBoundary7MA4YWxkTrZu0gW"
        filename = Path(filepath).name
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            f"Content-Type: video/webm\r\n\r\n"
        ).encode() + data + f"\r\n--{boundary}--\r\n".encode()

        req = urllib.request.Request(
            "https://tmpfiles.org/api/v1/upload",
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read())

        if payload.get("status") == "success":
            url = payload["data"]["url"]
            # Convert https://tmpfiles.org/XXXXXX/file.webm → https://tmpfiles.org/dl/XXXXXX/file.webm
            parts = url.split("tmpfiles.org/", 1)
            direct_url = parts[0] + "tmpfiles.org/dl/" + parts[1]
            print(f"Direct download URL: {direct_url}")
        else:
            print(f"Upload response: {payload}")
    except Exception as e:
        print(f"Upload failed: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Frames → Telegram WebM sticker")
    parser.add_argument("frames_dir", help="Directory containing frame_000.png ... files")
    parser.add_argument("output", nargs="?", help="Output .webm path (default: <frames_dir>.webm)")
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--duration", type=float, default=None, help="Override duration (seconds, max 3)")
    parser.add_argument("--no-upload", action="store_true", help="Skip tmpfiles.org upload")
    args = parser.parse_args()

    make_webm(
        frames_dir=args.frames_dir,
        output_path=args.output,
        fps=args.fps,
        duration=args.duration,
        upload=not args.no_upload,
    )
