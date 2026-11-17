# -*- coding: utf-8 -*-
"""Render PDF pages to PNG for visual self-checking.

Usage:
  python render_pdf.py --pdf signed.pdf --outdir out/ --dpi 200
  python render_pdf.py --pdf signed.pdf --outdir out/ --crop 38,145,575,250
Stdout: JSON {"status":"ok","count":N,"pages":[...]}
"""
from __future__ import annotations

import sys
import os
import json
import glob as globmod
import argparse

sys.stdout.reconfigure(encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True, help="input PDF (or glob)")
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--crop", default=None, help="clip in points: x0,y0,x1,y1")
    ap.add_argument("--page", type=int, default=None, help="only this page (1-based)")
    args = ap.parse_args()

    import fitz

    os.makedirs(args.outdir, exist_ok=True)
    clip = None
    if args.crop:
        x0, y0, x1, y1 = (float(v) for v in args.crop.split(","))
        clip = fitz.Rect(x0, y0, x1, y1)

    paths = sorted(globmod.glob(args.pdf)) if any(ch in args.pdf for ch in "*?[") else [args.pdf]
    result = []
    for path in paths:
        doc = fitz.open(path)
        stem = os.path.splitext(os.path.basename(path))[0]
        pages = range(doc.page_count)
        if args.page:
            pages = [args.page - 1]
        for i in pages:
            pix = doc[i].get_pixmap(dpi=args.dpi, alpha=False, clip=clip)
            multi = len(paths) > 1 or args.page is None and doc.page_count > 1
            name = f"{stem}_p{i+1:02d}.png" if multi else f"{stem}.png"
            out = os.path.join(args.outdir, name)
            pix.save(out)
            result.append({"pdf": os.path.basename(path), "page": i + 1, "file": out,
                           "width": pix.width, "height": pix.height})
        doc.close()
    print(json.dumps({"status": "ok", "count": len(result), "pages": result},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
