# -*- coding: utf-8 -*-
"""Locate the insertion region for signatures inside a PDF.

Strategy (fully data-driven, nothing specific to any form):
  1. Merge the page's vector drawings into "frames" (the form's boxes/cells).
  2. Find the given anchor TEXT on the page, take its text line bbox.
  3. The region = the smallest frame that contains that line, minus a top strip
     (everything at/above the anchor line) and inset by a small margin.

Also usable as a library:  from locate_anchor import find_region

Usage:
  python locate_anchor.py --pdf form.pdf --anchor "（签名）"
  python locate_anchor.py --pdf form.pdf --anchor "\u7b7e\u540d" --page 1 --inset 3 --gap 4
Stdout: JSON {"status":"ok","region":[x0,y0,x1,y1], ...}
"""
from __future__ import annotations

import sys
import json
import argparse

sys.stdout.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------- geometry ---
def merge_rects(rects, tol=0.5):
    """Merge overlapping / adjacent rects (list of [x0,y0,x1,y1]) into bboxes."""
    rects = [[float(v) for v in r] for r in rects]
    changed = True
    while changed:
        changed = False
        out, used = [], [False] * len(rects)
        for i in range(len(rects)):
            if used[i]:
                continue
            a = rects[i][:]
            for j in range(i + 1, len(rects)):
                if used[j]:
                    continue
                b = rects[j]
                if not (a[2] < b[0] - tol or b[2] < a[0] - tol
                        or a[3] < b[1] - tol or b[3] < a[1] - tol):
                    a = [min(a[0], b[0]), min(a[1], b[1]),
                         max(a[2], b[2]), max(a[3], b[3])]
                    used[j] = True
                    changed = True
            out.append(a)
        rects = out
    return rects


def page_frames(page, tol=0.5, min_size=4.0):
    """Return the page's merged drawing frames as list of dicts."""
    rects = []
    for d in page.get_drawings():
        r = d["rect"]
        rects.append([r.x0, r.y0, r.x1, r.y1])
    merged = merge_rects(rects, tol=tol)
    frames = [{"rect": [round(v, 2) for v in r],
               "w": round(r[2] - r[0], 2), "h": round(r[3] - r[1], 2)}
              for r in merged if (r[2] - r[0]) >= min_size and (r[3] - r[1]) >= min_size]
    return frames


def find_anchor_line(page, anchor, nth=0):
    """Find the nth text line containing `anchor`; return (line_bbox, spans)."""
    hits = []
    for b in page.get_text("dict")["blocks"]:
        if b.get("type") != 0:
            continue
        for line in b["lines"]:
            spans = [s for s in line["spans"] if s["text"].strip()]
            if not spans:
                continue
            if any(anchor in s["text"] for s in spans):
                x0 = min(s["bbox"][0] for s in spans)
                y0 = min(s["bbox"][1] for s in spans)
                x1 = max(s["bbox"][2] for s in spans)
                y1 = max(s["bbox"][3] for s in spans)
                hits.append({"bbox": [x0, y0, x1, y1],
                             "text": "".join(s["text"] for s in spans),
                             "spans": [{"text": s["text"],
                                        "bbox": [round(v, 2) for v in s["bbox"]]}
                                       for s in spans]})
    if not hits:
        return None, []
    if nth >= len(hits):
        return None, hits
    return hits[nth], hits


def contains(outer, inner, tol=0.5):
    return (outer[0] <= inner[0] + tol and outer[1] <= inner[1] + tol
            and outer[2] >= inner[2] - tol and outer[3] >= inner[3] - tol)


def find_region(pdf, page_no=1, anchor=None, inset=2.5, gap=3.0, nth=0,
                rect=None, box=None, tol=0.5):
    """Return a dict describing the insertion region (PDF points).

    rect: explicit [x0,y0,x1,y1] -> returned as-is.
    box : explicit frame [x0,y0,x1,y1] (region = below the anchor line inside box).
    """
    import fitz

    doc = fitz.open(pdf)
    try:
        page = doc[page_no - 1]
        frame = {"page": page_no, "page_size": [round(v, 2) for v in page.rect]}

        if rect is not None:
            frame.update({"mode": "explicit_rect", "region": [float(v) for v in rect]})
            return frame

        frames = page_frames(page, tol=tol)
        frame["frames"] = frames

        if box is not None:
            box = [float(v) for v in box]
            line = {"bbox": [box[0], box[1], box[2], box[3]], "text": "(explicit box)"}
        else:
            if not anchor:
                frame.update({"mode": "error",
                              "message": "need --anchor TEXT, --box or --rect"})
                return frame
            line, hits = find_anchor_line(page, anchor, nth=nth)
            if line is None:
                frame.update({"mode": "error",
                              "message": f"anchor not found: {anchor!r}",
                              "candidates": hits})
                return frame
            frame["anchor"] = {"text": line["text"],
                               "bbox": [round(v, 2) for v in line["bbox"]]}
            containers = [f for f in frames
                          if contains(f["rect"], line["bbox"], tol)
                          and f["h"] >= 2 * (line["bbox"][3] - line["bbox"][1])]
            containers.sort(key=lambda f: f["w"] * f["h"])
            if not containers:
                frame.update({"mode": "error",
                              "message": "no enclosing frame found for the anchor",
                              "hint": "pass --box or --rect explicitly"})
                return frame
            frame["enclosing_frame"] = containers[0]["rect"]
            box = containers[0]["rect"]

        lb = line["bbox"]
        x0 = box[0] + inset
        x1 = box[2] - inset
        y0 = lb[3] + gap
        y1 = box[3] - inset
        if x1 - x0 <= 0 or y1 - y0 <= 0:
            frame.update({"mode": "error",
                          "message": "computed region is empty; adjust inset/gap"})
            return frame
        frame.update({"mode": "anchor_below_line",
                      "box": [round(v, 2) for v in box],
                      "region": [round(x0, 2), round(y0, 2), round(x1, 2), round(y1, 2)]})
        return frame
    finally:
        doc.close()


# -------------------------------------------------------------------- CLI ----
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True, help="input PDF")
    ap.add_argument("--page", type=int, default=1)
    ap.add_argument("--anchor", default=None,
                    help="text substring marking the signature field, e.g. （签名）")
    ap.add_argument("--nth", type=int, default=0, help="which occurrence (0-based)")
    ap.add_argument("--inset", type=float, default=2.5, help="margin from frame edges (pt)")
    ap.add_argument("--gap", type=float, default=3.0, help="gap below anchor line (pt)")
    ap.add_argument("--box", default=None, help="explicit frame x0,y0,x1,y1")
    ap.add_argument("--rect", default=None, help="explicit region x0,y0,x1,y1")
    ap.add_argument("--no-frames", action="store_true",
                    help="do not list all page frames in the output")
    args = ap.parse_args()

    box = [float(v) for v in args.box.split(",")] if args.box else None
    rect = [float(v) for v in args.rect.split(",")] if args.rect else None
    res = find_region(args.pdf, page_no=args.page, anchor=args.anchor,
                      inset=args.inset, gap=args.gap, nth=args.nth,
                      rect=rect, box=box)
    if args.no_frames and "frames" in res:
        res["frames"] = [f for f in res["frames"] if f["rect"] == res.get("enclosing_frame")]
    status = "error" if res.get("mode") == "error" else "ok"
    print(json.dumps({"status": status, **res}, ensure_ascii=False, indent=2))
    sys.exit(1 if status == "error" else 0)


if __name__ == "__main__":
    main()
