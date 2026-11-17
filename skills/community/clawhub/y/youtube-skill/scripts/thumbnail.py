#!/usr/bin/env python3
"""Render YouTube thumbnail options from frames of the video (or a photo), plus a preview
of how each one looks at the sizes YouTube shows it.

    python3 scripts/thumbnail.py thumbs.json --out pack/

thumbs.json:
{
  "video": "final.mp4",
  "title": "The chosen title",            # for the preview only
  "channel": "Channel name",               # for the preview only
  "accent": "#FFD43B",                     # highlight colour
  "options": [
    {"name": "a", "frame": 83.2, "text": "Rings gone by 2025?", "highlight": "gone",
     "layout": "side", "side": "left", "focus": [0.6, 0.5], "zoom": 1.2},
    {"name": "b", "frame": "2:41", "text": "Saturn without rings", "layout": "box", "side": "right"},
    {"name": "c", "image": "photo.jpg", "layout": "none"}
  ]
}

layout: "side"  big white words on a dark fade from one side (the default)
        "box"   dark words on accent-coloured bars
        "none"  no words; the picture and the title do the work
frame:  seconds or "m:ss"; the sharpest frame within 0.25 s is used, so motion blur is avoided
focus:  the point to keep in the centre when cropping or zooming, as fractions of width/height
zoom:   1.0 to 2.5, crops in on the focus point

Writes thumb-<name>.jpg: 16:9 at the source's size up to 3840x2160, or 9:16 up to 2160x3840
for a vertical video (a Short), as YouTube recommends, and under 2 MB so it uploads from a
phone too. "short_side": 720 in thumbs.json forces a smaller size, "vertical": true/false
overrides the shape. Also preview.png: every option as a home-feed card and a small "up next"
card (or, for a Short, a Shorts-shelf card), with the title, on YouTube's dark background, and
thumbnails.json with sizes and warnings.
Needs Pillow; ffmpeg for frames.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile

try:
    from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageStat
except ImportError:
    sys.exit("Thumbnails need Pillow: pip install pillow")

W, H, S = 1280, 720, 1.0             # set per run: up to 3840x2160, never above the source
VERTICAL = False                     # a Short: 9:16, up to 2160x3840
MAX_BYTES = 2 * 1024 * 1024          # the phone upload limit; desktop allows 50 MB
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "fonts")


def set_size(short_side, vertical=False):
    """YouTube recommends 3840x2160 for videos and 2160x3840 for Shorts. Rendering above the
    source adds nothing, so the size follows the source's short side: 720, 1080, 1440 or 2160.
    Layout numbers below are for a 720-pixel short side and scale with S."""
    global W, H, S, VERTICAL
    short = max(v for v in (720, 1080, 1440, 2160) if v <= max(720, short_side))
    VERTICAL = vertical
    W, H = (short, short * 16 // 9) if vertical else (short * 16 // 9, short)
    S = short / 720


def px(v):
    return round(v * S)


SAFE_1280 = 56          # margin from the edges
STAMP_1280 = (300, 140) # the duration badge covers the bottom-right corner
MIN_TEXT = 80           # px at 1280 wide; smaller words disappear on a phone


def font(name, size, weight=None):
    f = ImageFont.truetype(os.path.join(FONTS, name), size)
    if weight:
        try:
            f.set_variation_by_name(weight)
        except Exception:
            pass
    return f


def secs(t):
    if isinstance(t, (int, float)):
        return float(t)
    total = 0.0
    for p in str(t).split(":"):
        total = total * 60 + float(p)
    return total


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def video_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                          "default=nw=1:nk=1", path], capture_output=True, text=True).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return 0.0


def grab(video, t, tmp):
    """The sharpest full-resolution frame within 0.25 s of t."""
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg is needed to take frames from the video.")
    best = None
    start = max(0.0, t - 0.25)
    pattern = os.path.join(tmp, f"g{int(t * 1000)}_%02d.png")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{start:.3f}", "-i", video, "-t", "0.5",
                    "-vf", "fps=10", "-frames:v", "6", pattern], check=True)
    for k in range(1, 7):
        p = pattern % k
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGB")
        sharp = ImageStat.Stat(im.convert("L").resize((640, int(640 * im.height / im.width)))
                               .filter(ImageFilter.FIND_EDGES)).var[0]
        if best is None or sharp > best[0]:
            best = (sharp, im)
    if best is None:
        sys.exit(f"Could not read a frame at {t:.2f} s.")
    return best[1]


def cover(im, focus=(0.5, 0.5), zoom=1.0):
    zoom = max(1.0, min(float(zoom), 2.5))
    scale = max(W / im.width, H / im.height) * zoom
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    fx, fy = focus
    x = min(max(0, round(fx * im.width - W / 2)), im.width - W)
    y = min(max(0, round(fy * im.height - H / 2)), im.height - H)
    return im.crop((x, y, x + W, y + H))


def grade(im):
    """A thumbnail-strength grade: a little more contrast, colour and crispness."""
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im = ImageEnhance.Color(im).enhance(1.12)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))


def wrap(words, f, max_w, max_lines):
    """Balanced lines: every line fits and the longest is as short as possible."""
    n = len(words)
    best = None

    def width(ws):
        return f.getlength(" ".join(ws))

    def splits(i, lines_left):
        if lines_left == 1:
            yield [words[i:]]
            return
        for j in range(i + 1, n - lines_left + 2):
            for rest in splits(j, lines_left - 1):
                yield [words[i:j]] + rest

    for k in range(1, min(max_lines, n) + 1):
        for s in splits(0, k):
            widest = max(width(x) for x in s)
            if widest > max_w:
                continue
            orphan = 1 if k > 1 and len(s[-1]) == 1 and len(" ".join(s[-1])) < 5 else 0
            cost = (widest, orphan, k)
            if best is None or (orphan, widest) < (best[0][1], best[0][0]):
                best = (cost, s)
        if best:
            return best[1]
    return None


def fit_text(text, max_w, max_h, max_lines=3, start=170, spacing=1.02):
    words = text.split()
    for size in range(px(start), px(40), -max(1, px(4))):
        f = font("Poppins-ExtraBold.ttf", size)
        lines = wrap(words, f, max_w, max_lines)
        if not lines:
            continue
        lh = round(size * spacing)
        if lh * len(lines) <= max_h:
            return f, size, [" ".join(l) for l in lines], lh
    return None


def word_key(w):
    """A word as highlight matching sees it: lower case, straight apostrophes, no punctuation."""
    return re.sub(r"[^\w']", "", w.replace("\u2019", "'")).lower()


def draw_words(d, x, y, line, f, color, hi_words, accent, stroke):
    """One line, left-aligned at x, with highlighted words in the accent colour."""
    cx = x
    for i, w in enumerate(line.split(" ")):
        piece = w + (" " if i < len(line.split(" ")) - 1 else "")
        col = accent if word_key(w) in hi_words else color
        d.text((cx, y), piece, font=f, fill=col, stroke_width=stroke, stroke_fill=(0, 0, 0))
        cx += f.getlength(piece)


def render(opt, spec, base_dir, tmp, warn):
    if opt.get("image"):
        p = opt["image"] if os.path.isabs(opt["image"]) else os.path.join(base_dir, opt["image"])
        im = Image.open(p).convert("RGB")
    else:
        video = spec["video"] if os.path.isabs(spec["video"]) else os.path.join(base_dir, spec["video"])
        im = grab(video, secs(opt.get("frame", 0)), tmp)
    src_w = im.width
    SAFE, STAMP_ZONE = px(SAFE_1280), (W - px(STAMP_1280[0]), H - px(STAMP_1280[1]))
    im = cover(im, tuple(opt.get("focus", (0.5, 0.5))), opt.get("zoom", 1.0))
    if src_w / max(1.0, min(float(opt.get("zoom", 1.0)), 2.5)) < W * 0.75:
        warn.append(f"{opt['name']}: the picture is enlarged a lot ({src_w}px wide source); it may look soft.")
    if opt.get("grade", True):
        im = grade(im)
    layout = opt.get("layout", "side" if opt.get("text") else "none")
    text = re.sub(r"(\w)'(\w)", "\\1\u2019\\2", (opt.get("text") or "").strip())  # curly apostrophes
    if layout == "none" or not text:
        return im
    n_words = len(text.split())
    if n_words > 6:
        warn.append(f"{opt['name']}: {n_words} words. Thumbnails read best with 2 to 5; the title carries the rest.")
    side = "center" if VERTICAL else opt.get("side", "left")
    accent = hex_rgb(spec.get("accent", "#FFD43B"))
    hl = opt.get("highlight", "")
    hl = " ".join(hl) if isinstance(hl, list) else str(hl)
    hi = {word_key(w) for w in hl.split()}
    missing = [w for w in hi if w and w not in {word_key(x) for x in text.split()}]
    if missing:
        warn.append(f"{opt['name']}: highlight word(s) not in the text: {', '.join(missing)}.")
    if VERTICAL:
        # Shorts: words across the upper part; the bottom third sits under the title and buttons
        region_w, region_h = W - 2 * SAFE, int(H * 0.36)
    else:
        region_w = int(W * (0.56 if layout == "side" else 0.60)) - SAFE
        region_h = H - 2 * SAFE - (px(90) if side == "right" else 0)
    fit = fit_text(text, region_w - (px(44) if layout == "box" else 0), region_h,
                   spacing=1.34 if layout == "box" else 1.02)
    if not fit:
        warn.append(f"{opt['name']}: the words don't fit; use fewer.")
        return im
    f, size, lines, lh = fit
    if size < px(MIN_TEXT):
        warn.append(f"{opt['name']}: the words end up small ({size / S:.0f}px at 1280 wide; under {MIN_TEXT} they "
                    "vanish on a phone). Use fewer words.")
    block_h = lh * len(lines)
    widths = [f.getlength(l) for l in lines]
    if layout == "side":
        shade = Image.new("L", (W, H), 0)
        sd = ImageDraw.Draw(shade)
        span = int(W * 0.72)
        for i in range(span):
            a = int(200 * (1 - i / span) ** 1.6)
            x = i if side == "left" else W - 1 - i
            sd.line([(x, 0), (x, H)], fill=a)
        if VERTICAL:
            shade = Image.new("L", (W, H), 0)
            sd = ImageDraw.Draw(shade)
            span = int(H * 0.62)
            for i in range(span):
                sd.line([(0, i), (W, i)], fill=int(190 * (1 - i / span) ** 1.4))
        im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, shade)
    d = ImageDraw.Draw(im)
    y0 = max(SAFE, min(round(H * 0.46 - block_h / 2), H - SAFE - block_h))
    if VERTICAL:
        y0 = max(px(110), round(H * 0.24 - block_h / 2))
    if side == "right":
        y0 = min(y0, STAMP_ZONE[1] - block_h - px(20))
    stroke = max(px(4), round(size * 0.06)) if layout == "side" else 0
    if layout == "side":
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        shd = ImageDraw.Draw(shadow)
    if layout == "box":
        # bars sized from the font's real ink (ascenders and descenders), drawn before any words
        top_ink, bottom_ink = f.getbbox("HgjpyÉ")[1], f.getbbox("Hgjpy")[3]
        pad_x, pad_y = px(24), round(size * 0.08)
        for k in range(len(lines)):
            x = (W - widths[k]) // 2 if side == "center" else SAFE if side == "left" else W - SAFE - widths[k]
            ty = y0 + k * lh
            d.rounded_rectangle([x - pad_x, ty + top_ink - pad_y, x + widths[k] + pad_x, ty + bottom_ink + pad_y],
                                radius=px(12), fill=accent)
        for k, line in enumerate(lines):
            x = (W - widths[k]) // 2 if side == "center" else SAFE if side == "left" else W - SAFE - widths[k]
            draw_words(d, x, y0 + k * lh, line, f, (15, 15, 15), hi, hex_rgb(spec.get("box_highlight", "#D62828")), 0)
        return im
    for k, line in enumerate(lines):
        x = (W - widths[k]) // 2 if side == "center" else SAFE if side == "left" else W - SAFE - widths[k]
        y = y0 + k * lh - round(size * 0.12)
        shd.text((x + px(6), y + px(8)), line, font=f, fill=(0, 0, 0, 170), stroke_width=stroke,
                 stroke_fill=(0, 0, 0, 170))
    if True:
        shadow = shadow.filter(ImageFilter.GaussianBlur(px(8)))
        im = Image.alpha_composite(im.convert("RGBA"), shadow).convert("RGB")
        d = ImageDraw.Draw(im)
        for k, line in enumerate(lines):
            x = (W - widths[k]) // 2 if side == "center" else SAFE if side == "left" else W - SAFE - widths[k]
            draw_words(d, x, y0 + k * lh - round(size * 0.12), line, f, (255, 255, 255), hi, accent, stroke)
    return im


def save_jpeg(im, path):
    """Best quality under 2 MB (the limit when uploading from a phone); steps the size down if
    even quality 72 is too big. Returns (quality, size, fits)."""
    while True:
        for q in (92, 88, 84, 80, 76, 72):
            im.save(path, "JPEG", quality=q, optimize=True, progressive=True)
            if os.path.getsize(path) <= MAX_BYTES:
                return q, im.size, True
        if min(im.size) <= 720:
            for q in (65, 55, 45):
                im.save(path, "JPEG", quality=q, optimize=True, progressive=True)
                if os.path.getsize(path) <= MAX_BYTES:
                    return q, im.size, True
            return q, im.size, False
        f = {2160: 1440, 1440: 1080}.get(min(im.size), 720) / min(im.size)
        im = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)


def ellipsize(text, f, max_w, max_lines):
    words, lines, cur = text.split(), [], ""
    for i, w in enumerate(words):
        t = (cur + " " + w).strip()
        if f.getlength(t) <= max_w:
            cur = t
            continue
        lines.append(cur)
        cur = w
        if len(lines) == max_lines:
            last = lines[-1]
            while f.getlength(last + "...") > max_w and " " in last:
                last = last.rsplit(" ", 1)[0]
            lines[-1] = last + "..."
            return lines
    lines.append(cur)
    return lines[:max_lines]


def badge(d, x2, y2, label, size):
    f = font("Inter.ttf", size, "SemiBold")
    tw = f.getlength(label)
    pad = round(size * 0.35)
    d.rounded_rectangle([x2 - tw - 2 * pad, y2 - size - 2 * pad + 2, x2, y2], radius=4, fill=(0, 0, 0, 200))
    d.text((x2 - tw - pad, y2 - size - pad - 1), label, font=f, fill=(255, 255, 255))


def preview_shorts(thumbs, spec, out):
    """Shorts-shelf cards (about 200 wide, 9:16) with the title under each, on the dark theme."""
    title = spec.get("title", "")
    cw, gap, pad = 210, 20, 32
    ch = round(cw * 16 / 9)
    n = len(thumbs)
    width = max(pad * 2 + n * cw + (n - 1) * gap, 520)
    bg = Image.new("RGB", (width, ch + 170), (15, 15, 15))
    d = ImageDraw.Draw(bg, "RGBA")
    hf = font("Inter.ttf", 15, "SemiBold")
    tf = font("Inter.ttf", 15, "SemiBold")
    d.text((pad, 18), "Shorts shelf (phone)", font=hf, fill=(170, 170, 170))
    for i, (name, im) in enumerate(thumbs):
        x, y = pad + i * (cw + gap), 48
        card = im.resize((cw, ch), Image.LANCZOS)
        mask = Image.new("L", (cw, ch), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, cw - 1, ch - 1], radius=12, fill=255)
        bg.paste(card, (x, y), mask)
        for k, line in enumerate(ellipsize(title, tf, cw, 2)):
            d.text((x, y + ch + 10 + k * 20), line, font=tf, fill=(241, 241, 241))
        d.text((x, y + ch + 60), f"option {name}", font=hf, fill=(255, 212, 59))
    bg.save(os.path.join(out, "preview.png"))


def preview(thumbs, spec, dur, out):
    """Home-feed cards (thumbnail 360 wide) and 'up next' cards (168 wide) on YouTube's dark theme."""
    if VERTICAL:
        return preview_shorts(thumbs, spec, out)
    title = spec.get("title", "")
    channel = spec.get("channel", "Your channel")
    m, s = divmod(int(dur), 60)
    h, m = divmod(m, 60)
    label = f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
    cw, gap, pad = 360, 24, 32
    n = len(thumbs)
    width = pad * 2 + n * cw + (n - 1) * gap
    height = 760
    bg = Image.new("RGB", (width, height), (15, 15, 15))
    d = ImageDraw.Draw(bg, "RGBA")
    hf = font("Inter.ttf", 15, "SemiBold")
    d.text((pad, 18), "Home feed (desktop)", font=hf, fill=(170, 170, 170))
    tf = font("Inter.ttf", 16, "SemiBold")
    cf = font("Inter.ttf", 14, "Regular")
    for i, (name, im) in enumerate(thumbs):
        x, y = pad + i * (cw + gap), 48
        th = round(cw * 9 / 16)
        card = im.resize((cw, th), Image.LANCZOS)
        mask = Image.new("L", (cw, th), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, cw - 1, th - 1], radius=12, fill=255)
        bg.paste(card, (x, y), mask)
        badge(d, x + cw - 8, y + th - 8, label, 12)
        d.ellipse([x, y + th + 12, x + 36, y + th + 48], fill=(70, 70, 70))
        for k, line in enumerate(ellipsize(title, tf, cw - 48, 2)):
            d.text((x + 48, y + th + 12 + k * 22), line, font=tf, fill=(241, 241, 241))
        d.text((x + 48, y + th + 60), channel, font=cf, fill=(170, 170, 170))
        d.text((x, y + th + 92), f"option {name}", font=hf, fill=(255, 212, 59))
    y2 = 400
    d.text((pad, y2), "Up next / search on a phone (small)", font=hf, fill=(170, 170, 170))
    sw, sh = 168, 94
    sf = font("Inter.ttf", 14, "SemiBold")
    per_row = max(1, (width - 2 * pad) // (sw + 220))
    for i, (name, im) in enumerate(thumbs):
        col, row = i % per_row, i // per_row
        x, y = pad + col * (sw + 220), y2 + 34 + row * (sh + 30)
        small = im.resize((sw, sh), Image.LANCZOS)
        mask = Image.new("L", (sw, sh), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw - 1, sh - 1], radius=8, fill=255)
        bg.paste(small, (x, y), mask)
        badge(d, x + sw - 4, y + sh - 4, label, 10)
        for k, line in enumerate(ellipsize(title, sf, 200, 2)):
            d.text((x + sw + 10, y + k * 19), line, font=sf, fill=(241, 241, 241))
        d.text((x + sw + 10, y + 44), channel, font=font("Inter.ttf", 12, "Regular"), fill=(170, 170, 170))
    bottom = y2 + 34 + ((n - 1) // per_row + 1) * (sh + 30) + 10
    bg = bg.crop((0, 0, width, max(bottom, 560)))
    bg.save(os.path.join(out, "preview.png"))


def main():
    ap = argparse.ArgumentParser(description="Render YouTube thumbnail options and a preview.")
    ap.add_argument("spec")
    ap.add_argument("--out", default="pack")
    a = ap.parse_args()
    spec = json.load(open(a.spec, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(a.spec))
    os.makedirs(a.out, exist_ok=True)
    warn, thumbs, results = [], [], []
    short, vertical = 720, False
    if spec.get("video"):
        v = spec["video"] if os.path.isabs(spec["video"]) else os.path.join(base, spec["video"])
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                              "stream=width,height:stream_side_data=rotation", "-of", "csv=p=0", v],
                             capture_output=True, text=True).stdout
        try:
            nums = [int(float(x)) for x in re.findall(r"-?\d+(?:\.\d+)?", out)]
            vw, vh = nums[0], nums[1]
            if len(nums) > 2 and abs(nums[2]) in (90, 270):
                vw, vh = vh, vw
            vertical = vh > vw
            short = min(vw, vh) if vertical else min(vh, round(vw * 9 / 16))
        except (ValueError, IndexError):
            pass
    vertical = spec.get("vertical", vertical)
    set_size(int(spec.get("short_side", short)), vertical)
    with tempfile.TemporaryDirectory() as tmp:
        for i, opt in enumerate(spec.get("options", [])):
            opt.setdefault("name", chr(97 + i))
            im = render(opt, spec, base, tmp, warn)
            path = os.path.join(a.out, f"thumb-{opt['name']}.jpg")
            q, size, fits = save_jpeg(im, path)
            if not fits:
                warn.append(f"{opt['name']}: over 2 MB even at low quality; upload it from a computer (50 MB limit).")
            thumbs.append((opt["name"], im))
            results.append({"name": opt["name"], "file": os.path.basename(path), "bytes": os.path.getsize(path),
                            "size": f"{size[0]}x{size[1]}", "quality": q})
    if not thumbs:
        sys.exit("thumbs.json has no options.")
    dur = 0.0
    if spec.get("video"):
        v = spec["video"] if os.path.isabs(spec["video"]) else os.path.join(base, spec["video"])
        dur = video_duration(v) if shutil.which("ffprobe") else 0.0
    preview(thumbs, spec, dur, a.out)
    with open(os.path.join(a.out, "thumbnails.json"), "w", encoding="utf-8") as fh:
        json.dump({"thumbnails": results, "warnings": warn}, fh, indent=2)
    for r in results:
        print(f"thumb-{r['name']}.jpg  {r['size']}  {r['bytes'] / 1024:.0f} KB")
    for w in warn:
        print("WARNING:", w)
    print(f"-> {a.out}/preview.png (judge them there, at the size people see them)")


if __name__ == "__main__":
    main()
