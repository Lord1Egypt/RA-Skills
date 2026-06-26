#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a 320px thumbnail-size preview for cover readability checks.")
    parser.add_argument("cover", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--width", type=int, default=320)
    parser.add_argument("--force", action="store_true", help="Overwrite existing preview output")
    args = parser.parse_args()

    if not args.cover.exists():
        print(f"FAIL: missing cover {args.cover}")
        return 1
    output = args.out or args.cover.with_suffix(f".preview-{args.width}.jpg")
    if output.exists() and not args.force:
        print(f"FAIL: output already exists, choose a new version or pass --force: {output}")
        return 1
    image = Image.open(args.cover).convert("RGB")
    if image.width <= 0 or image.height <= 0:
        print("FAIL: invalid cover dimensions")
        return 1
    height = round(image.height * args.width / image.width)
    resized = image.resize((args.width, height), Image.Resampling.LANCZOS)
    output.parent.mkdir(parents=True, exist_ok=True)
    resized.save(output, quality=92)
    print(f"PASS: wrote cover preview {output} ({args.width}x{height})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
