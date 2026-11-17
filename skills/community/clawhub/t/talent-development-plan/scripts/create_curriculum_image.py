#!/usr/bin/env python3
"""
课程体系架构图生成脚本：使用 PIL 绘制课程体系架构图，支持中文显示。
传入课程数据 JSON（字符串或文件路径），输出 PNG 图片。

布局策略：
- 自动根据最长课程名计算列宽，避免文字溢出
- 长课程名自动换行
- 自适应图片宽度（最小1200px，按需扩展至2000px）
- 层次化布局：标题 → 结构概览 → 分类课程详情
"""

import argparse
import json
import os
import sys


def load_font(size=16):
    """加载中文字体，按平台优先级尝试"""
    from PIL import ImageFont

    font_paths = [
        # Linux
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJKsc-Regular.otf",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        # macOS
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        # Windows
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ]

    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue

    # Fallback
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except Exception:
        return ImageFont.load_default()


def measure_text(text, font):
    """测量文本像素宽度"""
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0]


def wrap_text(text, font, max_width):
    """将长文本按max_width自动换行，返回行列表"""
    if measure_text(text, font) <= max_width:
        return [text]

    lines = []
    current = ""
    for ch in text:
        test = current + ch
        if measure_text(test, font) > max_width:
            if current:
                lines.append(current)
            current = ch
        else:
            current = test
    if current:
        lines.append(current)
    return lines


def draw_rounded_rect(draw, xy, fill, outline, radius=8, width=1):
    """绘制圆角矩形"""
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_arrow_down(draw, x, y, length, color="#999999", head_size=6):
    """绘制向下的箭头"""
    draw.line([(x, y), (x, y + length - head_size)], fill=color, width=2)
    draw.polygon([(x - head_size, y + length - head_size),
                  (x + head_size, y + length - head_size),
                  (x, y + length)], fill=color)


def generate_image(data, output_path, width=1400):
    """生成课程体系架构图"""
    from PIL import Image, ImageDraw

    # Extract data
    major_name = data.get("major_name", "XX专业")
    level = data.get("level", "中职")
    public_courses = data.get("public_courses", [])
    basic_courses = data.get("basic_courses", [])
    core_courses = data.get("core_courses", [])
    elective_courses = data.get("elective_courses", [])
    practice_courses = data.get("practice_courses", [])

    # Font sizes
    font_title_large = load_font(26)
    font_title = load_font(17)
    font_subtitle = load_font(14)
    font_text = load_font(13)
    font_small = load_font(11)

    # Category definitions
    categories = [
        ("公共基础课", public_courses, "#2E75B6", "#E8F0FE", "国家规定必修+限定选修"),
        ("专业基础课", basic_courses, "#548235", "#EBF1DE", "专业入门与基础技能"),
        ("专业核心课", core_courses, "#C00000", "#FBE5D6", "教学标准规定·核心能力"),
        ("专业拓展/选修课", elective_courses, "#7030A0", "#E8D5F5", "岗位拓展与个性发展"),
        ("集中实践教学", practice_courses, "#BF8F00", "#FFF2CC", "实训+岗位实习"),
    ]

    # Filter empty categories
    categories = [(t, c, hc, bc, desc) for t, c, hc, bc, desc in categories if c]
    if not categories:
        categories = [("课程", ["暂无课程数据"], "#999999", "#EEEEEE", "")]

    # --- Auto-calculate column widths based on content ---
    margin_x = 50
    gap = 18
    padding_x = 24  # text padding inside column
    header_h = 32
    sub_header_h = 22
    line_h = 22
    padding_bottom = 14

    # Calculate required width for each column
    col_widths = []
    for cat_title, courses, _, _, desc in categories:
        # Width needed for category title
        title_w = measure_text(cat_title, font_title) + padding_x * 2
        # Width needed for each course name (may wrap to 2 lines)
        max_course_w = 0
        for c in courses:
            wrapped = wrap_text(c, font_text, 300)  # generous max for measurement
            for line in wrapped:
                w = measure_text(line, font_text) + padding_x * 2
                max_course_w = max(max_course_w, w)
        col_w = max(title_w, max_course_w, 180)
        col_w = min(col_w, 320)  # cap at 320px
        col_widths.append(col_w)

    # Total required width
    total_content_w = sum(col_widths) + gap * (len(col_widths) - 1)
    min_width = max(total_content_w + margin_x * 2, 1200)
    actual_width = max(width, min_width)

    # Scale column widths if total < available
    available = actual_width - margin_x * 2 - gap * (len(col_widths) - 1)
    if sum(col_widths) < available:
        # Distribute extra space proportionally
        scale = available / sum(col_widths)
        col_widths = [int(w * scale) for w in col_widths]

    # Calculate max text width per column (for wrapping)
    max_text_widths = [w - padding_x * 2 for w in col_widths]

    # Calculate column heights (accounting for wrapped text)
    col_heights = []
    for i, (cat_title, courses, _, _, desc) in enumerate(categories):
        total_lines = 0
        for c in courses:
            wrapped = wrap_text(c, font_text, max_text_widths[i])
            total_lines += len(wrapped)
        h = header_h + sub_header_h + total_lines * line_h + padding_bottom
        col_heights.append(h)

    max_col_h = max(col_heights)

    # --- Image dimensions ---
    title_area_h = 70
    overview_h = 50
    arrow_h = 25
    detail_area_h = max_col_h + 20
    annotation_h = 30
    total_height = title_area_h + overview_h + arrow_h + detail_area_h + annotation_h + 30

    # Create image
    img = Image.new("RGB", (actual_width, total_height), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    # === 1. Title Area ===
    title_y = 20
    draw.text((actual_width // 2, title_y),
              f"{major_name}（{level}）课程体系架构图",
              fill="#1a1a1a", font=font_title_large, anchor="mt")

    # Subtitle line
    draw.line([(margin_x, title_y + 40), (actual_width - margin_x, title_y + 40)],
              fill="#CCCCCC", width=1)

    # === 2. Overview Bar ===
    ov_y = title_y + 50
    ov_h = 36
    draw_rounded_rect(draw, (margin_x, ov_y, actual_width - margin_x, ov_y + ov_h),
                      fill="#F5F5F5", outline="#CCCCCC", radius=4)
    draw.text((actual_width // 2, ov_y + ov_h // 2),
              f"{major_name} 人才培养方案课程体系",
              fill="#444444", font=font_title, anchor="mm")

    # === 3. Arrow ===
    arrow_y = ov_y + ov_h + 2
    draw_arrow_down(draw, actual_width // 2, arrow_y, arrow_h - 2, color="#888888")

    # === 4. Category Boxes ===
    start_x = margin_x
    start_y = arrow_y + arrow_h + 5

    for i, (cat_title, courses, header_color, body_color, desc) in enumerate(categories):
        cx = start_x
        for j in range(i):
            cx += col_widths[j] + gap

        cw = col_widths[i]
        ch = col_heights[i]

        # Body background (extend to max height for alignment)
        draw_rounded_rect(draw, (cx, start_y, cx + cw, start_y + max_col_h),
                          fill=body_color, outline="#AAAAAA", radius=6)

        # Header
        draw_rounded_rect(draw, (cx, start_y, cx + cw, start_y + header_h),
                          fill=header_color, outline=header_color, radius=6)
        # Cover bottom corners of header
        draw.rectangle([cx + 1, start_y + header_h - 6, cx + cw - 1, start_y + header_h],
                       fill=header_color)
        # Title text (centered)
        draw.text((cx + cw // 2, start_y + header_h // 2),
                  cat_title, fill="white", font=font_title, anchor="mm")

        # Sub-header / description
        if desc:
            draw.text((cx + cw // 2, start_y + header_h + sub_header_h // 2),
                      desc, fill="#666666", font=font_small, anchor="mm")

        # Course items (with wrapping)
        item_y = start_y + header_h + sub_header_h + 6
        for c in courses:
            wrapped = wrap_text(c, font_text, max_text_widths[i])
            for line in wrapped:
                if item_y + line_h > start_y + max_col_h - 4:
                    break
                # Bullet point
                draw.text((cx + padding_x // 2, item_y), "·", fill="#888888", font=font_text)
                draw.text((cx + padding_x // 2 + 10, item_y), line,
                          fill="#333333", font=font_text)
                item_y += line_h

    # === 5. Bottom annotation ===
    ann_y = start_y + max_col_h + 10
    draw.text((actual_width // 2, ann_y),
              "注：课程体系依据《专业教学标准》与《职业分析报告》整合生成",
              fill="#999999", font=font_small, anchor="mt")

    # === 6. Course count summary ===
    total_courses = sum(len(c) for _, c, _, _, _ in categories)
    summary_y = ann_y + 18
    draw.text((actual_width // 2, summary_y),
              f"共 {len(categories)} 类 {total_courses} 门课程",
              fill="#AAAAAA", font=font_small, anchor="mt")

    # Save
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    img.save(output_path, "PNG", dpi=(150, 150))

    return {
        "output_path": output_path,
        "width": actual_width,
        "height": total_height,
        "categories": len(categories),
        "total_courses": total_courses,
    }


def main():
    parser = argparse.ArgumentParser(
        description="生成课程体系架构图 PNG"
    )
    parser.add_argument(
        "--data", required=True,
        help="课程数据 JSON 字符串或 JSON 文件路径"
    )
    parser.add_argument(
        "-o", "--output", default="curriculum_architecture.png",
        help="输出 PNG 文件路径（默认 curriculum_architecture.png）"
    )
    parser.add_argument(
        "--width", type=int, default=1400,
        help="图片最小宽度（默认 1400px，按需自动扩展）"
    )
    args = parser.parse_args()

    # Load data
    data = None
    if os.path.exists(args.data):
        with open(args.data, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError:
            result = {
                "status": "error",
                "message": "无法解析 --data 参数：既非文件路径也非合法 JSON 字符串",
            }
            print(json.dumps(result, ensure_ascii=False))
            sys.exit(1)

    if not isinstance(data, dict):
        result = {"status": "error", "message": "课程数据必须是 JSON 对象"}
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    try:
        info = generate_image(data, args.output, args.width)
        result = {
            "status": "success",
            "output_path": info["output_path"],
            "image_size": f"{info['width']}x{info['height']}",
            "categories": info["categories"],
            "total_courses": info["total_courses"],
        }
    except Exception as e:
        result = {"status": "error", "message": f"生成图片失败: {str(e)}"}
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
