#!/usr/bin/env python3
"""extract_pdf.py — PDF helpers for the study-notes skill.

Three subcommands:

  text    Extract text per page (for textbook/worksheet reading).
  images  Render each page to a PNG (for scanned PDFs or layout viewing).
  crop    Crop a rectangular region of one page to a PNG (for MODE C: cutting a
          figure out of a worksheet so it can be embedded as base64).

All paths are arguments — nothing is hard-coded.

Requires PyMuPDF:  pip install pymupdf --break-system-packages -q
"""
import argparse
import os
import sys


def _open(path):
    try:
        import fitz  # PyMuPDF
    except ImportError:
        sys.exit("PyMuPDF not installed. Run: pip install pymupdf --break-system-packages -q")
    if not os.path.exists(path):
        sys.exit(f"File not found: {path}")
    return fitz.open(path)


def cmd_text(args):
    doc = _open(args.pdf)
    chunks, nonempty = [], 0
    for i, page in enumerate(doc):
        txt = page.get_text()
        if txt.strip():
            nonempty += 1
        chunks.append(f"--- PAGE {i + 1} ---\n{txt}")
    out = "\n".join(chunks)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        total_chars = len(out)
        print(f"Wrote {args.out}  ({len(doc)} pages, {nonempty} with text, {total_chars} chars)")
        if nonempty == 0:
            print("WARNING: no extractable text — this is likely a scanned PDF. "
                  "Run the 'images' subcommand and read the page PNGs instead.")
    else:
        print(out)


def cmd_images(args):
    doc = _open(args.pdf)
    os.makedirs(args.out, exist_ok=True)
    n = 0
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=args.dpi)
        dest = os.path.join(args.out, f"page_{i + 1:03d}.png")
        pix.save(dest)
        n += 1
    print(f"Saved {n} page image(s) to {args.out}/ at {args.dpi} dpi")


def _parse_bbox(s):
    try:
        parts = [float(x) for x in s.split(",")]
    except ValueError:
        sys.exit("--bbox must be four comma-separated numbers, e.g. 0.1,0.2,0.9,0.55")
    if len(parts) != 4:
        sys.exit("--bbox needs exactly 4 numbers: x0,y0,x1,y1")
    return parts


def cmd_crop(args):
    import fitz
    doc = _open(args.pdf)
    idx = args.page - 1
    if idx < 0 or idx >= len(doc):
        sys.exit(f"--page {args.page} out of range (PDF has {len(doc)} pages)")
    page = doc[idx]
    x0, y0, x1, y1 = _parse_bbox(args.bbox)
    rect = page.rect
    fractional = all(0.0 <= v <= 1.0 for v in (x0, y0, x1, y1))
    if fractional:
        clip = fitz.Rect(rect.x0 + x0 * rect.width,
                         rect.y0 + y0 * rect.height,
                         rect.x0 + x1 * rect.width,
                         rect.y0 + y1 * rect.height)
        mode = "fractional"
    else:
        clip = fitz.Rect(x0, y0, x1, y1)
        mode = "absolute(pt)"
    if clip.is_empty or clip.width <= 0 or clip.height <= 0:
        sys.exit(f"Computed clip is empty: {clip}")
    pix = page.get_pixmap(dpi=args.dpi, clip=clip)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    pix.save(args.out)
    print(f"Cropped page {args.page} ({mode} bbox) -> {args.out}  "
          f"[{pix.width}x{pix.height}px @ {args.dpi}dpi]")
    print("Next: python3 scripts/embed_images.py datauri " + args.out)


def main():
    p = argparse.ArgumentParser(description="PDF helpers for the study-notes skill.")
    sub = p.add_subparsers(dest="cmd", required=True)

    pt = sub.add_parser("text", help="extract text per page")
    pt.add_argument("pdf")
    pt.add_argument("-o", "--out", help="output .txt (prints to stdout if omitted)")
    pt.set_defaults(func=cmd_text)

    pi = sub.add_parser("images", help="render each page to PNG")
    pi.add_argument("pdf")
    pi.add_argument("-o", "--out", default="pages", help="output directory (default: pages)")
    pi.add_argument("--dpi", type=int, default=150)
    pi.set_defaults(func=cmd_images)

    pc = sub.add_parser("crop", help="crop a region of one page to PNG (for MODE C figures)")
    pc.add_argument("pdf")
    pc.add_argument("--page", type=int, required=True, help="1-based page number")
    pc.add_argument("--bbox", required=True,
                    help="x0,y0,x1,y1 — fractional (0..1, from top-left) or absolute points")
    pc.add_argument("-o", "--out", required=True, help="output .png")
    pc.add_argument("--dpi", type=int, default=200)
    pc.set_defaults(func=cmd_crop)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
