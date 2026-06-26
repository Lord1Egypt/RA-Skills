#!/usr/bin/env python3
"""
animate_bounce.py — Generate bounce animation frames from a sticker PNG.

Bounce: abs(sin) vertical translation with subtle squash/stretch.
Default: 24 fps, 1.5 seconds, ~20px vertical travel.

Usage:
    python3 animate_bounce.py <sticker.png> [--fps 24] [--duration 1.5] [--height 20] [--outdir frames_bounce]

Outputs frame PNGs to <outdir>/ (created if missing).
Feed the frames to make_webm.py to produce the final WebM.
"""

import sys
import math
import argparse
from pathlib import Path
from PIL import Image


def animate_bounce(
    sticker_path: str,
    outdir: str = "frames_bounce",
    fps: int = 24,
    duration: float = 1.5,
    height_px: float = 20.0,
) -> str:
    src = Path(sticker_path)
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    img = Image.open(src).convert("RGBA")
    W, H = img.size

    n_frames = int(fps * duration)

    for i in range(n_frames):
        t = i / n_frames
        phase = 2 * math.pi * t

        # Vertical offset: abs(sin) so it bounces up and comes back down
        dy = -int(height_px * abs(math.sin(phase)))

        # Squash/stretch: slightly wide at bottom of bounce, slightly tall at top
        # At dy=0 (bottom) → squash; at peak → stretch
        bounce_ratio = abs(math.sin(phase))  # 0 at bottom, 1 at peak
        scale_y = 1.0 + 0.05 * bounce_ratio      # stretch up at peak
        scale_x = 1.0 - 0.03 * bounce_ratio      # slight squash horizontally at peak

        new_w = max(1, int(W * scale_x))
        new_h = max(1, int(H * scale_y))
        scaled = img.resize((new_w, new_h), Image.LANCZOS)

        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        paste_x = (W - new_w) // 2
        # Keep bottom of image pinned: bottom of scaled should stay at H
        paste_y = (H - new_h) + dy
        canvas.paste(scaled, (paste_x, paste_y), scaled)

        # PNG enforced: hardcoded extension + explicit format arg — never change these.
        frame_path = out / f"frame_{i:03d}.png"
        canvas.save(frame_path, "PNG")

    print(f"Generated {n_frames} bounce frames in '{outdir}/'")
    return str(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate bounce animation frames.")
    parser.add_argument("sticker", help="Input sticker PNG (512x512, transparent bg)")
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--duration", type=float, default=1.5)
    parser.add_argument("--height", type=float, default=20.0, dest="height_px")
    parser.add_argument("--outdir", default="frames_bounce")
    args = parser.parse_args()

    animate_bounce(
        sticker_path=args.sticker,
        outdir=args.outdir,
        fps=args.fps,
        duration=args.duration,
        height_px=args.height_px,
    )
