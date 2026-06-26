#!/usr/bin/env python3
"""
batch_split.py — Full pipeline: background removal + grid split + alpha trim
For Codex batch output (dark slate background #1e2633).

Usage:
  python3 batch_split.py <input.png> <layout> [output_dir]
  python3 batch_split.py /tmp/batch.png 2x3 /tmp/icons/

Layout: rows x cols, e.g. "2x3" (2 rows, 3 cols), "3x2", "2x2", etc.
  First number = rows (vertical), second = cols (horizontal).
  Grid size in pixels: image_width/cols x image_height/rows
"""

import sys
import os
from pathlib import Path
from PIL import Image
import numpy as np


def make_bg_transparent(img, bg_color=(24, 35, 47), atol=20):
    arr = np.array(img.convert('RGBA'))
    bg = np.array(bg_color)
    diff = np.abs(arr[:,:,:3].astype(int) - bg)
    matches = np.all(diff <= atol, axis=2)
    arr[:,:,3] = np.where(matches, 0, 255)
    return Image.fromarray(arr, mode='RGBA')


def alpha_trim_cell(cell, pad=4):
    arr = np.array(cell)
    alpha = arr[:,:,3]
    rows_with = np.any(alpha > 0, axis=1)
    cols_with = np.any(alpha > 0, axis=0)
    if not rows_with.any() or not cols_with.any():
        return cell
    y1, y2 = np.where(rows_with)[0][[0, -1]]
    x1, x2 = np.where(cols_with)[0][[0, -1]]
    y1 = max(0, y1 - pad)
    y2 = min(cell.height - 1, y2 + pad)
    x1 = max(0, x1 - pad)
    x2 = min(cell.width - 1, x2 + pad)
    return cell.crop((x1, y1, x2+1, y2+1))


def split_and_trim(input_path, layout, output_dir):
    rows, cols = map(int, layout.lower().split('x'))
    
    img = Image.open(input_path)
    w, h = img.size
    cell_w, cell_h = w // cols, h // rows
    
    img_t = make_bg_transparent(img)
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    count = 0
    for r in range(rows):
        for c in range(cols):
            cx = c * cell_w
            cy = r * cell_h
            cell = img_t.crop((cx, cy, cx+cell_w, cy+cell_h))
            trimmed = alpha_trim_cell(cell)
            out_path = output_dir / f"sprite_{count:02d}.png"
            trimmed.save(out_path)
            print(f"  [{r},{c}] -> {out_path.name}  ({trimmed.width}x{trimmed.height})")
            count += 1
    
    print(f"\n✅ {input_path} ({w}x{h}, {layout}={rows}r{xcols}c, cell={cell_w}x{cell_h}) -> {count} sprites in {output_dir}/")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    input_path = sys.argv[1]
    layout = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "/tmp/sprite_out/"
    split_and_trim(input_path, layout, output_dir)
