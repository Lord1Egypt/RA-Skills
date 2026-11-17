#!/usr/bin/env python3



from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

from cad_common import round_number as _round  # noqa: E402,F401

import argparse
import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import cad_structure_model as structure


SCHEMA = "cad-concrete-ledger/v0.1"


def _number(value: Any) -> float:
    return float(value or 0.0)

def _difference(candidate: float, reference: float | None) -> tuple[float | None, float | None]:
    if reference is None:
        return None, None
    difference = candidate - reference
    percentage = difference / reference * 100.0 if reference else None
    return difference, percentage


def parse_reference_values(items: list[str]) -> dict[str, float]:
    result: dict[str, float] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"对照值必须是“名称=数值”：{item}")
        name, raw = item.split("=", 1)
        name = name.strip()
        if not name:
            raise ValueError(f"对照值名称为空：{item}")
        result[name] = float(raw.strip())
    return result


def parse_transform(value: str) -> tuple[float, float]:
    parts = [part.strip() for part in str(value).split(",")]
    if len(parts) != 2:
        raise ValueError("平移必须为 dx,dy")
    return float(parts[0]), float(parts[1])


def _normalize_prefab_code(value: Any) -> str:
    text = re.sub(r"\s+", "", str(value or "")).upper()
    match = re.fullmatch(r"(YDB|YKTB|AL)-?0*(\d+)", text)
    if not match:
        return text
    return f"{match.group(1)}-{int(match.group(2))}"


def _point_in_bbox(
        point: tuple[float, float],
        bbox: list[float] | tuple[float, ...] | None,
        margin: float = 0.0) -> bool:
    if not bbox or len(bbox) != 4:
        return True
    x, y = point
    return (
        float(bbox[0]) - margin <= x <= float(bbox[2]) + margin
        and float(bbox[1]) - margin <= y <= float(bbox[3]) + margin
    )


def _polyline_points(entity: Any) -> list[tuple[float, float]]:
    kind = entity.dxftype()
    if kind == "LWPOLYLINE":
        rows = list(entity.get_points("xyb"))
        if any(abs(float(row[2] or 0.0)) > 1e-9 for row in rows):
            from dev_dxf import make_path

            points = [
                (float(vertex.x), float(vertex.y))
                for vertex in make_path(entity).flattening(distance=1.0)
            ]
        else:
            points = [(float(row[0]), float(row[1])) for row in rows]
    elif kind == "POLYLINE_2D":
        points = [
            (float(point[0]), float(point[1]))
            for point in entity.get_points("xy")
        ]
    else:
        return []
    if len(points) > 1 and points[0] == points[-1]:
        points.pop()
    return points


def _assign_prefab_labels(
        polygons: list[dict[str, Any]],
        labels: list[dict[str, Any]],
        max_distance_mm: float = 5000.0) -> None:
    candidates: list[tuple[float, int, int, str]] = []
    for label_index, label in enumerate(labels):
        point = (float(label["x"]), float(label["y"]))
        code = _normalize_prefab_code(label.get("text"))
        if not code:
            continue
        for polygon_index, polygon in enumerate(polygons):
            points = [
                (float(row[0]), float(row[1]))
                for row in polygon.get("points") or []
            ]
            if len(points) < 3:
                continue
            if structure._point_in_polygon(point, points):
                distance = 0.0
            else:
                center = structure._polygon_center(points)
                distance = math.hypot(
                    point[0] - center[0], point[1] - center[1])
                if distance > max_distance_mm:
                    continue
            candidates.append(
                (distance, polygon_index, label_index, code))
    used_polygons: set[int] = set()
    used_labels: set[int] = set()
    for distance, polygon_index, label_index, code in sorted(candidates):
        if polygon_index in used_polygons or label_index in used_labels:
            continue
        polygon = polygons[polygon_index]
        polygon["component_code"] = code
        polygon["component_raw_label"] = labels[label_index].get("text")
        polygon["label_distance_mm"] = _round(distance, 1)
        used_polygons.add(polygon_index)
        used_labels.add(label_index)
    for polygon_index, polygon in enumerate(polygons):
        if polygon_index not in used_polygons:
            polygon["component_code"] = "UNLABELED"


def _load_prefab_polygons(
        path: Path | None,
        layer_pattern: str,
        transform: tuple[float, float],
        max_gap_mm: float,
        analysis_bbox: list[float] | None = None,
        label_layer_pattern: str = r"S-PC-编号") -> list[dict[str, Any]]:
    if path is None:
        return []
    from dev_dxf import readfile

    doc = readfile(path)
    tx, ty = transform
    polygons: list[dict[str, Any]] = []
    for entity in doc.modelspace():
        if entity.dxftype() not in ("LWPOLYLINE", "POLYLINE_2D"):
            continue
        if not re.search(layer_pattern, str(entity.dxf.layer or ""), re.I):
            continue
        source_points = _polyline_points(entity)
        if len(source_points) < 3:
            continue
        points = [(x + tx, y + ty) for x, y in source_points]
        center = structure._polygon_center(points)
        if not _point_in_bbox(center, analysis_bbox, margin=1000.0):
            continue
        area_m2 = abs(structure._polygon_area(points)) / 1_000_000.0
        if not 0.1 <= area_m2 <= 100.0:
            continue
        polygons.append({
            "points": points,
            "area_m2": _round(area_m2),
            "bbox": [_round(value, 1)
                     for value in structure._polygon_bbox(points)],
            "source_type": entity.dxftype(),
            "source_handle": str(entity.dxf.handle or ""),
            "closed": bool(getattr(entity, "closed", True)),
        })

    if polygons:
        labels: list[dict[str, Any]] = []
        for entity in doc.modelspace():
            if entity.dxftype() not in ("TEXT", "MTEXT"):
                continue
            if not re.search(
                    label_layer_pattern,
                    str(entity.dxf.layer or ""),
                    re.I):
                continue
            try:
                insert = entity.dxf.insert
            except AttributeError:
                continue
            x = float(insert.x) + tx
            y = float(insert.y) + ty
            if not _point_in_bbox((x, y), analysis_bbox, margin=1000.0):
                continue
            text = (
                entity.dxf.text
                if entity.dxftype() == "TEXT"
                else entity.text
            )
            labels.append({"x": x, "y": y, "text": text})
        _assign_prefab_labels(polygons, labels)
        return polygons

    segments: list[dict[str, Any]] = []
    for entity in doc.modelspace():
        if entity.dxftype() != "LINE":
            continue
        if not re.search(layer_pattern, str(entity.dxf.layer or ""), re.I):
            continue
        a = (
            float(entity.dxf.start.x) + tx,
            float(entity.dxf.start.y) + ty,
        )
        b = (
            float(entity.dxf.end.x) + tx,
            float(entity.dxf.end.y) + ty,
        )
        if not (
                _point_in_bbox(a, analysis_bbox, margin=1000.0)
                or _point_in_bbox(b, analysis_bbox, margin=1000.0)):
            continue
        segments.append({"a": [a[0], a[1]], "b": [b[0], b[1]]})
    fallback = structure._open_chain_polygons(
        segments,
        snap_mm=10.0,
        min_area_m2=0.1,
        max_area_m2=100.0,
        max_gap_mm=max_gap_mm,
    )
    for polygon in fallback:
        polygon["source_type"] = "LINE-chain"
        polygon["component_code"] = "UNLABELED"
    return fallback


def _load_prefab_model(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    raw_components = (
        data.get("components")
        if isinstance(data.get("components"), dict)
        else data
    )
    components: dict[str, dict[str, float | int]] = {}
    for raw_code, raw_values in raw_components.items():
        if not isinstance(raw_values, dict):
            continue
        code = _normalize_prefab_code(raw_code)
        if not code.startswith(("YDB-", "YKTB-", "AL-")):
            continue
        components[code] = {
            "count": int(raw_values.get("count") or 0),
            "projection_area_m2": _round(
                raw_values.get("projection_area_m2")),
            "volume_m3": _round(raw_values.get("volume_m3")),
        }
    return {
        "schema": data.get("schema") or "cad-prefab-model/v0.1",
        "floor": data.get("floor") or "",
        "components": components,
    }


def _polygon_distance(
        left: list[tuple[float, float]],
        right: list[tuple[float, float]]) -> float:
    if len(left) < 2 or len(right) < 2:
        return math.inf
    return min(
        min(
            structure._point_segment_distance(
                point, start, end)
            for point in source
            for start, end in zip(target, target[1:] + target[:1])
        )
        for source, target in ((left, right), (right, left))
    )


def _prefab_analysis(
        panels: list[dict[str, Any]],
        prefab_polygons: list[dict[str, Any]],
        reference_area_m2: float | None,
        model_components: dict[str, Any] | None = None) -> dict[str, Any]:
    assignments: list[dict[str, Any]] = []
    unassigned: list[dict[str, Any]] = []
    observed_by_panel: dict[str, float] = {}
    observed_by_code: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"count": 0, "area_m2": 0.0})
    for index, polygon in enumerate(prefab_polygons, 1):
        prefab_id = (
            str(polygon.get("source_handle") or "")
            or f"YDB-G{index:04d}"
        )
        code = _normalize_prefab_code(
            polygon.get("component_code") or "UNLABELED")
        observed_by_code[code]["count"] += 1
        observed_by_code[code]["area_m2"] += _number(
            polygon.get("area_m2"))
        points = [
            (float(point[0]), float(point[1]))
            for point in polygon.get("points") or []
        ]
        if len(points) < 3:
            continue
        center = structure._polygon_center(points)
        candidates = []
        for panel in panels:
            panel_points = [
                (float(point[0]), float(point[1]))
                for point in panel.get("points") or []
            ]
            if len(panel_points) >= 3 and structure._point_in_polygon(
                    center, panel_points):
                candidates.append(panel)
        if not candidates:
            nearest = None
            for panel in panels:
                panel_points = [
                    (float(point[0]), float(point[1]))
                    for point in panel.get("points") or []
                ]
                if len(panel_points) < 3:
                    continue
                distance = _polygon_distance(points, panel_points)
                if nearest is None or distance < nearest[0]:
                    nearest = (distance, panel)
            if nearest is not None and nearest[0] <= 500.0:
                panel = nearest[1]
                area = _number(polygon.get("area_m2"))
                observed_by_panel[panel["id"]] = (
                    observed_by_panel.get(panel["id"], 0.0) + area)
                assignments.append({
                    "prefab_id": prefab_id,
                    "component_code": code,
                    "area_m2": _round(area),
                    "bbox": polygon.get("bbox"),
                    "panel_id": panel["id"],
                    "panel_area_m2": _round(panel.get("area_m2")),
                    "assignment_status": "nearest-boundary-review",
                    "boundary_distance_mm": _round(nearest[0], 1),
                })
                continue
            unassigned.append({
                "prefab_id": prefab_id,
                "component_code": code,
                "area_m2": polygon.get("area_m2"),
                "bbox": polygon.get("bbox"),
                "reason": "构件中心未落入板拓扑面",
            })
            continue
        panel = min(candidates, key=lambda row: _number(row.get("area_m2")))
        area = _number(polygon.get("area_m2"))
        observed_by_panel[panel["id"]] = (
            observed_by_panel.get(panel["id"], 0.0) + area)
        assignments.append({
            "prefab_id": prefab_id,
            "component_code": code,
            "area_m2": _round(area),
            "bbox": polygon.get("bbox"),
            "panel_id": panel["id"],
            "panel_area_m2": _round(panel.get("area_m2")),
            "assignment_status": "center-inside",
            "boundary_distance_mm": 0.0,
        })
    for panel in panels:
        observed = observed_by_panel.get(panel["id"], 0.0)
        panel["observed_prefab_area_m2"] = _round(observed)
        panel["material_observation"] = (
            "prefab-observed" if observed > 0 else "not-observed"
        )
    observed_total = sum(
        _number(polygon.get("area_m2")) for polygon in prefab_polygons)
    assigned_total = sum(row["area_m2"] for row in assignments)
    raw_model_rows = (
        (model_components or {}).get("components")
        if isinstance(model_components, dict)
        else None
    ) or {}
    model_rows = {
        _normalize_prefab_code(code): row
        for code, row in raw_model_rows.items()
    }
    component_rows: list[dict[str, Any]] = []
    for code in sorted(set(observed_by_code) | set(model_rows)):
        observed = observed_by_code.get(code) or {}
        expected = model_rows.get(code) or {}
        observed_count = int(observed.get("count") or 0)
        expected_count = int(expected.get("count") or 0)
        factor = None
        status = "model-unlisted" if not expected else "cad-unobserved"
        if observed_count and expected_count:
            raw_factor = expected_count / observed_count
            rounded_factor = round(raw_factor)
            if abs(raw_factor - rounded_factor) <= 0.01:
                factor = int(rounded_factor)
                status = "exact-repeat" if factor > 1 else "exact"
            else:
                status = "count-mismatch"
        component_rows.append({
            "code": code,
            "status": status,
            "cad_template_count": observed_count,
            "model_count": expected_count,
            "repetition_factor": factor,
            "cad_template_area_m2": _round(
                observed.get("area_m2")),
            "model_projection_area_m2": _round(
                expected.get("projection_area_m2")),
            "model_volume_m3": _round(expected.get("volume_m3")),
            "reconstructed_projection_area_m2": (
                _round(_number(observed.get("area_m2")) * factor)
                if factor is not None else None
            ),
        })
    model_area_total = (
        sum(_number(row.get("projection_area_m2"))
            for row in model_rows.values())
        if model_rows else None
    )
    model_volume_total = (
        sum(_number(row.get("volume_m3"))
            for row in model_rows.values())
        if model_rows else None
    )
    reconstructed_area = sum(
        _number(row.get("reconstructed_projection_area_m2"))
        for row in component_rows
        if row.get("reconstructed_projection_area_m2") is not None
    )
    effective_reference_area = (
        model_area_total if model_area_total is not None
        else reference_area_m2
    )
    coverage = None
    if effective_reference_area:
        coverage = observed_total / effective_reference_area * 100.0
    matched_model_codes = sum(
        1 for row in component_rows
        if int(row.get("model_count") or 0) > 0
        and int(row.get("cad_template_count") or 0) > 0
    )
    model_code_count = sum(
        1 for row in model_rows.values()
        if int(row.get("count") or 0) > 0
    )
    code_match_pct = (
        matched_model_codes / model_code_count * 100.0
        if model_code_count else None
    )
    assignment_status_counts = Counter(
        row.get("assignment_status") for row in assignments)
    return {
        "polygon_count": len(prefab_polygons),
        "observed_area_m2": _round(observed_total),
        "source_type_counts": dict(Counter(
            row.get("source_type") or "unknown"
            for row in prefab_polygons)),
        "assigned_polygon_count": len(assignments),
        "assigned_area_m2": _round(assigned_total),
        "assigned_panel_count": len(observed_by_panel),
        "assigned_by_center_count": int(
            assignment_status_counts.get("center-inside") or 0),
        "assigned_by_boundary_count": int(
            assignment_status_counts.get("nearest-boundary-review") or 0),
        "unassigned_polygon_count": len(unassigned),
        "unassigned_area_m2": _round(
            sum(_number(row.get("area_m2")) for row in unassigned)),
        "reference_area_m2": (
            _round(effective_reference_area)
            if effective_reference_area is not None else None
        ),
        "reference_area_source": (
            "prefab-model-json"
            if model_area_total is not None else "cli-reference"
        ),
        "reference_coverage_pct": (
            _round(coverage, 2) if coverage is not None else None
        ),
        "model_component_count": model_code_count,
        "matched_model_component_count": matched_model_codes,
        "model_component_match_pct": (
            _round(code_match_pct, 2)
            if code_match_pct is not None else None
        ),
        "model_projection_area_m2": (
            _round(model_area_total)
            if model_area_total is not None else None
        ),
        "model_prefab_volume_m3": (
            _round(model_volume_total)
            if model_volume_total is not None else None
        ),
        "reconstructed_template_area_m2": (
            _round(reconstructed_area)
            if reconstructed_area else None
        ),
        "reconstruction_difference_m2": (
            _round(model_area_total - reconstructed_area, 4)
            if model_area_total is not None and reconstructed_area
            else None
        ),
        "components": component_rows,
        "assignments": assignments,
        "unassigned": unassigned,
    }


def _gate(gate_id: str,
          title: str,
          status: str,
          evidence: str,
          action: str) -> dict[str, Any]:
    return {
        "id": gate_id,
        "title": title,
        "status": status,
        "evidence": evidence,
        "action": action,
    }


def build_ledger(
        model: dict[str, Any],
        references: dict[str, float],
        reference_floor: str,
        floor_mapping_note: str,
        prefab_path: Path | None,
        prefab_layer: str,
        prefab_transform: tuple[float, float],
        prefab_gap_mm: float,
        prefab_reference_area_m2: float | None,
        prefab_label_layer: str = r"S-PC-编号",
        prefab_model: dict[str, Any] | None = None,
        report_title: str = "阶段十三：二层混凝土分账收口",
        floor_mapping_source: str = "") -> dict[str, Any]:
    beam = model["quantities"]["beam"]
    wall = model["quantities"]["wall"]
    edge = model["quantities"]["edge_member"]
    column = model["quantities"]["column"]
    slab = model["quantities"]["slab"]
    panels = model["members"]["slab_panels"]
    slab_rough = sum(
        _number(panel.get("area_m2"))
        * _number(panel.get("thickness_mm"))
        / 1000.0
        for panel in panels
    )
    vertical_candidate = (
        _number(wall.get("candidate_volume_m3"))
        + _number(edge.get("candidate_volume_m3"))
        + _number(column.get("candidate_volume_m3"))
    )
    candidate_total = (
        _number(beam.get("topology_volume_m3"))
        + vertical_candidate
        + slab_rough
    )
    panel_points = [
        (float(point[0]), float(point[1]))
        for panel in panels
        for point in panel.get("points") or []
    ]
    analysis_bbox = (
        structure._polygon_bbox(panel_points)
        if len(panel_points) >= 3 else None
    )
    prefab_polygons = _load_prefab_polygons(
        prefab_path,
        prefab_layer,
        prefab_transform,
        prefab_gap_mm,
        analysis_bbox=analysis_bbox,
        label_layer_pattern=prefab_label_layer,
    )
    prefab = _prefab_analysis(
        panels,
        prefab_polygons,
        prefab_reference_area_m2,
        model_components=prefab_model,
    )

    comparisons = [
        {
            "component": "梁",
            "scope": "全图拓扑中心线粗算，未扣支座",
            "candidate_value_m3": _round(beam.get("topology_volume_m3")),
            "reference_label": "梁及连梁",
            "reference_value_m3": references.get("梁及连梁"),
            "status": "research-candidate",
        },
        {
            "component": "墙柱",
            "scope": "墙条带 + 边缘构件 + 独立柱候选",
            "candidate_value_m3": _round(vertical_candidate),
            "reference_label": "剪力墙",
            "reference_value_m3": references.get("剪力墙"),
            "status": "candidate",
        },
        {
            "component": "板",
            "scope": "69 个板拓扑面按当前板厚粗折，未扣洞口且材料未闭合",
            "candidate_value_m3": _round(slab_rough),
            "reference_label": "板体系",
            "reference_value_m3": references.get("板体系"),
            "status": "research-candidate",
        },
        {
            "component": "合计",
            "scope": "梁拓扑 + 墙柱候选 + 板厚粗折",
            "candidate_value_m3": _round(candidate_total),
            "reference_label": "对照合计",
            "reference_value_m3": sum(references.values()) if references else None,
            "status": "research-only",
        },
    ]
    for row in comparisons:
        difference, percentage = _difference(
            _number(row["candidate_value_m3"]),
            row.get("reference_value_m3"),
        )
        row["difference_m3"] = _round(difference) if difference is not None else None
        row["difference_pct"] = (
            _round(percentage, 2) if percentage is not None else None
        )

    edge_labels = edge.get("label_summary") or {}
    thickness = slab.get("attribute_summary") or {}
    review_and_default = (
        int(thickness.get("thickness_review_required_count") or 0)
        + int(thickness.get("thickness_default_count") or 0)
    )
    gates = [
        _gate(
            "floor-mapping",
            "CAD图纸与模型楼层映射",
            "pass" if (floor_mapping_source and not floor_mapping_note)
            else "warn",
            (
                floor_mapping_note
                or (
                    f"对照模型层：{reference_floor or '-'}；"
                    f"映射依据：{floor_mapping_source or '未记录'}"
                )
            ),
            "按结构标高、轴网和构件编号确认图纸与模型楼层的唯一映射关系。",
        ),
        _gate(
            "beam-topology-assignment",
            "梁拓扑编号归属",
            "pass" if (
                int(beam.get("topology_unassigned_run_count") or 0) == 0
                and int(beam.get("topology_ambiguous_run_count") or 0) == 0
            ) else "warn",
            (
                f"已归属 {beam.get('topology_assigned_run_count')} / "
                f"{beam.get('topology_run_count')} 段；"
                f"竞争编号 {beam.get('topology_ambiguous_run_count')} 段；"
                f"默认截面 {((beam.get('topology_status_counts') or {}).get('assumed-default-section') or {}).get('count', 0)} 段"
            ),
            "继续复核未归属、竞争编号和默认截面段。",
        ),
        _gate(
            "beam-support-confirmation",
            "梁支座与净跨确认",
            "pass" if (
                int(beam.get("clear_span_count") or 0)
                == int(beam.get("count") or 0)
            ) else "fail",
            (
                f"确认 {beam.get('clear_span_count')} 根，"
                f"复核 {beam.get('review_clear_span_count')} 根，"
                f"推定 {beam.get('inferred_clear_span_count')} 根；"
                f"剩余假定端 {sum(len(row.get('inferred_end_supports') or []) for row in model['members']['beams'])} 个"
            ),
            "回原图确认端部构件、T 形节点及支座宽度；未完成前不进入梁钢筋翻样。",
        ),
        _gate(
            "vertical-classification",
            "墙柱候选归类",
            "pass" if (
                int(edge_labels.get("mirror_review_count") or 0) == 0
                and int(edge_labels.get("unlabeled_count") or 0) == 0
                and int((column.get("label_summary") or {}).get("unlabeled_count") or 0) == 0
            ) else "warn",
            (
                f"边缘构件 {edge.get('count')} 个，其中镜像待复核 "
                f"{edge_labels.get('mirror_review_count', 0)} 个；"
                f"独立柱 {column.get('count')} 个，未标注 "
                f"{(column.get('label_summary') or {}).get('unlabeled_count', 0)} 个"
            ),
            "复核待确认镜像编号，并完成墙条带、边缘构件和独立柱的最终归类。",
        ),
        _gate(
            "slab-thickness",
            "板厚证据",
            "pass" if review_and_default == 0 else "fail",
            (
                f"直接尺寸 {thickness.get('direct_thickness_count', 0)} 项，"
                f"HATCH 待复核 {thickness.get('thickness_review_required_count', 0)} 项，"
                f"默认 {thickness.get('thickness_default_count', 0)} 项"
            ),
            "按原始图例复核 HATCH，并消除默认板厚。",
        ),
        _gate(
            "slab-material",
            "叠合/现浇材料体系",
            "fail",
            (
                f"CAD 已观测预制底板 {prefab.get('polygon_count', 0)} 块、"
                f"{prefab.get('observed_area_m2', 0):.4f} m2，"
                f"其中落入板拓扑面 {prefab.get('assigned_area_m2', 0):.4f} m2；"
                f"模型参考面积 {prefab.get('reference_area_m2') or 0:.4f} m2；"
                f"编码匹配 {prefab.get('matched_model_component_count', 0)} / "
                f"{prefab.get('model_component_count', 0)}"
            ),
            "补齐预制板拆分图的所有构件实例，并分别建立预制底板、后浇叠合层、现浇板和板缝。",
        ),
        _gate(
            "slab-openings",
            "板洞口扣减",
            "fail" if int(thickness.get("opening_candidate_count") or 0) else "pass",
            f"洞口候选 {thickness.get('opening_candidate_count', 0)} 个，尚未形成可靠扣减环",
            "闭合洞口边线并区分楼梯洞口、管井、降板和叠合板拼缝。",
        ),
    ]
    return {
        "schema": SCHEMA,
        "source_model_schema": model.get("schema"),
        "floor": model.get("floor") or {},
        "reference_floor": reference_floor,
        "floor_mapping_note": floor_mapping_note,
        "floor_mapping_source": floor_mapping_source,
        "floor_mapping": {
            "status": (
                "confirmed"
                if floor_mapping_source and not floor_mapping_note
                else "needs-review"
            ),
            "reference_floor": reference_floor,
            "source": floor_mapping_source,
        },
        "status": "混凝土分账候选收口；材料体系、洞口和梁支座复核未闭合",
        "formal_ready": False,
        "report_title": report_title,
        "reference_values": {
            key: _round(value) for key, value in references.items()
        },
        "quantities": {
            "beam_topology_volume_m3": _round(
                beam.get("topology_volume_m3")),
            "beam_confirmed_clear_volume_m3": _round(
                beam.get("clear_span_volume_m3")),
            "beam_review_clear_volume_m3": _round(
                beam.get("review_clear_span_volume_m3")),
            "beam_inferred_clear_volume_m3": _round(
                beam.get("inferred_clear_span_volume_m3")),
            "vertical_candidate_volume_m3": _round(vertical_candidate),
            "slab_rough_volume_m3": _round(slab_rough),
            "candidate_total_volume_m3": _round(candidate_total),
        },
        "comparisons": comparisons,
        "prefab": prefab,
        "gate_summary": dict(Counter(row["status"] for row in gates)),
        "gates": gates,
        "status_counts": {
            "beam_quantity": dict(Counter(
                row.get("quantity_status") for row in model["members"]["beams"])),
            "slab_material_observation": dict(Counter(
                row.get("material_observation") for row in panels)),
        },
    }


def render_markdown(result: dict[str, Any]) -> str:
    quantities = result["quantities"]
    prefab = result["prefab"]
    lines = [
        f"# {result.get('report_title') or '混凝土分账'}",
        "",
        "## 结论",
        "",
        "本轮只完成混凝土分账的候选收口和门槛审计，不输出正式工程量。"
        "梁支座、板材料体系、洞口扣减和板厚依据仍未闭合。",
        "",
        "## 楼层映射",
        "",
        f"- 图纸模型输入：`{result.get('floor', {}).get('label') or '-'}`，"
        f"结构标高 `{result.get('floor', {}).get('elevation_mm') or '-'} mm`。",
        f"- 模型对照楼层：`{result.get('reference_floor') or '-'}`。",
        f"- 映射状态：`{result.get('floor_mapping', {}).get('status') or '-'}`；"
        f"依据：{result.get('floor_mapping_source') or '未记录'}。",
        "",
        "## 候选分账与模型对照",
        "",
        "| 构件 | CAD口径 | CAD值m3 | 模型对照 | 对照值m3 | 差异m3 | 差异率 | 状态 |",
        "|---|---|---:|---|---:|---:|---:|---|",
    ]
    for row in result["comparisons"]:
        reference = (
            f"{row['reference_value_m3']:.4f}"
            if row.get("reference_value_m3") is not None else "-"
        )
        difference = (
            f"{row['difference_m3']:+.4f}"
            if row.get("difference_m3") is not None else "-"
        )
        percentage = (
            f"{row['difference_pct']:+.2f}%"
            if row.get("difference_pct") is not None else "-"
        )
        lines.append(
            f"| {row['component']} | {row['scope']} | "
            f"{row['candidate_value_m3']:.4f} | {row['reference_label']} | "
            f"{reference} | {difference} | {percentage} | {row['status']} |"
        )
    lines += [
        "",
        "候选合计只用于研发对账，不能替代广联达结算模型；四项对照不构成正式汇总。",
        "",
        "## 梁分账",
        "",
        f"- 全图拓扑中心线粗算：`{quantities['beam_topology_volume_m3']:.4f} m3`。",
        f"- 已确认净跨：`{quantities['beam_confirmed_clear_volume_m3']:.4f} m3`。",
        f"- 待复核净跨：`{quantities['beam_review_clear_volume_m3']:.4f} m3`。",
        f"- 推定端净跨：`{quantities['beam_inferred_clear_volume_m3']:.4f} m3`。",
        "",
        "## 墙柱分账",
        "",
        f"- 墙条带、边缘构件和独立柱候选合计："
        f"`{quantities['vertical_candidate_volume_m3']:.4f} m3`。",
        "- 该合计仍是候选量，最终清单归类未闭合。",
        "",
        "## 板与预制底板证据",
        "",
        f"- 板厚粗折候选：`{quantities['slab_rough_volume_m3']:.4f} m3`；"
        "材料体系与洞口扣减未闭合。",
        f"- 预制底板轮廓观测：`{prefab['polygon_count']}` 块，"
        f"`{prefab['observed_area_m2']:.4f} m2`；"
        f"轮廓来源：`{prefab.get('source_type_counts') or {}}`。",
        f"- 落入当前板拓扑面的观测面积：`{prefab['assigned_area_m2']:.4f} m2`，"
        f"涉及 `{prefab['assigned_panel_count']}` 个板面；"
        f"中心命中 `{prefab.get('assigned_by_center_count', 0)}` 块，"
        f"近边界复核归位 `{prefab.get('assigned_by_boundary_count', 0)}` 块。",
        f"- 未落入板拓扑面的观测面积：`{prefab['unassigned_area_m2']:.4f} m2`。",
        f"- 模型预制底板投影面积："
        f"`{prefab.get('reference_area_m2') or 0:.4f} m2`；"
        f"当前 CAD 观测覆盖率："
        f"`{prefab.get('reference_coverage_pct') or 0:.2f}%`。",
        f"- 模型构件编码匹配："
        f"`{prefab.get('matched_model_component_count') or 0} / "
        f"{prefab.get('model_component_count') or 0}`；"
        f"按图面重复因子重构投影面积："
        f"`{prefab.get('reconstructed_template_area_m2') or 0:.4f} m2`，"
        f"与模型差 `{prefab.get('reconstruction_difference_m2') or 0:+.4f} m2`。",
        "",
        "预制底板平面布置图已有明确的 `YDB` 轮廓和镜像实例。若图面采用标准段重复，"
        "脚本会按同编号模型块数计算重复因子；但还不能把所有未逐块展开的面积"
        "直接指定为现浇板。",
        "",
        "## 分账门槛",
        "",
        "| 门槛 | 状态 | 证据 | 下一步 |",
        "|---|---|---|---|",
    ]
    for gate in result["gates"]:
        lines.append(
            f"| {gate['title']} | {gate['status']} | "
            f"{gate['evidence']} | {gate['action']} |"
        )
    lines += [
        "",
        "## 收口判定",
        "",
        f"- `formal_ready`：`{str(result['formal_ready']).lower()}`。",
        "- 当前结果可以用于继续开发分账、回图和差异定位，不能作为正式混凝土工程量。",
        "- 梁钢筋翻样仍不得开始；先完成支座原图复核，再完成板和墙柱材料分账。",
    ]
    if prefab.get("components"):
        lines += [
            "",
            "## 预制底板构件编码复核",
            "",
            "| 编号 | 状态 | CAD标准段 | 模型块数 | 重复因子 | CAD面积m2 | 模型面积m2 | 重构面积m2 |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
        for row in prefab["components"]:
            factor = row.get("repetition_factor")
            lines.append(
                f"| {row['code']} | {row['status']} | "
                f"{row['cad_template_count']} | {row['model_count']} | "
                f"{factor if factor is not None else '-'} | "
                f"{row['cad_template_area_m2']:.4f} | "
                f"{row['model_projection_area_m2']:.4f} | "
                f"{row['reconstructed_projection_area_m2']:.4f} | "
                if row.get("reconstructed_projection_area_m2") is not None
                else
                f"| {row['code']} | {row['status']} | "
                f"{row['cad_template_count']} | {row['model_count']} | "
                f"{factor if factor is not None else '-'} | "
                f"{row['cad_template_area_m2']:.4f} | "
                f"{row['model_projection_area_m2']:.4f} | - |"
            )
    return "\n".join(lines)


def csv_rows(result: dict[str, Any]) -> list[list[str]]:
    headers = [
        "记录类型", "构件", "口径", "CAD值", "单位",
        "模型对照", "对照值", "差异", "差异率", "状态", "证据/下一步",
    ]
    rows = [headers]
    for row in result["comparisons"]:
        rows.append([
            "分账对照",
            row["component"],
            row["scope"],
            str(row["candidate_value_m3"]),
            "m3",
            row["reference_label"],
            "" if row.get("reference_value_m3") is None
            else str(row["reference_value_m3"]),
            "" if row.get("difference_m3") is None
            else str(row["difference_m3"]),
            "" if row.get("difference_pct") is None
            else f"{row['difference_pct']:.2f}%",
            row["status"],
            "",
        ])
    for gate in result["gates"]:
        rows.append([
            "门槛",
            gate["title"],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            gate["status"],
            f"{gate['evidence']}；{gate['action']}",
        ])
    for panel in result["prefab"].get("assignments") or []:
        rows.append([
            "预制底板观测",
            "板",
            panel["panel_id"],
            str(panel["area_m2"]),
            "m2",
            f"{panel['prefab_id']} ({panel.get('component_code') or '-'})",
            "",
            "",
            "",
            panel.get("assignment_status") or "prefab-observed",
            (
                f"构件范围 {panel['bbox']}；"
                f"边界距离 {panel.get('boundary_distance_mm', 0):.1f} mm"
            ),
        ])
    for panel in result["prefab"].get("unassigned") or []:
        rows.append([
            "预制底板未归属",
            "板",
            "",
            str(panel["area_m2"]),
            "m2",
            f"{panel['prefab_id']} ({panel.get('component_code') or '-'})",
            "",
            "",
            "",
            "unassigned",
            panel["reason"],
        ])
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="从结构模型和可选预制底板几何生成混凝土分账收口台账")
    parser.add_argument("--model-json", required=True)
    parser.add_argument("--reference", action="append", default=[],
                        help="模型对照值，如 梁及连梁=26.191")
    parser.add_argument("--reference-floor", default="",
                        help="广联达对照楼层，如 第2层")
    parser.add_argument("--floor-mapping-note", default="",
                        help="图纸与模型楼层映射风险说明")
    parser.add_argument("--floor-mapping-source", default="",
                        help="图纸与模型楼层映射依据")
    parser.add_argument("--prefab-dxf", default=None)
    parser.add_argument("--prefab-layer",
                        default=r"S-PC-叠合板轮廓")
    parser.add_argument("--prefab-label-layer",
                        default=r"S-PC-编号")
    parser.add_argument("--prefab-model-json", default=None,
                        help="同编号模型块数/面积/体积汇总 JSON")
    parser.add_argument("--prefab-transform", type=parse_transform,
                        default=(0.0, 0.0))
    parser.add_argument("--prefab-gap-mm", type=float, default=5000.0)
    parser.add_argument("--prefab-reference-area-m2", type=float, default=None)
    parser.add_argument("--report-title",
                        default="阶段十三：二层混凝土分账收口")
    parser.add_argument("--format", default="all",
                        choices=["all", "json", "csv", "md"])
    parser.add_argument("-o", "--out", default="concrete_ledger")
    args = parser.parse_args()

    try:
        references = parse_reference_values(args.reference)
    except (TypeError, ValueError) as exc:
        parser.error(str(exc))
    model_path = Path(args.model_json)
    if not model_path.exists():
        parser.error(f"结构模型不存在：{model_path}")
    prefab_path = Path(args.prefab_dxf) if args.prefab_dxf else None
    if prefab_path is not None and not prefab_path.exists():
        parser.error(f"预制底板 DXF 不存在：{prefab_path}")
    prefab_model_path = (
        Path(args.prefab_model_json) if args.prefab_model_json else None
    )
    if prefab_model_path is not None and not prefab_model_path.exists():
        parser.error(f"预制底板模型汇总不存在：{prefab_model_path}")
    model = json.loads(model_path.read_text(encoding="utf-8"))
    prefab_model = _load_prefab_model(prefab_model_path)
    result = build_ledger(
        model,
        references,
        args.reference_floor,
        args.floor_mapping_note,
        prefab_path,
        args.prefab_layer,
        args.prefab_transform,
        args.prefab_gap_mm,
        args.prefab_reference_area_m2,
        prefab_label_layer=args.prefab_label_layer,
        prefab_model=prefab_model,
        report_title=args.report_title,
        floor_mapping_source=args.floor_mapping_source,
    )
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.format in ("json", "all"):
        out.with_suffix(".json").write_text(
            json.dumps(result, ensure_ascii=False, indent=1),
            encoding="utf-8",
        )
    if args.format in ("md", "all"):
        out.with_suffix(".md").write_text(
            render_markdown(result), encoding="utf-8")
    if args.format in ("csv", "all"):
        with out.with_suffix(".csv").open(
                "w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerows(csv_rows(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
