#!/usr/bin/env python3
"""Transform a Google Maps screenshot into a Ghibli hand-drawn style map.

Uses Pillow filters to create a watercolor / pencil-sketch aesthetic
reminiscent of Studio Ghibli background art.

Usage:
    python3 stylize_map.py --input map_screenshot.png --output stylized_map.png
"""

import argparse
import json
import math
import os
import sys

from PIL import (
    Image,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageOps,
)


def _load_palette(palette_path=None):
    """Load the Ghibli color palette."""
    if palette_path is None:
        skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        palette_path = os.path.join(skill_dir, "assets", "ghibli_palette.json")
    with open(palette_path, "r") as f:
        return json.load(f)


def _hex_to_rgb(hex_str):
    """Convert '#RRGGBB' to (R, G, B) tuple."""
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i : i + 2], 16) for i in (0, 2, 4))


def _posterize(img, bits=5):
    """Reduce color depth for a flatter, illustration-like appearance."""
    return ImageOps.posterize(img.convert("RGB"), bits)


def _warm_color_shift(img, red_boost=15, blue_reduce=10):
    """Shift the overall color tone warmer (more red, less blue).

    Applies per-channel offset to create the warm, sunset-like palette
    characteristic of Ghibli backgrounds.
    """
    r, g, b = img.split()

    r = r.point(lambda v: min(255, v + red_boost))
    b = b.point(lambda v: max(0, v - blue_reduce))
    g = g.point(lambda v: min(255, v + 3))  # very slight green warmth

    return Image.merge("RGB", (r, g, b))


def _remap_colors(img, palette):
    """Approximate color remapping toward the Ghibli palette.

    This is a heuristic: we shift hue ranges toward target palette colors
    rather than doing exact color replacement, which preserves map detail.
    """
    pixels = img.load()
    width, height = img.size

    road_rgb = _hex_to_rgb(palette.get("road", "#C4A882"))
    water_rgb = _hex_to_rgb(palette.get("water", "#7EB8C9"))
    veg_rgb = _hex_to_rgb(palette.get("vegetation", "#8FB573"))
    building_rgb = _hex_to_rgb(palette.get("building", "#F5E6D0"))

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]

            # Heuristic classification based on dominant channel
            brightness = (r + g + b) / 3.0

            if brightness > 240:
                # Very bright → keep as-is (labels, white space)
                continue
            elif brightness < 40:
                # Very dark → soften to dark brown
                pixels[x, y] = (60, 50, 40)
            elif b > r and b > g and b > 100:
                # Blue-dominant → water
                blend = min(1.0, (b - max(r, g)) / 120.0)
                pixels[x, y] = (
                    int(r + (water_rgb[0] - r) * blend * 0.6),
                    int(g + (water_rgb[1] - g) * blend * 0.6),
                    int(b + (water_rgb[2] - b) * blend * 0.6),
                )
            elif g > r and g > b and g > 80:
                # Green-dominant → vegetation
                blend = min(1.0, (g - max(r, b)) / 80.0)
                pixels[x, y] = (
                    int(r + (veg_rgb[0] - r) * blend * 0.5),
                    int(g + (veg_rgb[1] - g) * blend * 0.5),
                    int(b + (veg_rgb[2] - b) * blend * 0.5),
                )
            elif abs(r - g) < 30 and abs(g - b) < 30 and 150 < brightness < 230:
                # Gray-ish mid tones → roads
                blend = 0.4
                pixels[x, y] = (
                    int(r + (road_rgb[0] - r) * blend),
                    int(g + (road_rgb[1] - g) * blend),
                    int(b + (road_rgb[2] - b) * blend),
                )
            elif r > 180 and g > 160 and b > 140:
                # Light warm tones → buildings
                blend = 0.3
                pixels[x, y] = (
                    int(r + (building_rgb[0] - r) * blend),
                    int(g + (building_rgb[1] - g) * blend),
                    int(b + (building_rgb[2] - b) * blend),
                )

    return img


def _watercolor_effect(img):
    """Apply blur + sharpen to simulate watercolor brush strokes."""
    blurred = img.filter(ImageFilter.GaussianBlur(radius=1.8))
    sharpened = ImageEnhance.Sharpness(blurred).enhance(1.5)
    return sharpened


def _edge_overlay(img, opacity=0.25):
    """Generate hand-drawn edge lines and overlay on the image.

    Uses edge detection to find contours, tints them sepia-brown,
    and composites at reduced opacity for a pencil-sketch look.
    """
    gray = img.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES)
    # Threshold to keep only strong edges
    edges = edges.point(lambda v: 255 if v > 40 else 0)
    # Soften slightly
    edges = edges.filter(ImageFilter.GaussianBlur(radius=0.5))

    # Create sepia-brown edge layer
    edge_layer = Image.new("RGB", img.size, (90, 70, 50))  # dark brown
    edge_alpha = edges.point(lambda v: int(v * opacity))
    edge_rgba = edge_layer.copy()
    edge_rgba.putalpha(edge_alpha)

    result = img.convert("RGBA")
    result = Image.alpha_composite(result, edge_rgba)
    return result.convert("RGB")


def _apply_vignette(img, strength=0.35):
    """Apply a subtle vignette (darkened edges) for a storybook feel."""
    width, height = img.size
    vignette = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(vignette)

    cx, cy = width // 2, height // 2
    max_radius = math.sqrt(cx * cx + cy * cy)

    # Draw concentric ellipses from white (center) to black (edges)
    steps = 80
    for i in range(steps):
        t = i / float(steps)
        # Smooth falloff curve
        brightness = int(255 * (1.0 - (t ** 2.5) * strength))
        rx = int(cx * (1 - t * 0.3) + (width // 2) * t * 0.7)
        ry = int(cy * (1 - t * 0.3) + (height // 2) * t * 0.7)
        draw.ellipse(
            [cx - rx, cy - ry, cx + rx, cy + ry],
            fill=brightness,
        )

    # Blur the vignette mask for smoothness
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=40))

    # Apply: multiply the image by the vignette mask
    img_array = img.convert("RGB")
    r, g, b = img_array.split()
    r = Image.composite(r, Image.new("L", (width, height), 0), vignette)
    g = Image.composite(g, Image.new("L", (width, height), 0), vignette)
    b = Image.composite(b, Image.new("L", (width, height), 0), vignette)

    return Image.merge("RGB", (r, g, b))


def _reduce_saturation(img, factor=0.7):
    """Slightly desaturate to match the soft Ghibli watercolor palette."""
    return ImageEnhance.Color(img).enhance(factor)


def stylize(input_path, output_path, palette_path=None):
    """Run the full Ghibli stylization pipeline on a map screenshot.

    Pipeline:
    1. Posterize (flatten colors)
    2. Warm color shift
    3. Color remapping toward Ghibli palette
    4. Watercolor blur/sharpen effect
    5. Edge line overlay (pencil sketch)
    6. Desaturate slightly
    7. Vignette

    Args:
        input_path: Path to the Google Maps screenshot PNG.
        output_path: Path to write the stylized map PNG.
        palette_path: Optional path to ghibli_palette.json.

    Raises:
        FileNotFoundError: If input file doesn't exist.
        ValueError: If image processing fails.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    palette = _load_palette(palette_path)

    print(f"Loading map screenshot: {input_path}")
    try:
        img = Image.open(input_path).convert("RGB")
    except Exception as e:
        raise ValueError(f"Failed to load image: {e}")
    original_size = img.size
    print(f"  Image size: {original_size[0]}x{original_size[1]}")

    # For performance: process color remapping on a smaller version
    # then upscale back (pixel-level operations are slow on large images)
    process_size = (min(original_size[0], 1536), min(original_size[1], 1024))
    if img.size != process_size:
        img = img.resize(process_size, Image.LANCZOS)

    print("  Step 1/7: Posterizing...")
    img = _posterize(img, bits=5)

    print("  Step 2/7: Warm color shift...")
    img = _warm_color_shift(img, red_boost=12, blue_reduce=8)

    print("  Step 3/7: Color remapping to Ghibli palette...")
    img = _remap_colors(img, palette)

    print("  Step 4/7: Watercolor effect...")
    img = _watercolor_effect(img)

    print("  Step 5/7: Edge overlay (pencil lines)...")
    img = _edge_overlay(img, opacity=0.25)

    print("  Step 6/7: Desaturating...")
    img = _reduce_saturation(img, factor=0.75)

    print("  Step 7/7: Applying vignette...")
    img = _apply_vignette(img, strength=0.3)

    # Final brightness/contrast touch-up
    img = ImageEnhance.Brightness(img).enhance(1.05)
    img = ImageEnhance.Contrast(img).enhance(0.95)

    img.save(output_path, "PNG")
    print(f"Stylized map saved to: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Transform a Google Maps screenshot into Ghibli hand-drawn style"
    )
    parser.add_argument("--input", required=True, help="Input map screenshot PNG path")
    parser.add_argument("--output", required=True, help="Output stylized map PNG path")
    parser.add_argument("--palette", default=None, help="Path to ghibli_palette.json")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    try:
        result = stylize(args.input, args.output, args.palette)
        print(f"\n✓ Stylized map saved to: {result}")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
