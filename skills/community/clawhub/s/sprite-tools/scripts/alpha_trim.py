#!/usr/bin/env python3
"""
alpha_trim.py — Trim transparent borders from PNG images using alpha channel.

Usage:
  python3 alpha_trim.py <input.png> <output.png> [--batch] [--pad N]

  # Single file
  python3 alpha_trim.py /tmp/icon.png /tmp/icon_nobg.png

  # Batch: input is a directory
  python3 alpha_trim.py /tmp/icons/ /tmp/icons_nobg/ --batch --pad 4
"""

import sys
import os
from pathlib import Path
from PIL import Image


def trim_alpha(input_path, output_path, pad=0):
    """Crop to bounding box of non-zero-alpha pixels, optionally add padding."""
    img = Image.open(input_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    arr = Image.open(input_path).convert('RGBA')
    px = arr.load()
    w, h = arr.size

    # Find bounding box of non-transparent pixels
    bbox = None
    for y in range(h):
        for x in range(w):
            if px[x, y][3] > 0:
                if bbox is None:
                    bbox = [x, y, x, y]
                else:
                    bbox[0] = min(bbox[0], x)
                    bbox[1] = min(bbox[1], y)
                    bbox[2] = max(bbox[2], x)
                    bbox[3] = max(bbox[3], y)

    if bbox is None:
        print(f"  ⚠️  No opaque pixels found in {input_path}, saving as-is")
        img.save(output_path)
        return

    # Apply padding
    x1 = max(0, bbox[0] - pad)
    y1 = max(0, bbox[1] - pad)
    x2 = min(w, bbox[2] + 1 + pad)
    y2 = min(h, bbox[3] + 1 + pad)

    cropped = img.crop((x1, y1, x2, y2))
    cropped.save(output_path)
    orig_size = img.size
    new_size = cropped.size
    print(f"  ✅ {Path(input_path).name}: {orig_size[0]}x{orig_size[1]} → {new_size[0]}x{new_size[1]}  (pad={pad})")


def process_batch(input_dir, output_dir, pad=0):
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
        trim_alpha(str(f), str(out), pad)


if __name__ == "__main__":
    args = sys.argv[1:]

    pad = 0
    batch = False

    # Parse --pad and --batch flags
    clean_args = []
    i = 0
    while i < len(args):
        if args[i] == '--pad' and i + 1 < len(args):
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
        process_batch(input_path, output_path, pad)
    else:
        trim_alpha(input_path, output_path, pad)