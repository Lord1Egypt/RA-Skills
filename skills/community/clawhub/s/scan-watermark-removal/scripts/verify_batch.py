#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Independent verifier for watermark-removal output.

Recomputes content retention and watermark residue on every produced page
WITHOUT trusting the remover's own self-check. Catches the two failure modes
self-checks usually miss: wrong output filenames, and content silently lost.

Usage:
    python verify_batch.py <source dir>                     # image batch
    python verify_batch.py <original.pdf> --output <out.pdf>

Pass criteria differ by output format, on purpose:

  images (PNG)  retention >= 99.0%, visibly-dark residue <= 20 px
  PDF (JPEG)    retention >= 97.0%, visibly-dark residue <= 20 px

The looser PDF retention is not a fudge. Re-encoding to JPEG moves pale
antialiased edges by a few units, which pushes a percent or two of the palest
blue edge pixels across the counting threshold; the content itself is intact.
Verify that claim before trusting it: for every pixel that lost a category,
print its original min channel. Deficits from min in [120,150] are edge jitter;
deficits from min < 100 are real loss.

Residue is gated on how DARK the leftover pixels are rather than how many there
are, because JPEG ringing on white paper produces thousands of near-white pixels
that land inside the faint-watermark window while being invisible (min channel
240+). A real leftover is hundreds of clearly tinted pixels.

Exit code 0 = all pages pass; 1 = at least one page needs a human look.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from PIL import Image

import wmcore

IMG_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tif", ".tiff")
RESIDUE_VISIBLE_LIMIT = 20   # residue pixels dark enough to actually be seen
KEEP_TOLERANCE = 99.0        # min content retention %, PNG output
PDF_KEEP_TOLERANCE = 97.0    # JPEG re-encode costs ~2% of pale antialiased edges
LOGO_LEFTOVER_LIMIT = 100    # px of logo colour still detectable after removal


def out_name(stem, suffix):
    """name_275.png -> name_去水印_275.png (suffix before trailing number)."""
    m = re.match(r"^(.*)_(\d+)$", stem)
    if m:
        return f"{m.group(1)}{suffix}_{m.group(2)}.png"
    return f"{stem}{suffix}.png"


def content(a):
    """(red, dark, blue) pixel counts — the three content families we protect."""
    return wmcore._content_counts(a.astype(np.int16))


def verify_images(src, out, suffix):
    import wm_pdf
    files = sorted(f for f in os.listdir(src)
                   if f.lower().endswith(IMG_EXTS)
                   and suffix not in os.path.splitext(f)[0])
    if not files:
        sys.exit(f"no images found in {src}")
    bad, worst, worst_cnt, worst_erased = [], 0, 0, 0
    for i, f in enumerate(files, 1):
        op = os.path.join(out, out_name(os.path.splitext(f)[0], suffix))
        if not os.path.exists(op):
            bad.append((f, "missing output"))
            continue
        o = np.asarray(Image.open(os.path.join(src, f)).convert("RGB"))
        n = np.asarray(Image.open(op).convert("RGB"))
        # the header logo is opaque colour, so it reads as both red and dark
        # content — exclude it before comparing retention
        lm = wm_pdf.logo_mask(o.astype(np.int16))
        excl = wm_pdf._dilate(lm, 2) if lm.any() else None
        co, cn = o.astype(np.int16), n.astype(np.int16)
        if excl is not None:
            co = co.copy()
            cn = cn.copy()
            co[excl] = 255
            cn[excl] = 255
        (orr, odb, obl), (nrr, ndb, nbl) = content(co), content(cn)
        rk = 100.0 * nrr / orr if orr else 100.0
        dk = 100.0 * ndb / odb if odb else 100.0
        bk = 100.0 * nbl / obl if obl else 100.0
        res, res_dark = wmcore.residue_profile(n)
        erased = wmcore.erased_content(o.astype(np.int16), n.astype(np.int16),
                                       exclude=excl)
        worst = max(worst, res_dark)
        worst_cnt = max(worst_cnt, res)
        worst_erased = max(worst_erased, erased)
        if erased > 0 or res_dark > RESIDUE_VISIBLE_LIMIT or min(rk, dk, bk) < 90.0:
            bad.append((f, f"erased={erased} residue={res}(visible {res_dark}) "
                           f"retention {rk:.1f}/{dk:.1f}/{bk:.1f}%"))
        if lm.any():
            still = wm_pdf.logo_mask(n.astype(np.int16))
            if int(still.sum()) > LOGO_LEFTOVER_LIMIT:
                bad.append((f, f"header logo still visible ({int(still.sum())}px)"))
        if i % 40 == 0:
            print(f"  ...checked {i}/{len(files)}", flush=True)
    print(f"\nverified {len(files)} images")
    print(f"worst residue: {worst_cnt}px raw, {worst}px visible; "
          f"worst erased content: {worst_erased}px")
    if bad:
        print(f"PROBLEM ({len(bad)}):")
        for f, msg in bad:
            print("  ", f, msg)
        return 1
    print("ALL PASS")
    return 0


def verify_pdf(src, dst):
    import wm_pdf
    if wm_pdf.pymupdf is None:
        sys.exit("PDF verification requires pymupdf: pip install pymupdf")
    doc_a = wm_pdf.pymupdf.open(src)
    doc_b = wm_pdf.pymupdf.open(dst)
    print(f"pages: source={doc_a.page_count} output={doc_b.page_count}")
    if doc_a.page_count != doc_b.page_count:
        print("PAGE COUNT MISMATCH")
        return 1
    bad, worst, worst_cnt, worst_erased, logo_left = [], 0, 0, 0, []
    for i in range(doc_a.page_count):
        pa, _ = wm_pdf._page_array(doc_a[i])
        pb, _ = wm_pdf._page_array(doc_b[i])
        lm = wm_pdf.logo_mask(pa)
        excl = wm_pdf._dilate(lm, 5) if lm.any() else None
        ca, cb = pa.astype(np.int16).copy(), pb.astype(np.int16).copy()
        if excl is not None:
            ca[excl] = 255
            cb[excl] = 255
        (orr, odb, obl), (nrr, ndb, nbl) = content(ca), content(cb)
        rk = 100.0 * nrr / orr if orr else 100.0
        dk = 100.0 * ndb / odb if odb else 100.0
        bk = 100.0 * nbl / obl if obl else 100.0
        res, res_dark = wmcore.residue_profile(pb)
        erased = wmcore.erased_content(pa.astype(np.int16), pb.astype(np.int16),
                                       exclude=excl)
        worst = max(worst, res_dark)
        worst_cnt = max(worst_cnt, res)
        worst_erased = max(worst_erased, erased)
        if lm.any() and int(wm_pdf.logo_mask(pb).sum()) > LOGO_LEFTOVER_LIMIT:
            logo_left.append(i + 1)
        if (erased > 0 or res_dark > RESIDUE_VISIBLE_LIMIT
                or min(rk, dk, bk) < 90.0):
            bad.append((i + 1, f"erased={erased} residue={res}(visible {res_dark}) "
                               f"retention {rk:.1f}/{dk:.1f}/{bk:.1f}%"))
        if (i + 1) % 40 == 0:
            print(f"  ...checked {i + 1}/{doc_a.page_count}", flush=True)
    print(f"\nverified {doc_a.page_count} pages")
    print(f"worst residue: {worst_cnt}px raw, {worst}px visible; "
          f"worst erased content: {worst_erased}px")
    if logo_left:
        print(f"header logo still visible on pages: {logo_left}")
    if bad:
        print(f"PROBLEM ({len(bad)}):")
        for p, msg in bad[:20]:
            print("  page", p, msg)
        return 1
    if logo_left:
        return 1
    print("ALL PASS")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help="original image folder, or original PDF")
    ap.add_argument("--output", default=None,
                    help="output folder / output .pdf (defaults are inferred)")
    ap.add_argument("--suffix", default="_去水印")
    a = ap.parse_args()
    src = os.path.abspath(a.source)
    if not os.path.exists(src):
        sys.exit(f"not found: {src}")
    if src.lower().endswith(".pdf"):
        dst = a.output or (os.path.splitext(src)[0] + "_去水印.pdf")
        return verify_pdf(src, os.path.abspath(dst))
    out = os.path.abspath(a.output) if a.output else os.path.join(src, "去水印输出")
    return verify_images(src, out, a.suffix)


if __name__ == "__main__":
    sys.exit(main())
