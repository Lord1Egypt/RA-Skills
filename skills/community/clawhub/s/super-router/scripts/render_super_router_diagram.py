#!/usr/bin/env python3
"""Render the Super Router LangGraph architecture diagram.

This is a deterministic source for the root-level ``super-router.png`` asset.
It reads ``scripts/router.py`` to verify that the diagram still covers the
current ``build_router_graph`` node set before writing the image.
"""

from __future__ import annotations

import ast
import math
from pathlib import Path
from typing import Iterable, Sequence

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ROUTER_PATH = ROOT / "scripts" / "router.py"
OUTPUT_PATH = ROOT / "super-router.png"

WIDTH = 1861
HEIGHT = 2520
BACKGROUND = "#111820"
PANEL_FILL = "#151d26"
PANEL_OUTLINE = "#2a3440"
TEXT = "#d6dee8"
MUTED = "#9ba6b3"
EDGE = "#8e99a6"
EDGE_DIM = "#64717f"
BLUE = "#4ea1ff"
BLUE_FILL = "#09203f"
ORANGE = "#d49a20"
ORANGE_FILL = "#2d2109"
GREEN = "#36be5f"
GREEN_FILL = "#062916"
PURPLE = "#a66cff"
PURPLE_FILL = "#21122f"
RED = "#ff5a52"
RED_FILL = "#32191a"
GRAY = "#7f8a96"
GRAY_FILL = "#20272f"


EXPECTED_GRAPH_NODES = {
    "planner_warmup",
    "planner_invoke",
    "planner_parse",
    "planner_fallback",
    "dependency_judge",
    "dependency_validate",
    "planner_ready",
    "judge_warmup",
    "judge_subtask",
    "assemble_plan",
    "dependency_scheduler",
    "parallel_executor",
    "dependency_execution_join",
    "dependency_deadlock",
    "execution_finalize_join",
    "flash_finalizer",
    "flash_finalizer_verify",
    "pro_finalizer",
    "pro_finalizer_verify",
    "deterministic_finalizer",
    "finalizer_complete",
}


def load_font(name: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    font_paths = [
        Path("/System/Library/Fonts/Supplemental") / name,
        Path("/Library/Fonts") / name,
        Path("/usr/share/fonts/truetype/dejavu") / name,
    ]
    for path in font_paths:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


FONT_REG = load_font("Arial.ttf", 28)
FONT_REG_SMALL = load_font("Arial.ttf", 24)
FONT_REG_TINY = load_font("Arial.ttf", 20)
FONT_BOLD = load_font("Arial Bold.ttf", 30)
FONT_BOLD_MED = load_font("Arial Bold.ttf", 26)
FONT_BOLD_TINY = load_font("Arial Bold.ttf", 22)
FONT_BOLD_SMALL = load_font("Arial Bold.ttf", 24)
FONT_TITLE = load_font("Arial Bold.ttf", 44)
FONT_SECTION = load_font("Arial Bold.ttf", 28)


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def center_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    font: ImageFont.ImageFont,
    fill: str,
) -> None:
    x, y = xy
    width, height = text_size(draw, text, font)
    draw.text((x - width / 2, y - height / 2), text, font=font, fill=fill)


def wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.ImageFont,
    max_width: int,
) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if text_size(draw, candidate, font)[0] <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def rounded_box(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    title: str,
    subtitle: str = "",
    detail: str = "",
    *,
    outline: str,
    fill: str,
    title_fill: str | None = None,
    width: int = 5,
    radius: int = 18,
) -> None:
    x1, y1, x2, y2 = rect
    draw.rounded_rectangle(rect, radius=radius, fill=fill, outline=outline, width=width)
    title_fill = title_fill or outline
    title_font = FONT_BOLD
    if text_size(draw, title, title_font)[0] > x2 - x1 - 40:
        title_font = FONT_BOLD_MED
    if text_size(draw, title, title_font)[0] > x2 - x1 - 40:
        title_font = FONT_BOLD_TINY
    center_text(draw, ((x1 + x2) / 2, y1 + 31), title, title_font, title_fill)
    cursor = y1 + 62
    if subtitle:
        center_text(draw, ((x1 + x2) / 2, cursor + 12), subtitle, FONT_REG_SMALL, TEXT)
        cursor += 34
    if detail:
        for line in wrap_text(draw, detail, FONT_REG_TINY, x2 - x1 - 42)[:3]:
            center_text(draw, ((x1 + x2) / 2, cursor + 12), line, FONT_REG_TINY, MUTED)
            cursor += 26


def panel(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    title: str,
    *,
    color: str,
) -> None:
    draw.rounded_rectangle(rect, radius=24, fill=PANEL_FILL, outline=PANEL_OUTLINE, width=3)
    x1, y1, _, _ = rect
    draw.text((x1 + 26, y1 + 18), title, font=FONT_SECTION, fill=color)


def arrowhead_points(
    start: tuple[float, float],
    end: tuple[float, float],
    size: int = 18,
) -> list[tuple[float, float]]:
    sx, sy = start
    ex, ey = end
    angle = math.atan2(ey - sy, ex - sx)
    left = angle + math.pi * 0.82
    right = angle - math.pi * 0.82
    return [
        (ex, ey),
        (ex + size * math.cos(left), ey + size * math.sin(left)),
        (ex + size * math.cos(right), ey + size * math.sin(right)),
    ]


def draw_polyline(
    draw: ImageDraw.ImageDraw,
    points: Sequence[tuple[float, float]],
    *,
    fill: str = EDGE,
    width: int = 5,
    dashed: bool = False,
    label: str = "",
    label_pos: float = 0.5,
    label_color: str | None = None,
    label_offset: tuple[int, int] = (0, 0),
) -> None:
    if len(points) < 2:
        return
    segments = list(zip(points, points[1:]))
    if dashed:
        for start, end in segments:
            draw_dashed_segment(draw, start, end, fill=fill, width=width)
    else:
        draw.line(points, fill=fill, width=width, joint="curve")

    draw.polygon(arrowhead_points(points[-2], points[-1]), fill=fill)
    if label:
        label_color = label_color or fill
        lx, ly = point_along_polyline(points, label_pos)
        lx += label_offset[0]
        ly += label_offset[1]
        pad_x, pad_y = 10, 6
        tw, th = text_size(draw, label, FONT_BOLD_TINY)
        draw.rounded_rectangle(
            (lx - tw / 2 - pad_x, ly - th / 2 - pad_y, lx + tw / 2 + pad_x, ly + th / 2 + pad_y),
            radius=9,
            fill=BACKGROUND,
        )
        center_text(draw, (lx, ly), label, FONT_BOLD_TINY, label_color)


def draw_dashed_segment(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    fill: str,
    width: int,
    dash: int = 18,
    gap: int = 12,
) -> None:
    sx, sy = start
    ex, ey = end
    length = math.hypot(ex - sx, ey - sy)
    if length == 0:
        return
    dx = (ex - sx) / length
    dy = (ey - sy) / length
    distance = 0.0
    while distance < length:
        seg_start = distance
        seg_end = min(distance + dash, length)
        draw.line(
            (
                sx + dx * seg_start,
                sy + dy * seg_start,
                sx + dx * seg_end,
                sy + dy * seg_end,
            ),
            fill=fill,
            width=width,
        )
        distance += dash + gap


def point_along_polyline(points: Sequence[tuple[float, float]], fraction: float) -> tuple[float, float]:
    lengths = [
        math.hypot(points[i + 1][0] - points[i][0], points[i + 1][1] - points[i][1])
        for i in range(len(points) - 1)
    ]
    total = sum(lengths)
    target = total * fraction
    traversed = 0.0
    for index, length in enumerate(lengths):
        if traversed + length >= target:
            local = 0 if length == 0 else (target - traversed) / length
            x1, y1 = points[index]
            x2, y2 = points[index + 1]
            return (x1 + (x2 - x1) * local, y1 + (y2 - y1) * local)
        traversed += length
    return points[-1]


def extract_build_router_graph_nodes(source: str) -> set[str]:
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "build_router_graph":
            names: set[str] = set()
            for child in ast.walk(node):
                if not isinstance(child, ast.Call):
                    continue
                func = child.func
                if not (
                    isinstance(func, ast.Attribute)
                    and func.attr == "add_node"
                    and child.args
                    and isinstance(child.args[0], ast.Constant)
                    and isinstance(child.args[0].value, str)
                ):
                    continue
                names.add(child.args[0].value)
            return names
    raise RuntimeError("build_router_graph not found")


def assert_diagram_matches_router() -> None:
    actual_nodes = extract_build_router_graph_nodes(ROUTER_PATH.read_text())
    missing = actual_nodes - EXPECTED_GRAPH_NODES
    stale = EXPECTED_GRAPH_NODES - actual_nodes
    if missing or stale:
        details = []
        if missing:
            details.append(f"missing from diagram: {', '.join(sorted(missing))}")
        if stale:
            details.append(f"not in router graph: {', '.join(sorted(stale))}")
        raise RuntimeError("Diagram node set is stale: " + "; ".join(details))


def draw_status_nodes(draw: ImageDraw.ImageDraw) -> None:
    rounded_box(
        draw,
        (782, 118, 1079, 198),
        "START",
        outline=GRAY,
        fill=GRAY_FILL,
        title_fill=TEXT,
        width=4,
    )
    rounded_box(
        draw,
        (782, 2404, 1079, 2484),
        "END",
        outline=GRAY,
        fill=GRAY_FILL,
        title_fill=TEXT,
        width=4,
    )


def draw_planner(draw: ImageDraw.ImageDraw) -> None:
    panel(draw, (270, 250, 1591, 640), "Planner + Dependency Planning", color=BLUE)
    rounded_box(
        draw,
        (350, 340, 650, 435),
        "planner_warmup",
        "warm provider path",
        "loops until attempt 3, then invokes planner",
        outline=BLUE,
        fill=BLUE_FILL,
    )
    rounded_box(
        draw,
        (785, 340, 1085, 435),
        "planner_invoke",
        "planner model call",
        "provider fallback result is parsed next",
        outline=BLUE,
        fill=BLUE_FILL,
    )
    rounded_box(
        draw,
        (1220, 340, 1520, 435),
        "planner_parse",
        "JSON subtasks",
        "normalizes atomic subtasks",
        outline=BLUE,
        fill=BLUE_FILL,
    )
    rounded_box(
        draw,
        (785, 505, 1085, 600),
        "planner_fallback",
        "deterministic plan",
        "used when invoke or parse fails",
        outline=ORANGE,
        fill=ORANGE_FILL,
        title_fill=ORANGE,
    )

    draw_polyline(draw, [(930, 198), (930, 250), (500, 250), (500, 340)], fill=EDGE)
    draw_polyline(draw, [(650, 388), (785, 388)], fill=BLUE)
    draw_polyline(draw, [(1085, 388), (1220, 388)], fill=BLUE)
    draw_polyline(
        draw,
        [(500, 340), (500, 305), (330, 305), (330, 470), (500, 470), (500, 435)],
        fill=BLUE,
        dashed=True,
        label="warmup loop",
        label_pos=0.45,
        label_offset=(-55, -34),
    )
    draw_polyline(
        draw,
        [(935, 435), (935, 505)],
        fill=ORANGE,
        dashed=True,
        label_pos=0.45,
        label_color=ORANGE,
    )
    draw_polyline(
        draw,
        [(1370, 435), (1370, 555), (1085, 555)],
        fill=ORANGE,
        dashed=True,
        label="parse fail",
        label_pos=0.45,
        label_color=ORANGE,
        label_offset=(0, -36),
    )
    draw_polyline(draw, [(1370, 435), (1370, 690)], fill=EDGE_DIM)
    draw_polyline(draw, [(935, 600), (935, 690)], fill=ORANGE)


def draw_judge(draw: ImageDraw.ImageDraw) -> None:
    panel(draw, (210, 690, 1651, 1130), "Judge Fanout + Plan Assembly", color=ORANGE)
    rounded_box(
        draw,
        (310, 780, 625, 875),
        "dependency_judge",
        "infer dependencies",
        "model or heuristic dependency DAG",
        outline=ORANGE,
        fill=ORANGE_FILL,
        title_fill=ORANGE,
    )
    rounded_box(
        draw,
        (775, 780, 1090, 875),
        "dependency_validate",
        "validate DAG",
        "fallback to serial order if invalid",
        outline=ORANGE,
        fill=ORANGE_FILL,
        title_fill=ORANGE,
    )
    rounded_box(
        draw,
        (1240, 780, 1555, 875),
        "planner_ready",
        "planning complete",
        "hands subtasks to judge phase",
        outline=ORANGE,
        fill=ORANGE_FILL,
        title_fill=ORANGE,
    )
    rounded_box(
        draw,
        (310, 990, 625, 1085),
        "judge_warmup",
        "optional warmup",
        "conditional Send fanout follows",
        outline=ORANGE,
        fill=ORANGE_FILL,
        title_fill=ORANGE,
    )
    rounded_box(
        draw,
        (775, 990, 1090, 1085),
        "judge_subtask",
        "5-score routing",
        "PRO/FLASH per subtask",
        outline=ORANGE,
        fill=ORANGE_FILL,
        title_fill=ORANGE,
    )
    rounded_box(
        draw,
        (1240, 990, 1555, 1085),
        "assemble_plan",
        "ordered route plan",
        "collects judged branches",
        outline=ORANGE,
        fill=ORANGE_FILL,
        title_fill=ORANGE,
    )

    draw_polyline(draw, [(1370, 690), (1370, 735), (468, 735), (468, 780)], fill=EDGE)
    draw_polyline(draw, [(935, 690), (935, 735), (468, 735), (468, 780)], fill=ORANGE)
    draw_polyline(draw, [(625, 828), (775, 828)], fill=ORANGE)
    draw_polyline(draw, [(1090, 828), (1240, 828)], fill=ORANGE)
    draw_polyline(draw, [(1398, 875), (1398, 930), (468, 930), (468, 990)], fill=ORANGE)
    draw_polyline(
        draw,
        [(625, 1038), (775, 1038)],
        fill=ORANGE,
        label="fanout",
        label_color=ORANGE,
        label_offset=(0, -40),
    )
    draw_polyline(draw, [(1090, 1038), (1240, 1038)], fill=ORANGE)


def draw_execution(draw: ImageDraw.ImageDraw) -> None:
    panel(draw, (150, 1175, 1711, 1748), "Dependency-Aware Execution Loop", color=GREEN)
    rounded_box(
        draw,
        (700, 1260, 1160, 1365),
        "dependency_scheduler",
        "ready-set calculation",
        "ready -> fanout; empty -> finalizer; blocked -> deadlock",
        outline=GREEN,
        fill=GREEN_FILL,
        title_fill=GREEN,
    )
    rounded_box(
        draw,
        (250, 1445, 760, 1608),
        "parallel_executor",
        "PRO/FLASH execution",
        "provider fallback; FLASH review, retry, and escalation; embedded metadata extraction",
        outline=GREEN,
        fill=GREEN_FILL,
        title_fill=GREEN,
    )
    rounded_box(
        draw,
        (820, 1475, 1175, 1570),
        "dependency_execution_join",
        "merge results",
        "returns to scheduler until all IDs complete",
        outline=GREEN,
        fill=GREEN_FILL,
        title_fill=GREEN,
    )
    rounded_box(
        draw,
        (1280, 1445, 1610, 1540),
        "dependency_deadlock",
        "no ready subtasks",
        "records blocked dependency state",
        outline=RED,
        fill=RED_FILL,
        title_fill=RED,
    )
    rounded_box(
        draw,
        (700, 1650, 1160, 1735),
        "execution_finalize_join",
        "execution complete",
        "all branches or deadlock path have joined",
        outline=GREEN,
        fill=GREEN_FILL,
        title_fill=GREEN,
    )
    rounded_box(
        draw,
        (250, 1624, 760, 1709),
        "embedded result metadata",
        "not a graph node",
        "parallel_executor appends technical metadata to history",
        outline=BLUE,
        fill=BLUE_FILL,
        title_fill=BLUE,
        width=4,
    )

    draw_polyline(draw, [(1398, 1085), (1398, 1165), (930, 1165), (930, 1260)], fill=EDGE)
    draw_polyline(
        draw,
        [(700, 1312), (505, 1312), (505, 1445)],
        fill=GREEN,
        label="ready",
        label_color=GREEN,
        label_offset=(-5, -34),
    )
    draw_polyline(draw, [(760, 1527), (820, 1527)], fill=GREEN)
    draw_polyline(
        draw,
        [(998, 1475), (998, 1418), (1215, 1418), (1215, 1240), (930, 1240), (930, 1260)],
        fill=GREEN,
        dashed=True,
        label="remaining",
        label_pos=0.35,
        label_color=GREEN,
        label_offset=(0, -34),
    )
    draw_polyline(
        draw,
        [(1160, 1312), (1430, 1312), (1430, 1445)],
        fill=RED,
        dashed=True,
        label="blocked",
        label_color=RED,
        label_offset=(0, -34),
    )
    draw_polyline(draw, [(1445, 1540), (1445, 1692), (1160, 1692)], fill=RED, dashed=True)
    draw_polyline(
        draw,
        [(930, 1365), (930, 1408), (1225, 1408), (1225, 1692), (1160, 1692)],
        fill=GREEN,
        label_pos=0.45,
        label_color=GREEN,
    )
    draw_polyline(draw, [(505, 1608), (505, 1624)], fill=BLUE, dashed=True)


def draw_finalizer(draw: ImageDraw.ImageDraw) -> None:
    panel(draw, (200, 1815, 1661, 2345), "Finalizer Verification Cascade", color=PURPLE)
    rounded_box(
        draw,
        (330, 1905, 670, 2000),
        "flash_finalizer",
        "primary final report",
        "fast synthesis via provider fallback",
        outline=PURPLE,
        fill=PURPLE_FILL,
        title_fill=PURPLE,
    )
    rounded_box(
        draw,
        (810, 1905, 1150, 2000),
        "flash_finalizer_verify",
        "quality gate",
        "pass, escalate to PRO, or skip to deterministic",
        outline=PURPLE,
        fill=PURPLE_FILL,
        title_fill=PURPLE,
    )
    rounded_box(
        draw,
        (330, 2080, 670, 2175),
        "pro_finalizer",
        "fallback synthesis",
        "heavy model path when useful",
        outline=BLUE,
        fill=BLUE_FILL,
        title_fill=BLUE,
    )
    rounded_box(
        draw,
        (810, 2080, 1150, 2175),
        "pro_finalizer_verify",
        "quality gate",
        "pass or deterministic fallback",
        outline=BLUE,
        fill=BLUE_FILL,
        title_fill=BLUE,
    )
    rounded_box(
        draw,
        (610, 2220, 1015, 2315),
        "deterministic_finalizer",
        "last-resort report",
        "guaranteed local template",
        outline=RED,
        fill=RED_FILL,
        title_fill=RED,
    )
    rounded_box(
        draw,
        (1260, 2060, 1560, 2165),
        "finalizer_complete",
        "print + ledger",
        "token summary and optional JSONL usage ledger",
        outline=PURPLE,
        fill=PURPLE_FILL,
        title_fill=PURPLE,
    )

    draw_polyline(draw, [(930, 1735), (930, 1815), (500, 1815), (500, 1905)], fill=EDGE)
    draw_polyline(draw, [(670, 1952), (810, 1952)], fill=PURPLE)
    draw_polyline(
        draw,
        [(1150, 1952), (1260, 1952), (1260, 2112)],
        fill=PURPLE,
    )
    draw_polyline(
        draw,
        [(980, 2000), (980, 2035), (500, 2035), (500, 2080)],
        fill=BLUE,
        dashed=True,
        label="reject",
        label_color=BLUE,
        label_offset=(0, 38),
    )
    draw_polyline(draw, [(670, 2128), (810, 2128)], fill=BLUE)
    draw_polyline(
        draw,
        [(1150, 2128), (1260, 2128)],
        fill=PURPLE,
    )
    draw_polyline(
        draw,
        [(980, 2175), (980, 2220)],
        fill=RED,
        dashed=True,
        label="fail",
        label_color=RED,
        label_offset=(34, 0),
    )
    draw_polyline(
        draw,
        [(1150, 1952), (1210, 1952), (1210, 2268), (1015, 2268)],
        fill=RED,
        dashed=True,
        label="skip PRO",
        label_pos=0.52,
        label_color=RED,
        label_offset=(-64, -40),
    )
    draw_polyline(draw, [(1015, 2268), (1590, 2268), (1590, 2112), (1560, 2112)], fill=RED)
    draw_polyline(draw, [(1410, 2165), (1410, 2370), (930, 2370), (930, 2404)], fill=EDGE)


def draw_provider_legend(draw: ImageDraw.ImageDraw) -> None:
    x1, y1, x2, y2 = 1170, 118, 1710, 220
    draw.rounded_rectangle((x1, y1, x2, y2), radius=18, fill="#10161d", outline=PANEL_OUTLINE, width=3)
    draw.text((x1 + 22, y1 + 17), "Provider fallback subgraph", font=FONT_BOLD_SMALL, fill=TEXT)
    draw.text(
        (x1 + 22, y1 + 50),
        "invoke_with_provider_fallback: model_attempt_prepare -> model_invoke",
        font=FONT_REG_TINY,
        fill=MUTED,
    )
    draw.text(
        (x1 + 22, y1 + 76),
        "Used by planner, judge, executor branches, and finalizers.",
        font=FONT_REG_TINY,
        fill=MUTED,
    )


def draw_legend(draw: ImageDraw.ImageDraw) -> None:
    items = [
        (BLUE, "planner/provider call"),
        (ORANGE, "planning/judging"),
        (GREEN, "executor loop"),
        (PURPLE, "finalizer"),
        (RED, "fallback/error branch"),
    ]
    x = 110
    y = 128
    draw.rounded_rectangle((x - 18, y - 18, x + 675, y + 92), radius=18, fill="#10161d", outline=PANEL_OUTLINE, width=3)
    for index, (color, label) in enumerate(items):
        col = index // 3
        row = index % 3
        item_x = x + col * 350
        item_y = y + row * 32
        draw.rounded_rectangle((item_x, item_y, item_x + 24, item_y + 24), radius=6, fill=color)
        draw.text((item_x + 34, item_y - 2), label, font=FONT_REG_TINY, fill=MUTED)


def render() -> None:
    assert_diagram_matches_router()
    image = Image.new("RGBA", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    center_text(
        draw,
        (WIDTH / 2, 60),
        "LangGraph StateGraph - Super-Router",
        FONT_TITLE,
        BLUE,
    )
    center_text(
        draw,
        (WIDTH / 2, 105),
        "Current implementation: planner pipeline, dependency-aware fanout, executor loop, finalizer cascade",
        FONT_REG_SMALL,
        MUTED,
    )
    draw_status_nodes(draw)
    draw_planner(draw)
    draw_judge(draw)
    draw_execution(draw)
    draw_finalizer(draw)
    draw_provider_legend(draw)
    image.save(OUTPUT_PATH)


if __name__ == "__main__":
    render()
