#!/usr/bin/env python3
"""小红书配图生成器 - 根据文章内容生成配图"""
import sys
import random
from PIL import Image, ImageFont, ImageDraw

# 默认参数
TITLE = ""
SUBTITLE = ""
CONTENT = ""

# 解析参数
if len(sys.argv) > 1:
    TITLE = sys.argv[1]
if len(sys.argv) > 2:
    SUBTITLE = sys.argv[2]
if len(sys.argv) > 3:
    CONTENT = sys.argv[3].replace("\\n", "\n")

# 配置
OUTPUT_PATH = "/root/.openclaw/workspace/xhs_cover.jpg"
WIDTH, HEIGHT = 1080, 1440
BG_COLOR = (255, 250, 245)  # 暖白色
FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"

def generate_cover(title, subtitle, content, output_path=OUTPUT_PATH):
    """生成小红书配图"""
    
    # 创建图片
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 装饰元素 - 星星和圆点
    for _ in range(15):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        r = random.randint(2, 8)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(255, 200, 100))
    
    # 加载字体
    try:
        title_font = ImageFont.truetype(FONT_PATH, 52)
        content_font = ImageFont.truetype(FONT_PATH, 32)
    except Exception as e:
        print(f"字体加载失败: {e}")
        title_font = ImageFont.load_default()
        content_font = ImageFont.load_default()
    
    # 绘制标题
    if title:
        draw.text((60, 180), title, fill=(60, 60, 60), font=title_font)
    
    # 绘制副标题
    if subtitle:
        draw.text((60, 250), subtitle, fill=(100, 100, 100), font=content_font)
    
    # 绘制内容
    if content:
        lines = content.split('\n')
        y_offset = 400
        for line in lines:
            if line.strip():
                draw.text((60, y_offset), line, fill=(80, 80, 80), font=content_font)
                y_offset += 50
    
    # 底部标签
    draw.text((60, HEIGHT - 100), "#今日分享", fill=(150, 150, 150), font=content_font)
    
    # 保存
    img.save(output_path, "JPEG", quality=95)
    print(f"配图已生成: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_cover(TITLE, SUBTITLE, CONTENT)
