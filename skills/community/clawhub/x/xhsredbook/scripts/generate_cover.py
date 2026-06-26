#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cover.py - Generate Xiaohongshu-style cover images (大字报风格)
Features:
- Textured backgrounds (geometric patterns, noise, shapes)
- Bold eye-catching title text with decorative elements
- Multiple layout styles mimicking popular XHS covers
"""

import sys
import os
import random
import math
import platform
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from config import get_subdir

OUTPUT_DIR = get_subdir("generated_images")

# ── 配色方案 ────────────────────────────────────────────────────────────

PALETTES = [
    # 奶油白 + 黑字（极简大字报）
    {"bg": (245, 240, 230), "accent": (255, 90, 95), "text": (30, 30, 30), "sub": (120, 120, 120)},
    # 暖黄 + 棕字
    {"bg": (255, 243, 220), "accent": (255, 140, 50), "text": (80, 50, 20), "sub": (160, 120, 70)},
    # 浅粉 + 深红字
    {"bg": (255, 235, 235), "accent": (255, 80, 100), "text": (180, 40, 60), "sub": (200, 120, 130)},
    # 薄荷绿 + 深绿字
    {"bg": (230, 250, 240), "accent": (60, 200, 140), "text": (30, 80, 60), "sub": (100, 160, 130)},
    # 浅蓝 + 深蓝字
    {"bg": (230, 240, 255), "accent": (80, 130, 255), "text": (30, 50, 100), "sub": (100, 130, 180)},
    # 浅紫 + 紫字
    {"bg": (245, 235, 255), "accent": (160, 100, 240), "text": (80, 40, 130), "sub": (140, 110, 180)},
    # 纯白 + 红色强调
    {"bg": (255, 255, 255), "accent": (255, 60, 60), "text": (20, 20, 20), "sub": (150, 150, 150)},
    # 深色系 - 深灰 + 白字
    {"bg": (45, 45, 55), "accent": (255, 200, 80), "text": (255, 255, 255), "sub": (180, 180, 190)},
    # 深色系 - 墨绿 + 金字
    {"bg": (30, 50, 45), "accent": (220, 180, 100), "text": (240, 235, 220), "sub": (160, 170, 160)},
    # 莫兰迪粉 + 深色字
    {"bg": (225, 200, 195), "accent": (200, 100, 90), "text": (60, 40, 40), "sub": (130, 100, 95)},
]

# ── 字体 ────────────────────────────────────────────────────────────────

def _font_search_paths(bold: bool = True) -> list[str]:
    """Return candidate font paths for the current OS."""
    system = platform.system()
    env_font = os.environ.get("XHS_FONT_PATH")
    if env_font:
        return [env_font]

    if system == "Windows":
        fonts_dir = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
        if bold:
            return [str(fonts_dir / n) for n in ("msyhbd.ttc", "simhei.ttf", "msyh.ttc")]
        return [str(fonts_dir / n) for n in ("msyh.ttc", "simsun.ttc")]

    if system == "Darwin":  # macOS
        candidates = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
        ]
    else:  # Linux / other
        candidates = [
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
            "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc",
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        ]
    return candidates


def load_font(size: int, bold: bool = True):
    for fp in _font_search_paths(bold):
        try:
            return ImageFont.truetype(fp, size)
        except Exception:
            continue
    return ImageFont.load_default()


# ── 背景纹理 ────────────────────────────────────────────────────────────

def bg_noise(img, intensity=15):
    """Add subtle noise texture."""
    w, h = img.size
    pixels = img.load()
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            pixel = pixels[x, y]
            r, g, b = pixel[:3]
            a = pixel[3] if len(pixel) > 3 else 255
            n = random.randint(-intensity, intensity)
            pixels[x, y] = (
                max(0, min(255, r + n)),
                max(0, min(255, g + n)),
                max(0, min(255, b + n)),
                a,
            )


def bg_grid(draw, w, h, color, spacing=80):
    """Draw subtle grid lines."""
    line_color = color + (25,)
    for x in range(0, w, spacing):
        draw.line([(x, 0), (x, h)], fill=line_color, width=1)
    for y in range(0, h, spacing):
        draw.line([(0, y), (w, y)], fill=line_color, width=1)


def bg_dots(draw, w, h, color, spacing=60):
    """Draw dot pattern."""
    dot_color = color + (35,)
    for x in range(spacing//2, w, spacing):
        for y in range(spacing//2, h, spacing):
            r = 3
            draw.ellipse([(x-r, y-r), (x+r, y+r)], fill=dot_color)


def bg_circles(draw, w, h, accent):
    """Draw large decorative circles."""
    for _ in range(random.randint(2, 5)):
        cx = random.randint(-100, w+100)
        cy = random.randint(-100, h+100)
        radius = random.randint(100, 350)
        circle_color = accent + (20,)
        draw.ellipse([(cx-radius, cy-radius), (cx+radius, cy+radius)], fill=circle_color)


def bg_stripes(draw, w, h, color, angle=45):
    """Draw diagonal stripes."""
    stripe_color = color + (18,)
    spacing = 50
    for offset in range(-h, w+h, spacing):
        x1 = offset
        y1 = 0
        x2 = offset - h
        y2 = h
        draw.line([(x1, y1), (x2, y2)], fill=stripe_color, width=2)


def bg_blocks(draw, w, h, accent):
    """Draw random rectangular blocks."""
    for _ in range(random.randint(3, 8)):
        x1 = random.randint(0, w)
        y1 = random.randint(0, h)
        bw = random.randint(40, 200)
        bh = random.randint(40, 200)
        block_color = accent + (15,)
        draw.rectangle([(x1, y1), (x1+bw, y1+bh)], fill=block_color)


# ── 布局样式 ────────────────────────────────────────────────────────────

def layout_centered(draw, w, h, title, palette):
    """经典居中大字报"""
    lines = wrap_text(title, 6)
    font_size = 120 if len(lines) <= 2 else 95 if len(lines) <= 3 else 75
    font = load_font(font_size, bold=True)

    line_h = font_size + 35
    total_h = len(lines) * line_h
    start_y = (h - total_h) // 2

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = (w - tw) // 2
        y = start_y + i * line_h
        # Text shadow
        draw.text((x+3, y+3), line, fill=(0, 0, 0, 40), font=font)
        draw.text((x, y), line, fill=palette["text"], font=font)

    # Accent line under text
    line_y = start_y + total_h + 20
    line_w = min(400, w - 200)
    draw.rectangle(
        [((w - line_w)//2, line_y), ((w + line_w)//2, line_y + 6)],
        fill=palette["accent"]
    )


def layout_top_heavy(draw, w, h, title, palette):
    """标题在上方，下方留白"""
    lines = wrap_text(title, 7)
    font_size = 105 if len(lines) <= 2 else 85
    font = load_font(font_size, bold=True)

    line_h = font_size + 30
    start_y = 180

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = (w - tw) // 2
        y = start_y + i * line_h
        draw.text((x+3, y+3), line, fill=(0, 0, 0, 35), font=font)
        draw.text((x, y), line, fill=palette["text"], font=font)

    # Decorative emoji/icon area at bottom
    sub_font = load_font(32, bold=False)
    sub_text = random.choice([
        "👇 点击查看详情", "✨ 收藏不迷路", "📌 建议收藏",
        "💡 实用干货", "🔥 强烈推荐", "❤️ 喜欢就点赞"
    ])
    bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w-tw)//2, h - 150), sub_text, fill=palette["sub"], font=sub_font)


def layout_left_aligned(draw, w, h, title, palette):
    """左对齐，杂志风"""
    lines = wrap_text(title, 6)
    font_size = 110 if len(lines) <= 2 else 88
    font = load_font(font_size, bold=True)

    line_h = font_size + 35
    start_x = 100
    start_y = (h - len(lines) * line_h) // 2

    # Accent bar on the left
    bar_y1 = start_y - 20
    bar_y2 = start_y + len(lines) * line_h + 20
    draw.rectangle([(60, bar_y1), (72, bar_y2)], fill=palette["accent"])

    for i, line in enumerate(lines):
        y = start_y + i * line_h
        draw.text((start_x+3, y+3), line, fill=(0, 0, 0, 35), font=font)
        draw.text((start_x, y), line, fill=palette["text"], font=font)


def layout_highlight_box(draw, w, h, title, palette):
    """文字带高亮背景框"""
    lines = wrap_text(title, 7)
    font_size = 100 if len(lines) <= 2 else 80
    font = load_font(font_size, bold=True)

    line_h = font_size + 45
    total_h = len(lines) * line_h
    start_y = (h - total_h) // 2

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x = (w - tw) // 2
        y = start_y + i * line_h

        # Highlight box behind text
        pad_x, pad_y = 25, 12
        draw.rectangle(
            [(x - pad_x, y - pad_y), (x + tw + pad_x, y + th + pad_y)],
            fill=palette["accent"]
        )
        # White text on accent background
        draw.text((x, y), line, fill=(255, 255, 255), font=font)


def layout_number_style(draw, w, h, title, palette):
    """带数字/序号装饰的风格"""
    lines = wrap_text(title, 7)
    font_size = 95 if len(lines) <= 2 else 78
    font = load_font(font_size, bold=True)

    # Big decorative number in background
    num_font = load_font(350, bold=True)
    num = random.choice(["01", "!", "★", "♥", "?!"])
    bbox = draw.textbbox((0, 0), num, font=num_font)
    nw = bbox[2] - bbox[0]
    nh = bbox[3] - bbox[1]
    draw.text(((w-nw)//2, (h-nh)//2 - 50), num, fill=palette["accent"] + (30,), font=num_font)

    # Title text
    line_h = font_size + 35
    total_h = len(lines) * line_h
    start_y = (h - total_h) // 2

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = (w - tw) // 2
        y = start_y + i * line_h
        draw.text((x+3, y+3), line, fill=(0, 0, 0, 40), font=font)
        draw.text((x, y), line, fill=palette["text"], font=font)


# ── 工具函数 ────────────────────────────────────────────────────────────

def wrap_text(text: str, max_chars: int = 7) -> list:
    lines = []
    for i in range(0, len(text), max_chars):
        lines.append(text[i:i + max_chars])
    return lines


# ── 主生成函数 ──────────────────────────────────────────────────────────

def generate(prompt: str = "", text_fallback: str = "", count: int = 1) -> list:
    """
    Generate cover image(s).
    Returns list of file paths.
    """
    display_text = text_fallback or prompt[:20] or "好物分享"
    paths = []
    for idx in range(count):
        path = _generate_one(display_text, idx)
        paths.append(path)
    return paths


def _generate_one(display_text: str, idx: int = 0) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"{timestamp}_{idx}.png"

    print(f"[封面生成] 图片 {idx+1}: {display_text}")

    w, h = 1080, 1080

    palette = random.choice(PALETTES)

    # Create RGBA image
    img = Image.new('RGBA', (w, h), palette["bg"] + (255,))
    draw = ImageDraw.Draw(img, 'RGBA')

    # Apply random background texture
    texture = random.choice(["noise", "grid", "dots", "circles", "stripes", "blocks", "clean"])
    accent_rgb = palette["accent"]

    if texture == "noise":
        bg_noise(img, intensity=10)
        draw = ImageDraw.Draw(img, 'RGBA')  # refresh draw after pixel manipulation
    elif texture == "grid":
        bg_grid(draw, w, h, accent_rgb)
    elif texture == "dots":
        bg_dots(draw, w, h, accent_rgb)
    elif texture == "circles":
        bg_circles(draw, w, h, accent_rgb)
    elif texture == "stripes":
        bg_stripes(draw, w, h, accent_rgb)
    elif texture == "blocks":
        bg_blocks(draw, w, h, accent_rgb)
    # "clean" = no texture

    # Apply random layout
    layout = random.choice([
        layout_centered,
        layout_top_heavy,
        layout_left_aligned,
        layout_highlight_box,
        layout_number_style,
    ])

    layout(draw, w, h, display_text, palette)

    # Convert to RGB and save
    img_rgb = img.convert('RGB')
    img_rgb.save(str(output_path), quality=95)
    print(f"[封面生成] 风格: {texture} + {layout.__name__}")
    print(f"[封面生成] 保存: {output_path}")
    return str(output_path)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", default="")
    parser.add_argument("--text", default="好物分享")
    args = parser.parse_args()

    try:
        paths = generate(args.prompt, args.text, count=3)
        for p in paths:
            print(f"[SUCCESS] {p}")
    except Exception as e:
        print(f"\n[FAIL] {e}")
        sys.exit(1)
