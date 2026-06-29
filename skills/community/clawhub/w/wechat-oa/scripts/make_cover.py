# -*- coding: utf-8 -*-
# make_cover.ps1 - 生成微信公众号封面图（纯 Python + Pillow 实现，跨平台）
# 用法: python make_cover.py --title "标题" --subtitle "副标题" --output cover.jpg

import argparse
from PIL import Image, ImageDraw, ImageFont
import os

def make_cover(title, subtitle="", output="cover.jpg", width=900, height=383):
    # 创建渐变背景
    img = Image.new("RGB", (width, height), "#1a1a2e")
    draw = ImageDraw.Draw(img)

    # 简单渐变（从深蓝到深紫）
    for y in range(height):
        ratio = y / height
        r = int(26 + ratio * 20)
        g = int(26 + ratio * 10)
        b = int(46 + ratio * 60)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # 标题
    try:
        font_title = ImageFont.truetype("msyh.ttc", 48)
        font_sub = ImageFont.truetype("msyh.ttc", 24)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # 标题居中
    bbox = draw.textbbox((0, 0), title, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, height // 2 - 40), title, fill="white", font=font_title)

    if subtitle:
        bbox2 = draw.textbbox((0, 0), subtitle, font=font_sub)
        sw = bbox2[2] - bbox2[0]
        draw.text(((width - sw) // 2, height // 2 + 20), subtitle, fill="#aaaaff", font=font_sub)

    img.save(output, "JPEG", quality=90)
    print(f"封面图已生成：{output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成微信公众号封面图")
    parser.add_argument("--title", required=True, help="封面标题")
    parser.add_argument("--subtitle", default="", help="副标题")
    parser.add_argument("--output", default="cover.jpg", help="输出文件名")
    args = parser.parse_args()
    make_cover(args.title, args.subtitle, args.output)
