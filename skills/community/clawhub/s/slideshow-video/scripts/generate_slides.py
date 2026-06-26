#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
import os
import urllib.parse
import urllib.request
from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

CANVAS_W = 1080
CANVAS_H = 1920
DEFAULT_MARGIN = 84
DEFAULT_OVERLAY = 112


def load_font(size: int, bold: bool = False, font_path: str | None = None):
    candidates = []
    if font_path:
        candidates.append(font_path)
    candidates.extend([
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
    ])
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            try:
                return ImageFont.truetype(candidate, size=size)
            except Exception:
                pass
    return ImageFont.load_default()


def fit_cover(img: Image.Image, size: Tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    scale = max(target_w / img.width, target_h / img.height)
    resized = img.resize((math.ceil(img.width * scale), math.ceil(img.height * scale)), Image.LANCZOS)
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
    words = text.split()
    if not words:
        return [""]
    lines = []
    current = words[0]
    for word in words[1:]:
        test = f"{current} {word}"
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def draw_text_block(draw, block, canvas_w):
    text = block["text"]
    size = int(block.get("size", 72))
    bold = bool(block.get("bold", False) or str(block.get("weight", "")).lower() == "bold")
    font_path = block.get("fontPath")
    font = load_font(size, bold=bold, font_path=font_path)
    color = block.get("color", "#ffffff")
    align = block.get("align", "center")
    x = int(block.get("x", canvas_w // 2))
    y = int(block.get("y", 960))
    max_width = int(block.get("maxWidth", canvas_w - DEFAULT_MARGIN * 2))
    line_spacing = float(block.get("lineSpacing", 1.2))
    shadow = block.get("shadow", True)
    stroke_width = int(block.get("strokeWidth", 0))
    stroke_fill = block.get("strokeFill", "#000000")

    lines = wrap_text(draw, text, font, max_width)
    line_height = int(size * line_spacing)
    total_height = line_height * max(len(lines) - 1, 0)
    start_y = y - total_height // 2

    for i, line in enumerate(lines):
        yy = start_y + i * line_height
        anchor = {"center": "mm", "left": "lm", "right": "rm"}.get(align, "mm")
        if shadow:
            draw.text((x + 3, yy + 4), line, font=font, fill=(0, 0, 0, 180), anchor=anchor)
        draw.text((x, yy), line, font=font, fill=color, anchor=anchor, stroke_width=stroke_width, stroke_fill=stroke_fill)


def looks_like_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def cache_remote_image(url: str, cache_dir: Path) -> Path:
    parsed = urllib.parse.urlparse(url)
    suffix = Path(parsed.path).suffix or ".img"
    name = hashlib.sha256(url.encode("utf-8")).hexdigest()[:24] + suffix
    out = cache_dir / name
    if out.exists() and out.stat().st_size > 0:
        return out
    cache_dir.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw slideshow-video skill"})
    with urllib.request.urlopen(req, timeout=60) as response, open(out, "wb") as f:
        f.write(response.read())
    return out


def resolve_image_path(slide: dict, cache_dir: Path) -> Path:
    image_url = slide.get("imageUrl")
    image_path_value = slide.get("imagePath")

    if image_url:
        return cache_remote_image(image_url, cache_dir)

    if not image_path_value:
        raise ValueError("Each slide needs imagePath or imageUrl")

    if looks_like_url(str(image_path_value)):
        return cache_remote_image(str(image_path_value), cache_dir)

    image_path = Path(str(image_path_value)).expanduser()
    if not image_path.is_absolute():
        image_path = (Path.cwd() / image_path).resolve()
    return image_path


def render_slide(slide: dict, output_path: Path, cache_dir: Path):
    image_path = resolve_image_path(slide, cache_dir)
    img = Image.open(image_path).convert("RGB")
    img = fit_cover(img, (CANVAS_W, CANVAS_H))

    if slide.get("blur"):
        img = img.filter(ImageFilter.GaussianBlur(radius=float(slide["blur"])))
    if slide.get("brightness"):
        img = ImageEnhance.Brightness(img).enhance(float(slide["brightness"]))

    overlay = int(slide.get("overlay", DEFAULT_OVERLAY))
    base = img.convert("RGBA")
    dark = Image.new("RGBA", base.size, (0, 0, 0, overlay))
    composed = Image.alpha_composite(base, dark)

    draw = ImageDraw.Draw(composed)
    for block in slide.get("text", []):
        draw_text_block(draw, block, CANVAS_W)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    composed.convert("RGB").save(output_path, "PNG")


def main():
    parser = argparse.ArgumentParser(description="Generate 9:16 slideshow PNGs from a JSON config.")
    parser.add_argument("config", help="Path to slideshow JSON config")
    parser.add_argument("--output-dir", default="output", help="Directory for generated PNG slides")
    parser.add_argument("--prefix", default="slide_", help="Output filename prefix")
    parser.add_argument("--cache-dir", default=".slideshow-cache", help="Directory for cached remote images")
    args = parser.parse_args()

    config_path = Path(args.config).expanduser().resolve()
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    slides = data["slides"] if isinstance(data, dict) and "slides" in data else data
    output_dir = Path(args.output_dir).expanduser().resolve()
    cache_dir = Path(args.cache_dir).expanduser().resolve()

    for idx, slide in enumerate(slides, start=1):
        filename = slide.get("output") or f"{args.prefix}{idx:02d}.png"
        render_slide(slide, output_dir / filename, cache_dir)
        print(f"✓ {output_dir / filename}")

    print(f"Done, generated {len(slides)} slides in {output_dir}")


if __name__ == "__main__":
    main()
