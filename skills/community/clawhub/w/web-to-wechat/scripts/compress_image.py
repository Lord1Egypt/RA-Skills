#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compress_image.py — Compress images to meet WeChat size limits.

WeChat cover image limit: 64KB (for thumb_media_id upload)
WeChat content image limit: 1MB

Usage:
    python compress_image.py --input cover.png --output cover_compressed.jpg --max-size 64
    python compress_image.py --input photo.jpg --output photo_small.jpg --max-size 500 --max-width 1080

Dependencies: Pillow (auto-installed)
"""

import argparse
import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, Exception):
        pass

try:
    from PIL import Image
except ImportError:
    print("[INFO] Installing Pillow...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "-q"])
    from PIL import Image


def compress_image(
    input_path: str,
    output_path: str,
    max_size_kb: int = 64,
    max_width: int = 0,
    quality_start: int = 95,
    quality_min: int = 10,
    quality_step: int = 5,
) -> bool:
    """
    Compress an image to be under max_size_kb.

    Strategy:
    1. Resize if max_width is set and image is wider
    2. Convert to RGB (strip alpha for JPEG)
    3. Progressively reduce JPEG quality until under size limit
    4. If still too large, progressively downscale dimensions

    Returns True if successful, False otherwise.
    """
    img = Image.open(input_path)
    original_size = Path(input_path).stat().st_size
    print(f"[INPUT] {input_path}: {original_size / 1024:.1f} KB, {img.size[0]}x{img.size[1]}, mode={img.mode}")

    # Convert to RGB if necessary (JPEG doesn't support alpha)
    output_ext = Path(output_path).suffix.lower()
    if output_ext in (".jpg", ".jpeg"):
        if img.mode in ("RGBA", "P", "LA"):
            # Create white background for transparency
            bg = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            bg.paste(img, mask=img.split()[-1] if "A" in img.mode else None)
            img = bg
        elif img.mode != "RGB":
            img = img.convert("RGB")

    # Step 1: Resize if max_width specified
    if max_width > 0 and img.size[0] > max_width:
        ratio = max_width / img.size[0]
        new_height = int(img.size[1] * ratio)
        img = img.resize((max_width, new_height), Image.LANCZOS)
        print(f"[RESIZE] {img.size[0]}x{img.size[1]}")

    # Step 2: Progressive quality reduction
    quality = quality_start
    fmt = "JPEG" if output_ext in (".jpg", ".jpeg") else "PNG"

    while quality >= quality_min:
        if fmt == "JPEG":
            img.save(output_path, format=fmt, quality=quality, optimize=True)
        else:
            img.save(output_path, format=fmt, optimize=True)

        file_size = Path(output_path).stat().st_size
        size_kb = file_size / 1024

        if size_kb <= max_size_kb:
            print(f"[OK] Compressed to {size_kb:.1f} KB (quality={quality})")
            print(f"[INFO] Reduction: {original_size/1024:.1f} KB → {size_kb:.1f} KB ({(1 - size_kb/(original_size/1024))*100:.0f}%)")
            return True

        quality -= quality_step

    # Step 3: If still too large, downscale dimensions
    scale = 0.9
    while scale > 0.2:
        new_w = int(img.size[0] * scale)
        new_h = int(img.size[1] * scale)
        resized = img.resize((new_w, new_h), Image.LANCZOS)

        if fmt == "JPEG":
            resized.save(output_path, format=fmt, quality=quality_min, optimize=True)
        else:
            resized.save(output_path, format=fmt, optimize=True)

        file_size = Path(output_path).stat().st_size
        size_kb = file_size / 1024

        if size_kb <= max_size_kb:
            print(f"[OK] Compressed to {size_kb:.1f} KB (scaled to {new_w}x{new_h}, quality={quality_min})")
            print(f"[INFO] Reduction: {original_size/1024:.1f} KB → {size_kb:.1f} KB ({(1 - size_kb/(original_size/1024))*100:.0f}%)")
            return True

        scale -= 0.1

    # Failed
    final_size = Path(output_path).stat().st_size / 1024
    print(f"[ERROR] Could not compress below {max_size_kb} KB. Best: {final_size:.1f} KB")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Compress images to meet WeChat size limits",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compress cover to WeChat 64KB limit
  python compress_image.py --input cover.png --output cover.jpg --max-size 64

  # Compress content image with max width
  python compress_image.py --input photo.jpg --output photo_small.jpg --max-size 500 --max-width 1080

WeChat limits:
  Cover image (thumb_media_id): 64 KB
  Content images: 1 MB (1024 KB)
        """,
    )
    parser.add_argument("--input", required=True, help="Input image path")
    parser.add_argument("--output", required=True, help="Output image path (use .jpg for best compression)")
    parser.add_argument("--max-size", type=int, default=64, help="Max file size in KB (default: 64 for WeChat cover)")
    parser.add_argument("--max-width", type=int, default=0, help="Max width in pixels (0 = no limit)")
    parser.add_argument("--quality-start", type=int, default=95, help="Starting JPEG quality (default: 95)")
    parser.add_argument("--quality-min", type=int, default=10, help="Minimum JPEG quality (default: 10)")

    args = parser.parse_args()

    input_file = Path(args.input)
    if not input_file.exists():
        print(f"[ERROR] Input file not found: {args.input}")
        sys.exit(1)

    success = compress_image(
        str(input_file),
        args.output,
        max_size_kb=args.max_size,
        max_width=args.max_width,
        quality_start=args.quality_start,
        quality_min=args.quality_min,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
