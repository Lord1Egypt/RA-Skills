#!/usr/bin/env python3
"""Render TikTok photo-mode slideshows (and Instagram carousel copies) from a JSON spec.

Free and local: needs only Python 3.8+ and Pillow (`pip install pillow`).

Usage:
    python3 scripts/render_slides.py slides.json --out slideshow/
    python3 scripts/render_slides.py slides.json --out slideshow/ --font /path/to/Bold.ttf --no-instagram

Spec (slides.json):
{
  "theme": {"bg": "#101014", "fg": "#ffffff", "accent": "#ffd23f", "style": "auto", "font": null},
  "slides": [
    {"text": "I tried 4 habit apps for 30 days", "subtext": "only one stayed"},
    {"text": "The one I kept", "image": "screens/today.png", "layout": "screenshot"},
    {"text": "POV: your Sunday finally plans itself", "image": "photos/desk.jpg", "position": "top"}
  ]
}

Per slide:
  text      required, the slide's one text block (1 to 3 short lines, use \n to break)
  subtext   optional and rarely used: a second, smaller block. One block per slide reads best.
  image     optional path (relative to the spec file) to a photo or screenshot
  layout    "background" (default when there is an image: photo fills the slide, text on top)
            "fullscreen" (a real app screenshot as large as the slide allows, on the app's own
                          background color, with the text above it: the best way to show the app)
            "screenshot" (text at the top, the whole screenshot below it as a rounded card)
  backdrop  optional photo for the screenshot layout, shown blurred behind the card
  position  upper (default, the top third) | top | center | bottom
  style     classic | highlight | plain, best set once in "theme" for the whole slideshow.
            These match TikTok's own text tool:
            "classic"   = white TikTok Sans with a thin dark outline (default on photos)
            "highlight" = text on strips, one strip per line. "strip": "white" | "black" | "auto"
                          (in the theme) sets the strip color; auto picks by background
            "plain"     = text straight on a solid color (default without a photo)
  bg, fg, accent   per-slide colors (hex), overriding the theme. accent colors the subtext.

The bundled font is TikTok Sans (fonts/TikTokSans.ttf, SIL Open Font License), the font
TikTok uses in its own app.

Optional: with OpenCV installed (`pip install opencv-python-headless`) the renderer warns when
text covers a face. Without it, check every slide at full size.

Output:
    <out>/tiktok/slide-01.jpg ...     1080x1920 JPEG, text kept inside TikTok's safe zone
    <out>/instagram/slide-01.jpg ...  1080x1350 JPEG (4:5) copies for an Instagram carousel
    <out>/contact-sheet.png           all TikTok slides side by side, for review
    <out>/contact-sheet-instagram.png all Instagram slides side by side, for review
    <out>/manifest.json               file paths and byte sizes (needed for upload sessions)
"""
import argparse
import json
import os
import re
import sys

try:
    from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
except ImportError:
    sys.exit("Pillow is missing. Install it with: pip install pillow")

SIZES = {
    "tiktok": (1080, 1920),
    "instagram": (1080, 1350),
}

# Space kept free of text, in pixels. TikTok draws the profile and search bar at the top, the
# like/comment/share column on the right and the caption at the bottom. Left and right are
# equal so text stays centred on the frame.
SAFE = {
    "tiktok": {"top": 230, "bottom": 510, "left": 130, "right": 130},
    "instagram": {"top": 110, "bottom": 140, "left": 90, "right": 90},
}

MIN_MAIN, MIN_SUB = 56, 44

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLED_FONT = os.path.join(HERE, "..", "fonts", "TikTokSans.ttf")

FONT_CANDIDATES = [
    # macOS
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    # Linux
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/liberation-sans/LiberationSans-Bold.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    # Windows
    "C:\\Windows\\Fonts\\arialbd.ttf",
    "C:\\Windows\\Fonts\\segoeuib.ttf",
]

HEX = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def warn(message):
    print(f"Warning: {message}", file=sys.stderr)


FONT_URL = ("https://raw.githubusercontent.com/google/fonts/main/ofl/tiktoksans/"
            "TikTokSans%5Bopsz%2Cslnt%2Cwdth%2Cwght%5D.ttf")


def fetch_bundled_font():
    """Some skill registries ship text files only. Fetch TikTok Sans (SIL OFL) once if missing."""
    import subprocess
    import urllib.request
    os.makedirs(os.path.dirname(BUNDLED_FONT), exist_ok=True)
    try:
        with urllib.request.urlopen(FONT_URL, timeout=30) as response:
            data = response.read()
        with open(BUNDLED_FONT, "wb") as f:
            f.write(data)
    except Exception:
        # Python builds without system certificates (common on macOS): use curl instead.
        try:
            subprocess.run(["curl", "-fsSL", "-o", BUNDLED_FONT, FONT_URL], check=True, timeout=60)
        except Exception:
            return False
    if not os.path.exists(BUNDLED_FONT) or os.path.getsize(BUNDLED_FONT) < 100000:
        if os.path.exists(BUNDLED_FONT):
            os.remove(BUNDLED_FONT)
        return False
    print("Downloaded TikTok Sans into fonts/ (SIL Open Font License).", file=sys.stderr)
    return True


def find_font(explicit):
    if explicit:
        if not os.path.exists(explicit):
            sys.exit(f"Font not found: {explicit}")
        return explicit
    if os.path.exists(BUNDLED_FONT) or fetch_bundled_font():
        return BUNDLED_FONT
    warn("TikTok Sans is missing and couldn't be downloaded; using a system font. "
         "Slides look more native with it: see fonts/ in the GitHub repo.")
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return path
    return None


def load_font(path, size, weight="Bold"):
    if path:
        font = ImageFont.truetype(path, size)
        try:
            font.set_variation_by_name(weight)  # variable fonts such as TikTok Sans
        except Exception:
            pass
        return font
    try:
        font = ImageFont.load_default(size=size)  # Pillow 10.1+ with FreeType
    except TypeError:
        font = None
    if font is None or not hasattr(font, "size"):
        sys.exit("No bold font found on this system. Pass one with --font /path/to/font.ttf")
    return font


def color(value, fallback, where):
    value = value or fallback
    if not isinstance(value, str) or not HEX.match(value):
        sys.exit(f"{where}: '{value}' is not a hex color like #ffd23f")
    value = value.lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def split_long_word(draw, word, font, max_width):
    """Break a word that is wider than the line into pieces that fit."""
    pieces, piece = [], ""
    for ch in word:
        if piece and draw.textlength(piece + ch, font=font) > max_width:
            pieces.append(piece)
            piece = ch
        else:
            piece += ch
    pieces.append(piece)
    return pieces


def wrap(draw, text, font, max_width):
    lines = []
    for paragraph in text.split("\n"):
        words = []
        for word in paragraph.split():
            if draw.textlength(word, font=font) > max_width:
                words.extend(split_long_word(draw, word, font, max_width))
            else:
                words.append(word)
        if not words:
            lines.append("")
            continue
        para, line = [], words[0]
        for word in words[1:]:
            trial = f"{line} {word}"
            if draw.textlength(trial, font=font) <= max_width:
                line = trial
            else:
                para.append(line)
                line = word
        # Avoid a single word alone on the last line of a paragraph.
        if para and " " not in line:
            prev = para[-1].split()
            if len(prev) > 2:
                moved = f"{prev[-1]} {line}"
                if draw.textlength(moved, font=font) <= max_width:
                    para[-1] = " ".join(prev[:-1])
                    line = moved
        para.append(line)
        lines.extend(para)
    return lines


def measure(draw, lines, font, spacing):
    line_h = font.getbbox("Ag")[3] - font.getbbox("Ag")[1]
    height = len(lines) * line_h + max(0, len(lines) - 1) * int(line_h * spacing)
    widest = max((draw.textlength(l, font=font) for l in lines), default=0)
    return line_h, height, widest


def fit_text(draw, text, font_path, max_width, max_height, start, minimum, spacing, label,
             weight="Bold"):
    size = start
    while size >= minimum:
        font = load_font(font_path, size, weight)
        lines = wrap(draw, text, font, max_width)
        line_h, height, widest = measure(draw, lines, font, spacing)
        if height <= max_height and widest <= max_width:
            return font, lines, line_h, height
        size -= 4
    font = load_font(font_path, minimum, weight)
    lines = wrap(draw, text, font, max_width)
    line_h, height, _ = measure(draw, lines, font, spacing)
    warn(f"{label} is too long to fit at a readable size. Shorten it.")
    return font, lines, line_h, height


def open_image(slide, base_dir):
    path = slide.get("image")
    if not path:
        return None
    full = path if os.path.isabs(path) else os.path.join(base_dir, path)
    if not os.path.exists(full):
        sys.exit(f"Image not found: {full}")
    return ImageOps.exif_transpose(Image.open(full)).convert("RGB")


try:
    import cv2  # optional: enables the face check
    import numpy as np
    _FACES = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
except Exception:  # OpenCV not installed: the agent checks faces by eye instead
    _FACES = None


def faces_in(img):
    if _FACES is None:
        return []
    gray = cv2.cvtColor(np.array(img.convert("RGB")), cv2.COLOR_RGB2GRAY)
    found = _FACES.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6,
                                    minSize=(img.width // 10, img.width // 10))
    return [(x, y, x + w, y + h) for (x, y, w, h) in found]


def check_faces(img, text_box, label):
    for fx0, fy0, fx1, fy1 in faces_in(img):
        if not (text_box[2] < fx0 or text_box[0] > fx1 or text_box[3] < fy0 or text_box[1] > fy1):
            warn(f"{label}: the text covers a face. Move it with \"position\" "
                 "(top, upper, center, bottom) or pick another photo.")
            return


def line_box(font):
    ascent, descent = font.getmetrics()
    return ascent + descent


def layout_text(draw, slide, fmt, font_path, style, area, label):
    """Fit the slide's text (and optional subtext) into area = (left, top, width, height)."""
    left, top, width, height = area
    pad_x = 30 if style == "highlight" else 0
    main_start = 84 if fmt == "tiktok" else 80
    font, lines, _, _ = fit_text(
        draw, slide["text"].strip(), font_path, width - 2 * pad_x, int(height * 0.7),
        main_start, MIN_MAIN, 0.2, f"{label} text", "SemiBold" if style == "highlight" else "Bold")
    if font.size < 68:
        warn(f"{label} text had to shrink to {font.size}px. Fewer words read better.")
    sub_text = (slide.get("subtext") or "").strip()
    sub = None
    if sub_text:
        sub_font, sub_lines, _, _ = fit_text(
            draw, sub_text, font_path, width - 2 * pad_x, int(height * 0.26),
            max(MIN_SUB, int(font.size * 0.7)), MIN_SUB, 0.2, f"{label} subtext", "SemiBold")
        sub = (sub_font, sub_lines)
    block_h = text_height(lines, font, style)
    if sub:
        block_h += int(font.size * 0.5) + text_height(sub[1], sub[0], style)
    return {"font": font, "lines": lines, "sub": sub, "block_h": block_h}


def text_height(lines, font, style):
    step = line_box(font) + (int(font.size * 0.12) if style == "highlight" else int(font.size * 0.08))
    return len(lines) * step


def place_lines(lines, font, center_x, y, style):
    """Return (line, x, y) positions, one per line."""
    step = line_box(font) + (int(font.size * 0.12) if style == "highlight" else int(font.size * 0.08))
    out = []
    for line in lines:
        out.append((line, center_x, y))
        y += step
    return out, y


def draw_text(img, block, center_x, top, style, fg, accent, strip_color="auto"):
    draw = ImageDraw.Draw(img, "RGBA")
    groups = []
    placed, y = place_lines(block["lines"], block["font"], center_x, top, style)
    groups.append((block["font"], placed, fg))
    if block["sub"]:
        sub_font, sub_lines = block["sub"]
        placed, _ = place_lines(sub_lines, sub_font, center_x, y + int(block["font"].size * 0.5), style)
        groups.append((sub_font, placed, accent if style != "highlight" else (18, 18, 18)))

    if style == "highlight":
        # Pass 1: one strip per line, tall enough that neighbours touch and merge into one
        # shape, like TikTok's own background text. Pass 2: the text on top. On a bright
        # background the strips turn black with white text, as TikTok's text tool offers.
        first = groups[0][1]
        y0, y1 = first[0][2], groups[-1][1][-1][2] + line_box(groups[-1][0])
        region = img.crop((max(0, center_x - 300), max(0, y0), min(img.width, center_x + 300),
                           min(img.height, y1))).convert("L")
        hist = region.histogram()
        bright = sum(i * n for i, n in enumerate(hist)) / max(1, sum(hist)) > 185
        dark = {"black": True, "white": False}.get(strip_color, bright)
        strip, ink = ((18, 18, 18, 255), (255, 255, 255)) if dark else ((255, 255, 255, 255), (18, 18, 18))
        for font, placed, _ in groups:
            pad_x, pad_y = int(font.size * 0.3), int(font.size * 0.1)
            radius = int(font.size * 0.24)
            rects = []
            for line, x, ly in placed:
                w = draw.textlength(line, font=font)
                rects.append([x - w / 2 - pad_x, ly - pad_y, x + w / 2 + pad_x,
                              ly + line_box(font) + int(font.size * 0.12) + pad_y])
            for r in rects:
                draw.rounded_rectangle(r, radius=radius, fill=strip)
            # Fill the seam between neighbouring lines so the strips read as one shape.
            for a, b in zip(rects, rects[1:]):
                left, right = max(a[0], b[0]), min(a[2], b[2])
                draw.rectangle([left, a[3] - radius, right, b[1] + radius], fill=strip)
        for font, placed, _ in groups:
            for line, x, ly in placed:
                draw.text((x, ly), line, font=font, fill=ink, anchor="ma")
        return

    if style == "classic":
        # Soft shadow under white text, then the text with a thin outline.
        shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        for font, placed, _ in groups:
            for line, x, ly in placed:
                sd.text((x, ly + 4), line, font=font, fill=(0, 0, 0, 170), anchor="ma",
                        stroke_width=max(3, font.size // 16), stroke_fill=(0, 0, 0, 170))
        shadow = shadow.filter(ImageFilter.GaussianBlur(10))
        img.paste(shadow, (0, 0), shadow)
        draw = ImageDraw.Draw(img, "RGBA")
    for font, placed, color_ in groups:
        stroke = max(2, int(font.size * 0.035)) if style == "classic" else 0
        for line, x, ly in placed:
            draw.text((x, ly), line, font=font, fill=color_, anchor="ma",
                      stroke_width=stroke, stroke_fill=(0, 0, 0))


def rounded_card(image, radius):
    mask = Image.new("L", image.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, image.width - 1, image.height - 1],
                                           radius=radius, fill=255)
    return mask


def render_slide(slide, theme, fmt, font_path, base_dir, label):
    w, h = SIZES[fmt]
    safe = SAFE[fmt]
    bg = color(slide.get("bg") or theme.get("bg"), "#101014", f"{label} bg")
    fg = color(slide.get("fg") or theme.get("fg"), "#ffffff", f"{label} fg")
    accent = color(slide.get("accent") or theme.get("accent"), "#ffffff", f"{label} accent")
    image = open_image(slide, base_dir)
    layout = slide.get("layout") or ("background" if image else "none")
    if layout not in ("background", "fullscreen", "screenshot", "none"):
        sys.exit(f"{label}: layout must be background, fullscreen or screenshot")
    style = slide.get("style") or theme.get("style") or "auto"
    style = {"outline": "classic", "box": "highlight"}.get(style, style)
    if style == "auto":
        style = "plain" if layout == "none" and not slide.get("backdrop") else "classic"
    if style not in ("classic", "highlight", "plain"):
        sys.exit(f"{label}: style must be classic, highlight or plain")
    strip_color = slide.get("strip") or theme.get("strip") or "auto"
    if strip_color not in ("auto", "white", "black"):
        sys.exit(f"{label}: strip must be white, black or auto")

    if layout == "background":
        img = ImageOps.fit(image, (w, h), method=Image.LANCZOS)
        if style == "classic":
            img = ImageEnhance.Brightness(img).enhance(0.9)
    elif layout == "fullscreen":
        # The app's own background color fills the frame, so the screenshot reads as one screen.
        img = Image.new("RGB", (w, h), image.getpixel((8, image.height // 3)))
    elif slide.get("backdrop"):
        back = open_image({"image": slide["backdrop"]}, base_dir)
        img = ImageOps.fit(back, (w, h), method=Image.LANCZOS).filter(ImageFilter.GaussianBlur(28))
        img = ImageEnhance.Brightness(img).enhance(0.7)
    else:
        img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img, "RGBA")
    width = w - safe["left"] - safe["right"]
    area_h = h - safe["top"] - safe["bottom"]
    center_x = safe["left"] + width // 2

    if layout == "fullscreen":
        block = layout_text(draw, slide, fmt, font_path, style,
                            (safe["left"], safe["top"], width, int(area_h * 0.3)), label)
        top = safe["top"] - (60 if fmt == "tiktok" else 0)
        img_top = top + block["block_h"] + 50
        shot = ImageOps.contain(image, (w, h - img_top), method=Image.LANCZOS)
        img.paste(shot, ((w - shot.width) // 2, img_top))
        draw_text(img, block, center_x, top, style, fg, accent, strip_color)
        return img

    if layout == "screenshot":
        block = layout_text(draw, slide, fmt, font_path, style,
                            (safe["left"], safe["top"], width, int(area_h * 0.34)), label)
        top = safe["top"]
        draw_text(img, block, center_x, top, style, fg, accent, strip_color)
        img_top = top + block["block_h"] + 60
        img_bottom = h - (200 if fmt == "tiktok" else 70)
        shot = ImageOps.contain(image, (int(w * 0.72), img_bottom - img_top), method=Image.LANCZOS)
        radius = int(shot.width * 0.07)
        img.paste(shot, (center_x - shot.width // 2, img_top), rounded_card(shot, radius))
        return img

    block = layout_text(draw, slide, fmt, font_path, style,
                        (safe["left"], safe["top"], width, area_h), label)
    position = slide.get("position", "upper")
    if position == "top":
        top = safe["top"]
    elif position == "bottom":
        top = h - safe["bottom"] - block["block_h"]
    elif position == "center":
        top = safe["top"] + (area_h - block["block_h"]) // 2
    else:  # upper third, where TikTok text usually sits
        top = safe["top"] + int((area_h - block["block_h"]) * 0.3)
    if layout == "background":
        check_faces(img, (safe["left"], top - 20, w - safe["right"], top + block["block_h"] + 20), label)
    draw_text(img, block, center_x, top, style, fg, accent, strip_color)
    return img


def contact_sheet(paths, out_path, thumb):
    thumbs = [Image.open(p).resize(thumb, Image.LANCZOS) for p in paths]
    gap = 16
    sheet = Image.new("RGB", (len(thumbs) * (thumb[0] + gap) + gap, thumb[1] + 2 * gap),
                      (235, 235, 235))
    for i, t in enumerate(thumbs):
        sheet.paste(t, (gap + i * (thumb[0] + gap), gap))
    sheet.save(out_path)


def main():
    parser = argparse.ArgumentParser(description="Render TikTok slideshow slides from a JSON spec.")
    parser.add_argument("spec", help="path to slides.json")
    parser.add_argument("--out", default="slideshow", help="output folder")
    parser.add_argument("--font", help="path to a bold .ttf/.otf font")
    parser.add_argument("--no-instagram", action="store_true", help="skip the 4:5 Instagram copies")
    args = parser.parse_args()

    with open(args.spec, encoding="utf-8") as f:
        spec = json.load(f)
    slides = spec.get("slides") or []
    if not slides:
        sys.exit("The spec has no slides.")
    for i, slide in enumerate(slides, start=1):
        if not isinstance(slide.get("text"), str) or not slide["text"].strip():
            sys.exit(f"Slide {i} needs a 'text' string.")
        if "subtext" in slide and not isinstance(slide["subtext"], str):
            sys.exit(f"Slide {i}: 'subtext' must be a string.")
    if len(slides) > 10:
        warn("more than 10 slides. Instagram carousels take at most 10, and TikTok limits vary. "
             "Run posts_validate before promising it will post.")
    theme = spec.get("theme", {})
    if sum(1 for s in slides if s.get("subtext")) > 1:
        warn("subtext on more than one slide. TikTok slideshows read best with one text block "
             "per slide; merge the lines.")
    styles = {s.get("style") for s in slides if s.get("style")}
    if len(styles) > 1:
        warn(f"mixed text styles {sorted(styles)}. Set one style in the theme for the whole slideshow.")
    font_path = find_font(args.font or theme.get("font"))
    base_dir = os.path.dirname(os.path.abspath(args.spec))

    formats = ["tiktok"] if args.no_instagram else ["tiktok", "instagram"]
    manifest = {"slides": len(slides), "font": font_path or "Pillow default", "files": {}}
    for fmt in formats:
        folder = os.path.join(args.out, fmt)
        os.makedirs(folder, exist_ok=True)
        manifest["files"][fmt] = []
        for i, slide in enumerate(slides, start=1):
            label = f"Slide {i} ({fmt})"
            img = render_slide(slide, theme, fmt, font_path, base_dir, label)
            path = os.path.join(folder, f"slide-{i:02d}.jpg")
            img.save(path, "JPEG", quality=92, optimize=True)
            manifest["files"][fmt].append({"path": path, "bytes": os.path.getsize(path)})

    sheet = os.path.join(args.out, "contact-sheet.png")
    contact_sheet([f["path"] for f in manifest["files"]["tiktok"]], sheet, (270, 480))
    manifest["contactSheet"] = sheet
    if "instagram" in manifest["files"]:
        ig_sheet = os.path.join(args.out, "contact-sheet-instagram.png")
        contact_sheet([f["path"] for f in manifest["files"]["instagram"]], ig_sheet, (320, 400))
        manifest["contactSheetInstagram"] = ig_sheet
    with open(os.path.join(args.out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
