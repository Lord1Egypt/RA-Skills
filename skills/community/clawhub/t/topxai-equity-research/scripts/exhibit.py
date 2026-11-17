#!/usr/bin/env python3
"""Exhibits from original documents: crop a passage out of a filing, box the sentence the reader should see in red,
and write a PNG for the report.

Why: the most convincing evidence is the company's own words. "In 2022 the company admitted X" is weaker than the page
itself with the sentence boxed. The crop is reproducible (the same command gives the same image), so it is not done by hand.

    python3 scripts/exhibit.py <URL or local file> --find "original text" [--find "second passage"] --out research/<report-id>/exhibits/x.png
        [--page N]                only search page N (from 1, in PDF page order); default: the first match from the start
        [--above 90 --below 90]   context above and below the box, in points (default 90)
        [--clip x0,y0,x1,y1]      crop this area (points, PDF coordinates) instead of above / below
        [--full]                  the whole page
        [--underline]             underline instead of a box
        [--row]                   stretch the box across the text column (a whole table row: label and every period)
        [--zoom 2.2]              render scale (2.2 is about 158 dpi, sharp enough for an A4 text column)

Requires PyMuPDF (`pip install pymupdf`). PDF files are read directly; .htm / .html (most SEC filings) are first printed
to PDF with a local Chrome or Chromium (set CHROME to its path), then searched the same way.
Fetching: sec.gov needs SEC_USER_AGENT="Name email" (the SEC fair-access policy, same as sec.py); other sites get a
regular browser user agent. Downloads are cached under research/cache/exhibits/ in the project.

Output: the PNG and one line to cite (PDF page order, the document's own page label, where the box is). The exhibit's
source line must say the red box was added by the authors: the box is ours, not the original's.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

try:
    import pymupdf
except ImportError:  # optional dependency, only this script needs it
    raise SystemExit("exhibit.py needs PyMuPDF: pip install pymupdf")

CACHE = Path(os.environ.get("EXHIBIT_CACHE_DIR", "research/cache/exhibits")).expanduser().resolve()
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
RED = (0.78, 0.07, 0.07)
BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def fetch(src: str) -> Path:
    """URL -> cached file; a local path is returned as is."""
    if not re.match(r"https?://", src):
        p = Path(src).expanduser().resolve()
        if not p.is_file():
            raise SystemExit(f"file not found: {p}")
        return p
    CACHE.mkdir(parents=True, exist_ok=True)
    ext = Path(src.split("?")[0]).suffix.lower() or ".bin"
    dst = CACHE / (hashlib.sha1(src.encode()).hexdigest()[:16] + ext)
    if dst.exists() and dst.stat().st_size:
        return dst
    if "sec.gov" in src:
        ua = os.environ.get("SEC_USER_AGENT", "").strip()
        if not ua or "@" not in ua:
            raise SystemExit('sec.gov needs SEC_USER_AGENT="Name email" (SEC fair-access policy)')
    else:
        ua = BROWSER_UA
    req = urllib.request.Request(src, headers={"User-Agent": ua, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=90) as r:
        dst.write_bytes(r.read())
    return dst


def is_pdf(p: Path) -> bool:
    with open(p, "rb") as f:
        return f.read(5) == b"%PDF-"


def html_to_pdf(p: Path, base_url: str | None) -> Path:
    """HTML filing -> PDF through a local Chrome. A <base> tag lets relative images in the original still load."""
    out = p.with_suffix(".print.pdf")
    if out.exists() and out.stat().st_mtime >= p.stat().st_mtime:
        return out
    if not Path(CHROME).exists():
        raise SystemExit(f"HTML must be printed to PDF first; Chrome not found at {CHROME} (set CHROME)")
    html = p.read_text(encoding="utf-8", errors="replace")
    if base_url and "<base " not in html[:5000].lower():
        html = re.sub(r"(?i)<head[^>]*>", lambda m: m.group(0) + f'<base href="{base_url}">', html, count=1) \
            if re.search(r"(?i)<head[^>]*>", html) else f'<base href="{base_url}">' + html
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "doc.html"
        src.write_text(html, encoding="utf-8")
        # Judge by the file, not the exit code: Chrome often exits 2 after writing the PDF ("Teardown watchdog expired").
        out.unlink(missing_ok=True)
        r = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                            "--virtual-time-budget=8000", f"--print-to-pdf={out}", src.as_uri()],
                           capture_output=True, timeout=180)
    if not out.exists() or out.stat().st_size < 1000:
        raise SystemExit(f"Chrome produced no PDF (exit code {r.returncode}): {r.stderr.decode(errors='replace')[-300:]}")
    return out


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("“", '"').replace("”", '"')).strip()


def find_on_page(page: pymupdf.Page, phrase: str) -> list[pymupdf.Rect]:
    """Find a passage on one page and return the rectangles of its lines. Try as given, then with straight quotes and single spaces."""
    hits = page.search_for(phrase)
    if not hits:
        hits = page.search_for(norm(phrase))
    return hits


def locate(doc: pymupdf.Document, phrases: list[str], page_no: int | None):
    pages = [page_no - 1] if page_no else range(doc.page_count)
    for i in pages:
        page = doc[i]
        found = [find_on_page(page, ph) for ph in phrases]
        if all(found):
            return i, found
    missing = [ph for ph in phrases if not any(find_on_page(doc[i], ph) for i in pages)]
    raise SystemExit("passage not found (check spelling, hyphenation at line breaks, or shorten it):\n  " + "\n  ".join(missing))


def union(rects: list[pymupdf.Rect]) -> pymupdf.Rect:
    r = pymupdf.Rect(rects[0])
    for x in rects[1:]:
        r |= x
    return r


def text_column(page: pymupdf.Page) -> tuple[float, float]:
    """Left and right edges of the text column (measured from text blocks), so the crop reads like a page, not a fragment."""
    xs = [b[:4] for b in page.get_text("blocks") if b[4].strip()]
    if not xs:
        return page.rect.x0, page.rect.x1
    return max(page.rect.x0, min(b[0] for b in xs) - 12), min(page.rect.x1, max(b[2] for b in xs) + 12)


def snap_to_lines(page: pymupdf.Page, clip: pymupdf.Rect) -> pymupdf.Rect:
    """Snap the crop to whole lines, so no half-cut line at the top or bottom (it looks like tampered evidence)."""
    lines = [pymupdf.Rect(l["bbox"]) for b in page.get_text("dict")["blocks"] if b.get("type") == 0
             for l in b["lines"] if any(s["text"].strip() for s in l["spans"])]
    inside_top = [r.y0 for r in lines if r.y0 >= clip.y0 - 0.5]
    inside_bot = [r.y1 for r in lines if r.y1 <= clip.y1 + 0.5]
    y0 = min(inside_top) - 1 if inside_top else clip.y0
    y1 = max(inside_bot) + 2 if inside_bot else clip.y1
    return pymupdf.Rect(clip.x0, max(page.rect.y0, y0), clip.x1, min(page.rect.y1, y1)) if y1 > y0 else clip


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("src")
    ap.add_argument("--find", action="append", default=[], help="passage to box; may be given several times")
    ap.add_argument("--out", required=True)
    ap.add_argument("--page", type=int)
    ap.add_argument("--above", type=float, default=90)
    ap.add_argument("--below", type=float, default=90)
    ap.add_argument("--clip")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--underline", action="store_true")
    ap.add_argument("--row", action="store_true")
    ap.add_argument("--zoom", type=float, default=2.2)
    a = ap.parse_args()
    if not a.find and not (a.full or a.clip):
        raise SystemExit("give at least one --find (the passage to box), or --full / --clip for an unboxed crop")

    path = fetch(a.src)
    pdf = path if is_pdf(path) else html_to_pdf(path, a.src if re.match(r"https?://", a.src) else None)
    doc = pymupdf.open(pdf)

    if a.find:
        idx, found = locate(doc, a.find, a.page)
    else:
        idx, found = (a.page or 1) - 1, []
    page = doc[idx]

    boxes = []
    col = text_column(page)
    for rects in found:
        box = union(rects) + (-2.5, -2, 2.5, 2)   # pad so the line does not touch the text
        if a.row:
            box.x0, box.x1 = col[0] + 4, col[1] - 4
        boxes.append(box)
        shape = page.new_shape()
        if a.underline:
            for r in rects:
                shape.draw_line(r.bl + (0, 1.2), r.br + (0, 1.2))
        else:
            shape.draw_rect(box)
        shape.finish(color=RED, width=1.6, fill=None)
        shape.commit()

    if a.full:
        clip = page.rect
    elif a.clip:
        x0, y0, x1, y1 = (float(v) for v in a.clip.split(","))
        clip = pymupdf.Rect(x0, y0, x1, y1)
    else:
        allb = union(boxes)
        cx0, cx1 = col
        clip = snap_to_lines(page, pymupdf.Rect(cx0, max(page.rect.y0, allb.y0 - a.above),
                                                cx1, min(page.rect.y1, allb.y1 + a.below)))

    pix = page.get_pixmap(matrix=pymupdf.Matrix(a.zoom, a.zoom), clip=clip, alpha=False)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    pix.save(out)
    label = page.get_label() or "—"
    print(f"exhibit -> {out}  {pix.width}x{pix.height}px")
    print(f"  page: PDF page {idx + 1} of {doc.page_count}; the document's own page label: {label}")
    for ph, b in zip(a.find, boxes):
        print(f"  box: \"{ph[:60]}{'...' if len(ph) > 60 else ''}\" at y={b.y0:.0f}-{b.y1:.0f}pt")
    if path != pdf:
        print("  (HTML original printed to PDF through Chrome; PDF page order is not the original's page number: cite the section or Item)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
