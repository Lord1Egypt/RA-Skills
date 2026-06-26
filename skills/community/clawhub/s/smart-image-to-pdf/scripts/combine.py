#!/usr/bin/env python3
"""Combine exam paper screenshots into a paginated A4 PDF.

- Trims whitespace borders from each image
- Scales all images to the same width (A4 printable width)
- Packs images tightly onto pages
- Smart page breaks: finds whitespace rows to avoid cutting text
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("Missing dependencies. Install with: pip install Pillow numpy")
    sys.exit(1)

def _a4_size(dpi):
    """Calculate A4 pixel dimensions for a given DPI."""
    return int(210 / 25.4 * dpi), int(297 / 25.4 * dpi)


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}


def parse_args():
    p = argparse.ArgumentParser(description="Combine images into a paginated A4 PDF")
    p.add_argument("input", nargs="+", help="Image files or a single directory")
    p.add_argument("-o", "--output", default=None, help="Output PDF path")
    p.add_argument("--margin", type=int, default=80, help="Page margin in px at 300dpi (default: 80, ~7mm)")
    p.add_argument("--dpi", type=int, default=300, help="Output DPI (default: 300)")
    p.add_argument("--sort", choices=["natural", "ctime", "name"], default="natural",
                   help="Sort order: natural (1,2,10), ctime (creation time), name (lexical) (default: natural)")
    p.add_argument("--no-trim", dest="trim", action="store_false", default=True, help="Disable whitespace trimming")
    return p.parse_args()


def _natural_sort_key(path):
    """Sort key that treats numeric parts as integers: 1, 2, 10 (not 1, 10, 2)."""
    parts = re.split(r'(\d+)', path.name)
    return [int(p) if p.isdigit() else p.lower() for p in parts]


def collect_files(inputs, sort_mode="natural"):
    """Resolve inputs to a sorted list of image paths."""
    files = []
    for inp in inputs:
        p = Path(inp)
        if p.is_dir():
            files.extend(f for f in p.iterdir() if f.suffix.lower() in IMAGE_EXTS)
        elif p.is_file() and p.suffix.lower() in IMAGE_EXTS:
            files.append(p)

    if sort_mode == "ctime":
        files.sort(key=lambda f: f.stat().st_birthtime if hasattr(f.stat(), 'st_birthtime') else f.stat().st_ctime)
    elif sort_mode == "name":
        files.sort()
    else:  # natural
        files.sort(key=_natural_sort_key)

    return files


def trim_whitespace(img, threshold=240, padding=10):
    """Trim white borders, keeping a small padding."""
    arr = np.array(img)
    if arr.ndim == 3:
        gray = arr.min(axis=2)
    else:
        gray = arr
    mask = gray < threshold
    if not mask.any():
        return img
    rows = mask.any(axis=1)
    cols = mask.any(axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    rmin = max(0, rmin - padding)
    rmax = min(img.height - 1, rmax + padding)
    cmin = max(0, cmin - padding)
    cmax = min(img.width - 1, cmax + padding)
    return img.crop((cmin, rmin, cmax + 1, rmax + 1))


def find_split_row(arr, target_y, search_up=300, search_down=50):
    """Find a whitespace row near target_y for a clean page break.

    Searches upward first (up to search_up px above target_y), then
    a small range below. Returns the best row index for splitting.
    """
    h = arr.shape[0]
    y_lo = max(0, target_y - search_up)
    y_hi = min(h, target_y + search_down)
    if y_lo >= y_hi:
        return target_y

    region = arr[y_lo:y_hi]
    if region.ndim == 3:
        row_means = region.mean(axis=(1, 2))
    else:
        row_means = region.mean(axis=1)

    white_mask = row_means > 252
    target_local = target_y - y_lo

    # Find consecutive white bands (>=3 rows) and pick the closest one
    best_y = None
    best_cost = float("inf")
    i = 0
    n = len(white_mask)
    while i < n:
        if white_mask[i]:
            band_start = i
            while i < n and white_mask[i]:
                i += 1
            band_end = i
            if band_end - band_start >= 3:
                mid = (band_start + band_end) // 2
                # Prefer bands above target (less wasted space)
                cost = abs(mid - target_local)
                if mid > target_local:
                    cost *= 3  # penalize going below
                if cost < best_cost:
                    best_cost = cost
                    best_y = mid
        else:
            i += 1

    if best_y is not None:
        return y_lo + best_y
    return target_y


def smart_split(img, max_h):
    """Split an oversized image into pieces that each fit within max_h,
    cutting only at whitespace rows."""
    pieces = []
    arr = np.array(img)
    offset = 0
    while offset < img.height:
        remaining = img.height - offset
        if remaining <= max_h:
            pieces.append(img.crop((0, offset, img.width, img.height)))
            break
        split_y = find_split_row(arr, offset + max_h)
        if split_y <= offset:
            split_y = offset + max_h  # fallback
        pieces.append(img.crop((0, offset, img.width, split_y)))
        offset = split_y
    return pieces


def place_image(img, arr, page, pages, y, margin, printable_h, a4_w, a4_h):
    """Place an image on pages, splitting at whitespace if it doesn't fit.

    Returns (page, y) for the current working page state.
    """
    offset = 0

    while offset < img.height:
        space = printable_h - (y - margin)
        remain = img.height - offset

        if remain <= space:
            # Rest fits on current page
            crop = img.crop((0, offset, img.width, img.height))
            page.paste(crop, (margin, y))
            y += crop.height
            break

        # Minimum useful space (~13mm at 300dpi); skip if too little
        if space < 150:
            pages.append(page)
            page = Image.new("RGB", (a4_w, a4_h), "white")
            y = margin
            continue

        # Find a whitespace row to split within available space
        split_y = find_split_row(arr, offset + space)

        if split_y <= offset + 50:
            # No good split near the top of remaining content; start new page
            pages.append(page)
            page = Image.new("RGB", (a4_w, a4_h), "white")
            y = margin
            continue

        crop = img.crop((0, offset, img.width, split_y))
        page.paste(crop, (margin, y))
        offset = split_y

        # Move to next page for the remainder
        pages.append(page)
        page = Image.new("RGB", (a4_w, a4_h), "white")
        y = margin

    return page, y


def combine(image_files, output_path, margin, do_trim, dpi):
    a4_w, a4_h = _a4_size(dpi)
    printable_w = a4_w - 2 * margin
    printable_h = a4_h - 2 * margin

    # Load, trim, scale
    scaled = []
    for f in image_files:
        img = Image.open(f).convert("RGB")
        if do_trim:
            img = trim_whitespace(img)
        scale = printable_w / img.width
        new_h = int(img.height * scale)
        img = img.resize((printable_w, new_h), Image.LANCZOS)
        scaled.append(img)

    # Pack images onto pages, splitting at whitespace when needed
    pages = []
    page = Image.new("RGB", (a4_w, a4_h), "white")
    y = margin

    for img in scaled:
        arr = np.array(img)
        page, y = place_image(img, arr, page, pages, y, margin, printable_h, a4_w, a4_h)

    if y > margin:
        pages.append(page)

    if not pages:
        print("No images to process.")
        return

    pages[0].save(
        output_path,
        save_all=True,
        append_images=pages[1:],
        resolution=dpi,
    )
    print(f"Done: {len(image_files)} images -> {len(pages)} pages -> {output_path}")


def main():
    args = parse_args()
    files = collect_files(args.input, args.sort)
    if not files:
        print("No image files found.")
        sys.exit(1)

    output = args.output
    if output is None:
        first_input = Path(args.input[0])
        parent = first_input if first_input.is_dir() else first_input.parent
        output = str(parent / "output.pdf")

    print(f"Processing {len(files)} images...")
    combine(files, output, args.margin, args.trim, args.dpi)


if __name__ == "__main__":
    main()
