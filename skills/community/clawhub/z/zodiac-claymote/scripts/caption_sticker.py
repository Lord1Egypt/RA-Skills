#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
表情包文案叠加器 —— 裁正方 + 叠中文描边字 + 导出微信规格

为什么需要它：生图模型画中文几乎必错，所以提示词里绝不写文字，
生成无字图后用本脚本叠加文案。

用法:
  # 1) 按顺序给文案
  python caption_sticker.py --input ./raw --captions "好耶,无语,我裂开,摸了" --size 240

  # 2) 用映射文件（推荐，顺序可控）
  python caption_sticker.py --input ./raw --caption-map captions.json --size 240

  # captions.json 格式:
  #   {"01.png": "好耶", "02.png": "无语"}      或   ["好耶", "无语", ...]

  # 3) 只裁切不加字
  python caption_sticker.py --input ./raw --no-text --size 240

可选参数:
  --output/-o    输出目录（默认 ./sticker_out）
  --size         导出尺寸（240 = 微信表情主图；120 = 缩略图；512 = 高清）
  --font         字体文件路径（默认自动找微软雅黑粗体）
  --ratio        文字占画面高度比例，默认 0.13
  --position     bottom（默认）/ top
  --margin-bottom  文字距底边比例，默认 0.06
  --no-text      不加文字
  --color        文字颜色，默认 #FFFFFF
  --stroke       描边颜色，默认 #2B2B2B
"""

import argparse
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("[缺少依赖] 请先安装 Pillow：\n"
             "  C:\\Users\\peisenzhang\\.workbuddy\\binaries\\python\\envs\\default\\Scripts\\pip.exe install Pillow\n"
             "（或任意 python -m pip install Pillow）")

FONT_CANDIDATES = [
    "C:/Windows/Fonts/msyhbd.ttc",   # 微软雅黑 Bold
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",   # 黑体
    "C:/Windows/Fonts/Dengb.ttf",    # 等线 Bold
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
]

IMG_EXT = (".png", ".jpg", ".jpeg", ".webp", ".bmp")


def find_font(user_font=None):
    if user_font and os.path.exists(user_font):
        return user_font
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    sys.exit("[错误] 未找到中文字体，请用 --font 指定字体文件路径")


def square_crop(img):
    """居中裁剪为正方形（表情包必须是方的）"""
    w, h = img.size
    if w == h:
        return img
    s = min(w, h)
    left, top = (w - s) // 2, (h - s) // 2
    return img.crop((left, top, left + s, top + s))


def fit_font(draw, text, font_path, target_w, max_h):
    """从大到小找合适字号，保证不超出宽度与高度"""
    size = int(max_h)
    while size > 8:
        try:
            f = ImageFont.truetype(font_path, size)
        except Exception:
            f = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=f)
        if (bbox[2] - bbox[0]) <= target_w and (bbox[3] - bbox[1]) <= max_h:
            return f, size
        size -= 2
    try:
        return ImageFont.truetype(font_path, 8), 8
    except Exception:
        return ImageFont.load_default(), 8


def process(src, dst, caption, font_path, size, ratio, position, margin_bottom,
            color, stroke, stroke_ratio):
    img = Image.open(src)
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    img = square_crop(img)
    img = img.resize((size, size), Image.LANCZOS)

    if caption:
        draw = ImageDraw.Draw(img)
        max_h = int(size * ratio)
        target_w = int(size * 0.86)
        font, fsize = fit_font(draw, caption, font_path, target_w, max_h)
        bbox = draw.textbbox((0, 0), caption, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = (size - tw) // 2 - bbox[0]
        y = (int(size * (1 - margin_bottom) - th) if position == "bottom"
             else int(size * margin_bottom)) - bbox[1]
        sw = max(2, int(fsize * stroke_ratio))
        draw.text((x, y), caption, font=font, fill=color,
                  stroke_width=sw, stroke_fill=stroke)

    img.save(dst, "PNG", optimize=True)
    return os.path.getsize(dst)


def load_captions(caption_map, captions_arg, files):
    if caption_map:
        with open(caption_map, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return {k: v for k, v in data.items()}
        if isinstance(data, list):
            return {files[i]: data[i] for i in range(min(len(data), len(files)))}
    if captions_arg:
        parts = [p.strip() for p in captions_arg.replace("，", ",").split(",") if p.strip()]
        return {files[i]: parts[i] for i in range(min(len(parts), len(files)))}
    return {}


def main():
    ap = argparse.ArgumentParser(description="表情包文案叠加 + 裁切 + 导出")
    ap.add_argument("--input", "-i", required=True, help="原图目录")
    ap.add_argument("--output", "-o", default="sticker_out", help="输出目录")
    ap.add_argument("--captions", help="逗号分隔的文案，按文件名顺序对应")
    ap.add_argument("--caption-map", help="JSON 映射文件，{\"01.png\":\"好耶\"} 或数组")
    ap.add_argument("--size", type=int, default=240, help="导出尺寸，默认 240（微信表情主图）")
    ap.add_argument("--font", help="字体文件路径")
    ap.add_argument("--ratio", type=float, default=0.13, help="文字高度占画面比例")
    ap.add_argument("--position", choices=["bottom", "top"], default="bottom")
    ap.add_argument("--margin-bottom", type=float, default=0.06, help="文字距底边比例")
    ap.add_argument("--color", default="#FFFFFF", help="文字颜色")
    ap.add_argument("--stroke", default="#2B2B2B", help="描边颜色")
    ap.add_argument("--stroke-ratio", type=float, default=0.16, help="描边宽度相对字号比例")
    ap.add_argument("--no-text", action="store_true", help="只裁切导出，不加文字")
    args = ap.parse_args()

    src_dir = os.path.abspath(args.input)
    if not os.path.isdir(src_dir):
        sys.exit(f"[错误] 目录不存在: {src_dir}")
    files = sorted([f for f in os.listdir(src_dir) if f.lower().endswith(IMG_EXT)])
    if not files:
        sys.exit(f"[错误] {src_dir} 里没有图片")

    out_dir = os.path.abspath(args.output)
    os.makedirs(out_dir, exist_ok=True)
    font_path = find_font(args.font)
    cap_map = {} if args.no_text else load_captions(args.caption_map, args.captions, files)

    print(f"[信息] 字体: {font_path}")
    print(f"[信息] 输入 {len(files)} 张 → 输出尺寸 {args.size}x{args.size} → {out_dir}\n")

    results = []
    for i, fn in enumerate(files, 1):
        dst = os.path.join(out_dir, f"{i:02d}.png")
        cap = cap_map.get(fn, "")
        size_b = process(os.path.join(src_dir, fn), dst, cap, font_path, args.size,
                         args.ratio, args.position, args.margin_bottom,
                         args.color, args.stroke, args.stroke_ratio)
        flag = "  ⚠ 超过 100KB" if size_b > 100 * 1024 else ""
        print(f"  {i:02d}. {fn}  →  {os.path.basename(dst)}  文案「{cap or '—'}」"
              f"  {size_b/1024:.0f}KB{flag}")
        results.append((dst, size_b))

    over = [r for r in results if r[1] > 100 * 1024]
    print(f"\n[完成] {len(results)} 张已导出到 {out_dir}")
    if over:
        print(f"[提示] {len(over)} 张超过微信单张 100KB 上限，建议用 --size 240 或压缩工具处理")
    print("[提示] 微信投稿还需：缩略图 120x120、详情页横幅 750x400、聊天页图标 50x50")


if __name__ == "__main__":
    main()
