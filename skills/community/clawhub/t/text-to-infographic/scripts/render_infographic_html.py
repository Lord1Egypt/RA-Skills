#!/usr/bin/env python3
"""render_infographic_html.py — plan JSON → 自包含静态 HTML 信息图。

约束（即「安全渲染」叙事的技术承诺）：
- 仅 HTML + 内联 CSS + 内联 SVG（几何布局用），零 JavaScript；
- 零外部请求：无 CDN、无字体外链、无图片外链；
- 零依赖：仅 Python 标准库，无 pip 安装；
- 中文优先字体栈，print-safe。

v1.4.0（B 方向）新增可选 `--png`：调用本机已有浏览器截图出 PNG（小红书/公众号直发）。
- 可选能力：不安装任何浏览器；找不到就报错退出，**HTML 主路径不受影响**；
- 产物契约不变：PNG 由 HTML 截图而来，页面本身仍是零 JS 零外链。

用法:
    python3 render_infographic_html.py plan.json [out.html] [--png [OUT.png]] [--scale N]
    cat plan.json | python3 render_infographic_html.py - out.html
    python3 render_infographic_html.py plan.json out.html --png    # 同目录同名 .png

--png 相关：
    --png            出 PNG（省略值时用 out.html 同目录同名 .png；stdout 模式下不可省略）
    --scale N        像素密度倍数（默认 2，即 2x 图）
    --width N        视口宽（默认 852 = 卡片 820 + 页边距 32）
    --chrome PATH    显式指定浏览器路径（也可用环境变量 CHROME_PATH）
"""
import json
import math
import re
import sys
from html import escape

# ---------------------------------------------------------------- palettes
PALETTES = {
    "terracotta": {"accent": "#C96F4A", "accent2": "#E8A87C", "bg": "#FBF7F2",
                    "ink": "#2B2622", "muted": "#8A7F76", "line": "#E5D9CD"},
    "ocean":      {"accent": "#2C6E8F", "accent2": "#7FB6CF", "bg": "#F4F8FA",
                    "ink": "#1F2A30", "muted": "#71848E", "line": "#D6E4EC"},
    "forest":     {"accent": "#3E6B4F", "accent2": "#8FB996", "bg": "#F5F8F4",
                    "ink": "#22301F", "muted": "#74836F", "line": "#D8E4D4"},
    "ink":        {"accent": "#4A4A72", "accent2": "#9A9AC2", "bg": "#F6F6F9",
                    "ink": "#242432", "muted": "#75758A", "line": "#DFDFEA"},
    "mono":       {"accent": "#333333", "accent2": "#8C8C8C", "bg": "#F7F7F7",
                    "ink": "#1A1A1A", "muted": "#777777", "line": "#DDDDDD"},
    # v1.3.0 新增三个 preset：克制的设计 token，不追求风格数量，追求「一套对的」
    "editorial":  {"accent": "#BF4520", "accent2": "#E0956B", "bg": "#FAF6EF",
                    "ink": "#2D3142", "muted": "#8A8578", "line": "#E8DFD0"},
    "technical":  {"accent": "#2563EB", "accent2": "#93B4F5", "bg": "#F5F7FB",
                    "ink": "#1E2430", "muted": "#6B7686", "line": "#D9E0EA"},
    "warm":       {"accent": "#B4632C", "accent2": "#E3B23C", "bg": "#FBF4EC",
                    "ink": "#3A2E24", "muted": "#8F8172", "line": "#EBDCC9"},
}

# visual_system 中允许按 token 覆盖的字段 → 渲染器内部键的映射。
# paper 是用户侧命名（纸面底色），渲染器内部叫 bg。
TOKEN_KEYS = {"accent": "accent", "ink": "ink", "paper": "bg", "muted": "muted"}

FONT_STACK = ('-apple-system,"PingFang SC","Hiragino Sans GB",'
              '"Microsoft YaHei","Noto Sans CJK SC",sans-serif')

# 唯一允许的颜色格式：#RGB 或 #RRGGBB（纯十六进制，天然不含任何可注入字符）。
# 与 schemas/infographic-plan.schema.json 及 validate_infographic_plan.py 保持一致。
_HEX_COLOR_RE = re.compile(r'^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$')


def _validate_color(value, field="accent"):
    """渲染器边界校验：拒绝一切非十六进制颜色，防止 CSS/SVG 注入。"""
    if not isinstance(value, str) or not _HEX_COLOR_RE.match(value):
        raise ValueError(
            f"visual_system.{field} 必须是十六进制颜色（#RGB 或 #RRGGBB），收到: {value!r}")
    return value


def esc(s):
    return escape(str(s), quote=True)


def palette_of(plan):
    vs = plan.get("visual_system") or {}
    p = dict(PALETTES.get(vs.get("palette", "terracotta"), PALETTES["terracotta"]))
    # 严格校验：所有 token 都会插进 CSS 与 SVG 属性，只放行十六进制颜色，非法直接拒绝渲染。
    for field, key in TOKEN_KEYS.items():
        if vs.get(field):
            p[key] = _validate_color(vs[field], field)
    return p


def blocks_of(plan):
    return plan.get("blocks", [])


def rel_of(plan):
    return plan.get("relations", [])


def _fly_pt(cx, cy, r, a):
    return cx + r * math.cos(a), cy + r * math.sin(a)


# 「一列一色」马卡龙配色：蓝/黄/红/绿四主色，用于多主体并列的布局。
MACARON = ["#3B7DD8", "#D9A520", "#C0392B", "#3E8E5A"]
MACARON_LIGHT = ["#E8F1FB", "#FDF3DC", "#FBE3E3", "#E8F4EC"]


def _macaron(i):
    return MACARON[i % len(MACARON)], MACARON_LIGHT[i % len(MACARON_LIGHT)]


def _wrap_text(t, max_chars):
    """按最大字符数把文本切成多行（硬切，兼容 CJK）。"""
    if not t:
        return []
    lines = []
    while len(t) > max_chars:
        lines.append(t[:max_chars])
        t = t[max_chars:]
    if t:
        lines.append(t)
    return lines


# ---------------------------------------------------------------- flywheel
def render_flywheel(plan, p):
    """飞轮：中心圆盘（标题+副标题）+ N 个外围节点（标题+描述）+ 闭环箭头。

    v1.5.0 增强（相比早期「四瓣圆环」版本）：
    - 每个 block 的 title 与 text（描述）都渲染出来；
    - 中心放一块圆盘承载 meta.title / subtitle；
    - 节点之间用带箭头的圆弧相连，形成明确的闭环因果，而非色块拼缝。
    """
    blocks = blocks_of(plan)
    n = len(blocks)
    node_w, node_h = 204.0, 74.0
    gap = 16.0              # 节点色块与圆环之间的留白
    ring_r = 150.0          # 中心圆盘到圆环的半径（圆环在节点内侧）
    node_r = ring_r + node_h / 2 + gap   # 节点中心到圆心的距离（色块完全在环外）
    W = 820
    outer = node_r + node_h / 2
    H = max(600, int(2 * (outer + 40)))
    cx, cy = W / 2, H / 2
    parts = []

    # 1) 外围节点（放在圆环外侧，色块不与圆环相交）
    for i, b in enumerate(blocks):
        ang = -math.pi / 2 + 2 * math.pi * i / n
        nx = cx + node_r * math.cos(ang)
        ny = cy + node_r * math.sin(ang)
        fill = p["accent"] if i % 2 == 0 else p["accent2"]
        x0, y0 = nx - node_w / 2, ny - node_h / 2
        parts.append(
            f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{node_w}" height="{node_h}" rx="12" '
            f'fill="{fill}" stroke="#fff" stroke-width="2"/>')
        # 序号圆点
        parts.append(
            f'<circle cx="{x0 + 18:.1f}" cy="{ny:.1f}" r="11" fill="#fff" opacity="0.9"/>')
        parts.append(
            f'<text x="{x0 + 18:.1f}" y="{ny + 4:.1f}" text-anchor="middle" font-size="12" '
            f'font-weight="700" fill="{fill}">{i + 1}</text>')
        # 标题
        parts.append(
            f'<text x="{x0 + 38:.1f}" y="{ny - 14:.1f}" text-anchor="start" font-size="15" '
            f'font-weight="700" fill="#fff">{esc(b["title"])}</text>')
        # 描述（按节点可用宽度自动换行，最多两行）
        if b.get("text"):
            max_chars = 13
            t = b["text"]
            lines = []
            while len(t) > max_chars:
                lines.append(t[:max_chars])
                t = t[max_chars:]
            if t:
                lines.append(t)
            lines = lines[:2]
            y = ny + 6
            for ln in lines:
                shown = ln if len(ln) <= max_chars else ln[:max_chars - 1] + "…"
                parts.append(
                    f'<text x="{x0 + 38:.1f}" y="{y:.1f}" text-anchor="start" font-size="11" '
                    f'fill="#fff" opacity="0.95">{esc(shown)}</text>')
                y += 15

    # 2) 节点之间的闭环箭头（画在节点之间的空档处，贴着圆环外侧短弧）
    rels = rel_of(plan)
    idx = {b["id"]: i for i, b in enumerate(blocks)}
    for r in rels:
        i = idx.get(r["from"])
        j = idx.get(r["to"])
        if i is None or j is None:
            continue
        a_from = -math.pi / 2 + 2 * math.pi * i / n
        a_to = -math.pi / 2 + 2 * math.pi * j / n
        if a_to <= a_from:
            a_to += 2 * math.pi
        start_a = a_from + 2 * math.pi / n * 0.32
        end_a = a_to - 2 * math.pi / n * 0.32
        if end_a <= start_a:
            end_a = (a_from + a_to) / 2
        sx, sy = _fly_pt(cx, cy, ring_r, start_a)
        ex, ey = _fly_pt(cx, cy, ring_r, end_a)
        large = 1 if (end_a - start_a) > math.pi else 0
        parts.append(
            f'<path d="M{sx:.1f},{sy:.1f} A{ring_r},{ring_r} '
            f'0 {large} 1 {ex:.1f},{ey:.1f}" fill="none" stroke="{p["accent"]}" '
            f'stroke-width="2.5" marker-end="url(#fw-arrow)"/>')

    # 3) 中心圆盘
    center_r = 82.0
    parts.append(
        f'<circle cx="{cx}" cy="{cy}" r="{center_r}" fill="#fff" '
        f'stroke="{p["line"]}" stroke-width="1"/>')
    title = plan["meta"]["title"]
    parts.append(
        f'<text x="{cx}" y="{cy - 6}" text-anchor="middle" font-size="20" '
        f'font-weight="700" fill="{p["ink"]}">{esc(title)}</text>')
    if plan["meta"].get("subtitle"):
        sub = plan["meta"]["subtitle"]
        max_chars = 12
        slines = []
        tmp = sub
        while len(tmp) > max_chars:
            slines.append(tmp[:max_chars])
            tmp = tmp[max_chars:]
        if tmp:
            slines.append(tmp)
        slines = slines[:2]
        y = cy + 20
        for ln in slines:
            parts.append(
                f'<text x="{cx}" y="{y:.1f}" text-anchor="middle" font-size="11" '
                f'fill="{p["muted"]}">{esc(ln)}</text>')
            y += 15

    # 箭头 marker
    defs = (
        f'<defs><marker id="fw-arrow" viewBox="0 0 10 10" refX="8" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto">'
        f'<path d="M2 1L8 5L2 9" fill="none" stroke="{p["accent"]}" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')

    svg = (f'<svg viewBox="0 0 {W} {H}" role="img" '
           f'style="max-width:{W}px;width:100%;height:auto">{defs}{"".join(parts)}</svg>')
    return f'<div class="ig-canvas">{svg}</div>'


# ---------------------------------------------------------------- fishbone
def render_fishbone(plan, p):
    blocks = blocks_of(plan)
    heads = [b for b in blocks if b.get("role") == "head"]
    causes = [b for b in blocks if b.get("role") != "head"]
    head = heads[0] if heads else blocks[0]
    if not heads:
        causes = blocks[1:]

    W, H = 720, max(360, 120 * ((len(causes) + 1) // 2) + 120)
    sx0, sx1, sy = 40, W - 170, H / 2
    spine = (f'<line x1="{sx0}" y1="{sy}" x2="{sx1}" y2="{sy}" '
             f'stroke="{p["ink"]}" stroke-width="4"/>')
    head_box = (
        f'<rect x="{sx1 + 10}" y="{sy - 44}" width="150" height="88" rx="10" '
        f'fill="{p["accent"]}"/>'
        f'<text x="{sx1 + 85}" y="{sy - 8}" text-anchor="middle" font-size="15" '
        f'font-weight="700" fill="#fff">{esc(head["title"])}</text>')
    if head.get("text"):
        t = head["text"][:22]
        head_box += (f'<text x="{sx1 + 85}" y="{sy + 16}" text-anchor="middle" '
                     f'font-size="11" fill="#fff" opacity="0.9">{esc(t)}</text>')

    parts, up, down = [], [], []
    for b in causes:
        (up if len(up) <= len(down) else down).append(b)

    def branch(bs, sign):
        out = []
        k = len(bs)
        for j, b in enumerate(bs):
            bx = sx0 + (sx1 - sx0 - 90) * (j + 1) / (k + 1)
            tipy = sy + sign * 110
            out.append(f'<line x1="{bx - 70}" y1="{tipy}" x2="{bx}" y2="{sy}" '
                       f'stroke="{p["accent2"]}" stroke-width="3"/>')
            ly = tipy + (18 if sign > 0 else -10)
            out.append(f'<text x="{bx - 70}" y="{ly}" font-size="14" font-weight="600" '
                       f'fill="{p["ink"]}">{esc(b["title"])}</text>')
            if b.get("text"):
                out.append(f'<text x="{bx - 70}" y="{ly + 18}" font-size="11" '
                           f'fill="{p["muted"]}">{esc(b["text"][:30])}</text>')
        return out

    parts += branch(up, -1)
    parts += branch(down, +1)
    svg = (f'<svg viewBox="0 0 {W} {H}" role="img" style="max-width:{W}px;width:100%;height:auto">'
           f'{spine}{"".join(parts)}{head_box}</svg>')
    return f'<div class="ig-canvas">{svg}</div>'


# ---------------------------------------------------------------- sankey
def render_sankey(plan, p):
    blocks = {b["id"]: b for b in blocks_of(plan)}
    rels = [r for r in rel_of(plan) if r.get("weight") is not None]
    # column assignment: longest-path level
    level = {bid: 0 for bid in blocks}
    for _ in range(len(blocks)):
        for r in rels:
            level[r["to"]] = max(level[r["to"]], level[r["from"]] + 1)
    cols = {}
    for bid, lv in level.items():
        cols.setdefault(lv, []).append(bid)

    W, H = 760, 420
    pad, colw, x0 = 46, 26, 60
    total_w = x0 + len(cols) * (colw + 110)
    max_flow = max([sum(r["weight"] for r in rels if r["from"] == bid) or
                    sum(r["weight"] for r in rels if r["to"] == bid)
                    for bid in blocks] + [1])
    scale = (H - 2 * pad) / max_flow * 0.8

    def node_height(bid):
        f = max(sum(r["weight"] for r in rels if r["from"] == bid),
                sum(r["weight"] for r in rels if r["to"] == bid), 0.0001)
        return f * scale

    node_pos = {}
    for lv, ids in sorted(cols.items()):
        ids = sorted(ids, key=lambda b: -(node_height(b)))
        th = sum(node_height(b) for b in ids) + 14 * (len(ids) - 1)
        y = (H - th) / 2
        for bid in ids:
            h = node_height(bid)
            node_pos[bid] = (x0 + lv * (colw + 110), y, h)
            y += h + 14

    ribbons = []
    for r in rels:
        x0n, y0n, h0n = node_pos[r["from"]]
        x1n, y1n, h1n = node_pos[r["to"]]
        t = r["weight"] * scale
        ya = y0n + h0n / 2 - t / 2
        yb = y1n + h1n / 2 - t / 2
        xm = (x0n + colw + x1n) / 2
        ribbons.append(
            f'<path d="M{x0n + colw},{ya:.1f} C{xm},{ya:.1f} {xm},{yb:.1f} {x1n},{yb:.1f} '
            f'L{x1n},{yb + t:.1f} C{xm},{yb + t:.1f} {xm},{ya + t:.1f} {x0n + colw},{ya + t:.1f} Z" '
            f'fill="{p["accent2"]}" opacity="0.55" stroke="none"/>')

    nodes = []
    for bid, (nx, ny, nh) in node_pos.items():
        b = blocks[bid]
        nodes.append(f'<rect x="{nx}" y="{ny:.1f}" width="{colw}" height="{nh:.1f}" '
                     f'rx="3" fill="{p["accent"]}"/>')
        lbl = f'{esc(b["title"])}'
        if b.get("value"):
            lbl += f'（{esc(b["value"])}）'
        nodes.append(f'<text x="{nx + colw + 6}" y="{ny + nh / 2 + 4:.1f}" font-size="12" '
                     f'font-weight="600" fill="{p["ink"]}">{lbl}</text>')

    svg = (f'<svg viewBox="0 0 {max(total_w, W)} {H}" role="img" '
           f'style="max-width:{max(total_w, W)}px;width:100%;height:auto">'
           f'{"".join(ribbons)}{"".join(nodes)}</svg>')
    return f'<div class="ig-canvas">{svg}</div>'


# ---------------------------------------------------------------- pyramid
def render_pyramid(plan, p):
    """等腰金字塔：blocks 顺序即层级（第一个=基座，最后一个=塔尖）。

    v1.5.0 重写，解决早期版本「层块不对齐、基座画反」的问题：
    - 严格等腰：中轴固定，每层顶/底边宽线性收缩，塔尖收为顶点；
    - 一列一色：每层用马卡龙主色（蓝/黄/红/绿），层间无 opacity 混叠；
    - 层内标题居中；描述文字画在每层右侧，用细引线对齐该层中心。
    """
    blocks = blocks_of(plan)
    n = len(blocks)
    LH = 72                     # 每层高
    shape_w = 560               # 基座底边宽
    cx = 320                    # 中轴（左移，右侧留说明栏）
    top_y = 20                  # 塔尖 y
    side_x = 320 + shape_w / 2 + 60   # 右侧说明栏起点
    W = 820
    H = top_y + n * LH + 46     # 底部多留白，避免基座被裁切

    parts = []
    for i, b in enumerate(blocks):          # i=0 基座（最宽、画在最下），i=n-1 塔尖（最上）
        w_top = shape_w * (n - 1 - i) / n
        w_bot = shape_w * (n - i) / n
        # 基座（i=0）画在最底部：y 从 H 往上数
        y_bot = H - 46 - i * LH
        y_top = y_bot - LH
        xlt = cx - w_top / 2
        xrt = cx + w_top / 2
        xlb = cx - w_bot / 2
        xrb = cx + w_bot / 2
        main, light = _macaron(i)
        # 层块（等腰梯形；塔尖层为三角形）
        parts.append(
            f'<polygon points="{xlt:.1f},{y_top:.1f} {xrt:.1f},{y_top:.1f} '
            f'{xrb:.1f},{y_bot:.1f} {xlb:.1f},{y_bot:.1f}" '
            f'fill="{light}" stroke="{main}" stroke-width="1.5"/>')
        # 层内标题（居中）
        mid_y = y_top + LH / 2
        parts.append(f'<text x="{cx}" y="{mid_y + 5:.1f}" text-anchor="middle" '
                     f'font-size="15" font-weight="700" fill="{main}">'
                     f'{i + 1}. {esc(b["title"])}</text>')
        # 右侧说明（text + 引线）
        if b.get("text"):
            tx = side_x
            parts.append(f'<line x1="{xrb + 4:.1f}" y1="{mid_y:.1f}" x2="{tx - 8:.1f}" '
                         f'y2="{mid_y:.1f}" stroke="{main}" stroke-width="1" '
                         f'stroke-dasharray="3,3"/>')
            parts.append(f'<text x="{tx}" y="{mid_y + 4:.1f}" text-anchor="start" '
                         f'font-size="13" font-weight="600" fill="{p["ink"]}">'
                         f'{esc(b["text"][:20])}</text>')

    svg = (f'<svg viewBox="0 0 {W} {H}" role="img" '
           f'style="max-width:{W}px;width:100%;height:auto">{"".join(parts)}</svg>')
    return f'<div class="ig-canvas">{svg}</div>'


# ---------------------------------------------------------------- timeline
def render_timeline(plan, p):
    items = []
    for b in blocks_of(plan):
        t = f'<span class="tl-time">{esc(b["time"])}</span>' if b.get("time") else ""
        txt = f'<p class="tl-text">{esc(b["text"])}</p>' if b.get("text") else ""
        items.append(f'''
  <li class="tl-item">
    <span class="tl-dot"></span>
    <div class="tl-body">{t}<b class="tl-title">{esc(b["title"])}</b>{txt}</div>
  </li>''')
    return f'<ol class="timeline">{"".join(items)}</ol>'


# ---------------------------------------------------------------- dashboard
def render_dashboard(plan, p):
    cards = []
    for b in blocks_of(plan):
        val = f'<div class="db-value">{esc(b["value"])}<small>{esc(b.get("unit", ""))}</small></div>' \
            if b.get("value") else ""
        metric = f'<div class="db-metric">{esc(b["metric"])}</div>' if b.get("metric") else ""
        time = f'<span class="db-time">{esc(b["time"])}</span>' if b.get("time") else ""
        txt = f'<p class="db-text">{esc(b["text"])}</p>' if b.get("text") else ""
        cards.append(f'''
  <div class="db-card">
    {metric}{val}
    <b class="db-title">{esc(b["title"])}</b>{txt}{time}
  </div>''')
    return f'<div class="dashboard">{"".join(cards)}</div>'


# ---------------------------------------------------------------- comparison
def render_comparison(plan, p):
    """对比双栏：按 block.group 分列（左/右），逐条列出 title + text。

    - group 相同 → 同一列，group 顺序即列顺序
    - 每列一个主题色（马卡龙），标题条用主色，条目用浅色卡
    """
    blocks = blocks_of(plan)
    groups = []
    for b in blocks:
        g = b.get("group", "left")
        if g not in groups:
            groups.append(g)

    W = 760
    col_gap = 20
    col_w = (W - 40 - col_gap * (len(groups) - 1)) / len(groups)
    max_items = max(len([b for b in blocks if b.get("group", "left") == g])
                    for g in groups)
    item_h = 78
    header_h = 44
    H = header_h + max_items * item_h + 40

    cols_html = []
    for gi, g in enumerate(groups):
        main, light = _macaron(gi)
        items = [b for b in blocks if b.get("group", "left") == g]
        x = 20 + gi * (col_w + col_gap)
        col_title = items[0].get("group_title") or g
        parts = [f'<rect x="{x:.1f}" y="20" width="{col_w:.1f}" height="{header_h}" '
                 f'rx="8" fill="{main}"/>']
        parts.append(
            f'<text x="{x + col_w / 2:.1f}" y="{20 + header_h / 2 + 5:.1f}" '
            f'text-anchor="middle" font-size="16" font-weight="700" fill="#fff">'
            f'{esc(col_title)}</text>')
        for j, b in enumerate(items):
            iy = 20 + header_h + 12 + j * item_h
            parts.append(f'<rect x="{x:.1f}" y="{iy:.1f}" width="{col_w:.1f}" '
                         f'height="{item_h - 8:.1f}" rx="8" fill="{light}" '
                         f'stroke="{main}" stroke-width="1"/>')
            ty = iy + 24
            parts.append(f'<text x="{x + 14:.1f}" y="{ty:.1f}" text-anchor="start" '
                         f'font-size="14" font-weight="700" fill="{main}">{esc(b["title"])}</text>')
            if b.get("text"):
                lines = _wrap_text(b["text"], int(col_w / 17))
                for li, ln in enumerate(lines[:3]):
                    parts.append(
                        f'<text x="{x + 14:.1f}" y="{ty + 18 + li * 17:.1f}" '
                        f'text-anchor="start" font-size="12" fill="{p["ink"]}">{esc(ln)}</text>')
        cols_html.append("".join(parts))

    svg = (f'<svg viewBox="0 0 {W} {H}" role="img" '
           f'style="max-width:{W}px;width:100%;height:auto">{"".join(cols_html)}</svg>')
    return f'<div class="ig-canvas">{svg}</div>'


# ---------------------------------------------------------------- quadrant
def render_quadrant(plan, p):
    """2×2 矩阵：四象限，X/Y 轴标签来自 meta（x_label / y_label），
    四个 block 按顺序放：左上、右上、左下、右下。
    """
    blocks = blocks_of(plan)
    meta = plan["meta"]
    W = 680
    H = 560
    pad = 90
    ax_w = W - 2 * pad
    ax_h = H - 2 * pad
    cx = pad + ax_w / 2
    cy = pad + ax_h / 2

    parts = []
    parts.append(f'<line x1="{cx}" y1="{pad - 8}" x2="{cx}" y2="{pad + ax_h + 8}" '
                 f'stroke="{p["muted"]}" stroke-width="1.5"/>')
    parts.append(f'<line x1="{pad - 8}" y1="{cy}" x2="{pad + ax_w + 8}" y2="{cy}" '
                 f'stroke="{p["muted"]}" stroke-width="1.5"/>')
    parts.append(f'<polygon points="{cx - 4},{pad - 8} {cx + 4},{pad - 8} {cx},{pad - 20}" '
                 f'fill="{p["muted"]}"/>')
    parts.append(f'<polygon points="{pad + ax_w + 8},{cy - 4} {pad + ax_w + 8},{cy + 4} '
                 f'{pad + ax_w + 20},{cy}" fill="{p["muted"]}"/>')
    if meta.get("y_label"):
        parts.append(f'<text x="{cx}" y="{pad - 26}" text-anchor="middle" font-size="13" '
                     f'font-weight="700" fill="{p["ink"]}">{esc(meta["y_label"])}</text>')
    if meta.get("x_label"):
        parts.append(f'<text x="{pad + ax_w + 26}" y="{cy + 4}" text-anchor="start" '
                     f'font-size="13" font-weight="700" fill="{p["ink"]}">{esc(meta["x_label"])}</text>')

    positions = [
        (pad + 10, pad + 10, 0),
        (cx + 10, pad + 10, 1),
        (pad + 10, cy + 10, 2),
        (cx + 10, cy + 10, 3),
    ]
    qw = ax_w / 2 - 24
    qh = ax_h / 2 - 24
    for i, b in enumerate(blocks[:4]):
        qx, qy, ci = positions[i]
        main, light = _macaron(ci)
        parts.append(f'<rect x="{qx:.1f}" y="{qy:.1f}" width="{qw:.1f}" height="{qh:.1f}" '
                     f'rx="10" fill="{light}" stroke="{main}" stroke-width="1.5"/>')
        parts.append(f'<text x="{qx + 14:.1f}" y="{qy + 30:.1f}" text-anchor="start" '
                     f'font-size="15" font-weight="700" fill="{main}">{esc(b["title"])}</text>')
        if b.get("text"):
            lines = _wrap_text(b["text"], int(qw / 17))
            for li, ln in enumerate(lines[:4]):
                parts.append(
                    f'<text x="{qx + 14:.1f}" y="{qy + 52 + li * 18:.1f}" text-anchor="start" '
                    f'font-size="12" fill="{p["ink"]}">{esc(ln)}</text>')

    svg = (f'<svg viewBox="0 0 {W} {H}" role="img" '
           f'style="max-width:{W}px;width:100%;height:auto">{"".join(parts)}</svg>')
    return f'<div class="ig-canvas">{svg}</div>'


# ---------------------------------------------------------------- flow
def render_flow(plan, p):
    """流程步骤：横向步骤卡 + 箭头串联。顺序由 relations 决定，缺省按 blocks 顺序。"""
    blocks = blocks_of(plan)
    rels = rel_of(plan)
    idx = {b["id"]: i for i, b in enumerate(blocks)}
    order = []
    if rels:
        indeg = {b["id"]: 0 for b in blocks}
        adj = {b["id"]: [] for b in blocks}
        for r in rels:
            adj[r["from"]].append(r["to"])
            indeg[r["to"]] += 1
        q = [bid for bid, d in indeg.items() if d == 0]
        while q:
            cur = q.pop(0)
            order.append(cur)
            for nxt in adj[cur]:
                indeg[nxt] -= 1
                if indeg[nxt] == 0:
                    q.append(nxt)
    if len(order) != len(blocks):
        order = [b["id"] for b in blocks]

    n = len(order)
    card_w = 150
    card_h = 96
    gap = 44
    W = 60 + n * card_w + (n - 1) * gap + 60
    H = 200

    parts = []
    for i, bid in enumerate(order):
        b = blocks[idx[bid]]
        main, light = _macaron(i)
        x = 60 + i * (card_w + gap)
        y = (H - card_h) / 2
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{card_w}" height="{card_h}" '
                     f'rx="12" fill="{light}" stroke="{main}" stroke-width="2"/>')
        parts.append(f'<circle cx="{x + 18:.1f}" cy="{y + 18:.1f}" r="13" fill="{main}"/>')
        parts.append(f'<text x="{x + 18:.1f}" y="{y + 23:.1f}" text-anchor="middle" '
                     f'font-size="13" font-weight="700" fill="#fff">{i + 1}</text>')
        lines = _wrap_text(b["title"], 8)
        for li, ln in enumerate(lines[:2]):
            parts.append(f'<text x="{x + card_w / 2:.1f}" y="{y + 50 + li * 18:.1f}" '
                         f'text-anchor="middle" font-size="14" font-weight="700" '
                         f'fill="{p["ink"]}">{esc(ln)}</text>')
        if b.get("text"):
            tlines = _wrap_text(b["text"], 10)
            for li, ln in enumerate(tlines[:2]):
                parts.append(f'<text x="{x + card_w / 2:.1f}" y="{y + 72 + li * 14:.1f}" '
                             f'text-anchor="middle" font-size="11" fill="{p["muted"]}">{esc(ln)}</text>')
        if i < n - 1:
            ax = x + card_w + 8
            ay = y + card_h / 2
            parts.append(f'<line x1="{ax}" y1="{ay}" x2="{ax + gap - 16}" y2="{ay}" '
                         f'stroke="{p["muted"]}" stroke-width="2"/>')
            parts.append(f'<polygon points="{ax + gap - 16},{ay - 4} {ax + gap - 16},{ay + 4} '
                         f'{ax + gap - 4},{ay}" fill="{p["muted"]}"/>')

    svg = (f'<svg viewBox="0 0 {W} {H}" role="img" '
           f'style="max-width:{W}px;width:100%;height:auto">{"".join(parts)}</svg>')
    return f'<div class="ig-canvas">{svg}</div>'


# ---------------------------------------------------------------- venn
def render_venn(plan, p):
    """韦恩图：2-4 个集合圆，标题写在圆上方，交集区半透明。"""
    blocks = blocks_of(plan)
    n = len(blocks)
    W = 680
    H = 480
    r = 130
    if n == 2:
        centers = [(W / 2 - 80, H / 2), (W / 2 + 80, H / 2)]
    elif n == 3:
        centers = [(W / 2, H / 2 - 60), (W / 2 - 90, H / 2 + 50), (W / 2 + 90, H / 2 + 50)]
    else:
        centers = [(W / 2 - 70, H / 2 - 50), (W / 2 + 70, H / 2 - 50),
                   (W / 2 - 70, H / 2 + 50), (W / 2 + 70, H / 2 + 50)]

    parts = []
    for i, b in enumerate(blocks):
        main, _ = _macaron(i)
        cx, cy = centers[i]
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{main}" '
                     f'opacity="0.22" stroke="{main}" stroke-width="2"/>')
        ty = cy - r - 16
        parts.append(f'<text x="{cx:.1f}" y="{ty:.1f}" text-anchor="middle" font-size="14" '
                     f'font-weight="700" fill="{main}">{esc(b["title"])}</text>')
        if b.get("text"):
            tlines = _wrap_text(b["text"], 10)
            for li, ln in enumerate(tlines[:2]):
                parts.append(f'<text x="{cx:.1f}" y="{cy + li * 16:.1f}" text-anchor="middle" '
                             f'font-size="11" fill="{p["ink"]}">{esc(ln)}</text>')

    svg = (f'<svg viewBox="0 0 {W} {H}" role="img" '
           f'style="max-width:{W}px;width:100%;height:auto">{"".join(parts)}</svg>')
    return f'<div class="ig-canvas">{svg}</div>'


RENDERERS = {
    "flywheel": render_flywheel,
    "fishbone": render_fishbone,
    "sankey": render_sankey,
    "pyramid": render_pyramid,
    "timeline": render_timeline,
    "dashboard": render_dashboard,
    "comparison": render_comparison,
    "quadrant": render_quadrant,
    "flow": render_flow,
    "venn": render_venn,
}


# ---------------------------------------------------------------- shell
def render_html(plan):
    p = palette_of(plan)
    layout = plan["layout"]
    if layout not in RENDERERS:
        raise ValueError(f"unknown layout: {layout}")
    body = RENDERERS[layout](plan, p)
    meta = plan["meta"]
    footer = meta.get("footer") or meta.get("source_note") or ""
    title_line = f'<h1 class="ig-title">{esc(meta["title"])}</h1>'
    subtitle = f'<p class="ig-subtitle">{esc(meta["subtitle"])}</p>' if meta.get("subtitle") else ""
    footer_html = f'<div class="ig-footer">{esc(footer)}</div>' if footer else ""
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src data:; base-uri 'none'; form-action 'none'">
<title>{esc(meta["title"])}</title>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{background:{p["bg"]};color:{p["ink"]};font-family:{FONT_STACK};
       display:flex;justify-content:center;padding:32px 16px}}
  .ig{{background:#fff;border:1px solid {p["line"]};border-radius:16px;
      max-width:820px;width:100%;padding:36px 32px}}
  .ig-title{{font-size:26px;font-weight:800;letter-spacing:.5px}}
  .ig-subtitle{{color:{p["muted"]};font-size:14px;margin-top:6px}}
  .ig-canvas{{margin-top:22px;text-align:center}}
  .ig-footer{{margin-top:24px;padding-top:14px;border-top:1px dashed {p["line"]};
      color:{p["muted"]};font-size:12px}}
  /* timeline */
  .timeline{{list-style:none;margin-top:22px;padding-left:6px}}
  .tl-item{{position:relative;padding:0 0 22px 26px;border-left:2px solid {p["line"]}}}
  .tl-item:last-child{{border-left-color:transparent}}
  .tl-dot{{position:absolute;left:-7px;top:2px;width:12px;height:12px;border-radius:50%;
      background:{p["accent"]};box-shadow:0 0 0 3px {p["bg"]}}}
  .tl-time{{display:inline-block;font-size:12px;font-weight:700;color:{p["accent"]};
      background:{p["bg"]};border-radius:4px;padding:2px 8px;margin-bottom:4px}}
  .tl-title{{display:block;font-size:15px;margin-top:2px}}
  .tl-text{{font-size:13px;color:{p["muted"]};margin-top:3px}}
  /* dashboard */
  .dashboard{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
      gap:14px;margin-top:22px}}
  .db-card{{border:1px solid {p["line"]};border-radius:12px;padding:16px;
      background:linear-gradient(180deg,#fff, {p["bg"]})}}
  .db-metric{{font-size:12px;color:{p["muted"]};font-weight:600}}
  .db-value{{font-size:30px;font-weight:800;color:{p["accent"]};margin:4px 0 2px}}
  .db-value small{{font-size:13px;font-weight:600;color:{p["muted"]};margin-left:3px}}
  .db-title{{display:block;font-size:14px;margin-top:6px}}
  .db-text{{font-size:12px;color:{p["muted"]};margin-top:4px}}
  .db-time{{display:inline-block;margin-top:8px;font-size:11px;color:{p["muted"]}}}
  @media print{{body{{padding:0}}.ig{{border:none}}}}
</style>
</head>
<body>
<main class="ig">
  {title_line}
  {subtitle}
  {body}
  {footer_html}
</main>
</body>
</html>
'''


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__, file=sys.stderr)
        sys.exit(2)

    want_png = "--png" in args
    png_out = None
    scale, width, chrome_path = 2, 852, None
    clean = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--png":
            want_png = True
            nxt = args[i + 1] if i + 1 < len(args) else None
            if nxt and not nxt.startswith("-"):
                png_out = nxt            # 显式给了输出路径
                i += 2
                continue
            i += 1
            continue
        if a in ("--scale", "--width", "--chrome") and i + 1 < len(args):
            if a == "--scale":
                scale = int(args[i + 1])
            elif a == "--width":
                width = int(args[i + 1])
            else:
                chrome_path = args[i + 1]
            i += 2
            continue
        clean.append(a)
        i += 1

    if not clean:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    src = clean[0]
    data = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
    plan = json.loads(data)
    html_out = render_html(plan)

    out_arg = clean[1] if len(clean) > 1 else None
    wrote_html = False
    if out_arg and out_arg != "-":
        with open(out_arg, "w", encoding="utf-8") as f:
            f.write(html_out)
        wrote_html = True
        print(f"OK -> {out_arg}")
    else:
        sys.stdout.write(html_out)

    if not want_png:
        return

    # ---- PNG 导出（可选，失败不影响已产出的 HTML）
    if png_out is None:
        if out_arg and out_arg != "-":
            png_out = str(out_arg[:-5] if out_arg.endswith(".html")
                          else out_arg) + ".png"
        else:
            print("--png 需要输出路径（stdout 模式下无法推断）", file=sys.stderr)
            sys.exit(2)
    if not wrote_html:                             # stdout 模式：先落临时 HTML 再截图
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".html",
                                         delete=False, encoding="utf-8") as tf:
            tf.write(html_out)
            tmp_html = tf.name
    else:
        tmp_html = out_arg
    try:
        sys.path.insert(0, __file__.rsplit("/", 1)[0])
        import export_png as EP
        path, h, _ = EP.export(tmp_html, png_out, width=width, scale=scale,
                               chrome=chrome_path)
        print(f"OK -> {path}  ({h * scale}px 高)")
    except Exception as e:                         # HTML 已经拿到，PNG 失败只提示不中断
        print(f"[png] 导出失败，不影响已生成的 HTML：\n{e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
