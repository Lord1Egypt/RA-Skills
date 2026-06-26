"""
智能排版引擎 v1.0 — 自适应文字排布计算器
===========================================

根据画布尺寸和文字内容，自动计算最佳字号、位置、行距。

用法:
  python smart_layout.py --canvas 1748x2480 --texts "标题,副标题,正文" --analyze
  python smart_layout.py --preset ticket --data-field "姓名:张三" --calc
"""

import argparse
import math

from console_utils import configure_stdio

configure_stdio()


# ═══════════════════════════════════════════════════════
# 排版预设
# ═══════════════════════════════════════════════════════

PRESETS = {
    "ticket": {
        "canvas": (1748, 2480),
        "margin": 80,
        "elements": [
            {"role": "title", "y_pct": 0.08, "size_pct": 0.055, "align": "center"},
            {"role": "subtitle", "y_pct": 0.14, "size_pct": 0.025, "align": "center"},
            {"role": "info_label", "y_pct": 0.22, "size_pct": 0.028, "align": "left"},
            {"role": "info_value", "y_pct": 0.28, "size_pct": 0.035, "align": "left"},
        ]
    },
    "certificate": {
        "canvas": (2480, 1748),
        "margin": 120,
        "elements": [
            {"role": "title", "y_pct": 0.10, "size_pct": 0.070, "align": "center"},
            {"role": "body", "y_pct": 0.28, "size_pct": 0.032, "align": "center"},
            {"role": "recipient", "y_pct": 0.42, "size_pct": 0.045, "align": "center"},
            {"role": "date_sign", "y_pct": 0.78, "size_pct": 0.022, "align": "split"},
        ]
    },
    "badge": {
        "canvas": (1063, 1535),
        "margin": 40,
        "elements": [
            {"role": "org", "y_pct": 0.38, "size_pct": 0.030, "align": "center"},
            {"role": "name", "y_pct": 0.46, "size_pct": 0.065, "align": "center"},
            {"role": "role_title", "y_pct": 0.56, "size_pct": 0.032, "align": "center"},
        ]
    },
    "invitation": {
        "canvas": (1748, 2480),
        "margin": 100,
        "elements": [
            {"role": "decor", "y_pct": 0.06, "size_pct": 0.060, "align": "center"},
            {"role": "invite_label", "y_pct": 0.13, "size_pct": 0.025, "align": "center"},
            {"role": "event_name", "y_pct": 0.20, "size_pct": 0.052, "align": "center"},
            {"role": "details", "y_pct": 0.32, "size_pct": 0.030, "align": "center"},
        ]
    },
}


# ═══════════════════════════════════════════════════════
# 字号计算
# ═══════════════════════════════════════════════════════

def calc_font_size(canvas_w: int, canvas_h: int, text: str,
                   max_width_pct: float = 0.7, target_lines: int = 1,
                   char_width_ratio: float = 0.55) -> int:
    """
    根据画布宽度和文字内容计算最佳字号。
    char_width_ratio: 中文字符宽度 ≈ 字号 × 0.55（英文≈0.35）
    """
    available_w = int(canvas_w * max_width_pct)
    char_count = len(text)
    if char_count == 0:
        return 48

    # 单行模式下：字号 = 可用宽度 / (字符数 × 字符宽度比)
    size = available_w / (char_count * char_width_ratio) * target_lines
    size = int(size)
    # 限制范围
    size = max(12, min(size, canvas_h // 4))
    return size


def calc_text_bbox(text: str, font_size: int, char_width_ratio: float = 0.55) -> tuple:
    """估算文本区域宽度和高度"""
    tw = int(len(text) * font_size * char_width_ratio)
    th = int(font_size * 1.3)
    return tw, th


# ═══════════════════════════════════════════════════════
# 排版引擎
# ═══════════════════════════════════════════════════════

def layout_elements(canvas_w: int, canvas_h: int, elements: list,
                    margin: int = 80) -> list:
    """计算每个元素的精确位置和字号"""
    results = []
    available_w = canvas_w - 2 * margin

    for i, elem in enumerate(elements):
        role = elem["role"]
        y_pct = elem["y_pct"]
        size_pct = elem["size_pct"]
        align = elem["align"]

        # 计算字号（基于画布高度的百分比）
        font_size = int(canvas_h * size_pct)
        font_size = max(10, font_size)

        # 计算 y 坐标
        y = int(canvas_h * y_pct)

        # 计算 x 坐标
        if align == "center":
            x = canvas_w // 2
        elif align == "left":
            x = margin
        elif align == "right":
            x = canvas_w - margin
        else:
            x = margin

        results.append({
            "role": role,
            "x": x,
            "y": y,
            "font_size": font_size,
            "align": align,
            "max_width": available_w,
        })

    return results


def auto_layout(texts: list, canvas_w: int, canvas_h: int,
                margin: int = 80, vertical_spacing: float = 1.5) -> list:
    """
    自动排版：给定画布和文字列表，均匀分布并计算最优字号。
    
    返回: [{"text": str, "x": int, "y": int, "font_size": int, "align": str}, ...]
    """
    count = len(texts)
    if count == 0:
        return []

    available_h = canvas_h - 2 * margin
    # 为每个元素分配高度
    per_element_h = available_h / count
    # 字号不超过分配高度的 60%
    max_font = int(per_element_h * 0.6)

    results = []
    for i, text in enumerate(texts):
        # 计算适合宽度的字号
        fit_size = calc_font_size(canvas_w, canvas_h, text)
        font_size = min(fit_size, max_font, 120)
        font_size = max(font_size, 16)

        tw, th = calc_text_bbox(text, font_size)
        y_center = margin + int((i + 0.5) * per_element_h)
        y = y_center - th // 2
        x = (canvas_w - tw) // 2

        # 判断是否长文本需要换行
        lines_needed = math.ceil(tw / (canvas_w - 2 * margin)) if tw > canvas_w - 2 * margin else 1
        if lines_needed > 1:
            font_size = calc_font_size(canvas_w, canvas_h, text)
            tw, th = calc_text_bbox(text, font_size)

        results.append({
            "text": text,
            "x": x,
            "y": y,
            "font_size": font_size,
            "align": "center",
            "estimated_width": tw,
            "estimated_height": th,
            "lines": lines_needed,
        })

    return results


# ═══════════════════════════════════════════════════════
# 格式化输出
# ═══════════════════════════════════════════════════════

def print_layout(layout: list, canvas_w: int, canvas_h: int):
    """格式化打印排版方案"""
    print(f"\n📐 排版方案 ({canvas_w}×{canvas_h} px)")
    print(f"   {'─'*55}")
    print(f"   {'元素':<16} {'字号':>5} {'坐标':>16} {'对齐':>6} {'换行':>4}")
    print(f"   {'─'*55}")
    for elem in layout:
        text = elem.get("text", elem.get("role", "?"))[:14]
        size = elem["font_size"]
        if "x" in elem and "align" in elem:
            coord = f"({elem['x']},{elem['y']})"
            align = elem["align"]
        else:
            coord = f"({elem.get('x','?')},{elem.get('y','?')})"
            align = elem.get("align", "center")
        lines = elem.get("lines", 1)
        width = elem.get("estimated_width", "?")
        print(f"   {text:<16} {size:>4}pt {coord:>16} {align:>6} {lines:>3}行 (~{width}px)")
    print(f"   {'─'*55}\n")


# ═══════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════

def main():
    p = argparse.ArgumentParser(description="智能排版引擎 — 自适应文字排布")
    p.add_argument("--canvas", default="1748x2480", help="画布尺寸 WxH (默认: 1748x2480)")
    p.add_argument("--preset", choices=list(PRESETS.keys()), help="使用预设排版")
    p.add_argument("--texts", help="逗号分隔的文字列表 (用于自动排版)")
    p.add_argument("--margin", type=int, default=80, help="边距 (默认: 80px)")
    p.add_argument("--analyze", action="store_true", help="分析模式：展示详细计算过程")
    p.add_argument("--calc-size", help="计算指定文字的最佳字号")

    args = p.parse_args()

    w, h = map(int, args.canvas.split("x"))

    if args.calc_size:
        size = calc_font_size(w, h, args.calc_size)
        tw, th = calc_text_bbox(args.calc_size, size)
        print(f"\n📏 \"{args.calc_size}\" ({len(args.calc_size)}字)")
        print(f"   推荐字号: {size}pt")
        print(f"   估算宽度: {tw}px (可用: {int(w*0.7)}px)")
        print(f"   估算高度: {th}px")

    elif args.preset:
        preset = PRESETS[args.preset]
        pw, ph = preset["canvas"]
        pm = preset["margin"]
        layout = layout_elements(pw, ph, preset["elements"], pm)
        print(f"\n📋 预设: {args.preset} ({pw}×{ph}px, 边距{pm}px)")
        print_layout(layout, pw, ph)

    elif args.texts:
        texts = [t.strip() for t in args.texts.split(",")]
        layout = auto_layout(texts, w, h, args.margin)
        print_layout(layout, w, h)

        if args.analyze:
            print("📊 详细分析:")
            for elem in layout:
                text = elem["text"]
                print(f"   \"{text}\":")
                print(f"      字符数={len(text)}, 字号={elem['font_size']}pt, 行数={elem['lines']}")
                tw, th = calc_text_bbox(text, elem["font_size"])
                overflow = "⚠ 可能超出" if tw > w - 2 * args.margin else "✅ 宽度合适"
                print(f"      估算尺寸={tw}×{th}px  {overflow}\n")

    else:
        p.print_help()


if __name__ == "__main__":
    main()
