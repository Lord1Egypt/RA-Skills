#!/usr/bin/env python3
"""
Generate decorative images for WeChat article template:
1. Banner image (800×400) — deep dark gradient with stars
2. Divider image (600×6) — warm gold gradient line

Usage:
  python3 generate_images.py --output /tmp/
  # Creates banner.png and divider.png
"""

import argparse
import os
import struct
import zlib
import math
import random


def clamp(v):
    return max(0, min(255, int(v)))


def create_png(width, height, pixels):
    """Create a PNG from RGB pixel data."""
    def chunk(t, d):
        c = t + d
        return struct.pack(">I", len(d)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)

    sig = b"\x89PNG\r\n\x1a\n"
    raw = b""
    for y in range(height):
        raw += b"\x00"
        for x in range(width):
            r, g, b = pixels[y * width + x]
            raw += bytes([clamp(r), clamp(g), clamp(b)])

    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    idat = chunk(b"IDAT", zlib.compress(raw))
    iend = chunk(b"IEND", b"")
    return sig + ihdr + idat + iend


def generate_banner(width=800, height=400, seed=42):
    """Generate a dark banner image with subtle stars."""
    random.seed(seed)
    star_count = width * height // 5000  # ~64 stars

    # Pre-generate star positions using set for O(1) lookup
    stars = set()
    for _ in range(star_count):
        stars.add((random.randint(0, width - 1), random.randint(0, height * 3 // 5)))

    pixels = []
    for y in range(height):
        for x in range(width):
            ratio = y / height
            # Dark navy to deep purple gradient
            r = 15 + 25 * ratio
            g = 20 + 15 * ratio
            b = 50 + 30 * ratio

            # Draw stars
            if (x, y) in stars:
                r, g, b = 200, 200, 210
            else:
                # Check neighbors for star glow
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if (x + dx, y + dy) in stars and (dx != 0 or dy != 0):
                            dist = math.sqrt(dx * dx + dy * dy) / 2
                            br = int(80 * (1 - dist))
                            r += br
                            g += br
                            b += br

            # Subtle warm glow near bottom
            glow = max(0, 1 - abs(ratio - 0.85) * 5)
            r += 10 * glow
            g += 5 * glow
            b += 20 * glow

            pixels.append((clamp(r), clamp(g), clamp(b)))

    return create_png(width, height, pixels)


def generate_divider(width=600, height=6):
    """Generate a subtle warm gold divider line."""
    pixels = []
    center = width / 2
    for y in range(height):
        for x in range(width):
            dist = abs(x - center) / (width * 0.3)
            if dist < 0.6:
                v = 180
            elif dist < 1:
                v = int(180 * (1 - dist) * 2.5)
            else:
                v = 0
            # Warm gold color: rgba(212,165,116) approx
            r = clamp(v * 0.75)
            g = clamp(v * 0.55)
            b = clamp(v * 0.35)
            pixels.append((r, g, b))
    return create_png(width, height, pixels)


def generate_cover_circle(size=200, seed=42):
    """Generate a warm gold circle icon for cover."""
    random.seed(seed)
    pixels = []
    cx, cy = size // 2, size // 2
    for y in range(size):
        for x in range(size):
            dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2) / (size // 2)
            if dist < 1:
                v = int(255 * (1 - dist))
                r = v
                g = int(v * 0.75)
                b = int(v * 0.2)
            else:
                # Slightly warm off-white background
                r, g, b = 248, 245, 240
            pixels.append((clamp(r), clamp(g), clamp(b)))
    return create_png(size, size, pixels)


def main():
    parser = argparse.ArgumentParser(description="Generate WeChat article images")
    parser.add_argument("--output", default="/tmp", help="Output directory")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for banner stars")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    # Banner
    banner = generate_banner(seed=args.seed)
    banner_path = os.path.join(args.output, "banner.png")
    with open(banner_path, "wb") as f:
        f.write(banner)
    print(f"Banner: {banner_path} ({len(banner)} bytes)")

    # Divider
    divider = generate_divider()
    div_path = os.path.join(args.output, "divider.png")
    with open(div_path, "wb") as f:
        f.write(divider)
    print(f"Divider: {div_path} ({len(divider)} bytes)")

    # Cover circle
    cover = generate_cover_circle(seed=args.seed)
    cover_path = os.path.join(args.output, "cover.png")
    with open(cover_path, "wb") as f:
        f.write(cover)
    print(f"Cover: {cover_path} ({len(cover)} bytes)")


if __name__ == "__main__":
    main()
