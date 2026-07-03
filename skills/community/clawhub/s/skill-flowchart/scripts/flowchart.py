#!/usr/bin/env python3
"""
flowchart.py — Skill 决策流程图生成器

读取 nodes.json（结构化的节点/边/分支/回环），自动计算坐标布局，
输出 docs/decision-flowchart.html（自包含的 SVG + HTML）。

用法：
    python3 scripts/flowchart.py <nodes.json> [--out <output.html>] [--json-out <output.json>]

零外部依赖，仅使用 Python 标准库。
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

ROLE_COLORS: dict[str, dict[str, str]] = {
    "ai":       {"fill": "#E6F1FB", "stroke": "#185FA5", "text_class": "th"},
    "output":   {"fill": "#EEEDFE", "stroke": "#534AB7", "text_class": "th"},
    "decision": {"fill": "#FAEEDA", "stroke": "#854F0B", "text_class": "ths"},
    "script":   {"fill": "#E1F5EE", "stroke": "#0F6E56", "text_class": "ths"},
    "terminal": {"fill": "#FCEBEB", "stroke": "#A32D2D", "text_class": "th"},
}

DEFAULT_LEGEND: list[dict[str, str]] = [
    {"label": "AI 执行",   "fill": "#E6F1FB", "stroke": "#185FA5"},
    {"label": "输出/报告", "fill": "#EEEDFE", "stroke": "#534AB7"},
    {"label": "决策点",    "fill": "#FAEEDA", "stroke": "#854F0B"},
    {"label": "脚本",      "fill": "#E1F5EE", "stroke": "#0F6E56"},
    {"label": "终止",      "fill": "#FCEBEB", "stroke": "#A32D2D"},
]

# 暗色主题独立配色（HaluCatch 官方暗色色板）
# 深填充(surface/surface2) + 亮描边(accent)，确保与深背景有明度差
DARK_ROLE_COLORS: dict[str, dict[str, str]] = {
    "ai":       {"fill": "#1a1a2e", "stroke": "#6c63ff", "text_class": "th"},   # surface2 + accent 紫
    "output":   {"fill": "#12121a", "stroke": "#00d4aa", "text_class": "th"},   # surface + accent2 青绿
    "decision": {"fill": "#1a1a2e", "stroke": "#ffa94d", "text_class": "ths"},  # surface2 + orange
    "script":   {"fill": "#12121a", "stroke": "#51cf66", "text_class": "ths"},  # surface + green
    "terminal": {"fill": "#1a1a2e", "stroke": "#ff6b6b", "text_class": "th"},   # surface2 + red
}

DARK_LEGEND: list[dict[str, str]] = [
    {"label": "AI 执行",   "fill": "#1a1a2e", "stroke": "#6c63ff"},
    {"label": "输出/报告", "fill": "#12121a", "stroke": "#00d4aa"},
    {"label": "决策点",    "fill": "#1a1a2e", "stroke": "#ffa94d"},
    {"label": "脚本",      "fill": "#12121a", "stroke": "#51cf66"},
    {"label": "终止",      "fill": "#1a1a2e", "stroke": "#ff6b6b"},
]

# ---------------------------------------------------------------------------
# 主题
# ---------------------------------------------------------------------------
# light:     白底，标签用白色光晕遮线
# dark:      深底，标签用深色光晕遮线
# transparent: 无底色，垂直边标签偏移到线一侧（不遮线）

THEMES: dict[str, dict[str, Any]] = {
    "light": {
        "bg": "#ffffff",
        "text": "#2C2C2A",
        "subtitle": "#888780",
        "title_color": "#2C2C2A",
        "edge_stroke": "#888780",
        "edge_dash_stroke": "#B4B2A9",
        "label_halo": "#ffffff",
        "use_halo": True,
        "node_alpha_darken": False,
    },
    "dark": {
        "bg": "#0a0a0f",
        "text": "#e0e0f0",
        "subtitle": "#8888aa",
        "title_color": "#e0e0f0",
        "edge_stroke": "#2a2a3e",
        "edge_dash_stroke": "#1a1a2e",
        "label_halo": "#0a0a0f",
        "use_halo": True,
        "role_colors": DARK_ROLE_COLORS,
        "legend": DARK_LEGEND,
    },
    "transparent": {
        "bg": None,
        "text": "#2C2C2A",
        "subtitle": "#888780",
        "title_color": "#2C2C2A",
        "edge_stroke": "#888780",
        "edge_dash_stroke": "#B4B2A9",
        "label_halo": None,
        "use_halo": False,
        "node_alpha_darken": False,
    },
}

# 布局参数（与参考图对齐）
CENTER_X = 340.0          # 主流程中轴 X
SIDE_LEFT_X = 90.0        # 左侧支节点中心 X（终端节点）
SIDE_RIGHT_X = 566.0      # 右侧支节点中心 X（脚本节点等较宽）
GAP_Y = 86.0              # 层间距（参考图 level 间 y 差 ≈ 86）
TOP_PAD = 54.0            # 第一层节点 cy

# 节点尺寸
NODE_W = 220
NODE_H = 44
NODE_H_TALL = 56
DIAMOND_HALF_W = 75.0     # 菱形水平半宽（参考图 340±75 → 265~415）
DIAMOND_HALF_H = 30.0     # 菱形垂直半高（参考图 130±30 → 100~160）
TERMINAL_W = 120
TERMINAL_H = 44
SMALL_TERM_W = 96
SMALL_TERM_H = 34
PROCESS_W = 220
PROCESS_H = 44
SUB_W = 180               # 分支子节点宽（type_data 等）
SUB_H = 44

# y 布局单位（按主干路深度累加）
UNIT_H = 76.0             # 一个主干层级的高度（节点高 44 + 间距 32）
HALF_UNIT_H = 38.0        # 有 label 文本时额外加的高度


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------

@dataclass
class Node:
    id: str
    type: str            # entry / decision / process / output / terminal
    role: str            # ai / output / decision / script / terminal
    label: str
    subtitle: str = ""
    cx: float = 0.0
    cy: float = 0.0
    width: float = NODE_W
    height: float = NODE_H
    level: int = 0


@dataclass
class Edge:
    from_id: str
    to_id: str
    label: str = ""
    side: str = ""       # "" | "left" | "right" | "bottom"


@dataclass
class Loop:
    from_id: str
    to_id: str
    label: str = ""
    path: str = "left_edge"


@dataclass
class Graph:
    title: str = "Skill"
    subtitle: str = ""
    nodes: dict[str, Node] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)
    loops: list[Loop] = field(default_factory=list)
    legend: list[dict[str, str]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# 加载 & 校验
# ---------------------------------------------------------------------------

VALID_TYPES = {"entry", "decision", "process", "output", "terminal"}
VALID_ROLES = {"ai", "output", "decision", "script", "terminal"}
VALID_SIDES = {"", "left", "right", "bottom"}


def _node_default_size(node: Node) -> None:
    if node.type == "decision":
        node.width = DIAMOND_HALF_W * 2
        node.height = DIAMOND_HALF_H * 2
    elif node.type == "terminal":
        node.width = TERMINAL_W
        node.height = TERMINAL_H
    elif node.type == "entry":
        node.width = NODE_W
        node.height = NODE_H
    elif node.subtitle:
        node.width = NODE_W
        node.height = NODE_H_TALL
    else:
        node.width = NODE_W
        node.height = NODE_H


def load_graph(json_path: str) -> Graph:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    graph = Graph(
        title=data.get("title", "Skill"),
        subtitle=data.get("subtitle", ""),
        legend=data.get("legend", DEFAULT_LEGEND),
    )

    for n in data.get("nodes", []):
        node = Node(
            id=n["id"],
            type=n.get("type", "process"),
            role=n.get("role", "ai"),
            label=n.get("label", n["id"]),
            subtitle=n.get("subtitle", ""),
        )
        _node_default_size(node)
        graph.nodes[node.id] = node

    for e in data.get("edges", []):
        graph.edges.append(Edge(
            from_id=e["from"],
            to_id=e["to"],
            label=e.get("label", ""),
            side=e.get("side", ""),
        ))

    for l in data.get("loops", []):
        graph.loops.append(Loop(
            from_id=l["from"],
            to_id=l["to"],
            label=l.get("label", ""),
            path=l.get("path", "left_edge"),
        ))

    _validate_graph(graph)
    return graph


def _validate_graph(graph: Graph) -> None:
    valid_ids = set(graph.nodes.keys())
    # 节点 type/role 校验
    for nid, n in graph.nodes.items():
        if n.type not in VALID_TYPES:
            raise ValueError(f"节点 '{nid}' type 非法: '{n.type}'，合法: {sorted(VALID_TYPES)}")
        if n.role not in VALID_ROLES:
            raise ValueError(f"节点 '{nid}' role 非法: '{n.role}'，合法: {sorted(VALID_ROLES)}")
    # 边
    for e in graph.edges:
        if e.from_id not in valid_ids:
            raise ValueError(f"Edge from 引用了未知节点 id: '{e.from_id}'。有效: {sorted(valid_ids)}")
        if e.to_id not in valid_ids:
            raise ValueError(f"Edge to 引用了未知节点 id: '{e.to_id}'。有效: {sorted(valid_ids)}")
        if e.side not in VALID_SIDES:
            raise ValueError(f"Edge {e.from_id}->{e.to_id} side 非法: '{e.side}'，合法: {sorted(VALID_SIDES)}")
    for l in graph.loops:
        if l.from_id not in valid_ids:
            raise ValueError(f"Loop from 引用了未知节点 id: '{l.from_id}'")
        if l.to_id not in valid_ids:
            raise ValueError(f"Loop to 引用了未知节点 id: '{l.to_id}'")


# ---------------------------------------------------------------------------
# 布局：depth（层级）
# ---------------------------------------------------------------------------
#
# 规则（对照黄金坐标表）：
#   1. 决策菱形的侧支（side=left/right）→ 与决策同 level
#   2. side=bottom 的目标 → from.level + 1（主流程向下）
#   3. 普通矩形分叉（phase0→type_data/method，side=left/right 但 from 不是 decision）
#      → 仍是 from.level + 1（下一层斜线分叉，不是同层横向）
#   4. 汇合点（入边 ≥2）→ level = max(所有入边节点 level)
#
# 关键区分：只有「决策节点的 side=left/right」才是同层侧支；
#           普通节点的 side=left/right 是「下一层斜线分叉」。

def _assign_depth(graph: Graph) -> None:
    out_edges: dict[str, list[Edge]] = {nid: [] for nid in graph.nodes}
    in_edges: dict[str, list[Edge]] = {nid: [] for nid in graph.nodes}
    for e in graph.edges:
        out_edges[e.from_id].append(e)
        in_edges[e.to_id].append(e)

    entry_ids = [nid for nid, n in graph.nodes.items() if n.type == "entry"]
    if not entry_ids:
        entry_ids = [next(iter(graph.nodes))]

    depth: dict[str, int] = {eid: 0 for eid in entry_ids}
    for nid in graph.nodes:
        depth.setdefault(nid, 0)

    # 决策节点的侧支 target：与决策同 level
    # （仅对 from.type == decision 且 side in (left,right) 生效）
    side_targets: set[str] = set()   # 与决策同层的侧支
    for nid, node in graph.nodes.items():
        if node.type == "decision":
            for e in out_edges[nid]:
                if e.side in ("left", "right") and e.to_id in graph.nodes:
                    side_targets.add(e.to_id)

    # 汇合点：入边 ≥ 2
    convergence: set[str] = {
        nid for nid, ins in in_edges.items()
        if len(ins) >= 2 and nid in graph.nodes
    }

    # 单循环迭代：每轮同时更新非汇合点和汇合点，直到稳定
    # 这样嵌套汇合点（汇合点的入边依赖另一个汇合点）也能正确传播
    for _ in range(500):
        changed = False
        # 非汇合点 + 汇合点作为 source：从每条出边传播 depth
        for u in graph.nodes:
            for e in out_edges[u]:
                v = e.to_id
                if v not in graph.nodes or v in convergence:
                    continue
                if v in side_targets:
                    target = depth[u]
                else:
                    target = depth[u] + 1
                if depth[v] < target:
                    depth[v] = target
                    changed = True
        # 汇合点：max(入边 level) + 1
        for v in convergence:
            ins = in_edges[v]
            target = max(depth.get(e.from_id, 0) for e in ins) + 1
            if depth[v] < target:
                depth[v] = target
                changed = True
        if not changed:
            break

    for nid, d in depth.items():
        graph.nodes[nid].level = d


# ---------------------------------------------------------------------------
# 布局：y 坐标
# ---------------------------------------------------------------------------

def _assign_y(graph: Graph) -> None:
    """按主干路深度分配 y。

    规则：
    - 每个主干层级的「中心到中心」距离 = UNIT_H
    - 如果相邻层级之间的边有 label 文本 → 额外 +0.5 UNIT_H
    - 但实际 y 通过「上一行底部 + 净间距」累加，确保不同高度节点的间距一致
    """
    from collections import defaultdict
    by_level: dict[int, list[Node]] = defaultdict(list)
    for n in graph.nodes.values():
        by_level[n.level].append(n)

    # 建立 from_level → to_level 的边索引（含 label 信息）
    edges_between: dict[tuple[int, int], list[bool]] = defaultdict(list)
    for e in graph.edges:
        if e.from_id in graph.nodes and e.to_id in graph.nodes:
            src_lvl = graph.nodes[e.from_id].level
            dst_lvl = graph.nodes[e.to_id].level
            if src_lvl != dst_lvl:  # 只看跨层边
                edges_between[(src_lvl, dst_lvl)].append(bool(e.label))

    # 净间距常量（上一行底部到下一行顶部）
    GAP_NORMAL = 32.0    # 无 label 时的净间距
    GAP_WITH_LABEL = 56.0  # 有 label 时的净间距（多留空间放文字）

    sorted_levels = sorted(by_level.keys())
    level_y: dict[int, float] = {}
    for i, lvl in enumerate(sorted_levels):
        nodes = by_level[lvl]
        max_h = max(n.height for n in nodes)
        if i == 0:
            level_y[lvl] = TOP_PAD
        else:
            prev_lvl = sorted_levels[i - 1]
            prev_nodes = by_level[prev_lvl]
            prev_max_h = max(n.height for n in prev_nodes)
            prev_bottom = level_y[prev_lvl] + prev_max_h / 2
            # 检查 prev_lvl → lvl 之间的边是否有 label
            has_label = any(edges_between.get((prev_lvl, lvl), []))
            gap = GAP_WITH_LABEL if has_label else GAP_NORMAL
            level_y[lvl] = prev_bottom + gap + max_h / 2
    for lvl, y in level_y.items():
        for n in by_level[lvl]:
            n.cy = y


# ---------------------------------------------------------------------------
# 布局：x 坐标
# ---------------------------------------------------------------------------
#
# 规则（对照黄金坐标表）：
#   1. side=left  的入边目标 → cx = SIDE_LEFT_X (90)
#   2. side=right 的入边目标 → cx = SIDE_RIGHT_X (566)
#   3. side=bottom / "" 的单入边目标 → 继承上游 cx
#   4. 多入边节点（汇合点）→ cx = CENTER_X
#   5. 入口/孤立节点 → cx = CENTER_X

def _assign_x(graph: Graph) -> None:
    in_edges: dict[str, list[Edge]] = {nid: [] for nid in graph.nodes}
    out_edges: dict[str, list[Edge]] = {nid: [] for nid in graph.nodes}
    for e in graph.edges:
        in_edges[e.to_id].append(e)
        out_edges[e.from_id].append(e)

    # 重置
    for n in graph.nodes.values():
        n.cx = 0.0

    from collections import defaultdict
    by_level: dict[int, list[Node]] = defaultdict(list)
    for n in graph.nodes.values():
        by_level[n.level].append(n)

    # 决策侧支 x（水平连线的终端/脚本节点）
    SIDE_LEFT_X = 90.0
    SIDE_RIGHT_X = 566.0
    # 普通分叉子节点 x（斜线连线的处理节点）
    FORK_LEFT_X = 190.0
    FORK_RIGHT_X = 490.0

    for _ in range(10):
        for lvl in sorted(by_level.keys()):
            for n in by_level[lvl]:
                if n.cx != 0.0:
                    continue
                ins = in_edges[n.id]
                # 优先级 1：汇合点（入边 ≥ 2 且来源路径不同）→ cx = CENTER_X
                # 路径不同 = 来源 cx 不同 或 side 不同
                if len(ins) >= 2:
                    srcs_done = [(graph.nodes[e.from_id], e) for e in ins if e.from_id in graph.nodes]
                    paths = {(s.cx, e.side) for s, e in srcs_done if s.cx != 0.0}
                    if len(paths) > 1:
                        n.cx = CENTER_X
                        continue
                # 优先级 2：side 标记（决策侧支 / 普通分叉）
                for e in ins:
                    if e.side in ("left", "right"):
                        src = graph.nodes.get(e.from_id)
                        if src and src.type == "decision":
                            n.cx = SIDE_LEFT_X if e.side == "left" else SIDE_RIGHT_X
                        else:
                            n.cx = FORK_LEFT_X if e.side == "left" else FORK_RIGHT_X
                        break
                if n.cx != 0.0:
                    continue
                # 优先级 3：单入边继承上游
                if len(ins) == 1:
                    up = ins[0].from_id
                    if up in graph.nodes and graph.nodes[up].cx != 0.0:
                        n.cx = graph.nodes[up].cx
                        continue
                # 优先级 4：同层多入边但来源 cx 相同 → 也放中心
                if len(ins) >= 2:
                    n.cx = CENTER_X
                    continue
                # 入口/孤立
                n.cx = CENTER_X

    # 防御：同层节点 cx 重叠时自动错开
    for lvl in sorted(by_level.keys()):
        ns = by_level[lvl]
        used_cx: list[float] = []
        for n in sorted(ns, key=lambda x: x.cx):
            # 检查是否与已放置的节点 cx 重叠（且宽度会碰）
            overlap = False
            for ucx in used_cx:
                if abs(n.cx - ucx) < (n.width / 2 + 60):  # 60 = 最小半宽估算
                    overlap = True
                    break
            if overlap:
                # 找一个不重叠的位置
                for trial in [SIDE_LEFT_X, FORK_LEFT_X, CENTER_X, FORK_RIGHT_X, SIDE_RIGHT_X]:
                    ok = True
                    for ucx in used_cx:
                        if abs(trial - ucx) < (n.width / 2 + 60):
                            ok = False
                            break
                    if ok:
                        n.cx = trial
                        break
            used_cx.append(n.cx)


# ---------------------------------------------------------------------------
# 渲染
# ---------------------------------------------------------------------------

def _xml_escape(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def _node_polygon_points(n: Node) -> str:
    """菱形四个顶点。"""
    return f"{n.cx},{n.cy - DIAMOND_HALF_H} {n.cx + DIAMOND_HALF_W},{n.cy} {n.cx},{n.cy + DIAMOND_HALF_H} {n.cx - DIAMOND_HALF_W},{n.cy}"


def _render_node(n: Node, theme: dict[str, Any]) -> str:
    role_colors = theme.get("role_colors") or ROLE_COLORS
    colors = role_colors.get(n.role, role_colors.get("ai", ROLE_COLORS["ai"]))
    tcls = colors["text_class"]
    fill, stroke = _node_colors(n, theme)
    parts: list[str] = []
    if n.type == "decision":
        parts.append(f'  <polygon points="{_node_polygon_points(n)}" fill="{fill}" stroke="{stroke}" stroke-width="0.5"/>')
        parts.append(f'  <text class="{tcls}" x="{n.cx}" y="{n.cy}" text-anchor="middle" dominant-baseline="central">{_xml_escape(n.label)}</text>')
    else:
        x = n.cx - n.width / 2
        y = n.cy - n.height / 2
        rx = 10 if n.type in ("entry", "output") else 8
        parts.append(f'  <rect x="{x}" y="{y}" width="{n.width}" height="{n.height}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="0.5"/>')
        if n.subtitle:
            parts.append(f'  <text class="{tcls}" x="{n.cx}" y="{n.cy - 7}" text-anchor="middle" dominant-baseline="central">{_xml_escape(n.label)}</text>')
            sub_color = stroke if n.role in ("script", "output") else theme["subtitle"]
            parts.append(f'  <text class="ts" x="{n.cx}" y="{n.cy + 10}" text-anchor="middle" dominant-baseline="central" fill="{sub_color}">{_xml_escape(n.subtitle)}</text>')
        else:
            parts.append(f'  <text class="{tcls}" x="{n.cx}" y="{n.cy}" text-anchor="middle" dominant-baseline="central">{_xml_escape(n.label)}</text>')
    return "\n".join(parts)


def _edge_geometry(graph: Graph, e: Edge) -> dict[str, Any]:
    """返回一条边的几何信息。

    三种类型：
    - horizontal: 决策侧支，水平连线
    - vertical: 主流程向下，垂直连线
    - fork: 普通分叉，垂直→水平→垂直 折线（不画斜线）
    """
    src = graph.nodes[e.from_id]
    dst = graph.nodes[e.to_id]

    # 决策侧支：水平连线（src 是菱形，side=left/right）
    if src.type == "decision" and e.side in ("left", "right"):
        sx = src.cx + (-DIAMOND_HALF_W if e.side == "left" else DIAMOND_HALF_W)
        sy = src.cy
        # 到达端点始终是标准连接点（A4/C6）：同层→侧边中点，跨层→上中点
        if abs(src.cy - dst.cy) < 1:
            # 同层水平连线：到达 dst 侧边中点
            ex = dst.cx + (dst.width / 2 if e.side == "left" else -dst.width / 2)
            ey = dst.cy
            lx = (sx + ex) / 2
            ly = sy - 8
            return {"type": "horizontal", "x1": sx, "y1": sy, "x2": ex, "y2": ey, "lx": lx, "ly": ly}
        else:
            # 跨层：从菱形下顶点出发，折线到 dst 上中点
            sx2 = src.cx
            sy2 = src.cy + DIAMOND_HALF_H
            ex2 = dst.cx
            ey2 = dst.cy - (dst.height / 2 if dst.type != "decision" else DIAMOND_HALF_H)
            return {"type": "fork", "x1": sx2, "y1": sy2, "x2": ex2, "y2": ey2, "lx": (sx2 + ex2) / 2, "ly": (sy2 + ey2) / 2 - 6}

    # 普通分叉（src 不是决策，side=left/right）：折线，不画斜线
    if src.type != "decision" and e.side in ("left", "right"):
        sx = src.cx
        sy = src.cy + src.height / 2
        ex = dst.cx
        ey = dst.cy - dst.height / 2
        # label 放在水平段中点上方
        lx = (sx + ex) / 2
        ly = (sy + ey) / 2 - 6
        return {"type": "fork", "x1": sx, "y1": sy, "x2": ex, "y2": ey, "lx": lx, "ly": ly}

    # 默认：垂直连线（主流程向下）
    # 但如果 src.cx != dst.cx，转为折线（垂直→水平→垂直），避免斜线
    sx = src.cx
    sy = src.cy + (src.height / 2 if src.type != "decision" else DIAMOND_HALF_H)
    ex = dst.cx
    ey = dst.cy - (dst.height / 2 if dst.type != "decision" else DIAMOND_HALF_H)
    lx = (sx + ex) / 2
    ly = (sy + ey) / 2 - 6
    if abs(sx - ex) < 1:
        return {"type": "vertical", "x1": sx, "y1": sy, "x2": ex, "y2": ey, "lx": lx, "ly": ly}
    else:
        # cx 偏移 → 折线路由，同 fork 处理
        return {"type": "fork", "x1": sx, "y1": sy, "x2": ex, "y2": ey, "lx": lx, "ly": ly}


def _render_edge(graph: Graph, e: Edge, theme: dict[str, Any]) -> str:
    g = _edge_geometry(graph, e)
    parts: list[str] = []
    edge_class = "edge"
    if g["type"] == "fork":
        # 折线：垂直 → 水平 → 垂直（带箭头）
        mid_y = (g["y1"] + g["y2"]) / 2
        parts.append(f'  <line class="{edge_class}" x1="{g["x1"]}" y1="{g["y1"]}" x2="{g["x1"]}" y2="{mid_y}"/>')
        parts.append(f'  <line class="{edge_class}" x1="{g["x1"]}" y1="{mid_y}" x2="{g["x2"]}" y2="{mid_y}"/>')
        parts.append(f'  <line class="{edge_class}" x1="{g["x2"]}" y1="{mid_y}" x2="{g["x2"]}" y2="{g["y2"]}" marker-end="url(#arrow)"/>')
    else:
        line = f'  <line class="{edge_class}" x1="{g["x1"]}" y1="{g["y1"]}" x2="{g["x2"]}" y2="{g["y2"]}" marker-end="url(#arrow)"/>'
        parts.append(line)
    if e.label:
        lx, ly = g["lx"], g["ly"]
        anchor = "middle"
        halo_attr = ""
        if theme["use_halo"]:
            halo_attr = f' paint-order="stroke" stroke="{theme["label_halo"]}" stroke-width="3"'
        elif g["type"] == "vertical":
            # 透明主题：垂直边标签偏移到线一侧
            mid_x = g["x1"]  # 垂直边 x1 == x2
            if mid_x > CENTER_X:
                lx = mid_x - 6
                anchor = "end"
            elif mid_x < CENTER_X:
                lx = mid_x + 6
                anchor = "start"
            else:
                lx = mid_x + 6
                anchor = "start"
        parts.append(f'  <text class="ts" x="{lx}" y="{ly}" text-anchor="{anchor}"{halo_attr}>{_xml_escape(e.label)}</text>')
    return "\n".join(parts)


def _render_convergence(graph: Graph, theme: dict[str, Any]) -> list[str]:
    """汇合点：多条入边画成「垂直→水平→垂直」三段。

    触发条件（D5）：入边 ≥ 2 且存在不同路径（来源 cx 不同 或 side 不同）。
    当 src cx 相同但 side 不同时，各入边的垂直段终点 x 用各自的 fork 路由终点。
    """
    in_edges: dict[str, list[Edge]] = {nid: [] for nid in graph.nodes}
    for e in graph.edges:
        in_edges[e.to_id].append(e)

    parts: list[str] = []
    for nid, ins in in_edges.items():
        if len(ins) < 2:
            continue
        dst = graph.nodes[nid]
        # 检查入边是否来自不同路径（不同 cx 或不同 side）
        srcs = [graph.nodes[e.from_id] for e in ins if e.from_id in graph.nodes]
        paths = {(s.cx, e.side) for s, e in zip(srcs, ins) if s.id != nid}
        if len(paths) <= 1:
            continue  # 完全相同路径，不需要汇合三段
        # 汇合 y：dst 顶部上方一点
        dst_top = dst.cy - (dst.height / 2 if dst.type != "decision" else DIAMOND_HALF_H)
        mid_y = dst_top - 20
        # 每个 src 底部 → mid_y（垂直段，需要水平偏移时走折线）
        # 终点 x 取决于该边的 fork 路由：cx 不一致时用 dst.cx，一致时用 src.cx
        end_xs = []
        for s, e in zip(srcs, ins):
            sx = s.cx
            sy = s.cy + (s.height / 2 if s.type != "decision" else DIAMOND_HALF_H)
            # 如果这条边需要水平偏移（src.cx != dst.cx），垂直段终点用 dst.cx
            if abs(s.cx - dst.cx) < 1 and e.side in ("left", "right"):
                ex = dst.cx  # 侧支折到 dst cx
            elif abs(s.cx - dst.cx) < 1:
                ex = s.cx  # 同 cx bottom
            else:
                ex = dst.cx  # 不同 cx，折到 dst cx
            if abs(sx - ex) < 1:
                # 同 x：垂直线
                parts.append(f'  <line class="edge" x1="{sx}" y1="{sy}" x2="{ex}" y2="{mid_y}"/>')
                end_xs.append(ex)
            else:
                # 不同 x：折线（先垂直到 mid_y 再水平），不画斜线
                parts.append(f'  <line class="edge" x1="{sx}" y1="{sy}" x2="{sx}" y2="{mid_y}"/>')
                end_xs.append(sx)  # 垂直段终点是 sx，水平线从 sx 连到 dst.cx
        # 水平线（连接所有终点 x）
        left_x = min(end_xs)
        right_x = max(end_xs)
        if abs(left_x - right_x) >= 1:
            parts.append(f'  <line class="edge" x1="{left_x}" y1="{mid_y}" x2="{right_x}" y2="{mid_y}"/>')
        # 汇合点 → dst 顶部（垂直，带箭头）
        parts.append(f'  <line class="edge" x1="{dst.cx}" y1="{mid_y}" x2="{dst.cx}" y2="{dst_top}" marker-end="url(#arrow)"/>')
    return parts


def _render_loops(graph: Graph, theme: dict[str, Any]) -> list[str]:
    """回环虚线：从 src 左侧出发，沿图左边缘向上走到 dst 左侧。

    路由：src 左中 → (left_margin, src.cy) → (left_margin, dst.cy) → dst 左中
    全部虚线，最后一段带箭头。
    """
    parts: list[str] = []
    if not graph.loops:
        return parts

    # 计算图左边缘 x（所有节点最左再减 margin）
    all_left = [n.cx - n.width / 2 for n in graph.nodes.values()]
    left_margin = min(all_left) - 30

    for lp in graph.loops:
        src = graph.nodes.get(lp.from_id)
        dst = graph.nodes.get(lp.to_id)
        if not src or not dst:
            continue

        # src 左中点
        sx = src.cx - src.width / 2
        sy = src.cy
        # dst 左中点
        dx = dst.cx - dst.width / 2
        dy = dst.cy

        # 水平段：src 左中 → 左边缘
        parts.append(f'  <line class="edge-dash" x1="{sx}" y1="{sy}" x2="{left_margin}" y2="{sy}"/>')
        # 垂直段：左边缘上行/下行
        parts.append(f'  <line class="edge-dash" x1="{left_margin}" y1="{sy}" x2="{left_margin}" y2="{dy}"/>')
        # 水平段：左边缘 → dst 左中（带箭头）
        parts.append(f'  <line class="edge-dash" x1="{left_margin}" y1="{dy}" x2="{dx}" y2="{dy}" marker-end="url(#arrow)"/>')

        # 标签（在垂直段右侧，text-anchor=start 避免截断）
        if lp.label:
            lx = left_margin + 6
            ly = (sy + dy) / 2
            parts.append(f'  <text class="ts" text-anchor="start" x="{lx}" y="{ly}">{lp.label}</text>')

    return parts


def _render_legend(graph: Graph, svg_x: float, svg_w: float, theme: dict[str, Any]) -> str:
    items = theme.get("legend") or graph.legend or DEFAULT_LEGEND
    # 每个图例项：色块内放文本，宽度根据文本长度估算
    item_widths = [len(it["label"]) * 14 + 24 for it in items]
    item_height = 24
    gap = 12
    total = sum(item_widths) + gap * (len(items) - 1)
    start_x = svg_x + (svg_w - total) / 2
    max_bottom = max((n.cy + n.height / 2 for n in graph.nodes.values()), default=600)
    sep_y = max_bottom + 64
    legend_y = sep_y + 24
    parts: list[str] = []
    # 分隔线
    parts.append(f'  <line x1="{svg_x + 40}" y1="{sep_y}" x2="{svg_x + svg_w - 40}" y2="{sep_y}" stroke="{theme["edge_dash_stroke"]}" stroke-width="0.5"/>')
    # "图例" 标题
    parts.append(f'  <text class="ts" x="{svg_x + svg_w / 2}" y="{sep_y + 12}" text-anchor="middle" dominant-baseline="central">图例</text>')
    cur = start_x
    for it, w in zip(items, item_widths):
        fill = it["fill"]
        stroke = it["stroke"]
        parts.append(f'  <rect x="{cur}" y="{legend_y}" width="{w}" height="{item_height}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="0.5"/>')
        parts.append(f'  <text class="ts" x="{cur + w / 2}" y="{legend_y + item_height / 2}" text-anchor="middle" dominant-baseline="central">{_xml_escape(it["label"])}</text>')
        cur += w + gap
    return "\n".join(parts)


def _update_viewbox(graph: Graph) -> tuple[float, float, float, float]:
    xs, ys = [], []
    for n in graph.nodes.values():
        hw = (DIAMOND_HALF_W if n.type == "decision" else n.width / 2)
        hh = (DIAMOND_HALF_H if n.type == "decision" else n.height / 2)
        xs.extend([n.cx - hw, n.cx + hw])
        ys.extend([n.cy - hh, n.cy + hh])
    pad_x = 40
    pad_top = 24
    # 底部留白：主图底部到图例分隔线 64 + 标题 24 + 色块 24 + 底部 padding 20
    pad_bottom = 64 + 24 + 24 + 20
    # 左侧留白：如果有 loop，需要容纳左边缘路由 + 标签文字（~80px）
    if graph.loops:
        all_left = [n.cx - n.width / 2 for n in graph.nodes.values()]
        loop_left = min(all_left) - 30 - 80  # left_margin - label_width
        pad_x = max(pad_x, min(xs) - loop_left)
    min_x = min(xs) - pad_x
    max_x = max(xs) + pad_x
    max_y = max(ys) + pad_bottom
    return min_x, 0, max_x - min_x, max_y + pad_top


def _node_colors(n: Node, theme: dict[str, Any]) -> tuple[str, str]:
    """返回 (fill, stroke)。暗色主题用独立配色表。"""
    role_colors = theme.get("role_colors") or ROLE_COLORS
    colors = role_colors.get(n.role, role_colors.get("ai", ROLE_COLORS["ai"]))
    return colors["fill"], colors["stroke"]


def render_svg(graph: Graph, theme: dict[str, Any]) -> str:
    vb_x, vb_y, vb_w, vb_h = _update_viewbox(graph)
    parts: list[str] = []
    parts.append(f'<svg viewBox="{vb_x} {vb_y} {vb_w} {vb_h}" width="100%" role="img">')
    parts.append(f'  <title>{_xml_escape(graph.title)} 执行决策流程图</title>')
    # 背景（light/dark 画背景 rect；transparent 不画）
    if theme["bg"] is not None:
        parts.append(f'  <rect x="{vb_x}" y="{vb_y}" width="{vb_w}" height="{vb_h}" fill="{theme["bg"]}"/>')
    parts.append('  <defs>')
    arrow_stroke = theme["edge_stroke"]
    parts.append(f'    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">')
    parts.append(f'      <path d="M2 1L8 5L2 9" fill="none" stroke="{arrow_stroke}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>')
    parts.append('    </marker>')
    parts.append('  </defs>')
    text_color = theme["text"]
    subtitle_color = theme["subtitle"]
    edge_stroke = theme["edge_stroke"]
    edge_dash_stroke = theme["edge_dash_stroke"]
    parts.append('  <style>')
    parts.append(f'    .t {{ font-family: system-ui, sans-serif; font-size: 14px; fill: {text_color}; }}')
    parts.append(f'    .ts {{ font-family: system-ui, sans-serif; font-size: 12px; fill: {subtitle_color}; }}')
    parts.append(f'    .th {{ font-family: system-ui, sans-serif; font-size: 14px; font-weight: 500; fill: {text_color}; }}')
    parts.append(f'    .ths {{ font-family: system-ui, sans-serif; font-size: 12px; font-weight: 500; fill: {text_color}; }}')
    parts.append(f'    .edge {{ fill: none; stroke: {edge_stroke}; stroke-width: 1.2; }}')
    parts.append(f'    .edge-dash {{ fill: none; stroke: {edge_dash_stroke}; stroke-width: 0.8; stroke-dasharray: 4 3; }}')
    parts.append('  </style>')

    # 识别汇合点入边（由汇合三段接管，普通渲染跳过）
    # 条件同 _render_convergence：入边 ≥ 2 且存在不同路径（cx 或 side 不同）
    in_edges_map: dict[str, list[Edge]] = {nid: [] for nid in graph.nodes}
    for e in graph.edges:
        in_edges_map[e.to_id].append(e)
    convergence_edges: set[int] = set()
    for nid, ins in in_edges_map.items():
        if len(ins) < 2:
            continue
        srcs = [graph.nodes[e.from_id] for e in ins if e.from_id in graph.nodes]
        paths = {(s.cx, e.side) for s, e in zip(srcs, ins) if s.id != nid}
        if len(paths) > 1:
            for e in ins:
                convergence_edges.add(id(e))

    # 边（跳过汇合点入边）
    for e in graph.edges:
        if id(e) in convergence_edges:
            continue
        parts.append(_render_edge(graph, e, theme))
    # 汇合三段
    parts.extend(_render_convergence(graph, theme))
    # 回环（虚线，沿左边缘）
    parts.extend(_render_loops(graph, theme))
    # 节点
    for n in graph.nodes.values():
        parts.append(_render_node(n, theme))
    # 图例
    parts.append(_render_legend(graph, vb_x, vb_w, theme))
    parts.append('</svg>')
    return "\n".join(parts)


def render_html(graph: Graph, theme: dict[str, Any]) -> str:
    svg = render_svg(graph, theme)
    subtitle = graph.subtitle or ""
    bg = theme["bg"] if theme["bg"] else "transparent"
    title_color = theme["title_color"]
    subtitle_color = theme["subtitle"]
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{_xml_escape(graph.title)} 执行决策流程图</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: system-ui, -apple-system, sans-serif;
      background: {bg};
      color: {title_color};
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 24px 20px;
    }}
    h1 {{ font-size: 20px; font-weight: 500; margin-bottom: 8px; color: {title_color}; }}
    .subtitle {{ font-size: 13px; color: {subtitle_color}; margin-bottom: 16px; }}
    svg {{ max-width: 760px; width: 100%; height: auto; }}
  </style>
</head>
<body>
  <h1>{_xml_escape(graph.title)} · AI 执行决策流程图</h1>
  <p class="subtitle">{_xml_escape(subtitle)}</p>
{svg}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def layout(graph: Graph) -> None:
    _assign_depth(graph)
    _assign_y(graph)
    _assign_x(graph)


def main() -> None:
    parser = argparse.ArgumentParser(description="Skill 决策流程图生成器")
    parser.add_argument("nodes_json", help="nodes.json 路径")
    parser.add_argument("--out", default="docs/decision-flowchart.html", help="输出 HTML 路径")
    parser.add_argument("--theme", default="light", choices=list(THEMES.keys()), help="主题: light / dark / transparent")
    parser.add_argument("--json-out", default="", help="输出布局后 JSON 路径（调试用）")
    args = parser.parse_args()

    theme = THEMES[args.theme]
    graph = load_graph(args.nodes_json)
    layout(graph)

    html = render_html(graph, theme)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[完成] 节点: {len(graph.nodes)}, 边: {len(graph.edges)}, 主题: {args.theme}")
    print(f"[输出] {args.out}")

    if args.json_out:
        out = {
            "title": graph.title,
            "nodes": [
                {"id": n.id, "type": n.type, "role": n.role, "label": n.label,
                 "subtitle": n.subtitle, "level": n.level,
                 "cx": n.cx, "cy": n.cy, "width": n.width, "height": n.height}
                for n in graph.nodes.values()
            ],
            "edges": [{"from": e.from_id, "to": e.to_id, "label": e.label, "side": e.side} for e in graph.edges],
        }
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"[调试] {args.json_out}")


if __name__ == "__main__":
    main()
