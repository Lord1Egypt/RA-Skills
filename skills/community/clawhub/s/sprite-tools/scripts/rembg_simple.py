#!/usr/bin/env python3
"""
rembg_simple.py — Lightweight background removal via color distance.
No heavy ML models required. Based on superpixel-like color clustering.

Use when rembg is unavailable or for initial rough pass.

Usage:
  python3 rembg_simple.py <input.png> <output.png> [--strength 0.5] [--batch]

  # Single file
  python3 rembg_simple.py /tmp/hero.png /tmp/hero_nobg.png --strength 0.5

  # Batch
  python3 rembg_simple.py /tmp/batch/ /tmp/batch_nobg/ --batch --strength 0.5
"""

import sys
import os
from pathlib import Path
import numpy as np
from PIL import Image
from collections import deque


def flood_fill_mask(img_array, seed_x, seed_y, border_color, atol):
    """Flood fill from seed, return mask of border-colored regions."""
    h, w = img_array.shape[:2]
    visited = np.zeros((h, w), dtype=bool)
    mask = np.zeros((h, w), dtype=bool)
    queue = deque([(seed_x, seed_y)])

    while queue:
        x, y = queue.popleft()
        if visited[y, x]:
            continue
        visited[y, x] = True

        diff = np.abs(img_array[y, x, :3].astype(int) - np.array(border_color[:3]).astype(int))
        if np.all(diff <= atol):
            mask[y, x] = True
            if x > 0: queue.append((x-1, y))
            if x < w-1: queue.append((x+1, y))
            if y > 0: queue.append((x, y-1))
            if y < h-1: queue.append((x, y+1))

    return mask


def remove_background_simple(input_path, output_path, strength=0.5, atol_base=25):
    """
    Lightweight background removal:
    1. Detect border color from corners
    2. Flood-fill to find connected border region
    3. Use distance-from-border to create soft alpha
    """
    img = Image.open(input_path)
    arr = np.array(img)
    h, w = arr.shape[:2]

    # Detect border color from 4 corners
    corners = [
        tuple(arr[0, 0]),
        tuple(arr[0, w-1]),
        tuple(arr[h-1, 0]),
        tuple(arr[h-1, w-1]),
    ]
    # Most common corner color = background
    from collections import Counter
    corner_flat = [c[:3] for c in corners]
    border_color = Counter(corner_flat).most_common(1)[0][0]

    # Compute distance from border color
    diff = np.linalg.norm(arr[:, :, :3].astype(float) - np.array(border_color).astype(float), axis=2)
    max_dist = diff.max() if diff.max() > 0 else 1.0

    # Normalize distance → alpha
    normalized = diff / max_dist
    # Apply strength: higher strength = more aggressive (transparent more areas)
    threshold = 1.0 - strength
    alpha = np.where(normalized >= threshold, 255, (normalized / threshold * 255).astype(np.uint8))
    alpha = np.clip(alpha, 0, 255).astype(np.uint8)

    # Apply alpha channel
    if arr.shape[2] == 4:
        arr[:, :, 3] = alpha
    else:
        # Stack alpha
        arr_alpha = np.zeros((h, w, 4), dtype=arr.dtype)
        arr_alpha[:, :, :3] = arr[:, :, :3]
        arr_alpha[:, :, 3] = alpha
        arr = arr_alpha

    out_img = Image.fromarray(arr, mode='RGBA')
    out_img.save(output_path)

    # Stats
    n_transparent = int((alpha == 0).sum())
    n_opaque = int((alpha == 255).sum())
    print(f"  ✅ {Path(input_path).name}: {n_opaque} opaque / {n_transparent} transparent  (border=#{'{:02x}{:02x}{:02x}'.format(*map(int, border_color))}, strength={strength})")


def process_batch(input_dir, output_dir, strength=0.5):
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
        remove_background_simple(str(f), str(out), strength)


if __name__ == "__main__":
    args = sys.argv[1:]

    strength = 0.5
    batch = False

    i = 0
    clean_args = []
    while i < len(args):
        if args[i] == '--strength' and i + 1 < len(args):
            strength = float(args[i + 1])
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
        process_batch(input_path, output_path, strength)
    else:
        remove_background_simple(input_path, output_path, strength)