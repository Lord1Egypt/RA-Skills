#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""整册展开 DXF 里按图框登记梁编号标注位置，判断偏少编号该回本层图框还是别的楼层。"""



from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

from cad_common import to_number as _number, round_number as _round, to_text as _text  # noqa: E402,F401

import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterator


SCHEMA = "cad-beam-frame-label-index/v0.1"
CODE_RE = re.compile(
    r"^((?:WKL|KL|LL|L|WL|XL|AL|JZL)\d+[a-zA-Z]?\(\d+[A-Za-z]?\))")
TITLE_RE = re.compile(r"(梁平法施工图|板平法施工图|墙柱平法施工图|楼梯大样|节点详图)")



def _code_key(value: Any) -> str:
    return re.sub(r"\s+", "", _text(value)).upper()


def _pairs(handle: Any) -> Iterator[tuple[str, str]]:
    """按 DXF 组码/值成对读出，忽略大小写和换行差异。"""
    code: str | None = None
    for raw in handle:
        value = raw.rstrip("\r\n")
        if code is None:
            code = raw[:6].strip()
            continue
        yield code, value
        code = None


def scan_labels(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """流式扫描整册 DXF，收梁编号标注与图名，不加载实体到内存。"""
    labels: list[dict[str, Any]] = []
    titles: list[dict[str, Any]] = []
    kind = ""
    layer = ""
    x: float | None = None
    y: float | None = None
    parts: list[str] = []

    def emit() -> None:
        if not parts or x is None:
            return
        text = "".join(parts).strip()
        if not text:
            return
        record = {"text": text[:64], "layer": layer, "kind": kind,
                  "x": _round(x, 1), "y": _round(y, 1)}
        match = CODE_RE.match(text)
        if match:
            record["code"] = match.group(1)
            labels.append(record)
        elif TITLE_RE.search(text) and len(text) <= 48:
            record["code"] = ""
            titles.append(record)

    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for code, value in _pairs(handle):
            if code == "0":
                emit()
                kind, layer, x, y, parts = value, "", None, None, []
            elif code == "8":
                layer = value
            elif code == "10":
                try:
                    x = float(value)
                except ValueError:
                    pass
            elif code == "20":
                try:
                    y = float(value)
                except ValueError:
                    pass
            elif code in ("1", "3"):
                parts.append(value)
    emit()
    return labels, titles


def build_frames(titles: list[dict[str, Any]],
                 options: dict[str, Any]) -> list[dict[str, Any]]:
    """图名在图框下方，按 x 分列、y 升序建立图框归属表。"""
    column_tolerance = _number(options.get("column_tolerance_mm"), 50000.0)
    columns: list[list[dict[str, Any]]] = []
    for title in sorted(titles, key=lambda row: _number(row.get("x"))):
        for column in columns:
            if abs(_number(column[0].get("x")) - _number(title.get("x"))) \
                    <= column_tolerance:
                column.append(title)
                break
        else:
            columns.append([title])
    frames: list[dict[str, Any]] = []
    for column in columns:
        ordered = sorted(column, key=lambda row: _number(row.get("y")))
        for index, title in enumerate(ordered):
            frames.append({
                "frame": _text(title.get("text")),
                "column_x_mm": _round(title.get("x"), 1),
                "title_y_mm": _round(title.get("y"), 1),
                "y_min_mm": _round(title.get("y"), 1),
                "y_max_mm": _round(
                    ordered[index + 1].get("y")
                    if index + 1 < len(ordered) else 1e12, 1),
            })
    return frames


def assign_labels(labels: list[dict[str, Any]],
                  frames: list[dict[str, Any]],
                  options: dict[str, Any]) -> list[dict[str, Any]]:
    """每个编号标注归到"图名在其下方且最近"的那个图框。"""
    column_tolerance = _number(options.get("column_tolerance_mm"), 50000.0)
    rows: list[dict[str, Any]] = []
    for label in labels:
        x = _number(label.get("x"))
        y = _number(label.get("y"))
        candidates = [frame for frame in frames
                      if abs(_number(frame.get("column_x_mm")) - x)
                      <= column_tolerance
                      and _number(frame.get("y_min_mm")) - 2000.0 <= y
                      < _number(frame.get("y_max_mm"))]
        if not candidates:
            rows.append(dict(label, frame="", frame_title_y_mm=None))
            continue
        best = max(candidates, key=lambda frame: _number(frame.get("title_y_mm")))
        rows.append(dict(label, frame=_text(best.get("frame")),
                         frame_title_y_mm=_number(best.get("title_y_mm"))))
    return rows


def build_index(labels: list[dict[str, Any]], titles: list[dict[str, Any]],
                reconciliation: dict[str, Any],
                options: dict[str, Any]) -> dict[str, Any]:
    frames = build_frames(titles, options)
    assigned = assign_labels(labels, frames, options)
    per_frame: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in assigned:
        code = _text(row.get("code"))
        frame = _text(row.get("frame")) or "未归属图框"
        per_frame[frame][code] += 1
    target_frames = [_text(options.get("target_frame"))]
    own = per_frame.get(target_frames[0]) or {}
    rows: list[dict[str, Any]] = []
    for row in reconciliation.get("beam_code_reconciliation") or []:
        code = _text(row.get("code"))
        key = _code_key(code)
        own_count = sum(value for ckey, value in own.items()
                        if _code_key(ckey).startswith(key))
        other = {frame: sum(value for ckey, value in counts.items()
                            if _code_key(ckey).startswith(key))
                 for frame, counts in per_frame.items()
                 if frame != target_frames[0] and any(
                     _code_key(ckey).startswith(key) for ckey in counts)}
        other = {key2: value for key2, value in other.items() if value}
        cad_span = _number(row.get("cad_selected_span_mm"))
        single = _number(row.get("reference_single_axis_length_mm"))
        difference = _number(row.get("current_code_difference_m3"))
        ratio = cad_span / single if single > 0.0 else 0.0
        if difference >= -0.0005:
            classification = "volume-matched-or-over"
        elif own_count == 0:
            classification = "no-label-in-target-frame"
        elif 0.80 <= ratio < 1.0:
            classification = "length-not-closed-in-same-beam"
        elif ratio < 0.80:
            classification = "instance-or-length-missing"
        else:
            classification = "instance-count-mismatch"
        rows.append({
            "code": code,
            "reference_instance_count": int(_number(
                row.get("reference_instance_count"))),
            "selected_equivalent_instance_count": int(_number(
                row.get("selected_equivalent_instance_count"))),
            "reference_single_axis_length_mm": _round(single, 1),
            "cad_selected_span_mm": _round(cad_span, 1),
            "cad_span_over_single_instance": _round(ratio, 2),
            "current_code_difference_m3": _round(difference),
            "target_frame_label_count": own_count,
            "other_frame_label_counts": other,
            "other_frame_label_total": sum(other.values()),
            "classification": classification,
            "action": {
                "length-not-closed-in-same-beam":
                    "本层图框有该编号标注，缺的是同一根梁的长度，走支座与净跨闭合",
                "instance-or-length-missing":
                    "本层图框有该编号标注，但 CAD 链长不足单实例轴长的 80%，"
                    "实例与长度双缺，先回图核标注覆盖范围，不得跨楼层取量",
                "instance-count-mismatch":
                    "CAD 链长已超过单实例轴长，参考实例数与图面标注数不一致，"
                    "按标注数复核广联达实例数口径",
                "no-label-in-target-frame":
                    "本层图框内没有该编号标注，量差来源不在本图，转其他图框或模型口径核对",
                "volume-matched-or-over": "量差不为负，不需要补几何",
            }[classification],
        })
    under = [row for row in rows
             if _number(row["current_code_difference_m3"]) < -0.0005]
    counts: dict[str, int] = defaultdict(int)
    for row in under:
        counts[row["classification"]] += 1
    volume_by_class: dict[str, float] = defaultdict(float)
    for row in under:
        volume_by_class[row["classification"]] += abs(
            _number(row["current_code_difference_m3"]))
    return {
        "schema": SCHEMA,
        "rule": ("图名位于图框下方，编号标注归给「其下方最近图名」所属图框；"
                 "只有目标图框内的标注才算本层证据，其他楼层图框的同名标注不得计入。"),
        "options": {
            "target_frame": target_frames[0],
            "column_tolerance_mm": _round(
                options.get("column_tolerance_mm", 50000.0), 1),
            "source_dxf": _text(options.get("source_dxf")),
        },
        "summary": {
            "label_count": len(labels),
            "title_count": len(titles),
            "frame_count": len(frames),
            "frame_label_counts": {
                frame: sum(counts.values()) for frame, counts in per_frame.items()},
            "under_code_count": len(under),
            "classification_counts": dict(counts),
            "classification_volume_m3": {
                key: _round(value) for key, value in volume_by_class.items()},
            "length_closure_volume_m3": _round(volume_by_class.get(
                "length-not-closed-in-same-beam")),
            "cross_floor_label_only_volume_m3": _round(
                sum(value for key, value in volume_by_class.items()
                    if key in ("no-label-in-target-frame",
                               "instance-or-length-missing"))),
        },
        "frames": frames,
        "code_index": rows,
        "labels": assigned[:400],
        "formal_ready": False,
        "applied_to_formal_quantity": False,
    }


def csv_rows(result: dict[str, Any]) -> list[list[Any]]:
    rows: list[list[Any]] = [
        ["section", "group", "code", "frame", "label_count", "single_len_mm",
         "cad_span_mm", "ratio", "difference_m3", "classification", "note"]]
    for frame in result["frames"]:
        rows.append(["frame", _text(frame.get("column_x_mm")), "",
                     _text(frame.get("frame")),
                     result["summary"]["frame_label_counts"].get(
                         _text(frame.get("frame")), 0),
                     "", "", "", "", "frame-title",
                     f"图名y {frame['title_y_mm']} ~ {frame['y_max_mm']}"])
    for row in result["code_index"]:
        rows.append(["code", _text(row.get("classification")),
                     _text(row.get("code")), _text(
                         result["options"].get("target_frame")),
                     row.get("target_frame_label_count"),
                     row.get("reference_single_axis_length_mm"),
                     row.get("cad_selected_span_mm"),
                     row.get("cad_span_over_single_instance"),
                     row.get("current_code_difference_m3"),
                     _text(row.get("classification")),
                     f"其他图框标注 {_text(row.get('other_frame_label_counts'))}；"
                     f"{_text(row.get('action'))}"])
    return rows


def render_markdown(result: dict[str, Any]) -> str:
    summary = result["summary"]
    lines = [
        "# 梁编号图框标签索引",
        "",
        f"- 规则：{result['rule']}",
        f"- 源文件：`{_text(result['options'].get('source_dxf'))}`；"
        f"编号标注 {summary['label_count']} 条、图名 {summary['title_count']} 处、"
        f"图框 {summary['frame_count']} 个。",
        f"- 目标图框：`{_text(result['options'].get('target_frame'))}`；"
        f"框内编号标注 "
        f"{summary['frame_label_counts'].get(_text(result['options'].get('target_frame')), 0)} 条。",
        "",
        "## 图框清单",
        "",
        "| 图框 | 列x mm | 图名y mm | 框内编号标注 |",
        "|---|---:|---:|---:|",
    ]
    for frame in result["frames"]:
        lines.append(
            f"| {_text(frame.get('frame'))} | {_text(frame.get('column_x_mm'))} | "
            f"{_text(frame.get('title_y_mm'))} | "
            f"{summary['frame_label_counts'].get(_text(frame.get('frame')), 0)} |")
    lines += [
        "",
        "## 偏少编号归属",
        "",
        "| 编号 | 参考实例 | 选中实例 | 单实例轴长mm | CAD链长mm | 倍率 | 量差m3 | 本框标注 | 其他框标注 | 判定 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in result["code_index"]:
        if _number(row.get("current_code_difference_m3")) >= -0.0005:
            continue
        others = "、".join(
            f"{key.replace('梁平法施工图', '').replace('墙柱平法施工图', '墙柱')}"
            f" {value}"
            for key, value in sorted(
                row["other_frame_label_counts"].items(),
                key=lambda item: -item[1])[:4]) or "无"
        lines.append(
            f"| {row['code']} | {row['reference_instance_count']} | "
            f"{row['selected_equivalent_instance_count']} | "
            f"{row['reference_single_axis_length_mm']:.0f} | "
            f"{row['cad_selected_span_mm']:.0f} | "
            f"{row['cad_span_over_single_instance']:.2f} | "
            f"{row['current_code_difference_m3']:.4f} | "
            f"{row['target_frame_label_count']} | {others} | "
            f"{row['classification']} |")
    lines += [
        "",
        "## 分类汇总",
        "",
        "| 判定 | 编号数 | 量差m3 | 处置 |",
        "|---|---:|---:|---|",
    ]
    actions = {
        "length-not-closed-in-same-beam": "走支座与净跨闭合，不跨图框",
        "instance-count-mismatch": "按图面标注数复核广联达实例数口径",
        "instance-or-length-missing": "先核标注覆盖范围，禁止跨楼层取量",
        "no-label-in-target-frame": "本图框无该编号，转模型口径核对",
    }
    for key, count in sorted(summary["classification_counts"].items(),
                             key=lambda item: -item[1]):
        lines.append(f"| {key} | {count} | "
                     f"{summary['classification_volume_m3'].get(key, 0):.4f} | "
                     f"{actions.get(key, '逐条回图')} |")
    no_label = summary["classification_counts"].get(
        "no-label-in-target-frame", 0)
    lines += [
        "",
        "## 结论",
        "",
        f"- 偏少编号里 `{summary['classification_counts'].get('length-not-closed-in-same-beam', 0)}` "
        f"个属于同一根梁长度未闭合（`{summary['length_closure_volume_m3']:.4f}` m3），"
        "必须走支座与净跨闭合。",
        f"- `{summary['classification_counts'].get('instance-count-mismatch', 0)}` "
        "个 CAD 链长已超单实例轴长，是参考实例数与图面标注数不一致，不得补造几何。",
        f"- `{summary['classification_counts'].get('instance-or-length-missing', 0)}` "
        f"个（`{summary['cross_floor_label_only_volume_m3']:.4f}` m3）本层图框有标注但"
        " CAD 链长不足单实例的 80%，属实例与长度双缺，需回图核标注覆盖范围。",
        ("- 本层图框内**没有**任何偏少编号缺标注。"
         if not no_label else
         f"- 有 `{no_label}` 个偏少编号在本层图框内没有标注，只能转其他图框核对。"),
        "- 同名编号在别的楼层图框的标注不计入本层，缺量不能靠跨楼层取量闭合。",
        "- 本节只做证据定位，不改体积，`formal_ready` 仍为 `false`。",
    ]
    return "\n".join(lines) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="整册 DXF 梁编号标注的图框归属与偏少编号定位")
    parser.add_argument("--geometry-dxf", required=True,
                        help="整册展开后的 DXF（块已炸开）")
    parser.add_argument("--reconciliation-json", required=True,
                        help="梁编号参考对账 JSON")
    parser.add_argument("--target-frame", required=True,
                        help="目标图框名，例如 二层梁平法施工图")
    parser.add_argument("--column-tolerance-mm", type=float, default=50000.0)
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()
    source = Path(args.geometry_dxf)
    recon_path = Path(args.reconciliation_json)
    missing = [str(path) for path in (source, recon_path) if not path.exists()]
    if missing:
        parser.error("缺少输入：" + "、".join(missing))
    labels, titles = scan_labels(source)
    result = build_index(labels, titles, json.loads(recon_path.read_text(
        encoding="utf-8")), {"target_frame": args.target_frame,
                             "column_tolerance_mm": args.column_tolerance_mm,
                             "source_dxf": str(source.resolve())})
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    json_path = out.with_suffix(".json")
    csv_path = out.with_suffix(".csv")
    md_path = out.with_suffix(".md")
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=1),
                         encoding="utf-8")
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle).writerows(csv_rows(result))
    md_path.write_text(render_markdown(result), encoding="utf-8")
    checksums = out.with_name(out.name + ".sha256")
    checksums.write_text("\n".join(
        f"{sha256(path)}  {path.resolve()}"
        for path in (json_path, csv_path, md_path)) + "\n", encoding="utf-8")
    print(json.dumps({
        "schema": result["schema"],
        "summary": result["summary"],
        "formal_ready": result["formal_ready"],
        "outputs": [str(json_path), str(csv_path), str(md_path), str(checksums)],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
