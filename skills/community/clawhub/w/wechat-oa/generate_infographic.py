# -*- coding: utf-8 -*-
"""
公众号文章配图生成器（PIL）
根据章节内容自动生成信息图、流程图、文字卡片等配图

用法:
    python generate_infographic.py <类型> <输出路径> [参数...]
    
类型:
    steps     - 流程图（步骤流程）
    comparison - 对比图（两列对比）
    timeline  - 时间线
    textcard  - 文字卡片（金句/要点）
    stats     - 数据统计图

示例:
    python generate_infographic.py steps output/step.png "注册账号" "填写信息" "完成汇款"
    python generate_infographic.py comparison output/compare.png "传统方式:3天" "西联:几分钟"
    python generate_infographic.py textcard output/quote.png "天下没有难汇的款"
"""

import sys
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# 字体路径（Windows）
FONT_DIR = "C:/Windows/Fonts"

# 默认颜色配置
COLORS = {
    'primary': (41, 128, 185),      # 蓝色
    'success': (39, 174, 96),       # 绿色
    'warning': (230, 126, 34),      # 橙色
    'danger': (231, 76, 60),        # 红色
    'dark': (44, 62, 80),           # 深灰蓝
    'light': (236, 240, 241),       # 浅灰
    'white': (255, 255, 255),
    'gray': (127, 140, 141),
}


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """获取字体"""
    fonts = {
        'title': 'msyhbd.ttc' if bold else 'msyh.ttc',
        'body': 'msyh.ttc',
    }
    
    try:
        return ImageFont.truetype(f"{FONT_DIR}/msyh.ttc", size)
    except:
        try:
            return ImageFont.truetype(f"{FONT_DIR}/SIMHEI.ttf", size)
        except:
            return ImageFont.load_default()


def create_gradient(width: int, height: int, color1: tuple, color2: tuple, direction: str = 'horizontal'):
    """创建渐变背景"""
    img = Image.new('RGB', (width, height), color1)
    draw = ImageDraw.Draw(img)
    
    for i in range(height if direction == 'vertical' else width):
        ratio = i / (height if direction == 'vertical' else width)
        
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        
        if direction == 'vertical':
            draw.line([(0, i), (width, i)], fill=(r, g, b))
        else:
            draw.line([(i, 0), (i, height)], fill=(r, g, b))
    
    return img


def draw_rounded_rect(draw, xy, radius: int, fill: tuple, outline: tuple = None, width: int = 1):
    """绘制圆角矩形"""
    x1, y1, x2, y2 = xy
    
    # 绘制主体
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    
    # 绘制四个角
    draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill)
    draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill)
    
    # 绘制边框
    if outline:
        draw.arc([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=outline, width=width)
        draw.arc([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([x1 + radius, y1, x2 - radius, y1], fill=outline, width=width)
        draw.line([x1 + radius, y2, x2 - radius, y2], fill=outline, width=width)
        draw.line([x1, y1 + radius, x1, y2 - radius], fill=outline, width=width)
        draw.line([x2, y1 + radius, x2, y2 - radius], fill=outline, width=width)


def generate_steps(steps: list, output_path: str, title: str = "") -> str:
    """生成流程图"""
    width = 677
    step_height = 60
    padding = 30
    gap = 20
    arrow_height = 30
    
    # 计算高度
    content_height = len(steps) * step_height + (len(steps) - 1) * gap + (len(steps) - 1) * arrow_height
    height = padding * 2 + content_height + (50 if title else 0)
    
    # 创建画布
    img = Image.new('RGB', (width, height), COLORS['white'])
    draw = ImageDraw.Draw(img)
    
    # 标题
    y = padding
    if title:
        font = get_font(18, bold=True)
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) // 2, y), title, font=font, fill=COLORS['dark'])
        y += 50
    
    # 绘制步骤
    colors = [COLORS['primary'], COLORS['success'], COLORS['warning'], COLORS['danger']]
    
    for i, step in enumerate(steps):
        color = colors[i % len(colors)]
        
        # 步骤框
        box_y = y
        draw_rounded_rect(draw, [30, box_y, width - 30, box_y + step_height], 10, color)
        
        # 步骤编号
        num_font = get_font(20, bold=True)
        num_text = str(i + 1)
        draw.text((50, box_y + 15), num_text, font=num_font, fill=COLORS['white'])
        
        # 步骤文字
        text_font = get_font(16)
        draw.text((90, box_y + 18), step, font=text_font, fill=COLORS['white'])
        
        y += step_height
        
        # 箭头
        if i < len(steps) - 1:
            arrow_y = y + 5
            center_x = width // 2
            
            # 箭头线
            draw.line([(center_x, arrow_y), (center_x, arrow_y + arrow_height - 15)], fill=COLORS['gray'], width=3)
            
            # 箭头尖
            draw.polygon([
                (center_x, arrow_y + arrow_height),
                (center_x - 10, arrow_y + arrow_height - 15),
                (center_x + 10, arrow_y + arrow_height - 15)
            ], fill=COLORS['gray'])
            
            y += arrow_height
    
    img.save(output_path, 'PNG')
    return output_path


def generate_comparison(items: list, output_path: str, title: str = "") -> str:
    """生成对比图"""
    width = 677
    item_height = 80
    padding = 30
    gap = 20
    
    # 计算高度
    content_height = len(items) * item_height + (len(items) - 1) * gap
    height = padding * 2 + content_height + (50 if title else 0)
    
    # 创建画布
    img = Image.new('RGB', (width, height), COLORS['white'])
    draw = ImageDraw.Draw(img)
    
    # 标题
    y = padding
    if title:
        font = get_font(18, bold=True)
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) // 2, y), title, font=font, fill=COLORS['dark'])
        y += 50
    
    # 绘制对比项
    for item in items:
        if ':' in item:
            label, value = item.split(':', 1)
        else:
            label = ""
            value = item
        
        left_color = COLORS['gray']
        right_color = COLORS['primary']
        
        # 左侧标签
        left_x = padding
        draw_rounded_rect(draw, [left_x, y, left_x + 250, y + item_height], 10, left_color)
        font = get_font(14)
        draw.text((left_x + 20, y + 30), label.strip(), font=font, fill=COLORS['white'])
        
        # 右侧值
        right_x = width - padding - 250
        draw_rounded_rect(draw, [right_x, y, right_x + 250, y + item_height], 10, right_color)
        draw.text((right_x + 20, y + 30), value.strip(), font=font, fill=COLORS['white'])
        
        y += item_height + gap
    
    img.save(output_path, 'PNG')
    return output_path


def generate_timeline(events: list, output_path: str, title: str = "") -> str:
    """生成时间线"""
    width = 677
    event_height = 60
    dot_radius = 8
    padding = 30
    line_x = 60
    
    # 计算高度
    height = padding * 2 + len(events) * event_height + (50 if title else 0)
    
    # 创建画布
    img = Image.new('RGB', (width, height), COLORS['white'])
    draw = ImageDraw.Draw(img)
    
    # 标题
    y = padding
    if title:
        font = get_font(18, bold=True)
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) // 2, y), title, font=font, fill=COLORS['dark'])
        y += 50
    
    # 绘制主线
    draw.line([(line_x, y + dot_radius), (line_x, y + len(events) * event_height - dot_radius)], 
               fill=COLORS['light'], width=4)
    
    # 绘制事件
    for i, event in enumerate(events):
        if ':' in event:
            time, desc = event.split(':', 1)
        else:
            time = ""
            desc = event
        
        event_y = y + i * event_height
        
        # 时间点
        draw.ellipse([line_x - dot_radius, event_y, line_x + dot_radius, event_y + dot_radius * 2], 
                     fill=COLORS['primary'])
        
        # 时间
        font = get_font(12)
        draw.text((line_x + 25, event_y + 5), time.strip(), font=font, fill=COLORS['gray'])
        
        # 描述
        font = get_font(14)
        desc_x = line_x + 120
        draw.text((desc_x, event_y + 5), desc.strip(), font=font, fill=COLORS['dark'])
    
    img.save(output_path, 'PNG')
    return output_path


def generate_textcard(text: str, output_path: str, bg_color: tuple = None, width: int = 677, height: int = 200) -> str:
    """生成文字卡片"""
    if bg_color is None:
        bg_color = COLORS['primary']
    
    # 创建画布
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # 装饰线
    line_y = height // 2 - 30
    draw.rectangle([50, line_y, width - 50, line_y + 2], fill=COLORS['white'])
    
    # 文字
    font_size = 28 if len(text) < 20 else (24 if len(text) < 30 else 20)
    font = get_font(font_size, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    draw.text((x, y), text, font=font, fill=COLORS['white'])
    
    img.save(output_path, 'PNG')
    return output_path


def generate_stats(stats: list, output_path: str, title: str = "") -> str:
    """生成数据统计图"""
    width = 677
    bar_height = 50
    padding = 30
    label_width = 150
    gap = 15
    
    # 计算高度
    height = padding * 2 + len(stats) * bar_height + (len(stats) - 1) * gap + (50 if title else 0)
    
    # 创建画布
    img = Image.new('RGB', (width, height), COLORS['white'])
    draw = ImageDraw.Draw(img)
    
    # 标题
    y = padding
    if title:
        font = get_font(18, bold=True)
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) // 2, y), title, font=font, fill=COLORS['dark'])
        y += 50
    
    max_value = max(float(s.split(':')[1]) if ':' in s else 100 for s in stats)
    bar_max_width = width - padding * 2 - label_width - 80
    
    # 绘制统计条
    for stat in stats:
        if ':' in stat:
            label, value = stat.split(':', 1)
            value = float(value)
        else:
            label = stat
            value = 100
        
        # 标签
        font = get_font(14)
        draw.text((padding, y + 15), label.strip(), font=font, fill=COLORS['dark'])
        
        # 条形背景
        bar_x = padding + label_width
        draw_rounded_rect(draw, [bar_x, y + 5, bar_x + bar_max_width, y + bar_height], 8, COLORS['light'])
        
        # 条形值
        bar_width = int(bar_max_width * (value / max_value))
        if bar_width > 0:
            draw_rounded_rect(draw, [bar_x, y + 5, bar_x + bar_width, y + bar_height], 8, COLORS['primary'])
        
        # 数值
        value_font = get_font(14, bold=True)
        draw.text((bar_x + bar_width + 10, y + 15), f"{value:.0f}", font=value_font, fill=COLORS['dark'])
        
        y += bar_height + gap
    
    img.save(output_path, 'PNG')
    return output_path


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    img_type = sys.argv[1]
    output_path = sys.argv[2]
    args = sys.argv[3:] if len(sys.argv) > 3 else []
    
    # 确保输出目录存在
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    result = None
    
    if img_type == 'steps':
        # 流程图: python generate_infographic.py steps output.png "步骤1" "步骤2" "步骤3"
        if len(args) < 2:
            print("错误: steps 类型需要至少2个步骤")
            sys.exit(1)
        title = args[0] if not args[0].startswith('"') else ""
        steps = args
        result = generate_steps(steps, output_path, title)
        
    elif img_type == 'comparison':
        # 对比图: python generate_infographic.py comparison output.png "优点:很多" "缺点:很少"
        if len(args) < 1:
            print("错误: comparison 类型需要至少1组对比数据")
            sys.exit(1)
        title = args[0] if len(args) > 1 and not args[0].startswith('"') else ""
        items = args[1:] if title else args
        result = generate_comparison(items, output_path, title)
        
    elif img_type == 'timeline':
        # 时间线: python generate_infographic.py timeline output.png "2024:事件1" "2025:事件2"
        if len(args) < 2:
            print("错误: timeline 类型需要至少2个时间点")
            sys.exit(1)
        title = args[0] if not args[0].startswith('"') else ""
        events = args[1:] if title else args
        result = generate_timeline(events, output_path, title)
        
    elif img_type == 'textcard':
        # 文字卡片: python generate_infographic.py textcard output.png "要显示的文字"
        if len(args) < 1:
            print("错误: textcard 类型需要文字内容")
            sys.exit(1)
        result = generate_textcard(args[0], output_path)
        
    elif img_type == 'stats':
        # 数据统计: python generate_infographic.py stats output.png "满意度:85" "便利性:90"
        if len(args) < 1:
            print("错误: stats 类型需要至少1组数据")
            sys.exit(1)
        title = args[0] if len(args) > 1 and not args[0].startswith('"') else ""
        stats = args[1:] if title else args
        result = generate_stats(stats, output_path, title)
        
    else:
        print(f"错误: 未知的类型 '{img_type}'")
        print(__doc__)
        sys.exit(1)
    
    print(f"✅ 配图已保存: {result}")
    return result


if __name__ == "__main__":
    main()
