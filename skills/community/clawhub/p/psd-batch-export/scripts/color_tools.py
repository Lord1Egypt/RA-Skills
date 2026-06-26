"""
智能配色工具 v1.0 — 色彩提取、配色推荐、对比度检查
=====================================================

用法:
  python color_tools.py --extract image.png          # 提取主色调
  python color_tools.py --palette 5 --base "#8B0000" # 生成5色调色板
  python color_tools.py --contrast "#FFF" "#8B0000"  # 检查对比度
  python color_tools.py --recommend ticket           # 按场景推荐配色
"""

import argparse
import colorsys
import math
from pathlib import Path
from PIL import Image

from console_utils import configure_stdio

configure_stdio()


# ═══════════════════════════════════════════════════════
# 色彩工具函数
# ═══════════════════════════════════════════════════════

def hex_to_rgb(hex_color: str) -> tuple:
    """#RRGGBB → (R, G, B)"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: tuple) -> str:
    """(R, G, B) → #RRGGBB"""
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"


def rgb_to_hsl(rgb: tuple) -> tuple:
    """RGB → HSL"""
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, s * 100, l * 100


def hsl_to_rgb(hsl: tuple) -> tuple:
    """HSL → RGB"""
    h, s, l = [x / 360.0 if i == 0 else x / 100.0 for i, x in enumerate(hsl)]
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return tuple(int(x * 255) for x in (r, g, b))


def relative_luminance(rgb: tuple) -> float:
    """WCAG 相对亮度"""
    def _channel(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * _channel(rgb[0]) + 0.7152 * _channel(rgb[1]) + 0.0722 * _channel(rgb[2])


def contrast_ratio(rgb1: tuple, rgb2: tuple) -> float:
    """WCAG 对比度"""
    l1 = relative_luminance(rgb1)
    l2 = relative_luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def wcag_level(ratio: float) -> str:
    """WCAG 等级"""
    if ratio >= 7:
        return "AAA ✅"
    elif ratio >= 4.5:
        return "AA  ✅"
    elif ratio >= 3:
        return "AA (大字体) ⚠️"
    else:
        return "不合格 ❌"


# ═══════════════════════════════════════════════════════
# 配色生成
# ═══════════════════════════════════════════════════════

def generate_palette(base_hex: str, count: int = 5) -> list:
    """基于一个基色生成调色板"""
    base_rgb = hex_to_rgb(base_hex)
    h, s, l = rgb_to_hsl(base_rgb)
    palette = []

    if count >= 5:
        # 互补色
        palette.append({"name": "主色", "hex": base_hex, "hsl": f"H{h:.0f} S{s:.0f} L{l:.0f}"})
        # 深色变体
        dark = hsl_to_rgb((h, s, max(l - 25, 5)))
        palette.append({"name": "深色", "hex": rgb_to_hex(dark), "hsl": f"H{h:.0f} S{s:.0f} L{max(l-25,5):.0f}"})
        # 浅色变体
        light = hsl_to_rgb((h, min(s * 0.5, 100), min(l + 30, 95)))
        palette.append({"name": "浅色", "hex": rgb_to_hex(light), "hsl": f"H{h:.0f} S{min(s*0.5,100):.0f} L{min(l+30,95):.0f}"})
        # 互补色
        comp_h = (h + 180) % 360
        comp = hsl_to_rgb((comp_h, s * 0.8, 50))
        palette.append({"name": "互补", "hex": rgb_to_hex(comp), "hsl": f"H{comp_h:.0f} S{s*0.8:.0f} L50"})
        # 类比色
        analog_h = (h + 30) % 360
        analog = hsl_to_rgb((analog_h, s, l))
        palette.append({"name": "类比", "hex": rgb_to_hex(analog), "hsl": f"H{analog_h:.0f} S{s:.0f} L{l:.0f}"})

    elif count == 3:
        palette.append({"name": "主色", "hex": base_hex, "hsl": f"H{h:.0f} S{s:.0f} L{l:.0f}"})
        dark = hsl_to_rgb((h, s, max(l - 20, 10)))
        palette.append({"name": "强调", "hex": rgb_to_hex(dark), "hsl": f"H{h:.0f} S{s:.0f} L{max(l-20,10):.0f}"})
        light = hsl_to_rgb((h, s * 0.4, min(l + 35, 95)))
        palette.append({"name": "背景", "hex": rgb_to_hex(light), "hsl": f"H{h:.0f} S{s*0.4:.0f} L{min(l+35,95):.0f}"})

    return palette


def generate_harmonious_palette(base_hex: str, scheme: str = "complementary") -> list:
    """生成和谐配色方案"""
    base_rgb = hex_to_rgb(base_hex)
    h, s, l = rgb_to_hsl(base_rgb)
    result = [{"name": "基色", "hex": base_hex}]

    if scheme == "complementary":
        for angle in [180]:
            nh = (h + angle) % 360
            result.append({"name": "互补色", "hex": rgb_to_hex(hsl_to_rgb((nh, s, l)))})

    elif scheme == "triadic":
        for angle in [120, 240]:
            nh = (h + angle) % 360
            result.append({"name": f"三角{angle}°", "hex": rgb_to_hex(hsl_to_rgb((nh, s, l)))})

    elif scheme == "analogous":
        for angle in [-30, 30]:
            nh = (h + angle) % 360
            result.append({"name": f"类比{angle}°", "hex": rgb_to_hex(hsl_to_rgb((nh, s, l)))})

    elif scheme == "monochromatic":
        for dl in [-20, -10, 10, 20]:
            nl = max(5, min(95, l + dl))
            result.append({"name": f"深浅{dl:+d}%", "hex": rgb_to_hex(hsl_to_rgb((h, s * 0.5, nl)))})

    return result


# ═══════════════════════════════════════════════════════
# 场景推荐
# ═══════════════════════════════════════════════════════

SCENE_RECOMMENDATIONS = {
    "ticket": {
        "name": "门票/入场券",
        "palettes": [
            {"name": "经典红金", "bg": "#8B0000", "accent": "#FFD700", "text": "#FFFFFF"},
            {"name": "深蓝金", "bg": "#1B2A4A", "accent": "#C5A55A", "text": "#FFFFFF"},
            {"name": "白底黑字", "bg": "#FFFFFF", "accent": "#2C3E50", "text": "#2C3E50"},
        ],
        "tip": "高对比度确保可读性，红色/蓝色系传达正式感。"
    },
    "certificate": {
        "name": "证书/奖状",
        "palettes": [
            {"name": "金色典雅", "bg": "#FFF8F0", "accent": "#8B6914", "text": "#3D2C2A"},
            {"name": "宝蓝金", "bg": "#0D1B2A", "accent": "#FFD700", "text": "#FFFFFF"},
            {"name": "墨绿金", "bg": "#F0F7F0", "accent": "#2D5A27", "text": "#1A3A1A"},
        ],
        "tip": "证书宜用暖色或金色系，传递荣誉与庄重感。"
    },
    "badge": {
        "name": "工牌/参会证",
        "palettes": [
            {"name": "科技蓝", "bg": "#0D1B2A", "accent": "#00D4FF", "text": "#FFFFFF"},
            {"name": "现代暗色", "bg": "#1A1A2E", "accent": "#E94560", "text": "#FFFFFF"},
            {"name": "清新白", "bg": "#FFFFFF", "accent": "#2C6BED", "text": "#2C3E50"},
        ],
        "tip": "工牌信息密度高，优先保证文字与背景的高对比度。"
    },
    "invitation": {
        "name": "邀请函",
        "palettes": [
            {"name": "皇家紫", "bg": "#2D1B4E", "accent": "#FFB347", "text": "#FFFFFF"},
            {"name": "玫瑰金", "bg": "#FFF5F0", "accent": "#E87461", "text": "#3D2C2A"},
            {"name": "深海蓝", "bg": "#0A1628", "accent": "#D4AF37", "text": "#FFFFFF"},
        ],
        "tip": "邀请函倾向优雅华丽配色，紫色/金色/玫瑰色系效果佳。"
    },
    "poster": {
        "name": "海报/宣传",
        "palettes": [
            {"name": "活力橙", "bg": "#1A1A2E", "accent": "#FF6B35", "text": "#FFFFFF"},
            {"name": "清新绿", "bg": "#F5FFF5", "accent": "#00A86B", "text": "#1A3A1A"},
            {"name": "大胆红", "bg": "#FFFFFF", "accent": "#E63946", "text": "#1D1D1D"},
        ],
        "tip": "海报需要强烈的视觉冲击力，高饱和互补色效果最佳。"
    },
}


# ═══════════════════════════════════════════════════════
# 图像主色提取
# ═══════════════════════════════════════════════════════

def extract_dominant_colors(image_path: Path, count: int = 5) -> list:
    """从图片提取主色调（基于量化）"""
    img = Image.open(image_path).convert("RGB")
    img = img.resize((150, 150))  # 缩小加速
    pixels = list(img.getdata())

    # 简单量化：按颜色频率排序
    from collections import Counter
    # 量化颜色到 32 级
    quantized = [(r // 32 * 32, g // 32 * 32, b // 32 * 32) for r, g, b in pixels]
    color_counts = Counter(quantized)
    dominant = color_counts.most_common(count)

    results = []
    for color, freq in dominant:
        pct = freq / len(pixels) * 100
        results.append({
            "hex": rgb_to_hex(color),
            "rgb": color,
            "coverage": round(pct, 1),
        })
    return results


# ═══════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════

def main():
    p = argparse.ArgumentParser(description="智能配色工具 — 色彩提取、推荐、对比度检查")
    p.add_argument("--extract", help="从图片提取主色调")
    p.add_argument("--palette", type=int, help="生成N色调色板")
    p.add_argument("--base", default="#8B0000", help="基色 (默认: #8B0000)")
    p.add_argument("--harmony", choices=["complementary", "triadic", "analogous", "monochromatic"],
                   help="生成和谐配色方案")
    p.add_argument("--contrast", nargs=2, metavar=("COLOR1", "COLOR2"), help="检查两色对比度")
    p.add_argument("--recommend", choices=list(SCENE_RECOMMENDATIONS.keys()),
                   help="按场景推荐配色")
    p.add_argument("--count", type=int, default=5, help="提取颜色数量")

    args = p.parse_args()

    if args.extract:
        colors = extract_dominant_colors(Path(args.extract), args.count)
        print(f"\n📸 主色调 ({Path(args.extract).name}):\n")
        for c in colors:
            bar = "█" * int(c["coverage"] // 5)
            print(f"  {c['hex']}  {bar} {c['coverage']}%")

    elif args.recommend:
        scene = SCENE_RECOMMENDATIONS[args.recommend]
        print(f"\n🎨 {scene['name']} 推荐配色:\n")
        for pn in scene["palettes"]:
            print(f"  {pn['name']}:  bg={pn['bg']} accent={pn['accent']} text={pn['text']}")
            # 检查对比度
            cr = contrast_ratio(hex_to_rgb(pn["text"]), hex_to_rgb(pn["bg"]))
            print(f"           文字/背景对比度: {cr:.1f}:1 {wcag_level(cr)}")
        print(f"\n  💡 {scene['tip']}")

    elif args.contrast:
        c1, c2 = args.contrast
        r1, r2 = hex_to_rgb(c1), hex_to_rgb(c2)
        cr = contrast_ratio(r1, r2)
        print(f"\n📐 对比度: {c1} vs {c2}")
        print(f"   比率: {cr:.2f}:1  ({wcag_level(cr)})")

    elif args.palette:
        palette = generate_palette(args.base, args.palette)
        print(f"\n🎨 基于 {args.base} 的 {args.palette} 色调色板:\n")
        for c in palette:
            bar = "████████"
            print(f"  {c['hex']}  {bar}  {c['name']:<6} ({c['hsl']})")

    elif args.harmony:
        result = generate_harmonious_palette(args.base, args.harmony)
        print(f"\n🌈 {args.harmony} 配色方案 (基色 {args.base}):\n")
        for c in result:
            print(f"  {c['hex']}  {c['name']}")

    else:
        p.print_help()


if __name__ == "__main__":
    main()
