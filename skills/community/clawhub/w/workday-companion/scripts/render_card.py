#!/usr/bin/env python3
"""Render a Workday Companion card JSON into standalone HTML and SVG."""

from __future__ import annotations

import argparse
import html
import json
import unicodedata
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "assets" / "card-template.html"
CSS_PATH = ROOT / "assets" / "card-template.css"

ROUTE_CLASS = {
    "sign-strip": "sign-strip",
    "lunch-receipt": "lunch-receipt",
    "mood-notice": "mood-notice",
    "afterwork-pass": "afterwork-pass",
}

REQUIRED = ["module", "route", "time_label", "title", "reason", "action", "footer", "alt_text", "share_safe"]
PUBLIC_TEXT_FIELDS = ("module", "time_label", "title", "reason", "action", "footer", "corner", "alt_text")
PRIVATE_MARKERS = (
    "公司名",
    "公司名称",
    "具体住址",
    "真实地址",
    "精确定位",
    "同事姓名",
    "会议内容",
    "会议主题",
    "客户姓名",
    "手机号",
    "支付信息",
    "账号信息",
)


def iter_public_text(data: dict[str, Any]) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    for field in PUBLIC_TEXT_FIELDS:
        value = data.get(field)
        if isinstance(value, str):
            values.append((field, value))
    tags = data.get("tags", [])
    if isinstance(tags, list):
        for index, tag in enumerate(tags, start=1):
            if isinstance(tag, str):
                values.append((f"tags[{index}]", tag))
    return values


def assert_public_safe_text(data: dict[str, Any]) -> None:
    for field, value in iter_public_text(data):
        for marker in PRIVATE_MARKERS:
            if marker in value:
                raise SystemExit(f"{field} contains private marker: {marker}")


def load_card(path: str) -> dict[str, Any]:
    raw = Path(path).read_text(encoding="utf-8") if path != "-" else __import__("sys").stdin.read()
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise SystemExit("Card JSON must be an object.")
    missing = [key for key in REQUIRED if key not in data]
    if missing:
        raise SystemExit(f"Missing required fields: {', '.join(missing)}")
    blank = [key for key in REQUIRED if key != "share_safe" and not data.get(key)]
    if blank:
        raise SystemExit(f"Blank required fields: {', '.join(blank)}")
    route = data.get("route")
    if route not in ROUTE_CLASS:
        raise SystemExit(f"Unsupported route: {route}")
    tags = data.get("tags", [])
    if not isinstance(tags, list) or len(tags) > 4:
        raise SystemExit("tags must be a list with at most 4 items.")
    if data.get("share_safe") is not True:
        raise SystemExit("share_safe must be true before rendering.")
    assert_public_safe_text(data)
    return data


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def ratio_css(ratio: str) -> str:
    return "3 / 4" if ratio == "3:4" else "9 / 16"


def render_tags(tags: list[Any]) -> str:
    return "".join(f'<span class="tag">{esc(tag)}</span>' for tag in tags)


def render_html(data: dict[str, Any]) -> str:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    css = CSS_PATH.read_text(encoding="utf-8")
    values = {
        "css": css,
        "module": esc(data["module"]),
        "time_label": esc(data["time_label"]),
        "route": esc(ROUTE_CLASS[data["route"]]),
        "title": esc(data["title"]),
        "reason": esc(data["reason"]),
        "action": esc(data["action"]),
        "tags": render_tags(data.get("tags", [])),
        "corner": esc(data.get("corner", "重判")),
        "footer": esc(data["footer"]),
        "ratio_css": ratio_css(data.get("ratio", "9:16")),
    }
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def svg_text(text: str, x: int, y: int, size: int, weight: int = 700, color: str = "#211f1b") -> str:
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}">{esc(text)}</text>'


def display_units(text: str) -> int:
    return sum(2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1 for char in text)


def wrap_display(text: str, max_units: int, max_lines: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in text:
        candidate = current + char
        if current and display_units(candidate) > max_units:
            lines.append(current.rstrip())
            current = char.lstrip()
        else:
            current = candidate
    if current or not lines:
        lines.append(current.rstrip())
    if len(lines) <= max_lines:
        return lines
    kept = lines[:max_lines]
    tail = "".join(lines[max_lines - 1 :])
    while tail and display_units(tail + "…") > max_units:
        tail = tail[:-1]
    kept[-1] = tail.rstrip() + "…"
    return kept


def svg_multiline(text: str, x: int, y: int, size: int, max_units: int, max_lines: int, line_height: int, weight: int = 700, color: str = "#211f1b") -> str:
    lines = wrap_display(text, max_units=max_units, max_lines=max_lines)
    tspans = "".join(
        f'<tspan x="{x}" y="{y + index * line_height}">{esc(line)}</tspan>'
        for index, line in enumerate(lines)
    )
    return f'<text font-size="{size}" font-weight="{weight}" fill="{color}">{tspans}</text>'


def render_svg(data: dict[str, Any]) -> str:
    width, height = (900, 1200) if data.get("ratio") == "3:4" else (900, 1600)
    tags = data.get("tags", [])[:4]
    tag_nodes = []
    x = 78
    y = height - 270
    for tag in tags:
        label = str(tag)
        tag_width = max(92, min(210, 42 + len(label) * 20))
        if x + tag_width > 822:
            x = 78
            y += 64
        tag_nodes.append(f'<rect x="{x}" y="{y - 34}" width="{tag_width}" height="52" rx="26" fill="#e8dfcf"/>')
        tag_nodes.append(svg_text(label, x + 20, y, 24, 700))
        x += tag_width + 18
    module_time = f'{data["module"]} · {data["time_label"]}'
    title = str(data["title"])
    reason = str(data["reason"])
    action = str(data["action"])
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            f'<desc>{esc(data["alt_text"])}</desc>',
            '<rect width="100%" height="100%" fill="#ece7dc"/>',
            '<rect x="50" y="50" width="800" height="' + str(height - 100) + '" rx="44" fill="#fffaf0" stroke="#d8cdbb"/>',
            '<rect x="78" y="78" width="744" height="' + str(height - 156) + '" rx="32" fill="none" stroke="#d8cdbb" stroke-dasharray="10 12"/>',
            svg_text(str(module_time), 78, 138, 28, 800, "#746f66"),
            svg_text(str(data.get("corner", "重判")), width - 220, 138, 28, 800, "#c95f3d"),
            svg_multiline(title, 78, 260, 68, 20, 2, 78, 900),
            '<rect x="78" y="420" width="744" height="210" rx="28" fill="#ffffff" opacity="0.62" stroke="#d8cdbb"/>',
            svg_text("依据", 110, 465, 24, 600, "#746f66"),
            svg_multiline(reason, 110, 515, 30, 38, 3, 42, 750),
            '<rect x="78" y="660" width="744" height="210" rx="28" fill="#ffffff" opacity="0.62" stroke="#d8cdbb"/>',
            svg_text("现在做", 110, 705, 24, 600, "#746f66"),
            svg_multiline(action, 110, 755, 30, 38, 3, 42, 750),
            *tag_nodes,
            f'<line x1="78" y1="{height - 150}" x2="822" y2="{height - 150}" stroke="#d8cdbb"/>',
            svg_text(str(data["footer"]), 78, height - 92, 28, 700, "#746f66"),
            svg_text("WORKDAY COMPANION", width - 390, height - 92, 24, 700, "#746f66"),
            "</svg>",
        ]
    )


def find_font_path(explicit: str | None = None) -> Path:
    candidates = [
        explicit,
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return Path(candidate)
    raise SystemExit("No CJK-capable font found. Pass --font PATH when rendering PNG.")


def render_png(data: dict[str, Any], output: str, font_path: str | None = None) -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as exc:
        raise SystemExit("PNG rendering needs Pillow. SVG and HTML rendering remain available.") from exc

    width, height = (900, 1200) if data.get("ratio") == "3:4" else (900, 1600)
    route_colors = {
        "sign-strip": (255, 247, 231),
        "lunch-receipt": (255, 250, 242),
        "mood-notice": (237, 244, 242),
        "afterwork-pass": (242, 240, 251),
    }
    font_file = str(find_font_path(font_path))
    image = Image.new("RGB", (width, height), (236, 231, 220))
    draw = ImageDraw.Draw(image)
    paper = route_colors[data["route"]]
    ink = (33, 31, 27)
    muted = (116, 111, 102)
    accent = (177, 91, 42)
    line = (216, 205, 187)
    soft = (232, 223, 207)
    draw.rounded_rectangle((50, 50, 850, height - 50), radius=44, fill=paper, outline=line, width=2)
    for x in range(78, 822, 22):
        draw.line((x, 78, min(x + 10, 822), 78), fill=line, width=2)
        draw.line((x, height - 78, min(x + 10, 822), height - 78), fill=line, width=2)
    for y in range(78, height - 78, 22):
        draw.line((78, y, 78, min(y + 10, height - 78)), fill=line, width=2)
        draw.line((822, y, 822, min(y + 10, height - 78)), fill=line, width=2)

    def font(size: int):
        return ImageFont.truetype(font_file, size=size)

    def pixel_lines(text: str, text_font: Any, max_width: int, max_lines: int) -> list[str]:
        lines: list[str] = []
        current = ""
        for char in text:
            candidate = current + char
            if current and draw.textlength(candidate, font=text_font) > max_width:
                lines.append(current.rstrip())
                current = char.lstrip()
            else:
                current = candidate
        if current or not lines:
            lines.append(current.rstrip())
        if len(lines) <= max_lines:
            return lines
        tail = "".join(lines[max_lines - 1 :])
        while tail and draw.textlength(tail + "…", font=text_font) > max_width:
            tail = tail[:-1]
        return lines[: max_lines - 1] + [tail.rstrip() + "…"]

    meta_font = font(28)
    title_font = font(68)
    label_font = font(24)
    body_font = font(30)
    tag_font = font(24)
    footer_font = font(24)
    draw.text((78, 105), f'{data["module"]} · {data["time_label"]}', font=meta_font, fill=muted)
    draw.text((680, 105), str(data.get("corner", "重判")), font=meta_font, fill=accent)
    for index, line_text in enumerate(pixel_lines(str(data["title"]), title_font, 744, 2)):
        draw.text((78, 205 + index * 78), line_text, font=title_font, fill=ink)
    draw.rounded_rectangle((78, 420, 822, 630), radius=28, fill=(255, 255, 255), outline=line, width=2)
    draw.text((110, 442), "依据", font=label_font, fill=muted)
    for index, line_text in enumerate(pixel_lines(str(data["reason"]), body_font, 680, 3)):
        draw.text((110, 488 + index * 42), line_text, font=body_font, fill=ink)
    draw.rounded_rectangle((78, 660, 822, 870), radius=28, fill=(255, 255, 255), outline=line, width=2)
    draw.text((110, 682), "现在做", font=label_font, fill=muted)
    for index, line_text in enumerate(pixel_lines(str(data["action"]), body_font, 680, 3)):
        draw.text((110, 728 + index * 42), line_text, font=body_font, fill=ink)
    x, y = 78, height - 304
    for tag in data.get("tags", [])[:4]:
        label = str(tag)
        tag_width = max(92, min(210, int(draw.textlength(label, font=tag_font)) + 40))
        if x + tag_width > 822:
            x, y = 78, y + 64
        draw.rounded_rectangle((x, y, x + tag_width, y + 52), radius=26, fill=soft)
        draw.text((x + 20, y + 10), label, font=tag_font, fill=ink)
        x += tag_width + 18
    draw.line((78, height - 150, 822, height - 150), fill=line, width=2)
    footer = pixel_lines(str(data["footer"]), footer_font, 330, 1)[0]
    draw.text((78, height - 125), footer, font=footer_font, fill=muted)
    draw.text((510, height - 125), "WORKDAY COMPANION", font=footer_font, fill=muted)
    image.save(output, format="PNG", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Workday Companion card JSON.")
    parser.add_argument("input", help="Path to card JSON, or - for stdin.")
    parser.add_argument("--html", dest="html_out", help="Output standalone HTML path.")
    parser.add_argument("--svg", dest="svg_out", help="Output SVG path.")
    parser.add_argument("--png", dest="png_out", help="Output PNG path. Requires Pillow.")
    parser.add_argument("--font", dest="font_path", help="Optional font path for PNG rendering.")
    args = parser.parse_args()

    data = load_card(args.input)
    if not args.html_out and not args.svg_out and not args.png_out:
        print(render_html(data))
        return
    if args.html_out:
        Path(args.html_out).write_text(render_html(data), encoding="utf-8")
    if args.svg_out:
        Path(args.svg_out).write_text(render_svg(data), encoding="utf-8")
    if args.png_out:
        render_png(data, args.png_out, font_path=args.font_path)


if __name__ == "__main__":
    main()
