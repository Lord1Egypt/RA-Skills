#!/usr/bin/env python3
"""
animate_shake.py — Generate shake/vibrate animation frames from a sticker PNG.

Shake: rapid left-right jitter with slight rotation, feels hype/energetic.
Default: 24 fps, 1.0 second, ~10px jitter.

Usage:
    python3 animate_shake.py <sticker.png> [--fps 24] [--duration 1.0] [--intensity 10] [--outdir frames_shake]

Outputs frame PNGs to <outdir>/ (created if missing).
Feed the frames to make_webm.py to produce the final WebM.
"""

import math
import argparse
from pathlib import Path
from PIL import Image


def animate_shake(
    sticker_path: str,
    outdir: str = "frames_shake",
    fps: int = 24,
    duration: float = 1.0,
    intensity: float = 10.0,
) -> str:
    src = Path(sticker_path)
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    img = Image.open(src).convert("RGBA")
    W, H = img.size
    n_frames = int(fps * duration)

    for i in range(n_frames):
        t = i / n_frames
        # Fast oscillation (4 shakes per second)
        phase = 2 * math.pi * t * 4
        dx = int(intensity * math.sin(phase))
        angle = 2.0 * math.sin(phase)  # subtle tilt to sell the shake

        rotated = img.rotate(
            -angle,
            resample=Image.BICUBIC,
            center=(W // 2, H // 2),
            expand=False,
        )
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        canvas.paste(rotated, (dx, 0), rotated)

        # PNG enforced — never change these.
        frame_path = out / f"frame_{i:03d}.png"
        canvas.save(frame_path, "PNG")

    print(f"Generated {n_frames} shake frames in '{outdir}/'")
    return str(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate shake animation frames.")
    parser.add_argument("sticker", help="Input sticker PNG (512x512, transparent bg)")
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--duration", type=float, default=1.0)
    parser.add_argument("--intensity", type=float, default=10.0)
    parser.add_argument("--outdir", default="frames_shake")
    args = parser.parse_args()

    animate_shake(
        sticker_path=args.sticker,
        outdir=args.outdir,
        fps=args.fps,
        duration=args.duration,
        intensity=args.intensity,
    )
