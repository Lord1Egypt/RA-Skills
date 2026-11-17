# -*- coding: utf-8 -*-
"""Diagnose signature images (run this when a new image preprocesses badly).

Reports, per image: mode/size/format, alpha & luminance ranges, ink colour
chroma, composited-over-white background, guessed polarity, detected frame
rules (screenshot borders) and the ink bbox / aspect ratio.

Usage:
  python inspect_signatures.py --input raw/ --glob "*.png"
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


def border_mask(H, W, frac):
    import numpy as np

    m = np.zeros((H, W), bool)
    bh, bw = max(1, int(round(H * frac))), max(1, int(round(W * frac)))
    m[:bh, :] = True
    m[H - bh:, :] = True
    m[:, :bw] = True
    m[:, W - bw:] = True
    return m


def analyze(path, ink_thr=35.0, frame_thr=20.0, span=0.85, margin_frac=0.12):
    import numpy as np
    from PIL import Image

    im = Image.open(path)
    info = {"file": os.path.basename(path), "mode": im.mode,
            "size": list(im.size), "format": im.format}
    rgba = im.convert("RGBA")
    arr = np.asarray(rgba).astype(np.float32)
    rgb, alpha = arr[..., :3], arr[..., 3]
    lum = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    lum_eff = 255.0 - (255.0 - lum) * (alpha / 255.0)
    H, W = lum_eff.shape

    info["alpha_range"] = [int(alpha.min()), int(alpha.max())]
    info["lum_range"] = [int(lum.min()), int(lum.max())]
    info["max_chroma"] = int((rgb.max(axis=2) - rgb.min(axis=2)).max())
    m = border_mask(H, W, margin_frac)
    bg = float(np.median(lum_eff[m]))
    info["bg_lum_eff"] = round(bg, 1)
    info["polarity_guess"] = "dark" if bg < 128 else "light"

    ink = (255.0 - lum_eff) if info["polarity_guess"] == "light" else lum_eff
    nw = ink > frame_thr
    col_f, row_f = nw.mean(axis=0), nw.mean(axis=1)
    mh, mw = max(3, int(H * margin_frac)), max(3, int(W * margin_frac))
    info["frame_lines"] = {
        "threshold": frame_thr, "span": span,
        "left_cols": [int(x) for x in range(min(mw, W)) if col_f[x] > span],
        "right_cols": [int(x) for x in range(W - 1, max(W - 1 - mw, -1), -1) if col_f[x] > span],
        "top_rows": [int(y) for y in range(min(mh, H)) if row_f[y] > span],
        "bottom_rows": [int(y) for y in range(H - 1, max(H - 1 - mh, -1), -1) if row_f[y] > span],
    }
    mask = ink > ink_thr
    ys, xs = np.where(mask)
    if len(xs):
        x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
        w, h = x1 - x0 + 1, y1 - y0 + 1
        info["ink_bbox"] = [x0, y0, x1, y1]
        info["ink_size"] = [w, h]
        info["ink_aspect"] = round(w / h, 3)
        info["ink_pixels"] = int(mask.sum())
    else:
        info["ink_bbox"] = None
    return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", nargs="+", required=True)
    ap.add_argument("--glob", default="*")
    ap.add_argument("--ink-threshold", type=float, default=35.0)
    ap.add_argument("--frame-threshold", type=float, default=20.0)
    ap.add_argument("--frame-span", type=float, default=0.85)
    ap.add_argument("--margin-frac", type=float, default=0.12)
    args = ap.parse_args()

    files = []
    for it in args.input:
        if os.path.isdir(it):
            files += [f for f in sorted(globmod.glob(os.path.join(it, args.glob)))
                      if f.lower().endswith(IMG_EXT)]
        else:
            files += [f for f in sorted(globmod.glob(it)) if os.path.isfile(f)]
    if not files:
        print(json.dumps({"status": "error", "message": "no input images"}, ensure_ascii=False))
        sys.exit(1)

    items = [analyze(f, args.ink_threshold, args.frame_threshold,
                     args.frame_span, args.margin_frac) for f in files]
    print(json.dumps({"status": "ok", "count": len(items), "items": items},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
