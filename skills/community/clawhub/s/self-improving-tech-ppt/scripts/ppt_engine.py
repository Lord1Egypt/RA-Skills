#!/usr/bin/env python3
"""
Reusable Native Editable PPTX + SVG + Icon + Automated Self-Check + QuickLook QA Engine
for the `self-improving-tech-ppt` Open-Source Skill (v1.1.0 — Model-Agnostic Hard-Gate Edition).

Key Hard-Gate Protections (preventing ChatGPT / GPT / other models from drifting into
low-density "AI Gamma/Keynote blog slides" or teal+orange AI-slop palettes):
  1. Strict Theme Lock (`enforce_palette=True`): rejects off-palette ad-hoc colors;
     defaults strictly to `executive-blue` unless user explicitly requests another theme.
  2. Anti-AI-Amber-Banner Gate: caps amber/orange area (<= 4.5% of slide) and max width
     (<= 240pt) so models CANNOT draw full-width orange callout banners at the bottom.
  3. Anti-Gamma-Header & Anti-Sparse-Slide Density Gate (`mode="tech-arch"` default):
     - Blocks oversized hero titles (> 19pt) and giant header whitespace
     - Enforces minimum structural density (>= 35 nodes, >= 6 orthogonal edges, >= 55% panel coverage)
     - Requires balanced multi-quadrant layout (not a sparse 2-column table)
  4. Anti-Circular Logic (`forbid_terms`), Anti-AI Blacklist (`DEFAULT_BANNED_WORDS`),
     Zero-Parenthesis, Orthogonal Edges, Single-Line & Overflow Checks.
  5. High-Level Architectural Layout Helpers (`add_arch_header`, `add_problem_goal_band`,
     `add_swimlane_shell`, `add_chip_module`, `add_header_strip_module`) so every model
     builds on a real high-density executive skeleton rather than improvising sparse slides.
"""
from __future__ import annotations

import base64
import html
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls, qn
from pptx.util import Pt

W_PT = 960.0
H_PT = 540.0
SLIDE_AREA = W_PT * H_PT

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# =============================================================================
# SWITCHABLE THEME SYSTEM (Default: executive-blue; Calm & Non-AI-Slop!)
# =============================================================================
DEFAULT_THEME_NAME = "executive-blue"

THEMES: Dict[str, Dict[str, str]] = {
    "executive-blue": {
        "navy_deep":  "#08306B",
        "navy":       "#0B3D91",
        "blue_main":  "#005EA8",
        "blue_mid":   "#0074C7",
        "blue_line":  "#3B82D6",
        "blue_soft":  "#D8EBFA",
        "blue_pale":  "#EBF4FC",
        "panel_bg":   "#F5F9FE",
        "border":     "#BDD5EE",
        "border_lt":  "#D6E6F6",
        "white":      "#FFFFFF",
        "text":       "#1E293B",
        "muted":      "#475569",
        "sub_white":  "#DCEEFF",
        "amber":      "#B85D00",
        "amber_bdr":  "#E59A38",
        "amber_bg":   "#FFF9EE",
        "amber_warn": "#FFF5E2",
    },
    "slate-minimal": {
        "navy_deep":  "#0F172A",
        "navy":       "#1E293B",
        "blue_main":  "#334155",
        "blue_mid":   "#2563EB",
        "blue_line":  "#64748B",
        "blue_soft":  "#E2E8F0",
        "blue_pale":  "#F1F5F9",
        "panel_bg":   "#F8FAFC",
        "border":     "#CBD5E1",
        "border_lt":  "#E2E8F0",
        "white":      "#FFFFFF",
        "text":       "#1E293B",
        "muted":      "#475569",
        "sub_white":  "#E2E8F0",
        "amber":      "#B45309",
        "amber_bdr":  "#D97706",
        "amber_bg":   "#FFFBEB",
        "amber_warn": "#FEF3C7",
    },
    # Toned-down cool steel-teal (explicit user opt-in only; avoids harsh AI green-teal glare)
    "steel-teal": {
        "navy_deep":  "#133B4A",
        "navy":       "#1A4F63",
        "blue_main":  "#20647A",
        "blue_mid":   "#2B7D96",
        "blue_line":  "#4F93A8",
        "blue_soft":  "#D8ECEF",
        "blue_pale":  "#ECF6F8",
        "panel_bg":   "#F5FAFB",
        "border":     "#BDD8DF",
        "border_lt":  "#D6E8EC",
        "white":      "#FFFFFF",
        "text":       "#1E293B",
        "muted":      "#475569",
        "sub_white":  "#DCF0F4",
        "amber":      "#B85D00",
        "amber_bdr":  "#E59A38",
        "amber_bg":   "#FFF9EE",
        "amber_warn": "#FFF5E2",
    },
    "academic-indigo": {
        "navy_deep":  "#19285E",
        "navy":       "#243B8A",
        "blue_main":  "#3451B2",
        "blue_mid":   "#4A67CC",
        "blue_line":  "#627CD9",
        "blue_soft":  "#DDE4FA",
        "blue_pale":  "#EEF2FD",
        "panel_bg":   "#F6F8FE",
        "border":     "#C4D0F0",
        "border_lt":  "#DCE3F8",
        "white":      "#FFFFFF",
        "text":       "#1E293B",
        "muted":      "#475569",
        "sub_white":  "#E0E7FF",
        "amber":      "#B85D00",
        "amber_bdr":  "#E59A38",
        "amber_bg":   "#FFF9EE",
        "amber_warn": "#FFF5E2",
    },
}

# Backward-compatible aliases
THEMES["deep-teal"] = THEMES["steel-teal"]
PALETTE = THEMES[DEFAULT_THEME_NAME]

NEUTRAL_ALLOWED_HEX: Set[str] = {
    "#FFFFFF", "#F8FAFC", "#F1F5F9", "#E2E8F0", "#CBD5E1", "#94A3B8", "#64748B", "#475569", "#334155", "#1E293B", "#0F172A",
}

DEFAULT_BANNED_WORDS: List[str] = [
    # AI buzzwords & empty corporate clichés
    "底座", "赋能", "拉通", "抓手", "闭环", "范式", "鸿沟", "断层", "锚点", "破题载体",
    # Colloquialisms / informal slang
    "撑不住", "把不住", "用不起来", "兜不住", "自由发挥", "写死", "脑补",
    # Arcane / awkward compressed jargon & grammatical bugs
    "直读", "只读", "编检", "守恒", "反译", "核极性", "加独立", "可算可跑",
    "封闭可终止", "强覆盖伤存量", "结构漂移", "多维索引", "归一依据", "归一引用",
    "物理量纲", "量纲", "纯度", "文法", "异构", "形式化", "未决", "无损", "裁决",
    "提案", "硬门禁", "程序硬检", "防漏增", "状态解耦", "拦截报差", "依赖闭合",
    "新项与差异", "语义混杂", "不可计算", "靠人审定", "靠人工审定", "靠人工兜底",
    # Toy business story / diluted blog-slide signals
    "例：", "例如", "难点：", "核心：", "技术一", "技术二", "技术三", "原话", "解析示意",
]


def get_theme(name: str = DEFAULT_THEME_NAME) -> Dict[str, str]:
    if name not in THEMES:
        raise ValueError(f"Unknown theme '{name}'. Available themes: {sorted(THEMES.keys())}")
    return dict(THEMES[name])


def build_theme(base: str = DEFAULT_THEME_NAME, overrides: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    t = get_theme(base)
    if overrides:
        t.update(overrides)
    return t


@dataclass
class TextRun:
    text: str
    color: str = PALETTE["text"]
    bold: bool = False
    size: Optional[float] = None


@dataclass
class ShapeNode:
    kind: str  # rect | rrect | ellipse | diamond | can | stadium | chevron_r | wedge_r | image
    x: float
    y: float
    w: float
    h: float
    fill: Optional[str] = None
    grad_fill: Optional[Tuple[str, str, int]] = None
    stroke: Optional[str] = None
    stroke_w: float = 0.85
    dashed: bool = False
    radius: float = 4.0
    text: str = ""
    runs: Optional[List[List[TextRun]]] = None
    font_size: float = 7.6
    font_color: str = PALETTE["text"]
    bold: bool = False
    align: str = "center"
    valign: str = "middle"
    pad_x: float = 3.5
    pad_y: float = 1.5
    line_spacing: float = 1.18
    image_path: Optional[str] = None
    single_line_each_para: bool = False
    forbid_terms: Sequence[str] = field(default_factory=tuple)
    allow_custom_color: bool = False  # Set True ONLY for brand header accent strips / logos


@dataclass
class Edge:
    points: List[Tuple[float, float]]
    stroke: str = PALETTE["blue_line"]
    stroke_w: float = 0.95
    dashed: bool = False
    arrow_start: bool = False
    arrow_end: bool = True


class Scene:
    def __init__(self, name: str, theme: Optional[Dict[str, str]] = None, theme_name: str = DEFAULT_THEME_NAME):
        self.name = name
        self.theme_name = theme_name if theme is None else "custom"
        self.theme: Dict[str, str] = dict(theme) if theme is not None else get_theme(theme_name)
        self.nodes: List[ShapeNode] = []
        self.edges: List[Edge] = []

    def add_node(self, *args, **kwargs):
        self.nodes.append(ShapeNode(*args, **kwargs))

    def add_edge(self, *args, **kwargs):
        if "stroke" not in kwargs:
            kwargs["stroke"] = self.theme["blue_line"]
        self.edges.append(Edge(*args, **kwargs))


def hex_to_rgb(hx: str) -> RGBColor:
    h = hx.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _is_warm_amber_hex(hx: Optional[str]) -> bool:
    """Detect orange / amber / yellow-beige warning colors (to cap AI-slop callout banners)."""
    if not hx or not hx.startswith("#") or len(hx) != 7:
        return False
    r, g, b = int(hx[1:3], 16), int(hx[3:5], 16), int(hx[5:7], 16)
    # Warm hue where red dominates blue strongly (orange/amber/peach/beige callouts)
    return (r - b) >= 24 and r >= 170 and g >= 85 and (r - g) <= 135


# =============================================================================
# HIGH-LEVEL ARCHITECTURAL FRAME & COMPONENT BUILDERS
# =============================================================================
def add_arch_header(
    s: Scene,
    title: str,
    accent_colors: Optional[Sequence[str]] = None,
    logo_path: Optional[str] = None,
):
    """Compact executive header (y=0..52, <= 10% height; blocks Gamma-style giant hero headers)."""
    t = s.theme
    title_w = 764 if logo_path else 928
    s.add_node(
        "rect", 16, 11, title_w, 32, align="left", valign="middle", pad_x=0, pad_y=0,
        single_line_each_para=True, text=title, font_size=16.2, font_color=t["navy"], bold=True,
    )
    bar_w = 762 if logo_path else 928
    if accent_colors:
        seg = bar_w / len(accent_colors)
        for i, col in enumerate(accent_colors):
            s.add_node("rect", 16 + i * seg, 48, seg, 2.2, fill=col, stroke_w=0, allow_custom_color=True)
    else:
        s.add_node("rect", 16, 48, bar_w * 0.35, 2.2, fill=t["navy_deep"], stroke_w=0)
        s.add_node("rect", 16 + bar_w * 0.35, 48, bar_w * 0.65, 2.2, fill=t["blue_main"], stroke_w=0)
    if logo_path:
        s.add_node("image", 786, 4, 156, 48, image_path=logo_path)


def add_problem_goal_band(
    s: Scene,
    problems: Sequence[Tuple[str, str]],
    goal_title: str,
    goal_sub: str,
    forbid_terms: Sequence[str] = (),
):
    """Top Problem -> Goal executive band (y=56..107, h=51) with anti-circular term guard."""
    t = s.theme
    s.add_node("rrect", 16, 56, 24, 51, fill=t["blue_main"], radius=4.0,
               text="问\n题", font_size=9.0, font_color=t["white"], bold=True, line_spacing=1.22, pad_x=1)
    p_count = max(len(problems), 1)
    p_total_w = 526.0
    gap = 6.0
    pw = (p_total_w - gap * (p_count - 1)) / p_count
    for idx, (pt, ps) in enumerate(problems):
        px = 45 + idx * (pw + gap)
        s.add_node("rrect", px, 56, pw, 51, fill=t["white"], stroke=t["border"], stroke_w=0.9, radius=4.5)
        s.add_node("rrect", px + 8, 69, 24, 24, fill=t["blue_pale"], stroke=t["border"], stroke_w=0.75, radius=12.0,
                   text=f"0{idx+1}", font_size=7.4, font_color=t["blue_main"], bold=True, pad_x=0)
        s.add_node("rect", px + 38, 58, pw - 44, 47, align="left", valign="middle", pad_x=1, pad_y=1,
                   line_spacing=1.20, forbid_terms=forbid_terms,
                   runs=[
                       [TextRun(pt, color=t["navy"], bold=True, size=8.2)],
                       [TextRun(ps, color=t["text"], size=6.7)],
                   ])
    s.add_node("chevron_r", 577, 72, 14, 19, fill=t["blue_line"])
    s.add_node("rrect", 597, 56, 24, 51, fill=t["blue_main"], radius=4.0,
               text="目\n标", font_size=9.0, font_color=t["white"], bold=True, line_spacing=1.22, pad_x=1)
    s.add_node("rrect", 626, 56, 318, 51, fill=t["blue_main"], radius=4.5)
    s.add_node("rect", 636, 58, 298, 47, align="left", valign="middle", pad_x=1, pad_y=1, line_spacing=1.24,
               runs=[
                   [TextRun(goal_title, color=t["white"], bold=True, size=9.2)],
                   [TextRun(goal_sub, color=t["sub_white"], size=6.7)],
               ])


def add_swimlane_shell(
    s: Scene,
    x: float,
    y: float,
    w: float,
    h: float,
    vertical_label: str,
    dark: bool = False,
    icon_path: Optional[str] = None,
):
    """Calm panel-bg swimlane shell with vertical colored left tab."""
    t = s.theme
    tab_fill = t["navy_deep"] if dark else t["blue_main"]
    bdr = t["blue_line"] if dark else t["border"]
    s.add_node("rrect", x, y, w, h, fill=t["panel_bg"], stroke=bdr, stroke_w=0.85, radius=4.5)
    s.add_node("rrect", x + 2, y + 2, 24, h - 4, fill=tab_fill, radius=4.0)
    if icon_path:
        s.add_node("image", x + 7, y + 8, 14, 14, image_path=icon_path)
        s.add_node("rect", x + 2, y + 24, 24, h - 28, text=vertical_label,
                   font_size=7.5, font_color=t["white"], bold=True, line_spacing=1.18, pad_x=1)
    else:
        s.add_node("rect", x + 2, y + 4, 24, h - 8, text=vertical_label,
                   font_size=7.6, font_color=t["white"], bold=True, line_spacing=1.22, pad_x=1)


def add_labeled_box(
    s: Scene,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    sub: str = "",
    fill: Optional[str] = None,
    stroke: Optional[str] = None,
    stroke_w: float = 0.85,
    title_color: Optional[str] = None,
    sub_color: Optional[str] = None,
    title_size: float = 6.3,
    sub_size: float = 5.2,
    radius: float = 3.2,
    dashed: bool = False,
    forbid_terms: Sequence[str] = (),
):
    t = s.theme
    _fill = t["white"] if fill is None else fill
    _stroke = t["blue_line"] if stroke is None else (None if stroke == "none" else stroke)
    _tc = t["navy"] if title_color is None else title_color
    _sc = t["muted"] if sub_color is None else sub_color
    s.add_node("rrect", x, y, w, h, fill=_fill, stroke=_stroke, stroke_w=stroke_w, dashed=dashed, radius=radius)
    if sub:
        runs = [[TextRun(line, color=_tc, bold=True, size=title_size)] for line in title.split("\n")]
        runs += [[TextRun(line, color=_sc, bold=False, size=sub_size)] for line in sub.split("\n")]
        s.add_node(
            "rect", x + 1, y + 1, w - 2, h - 2, fill=None, stroke=None,
            align="center", valign="middle", pad_x=2, pad_y=0.5, line_spacing=1.14,
            runs=runs, forbid_terms=forbid_terms,
        )
    else:
        s.add_node(
            "rect", x + 1, y + 1, w - 2, h - 2, fill=None, stroke=None,
            align="center", valign="middle", pad_x=2, pad_y=0.5, line_spacing=1.14,
            text=title, font_size=title_size, font_color=_tc, bold=True,
            forbid_terms=forbid_terms,
        )


def add_chip_module(
    s: Scene,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    chips: Sequence[str],
    cols: Optional[int] = None,
    stroke: Optional[str] = None,
    title_size: float = 6.2,
    chip_size: float = 5.1,
):
    """Structured compact module: crisp title + inner micro-tag chips (eliminates hollow bricks)."""
    t = s.theme
    s.add_node("rrect", x, y, w, h, fill=t["white"], stroke=stroke or t["blue_line"], stroke_w=0.85, radius=3.5)
    s.add_node(
        "rect", x + 2, y + 1.5, w - 4, 12, fill=None, stroke=None,
        text=title, font_size=title_size, font_color=t["navy"], bold=True,
        pad_x=0, pad_y=0, single_line_each_para=True,
    )
    n_cols = cols or len(chips)
    n_rows = (len(chips) + n_cols - 1) // n_cols
    gap = 3.5
    inner_x = x + 4
    inner_w = w - 8
    chip_w = (inner_w - gap * (n_cols - 1)) / n_cols
    start_y = y + 15.0
    avail_h = max(h - 18.0, 11.0)
    chip_h = (avail_h - gap * (n_rows - 1)) / n_rows
    for idx, ctxt in enumerate(chips):
        r, c = idx // n_cols, idx % n_cols
        cx = inner_x + c * (chip_w + gap)
        cy = start_y + r * (chip_h + gap)
        s.add_node(
            "rrect", cx, cy, chip_w, chip_h, fill=t["panel_bg"], stroke=t["border"],
            stroke_w=0.65, radius=2.0, text=ctxt, font_size=chip_size, font_color=t["text"],
            bold=True, pad_x=0, pad_y=0, single_line_each_para=True,
        )


def add_header_strip_module(
    s: Scene,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    lines: Sequence[str],
    header_fill: Optional[str] = None,
    stroke: Optional[str] = None,
):
    """Solid-header crisp card + soft tinted horizontal rows (eliminates heavy solid slabs)."""
    t = s.theme
    hf = header_fill or t["blue_main"]
    s.add_node("rrect", x, y, w, h, fill=t["white"], stroke=stroke or hf, stroke_w=0.9, radius=3.5)
    s.add_node(
        "rrect", x + 1, y + 1, w - 2, 13.5, fill=hf, stroke=None, radius=2.5,
        text=title, font_size=6.0, font_color=t["white"], bold=True,
        pad_x=0, pad_y=0, single_line_each_para=True,
    )
    gap = 2.2
    start_y = y + 16.5
    avail_h = max(h - 18.5, 10.0)
    row_h = (avail_h - gap * max(len(lines) - 1, 0)) / max(len(lines), 1)
    for idx, txt in enumerate(lines):
        ry = start_y + idx * (row_h + gap)
        s.add_node(
            "rrect", x + 3, ry, w - 6, row_h, fill=t["blue_pale"], stroke=t["border"],
            stroke_w=0.6, radius=2.0, text=txt, font_size=5.1, font_color=t["navy"],
            bold=True, pad_x=0, pad_y=0, single_line_each_para=True,
        )


# =============================================================================
# AUTOMATED SELF-CHECK GATE (TEXT + GEOMETRY + COLOR DISCIPLINE + DENSITY)
# =============================================================================
NO_LINE_START = set("，。、；：！？）》】”’,.!?;:)]}")


def wrap_text_cn(text: str, max_pt: float, font_pt: float) -> List[str]:
    lines = []
    for raw in text.split("\n"):
        if not raw:
            lines.append("")
            continue
        cur, cur_w = "", 0.0
        for ch in raw:
            cw = font_pt * (0.58 if ord(ch) < 128 else 1.0)
            if cur and cur_w + cw > max_pt and ch not in NO_LINE_START:
                lines.append(cur)
                cur, cur_w = ch, cw
            else:
                cur += ch
                cur_w += cw
        if cur:
            lines.append(cur)
    return lines


def wrap_runs_cn(pruns: List[TextRun], max_pt: float, default_fs: float) -> List[Tuple[List[TextRun], float]]:
    out_lines: List[Tuple[List[TextRun], float]] = []
    cur_runs: List[TextRun] = []
    cur_w, cur_max_fs = 0.0, default_fs

    def flush():
        nonlocal cur_runs, cur_w, cur_max_fs
        if cur_runs:
            out_lines.append((cur_runs, cur_max_fs))
            cur_runs, cur_w, cur_max_fs = [], 0.0, default_fs

    for run in pruns:
        fs = run.size or default_fs
        for part_idx, part in enumerate(run.text.split("\n")):
            if part_idx > 0:
                flush()
            buf = ""
            for ch in part:
                cw = fs * (0.58 if ord(ch) < 128 else 1.0)
                if (cur_runs or buf) and cur_w + cw > max_pt and ch not in NO_LINE_START:
                    if buf:
                        cur_runs.append(TextRun(buf, run.color, run.bold, fs))
                        cur_max_fs = max(cur_max_fs, fs)
                        buf = ""
                    flush()
                buf += ch
                cur_w += cw
                cur_max_fs = max(cur_max_fs, fs)
            if buf:
                cur_runs.append(TextRun(buf, run.color, run.bold, fs))
                cur_max_fs = max(cur_max_fs, fs)
    flush()
    return out_lines


def run_self_check(
    scene: Scene,
    mode: str = "tech-arch",  # "tech-arch" (strict high-density executive gate) | "minimal" (unit test only)
    extra_banned_words: Iterable[str] = (),
    allow_parens: bool = False,
    enforce_palette: bool = True,
    min_nodes: int = 35,
    min_edges: int = 6,
    max_amber_area_ratio: float = 0.045,
    max_amber_width_pt: float = 240.0,
    max_title_font_pt: float = 19.0,
):
    banned = list(DEFAULT_BANNED_WORDS) + list(extra_banned_words)
    allowed_colors: Set[str] = {v.upper() for v in scene.theme.values()} | NEUTRAL_ALLOWED_HEX
    errors: List[str] = []

    # 1. Orthogonal Edge Gate
    for eidx, e in enumerate(scene.edges):
        for i in range(len(e.points) - 1):
            x1, y1 = e.points[i]
            x2, y2 = e.points[i + 1]
            if abs(x1 - x2) > 0.5 and abs(y1 - y2) > 0.5:
                errors.append(f"[Edge {eidx}] Diagonal line forbidden: ({x1},{y1})->({x2},{y2})")
        if enforce_palette and e.stroke.upper() not in allowed_colors:
            errors.append(f"[Edge {eidx}] Off-palette edge color '{e.stroke}' not in theme '{scene.theme_name}'")

    amber_area = 0.0
    quadrant_hits = [0, 0, 0, 0]  # TL, TR, BL, BR
    filled_panel_area = 0.0

    for idx, n in enumerate(scene.nodes):
        # 2. Strict Palette Discipline & Anti-AI-Amber-Banner Gate
        if enforce_palette and not n.allow_custom_color:
            for attr_name, col in (("fill", n.fill), ("stroke", n.stroke)):
                if col and col.upper() not in allowed_colors:
                    errors.append(
                        f"[Node {idx}] Off-palette {attr_name} '{col}' forbidden! "
                        f"Use scene.theme tokens (active theme='{scene.theme_name}')."
                    )
            if n.grad_fill:
                for gc in (n.grad_fill[0], n.grad_fill[1]):
                    if gc.upper() not in allowed_colors:
                        errors.append(f"[Node {idx}] Off-palette gradient stop '{gc}' not in theme '{scene.theme_name}'")

        if _is_warm_amber_hex(n.fill) or _is_warm_amber_hex(n.stroke):
            amber_area += n.w * n.h
            if n.w > max_amber_width_pt:
                errors.append(
                    f"[Node {idx}] Anti-AI-slop gate: wide amber/orange callout banner forbidden "
                    f"(w={n.w:.1f}pt > {max_amber_width_pt:.0f}pt). Reserve amber strictly for small exception nodes!"
                )

        # Track visual density across 4 slide quadrants (excluding top header y < 54)
        if n.y >= 54 and (n.fill or n.stroke or n.text or n.runs):
            cx, cy = n.x + n.w / 2.0, n.y + n.h / 2.0
            q = (0 if cy < H_PT / 2.0 else 2) + (0 if cx < W_PT / 2.0 else 1)
            quadrant_hits[q] += 1
            if n.fill and n.w >= 40 and n.h >= 20:
                filled_panel_area += n.w * n.h

        # 3. Anti-Oversized-Gamma-Hero-Title Gate
        if mode == "tech-arch":
            if n.font_size > max_title_font_pt:
                errors.append(
                    f"[Node {idx}] Oversized Gamma-style title ({n.font_size}pt > {max_title_font_pt}pt) "
                    f"wastes vertical budget in tech-arch mode."
                )
            if n.runs:
                for pr in n.runs:
                    for r in pr:
                        if r.size and r.size > max_title_font_pt:
                            errors.append(
                                f"[Node {idx}] Oversized text run ({r.size}pt > {max_title_font_pt}pt) in tech-arch mode."
                            )

        # 4. Text / Anti-Circular / Anti-AI / Overflow Gate
        all_txt = n.text
        if n.runs:
            all_txt += "\n" + "\n".join("".join(r.text for r in pr) for pr in n.runs)
        if not all_txt.strip():
            continue

        for ft in n.forbid_terms:
            if ft.lower() in all_txt.lower():
                errors.append(f"[Node {idx}] Circular logic! Term '{ft}' forbidden here: {all_txt!r}")

        if not allow_parens:
            for p in ("（", "）", "(", ")"):
                if p in all_txt:
                    errors.append(f"[Node {idx}] Parenthesis '{p}' forbidden: {all_txt!r}")

        for bw in banned:
            if bw and bw in all_txt:
                errors.append(f"[Node {idx}] Banned AI/colloquial phrase '{bw}' found in: {all_txt!r}")

        max_w = max(n.w - 2 * n.pad_x, 8.0)
        rendered: List[Tuple[List[TextRun], float]] = []
        if n.runs:
            for pr in n.runs:
                wrapped = wrap_runs_cn(pr, max_w, n.font_size)
                if n.single_line_each_para and len(wrapped) > 1:
                    errors.append(f"[Node {idx}] Expected single-line paragraph but wrapped: {''.join(r.text for r in pr)!r}")
                rendered.extend(wrapped)
        else:
            for raw_p in n.text.split("\n"):
                wrapped_p = wrap_text_cn(raw_p, max_w, n.font_size)
                if n.single_line_each_para and len(wrapped_p) > 1:
                    errors.append(f"[Node {idx}] Expected single-line text but wrapped: {raw_p!r}")
                for ln in wrapped_p:
                    rendered.append(([TextRun(ln, n.font_color, n.bold, n.font_size)], n.font_size))

        total_h = sum(fs * n.line_spacing for _, fs in rendered)
        avail_h = n.h - 2 * n.pad_y + 2.5
        if total_h > avail_h:
            errors.append(f"[Node {idx}] Text overflow ({total_h:.1f}pt > {avail_h:.1f}pt): {all_txt[:45]!r}")

    # 5. Slide-Level Amber Area Cap
    amber_ratio = amber_area / SLIDE_AREA
    if amber_ratio > max_amber_area_ratio:
        errors.append(
            f"[Slide] Amber/orange area ratio too high ({amber_ratio:.1%} > {max_amber_area_ratio:.1%}). "
            "Do NOT use orange/amber as a major theme or banner color!"
        )

    # 6. High-Density Technical Architecture Floor (blocks sparse ChatGPT blog-post slides!)
    if mode == "tech-arch":
        if len(scene.nodes) < min_nodes:
            errors.append(
                f"[Density] Slide too sparse ({len(scene.nodes)} nodes < {min_nodes}). "
                "Do NOT generate a diluted 2-column blog slide! Use full Problem->Goal + Challenges + Technical Swimlanes."
            )
        if len(scene.edges) < min_edges:
            errors.append(
                f"[Density] Too few technical flow connectors ({len(scene.edges)} edges < {min_edges}). "
                "Technical architecture slides must show real data/control mechanisms, not static text tables."
            )
        empty_quads = [i for i, cnt in enumerate(quadrant_hits) if cnt < 3]
        if empty_quads:
            errors.append(
                f"[Density] Unbalanced whitespace: quadrants {empty_quads} have <3 nodes ({quadrant_hits}). "
                "Fill all 4 quadrants cleanly with balanced architectural zones."
            )
        if filled_panel_area / SLIDE_AREA < 0.55:
            errors.append(
                f"[Density] Too much empty canvas (panel coverage {filled_panel_area/SLIDE_AREA:.0%} < 55%)."
            )

    if errors:
        raise AssertionError("SELF-CHECK FAILED:\n  " + "\n  ".join(errors))
    print(
        f"SELF-CHECK PASSED [{mode} | theme={scene.theme_name}]: "
        f"{len(scene.nodes)} nodes, {len(scene.edges)} orthogonal edges, "
        f"amber={amber_ratio:.1%}, quads={quadrant_hits} (0 errors)."
    )


# =============================================================================
# TRANSPARENT VECTOR ICON GENERATOR
# =============================================================================
def generate_svg_icons(icon_specs: Dict[str, Tuple[str, str]], out_dir: str, size_px: int = 96):
    os.makedirs(out_dir, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        for name, (col, body) in icon_specs.items():
            html_p = os.path.join(td, f"{name}.html")
            out_p = os.path.join(out_dir, f"{name}.png")
            svg = (
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{size_px}" height="{size_px}" '
                f'viewBox="0 0 24 24" fill="none" stroke="{col}" stroke-width="2.1" '
                f'stroke-linecap="round" stroke-linejoin="round">{body}</svg>'
            )
            with open(html_p, "w", encoding="utf-8") as f:
                f.write(
                    f'<!DOCTYPE html><html><body style="margin:0;padding:0;background:transparent;'
                    f'width:{size_px}px;height:{size_px}px;overflow:hidden">{svg}</body></html>'
                )
            subprocess.run(
                [
                    CHROME_BIN, "--headless=new", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", f"--window-size={size_px},{size_px}",
                    "--force-device-scale-factor=1", "--default-background-color=00000000",
                    f"--screenshot={out_p}", f"file://{html_p}",
                ],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )


# =============================================================================
# SVG & NATIVE EDITABLE PPTX COMPILERS
# =============================================================================
def export_svg(scene: Scene, out_path: str):
    t = scene.theme
    grad_defs, grad_map = [], {}

    def get_grad_id(g: Tuple[str, str, int]) -> str:
        if g not in grad_map:
            gid = f"grad_{len(grad_map)}"
            grad_map[g] = gid
            c1, c2, ang = g
            x2, y2 = ("1", "0") if ang == 0 else ("0", "1")
            grad_defs.append(
                f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">'
                f'<stop offset="0%" stop-color="{c1}"/><stop offset="100%" stop-color="{c2}"/></linearGradient>'
            )
        return grad_map[g]

    for n in scene.nodes:
        if n.grad_fill:
            get_grad_id(n.grad_fill)

    marker_defs = [
        f'<marker id="arr_{mc.lstrip("#")}" viewBox="0 0 10 10" refX="8.5" refY="5" '
        f'markerWidth="4.8" markerHeight="4.8" orient="auto-start-reverse">'
        f'<path d="M 0 1.2 L 9.5 5 L 0 8.8 z" fill="{mc}"/></marker>'
        for mc in sorted({e.stroke for e in scene.edges})
    ]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 {W_PT} {H_PT}">',
        "<defs>",
        '<style>text{font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Helvetica Neue",sans-serif;}</style>',
        *grad_defs, *marker_defs,
        "</defs>",
        f'<rect x="0" y="0" width="{W_PT}" height="{H_PT}" fill="#FFFFFF"/>',
    ]

    for n in scene.nodes:
        if n.kind == "image" and n.image_path:
            b64 = base64.b64encode(open(n.image_path, "rb").read()).decode("ascii")
            parts.append(
                f'<image x="{n.x:.2f}" y="{n.y:.2f}" width="{n.w:.2f}" height="{n.h:.2f}" '
                f'href="data:image/png;base64,{b64}" preserveAspectRatio="xMidYMid meet"/>'
            )
            continue

        fill_attr = f'fill="url(#{get_grad_id(n.grad_fill)})"' if n.grad_fill else (f'fill="{n.fill}"' if n.fill else 'fill="none"')
        stroke_attr = f'stroke="{n.stroke}" stroke-width="{n.stroke_w}"' if n.stroke and n.stroke_w > 0 else 'stroke="none"'
        dash_attr = ' stroke-dasharray="3.5,2.5"' if n.dashed else ""

        if n.kind == "rect":
            if n.fill or n.grad_fill or (n.stroke and n.stroke_w > 0):
                parts.append(f'<rect x="{n.x:.2f}" y="{n.y:.2f}" width="{n.w:.2f}" height="{n.h:.2f}" {fill_attr} {stroke_attr}{dash_attr}/>')
        elif n.kind == "rrect":
            parts.append(f'<rect x="{n.x:.2f}" y="{n.y:.2f}" width="{n.w:.2f}" height="{n.h:.2f}" rx="{n.radius:.2f}" ry="{n.radius:.2f}" {fill_attr} {stroke_attr}{dash_attr}/>')
        elif n.kind == "stadium":
            rad = n.h / 2.0
            parts.append(f'<rect x="{n.x:.2f}" y="{n.y:.2f}" width="{n.w:.2f}" height="{n.h:.2f}" rx="{rad:.2f}" ry="{rad:.2f}" {fill_attr} {stroke_attr}{dash_attr}/>')
        elif n.kind == "ellipse":
            parts.append(f'<ellipse cx="{n.x+n.w/2:.2f}" cy="{n.y+n.h/2:.2f}" rx="{n.w/2:.2f}" ry="{n.h/2:.2f}" {fill_attr} {stroke_attr}{dash_attr}/>')
        elif n.kind == "diamond":
            cx, cy_m = n.x + n.w / 2.0, n.y + n.h / 2.0
            pts = f"{cx:.2f},{n.y:.2f} {n.x+n.w:.2f},{cy_m:.2f} {cx:.2f},{n.y+n.h:.2f} {n.x:.2f},{cy_m:.2f}"
            parts.append(f'<polygon points="{pts}" {fill_attr} {stroke_attr}{dash_attr}/>')
        elif n.kind == "can":
            ry = min(6.0, n.h * 0.16)
            cx = n.x + n.w / 2.0
            bdr = n.stroke or t["blue_line"]
            parts.append(
                f'<path d="M {n.x:.2f} {n.y+ry:.2f} L {n.x:.2f} {n.y+n.h-ry:.2f} '
                f'A {n.w/2:.2f} {ry:.2f} 0 0 0 {n.x+n.w:.2f} {n.y+n.h-ry:.2f} '
                f'L {n.x+n.w:.2f} {n.y+ry:.2f} Z" fill="{n.fill or t["white"]}" stroke="{bdr}" stroke-width="{n.stroke_w}"/>'
            )
            parts.append(
                f'<ellipse cx="{cx:.2f}" cy="{n.y+ry:.2f}" rx="{n.w/2:.2f}" ry="{ry:.2f}" '
                f'fill="{t["blue_pale"]}" stroke="{bdr}" stroke-width="{n.stroke_w}"/>'
            )
        elif n.kind == "wedge_r":
            pts = f"{n.x:.2f},{n.y:.2f} {n.x+n.w:.2f},{n.y+n.h*0.5:.2f} {n.x:.2f},{n.y+n.h:.2f}"
            parts.append(f'<polygon points="{pts}" {fill_attr} stroke="none"/>')
        elif n.kind == "chevron_r":
            pts = (
                f"{n.x:.2f},{n.y+n.h*0.24:.2f} {n.x+n.w*0.52:.2f},{n.y+n.h*0.24:.2f} "
                f"{n.x+n.w*0.52:.2f},{n.y:.2f} {n.x+n.w:.2f},{n.y+n.h*0.5:.2f} "
                f"{n.x+n.w*0.52:.2f},{n.y+n.h:.2f} {n.x+n.w*0.52:.2f},{n.y+n.h*0.76:.2f} "
                f"{n.x:.2f},{n.y+n.h*0.76:.2f}"
            )
            parts.append(f'<polygon points="{pts}" {fill_attr} {stroke_attr}/>')

        if n.runs or n.text:
            max_w = max(n.w - 2 * n.pad_x, 8.0)
            rendered_lines: List[Tuple[List[TextRun], float]] = []
            if n.runs:
                for pruns in n.runs:
                    rendered_lines.extend(wrap_runs_cn(pruns, max_w, n.font_size))
            else:
                for ln in wrap_text_cn(n.text, max_w, n.font_size):
                    rendered_lines.append(([TextRun(ln, n.font_color, n.bold, n.font_size)], n.font_size))

            line_heights = [fs * n.line_spacing for _, fs in rendered_lines]
            total_h = sum(line_heights)
            y_offset = (min(6.0, n.h * 0.16) * 1.4) if n.kind == "can" else 0.0
            cur_y = (
                n.y + n.pad_y + y_offset if n.valign == "top"
                else (n.y + n.h - n.pad_y - total_h if n.valign == "bottom" else n.y + y_offset + (n.h - y_offset - total_h) / 2.0)
            )
            anchor = {"left": "start", "center": "middle", "right": "end"}[n.align]
            tx = n.x + n.pad_x if n.align == "left" else (n.x + n.w - n.pad_x if n.align == "right" else n.x + n.w / 2.0)

            for (rlist, fs), lh in zip(rendered_lines, line_heights):
                baseline_y = cur_y + lh * 0.78
                tspans = [
                    f'<tspan fill="{r.color}" font-size="{(r.size or fs):.2f}" '
                    f'font-weight="{"700" if r.bold else "400"}" xml:space="preserve">{html.escape(r.text)}</tspan>'
                    for r in rlist
                ]
                parts.append(f'<text x="{tx:.2f}" y="{baseline_y:.2f}" text-anchor="{anchor}">{"".join(tspans)}</text>')
                cur_y += lh

    for e in scene.edges:
        d = " ".join((f"M {px:.2f} {py:.2f}" if i == 0 else f"L {px:.2f} {py:.2f}") for i, (px, py) in enumerate(e.points))
        mid = "arr_" + e.stroke.lstrip("#")
        dash = ' stroke-dasharray="3.2,2.2"' if e.dashed else ""
        me = f' marker-end="url(#{mid})"' if e.arrow_end else ""
        ms = f' marker-start="url(#{mid})"' if e.arrow_start else ""
        parts.append(f'<path d="{d}" fill="none" stroke="{e.stroke}" stroke-width="{e.stroke_w}"{dash}{ms}{me}/>')

    parts.append("</svg>")
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))


def _set_ea_font(run, font_name: str = "PingFang SC"):
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:latin", "a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            rPr.append(parse_xml(f'<{tag} {nsdecls("a")} typeface="{font_name}"/>'))
        else:
            el.set("typeface", font_name)


def _apply_grad_fill(shape, c1_hex: str, c2_hex: str, angle_deg: int, rot_with_shape: bool = True):
    spPr = shape._element.spPr
    for tag in ("a:solidFill", "a:gradFill", "a:noFill"):
        old = spPr.find(qn(tag))
        if old is not None:
            spPr.remove(old)
    ang = int((angle_deg % 360) * 60000)
    rw = "1" if rot_with_shape else "0"
    gf = parse_xml(
        f'<a:gradFill {nsdecls("a")} rotWithShape="{rw}">'
        f'<a:gsLst><a:gs pos="0"><a:srgbClr val="{c1_hex.lstrip("#")}"/></a:gs>'
        f'<a:gs pos="100000"><a:srgbClr val="{c2_hex.lstrip("#")}"/></a:gs></a:gsLst>'
        f'<a:lin ang="{ang}" scaled="1"/></a:gradFill>'
    )
    ln = spPr.find(qn("a:ln"))
    if ln is not None:
        spPr.insert(list(spPr).index(ln), gf)
    else:
        spPr.append(gf)


def _add_arrow_heads(connector, start: bool, end: bool):
    ln = connector._element.spPr.find(qn("a:ln"))
    if ln is None:
        ln = parse_xml(f'<a:ln {nsdecls("a")}/>')
        connector._element.spPr.append(ln)
    if start:
        ln.append(parse_xml(f'<a:headEnd {nsdecls("a")} type="triangle" w="sm" len="sm"/>'))
    if end:
        ln.append(parse_xml(f'<a:tailEnd {nsdecls("a")} type="triangle" w="sm" len="sm"/>'))


def export_pptx(scene: Scene, out_path: str, font_name: str = "PingFang SC"):
    prs = Presentation()
    prs.slide_width = Pt(W_PT)
    prs.slide_height = Pt(H_PT)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    align_map = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}
    valign_map = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}

    for n in scene.nodes:
        if n.kind == "image" and n.image_path:
            slide.shapes.add_picture(n.image_path, Pt(n.x), Pt(n.y), Pt(n.w), Pt(n.h))
            continue

        mso = {
            "rect": MSO_SHAPE.RECTANGLE,
            "rrect": MSO_SHAPE.ROUNDED_RECTANGLE,
            "stadium": MSO_SHAPE.ROUNDED_RECTANGLE,
            "ellipse": MSO_SHAPE.OVAL,
            "diamond": MSO_SHAPE.DIAMOND,
            "can": MSO_SHAPE.CAN,
            "chevron_r": MSO_SHAPE.RIGHT_ARROW,
            "wedge_r": MSO_SHAPE.ISOSCELES_TRIANGLE,
        }.get(n.kind, MSO_SHAPE.RECTANGLE)

        if n.kind == "wedge_r":
            cx_w, cy_w = n.x + n.w / 2.0, n.y + n.h / 2.0
            sh = slide.shapes.add_shape(mso, Pt(cx_w - n.h / 2.0), Pt(cy_w - n.w / 2.0), Pt(n.h), Pt(n.w))
            sh.rotation = 90.0
        else:
            sh = slide.shapes.add_shape(mso, Pt(n.x), Pt(n.y), Pt(n.w), Pt(n.h))

        sh.shadow.inherit = False
        if n.kind == "rrect" and len(sh.adjustments) > 0:
            sh.adjustments[0] = min(0.5, n.radius / max(min(n.w, n.h), 1.0))
        elif n.kind == "stadium" and len(sh.adjustments) > 0:
            sh.adjustments[0] = 0.5
        elif n.kind == "can" and len(sh.adjustments) > 0:
            sh.adjustments[0] = 0.20

        if n.grad_fill:
            c1, c2, ang = n.grad_fill
            _apply_grad_fill(sh, c1, c2, 270 if n.kind == "wedge_r" else ang, rot_with_shape=True)
        elif n.fill:
            sh.fill.solid()
            sh.fill.fore_color.rgb = hex_to_rgb(n.fill)
        else:
            sh.fill.background()

        if n.stroke and n.stroke_w > 0:
            sh.line.color.rgb = hex_to_rgb(n.stroke)
            sh.line.width = Pt(n.stroke_w)
            if n.dashed:
                sh.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        else:
            sh.line.fill.background()

        if n.runs or n.text:
            tf = sh.text_frame
            tf.word_wrap = True
            tf.vertical_anchor = valign_map[n.valign]
            tf.margin_left = Pt(n.pad_x)
            tf.margin_right = Pt(n.pad_x)
            tf.margin_top = Pt(1.0 if n.kind == "can" else n.pad_y)
            tf.margin_bottom = Pt(1.0 if n.kind == "can" else n.pad_y)
            tf.clear()

            paras = n.runs if n.runs else [[TextRun(line, n.font_color, n.bold, n.font_size)] for line in n.text.split("\n")]
            for pi, pruns in enumerate(paras):
                p = tf.paragraphs[0] if pi == 0 else tf.add_paragraph()
                p.alignment = align_map[n.align]
                p.line_spacing = n.line_spacing
                p.space_before = Pt(0)
                p.space_after = Pt(0.8) if (pi == 0 and len(paras) > 1 and n.runs is not None) else Pt(0.2)
                if pi == len(paras) - 1:
                    p.space_after = Pt(0)
                for rspec in pruns:
                    r = p.add_run()
                    r.text = rspec.text
                    r.font.size = Pt(rspec.size or n.font_size)
                    r.font.bold = rspec.bold
                    r.font.color.rgb = hex_to_rgb(rspec.color)
                    r.font.name = font_name
                    _set_ea_font(r, font_name)

    for e in scene.edges:
        for i in range(len(e.points) - 1):
            x1, y1 = e.points[i]
            x2, y2 = e.points[i + 1]
            conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Pt(x1), Pt(y1), Pt(x2), Pt(y2))
            conn.line.color.rgb = hex_to_rgb(e.stroke)
            conn.line.width = Pt(e.stroke_w)
            if e.dashed:
                conn.line.dash_style = MSO_LINE_DASH_STYLE.DASH
            _add_arrow_heads(conn, e.arrow_start and i == 0, e.arrow_end and i == len(e.points) - 2)

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    prs.save(out_path)


# =============================================================================
# ARCHIVE + REAL QUICKLOOK RENDER + DETAIL CROP QA
# =============================================================================
def archive_before_overwrite(pptx_path: str, archive_dir: Optional[str] = None) -> Optional[str]:
    if not os.path.exists(pptx_path):
        return None
    base_dir = os.path.dirname(os.path.abspath(pptx_path))
    arch = archive_dir or os.path.join(base_dir, "archive")
    os.makedirs(arch, exist_ok=True)
    stem = os.path.splitext(os.path.basename(pptx_path))[0]
    ver = 1
    while os.path.exists(os.path.join(arch, f"{stem}_v{ver}.pptx")):
        ver += 1
    dst = os.path.join(arch, f"{stem}_v{ver}.pptx")
    shutil.copy2(pptx_path, dst)
    return dst


def render_quicklook_and_crop(
    pptx_path: str,
    out_dir: str,
    crops: Optional[Dict[str, Tuple[float, float, float, float]]] = None,
    size: int = 1920,
) -> Dict[str, str]:
    from PIL import Image

    os.makedirs(out_dir, exist_ok=True)
    subprocess.run(
        ["qlmanage", "-t", "-s", str(size), "-o", out_dir, pptx_path],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    full_png = os.path.join(out_dir, os.path.basename(pptx_path) + ".png")
    results = {"full": full_png}
    if crops:
        im = Image.open(full_png)
        w, h = im.size
        for cname, (fx0, fy0, fx1, fy1) in crops.items():
            cp = os.path.join(out_dir, f"crop_{cname}.png")
            im.crop((int(w * fx0), int(h * fy0), int(w * fx1), int(h * fy1))).save(cp)
            results[cname] = cp
    return results
