#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从图面表格里抽混凝土强度等级绑定，产出分标号规则草稿。

支持两类表：
  story-height-table 结构楼层标高表：一行一个楼层，表头分「墙、柱、连梁」和「梁、板」等列；
  material-table     主要结构材料表：一行为一个构件部位，表头含「混凝土强度」列。
表头按列头文字定位竖向/水平/材料列，数据格按 x 落到最近的列带上。
空列带按同列上方最近的等级继承（合并单元格），继承值一律标 needs_review，
不当图面直接证据。输出 `cad-concrete-grade-source/v0.1`；给 --components-json
时同时产出能直接喂 cad_concrete_grade.py 的 `cad-concrete-grade-rules/v0.1` 草稿。
"""
from __future__ import annotations
from cad_common import to_number as _number  # noqa: E402,F401

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA_SOURCE = "cad-concrete-grade-source/v0.1"
SCHEMA_RULES = "cad-concrete-grade-rules/v0.1"
GRADE_TOKEN = re.compile(r"\bC\s?(\d{2})\b")
VERTICAL_WORDS = ("墙", "柱", "连梁")
HORIZONTAL_WORDS = ("梁", "板", "楼梯")
LABEL_WORDS = ("楼层", "层号", "标高", "层高", "部位", "构件", "序号", "层次")
BEAM_SLAB_GROUPS = {"beam", "slab", "stair-beam", "coupling-beam"}


def _text(value: Any) -> str:
    return str(value if value is not None else "").strip()

def grade_in(text: str) -> str | None:
    match = GRADE_TOKEN.search(_text(text))
    return ("C" + match.group(1)) if match else None


def read_texts(dxf_path: Path) -> list[dict[str, Any]]:
    """读模型空间文字实体；块引用请先展开，否则表内文字会缺。"""
    from dev_dxf import plain_mtext, readfile

    document = readfile(dxf_path)
    records: list[dict[str, Any]] = []
    for entity in document.modelspace():
        kind = entity.dxftype()
        if kind not in ("TEXT", "MTEXT", "ATTRIB", "ATTDEF"):
            continue
        try:
            insert = entity.dxf.insert
            value = plain_mtext(entity.text) if kind == "MTEXT" else entity.dxf.text
        except Exception:  # 图面脏数据不阻断整表提取
            continue
        text = _text(value).replace("\n", " ")
        if not text:
            continue
        records.append({
            "handle": _text(entity.dxf.handle),
            "layer": _text(entity.dxf.layer),
            "kind": kind,
            "x": _number(getattr(insert, "x", 0.0)),
            "y": _number(getattr(insert, "y", 0.0)),
            "text": text,
        })
    return records


def rows_in_region(records: list[dict[str, Any]], region: dict[str, Any],
                   y_tolerance: float) -> list[list[dict[str, Any]]]:
    x0, y0, x1, y1 = (_number(value) for value in region["bbox"])
    picked = [row for row in records
              if x0 <= row["x"] <= x1 and y0 <= row["y"] <= y1]
    picked.sort(key=lambda row: (-row["y"], row["x"]))
    rows: list[list[dict[str, Any]]] = []
    for row in picked:
        if rows and abs(row["y"] - rows[-1][0]["y"]) <= y_tolerance:
            rows[-1].append(row)
        else:
            rows.append([row])
    for row in rows:
        row.sort(key=lambda item: item["x"])
    return rows


def is_header_row(row: list[dict[str, Any]], role: str) -> bool:
    """有列头关键词且整行没有等级值，才算表头行。"""
    if any(grade_in(cell["text"]) for cell in row):
        return False
    texts = [cell["text"] for cell in row]
    if role == "story-height-table":
        vertical = any(any(word in text for word in VERTICAL_WORDS)
                       for text in texts)
        horizontal = any(any(word in text for word in HORIZONTAL_WORDS)
                         for text in texts)
        return vertical and horizontal
    return any("混凝土" in text or "强度" in text for text in texts)


def build_bands(row: list[dict[str, Any]], role: str) -> list[dict[str, Any]]:
    """从表头行取列带：等级列给分组，最左的文字列当行标签列。"""
    bands: list[dict[str, Any]] = []
    for cell in sorted(row, key=lambda item: item["x"]):
        text = cell["text"]
        group = None
        if role == "story-height-table":
            if any(word in text for word in VERTICAL_WORDS):
                group = "vertical"
            elif any(word in text for word in HORIZONTAL_WORDS):
                group = "beam-slab"
        elif "混凝土" in text or "强度" in text:
            group = "material-grade"
        if group:
            bands.append({"x": cell["x"], "header": text, "group": group,
                          "handle": cell["handle"], "y": cell["y"]})
        elif any(word in text for word in LABEL_WORDS) and not bands:
            bands.append({"x": cell["x"], "header": text, "group": "label",
                          "handle": cell["handle"], "y": cell["y"]})
    return bands


def _member_group(label: str) -> str:
    """部位文字里同时出现梁板和楼梯时按水平构件归类，不拆成楼梯梁。"""
    def has(*words: str) -> bool:
        return any(word in label for word in words)
    if has("筏板", "基础", "垫层"):
        return "foundation"
    if has("圈梁", "构造柱", "过梁"):
        return "secondary"
    if has("楼梯") and has("梁", "板"):
        return "beam-slab"
    if has("楼梯"):
        return "stair-beam"
    if has("墙", "柱"):
        return "vertical"
    if has("梁"):
        return "beam"
    if has("板"):
        return "slab"
    return "other"


def _row_y(row: list[dict[str, Any]]) -> float:
    return sum(_number(cell["y"]) for cell in row) / float(len(row))


def _anchor(name: str, role: str, band: dict[str, Any], cell: dict[str, Any],
            index: int, label: str) -> dict[str, Any]:
    return {
        "region": name, "role": role, "row_index": index, "row_label": label,
        "column": band["header"],
        "member_group": (_member_group(label) if role != "story-height-table"
                         else band["group"]),
        "grade": grade_in(cell["text"]), "inherited": False,
        "handle": cell["handle"], "layer": cell["layer"],
        "x": round(cell["x"], 1), "y": round(cell["y"], 1),
        "needs_review": not label,
    }


def interval_boundaries_confirmed(anchors: list[dict[str, Any]],
                                  labelled: list[tuple[int, str, float]]
                                  ) -> dict[int, bool]:
    """判断每个楼层行的等级归属是不是被表结构唯一确定。

    合并格只写一个等级值，格边界必须是表格行线，所以：
      整列只有一个等级值 → 没有边界可猜，全部行确定；
      相邻两个不同等级值的中点落在两行之间 → 分档唯一确定；
      中点正好压在某一行的行线上，或落在行范围之外 → 那一档归属不定，标需复核。
    """
    result = {index: False for index, _label, _y in labelled}
    if len({round(float(item["y"]), 1) for item in anchors}) <= 1:
        return {index: True for index, _label, _y in labelled}
    ys = sorted({round(y, 1) for _index, _label, y in labelled}, reverse=True)
    distinct = sorted({round(float(item["y"]), 1)
                       for item in anchors}, reverse=True)
    boundaries = [(upper + lower) / 2.0
                  for upper, lower in zip(distinct, distinct[1:])]
    ambiguous = []
    for middle in boundaries:
        if any(abs(middle - value) <= 1.0 for value in ys):
            ambiguous.append(middle)
            continue
        if not any(min(below, above) < middle < max(below, above)
                   for above, below in zip(ys, ys[1:])):
            ambiguous.append(middle)
    for index, _label, y in labelled:
        anchor_y = min((float(item["y"]) for item in anchors),
                       key=lambda value: abs(value - y))
        if abs(anchor_y - y) <= 1.0:
            result[index] = True  # 等级格就画在本行
            continue
        low, high = sorted((y, anchor_y))
        result[index] = not any(low <= middle <= high for middle in ambiguous)
    return result


def bind_region(region: dict[str, Any], rows: list[list[dict[str, Any]]],
                role: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]],
                                    list[dict[str, Any]], list[int]]:
    """先定位列带和列带里的等级格，再按 y 就近归属到每一行。

    合并单元格的等级文字画在格的中间，所以它会自成一行"锚点行"；
    锚点行不是楼层行，只当证据源，不出绑定行。
    """
    name = _text(region.get("name"))
    bindings: list[dict[str, Any]] = []
    headers: list[dict[str, Any]] = []
    header_indexes: list[int] = []
    bands: list[dict[str, Any]] = []
    anchors: dict[int, list[dict[str, Any]]] = {}
    labelled: list[tuple[int, str, float]] = []
    # 表头可能在数据上方也可能在下方（楼层表常把表头画在底部），先两遍扫
    for index, row in enumerate(rows):
        if not row or not is_header_row(row, role):
            continue
        header_indexes.append(index)
        found = build_bands(row, role)
        if found:
            bands = found
            headers.append({
                "region": name, "row_index": index,
                "columns": sorted({band["group"] for band in bands}),
                "text": " | ".join(cell["text"] for cell in row)})
    if not bands:
        return [], headers, header_indexes, 0
    non_header = set(header_indexes)
    for index, row in enumerate(rows):
        if not row or index in non_header:
            continue
        left = min(band["x"] for band in bands)
        label = " ".join(cell["text"] for cell in row
                         if cell["x"] <= left + 1.0
                         and grade_in(cell["text"]) is None)[:60].strip()
        grade_bands = [i for i, band in enumerate(bands) if band["group"] != "label"]
        for cell in [item for item in row if grade_in(item["text"])]:
            band_index = min(grade_bands,
                             key=lambda i: abs(bands[i]["x"] - cell["x"]),
                             default=None)
            if band_index is None:
                continue
            anchors.setdefault(band_index, []).append(
                _anchor(name, role, bands[band_index], cell, index, label))
        if label:
            labelled.append((index, label, _row_y(row)))

    for band_index, entries in anchors.items():
        if role != "story-height-table":
            bindings.extend(entry for entry in entries if entry["row_label"])
            continue
        confirmed = interval_boundaries_confirmed(entries, labelled)
        for index, label, y in labelled:
            anchor = min(entries, key=lambda item: abs(item["y"] - y))
            entry = dict(anchor)
            entry.update({"row_index": index, "row_label": label})
            entry["interval_confirmed"] = bool(
                confirmed.get(index, False) or anchor["row_index"] == index)
            if anchor["row_index"] == index:
                entry["needs_review"] = False
            else:
                entry.update({
                    "inherited": True,
                    "inherited_from_row": anchor["row_index"],
                    "band_gap_mm": round(abs(anchor["y"] - y), 1),
                    "needs_review": not entry["interval_confirmed"]})
            bindings.append(entry)
    return bindings, headers, header_indexes, len(labelled)


def build_gates(bindings: list[dict[str, Any]], headers: list[dict[str, Any]],
                summary: dict[str, Any]) -> list[dict[str, Any]]:
    """三张门槛：表头定位、合并格定界、行标签覆盖。

    合并格的等级值靠距离继承时，只有在"分档边界落在相邻两行之间"才算定界；
    没定界的必须挂需复核，不得当图面直接证据报量。
    """
    inherited = [row for row in bindings if row["inherited"]]
    confirmed = [row for row in inherited if row.get("interval_confirmed")]
    loose = [row for row in inherited
             if not row.get("interval_confirmed") and not row["needs_review"]]
    return [
        {"id": "source-table-located", "title": "等级表头已定位",
         "status": "pass" if headers else "fail",
         "evidence": "命中表头 %d 行" % len(headers),
         "action": "没命中时先核对区域 bbox 与列头文字。"},
        {"id": "merged-cells-flagged", "title": "合并格已定界或挂复核",
         "status": "pass" if not loose else "fail",
         "evidence": "继承档 %d 处，其中 %d 处分档边界落在相邻行之间已定界，"
                     "未定界且未挂复核 %d 处" % (len(inherited), len(confirmed),
                                                len(loose)),
         "action": "未定界的继承值只能当推定，不得升级为正式量。"},
        {"id": "label-coverage", "title": "行标签覆盖",
         "status": ("warn" if summary["needs_review_count"] else "pass"),
         "evidence": "需复核绑定 %d/%d" % (summary["needs_review_count"],
                                          summary["binding_count"]),
         "action": "行标签空白或未定界的绑定要回图逐层确认。"},
    ]


def build_bindings(records: list[dict[str, Any]], regions: list[dict[str, Any]],
                   y_tolerance: float, inherit: bool = True) -> dict[str, Any]:
    bindings: list[dict[str, Any]] = []
    headers: list[dict[str, Any]] = []
    for region in regions:
        role = _text(region.get("role") or "story-height-table")
        rows = rows_in_region(records, region, y_tolerance)
        found, header_rows, _, _ = bind_region(region, rows, role)
        if not inherit:
            found = [row for row in found if not row["inherited"]]
        bindings.extend(found)
        headers.extend(header_rows)
    return {"bindings": bindings, "headers": headers}


def rules_draft(bindings: list[dict[str, Any]], components: list[dict[str, Any]],
                floor: str, expected_total: float | None,
                notes: dict[str, Any] | None = None) -> dict[str, Any]:
    """把等级绑定套到构件量上；没有绑定的分组进未定档，不猜等级。"""
    by_group: dict[str, list[dict[str, Any]]] = {}
    for binding in bindings:
        by_group.setdefault(binding["member_group"], []).append(binding)

    def pick(group: str) -> dict[str, Any] | None:
        candidates = by_group.get(group)
        if not candidates and group in BEAM_SLAB_GROUPS:
            candidates = by_group.get("beam-slab")
        if not candidates and group in ("column", "wall"):
            candidates = by_group.get("vertical")
        if not candidates:
            return None
        return sorted(candidates, key=lambda item: item["needs_review"])[0]

    rows: list[dict[str, Any]] = []
    used: set[str] = set()
    for component in components:
        group = _text(component.get("member_group"))
        best = pick(group)
        volume = _number(component.get("volume_m3"))
        if best is None:
            rows.append({
                "component": _text(component.get("component")),
                "member_group": group, "volume_m3": round(volume, 4),
                "grade": "未定", "source_type": "unknown",
                "source_ref": "图面表格未给出该分组等级",
                "treatment": _text(component.get("treatment") or "count"),
                "needs_review": True})
            continue
        used.add(group)
        rows.append({
            "component": _text(component.get("component")),
            "member_group": group, "volume_m3": round(volume, 4),
            "grade": best["grade"],
            "source_type": ("design-booklet-table"
                            if best["role"] == "story-height-table"
                            else "drawing-table"),
            "source_ref": "%s｜%s｜%s" % (
                best["region"], best["column"], best["row_label"] or "行标签空白"),
            "treatment": _text(component.get("treatment") or "count"),
            "needs_review": bool(best["needs_review"])})
    payload: dict[str, Any] = {
        "schema": SCHEMA_RULES, "floor": floor, "rows": rows,
        "rule_notes": {"auto_draft": "等级由图面表格自动绑定，粒度到构件分组",
                       "binding_groups": sorted(by_group),
                       "unbound_groups": sorted(set(by_group) - used)}
        | dict(notes or {}),
    }
    if expected_total is not None:
        payload["expected_total_m3"] = round(expected_total, 4)
    return payload


def render_csv(payload: dict[str, Any], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["表区", "角色", "行号", "行标签", "列头", "构件分组",
                         "等级", "继承", "定界", "需复核", "格距mm",
                         "句柄", "图层", "X", "Y"])
        for row in payload["bindings"]:
            writer.writerow([row["region"], row["role"], row["row_index"],
                             row["row_label"], row["column"], row["member_group"],
                             row["grade"], "是" if row["inherited"] else "否",
                             "是" if row.get("interval_confirmed") else "否",
                             "是" if row["needs_review"] else "否",
                             row.get("band_gap_mm", ""), row["handle"],
                             row["layer"], row["x"], row["y"]])
        writer.writerow([])
        writer.writerow(["表头", "行号", "列", "原文"])
        for header in payload["headers"]:
            writer.writerow([header["region"], header["row_index"],
                             "、".join(header["columns"]), header["text"]])


def parse_region(raw: str) -> dict[str, Any]:
    parts = dict(item.split("=", 1) for item in raw.split(",") if "=" in item)
    for key in ("x0", "y0", "x1", "y1"):
        if key not in parts:
            raise ValueError(f"区域缺少 {key}：{raw}")
    return {"name": parts.get("name") or "region",
            "role": parts.get("role") or "story-height-table",
            "bbox": [float(parts[key]) for key in ("x0", "y0", "x1", "y1")]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dxf", nargs="?", help="已展开块引用的 DXF")
    parser.add_argument("--records-json",
                        help="文字记录 JSON（[{handle,layer,x,y,text}]）；"
                             "几十 MB 图先流式抽出表格区域再喂本内核，省内存")
    parser.add_argument("--region", action="append", default=[],
                        help="name=表名,x0=,y0=,x1=,y1=,role=story-height-table|material-table")
    parser.add_argument("--region-file", help="区域 JSON（列表或 {regions:[...]}）")
    parser.add_argument("--y-tolerance-mm", type=float, default=120.0)
    parser.add_argument("--no-inherit", action="store_true", help="关闭合并单元格继承")
    parser.add_argument("--components-json",
                        help="构件量 JSON：[{component,member_group,volume_m3}]")
    parser.add_argument("--floor", default="")
    parser.add_argument("--expected-total-m3", type=float)
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()

    regions: list[dict[str, Any]] = []
    try:
        regions.extend(parse_region(raw) for raw in args.region)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.region_file:
        data = json.loads(Path(args.region_file).read_text(encoding="utf-8"))
        for item in (data.get("regions") if isinstance(data, dict) else data) or []:
            item.setdefault("name", "region")
            item.setdefault("role", "story-height-table")
            regions.append(item)
    if not regions:
        print("至少要给一个 --region 或 --region-file", file=sys.stderr)
        return 2

    if args.records_json:
        records = json.loads(Path(args.records_json).read_text(encoding="utf-8"))
        if isinstance(records, dict):
            records = records.get("records") or records.get("text_records") or []
    elif args.dxf:
        records = read_texts(Path(args.dxf).expanduser().resolve())
    else:
        print("要给 DXF 或 --records-json", file=sys.stderr)
        return 2
    table = build_bindings(records, regions, args.y_tolerance_mm,
                           inherit=not args.no_inherit)
    summary = {
        "binding_count": len(table["bindings"]),
        "inherited_count": sum(1 for row in table["bindings"] if row["inherited"]),
        "needs_review_count": sum(1 for row in table["bindings"]
                                  if row["needs_review"]),
        "interval_confirmed_count": sum(1 for row in table["bindings"]
                                        if row.get("interval_confirmed")),
        "grade_counts": {}, "group_counts": {},
    }
    for row in table["bindings"]:
        summary["grade_counts"][row["grade"]] = summary["grade_counts"].get(
            row["grade"], 0) + 1
        summary["group_counts"][row["member_group"]] = summary["group_counts"].get(
            row["member_group"], 0) + 1
    payload: dict[str, Any] = {
        "schema": SCHEMA_SOURCE, "floor": args.floor,
        "text_record_count": len(records),
        "regions": regions, "headers": table["headers"],
        "bindings": table["bindings"], "summary": summary,
        "gates": build_gates(table["bindings"], table["headers"], summary),
    }
    out = Path(args.output).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.components_json:
        data = json.loads(Path(args.components_json).read_text(encoding="utf-8"))
        items = data.get("components") if isinstance(data, dict) else data
        payload["rules_draft"] = rules_draft(
            table["bindings"], items or [], args.floor, args.expected_total_m3,
            notes={"components_source": str(args.components_json)})
        Path(str(out) + "-rules.json").write_text(
            json.dumps(payload["rules_draft"], ensure_ascii=False, indent=1),
            encoding="utf-8")
    out.with_suffix(".json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    render_csv(payload, out.with_suffix(".csv"))
    digests = []
    for path in (out.with_suffix(".json"), out.with_suffix(".csv"),
                 Path(str(out) + "-rules.json")):
        if path.exists():
            digests.append("%s  %s" % (
                hashlib.sha256(path.read_bytes()).hexdigest(), path))
    out.with_suffix(".sha256").write_text("\n".join(digests) + "\n")
    print(json.dumps({"summary": payload["summary"],
                      "gates": {row["id"]: row["status"] for row in payload["gates"]},
                      "has_rules_draft": "rules_draft" in payload},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
