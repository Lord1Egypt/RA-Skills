#!/usr/bin/env python3
"""Remove watermarks from white-background document images.

Supports two modes:
1. Region mode (--region): only process a specific area, leave the rest untouched
2. Full mode (default): process the entire image with text-aware watermark removal

After removal, optionally enhances text contrast (--enhance).
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageFilter
    import numpy as np
except ImportError:
    print("Missing dependencies. Install with: pip install Pillow numpy")
    sys.exit(1)

try:
    from scipy.ndimage import binary_dilation, gaussian_filter
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}

# Region presets: (y_start%, y_end%, x_start%, x_end%) as fractions of image size
REGION_PRESETS = {
    "bottom-right": (0.85, 1.0, 0.55, 1.0),
    "bottom-left":  (0.85, 1.0, 0.0, 0.45),
    "top-right":    (0.0, 0.15, 0.55, 1.0),
    "top-left":     (0.0, 0.15, 0.0, 0.45),
    "bottom":       (0.85, 1.0, 0.0, 1.0),
    "top":          (0.0, 0.15, 0.0, 1.0),
    "right":        (0.0, 1.0, 0.75, 1.0),
    "left":         (0.0, 1.0, 0.0, 0.25),
    "center":       (0.3, 0.7, 0.2, 0.8),
    "full":         (0.0, 1.0, 0.0, 1.0),
}


def parse_args():
    p = argparse.ArgumentParser(
        description="Remove watermarks from document images",
        epilog="Region presets: " + ", ".join(REGION_PRESETS.keys()),
    )
    sub = p.add_subparsers(dest="command", help="Command to run")

    # --- analyze subcommand ---
    a = sub.add_parser("analyze", help="Analyze brightness distribution of a region")
    a.add_argument("input", help="Single image file to analyze")
    a.add_argument("--region", default="bottom-right",
                   help="Region to analyze. Preset or 'y0%%,y1%%,x0%%,x1%%' (default: bottom-right)")

    # --- remove subcommand ---
    r = sub.add_parser("remove", help="Remove watermarks from images")
    r.add_argument("input", nargs="+", help="Image files or a single directory")
    r.add_argument("-o", "--output", default=None, help="Output directory (default: <input>_clean/)")
    r.add_argument("--region", default="full",
                   help="Region to process. Preset or 'y0%%,y1%%,x0%%,x1%%' (default: full)")
    r.add_argument("--threshold", type=int, default=180,
                   help="Brightness threshold (0-255). (default: 180)")
    r.add_argument("--enhance", action="store_true", default=False,
                   help="Enhance text contrast after watermark removal")
    r.add_argument("--preview", action="store_true", help="Print stats without saving")

    return p.parse_args()


def parse_region(region_str):
    """Parse region string into (y0_frac, y1_frac, x0_frac, x1_frac)."""
    if region_str in REGION_PRESETS:
        return REGION_PRESETS[region_str]
    try:
        parts = [float(x) / 100.0 for x in region_str.split(",")]
        if len(parts) == 4:
            return tuple(parts)
    except ValueError:
        pass
    print(f"Invalid region: {region_str}")
    print(f"Use a preset ({', '.join(REGION_PRESETS.keys())}) or 'y0%,y1%,x0%,x1%'")
    sys.exit(1)


def collect_files(inputs):
    """Resolve inputs to a list of image paths."""
    files = []
    for inp in inputs:
        p = Path(inp)
        if p.is_dir():
            files.extend(sorted(f for f in p.iterdir() if f.suffix.lower() in IMAGE_EXTS))
        elif p.is_file() and p.suffix.lower() in IMAGE_EXTS:
            files.append(p)
    return files


def remove_watermark_region(img, region, threshold=180):
    """Remove watermark only within the specified region.

    Pixels in the region with brightness >= threshold are set to white.
    Pixels outside the region are untouched.
    """
    arr = np.array(img, dtype=np.float32)
    h, w = arr.shape[:2]

    y0, y1, x0, x1 = region
    ry0, ry1 = int(h * y0), int(h * y1)
    rx0, rx1 = int(w * x0), int(w * x1)

    # Extract region
    region_arr = arr[ry0:ry1, rx0:rx1]
    if region_arr.ndim == 3:
        gray = np.mean(region_arr[:, :, :3], axis=2)
    else:
        gray = region_arr.copy()

    # Simple threshold for the region - anything above threshold becomes white
    mask = gray >= threshold

    if region_arr.ndim == 3:
        for c in range(region_arr.shape[2]):
            region_arr[:, :, c][mask] = 255
    else:
        region_arr[mask] = 255

    arr[ry0:ry1, rx0:rx1] = region_arr
    return Image.fromarray(arr.astype(np.uint8))


def remove_watermark_full(img, threshold=180):
    """Remove watermark from the entire image using text-aware approach.

    Two-pass strategy:
    1. Identify dark text pixels as anchors (brightness < dark_cutoff).
    2. Dilate anchor mask to protect anti-aliased edges.
    3. Mid-range pixels near text -> keep; isolated mid-range -> watermark.
    4. Pixels >= threshold -> always white.
    """
    if not HAS_SCIPY:
        print("Error: full mode requires scipy. Run with: uv run --with Pillow --with numpy --with scipy ...")
        sys.exit(1)

    arr = np.array(img, dtype=np.float32)

    if arr.ndim == 3:
        gray = np.mean(arr[:, :, :3], axis=2)
    else:
        gray = arr.copy()

    dark_cutoff = 120
    dark_mask = gray < dark_cutoff

    # Dilate to protect anti-aliased text edges
    struct = np.ones((13, 13), dtype=bool)
    near_text = binary_dilation(dark_mask, structure=struct, iterations=1)

    # Build alpha: 1 = white, 0 = keep
    alpha = np.zeros_like(gray)
    alpha[gray >= threshold] = 1.0

    # Isolated mid-range pixels -> watermark
    mid_range = (gray >= dark_cutoff) & (gray < threshold)
    alpha[mid_range & ~near_text] = 1.0

    # Smooth edges
    alpha = gaussian_filter(alpha, sigma=1.0)
    alpha = np.clip(alpha, 0, 1)

    if arr.ndim == 3:
        for c in range(arr.shape[2]):
            arr[:, :, c] = arr[:, :, c] * (1 - alpha) + 255 * alpha
    else:
        arr = arr * (1 - alpha) + 255 * alpha

    return Image.fromarray(arr.astype(np.uint8))


def enhance_text(img):
    """Enhance text contrast on white-background documents.

    Makes dark text darker and white background whiter, improving readability.
    """
    arr = np.array(img, dtype=np.float32)

    if arr.ndim == 3:
        gray = np.mean(arr[:, :, :3], axis=2)
    else:
        gray = arr.copy()

    # Apply a curve: darken dark pixels, brighten light pixels
    # Using a simple sigmoid-like contrast boost centered at midpoint
    midpoint = 180.0
    strength = 1.5  # >1 increases contrast

    # Normalize to 0-1
    normalized = gray / 255.0
    mid_norm = midpoint / 255.0

    # Apply contrast curve per channel
    if arr.ndim == 3:
        for c in range(arr.shape[2]):
            ch = arr[:, :, c] / 255.0
            # Boost contrast: pixels below midpoint get darker, above get lighter
            ch = mid_norm + (ch - mid_norm) * strength
            arr[:, :, c] = np.clip(ch * 255, 0, 255)
    else:
        arr = arr / 255.0
        arr = mid_norm + (arr - mid_norm) * strength
        arr = np.clip(arr * 255, 0, 255)

    return Image.fromarray(arr.astype(np.uint8))


def analyze_region(image_path, region):
    """Analyze brightness distribution of a specific region in an image.

    Prints a summary to help determine the right threshold for watermark removal.
    """
    img = Image.open(image_path).convert("RGB")
    arr = np.array(img)
    h, w = arr.shape[:2]

    y0, y1, x0, x1 = region
    ry0, ry1 = int(h * y0), int(h * y1)
    rx0, rx1 = int(w * x0), int(w * x1)

    region_arr = arr[ry0:ry1, rx0:rx1]
    gray = np.mean(region_arr, axis=2) if region_arr.ndim == 3 else region_arr.astype(float)

    total = gray.size
    print(f"Image: {image_path} ({w}x{h})")
    print(f"Region: y=[{ry0}:{ry1}] x=[{rx0}:{rx1}] ({rx1-rx0}x{ry1-ry0} pixels)")
    print()
    print("Brightness distribution:")

    ranges = [
        (0, 50, "black/dark text"),
        (50, 100, "dark gray"),
        (100, 130, "medium gray"),
        (130, 160, "light gray"),
        (160, 190, "very light"),
        (190, 220, "near white"),
        (220, 256, "white/background"),
    ]
    for lo, hi, label in ranges:
        count = int(np.sum((gray >= lo) & (gray < hi)))
        pct = count / total * 100
        bar = "#" * int(pct)
        print(f"  {lo:3d}-{hi:<3d} ({label:16s}): {count:>7d} ({pct:5.1f}%) {bar}")

    print()
    print("Suggested threshold:")
    # Find the gap between text and background
    non_white = gray[gray < 240]
    if len(non_white) > 0:
        p75 = np.percentile(non_white, 75)
        p90 = np.percentile(non_white, 90)
        print(f"  Non-white P75={p75:.0f}, P90={p90:.0f}")
        suggested = max(50, int(p75 - 10))
        print(f"  Suggested: --threshold {suggested}")
        print(f"  (This would remove {np.sum(gray >= suggested) / total * 100:.1f}% of region pixels)")
    else:
        print("  Region is almost entirely white - no watermark detected.")


def main():
    args = parse_args()

    if args.command == "analyze":
        region = parse_region(args.region)
        analyze_region(args.input, region)
        return

    if args.command != "remove":
        print("Usage: remove_watermark.py {analyze|remove} ...")
        sys.exit(1)

    files = collect_files(args.input)
    if not files:
        print("No image files found.")
        sys.exit(1)

    region = parse_region(args.region)
    is_full = (args.region == "full")

    # Determine output directory
    if args.output:
        out_dir = Path(args.output)
    else:
        first_input = Path(args.input[0])
        parent = first_input if first_input.is_dir() else first_input.parent
        out_dir = parent.parent / (parent.name + "_clean")

    if not args.preview:
        out_dir.mkdir(parents=True, exist_ok=True)

    mode_desc = "full image" if is_full else f"region={args.region}"
    print(f"Processing {len(files)} images ({mode_desc}, threshold={args.threshold})...")

    for f in files:
        img = Image.open(f).convert("RGB")

        if is_full:
            cleaned = remove_watermark_full(img, args.threshold)
        else:
            cleaned = remove_watermark_region(img, region, args.threshold)

        if args.enhance:
            cleaned = enhance_text(cleaned)

        if args.preview:
            orig_arr = np.array(img)
            clean_arr = np.array(cleaned)
            changed = np.sum(np.any(orig_arr != clean_arr, axis=2))
            total = orig_arr.shape[0] * orig_arr.shape[1]
            print(f"  {f.name}: {changed}/{total} pixels changed ({changed/total*100:.1f}%)")
        else:
            out_path = out_dir / f.name
            cleaned.save(out_path, quality=95)

    if args.preview:
        print("Preview mode - no files saved.")
    else:
        print(f"Done: {len(files)} images -> {out_dir}")


if __name__ == "__main__":
    main()
