#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WB-SAFE 专家团头像离线生成器（纯本地 PIL，零积分、无网络调用）。

用法：python3 scripts/gen_avatars.py [输出目录]
默认输出 ../avatars/，生成 10 张 512x512 PNG。
风格锚定 categoryId=11-SecurityCompliance：深靛蓝底 + 盾形水印 + 银环 + accent 弧 + 缩写字标。
与 MX-OPS（deep teal）刻意区分开，一眼能分辨是"安全团"。
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

SIZE = 512
SS = 4  # 超采样倍率：先画 2048 再缩小做抗锯齿
C = SIZE * SS

BG_INNER = (30, 62, 108)   # 中心亮靛蓝
BG_OUTER = (8, 16, 34)     # 边缘近黑蓝
SILVER = (201, 214, 223)

FONT_DIRS = ["C:/Windows/Fonts", "/usr/share/fonts", os.path.expanduser("~/.fonts")]
BOLD_CANDIDATES = ["arialbd.ttf", "ARIALBD.TTF", "DejaVuSans-Bold.ttf", "seguisb.ttf"]
REG_CANDIDATES = ["arial.ttf", "ARIAL.TTF", "DejaVuSans.ttf", "segoeui.ttf"]

# id -> (缩写, 底部标签, accent 色)
SPEC = {
    "team":                ("SAFE", "WB-SAFE TEAM", (224, 179, 106)),
    "wb-safe-lead":        ("GOV",  "SAFE LEAD",    (224, 179, 106)),
    "wb-cred-guard":       ("KEY",  "CREDENTIAL",   (228, 87, 46)),
    "wb-credit-steward":   ("CR",   "CREDITS",      (127, 176, 105)),
    "wb-link-monitor":     ("NET",  "CONNECTIVITY", (78, 205, 196)),
    "wb-config-auditor":   ("CFG",  "CONFIG AUDIT", (90, 169, 230)),
    "wb-crypto-keeper":    ("ENC",  "CRYPTO KEYS",  (176, 139, 187)),
    "wb-health-sentinel":  ("HP",   "HEALTH",       (232, 117, 154)),
    "wb-risk-planner":     ("RSK",  "RISK PLAN",    (242, 166, 90)),
    "wb-recovery-keeper":  ("RCV",  "RECOVERY",     (201, 214, 223)),
}


def find_font(candidates):
    for d in FONT_DIRS:
        for name in candidates:
            p = os.path.join(d, name)
            if os.path.isfile(p):
                return p
    return None


def radial_bg(size):
    """小画布画径向渐变再放大，比画上千个同心圆快得多。"""
    n = 192
    small = Image.new("RGB", (n, n))
    d = ImageDraw.Draw(small)
    cx, cy = n / 2, n * 0.42          # 光心略偏上，更像受光体
    maxr = (n ** 2 * 0.5) ** 0.5
    for r in range(int(maxr), 0, -1):
        t = min(1.0, r / maxr) ** 0.9
        col = tuple(int(BG_INNER[i] + (BG_OUTER[i] - BG_INNER[i]) * t) for i in range(3))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    return small.resize((size, size), Image.LANCZOS)


def draw_spaced(draw, text, font, cx, cy, fill, spacing):
    """手动字距绘制并整体居中。"""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    bb = draw.textbbox((0, 0), text, font=font)
    x = cx - total / 2
    y = cy - (bb[3] + bb[1]) / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + spacing


def fit_font(draw, text, path, target_w, max_size=None, spacing_ratio=0.06):
    """二分找到让文字宽度贴合 target_w（且不超 max_size）的字号。"""
    lo = 20
    hi = int(max_size) if max_size else int(C * 0.6)
    best = lo
    while lo <= hi:
        mid = (lo + hi) // 2
        f = ImageFont.truetype(path, mid)
        w = sum(draw.textlength(ch, font=f) for ch in text) + mid * spacing_ratio * (len(text) - 1)
        if w <= target_w:
            best, lo = mid, mid + 1
        else:
            hi = mid - 1
    return ImageFont.truetype(path, best)


def shield_points(m):
    """盾形轮廓（上宽下收尖），作为"防护"语义的淡水印。"""
    pts = [(0.265, 0.245), (0.5, 0.165), (0.735, 0.245),
           (0.735, 0.535), (0.655, 0.700), (0.5, 0.815),
           (0.345, 0.700), (0.265, 0.535)]
    return [(x * 512 * m, y * 512 * m) for x, y in pts]


def make_avatar(abbr, label, accent, bold_path, reg_path):
    img = radial_bg(C).convert("RGBA")
    d = ImageDraw.Draw(img)
    m = C / 512.0  # 相对 512 的比例尺

    # 盾形水印（先画，压在文字之下）
    d.polygon(shield_points(m), outline=SILVER + (58,), width=int(3 * m))

    # 外银环
    d.ellipse([28 * m, 28 * m, C - 28 * m, C - 28 * m],
              outline=SILVER + (110,), width=int(3 * m))
    # accent 弧：上半 140°（与 MX-OPS 的右下弧刻意错开）
    d.arc([28 * m, 28 * m, C - 28 * m, C - 28 * m],
          start=200, end=340, fill=accent + (255,), width=int(9 * m))
    # 内侧细弧（银），构成"守卫徽章"层次
    d.arc([58 * m, 58 * m, C - 58 * m, C - 58 * m],
          start=25, end=155, fill=SILVER + (75,), width=int(2 * m))

    # 中央缩写
    tw = {2: 0.40, 3: 0.50}.get(len(abbr), 0.58)
    f_abbr = fit_font(d, abbr, bold_path, C * tw)
    draw_spaced(d, abbr, f_abbr, C / 2, C * 0.445, (255, 255, 255, 250),
                f_abbr.size * 0.06)

    # 缩写下的 accent 短横
    bar_w = C * 0.19
    d.rounded_rectangle([C / 2 - bar_w / 2, C * 0.585, C / 2 + bar_w / 2, C * 0.585 + 7 * m],
                        radius=4 * m, fill=accent + (235,))

    # 底部英文标签（长标签自动缩字号，避免溢出）
    f_lab = fit_font(d, label, reg_path, C * 0.62, max_size=34 * m, spacing_ratio=0.13)
    draw_spaced(d, label, f_lab, C / 2, C * 0.700, SILVER + (215,), f_lab.size * 0.13)

    return img.resize((SIZE, SIZE), Image.LANCZOS).convert("RGB")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "avatars")
    out = os.path.abspath(out)
    os.makedirs(out, exist_ok=True)

    bold_path, reg_path = find_font(BOLD_CANDIDATES), find_font(REG_CANDIDATES)
    if not bold_path or not reg_path:
        sys.exit("未找到可用字体，请检查 FONT_DIRS")

    for key, (abbr, label, accent) in SPEC.items():
        img = make_avatar(abbr, label, accent, bold_path, reg_path)
        path = os.path.join(out, key + ".png")
        img.save(path, "PNG", optimize=True)
        print("%-30s %6.1f KB" % (key + ".png", os.path.getsize(path) / 1024))
    print("\n完成：%d 张 -> %s（零积分，纯本地 PIL）" % (len(SPEC), out))


if __name__ == "__main__":
    main()
