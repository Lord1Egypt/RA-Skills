# -*- coding: utf-8 -*-
"""Build a preview contact sheet of signature PNGs on a solid background.

Useful to eyeball preprocessing results (transparency, cropping, sizing).

Usage:
  python contact_sheet.py --input clean/ --out preview.png --scale 1.0
Stdout: JSON
"""
from __future__ import annotations

import sys
import os
import json
import glob as globmod
import argparse

sys.stdout.reconfigure(encoding="utf-8")

IMG_EXT = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", nargs="+", required=True)
    ap.add_argument("--glob", default="*")
    ap.add_argument("--out", required=True)
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--bg", default="white")
    args = ap.parse_args()

    from PIL import Image, ImageDraw

    files = []
    for it in args.input:
        if os.path.isdir(it):
            files += [f for f in sorted(globmod.glob(os.path.join(it, args.glob)))
                      if f.lower().endswith(IMG_EXT)]
        else:
            files += [f for f in sorted(globmod.glob(it)) if os.path.isfile(f)]
    if not files:
        print(json.dumps({"status": "error", "message": "no images"}, ensure_ascii=False))
        sys.exit(1)

    imgs = []
    for f in files:
        im = Image.open(f).convert("RGBA")
        if args.scale != 1.0:
            im = im.resize((max(1, int(im.width * args.scale)),
                            max(1, int(im.height * args.scale))), Image.LANCZOS)
        imgs.append((os.path.basename(f), im))

    pad, gap, label_h = 20, 30, 28
    maxw = max(im.width for _, im in imgs)
    total_w = maxw + 2 * pad
    total_h = sum(im.height for _, im in imgs) + gap * (len(imgs) - 1) + len(imgs) * label_h + 2 * pad
    canvas = Image.new("RGB", (total_w, total_h), args.bg)
    y = pad
    for name, im in imgs:
        canvas.paste(im, (pad, y), im)
        ImageDraw.Draw(canvas).text((pad, y + im.height + 4),
                                    f"{name}  {im.width}x{im.height}", fill="black")
        y += im.height + label_h + gap
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    canvas.save(args.out)
    print(json.dumps({"status": "ok", "out": args.out, "size": list(canvas.size),
                      "count": len(imgs)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
