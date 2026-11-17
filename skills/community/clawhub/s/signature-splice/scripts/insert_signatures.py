# -*- coding: utf-8 -*-
"""Insert signature images into a PDF, evenly laid out, in a chosen order.

The insertion region is resolved data-driven (see locate_anchor) or given
explicitly.  Nothing is hard-coded to any particular form, person or filename.

Layout: the region is divided into rows x cols even cells; every signature is
scaled (aspect preserved) to fit its cell minus a margin and centred.

Usage:
  python insert_signatures.py --pdf form.pdf --input a.png b.png c.png \
         --anchor "（签名）" --out signed.pdf
  python insert_signatures.py --pdf form.pdf --input clean/ --glob "*.png" \
         --order "杨,口,乔,张" --rect 43,186,569,231 --out signed.pdf
Stdout: JSON {"status":"ok","slots":[...]}
"""
from __future__ import annotations

import sys
import os
import json
import math
import glob as globmod
import argparse

sys.stdout.reconfigure(encoding="utf-8")

sys.dont_write_bytecode = True  # keep the (synced) skill dir free of __pycache__
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import locate_anchor  # noqa: E402

IMG_EXT = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp")


def resolve_inputs(items, pattern="*"):
    files = []
    for it in items:
        if os.path.isdir(it):
            files += [f for f in sorted(globmod.glob(os.path.join(it, pattern)))
                      if f.lower().endswith(IMG_EXT)]
        else:
            files += [f for f in sorted(globmod.glob(it)) if os.path.isfile(f)]
    seen, out = set(), []
    for f in files:
        a = os.path.abspath(f)
        if a not in seen:
            seen.add(a)
            out.append(a)
    return out


def reorder_by_keys(files, keys):
    """Reorder files so the i-th key matches (substring) the i-th file."""
    remaining = list(files)
    ordered = []
    for k in keys:
        k = k.strip()
        if not k:
            continue
        hit = next((f for f in remaining if k.lower() in os.path.basename(f).lower()), None)
        if hit is None:
            raise RuntimeError(f"order key not matched by any file: {k!r}")
        remaining.remove(hit)
        ordered.append(hit)
    if remaining:
        raise RuntimeError(f"{len(remaining)} file(s) not covered by --order: "
                           + ", ".join(os.path.basename(f) for f in remaining))
    return ordered


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--page", type=int, default=1)
    ap.add_argument("--input", nargs="+", required=True,
                    help="signature images and/or directories (see --glob), injection order")
    ap.add_argument("--glob", default="*", help="pattern when a --input is a dir")
    ap.add_argument("--order", default=None,
                    help="comma-separated name list; reorders --input to match")
    ap.add_argument("--order-file", default=None,
                    help="text file with one name per line; reorders --input")
    # region
    ap.add_argument("--anchor", default=None, help="anchor text for auto region")
    ap.add_argument("--nth", type=int, default=0)
    ap.add_argument("--inset", type=float, default=2.5)
    ap.add_argument("--gap", type=float, default=3.0)
    ap.add_argument("--box", default=None, help="explicit frame x0,y0,x1,y1")
    ap.add_argument("--rect", default=None, help="explicit region x0,y0,x1,y1")
    # layout
    ap.add_argument("--rows", type=int, default=1)
    ap.add_argument("--cols", type=int, default=None)
    ap.add_argument("--cell-fill", type=float, default=0.94,
                    help="fraction of a cell the signature may occupy")
    # extras
    ap.add_argument("--labels", action="store_true", help="draw a caption under each signature")
    ap.add_argument("--label-size", type=float, default=6.0)
    ap.add_argument("--label-gap", type=float, default=3.0)
    ap.add_argument("--label-color", default="0.35,0.35,0.35")
    ap.add_argument("--label-font", default="china-s", help="PyMuPDF built-in font name")
    ap.add_argument("--debug", action="store_true", help="draw slot rectangles")
    args = ap.parse_args()

    import fitz
    from PIL import Image

    files = resolve_inputs(args.input, args.glob)
    if not files:
        print(json.dumps({"status": "error", "message": "no input images found"},
                         ensure_ascii=False))
        sys.exit(1)
    keys = None
    if args.order:
        keys = args.order.split(",")
    elif args.order_file:
        with open(args.order_file, encoding="utf-8") as fh:
            keys = [ln.strip() for ln in fh if ln.strip()]
    if keys:
        try:
            files = reorder_by_keys(files, keys)
        except RuntimeError as e:
            print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
            sys.exit(1)

    box = [float(v) for v in args.box.split(",")] if args.box else None
    rect = [float(v) for v in args.rect.split(",")] if args.rect else None
    loc = locate_anchor.find_region(args.pdf, page_no=args.page, anchor=args.anchor,
                                    inset=args.inset, gap=args.gap, nth=args.nth,
                                    rect=rect, box=box)
    if loc.get("mode") == "error":
        print(json.dumps({"status": "error", **loc}, ensure_ascii=False, indent=2))
        sys.exit(1)
    x0, y0, x1, y1 = loc["region"]

    n = len(files)
    rows = max(1, args.rows)
    cols = args.cols if args.cols else int(math.ceil(n / rows))
    if rows * cols < n:
        print(json.dumps({"status": "error",
                          "message": f"grid {rows}x{cols} cannot hold {n} signatures"},
                         ensure_ascii=False))
        sys.exit(1)
    cw = (x1 - x0) / cols
    ch = (y1 - y0) / rows
    fill = min(max(args.cell_fill, 0.1), 1.0)
    try:
        label_color = tuple(float(v) for v in args.label_color.split(","))
    except ValueError:
        label_color = (0.35, 0.35, 0.35)

    doc = fitz.open(args.pdf)
    page = doc[args.page - 1]

    report = {"status": "ok", "pdf_in": args.pdf, "pdf_out": args.out,
              "page_size": [round(v, 2) for v in page.rect],
              "region": loc["region"], "region_mode": loc.get("mode"),
              "grid": [rows, cols], "slots": []}

    for i, path in enumerate(files):
        r, c = divmod(i, cols)
        cx0 = x0 + c * cw
        cy0 = y0 + r * ch
        cell = fitz.Rect(cx0, cy0, cx0 + cw, cy0 + ch)
        mw = cw * (1 - fill) / 2.0
        mh = ch * (1 - fill) / 2.0
        target = fitz.Rect(cell.x0 + mw, cell.y0 + mh, cell.x1 - mw, cell.y1 - mh)
        im = Image.open(path)
        iw, ih = im.size
        sc = min(target.width / iw, target.height / ih)
        page.insert_image(target, filename=path, keep_proportion=True)

        slot = {"order": i + 1, "file": os.path.basename(path), "src_px": [iw, ih],
                "cell": [round(v, 2) for v in cell],
                "target": [round(v, 2) for v in target],
                "drawn_pt": [round(iw * sc, 2), round(ih * sc, 2)]}
        if args.labels:
            label = os.path.splitext(os.path.basename(path))[0]
            tw = fitz.get_text_length(label, fontname=args.label_font, fontsize=args.label_size)
            lx = (cell.x0 + cell.x1) / 2.0 - tw / 2.0
            ly = cell.y1 - mh * 0.2
            page.insert_text((lx, ly + args.label_gap), label,
                             fontname=args.label_font, fontsize=args.label_size,
                             color=label_color)
            slot["label"] = label
        if args.debug:
            page.draw_rect(cell, color=(1, 0, 0), width=0.5)
            page.insert_text((cell.x0 + 1, cell.y0 - 2), str(i + 1),
                             fontsize=5, color=(1, 0, 0))
        report["slots"].append(slot)

    outdir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(outdir, exist_ok=True)
    doc.save(args.out, garbage=3, deflate=True)
    doc.close()
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
