#!/usr/bin/env python3
"""Render a resume review as a retro Japanese manga stat-sheet poster."""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1600
PAPER = (244, 236, 212)
INK = (19, 18, 20)
RED = (190, 34, 45)
WHITE = (255, 252, 240)
GRAY = (122, 116, 109)
LIGHT = (221, 210, 190)

FONT_CANDIDATES = {
    "darwin": [
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/Songti.ttc",
    ],
    "win32": [
        r"C:\Windows\Fonts\msyhbd.ttc",
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
    ],
    "linux": [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    ],
}

RATING_BANDS = [(90, "A"), (75, "B"), (60, "C"), (45, "D"), (0, "E")]


def find_font(explicit: str | None) -> str:
    if explicit and Path(explicit).exists():
        return explicit
    for candidate in FONT_CANDIDATES.get(sys.platform, FONT_CANDIDATES["linux"]):
        if Path(candidate).exists():
            return candidate
    raise SystemExit("找不到中文字体,请使用 --font /path/to/font.ttf")


def font(path: str, size: int, index: int = 0):
    return ImageFont.truetype(path, size, index=index)


def grade(score: float) -> str:
    for threshold, value in RATING_BANDS:
        if score >= threshold:
            return value
    return "E"


def dimension_grade(score: float, maximum: float) -> str:
    return grade(score / max(1.0, maximum) * 100.0)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, width: int) -> list[str]:
    lines, current = [], ""
    for char in text:
        if char == "\n":
            lines.append(current)
            current = ""
            continue
        trial = current + char
        if not current or draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            lines.append(current)
            current = char
    if current:
        lines.append(current)
    return lines or [""]


def point(cx: float, cy: float, radius: float, index: int) -> tuple[float, float]:
    angle = math.radians(-90 + index * 60)
    return cx + radius * math.cos(angle), cy + radius * math.sin(angle)


def polygon_points(cx: float, cy: float, radius: float) -> list[tuple[float, float]]:
    return [point(cx, cy, radius, i) for i in range(6)]


def fit_text(draw: ImageDraw.ImageDraw, text: str, path: str, start: int,
             minimum: int, max_width: int):
    size = start
    while size >= minimum:
        candidate = font(path, size)
        if draw.textlength(text, font=candidate) <= max_width:
            return candidate
        size -= 2
    return font(path, minimum)


def add_print_texture(img: Image.Image) -> None:
    rng = random.Random(260816)
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    # Paper grain.
    for _ in range(16000):
        x, y = rng.randrange(W), rng.randrange(H)
        alpha = rng.randrange(5, 16)
        color = (20, 18, 20, alpha) if rng.random() < 0.62 else (255, 255, 255, alpha)
        draw.point((x, y), fill=color)
    # Halftone discs on the right edge.
    for y in range(125, 515, 16):
        for x in range(920, 1200, 16):
            d = math.hypot(x - 1090, y - 300)
            if d < 245:
                radius = max(1, int(4 * (1 - d / 245)))
                draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(20, 18, 20, 42))
    img.alpha_composite(overlay)


def rough_line(draw: ImageDraw.ImageDraw, points, fill=INK, width=4, seed=0) -> None:
    rng = random.Random(seed)
    draw.line(points, fill=fill, width=width)
    shifted = [(x + rng.choice((-1, 0, 1)), y + rng.choice((-1, 0, 1))) for x, y in points]
    draw.line(shifted, fill=fill, width=max(1, width // 2))


def draw_speed_lines(draw: ImageDraw.ImageDraw) -> None:
    origin = (1040, 610)
    for i in range(34):
        angle = math.radians(145 + i * 3.0)
        inner = 270 + (i % 4) * 14
        outer = 560 + (i % 3) * 28
        x1 = origin[0] + math.cos(angle) * inner
        y1 = origin[1] + math.sin(angle) * inner
        x2 = origin[0] + math.cos(angle) * outer
        y2 = origin[1] + math.sin(angle) * outer
        draw.line((x1, y1, x2, y2), fill=(171, 160, 145), width=1 + i % 2)


def draw_radar(img: Image.Image, cx: int, cy: int, radius: int,
               dimensions: list[dict], fnt_path: str) -> None:
    draw = ImageDraw.Draw(img)
    draw.polygon([(cx - 330, cy - 285), (cx + 315, cy - 285),
                  (cx + 355, cy + 320), (cx - 355, cy + 320)],
                 fill=WHITE, outline=INK, width=7)
    # Offset black frame gives a misregistered print feel.
    draw.line((cx - 342, cy - 271, cx - 370, cy + 310), fill=RED, width=9)
    draw.line((cx + 330, cy - 271, cx + 368, cy + 310), fill=RED, width=9)

    for fraction, width in ((1.0, 6), (0.75, 2), (0.5, 2), (0.25, 2)):
        draw.polygon(polygon_points(cx, cy, radius * fraction), outline=INK, width=width)
    outer = polygon_points(cx, cy, radius)
    for x, y in outer:
        rough_line(draw, [(cx, cy), (x, y)], fill=GRAY, width=2, seed=int(x + y))

    ratios = [max(0.04, min(1.0, d["score"] / max(1, d["max"]))) for d in dimensions]
    values = [point(cx, cy, radius * ratios[i], i) for i in range(6)]
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    # Diagonal hatch inside data polygon.
    ld.polygon(values, fill=(190, 34, 45, 80), outline=(190, 34, 45, 255), width=7)
    mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(mask)
    md.polygon(values, fill=255)
    hatch = Image.new("RGBA", img.size, (0, 0, 0, 0))
    hd = ImageDraw.Draw(hatch)
    for x in range(-H, W, 17):
        hd.line((x, 0, x + H, H), fill=(190, 34, 45, 75), width=3)
    layer.alpha_composite(Image.composite(hatch, Image.new("RGBA", img.size), mask))
    for x, y in values:
        ld.ellipse((x - 11, y - 11, x + 11, y + 11), fill=RED, outline=INK, width=3)
    img.alpha_composite(layer)
    draw = ImageDraw.Draw(img)

    # Keep captions close to their corresponding vertices so the mapping is obvious.
    # The small gap preserves the chart silhouette without making labels float away.
    anchors = [
        (cx, cy - radius - 45, "center"),
        (cx + radius + 24, cy - radius // 2 - 26, "left"),
        (cx + radius + 24, cy + radius // 2 - 26, "left"),
        (cx, cy + radius + 24, "center"),
        (cx - radius - 24, cy + radius // 2 - 26, "right"),
        (cx - radius - 24, cy - radius // 2 - 26, "right"),
    ]
    label_font = font(fnt_path, 35)
    value_font = font(fnt_path, 28)
    for i, dimension in enumerate(dimensions):
        lx, ly, align = anchors[i]
        label = str(dimension["name"])
        value = f'{dimension["score"]}/{dimension["max"]}'
        lw = draw.textlength(label, font=label_font)
        vw = draw.textlength(value, font=value_font)
        if align == "center":
            tx = lx - lw / 2
            vx = lx - vw / 2
        elif align == "right":
            tx = lx - lw
            vx = lx - vw
        else:
            tx, vx = lx, lx
        # Opaque manga caption strip isolates text from hatch, frame and paper grain.
        box_left = min(tx, vx) - 12
        box_right = max(tx + lw, vx + vw) + 12
        # Draw the leader first, ending at the nearest caption edge. The opaque
        # caption is painted afterwards so no line can cross its text.
        vx_vertex, vy_vertex = outer[i]
        if align == "left":
            edge_x = box_left - 8
            draw.line((vx_vertex, vy_vertex, edge_x, ly + 33), fill=RED, width=7)
            draw.line((vx_vertex, vy_vertex, edge_x, ly + 33), fill=INK, width=3)
        elif align == "right":
            edge_x = box_right + 8
            draw.line((vx_vertex, vy_vertex, edge_x, ly + 33), fill=RED, width=7)
            draw.line((vx_vertex, vy_vertex, edge_x, ly + 33), fill=INK, width=3)
        elif i == 0:
            draw.line((vx_vertex, vy_vertex, lx, ly + 78), fill=RED, width=7)
            draw.line((vx_vertex, vy_vertex, lx, ly + 78), fill=INK, width=3)
        else:
            draw.line((vx_vertex, vy_vertex, lx, ly - 13), fill=RED, width=7)
            draw.line((vx_vertex, vy_vertex, lx, ly - 13), fill=INK, width=3)
        draw.polygon([(box_left, ly - 6), (box_right + 8, ly - 6),
                      (box_right, ly + 72), (box_left - 8, ly + 72)],
                     fill=(255, 255, 248), outline=INK, width=3)
        draw.text((tx, ly), label, font=label_font, fill=INK,
                  stroke_width=1, stroke_fill=INK)
        draw.text((vx, ly + 39), value, font=value_font, fill=RED,
                  stroke_width=1, stroke_fill=WHITE)


def draw_stat_row(draw: ImageDraw.ImageDraw, x: int, y: int, width: int,
                  dimension: dict, fnt_path: str, index: int) -> None:
    score = float(dimension["score"])
    maximum = max(1.0, float(dimension["max"]))
    ratio = score / maximum
    rank = dimension_grade(score, maximum)
    # Alternating black/cream strips with sharp corners.
    dark = index % 2 == 0
    fill, text, accent = (INK, WHITE, RED) if dark else (WHITE, INK, RED)
    polygon = [(x, y), (x + width - 24, y), (x + width, y + 34),
               (x + width - 24, y + 70), (x, y + 70), (x + 15, y + 34)]
    draw.polygon(polygon, fill=fill, outline=INK)
    label_font = font(fnt_path, 27)
    rank_font = font(fnt_path, 42)
    draw.text((x + 28, y + 17), str(dimension["name"]), font=label_font, fill=text)
    # Five manga ticks, filled by normalized performance.
    filled = max(1, round(ratio * 5))
    tick_x = x + 192
    for i in range(5):
        color = accent if i < filled else (120, 116, 109)
        tx = tick_x + i * 29
        draw.rectangle((tx, y + 25, tx + 20, y + 46), fill=color,
                       outline=WHITE if dark else INK, width=1)
    score_text = f'{int(score)}/{int(maximum)}'
    # Dedicated high-contrast score plate prevents digits from touching ticks or rank.
    score_box = (x + 342, y + 13, x + 435, y + 57)
    score_fill = WHITE if dark else INK
    score_ink = INK if dark else WHITE
    draw.rectangle(score_box, fill=score_fill, outline=RED, width=3)
    score_font = font(fnt_path, 23)
    sw = draw.textlength(score_text, font=score_font)
    draw.text((x + 388 - sw / 2, y + 21), score_text, font=score_font,
              fill=score_ink)
    draw.polygon([(x + width - 73, y + 4), (x + width - 9, y + 4),
                  (x + width - 22, y + 65), (x + width - 86, y + 65)], fill=accent)
    rw = draw.textlength(rank, font=rank_font)
    draw.text((x + width - 48 - rw / 2, y + 9), rank, font=rank_font, fill=WHITE,
              stroke_width=2, stroke_fill=INK)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a resume review as a manga stat poster")
    parser.add_argument("panel", help="panel JSON")
    parser.add_argument("out", help="output PNG")
    parser.add_argument("--font", default=None, help="CJK font path")
    args = parser.parse_args()

    data = json.loads(Path(args.panel).read_text(encoding="utf-8"))
    dimensions = data.get("dimensions")
    if not isinstance(dimensions, list) or len(dimensions) != 6:
        raise SystemExit("dimensions 必须是 6 个维度")
    total = float(data.get("total_score", 0))
    fnt_path = find_font(args.font)

    img = Image.new("RGBA", (W, H), PAPER + (255,))
    add_print_texture(img)
    draw = ImageDraw.Draw(img)
    draw_speed_lines(draw)

    # Asymmetric manga masthead.
    draw.polygon([(0, 0), (W, 0), (W, 112), (735, 112), (690, 150), (0, 150)], fill=INK)
    draw.polygon([(0, 112), (724, 112), (680, 154), (0, 154)], fill=RED)
    draw.text((54, 23), "STAND  PARAMETER", font=font(fnt_path, 47), fill=WHITE)
    draw.text((760, 34), "简历评测", font=font(fnt_path, 34), fill=WHITE)
    draw.text((30, 250), "ゴ", font=font(fnt_path, 94), fill=(170, 160, 145))
    draw.text((1085, 440), "ゴ", font=font(fnt_path, 94), fill=(170, 160, 145))

    # Identity: clean 200 px safe zone before chart labels.
    stand_name = str(data.get("stand_name", "「无题」"))
    persona = str(data.get("persona", ""))
    # Solid knockout panel keeps identity text separate from speed lines and grain.
    draw.polygon([(42, 174), (860, 174), (830, 390), (42, 390)],
                 fill=PAPER, outline=INK)
    draw.text((58, 190), "STAND NAME / 替身名", font=font(fnt_path, 24), fill=RED)
    name_font = fit_text(draw, stand_name, fnt_path, 90, 56, 770)
    draw.text((54, 226), stand_name, font=name_font, fill=INK, stroke_width=2, stroke_fill=INK)
    persona_font = fit_text(draw, f"USER / {persona}", fnt_path, 31, 23, 810)
    draw.text((58, 332), f"USER / {persona}", font=persona_font, fill=INK,
              stroke_width=1, stroke_fill=PAPER)
    draw.line((58, 380, 860, 380), fill=INK, width=5)

    # Angular rank plate.
    current_grade = grade(total)
    draw.polygon([(900, 175), (1140, 150), (1160, 345), (920, 370), (875, 260)],
                 fill=RED, outline=INK)
    draw.line((900, 175, 1140, 150, 1160, 345, 920, 370, 875, 260, 900, 175), fill=INK, width=7)
    rank_font = font(fnt_path, 150)
    rw = draw.textlength(current_grade, font=rank_font)
    draw.text((1018 - rw / 2, 169), current_grade, font=rank_font, fill=WHITE,
              stroke_width=4, stroke_fill=INK)
    draw.text((963, 325), f"TOTAL {int(total):03d}", font=font(fnt_path, 23), fill=WHITE)

    # Chart starts safely below identity; no label can overlap the header.
    draw_radar(img, W // 2, 665, 195, dimensions, fnt_path)
    draw = ImageDraw.Draw(img)
    draw.ellipse((W // 2 - 44, 621, W // 2 + 44, 709), fill=INK, outline=RED, width=5)
    total_text = str(int(total))
    total_font = font(fnt_path, 35)
    tw = draw.textlength(total_text, font=total_font)
    draw.text((W / 2 - tw / 2, 642), total_text, font=total_font, fill=WHITE)

    # Stat rows: sharp manga strips, not rounded UI cards.
    draw.polygon([(42, 972), (436, 972), (470, 1013), (42, 1013)], fill=RED)
    draw.text((63, 978), "能力参数 / STAT BREAKDOWN", font=font(fnt_path, 27), fill=WHITE)
    for i, dimension in enumerate(dimensions):
        x = 48 + (i % 2) * 560
        y = 1034 + (i // 2) * 83
        draw_stat_row(draw, x, y, 530, dimension, fnt_path, i)

    # Ability panel with diagonal cut and halftone accent.
    panel = [(48, 1300), (1128, 1300), (1160, 1340), (1118, 1510), (80, 1510), (42, 1467)]
    draw.polygon(panel, fill=INK, outline=RED)
    draw.line(panel + [panel[0]], fill=RED, width=7)
    draw.text((82, 1326), "ABILITY / 替身能力", font=font(fnt_path, 28), fill=RED)
    ability_font = font(fnt_path, 33)
    ability_lines = wrap(draw, str(data.get("ability", "")), ability_font, 980)
    for index, line in enumerate(ability_lines[:3]):
        draw.text((82, 1377 + index * 43), line, font=ability_font, fill=WHITE)

    verdict = str(data.get("verdict", ""))
    verdict_font = fit_text(draw, f"判定 / {verdict}", fnt_path, 28, 22, 860)
    # Footer also gets a clean paper strip so grain never reduces contrast.
    draw.rectangle((42, 1528, 930, 1590), fill=PAPER)
    draw.text((55, 1542), f"判定 / {verdict}", font=verdict_font, fill=INK,
              stroke_width=1, stroke_fill=PAPER)
    draw.text((1015, 1537), "END", font=font(fnt_path, 35), fill=RED)

    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(output, quality=96)
    print(f"完成: {output}  {W}x{H}  评级 {current_grade}")


if __name__ == "__main__":
    main()
