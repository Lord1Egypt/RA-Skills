#!/usr/bin/env python3
"""
连环画页面合成脚本
将插图与文字说明合成为最终页面
"""

import argparse
import os
from PIL import Image, ImageDraw, ImageFont
import logging
import json
from datetime import datetime

# 1. 配置日志器
logger = logging.getLogger("LLM_Interaction")
logger.setLevel(logging.DEBUG)

# 避免重复添加 handler
if not logger.handlers:
    # 文件 Handler
    fh = logging.FileHandler("composite-page.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    
    # 控制台 Handler (可选)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # 格式化器
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="合成连环画页面（插图 + 文字）"
    )
    parser.add_argument("--image", required=True, help="插图文件路径")
    parser.add_argument("--text", required=True, help="文字说明内容")
    parser.add_argument("--output", required=True, help="输出文件路径")
    parser.add_argument("--text-ratio", type=float, default=0.20, help="文字区域占比（默认 0.20）")
    parser.add_argument("--aspect", default="3:4", help="宽高比（默认 3:4）")
    parser.add_argument("--bg-color", default="#FFFFFF", help="文字区域背景色（默认 #FFFFFF）")
    parser.add_argument("--text-color", default="#1A1A1A", help="文字颜色（默认 #1A1A1A）")
    parser.add_argument("--font-size", type=int, default=0, help="字体大小（0 表示自动）")
    parser.add_argument("--font-family", default="", help="字体文件路径")
    parser.add_argument("--padding", type=int, default=0, help="内边距（0 表示自动）")
    # 新增：页码相关选项
    parser.add_argument("--page-number", default="", help="页面数字文本，如 '1/10' 或 '1'（默认空，不显示）")
    parser.add_argument("--page-number-color", default="#666666", help="页码颜色（默认 #666666）")
    parser.add_argument("--page-number-font-size", type=int, default=0, help="页码字体大小（0 表示自动）")
    parser.add_argument("--page-number-margin", type=int, default=0, help="页码距右下角边距（0 表示自动）")
    return parser.parse_args()


def parse_aspect(aspect_str):
    """解析宽高比字符串（如 '3:4'）"""
    parts = aspect_str.split(":")
    return float(parts[0]), float(parts[1])


def wrap_text(text, font, max_width, draw):
    """
    将文字按最大宽度换行
    返回行列表
    """
    lines = []
    current_line = ""

    for char in text:
        test_line = current_line + char
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]

        if width > max_width and len(current_line) > 0:
            lines.append(current_line)
            current_line = char
        else:
            current_line = test_line

    if current_line:
        lines.append(current_line)

    return lines


def get_font(font_path, size):
    """
    尝试加载字体
    优先使用指定字体，否则使用系统中文字体，最后降级到默认字体
    """
    # 中文字体候选列表（按优先级排序）
    font_candidates = [
        "C:\\Windows\\Fonts\\simsun.ttc",  # 宋体
        "C:\\Windows\\Fonts\\msyh.ttc",     # 微软雅黑
        "C:\\Windows\\Fonts\\simhei.ttf",   # 黑体
        "/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc",  # Linux Noto
        "/System/Library/Fonts/PingFang.ttc",  # macOS
        "/System/Library/Fonts/STHeiti Light.ttc",  # macOS 旧版
    ]

    if font_path:
        try:
            return ImageFont.truetype(font_path, size)
        except:
            pass

    # 尝试系统字体
    for font_file in font_candidates:
        if os.path.exists(font_file):
            try:
                return ImageFont.truetype(font_file, size)
            except:
                continue

    # 降级到默认字体
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()


def composite(args):
    """合成插图和文字"""
    # 加载插图
    img = Image.open(args.image)

    logger.info(f"开始合成: {args.image}")
    # 解析宽高比
    aspect_w, aspect_h = parse_aspect(args.aspect)

    # 计算画布尺寸（基准宽度 960px）
    base_width = 960
    base_height = int(base_width * (aspect_h / aspect_w))

    text_area_height = int(base_height * args.text_ratio)
    image_area_height = base_height - text_area_height
    padding = args.padding if args.padding > 0 else int(base_width * 0.04)

    # 创建画布
    canvas = Image.new("RGB", (base_width, base_height), "#FFFFFF")
    draw = ImageDraw.Draw(canvas)

    # 1. 绘制插图（覆盖模式：裁剪以适应）
    img_aspect = img.width / img.height
    area_aspect = base_width / image_area_height

    if img_aspect > area_aspect:
        # 图片较宽 - 适配高度，裁剪两侧
        draw_h = image_area_height
        draw_w = int(image_area_height * img_aspect)
        draw_x = (base_width - draw_w) // 2
        draw_y = 0
    else:
        # 图片较高 - 适配宽度，裁剪上下
        draw_w = base_width
        draw_h = int(base_width / img_aspect)
        draw_x = 0
        draw_y = (image_area_height - draw_h) // 2

    # 缩放并粘贴插图
    img_resized = img.resize((draw_w, draw_h), Image.Resampling.LANCZOS)
    canvas.paste(img_resized, (draw_x, draw_y))

    # 2. 绘制文字区域背景
    draw.rectangle(
        [0, image_area_height, base_width, base_height],
        fill=args.bg_color
    )

    # 3. 绘制分隔线
    draw.line(
        [(padding, image_area_height), (base_width - padding, image_area_height)],
        fill="#CCCCCC",
        width=2
    )

    # 4. 计算字体大小并排版文字
    max_text_width = base_width - padding * 2
    max_text_height = text_area_height - padding * 2

    font_size = args.font_size if args.font_size > 0 else int(base_width * 0.026)
    min_font_size = 14
    line_height_ratio = 1.7

    # 自动缩小字体以适应区域
    font = get_font(args.font_family, font_size)
    lines = wrap_text(args.text, font, max_text_width, draw)
    line_height = int(font_size * line_height_ratio)

    while True:
        total_height = len(lines) * line_height
        if total_height <= max_text_height or font_size <= min_font_size:
            break
        font_size -= 1
        font = get_font(args.font_family, font_size)
        lines = wrap_text(args.text, font, max_text_width, draw)
        line_height = int(font_size * line_height_ratio)

    # 5. 绘制文字（居中）
    total_text_height = len(lines) * line_height
    text_start_y = image_area_height + (text_area_height - total_text_height) // 2 + line_height // 2

    for i, line in enumerate(lines):
        y = text_start_y + i * line_height
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (base_width - text_width) // 2
        draw.text((x, y), line, fill=args.text_color, font=font)

    # 6. 绘制页码（右下方）
    if args.page_number:
        pn_font_size = (
            args.page_number_font_size
            if args.page_number_font_size > 0
            else int(base_width * 0.022)
        )
        pn_font = get_font(args.font_family, pn_font_size)
        pn_margin = (
            args.page_number_margin
            if args.page_number_margin > 0
            else int(base_width * 0.03)
        )

        bbox = draw.textbbox((0, 0), args.page_number, font=pn_font)
        pn_width = bbox[2] - bbox[0]
        pn_height = bbox[3] - bbox[1]

        # 右下角坐标（考虑 textbbox 的偏移）
        pn_x = base_width - pn_margin - pn_width - bbox[0]
        pn_y = base_height - pn_margin - pn_height - bbox[1]

        draw.text(
            (pn_x, pn_y),
            args.page_number,
            fill=args.page_number_color,
            font=pn_font
        )

    # 7. 保存输出
    output_dir = os.path.dirname(os.path.abspath(args.output))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    canvas.save(args.output, "PNG")

    logger.info(f"合成完成: {args.output}")


if __name__ == "__main__":
    args = parse_args()
    try:
        composite(args)
    except Exception as e:
        print(f"合成失败: {e}")
        import traceback
        traceback.print_exc()
        exit(1)