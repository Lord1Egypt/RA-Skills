#!/usr/bin/env python3
"""Render PDF pages to PNG assets for HTML decks.

Requires PyMuPDF:
  python -m pip install pymupdf
"""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_pages(spec: str | None, total: int) -> list[int]:
    if not spec:
        return list(range(total))
    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            pages.update(range(start - 1, end))
        else:
            pages.add(int(part) - 1)
    return [p for p in sorted(pages) if 0 <= p < total]


def main() -> int:
    parser = argparse.ArgumentParser(description="Render selected PDF pages to PNG files.")
    parser.add_argument("pdf", type=Path, help="Input PDF path.")
    parser.add_argument("output_dir", type=Path, help="Directory for rendered PNG files.")
    parser.add_argument("--pages", help="Pages to render, for example 1-6 or 1,3,5.")
    parser.add_argument("--zoom", type=float, default=2.0, help="Render zoom. Default: 2.0")
    args = parser.parse_args()

    try:
        import fitz  # type: ignore
    except ImportError as exc:
        raise SystemExit("PyMuPDF is required. Install with: python -m pip install pymupdf") from exc

    args.output_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(args.pdf)
    selected = parse_pages(args.pages, len(doc))
    matrix = fitz.Matrix(args.zoom, args.zoom)
    for page_index in selected:
        page = doc.load_page(page_index)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        out = args.output_dir / f"page-{page_index + 1:02d}.png"
        pix.save(out)
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
