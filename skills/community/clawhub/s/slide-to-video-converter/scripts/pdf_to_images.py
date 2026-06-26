#!/usr/bin/env python3
"""
Step 1: Convert PDF slides to high-resolution PNG images.

Usage:
    python scripts/pdf_to_images.py

Input:  slides/presentation.pdf
Output: output/images/slide_01.png, slide_02.png, ...
"""

import argparse
import sys
from pathlib import Path

from pdf2image import convert_from_path

from utils import PROJECT_ROOT, PDF_PATH, IMAGES_DIR, load_config


# ---- Load config (with fallback defaults) ----
try:
    _config = load_config()
    _image_cfg = _config.get("image", {})
except FileNotFoundError:
    _image_cfg = {}

# Quality presets (from config.json → image section)
PRESET_NORMAL = {
    "dpi": _image_cfg.get("dpi", 300),
    "width": _image_cfg.get("width", 1920),
    "height": _image_cfg.get("height", 1080),
}
PRESET_FAST = {
    "dpi": _image_cfg.get("dpi_fast", 150),
    "width": _image_cfg.get("width_fast", 1280),
    "height": _image_cfg.get("height_fast", 720),
}

# Output directory
OUTPUT_DIR = IMAGES_DIR


def pdf_to_images(fast: bool = False):
    """Convert each page of the PDF to a PNG image."""
    preset = PRESET_FAST if fast else PRESET_NORMAL
    dpi = preset["dpi"]
    target_w = preset["width"]
    target_h = preset["height"]

    # Validate input
    if not PDF_PATH.exists():
        print(f"Error: PDF not found at {PDF_PATH}")
        sys.exit(1)

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    mode_label = "⚡ FAST" if fast else "HQ"
    print(f"Converting: {PDF_PATH}")
    print(f"Output dir: {OUTPUT_DIR}")
    print(f"Mode: {mode_label} | DPI: {dpi}, Target: {target_w}x{target_h}")
    print("-" * 50)

    # Convert PDF to images
    images = convert_from_path(
        str(PDF_PATH),
        dpi=dpi,
        fmt="png",
    )

    print(f"Total pages: {len(images)}")

    for i, img in enumerate(images, start=1):
        # Resize to target resolution with high-quality resampling
        from PIL import Image
        img_resized = img.resize(
            (target_w, target_h),
            Image.LANCZOS,
        )

        # Save as PNG
        output_path = OUTPUT_DIR / f"slide_{i:02d}.png"
        img_resized.save(str(output_path), "PNG", optimize=True)

        # File size info
        size_kb = output_path.stat().st_size / 1024
        print(f"  ✅ Page {i:2d} -> {output_path.name} ({size_kb:.0f} KB)")

    print("-" * 50)
    print(f"Done! {len(images)} images saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF slides to images")
    parser.add_argument("--fast", action="store_true", help="Fast mode: lower DPI (150) and 720p resolution")
    args = parser.parse_args()
    pdf_to_images(fast=args.fast)