#!/usr/bin/env python3
"""
Extract evenly spaced frames from a video for agent vision review (Cursor / Claude Code).

Uses ffprobe for duration and ffmpeg for still frames. Writes manifest.json for each run.

Usage:
  python3 extract_verification_frames.py path/to/render.mp4
  python3 extract_verification_frames.py path/to/render.mp4 --count 10 --format png
  python3 extract_verification_frames.py path/to/render.mp4 --output-dir exports/verification/custom

(On many Linux/macOS systems only ``python3`` is available; use that if ``python`` is not found.)
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


# Reject paths that could break subprocess or confuse shells if ever wrapped.
_UNSAFE_PATH = re.compile(r"[;&|`$(){}\[\]!#~]")


def validate_media_path(path: str) -> Path:
    """Ensure the input path is safe and exists."""
    if _UNSAFE_PATH.search(path):
        raise ValueError(
            f"Invalid path {path!r}: contains disallowed shell metacharacters."
        )
    p = Path(path).resolve()
    if not p.is_file():
        raise FileNotFoundError(f"Video file not found: {p}")
    return p


def probe_duration_seconds(video: Path) -> float:
    """Return container duration in seconds via ffprobe."""
    if shutil.which("ffprobe") is None:
        raise RuntimeError("ffprobe not found on PATH. Install ffmpeg (includes ffprobe).")

    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(video),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr.strip() or result.stdout}")

    line = (result.stdout or "").strip().splitlines()[-1] if result.stdout else ""
    try:
        return max(0.0, float(line))
    except ValueError as exc:
        raise RuntimeError(f"Could not parse duration from ffprobe output: {line!r}") from exc


def default_output_dir(video: Path, cwd: Path) -> Path:
    """exports/verification/<stem>_<utc_timestamp>/ under cwd."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_stem = re.sub(r"[^\w.\-]+", "_", video.stem)[:80]
    out = cwd / "exports" / "verification" / f"{safe_stem}_{ts}"
    return out


def extract_frames(
    video: Path,
    out_dir: Path,
    count: int,
    image_format: str,
) -> tuple[list[dict], float]:
    """Extract ``count`` frames evenly from 0% to 100% (inclusive).

    Returns (manifest frame entries, duration_seconds).
    """
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg not found on PATH.")

    if count < 1:
        raise ValueError("count must be >= 1")

    duration = probe_duration_seconds(video)
    if duration <= 0:
        raise RuntimeError("Video duration is zero or unknown; cannot sample frames.")

    out_dir.mkdir(parents=True, exist_ok=True)
    ext = "png" if image_format.lower() == "png" else "jpg"

    entries: list[dict] = []
    for i in range(count):
        if count == 1:
            t = 0.0
            pct = 0.0
        else:
            pct = 100.0 * i / (count - 1)
            t = duration * (i / (count - 1))

        # Small inward clamp so -ss does not land past last frame on some files.
        t_safe = min(max(0.0, t), max(0.0, duration - 0.05))

        filename = f"frame_{i:02d}_t{t_safe:.3f}s_pct{pct:.1f}.{ext}"
        dest = out_dir / filename

        cmd = [
            "ffmpeg",
            "-y",
            "-ss",
            f"{t_safe:.6f}",
            "-i",
            str(video),
            "-vframes",
            "1",
            "-q:v",
            "2" if ext == "jpg" else "0",
            str(dest),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            raise RuntimeError(
                f"ffmpeg failed at t={t_safe}s: {result.stderr.strip() or result.stdout}"
            )

        entries.append(
            {
                "index": i,
                "t_seconds": round(t_safe, 4),
                "pct": round(pct, 2),
                "filename": filename,
            }
        )

    return entries, duration


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract verification frames from a video for multimodal agent review."
    )
    parser.add_argument("video", help="Path to MP4, GIF, or other ffmpeg-readable video")
    parser.add_argument(
        "--count",
        type=int,
        default=8,
        help="Number of evenly spaced frames (default: 8)",
    )
    parser.add_argument(
        "--format",
        choices=("jpg", "png"),
        default="jpg",
        help="Still image format (default: jpg)",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory (default: ./exports/verification/<stem>_<timestamp>/)",
    )
    parser.add_argument(
        "--cwd",
        default=".",
        help="Base path for default output-dir resolution (default: current directory)",
    )
    args = parser.parse_args()

    try:
        video = validate_media_path(args.video)
        cwd = Path(args.cwd).resolve()

        if args.output_dir:
            out_dir = Path(args.output_dir).resolve()
        else:
            out_dir = default_output_dir(video, cwd)

        entries, duration_sec = extract_frames(video, out_dir, args.count, args.format)

        manifest = {
            "video": str(video),
            "duration_seconds": round(duration_sec, 4),
            "frame_count": len(entries),
            "image_format": args.format,
            "output_dir": str(out_dir),
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "frames": entries,
        }

        (out_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2),
            encoding="utf-8",
        )

        print(f"Wrote {len(entries)} frames to {out_dir}")
        print(f"Manifest: {out_dir / 'manifest.json'}")
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
