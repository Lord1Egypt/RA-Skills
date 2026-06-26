#!/usr/bin/env python3
"""
小红书图卡生成器（模板版）

使用方法：
1. 修改 DESIGN_TOKENS 中的配色方案为你的品牌色
2. 修改 CARDS 列表中的图卡内容
3. 运行：python3 gen_text_cards.py

依赖：pip install Pillow

输出：1080x1440px 的 3:4 竖图 PNG
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ============================================================
# Design Tokens（修改这里来匹配你的品牌风格）
# ============================================================

DESIGN_TOKENS = {
    # 画布
    "width": 1080,
    "height": 1440,
    
    # 调色板（示例：暖色极简风）
    "bg_color": (245, 240, 232),        # 背景色（奶油米色）
    "text_primary": (30, 30, 30),        # 标题文字（近黑）
    "text_secondary": (60, 55, 50),      # 正文文字（深棕）
    "text_tertiary": (120, 115, 108),    # 辅助文字（中灰）
    "accent_warm": (212, 168, 83),       # 暖色强调（黄金色）
    "accent_highlight": (199, 91, 58),   # 高亮色（暖红）
    "accent_soft": (225, 215, 200),      # 柔和色（米色，分隔线等）
    
    # 间距
    "margin_x": 96,         # 左右边距
    "margin_top": 140,      # 顶部留白
    "line_height_title": 80,  # 标题行高
    "line_height_body": 52,   # 正文行高
    
    # 字体（修改为你系统中可用的字体路径）
    "font_title": None,      # 中文标题字体路径（粗体）
    "font_body": None,       # 中文正文字体路径
    "font_en_title": None,   # 英文标题字体路径
    "font_en_body": None,    # 英文正文字体路径
}

# ============================================================
# 字体加载
# ============================================================

def load_fonts(tokens):
    """加载字体，失败时回退到默认字体"""
    fonts = {}
    
    # macOS 常用字体路径
    mac_fonts = {
        "cn_bold": "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "cn_regular": "/System/Library/Fonts/Hiragino Sans GB.ttc",
    }
    
    # 尝试加载中文标题字体
    try:
        path = tokens["font_title"] or mac_fonts.get("cn_bold")
        if path and os.path.exists(path):
            fonts["title_48"] = ImageFont.truetype(path, 48, index=1)
            fonts["title_36"] = ImageFont.truetype(path, 36, index=1)
            fonts["title_28"] = ImageFont.truetype(path, 28, index=1)
        else:
            fonts["title_48"] = ImageFont.load_default()
            fonts["title_36"] = ImageFont.load_default()
            fonts["title_28"] = ImageFont.load_default()
    except Exception:
        fonts["title_48"] = ImageFont.load_default()
        fonts["title_36"] = ImageFont.load_default()
        fonts["title_28"] = ImageFont.load_default()
    
    # 尝试加载中文正文字体
    try:
        path = tokens["font_body"] or mac_fonts.get("cn_regular")
        if path and os.path.exists(path):
            fonts["body_28"] = ImageFont.truetype(path, 28, index=0)
            fonts["body_24"] = ImageFont.truetype(path, 24, index=0)
            fonts["body_20"] = ImageFont.truetype(path, 20, index=0)
        else:
            fonts["body_28"] = ImageFont.load_default()
            fonts["body_24"] = ImageFont.load_default()
            fonts["body_20"] = ImageFont.load_default()
    except Exception:
        fonts["body_28"] = ImageFont.load_default()
        fonts["body_24"] = ImageFont.load_default()
        fonts["body_20"] = ImageFont.load_default()
    
    # 英文字体
    try:
        path = tokens["font_en_title"]
        if path and os.path.exists(path):
            fonts["en_title_160"] = ImageFont.truetype(path, 160)
            fonts["en_title_20"] = ImageFont.truetype(path, 20)
        else:
            fonts["en_title_160"] = fonts["title_48"]
            fonts["en_title_20"] = fonts["body_20"]
    except Exception:
        fonts["en_title_160"] = fonts["title_48"]
        fonts["en_title_20"] = fonts["body_20"]
    
    return fonts


# ============================================================
# 绘制辅助函数
# ============================================================

def draw_tag(draw, x, y, text, font, bg_color, text_color, padding=(12, 6)):
    """绘制圆角标签"""
    bbox = font.getbbox(text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    rect = [x, y, x + tw + padding[0] * 2, y + th + padding[1] * 2]
    draw.rounded_rectangle(rect, radius=6, fill=bg_color)
    draw.text((x + padding[0], y + padding[1]), text, fill=text_color, font=font)
    return rect[3] + 12  # 返回下一行 y 坐标


def draw_separator(draw, y, tokens):
    """绘制分隔线"""
    mx = tokens["margin_x"]
    w = tokens["width"]
    draw.line([(mx, y), (w - mx, y)], fill=tokens["accent_soft"], width=1)
    return y + 24


def wrap_text(text, font, max_width):
    """中文文本自动换行"""
    lines = []
    current_line = ""
    for char in text:
        test = current_line + char
        bbox = font.getbbox(test)
        if bbox[2] - bbox[0] > max_width:
            lines.append(current_line)
            current_line = char
        else:
            current_line = test
    if current_line:
        lines.append(current_line)
    return lines


# ============================================================
# 图卡生成
# ============================================================

def generate_card(card_config, tokens, fonts, output_path):
    """生成单张图卡"""
    w, h = tokens["width"], tokens["height"]
    img = Image.new("RGB", (w, h), tokens["bg_color"])
    draw = ImageDraw.Draw(img)
    
    mx = tokens["margin_x"]
    max_text_w = w - mx * 2
    y = tokens["margin_top"]
    
    # 标签
    if "tag" in card_config:
        y = draw_tag(
            draw, mx, y, card_config["tag"],
            fonts["body_20"], tokens["accent_warm"], (255, 255, 255)
        )
        y += 8
    
    # 标题
    if "title" in card_config:
        title_lines = wrap_text(card_config["title"], fonts["title_48"], max_text_w)
        for line in title_lines:
            draw.text((mx, y), line, fill=tokens["text_primary"], font=fonts["title_48"])
            y += tokens["line_height_title"]
        y += 16
    
    # 分隔线
    y = draw_separator(draw, y, tokens)
    
    # 正文内容
    if "body" in card_config:
        for paragraph in card_config["body"]:
            body_lines = wrap_text(paragraph, fonts["body_28"], max_text_w)
            for line in body_lines:
                draw.text((mx, y), line, fill=tokens["text_secondary"], font=fonts["body_28"])
                y += tokens["line_height_body"]
            y += 16  # 段间距
    
    # 列表项
    if "list_items" in card_config:
        for i, item in enumerate(card_config["list_items"], 1):
            # 序号圆圈
            cx, cy = mx + 16, y + 14
            draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=tokens["accent_warm"])
            draw.text((cx - 5, cy - 10), str(i), fill=(255, 255, 255), font=fonts["body_20"])
            
            # 列表文字
            item_lines = wrap_text(item, fonts["body_28"], max_text_w - 50)
            for line in item_lines:
                draw.text((mx + 44, y), line, fill=tokens["text_secondary"], font=fonts["body_28"])
                y += tokens["line_height_body"]
            y += 12
    
    # 底部引用/金句
    if "quote" in card_config:
        y += 16
        # 大引号装饰
        draw.text((mx, y - 10), """, fill=tokens["accent_soft"], font=fonts["title_48"])
        y += 40
        quote_lines = wrap_text(card_config["quote"], fonts["title_36"], max_text_w - 20)
        for line in quote_lines:
            draw.text((mx + 10, y), line, fill=tokens["text_primary"], font=fonts["title_36"])
            y += 60
    
    # 高亮句
    if "highlight" in card_config:
        y += 12
        hl_lines = wrap_text(card_config["highlight"], fonts["body_28"], max_text_w)
        for line in hl_lines:
            draw.text((mx, y), line, fill=tokens["accent_highlight"], font=fonts["body_28"])
            y += tokens["line_height_body"]
    
    # 保存
    img.save(output_path)
    print(f"✅ 生成: {output_path} ({w}x{h})")


# ============================================================
# 示例图卡配置
# ============================================================

SAMPLE_CARDS = [
    {
        "filename": "card-intro.png",
        "tag": "科普",
        "title": "这是一个示例标题",
        "body": [
            "这是第一段正文内容，用来介绍主题背景。",
            "这是第二段正文，进一步展开说明。"
        ],
    },
    {
        "filename": "card-list.png",
        "tag": "方法",
        "title": "3 个关键步骤",
        "list_items": [
            "第一步：先做精准调研（10分钟）",
            "第二步：确定视觉方向和 Design Token",
            "第三步：写 prompt 并过自检 checklist",
        ],
    },
    {
        "filename": "card-quote.png",
        "quote": "配图能力的核心不是工具操作，而是审美和生态理解。",
        "highlight": "工具可以学会，审美才是真正的壁垒。",
    },
]


# ============================================================
# 主函数
# ============================================================

if __name__ == "__main__":
    tokens = DESIGN_TOKENS
    fonts = load_fonts(tokens)
    
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    for card in SAMPLE_CARDS:
        output_path = os.path.join(output_dir, card["filename"])
        generate_card(card, tokens, fonts, output_path)
    
    print(f"\n✅ 完成！共生成 {len(SAMPLE_CARDS)} 张图卡")
    print(f"📁 输出目录: {output_dir}/")
