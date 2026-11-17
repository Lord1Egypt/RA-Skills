#!/usr/bin/env python3
"""Build legible contact sheets from rendered page PNGs for complete-page QA."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("render_dir", type=Path)
    parser.add_argument("output_png", type=Path)
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--thumb-width", type=int, default=300)
    parser.add_argument("--pages-per-sheet", type=int, default=20)
    args = parser.parse_args()

    pages = sorted(args.render_dir.glob("page-*.png"))
    if not pages:
        raise SystemExit("no page-*.png files found")
    font = ImageFont.load_default()
    outputs = []
    for group_index in range(0, len(pages), args.pages_per_sheet):
        group = pages[group_index:group_index + args.pages_per_sheet]
        samples = []
        for path in group:
            with Image.open(path) as image:
                ratio = args.thumb_width / image.width
                thumb = image.convert("RGB").resize((args.thumb_width, round(image.height * ratio)))
                samples.append((path, thumb))
        cell_height = max(image.height for _, image in samples) + 28
        rows = math.ceil(len(samples) / args.columns)
        sheet = Image.new("RGB", (args.columns * args.thumb_width, rows * cell_height), "#d9d9d9")
        draw = ImageDraw.Draw(sheet)
        for index, (path, image) in enumerate(samples):
            x = (index % args.columns) * args.thumb_width
            y = (index // args.columns) * cell_height
            sheet.paste(image, (x, y + 20))
            draw.text((x + 5, y + 3), path.stem, fill="black", font=font)
        suffix = "" if len(pages) <= args.pages_per_sheet else f"_{group_index // args.pages_per_sheet + 1:02d}"
        target = args.output_png.with_name(args.output_png.stem + suffix + args.output_png.suffix)
        target.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(target)
        outputs.append(str(target))
    print("\n".join(outputs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

