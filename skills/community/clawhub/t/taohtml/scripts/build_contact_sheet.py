#!/usr/bin/env python3
"""Create a contact sheet from deck QA screenshots.

Requires Pillow:
  python -m pip install pillow
"""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a PNG contact sheet from screenshots.")
    parser.add_argument("input_dir", type=Path, help="Directory containing screenshots.")
    parser.add_argument("output", type=Path, help="Output PNG path.")
    parser.add_argument("--glob", default="*.png", help="Input glob. Default: *.png")
    parser.add_argument("--cols", type=int, default=3, help="Number of columns. Default: 3")
    parser.add_argument("--thumb-width", type=int, default=480, help="Thumbnail width. Default: 480")
    parser.add_argument("--gap", type=int, default=18, help="Gap between thumbnails. Default: 18")
    args = parser.parse_args()

    try:
        from PIL import Image, ImageDraw
    except ImportError as exc:
        raise SystemExit("Pillow is required. Install with: python -m pip install pillow") from exc

    files = sorted(p for p in args.input_dir.glob(args.glob) if p.is_file())
    if not files:
        raise SystemExit(f"No files matched {args.glob} in {args.input_dir}")

    thumbs = []
    for path in files:
        img = Image.open(path).convert("RGB")
        ratio = args.thumb_width / img.width
        size = (args.thumb_width, int(img.height * ratio))
        img = img.resize(size, Image.LANCZOS)
        thumbs.append((path.name, img))

    label_h = 26
    cell_w = args.thumb_width
    cell_h = max(img.height for _, img in thumbs) + label_h
    rows = (len(thumbs) + args.cols - 1) // args.cols
    sheet_w = args.cols * cell_w + (args.cols + 1) * args.gap
    sheet_h = rows * cell_h + (rows + 1) * args.gap
    sheet = Image.new("RGB", (sheet_w, sheet_h), "#f3f3ed")
    draw = ImageDraw.Draw(sheet)

    for i, (name, img) in enumerate(thumbs):
        col = i % args.cols
        row = i // args.cols
        x = args.gap + col * (cell_w + args.gap)
        y = args.gap + row * (cell_h + args.gap)
        draw.text((x, y), name, fill="#111111")
        sheet.paste(img, (x, y + label_h))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
