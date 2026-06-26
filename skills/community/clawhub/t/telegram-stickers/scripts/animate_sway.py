#!/usr/bin/env python3
"""
animate_sway.py — Generate sway animation frames from a sticker PNG.

Sway: sine-wave horizontal translation + rotation anchored at the foot of the image.
Default: 24 fps, 2 seconds, ~18px shift, ~4 degrees max rotation.

Usage:
    python3 animate_sway.py <sticker.png> [--fps 24] [--duration 2.0] [--shift 18] [--angle 4] [--outdir frames_sway]

Outputs frame PNGs to <outdir>/ (created if missing).
Feed the frames to make_webm.py to produce the final WebM.
"""

import sys
import math
import argparse
from pathlib import Path
from PIL import Image


def animate_sway(
    sticker_path: str,
    outdir: str = "frames_sway",
    fps: int = 24,
    duration: float = 2.0,
    shift_px: float = 18.0,
    max_angle: float = 4.0,
) -> str:
    src = Path(sticker_path)
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    img = Image.open(src).convert("RGBA")
    W, H = img.size  # should be 512x512

    n_frames = int(fps * duration)
    # Anchor point at the bottom-center of the visible content
    bbox = img.getbbox()
    anchor_y = bbox[3] if bbox else H  # bottom of content

    for i in range(n_frames):
        t = i / n_frames  # 0..1 (exclusive)
        phase = 2 * math.pi * t  # full cycle

        dx = shift_px * math.sin(phase)
        angle = max_angle * math.sin(phase)

        # Rotate around foot anchor
        # Translate so anchor is at origin, rotate, translate back
        rotated = img.rotate(
            -angle,  # PIL rotates CCW, negative = CW for rightward lean
            resample=Image.BICUBIC,
            center=(W // 2, anchor_y),
            expand=False,
        )

        # Translate horizontally
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        canvas.paste(rotated, (int(round(dx)), 0), rotated)

        # PNG enforced: hardcoded extension + explicit format arg — never change these.
        frame_path = out / f"frame_{i:03d}.png"
        canvas.save(frame_path, "PNG")

    print(f"Generated {n_frames} sway frames in '{outdir}/'")
    return str(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate sway animation frames.")
    parser.add_argument("sticker", help="Input sticker PNG (512x512, transparent bg)")
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--duration", type=float, default=2.0)
    parser.add_argument("--shift", type=float, default=18.0, dest="shift_px")
    parser.add_argument("--angle", type=float, default=4.0, dest="max_angle")
    parser.add_argument("--outdir", default="frames_sway")
    args = parser.parse_args()

    animate_sway(
        sticker_path=args.sticker,
        outdir=args.outdir,
        fps=args.fps,
        duration=args.duration,
        shift_px=args.shift_px,
        max_angle=args.max_angle,
    )
