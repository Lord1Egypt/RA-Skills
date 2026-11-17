# -*- coding: utf-8 -*-
"""Preprocess signature images into clean, tight, transparent-black PNGs.

Works on any signature scan/photo/screenshot; nothing is hard-coded to a
particular person or form.  Pipeline per image:

  1. "Inkness" map built from the COMPOSITED-over-white luminance, so it handles
     white-background JPGs, transparent PNGs and black-ink-in-alpha PNGs alike:
        lum_eff = 255 - (255 - lum) * (alpha/255)
        dark ink on light bg : ink = 255 - lum_eff
        light ink on dark bg : ink = lum_eff          (polarity auto-detected)
  2. Trim screenshot frame lines: rows/cols in an outer margin band that are
     (nearly) fully non-background are treated as frame rules and cut away.
  3. Threshold to an ink mask (adaptive to the estimated background), drop tiny
     blobs (JPEG noise / specks).
  4. Crop to the ink bbox + a small transparent padding.
  5. Rebuild as RGBA: alpha = inkness, RGB = black (or original with --keep-color).

Usage:
  python preprocess_signatures.py --input a.png b.jpg --outdir clean/
  python preprocess_signatures.py --input raw/ --glob "*.png" --outdir clean/
Stdout: JSON {"status":"ok","items":[...]}
"""
from __future__ import annotations

import sys
import os
import json
import glob as globmod
import argparse

sys.stdout.reconfigure(encoding="utf-8")

IMG_EXT = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp")


def resolve_inputs(items, pattern="*"):
    files = []
    for it in items:
        if os.path.isdir(it):
            for f in sorted(globmod.glob(os.path.join(it, pattern))):
                if f.lower().endswith(IMG_EXT):
                    files.append(f)
        else:
            for f in sorted(globmod.glob(it)):
                if os.path.isfile(f):
                    files.append(f)
    # de-dup, keep order
    seen, out = set(), []
    for f in files:
        a = os.path.abspath(f)
        if a not in seen:
            seen.add(a)
            out.append(a)
    return out


def _border_mask(H, W, frac):
    import numpy as np

    m = np.zeros((H, W), bool)
    bh = max(1, int(round(H * frac)))
    bw = max(1, int(round(W * frac)))
    m[:bh, :] = True
    m[H - bh:, :] = True
    m[:, :bw] = True
    m[:, W - bw:] = True
    return m


def build_ink(path, polarity="auto", border_frac=0.12):
    """Return (ink, rgb, alpha) float arrays and the chosen polarity."""
    import numpy as np
    from PIL import Image

    im = Image.open(path).convert("RGBA")
    arr = np.asarray(im).astype(np.float32)
    rgb = arr[..., :3]
    alpha = arr[..., 3]
    lum = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    a = alpha / 255.0
    lum_eff = 255.0 - (255.0 - lum) * a          # composited over white

    pol = polarity
    if pol == "auto":
        m = _border_mask(lum_eff.shape[0], lum_eff.shape[1], border_frac)
        bg = float(np.median(lum_eff[m]))
        pol = "dark" if bg < 128 else "light"
    else:
        m = _border_mask(lum_eff.shape[0], lum_eff.shape[1], border_frac)
        bg = float(np.median(lum_eff[m]))
    ink = (255.0 - lum_eff) if pol == "light" else lum_eff
    return ink, rgb, alpha, pol, bg


def trim_frame(ink, frame_thr, span, margin_frac):
    H, W = ink.shape
    nw = ink > frame_thr
    col = nw.mean(axis=0)
    row = nw.mean(axis=1)
    mh = max(3, int(round(H * margin_frac)))
    mw = max(3, int(round(W * margin_frac)))
    L = -1
    for x in range(min(mw, W)):
        if col[x] > span:
            L = x
    top = -1
    for y in range(min(mh, H)):
        if row[y] > span:
            top = y
    R = W
    for x in range(W - 1, max(W - 1 - mw, -1), -1):
        if col[x] > span:
            R = x
    B = H
    for y in range(H - 1, max(H - 1 - mh, -1), -1):
        if row[y] > span:
            B = y
    removed = {"top": top + 1, "bottom": H - B, "left": L + 1, "right": W - R}
    return ink[top + 1:B, L + 1:R], removed


def despeckle(mask, min_blob):
    import numpy as np
    from scipy import ndimage

    lab, n = ndimage.label(mask)
    if n == 0:
        return mask
    sizes = ndimage.sum(np.ones_like(lab), lab, index=np.arange(1, n + 1))
    keep = np.zeros(n + 1, dtype=bool)
    keep[1:] = sizes >= min_blob
    return keep[lab]


def process(path, out_path, opts):
    import numpy as np
    from PIL import Image

    ink, rgb, alpha, pol, bg = build_ink(path, polarity=opts["polarity"])
    ink, frame = trim_frame(ink, opts["frame_threshold"], opts["frame_span"],
                            opts["margin_frac"])

    thr = opts["ink_threshold"]
    if opts["adaptive_delta"] > 0 and ink.size:
        bg_ink = float(np.percentile(ink, 25))
        thr = max(thr, bg_ink + opts["adaptive_delta"])
    mask = ink > thr
    if opts["min_blob"] > 0 and mask.any():
        mask = despeckle(mask, opts["min_blob"])
    ys, xs = np.where(mask)
    if len(xs) == 0:
        raise RuntimeError(f"no ink found (threshold={thr:.1f}, polarity={pol})")
    x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())

    pad = int(round(opts["pad_frac"] * max(x1 - x0 + 1, y1 - y0 + 1))) + 2
    H, W = ink.shape
    xa, xb = max(0, x0 - pad), min(W, x1 + 1 + pad)
    ya, yb = max(0, y0 - pad), min(H, y1 + 1 + pad)

    alpha_out = np.clip(ink[ya:yb, xa:xb], 0, 255).astype(np.uint8)
    rgba = np.zeros((alpha_out.shape[0], alpha_out.shape[1], 4), dtype=np.uint8)
    if opts["keep_color"] and pol == "light":
        rgba[..., :3] = rgb[ya:yb, xa:xb].astype(np.uint8)
    rgba[..., 3] = alpha_out
    Image.fromarray(rgba, "RGBA").save(out_path)

    w, h = xb - xa, yb - ya
    return {"src": os.path.basename(path), "dst": os.path.basename(out_path),
            "polarity": pol, "bg_lum_eff": round(bg, 1),
            "threshold_used": round(float(thr), 1),
            "frame_trimmed": frame, "out_size": [w, h],
            "aspect": round(w / h, 3) if h else None,
            "ink_pixels": int(mask.sum())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", nargs="+", required=True,
                    help="image files and/or directories (see --glob)")
    ap.add_argument("--glob", default="*", help="pattern when a --input is a dir")
    ap.add_argument("--outdir", required=True, help="output directory for clean PNGs")
    ap.add_argument("--ink-threshold", type=float, default=35.0)
    ap.add_argument("--adaptive-delta", type=float, default=25.0,
                    help="threshold >= background_ink + this (0 disables)")
    ap.add_argument("--frame-threshold", type=float, default=20.0)
    ap.add_argument("--frame-span", type=float, default=0.85)
    ap.add_argument("--margin-frac", type=float, default=0.06,
                    help="outer band searched for frame rules")
    ap.add_argument("--min-blob", type=int, default=14)
    ap.add_argument("--pad-frac", type=float, default=0.03)
    ap.add_argument("--polarity", choices=["auto", "light", "dark"], default="auto")
    ap.add_argument("--keep-color", action="store_true",
                    help="keep original ink colour instead of forcing black")
    args = ap.parse_args()

    opts = vars(args)
    files = resolve_inputs(args.input, args.glob)
    if not files:
        print(json.dumps({"status": "error", "message": "no input images found"},
                         ensure_ascii=False))
        sys.exit(1)

    os.makedirs(args.outdir, exist_ok=True)
    items, errors = [], []
    for f in files:
        out_path = os.path.join(args.outdir, os.path.splitext(os.path.basename(f))[0] + ".png")
        try:
            items.append(process(f, out_path, opts))
        except Exception as e:  # noqa: BLE001
            errors.append({"src": os.path.basename(f), "error": str(e)})
    status = "ok" if not errors else ("partial" if items else "error")
    print(json.dumps({"status": status, "count": len(items),
                      "items": items, "errors": errors},
                     ensure_ascii=False, indent=2))
    sys.exit(0 if items else 1)


if __name__ == "__main__":
    main()
