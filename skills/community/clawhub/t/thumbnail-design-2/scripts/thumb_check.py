#!/usr/bin/env python3
"""Quality check for a thumbnail (pip install pillow).

Usage: thumb_check.py IMAGE [--layout IMAGE.layout.json] [--preview DIR] [--json out.json]

Checks
  file     format, 16:9 (or 9:16) ratio, size in pixels, file size vs YouTube's mobile upload limit (2 MB)
  image    brightness, contrast, colourfulness, detail in the bottom-right corner (YouTube's duration badge covers it)
  layout   (needs the .layout.json written by thumb_compose.py) word count, text height at feed size,
           text contrast against the pixels behind it, margins, overlap of text and badge corner, text vs subject overlap
  preview  small-size renders (feed 360 px, mobile 168 px) on dark and light backgrounds in one sheet

These are heuristics. They catch common mistakes; they cannot judge whether a thumbnail will get clicks.
"""
import argparse
import json
import math
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageStat
except ImportError:
    sys.exit("Pillow is required: pip install pillow")


def lum(rgb):
    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb[:3]
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def pix(im):
    return list(im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata())


def colourfulness(im):
    """Hasler-Suesstrunk colourfulness metric on a small RGB image."""
    r, g, b = (pix(c) for c in im.convert("RGB").split())
    rg = [x - y for x, y in zip(r, g)]
    yb = [0.5 * (x + y) - z for x, y, z in zip(r, g, b)]

    def ms(v):
        m = sum(v) / len(v)
        return m, math.sqrt(sum((x - m) ** 2 for x in v) / len(v))
    (m1, s1), (m2, s2) = ms(rg), ms(yb)
    return math.sqrt(s1 ** 2 + s2 ** 2) + 0.3 * math.sqrt(m1 ** 2 + m2 ** 2)


def detail(im):
    return ImageStat.Stat(im.convert("L").filter(ImageFilter.FIND_EDGES)).mean[0]


def overlap(a, b):
    x1, y1, x2, y2 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    return max(0, x2 - x1) * max(0, y2 - y1)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image")
    ap.add_argument("--layout")
    ap.add_argument("--preview")
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    p = Path(a.image)
    if not p.exists():
        print(f"error: {p} not found", file=sys.stderr)
        return 1
    im = Image.open(p)
    fmt = im.format
    im = im.convert("RGB")
    W, H = im.size
    res = []  # (level, text)

    def add(level, text):
        res.append((level, text))

    size_b = p.stat().st_size
    if fmt not in ("JPEG", "PNG"):
        add("FAIL", f"Format {fmt}: YouTube accepts JPG or PNG.")
    vertical = H > W
    target = 9 / 16 if vertical else 16 / 9
    if abs(W / H - target) > 0.01:
        add("FAIL", f"Aspect ratio {W}:{H} is not {'9:16' if vertical else '16:9'}.")
    if (not vertical and W < 640) or (vertical and H < 640):
        add("FAIL", f"{W}x{H} is below YouTube's minimum ({'height' if vertical else 'width'} 640 px).")
    elif not vertical and W < 1280:
        add("WARN", f"{W}px wide; 1280x720 is the usual minimum for a sharp thumbnail.")
    if size_b > 2 * 1024 * 1024:
        add("WARN", f"{size_b / 1048576:.2f} MB: over 2 MB, which can fail on mobile uploads (desktop allows more).")
    else:
        add("OK", f"{W}x{H} {fmt}, {size_b / 1024:.0f} KB.")

    small = im.resize((320, round(320 * H / W)))
    st = ImageStat.Stat(small.convert("L"))
    mean, std = st.mean[0], st.stddev[0]
    if mean < 45:
        add("WARN", f"Very dark (mean luminance {mean:.0f}/255); it may vanish on YouTube's dark theme.")
    elif mean > 215:
        add("WARN", f"Very bright (mean {mean:.0f}/255); it may wash out on white feeds.")
    if std < 28:
        add("WARN", f"Low contrast (std {std:.0f}); the image looks flat at small size.")
    cf = colourfulness(small)
    if cf < 25:
        add("INFO", f"Muted colours (score {cf:.0f}); fine if intentional, otherwise add a contrasting accent.")
    br_box = (int(W * 0.78), int(H * 0.82), W, H)
    corner = im.crop(br_box)
    cd = detail(corner)
    if cd > 18:
        add("INFO", "Busy bottom-right corner: YouTube's duration badge covers it; keep key content away from it.")

    layout = None
    lp = Path(a.layout) if a.layout else p.with_suffix(".layout.json")
    if lp.exists():
        layout = json.loads(lp.read_text(encoding="utf-8"))
    elif a.layout:
        add("WARN", f"Layout file {lp} not found; text checks skipped.")
    if layout:
        texts, subs = layout.get("texts", []), layout.get("subjects", [])
        words = sum(len(t["text"].split()) for t in texts)
        if not texts:
            add("INFO", "No text layer. That can work for image-led thumbnails; check the title carries the promise.")
        if words > 6:
            add("WARN", f"{words} words of thumbnail text; aim for 1 to 5 so it reads at a glance.")
        for t in texts:
            x1, y1, x2, y2 = t["bbox"]
            feed_px = t["font_px"] * 360 / W
            if feed_px < 14:
                add("WARN", f"Text '{t['text'][:30]}' is about {feed_px:.0f}px tall in a 360px-wide feed; make it larger or shorter.")
            m = min(x1, y1, W - x2, H - y2)
            if m < W * 0.025:
                add("WARN", f"Text '{t['text'][:30]}' is {m}px from an edge; keep at least about 3% margin.")
            if overlap(t["bbox"], br_box) > 0:
                add("WARN", f"Text '{t['text'][:30]}' overlaps the bottom-right corner covered by the duration badge.")
            region = im.crop((max(x1, 0), max(y1, 0), min(x2, W), min(y2, H)))
            if region.width > 4 and region.height > 4:
                bgc = ImageStat.Stat(region).median
                r = ratio(hex_rgb(t["color"]), tuple(int(v) for v in bgc))
                if r < 3:
                    add("INFO", f"Text '{t['text'][:30]}': fill vs background contrast {r:.1f}:1 (the outline helps, but check by eye).")
            for s in subs:
                ov = overlap(t["bbox"], s["bbox"])
                area = max(1, (x2 - x1) * (y2 - y1))
                if ov / area > 0.25:
                    add("WARN", f"Text '{t['text'][:30]}' overlaps the subject by {ov / area:.0%}; move one of them.")
        for s in subs:  # an image layer placed (partly) outside the canvas is silently cropped by the composer
            x1, y1, x2, y2 = s["bbox"]
            area = max(1, (x2 - x1) * (y2 - y1))
            vis = overlap(s["bbox"], (0, 0, W, H)) / area
            if vis < 0.5:
                add("FAIL", f"Image layer {s['file']} is {vis:.0%} visible (mostly off the canvas). In image layers, x and y "
                            "are margins from the anchor edge, not positions: try x 0, y 0.")
            elif vis < 0.9:
                add("WARN", f"Image layer {s['file']} is only {vis:.0%} inside the canvas; check the crop is intended.")
        for n in layout.get("notes", []):
            add("WARN", n)
    add("INFO", "Look at the small preview: is the idea clear in one second, with one focal point and one emotion?")

    if a.preview:
        d = Path(a.preview)
        d.mkdir(parents=True, exist_ok=True)
        sizes = [(360, "feed"), (168, "mobile")]
        sheet = Image.new("RGB", (360 * 2 + 60, 202 + 94 + 70), (24, 24, 28))
        dr = ImageDraw.Draw(sheet)
        x = 20
        for bgc, off in (((24, 24, 28), 0), ((250, 250, 250), 380)):
            dr.rectangle([off, 0, off + 380, sheet.height], fill=bgc)
            y = 20
            for w, name in sizes:
                t = im.resize((w, round(w * H / W)), Image.LANCZOS)
                sheet.paste(t, (off + 10, y))
                y += t.height + 24
        sheet.save(d / "preview.png")
        add("INFO", f"Wrote {d / 'preview.png'} (feed and mobile sizes on dark and light backgrounds).")

    icon = {"FAIL": "[FAIL]", "WARN": "[WARN]", "INFO": "[INFO]", "OK": "[ OK ]"}
    for lvl, t in res:
        print(f"{icon[lvl]} {t}")
    fails = sum(1 for l, _ in res if l == "FAIL")
    warns = sum(1 for l, _ in res if l == "WARN")
    print(f"\n{fails} fail, {warns} warn. Heuristics only; compare with real CTR data once the video is live.")
    if a.json:
        Path(a.json).write_text(json.dumps([{"level": l, "text": t} for l, t in res], indent=2), encoding="utf-8")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
