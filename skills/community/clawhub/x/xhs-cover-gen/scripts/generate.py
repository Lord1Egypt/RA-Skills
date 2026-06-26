#!/usr/bin/env python3
"""
xhs-cover: Generate Xiaohongshu (小红书) cover images.

Usage:
    python3 scripts/generate.py --title "主标题" --subtitle "副标题" \
        --style split --left-label "左标签" --right-label "右标签" \
        --output cover.jpg

Styles:
    split    - Left/right comparison (e.g. PUA vs 暖心)
    gradient - Single gradient background with centered text
    card     - White card on colored background
"""
import argparse, os, sys, subprocess, tempfile, hashlib
from pathlib import Path

# --- font management ---
FONT_URL = "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Bold.otf"
FONT_CACHE = Path(tempfile.gettempdir()) / "NotoSansCJKsc-Bold.otf"
FONT_SHA256 = None  # skip hash check for now

def ensure_font():
    if FONT_CACHE.exists() and FONT_CACHE.stat().st_size > 1_000_000:
        return str(FONT_CACHE)
    print(f"Downloading CJK font to {FONT_CACHE} ...")
    subprocess.run(["curl", "-sL", FONT_URL, "-o", str(FONT_CACHE), "--max-time", "120"], check=True)
    return str(FONT_CACHE)

# --- image generation ---
def generate_base_image(prompt, width=1080, height=1440):
    """Generate base image via Pollinations.ai"""
    import urllib.parse
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width={width}&height={height}&model=flux&nologo=true"
    tmp = Path(tempfile.gettempdir()) / f"xhs_base_{hashlib.md5(prompt.encode()).hexdigest()}.jpg"
    subprocess.run(["curl", "-sL", url, "-o", str(tmp), "--max-time", "180"], check=True)
    return str(tmp)

def make_split_cover(args):
    from PIL import Image, ImageDraw, ImageFont
    font_path = ensure_font()

    if args.base_prompt:
        base_path = generate_base_image(args.base_prompt, args.width, args.height)
        base = Image.open(base_path).convert("RGBA")
    else:
        # Create a simple split background
        base = Image.new("RGBA", (args.width, args.height))
        draw_bg = ImageDraw.Draw(base)
        mid = args.width // 2
        # Left half - soft red/pink
        for y in range(args.height):
            r = int(255 - (y / args.height) * 30)
            draw_bg.line([(0, y), (mid, y)], fill=(r, 100, 120, 255))
        # Right half - soft green/mint
        for y in range(args.height):
            g = int(220 - (y / args.height) * 30)
            draw_bg.line([(mid, y), (args.width, y)], fill=(80, g, 130, 255))

    w, h = base.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    f_label = ImageFont.truetype(font_path, 52)
    f_title = ImageFont.truetype(font_path, 44)
    f_sub = ImageFont.truetype(font_path, 30)
    f_vs = ImageFont.truetype(font_path, 48)

    # Left label
    if args.left_label:
        lx = w // 4
        bbox = f_label.getbbox(args.left_label)
        pw = (bbox[2] - bbox[0]) // 2 + 30
        draw.rounded_rectangle([lx - pw, 50, lx + pw, 120], radius=20,
                               fill=tuple(args.left_color + [220]))
        draw.text((lx, 85), args.left_label, fill="white", font=f_label, anchor="mm")

    # Right label
    if args.right_label:
        rx = 3 * w // 4
        bbox = f_label.getbbox(args.right_label)
        pw = (bbox[2] - bbox[0]) // 2 + 30
        draw.rounded_rectangle([rx - pw, 50, rx + pw, 120], radius=20,
                               fill=tuple(args.right_color + [220]))
        draw.text((rx, 85), args.right_label, fill="white", font=f_label, anchor="mm")

    # VS circle
    cx, cy = w // 2, h // 2 - 80
    draw.ellipse([cx - 55, cy - 55, cx + 55, cy + 55],
                 fill=(255, 150, 0, 240), outline="white", width=5)
    draw.text((cx, cy), "VS", fill="white", font=f_vs, anchor="mm")

    # Bottom bar
    draw.rectangle([0, h - 240, w, h], fill=(0, 0, 0, 185))
    draw.text((w // 2, h - 180), args.title, fill="white", font=f_title, anchor="mm")
    if args.subtitle:
        draw.text((w // 2, h - 120), args.subtitle, fill="white", font=f_title, anchor="mm")
    if args.tagline:
        draw.text((w // 2, h - 60), args.tagline, fill=(255, 255, 200, 255), font=f_sub, anchor="mm")

    result = Image.alpha_composite(base, overlay).convert("RGB")
    result.save(args.output, quality=95)
    print(f"Saved: {args.output} ({os.path.getsize(args.output)} bytes)")


def make_gradient_cover(args):
    from PIL import Image, ImageDraw, ImageFont
    font_path = ensure_font()

    if args.base_prompt:
        base_path = generate_base_image(args.base_prompt, args.width, args.height)
        base = Image.open(base_path).convert("RGBA")
    else:
        base = Image.new("RGBA", (args.width, args.height), tuple(args.left_color + [255]))

    w, h = base.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    f_title = ImageFont.truetype(font_path, 56)
    f_sub = ImageFont.truetype(font_path, 34)

    # Dark overlay bottom half
    draw.rectangle([0, h // 2, w, h], fill=(0, 0, 0, 150))

    draw.text((w // 2, h * 2 // 3), args.title, fill="white", font=f_title, anchor="mm")
    if args.subtitle:
        draw.text((w // 2, h * 2 // 3 + 70), args.subtitle, fill=(255, 255, 200, 255),
                   font=f_sub, anchor="mm")

    result = Image.alpha_composite(base, overlay).convert("RGB")
    result.save(args.output, quality=95)
    print(f"Saved: {args.output} ({os.path.getsize(args.output)} bytes)")


def make_card_cover(args):
    from PIL import Image, ImageDraw, ImageFont
    font_path = ensure_font()

    if args.base_prompt:
        base_path = generate_base_image(args.base_prompt, args.width, args.height)
        base = Image.open(base_path).convert("RGBA")
    else:
        base = Image.new("RGBA", (args.width, args.height), tuple(args.left_color + [255]))

    w, h = base.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # White card
    margin = 60
    card_top = h // 3
    draw.rounded_rectangle([margin, card_top, w - margin, h - margin],
                           radius=30, fill=(255, 255, 255, 240))

    f_title = ImageFont.truetype(font_path, 48)
    f_sub = ImageFont.truetype(font_path, 32)

    draw.text((w // 2, card_top + 120), args.title, fill=(30, 30, 30, 255),
              font=f_title, anchor="mm")
    if args.subtitle:
        draw.text((w // 2, card_top + 200), args.subtitle, fill=(100, 100, 100, 255),
                   font=f_sub, anchor="mm")

    result = Image.alpha_composite(base, overlay).convert("RGB")
    result.save(args.output, quality=95)
    print(f"Saved: {args.output} ({os.path.getsize(args.output)} bytes)")


def parse_color(s):
    """Parse 'R,G,B' string to [R, G, B] list"""
    return [int(x.strip()) for x in s.split(",")]


def main():
    p = argparse.ArgumentParser(description="Generate Xiaohongshu cover images")
    p.add_argument("--title", required=True, help="Main title text")
    p.add_argument("--subtitle", default="", help="Subtitle text")
    p.add_argument("--tagline", default="", help="Bottom tagline")
    p.add_argument("--style", choices=["split", "gradient", "card"], default="gradient")
    p.add_argument("--left-label", default="")
    p.add_argument("--right-label", default="")
    p.add_argument("--left-color", default="255,60,70", help="R,G,B")
    p.add_argument("--right-color", default="30,190,100", help="R,G,B")
    p.add_argument("--base-prompt", default="", help="Pollinations.ai prompt for base image")
    p.add_argument("--width", type=int, default=1080)
    p.add_argument("--height", type=int, default=1440)
    p.add_argument("--output", default="cover.jpg")

    args = p.parse_args()
    args.left_color = parse_color(args.left_color)
    args.right_color = parse_color(args.right_color)

    if args.style == "split":
        make_split_cover(args)
    elif args.style == "gradient":
        make_gradient_cover(args)
    elif args.style == "card":
        make_card_cover(args)


if __name__ == "__main__":
    main()
