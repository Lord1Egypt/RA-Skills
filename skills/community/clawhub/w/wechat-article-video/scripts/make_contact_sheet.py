#!/usr/bin/env python3
"""Sample each scene at entry, midpoint, and exit into a labeled contact sheet."""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
]


def load_font(size: int):
    for candidate in FONT_CANDIDATES:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size, index=0)
    return ImageFont.load_default()


def probe_duration(video: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def sample_plan(timeline: dict | None, duration: float) -> list[tuple[float, str]]:
    samples: list[tuple[float, str]] = []
    if timeline and timeline.get("scenes"):
        for scene in timeline["scenes"]:
            start = float(scene["start_sec"])
            end = float(scene["end_sec"])
            span = max(end - start, 0.01)
            for ratio, label in ((0.1, "entry"), (0.5, "middle"), (0.9, "exit")):
                timestamp = min(start + span * ratio, max(end - 0.02, start))
                samples.append((timestamp, f"{scene['id']} {label} {timestamp:.2f}s"))
        return samples

    for index in range(9):
        ratio = index / 8 if index else 0
        timestamp = min(max(duration * ratio, 0.02), max(duration - 0.02, 0.02))
        samples.append((timestamp, f"sample {index + 1} {timestamp:.2f}s"))
    return samples


def extract_frame(video: Path, timestamp: float, destination: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-ss",
            f"{timestamp:.3f}",
            "-i",
            str(video),
            "-frames:v",
            "1",
            "-vf",
            "scale=270:480:force_original_aspect_ratio=decrease",
            str(destination),
        ],
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, type=Path)
    parser.add_argument("--timeline", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--columns", type=int, default=3)
    args = parser.parse_args()

    duration = probe_duration(args.video)
    timeline = None
    if args.timeline:
        timeline = json.loads(args.timeline.read_text(encoding="utf-8"))
    samples = sample_plan(timeline, duration)

    tile_width, image_height, label_height = 270, 480, 42
    tile_height = image_height + label_height
    columns = max(1, args.columns)
    rows = math.ceil(len(samples) / columns)
    sheet = Image.new("RGB", (columns * tile_width, rows * tile_height), "#E8EEF2")
    draw = ImageDraw.Draw(sheet)
    font = load_font(18)

    with tempfile.TemporaryDirectory(prefix="wechat-video-contact-") as temp_dir:
        temp = Path(temp_dir)
        for index, (timestamp, label) in enumerate(samples):
            frame_path = temp / f"frame-{index:03d}.jpg"
            extract_frame(args.video, timestamp, frame_path)
            with Image.open(frame_path) as frame:
                tile = ImageOps.pad(
                    frame.convert("RGB"),
                    (tile_width, image_height),
                    color="#101820",
                    method=Image.Resampling.LANCZOS,
                )
            x = (index % columns) * tile_width
            y = (index // columns) * tile_height
            sheet.paste(tile, (x, y))
            draw.rectangle(
                (x, y + image_height, x + tile_width, y + tile_height),
                fill="#101820",
            )
            draw.text(
                (x + 10, y + image_height + 10),
                label,
                font=font,
                fill="#F4F7F8",
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output, quality=92)
    print(f"contact sheet: {len(samples)} frames -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
