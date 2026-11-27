#!/usr/bin/env python3
"""Compose YouTube thumbnails from a JSON spec with Pillow (pip install pillow).

Commands
  render   SPEC.json                      render one thumbnail (+ SPEC output .layout.json for thumb_check.py)
  variants SPEC.json --texts "A|B|C" [--themes dark,bright,warm,cool] [--flip] [--max 6] [--outdir DIR]
                                          render several variations and a contact sheet
  resize   IMAGE --to youtube|youtube_hd|shorts|WxH [--focus 0.5,0.5] [--out PATH]
                                          cover-crop an existing image to another size (re-layout is better)
  sheet    IMG [IMG ...] --out sheet.jpg  contact sheet with labels

Spec (all positions are fractions of the canvas, 0 to 1)
  size        "youtube" (1280x720) | "youtube_hd" (1920x1080) | "shorts" (1080x1920) | "WxH"
  output      path (.jpg or .png)           max_mb  default 1.9 (YouTube mobile uploads allow 2 MB)
  background  {image, focus:[x,y], blur, darken, saturation, contrast, vignette}
              or {gradient:[c1,c2], angle}  or {color}
  layers      list, drawn in order:
    {type:"image", file, anchor:left|right|center, height|width, x, y, valign:bottom|center|top,
     outline:{color,width}, glow:{color,radius}, shadow:true}
       NOTE: for image layers x and y are MARGINS from the anchor/valign edge (x 0 = touching that edge), not
       positions. anchor "right" with x 0.9 pushes the image almost off the left side. thumb_check flags that.
    {type:"text", text, box:[x,y,w,h], font, color, stroke:{color,width}, shadow:true,
     highlight:{words:[..], color}, align:left|center|right, max_lines, uppercase, line_gap}
    {type:"shape", shape:arrow|circle|rect|rounded|badge, xy:[x1,y1,x2,y2], color, width, fill, text}
"""
import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
except ImportError:
    sys.exit("Pillow is required: pip install pillow")

SIZES = {"youtube": (1280, 720), "youtube_hd": (1920, 1080), "shorts": (1080, 1920)}
THEMES = {
    "dark": {"color": "#FFFFFF", "stroke": "#000000", "highlight": "#FFE600"},
    "bright": {"color": "#FFE600", "stroke": "#000000", "highlight": "#FFFFFF"},
    "warm": {"color": "#FFFFFF", "stroke": "#7A1500", "highlight": "#FF8A00"},
    "cool": {"color": "#FFFFFF", "stroke": "#04204D", "highlight": "#35E0FF"},
}
FONT_FALLBACKS = [
    "/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Impact.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "C:/Windows/Fonts/impact.ttf", "C:/Windows/Fonts/arialbd.ttf",
]


class Fail(RuntimeError):
    pass


def parse_size(s):
    if isinstance(s, (list, tuple)) and len(s) == 2:
        return int(s[0]), int(s[1])
    if s in SIZES:
        return SIZES[s]
    m = re.fullmatch(r"(\d{3,5})x(\d{3,5})", str(s or "youtube"))
    if not m:
        raise Fail(f"Bad size {s!r}; use youtube, youtube_hd, shorts or WIDTHxHEIGHT.")
    return int(m.group(1)), int(m.group(2))


def hexc(c, alpha=255):
    if isinstance(c, (list, tuple)):
        return tuple(c) + ((alpha,) if len(c) == 3 else ())
    c = str(c).lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", c):
        raise Fail(f"Bad colour {c!r}; use #RRGGBB.")
    return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), alpha)


# ---- fonts -------------------------------------------------------------------
def find_font(name):
    if name and Path(name).exists():
        return name
    if name and shutil.which("fc-match"):
        try:
            out = subprocess.run(["fc-match", "-f", "%{file}", f"{name}:bold"], capture_output=True, text=True,
                                 timeout=10).stdout.strip()
            if out and Path(out).exists() and name.split()[0].lower() in Path(out).name.lower():
                return out
        except (OSError, subprocess.SubprocessError):
            pass
    for f in FONT_FALLBACKS:
        if Path(f).exists():
            return f
    return None


def load_font(path, size):
    if not path:
        try:
            return ImageFont.load_default(size)
        except TypeError:
            return ImageFont.load_default()
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_name("Bold")
    except Exception:
        pass
    return f


# ---- background --------------------------------------------------------------
def cover(img, w, h, focus=(0.5, 0.5)):
    iw, ih = img.size
    s = max(w / iw, h / ih)
    nw, nh = max(w, round(iw * s)), max(h, round(ih * s))
    img = img.resize((nw, nh), Image.LANCZOS)
    fx, fy = focus
    left = min(max(round(fx * nw - w / 2), 0), nw - w)
    top = min(max(round(fy * nh - h / 2), 0), nh - h)
    return img.crop((left, top, left + w, top + h))


def make_background(spec, w, h, base, notes):
    bg = spec or {}
    if bg.get("image"):
        p = Path(base) / bg["image"]
        if not p.exists():
            raise Fail(f"Background image not found: {p}")
        src = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
        if src.width < w * 0.9:
            notes.append(f"Background is only {src.width}px wide for a {w}px canvas; it will look soft. Use a larger image or upscale.")
        img = cover(src, w, h, tuple(bg.get("focus", (0.5, 0.5))))
    elif bg.get("gradient"):
        c1, c2 = (hexc(x)[:3] for x in bg["gradient"][:2])
        d = int(math.hypot(w, h)) + 4
        mask = Image.linear_gradient("L").resize((d, d), Image.BICUBIC).rotate(bg.get("angle", 0) + 0.0,
                                                                          resample=Image.BICUBIC)
        left, top = (d - w) // 2, (d - h) // 2
        mask = mask.crop((left, top, left + w, top + h))
        img = Image.composite(Image.new("RGB", (w, h), c2), Image.new("RGB", (w, h), c1), mask)
    else:
        img = Image.new("RGB", (w, h), hexc(bg.get("color", "#101418"))[:3])
    if bg.get("blur"):
        img = img.filter(ImageFilter.GaussianBlur(float(bg["blur"])))
    if bg.get("saturation") is not None:
        img = ImageEnhance.Color(img).enhance(float(bg["saturation"]))
    if bg.get("contrast") is not None:
        img = ImageEnhance.Contrast(img).enhance(float(bg["contrast"]))
    if bg.get("darken"):
        img = Image.blend(img, Image.new("RGB", (w, h), (0, 0, 0)), min(max(float(bg["darken"]), 0), 0.9))
    if bg.get("vignette"):
        v = min(max(float(bg["vignette"]), 0), 1)
        m = Image.radial_gradient("L").resize((w, h), Image.BICUBIC).point(lambda p: int(p * v))
        img = Image.composite(Image.new("RGB", (w, h), (0, 0, 0)), img, m)
    return img.convert("RGBA")


# ---- layers ------------------------------------------------------------------
def dilate(alpha, px):
    out = alpha
    left = int(px)
    while left > 0:
        k = min(left, 7)
        out = out.filter(ImageFilter.MaxFilter(2 * k + 1))
        left -= k
    return out


def paste_effects(canvas, im, pos, layer):
    """Draw shadow / glow / outline for an RGBA image, then the image itself."""
    alpha = im.getchannel("A")
    pad = 80
    big = Image.new("L", (im.width + 2 * pad, im.height + 2 * pad), 0)
    big.paste(alpha, (pad, pad))
    ox, oy = pos[0] - pad, pos[1] - pad
    if layer.get("shadow"):
        sh = big.filter(ImageFilter.GaussianBlur(14)).point(lambda p: int(p * 0.6))
        black = Image.new("RGBA", big.size, (0, 0, 0, 255))
        black.putalpha(sh)
        _paste(canvas, black, (ox + 8, oy + 12))
    g = layer.get("glow")
    if g:
        r = float(g.get("radius", 20))
        m = dilate(big, r / 3).filter(ImageFilter.GaussianBlur(r / 2))
        col = Image.new("RGBA", big.size, hexc(g.get("color", "#FFFFFF")))
        col.putalpha(m)
        _paste(canvas, col, (ox, oy))
    o = layer.get("outline")
    if o:
        m = dilate(big, int(o.get("width", 6))).filter(ImageFilter.GaussianBlur(0.8))
        col = Image.new("RGBA", big.size, hexc(o.get("color", "#FFFFFF")))
        col.putalpha(m)
        _paste(canvas, col, (ox, oy))
    _paste(canvas, im, pos)


def _paste(canvas, im, pos):
    """alpha_composite that tolerates negative or overflowing positions."""
    x, y = pos
    sx, sy = max(0, -x), max(0, -y)
    ex, ey = min(im.width, canvas.width - x), min(im.height, canvas.height - y)
    if ex <= sx or ey <= sy:
        return
    canvas.alpha_composite(im.crop((sx, sy, ex, ey)), (x + sx, y + sy))


def draw_image(canvas, layer, base, meta):
    p = Path(base) / layer["file"]
    if not p.exists():
        raise Fail(f"Image layer not found: {p}")
    im = Image.open(p).convert("RGBA")
    if im.getextrema()[3] == (255, 255):
        meta["notes"].append(f"{layer['file']} has no transparency; cut the subject out first (thumb_assets.py cutout).")
    W, H = canvas.size
    if layer.get("height"):
        s = layer["height"] * H / im.height
    elif layer.get("width"):
        s = layer["width"] * W / im.width
    else:
        s = 0.9 * H / im.height
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    anchor = layer.get("anchor", "right")
    mx = layer.get("x", 0.0) * W
    x = {"left": mx, "right": W - im.width - mx, "center": (W - im.width) / 2 + mx}.get(anchor, mx)
    va = layer.get("valign", "bottom")
    my = layer.get("y", 0.0) * H
    y = {"bottom": H - im.height - my, "top": my, "center": (H - im.height) / 2 + my}.get(va, my)
    pos = (round(x), round(y))
    paste_effects(canvas, im, pos, layer)
    meta["subjects"].append({"file": layer["file"], "bbox": [pos[0], pos[1], pos[0] + im.width, pos[1] + im.height]})


def wrap_fit(words, font, max_w, max_lines):
    lines, cur = [], []
    for w in words:
        t = " ".join(cur + [w])
        if cur and font.getlength(t) > max_w:
            lines.append(cur)
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(cur)
    return lines if len(lines) <= max_lines else None


def draw_text(canvas, layer, meta):
    W, H = canvas.size
    text = layer.get("text", "").strip()
    if not text:
        return
    if layer.get("uppercase", True):
        text = text.upper()
    bx, by, bw, bh = layer.get("box", [0.05, 0.1, 0.6, 0.6])
    bx, by, bw, bh = bx * W, by * H, bw * W, bh * H
    fpath = find_font(layer.get("font"))
    if not fpath:
        meta["notes"].append("No bold font file found; using Pillow's default. Pass a font path in the spec.")
    stroke = layer.get("stroke", {"color": "#000000", "width": max(4, round(H / 70))})
    sw = int(stroke.get("width", 8))
    gap_f = float(layer.get("line_gap", 0.08))
    words = text.split()
    max_lines = int(layer.get("max_lines", 3))
    chosen = None
    for size in range(int(bh), 11, -2):
        font = load_font(fpath, size)
        lines = wrap_fit(words, font, bw - 2 * sw, max_lines)
        if not lines:
            continue
        asc, desc = font.getmetrics()
        lh = asc + desc
        total = lh * len(lines) + lh * gap_f * (len(lines) - 1) + 2 * sw
        if total <= bh:
            chosen = (font, size, lines, lh)
            break
    if not chosen:
        raise Fail(f"Text {text!r} does not fit its box; shorten it or enlarge the box.")
    font, size, lines, lh = chosen
    hl = {w.upper().strip(".,!?:;") for w in (layer.get("highlight") or {}).get("words", [])}
    hlc = hexc((layer.get("highlight") or {}).get("color", "#FFE600"))
    col = hexc(layer.get("color", "#FFFFFF"))
    sc = hexc(stroke.get("color", "#000000"))
    layer_img = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer_img)
    align = layer.get("align", "left")
    y = by + sw
    x0s, x1s = [], []
    for ln in lines:
        widths = [font.getlength(w) for w in ln]
        space = font.getlength(" ")
        lw = sum(widths) + space * (len(ln) - 1)
        x = bx + sw if align == "left" else bx + (bw - lw) / 2 if align == "center" else bx + bw - lw - sw
        x0s.append(x)
        x1s.append(x + lw)
        for w, wd in zip(ln, widths):
            c = hlc if w.upper().strip(".,!?:;") in hl else col
            d.text((x, y), w, font=font, fill=c, stroke_width=sw, stroke_fill=sc)
            x += wd + space
        y += lh * (1 + gap_f)
    if layer.get("shadow", True):
        a = layer_img.getchannel("A")
        sh = a.filter(ImageFilter.GaussianBlur(max(3, size // 14))).point(lambda p: int(p * 0.65))
        black = Image.new("RGBA", canvas.size, (0, 0, 0, 255))
        black.putalpha(ImageChops.offset(sh, max(3, size // 24), max(4, size // 18)))
        canvas.alpha_composite(black)
    canvas.alpha_composite(layer_img)
    box = [round(min(x0s) - sw), round(by), round(max(x1s) + sw), round(min(y - lh * gap_f + sw, by + bh))]
    meta["texts"].append({"text": text, "bbox": box, "font_px": size, "color": "#%02X%02X%02X" % col[:3],
                          "stroke_px": sw, "lines": len(lines)})


def draw_shape(canvas, layer, meta):
    W, H = canvas.size
    S = 2
    ov = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    x1, y1, x2, y2 = (v * (W if i % 2 == 0 else H) * S for i, v in enumerate(layer["xy"]))
    col = hexc(layer.get("color", "#FF2D2D"))
    wd = int(layer.get("width", 14) * S)
    fill = hexc(layer["fill"]) if layer.get("fill") else None
    kind = layer.get("shape", "rect")
    if kind == "arrow":
        ang = math.atan2(y2 - y1, x2 - x1)
        head = wd * 3.2
        bx, by = x2 - head * math.cos(ang), y2 - head * math.sin(ang)
        d.line([(x1, y1), (bx, by)], fill=col, width=wd)
        px, py = -math.sin(ang), math.cos(ang)
        d.polygon([(x2, y2), (bx + px * head * 0.7, by + py * head * 0.7), (bx - px * head * 0.7, by - py * head * 0.7)],
                  fill=col)
    elif kind == "circle":
        d.ellipse([x1, y1, x2, y2], outline=col, width=wd, fill=fill)
    elif kind in ("rect", "rounded", "badge"):
        r = min(abs(x2 - x1), abs(y2 - y1)) * (0.25 if kind != "rect" else 0)
        d.rounded_rectangle([x1, y1, x2, y2], radius=r, outline=None if (kind == "badge" or fill) and not layer.get("color") else col,
                            width=wd if kind != "badge" else 0, fill=fill or (col if kind == "badge" else None))
    else:
        raise Fail(f"Unknown shape {kind!r}.")
    ov = ov.resize((W, H), Image.LANCZOS)
    if layer.get("shadow"):
        sh = ov.getchannel("A").filter(ImageFilter.GaussianBlur(6)).point(lambda p: int(p * 0.5))
        blk = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        blk.putalpha(ImageChops.offset(sh, 4, 6))
        canvas.alpha_composite(blk)
    canvas.alpha_composite(ov)
    if layer.get("text") and kind in ("badge", "rect", "rounded"):
        t = dict(type="text", text=layer["text"], box=[layer["xy"][0], layer["xy"][1], layer["xy"][2] - layer["xy"][0],
                                                        layer["xy"][3] - layer["xy"][1]], align="center",
                 color=layer.get("text_color", "#FFFFFF"), stroke={"color": "#000000", "width": 3}, shadow=False,
                 max_lines=1, font=layer.get("font"))
        draw_text(canvas, t, meta)


def render(spec, base=".", out=None):
    w, h = parse_size(spec.get("size", "youtube"))
    meta = {"size": [w, h], "texts": [], "subjects": [], "notes": []}
    canvas = make_background(spec.get("background"), w, h, base, meta["notes"])
    for layer in spec.get("layers", []):
        t = layer.get("type")
        if t == "image":
            draw_image(canvas, layer, base, meta)
        elif t == "text":
            draw_text(canvas, layer, meta)
        elif t == "shape":
            draw_shape(canvas, layer, meta)
        else:
            raise Fail(f"Unknown layer type {t!r}.")
    out = Path(out or spec.get("output") or "thumbnail.jpg")
    if not out.is_absolute():
        out = Path(base) / out
    out.parent.mkdir(parents=True, exist_ok=True)
    rgb = canvas.convert("RGB")
    limit = float(spec.get("max_mb", 1.9)) * 1024 * 1024
    if out.suffix.lower() == ".png":
        rgb.save(out, optimize=True)
        if out.stat().st_size > limit:
            meta["notes"].append(f"PNG is {out.stat().st_size / 1048576:.1f} MB, over the {limit / 1048576:.1f} MB target; export as .jpg.")
    else:
        for q in (94, 90, 86, 80, 72, 64):
            rgb.save(out, quality=q, optimize=True, subsampling=0 if q >= 90 else 2)
            if out.stat().st_size <= limit:
                break
        else:
            meta["notes"].append("Could not get under the size limit even at quality 64.")
    meta["output"] = str(out)
    meta["bytes"] = out.stat().st_size
    out.with_suffix(".layout.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return out, meta


# ---- variants / sheets / resize -------------------------------------------------
def flip_spec(spec):
    s = json.loads(json.dumps(spec))
    for l in s.get("layers", []):
        if l.get("type") == "image":
            l["anchor"] = {"left": "right", "right": "left"}.get(l.get("anchor", "right"), l.get("anchor"))
        elif l.get("type") == "text" and l.get("box"):
            bx, by, bw, bh = l["box"]
            l["box"] = [1 - bx - bw, by, bw, bh]
            l["align"] = {"left": "right", "right": "left"}.get(l.get("align", "left"), l.get("align"))
        elif l.get("type") == "shape":
            x1, y1, x2, y2 = l["xy"]
            nx1, nx2 = 1 - x1, 1 - x2
            l["xy"] = [nx1, y1, nx2, y2] if l.get("shape") == "arrow" else [min(nx1, nx2), y1, max(nx1, nx2), y2]
    return s


def apply_theme(spec, theme):
    t = THEMES[theme]
    for l in spec.get("layers", []):
        if l.get("type") == "text":
            l["color"] = t["color"]
            l["stroke"] = {"color": t["stroke"], "width": (l.get("stroke") or {}).get("width", 9)}
            if l.get("highlight"):
                l["highlight"]["color"] = t["highlight"]
    return spec


def sheet(paths, out, labels=None, cols=3, cell_w=420):
    ims = [Image.open(p).convert("RGB") for p in paths]
    if not ims:
        raise Fail("No images for the sheet.")
    cell_h = round(cell_w * ims[0].height / ims[0].width)
    rows = math.ceil(len(ims) / cols)
    pad, lab = 14, 26
    sh = Image.new("RGB", (cols * (cell_w + pad) + pad, rows * (cell_h + lab + pad) + pad), (24, 24, 28))
    d = ImageDraw.Draw(sh)
    f = load_font(find_font(None), 16)
    for i, im in enumerate(ims):
        x = pad + (i % cols) * (cell_w + pad)
        y = pad + (i // cols) * (cell_h + lab + pad)
        sh.paste(im.resize((cell_w, cell_h), Image.LANCZOS), (x, y + lab))
        d.text((x, y + 3), (labels[i] if labels else Path(paths[i]).stem)[:60], fill=(230, 230, 230), font=f)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    sh.save(out, quality=90)
    return out


def cmd_render(a):
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8-sig"))
    out, meta = render(spec, base=str(Path(a.spec).resolve().parent), out=a.out)
    print(f"Wrote {out} ({meta['size'][0]}x{meta['size'][1]}, {meta['bytes'] / 1024:.0f} KB)")
    for n in meta["notes"]:
        print(f"[NOTE] {n}")


def cmd_variants(a):
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8-sig"))
    base = str(Path(a.spec).resolve().parent)
    texts = [t.strip() for t in a.texts.split("|") if t.strip()] if a.texts else [None]
    themes = [t for t in a.themes.split(",") if t] if a.themes else [None]
    bad = [t for t in themes if t and t not in THEMES]
    if bad:
        raise Fail(f"Unknown theme(s) {bad}; choose from {', '.join(THEMES)}.")
    flips = [False, True] if a.flip else [False]
    outdir = Path(a.outdir) if a.outdir else Path(base) / "out" / "variants"
    outdir.mkdir(parents=True, exist_ok=True)
    # texts vary fastest, so when --max cuts the list every text still appears at least once
    allc = [(t, th, fl) for th in themes for fl in flips for t in texts]
    combos = allc[:a.max]
    if len(allc) > len(combos):
        left = sorted({str(t) for t, _, _ in allc} - {str(t) for t, _, _ in combos})
        print(f"[NOTE] {len(allc)} combinations, --max {a.max} keeps {len(combos)}; "
              + (f"texts not rendered: {', '.join(left)}. " if left else "every text is included. ")
              + "Raise --max to render the rest.")
    files, labels = [], []
    for i, (t, th, fl) in enumerate(combos, 1):
        s = flip_spec(spec) if fl else json.loads(json.dumps(spec))
        if th:
            apply_theme(s, th)
        if t:
            first = next((l for l in s.get("layers", []) if l.get("type") == "text"), None)
            if first:
                first["text"] = t
        out, meta = render(s, base=base, out=outdir / f"v{i}.jpg")
        files.append(out)
        labels.append(f"v{i} {t or ''} {th or ''}{' flip' if fl else ''}".strip())
        for n in meta["notes"]:
            print(f"[v{i}] {n}")
    sh = sheet(files, outdir / "sheet.jpg", labels)
    print(f"Wrote {len(files)} variants and {sh}")


def cmd_resize(a):
    w, h = parse_size(a.to)
    fx, fy = (float(x) for x in a.focus.split(","))
    im = ImageOps.exif_transpose(Image.open(a.image)).convert("RGB")
    out = Path(a.out) if a.out else Path(a.image).with_name(f"{Path(a.image).stem}_{w}x{h}.jpg")
    cover(im, w, h, (fx, fy)).save(out, quality=92, optimize=True)
    print(f"Wrote {out} ({w}x{h}). Cropping loses edges; check the text and subject are still inside.")


def cmd_sheet(a):
    print(f"Wrote {sheet(a.images, a.out)}")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("render")
    r.add_argument("spec")
    r.add_argument("--out")
    r.set_defaults(fn=cmd_render)
    v = sub.add_parser("variants")
    v.add_argument("spec")
    v.add_argument("--texts")
    v.add_argument("--themes")
    v.add_argument("--flip", action="store_true")
    v.add_argument("--max", type=int, default=6)
    v.add_argument("--outdir")
    v.set_defaults(fn=cmd_variants)
    z = sub.add_parser("resize")
    z.add_argument("image")
    z.add_argument("--to", required=True)
    z.add_argument("--focus", default="0.5,0.5")
    z.add_argument("--out")
    z.set_defaults(fn=cmd_resize)
    s = sub.add_parser("sheet")
    s.add_argument("images", nargs="+")
    s.add_argument("--out", required=True)
    s.set_defaults(fn=cmd_sheet)
    a = p.parse_args(argv)
    try:
        a.fn(a)
        return 0
    except Fail as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError) as e:
        print(f"error: {type(e).__name__}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
