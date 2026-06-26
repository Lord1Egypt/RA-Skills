#!/usr/bin/env python3
"""
color_trim.py — Crop fixed-color borders from images.
Uses the top-left pixel (0,0) as the border color, crops inward.

Usage:
  python3 color_trim.py <input.png> <output.png> [--atol N] [--batch] [--pad N]

  # White background (default atol=10)
  python3 color_trim.py /tmp/icon.png /tmp/icon_nobg.png

  # Gray background
  python3 color_trim.py /tmp/icon.png /tmp/icon_nobg.png --atol 20

  # Batch mode
  python3 color_trim.py /tmp/icons/ /tmp/icons_nobg/ --batch --atol 10 --pad 2
"""

import sys
import os
from pathlib import Path
import numpy as np
from PIL import Image


def trim_by_border_color(input_path, output_path, atol=10, pad=0):
    """Crop image by detecting border color from top-left corner."""
    img = Image.open(input_path)
    arr = np.array(img)
    h, w = arr.shape[:2]

    # Get border color from top-left pixel
    border_color = tuple(arr[0, 0])
    if len(border_color) == 4 and arr.shape[2] == 4:
        # RGBA: compare RGB only for background detection
        border_rgb = border_color[:3]
    else:
        border_rgb = border_color[:3]

    # Build mask: pixels that differ from border (beyond atol)
    diff = np.abs(arr[:, :, :3].astype(int) - np.array(border_rgb).astype(int))
    mask = np.any(diff > atol, axis=2)

    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)

    if not rows.any() or not cols.any():
        print(f"  ⚠️  No content found in {input_path}, saving as-is")
        img.save(output_path)
        return

    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    x1 = max(0, cmin - pad)
    y1 = max(0, rmin - pad)
    x2 = min(w, cmax + 1 + pad)
    y2 = min(h, rmax + 1 + pad)

    cropped = img.crop((x1, y1, x2, y2))
    cropped.save(output_path)
    orig_size = img.size
    new_size = cropped.size
    border_hex = '#{:02x}{:02x}{:02x}'.format(*border_rgb)
    print(f"  ✅ {Path(input_path).name}: border={border_hex} atol={atol}, {orig_size[0]}x{orig_size[1]} → {new_size[0]}x{new_size[1]}")


def process_batch(input_dir, output_dir, atol=10, pad=0):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(input_dir.glob("*.png")) + sorted(input_dir.glob("*.jpg")) + sorted(input_dir.glob("*.webp"))
    if not files:
        print(f"  ⚠️  No images found in {input_dir}")
        return

    print(f"Batch: {len(files)} images → {output_dir}/")
    for f in files:
        out = output_dir / f.name
        trim_by_border_color(str(f), str(out), atol, pad)


if __name__ == "__main__":
    args = sys.argv[1:]

    atol = 10
    pad = 0
    batch = False

    i = 0
    clean_args = []
    while i < len(args):
        if args[i] == '--atol' and i + 1 < len(args):
            atol = int(args[i + 1])
            i += 2
        elif args[i] == '--pad' and i + 1 < len(args):
            pad = int(args[i + 1])
            i += 2
        elif args[i] == '--batch':
            batch = True
            i += 1
        else:
            clean_args.append(args[i])
            i += 1

    if len(clean_args) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = clean_args[0]
    output_path = clean_args[1]

    if batch:
        process_batch(input_path, output_path, atol, pad)
    else:
        trim_by_border_color(input_path, output_path, atol, pad)