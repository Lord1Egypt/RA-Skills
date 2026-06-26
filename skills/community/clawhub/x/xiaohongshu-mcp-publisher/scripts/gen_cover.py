#!/usr/bin/env python3
"""
小红书封面生成脚本

生成纯文字风格的封面图，适合新闻类笔记。

Usage:
    python gen_cover.py --title "标题" --keyword "关键词" --output "/tmp/openclaw/uploads/cover.png"
"""

import argparse
from PIL import Image, ImageDraw, ImageFont
import os

# 默认尺寸（小红书推荐 3:4）
WIDTH = 1080
HEIGHT = 1440

# 颜色配置
COLORS = {
    "blue": "#4A90D9",
    "pink": "#E8A0BF",
    "green": "#7BC47F",
    "orange": "#F5A623",
    "purple": "#9B59B6",
}

def find_font(size=60):
    """查找可用的中文字体"""
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    # fallback
    return ImageFont.load_default()


def create_cover(title, keyword=None, color="blue", output_path="/tmp/openclaw/uploads/cover.png"):
    """生成封面图"""
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 创建背景
    bg_color = COLORS.get(color, COLORS["blue"])
    img = Image.new("RGB", (WIDTH, HEIGHT), bg_color)
    draw = ImageDraw.Draw(img)
    
    # 绘制白色卡片
    card_margin = 80
    card_x1 = card_margin
    card_y1 = card_margin + 100
    card_x2 = WIDTH - card_margin
    card_y2 = HEIGHT - card_margin - 100
    
    draw.rectangle(
        [(card_x1, card_y1), (card_x2, card_y2)],
        fill="white",
        outline=None
    )
    
    # 绘制标题
    title_font = find_font(80)
    
    # 计算标题位置（居中）
    title_lines = []
    if len(title) > 15:
        # 分行
        mid = len(title) // 2
        title_lines = [title[:mid], title[mid:]]
    else:
        title_lines = [title]
    
    line_height = 100
    total_height = len(title_lines) * line_height
    start_y = (card_y1 + card_y2) // 2 - total_height // 2
    
    for i, line in enumerate(title_lines):
        # 计算每行宽度
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2
        y = start_y + i * line_height
        
        draw.text((x, y), line, fill="black", font=title_font)
    
    # 绘制关键词高亮（如果有）
    if keyword:
        kw_font = find_font(50)
        kw_bbox = draw.textbbox((0, 0), keyword, font=kw_font)
        kw_width = kw_bbox[2] - kw_bbox[0]
        kw_x = (WIDTH - kw_width) // 2
        kw_y = start_y + len(title_lines) * line_height + 50
        
        # 高亮背景
        highlight_margin = 20
        draw.rectangle(
            [(kw_x - highlight_margin, kw_y - 10), 
             (kw_x + kw_width + highlight_margin, kw_y + 50)],
            fill=bg_color
        )
        draw.text((kw_x, kw_y), keyword, fill="white", font=kw_font)
    
    # 保存
    img.save(output_path, "PNG")
    print(f"✅ 封面已生成: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="生成小红书封面")
    parser.add_argument("--title", required=True, help="标题文字")
    parser.add_argument("--keyword", default=None, help="关键词高亮")
    parser.add_argument("--color", default="blue", choices=COLORS.keys(), help="背景颜色")
    parser.add_argument("--output", default="/tmp/openclaw/uploads/cover.png", help="输出路径")
    
    args = parser.parse_args()
    
    create_cover(args.title, args.keyword, args.color, args.output)


if __name__ == "__main__":
    main()