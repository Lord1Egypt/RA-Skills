"""reader 契约 -> 出图底图（base-map/v1）适配层。

为什么需要这一层
----------------
cad-file-reader 只出"证据"：单位写在 scale_unit_audit[] 或逐条候选里，
图纸没写单位时它如实标 missing_unit，不会替项目拍板。出图侧必须按 mm 落笔，
所以需要一层把"候选单位"变成"施工口径"，并留下判定依据。

硬规则：
- 单位优先级：顶层声明 > reader 单位审计 > 逐条几何声明 > 人工确认。
- 多来源单位冲突 -> 拒绝（exit 4），不挑一个"看起来对"的。
- 没有任何单位时，必须 `--unit` + `--confirmed-by` 人工确认，不猜 10/1000 倍。
- 输入只读；输出只写 out-dir，绝不回写 reader 契约。
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from . import __version__
from .model import SiteLayoutError, UnitError, normalize_unit

BASE_MAP_SCHEMA = "site-layout-base-map/v1"
UNIT_TO_MM = {"mm": 1.0, "cm": 10.0, "m": 1000.0, "ft": 304.8}
SUPPORTED_UNITS = tuple(UNIT_TO_MM)
REDLINE_KEYWORDS = ("REDLINE", "BOUNDARY", "红线", "用地")
FENCE_KEYWORDS = ("FENCE", "HOARD", "围挡")
_TOP_KEYS = ("coord_unit", "unit", "units", "drawing_unit")
_ROW_KEYS = ("units", "unit", "drawing_unit")


# 识图硬链路：DWG/DXF/PDF → lis-skill-bus → cad-file-reader → cad-contract/v1
# → lis-skill-bus → 本技能。本技能只消费 reader 契约，不提供任何直读 CAD 的逃生口。
READER_SITE_SCHEMA = "cad-site-geometry/v1"
READER_CONTRACT_VERSION = "cad-contract/v1"
DIRECT_CAD_SUFFIXES = (".dwg", ".dxf", ".pdf", ".dwt", ".dwf", ".dws")


@dataclass
class UnitDecision:
    unit: str
    mm_per_unit: float
    basis: str
    evidence: List[Dict[str, str]] = field(default_factory=list)
    confirmed_by: str = ""
    warnings: List[str] = field(default_factory=list)


def validate_reader_path(path: Path) -> None:
    """路径闸门：读取前就拒绝直读 CAD/PDF，避免把二进制当 JSON 解析。"""
    suffix = path.suffix.lower()
    if suffix in DIRECT_CAD_SUFFIXES:
        raise SiteLayoutError(
            f"拒绝直接读取 {suffix}：识图必须经 lis-skill-bus → cad-file-reader，"
            "由 reader 输出 cad-site-geometry/v1（cad-contract/v1）后再交给本技能；"
            "本技能不打开、不解析任何 CAD/PDF 文件"
        )


def validate_reader_contract(path: Path, data: Any) -> None:
    """闸门：只接受经 lis-skill-bus 的 cad-file-reader 契约。

    - 直接给 DWG/DXF/PDF 一律拒绝（exit 2），不降级自行解图；
    - schema 必须是 cad-site-geometry/v1，契约版本必须是 cad-contract/v1；
    - 本函数故意不提供 CAD_ALLOW_DIRECT 之类逃生口。
    """
    validate_reader_path(path)
    if not isinstance(data, dict):
        raise SiteLayoutError(
            "reader 契约必须是 JSON 对象；请先走 lis-skill-bus → cad-file-reader"
        )
    contract = data.get("contract") if isinstance(data.get("contract"), dict) else {}
    schema = _text(data.get("schema") or contract.get("schema"))
    version = _text(contract.get("contract_version"))
    if schema != READER_SITE_SCHEMA or version != READER_CONTRACT_VERSION:
        raise SiteLayoutError(
            "非 cad-file-reader 契约：要求 schema={} 且 contract.contract_version={}；"
            "实际 schema={!r}、contract_version={!r}。"
            "请先走 lis-skill-bus → cad-file-reader 重新出契约".format(
                READER_SITE_SCHEMA, READER_CONTRACT_VERSION, schema, version)
        )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _distance(a: Sequence[float], b: Sequence[float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _polygon_area(points: Sequence[Sequence[float]]) -> float:
    if len(points) < 3:
        return 0.0
    return abs(
        sum(
            points[i][0] * points[(i + 1) % len(points)][1]
            - points[(i + 1) % len(points)][0] * points[i][1]
            for i in range(len(points))
        )
        / 2.0
    )


_ANNOTATION_TOKENS = (
    "标注", "文字", "定位", "间距", "角点", "图例", "说明", "注释",
    "ANNO", "DIM", "TEXT", "LABEL", "LEGEND", "NOTE",
)


def _is_annotation_layer(layer: str) -> bool:
    """标注/定位/图例层不是边界几何；混进来会把红线串成两个点。"""
    upper = (layer or "").upper()
    return any(token.upper() in upper for token in _ANNOTATION_TOKENS)


_UNIT_IN_TEXT = re.compile(r"(\d+(?:\.\d+)?)\s*(mm|cm|ft|m)\b", re.IGNORECASE)
_UNIT_WEAK_CONTEXT = ("打印", "线宽", "线型", "出图", "图框", "字高", "标注样式")
_UNIT_DECLARE_CONTEXT = ("单位", "坐标为", "以米计", "以毫米计", "mm计", "m计")


def _unit_text_strength(text: str, unit: str) -> Optional[str]:
    """判断一条文字能否证明指定坐标单位，返回 weak/strong/None。

    只认“单位：mm”这类显式声明，或像“6000mm”“3.5m”这样量级合理的尺寸。
    标高（H=56.85m）、线宽（1.2mm）、图名等都不作为坐标单位证据。
    """
    value = _text(text)
    target = _text(unit).lower()
    if not value or not target:
        return None
    matches = [m for m in _UNIT_IN_TEXT.finditer(value) if m.group(2).lower() == target]
    if not matches:
        return None
    if value.startswith(("H=", "h=")) or "标高" in value:
        return None
    if any(token in value for token in _UNIT_WEAK_CONTEXT):
        return "weak"
    declared = any(token in value for token in _UNIT_DECLARE_CONTEXT)
    for match in matches:
        try:
            number = float(match.group(1))
        except ValueError:
            continue
        if target == "mm":
            if number <= 5.0:
                continue
            return "strong"
        if target in ("m", "cm", "ft"):
            if 0.001 <= number <= 100000.0:
                return "strong"
    if declared:
        return "strong"
    return "weak"


def _audit_row_is_weak(row: Dict[str, Any], unit: str) -> bool:
    evidence = row.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        return False
    strengths = [
        _unit_text_strength(_text(item.get("text")), unit)
        for item in evidence
        if isinstance(item, dict)
    ]
    strengths = [item for item in strengths if item]
    return not any(item == "strong" for item in strengths)


def assemble_loops(
    segments: Sequence[Tuple[float, float, float, float]],
    tolerance_mm: float = 50.0,
) -> List[Tuple[List[Tuple[float, float]], bool, Optional[float]]]:
    """端点吸附后把每条连通链各自走成折线，返回 [(顶点, 闭合, 首尾缺口)]。

    与 assemble_loop 共用同一套聚类/走链算法；区别是这里返回全部连通分量，
    供主体轮廓（可能由多栋/多个大厅组成）逐栋提取，而不是只留最大的一条。
    """
    usable = [seg for seg in segments if _distance((seg[0], seg[1]), (seg[2], seg[3])) > 1e-9]
    if not usable:
        return []

    # 端点聚类：O(n^2) 只用于边界/围挡/主体轮廓，量级在千段以内。
    raw_points: List[Tuple[float, float]] = []
    for seg in usable:
        raw_points.append((seg[0], seg[1]))
        raw_points.append((seg[2], seg[3]))
    parent = list(range(len(raw_points)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for i in range(len(raw_points)):
        for j in range(i):
            if _distance(raw_points[i], raw_points[j]) <= tolerance_mm + 1e-9:
                union(i, j)

    clusters: Dict[int, List[Tuple[float, float]]] = {}
    for index, point in enumerate(raw_points):
        clusters.setdefault(find(index), []).append(point)
    node_xy = {
        root: (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
        for root, pts in clusters.items()
    }

    edges: List[Tuple[int, int, float]] = []
    adjacency: Dict[int, List[int]] = {node: [] for node in node_xy}
    for index, seg in enumerate(usable):
        a, b = find(2 * index), find(2 * index + 1)
        if a == b:
            continue
        edge_index = len(edges)
        edges.append((a, b, _distance(node_xy[a], node_xy[b])))
        adjacency[a].append(edge_index)
        adjacency[b].append(edge_index)

    if not edges:
        return []

    # 连通分量
    unvisited = set(range(len(edges)))
    components: List[List[int]] = []
    while unvisited:
        seed = unvisited.pop()
        stack = [seed]
        component = [seed]
        while stack:
            edge = stack.pop()
            for node in (edges[edge][0], edges[edge][1]):
                for nxt in adjacency[node]:
                    if nxt in unvisited:
                        unvisited.remove(nxt)
                        stack.append(nxt)
                        component.append(nxt)
        components.append(component)

    def walk(component: List[int]) -> List[Tuple[float, float]]:
        unused = set(component)
        degree: Dict[int, int] = {}
        for edge in component:
            for node in (edges[edge][0], edges[edge][1]):
                degree[node] = degree.get(node, 0) + 1
        endpoints = sorted(node for node, count in degree.items() if count == 1)
        start = endpoints[0] if endpoints else edges[component[0]][0]
        points: List[Tuple[float, float]] = [node_xy[start]]
        current, previous = start, None
        while True:
            candidates = [edge for edge in adjacency[current] if edge in unused]
            if not candidates:
                break
            # 优先不走回上一点；仍有多个时取较短边，避免被装饰性长线带偏。
            candidates.sort(key=lambda edge: (
                (edges[edge][1] if edges[edge][0] == current else edges[edge][0]) == previous,
                edges[edge][2],
                edge,
            ))
            edge = candidates[0]
            unused.remove(edge)
            nxt = edges[edge][1] if edges[edge][0] == current else edges[edge][0]
            points.append(node_xy[nxt])
            previous, current = current, nxt
            if current == start:
                break
        return points

    out: List[Tuple[List[Tuple[float, float]], bool, Optional[float]]] = []
    for component in components:
        points = walk(component)
        if len(points) < 2:
            continue
        gap = _distance(points[-1], points[0])
        closed = len(points) >= 4 and gap <= tolerance_mm + 1e-9
        out.append((points, closed, gap))
    return out


def assemble_loop(
    segments: Sequence[Tuple[float, float, float, float]],
    tolerance_mm: float = 50.0,
    close_gap_mm: Optional[float] = None,
    evidence: Optional[Dict[str, Any]] = None,
) -> Tuple[List[Tuple[float, float]], bool, Optional[float]]:
    """端点吸附串成闭合环；返回顶点、是否闭合、首尾缺口（mm）。

    旧实现从输入第一段出发单向贪心，若第一段落在环的中间，只能串到一侧
    端点就停，典型表现是“136 段红线只剩 2 个点”。这里改为：
    1) 先按 tolerance 把端点聚成节点；
    2) 找连通分量；
    3) 每个分量从端点起走完整条链（无端点则从任意点起）；
    4) 选长度/面积最大的分量，闭合时把首尾差吸附到 0。
    """
    best: List[Tuple[float, float]] = []
    best_score = -1.0
    for points, closed, _gap in assemble_loops(segments, tolerance_mm):
        if len(points) < 2:
            continue
        score = _polygon_area(points) if closed else -1.0
        if score <= 0:
            score = sum(_distance(points[i], points[i + 1]) for i in range(len(points) - 1))
        if score > best_score:
            best, best_score = points, score

    if not best:
        return [], False, None
    gap = _distance(best[-1], best[0])
    gap_before_close = gap
    closed = len(best) >= 4 and gap <= tolerance_mm + 1e-9
    closed_by_gap_snap = False
    if closed:
        best[-1] = best[0]
        best = best[:-1]
        gap = 0.0
    elif (
        close_gap_mm is not None
        and len(best) >= 4
        and gap <= close_gap_mm + 1e-9
    ):
        # 端点聚类保持小容差以保住真实短边；只在收口时允许一次较大的缺口吸附。
        # 例：真实总图 136 段红线在 50 mm 容差下走成 137 点，首尾差 1926.691 mm，
        # 按 2500 mm 收口可闭合，同时不把 1.9 m 的曲线弦长误并成一点。
        best = best[:-1]
        closed = True
        closed_by_gap_snap = True
        gap = 0.0
    if evidence is not None:
        evidence["gap_before_close_mm"] = round(gap_before_close, 3)
        evidence["closed_by_gap_snap"] = closed_by_gap_snap
        evidence["close_gap_mm"] = close_gap_mm
    return best, closed, gap


def _iter_declared(values: Any) -> Iterable[str]:
    if isinstance(values, (list, tuple)):
        for item in values:
            text = _text(item)
            if text:
                yield text
    else:
        text = _text(values)
        if text:
            yield text


def _basis_of(source: str) -> str:
    """把 evidence source 归一成 top/audit/geometry。"""
    head = source.split(":", 1)[0]
    return head.split("[", 1)[0]


def collect_units(data: Dict[str, Any]) -> List[Dict[str, str]]:
    """收集所有单位声明，返回 [{unit, source, evidence}]。"""
    found: List[Dict[str, str]] = []

    def add(
        value: Any,
        source: str,
        evidence: str,
        weak_units: Optional[Dict[str, bool]] = None,
    ) -> None:
        for raw in _iter_declared(value):
            try:
                unit = normalize_unit(raw)
            except UnitError:
                continue
            weak = bool(weak_units and weak_units.get(unit))
            found.append(
                {"unit": unit, "source": source, "evidence": evidence, "weak": weak}
            )

    for key in _TOP_KEYS:
        add(data.get(key), f"top:{key}", f"顶层字段 {key}")
    audit = data.get("scale_unit_audit")
    if isinstance(audit, list):
        for index, row in enumerate(audit):
            if not isinstance(row, dict):
                continue
            texts = [
                _text(item.get("text"))
                for item in (row.get("evidence") or [])
                if isinstance(item, dict) and _text(item.get("text"))
            ]
            weak_units: Dict[str, bool] = {}
            for key in _ROW_KEYS:
                for raw in _iter_declared(row.get(key)):
                    try:
                        declared_unit = normalize_unit(raw)
                    except UnitError:
                        continue
                    weak_units[declared_unit] = _audit_row_is_weak(row, declared_unit)
            detail = f"单位审计第 {index + 1} 条"
            if texts:
                detail += "：" + "；".join(texts[:3])
            if any(weak_units.values()):
                detail += "（未找到能证明坐标单位的明确尺寸/单位声明）"
            for key in _ROW_KEYS:
                add(row.get(key), f"audit[{index}]:{key}", detail, weak_units=weak_units)
    rows = data.get("site_geometry")
    if isinstance(rows, list):
        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                continue
            for key in _ROW_KEYS:
                add(row.get(key), f"geometry[{index}]:{key}", f"几何第 {index + 1} 条")
    return found


def resolve_unit(
    data: Dict[str, Any], override: Optional[str] = None, confirmed_by: str = ""
) -> UnitDecision:
    found = collect_units(data)
    unique = {item["unit"] for item in found}
    if len(unique) > 1:
        detail = "；".join(f"{item['unit']}（{item['evidence']}）" for item in found[:8])
        raise UnitError(f"单位声明互相冲突：{detail}；请先统一图纸单位，不能自动挑一个")
    if len(unique) == 1:
        unit = next(iter(unique))
        weak_only = all(item.get("weak") for item in found)
        if override:
            declared = normalize_unit(override)
            if declared != unit:
                if not weak_only:
                    raise UnitError(
                        f"--unit {declared} 与读者声明 {unit} 冲突；以图纸为准，请先核对"
                    )
                return UnitDecision(
                    unit=declared,
                    mm_per_unit=UNIT_TO_MM[declared],
                    basis="manual_confirmed",
                    evidence=found,
                    confirmed_by=confirmed_by,
                    warnings=[
                        f"reader 审计单位 {unit} 仅来自打印/线宽类文字，不能证明坐标单位；"
                        f"已按人工确认 {declared} 换算"
                    ],
                )
            return UnitDecision(
                unit=unit,
                mm_per_unit=UNIT_TO_MM[unit],
                basis="manual_confirmed",
                evidence=found,
                confirmed_by=confirmed_by,
                warnings=["reader 单位证据偏弱，已由人工确认同一单位"],
            )
        if weak_only:
            raise UnitError(
                "reader 单位审计只找到打印/线宽类文字（如 1.2mm），不足以证明坐标单位；"
                "请用 --unit mm|m|cm|ft 并给 --confirmed-by 人工确认，本工具不猜"
            )
        basis = _basis_of(found[0]["source"]) if found else "reader"
        return UnitDecision(
            unit=unit,
            mm_per_unit=UNIT_TO_MM[unit],
            basis=basis,
            evidence=found,
            confirmed_by="",  # 读者已取证，人工未参与判定
            warnings=[],
        )
    if override:
        unit = normalize_unit(override)
        if unit not in UNIT_TO_MM:  # normalize_unit 已限定，防御式保留
            raise UnitError(f"不支持的单位 {unit}")
        return UnitDecision(
            unit=unit,
            mm_per_unit=UNIT_TO_MM[unit],
            basis="manual_confirmed",
            evidence=[],
            confirmed_by=confirmed_by,
            warnings=["图纸未声明单位：按人工确认值换算，已在图签与报告中留痕"],
        )
    raise UnitError(
        "图纸未声明单位（reader 标 missing_unit）：请用 --unit mm|m|cm|ft "
        "并同时给 --confirmed-by 记录确认人；本工具不猜 10/1000 倍"
    )


def _convert(value: Any, factor: float) -> Optional[float]:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return round(number * factor, 3)


def _collect_segments(
    rows: Sequence[Any], factor: float, keywords: Sequence[str]
) -> List[Tuple[float, float, float, float]]:
    out: List[Tuple[float, float, float, float]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        geometry = row.get("geometry")
        if not isinstance(geometry, (list, tuple)) or len(geometry) < 4:
            continue
        layer = _text(row.get("layer") or row.get("layer_name") or row.get("category"))
        if keywords and not any(keyword.upper() in layer.upper() for keyword in keywords):
            continue
        coords = [_convert(value, factor) for value in geometry[:4]]
        if any(item is None for item in coords):
            continue
        out.append((coords[0], coords[1], coords[2], coords[3]))  # type: ignore[arg-type]
    return out


_BOUNDARY_LAYER_RANK = (
    ("用地红线", 0),
    ("建筑红线", 1),
    ("道路红线", 2),
    ("红线", 3),
    ("REDLINE", 3),
    ("BOUNDARY", 4),
    ("用地", 5),
)


def _boundary_layer_rank(layer: str) -> Optional[int]:
    """边界层等级；数值越小越权威。未命中返回 None。"""
    upper = (layer or "").upper()
    for token, rank in _BOUNDARY_LAYER_RANK:
        if token.upper() in upper:
            return rank
    return None


def _collect_boundary_segments(
    rows: Sequence[Any],
    factor: float,
    tolerance_mm: float = 50.0,
    explicit_layer: str = "",
    close_gap_mm: Optional[float] = None,
) -> Tuple[List[Tuple[float, float, float, float]], Dict[str, Any]]:
    """按图层分组收集边界线段，只选一个权威层，禁止跨层混串。

    旧实现把“0-控制线-用地红线”和“1-标注-间距-建筑距红线”等一起喂给
    assemble_loop，标注层的短线段会把真正的 136 段红线挤掉。这里：
    1) 排除标注/文字/定位/图例层；
    2) 同层分组，不跨“用地/建筑/道路红线”混取；
    3) 按层权威度优先，其次闭合、面积、段数。
    """
    groups: Dict[str, List[Tuple[float, float, float, float]]] = {}
    annotation_layers: Dict[str, int] = {}
    ignored = 0
    for row in rows:
        if not isinstance(row, dict):
            continue
        layer = _text(row.get("layer") or row.get("layer_name") or row.get("category"))
        if explicit_layer and layer != explicit_layer:
            continue
        if _is_annotation_layer(layer):
            annotation_layers[layer] = annotation_layers.get(layer, 0) + 1
            ignored += 1
            continue
        if _boundary_layer_rank(layer) is None:
            continue
        geometry = row.get("geometry")
        if not isinstance(geometry, (list, tuple)) or len(geometry) < 4:
            continue
        coords = [_convert(value, factor) for value in geometry[:4]]
        if any(item is None for item in coords):
            continue
        groups.setdefault(layer, []).append(
            (coords[0], coords[1], coords[2], coords[3])  # type: ignore[arg-type]
        )

    candidates: List[Dict[str, Any]] = []
    for layer, segments in groups.items():
        loop_evidence: Dict[str, Any] = {}
        vertices, closed, gap = assemble_loop(
            segments, tolerance_mm, close_gap_mm, evidence=loop_evidence
        )
        area = _polygon_area(vertices) if closed else 0.0
        candidates.append(
            {
                "layer": layer,
                "rank": _boundary_layer_rank(layer),
                "segments": len(segments),
                "vertices": len(vertices),
                "closed": closed,
                "gap_mm": None if gap is None else round(gap, 3),
                "gap_before_close_mm": loop_evidence.get("gap_before_close_mm"),
                "closed_by_gap_snap": bool(loop_evidence.get("closed_by_gap_snap")),
                "area_m2": round(area / 1_000_000.0, 3) if closed else None,
                "_points": vertices,
            }
        )
    candidates.sort(
        key=lambda item: (
            item["rank"],
            0 if item["closed"] else 1,
            -(item["area_m2"] or 0.0),
            -item["segments"],
            item["layer"],
        )
    )
    selection: Dict[str, Any] = {
        "requested_layer": explicit_layer,
        "selected_layer": "",
        "selected_segments": 0,
        "annotation_segments_excluded": ignored,
        "annotation_layers": annotation_layers,
        "tolerance_mm": tolerance_mm,
        "close_gap_mm": close_gap_mm,
        "candidates": [
            {key: value for key, value in item.items() if key != "_points"}
            for item in candidates[:20]
        ],
    }
    if not candidates:
        return [], selection
    chosen = candidates[0]
    selection.update(
        {
            "selected_layer": chosen["layer"],
            "selected_segments": chosen["segments"],
            "selected_vertices": chosen["vertices"],
            "selected_closed": chosen["closed"],
            "selected_gap_mm": chosen["gap_mm"],
            "selected_gap_before_close_mm": chosen.get("gap_before_close_mm"),
            "selected_closed_by_gap_snap": chosen.get("closed_by_gap_snap"),
            "selected_area_m2": chosen["area_m2"],
        }
    )
    selection["_points"] = chosen["_points"]
    return groups[chosen["layer"]], selection


# 主体轮廓候选层：先认“建筑-屋顶-外轮廓”，再认“建筑-平面/轮廓”，最后认 BUILDING/FOOTPRINT。
# 高差线、户型分隔、屋脊、阳台、构架、填充不是外轮廓，命中即跳过。
_BUILDING_OUTLINE_REJECT = (
    "高差", "分隔", "屋脊", "屋檐", "阳台", "凸窗", "构架", "填充",
    "标注", "注释", "图例", "说明",
)


def _building_layer_rank(layer: str) -> Optional[int]:
    """主体轮廓层等级；数值越小越权威，未命中返回 None。"""
    text = _text(layer)
    upper = text.upper()
    if any(token in text for token in _BUILDING_OUTLINE_REJECT):
        return None
    if "建筑" in text and "外轮廓" in text:
        if "地下室" in text:
            return 3
        return 0
    if "建筑" in text and ("轮廓" in text or "平面" in text):
        return 1
    if "BACKGROUND" in upper:
        return None
    for token, rank in (("FOOTPRINT", 2), ("BUILDING", 2), ("结构轮廓", 2), ("主体轮廓", 2)):
        if token.upper() in upper:
            return rank
    return None


def _loop_area_m2(points: Sequence[Sequence[float]]) -> float:
    return _polygon_area(points) / 1_000_000.0


def _collect_buildings(
    rows: Sequence[Any],
    factor: float,
    redline_vertices: Sequence[Sequence[float]],
    tolerance_mm: float = 50.0,
    explicit_layer: str = "",
    min_area_m2: float = 200.0,
    margin_mm: float = 30_000.0,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """从 site_geometry 的建筑类图层提取主体轮廓（逐栋闭合环）。

    为什么要裁剪：真实总图常把同一栋楼同时画在“图面坐标”和“原点附近的详图/块”
    两套坐标里，不裁剪会把相距几公里的两套线串成一个假环（面积可达几十平方公里）。
    这里先用红线外扩 margin 做窗口，再按层分组、逐连通分量走环、只留闭合且面积达标的环。
    """
    selection: Dict[str, Any] = {
        "requested_layer": explicit_layer,
        "window_mm": None,
        "min_area_m2": min_area_m2,
        "layers": {},
        "rejected_outside_window": 0,
        "rejected_not_closed": 0,
        "rejected_too_small": 0,
        "buildings": 0,
    }
    window: Optional[Tuple[float, float, float, float]] = None
    if redline_vertices:
        xs = [float(p[0]) for p in redline_vertices]
        ys = [float(p[1]) for p in redline_vertices]
        window = (min(xs) - margin_mm, min(ys) - margin_mm,
                  max(xs) + margin_mm, max(ys) + margin_mm)
        selection["window_mm"] = [round(v, 1) for v in window]

    groups: Dict[str, List[Tuple[float, float, float, float]]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        layer = _text(row.get("layer") or row.get("layer_name") or row.get("category"))
        if explicit_layer and layer != explicit_layer:
            continue
        if _building_layer_rank(layer) is None:
            continue
        geometry = row.get("geometry")
        if not isinstance(geometry, (list, tuple)) or len(geometry) < 4:
            continue
        coords = [_convert(value, factor) for value in geometry[:4]]
        if any(item is None for item in coords):
            continue
        seg = (coords[0], coords[1], coords[2], coords[3])  # type: ignore[arg-type]
        if window is not None:
            inside = all(
                window[0] <= seg[i] <= window[2] and window[1] <= seg[i + 1] <= window[3]
                for i in (0, 2)
            )
            if not inside:
                selection["rejected_outside_window"] += 1
                continue
        groups.setdefault(layer, []).append(seg)

    found: List[Dict[str, Any]] = []
    for layer, segments in groups.items():
        rank = _building_layer_rank(layer)
        loops = assemble_loops(segments, tolerance_mm)
        kept = 0
        for points, closed, gap in loops:
            if not closed:
                selection["rejected_not_closed"] += 1
                continue
            area = _loop_area_m2(points)
            if area < min_area_m2:
                selection["rejected_too_small"] += 1
                continue
            found.append({
                "layer": layer,
                "rank": rank,
                "footprint": [[round(float(x), 3), round(float(y), 3)] for x, y in points],
                "area_m2": round(area, 3),
                "status": "candidate",
                "confidence": 0.86,
                "gap_mm": round(gap, 3) if gap is not None else None,
            })
            kept += 1
        selection["layers"][layer] = {
            "rank": rank, "segments": len(segments), "loops": len(loops), "kept": kept,
        }

    # 权威层优先，同层按面积降序：buildings[0] 即主体最大单栋
    found.sort(key=lambda item: (item["rank"], -item["area_m2"]))
    selection["buildings"] = len(found)
    return found, selection


def _convert_polygon(value: Any, factor: float) -> List[List[float]]:
    points: List[List[float]] = []
    if not isinstance(value, list):
        return points
    for item in value:
        if not isinstance(item, (list, tuple)) or len(item) < 2:
            continue
        x = _convert(item[0], factor)
        y = _convert(item[1], factor)
        if x is None or y is None:
            continue
        points.append([x, y])
    if len(points) >= 2 and _distance(points[0], points[-1]) <= 1e-9:
        points = points[:-1]
    return points


def prepare(
    data: Dict[str, Any],
    source: Path,
    unit_override: Optional[str] = None,
    confirmed_by: str = "",
    tolerance_mm: float = 50.0,
    boundary_layer: str = "",
    close_gap_mm: Optional[float] = None,
    building_layer: str = "",
    min_building_area_m2: float = 200.0,
) -> Dict[str, Any]:
    if not isinstance(data, dict):
        raise SiteLayoutError("reader 契约顶层必须是对象")
    decision = resolve_unit(data, unit_override, confirmed_by)
    factor = decision.mm_per_unit

    rows = data.get("site_geometry") or []
    if not isinstance(rows, list):
        raise SiteLayoutError("site_geometry 必须是数组")
    converted: List[Dict[str, Any]] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            continue
        geometry = row.get("geometry")
        if not isinstance(geometry, (list, tuple)) or len(geometry) < 4:
            continue
        coords = [_convert(value, factor) for value in geometry[:4]]
        if any(item is None for item in coords):
            continue
        converted.append(
            {
                "category": _text(row.get("category")),
                "layer": _text(row.get("layer") or row.get("layer_name")),
                "system": _text(row.get("system")),
                "geometry": coords,
                "status": _text(row.get("status")) or "candidate",
            }
        )

    warnings = list(decision.warnings)
    if not converted:
        warnings.append("reader 契约没有 site_geometry 线段；底图将为空，出图只能看到塔吊与结论点")

    contract_id = _text(data.get("contract_id")) or _text((data.get("contract") or {}).get("contract_id"))
    if not contract_id:
        warnings.append("reader 契约无 contract_id；出图契约闸门会判缺失，只能 --draft")

    direct = data.get("redline") or data.get("boundary")
    redline_vertices = _convert_polygon(direct, factor)
    redline_segments: List[Tuple[float, float, float, float]] = []
    boundary_selection: Dict[str, Any] = {
        "requested_layer": boundary_layer,
        "selected_layer": "direct:redline",
        "selected_segments": 0,
        "annotation_segments_excluded": 0,
        "annotation_layers": {},
        "candidates": [],
        "tolerance_mm": tolerance_mm,
        "close_gap_mm": close_gap_mm,
    }
    if redline_vertices:
        redline_closed = len(redline_vertices) >= 3
        redline_gap = 0.0 if redline_closed else None
        redline_segments = _collect_segments(rows, factor, REDLINE_KEYWORDS)
    else:
        redline_segments, boundary_selection = _collect_boundary_segments(
            rows, factor, tolerance_mm, boundary_layer, close_gap_mm
        )
        redline_vertices = boundary_selection.pop("_points", [])
        if not redline_vertices:
            redline_vertices, redline_closed, redline_gap = assemble_loop(
                redline_segments, tolerance_mm, close_gap_mm
            )
        else:
            redline_closed = bool(boundary_selection.get("selected_closed"))
            redline_gap = boundary_selection.get("selected_gap_mm")
            if redline_gap is None and not redline_closed:
                redline_gap = assemble_loop(redline_segments, tolerance_mm, close_gap_mm)[2]
    if not redline_vertices:
        warnings.append("未找到红线/用地边界几何；出图自检第 1 条会 fail，请补图层或手工指定边界")
    elif not redline_closed:
        gap_text = "未知" if redline_gap is None else f"{redline_gap:.1f} mm"
        warnings.append(f"红线未闭合，首尾缺口 {gap_text}；只会按已串接顶点出图")
    elif boundary_selection.get("selected_layer"):
        warnings.append(
            f"红线取自单一图层「{boundary_selection['selected_layer']}」"
            f"（{boundary_selection.get('selected_segments')} 段，已排除 "
            f"{boundary_selection.get('annotation_segments_excluded', 0)} 条标注层线段）"
        )
        if boundary_selection.get("selected_closed_by_gap_snap"):
            warnings.append(
                "红线首尾原缺口 "
                f"{boundary_selection.get('selected_gap_before_close_mm')} mm，"
                f"按 --close-gap-mm {boundary_selection.get('close_gap_mm')} 收口；"
                "已闭合但缺口证据保留，需人工复核"
            )

    buildings, building_selection = _collect_buildings(
        rows,
        factor,
        redline_vertices,
        tolerance_mm=tolerance_mm,
        explicit_layer=building_layer,
        min_area_m2=min_building_area_m2,
    )
    structure_outline = buildings[0]["footprint"] if buildings else []
    if buildings:
        warnings.append(
            f"主体轮廓取自图层「{buildings[0]['layer']}」，{len(buildings[0]['footprint'])} 个顶点，"
            f"面积 {buildings[0]['area_m2']} m²，共识别 {len(buildings)} 栋/环；仍需与建筑总平面图核对"
        )
    else:
        warnings.append(
            "未从 reader 契约提取到主体建筑外轮廓（site_geometry 无建筑类图层或未闭合）；"
            "generate_site_layout.py 会拒绝按假定矩形出 A/B/C，需补 --requirements building.footprint 或用 --building-layer 指定图层"
        )

    fence_segments = _collect_segments(rows, factor, FENCE_KEYWORDS)
    fence_vertices, fence_closed, _fence_gap = assemble_loop(
        fence_segments, tolerance_mm, close_gap_mm
    )

    xs = [point[0] for point in redline_vertices] or [seg[i] for seg in redline_segments for i in (0, 2)]
    ys = [point[1] for point in redline_vertices] or [seg[i] for seg in redline_segments for i in (1, 3)]
    extents = [min(xs), min(ys), max(xs), max(ys)] if xs and ys else None

    # 红线窗口外过滤：真实总图常把同一项目同时画在图面坐标和原点附近的详图/其他图幅，
    # 不裁剪会把相距几百公里的线段一起带进出图范围，导致主图缩成一个点、标注跨全图。
    geometry_selection: Dict[str, Any] = {
        "window_mm": None,
        "margin_mm": 50_000.0,
        "kept": len(converted),
        "rejected_outside_window": 0,
    }
    if extents and converted:
        margin = geometry_selection["margin_mm"]
        window = (extents[0] - margin, extents[1] - margin,
                  extents[2] + margin, extents[3] + margin)
        kept_rows: List[Dict[str, Any]] = []
        for row in converted:
            gx0, gy0, gx1, gy1 = (float(v) for v in row["geometry"])
            if (min(gx0, gx1) <= window[2] and max(gx0, gx1) >= window[0]
                    and min(gy0, gy1) <= window[3] and max(gy0, gy1) >= window[1]):
                kept_rows.append(row)
        rejected = len(converted) - len(kept_rows)
        geometry_selection.update({
            "window_mm": [round(v, 1) for v in window],
            "kept": len(kept_rows),
            "rejected_outside_window": rejected,
        })
        if rejected:
            warnings.append(
                f"已过滤红线窗口（外扩 {margin / 1000.0:.0f} m）外底图线段 {rejected} 条，"
                f"保留 {len(kept_rows)} 条；过滤项多为原点详图/其他图幅，出图与标注只用窗口内几何"
            )
        converted = kept_rows

    reader_contract = data.get("contract") or {}
    return {
        "schema": BASE_MAP_SCHEMA,
        "contract_id": contract_id,
        "source_file": str(source),
        "source_sha256": _sha256(source),
        "source_schema": _text(data.get("schema")),
        "reader_version": _text(reader_contract.get("reader_version")),
        "drawing_sha256": _text(reader_contract.get("source_sha256")),
        "reader_contract_id": _text(reader_contract.get("contract_id")),
        "coord_unit": "mm",
        "unit": {
            "basis": decision.basis,
            "source_unit": decision.unit,
            "mm_per_unit": decision.mm_per_unit,
            "evidence": decision.evidence,
            "confirmed_by": decision.confirmed_by,
        },
        "prepared_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "prepared_by": f"site-layout-plan/{__version__}",
        "redline": redline_vertices,
        "redline_closed": redline_closed,
        "redline_gap_mm": redline_gap,
        "redline_area_m2": round(_polygon_area(redline_vertices) / 1_000_000.0, 3) if redline_closed else None,
        "boundary_selection": boundary_selection,
        "fence": fence_vertices,
        "fence_closed": fence_closed,
        "buildings": buildings,
        "structure_outline": structure_outline,
        "building_selection": building_selection,
        "site_geometry": converted,
        "geometry_selection": geometry_selection,
        "extents_mm": extents,
        "warnings": warnings,
        "boundary": "底图适配层只做单位换算、红线串接与留痕；不重新识图、不判定合规。",
    }


def render_markdown(base_map: Dict[str, Any], base_json: Optional[Path] = None) -> str:
    unit = base_map["unit"]
    extent = base_map.get("extents_mm")
    lines = [
        "# 出图底图（base-map）适配报告",
        "",
        f"- 源文件：`{base_map['source_file']}`",
        f"- 契约号：`{base_map['contract_id'] or '缺失'}`",
        f"- reader 版本：`{base_map['reader_version'] or '未知'}`",
        f"- 统一单位：`{base_map['coord_unit']}`（源单位 `{unit['source_unit']}`，系数 {unit['mm_per_unit']:g}）",
        f"- 单位依据：`{unit['basis']}`" + (f"，确认人 `{unit['confirmed_by']}`" if unit.get("confirmed_by") else ""),
        f"- 红线：{len(base_map['redline'])} 个顶点，闭合={'是' if base_map['redline_closed'] else '否'}"
        + (f"，面积 {base_map['redline_area_m2']} m²" if base_map.get("redline_area_m2") else ""),
        f"- 主体轮廓：{len(base_map.get('buildings') or [])} 栋/环"
        + (f"，最大一栋 {base_map['buildings'][0]['area_m2']} m²（图层 `{base_map['buildings'][0]['layer']}`）"
           if base_map.get("buildings") else "（未提取到，出 A/B/C 前必须补）"),
        f"- 几何线段：{len(base_map['site_geometry'])} 条"
        + (f"（已过滤窗口外 {base_map['geometry_selection']['rejected_outside_window']} 条）"
           if (base_map.get("geometry_selection") or {}).get("rejected_outside_window") else ""),
        f"- 范围（mm）：{extent if extent else '空'}",
        "",
        "## 单位证据",
        "",
    ]
    if unit["evidence"]:
        lines += ["| 单位 | 来源 | 证据 |", "|---|---|---|"]
        for item in unit["evidence"]:
            lines.append(f"| {item['unit']} | {item['source']} | {item['evidence']} |")
    else:
        lines.append("- 无 reader 单位证据：按人工确认值换算。")
    lines += ["", "## 警告", ""]
    lines += [f"- {warning}" for warning in base_map["warnings"]] or ["- 无"]
    lines += [
        "",
        "## 下一步",
        "",
        "```bash",
        "python3 scripts/crane_check.py \\",
        "  --handoff site_handoff.json --fleet crane_fleet.json \\",
        "  --baseline baseline.json --out-dir out/crane",
        "python3 scripts/draw_layout.py \\",
        f"  --site {base_json or 'out/prepared/base-map.json'} \\",
        "  --handoff site_handoff.json --check out/crane/crane_check.json \\",
        "  --baseline baseline.json --layout crane_layout.json --out-dir out/layout",
        "```",
        "",
    ]
    return "\n".join(lines)


def write_outputs(base_map: Dict[str, Any], out_dir: Path, stem: str = "base-map") -> Tuple[Path, Path]:
    out_dir = out_dir.expanduser().resolve()
    source = Path(base_map["source_file"]).expanduser().resolve()
    json_path = (out_dir / f"{stem}.json").resolve()
    md_path = (out_dir / f"{stem}.md").resolve()
    if json_path == source:
        raise SiteLayoutError("输出路径与输入契约相同；请换 --out-dir")
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(base_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(base_map, json_path), encoding="utf-8")
    return json_path, md_path
