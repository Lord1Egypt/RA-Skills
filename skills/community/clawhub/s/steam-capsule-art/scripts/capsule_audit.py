#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Audit a Steam capsule image.

Checks, in order of how often they actually fail:
  1. exact pixel size (Valve wants the declared dimensions, no scaling)
  2. saturation and edge density against benchmark P25 floors
  3. negative-space liveness — is the logo zone structured or a dead field
  4. writes a 120x45 thumbnail, the size users actually see in search

Thresholds come from 20 top-selling capsules measured at a normalised
400x229. They are percentiles, not opinions: see SKILL.md.

Usage:
  python capsule_audit.py image.png --target 1232x706
  python capsule_audit.py image.png --target 462x174 --logo-zone left
  python capsule_audit.py image.png                 # size check skipped

Exit code 0 = all hard gates pass, 1 = at least one hard gate failed.
"""
import argparse
import os
import sys

from PIL import Image
import numpy as np

P25_SAT = 0.360
P25_EDGE = 4.92
NORM = (400, 229)
EDGE_DELTA = 28
WARM_HUE = (6, 40)      # HSV hue in 0-255 units, roughly 8-56 degrees
WARM_MIN_S = 0.30
WARM_MIN_V = 0.35


def measure(im):
    s = im.convert("RGB").resize(NORM, Image.LANCZOS)
    a = np.asarray(s, dtype=float)
    lum = 0.2126 * a[:, :, 0] + 0.7152 * a[:, :, 1] + 0.0722 * a[:, :, 2]
    g = np.asarray(s.convert("L"), dtype=int)
    edge = float((np.abs(g[:, 1:] - g[:, :-1]) > EDGE_DELTA).mean() * 100)
    hsv = np.asarray(s.convert("HSV"), dtype=float)
    sat = float(hsv[:, :, 1].mean() / 255.0)
    return {"sat": sat, "edge": edge, "lum_sd": float(lum.std()), "hsv": hsv, "lum": lum}


def zone(hsv, lum, box):
    h, w = hsv.shape[:2]
    x0, x1 = int(w * box[0]), int(w * box[1])
    sub_hsv = hsv[:, x0:x1]
    sub_lum = lum[:, x0:x1]
    hue, s, v = sub_hsv[:, :, 0], sub_hsv[:, :, 1] / 255.0, sub_hsv[:, :, 2] / 255.0
    warm = ((hue >= WARM_HUE[0]) & (hue <= WARM_HUE[1]) & (s >= WARM_MIN_S) & (v >= WARM_MIN_V))
    return {
        "lum_sd": float(sub_lum.std()),
        "warm_frac": float(warm.mean() * 100),
        "warm_px": int(warm.sum()),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--target", help="expected size, e.g. 1232x706")
    ap.add_argument("--logo-zone", choices=["left", "right", "none"], default="none",
                    help="zone reserved for the logotype; checked for dead space")
    ap.add_argument("--thumb", default=None, help="thumbnail output path")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    if not os.path.exists(args.image):
        sys.exit("no such file: %s" % args.image)

    im = Image.open(args.image)
    w, h = im.size
    m = measure(im)
    fails, warns, rows = [], [], []

    if args.target:
        try:
            tw, th = [int(x) for x in args.target.lower().split("x")]
        except ValueError:
            sys.exit("--target must look like 1232x706")
        ok = (w, h) == (tw, th)
        rows.append(("exact size", "%dx%d" % (w, h), "%dx%d" % (tw, th), ok))
        if not ok:
            fails.append("size %dx%d != %dx%d" % (w, h, tw, th))

    ok_sat = m["sat"] >= P25_SAT
    rows.append(("saturation", "%.3f" % m["sat"], ">= %.3f" % P25_SAT, ok_sat))
    if not ok_sat:
        warns.append("saturation below benchmark P25 (not fatal - see Cult of the Lamb 0.221)")

    ok_edge = m["edge"] >= P25_EDGE
    rows.append(("edge density", "%.2f%%" % m["edge"], ">= %.1f%%" % P25_EDGE, ok_edge))
    if not ok_edge:
        fails.append("edge density %.2f%% below benchmark P25" % m["edge"])

    if args.logo_zone != "none":
        box = (0.0, 0.62) if args.logo_zone == "left" else (0.38, 1.0)
        z = zone(m["hsv"], m["lum"], box)
        dead = z["lum_sd"] < 8.0 and z["warm_frac"] < 0.5
        rows.append(("%s zone liveness" % args.logo_zone,
                     "lumSD %.1f / warm %.2f%%" % (z["lum_sd"], z["warm_frac"]),
                     "lumSD>=8 or warm>=0.5%", not dead))
        if dead:
            fails.append("%s zone is a dead flat field - name concrete elements for it" % args.logo_zone)

    thumb_path = args.thumb
    if thumb_path is None:
        root, _ = os.path.splitext(args.image)
        thumb_path = root + "_120x45.png"
    im.convert("RGB").resize((120, 45), Image.LANCZOS).save(thumb_path)

    if args.json:
        import json
        print(json.dumps({"file": args.image, "size": [w, h], "sat": round(m["sat"], 4),
                          "edge": round(m["edge"], 2), "lum_sd": round(m["lum_sd"], 1),
                          "thumb": thumb_path, "fails": fails, "warns": warns}, indent=1))
    else:
        print("file  %s  (%dx%d)" % (args.image, w, h))
        for name, got, want, ok in rows:
            print("  %-20s %-24s %-22s %s" % (name, got, want, "PASS" if ok else "FAIL"))
        print("  thumbnail            %s" % thumb_path)
        for f in fails:
            print("  FAIL: %s" % f)
        for wmsg in warns:
            print("  WARN: %s" % wmsg)
        print("result: %s" % ("FAIL" if fails else "PASS"))

    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
