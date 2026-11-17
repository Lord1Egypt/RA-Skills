#!/usr/bin/env python3
"""从单个主色 hex 派生全套 OpenClaw 主题 CSS 变量（HSL 偏移法）

用法：
  python3 derive-palette.py <hex>           # 深色主题（默认）
  python3 derive-palette.py <hex> --light   # 浅色主题（亮度反转）
"""

import argparse
import colorsys
import re

HEX_RE = re.compile(r"^[0-9a-fA-F]{6}$")


def hex_error(c: str):
    """校验颜色格式，返回中文错误原因；合法返回 None。"""
    if not isinstance(c, str) or not c.startswith("#"):
        return '缺少 "#" 前缀（如 #7ca843）'
    body = c[1:]
    if len(body) == 3 and re.fullmatch(r"[0-9a-fA-F]{3}", body):
        return "3 位简写不支持，请写成 6 位完整形式（如 #a8c → #aa88cc）"
    if not HEX_RE.fullmatch(body):
        return '不是 "# + 6 位十六进制" 格式（如 #7ca843）'
    return None


def parse_hex(c: str):
    """合法 hex → (r, g, b) 归一化浮点"""
    return (
        int(c[1:3], 16) / 255,
        int(c[3:5], 16) / 255,
        int(c[5:7], 16) / 255,
    )


def relative_luminance(rgb: tuple) -> float:
    """WCAG 相对亮度（rgb 为 0-1 浮点）"""
    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast_ratio(lum1: float, lum2: float) -> float:
    """两相对亮度 → WCAG 对比度"""
    lighter, darker = max(lum1, lum2), min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)


# border 类对比度目标：WCAG 非文字 UI 组件 ≥ 3:1。留余量且保持
# border < border-strong < border-hover 的视觉层级，不刺眼。
BORDER_TARGET = 3.2
BORDER_STRONG_TARGET = 4.2
BORDER_HOVER_TARGET = 5.5


def border_color(hue: float, sat: float, bg_hex: str, target: float,
                 light: bool = False) -> str:
    """同色相/同饱和度下二分找亮度，让 border 对 bg 的对比度 ≈ target。

    HSL 亮度单调决定 WCAG 相对亮度，故二分必收敛：
    - 深色模式：亮度越高对比度越高，从下界往上搜；
    - 浅色模式：亮度越高对比度越低，从上界往下搜。
    保证任意色相派生 border 都稳定过 ≥ 3:1（UI 组件），且贴着目标不刺眼。
    """
    bg_lum = relative_luminance(parse_hex(bg_hex))
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lum = relative_luminance(colorsys.hls_to_rgb(hue % 360, mid, sat))
        ratio = contrast_ratio(lum, bg_lum)
        if (ratio < target) != light:   # 深色：ratio 不足 → 升亮度；浅色：ratio 不足 → 降亮度
            lo = mid
        else:
            hi = mid
    rgb = colorsys.hls_to_rgb(hue % 360, (lo + hi) / 2, sat)
    return f"#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}"


def derive_palette(hex_color: str, light: bool = False) -> dict:
    """输入主色 hex（如 #7ca843），输出全套 :root CSS 变量。

    light=True：亮度反转——色相/饱和度不变、亮度 l → 1-l（背景转浅、文字转深）；
    例外：主色 --accent 保持原值、--accent-foreground 保持深色（浅色模式下
    强调色仍是中亮度，深字对比度才 ≥ 4.5:1）、--accent-glow 保持 rgba、
    border 类不按反转走（见下）。

    border 类单独处理：以最终 --bg 为基准二分对齐对比度目标
    （--border ≥3.2 / --border-strong ≥4.2 / --border-hover ≥5.5，
    见 border_color），保证两种模式都过必查配对清单的 UI 组件 ≥3:1。
    """
    r, g, b = parse_hex(hex_color)
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    def hsl(hue, sat, lit):
        rgb = colorsys.hls_to_rgb(hue % 360, lit, sat)
        return f"#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}"

    def invert_l(hexv: str) -> str:
        rr, gg, bb = parse_hex(hexv)
        hh, ll, ss = colorsys.rgb_to_hls(rr, gg, bb)
        return hsl(hh, ss, 1 - ll)

    bg_dark = hsl(h, 0.15, 0.06)
    bg_final = invert_l(bg_dark) if light else bg_dark

    palette = {
        '--bg':               bg_final,
        '--bg-elevated':      hsl(h, 0.12, 0.09),
        '--bg-muted':         hsl(h, 0.10, 0.11),
        '--bg-content':       hsl(h, 0.15, 0.05),
        '--bg-hover':         hsl(h, 0.12, 0.12),
        '--card':             hsl(h, 0.08, 0.08),
        '--card-foreground':  hsl(h, 0.08, 0.92),
        '--chat-text':        hsl(h, 0.08, 0.92),
        '--chat-box-inset':   hsl(h, 0.15, 0.04),
        '--border':           border_color(h, 0.20, bg_final, BORDER_TARGET, light),
        '--border-hover':     border_color(h, 0.50, bg_final, BORDER_HOVER_TARGET, light),
        '--border-strong':    border_color(h, 0.25, bg_final, BORDER_STRONG_TARGET, light),
        '--accent':           hex_color,
        '--accent-hover':     hsl(h, 0.55, 0.52),
        '--accent-muted':     hsl(h, 0.35, 0.38),
        '--accent-foreground': hsl(h, 0.10, 0.06),
        '--accent-glow':      f"rgba({int(r*255)},{int(g*255)},{int(b*255)},.4)",
        '--accent-2':         hsl(h + 30, 0.30, 0.35),
        '--accent-2-muted':   hsl(h + 30, 0.25, 0.28),
        '--accent-2-subtle':  hsl(h + 30, 0.15, 0.14),
    }

    if light:
        keep = {'--bg', '--accent', '--accent-foreground', '--accent-glow',
                '--border', '--border-hover', '--border-strong'}

        for var, val in palette.items():
            if var in keep or not val.startswith('#'):
                continue
            palette[var] = invert_l(val)

    return palette


def print_css(palette: dict, light: bool = False):
    if light:
        print("/* light 模式：亮度反转派生（背景转浅、文字转深、主色不变）；"
              "改完必须跑 contrast-check.py 必查配对清单 */")
    print(":root {")
    for var, val in palette.items():
        print(f"  {var}: {val} !important;")
    print("}")


def main():
    parser = argparse.ArgumentParser(
        description="从单个主色 hex 派生全套 OpenClaw 主题 CSS 变量（默认深色，--light 浅色亮度反转）",
        epilog="示例：python3 derive-palette.py '#7ca843'  |  "
               "python3 derive-palette.py '#7ca843' --light",
    )
    parser.add_argument("hex_color",
                        help="主色，格式必须 # + 6 位十六进制（如 #7ca843）")
    parser.add_argument("--light", action="store_true",
                        help="浅色模式：亮度反转（背景转浅、文字转深；主色、强调色上文字、辉光不变）")
    args = parser.parse_args()

    err = hex_error(args.hex_color)
    if err:
        parser.error(f"非法颜色值 {args.hex_color!r}：{err}")

    palette = derive_palette(args.hex_color, light=args.light)
    print_css(palette, light=args.light)


if __name__ == "__main__":
    main()
