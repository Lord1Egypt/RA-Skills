#!/usr/bin/env python3
"""Tile multiple PNG/JPG images into a single PNG (for model/plot comparisons).

Usage:
  python tile_images.py --out tiled.png img1.png img2.png ...

Notes:
- Uses OpenCV; keeps aspect ratio; pads with white.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Tuple

import cv2
import numpy as np


def read_img(p: Path) -> np.ndarray:
    img = cv2.imread(str(p), cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {p}")
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if img.shape[2] == 4:
        # alpha -> white background
        alpha = img[:, :, 3:4].astype(np.float32) / 255.0
        rgb = img[:, :, :3].astype(np.float32)
        white = np.full_like(rgb, 255.0)
        rgb = rgb * alpha + white * (1.0 - alpha)
        img = rgb.astype(np.uint8)
    return img


def fit_to(img: np.ndarray, target_wh: Tuple[int, int]) -> np.ndarray:
    tw, th = target_wh
    h, w = img.shape[:2]
    scale = min(tw / w, th / h)
    nw, nh = int(round(w * scale)), int(round(h * scale))
    resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_AREA)
    canvas = np.full((th, tw, 3), 255, dtype=np.uint8)
    x0 = (tw - nw) // 2
    y0 = (th - nh) // 2
    canvas[y0 : y0 + nh, x0 : x0 + nw] = resized
    return canvas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--cols", type=int, default=2)
    ap.add_argument("--cell", type=str, default="1200x800", help="WxH")
    ap.add_argument("images", nargs="+")
    args = ap.parse_args()

    cw, ch = (int(x) for x in args.cell.lower().split("x"))
    cols = max(1, args.cols)

    imgs = [read_img(Path(p)) for p in args.images]
    n = len(imgs)
    rows = (n + cols - 1) // cols

    cells = [fit_to(im, (cw, ch)) for im in imgs]

    # pad last row
    while len(cells) < rows * cols:
        cells.append(np.full((ch, cw, 3), 255, dtype=np.uint8))

    grid_rows = []
    for r in range(rows):
        row = np.concatenate(cells[r * cols : (r + 1) * cols], axis=1)
        grid_rows.append(row)
    grid = np.concatenate(grid_rows, axis=0)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out), grid)


if __name__ == "__main__":
    main()
