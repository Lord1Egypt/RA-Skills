#!/usr/bin/env python3
"""
build_pdfs.py — Expense Claim Skill
Generates per-day per-category PDFs from a bills manifest.

Usage:
    python3 build_pdfs.py --manifest bills_manifest.json
    python3 build_pdfs.py --manifest bills_manifest.json --out /mnt/user-data/outputs/bills_by_category

Manifest format (bills_manifest.json):
[
  {
    "date": "13_Feb_2026",
    "category": "Travel_Expenses_Conveyance",
    "files": [
      "/mnt/user-data/uploads/receipt_abc123.pdf",
      "/mnt/user-data/uploads/Screenshot_xyz.png"
    ]
  },
  ...
]
"""

import argparse
import io
import json
import os
import sys

try:
    import img2pdf
    from PIL import Image
    from pypdf import PdfReader, PdfWriter
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install img2pdf Pillow pypdf --break-system-packages")
    sys.exit(1)


def img_to_pdf_bytes(img_path: str) -> bytes:
    """Convert an image file to PDF bytes."""
    img = Image.open(img_path)
    if img.mode in ("RGBA", "P", "LA"):
        img = img.convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=92)
    buf.seek(0)
    return img2pdf.convert(buf.read())


def make_pdf(out_path: str, files: list[str]) -> int:
    """Merge images and PDFs into a single output PDF. Returns page count."""
    writer = PdfWriter()
    for fpath in files:
        if not os.path.exists(fpath):
            print(f"  [WARN] Missing file, skipping: {fpath}")
            continue
        ext = fpath.lower().rsplit(".", 1)[-1]
        if ext in ("jpg", "jpeg", "png", "webp", "bmp", "tiff", "gif"):
            pdf_bytes = img_to_pdf_bytes(fpath)
            reader = PdfReader(io.BytesIO(pdf_bytes))
        elif ext == "pdf":
            reader = PdfReader(fpath)
        else:
            print(f"  [WARN] Unknown file type, skipping: {fpath}")
            continue
        for page in reader.pages:
            writer.add_page(page)

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "wb") as f:
        writer.write(f)
    return len(writer.pages)


def main():
    parser = argparse.ArgumentParser(description="Build per-day per-category expense PDFs")
    parser.add_argument("--manifest", required=True, help="Path to bills_manifest.json")
    parser.add_argument(
        "--out",
        default="/mnt/user-data/outputs/bills_by_category",
        help="Output directory",
    )
    args = parser.parse_args()

    with open(args.manifest) as f:
        manifest = json.load(f)

    print(f"Building {len(manifest)} PDFs → {args.out}\n")
    results = []
    for entry in manifest:
        date = entry["date"]          # e.g. "13_Feb_2026"
        category = entry["category"]  # e.g. "Travel_Expenses_Conveyance"
        files = entry["files"]
        fname = f"{date}_{category}.pdf"
        out_path = os.path.join(args.out, fname)
        pages = make_pdf(out_path, files)
        print(f"  ✓ {fname} ({len(files)} receipts, {pages} pages)")
        results.append({"file": out_path, "pages": pages})

    print(f"\nDone. {len(results)} PDFs created in {args.out}")
    return results


if __name__ == "__main__":
    main()
