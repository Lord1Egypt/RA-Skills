# -*- coding: utf-8 -*-
"""按杖特画一张扁平风魔杖插画（卡片内嵌用）。

用法：
    python make_wand_art.py                                  # 橡木·炉心泥·11½·微韧（默认）
    python make_wand_art.py --wood 紫杉 --core 雾露晶 --flex 挺韧 --seed 12
    python make_wand_art.py --out 某路径.png

设计口径：
- 扁平矢量风，3:2 横版，暖白底，与卡片同色系（紫 #5A4AA3 / 金 #854F0B / 木棕 / 羊皮纸）
- 构图：杖身自左下向右上斜放，杖尖在右上带星芒
- 画面直接印杖的特性：杖名、树籍、木/芯/长/韧四行，以及杖芯色标
  —— 木色、芯色、缠绕纹圈数、星点位置都由「杖特 + seed」决定，
     同一根杖永远同一张图（确定性），不同杖必然不同图

依赖：Pillow（建议用隔离环境 C:\\Users\\yangduo\\.workbuddy\\binaries\\python\\envs\\default）
"""

import argparse
import json
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

S = 2                        # 超采样倍数
OUT_W, OUT_H = 1000, 656     # 3:2 出图尺寸（比卡片原 900×600 更醒目）

BG      = (255, 253, 248)
CREAM   = (248, 242, 230)
PARCH   = (238, 228, 209)
GOLD    = (201, 168, 92)
GOLD_DK = (133, 79, 11)
PURPLE  = (90, 74, 163)
INK     = (58, 51, 85)
MUTED   = (138, 128, 116)
WHITE   = (255, 255, 255)
HILITE  = (255, 250, 238)

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\simsun.ttc",
]

WOOD_HEX = {
    "橡木": "#A9784B", "山楂木": "#B08258", "桦木": "#D8C39E", "紫杉": "#6E4A4A",
    "樱桃木": "#B4664A", "胡桃木": "#7B5230", "白蜡木": "#CDB183", "枫木": "#C08F5A",
}

# 杖芯色标（本 Skill 的杖芯色 = 材料情绪色，与卡片配色同族）
CORE_RGB = {
    "星陨砂": (142, 124, 216),   # 夜紫
    "萤火绒": (232, 197, 106),   # 暖金
    "雷纹羽": (110, 116, 200),   # 电蓝紫
    "潮汐珠": (78, 147, 184),    # 海青
    "炉心泥": (193, 107, 74),    # 窑火橙
    "雾露晶": (159, 182, 216),   # 雾蓝
}

LEN_INCH = {"沉静型": ("10¼", 10.25), "均衡型": ("11½", 11.5), "丰盛型": ("13½", 13.5)}

FLEX_TXT = {
    "轻盈": "打断来了先退一步，退完发现路还在",
    "微韧": "弯而不折，有底线",
    "挺韧": "顶得住，不绕路",
    "坚硬": "宁折不弯，认死理但纯粹",
}


def font(size):
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def shade(rgb, k):
    return tuple(max(0, min(255, int(c * k))) for c in rgb)


def draw_star(d, cx, cy, r, col):
    d.polygon([(cx, cy - r), (cx + r * 0.26, cy - r * 0.26), (cx + r, cy),
               (cx + r * 0.26, cy + r * 0.26), (cx, cy + r),
               (cx - r * 0.26, cy + r * 0.26), (cx - r, cy),
               (cx - r * 0.26, cy - r * 0.26)], fill=col)


def draw_wand(d, wood_rgb, core_rgb, rnd):
    """斜放的魔杖：杖身（含体积明暗）+ 握把缠线 + 螺旋纹（每根条数不同）+ 心材线 + 杖尖星芒。"""
    x0, y0 = 90 * S, 600 * S
    x1, y1 = 905 * S, 128 * S
    light = wood_rgb
    dark = shade(wood_rgb, 0.60)
    deep = shade(wood_rgb, 0.42)

    steps = 380
    w_tail, w_tip = 19.0 * S, 6.0 * S
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t + math.sin(t * 3.1) * 6 * S
        w = w_tail + (w_tip - w_tail) * t
        pts.append((x, y, w))

    # 杖身主体 + 下缘暗面 + 上缘高光（错位叠圆，做出圆柱感）
    for (x, y, w) in pts:
        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=light)
    for (x, y, w) in pts:
        d.ellipse([x - w / 2, y + w * 0.26 - w / 2, x + w / 2, y + w * 0.26 + w / 2], fill=dark)
    for i, (x, y, w) in enumerate(pts):
        if i % 2:
            continue
        hw = w * 0.36
        d.ellipse([x - hw / 2, y - w * 0.32 - hw / 2, x + hw / 2, y - w * 0.32 + hw / 2], fill=HILITE)

    ang = math.atan2(y1 - y0, x1 - x0) + math.pi / 2

    # 螺旋缠绕纹：条数、相位、幅度都随杖变
    coils = rnd.randint(12, 20)
    phase = rnd.random() * math.pi
    swing = rnd.choice([26, 34, 42])
    for k in range(coils):
        t = 0.09 + 0.84 * (k / max(1, coils - 1))
        x, y, w = pts[int(t * steps)]
        r = w * 0.66
        a0 = math.degrees(ang) + 18 + swing * math.sin(phase + k * 0.9)
        d.arc([x - r, y - r, x + r, y + r], int(a0), int(a0 + 128),
              fill=deep, width=max(1, int(1.7 * S)))

    # 握把缠线（紫，呼应卡片主色）
    g0, g1 = int(steps * 0.07), int(steps * 0.33)
    for i in range(g0, g1, 3):
        x, y, w = pts[i]
        r = w * 0.74
        d.arc([x - r, y - r, x + r, y + r],
              int(math.degrees(ang) - 10), int(math.degrees(ang) + 190),
              fill=PURPLE, width=max(1, int(2.0 * S)))
    xg, yg, wg = pts[g1]
    d.ellipse([xg - wg * 0.46, yg - wg * 0.46, xg + wg * 0.46, yg + wg * 0.46], fill=PURPLE)

    # 心材线：杖芯色沿中轴露出一线
    for i in range(int(steps * 0.16), int(steps * 0.975), 2):
        x, y, w = pts[i]
        ww = max(1.3 * S, w * 0.19)
        d.ellipse([x - ww / 2, y - ww / 2, x + ww / 2, y + ww / 2], fill=core_rgb)

    # 杖尖：亮头 + 星芒（四长四短，点端加粗，保证小图下也清晰）
    xt, yt, wt = pts[-1]
    for (r, col) in [(wt * 1.6, core_rgb), (wt * 0.9, HILITE)]:
        d.ellipse([xt - r, yt - r, xt + r, yt + r], fill=col)
    rays = [(1, 0, 72 * S), (0.87, 0.5, 46 * S), (0.5, 0.87, 34 * S), (0, 1, 30 * S),
            (-0.5, 0.87, 28 * S), (-0.87, 0.5, 24 * S), (-0.87, -0.5, 28 * S), (-0.5, -0.87, 32 * S),
            (0, -1, 40 * S), (0.5, -0.87, 46 * S), (0.87, -0.5, 56 * S)]
    for (dx, dy, ln) in rays:
        ex, ey = xt + dx * ln, yt + dy * ln
        d.line([xt, yt, ex, ey], fill=GOLD, width=max(1, int(2.6 * S)))
        r2 = 4.0 * S
        d.ellipse([ex - r2, ey - r2, ex + r2, ey + r2], fill=GOLD)


def render(cfg, out_path):
    rnd = random.Random(cfg["seed"])
    W, H = OUT_W * S, OUT_H * S
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # 顶部浅色带 + 店招
    d.rectangle([0, 0, W, 104 * S], fill=CREAM)
    d.text((46 * S, 26 * S), cfg["shop_name"], font=font(24 * S), fill=GOLD_DK)
    d.text((46 * S, 58 * S), "它选了你", font=font(32 * S), fill=INK)

    # 右上角三格色卡（木浅 / 木深 / 芯色）
    wood_rgb = hex2rgb(cfg["wood_hex"])
    core_rgb = cfg["core_rgb"]
    for i, c in enumerate([wood_rgb, shade(wood_rgb, 0.6), core_rgb]):
        x = W - (46 + 150 - i * 46) * S
        d.rounded_rectangle([x, 32 * S, x + 34 * S, 72 * S], radius=9 * S, fill=c)

    draw_wand(d, wood_rgb, core_rgb, rnd)

    for _ in range(rnd.randint(4, 7)):
        sx = rnd.randint(int(470 * S), int(930 * S))
        sy = rnd.randint(int(120 * S), int(330 * S))
        draw_star(d, sx, sy, rnd.choice([5, 7, 9]) * S, GOLD)

    # 特性面板（下方横排，全宽，标题一行放得下）
    pw, ph = W - 88 * S, 236 * S
    px, py = 44 * S, H - ph - 36 * S
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=20 * S,
                        fill=WHITE, outline=PARCH, width=max(1, int(2 * S)))
    d.rounded_rectangle([px, py, px + 10 * S, py + ph], radius=5 * S, fill=GOLD)

    tx, ty = px + 34 * S, py + 22 * S
    d.text((tx, ty), cfg["wand_name"], font=font(38 * S), fill=INK)
    ty += 52 * S
    d.text((tx, ty), cfg["grove_line"], font=font(20 * S), fill=GOLD_DK)
    ty += 36 * S
    d.line([tx, ty, px + pw - 34 * S, ty], fill=PARCH, width=max(1, int(2 * S)))
    ty += 16 * S
    d.text((tx, ty), cfg["specs"][0], font=font(21 * S), fill=INK)   # 芯·长·韧 一行
    # 芯色标 + 来历（第二行）
    ty += 40 * S
    d.rounded_rectangle([tx, ty, tx + 96 * S, ty + 20 * S], radius=10 * S, fill=core_rgb)
    d.text((tx + 112 * S, ty - 2 * S), cfg["core_label"], font=font(18 * S), fill=MUTED)

    d.text((46 * S, H - 46 * S), cfg["declaration"], font=font(15 * S), fill=MUTED)

    img = img.resize((OUT_W, OUT_H), Image.LANCZOS)
    if out_path.lower().endswith((".jpg", ".jpeg")):
        img.save(out_path, "JPEG", quality=88, optimize=True)
    else:
        img.save(out_path, "PNG", optimize=True)
    return out_path


def build_cfg(wood, core, len_name, flex, seed):
    woods = json.load(open(os.path.join(DATA, "woods.json"), encoding="utf-8"))["woods"]
    cores = json.load(open(os.path.join(DATA, "cores.json"), encoding="utf-8"))["cores"]
    meta = json.load(open(os.path.join(DATA, "meta.json"), encoding="utf-8"))
    wo = next(w for w in woods if w["name"] == wood)
    co = next(c for c in cores if c["name"] == core)
    frac = LEN_INCH.get(len_name, ("11½", 11.5))[0]
    return {
        "seed": seed,
        "shop_name": meta["shop_name"],
        "declaration": meta["declaration"],
        "wood_hex": wo.get("hex") or WOOD_HEX.get(wood, "#A9784B"),
        "core_rgb": CORE_RGB.get(core, WOOD_HEX and (142, 124, 216)),
        "wand_name": f"{wood} · {core} · {frac} 英寸 · {flex}",
        "grove_line": f"{wo['grove']} · {wo['grove_line']}",
        "specs": [
            f"芯 · {core}（{co['drive']}）　　长 · {frac} 英寸 · {len_name}　　韧 · {flex}",
        ],
        "core_label": co["origin"].split("，")[0][:22],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wood", default="橡木")
    ap.add_argument("--core", default="炉心泥")
    ap.add_argument("--len", dest="len_name", default="均衡型")
    ap.add_argument("--flex", default="微韧")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    seed = a.seed or (abs(hash((a.wood, a.core, a.len_name, a.flex))) % 9999 + 1)
    cfg = build_cfg(a.wood, a.core, a.len_name, a.flex, seed)
    out = a.out or os.path.join(ROOT, "assets", "preview_wand.png")
    render(cfg, out)
    print("已生成", out, os.path.getsize(out), "bytes")
    print("·", cfg["wand_name"], "| seed", seed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
