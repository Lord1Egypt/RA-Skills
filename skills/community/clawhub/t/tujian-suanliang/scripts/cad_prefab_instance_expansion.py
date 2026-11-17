#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""预制底板图面实例展开：把"展开倍率"从借用外部模型块数改成图面自身证据。

图面能自证的是单块面积和镜像关系，自证不了的是块数。本脚本逐编号把
图面标注数、图面轮廓数、图面单块面积与外部模型（广联达）的块数、单块面积摆在一起，
按编号数量倍率重构展开面积，再判断差出来的块数能不能用镜像半幅补齐。
只做证据分类，不改任何混凝土量，预制子层是否进报量由材料分账决定。
"""



from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

from cad_common import to_number as _number, to_text as _text  # noqa: F401

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterator, Dict, List

SCHEMA = "cad-prefab-instance-expansion/v0.1"
FORM_CODE = re.compile(r"\\[ACPFCpTfHhWQkK][^;]*;?|[{}]")
CODE_PATTERN = re.compile(r"^(Y[A-Z]+-\d+)(\((?:W|w)\))?$")


def _round(value: Any, places: int = 4) -> float:
    return round(_number(value), places)


def clean_text(value: Any) -> str:
    return FORM_CODE.sub("", _text(value)).strip()


def ring_area(points: List[tuple]) -> float:
    """鞋带公式，DXF 单位 mm，返回 m2。"""
    total = 0.0
    count = len(points)
    for index in range(count):
        x1, y1 = points[index]
        x2, y2 = points[(index + 1) % count]
        total += x1 * y2 - x2 * y1
    return abs(total) / 2.0 / 1.0e6


def stream_entities(path: str) -> Iterator[Dict[str, Any]]:
    """流式扫 ENTITIES，只留图层/文字/顶点，43 MB 展开图不吃内存。"""
    current: Dict[str, Any] = {}
    etype = None
    code = None
    inside = False
    with open(path, "r", encoding="utf-8", errors="ignore") as handle:
        for raw in handle:
            line = raw.rstrip("\n")
            if not inside:
                if line == "ENTITIES":
                    inside = True
                continue
            if len(line) < 6 and line.strip().isdigit():
                code = int(line.strip())
                value = next(handle, "").rstrip("\n")
                if value == "ENDRL":
                    continue
                if code == 0:
                    if etype:
                        yield {"type": etype, **current}
                    if value == "ENDSEC":
                        if etype:
                            yield {"type": etype, **current}
                        return
                    etype, current = value, {}
                    continue
                if code == 8:
                    current["layer"] = value
                elif code in (1, 3):
                    current["text"] = current.get("text", "") + value
                elif code in (10, 20):
                    try:
                        num = float(value)
                    except ValueError:
                        continue
                    current.setdefault("xs" if code == 10 else "ys", []).append(num)
                elif code == 70:
                    try:
                        current["closed"] = bool(int(value) & 1)
                    except ValueError:
                        pass
    if etype:
        yield {"type": etype, **current}


def collect(dxf_path: str, *, outline_layer: str, label_layer: str,
            title_keys: List[str], min_area: float) -> Dict[str, Any]:
    """一次扫描拿到图名、闭合轮廓、编号标注。"""
    titles: List[Dict[str, Any]] = []
    outlines: List[Dict[str, Any]] = []
    labels: List[Dict[str, Any]] = []
    for row in stream_entities(dxf_path):
        etype = _text(row.get("type"))
        layer = _text(row.get("layer"))
        xs = list(row.get("xs") or [])
        ys = list(row.get("ys") or [])
        if etype in ("TEXT", "MTEXT") and xs:
            text = clean_text(row.get("text"))
            if not text:
                continue
            if "图名" in layer and any(key in text for key in title_keys):
                titles.append({"text": text, "x": xs[0], "y": ys[0]})
            elif layer == label_layer:
                hit = CODE_PATTERN.match(text)
                if hit:
                    labels.append({"text": text, "code": hit.group(1),
                                   "suffix": hit.group(2) or "",
                                   "x": xs[0], "y": ys[0]})
        elif etype == "LWPOLYLINE" and layer == outline_layer and row.get("closed") \
                and len(xs) >= 3:
            area = ring_area(list(zip(xs, ys)))
            if area < min_area:
                continue
            outlines.append({"area_m2": _round(area), "bbox": [min(xs), min(ys),
                                                                max(xs), max(ys)],
                             "cx": _round(sum(xs) / len(xs), 1),
                             "cy": _round(sum(ys) / len(ys), 1)})
    return {"titles": titles, "outlines": outlines, "labels": labels}


def assign_frames(collected: Dict[str, Any], *, frame_title_key: str,
                  half_width_mm: float) -> Dict[str, Any]:
    """图名在图框下方：构件取正下方最近的图名，且不得越过上一个图名。"""
    ordered = sorted(collected["titles"], key=lambda row: _number(row.get("y")))
    chosen = next((row for row in ordered if frame_title_key in _text(row.get("text"))),
                  None)
    if chosen is None:
        return {"frame": None, "outlines": [], "labels": []}
    index = ordered.index(chosen)
    lower = _number(chosen.get("y"))
    upper = _number(ordered[index + 1].get("y")) if index + 1 < len(ordered) else 1e18
    frame_x = _number(chosen.get("x"))

    def owned(row: Dict[str, Any]) -> bool:
        y = _number(row.get("cy", row.get("y")))
        x = _number(row.get("cx", row.get("x")))
        return lower < y < upper and abs(x - frame_x) <= half_width_mm

    return {"frame": {"title": _text(chosen.get("text")), "x": frame_x, "y": lower,
                      "upper_title": _text(ordered[index + 1].get("text"))
                      if index + 1 < len(ordered) else ""},
            "outlines": [row for row in collected["outlines"] if owned(row)],
            "labels": [row for row in collected["labels"] if owned(row)]}


def own_labels(frame: Dict[str, Any], *, link_mm: float) -> Dict[str, Any]:
    """编号标注归轮廓：包含优先（多块包含取最小块），否则就近 link_mm 内认领。"""
    outlines = list(frame["outlines"])
    taken: Dict[int, str] = {}
    orphan_labels: List[str] = []
    for label in sorted(frame["labels"], key=lambda row: (row["code"], row["suffix"])):
        best = None
        for index, outline in enumerate(outlines):
            if index in taken:
                continue
            box = outline["bbox"]
            if box[0] - 1.0 <= label["x"] <= box[2] + 1.0 \
                    and box[1] - 1.0 <= label["y"] <= box[3] + 1.0:
                size = (box[2] - box[0]) * (box[3] - box[1])
                if best is None or size < best[0]:
                    best = (size, index)
        if best is None:
            for index, outline in enumerate(outlines):
                if index in taken:
                    continue
                distance = ((outline["cx"] - label["x"]) ** 2
                            + (outline["cy"] - label["y"]) ** 2) ** 0.5
                if distance <= link_mm and (best is None or distance < best[0]):
                    best = (distance, index)
        if best is None:
            orphan_labels.append(label["text"])
            continue
        taken[best[1]] = label["text"] + label["suffix"]
    rows: Dict[str, Dict[str, Any]] = {}
    for index, name in taken.items():
        row = rows.setdefault(name, {"label": name, "code": name.replace(
            _suffix_of(name), "") if _suffix_of(name) else name,
            "suffix": _suffix_of(name), "outline_count": 0, "area_m2": 0.0,
            "unit_areas": []})
        row["outline_count"] += 1
        row["area_m2"] = _round(row["area_m2"] + outlines[index]["area_m2"])
        row["unit_areas"].append(outlines[index]["area_m2"])
    unlabeled = [outlines[index] for index in range(len(outlines)) if index not in taken]
    return {"rows": sorted(rows.values(), key=lambda row: sort_key(row["label"])),
            "orphan_labels": sorted(orphan_labels),
            "unlabeled_outlines": sorted(unlabeled, key=lambda row: -row["area_m2"])}


def _suffix_of(label: str) -> str:
    hit = CODE_PATTERN.match(label)
    return hit.group(2) or "" if hit else ""


def sort_key(label: str) -> tuple:
    hit = CODE_PATTERN.match(label)
    if not hit:
        return (2, label, "")
    prefix = hit.group(1)
    digits = int(re.sub(r"\D", "", prefix) or 0)
    return (0 if not hit.group(2) else 1, digits, label)


def mirror_audit(outlines: List[Dict[str, Any]], *, tolerance_mm: float) -> Dict[str, Any]:
    """整幅镜像检测：图面只画半幅时，倍率能用镜像解释；已画双侧就不能。"""
    if len(outlines) < 2:
        return {"axis_x": None, "paired_count": 0, "outline_count": len(outlines),
                "same_area_pair_count": 0, "paired_ratio": 0.0, "unpaired": [],
                "explains_doubling": False}
    xs = [_number(row.get("cx")) for row in outlines]
    span = (min(xs) + max(xs)) / 2.0
    best = (None, -1)
    for step in range(-60, 61):
        axis = span + step * 100.0
        paired = 0
        for index, row in enumerate(outlines):
            for other, rival in enumerate(outlines):
                if other == index:
                    continue
                if abs((2 * axis - _number(row.get("cx"))) - _number(rival.get("cx"))) \
                        <= tolerance_mm and abs(_number(row.get("cy"))
                                                - _number(rival.get("cy"))) <= tolerance_mm \
                        and abs(_number(row.get("cx")) - _number(rival.get("cx"))) > tolerance_mm:
                    paired += 1
                    break
        if paired > best[1]:
            best = (axis, paired)
    axis, paired = best
    same_area = 0
    unpaired: List[Dict[str, Any]] = []
    for index, row in enumerate(outlines):
        found = None
        for other, rival in enumerate(outlines):
            if other == index:
                continue
            if abs((2 * axis - _number(row.get("cx"))) - _number(rival.get("cx"))) \
                    <= tolerance_mm and abs(_number(row.get("cy"))
                                             - _number(rival.get("cy"))) <= tolerance_mm:
                found = rival
                break
        if found is None:
            unpaired.append({"area_m2": row["area_m2"], "cx": row["cx"], "cy": row["cy"]})
        elif abs(_number(found.get("area_m2")) - _number(row.get("area_m2"))) < 1e-4:
            same_area += 1
    return {"axis_x": _round(axis, 1), "paired_count": paired,
            "outline_count": len(outlines), "same_area_pair_count": same_area,
            "paired_ratio": _round(paired / float(len(outlines)), 4),
            "unpaired": unpaired,
            "explains_doubling": bool(paired < len(outlines) * 0.5)}


def build_expansion(collected: Dict[str, Any], ledger: Dict[str, Any],
                    params: Dict[str, Any]) -> Dict[str, Any]:
    """逐编号：图面块数/单块面积 对 模型块数/单块面积，按编号倍率重构展开面积。"""
    frame = assign_frames(collected, frame_title_key=params["frame_title_key"],
                          half_width_mm=params["frame_half_width_mm"])
    owned = own_labels(frame, link_mm=params["label_link_mm"]) \
        if frame["frame"] else {"rows": [], "orphan_labels": [], "unlabeled_outlines": []}
    model = { _text(row.get("code")): row
              for row in (ledger.get("component_reconciliation") or [])}
    unit_tol = params["unit_area_tolerance_m2"]
    rows: List[Dict[str, Any]] = []
    predicted = 0.0
    observed = 0.0
    model_area = 0.0
    cad_count_matched = 0
    seen_codes: set = set()
    for row in owned["rows"]:
        code = row["code"]
        if code in seen_codes:
            # 同一图框里同编号出现两族标注（如镜像后缀混框），只登记不重复计量
            rows.append({"code": code, "cad_label_count": row["outline_count"],
                         "cad_outline_count": row["outline_count"],
                         "cad_area_m2": _round(row["area_m2"]),
                         "cad_unit_area_m2": _round(row["area_m2"] / max(
                             row["outline_count"], 1)),
                         "model_count": None, "model_unit_area_m2": None,
                         "count_ratio": None, "unit_area_residual_m2": None,
                         "predicted_expanded_area_m2": None,
                         "status": "duplicate-code-in-frame"})
            continue
        seen_codes.add(code)
        ref = model.get(code)
        if not ref:
            rows.append({"code": code, "cad_label_count": row["outline_count"],
                         "cad_outline_count": row["outline_count"],
                         "cad_area_m2": row["area_m2"],
                         "cad_unit_area_m2": _round(row["area_m2"] / max(
                             row["outline_count"], 1)),
                         "model_count": None, "model_unit_area_m2": None,
                         "count_ratio": None, "unit_area_residual_m2": None,
                         "predicted_expanded_area_m2": None,
                         "status": "no-model-row"})
            continue
        cad_count = max(int(row["outline_count"]), 1)
        cad_unit = row["area_m2"] / cad_count
        model_count = int(_number(ref.get("model_count")) or 0)
        model_unit = _number(ref.get("model_unit_area_m2"))
        ratio = model_count / float(cad_count) if cad_count else None
        part = {"code": code,
               "cad_label_count": cad_count,
               "cad_outline_count": cad_count,
               "cad_area_m2": _round(row["area_m2"]),
               "cad_unit_area_m2": _round(cad_unit),
               "model_count": model_count,
               "model_unit_area_m2": _round(model_unit),
               "count_ratio": _round(ratio, 4),
               "unit_area_residual_m2": _round(cad_unit - model_unit, 6),
               "predicted_expanded_area_m2": _round(row["area_m2"] * (ratio or 0.0)),
               "status": "unit-area-exact" if abs(cad_unit - model_unit) <= unit_tol
               else "unit-area-review"}
        rows.append(part)
        predicted += _number(part["predicted_expanded_area_m2"])
        observed += _number(row["area_m2"])
        model_area += _number(ref.get("model_area_m2"))
        cad_count_matched += cad_count
    swaps = _swap_findings(rows, unit_tol)
    summary = {
        "frame_title": _text((frame["frame"] or {}).get("title")) if frame["frame"] else "",
        "cad_outline_count": len(frame["outlines"]),
        "cad_label_count": len(frame["labels"]),
        "cad_observed_area_m2": _round(observed),
        "cad_owned_outline_count": cad_count_matched,
        "model_instance_count": sum(int(_number(row.get("model_count")) or 0)
                                    for row in model.values()
                                    if _text(row.get("code")) in seen_codes),
        "model_expanded_area_m2": _round(model_area),
        "count_ratio_expanded_area_m2": _round(predicted),
        "expansion_area_residual_m2": _round(predicted - model_area, 6),
        "global_area_multiplier": _round(observed and model_area / observed),
        "global_count_multiplier": _round(
            sum(int(_number(row.get("model_count")) or 0) for row in model.values()
                if _text(row.get("code")) in seen_codes)
            / float(cad_count_matched or 1)),
        "codes_reviewed": len(rows),
        "codes_unit_area_exact": sum(1 for row in rows
                                     if row["status"] == "unit-area-exact"),
        "codes_unit_area_review": sum(1 for row in rows
                                       if row["status"] == "unit-area-review"),
        "orphan_label_count": len(owned["orphan_labels"]),
        "unlabeled_outline_count": len(owned["unlabeled_outlines"]),
        "unlabeled_outline_area_m2": _round(sum(_number(row.get("area_m2"))
                                                for row in owned["unlabeled_outlines"])),
    }
    mirror = mirror_audit(frame["outlines"], tolerance_mm=params["mirror_tolerance_mm"])
    summary["mirror_paired_ratio"] = mirror["paired_ratio"] if "paired_ratio" in mirror else None
    payload = {
        "schema": SCHEMA, "title": params["title"], "floor": params["floor"],
        "source": {"dxf": params["dxf"],
                   "material_ledger": params["material_ledger"],
                   "outline_layer": params["outline_layer"],
                   "label_layer": params["label_layer"],
                   "frame_title_key": params["frame_title_key"]},
        "parameters": params,
        "summary": summary,
        "component_expansion": rows,
        "unit_area_swap_candidates": swaps,
        "mirror_audit": mirror,
        "orphan_labels": owned["orphan_labels"],
        "unlabeled_outlines": owned["unlabeled_outlines"][:20],
        "gates": [],
    }
    payload["gates"] = _gates(payload, params)
    return payload


def _swap_findings(rows: List[Dict[str, Any]], unit_tol: float) -> List[Dict[str, Any]]:
    """两个编号的单块面积残差一正一负、合计对平 -> 编号与轮廓互换了，不是漏量。"""
    pending = [row for row in rows
               if abs(_number(row.get("unit_area_residual_m2"))) > unit_tol]
    out: List[Dict[str, Any]] = []
    used = set()
    for position, first in enumerate(pending):
        if first["code"] in used:
            continue
        for second in pending[position + 1:]:
            if second["code"] in used:
                continue
            total = _number(first["unit_area_residual_m2"]) + _number(second["unit_area_residual_m2"])
            if _number(first["unit_area_residual_m2"]) * _number(
                    second["unit_area_residual_m2"]) < 0 \
                    and abs(total) <= max(unit_tol, 0.002):
                out.append({"codes": [first["code"], second["code"]],
                            "unit_area_residual_m2": [_number(first["unit_area_residual_m2"]),
                                                      _number(second["unit_area_residual_m2"])],
                            "pair_residual_m2": _round(total, 6),
                            "status": "code-outline-swapped-pair"})
                used.update({first["code"], second["code"]})
                break
    return out


def _gates(payload: Dict[str, Any], params: Dict[str, Any]) -> List[Dict[str, Any]]:
    summary = payload["summary"]
    tol = params["identity_tolerance_m2"]
    gates: List[Dict[str, Any]] = []
    review = int(summary["codes_unit_area_review"])
    swaps = payload["unit_area_swap_candidates"]
    review_codes = {_text(row["code"]) for row in payload["component_expansion"]
                    if row["status"] == "unit-area-review"}
    swapped_codes = {code for row in swaps for code in row["codes"]}
    residual = abs(_number(summary["expansion_area_residual_m2"]))
    gates.append({
        "id": "prefab-unit-area-self-evidence",
        "title": "预制底板单块面积图面自证",
        "status": "pass" if review_codes == swapped_codes else "fail",
        "evidence": f"{summary['codes_unit_area_exact']} 个编号图面单块面积与模型单块面积"
                    f"残差≤{params['unit_area_tolerance_m2']} m2；"
                    f"不一致 {review} 个，互换成对 {len(swaps)} 对："
                    + ("、".join("/".join(row["codes"]) for row in swaps) or "无"),
        "action": ("面积单元已由图面自证，编号换位只影响归类不影响总量"
                   if review_codes == swapped_codes else
                   "回图核对不一致编号的轮廓归属，确认是换位还是单块面积确实不同"),
    })
    gates.append({
        "id": "prefab-expansion-area-identity",
        "title": "按编号数量倍率重构展开面积",
        "status": "pass" if residual <= tol else "fail",
        "evidence": f"Σ(图面面积×模型块数/图面块数) = {summary['count_ratio_expanded_area_m2']} m2 "
                    f"对模型展开 {summary['model_expanded_area_m2']} m2，"
                    f"残差 {summary['expansion_area_residual_m2']} m2"
                    f"（阈值 {tol} m2）；展开倍率由借用外部块数改为逐编号数量倍率",
        "action": ("倍率分解到编号级且面积对平，可作为台账口径"
                   if residual <= tol else "逐编号核对块数，倍率不得合并成一个全局系数"),
    })
    mirror = payload["mirror_audit"]
    count_gap = int(summary["model_instance_count"]) - int(summary["cad_owned_outline_count"])
    explains = bool(mirror.get("explains_doubling"))
    gates.append({
        "id": "prefab-instance-count-cad-evidence",
        "title": "预制底板块数图面证据",
        "status": "pass" if explains or count_gap <= 0 else "warn",
        "evidence": f"图面认领 {summary['cad_owned_outline_count']} 块、模型 "
                    f"{summary['model_instance_count']} 块，差 {count_gap} 块；"
                    f"镜像轴 x={mirror.get('axis_x')} mm，配对 "
                    f"{mirror.get('paired_count')}/{mirror.get('outline_count')} 块"
                    f"（同面积配对 {mirror.get('same_area_pair_count')} 块）"
                    f"{'，图面只画半幅，倍率可用镜像补齐' if explains else '，图面已含双侧，倍率不能由镜像解释'}",
        "action": ("按镜像轴补齐实例数即可自证块数" if explains else
                   "块数缺口须查深化图纸或构件表，不得用镜像解释；预制子层只进装配式台账"),
    })
    return gates


def csv_rows(payload: Dict[str, Any]) -> List[List[Any]]:
    summary = payload["summary"]
    rows: List[List[Any]] = [
        ["项目", "值", "说明"],
        ["图框", summary["frame_title"], ""],
        ["图面轮廓数", summary["cad_owned_outline_count"], "被编号标注认领的轮廓"],
        ["图面轮廓面积 m2", summary["cad_observed_area_m2"], ""],
        ["模型实例数", summary["model_instance_count"], "外部模型块数"],
        ["模型展开面积 m2", summary["model_expanded_area_m2"], ""],
        ["按编号倍率重构面积 m2", summary["count_ratio_expanded_area_m2"], ""],
        ["重构残差 m2", summary["expansion_area_residual_m2"], ""],
        ["全局面积倍率", summary["global_area_multiplier"], "模型展开/图面轮廓"],
        ["全局块数倍率", summary["global_count_multiplier"], "模型块数/图面块数"],
        ["镜像配对率", payload["mirror_audit"].get("paired_ratio"), "图面是否只画半幅"],
        ["", "", ""],
        ["编号", "图面块数", "图面单块面积 m2", "模型块数", "模型单块面积 m2",
         "数量倍率", "单块面积残差 m2", "倍率重构面积 m2", "状态"],
    ]
    for row in payload["component_expansion"]:
        rows.append([row["code"], row.get("cad_outline_count"), row.get("cad_unit_area_m2"),
                     row.get("model_count"), row.get("model_unit_area_m2"),
                     row.get("count_ratio"), row.get("unit_area_residual_m2"),
                     row.get("predicted_expanded_area_m2"), row["status"]])
    rows += [["", "", ""], ["门槛", "状态", "证据"]]
    rows += [[gate["id"], gate["status"], gate["evidence"]] for gate in payload["gates"]]
    return rows


def render_markdown(payload: Dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [f"# {payload['title']}", "",
             f"- 图框：`{summary['frame_title']}`",
             f"- 图面：`{summary['cad_owned_outline_count']}` 块 / "
             f"`{summary['cad_observed_area_m2']}` m2；"
             f"模型：`{summary['model_instance_count']}` 块 / "
             f"`{summary['model_expanded_area_m2']}` m2",
             f"- 按编号数量倍率重构展开面积 `{summary['count_ratio_expanded_area_m2']}` m2，"
             f"残差 `{summary['expansion_area_residual_m2']}` m2；"
             f"面积倍率 `{summary['global_area_multiplier']}`、块数倍率 "
             f"`{summary['global_count_multiplier']}`",
             f"- 镜像审计：轴 `x={payload['mirror_audit'].get('axis_x')}` mm，配对 "
             f"`{payload['mirror_audit'].get('paired_count')}/"
             f"{payload['mirror_audit'].get('outline_count')}`，同面积配对 "
             f"`{payload['mirror_audit'].get('same_area_pair_count')}` → "
             f"{'图面只画半幅，倍率可用镜像补齐' if payload['mirror_audit'].get('explains_doubling') else '图面已含双侧，倍率不能由镜像解释'}",
             "", "| 编号 | 图面块数 | 图面单块 m2 | 模型块数 | 模型单块 m2 | 倍率 | 残差 m2 | 状态 |",
             "|---|---:|---:|---:|---:|---:|---:|---|"]
    for row in payload["component_expansion"]:
        lines.append(f"| {row['code']} | {row.get('cad_outline_count')} | "
                     f"{row.get('cad_unit_area_m2')} | {row.get('model_count')} | "
                     f"{row.get('model_unit_area_m2')} | {row.get('count_ratio')} | "
                     f"{row.get('unit_area_residual_m2')} | {row['status']} |")
    if payload["unit_area_swap_candidates"]:
        lines += ["", "## 编号-轮廓换位", ""]
        for row in payload["unit_area_swap_candidates"]:
            lines.append(f"- {'、'.join(row['codes'])}：单块面积残差 "
                         f"{row['unit_area_residual_m2']}，互抵后 "
                         f"{row['pair_residual_m2']} m2，判 `{row['status']}`")
    lines += ["", "## 门槛", ""]
    for gate in payload["gates"]:
        lines.append(f"- [{gate['status']}] {gate['id']}：{gate['evidence']} 处理：{gate['action']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="预制底板图面实例展开（编号级数量倍率自证）")
    parser.add_argument("--expanded-dxf", required=True)
    parser.add_argument("--material-ledger-json", required=True,
                        help="材料分账 JSON，取 component_reconciliation")
    parser.add_argument("--outline-layer", default="S-PC-叠合板轮廓")
    parser.add_argument("--label-layer", default="S-PC-编号")
    parser.add_argument("--title-key", action="append", default=[],
                        help="图名关键字，可重复；缺省用预制底板平面布置图")
    parser.add_argument("--frame-title-key", default="预制底板平面布置图")
    parser.add_argument("--frame-half-width-mm", type=float, default=45000.0)
    parser.add_argument("--label-link-mm", type=float, default=1500.0)
    parser.add_argument("--mirror-tolerance-mm", type=float, default=400.0)
    parser.add_argument("--min-outline-area-m2", type=float, default=0.2)
    parser.add_argument("--unit-area-tolerance-m2", type=float, default=0.01)
    parser.add_argument("--identity-tolerance-m2", type=float, default=0.05)
    parser.add_argument("--floor", default="首层")
    parser.add_argument("--title", default="预制底板图面实例展开")
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()
    params = {"dxf": args.expanded_dxf, "material_ledger": args.material_ledger_json,
              "outline_layer": args.outline_layer, "label_layer": args.label_layer,
              "title_keys": args.title_key or ["预制底板平面布置图"],
              "frame_title_key": args.frame_title_key,
              "frame_half_width_mm": args.frame_half_width_mm,
              "label_link_mm": args.label_link_mm,
              "mirror_tolerance_mm": args.mirror_tolerance_mm,
              "min_outline_area_m2": args.min_outline_area_m2,
              "unit_area_tolerance_m2": args.unit_area_tolerance_m2,
              "identity_tolerance_m2": args.identity_tolerance_m2,
              "floor": args.floor, "title": args.title}
    ledger = json.loads(Path(args.material_ledger_json).read_text(encoding="utf-8"))
    payload = build_expansion(
        collect(args.expanded_dxf, outline_layer=args.outline_layer,
                label_layer=args.label_layer, title_keys=params["title_keys"],
                min_area=args.min_outline_area_m2),
        ledger, params)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    json_path = out.with_suffix(".json")
    csv_path = out.with_suffix(".csv")
    md_path = out.with_suffix(".md")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle).writerows(csv_rows(payload))
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    out.with_name(out.name + ".sha256").write_text("\n".join(
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.resolve()}"
        for path in (json_path, csv_path, md_path)) + "\n", encoding="utf-8")
    print(json.dumps({"summary": payload["summary"],
                      "gates": {row["id"]: row["status"] for row in payload["gates"]},
                      "outputs": [str(json_path), str(csv_path), str(md_path)]},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
