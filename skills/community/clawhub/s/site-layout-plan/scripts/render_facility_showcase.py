#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""导出设施图块大样 PNG：合并大样 + 每个设施单独一张。

图元与 DXF BLOCK 同源（site_layout.symbols.primitives），不复制第三方图块、不联网。
仅用于方案讨论和交底配图；厂家尺寸、基础、附着和型号仍须按专项方案替换。
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.bootstrap import ensure_runtime  # noqa: E402

ensure_runtime(__file__)

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

from site_layout.symbols import SYMBOLS, block_name, draw_pictogram  # noqa: E402

BG = "#f7f7f4"
CARD = "#ffffff"
INK = "#1f2933"
MUTED = "#5b6773"
GRID = "#d8dde3"
ACCENT = "#2e4053"
VERSION = "0.7.0"


def _item(category: str, key: str, color: str, note: str, summary: str) -> Dict[str, Any]:
    meta = SYMBOLS[category]
    stages = meta.get("stages") or ()
    stage_text = " / ".join(_stage_zh(stage) for stage in stages) if stages else "按项目"
    return {
        "key": key,
        "category": category,
        "label": meta["zh"],
        "block": block_name(category),
        "size_mm": float(meta["size_mm"]),
        "layer": meta.get("layer", ""),
        "stages": tuple(stages),
        "stage_text": stage_text,
        "color": color,
        "note": note or meta.get("note", ""),
        "summary": summary,
    }


def _stage_zh(stage: str) -> str:
    return {"earthwork": "土石方", "structure": "主体", "finish": "装饰"}.get(stage, stage)


ITEMS: List[Dict[str, Any]] = [
    _item("tower_crane", "crane", "#b03a2e",
          "基础节、标准节、附着撑杆、回转总成、驾驶室、分节起重臂、小车、双倍率吊钩、平衡臂配重、塔尖拉杆、幅度标注线",
          "基础节/附着/分节臂/小车/双倍率吊钩"),
    _item("construction_elevator", "elev", "#b9770e",
          "底座、双导轨、腹杆、附墙架、层门、吊笼门、电缆滑车、地面围栏与防护棚",
          "双导轨/附墙/层门/吊笼门/电缆滑车"),
    _item("weighbridge", "weighbridge", "#1e8449",
          "分节秤台、四角传感器、限位挡块、两端引坡与坡度箭头、称重房、行车方向",
          "分节秤台/传感器/引坡/称重房/方向"),
    _item("wheel_wash", "wash", "#1f618d",
          "洗车平台、引坡、喷淋拱、三级沉淀池（编号 1/2/3）、排水沟、减速带",
          "平台/喷淋拱/三级沉淀池/排水沟/减速带"),
    _item("site_office", "office", "#7d3c98",
          "两层箱房排、外走廊、楼梯、停车位、旗杆、宣传栏",
          "两层箱房/外走廊/楼梯/停车/旗杆"),
    _item("staff_dormitory", "dorm", "#117a65",
          "箱房排、空调外机、床位、晾晒区、两端疏散楼梯",
          "箱房/空调/床位/晾晒/疏散楼梯"),
    _item("worker_living_zone", "living", "#a04000",
          "宿舍排、食堂、淋浴/厕所、晾晒区、活动场，分区虚线",
          "宿舍/食堂/淋浴/晾晒/活动场"),
]
BY_KEY = {item["key"]: item for item in ITEMS}
ALIASES: Dict[str, str] = {}
for item in ITEMS:
    ALIASES[item["key"]] = item["key"]
    ALIASES[item["category"]] = item["key"]
ALIASES.update({
    "towercrane": "crane", "tower_crane": "crane", "crane": "crane",
    "elevator": "elev", "construction_elevator": "elev",
    "wash": "wash", "wheel_wash": "wash", "carwash": "wash",
    "weigh": "weighbridge", "weighbridge": "weighbridge", "地磅": "weighbridge",
    "office": "office", "site_office": "office",
    "dorm": "dorm", "staff_dorm": "dorm", "staff_dormitory": "dorm",
    "living": "living", "worker_living": "living", "worker_living_zone": "living",
})


def _font(size: int):
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if Path(path).is_file():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _wrap(draw: ImageDraw.ImageDraw, text: str, font, max_width: float) -> List[str]:
    lines: List[str] = []
    line = ""
    for ch in text:
        trial = line + ch
        if line and draw.textlength(trial, font=font) > max_width:
            lines.append(line)
            line = ch
        else:
            line = trial
    if line:
        lines.append(line)
    return lines


def _draw_wrapped(draw: ImageDraw.ImageDraw, text: str, x: float, y: float,
                  font, fill: str, max_width: float, line_gap: float = 8.0) -> float:
    lines = _wrap(draw, text, font, max_width)
    line_height = font.size + line_gap
    for index, line in enumerate(lines):
        draw.text((x, y + index * line_height), line, font=font, fill=fill)
    return y + max(0, len(lines) - 1) * line_height


def _select(value: Optional[str], ap: argparse.ArgumentParser) -> List[Dict[str, Any]]:
    if not value:
        return list(ITEMS)
    selected: List[Dict[str, Any]] = []
    for raw in value.split(","):
        key = raw.strip().lower()
        if not key:
            continue
        resolved = ALIASES.get(key)
        if not resolved or resolved not in BY_KEY:
            ap.error(f"未知设施键 {raw!r}；可用键：{', '.join(BY_KEY)}")
        item = BY_KEY[resolved]
        if item not in selected:
            selected.append(item)
    if not selected:
        ap.error("--only 未给出有效设施键")
    return selected


def render_merged(items: Sequence[Dict[str, Any]], out: Path) -> None:
    cols = 4
    rows = max(1, math.ceil(len(items) / cols))
    card_w, card_h = 400, 500
    margin_x, top = 60, 170
    width = margin_x * 2 + cols * card_w
    height = top + rows * card_h + 90
    image = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(image)
    draw.text((margin_x, 42), "施工设施图块大样（类型示意）", font=_font(42), fill=INK)
    draw.text((margin_x + 2, 102),
              "与 DXF BLOCK 同源 · 本机矢量绘制 · 不替代厂家标准块与专项方案",
              font=_font(22), fill=MUTED)

    for index, item in enumerate(items):
        row, col = divmod(index, cols)
        x0 = margin_x + col * card_w
        y0 = top + row * card_h
        x1, y1 = x0 + card_w - 16, y0 + card_h - 16
        draw.rounded_rectangle((x0, y0, x1, y1), radius=14, fill=CARD,
                               outline=GRID, width=2)
        cx, cy = (x0 + x1) / 2, y0 + 190
        draw_pictogram(draw, item["category"], cx, cy, 280, item["color"], width=3)
        draw.text((x0 + 24, y0 + 342), item["label"], font=_font(30), fill=INK)
        draw.text((x0 + 24, y0 + 380), f"块名 {item['block']}", font=_font(18),
                  fill=item["color"])
        draw.text((x0 + 24, y0 + 406),
                  f"建议 {item['size_mm'] / 1000:.0f} m · {item['stage_text']}",
                  font=_font(16), fill=MUTED)
        _draw_wrapped(draw, item["summary"], x0 + 24, y0 + 432, _font(16), MUTED,
                      card_w - 64, 5)

    # 第 8 格放使用说明；不足 8 项时放在末尾
    note_index = len(items)
    if note_index < cols * rows:
        row, col = divmod(note_index, cols)
        x0 = margin_x + col * card_w
        y0 = top + row * card_h
        x1, y1 = x0 + card_w - 16, y0 + card_h - 16
        draw.rounded_rectangle((x0, y0, x1, y1), radius=14, fill="#eef2f5",
                               outline=GRID, width=2)
        draw.text((x0 + 24, y0 + 26), "图块使用说明", font=_font(28), fill=ACCENT)
        notes = [
            "块基准 1000×1000，原点居中；插入时按建议尺寸缩放。",
            "DXF BLOCK 与 PNG 使用同一套图元，不各画一套。",
            "块名保持稳定，展示键只用于选择，不重命名块。",
            "图块只表达设施类型；厂家型号、基础、附着须替换。",
            "第三方图块须记录来源 URL、许可证、型号、版本、SHA-256。",
        ]
        yy = y0 + 78
        for text in notes:
            draw.text((x0 + 24, yy), "·", font=_font(20), fill=item["color"])
            yy = _draw_wrapped(draw, text, x0 + 44, yy, _font(17), INK,
                               card_w - 78, 6) + 18

    draw.text((margin_x, height - 52),
              f"site-layout-plan · {VERSION} · 图形仅表达设施类型与相对关系；塔吊/电梯/地磅须按实际型号替换。",
              font=_font(18), fill=MUTED)
    out.parent.mkdir(parents=True, exist_ok=True)
    image.save(out)
    print(out)


def render_one(item: Dict[str, Any], out: Path) -> None:
    width, height = 1400, 1500
    image = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(image)
    draw.text((70, 46), f"{item['label']} · 图块大样", font=_font(46), fill=INK)
    draw.text((72, 108),
              "DXF BLOCK 与 PNG 同源 · 类型示意 · 不替代厂家标准块与专项方案",
              font=_font(22), fill=MUTED)
    draw.rounded_rectangle((60, 180, 1340, 1120), radius=18, fill=CARD,
                           outline=GRID, width=2)
    cx, cy = width / 2, 620
    # 中心十字与基准提示，说明原点居中
    draw.line((cx - 560, cy, cx + 560, cy), fill="#e3e8ed", width=2)
    draw.line((cx, cy - 400, cx, cy + 400), fill="#e3e8ed", width=2)
    draw_pictogram(draw, item["category"], cx, cy, 860, item["color"], width=4)
    draw.text((90, 1035), "块基准 1000×1000 · 原点居中 · 图形不按实际尺寸",
              font=_font(20), fill=MUTED)
    draw.text((1040, 1035), "1000 × 1000", font=_font(18), fill=item["color"])

    rows = [
        ("块名", item["block"]),
        ("中文名", item["label"]),
        ("建议尺寸", f"{item['size_mm'] / 1000:.1f} m（类型示意，按项目确认）"),
        ("适用阶段", item["stage_text"]),
        ("建议图层", item["layer"] or "按项目图层表"),
        ("几何要点", item["note"]),
    ]
    y = 1160
    for label, value in rows:
        draw.text((80, y), label, font=_font(20), fill=MUTED)
        if label == "几何要点":
            _draw_wrapped(draw, value, 210, y - 2, _font(20), INK, 1090, 7)
            y += 74
        else:
            draw.text((210, y - 2), value, font=_font(21), fill=INK)
            y += 44
    draw.text((70, height - 46),
              f"site-layout-plan · {VERSION} · 需要厂家图时按 references/draw.md 记录来源、许可证、型号、版本与 SHA-256。",
              font=_font(17), fill=MUTED)
    out.parent.mkdir(parents=True, exist_ok=True)
    image.save(out)
    print(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="导出设施图块大样 PNG（合并 + 分张）")
    ap.add_argument("--out", default=None,
                    help="合并大样 PNG；省略时若未给 --out-dir 则默认 facility-showcase.png")
    ap.add_argument("--out-dir", default=None,
                    help="分张输出目录；每张命名 facility-showcase-<key>.png")
    ap.add_argument("--only", default=None,
                    help="只导出指定设施，逗号分隔：crane,elev,weighbridge,wash,office,dorm,living")
    args = ap.parse_args()

    items = _select(args.only, ap)
    out = Path(args.out).expanduser().resolve() if args.out else None
    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else None
    if out is None and out_dir is None:
        out = Path("facility-showcase.png").resolve()

    if out is not None:
        render_merged(items, out)
        if out_dir is None:
            out_dir = out.parent / f"{out.stem}-items"
    if out_dir is not None:
        for item in items:
            render_one(item, out_dir / f"facility-showcase-{item['key']}.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
