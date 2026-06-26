#!/usr/bin/env python3
"""
Signature Extractor — extract signature ink from photos, remove background,
upscale resolution, and solidify ink strokes.

Modes:
  extract    — Remove background, keep black ink as semi-transparent alpha
  hd         — 3x upscale + sharpen + extract (higher resolution)
  solid      — 3x upscale + sharpen + extract + solid black alpha (no transparency)

Usage:
  python3 extract_signature.py <input_path> <output_path> [--mode extract|hd|solid] [--scale N]
"""

import argparse
import sys
from PIL import Image, ImageFilter
import numpy as np


def extract_ink(data, dark_threshold=90, dilation=1, solid=False, smooth=True):
    """
    Extract black ink pixels from image data.

    Args:
        data: numpy float32 array (H, W, 3) in RGB
        dark_threshold: brightness threshold for ink detection
        dilation: MaxFilter kernel size for filling gaps
        solid: if True, alpha = 255 for all ink pixels; else alpha varies by brightness
        smooth: if True, apply SMOOTH filter to alpha channel

    Returns:
        RGBA uint8 numpy array (H, W, 4)
    """
    R, G, B = data[:, :, 0], data[:, :, 1], data[:, :, 2]

    brightness = 0.299 * R + 0.587 * G + 0.114 * B

    # Saturation
    cmax = np.maximum(np.maximum(R, G), B)
    cmin = np.minimum(np.minimum(R, G), B)
    with np.errstate(divide="ignore", invalid="ignore"):
        saturation = np.where(cmax > 0, (cmax - cmin) / cmax, 0)

    # Black ink criteria: dark, not reddish, low saturation
    is_dark = brightness < dark_threshold
    is_not_red = (R - G) < 40
    is_low_sat = saturation < 0.6
    is_black_ink = is_dark & is_not_red & is_low_sat

    alpha = np.zeros((data.shape[0], data.shape[1]), dtype=np.uint8)
    if solid:
        alpha[is_black_ink] = 255
    else:
        grad = np.clip((dark_threshold - brightness) / dark_threshold * 255, 0, 255).astype(np.uint8)
        alpha[is_black_ink] = grad[is_black_ink]

    result = np.zeros((data.shape[0], data.shape[1], 4), dtype=np.uint8)
    result[:, :, 3] = alpha

    out = Image.fromarray(result, "RGBA")
    r, g, b, a = out.split()

    # Fill small gaps in the ink stroke
    if dilation > 0:
        for _ in range(dilation):
            a = a.filter(ImageFilter.MaxFilter(3))

    # Smooth jagged edges
    if smooth:
        a = a.filter(ImageFilter.SMOOTH)

    return np.array(Image.merge("RGBA", (r, g, b, a)), dtype=np.uint8)


def process(input_path, output_path, mode="solid", scale=3):
    """
    Main processing pipeline.

    Args:
        input_path: path to input image (JPG/PNG/etc.)
        output_path: path for output PNG
        mode: "extract" | "hd" | "solid"
        scale: upscale factor (used in hd and solid modes)
    """
    img = Image.open(input_path).convert("RGB")
    print(f"Input: {input_path} ({img.size[0]}x{img.size[1]})")

    if mode in ("hd", "solid"):
        # Upscale
        new_size = (img.size[0] * scale, img.size[1] * scale)
        img = img.resize(new_size, Image.LANCZOS)
        print(f"Upscaled to: {new_size[0]}x{new_size[1]} (x{scale})")

        # Sharpen
        img = img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=150, threshold=3))
        print("Sharpened")

    data = np.array(img, dtype=np.float32)

    ink_solid = (mode == "solid")
    result = extract_ink(
        data,
        dark_threshold=90 if mode in ("hd", "solid") else 80,
        dilation=1 if mode == "solid" else 0,
        solid=ink_solid,
        smooth=True,
    )

    out_img = Image.fromarray(result, "RGBA")
    out_img.save(output_path, optimize=True)

    ink_px = np.sum(np.array(out_img.split()[3]) > 0)
    print(f"Ink pixels: {ink_px}")
    print(f"Output: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract clean signature ink from photos with transparent background."
    )
    parser.add_argument("input", help="Path to input image")
    parser.add_argument("output", help="Path to output PNG")
    parser.add_argument(
        "--mode", choices=["extract", "hd", "solid"], default="solid",
        help="Processing mode: extract (basic), hd (upscale+extract), solid (upscale+deep black, default)"
    )
    parser.add_argument("--scale", type=int, default=3, help="Upscale factor for hd/solid modes (default: 3)")

    args = parser.parse_args()
    process(args.input, args.output, mode=args.mode, scale=args.scale)


if __name__ == "__main__":
    main()
