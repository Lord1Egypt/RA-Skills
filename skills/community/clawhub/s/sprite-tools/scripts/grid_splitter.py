#!/usr/bin/env python3
"""
grid_splitter.py — Split Codex batch output grid into individual sprites.

Usage:
  python3 grid_splitter.py <input_image> <layout> [output_dir]
  python3 grid_splitter.py /tmp/batch.png 2x3 /tmp/icons/

Layout: rows x cols, e.g. 2x3 (2 rows, 3 cols), 3x2, 2x2, 4x3, etc.
Output: sprite_00.png, sprite_01.png, ... (row-major order: left-to-right, top-to-bottom)
"""

import sys
import os
from pathlib import Path
from PIL import Image


def split_grid(input_path, layout, output_dir):
    rows, cols = map(int, layout.lower().split('x'))
    img = Image.open(input_path)
    w, h = img.size
    cell_w = w // cols
    cell_h = h // rows

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for r in range(rows):
        for c in range(cols):
            left = c * cell_w
            upper = r * cell_h
            right = left + cell_w
            lower = upper + cell_h
            cell = img.crop((left, upper, right, lower))
            out_name = output_dir / f"sprite_{count:02d}.png"
            cell.save(out_name)
            print(f"  [{r},{c}] → {out_name.name}  ({cell_w}x{cell_h})")
            count += 1

    print(f"\n✅ Split {input_path} ({w}x{h}, {layout}) → {count} sprites in {output_dir}/")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    input_path = sys.argv[1]
    layout = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "/tmp/sprite_out/"
    split_grid(input_path, layout, output_dir)