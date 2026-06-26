#!/usr/bin/env python3
"""
make_sticker.py — Convert any image to a Telegram-ready static sticker (512x512 PNG, transparent bg).

Usage:
    python3 make_sticker.py <input_image> [output.png]

Output defaults to <input_stem>_sticker.png in the same directory.
"""

import sys
from pathlib import Path
from PIL import Image
import rembg

def _enforce_png_ext(path: str) -> str:
    """Guarantee the output path has a .png extension — no exceptions."""
    p = Path(path)
    if p.suffix.lower() != ".png":
        p = p.with_suffix(".png")
        print(f"NOTE: Output extension changed to .png → {p}")
    return str(p)


def make_sticker(input_path: str, output_path: str = None) -> str:
    src = Path(input_path)
    if output_path is None:
        output_path = str(src.parent / f"{src.stem}_sticker.png")

    # Static stickers MUST be PNG — enforce the extension regardless of what was passed in.
    output_path = _enforce_png_ext(output_path)

    # Load and remove background
    with open(src, "rb") as f:
        raw = f.read()

    result_bytes = rembg.remove(raw, model="u2net")

    from io import BytesIO
    img = Image.open(BytesIO(result_bytes)).convert("RGBA")

    # Crop to non-transparent bounding box
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    # Resize to fit within 512x512 preserving aspect ratio
    img.thumbnail((512, 512), Image.LANCZOS)

    # Paste centered on a 512x512 transparent canvas
    canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    x = (512 - img.width) // 2
    y = (512 - img.height) // 2
    canvas.paste(img, (x, y), img)

    # Explicit format="PNG" — never infer from extension, always write PNG.
    canvas.save(output_path, "PNG", optimize=True)

    size_kb = Path(output_path).stat().st_size / 1024
    print(f"Saved: {output_path} ({size_kb:.1f} KB)")
    if size_kb > 512:
        print("WARNING: File exceeds 512KB — Telegram may reject it.")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    make_sticker(inp, out)
