#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unify CAD member schedules, evidence and concrete quantities into one report."""
from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass



import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


SCHEMA = "cad-quantity-report/v0.21"
INTERSECTION_SCHEMAS = {
    "cad-member-intersection-audit/v0.1",
    "cad-member-intersection-audit/v0.2",
    "cad-member-intersection-audit/v0.3",
}
SLAB_OPENING_SCHEMA = "cad-slab-opening-audit/v0.1"
BEAM_GAP_SCHEMA = "cad-beam-gap-attribution/v0.1"
BEAM_COVERAGE_SCHEMA = "cad-beam-coverage-audit/v0.1"
BEAM_ATTRIBUTION_SCHEMA = "cad-beam-candidate-attribution/v0.1"
BEAM_FRAME_INDEX_SCHEMA = "cad-beam-frame-label-index/v0.1"
BEAM_SPAN_CLOSURE_SCHEMA = "cad-beam-span-closure/v0.1"
BEAM_MULTISPAN_SCHEMA = "cad-beam-multispan-closure/v0.1"
BEAM_DEDUP_SCHEMA = "cad-beam-instance-dedup/v0.1"
BEAM_CONFLICT_SCHEMA = "cad-beam-attribution-conflict/v0.1"
BEAM_CENTERLINE_SCHEMA = "cad-beam-centerline-support/v0.1"
WALL_EDGE_CLOSEOUT_SCHEMA = "cad-wall-edge-closeout/v0.1"
SLAB_PARTITION_SCHEMA = "cad-slab-thickness-partition/v0.1"
DEDUCTION_LEDGER_SCHEMA = "cad-deduction-ledger/v0.1"
PREFAB_EXPANSION_SCHEMA = "cad-prefab-instance-expansion/v0.1"
GLB_SCOPE_SCHEMA = "cad-glb-indicator-scope/v0.1"
SLAB_BIN_SCHEMA = "cad-slab-bin-reconciliation/v0.1"
SLAB_EVIDENCE_SCHEMA = "cad-slab-thickness-evidence/v0.1"
PREFAB_BOOKLET_SCHEMA = "cad-prefab-booklet-evidence/v0.1"
GRADE_LEDGER_SCHEMA = "cad-concrete-grade-ledger/v0.1"
SLAB_OPENING_STATUSES = {"rectangle-x", "closed-polyline", "closed-line-ring"}


def _load_json(path: str | Path | None) -> dict[str, Any]:
    if not path:
        return {}
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(str(source))
    data = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON 顶层必须是对象：{source}")
    return data


def _number(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _round(value: Any, digits: int = 4) -> float | None:
    number = _number(value)
    return round(number, digits) if number is not None else None


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        return "、".join(str(item) for item in value if item not in (None, ""))
    return str(value)


def _dedupe(values: list[Any]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        text = _text(value).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def _section(raw: dict[str, Any]) -> str:
    section = _text(
        raw.get("section")
        or raw.get("截面")
        or raw.get("截面b×h")
    ).strip()
    if section:
        return section
    b = _number(raw.get("b") or raw.get("截面b"))
    h = _number(raw.get("h") or raw.get("截面h"))
    if b and h:
        return f"{b:g}x{h:g}"
    sizes = [_text(item) for item in raw.get("sizes") or []]
    for item in sizes:
        match = re.search(
            r"(?<!\d)(\d{2,4})\s*[xX×]\s*(\d{2,4})(?!\d)", item)
        if match:
            return f"{match.group(1)}x{match.group(2)}"
        match = re.search(r"h\s*=\s*(\d{2,4})", item, re.I)
        if match:
            return f"h={match.group(1)}"
    return ""


def build_component_schedule(
        scan: dict[str, Any] | None,
        model: dict[str, Any] | None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    scan = scan or {}
    model = model or {}
    for category, members in (scan.get("members") or {}).items():
        if not isinstance(members, dict):
            continue
        for code, raw_value in members.items():
            raw = raw_value if isinstance(raw_value, dict) else {}
            section = _section(raw)
            stirrup = _text(
                raw.get("stirrup")
                or raw.get("箍筋")
                or raw.get("stir")
            )
            longitudinal = _text(
                raw.get("l_txt")
                or raw.get("纵筋原文")
                or raw.get("纵筋")
            )
            rebar_types = _dedupe([
                *(raw.get("rebar") or []),
                stirrup,
                longitudinal,
            ])
            observed = int(_number(raw.get("count")) or 0)
            estimated = int(_number(raw.get("est")) or observed)
            status = "complete" if section else "partial"
            if not section and not stirrup and not longitudinal:
                status = "index-only"
            rows.append({
                "category": category,
                "code": _text(code),
                "section": section,
                "stirrup": stirrup,
                "longitudinal": longitudinal,
                "rebar_types": rebar_types,
                "observed_count": observed,
                "estimated_count": estimated,
                "span_count": _text(raw.get("span") or raw.get("标注跨数")),
                "cantilever": _text(raw.get("cant") or raw.get("悬挑")),
                "length_mm": _round(raw.get("len_mm")),
                "concrete_candidate_m3": _round(raw.get("vol_m3")),
                "sizes": _dedupe(list(raw.get("sizes") or [])),
                "status": status,
                "source": "scan.members",
            })

    if rows:
        return sorted(
            rows,
            key=lambda row: (
                str(row["category"]),
                str(row["code"]).upper(),
            ),
        )

    for member in (model.get("members") or {}).get("beams") or []:
        rows.append({
            "category": "梁",
            "code": _text(member.get("code") or member.get("id")),
            "section": _text(member.get("section")),
            "stirrup": "",
            "longitudinal": "",
            "rebar_types": [],
            "observed_count": 1,
            "estimated_count": 1,
            "span_count": "",
            "cantilever": "",
            "length_mm": _round(member.get("centerline_length_mm")),
            "concrete_candidate_m3": _round(
                member.get("clear_volume_m3")
                or member.get("gross_volume_m3")),
            "sizes": [],
            "status": _text(member.get("quantity_status") or "model-only"),
            "source": "model.members.beams",
        })
    return rows


def build_rebar_schedule(scan: dict[str, Any] | None) -> list[dict[str, Any]]:
    scan = scan or {}
    rows: list[dict[str, Any]] = []
    summary = scan.get("rebar_summary") or {}
    for kind in ("箍筋", "纵筋"):
        for raw in summary.get(kind) or []:
            rows.append({
                "kind": kind,
                "model": _text(
                    raw.get("型号")
                    or raw.get("model")
                    or raw.get("spec")),
                "component_type_count": int(
                    _number(raw.get("构件型数")) or 0),
                "estimated_count": int(
                    _number(raw.get("估算根数")) or 0),
                "component_codes": _text(
                    raw.get("构件编号")
                    or raw.get("components")),
                "source": "scan.rebar_summary",
            })
    if rows:
        return rows

    for row in build_component_schedule(scan, None):
        for kind, value in (
                ("箍筋", row.get("stirrup")),
                ("纵筋", row.get("longitudinal"))):
            if not value:
                continue
            rows.append({
                "kind": kind,
                "model": value,
                "component_type_count": 1,
                "estimated_count": row.get("estimated_count") or 0,
                "component_codes": row.get("code") or "",
                "source": "component-schedule",
            })
    merged: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        key = (row["kind"], row["model"])
        if key not in merged:
            merged[key] = row
            continue
        target = merged[key]
        target["component_type_count"] += row["component_type_count"]
        target["estimated_count"] += row["estimated_count"]
        target["component_codes"] = "、".join(_dedupe([
            target["component_codes"],
            row["component_codes"],
        ]))
    return sorted(
        merged.values(),
        key=lambda row: (row["kind"], -row["estimated_count"], row["model"]),
    )


def build_column_schedule(
        scan: dict[str, Any] | None,
        model: dict[str, Any] | None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in build_component_schedule(scan, None):
        if row["category"] == "柱":
            rows.append({
                "code": row["code"],
                "section": row["section"],
                "count": row["estimated_count"],
                "stirrup": row["stirrup"],
                "longitudinal": row["longitudinal"],
                "status": row["status"],
                "source": "scan.members",
            })
    model = model or {}
    for index, member in enumerate(
            (model.get("members") or {}).get("columns") or [], 1):
        rows.append({
            "code": _text(member.get("label") or f"C{index:04d}"),
            "section": (
                f"{_number(member.get('b_mm')):g}x"
                f"{_number(member.get('h_mm')):g}"
                if _number(member.get("b_mm"))
                and _number(member.get("h_mm")) else ""
            ),
            "count": 1,
            "stirrup": "",
            "longitudinal": "",
            "status": _text(member.get("status") or "geometry"),
            "source": "model.members.columns",
        })
    return rows


def build_slab_schedule(
        scan: dict[str, Any] | None,
        model: dict[str, Any] | None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    model = model or {}
    for member in (model.get("members") or {}).get("slabs") or []:
        opening_area = _number(member.get("opening_area_m2"))
        opening_count = (
            int(_number(member.get("opening_count")) or 0)
            or len(member.get("opening_evidence") or [])
            or (1 if opening_area else 0)
        )
        area = _number(member.get("area_m2"))
        rows.append({
            "id": _text(member.get("id")),
            "code": _text(member.get("code")),
            "thickness_mm": _round(member.get("thickness_mm"), 1),
            "area_m2": _round(area),
            "gross_area_m2": _round(member.get("gross_area_m2")),
            "opening_count": opening_count,
            "opening_area_m2": _round(opening_area),
            "opening_status": _text(member.get("opening_status")),
            "net_area_m2": _round(
                area - (opening_area or 0.0)
                if area is not None else None),
            "volume_m3": _round(member.get("volume_m3")),
            "status": _text(member.get("status")),
            "material_observation": _text(
                member.get("material_observation")),
            "source": "model.members.slabs",
        })
    for panel in (model.get("members") or {}).get(
            "slab_panels") or []:
        opening_area = _number(panel.get("opening_area_m2"))
        opening_count = (
            int(_number(panel.get("opening_count")) or 0)
            or len(panel.get("opening_evidence") or [])
            or (1 if opening_area else 0)
        )
        area = _number(panel.get("area_m2"))
        rows.append({
            "id": _text(panel.get("id")),
            "code": _text(panel.get("code")),
            "thickness_mm": _round(panel.get("thickness_mm"), 1),
            "area_m2": _round(area),
            "gross_area_m2": _round(panel.get("gross_area_m2")),
            "opening_count": opening_count,
            "opening_area_m2": _round(opening_area),
            "opening_status": _text(panel.get("opening_status")),
            "net_area_m2": _round(
                area - (opening_area or 0.0)
                if area is not None else None),
            "volume_m3": _round(panel.get("volume_m3")),
            "status": _text(panel.get("status") or "panel-candidate"),
            "material_observation": _text(
                panel.get("material_observation")),
            "source": "model.members.slab_panels",
        })
    if rows:
        return rows
    scan = scan or {}
    for member in (scan.get("slab_thk") or {}).items():
        rows.append({
            "id": "",
            "code": "",
            "thickness_mm": _round(member[0], 1),
            "area_m2": None,
            "gross_area_m2": None,
            "opening_count": 0,
            "opening_area_m2": None,
            "volume_m3": None,
            "status": "thickness-candidate",
            "material_observation": "",
            "source": f"scan.slab_thk count={member[1]}",
        })
    return rows


def build_beam_schedule(
        model: dict[str, Any] | None,
        beam: dict[str, Any] | None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    model = model or {}
    for member in (model.get("members") or {}).get("beams") or []:
        centerline = member.get("centerline") or {}
        rows.append({
            "id": _text(member.get("id")),
            "code": _text(member.get("code")),
            "base_code": _text(member.get("base_code")),
            "section": _text(member.get("section")),
            "centerline_length_mm": _round(
                member.get("centerline_length_mm")
                or centerline.get("length_mm"), 1),
            "clear_length_mm": _round(member.get("clear_length_mm"), 1),
            "gross_volume_m3": _round(member.get("gross_volume_m3")),
            "clear_volume_m3": _round(member.get("clear_volume_m3")),
            "support_count": int(_number(member.get("support_count")) or 0),
            "quantity_status": _text(member.get("quantity_status")),
            "issue": _text(member.get("issue")),
            "x": _round((member.get("position") or {}).get("x"), 1),
            "y": _round((member.get("position") or {}).get("y"), 1),
            "source": "model.members.beams",
        })
    if rows:
        return rows
    beam = beam or {}
    for row in beam.get("rows") or []:
        rows.append({
            "id": "",
            "code": _text(row.get("code")),
            "base_code": _text(row.get("base_code")),
            "section": _text(row.get("section")),
            "centerline_length_mm": _round(row.get("length_mm"), 1),
            "clear_length_mm": None,
            "gross_volume_m3": _round(row.get("volume_m3")),
            "clear_volume_m3": None,
            "support_count": int(_number(row.get("support_count")) or 0),
            "quantity_status": _text(row.get("volume_status")),
            "issue": _text(row.get("issue")),
            "x": _round(row.get("x"), 1),
            "y": _round(row.get("y"), 1),
            "source": "beam_objects.rows",
        })
    return rows


def _supplement_summary(
        supplements: dict[str, dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for name, data in supplements.items():
        schema = _text(data.get("schema"))
        item: dict[str, Any] = {
            "schema": schema,
            "floor": _text(data.get("floor")),
            "formal_ready": data.get("formal_ready"),
            "status": _text(data.get("status")),
        }
        if schema == "cad-concrete-material-model/v0.1":
            item["totals"] = dict(data.get("totals") or {})
            item["ledger"] = list(data.get("ledger") or [])
        elif schema == "cad-vertical-model/v0.1":
            item["classification"] = dict(data.get("classification") or {})
            item["corrected_quantities"] = dict(
                data.get("corrected_quantities") or {})
            item["reference_quantities"] = dict(
                data.get("reference_quantities") or {})
        elif schema == "cad-composite-slab-material-ledger/v0.1":
            item["remaining_blockers"] = _dedupe(
                data.get("remaining_blockers") or [])
            item["material_ledger"] = list(data.get("material_ledger") or [])
            item["phase15_summary"] = dict(
                data.get("phase15") or {})
        elif schema == "cad-vertical-member-audit/v0.1":
            item["classification"] = dict(data.get("classification") or {})
            item["quantity_reconciliation"] = list(
                data.get("quantity_reconciliation") or [])
            item["remaining_blockers"] = _dedupe(
                data.get("remaining_blockers") or [])
        elif schema == "cad-model-only-beam-coverage/v0.1":
            ledger = list(data.get("coupling_beam_ledger") or [])
            item["coupling_beam_count"] = len(ledger)
            item["coupling_beam_volume_m3"] = _round(sum(
                _number(row.get("volume_m3")) or 0.0 for row in ledger))
            item["stair_beam_candidate_count"] = len(
                data.get("stair_beam_candidates") or [])
            item["concrete_ledger"] = dict(
                data.get("concrete_ledger") or {})
        elif schema == "cad-beam-reference-reconciliation/v0.1":
            summary = dict(data.get("summary") or {})
            transfers = dict(data.get("transfer_projection") or {})
            missing_by_code = [
                {
                    "code": _text(row.get("code")),
                    "reference_instance_count": int(
                        _number(row.get("reference_instance_count")) or 0),
                    "selected_equivalent_instance_count": int(
                        _number(row.get("selected_equivalent_instance_count"))
                        or 0),
                    "missing_equivalent_instance_count": int(
                        _number(row.get("missing_equivalent_instance_count"))
                        or 0),
                    "current_code_volume_m3": _round(
                        row.get("current_code_volume_m3")),
                    "reference_volume_m3": _round(
                        row.get("reference_volume_m3")),
                    "status": _text(row.get("status")),
                }
                for row in data.get("beam_code_reconciliation") or []
                if int(_number(row.get("missing_equivalent_instance_count"))
                       or 0) > 0
            ]
            missing_by_code.sort(key=lambda row: (
                -row["missing_equivalent_instance_count"],
                -abs((_number(row.get("current_code_volume_m3")) or 0.0)
                     - (_number(row.get("reference_volume_m3")) or 0.0)),
                row["code"],
            ))
            item["summary"] = summary
            item["transfer_projection"] = transfers
            item["missing_by_code"] = missing_by_code
        elif schema == "cad-special-member-and-wall-attribution/v0.1":
            spatial = data.get("edge_member_spatial_attribution") or {}
            special = data.get("special_member_localization") or {}
            item["edge_member_spatial"] = {
                "status": _text(spatial.get("status")),
                "outside_total_m2": _round(spatial.get("outside_total_m2")),
                "significant_member_count": int(
                    _number(spatial.get("significant_member_count")) or 0),
                "remaining_gate": _text(spatial.get("remaining_gate")),
            }
            item["special_members"] = {
                code: {
                    "status": _text(value.get("status")),
                    "reference_volume_m3": _round(
                        value.get("reference_volume_m3")),
                }
                for code, value in special.items()
                if isinstance(value, dict)
            }
        elif schema == BEAM_GAP_SCHEMA:
            summary = dict(data.get("summary") or {})
            item["summary"] = summary
            item["code_attribution"] = [
                row for row in data.get("code_attribution") or []
                if row.get("classification") != "volume-matched"][:14]
            item["search_targets"] = list(data.get("search_targets") or [])
            item["gap_decomposition"] = dict(
                summary.get("gap_decomposition") or {})
            item["support_and_span"] = dict(
                data.get("support_and_span") or {})
        elif schema == BEAM_COVERAGE_SCHEMA:
            summary = dict(data.get("summary") or {})
            item["summary"] = summary
            item["candidates"] = [
                row for row in data.get("candidates") or []
                if row.get("status") == "uncovered-beam-candidate"
            ][:16]
            item["duplicate_view_lines"] = list(
                data.get("duplicate_view_lines") or [])[:10]
        elif schema == BEAM_ATTRIBUTION_SCHEMA:
            summary = dict(data.get("summary") or {})
            item["summary"] = summary
            item["candidate_attribution"] = list(
                data.get("candidate_attribution") or [])[:12]
            item["residual_decomposition"] = dict(
                data.get("residual_decomposition") or {})
            targets = dict(data.get("under_code_targets") or {})
            targets["codes"] = list(targets.get("codes") or [])[:16]
            item["under_code_targets"] = targets
            item["section_recheck"] = {
                key: value
                for key, value in (data.get("section_recheck") or {}).items()
                if not isinstance(value, list)
            }
        elif schema == BEAM_FRAME_INDEX_SCHEMA:
            summary = dict(data.get("summary") or {})
            item["summary"] = summary
            item["frames"] = list(data.get("frames") or [])[:20]
            item["code_index"] = [
                row for row in data.get("code_index") or []
                if row.get("classification") != "volume-matched-or-over"][:16]
        elif schema == BEAM_SPAN_CLOSURE_SCHEMA:
            summary = dict(data.get("summary") or {})
            item["summary"] = summary
            item["code_closure"] = list(data.get("code_closure") or [])[:16]
            item["closure"] = dict(data.get("closure") or {})
        elif schema == BEAM_MULTISPAN_SCHEMA:
            summary = dict(data.get("summary") or {})
            item["summary"] = summary
            item["beams"] = [
                row for row in data.get("beams") or []
                if int(_number(row.get("extensions"))) > 0][:12]
            item["closure"] = dict(data.get("closure") or {})
        elif schema == BEAM_DEDUP_SCHEMA:
            summary = dict(data.get("summary") or {})
            item["summary"] = summary
            item["beam_only"] = [
                row for row in data.get("links") or []
                if _text(row.get("status")) == "beam-only"][:24]
            item["run_verdicts"] = [
                row for row in data.get("unpaired_run_triage") or []
                if _text(row.get("verdict")) in ("continuation-candidate",
                                                 "model-missing-instance")][:24]
            item["run_self_overlap"] = dict(data.get("run_self_overlap") or {})
            item["closure"] = dict(data.get("closure") or {})
        elif schema == BEAM_CONFLICT_SCHEMA:
            summary = dict(data.get("summary") or {})
            item["summary"] = summary
            item["conflicts"] = list(data.get("conflicts") or [])[:20]
            item["closure"] = dict(data.get("closure") or {})
        elif schema == SLAB_EVIDENCE_SCHEMA:
            item["summary"] = dict(data.get("summary") or {})
            item["closure"] = dict(data.get("closure") or {})
            item["conflicts"] = list(data.get("conflicts") or [])[:12]
        elif schema == PREFAB_BOOKLET_SCHEMA:
            item["summary"] = dict(data.get("summary") or {})
            item["closure"] = dict(data.get("closure") or {})
            item["design_facts"] = dict(data.get("design_facts") or {})
            item["comparisons"] = [
                {key: value for key, value in row.items() if not isinstance(value, dict)}
                for row in (data.get("comparisons") or [])[:12]
            ]
            item["identity_checks"] = list(data.get("identity_checks") or [])[:16]
            item["sheet_internal_notes"] = list(
                data.get("sheet_internal_notes") or [])[:8]
            proof = dict(data.get("version_self_proof") or {})
            item["version_self_proof"] = {
                key: value for key, value in proof.items()
                if not isinstance(value, (list, dict))
            }
            item["conclusions"] = list(data.get("conclusions") or [])[:6]
            item["frame_label_probe"] = dict(data.get("frame_label_probe") or {})
        elif schema == GRADE_LEDGER_SCHEMA:
            item["summary"] = dict(data.get("summary") or {})
            item["by_grade"] = dict(data.get("by_grade") or {})
            item["grade_source_types"] = {
                key: _dedupe(value or []) for key, value in
                (data.get("grade_source_types") or {}).items()
            }
            item["rows"] = list(data.get("rows") or [])[:14]
            item["rule_notes"] = dict(data.get("rule_notes") or {})
            item["floor"] = _text(data.get("floor"))
        elif schema == SLAB_BIN_SCHEMA:
            item["summary"] = dict(data.get("summary") or {})
            item["closure"] = dict(data.get("closure") or {})
            item["thickness_evidence_summary"] = dict(
                data.get("thickness_evidence_summary") or {})
        elif schema == GLB_SCOPE_SCHEMA:
            item["summary"] = dict(data.get("summary") or {})
            item["scope_buckets"] = list(data.get("scope_buckets") or [])
            item["identity_checks"] = dict(data.get("identity_checks") or {})
            item["slab_caliber"] = {
                key: value
                for key, value in (data.get("slab_caliber") or {}).items()
                if not isinstance(value, (list, dict))
            }
            item["closure"] = dict(data.get("closure") or {})
            item["next_actions"] = _dedupe(
                data.get("next_actions") or [])[:6]
        elif schema == SLAB_OPENING_SCHEMA:
            summary = dict(data.get("summary") or {})
            records = list(data.get("records") or [])
            item["summary"] = summary
            item["confirmed_openings"] = list(
                data.get("confirmed_openings") or [])
            item["review_records"] = [
                row for row in records if row.get("review_required")]
            item["prior_candidate_reconciliation"] = list(
                data.get("prior_candidate_reconciliation") or [])
        elif schema == SLAB_PARTITION_SCHEMA:
            item["summary"] = dict(data.get("summary") or {})
            item["gates"] = list(data.get("gates") or [])
        elif schema == DEDUCTION_LEDGER_SCHEMA:
            item["summary"] = dict(data.get("summary") or {})
            item["gates"] = list(data.get("gates") or [])
            item["rule_tally"] = list(data.get("rule_tally") or [])
            item["cross_book_overlaps"] = list(data.get("cross_book_overlaps") or [])
            item["verdicts"] = list(data.get("verdicts") or [])
        elif schema == PREFAB_EXPANSION_SCHEMA:
            item["summary"] = dict(data.get("summary") or {})
            item["gates"] = list(data.get("gates") or [])
            item["component_expansion"] = list(data.get("component_expansion") or [])
            item["unit_area_swap_candidates"] = list(
                data.get("unit_area_swap_candidates") or [])
            item["mirror_audit"] = dict(data.get("mirror_audit") or {})
        elif schema == WALL_EDGE_CLOSEOUT_SCHEMA:
            item["summary"] = dict(data.get("summary") or {})
            item["special_members"] = list(data.get("special_members") or [])
            item["reference_bucket_check"] = dict(data.get("reference_bucket_check") or {})
        elif schema == BEAM_CENTERLINE_SCHEMA:
            item["summary"] = dict(data.get("summary") or {})
            item["overlap_cross_check"] = {
                key: value for key, value in (data.get("overlap_cross_check") or {}).items()
                if not isinstance(value, (list, dict))}
        elif schema in INTERSECTION_SCHEMAS:
            item["summary"] = dict(data.get("summary") or {})
            item["net_quantity"] = dict(data.get("net_quantity") or {})
            item["top_overlaps"] = list(data.get("overlaps") or [])[:10]
            item["closure"] = dict(data.get("closure") or {})
        result[name] = item
    return result


def _special_member_closeout_gate(
        ledger: dict[str, Any],
        closeout: dict[str, Any] | None = None,
        ) -> dict[str, Any]:
    """特殊构件与空间闭合门槛：有逐格收口证据时按收口判定，否则按台账登记值。"""
    edge = dict(ledger.get("edge_member_spatial_attribution") or {})
    special = dict(ledger.get("special_member_localization") or {})
    outside = _number(edge.get("outside_total_m2")) or 0.0
    close_note = ""
    if closeout:
        cl_summary = dict(closeout.get("summary") or {})
        outside = _number(cl_summary.get("unattributed_area_m2")) or 0.0
        close_note = "；面域外已逐格归属（贴墙端 {0} m2、无墙可解释 {1} m2）".format(
            cl_summary.get("attached_area_m2"), outside)
        special = {row.get("code"): row for row in closeout.get("special_members") or []}
    tolerance = _number(edge.get("outside_review_tolerance_m2"))
    tolerance = 0.001 if tolerance is None else tolerance
    unresolved = []
    for code in sorted(special):
        info = dict(special.get(code) or {})
        status = _text(info.get("volume_status") or info.get("status")).lower()
        if closeout:
            if status not in ("counted-in-reference-beam-bucket-not-additive",
                              "independent-cad-quantity"):
                unresolved.append(code)
        elif any(word in status for word in
                 ("not-independent", "reference-only", "candidate", "partially")):
            unresolved.append(code)
    closed = bool(special or edge) and not unresolved and outside <= tolerance
    parts = []
    if special:
        parts.append("特殊构件独立 CAD 算量未定档 %d 个：%s" % (
            len(unresolved), "、".join(unresolved) or "无"))
    if edge:
        parts.append("边缘构件面域外面积 %.4f m2（阈值 %.4f m2、完全在面域外 %d 个）" % (
            outside, tolerance,
            int(_number(edge.get("fully_outside_member_count")) or 0)))
    evidence = "；".join(parts) or "台账未给出特殊构件与边缘构件字段"
    evidence += close_note
    return {
        "id": "special-member-closeout",
        "title": "特殊构件与空间闭合",
        "status": "pass" if closed else "fail",
        "evidence": evidence,
        "action": ("特殊构件归属已定且面域外面积已全部解释，可并入正式量"
                   if closed else
                   "回图确认特殊构件截面与支座，并把面域外轮廓归到构件后重算"),
    }


def _normalize_ledger(ledger: dict[str, Any]) -> dict[str, Any]:
    if not ledger or ledger.get("quantities"):
        return ledger
    concrete = ledger.get("concrete_ledger")
    if not isinstance(concrete, dict):
        return ledger
    candidate = _number(concrete.get("located_total_m3"))
    reference = _number(concrete.get("reference_total_m3"))
    comparisons = [
        {
            "component": "梁及连梁",
            "scope": "已定位 CAD 几何与楼梯梁独立台账",
            "candidate_value_m3": _round(concrete.get("located_beam_total_m3")),
            "reference_value_m3": _round(concrete.get("beam_reference_m3")),
            "difference_m3": _round(-( (
                _number(concrete.get("beam_remaining_m3")) or 0.0))),
            "status": "research-candidate",
        },
        {
            "component": "剪力墙",
            "scope": "墙柱候选",
            "candidate_value_m3": _round(concrete.get("vertical_candidate_m3")),
            "reference_value_m3": _round(concrete.get("vertical_reference_m3")),
            "difference_m3": _round(concrete.get("vertical_remaining_m3")),
            "status": "research-candidate",
        },
        {
            "component": "板体系",
            "scope": "板体系分账",
            "candidate_value_m3": _round(concrete.get("slab_m3")),
            "reference_value_m3": _round(concrete.get("slab_m3")),
            "difference_m3": 0.0,
            "status": "research-candidate",
        },
        {
            "component": "合计",
            "scope": "综合定位量",
            "candidate_value_m3": _round(candidate),
            "reference_value_m3": _round(reference),
            "difference_m3": _round(concrete.get("remaining_total_m3")),
            "status": "research-only",
        },
    ]
    for row in comparisons:
        value = _number(row.get("reference_value_m3"))
        difference = _number(row.get("difference_m3"))
        row["difference_pct"] = (
            round(difference / value * 100.0, 2)
            if difference is not None and value
            else None
        )
    gates = list(ledger.get("gates") or [])
    if not gates:
        gates = [_special_member_closeout_gate(ledger)]
    return {
        "schema": _text(ledger.get("schema") or "cad-concrete-ledger/embedded"),
        "source_schema": _text(ledger.get("schema")),
        "floor": ledger.get("floor") or {},
        "formal_ready": bool(ledger.get("formal_ready")),
        "reference_values": {"综合参考": reference} if reference is not None else {},
        "quantities": {
            "beam_topology_volume_m3": _round(
                concrete.get("main_beam_cad_m3")),
            "beam_located_total_volume_m3": _round(
                concrete.get("located_beam_total_m3")),
            "vertical_candidate_volume_m3": _round(
                concrete.get("vertical_candidate_m3")),
            "slab_rough_volume_m3": _round(concrete.get("slab_m3")),
            "candidate_total_volume_m3": _round(candidate),
            "remaining_total_volume_m3": _round(
                concrete.get("remaining_total_m3")),
            "beam_coverage_ratio": _round(
                concrete.get("beam_coverage_ratio")),
        },
        "comparisons": comparisons,
        "gate_summary": dict(Counter(row["status"] for row in gates)),
        "gates": gates,
        "embedded_concrete_ledger": concrete,
    }


def _closure_dashboard(
        ledger: dict[str, Any],
        supplements: dict[str, dict[str, Any]],
        anomalies: list[dict[str, Any]]) -> dict[str, Any]:
    gates = [
        {
            "id": _text(row.get("id") or row.get("title")),
            "title": _text(row.get("title") or row.get("id")),
            "status": _text(row.get("status") or "unknown"),
            "evidence": _text(row.get("evidence")),
            "action": _text(row.get("action")),
        }
        for row in ledger.get("gates") or []
    ]
    closeout = next((data for data in supplements.values()
                     if _text(data.get("schema")) == WALL_EDGE_CLOSEOUT_SCHEMA), None)
    if closeout:
        # 就地替换、不改变顺序：回归按列表索引展平，换位会造出假漂移
        gates = [_special_member_closeout_gate(ledger, closeout)
                 if row["id"] == "special-member-closeout" else row for row in gates]
    gate_counts = Counter(row["status"] for row in gates)
    blockers = [
        row for row in anomalies if row.get("severity") == "blocking"
    ]
    grouped: dict[tuple[str, str], dict[str, Any]] = {}
    for row in blockers:
        key = (_text(row.get("area")), _text(row.get("status")))
        if key not in grouped:
            grouped[key] = {
                "area": key[0],
                "status": key[1],
                "count": 0,
                "member_ids": [],
                "codes": [],
            }
        group = grouped[key]
        group["count"] += 1
        for field, source in (
                ("member_ids", "member_id"),
                ("codes", "code")):
            value = _text(row.get(source))
            if value and value not in group[field]:
                group[field].append(value)
    blocking_groups = sorted(
        grouped.values(),
        key=lambda row: (-row["count"], row["area"], row["status"]),
    )

    component_gaps: list[dict[str, Any]] = []
    # 新门槛一律追加尾部：回归按列表索引展平比较，插在中间会挪动后面每一条
    tail_gates: list[dict[str, Any]] = []
    for name, data in supplements.items():
        schema = _text(data.get("schema"))
        if schema == "cad-beam-reference-reconciliation/v0.1":
            summary = data.get("summary") or {}
            missing = int(_number(
                summary.get("missing_equivalent_instance_count")) or 0)
            component_gaps.append({
                "component": "梁等效实例",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": missing,
                "evidence": (
                    f"参考 {summary.get('reference_main_instance_count', 0)}；"
                    f"已定位 {summary.get('selected_equivalent_instance_count', 0)}；"
                    f"缺失 {missing}"
                ),
                "blockers": [
                    f"{row.get('code')} 缺 "
                    f"{row.get('missing_equivalent_instance_count')} 个实例"
                    for row in data.get("beam_code_reconciliation") or []
                    if int(_number(
                        row.get("missing_equivalent_instance_count")) or 0)
                    > 0
                ],
                "action": (
                    "回图定位缺失的梁等效实例；"
                    + (
                        "优先 WKL4(1)、KL12(2)、L5(1)。"
                        if missing else "复核编号级长度差异。"
                    )
                ),
            })
        elif schema == "cad-composite-slab-material-ledger/v0.1":
            phase15 = data.get("phase15_summary") or data.get("phase15") or {}
            phase15_evidence: list[str] = []
            if phase15.get("panel_area_m2") is not None:
                phase15_evidence.append(
                    f"板拓扑毛 {phase15.get('panel_area_m2')} m2")
            if phase15.get("opening_count") is not None:
                phase15_evidence.append(
                    f"洞口 {phase15.get('opening_count')} 个")
            if phase15.get("net_panel_area_m2") is not None:
                phase15_evidence.append(
                    f"净 {phase15.get('net_panel_area_m2')} m2")
            component_gaps.append({
                "component": "板材料体系",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": len(data.get("remaining_blockers") or []),
                "evidence": "；".join(_dedupe([
                    _text(data.get("status")),
                    "，".join(phase15_evidence) if phase15_evidence else "",
                ])),
                "blockers": _dedupe(data.get("remaining_blockers") or []),
                "action": (
                    "核对阶段十五洞口扣减与板材料体系；"
                    "按剩余阻断项回图复核。"
                ),
            })
        elif schema == "cad-vertical-member-audit/v0.1":
            component_gaps.append({
                "component": "墙柱归类",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": len(data.get("remaining_blockers") or []),
                "evidence": _text(
                    (data.get("classification") or {}).get("status")),
                "blockers": _dedupe(
                    data.get("remaining_blockers") or []),
                "action": "完成墙柱条带、边缘构件和独立柱归类复核。",
            })
        elif schema == "cad-special-member-and-wall-attribution/v0.1":
            spatial = data.get("edge_member_spatial_attribution") or {}
            special = data.get("special_member_localization") or {}
            special_rows = [
                {
                    "code": code,
                    "status": _text(value.get("status")),
                }
                for code, value in special.items()
                if isinstance(value, dict)
            ]
            component_gaps.append({
                "component": "特殊构件与空间闭合",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": len([
                    row for row in special_rows
                    if "localized" not in _text(row.get("status"))
                ]) + len([
                    row for row in spatial.get("members") or []
                    if row.get("review_required")
                ]),
                "evidence": _text(spatial.get("remaining_gate")),
                "blockers": [
                    f"{row.get('id')} 面域外 {_text(row.get('outside_area_m2'))} m2"
                    for row in spatial.get("members") or []
                    if row.get("review_required")
                ],
                "action": "闭合边缘构件外置面域，并复核特殊梁独立量。",
            })
        elif schema == BEAM_GAP_SCHEMA:
            audit_summary = data.get("summary") or {}
            gap_total = abs(_number(audit_summary.get("net_code_difference_m3")))
            component_gaps.append({
                "component": "梁体积缺口",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": int(_number(
                    audit_summary.get("search_target_count")) or 0),
                "evidence": (
                    f"净未定位 {gap_total:.4f} m3；"
                    f"计数口径差实例 "
                    f"{int(_number(audit_summary.get('count_only_missing_instance_count')) or 0)} 个；"
                    f"未归属图线池 "
                    f"{_text(audit_summary.get('unassigned_run_volume_m3'))} m3"
                ),
                "blockers": [
                    f"{row.get('code')} 缺 {_text(row.get('missing_volume_m3'))} m3"
                    f"/需补 {_text(row.get('needed_length_mm'))} mm"
                    for row in (data.get("search_targets") or [])[:8]
                ],
                "action": (
                    "按检索目标回图补梁几何或确认编号归属；"
                    "计数口径差不得补造几何。"
                ),
            })
            decomposition = audit_summary.get("gap_decomposition") or {}
            gates.append({
                "id": "beam-volume-gap-attribution",
                "title": "梁体积缺口归因",
                "status": (
                    "pass" if (data.get("closure") or {}).get("reconciled")
                    and gap_total <= 0.05 else "warn"),
                "evidence": (
                    f"分解合计 "
                    f"{_text(decomposition.get('sum_difference_m3'))} m3"
                    f"{'与台账一致' if decomposition.get('matches_ledger') else '与台账不一致'}；"
                    f"缺量编号 {int(_number(audit_summary.get('volume_under_code_count')) or 0)} 个"
                ),
                "action": (
                    "补齐检索目标中的梁几何后重算；未补齐前梁净跨量仍为中心线粗算。"
                ),
            })
        elif schema == BEAM_COVERAGE_SCHEMA:
            audit_summary = data.get("summary") or {}
            component_gaps.append({
                "component": "梁图层覆盖",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": int(_number(
                    audit_summary.get("uncovered_in_frame_count")) or 0),
                "evidence": (
                    f"提取窗口内覆盖率 "
                    f"{(_number(audit_summary.get('in_frame_coverage_ratio')) or 0) * 100:.2f}%；"
                    f"未覆盖 {_number(audit_summary.get('uncovered_in_frame_length_mm')) or 0:.0f} mm；"
                    f"窗口内候选梁 "
                    f"{int(_number(audit_summary.get('candidate_beam_in_frame_count')) or 0)} 条/"
                    f"{_text(audit_summary.get('candidate_volume_in_frame_m3'))} m3；"
                    f"窗口外板面域内 "
                    f"{_text(audit_summary.get('candidate_volume_window_out_m3'))} m3"
                ),
                "blockers": [
                    f"{'+'.join(row.get('handles') or [])} "
                    f"{_text(row.get('width_mm'))}x{_text(row.get('assumed_height_mm'))}"
                    f"/{_text(row.get('length_mm'))} mm ({row.get('view_zone')})"
                    for row in (data.get("candidates") or [])[:8]
                ],
                "action": (
                    "窗口外图线已按镜像对称和整视图平移归位，扩窗已证伪；"
                    "剩余缺口回到梁实例台账逐编号核对截面高度与编号归属。"
                ),
            })
            gates.append({
                "id": "beam-coverage-audit",
                "title": "梁图层覆盖审计",
                "status": (
                    "pass" if audit_summary.get("coverage_closed")
                    and audit_summary.get("residual_within_tolerance")
                    else "warn"),
                "evidence": (
                    f"窗口内覆盖率 "
                    f"{(_number(audit_summary.get('in_frame_coverage_ratio')) or 0) * 100:.2f}%；"
                    f"缺口未解释 "
                    f"{_text(audit_summary.get('residual_still_unexplained_m3'))} m3；"
                    f"重复视图剔除 "
                    f"{int(_number(audit_summary.get('duplicate_view_line_count')) or 0)} 段"
                    f"（偏移 {_text(audit_summary.get('duplicate_view_offset_mm'))} mm）"
                ),
                "action": (
                    "镜像对称线与平移孪生线只作视图归属证据，不得并入本层漏量；"
                    "未解释余量按截面高度与编号归属追查，不得用窗口外图线凑量。"
                ),
            })
        elif schema == BEAM_ATTRIBUTION_SCHEMA:
            attr_summary = data.get("summary") or {}
            decomposition = dict(data.get("residual_decomposition") or {})
            targets = dict(data.get("under_code_targets") or {})
            gates_row = dict((data.get("closure") or {}).get("gates") or {})
            component_gaps.append({
                "component": "梁候选段归属",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": int(_number(
                    attr_summary.get("no_coaxial_run_count")) or 0),
                "evidence": (
                    f"截面口径差 {_text(attr_summary.get('section_caliber_delta_m3'))} m3；"
                    f"可归属续接段 {_text(attr_summary.get('attached_to_existing_code_m3'))} m3；"
                    f"无编号候选 {_text(attr_summary.get('unattached_candidate_m3'))} m3/"
                    f"{_text(decomposition.get('unattached_length_mm'))} mm；"
                    f"本图框无法解释 {_text(attr_summary.get('unexplained_by_this_frame_m3'))} m3"
                ),
                "blockers": [
                    f"{_text(row.get('handles'))} "
                    f"{_text(row.get('length_mm'))}mm → "
                    f"{_text(row.get('matched_code')) or '无同轴编号'}"
                    for row in (data.get("candidate_attribution") or [])[:8]
                ],
                "action": (
                    "偏少编号需跨图框检索 "
                    f"{int(_number(targets.get('cross_frame_code_count')) or 0)} 个/"
                    f"{_text(targets.get('cross_frame_needed_length_mm'))} mm；"
                    "认领只缩短回图清单，不计入梁量。"
                ),
            })
            gates.append({
                "id": "beam-candidate-attribution",
                "title": "梁候选段归属与截面口径",
                "status": "pass" if not int(_number(
                    (data.get("closure") or {}).get("fail_count")) or 0) else "warn",
                "evidence": (
                    f"门槛 "
                    + "、".join(
                        f"{key}={'通过' if value else '未过'}"
                        for key, value in sorted(gates_row.items()))
                ),
                "action": (
                    "无同轴编号的候选段不得凭位置补编号；"
                    "截面口径已排除后，剩余缺量只能回图或跨图框取证。"
                ),
            })
        elif schema == BEAM_FRAME_INDEX_SCHEMA:
            index_summary = data.get("summary") or {}
            counts = dict(index_summary.get("classification_counts") or {})
            volumes = dict(index_summary.get("classification_volume_m3") or {})
            component_gaps.append({
                "component": "梁编号图框归属",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": int(_number(
                    index_summary.get("under_code_count")) or 0),
                "evidence": (
                    f"整册编号标注 {int(_number(index_summary.get('label_count')) or 0)} 条/"
                    f"图框 {int(_number(index_summary.get('frame_count')) or 0)} 个；"
                    f"本层图框偏少编号分类 "
                    + "、".join(f"{key} {value}" for key, value in sorted(counts.items()))
                ),
                "blockers": [
                    f"{_text(row.get('code'))} → {_text(row.get('classification'))}"
                    for row in (data.get("code_index") or [])[:8]
                ],
                "action": (
                    "同名标注在其他楼层图框的编号不计入本层；"
                    "缺量按本层图框标注与链长倍率定责，不得跨楼层补量。"
                ),
            })
            gates.append({
                "id": "beam-frame-label-index",
                "title": "梁编号图框标签索引",
                "status": ("pass" if int(_number(
                    counts.get("no-label-in-target-frame")) or 0) == 0
                    and int(_number(
                        index_summary.get("under_code_count")) or 0) == 0
                    else "warn"),
                "evidence": (
                    f"偏少编号 {int(_number(index_summary.get('under_code_count')) or 0)} 个；"
                    f"长度未闭合 "
                    f"{_text(index_summary.get('length_closure_volume_m3'))} m3；"
                    f"本层无标注 {int(_number(counts.get('no-label-in-target-frame')) or 0)} 个"
                ),
                "action": (
                    f"其他楼层图框标注 "
                    f"{_text(index_summary.get('cross_floor_label_only_volume_m3'))} m3 "
                    "只作定位证据，不计入本层。"
                ),
            })
        elif schema == BEAM_SPAN_CLOSURE_SCHEMA:
            closure_summary = data.get("summary") or {}
            verdict_counts = dict(closure_summary.get("verdict_counts") or {})
            verdict_volumes = dict(closure_summary.get("verdict_volume_m3") or {})
            closure_gates = dict((data.get("closure") or {}).get("gates") or {})
            component_gaps.append({
                "component": "梁净跨口径",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": int(_number(
                    verdict_counts.get("deficit-exceeds-support-inference")) or 0)
                + int(_number(verdict_counts.get("chain-lost-in-reconciliation")) or 0),
                "evidence": (
                    f"中心线 {_text(closure_summary.get('gross_volume_m3'))} m3 / "
                    f"净跨 {_text(closure_summary.get('clear_volume_m3'))} m3，"
                    f"口径差 {_text(closure_summary.get('span_caliber_difference_m3'))} m3；"
                    f"相交审计梁侧可扣 "
                    f"{_text(closure_summary.get('intersection_beam_side_deduction_m3'))} m3，"
                    f"冲突 {_text(closure_summary.get('span_caliber_vs_intersection_conflict_m3'))} m3"
                ),
                "blockers": [
                    f"{_text(row.get('code'))} → {_text(row.get('verdict'))}"
                    f"（差 {_text(row.get('single_instance_deficit_mm'))} mm）"
                    for row in (data.get("code_closure") or [])[:8]
                ],
                "action": (
                    "推定端 "
                    f"{_text(closure_summary.get('inferred_end_support_width_mm'))} mm "
                    "未经原图确认前维持中心线口径；定责合计需覆盖偏少编号毛差。"
                ),
            })
            gates.append({
                "id": "beam-span-caliber",
                "title": "梁净跨口径与支座扣减",
                "status": ("pass" if closure_gates and all(
                    bool(value) for value in closure_gates.values())
                    else "warn"),
                "evidence": (
                    "定责 " + "、".join(
                        f"{key} {value}/{verdict_volumes.get(key, 0)}m3"
                        for key, value in sorted(verdict_counts.items()))
                    + f"，合计 {_text(closure_summary.get('verdict_total_m3'))} m3"
                ),
                "action": (
                    "真需补几何 "
                    f"{_text(closure_summary.get('needs_new_geometry_volume_m3'))} m3、"
                    f"编号链丢失 "
                    f"{_text(closure_summary.get('chain_lost_volume_m3'))} m3，"
                    f"其余 {_text(closure_summary.get('caliber_only_volume_m3'))} m3 为口径问题。"
                ),
            })
        elif schema == BEAM_MULTISPAN_SCHEMA:
            multi_summary = data.get("summary") or {}
            multi_gates = dict((data.get("closure") or {}).get("gates") or {})
            component_gaps.append({
                "component": "多跨梁续接候选",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": int(_number(
                    multi_summary.get("no_continuation_beam_count")) or 0),
                "evidence": (
                    f"带宽≥2 的梁 {int(_number(multi_summary.get('multispan_beam_count')) or 0)} 根，"
                    f"续接成功 {int(_number(multi_summary.get('continued_beam_count')) or 0)} 根/"
                    f"{_text(multi_summary.get('added_axis_length_mm'))} mm/"
                    f"候选 {_text(multi_summary.get('added_volume_candidate_m3'))} m3；"
                    f"单实例长度缺口 {_text(multi_summary.get('deficit_before_mm'))}"
                    f"→{_text(multi_summary.get('deficit_after_mm'))} mm"
                ),
                "blockers": [
                    f"{_text(row.get('beam_id'))} {_text(row.get('code'))} "
                    f"+{_text(row.get('added_axis_length_mm'))}mm "
                    f"经 {_text((row.get('added_evidence') or [{}])[0].get('support_handle'))}"
                    f"→{_text((row.get('added_evidence') or [{}])[0].get('beam_handle'))}"
                    for row in (data.get("beams") or [])[:8]
                ],
                "action": (
                    "续接量未经回图确认不并入混凝土量；"
                    "剩余缺口按支座性质与编号覆盖范围逐条核对。"
                ),
            })
            gates.append({
                "id": "beam-multispan-continuation",
                "title": "多跨梁跨支座续接",
                "status": ("pass" if multi_gates.get(
                    "continuation-covers-deficit")
                    and not multi_gates.get("applied-to-formal-quantity")
                    else "warn"),
                "evidence": (
                    f"闭合率 "
                    f"{(_number(multi_summary.get('deficit_closed_ratio')) or 0) * 100:.1f}%；"
                    f"候选 {_text(multi_summary.get('added_volume_candidate_m3'))} m3；"
                    f"无续接 {int(_number(multi_summary.get('no_continuation_beam_count')) or 0)} 根"
                ),
                "action": (
                    f"按句柄回图确认续接段编号归属后，才能把 "
                    f"{_text(multi_summary.get('added_volume_candidate_m3'))} m3 "
                    "并入梁量。"
                ),
            })
        elif schema == BEAM_DEDUP_SCHEMA:
            dedup_summary = data.get("summary") or {}
            dedup_gates = dict((data.get("closure") or {}).get("gates") or {})
            class_count = dict(
                dedup_summary.get("beam_only_class_count") or {})
            class_volume = dict(
                dedup_summary.get("beam_only_class_volume_m3") or {})
            verdict_volume = dict(
                dedup_summary.get("unpaired_run_verdict_volume_m3") or {})
            component_gaps.append({
                "component": "梁实例双口径去重",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": int(_number(
                    dedup_summary.get("unmatched_run_count")) or 0),
                "evidence": (
                    f"模型梁 {int(_number(dedup_summary.get('beam_count')) or 0)} 根/"
                    f"{_text(dedup_summary.get('beam_volume_m3'))} m3 与算量实例 "
                    f"{int(_number(dedup_summary.get('run_count')) or 0)} 条/"
                    f"{_text(dedup_summary.get('run_volume_m3'))} m3 配对 "
                    f"{int(_number(dedup_summary.get('matched_beam_count')) or 0)} 根，"
                    f"两口径相加重复计量 {_text(dedup_summary.get('double_count_volume_m3'))} m3；"
                    f"无 run 梁里归属冲突 "
                    f"{int(class_count.get('attribution-conflict') or 0)} 根/"
                    f"{_text(class_volume.get('attribution-conflict'))} m3、"
                    f"真编号缺失 {int(class_count.get('code-absent') or 0)} 根/"
                    f"{_text(class_volume.get('code-absent'))} m3"
                ),
                "blockers": [
                    (
                        lambda run_ids: (
                            f"{_text(row.get('beam_id'))} {_text(row.get('code'))} "
                            f"{_text(row.get('beam_volume_m3'))} m3 "
                            f"{_text(row.get('beam_only_class'))} "
                            f"同编号未配对 run {_text(run_ids)}"
                        )
                    )("|".join(row.get("unpaired_same_code_run_ids") or []) or "无")
                    for row in (data.get("links") or [])
                    if _text(row.get("status")) == "beam-only"
                ][:12],
                "action": (
                    f"模型梁口径净新增仅 "
                    f"{_text(dedup_summary.get('model_beam_net_new_volume_m3'))} m3，"
                    "禁止把模型梁并进分账；未配对 run 里模型缺实例 "
                    f"{_text(verdict_volume.get('model-missing-instance'))} m3"
                    "，只有带引线证据的部分可用于与参考实例逐编号对账。"
                ),
            })
            gates.append({
                "id": "beam-instance-dedup",
                "title": "梁实例双口径去重",
                "status": ("pass" if dedup_gates.get(
                    "no-silent-double-count")
                    and dedup_gates.get("run-population-no-self-overlap")
                    else "warn"),
                "evidence": (
                    f"重复计量风险 "
                    f"{_text(dedup_summary.get('double_count_volume_m3'))} m3；"
                    f"模型梁净新增候选 "
                    f"{_text(dedup_summary.get('model_beam_net_new_volume_m3'))} m3；"
                    f"run 口径内部重叠 "
                    f"{int(_number(dedup_summary.get('run_self_overlap_pair_count')) or 0)} 处"
                ),
                "action": (
                    "统一分账按 run 口径计梁，模型梁口径只作复核；"
                    "归属冲突与模型缺实例须回图定责后才可改量。"
                ),
            })
        elif schema == BEAM_CONFLICT_SCHEMA:
            conflict_summary = data.get("summary") or {}
            conflict_gates = dict((data.get("closure") or {}).get("gates") or {})
            conflict_verdicts = dict(conflict_summary.get("verdicts") or {})
            component_gaps.append({
                "component": "梁编号归属冲突",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": int(_number(
                    conflict_summary.get("conflict_pair_count")) or 0),
                "evidence": (
                    f"冲突 {int(_number(conflict_summary.get('conflict_pair_count')) or 0)} 对/"
                    f"涉及 run {int(_number(conflict_summary.get('conflict_run_count')) or 0)} 条、"
                    f"模型梁 {int(_number(conflict_summary.get('conflict_beam_count')) or 0)} 根，"
                    f"两口径相加重复计量风险 "
                    f"{_text(conflict_summary.get('double_count_risk_m3'))} m3；"
                    f"run 编号成立 {int((conflict_verdicts.get('run-label-holds') or {}).get('pair_count') or 0)} 对、"
                    f"模型梁编号成立 {int((conflict_verdicts.get('beam-label-holds') or {}).get('pair_count') or 0)} 对、"
                    f"同轴双标注 {int((conflict_verdicts.get('dual-label-same-line') or {}).get('pair_count') or 0)} 对、"
                    f"无标注证据 {int((conflict_verdicts.get('no-label-evidence') or {}).get('pair_count') or 0)} 对；"
                    f"逐对定主后已定 "
                    f"{int(_number(conflict_summary.get('ownership_decided_pair_count')) or 0)} 对、"
                    f"仍需复核 {int(_number(conflict_summary.get('ownership_open_pair_count')) or 0)} 对，"
                    f"编号转移 {_text(conflict_summary.get('attribution_transfer_m3'))} m3"
                    f"（对平残差 {_text(conflict_summary.get('attribution_balance_residual_m3'))}）、"
                    f"归属后剩余风险 {_text(conflict_summary.get('residual_double_count_risk_m3'))} m3"
                ),
                "blockers": [
                    f"{_text(row.get('run_id'))} {_text(row.get('run_code'))} vs "
                    f"{_text(row.get('beam_id'))} {_text(row.get('beam_code'))} "
                    f"{_text(row.get('verdict'))}/{_text(row.get('confidence'))} "
                    f"风险 {_text(row.get('double_count_risk_m3'))} m3 "
                    f"回图 {_text(row.get('review_xy'))}"
                    for row in (data.get("conflicts") or [])
                    if _text((row.get("ownership") or {}).get("status")) == "review-open"
                ][:12] + [
                    f"{_text(row.get('run_id'))}/{_text(row.get('beam_id'))} 判归 "
                    f"{_text((row.get('ownership') or {}).get('code'))}，"
                    f"从 {_text(row.get('loser_code'))} 搬 {row.get('ownership', {}).get('transfer_m3')} m3"
                    for row in (data.get("conflicts") or [])
                    if _text((row.get("ownership") or {}).get("status")) == "owner-decided"
                ][:12],
                "action": (
                    "定主只搬编号归属、不搬几何，逐对转移必须与总量对平；"
                    "同轴双标注与无标注证据两类不得自动定主；"
                    "同线异跨要先修算量实例成链的支座断链规则再定主。"
                ),
            })
            open_pairs = int(_number(
                conflict_summary.get("ownership_open_pair_count")) or 0)
            balance = abs(_number(
                conflict_summary.get("attribution_balance_residual_m3")))
            has_ownership = "ownership_decided_pair_count" in conflict_summary
            gates.append({
                "id": "beam-attribution-conflict",
                "title": "梁编号归属冲突定责",
                "status": ("pass" if has_ownership and open_pairs == 0
                           and balance <= 1e-9 and conflict_gates.get(
                               "no-unadjudicated-dual-label")
                           and not (conflict_verdicts.get("no-label-evidence"))
                           and not (conflict_verdicts.get("same-line-different-spans"))
                           else "warn"),
                "evidence": (
                    (f"{int(_number(conflict_summary.get('conflict_pair_count')) or 0)} 对冲突/"
                     f"定主后剩余风险 "
                     f"{_text(conflict_summary.get('residual_double_count_risk_m3'))} m3/"
                     f"待复核 {open_pairs} 对；"
                     f"引线置信 {json.dumps(conflict_summary.get('label_confidence_counts') or {}, ensure_ascii=False)}")
                    if has_ownership else
                    f"{int(_number(conflict_summary.get('conflict_pair_count')) or 0)} 对冲突/"
                    f"风险 {_text(conflict_summary.get('double_count_risk_m3'))} m3；"
                    f"引线置信 {json.dumps(conflict_summary.get('label_confidence_counts') or {}, ensure_ascii=False)}"
                ),
                "action": (
                    "剩余待复核对按回图坐标定跨；无标注证据的冲突不得改编号。"
                ),
            })
            if has_ownership:
                tail_gates.append({
                    "id": "beam-conflict-ownership-transfer-balanced",
                    "title": "编号归属转移与总量对平",
                    "status": "pass" if balance <= 1e-9 else "fail",
                    "evidence": (
                        f"定主 {int(_number(conflict_summary.get('ownership_decided_pair_count')) or 0)} 对、"
                        f"搬移 {conflict_summary.get('attribution_transfer_m3')} m3，"
                        f"逐编号增减求和残差 {conflict_summary.get('attribution_balance_residual_m3')}"
                        f"（阈值 0）；冲突前风险 "
                        f"{conflict_summary.get('double_count_risk_m3')} m3 = 已定主 "
                        f"{conflict_summary.get('closed_double_count_risk_m3')} m3 + 剩余 "
                        f"{conflict_summary.get('residual_double_count_risk_m3')} m3"
                    ),
                    "action": "残差非 0 说明归属层改了几何总量，必须先回退再查因。",
                })
                if open_pairs:
                    tail_gates.append({
                        "id": "beam-conflict-ownership-open",
                        "title": "未定主冲突对复核心",
                        "status": "warn",
                        "evidence": (
                            f"{open_pairs} 对无法由图面证据定主，涉及 "
                            f"{conflict_summary.get('residual_double_count_risk_m3')} m3；"
                            f"逐对已给 run/模型梁编号、引线句柄与回图坐标"
                        ),
                        "action": "定主前该重叠段只按一个编号计量，两编号都进台账但不相加。",
                    })
        elif schema == WALL_EDGE_CLOSEOUT_SCHEMA:
            closeout_summary = data.get("summary") or {}
            bucket = data.get("reference_bucket_check") or {}
            component_gaps.append({
                "component": "墙身空间闭合与特殊构件",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": int(_number(
                    closeout_summary.get("unattributed_member_count")) or 0),
                "evidence": (
                    f"边缘构件轮廓合计 {_text(closeout_summary.get('edge_member_area_total_m2'))} m2，"
                    f"与墙身重叠 {_text(closeout_summary.get('wall_region_overlap_m2'))} m2，"
                    f"面域外 {_text(closeout_summary.get('outside_total_m2'))} m2 中贴墙端 "
                    f"{_text(closeout_summary.get('attached_area_m2'))} m2、"
                    f"无墙可解释 {_text(closeout_summary.get('unattributed_area_m2'))} m2，"
                    f"恒等式残差 {_text(closeout_summary.get('accounting_residual_m2'))}；"
                    f"特殊构件 {len(data.get('special_members') or [])} 个已在梁档内"
                    f"（梁类合计 {_text(bucket.get('beam_sheet_total_m3'))} m3 = 逐编号求和 "
                    f"{_text(bucket.get('beam_member_sum_m3'))} m3）"
                ),
                "blockers": [
                    f"{_text(row.get('code'))}：参考 {_text(row.get('reference_volume_m3'))} m3，"
                    f"CAD 轴长覆盖 {_text(row.get('cad_axis_coverage_ratio'))}，"
                    f"{_text(row.get('volume_status'))}"
                    for row in (data.get("special_members") or [])
                ] + [
                    f"{_text(row.get('id'))} {_text(row.get('label'))} 无墙可解释 "
                    f"{_text(row.get('unattributed_area_m2'))} m2，格 {_text(row.get('unattributed_cells'))}"
                    for row in (data.get("members") or [])
                    if _number(row.get("unattributed_area_m2")) > 0.0
                ][:12],
                "action": (
                    "墙端边缘构件外凸部分已归墙身，边缘构件不得另立体积行；"
                    "特殊构件体积含在参考梁档内，CAD 侧只登记定位证据、加量为 0。"
                ),
            })
            for gate in data.get("gates") or []:
                gates.append({
                    "id": _text(gate.get("id")),
                    "title": {
                        "wall-edge-accounting-identity": "墙身面积恒等式",
                        "wall-edge-spatial-closure": "墙身空间闭合",
                        "wall-edge-double-count-guard": "边缘构件重复计量防护",
                        "special-member-reference-containment": "特殊构件参考归属",
                        "special-member-bucket-total-identity": "梁档合计恒等式",
                    }.get(_text(gate.get("id")), "墙身与特殊构件证据"),
                    "status": _text(gate.get("status") or "warn"),
                    "evidence": _text(gate.get("evidence")),
                    "action": _text(gate.get("action")),
                })
        elif schema == SLAB_PARTITION_SCHEMA:
            part = data.get("summary") or {}
            sens = part.get("priority_sensitivity") or {}
            component_gaps.append({
                "component": "板厚子面域拆分",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": int(_number(part.get("partitioned_panel_count")) or 0),
                "evidence": (
                    f"{_text(part.get('panel_count'))} 块面板 {_text(part.get('panel_area_total_m2'))} m2 "
                    f"按 {_text(part.get('grid_step_mm'))} mm 网格拆档，证据覆盖率 "
                    f"{_text(part.get('evidence_coverage_ratio'))}，恒等式残差 "
                    f"{_text(part.get('identity_residual_m2'))} m2；整块口径 "
                    f"{_text(part.get('volume_as_assigned_total_m3'))} m3 对拆分后 "
                    f"{_text(part.get('volume_partitioned_total_m3'))} m3；"
                    f"标注优先 {_text(sens.get('label_first_volume_m3'))} m3 对图例优先 "
                    f"{_text(sens.get('fill_first_volume_m3'))} m3（摆动 "
                    f"{_text(part.get('priority_swing_m3'))} m3）；降板填充 "
                    f"{_text(part.get('elevation_only_area_m2'))} m2 只计标高不计厚"
                ),
                "blockers": [
                    f"{_text(row.get('id'))}：归档 {_text(row.get('assigned_thickness_mm'))} mm "
                    f"({_text(row.get('assigned_source'))})，{_text(row.get('area_by_grade_m2'))}"
                    for row in (data.get("panels") or []) if row.get("partition_conflict")
                ][:10],
                "action": (
                    "板厚证据链按直接标注 > 图例填充 > 说明默认三档闭合；"
                    "分档体积只用于 CAD 独立板量，报量仍按材料分账口径，两本账不得相加。"
                ),
            })
            for gate in data.get("gates") or []:
                gates.append({
                    "id": _text(gate.get("id")),
                    "title": {
                        "slab-thickness-partition-identity": "板厚分档面积恒等式",
                        "slab-thickness-evidence-closed": "板厚证据链闭合",
                        "slab-thickness-conflict-partitioned": "板厚跨档拆分",
                        "slab-elevation-only-not-thickness": "降板只计标高",
                    }.get(_text(gate.get("id")), "板厚分档证据"),
                    "status": _text(gate.get("status") or "warn"),
                    "evidence": _text(gate.get("evidence")),
                    "action": _text(gate.get("action")),
                })
        elif schema == BEAM_CENTERLINE_SCHEMA:
            cl_summary = data.get("summary") or {}
            check = data.get("overlap_cross_check") or {}
            component_gaps.append({
                "component": "梁中心线图面支撑",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": int(_number(
                    cl_summary.get("phantom_model_count")) or 0)
                + int(_number(cl_summary.get("length_gap_model_count")) or 0),
                "evidence": (
                    f"算量实例 {int(_number(cl_summary.get('run_instance_count')) or 0)} 个"
                    f"中心线支撑率 {_text(cl_summary.get('verified_run_ratio'))}；"
                    f"模型实例幻影 {int(_number(cl_summary.get('phantom_model_count')) or 0)} 个/"
                    f"{_text(cl_summary.get('phantom_model_volume_m3'))} m3、"
                    f"区间无覆盖 {int(_number(cl_summary.get('length_gap_model_count')) or 0)} 个/"
                    f"{_text(cl_summary.get('length_gap_model_volume_m3'))} m3；"
                    f"退出台账体积（模型口径）"
                    f"{_text(cl_summary.get('ledger_excluded_model_volume_m3'))} m3；"
                    f"与人工判读重叠对 "
                    f"{int(_number(check.get('agree_count')) or 0)}/"
                    f"{int(_number(check.get('pair_count')) or 0)} 一致"
                ),
                "blockers": [
                    f"{_text(row.get('id'))} {_text(row.get('code'))} 轴 "
                    f"{_text(row.get('axis_mm'))} 长 {_text(row.get('length_mm'))} mm "
                    f"{_text(row.get('centerline_status'))}"
                    for row in (data.get("instances") or [])
                    if row.get("ledger_excluded")][:12],
                "action": (
                    "幻影中心线既不扣也不加，模型实例口径整体退出分标号台账；"
                    "区间无覆盖者转梁长度与支座闭合，不得当缺几何补画。"
                ),
            })
            for gate in data.get("gates") or []:
                gates.append({
                    "id": _text(gate.get("id")),
                    "title": {
                        "centerline-support-closed": "梁中心线图面支撑",
                        "centerline-support-single-line": "梁中心线单边线",
                        "centerline-support-cross-check": "中心线判读交叉核对",
                    }.get(_text(gate.get("id")), "梁中心线证据"),
                    "status": _text(gate.get("status") or "warn"),
                    "evidence": _text(gate.get("evidence")),
                    "action": _text(gate.get("action")),
                })
        elif schema == SLAB_EVIDENCE_SCHEMA:
            ev_summary = data.get("summary") or {}
            component_gaps.append({
                "component": "板厚证据冲突",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": int(_number(
                    ev_summary.get("conflict_count")) or 0),
                "evidence": (
                    f"图例填充与归档不一致 {_text(ev_summary.get('conflict_count'))} 块 / "
                    f"{_text(ev_summary.get('conflict_area_m2'))} m2，"
                    f"体积摆动 {_text(ev_summary.get('volume_swing_m3'))} m3；"
                    f"图面直接 h= 标注 {_text(ev_summary.get('direct_h_equals_labels'))} 处、"
                    f"落回面板 {_text(ev_summary.get('direct_labels_bound_to_panel'))} 处、"
                    f"与归档一致 {_text(ev_summary.get('direct_labels_agreeing'))} 处"
                ),
                "blockers": [
                    f"{_text(row.get('id'))}：归档 {_text(row.get('assigned_thickness_mm'))} mm"
                    f" vs 图例 {'/'.join(str(v) for v in row.get('hatch_thickness_mm') or [])} mm"
                    f"，{_text(row.get('area_m2'))} m2"
                    for row in (data.get("conflicts") or [])[:10]
                ],
                "action": (
                    "总量对板厚归档不敏感，先按现口径锁总量；"
                    "要分档出量必须用 HATCH 边界做子面域拆分后再改档。"
                ),
            })
            for gate in data.get("gates") or []:
                gates.append({
                    "id": _text(gate.get("id")),
                    "title": _text(gate.get("title")),
                    "status": _text(gate.get("status") or "warn"),
                    "evidence": _text(gate.get("evidence")),
                    "action": "需要分档出量时再做子面域拆分。",
                })
        elif schema == PREFAB_BOOKLET_SCHEMA:
            book_summary = data.get("summary") or {}
            checks_total = int(_number(book_summary.get("identity_checks_total")) or 0)
            checks_passed = int(_number(book_summary.get("identity_checks_passed")) or 0)
            component_gaps.append({
                "component": "设计指标锚点与预制覆盖",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": sum(
                    1 for gate in (data.get("gates") or [])
                    if _text(gate.get("status")) != "pass")
                + (0 if checks_total == checks_passed else 1),
                "evidence": (
                    f"设计书水平构件 {_text(book_summary.get('design_plate_area_m2'))} m2/层 vs CAD "
                    f"{_text(book_summary.get('cad_plate_area_m2'))} m2"
                    f"（{_text(book_summary.get('cad_vs_design_plate_area_pct'))}%）；"
                    f"预制叠合板设计 {_text(book_summary.get('design_prefab_area_m2'))} m2、"
                    f"CAD 图面轮廓 {_text(book_summary.get('cad_prefab_outline_area_m2'))} m2、"
                    f"按编号展开 {_text(book_summary.get('cad_prefab_expanded_area_m2'))} m2"
                    f"（倍率 {book_summary.get('prefab_expansion_multiplier_design')} vs 广联达 "
                    f"{book_summary.get('prefab_expansion_multiplier_glodon')}），"
                    f"展开后仍缺 {_text(book_summary.get('prefab_area_gap_m2'))} m2 ≈ "
                    f"{_text(book_summary.get('prefab_gap_volume_at_design_thickness_m3'))} m3"),
                "blockers": [
                    _text(row.get("item")) + "：" + _text(row.get("note"))
                    for row in (data.get("comparisons") or [])
                    if _number(row.get("cad_vs_design_pct")) is not None
                    and abs(_number(row.get("cad_vs_design_pct"))) > 3.0
                ][:8],
                "action": (
                    "版本差不成立：图纸唯一版本已证，同册计算书与广联达同侧。"
                    "实例倍率已改由图面逐编号数量倍率重构并通过面积恒等式，"
                    "块数缺口见统一报告「预制底板实例展开」分档。"
                ),
            })
            for gate in data.get("gates") or []:
                gates.append({
                    "id": _text(gate.get("id")),
                    "title": _text(gate.get("title")),
                    "status": _text(gate.get("status") or "warn"),
                    "evidence": _text(gate.get("evidence")),
                    "action": _text(gate.get("action")),
                })
        elif schema == GRADE_LEDGER_SCHEMA:
            grade_summary = data.get("summary") or {}
            weak = [str(value) for value in (grade_summary.get(
                "grades_with_weak_source") or [])]
            component_gaps.append({
                "component": "混凝土分标号台账",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": sum(
                    1 for gate in (data.get("gates") or [])
                    if _text(gate.get("status")) != "pass"),
                "evidence": "分级合计 %s m3（恒等式残差 %s m3）：%s；未定 %s m3、需回图确认 %s m3" % (
                    _text(grade_summary.get("counted_total_m3")),
                    _text(grade_summary.get("identity_residual_m3")),
                    "、".join("%s=%s m3" % (key, value) for key, value in
                             sorted((data.get("by_grade") or {}).items())) or "无",
                    _text(grade_summary.get("unconfirmed_m3")),
                    _text(grade_summary.get("needs_review_m3"))),
                "blockers": [
                    "%s：%s（%s m3，来源 %s）" % (
                        _text(row.get("component")), _text(row.get("grade")),
                        _text(row.get("volume_m3")), _text(row.get("source_type")))
                    for row in (data.get("rows") or [])
                    if row.get("needs_review")
                ][:8],
                "action": (
                    "把 C40 档从层高表合并单元格改成逐层直接证据，"
                    "并给预制底板找到图面等级来源；未定与需复核量清零前不得出正式分标号量。"),
            })
            for gate in data.get("gates") or []:
                gates.append({
                    "id": _text(gate.get("id")),
                    "title": _text(gate.get("title")),
                    "status": _text(gate.get("status") or "warn"),
                    "evidence": _text(gate.get("evidence")),
                    "action": _text(gate.get("action")),
                })
        elif schema == SLAB_BIN_SCHEMA:
            bin_summary = data.get("summary") or {}
            bin_closure = dict(data.get("closure") or {})
            evidence = dict(data.get("thickness_evidence_summary") or {})
            component_gaps.append({
                "component": "板面域分层与板缝归属",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": sum(
                    1 for value in bin_closure.values() if value is False),
                "evidence": (
                    f"CAD 板面域拆成纯现浇 {_text(bin_summary.get('cad_cast_only_area_m2'))} m2、"
                    f"板缝条带 {_text(bin_summary.get('cad_seam_band_area_m2'))} m2、"
                    f"压在预制底板上 {_text(bin_summary.get('cad_on_prefab_area_m2'))} m2；"
                    f"纯现浇体积 {_text(bin_summary.get('cad_cast_only_volume_m3'))} m3"
                    f" 对广联达现浇板 "
                    f"{_text(bin_summary.get('glodon_cast_in_place_volume_m3'))} m3"
                ),
                "blockers": [
                    f"{_text(row.get('key'))}：{_text(row.get('panel_count'))} 块 / "
                    f"{_text(row.get('area_m2'))} m2"
                    for row in (data.get("thickness_evidence") or [])[:8]
                ],
                "action": (
                    "板缝条带与广联达单列板缝重叠未扣；"
                    "近半板面域板厚取自说明默认值，须按图面逐块取证后才可分档出量。"
                ),
            })
            for gate in data.get("gates") or []:
                gates.append({
                    "id": _text(gate.get("id")),
                    "title": _text(gate.get("title")),
                    "status": _text(gate.get("status") or "warn"),
                    "evidence": _text(gate.get("evidence")),
                    "action": (
                        "先补齐逐块板厚证据（尺寸标注或图例），"
                        "再把板缝条带从 CAD 现浇面域里剔除。"
                    ),
                })
        elif schema == GLB_SCOPE_SCHEMA:
            scope_summary = data.get("summary") or {}
            checks = dict(data.get("identity_checks") or {})
            prefab_double = _number(
                scope_summary.get("double_count_prefab_m3")) or 0.0
            scope_closure = dict(data.get("closure") or {})
            prefab_ratio = _round(
                scope_summary.get("prefab_over_whole_area_ratio"), 4)
            deduped = _number(scope_summary.get(
                "de_duped_reference_total_m3"))
            component_gaps.append({
                "component": "广联达口径与算量范围",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": sum(
                    1 for row in data.get("scope_buckets") or []
                    if str(row.get("cad_scope")).startswith("out-of")),
                "evidence": (
                    f"清单口径 {_text(scope_summary.get('schedule_first_floor_total_m3'))} m3；"
                    f"构件实物量 {_text(scope_summary.get('export_first_floor_total_m3'))} m3；"
                    f"勾稽残差 {_text(scope_summary.get('cross_caliber_residual_m3'))} m3；"
                    f"主体 {_text(scope_summary.get('main_structure_m3'))} m3 + "
                    f"装配式板层 {_text(scope_summary.get('assembly_slab_m3'))} m3"
                ),
                "blockers": [
                    f"{_text(row.get('bucket'))}：{_text(row.get('m3'))} m3，"
                    f"{_text(row.get('cad_scope'))}"
                    for row in data.get("scope_buckets") or []
                ],
                "scope_rows": [
                    {
                        "bucket": _text(row.get("bucket")),
                        "volume_m3": _round(row.get("m3")),
                        "cad_scope": _text(row.get("cad_scope")),
                        "in_schedule": bool(row.get("in_schedule")),
                        "note": _text(row.get("note")),
                    }
                    for row in data.get("scope_buckets") or []
                ],
                "action": (
                    "对外只报三条口径：结构主体去重量、广联达清单量、构件实物量；"
                    "二次结构、楼梯梯段与建筑零星必须标为范围外，"
                    "不得再用它们解释 CAD 缺口。"
                ),
            })
            gates.append({
                "id": "glodon-schedule-scope",
                "title": "广联达口径与算量范围",
                "status": "pass" if checks.get(
                    "cross_caliber_residual_within_tolerance") else "fail",
                "evidence": (
                    f"清单 {_text(scope_summary.get('schedule_first_floor_total_m3'))} "
                    f"对构件实物量 {_text(scope_summary.get('export_first_floor_total_m3'))}"
                    f"，口径外 "
                    f"{_text(scope_summary.get('secondary_structure_m3'))}+"
                    f"{_text(scope_summary.get('stair_m3'))}+"
                    f"{_text(scope_summary.get('building_misc_m3'))} m3 属范围外"
                ),
                "action": (
                    "按范围桶输出，范围外类别不计入本层结构混凝土。"
                ),
            })
            gates.append({
                "id": "prefab-sublayer-double-count",
                "title": "预制底板子层重复计量",
                "status": "fail" if prefab_double > 0 else "pass",
                "evidence": (
                    f"参考量把预制底板 {prefab_double:.4f} m3 叠在叠合板整厚之上，"
                    f"去重后参考应为 {_text(deduped)} m3；"
                    f"预制/整厚面积比 {_text(prefab_ratio)}"
                    f"{'，配比一致支持口径 A' if scope_closure.get('prefab-sublayer-ratio-consistent') else '，配比不支持口径 A'}"
                ),
                "action": (
                    "板体系按材料分账：现浇口径只做 CAD 对标，预制底板另立装配式台账；"
                    "去重未落进分账前不得升级正式量。"
                ),
            })
        elif schema == SLAB_OPENING_SCHEMA:
            audit_summary = data.get("summary") or {}
            review_count = int(_number(
                audit_summary.get("review_required_count")) or 0)
            ledger_closed = bool(audit_summary.get("entity_ledger_closed"))
            component_gaps.append({
                "component": "板洞口证据",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": review_count,
                "evidence": (
                    f"图层实体 "
                    f"{int(_number(audit_summary.get('source_entity_count')) or 0)} 条、"
                    f"确认洞口 {int(_number(audit_summary.get('confirmed_opening_count')) or 0)} 个/"
                    f"{_text(audit_summary.get('confirmed_opening_area_m2'))} m2、"
                    f"待复核 {review_count} 组"
                ),
                "blockers": [
                    f"{'+'.join(row.get('handles') or [])} "
                    f"{row.get('status')}：{_text(row.get('evidence'))}"
                    for row in data.get("review_records") or []
                ],
                "action": (
                    "人工确认待复核开洞图层图线的真实含义；"
                    "未成环图线一律不扣板面积。"
                ),
            })
            gates.append({
                "id": "slab-opening-evidence",
                "title": "板洞口证据",
                "status": (
                    "pass" if audit_summary.get("openings_closed")
                    else "warn" if ledger_closed else "fail"),
                "evidence": (
                    f"实体台账{'已' if ledger_closed else '未'}闭合；"
                    f"待复核 {review_count} 组；"
                    f"净板面积 {_text(audit_summary.get('net_panel_area_m2'))} m2"
                ),
                "action": (
                    "复核剩余开洞图线；确认成环后才允许升级为正式洞口扣减。"
                ),
            })
        elif schema == DEDUCTION_LEDGER_SCHEMA:
            led = data.get("summary") or {}
            tally = {row.get("rule"): row for row in (data.get("rule_tally") or [])
                     if isinstance(row, dict)}
            component_gaps.append({
                "component": "统一扣减台账",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": int(_number(led.get("aperture_unjudged_count")) or 0)
                + int(_number(led.get("aperture_review_pending_count")) or 0),
                "evidence": (
                    f"节点格 {_text(led.get('intersection_cell_count'))} 格已扣 "
                    f"{_text(led.get('node_deduction_applied_m3'))} m3、同类竖向未定归属 "
                    f"{_text(led.get('node_ownership_unresolved_m3'))} m3；开洞图线 "
                    f"{_text(led.get('aperture_record_count'))} 组：看图确认 "
                    f"{_text(led.get('aperture_user_confirmed_m3'))} m3、CAD 自证未入账 "
                    f"{_text(led.get('aperture_cad_confirmed_m3'))} m3、判非洞口 "
                    f"{int(_number(led.get('aperture_not_opening_count'))) + int(_number(led.get('aperture_explained_not_opening_count')))} 组；"
                    f"报量表洞口扣减 {_text(led.get('sheet_opening_deduction_m3'))} m3 "
                    f"对台账残差 {_text(led.get('sheet_deduction_residual_m3'))} m3；"
                    f"跨账重叠 {_text(led.get('cross_book_overlap_pair_count'))} 对"
                    f"（潜在重复扣 {_text(led.get('cross_book_double_deduct_m3'))} m3）"
                ),
                "blockers": [
                    f"{row.get('aperture_id')}×{row.get('node_id')} 重叠 "
                    f"{_text(row.get('overlap_area_m2'))} m2，潜在各扣一次 "
                    f"{_text(row.get('double_deduct_volume_m3'))} m3"
                    for row in (data.get("cross_book_overlaps") or [])[:6]
                ] + ([
                    f"CAD 自证洞口 {led.get('aperture_cad_confirmed_m3')} m3 未进报量扣减行，"
                    f"需确认参考模型板量是否已开洞"
                ] if _number(led.get("aperture_cad_confirmed_m3")) > 0 else []) + ([
                    f"同类竖向构件重叠 {led.get('node_ownership_unresolved_m3')} m3 归属未定，只审计不扣"
                ] if _number(led.get("node_ownership_unresolved_m3")) > 0 else []),
                "action": (
                    "扣减只在本台账定归属：已扣量与未入账量分列，"
                    "跨账重叠必须先定归属再扣，不得两边各扣一次。"
                ),
            })
        elif schema == PREFAB_EXPANSION_SCHEMA:
            exp = data.get("summary") or {}
            mirror = data.get("mirror_audit") or {}
            swaps = data.get("unit_area_swap_candidates") or []
            count_gap = int(_number(exp.get("model_instance_count")) or 0) - int(
                _number(exp.get("cad_owned_outline_count")) or 0)
            exp_blockers = ([
                f"{row.get('code')}：图面 {row.get('cad_outline_count')} 块、"
                f"模型 {row.get('model_count')} 块、单块面积残差 "
                f"{row.get('unit_area_residual_m2')} m2"
                for row in (data.get("component_expansion") or [])
                if _text(row.get("status")) == "unit-area-review"
            ] + ([
                f"图面块数 {exp.get('cad_owned_outline_count')} 对模型 "
                f"{exp.get('model_instance_count')}，差 {count_gap} 块；"
                "镜像已自证双侧，不能用来解释倍率，需查深化构件表"
            ] if count_gap > 0 else []))
            component_gaps.append({
                "component": "预制底板实例展开",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": count_gap,
                "evidence": (
                    f"图面 {exp.get('frame_title')}：认领 "
                    f"{_text(exp.get('cad_owned_outline_count'))} 块 / "
                    f"{_text(exp.get('cad_observed_area_m2'))} m2；外部模型 "
                    f"{_text(exp.get('model_instance_count'))} 块 / "
                    f"{_text(exp.get('model_expanded_area_m2'))} m2；"
                    f"按编号数量倍率重构 {_text(exp.get('count_ratio_expanded_area_m2'))} m2"
                    f"（残差 {_text(exp.get('expansion_area_residual_m2'))} m2）、"
                    f"块数倍率 {_text(exp.get('global_count_multiplier'))}；"
                    f"单块面积自证 {_text(exp.get('codes_unit_area_exact'))} 编号一致、"
                    f"{_text(exp.get('codes_unit_area_review'))} 编号不一致"
                    f"（互换成对 {len(swaps)} 对）；镜像配对率 "
                    f"{_text(mirror.get('paired_ratio'))}"
                ),
                "blockers": exp_blockers,
                "action": (
                    "倍率已拆到编号级数量倍率并通过面积恒等式；块数缺口只影响装配式采购台账，"
                    "现浇报量不含预制子层，该项不并入混凝土量。"
                ),
            })
        elif schema in INTERSECTION_SCHEMAS:
            audit_summary = data.get("summary") or {}
            groups = audit_summary.get("groups") or {}
            total = _number(audit_summary.get(
                "potential_deduction_volume_m3")) or 0.0
            beam_side = _number(audit_summary.get(
                "beam_side_deduction_candidate_m3")) or 0.0
            component_gaps.append({
                "component": "构件相交重复计量",
                "formal_ready": bool(data.get("formal_ready")),
                "remaining_count": int(_number(
                    audit_summary.get("overlap_count")) or 0),
                "evidence": (
                    f"潜在重复量 {total:.4f} m3；"
                    f"梁侧候选扣减 {beam_side:.4f} m3"
                ),
                "blockers": [
                    f"{row.get('pair_type')}："
                    f"{'/'.join(filter(None, row.get('codes') or [])) or '/'.join(row.get('member_ids') or [])} "
                    f"潜在 {_text(row.get('potential_deduction_volume_m3'))} m3"
                    for row in (data.get("overlaps") or [])[:5]
                ],
                "action": (
                    "确定节点混凝土归属和构件顶底标高后，"
                    "由相交引擎一次扣除重复体积；当前不自动改总量。"
                ),
            })
            gates.append({
                "id": "member-intersection-deduction",
                "title": "构件相交扣减",
                "status": "warn" if total > 0 else "pass",
                "evidence": (
                    f"{int(_number(audit_summary.get('overlap_count')) or 0)} 对重叠，"
                    f"面积 {_text(audit_summary.get('overlap_area_m2'))} m2"
                ),
                "action": (
                    "复核重叠节点归属；未确认前不得把审计体积当作正式扣减。"
                ),
            })

    component_actions: list[str] = []
    gate_counts = Counter(row["status"] for row in gates)
    partition = next((dict(data.get("summary") or {})
                      for data in supplements.values()
                      if _text(data.get("schema")) == SLAB_PARTITION_SCHEMA), None)
    if partition:
        closed = (_number(partition.get("evidence_coverage_ratio")) or 0.0) >= 0.999
        legends = [row for row in (partition.get("legend_rules") or [])
                   if isinstance(row, dict)]
        replacement = {
            "id": "slab-thickness-evidence",
            "title": "板厚证据链",
            "status": "pass" if closed else "fail",
            "evidence": "".join([
                _text(partition.get("panel_count")), " 块面板逐块定档，证据覆盖率 ",
                _text(partition.get("evidence_coverage_ratio")),
                "；三档来源全部来自图面：直接标注 ",
                _text((partition.get("area_by_evidence_m2") or {}).get("dimension-label")),
                " m2、图例填充 ",
                _text((partition.get("area_by_evidence_m2") or {}).get("legend-hatch-rule")),
                " m2（图例句句柄 ",
                "、".join(_text(row.get("handle")) for row in legends) or "无", "）",
                "、说明默认档 ",
                _text(partition.get("note_default_thickness_mm")), " mm（句柄 ",
                _text(partition.get("note_rule_handles")), "）；分档面积恒等式残差 ",
                _text(partition.get("identity_residual_m2")), " m2"]),
            "action": "分档体积进 CAD 独立板量；报量仍按材料分账口径，两本账不得相加。",
        }
        gates = [replacement if row["id"] == "slab-thickness-evidence" else row
                 for row in gates]
        gate_counts = Counter(row["status"] for row in gates)
    ledger_deduction = next((dict(data.get("summary") or {})
                             for data in supplements.values()
                             if _text(data.get("schema")) == DEDUCTION_LEDGER_SCHEMA), None)
    if ledger_deduction:
        unjudged = int(_number(ledger_deduction.get("aperture_unjudged_count")) or 0)
        pending = int(_number(ledger_deduction.get("aperture_review_pending_count")) or 0)
        unresolved = _number(ledger_deduction.get("node_ownership_unresolved_m3"))
        replacements = {
            "slab-opening-evidence": {
                "id": "slab-opening-evidence",
                "title": "板洞口证据",
                "status": "pass" if unjudged == 0 and pending == 0 else "warn",
                "evidence": (
                    f"{_text(ledger_deduction.get('aperture_record_count'))} 组开洞图线全部落归属规则："
                    f"看图确认 {_text(ledger_deduction.get('aperture_user_confirmed_m3'))} m3、"
                    f"CAD 自证 {_text(ledger_deduction.get('aperture_cad_confirmed_m3'))} m3、"
                    f"判非洞口 "
                    f"{int(_number(ledger_deduction.get('aperture_not_opening_count')) or 0) + int(_number(ledger_deduction.get('aperture_explained_not_opening_count')) or 0)} 组、"
                    f"未判定 {unjudged + pending} 组"),
                "action": "未判定图线一律不扣板面积；判定结论必须带句柄与原因入统一扣减台账。",
            },
            "member-intersection-deduction": {
                "id": "member-intersection-deduction",
                "title": "构件相交扣减",
                "status": "warn" if unresolved > 0 else "pass",
                "evidence": (
                    f"节点格 {_text(ledger_deduction.get('intersection_cell_count'))} 格按一套互斥规则归属，"
                    f"已扣 {_text(ledger_deduction.get('node_deduction_applied_m3'))} m3、"
                    f"同类竖向未定归属 {unresolved} m3（只审计不扣）"),
                "action": "竖向构件之间归属未定前不得自动扣减；跨账重叠格先定归属再扣。",
            },
        }
        gates = [replacements.get(row["id"], row) for row in gates]
        for row in (supplements.get("统一扣减") or {}).get("gates") or []:
            if _text(row.get("id")) in (
                    "deduction-applied-once-across-books",
                    "deduction-no-cross-book-double-count",
                    "deduction-slab-opening-attribution-pending"):
                gates.append({
                    "id": _text(row.get("id")),
                    "title": {"deduction-applied-once-across-books": "洞口扣减不重复入账",
                              "deduction-no-cross-book-double-count": "跨账重复扣减防护",
                              "deduction-slab-opening-attribution-pending": "CAD 自证洞口归属待定"}.get(
                                  _text(row.get("id")), "统一扣减"),
                    "status": _text(row.get("status") or "warn"),
                    "evidence": _text(row.get("evidence")),
                    "action": _text(row.get("action")),
                })
        gate_counts = Counter(row["status"] for row in gates)
    prefab_expansion = next((
        data for data in supplements.values()
        if _text(data.get("schema")) == PREFAB_EXPANSION_SCHEMA), None)
    if prefab_expansion:
        exp_gates = {_text(row.get("id")): row
                     for row in (prefab_expansion.get("gates") or [])}
        count_gate = dict(exp_gates.get("prefab-instance-count-cad-evidence") or {})
        # 原位替换旧锚点门槛：回归按列表索引展平，换位会造出假漂移
        gates = [
            {
                "id": "prefab-instance-expansion-anchor",
                "title": "预制底板展开倍率图面自证",
                "status": _text(count_gate.get("status") or "warn"),
                "evidence": _text(count_gate.get("evidence")),
                "action": _text(count_gate.get("action")),
            } if row["id"] == "prefab-instance-expansion-anchor" else row
            for row in gates
        ]
        for gate_id in ("prefab-unit-area-self-evidence",
                        "prefab-expansion-area-identity"):
            row = dict(exp_gates.get(gate_id) or {})
            if row:
                gates.append({
                    "id": gate_id,
                    "title": _text(row.get("title")),
                    "status": _text(row.get("status") or "warn"),
                    "evidence": _text(row.get("evidence")),
                    "action": _text(row.get("action")),
                })
        gate_counts = Counter(row["status"] for row in gates)
    if tail_gates:
        gates.extend(tail_gates)
        gate_counts = Counter(row["status"] for row in gates)
    grade_split = next((
        dict(data.get("summary") or {}) for data in supplements.values()
        if _text(data.get("schema")) == GRADE_LEDGER_SCHEMA
        and _number((data.get("summary") or {}).get("prefab_sublayer_input_m3"))), None)
    if grade_split:
        dedup_ok = abs(
            _number(grade_split.get("composite_whole_thickness_m3"))
            - _number(grade_split.get("composite_cast_layer_m3"))
            - _number(grade_split.get("composite_prefab_sublayer_m3"))) <= 0.001
        target = grade_split.get("slab_cast_caliber_target_m3")
        caliber_ok = target is None or abs(
            _number(grade_split.get("slab_cast_caliber_m3"))
            - _number(target)) <= 0.001
        parts = [
            "分标号台账已把叠合板整厚",
            _text(grade_split.get("composite_whole_thickness_m3")), " m3 拆成补浇层",
            _text(grade_split.get("composite_cast_layer_m3")), " m3 + 预制子层",
            _text(grade_split.get("composite_prefab_sublayer_m3")),
            " m3；现浇板+板缝+补浇层",
            _text(grade_split.get("slab_cast_caliber_m3")), " m3 = 现浇口径",
            _text(target), " m3；现浇分账合计",
            _text(grade_split.get("cast_in_place_total_m3")), " m3",
        ]
        gates = [
            {"id": "prefab-sublayer-double-count",
             "title": "预制底板子层重复计量",
             "status": "pass" if dedup_ok and caliber_ok else "fail",
             "evidence": "".join(parts),
             "action": ("报现浇混凝土量用补浇层口径；预制底板走装配式采购台账，"
                        "不得与整厚相加，也不得再按子层重复扣一次。")}
            if row["id"] == "prefab-sublayer-double-count" else row
            for row in gates]
        gate_counts = Counter(row["status"] for row in gates)

    for gap in component_gaps:
        action = _text(gap.get("action"))
        if action:
            component_actions.append(action)
        if _text(gap.get("component")) in (
                "板材料体系", "墙柱归类"):
            component_actions.extend(_text(row) for row in gap.get(
                "blockers") or [])
    next_actions = _dedupe([
        row.get("action") for row in gates
        if row.get("status") == "fail" and row.get("action")
    ] + _dedupe(component_actions))
    return {
        "gate_status_counts": dict(gate_counts),
        "gates": gates,
        "blocking_count": len(blockers),
        "blocking_groups": blocking_groups,
        "component_gaps": component_gaps,
        "next_actions": next_actions,
        "formal_ready": bool(ledger.get("formal_ready")),
    }


def _anomalies(
        model: dict[str, Any],
        ledger: dict[str, Any],
        scan: dict[str, Any],
        beam: dict[str, Any],
        beam_rows: list[dict[str, Any]],
        slab_rows: list[dict[str, Any]],
        supplements: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for issue in model.get("issues") or []:
        rows.append({
            "severity": "warning",
            "area": "model",
            "member_type": _text(issue.get("member_type")),
            "member_id": _text(issue.get("member_id")),
            "code": _text(issue.get("code")),
            "status": "model-issue",
            "message": _text(issue.get("issue")),
        })
    for row in beam_rows:
        status = _text(row.get("quantity_status"))
        if status in ("unresolved", "no-length", "no-section", "support-gap"):
            rows.append({
                "severity": "blocking",
                "area": "beam",
                "member_type": "beam",
                "member_id": _text(row.get("id")),
                "code": _text(row.get("code")),
                "status": status,
                "message": _text(row.get("issue")) or "梁几何/支座未闭合",
                "x": row.get("x"),
                "y": row.get("y"),
            })
    for row in slab_rows:
        if row.get("status") not in ("closed", "thickness-candidate"):
            rows.append({
                "severity": "warning",
                "area": "slab",
                "member_type": "slab",
                "member_id": _text(row.get("id")),
                "code": _text(row.get("code")),
                "status": _text(row.get("status")),
                "message": (
                    "板材料体系未闭合；阶段十五洞口扣减证据可见"
                    if row.get("opening_status") == "confirmed-opening"
                    else "板边界、材料体系或洞口扣减未闭合"
                ),
            })
    for gate in ledger.get("gates") or []:
        if gate.get("status") == "fail":
            rows.append({
                "severity": "blocking",
                "area": "concrete",
                "member_type": "",
                "member_id": "",
                "code": "",
                "status": _text(gate.get("id") or gate.get("title")),
                "message": (
                    f"{_text(gate.get('evidence'))}；"
                    f"{_text(gate.get('action'))}"
                ),
            })
    for note in scan.get("notes") or []:
        rows.append({
            "severity": "warning",
            "area": "scan",
            "member_type": "",
            "member_id": "",
            "code": "",
            "status": "scan-note",
            "message": _text(note),
        })
    for row in beam.get("rows") or []:
        if row.get("volume_status") in ("no-section", "no-length"):
            rows.append({
                "severity": "blocking",
                "area": "beam",
                "member_type": "beam",
                "member_id": "",
                "code": _text(row.get("code")),
                "status": _text(row.get("volume_status")),
                "message": _text(row.get("issue")),
                "x": row.get("x"),
                "y": row.get("y"),
            })
    for name, data in supplements.items():
        schema = _text(data.get("schema"))
        if schema == "cad-special-member-and-wall-attribution/v0.1":
            spatial = data.get("edge_member_spatial_attribution") or {}
            for row in spatial.get("members") or []:
                if not row.get("review_required"):
                    continue
                rows.append({
                    "severity": "blocking",
                    "area": "edge-member",
                    "member_type": "edge-member",
                    "member_id": _text(row.get("id")),
                    "code": _text(row.get("label")),
                    "status": "outside-profile",
                    "message": (
                        f"面域外 {_round(row.get('outside_area_m2')) or 0:.4f} m2"
                        f"，位置 {row.get('bbox_mm')}"
                    ),
                })
        elif schema == "cad-model-only-beam-coverage/v0.1":
            coverage = data.get("concrete_ledger") or {}
            missing = coverage.get("missing_instances") or {}
            if isinstance(missing, dict) and missing:
                rows.append({
                    "severity": "blocking",
                    "area": "beam",
                    "member_type": "beam",
                    "member_id": "",
                    "code": "",
                    "status": "missing-instances",
                    "message": _text(missing),
                })
        elif schema == "cad-beam-reference-reconciliation/v0.1":
            for row in data.get("beam_code_reconciliation") or []:
                missing = int(
                    _number(row.get("missing_equivalent_instance_count"))
                    or 0)
                if missing <= 0:
                    continue
                rows.append({
                    "severity": "blocking",
                    "area": "beam",
                    "member_type": "beam",
                    "member_id": "",
                    "code": _text(row.get("code")),
                    "status": "missing-equivalent-instance",
                    "message": (
                        f"缺少 {missing} 个等效实例；"
                        f"状态 {_text(row.get('status'))}"
                    ),
                })
            for row in (data.get("transfer_projection") or {}).get(
                    "transfers") or []:
                if row.get("applied"):
                    continue
                rows.append({
                    "severity": "warning",
                    "area": "beam",
                    "member_type": "beam",
                    "member_id": _text(row.get("run_id")),
                    "code": f"{_text(row.get('from'))}->{_text(row.get('to'))}",
                    "status": "transfer-review-only",
                    "message": _text(row.get("basis")),
                })
    unique: dict[tuple[str, ...], dict[str, Any]] = {}
    for row in rows:
        key = (
            _text(row.get("severity")),
            _text(row.get("area")),
            _text(row.get("member_id")),
            _text(row.get("code")),
            _text(row.get("status")),
            _text(row.get("message")),
        )
        unique.setdefault(key, row)
    return list(unique.values())


def build_report(
        model: dict[str, Any],
        ledger: dict[str, Any] | None = None,
        scan: dict[str, Any] | None = None,
        beam: dict[str, Any] | None = None,
        supplements: dict[str, dict[str, Any]] | None = None,
        floor_label: str = "",
        title: str = "",
        caveats: list[str] | None = None) -> dict[str, Any]:
    ledger = _normalize_ledger(ledger or {})
    scan = scan or {}
    beam = beam or {}
    supplements = supplements or {}
    component_schedule = build_component_schedule(scan, model)
    rebar_schedule = build_rebar_schedule(scan)
    column_schedule = build_column_schedule(scan, model)
    slab_schedule = build_slab_schedule(scan, model)
    beam_schedule = build_beam_schedule(model, beam)
    anomalies = _anomalies(
        model,
        ledger,
        scan,
        beam,
        beam_schedule,
        slab_schedule,
        supplements,
    )
    closure_dashboard = _closure_dashboard(ledger, supplements, anomalies)
    formal_ready = bool(ledger.get("formal_ready")) if ledger else False
    if not ledger:
        anomalies.append({
            "severity": "blocking",
            "area": "concrete",
            "member_type": "",
            "member_id": "",
            "code": "",
            "status": "ledger-missing",
            "message": "未提供混凝土分账，不能判定正式工程量",
        })
    category_counts = Counter(
        row["category"] for row in component_schedule)
    quantity_summary = dict(ledger.get("quantities") or {})
    supplement_summary = _supplement_summary(supplements)
    phase15_summary = dict(
        ((model.get("phase15") or {}).get("summary") or {}))
    reference_reconciliation = next((
        item for item in supplement_summary.values()
        if item.get("schema")
        == "cad-beam-reference-reconciliation/v0.1"
    ), None)
    direct_outputs = {
        "component_type_counts": dict(category_counts),
        "component_schedule_count": len(component_schedule),
        "column_schedule_count": len(column_schedule),
        "rebar_type_count": len(rebar_schedule),
        "slab_schedule_count": len(slab_schedule),
        "beam_schedule_count": len(beam_schedule),
        "anomaly_count": len(anomalies),
        "blocking_anomaly_count": sum(
            1 for row in anomalies if row.get("severity") == "blocking"),
        "concrete_candidate_total_m3": quantity_summary.get(
            "candidate_total_volume_m3"),
        "concrete_reference_total_m3": sum(
            _number(value) or 0.0
            for value in (ledger.get("reference_values") or {}).values()
        ) if ledger else None,
        "gate_status_counts": dict(closure_dashboard["gate_status_counts"]),
        "blocking_group_count": len(closure_dashboard["blocking_groups"]),
    }
    if reference_reconciliation:
        summary = reference_reconciliation.get("summary") or {}
        direct_outputs.update({
            "beam_reference_instance_count": int(
                _number(summary.get("reference_main_instance_count")) or 0),
            "beam_selected_equivalent_instance_count": int(
                _number(summary.get("selected_equivalent_instance_count"))
                or 0),
            "beam_missing_equivalent_instance_count": int(
                _number(summary.get("missing_equivalent_instance_count"))
                or 0),
        })
    spatial_summary = next((
        item.get("edge_member_spatial")
        for item in supplement_summary.values()
        if item.get("schema")
        == "cad-special-member-and-wall-attribution/v0.1"
    ), None)
    if spatial_summary:
        direct_outputs.update({
            "edge_member_outside_area_m2": spatial_summary.get(
                "outside_total_m2"),
            "edge_member_outside_review_count": spatial_summary.get(
                "significant_member_count"),
        })
    if phase15_summary:
        direct_outputs.update({
            "slab_phase15_gross_area_m2": _round(
                phase15_summary.get("panel_area_m2")),
            "slab_phase15_opening_count": int(
                _number(phase15_summary.get("opening_count")) or 0),
            "slab_phase15_opening_area_m2": _round(
                phase15_summary.get("opening_area_m2")),
            "slab_phase15_net_area_m2": _round(
                phase15_summary.get("net_panel_area_m2")),
            "slab_phase15_thickness_area_m2": dict(
                phase15_summary.get("thickness_area_m2") or {}),
            "slab_phase15_rough_volume_m3": _round(
                phase15_summary.get("slab_rough_volume_m3")),
        })
    concrete_detail = dict(
        (ledger.get("embedded_concrete_ledger") or {}) if ledger else {})
    beam_independent = _round(
        (_number(concrete_detail.get("main_beam_cad_m3")) or 0.0)
        + (_number(concrete_detail.get("stair_beam_cad_m3")) or 0.0))
    reference_backfill = _round(
        (_number(concrete_detail.get("coupling_beam_m3")) or 0.0)
        + (_number(concrete_detail.get("lb_reference_m3")) or 0.0)
        + (_number(concrete_detail.get("tl2_reference_m3")) or 0.0))
    if concrete_detail:
        cad_independent_core = _round(
            (beam_independent or 0.0)
            + (_number(quantity_summary.get("vertical_candidate_volume_m3"))
               or 0.0))
        cad_independent_total = _round(
            (cad_independent_core or 0.0)
            + (_number(direct_outputs.get("slab_phase15_rough_volume_m3"))
               or 0.0))
        direct_outputs.update({
            "beam_cad_independent_m3": beam_independent,
            "reference_backfill_m3": reference_backfill,
            "cad_independent_verifiable_m3": cad_independent_core,
            "cad_independent_with_slab_m3": cad_independent_total,
            "cad_independent_ratio_of_candidate": (
                round((cad_independent_total or 0.0)
                      / (direct_outputs.get("concrete_candidate_total_m3")
                         or 1.0), 6)
                if direct_outputs.get("concrete_candidate_total_m3")
                else None),
        })
    thickness_audit = next((
        item for item in supplement_summary.values()
        if _text(item.get("schema")) == SLAB_EVIDENCE_SCHEMA
    ), None)
    if thickness_audit:
        ev_summary = thickness_audit.get("summary") or {}
        direct_count = int(_number(
            ev_summary.get("direct_h_equals_labels")) or 0)
        direct_bound = int(_number(
            ev_summary.get("direct_labels_bound_to_panel")) or 0)
        direct_ok = int(_number(
            ev_summary.get("direct_labels_agreeing")) or 0)
        direct_unbound = max(0, direct_count - direct_bound)
        direct_mismatch = max(0, direct_bound - direct_ok)
        direct_weak = direct_unbound + direct_mismatch
        direct_strong = direct_ok
        direct_outputs.update({
            "slab_thickness_conflict_count": int(_number(
                ev_summary.get("conflict_count")) or 0),
            "slab_thickness_conflict_area_m2": _round(
                ev_summary.get("conflict_area_m2")),
            "slab_thickness_conflict_area_ratio": _round(
                ev_summary.get("conflict_area_ratio"), 4),
            "slab_thickness_volume_swing_m3": _round(
                ev_summary.get("volume_swing_m3")),
            "slab_thickness_direct_labels_total": int(_number(
                ev_summary.get("direct_h_equals_labels")) or 0),
            "slab_thickness_direct_labels_bound": int(_number(
                ev_summary.get("direct_labels_bound_to_panel")) or 0),
            "slab_thickness_direct_labels_agreeing": int(_number(
                ev_summary.get("direct_labels_agreeing")) or 0),
        })
    grade_ledger = next((
        item for item in supplement_summary.values()
        if _text(item.get("schema")) == GRADE_LEDGER_SCHEMA
    ), None)
    if grade_ledger:
        grade_summary = grade_ledger.get("summary") or {}

        def _grade_slug(grade: str) -> str:
            text = _text(grade).strip().upper()
            return "unknown" if text in ("", "未定") else text.replace("/", "_")

        direct_outputs.update({
            "grade_ledger_total_m3": _round(grade_summary.get("counted_total_m3")),
            "grade_ledger_row_count": int(_number(
                grade_summary.get("row_count")) or 0),
            "grade_ledger_identity_residual_m3": _round(
                grade_summary.get("identity_residual_m3")),
            "grade_ledger_excluded_sublayer_m3": _round(
                grade_summary.get("excluded_sublayer_m3")),
            "grade_ledger_unconfirmed_m3": _round(
                grade_summary.get("unconfirmed_m3")),
            "grade_ledger_needs_review_m3": _round(
                grade_summary.get("needs_review_m3")),
            "grade_ledger_needs_review_ratio": _round(
                grade_summary.get("needs_review_ratio"), 4),
        })
        for grade, volume in sorted((grade_ledger.get("by_grade") or {}).items()):
            direct_outputs["grade_volume_%s_m3" % _grade_slug(grade)] = _round(volume)
        direct_outputs["grade_joint_zone_m3"] = round(sum(
            _number(row.get("volume_m3")) or 0.0
            for row in (grade_ledger.get("rows") or [])
            if _text(row.get("member_group")) == "joint-zone"), 4)
    slab_bin_audit = next((
        item for item in supplement_summary.values()
        if _text(item.get("schema")) == SLAB_BIN_SCHEMA
    ), None)
    prefab_booklet = next((
        item for item in supplement_summary.values()
        if _text(item.get("schema")) == PREFAB_BOOKLET_SCHEMA
    ), None)
    if prefab_booklet:
        book_summary = prefab_booklet.get("summary") or {}
        book_facts = prefab_booklet.get("design_facts") or {}
        direct_outputs.update({
            "design_plate_area_anchor_m2": _round(book_summary.get("design_plate_area_m2")),
            "design_prefab_area_anchor_m2": _round(book_summary.get("design_prefab_area_m2")),
            "cad_prefab_outline_area_m2": _round(book_summary.get("cad_prefab_outline_area_m2")),
            "cad_prefab_expanded_area_m2": _round(
                book_summary.get("cad_prefab_expanded_area_m2")),
            "prefab_expansion_multiplier_design": _round(
                book_summary.get("prefab_expansion_multiplier_design")),
            "prefab_expansion_multiplier_glodon": _round(
                book_summary.get("prefab_expansion_multiplier_glodon")),
            "cad_vs_design_plate_area_pct": _round(
                book_summary.get("cad_vs_design_plate_area_pct"), 2),
            "cad_vs_design_prefab_area_pct": _round(
                book_summary.get("cad_vs_design_prefab_area_pct"), 2),
            "prefab_area_gap_vs_design_m2": _round(book_summary.get("prefab_area_gap_m2")),
            "prefab_gap_volume_at_design_thickness_m3": _round(
                book_summary.get("prefab_gap_volume_at_design_thickness_m3")),
            "design_slab_thickness_mm": _number(
                book_facts.get("design_composite_slab_thickness_mm")),
            "design_beam_and_wall_width_mm": _number(
                book_facts.get("design_vertical_and_beam_width_mm")),
            "design_composite_seam_width_mm": _number(
                book_facts.get("design_composite_seam_width_mm")),
            "design_precast_wall_bottom_level_m": _number(
                book_facts.get("design_precast_wall_from_m")),
            "design_vertical_volume_std_floor_m3": _round(
                book_facts.get("design_std_vertical_volume_m3")),
            "design_vertical_area_std_floor_m2": _round(
                book_facts.get("design_std_vertical_area_m2")),
            "design_assembly_ratio_pct": _number(book_facts.get("design_assembly_ratio_pct")),
            "drawing_version_copies_identical": bool(
                book_summary.get("drawing_copies_identical")),
            "design_agrees_with_glodon_prefab_area": bool(
                book_summary.get("design_agrees_with_glodon")),
            "prefab_label_probe_window_note": "邻域窗口含相邻图框，只作实例复核线索",
            "prefab_frame_label_count": int(_number(
                (prefab_booklet.get("frame_label_probe") or {}).get("labels")) or 0),
            "prefab_frame_ring_count": int(_number(
                (prefab_booklet.get("frame_label_probe") or {}).get("rings")) or 0),
            "prefab_frame_w_series_label_count": int(_number(
                (prefab_booklet.get("frame_label_probe") or {}).get("w_series_labels")) or 0),
            "prefab_booklet_identity_checks": "%d/%d" % (
                int(_number(book_summary.get("identity_checks_passed")) or 0),
                int(_number(book_summary.get("identity_checks_total")) or 0)),
        })
    prefab_expansion_item = next((
        item for item in supplement_summary.values()
        if _text(item.get("schema")) == PREFAB_EXPANSION_SCHEMA
    ), None)
    if prefab_expansion_item:
        exp = prefab_expansion_item.get("summary") or {}
        mirror = prefab_expansion_item.get("mirror_audit") or {}
        count_gap = int(_number(exp.get("model_instance_count")) or 0) - int(
            _number(exp.get("cad_owned_outline_count")) or 0)
        direct_outputs.update({
            "prefab_frame_title": _text(exp.get("frame_title")),
            "prefab_frame_outline_count": int(_number(exp.get("cad_outline_count")) or 0),
            "prefab_cad_owned_count": int(_number(exp.get("cad_owned_outline_count")) or 0),
            "prefab_cad_observed_area_m2": _round(exp.get("cad_observed_area_m2")),
            "prefab_model_instance_count": int(_number(exp.get("model_instance_count")) or 0),
            "prefab_model_expanded_area_m2": _round(exp.get("model_expanded_area_m2")),
            "prefab_count_ratio_expanded_area_m2": _round(
                exp.get("count_ratio_expanded_area_m2")),
            "prefab_expansion_area_residual_m2": _round(
                exp.get("expansion_area_residual_m2")),
            "prefab_count_multiplier": _round(exp.get("global_count_multiplier")),
            "prefab_area_multiplier": _round(exp.get("global_area_multiplier")),
            "prefab_unit_area_exact_codes": int(_number(exp.get("codes_unit_area_exact")) or 0),
            "prefab_unit_area_review_codes": int(
                _number(exp.get("codes_unit_area_review")) or 0),
            "prefab_unit_area_swap_pairs": len(
                prefab_expansion_item.get("unit_area_swap_candidates") or []),
            "prefab_instance_count_gap": count_gap,
            "prefab_mirror_paired_ratio": _round(mirror.get("paired_ratio"), 4),
            "prefab_mirror_explains_doubling": bool(mirror.get("explains_doubling")),
            "prefab_cast_in_place_impact_m3": 0.0,
        })
    if slab_bin_audit:
        bin_summary = slab_bin_audit.get("summary") or {}
        evidence = slab_bin_audit.get("thickness_evidence_summary") or {}
        direct_outputs.update({
            "slab_cast_only_area_m2": _round(bin_summary.get(
                "cad_cast_only_area_m2")),
            "slab_seam_band_area_m2": _round(bin_summary.get(
                "cad_seam_band_area_m2")),
            "slab_on_prefab_area_m2": _round(bin_summary.get(
                "cad_on_prefab_area_m2")),
            "slab_cast_only_volume_m3": _round(bin_summary.get(
                "cad_cast_only_volume_m3")),
            "slab_seam_band_volume_m3": _round(bin_summary.get(
                "cad_seam_band_volume_m3")),
            "slab_seam_band_vs_glodon_seam_ratio": _round(
                bin_summary.get("seam_band_inside_cast_ratio"), 4),
            "slab_cast_volume_minus_glodon_m3": _round(
                bin_summary.get("cast_only_minus_glodon_cast_volume_m3")),
            "slab_thickness_default_note_area_m2": _round(
                evidence.get("default_note_area_m2")),
            "slab_thickness_default_note_area_ratio": _round(
                evidence.get("default_note_area_ratio"), 4),
            "slab_thickness_direct_label_area_m2": _round(
                evidence.get("direct_label_area_m2")),
        })
    scope_audit = next((
        item for item in supplement_summary.values()
        if _text(item.get("schema")) == GLB_SCOPE_SCHEMA
    ), None)
    if scope_audit:
        scope_summary = scope_audit.get("summary") or {}
        direct_outputs.update({
            "glodon_schedule_total_m3": _round(
                scope_summary.get("schedule_first_floor_total_m3")),
            "glodon_component_export_total_m3": _round(
                scope_summary.get("export_first_floor_total_m3")),
            "glodon_main_structure_scope_m3": _round(
                scope_summary.get("main_structure_m3")),
            "glodon_assembly_slab_scope_m3": _round(
                scope_summary.get("assembly_slab_m3")),
            "glodon_prefab_sublayer_double_count_m3": _round(
                scope_summary.get("double_count_prefab_m3")),
            "glodon_reference_deduped_total_m3": _round(
                scope_summary.get("de_duped_reference_total_m3")),
            "glodon_secondary_structure_m3": _round(
                scope_summary.get("secondary_structure_m3")),
            "glodon_stair_flight_m3": _round(scope_summary.get("stair_m3")),
            "glodon_building_misc_m3": _round(
                scope_summary.get("building_misc_m3")),
            "glodon_cross_caliber_residual_m3": _round(
                scope_summary.get("cross_caliber_residual_m3")),
            "slab_cast_in_place_caliber_a_m3": _round(
                scope_summary.get("slab_cast_in_place_caliber_A_m3")),
            "glodon_prefab_over_whole_area_ratio": _round(
                scope_summary.get("prefab_over_whole_area_ratio")),
            "glodon_prefab_mean_block_area_m2": _round(
                scope_summary.get("prefab_mean_block_area_m2")),
            "glodon_whole_mean_block_area_m2": _round(
                scope_summary.get("whole_mean_block_area_m2")),
            "slab_caliber_a_total_m3": _round(
                scope_summary.get("slab_caliber_A_total_m3")),
            "cad_slab_vs_caliber_a_diff_m3": _round(
                scope_summary.get("cad_vs_slab_caliber_A_diff_m3")),
        })
    intersection_audit = next((
        item for item in supplement_summary.values()
        if _text(item.get("schema")) in INTERSECTION_SCHEMAS
    ), None)
    if intersection_audit:
        summary = intersection_audit.get("summary") or {}
        direct_outputs.update({
            "intersection_overlap_count": int(_number(
                summary.get("overlap_count")) or 0),
            "intersection_overlap_area_m2": _round(
                summary.get("overlap_area_m2")),
            "intersection_potential_deduction_volume_m3": _round(
                summary.get("potential_deduction_volume_m3")),
            "intersection_unique_overlap_cell_count": int(_number(
                summary.get("unique_overlap_cell_count")) or 0),
            "intersection_pairwise_potential_volume_m3": _round(
                summary.get("pairwise_potential_deduction_volume_m3")),
            "intersection_deduplication_overcount_m3": _round(
                summary.get("deduplication_overcount_m3")),
            "intersection_beam_side_candidate_m3": _round(
                summary.get("beam_side_deduction_candidate_m3")),
            "intersection_applied_net_deduction_m3": _round(
                (intersection_audit.get("net_quantity") or {}).get(
                    "applied_deduction_m3")),
            "intersection_candidate_net_total_m3": _round(
                (intersection_audit.get("net_quantity") or {}).get(
                    "candidate_total_after_beam_deduction_m3")),
            "intersection_audit_applied": bool(
                (intersection_audit.get("closure") or {}).get(
                    "applied_to_formal_quantity")),
        })
    beam_gap_audit = next((
        item for item in supplement_summary.values()
        if _text(item.get("schema")) == BEAM_GAP_SCHEMA
    ), None)
    if beam_gap_audit:
        audit_summary = beam_gap_audit.get("summary") or {}
        decomposition = audit_summary.get("gap_decomposition") or {}
        direct_outputs.update({
            "beam_code_count": int(_number(
                audit_summary.get("code_count")) or 0),
            "beam_volume_under_code_count": int(_number(
                audit_summary.get("volume_under_code_count")) or 0),
            "beam_volume_over_code_count": int(_number(
                audit_summary.get("volume_over_code_count")) or 0),
            "beam_under_total_m3": _round(audit_summary.get("under_total_m3")),
            "beam_over_total_m3": _round(audit_summary.get("over_total_m3")),
            "beam_reattribution_capacity_m3": _round(
                audit_summary.get("reattribution_capacity_m3")),
            "beam_net_unlocated_m3": _round(
                audit_summary.get("main_beam_net_unlocated_m3")),
            "beam_unassigned_run_volume_m3": _round(
                audit_summary.get("unassigned_run_volume_m3")),
            "beam_residual_needing_new_geometry_m3": _round(
                audit_summary.get("residual_needing_new_geometry_m3")),
            "beam_missing_instance_count": int(_number(
                audit_summary.get("missing_instance_count")) or 0),
            "beam_volume_explained_instance_count": int(_number(
                audit_summary.get(
                    "volume_explained_missing_instance_count")) or 0),
            "beam_count_only_instance_gap": int(_number(
                audit_summary.get("count_only_missing_instance_count")) or 0),
            "beam_gap_decomposition_sum_m3": _round(
                decomposition.get("sum_difference_m3")),
            "beam_gap_decomposition_matches_ledger": bool(
                decomposition.get("matches_ledger")),
        })
    beam_coverage_audit = next((
        item for item in supplement_summary.values()
        if _text(item.get("schema")) == BEAM_COVERAGE_SCHEMA
    ), None)
    if beam_coverage_audit:
        audit_summary = beam_coverage_audit.get("summary") or {}
        direct_outputs.update({
            "beam_in_frame_coverage_ratio": _round(
                audit_summary.get("in_frame_coverage_ratio"), 6),
            "beam_in_frame_length_mm": _round(
                audit_summary.get("in_frame_length_mm"), 1),
            "beam_uncovered_in_frame_length_mm": _round(
                audit_summary.get("uncovered_in_frame_length_mm"), 1),
            "beam_uncovered_in_frame_count": int(_number(
                audit_summary.get("uncovered_in_frame_count")) or 0),
            "beam_partial_covered_count": int(_number(
                audit_summary.get("partial_covered_segment_count")) or 0),
            "beam_candidate_in_frame_count": int(_number(
                audit_summary.get("candidate_beam_in_frame_count")) or 0),
            "beam_candidate_in_frame_volume_m3": _round(
                audit_summary.get("candidate_volume_in_frame_m3")),
            "beam_candidate_window_out_volume_m3": _round(
                audit_summary.get("candidate_volume_window_out_m3")),
            "beam_candidate_beyond_plan_volume_m3": _round(
                audit_summary.get("candidate_volume_beyond_plan_m3")),
            "beam_duplicate_view_offset_mm": _round(
                audit_summary.get("duplicate_view_offset_mm"), 1),
            "beam_duplicate_view_count": int(_number(
                audit_summary.get("duplicate_view_line_count")) or 0),
            "beam_mirrored_view_count": int(_number(
                audit_summary.get("mirrored_line_count")) or 0),
            "beam_mirror_pair_volume_m3": _round(
                audit_summary.get("candidate_volume_mirror_pair_m3")),
            "beam_mirror_pair_countable": bool(
                audit_summary.get("mirror_pair_countable")),
            "beam_translated_view_volume_m3": _round(
                audit_summary.get("candidate_volume_translated_view_m3")),
            "beam_residual_still_unexplained_m3": _round(
                audit_summary.get("residual_still_unexplained_m3")),
            "beam_coverage_closed": bool(audit_summary.get("coverage_closed")),
        })
    beam_attribution = next((
        item for item in supplement_summary.values()
        if _text(item.get("schema")) == BEAM_ATTRIBUTION_SCHEMA
    ), None)
    if beam_attribution:
        attr_summary = beam_attribution.get("summary") or {}
        attr_decomposition = beam_attribution.get("residual_decomposition") or {}
        attr_targets = beam_attribution.get("under_code_targets") or {}
        direct_outputs.update({
            "beam_section_caliber_delta_m3": _round(
                attr_summary.get("section_caliber_delta_m3")),
            "beam_section_mismatch_run_count": int(_number(
                attr_summary.get("run_section_mismatch_count")) or 0),
            "beam_candidate_attached_m3": _round(
                attr_summary.get("attached_to_existing_code_m3")),
            "beam_candidate_unattached_m3": _round(
                attr_summary.get("unattached_candidate_m3")),
            "beam_unexplained_in_frame_m3": _round(
                attr_summary.get("unexplained_by_this_frame_m3")),
            "beam_unattached_length_mm": _round(
                attr_decomposition.get("unattached_length_mm"), 1),
            "beam_decomposition_identity_closed": bool(
                attr_decomposition.get("matches_identity")),
            "beam_cross_frame_code_count": int(_number(
                attr_targets.get("cross_frame_code_count")) or 0),
            "beam_cross_frame_needed_length_mm": _round(
                attr_targets.get("cross_frame_needed_length_mm"), 1),
        })
    frame_index_audit = next((
        item for item in supplement_summary.values()
        if _text(item.get("schema")) == BEAM_FRAME_INDEX_SCHEMA
    ), None)
    if frame_index_audit:
        index_summary = frame_index_audit.get("summary") or {}
        index_counts = dict(index_summary.get("classification_counts") or {})
        direct_outputs.update({
            "beam_frame_count": int(_number(
                index_summary.get("frame_count")) or 0),
            "beam_frame_label_count": int(_number(
                index_summary.get("label_count")) or 0),
            "beam_target_frame_under_code_count": int(_number(
                index_summary.get("under_code_count")) or 0),
            "beam_length_not_closed_code_count": int(_number(
                index_counts.get("length-not-closed-in-same-beam")) or 0),
            "beam_length_not_closed_volume_m3": _round(
                index_summary.get("length_closure_volume_m3")),
            "beam_other_frame_label_volume_m3": _round(
                index_summary.get("cross_floor_label_only_volume_m3")),
            "beam_no_label_in_target_frame_count": int(_number(
                index_counts.get("no-label-in-target-frame")) or 0),
        })
    span_closure_audit = next((
        item for item in supplement_summary.values()
        if _text(item.get("schema")) == BEAM_SPAN_CLOSURE_SCHEMA
    ), None)
    if span_closure_audit:
        closure_summary = span_closure_audit.get("summary") or {}
        direct_outputs.update({
            "beam_centerline_length_mm": _round(
                closure_summary.get("centerline_length_mm"), 1),
            "beam_clear_length_mm": _round(
                closure_summary.get("clear_length_mm"), 1),
            "beam_support_deduction_length_mm": _round(
                closure_summary.get("support_deduction_length_mm"), 1),
            "beam_gross_volume_m3": _round(closure_summary.get("gross_volume_m3")),
            "beam_clear_span_volume_m3": _round(
                closure_summary.get("clear_volume_m3")),
            "beam_span_caliber_difference_m3": _round(
                closure_summary.get("span_caliber_difference_m3")),
            "beam_span_vs_intersection_conflict_m3": _round(
                closure_summary.get("span_caliber_vs_intersection_conflict_m3")),
            "beam_deficit_caliber_volume_m3": _round(
                closure_summary.get("support_deduction_caliber_volume_m3")),
            "beam_deficit_needs_geometry_m3": _round(
                closure_summary.get("needs_new_geometry_volume_m3")),
            "beam_chain_lost_volume_m3": _round(
                closure_summary.get("chain_lost_volume_m3")),
            "beam_verdict_total_m3": _round(
                closure_summary.get("verdict_total_m3")),
            "beam_inferred_end_width_mm": _round(
                closure_summary.get("inferred_end_support_width_mm"), 1),
        })
    multispan_audit = next((
        item for item in supplement_summary.values()
        if _text(item.get("schema")) == BEAM_MULTISPAN_SCHEMA
    ), None)
    if multispan_audit:
        multi_summary = multispan_audit.get("summary") or {}
        direct_outputs.update({
            "beam_multispan_beam_count": int(_number(
                multi_summary.get("multispan_beam_count")) or 0),
            "beam_multispan_continued_count": int(_number(
                multi_summary.get("continued_beam_count")) or 0),
            "beam_multispan_added_axis_length_mm": _round(
                multi_summary.get("added_axis_length_mm"), 1),
            "beam_multispan_candidate_volume_m3": _round(
                multi_summary.get("added_volume_candidate_m3")),
            "beam_multispan_deficit_before_mm": _round(
                multi_summary.get("deficit_before_mm"), 1),
            "beam_multispan_deficit_after_mm": _round(
                multi_summary.get("deficit_after_mm"), 1),
            "beam_multispan_deficit_closed_ratio": _round(
                multi_summary.get("deficit_closed_ratio"), 4),
            "beam_multispan_applied_to_formal": bool(
                (multispan_audit.get("closure") or {}).get("gates", {})
                .get("applied-to-formal-quantity")),
        })
    dedup_audit = next((
        item for item in supplement_summary.values()
        if _text(item.get("schema")) == BEAM_DEDUP_SCHEMA
    ), None)
    if dedup_audit:
        dedup_summary = dedup_audit.get("summary") or {}
        dedup_class = dict(dedup_summary.get("beam_only_class_count") or {})
        dedup_class_volume = dict(
            dedup_summary.get("beam_only_class_volume_m3") or {})
        dedup_verdict = dict(
            dedup_summary.get("unpaired_run_verdict_volume_m3") or {})
        direct_outputs.update({
            "beam_dedup_matched_beam_count": int(_number(
                dedup_summary.get("matched_beam_count")) or 0),
            "beam_dedup_beam_only_count": int(_number(
                dedup_summary.get("beam_only_count")) or 0),
            "beam_dedup_double_count_volume_m3": _round(
                dedup_summary.get("double_count_volume_m3")),
            "beam_dedup_net_new_volume_m3": _round(
                dedup_summary.get("model_beam_net_new_volume_m3")),
            "beam_dedup_conflict_beam_count": int(_number(
                dedup_class.get("attribution-conflict")) or 0),
            "beam_dedup_conflict_beam_volume_m3": _round(
                dedup_class_volume.get("attribution-conflict")),
            "beam_dedup_code_absent_volume_m3": _round(
                dedup_class_volume.get("code-absent")),
            "beam_dedup_unpaired_run_count": int(_number(
                dedup_summary.get("unmatched_run_count")) or 0),
            "beam_dedup_unpaired_run_volume_m3": _round(
                dedup_summary.get("unmatched_run_volume_m3")),
            "beam_dedup_missing_instance_volume_m3": _round(
                dedup_verdict.get("model-missing-instance")),
            "beam_dedup_continuation_volume_m3": _round(
                dedup_verdict.get("continuation-candidate")),
            "beam_dedup_run_self_overlap_pairs": int(_number(
                dedup_summary.get("run_self_overlap_pair_count")) or 0),
            "beam_dedup_run_self_overlap_volume_m3": _round(
                dedup_summary.get("run_self_overlap_volume_m3")),
            "beam_dedup_applied_to_formal": False,
        })
    conflict_audit = next((
        item for item in supplement_summary.values()
        if _text(item.get("schema")) == BEAM_CONFLICT_SCHEMA
    ), None)
    if conflict_audit:
        conflict_summary = conflict_audit.get("summary") or {}
        conflict_verdicts = dict(conflict_summary.get("verdicts") or {})
        if "ownership_decided_pair_count" in conflict_summary:
            direct_outputs.update({
                "beam_conflict_owner_decided_pairs": int(_number(
                    conflict_summary.get("ownership_decided_pair_count")) or 0),
                "beam_conflict_open_pairs": int(_number(
                    conflict_summary.get("ownership_open_pair_count")) or 0),
                "beam_conflict_separate_line_pairs": int(_number((
                    conflict_summary.get("ownership_status_counts") or {}).get(
                        "resolved-separate-lines")) or 0),
                "beam_conflict_attribution_transfer_m3": _round(
                    conflict_summary.get("attribution_transfer_m3")),
                "beam_conflict_transfer_balance_m3": _round(
                    conflict_summary.get("attribution_balance_residual_m3"), 6),
                "beam_conflict_closed_risk_m3": _round(
                    conflict_summary.get("closed_double_count_risk_m3")),
                "beam_conflict_residual_risk_m3": _round(
                    conflict_summary.get("residual_double_count_risk_m3")),
                "beam_conflict_shift_codes": len(
                    conflict_summary.get("code_attribution_shift") or []),
            })
        direct_outputs.update({
            "beam_conflict_pair_count": int(_number(
                conflict_summary.get("conflict_pair_count")) or 0),
            "beam_conflict_run_count": int(_number(
                conflict_summary.get("conflict_run_count")) or 0),
            "beam_conflict_beam_count": int(_number(
                conflict_summary.get("conflict_beam_count")) or 0),
            "beam_conflict_same_axis_pair_count": int(_number(
                conflict_summary.get("same_axis_pair_count")) or 0),
            "beam_conflict_same_line_pair_count": int(_number(
                conflict_summary.get("same_line_pair_count")) or 0),
            "beam_conflict_parallel_pair_count": int(_number(
                conflict_summary.get("parallel_pair_count")) or 0),
            "beam_conflict_span_split_pairs": int(_number(
                (conflict_verdicts.get("same-line-different-spans") or {}).get(
                    "pair_count")) or 0),
            "beam_conflict_double_count_risk_m3": _round(
                conflict_summary.get("double_count_risk_m3")),
            "beam_conflict_run_holds_pairs": int(_number(
                (conflict_verdicts.get("run-label-holds") or {}).get(
                    "pair_count")) or 0),
            "beam_conflict_beam_holds_pairs": int(_number(
                (conflict_verdicts.get("beam-label-holds") or {}).get(
                    "pair_count")) or 0),
            "beam_conflict_dual_label_pairs": int(_number(
                (conflict_verdicts.get("dual-label-same-line") or {}).get(
                    "pair_count")) or 0),
            "beam_conflict_no_label_pairs": int(_number(
                (conflict_verdicts.get("no-label-evidence") or {}).get(
                    "pair_count")) or 0),
            "beam_conflict_label_confidence": dict(
                conflict_summary.get("label_confidence_counts") or {}),
            "beam_conflict_applied_to_formal": False,
        })
    slab_opening_audit = next((
        item for item in supplement_summary.values()
        if _text(item.get("schema")) == SLAB_OPENING_SCHEMA
    ), None)
    if slab_opening_audit:
        audit_summary = slab_opening_audit.get("summary") or {}
        direct_outputs.update({
            "slab_opening_entity_count": int(_number(
                audit_summary.get("source_entity_count")) or 0),
            "slab_opening_entity_ledger_closed": bool(
                audit_summary.get("entity_ledger_closed")),
            "slab_opening_confirmed_count": int(_number(
                audit_summary.get("confirmed_opening_count")) or 0),
            "slab_opening_confirmed_area_m2": _round(
                audit_summary.get("confirmed_opening_area_m2")),
            "slab_opening_annotation_count": int(_number(
                audit_summary.get("annotation_record_count")) or 0),
            "slab_opening_review_count": int(_number(
                audit_summary.get("review_required_count")) or 0),
            "slab_opening_review_area_upper_bound_m2": _round(
                audit_summary.get(
                    "review_envelope_area_upper_bound_m2")),
            "slab_opening_review_volume_upper_bound_m3": _round(
                audit_summary.get("review_volume_upper_bound_m3")),
            "slab_opening_prior_candidate_count": int(_number(
                audit_summary.get("prior_candidate_panel_count")) or 0),
            "slab_opening_prior_explained_count": int(_number(
                audit_summary.get("prior_candidate_explained_panel_count"))
                or 0),
            "slab_opening_gross_area_m2": _round(
                audit_summary.get("gross_panel_area_m2")),
            "slab_opening_net_area_m2": _round(
                audit_summary.get("net_panel_area_m2")),
            "slab_openings_closed": bool(audit_summary.get("openings_closed")),
        })
    deduction_ledger = next((item for item in supplement_summary.values()
                             if _text(item.get("schema")) == DEDUCTION_LEDGER_SCHEMA), None)
    if deduction_ledger:
        led = deduction_ledger.get("summary") or {}
        direct_outputs.update({
            "deduction_node_cell_count": int(_number(
                led.get("intersection_cell_count")) or 0),
            "deduction_node_applied_m3": _round(led.get("node_deduction_applied_m3")),
            "deduction_node_unresolved_m3": _round(
                led.get("node_ownership_unresolved_m3")),
            "deduction_aperture_user_confirmed_m3": _round(
                led.get("aperture_user_confirmed_m3")),
            "deduction_aperture_cad_confirmed_m3": _round(
                led.get("aperture_cad_confirmed_m3")),
            "deduction_aperture_unjudged_count": int(_number(
                led.get("aperture_unjudged_count")) or 0),
            "deduction_sheet_residual_m3": _round(led.get("sheet_deduction_residual_m3")),
            "deduction_cross_book_double_deduct_m3": _round(
                led.get("cross_book_double_deduct_m3")),
            "deduction_total_candidate_m3": _round(
                led.get("total_deduction_candidate_m3")),
        })
    return {
        "schema": SCHEMA,
        "title": title or "CAD 结构算量统一报告",
        "floor_label": floor_label or _text(
            (model.get("floor") or {}).get("label")),
        "caveats": [_text(row) for row in (caveats or []) if _text(row)],
        "formal_ready": formal_ready,
        "readiness": {
            "formal_ready": formal_ready,
            "candidate_only": not formal_ready,
            "blocking_count": direct_outputs["blocking_anomaly_count"],
            "status": (
                "formal-ready" if formal_ready
                else "candidate-only"
            ),
        },
        "source_schemas": {
            "model": _text(model.get("schema")),
            "ledger": _text(ledger.get("schema")),
            "scan": "cad-scan",
            "beam_objects": _text(
                (beam.get("run_registry") or {}).get("schema")
                or "cad-beam-objects"),
        },
        "direct_outputs": direct_outputs,
        "specifications": dict(scan.get("spec") or {}),
        "component_schedule": component_schedule,
        "column_schedule": column_schedule,
        "rebar_schedule": rebar_schedule,
        "slab_schedule": slab_schedule,
        "beam_schedule": beam_schedule,
        "concrete": {
            "reference_values": dict(ledger.get("reference_values") or {}),
            "quantities": quantity_summary,
            "comparisons": list(ledger.get("comparisons") or []),
            "gate_summary": dict(ledger.get("gate_summary") or {}),
            "gates": list(ledger.get("gates") or []),
        },
        "closure_dashboard": closure_dashboard,
        "supplemental_breakdown": supplement_summary,
        "anomalies": anomalies,
        "status": (
            "统一报告；正式工程量门槛已通过"
            if formal_ready
            else "统一报告；仅输出图纸数据和研发对账候选，不输出正式工程量"
        ),
    }


def _md_cell(value: Any) -> str:
    return _text(value).replace("|", "\\|").replace("\n", " ")


def _pct(ratio: Any) -> str:
    value = _number(ratio)
    return "-" if value is None or _number(ratio) == 0.0 else "%.1f%%" % (value * 100.0)


def summary_int(source: dict[str, Any], key: str) -> int:
    return int(_number(source.get(key)) or 0)


def render_markdown(report: dict[str, Any]) -> str:
    direct = report.get("direct_outputs") or {}
    lines = [
        f"# {report.get('title') or 'CAD 结构算量统一报告'}",
        "",
        "## 结论",
        "",
        f"- 图纸/楼层：`{report.get('floor_label') or '-'}`。",
        f"- `formal_ready`：`{str(report.get('formal_ready')).lower()}`。",
        f"- 阻塞项：`{direct.get('blocking_anomaly_count', 0)}`。",
        "- 本报告合并构件规格、钢筋型号、柱表候选、板表、梁净跨状态和混凝土分账；"
        "未通过正式门槛的数据只作研发对账。",
        "",
        "## 直接可读数据",
        "",
        "| 数据 | 数量/值 |",
        "|---|---:|",
        f"| 构件规格记录 | {direct.get('component_schedule_count', 0)} |",
        f"| 柱规格记录 | {direct.get('column_schedule_count', 0)} |",
        f"| 钢筋型号 | {direct.get('rebar_type_count', 0)} |",
        f"| 板记录 | {direct.get('slab_schedule_count', 0)} |",
        f"| 梁记录 | {direct.get('beam_schedule_count', 0)} |",
        f"| 门槛通过数 | {direct.get('gate_status_counts', {}).get('pass', 0)} |",
        f"| 门槛警告数 | {direct.get('gate_status_counts', {}).get('warn', 0)} |",
        f"| 门槛失败数 | {direct.get('gate_status_counts', {}).get('fail', 0)} |",
        f"| 混凝土候选合计m3 | "
        f"{direct.get('concrete_candidate_total_m3') if direct.get('concrete_candidate_total_m3') is not None else '-'} |",
        f"| 板拓扑毛面积m2 | "
        f"{direct.get('slab_phase15_gross_area_m2') if direct.get('slab_phase15_gross_area_m2') is not None else '-'} |",
        f"| 板洞口数/面积m2 | "
        f"{direct.get('slab_phase15_opening_count', '-') if direct.get('slab_phase15_opening_count') is not None else '-'}"
        f" / "
        f"{direct.get('slab_phase15_opening_area_m2') if direct.get('slab_phase15_opening_area_m2') is not None else '-'} |",
        f"| 板拓扑净面积m2 | "
        f"{direct.get('slab_phase15_net_area_m2') if direct.get('slab_phase15_net_area_m2') is not None else '-'} |",
        f"| 板厚粗折候选m3 | "
        f"{direct.get('slab_phase15_rough_volume_m3') if direct.get('slab_phase15_rough_volume_m3') is not None else '-'} |",
        f"| 构件相交重叠对 | "
        f"{direct.get('intersection_overlap_count') if direct.get('intersection_overlap_count') is not None else '-'} |",
        f"| 构件相交唯一重叠格 | "
        f"{direct.get('intersection_unique_overlap_cell_count') if direct.get('intersection_unique_overlap_cell_count') is not None else '-'} |",
        f"| 构件相交重叠面积m2 | "
        f"{direct.get('intersection_overlap_area_m2') if direct.get('intersection_overlap_area_m2') is not None else '-'} |",
        f"| 构件相交潜在重复量m3 | "
        f"{direct.get('intersection_potential_deduction_volume_m3') if direct.get('intersection_potential_deduction_volume_m3') is not None else '-'} |",
        f"| 构件相交净扣候选m3 | "
        f"{direct.get('intersection_applied_net_deduction_m3') if direct.get('intersection_applied_net_deduction_m3') is not None else '-'} |",
        f"| 规则试算总量m3 | "
        f"{direct.get('intersection_candidate_net_total_m3') if direct.get('intersection_candidate_net_total_m3') is not None else '-'} |",
        f"| 板面域拆分：纯现浇/板缝条带/压预制m2 | "
        f"{direct.get('slab_cast_only_area_m2') if direct.get('slab_cast_only_area_m2') is not None else '-'}"
        f" / "
        f"{direct.get('slab_seam_band_area_m2') if direct.get('slab_seam_band_area_m2') is not None else '-'}"
        f" / "
        f"{direct.get('slab_on_prefab_area_m2') if direct.get('slab_on_prefab_area_m2') is not None else '-'} |",
        f"| 板厚图例冲突面积m2 / 体积摆动m3 | "
        f"{direct.get('slab_thickness_conflict_area_m2') if direct.get('slab_thickness_conflict_area_m2') is not None else '-'}"
        f" / "
        f"{direct.get('slab_thickness_volume_swing_m3') if direct.get('slab_thickness_volume_swing_m3') is not None else '-'} |",
        f"| 板厚取自说明默认值面积m2（占比） | "
        f"{direct.get('slab_thickness_default_note_area_m2') if direct.get('slab_thickness_default_note_area_m2') is not None else '-'}"
        f"（{_pct(direct.get('slab_thickness_default_note_area_ratio'))}） |",
        f"| CAD独立可核量m3（梁+墙柱，不含参考回填） | "
        f"{direct.get('cad_independent_verifiable_m3') if direct.get('cad_independent_verifiable_m3') is not None else '-'} |",
        f"| CAD独立可核量m3（含CAD独立板量） | "
        f"{direct.get('cad_independent_with_slab_m3') if direct.get('cad_independent_with_slab_m3') is not None else '-'} |",
        f"| 参考回填量m3（连梁+Lb-1+TL2） | "
        f"{direct.get('reference_backfill_m3') if direct.get('reference_backfill_m3') is not None else '-'} |",
        f"| 广联达清单口径m3 | "
        f"{direct.get('glodon_schedule_total_m3') if direct.get('glodon_schedule_total_m3') is not None else '-'} |",
        f"| 去重后参考量m3（预制底板不再叠加） | "
        f"{direct.get('glodon_reference_deduped_total_m3') if direct.get('glodon_reference_deduped_total_m3') is not None else '-'} |",
        f"| 范围外二次结构+楼梯+零星m3 | "
        f"{direct.get('glodon_secondary_structure_m3') if direct.get('glodon_secondary_structure_m3') is not None else '-'}"
        f" / "
        f"{direct.get('glodon_stair_flight_m3') if direct.get('glodon_stair_flight_m3') is not None else '-'}"
        f" / "
        f"{direct.get('glodon_building_misc_m3') if direct.get('glodon_building_misc_m3') is not None else '-'} |",
        f"| 板现浇口径A_m3 / CAD独立板量差m3 | "
        f"{direct.get('slab_cast_in_place_caliber_a_m3') if direct.get('slab_cast_in_place_caliber_a_m3') is not None else '-'}"
        f" / "
        f"{direct.get('cad_slab_vs_caliber_a_diff_m3') if direct.get('cad_slab_vs_caliber_a_diff_m3') is not None else '-'} |",
        f"| 梁净未定位量m3 | "
        f"{direct.get('beam_net_unlocated_m3') if direct.get('beam_net_unlocated_m3') is not None else '-'} |",
        f"| 梁真实需补新几何m3 | "
        f"{direct.get('beam_residual_needing_new_geometry_m3') if direct.get('beam_residual_needing_new_geometry_m3') is not None else '-'} |",
        f"| 梁实例缺口中仅计数口径个数 | "
        f"{direct.get('beam_count_only_instance_gap') if direct.get('beam_count_only_instance_gap') is not None else '-'} |",
        f"| 板开洞图层图线数 | "
        f"{direct.get('slab_opening_entity_count') if direct.get('slab_opening_entity_count') is not None else '-'} |",
        f"| 板确认洞口数/面积m2 | "
        f"{direct.get('slab_opening_confirmed_count') if direct.get('slab_opening_confirmed_count') is not None else '-'}"
        f" / "
        f"{direct.get('slab_opening_confirmed_area_m2') if direct.get('slab_opening_confirmed_area_m2') is not None else '-'} |",
        f"| 板待复核图线组 | "
        f"{direct.get('slab_opening_review_count') if direct.get('slab_opening_review_count') is not None else '-'} |",
        f"| 板待复核体积上限m3 | "
        f"{direct.get('slab_opening_review_volume_upper_bound_m3') if direct.get('slab_opening_review_volume_upper_bound_m3') is not None else '-'} |",
        "",
        "## 构件规格",
        "",
        "| 类别 | 编号 | 截面/尺寸 | 箍筋 | 纵筋 | 估算根数 | 状态 |",
        "|---|---|---|---|---|---:|---|",
    ]
    for row in report.get("component_schedule") or []:
        lines.append(
            f"| {_md_cell(row.get('category'))} | {_md_cell(row.get('code'))} | "
            f"{_md_cell(row.get('section'))} | {_md_cell(row.get('stirrup'))} | "
            f"{_md_cell(row.get('longitudinal'))} | {row.get('estimated_count', 0)} | "
        f"{_md_cell(row.get('status'))} |"
        )
    closure = report.get("closure_dashboard") or {}
    if closure:
        lines += [
            "",
            "## 闭合门槛与阻断分组",
            "",
            "| 门槛 | 状态 | 证据 | 处理动作 |",
            "|---|---|---|---|",
        ]
        for row in closure.get("gates") or []:
            lines.append(
                f"| {_md_cell(row.get('title') or row.get('id'))} | "
                f"{_md_cell(row.get('status'))} | "
                f"{_md_cell(row.get('evidence'))} | "
                f"{_md_cell(row.get('action'))} |"
            )
        lines += [
            "",
            "| 阻断区域 | 状态 | 数量 | 涉及构件 |",
            "|---|---|---:|---|",
        ]
        for row in closure.get("blocking_groups") or []:
            members = row.get("member_ids") or row.get("codes") or []
            shown = "、".join(str(value) for value in members[:8])
            if len(members) > 8:
                shown += f" 等{len(members)}项"
            lines.append(
                f"| {_md_cell(row.get('area'))} | "
                f"{_md_cell(row.get('status'))} | {row.get('count', 0)} | "
                f"{_md_cell(shown)} |"
            )
        if closure.get("component_gaps"):
            lines += [
                "",
                "| 闭合组件 | 剩余阻断数 | 证据 | 动作 |",
                "|---|---:|---|---|",
            ]
            for row in closure.get("component_gaps") or []:
                lines.append(
                    f"| {_md_cell(row.get('component'))} | "
                    f"{row.get('remaining_count', 0)} | "
                    f"{_md_cell(row.get('evidence'))} | "
                    f"{_md_cell(row.get('action'))} |"
                )
        next_actions = closure.get("next_actions") or []
        if next_actions:
            lines += ["", "### 下一步闭合动作", ""]
            for action in next_actions:
                lines.append(f"- {action}")
    lines += [
        "",
        "## 柱规格与配筋候选",
        "",
        "| 编号 | 截面 | 根数 | 箍筋 | 纵筋 | 状态 | 来源 |",
        "|---|---|---:|---|---|---|---|",
    ]
    for row in report.get("column_schedule") or []:
        lines.append(
            f"| {_md_cell(row.get('code'))} | {_md_cell(row.get('section'))} | "
            f"{row.get('count', 0)} | {_md_cell(row.get('stirrup'))} | "
            f"{_md_cell(row.get('longitudinal'))} | {_md_cell(row.get('status'))} | "
            f"{_md_cell(row.get('source'))} |"
        )
    lines += [
        "",
        "## 钢筋型号",
        "",
        "| 类型 | 型号 | 构件型数 | 估算根数 | 构件编号 |",
        "|---|---|---:|---:|---|",
    ]
    for row in report.get("rebar_schedule") or []:
        lines.append(
            f"| {_md_cell(row.get('kind'))} | {_md_cell(row.get('model'))} | "
            f"{row.get('component_type_count', 0)} | "
            f"{row.get('estimated_count', 0)} | "
            f"{_md_cell(row.get('component_codes'))} |"
        )
    lines += [
        "",
        "## 板厚与洞口",
        "",
        "| 编号 | 板厚mm | 面积m2 | 净面积m2 | 洞口数 | 洞口面积m2 | 体积m3 | 状态 |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in report.get("slab_schedule") or []:
        lines.append(
            f"| {_md_cell(row.get('id') or row.get('code'))} | "
            f"{_md_cell(row.get('thickness_mm'))} | "
            f"{_md_cell(row.get('area_m2'))} | "
            f"{_md_cell(row.get('net_area_m2'))} | "
            f"{row.get('opening_count', 0)} | "
            f"{_md_cell(row.get('opening_area_m2'))} | "
            f"{_md_cell(row.get('volume_m3'))} | "
            f"{_md_cell(row.get('status'))} |"
        )
    lines += [
        "",
        "## 梁规格与净跨状态",
        "",
        "| 编号 | 截面 | 中心线mm | 净长mm | 粗量m3 | 净量m3 | 状态 | 问题 |",
        "|---|---|---:|---:|---:|---:|---|---|",
    ]
    for row in report.get("beam_schedule") or []:
        lines.append(
            f"| {_md_cell(row.get('code'))} | {_md_cell(row.get('section'))} | "
            f"{_md_cell(row.get('centerline_length_mm'))} | "
            f"{_md_cell(row.get('clear_length_mm'))} | "
            f"{_md_cell(row.get('gross_volume_m3'))} | "
            f"{_md_cell(row.get('clear_volume_m3'))} | "
            f"{_md_cell(row.get('quantity_status'))} | "
            f"{_md_cell(row.get('issue'))} |"
        )
    concrete = report.get("concrete") or {}
    lines += [
        "",
        "## 混凝土分账",
        "",
        "| 构件 | CAD口径 | 候选m3 | 对照m3 | 差异m3 | 差异率 | 状态 |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in concrete.get("comparisons") or []:
        lines.append(
            f"| {_md_cell(row.get('component'))} | {_md_cell(row.get('scope'))} | "
            f"{_md_cell(row.get('candidate_value_m3'))} | "
            f"{_md_cell(row.get('reference_value_m3'))} | "
            f"{_md_cell(row.get('difference_m3'))} | "
            f"{_md_cell(row.get('difference_pct'))}% | "
            f"{_md_cell(row.get('status'))} |"
        )
    lines += [
        "",
        "## 异常与回图定位",
        "",
        "| 级别 | 区域 | 构件 | 编号 | 状态 | 坐标 | 说明 |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in report.get("anomalies") or []:
        coordinate = (
            f"{row.get('x')},{row.get('y')}"
            if row.get("x") is not None or row.get("y") is not None
            else ""
        )
        lines.append(
            f"| {_md_cell(row.get('severity'))} | {_md_cell(row.get('area'))} | "
            f"{_md_cell(row.get('member_type'))} | "
            f"{_md_cell(row.get('member_id') or row.get('code'))} | "
            f"{_md_cell(row.get('status'))} | {_md_cell(coordinate)} | "
            f"{_md_cell(row.get('message'))} |"
        )
    supplements = report.get("supplemental_breakdown") or {}
    if supplements:
        lines += ["", "## 补充模型归一", ""]
        for name, item in supplements.items():
            lines.append(f"- `{name}`：`{item.get('schema') or '-'}`，"
                         f"状态 `{item.get('status') or '-'}`。")
        for item in supplements.values():
            if item.get("schema") != "cad-beam-reference-reconciliation/v0.1":
                continue
            summary = item.get("summary") or {}
            transfers = item.get("transfer_projection") or {}
            missing_by_code = item.get("missing_by_code") or []
            lines += [
                "",
                "## 梁实例对账",
                "",
                "| 编号 | 参考实例 | 已定位等效 | 缺失 | 当前m3 | 参考m3 | 状态 |",
                "|---|---:|---:|---:|---:|---:|---|",
            ]
            for row in missing_by_code:
                lines.append(
                    f"| {_md_cell(row.get('code'))} | "
                    f"{row.get('reference_instance_count', 0)} | "
                    f"{row.get('selected_equivalent_instance_count', 0)} | "
                    f"{row.get('missing_equivalent_instance_count', 0)} | "
                    f"{_md_cell(row.get('current_code_volume_m3'))} | "
                    f"{_md_cell(row.get('reference_volume_m3'))} | "
                    f"{_md_cell(row.get('status'))} |"
                )
            lines += [
                "",
                f"- 参考实例：`{summary.get('reference_main_instance_count', 0)}`；"
                f"已定位等效：`{summary.get('selected_equivalent_instance_count', 0)}`；"
                f"缺失：`{summary.get('missing_equivalent_instance_count', 0)}`。",
                f"- A级转移后编号误差："
                f"`{transfers.get('grade_a_absolute_code_error_m3', '-')}` m3；"
                f"A+B复核投影："
                f"`{transfers.get('grade_ab_absolute_code_error_m3', '-')}` m3。",
                "- 这些是研发对账口径，不补造几何，也不能据此宣告实例闭合。",
            ]
        for item in supplements.values():
            if _text(item.get("schema")) not in INTERSECTION_SCHEMAS:
                continue
            audit_summary = item.get("summary") or {}
            groups = audit_summary.get("groups") or {}
            labels = {
                "beam-vertical": "梁与墙柱",
                "beam-beam": "梁与梁",
                "beam-coupling": "梁与连梁",
                "coupling-vertical": "连梁与竖向构件",
                "vertical-vertical": "竖向构件之间",
                "other": "其他",
            }
            lines += [
                "",
                "## 构件相交重复计量",
                "",
                "| 类型 | 重叠对 | 唯一格 | 面积m2 | 潜在体积m3 | 成对原值m3 | 去重量m3 | 是否已扣减 |",
                "|---|---:|---:|---:|---:|---:|---:|---|",
            ]
            for key in ("beam-vertical", "beam-beam", "beam-coupling",
                        "coupling-vertical", "vertical-vertical"):
                row = groups.get(key)
                if not row:
                    continue
                applied = bool((item.get("closure") or {}).get(
                    "applied_to_formal_quantity"))
                lines.append(
                    f"| {labels.get(key, key)} | {row.get('overlap_count', 0)} | "
                    f"{row.get('unique_overlap_cell_count', 0)} | "
                    f"{_md_cell(row.get('overlap_area_m2'))} | "
                    f"{_md_cell(row.get('potential_deduction_volume_m3'))} | "
                    f"{_md_cell(row.get('pairwise_potential_deduction_volume_m3'))} | "
                    f"{_md_cell(row.get('deduplication_overcount_m3'))} | "
                    f"{str(applied).lower()} |"
                )
            lines += ["", "| 构件1 | 构件2 | 面积m2 | 高度mm | 潜在体积m3 | 坐标范围 |",
                      "|---|---|---:|---:|---:|---|"]
            for row in item.get("top_overlaps") or []:
                codes = row.get("codes") or row.get("member_ids") or ["", ""]
                lines.append(
                    f"| {_md_cell(codes[0])} | {_md_cell(codes[1] if len(codes) > 1 else '')} | "
                    f"{_md_cell(row.get('overlap_area_m2'))} | "
                    f"{_md_cell(row.get('deduction_height_mm'))} | "
                    f"{_md_cell(row.get('potential_deduction_volume_m3'))} | "
                    f"{_md_cell(';'.join(str(v) for v in row.get('overlap_bbox_mm') or []))} |"
                )
            lines.append(
                "- 审计只暴露重叠区，未确认节点归属前不自动改写混凝土候选合计。")
            net = item.get("net_quantity") or {}
            if net:
                lines += [
                    "",
                    "### 候选构件净量",
                    "",
                    f"- 规则：{net.get('rule') or '-'}。",
                    f"- 梁净扣候选：`{_md_cell(net.get('applied_deduction_m3'))}` m3；"
                    f"连梁参考净扣：`{_md_cell(net.get('reference_only_deduction_m3'))}` m3。",
                    f"- 规则试算总量：`{_md_cell(net.get('candidate_total_after_beam_deduction_m3'))}` m3；"
                    f"当前正式候选仍为 `{_md_cell(net.get('current_located_total_m3'))}` m3。",
                    f"- 竖向构件之间未决面积：`{_md_cell(net.get('unresolved_vertical_overlap_area_m2'))}` m2，"
                    f"潜在体积 `{_md_cell(net.get('unresolved_vertical_overlap_volume_m3'))}` m3。",
                    "",
                    "| 构件 | 毛量m3 | 相交扣减m3 | 净量m3 |",
                    "|---|---:|---:|---:|",
                ]
                for row in (net.get("top_affected_members") or {}).get("beam", [])[:12]:
                    lines.append(
                        f"| {_md_cell(row.get('code') or row.get('id'))} | "
                        f"{_md_cell(row.get('gross_volume_m3'))} | "
                        f"{_md_cell(row.get('intersection_deduction_m3'))} | "
                        f"{_md_cell(row.get('net_volume_m3'))} |"
                    )
                lines.append(
                    "- 净量来自相交去重规则，不是正式构件计量；等截面梁同点所有者仅作试算拆分。")
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != BEAM_GAP_SCHEMA:
            continue
        audit_summary = item.get("summary") or {}
        decomposition = item.get("gap_decomposition") or {}
        lines += [
            "",
            "## 梁体积缺口归因",
            "",
            f"- {int(_number(audit_summary.get('code_count')) or 0)} 个编号按体积对账："
            f"体积一致 {int(_number(audit_summary.get('volume_matched_code_count')) or 0)} 个、"
            f"缺量 {int(_number(audit_summary.get('volume_under_code_count')) or 0)} 个"
            f"（`{_md_cell(audit_summary.get('under_total_m3'))}` m3）、"
            f"多计 {int(_number(audit_summary.get('volume_over_code_count')) or 0)} 个"
            f"（`{_md_cell(audit_summary.get('over_total_m3'))}` m3）。",
            f"- 原报缺失实例 `{int(_number(audit_summary.get('missing_instance_count')) or 0)}` 个："
            f"体积可支撑 `{int(_number(audit_summary.get('volume_explained_missing_instance_count')) or 0)}` 个，"
            f"仅计数口径差 `{int(_number(audit_summary.get('count_only_missing_instance_count')) or 0)}` 个"
            "（只影响钢筋支数，不算混凝土缺口）。",
            f"- 净未定位 `{_md_cell(audit_summary.get('main_beam_net_unlocated_m3'))}` m3；"
            f"未归属图线池 `{_md_cell(audit_summary.get('unassigned_run_volume_m3'))}` m3；"
            f"仍需检索新几何 "
            f"`{_md_cell(audit_summary.get('residual_needing_new_geometry_m3'))}` m3。",
            "",
            "| 分项 | 参考m3 | 已定位m3 | 差m3 | 说明 |",
            "|---|---:|---:|---:|---|",
        ]
        for row in decomposition.get("components") or []:
            lines.append(
                f"| {row.get('component')} | {_md_cell(row.get('reference_m3'))} | "
                f"{_md_cell(row.get('located_m3'))} | "
                f"{_md_cell(row.get('difference_m3'))} | "
                f"{_md_cell(row.get('note'))} |")
        lines += [
            f"| 合计 | {_md_cell(decomposition.get('beam_reference_m3'))} | "
            f"{_md_cell(decomposition.get('beam_located_m3'))} | "
            f"{_md_cell(decomposition.get('sum_difference_m3'))} | 台账缺口 "
            f"{_md_cell(decomposition.get('beam_remaining_m3'))} m3，"
            + ("完全对上 |" if decomposition.get("matches_ledger") else "未对上 |"),
            "",
            "| 编号 | 截面 | 缺量m3 | 需补梁线mm | 未归属同截面图线 |",
            "|---|---|---:|---:|---:|",
        ]
        for row in item.get("search_targets") or []:
            lines.append(
                f"| {row.get('code')} | {row.get('section')} | "
                f"{_md_cell(row.get('missing_volume_m3'))} | "
                f"{_md_cell(row.get('needed_length_mm'))} | "
                f"{row.get('unassigned_candidate_count', 0)} |")
        lines.append(
            "- 编号级差值只用于定位该回图查哪个编号，不自动改写几何或总量。")
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != BEAM_COVERAGE_SCHEMA:
            continue
        audit_summary = item.get("summary") or {}
        lines += [
            "",
            "## 梁图层覆盖审计",
            "",
            f"- 提取窗口内梁线 "
            f"{int(_number(audit_summary.get('in_frame_segment_count')) or 0)} 条/"
            f"`{_md_cell(audit_summary.get('in_frame_length_mm'))}` mm，被实例边线覆盖 "
            f"**{_number(audit_summary.get('in_frame_coverage_ratio')) * 100:.2f}%**"
            "（按区间计长，部分覆盖按实长计入）。",
            f"- 窗口内未覆盖 "
            f"{int(_number(audit_summary.get('uncovered_in_frame_count')) or 0)} 段/"
            f"`{_md_cell(audit_summary.get('uncovered_in_frame_length_mm'))}` mm，"
            f"配对 "
            f"{int(_number(audit_summary.get('candidate_beam_in_frame_count')) or 0)} 条候选梁/"
            f"`{_md_cell(audit_summary.get('candidate_volume_in_frame_m3'))}` m3。",
            f"- 提取窗口外图线全部有视图归属，一律不计本层漏量："
            f"镜像对称 "
            f"{int(_number(audit_summary.get('mirrored_line_count')) or 0)} 段/"
            f"`{_md_cell(audit_summary.get('candidate_volume_mirror_pair_m3'))}` m3"
            f"（配对体量比缺口多 "
            f"`{_md_cell(audit_summary.get('mirror_pair_overshoot_m3'))}` m3，"
            f"计入即超出广联达参考量）；平移孪生 "
            f"{int(_number(audit_summary.get('duplicate_view_line_count')) or 0)} 段/"
            f"`{_md_cell(audit_summary.get('candidate_volume_translated_view_m3'))}` m3"
            f"（统一偏移 `{_md_cell(audit_summary.get('duplicate_view_offset_mm'))}` mm）。"
            f"板面域内但窗口外 "
            f"`{_md_cell(audit_summary.get('candidate_volume_window_out_m3'))}` m3、"
            f"板面域外 "
            f"`{_md_cell(audit_summary.get('candidate_volume_beyond_plan_m3'))}` m3 "
            f"才是可并入的漏量候选，当前均为 0；"
            "扩窗重跑源 DWG 已核验新增实体为 0，不存在被裁掉的梁线。",
            f"- 对照梁净缺口：仍无法解释 "
            f"`{_md_cell(audit_summary.get('residual_still_unexplained_m3'))}` m3；"
            f"连梁图层 {int(_number(audit_summary.get('coupling_uncovered_count')) or 0)} 段"
            "另走连梁独立台账，不计入本门槛。",
            "",
            "| 候选段 | 视图归属 | 宽mm | 长mm | 假定高mm | 体积m3 |",
            "|---|---|---:|---:|---:|---:|",
        ]
        for row in item.get("candidates") or []:
            lines.append(
                f"| {'+'.join(row.get('handles') or [])} | "
                f"{_md_cell(row.get('view_zone'))} | {_md_cell(row.get('width_mm'))} | "
                f"{_md_cell(row.get('length_mm'))} | "
                f"{_md_cell(row.get('assumed_height_mm'))} | "
                f"{_md_cell(row.get('volume_m3'))} |")
        lines.append(
            "- 候选段只作回图目标；梁实例提取窗口扩到整层板面域前，"
            "混凝土合计维持候选口径。")
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != BEAM_ATTRIBUTION_SCHEMA:
            continue
        attr_summary = item.get("summary") or {}
        decomposition = item.get("residual_decomposition") or {}
        targets = item.get("under_code_targets") or {}
        caliber = item.get("section_recheck") or {}
        lines += [
            "",
            "## 梁候选段归属与截面口径复核",
            "",
            f"- 可比对实例 {int(_number(caliber.get('run_rechecked_count')) or 0)} 条，"
            f"截面与编号参考值不一致 "
            f"{int(_number(attr_summary.get('run_section_mismatch_count')) or 0)} 条，"
            f"换成参考截面后体积差 `{_md_cell(caliber.get('run_recheck_delta_m3'))}` m3："
            "偏少编号的缺口不是截面高取值造成。",
            f"- 提取窗口内候选段 {int(_number(attr_summary.get('in_frame_candidate_count')) or 0)} 条："
            f"同轴续接可归属 "
            f"`{_md_cell(attr_summary.get('attached_to_existing_code_m3'))}` m3、"
            f"无同轴编号 `{int(_number(attr_summary.get('no_coaxial_run_count')) or 0)}` 条/"
            f"`{_md_cell(attr_summary.get('unattached_candidate_m3'))}` m3。",
            f"- 缺口分解恒等式 "
            f"`{'成立' if decomposition.get('matches_identity') else '不成立'}`；"
            f"扣掉可归属续接段后本图框仍无法解释 "
            f"`{_md_cell(attr_summary.get('unexplained_by_this_frame_m3'))}` m3。",
            f"- 偏少编号 {int(_number(attr_summary.get('under_code_count')) or 0)} 个"
            f"（毛差 `{_md_cell(targets.get('under_total_m3'))}` m3）里，"
            f"需跨图框检索 {int(_number(targets.get('cross_frame_code_count')) or 0)} 个/"
            f"`{_md_cell(targets.get('cross_frame_needed_length_mm'))}` mm；"
            f"计数口径 {int(_number(targets.get('count_only_code_count')) or 0)} 个不需要新几何。",
            "",
            "| 候选段 | 长mm | 归属编号 | 归属量m3 | 端头间隙mm | 状态 |",
            "|---|---:|---|---:|---:|---|",
        ]
        for row in item.get("candidate_attribution") or []:
            lines.append(
                f"| {_md_cell(row.get('handles'))} | "
                f"{_md_cell(row.get('length_mm'))} | "
                f"{_md_cell(row.get('matched_code')) or '—'} | "
                f"{_md_cell(row.get('attributed_volume_m3'))} | "
                f"{_md_cell(row.get('joint_gap_mm'))} | "
                f"{_md_cell(row.get('status'))} |")
        lines += [
            "",
            "| 偏少编号 | 参考截面 | 量差m3 | 需补mm | 本图框认领 | 判定 |",
            "|---|---|---:|---:|---|---|",
        ]
        for row in (targets.get("codes") or [])[:12]:
            lines.append(
                f"| {_md_cell(row.get('code'))} | "
                f"{_md_cell(row.get('reference_section'))} | "
                f"{_md_cell(row.get('difference_m3'))} | "
                f"{_md_cell(row.get('needed_length_mm'))} | "
                f"{_md_cell(row.get('claim_candidate_handles')) or '—'} | "
                f"{_md_cell(row.get('classification'))} |")
        lines.append(
            "- 认领只缩短回图目标清单，候选量仍留在"
            "「有几何无编号」栏，不重复计入梁混凝土量。")
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != BEAM_FRAME_INDEX_SCHEMA:
            continue
        index_summary = item.get("summary") or {}
        counts = dict(index_summary.get("classification_counts") or {})
        volumes = dict(index_summary.get("classification_volume_m3") or {})
        lines += [
            "",
            "## 梁编号图框标签索引",
            "",
            f"- 整册编号标注 "
            f"`{int(_number(index_summary.get('label_count')) or 0)}` 条、"
            f"图名 `{int(_number(index_summary.get('title_count')) or 0)}` 处、"
            f"图框 `{int(_number(index_summary.get('frame_count')) or 0)}` 个全部归属完成。",
            f"- 偏少编号 "
            f"`{int(_number(index_summary.get('under_code_count')) or 0)}` 个在本层图框内"
            f"都有集中标注（`no-label-in-target-frame` "
            f"{int(_number(counts.get('no-label-in-target-frame')) or 0)} 个），"
            "同名标注的其余副本在其他楼层图框，不计入本层。",
            "",
            "| 判定 | 编号数 | 毛差m3 |",
            "|---|---:|---:|",
        ]
        for key, count in sorted(counts.items(), key=lambda row: -row[1]):
            lines.append(f"| {key} | {count} | "
                         f"{_md_cell(volumes.get(key))} |")
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != BEAM_SPAN_CLOSURE_SCHEMA:
            continue
        closure_summary = item.get("summary") or {}
        verdict_counts = dict(closure_summary.get("verdict_counts") or {})
        verdict_volumes = dict(closure_summary.get("verdict_volume_m3") or {})
        lines += [
            "",
            "## 梁净跨口径与支座扣减",
            "",
            f"- {int(_number(closure_summary.get('beam_instance_count')) or 0)} 根梁："
            f"中心线 `{_md_cell(closure_summary.get('centerline_length_mm'))}` mm、"
            f"净长 `{_md_cell(closure_summary.get('clear_length_mm'))}` mm、"
            f"支座扣减 `{_md_cell(closure_summary.get('support_deduction_length_mm'))}` mm。",
            f"- 中心线口径 `{_md_cell(closure_summary.get('gross_volume_m3'))}` m3、"
            f"净跨口径 `{_md_cell(closure_summary.get('clear_volume_m3'))}` m3，"
            f"口径差 `{_md_cell(closure_summary.get('span_caliber_difference_m3'))}` m3；"
            f"相交审计梁侧可扣 "
            f"`{_md_cell(closure_summary.get('intersection_beam_side_deduction_m3'))}` m3，"
            f"冲突 `{_md_cell(closure_summary.get('span_caliber_vs_intersection_conflict_m3'))}` m3"
            f"（推定端合计 "
            f"`{_md_cell(closure_summary.get('inferred_end_support_width_mm'))}` mm）。",
            f"- 定责合计 `{_md_cell(closure_summary.get('verdict_total_m3'))}` m3 覆盖偏少编号毛差；"
            f"真需补几何 `{_md_cell(closure_summary.get('needs_new_geometry_volume_m3'))}` m3、"
            f"编号链丢失 `{_md_cell(closure_summary.get('chain_lost_volume_m3'))}` m3，"
            f"其余 `{_md_cell(closure_summary.get('caliber_only_volume_m3'))}` m3 为口径问题。",
            "",
            "| 编号 | 图框判定 | 定责 | 参考单实例mm | CAD每实例mm | 长度差mm | 支座扣减mm | 量差m3 |",
            "|---|---|---|---:|---:|---:|---:|---:|",
        ]
        for row in item.get("code_closure") or []:
            lines.append(
                f"| {_md_cell(row.get('code'))} | "
                f"{_md_cell(row.get('frame_classification'))} | "
                f"{_md_cell(row.get('verdict'))} | "
                f"{_md_cell(row.get('reference_single_axis_length_mm'))} | "
                f"{_md_cell(row.get('cad_span_per_selected_instance_mm'))} | "
                f"{_md_cell(row.get('single_instance_deficit_mm'))} | "
                f"{_md_cell(row.get('model_support_deduction_per_instance_mm'))} | "
                f"{_md_cell(row.get('current_code_difference_m3'))} |")
        lines.append(
            "- 长度差不超过支座扣减的编号属轴线/净跨口径差，计入即与柱墙重复计量。")
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != BEAM_MULTISPAN_SCHEMA:
            continue
        multi_summary = item.get("summary") or {}
        lines += [
            "",
            "## 多跨梁跨支座续接候选",
            "",
            f"- 带宽 ≥2 的梁 {int(_number(multi_summary.get('multispan_beam_count')) or 0)} 根，"
            f"同轴跨支座续接成功 "
            f"{int(_number(multi_summary.get('continued_beam_count')) or 0)} 根，"
            f"补梁线 {_md_cell(multi_summary.get('added_beam_length_mm'))} mm + "
            f"支座 {_md_cell(multi_summary.get('added_support_width_mm'))} mm = "
            f"轴线长 {_md_cell(multi_summary.get('added_axis_length_mm'))} mm，"
            f"候选体积 {_md_cell(multi_summary.get('added_volume_candidate_m3'))} m3。",
            f"- 单实例长度缺口由 {_md_cell(multi_summary.get('deficit_before_mm'))} mm 降到 "
            f"{_md_cell(multi_summary.get('deficit_after_mm'))} mm，闭合率 "
            f"{(_number(multi_summary.get('deficit_closed_ratio')) or 0) * 100:.1f}%。",
            "",
            "| 实例 | 编号 | 带宽 | 现中心线mm | 续接后mm | 候选m3 | 剩余缺口mm | 续接证据 |",
            "|---|---|---:|---:|---:|---:|---:|---|",
        ]
        for row in item.get("beams") or []:
            evidence = "；".join(
                f"穿 {_text(pair.get('support_layer'))}#{_text(pair.get('support_handle'))}"
                f"接 #{_text(pair.get('beam_handle'))}"
                for pair in row.get("added_evidence") or [])
            lines.append(
                f"| {_md_cell(row.get('beam_id'))} | {_md_cell(row.get('code'))} | "
                f"{row.get('span_count')} | "
                f"{_md_cell(row.get('current_centerline_mm'))} | "
                f"{_md_cell(row.get('continued_centerline_mm'))} | "
                f"{_md_cell(row.get('added_volume_candidate_m3'))} | "
                f"{_md_cell(row.get('remaining_deficit_mm'))} | {evidence} |")
        lines.append(
            "- 续接量只作候选，`applied_to_formal_quantity=false`；"
            "并入前须按句柄回图确认编号归属与支座性质。")
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != BEAM_DEDUP_SCHEMA:
            continue
        dedup_summary = item.get("summary") or {}
        class_count = dict(dedup_summary.get("beam_only_class_count") or {})
        class_volume = dict(dedup_summary.get("beam_only_class_volume_m3") or {})
        verdict_count = dict(
            dedup_summary.get("unpaired_run_verdict_count") or {})
        verdict_volume = dict(
            dedup_summary.get("unpaired_run_verdict_volume_m3") or {})
        overlap = item.get("run_self_overlap") or {}
        lines += [
            "",
            "## 梁实例双口径去重",
            "",
            f"- 模型梁 {int(_number(dedup_summary.get('beam_count')) or 0)} 根/"
            f"{_text(dedup_summary.get('beam_volume_m3'))} m3 与算量实例 "
            f"{int(_number(dedup_summary.get('run_count')) or 0)} 条/"
            f"{_text(dedup_summary.get('run_volume_m3'))} m3 中，"
            f"{int(_number(dedup_summary.get('matched_beam_count')) or 0)} 根判为同一根物理梁，"
            f"两套口径相加会重复计量 {_text(dedup_summary.get('double_count_volume_m3'))} m3。",
            f"- 无 run 可配的模型梁 {int(_number(dedup_summary.get('beam_only_count')) or 0)} 根/"
            f"{_text(dedup_summary.get('beam_only_candidate_volume_m3'))} m3，"
            f"其中归属冲突 {int(class_count.get('attribution-conflict') or 0)} 根/"
            f"{_text(class_volume.get('attribution-conflict'))} m3、"
            f"模型多实例 {int(class_count.get('model-extra-instance') or 0)} 根/"
            f"{_text(class_volume.get('model-extra-instance'))} m3、"
            f"编号缺失 {int(class_count.get('code-absent') or 0)} 根/"
            f"{_text(class_volume.get('code-absent'))} m3；"
            f"模型梁口径净新增只有 "
            f"**{_text(dedup_summary.get('model_beam_net_new_volume_m3'))} m3**，"
            "因此不得把模型梁并入混凝土分账。",
            f"- 只有 run 没有模型梁 {int(_number(dedup_summary.get('unmatched_run_count')) or 0)} 条/"
            f"{_text(dedup_summary.get('unmatched_run_volume_m3'))} m3，定责："
            f"续接段 {int(verdict_count.get('continuation-candidate') or 0)} 条/"
            f"{_text(verdict_volume.get('continuation-candidate'))} m3、"
            f"归属冲突 {int(verdict_count.get('attribution-conflict') or 0)} 条/"
            f"{_text(verdict_volume.get('attribution-conflict'))} m3、"
            f"同编号他处 {int(verdict_count.get('same-code-other-location') or 0)} 条/"
            f"{_text(verdict_volume.get('same-code-other-location'))} m3、"
            f"模型缺实例 {int(verdict_count.get('model-missing-instance') or 0)} 条/"
            f"{_text(verdict_volume.get('model-missing-instance'))} m3。",
            f"- run 口径内部同轴重叠 {int(_number(overlap.get('pair_count')) or 0)} 处/"
            f"{_text(overlap.get('overlapped_volume_m3'))} m3，"
            "为 0 说明分账的梁基数自身没有重复计量。",
            "",
            "| 无 run 模型梁 | 编号 | 体积m3 | 分类 | 同编号未配对 run |",
            "|---|---|---:|---|---|",
        ]
        for row in item.get("beam_only") or []:
            lines.append(
                f"| {_md_cell(row.get('beam_id'))} | {_md_cell(row.get('code'))} | "
                f"{_md_cell(row.get('beam_volume_m3'))} | "
                f"{_md_cell(row.get('beam_only_class'))} | "
                f"{_md_cell('|'.join(row.get('unpaired_same_code_run_ids') or []))} |")
        lines += [
            "",
            "| 未配对 run | 编号 | 向 | 体积m3 | 编号证据 | 定责 |",
            "|---|---|---|---:|---|---|",
        ]
        for row in item.get("run_verdicts") or []:
            lines.append(
                f"| {_md_cell(row.get('run_id'))} | {_md_cell(row.get('code'))} | "
                f"{_md_cell(row.get('orientation'))} | "
                f"{_md_cell(row.get('volume_m3'))} | "
                f"{_md_cell(row.get('evidence'))} | "
                f"{_md_cell(row.get('verdict'))} |")
        lines.append(
            "- 本章节只做口径归属判定，`applied_to_formal_quantity=false`，"
            "未改任何构件体积。")
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != BEAM_CONFLICT_SCHEMA:
            continue
        conflict_summary = item.get("summary") or {}
        conflict_verdicts = dict(conflict_summary.get("verdicts") or {})
        lines += [
            "",
            "## 梁编号归属冲突定责",
            "",
            f"- {summary_int(conflict_summary, 'conflict_pair_count')} 对"
            f"同向同截面同轴但编号不同的冲突，涉及 run "
            f"{summary_int(conflict_summary, 'conflict_run_count')} 条、模型梁 "
            f"{summary_int(conflict_summary, 'conflict_beam_count')} 根；"
            f"完全同轴 {summary_int(conflict_summary, 'same_axis_pair_count')} 对；"
            f"两口径相加重复计量风险 "
            f"**{_text(conflict_summary.get('double_count_risk_m3'))} m3**。",
            f"- 引线证据置信度："
            f"{json.dumps(conflict_summary.get('label_confidence_counts') or {}, ensure_ascii=False)}。",
            (f"- 逐对定主：已定 "
             f"{summary_int(conflict_summary, 'ownership_decided_pair_count')} 对、"
             f"仍需复核 {summary_int(conflict_summary, 'ownership_open_pair_count')} 对，"
             f"编号搬移 {_text(conflict_summary.get('attribution_transfer_m3'))} m3"
             f"（逐编号增减求和残差 "
             f"{_text(conflict_summary.get('attribution_balance_residual_m3'))}），"
             f"风险由 {_text(conflict_summary.get('double_count_risk_m3'))} m3 收到 "
             f"**{_text(conflict_summary.get('residual_double_count_risk_m3'))} m3**。"
             if "ownership_decided_pair_count" in conflict_summary else ""),
            "",
            "| 判定 | 对数 | 重复计量风险m3 | 含义 |",
            "|---|---:|---:|---|",
        ]
        meaning = {
            "run-label-holds": "只有 run 的编号被引线指向这段线，模型梁编号错挂",
            "beam-label-holds": "只有模型梁的编号被引线指向这段线，run 编号错挂",
            "dual-label-same-line": "两侧编号都有引线落在同一段线上，图纸同轴两构件，须人工定跨",
            "no-label-evidence": "两侧编号都无引线落在该段线上，属推定冲突",
        }
        for key in ("run-label-holds", "beam-label-holds", "dual-label-same-line",
                    "no-label-evidence"):
            value = conflict_verdicts.get(key)
            if not value:
                continue
            lines.append(
                f"| `{key}` | {int(_number(value.get('pair_count')) or 0)} | "
                f"{_text(value.get('double_count_risk_m3'))} | {meaning[key]} |")
        lines += [
            "",
            "| run | run编号 | 模型梁 | 梁编号 | 向 | 轴偏mm | 重叠mm | 线上标注 | 判定 | 置信 | 风险m3 | 归属主 | 剩余风险m3 | 回图坐标 |",
            "|---|---|---|---|---|---:|---:|---|---|---|---:|---|---:|---|",
        ]
        for row in item.get("conflicts") or []:
            lines.append(
                f"| {_md_cell(row.get('run_id'))} | {_md_cell(row.get('run_code'))} | "
                f"{_md_cell(row.get('beam_id'))} | {_md_cell(row.get('beam_code'))} | "
                f"{_md_cell(row.get('orientation'))} | "
                f"{_md_cell(row.get('axis_offset_mm'))} | "
                f"{_md_cell(row.get('overlap_mm'))} | "
                f"{_md_cell(', '.join(row.get('label_leader_ids') or []))} | "
                f"{_md_cell(row.get('verdict'))} | {_md_cell(row.get('confidence'))} | "
                f"{_md_cell(row.get('double_count_risk_m3'))} | "
                f"{_md_cell((row.get('ownership') or {}).get('code'))} | "
                f"{_md_cell((row.get('ownership') or {}).get('residual_risk_m3'))} | "
                f"{_md_cell(', '.join(str(value) for value in row.get('review_xy') or []))} |")
        lines.append(
            "- 定主只搬编号归属、不搬几何；未定主的段两编号都进台账但不得相加，"
            "`applied_to_formal_quantity=false`。")
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != SLAB_OPENING_SCHEMA:
            continue
        audit_summary = item.get("summary") or {}
        lines += [
            "",
            "## 板洞口证据审计",
            "",
            f"- 开洞图层图线 "
            f"`{int(_number(audit_summary.get('source_entity_count')) or 0)}` 条，"
            f"实体台账闭合 "
            f"`{str(bool(audit_summary.get('entity_ledger_closed'))).lower()}`。",
            f"- 确认洞口 "
            f"`{int(_number(audit_summary.get('confirmed_opening_count')) or 0)}` 个、"
            f"`{_md_cell(audit_summary.get('confirmed_opening_area_m2'))}` m2；"
            f"判为标注/引出线 "
            f"`{int(_number(audit_summary.get('annotation_record_count')) or 0)}` 组；"
            f"图框外重复 "
            f"`{int(_number(audit_summary.get('out_of_frame_count')) or 0)}` 组。",
            f"- 板面毛 `{_md_cell(audit_summary.get('gross_panel_area_m2'))}` m2，"
            f"扣洞净 `{_md_cell(audit_summary.get('net_panel_area_m2'))}` m2。",
            f"- 历史洞口候选板 "
            f"`{int(_number(audit_summary.get('prior_candidate_panel_count')) or 0)}` 个："
            f"已解释 `{int(_number(audit_summary.get('prior_candidate_explained_panel_count')) or 0)}` 个、"
            f"待复核 `{int(_number(audit_summary.get('prior_candidate_review_panel_count')) or 0)}` 个。",
            f"- 待复核包络上限 "
            f"`{_md_cell(audit_summary.get('review_envelope_area_upper_bound_m2'))}` m2 / "
            f"`{_md_cell(audit_summary.get('review_volume_upper_bound_m3'))}` m3，"
            "未计入任何扣减。",
            "",
            "| 确认洞口 | 句柄 | 板面 | 面积m2 | 证据 |",
            "|---|---|---|---:|---|",
        ]
        for row in item.get("confirmed_openings") or []:
            lines.append(
                f"| {row.get('status')} | {_md_cell('+'.join(row.get('handles') or []))} | "
                f"{_md_cell(row.get('panel_id'))} | "
                f"{_md_cell(row.get('deduct_area_m2'))} | "
                f"{_md_cell(row.get('evidence'))} |")
        if item.get("review_records"):
            lines += [
                "",
                "| 待复核图线 | 句柄 | 状态 | 包络m2 | 体积上限m3 | 证据 |",
                "|---|---|---|---:|---:|---|",
            ]
            for row in item.get("review_records") or []:
                lines.append(
                    f"| 开洞图层 | {_md_cell('+'.join(row.get('handles') or []))} | "
                    f"{_md_cell(row.get('status'))} | "
                    f"{_md_cell(row.get('envelope_area_m2'))} | "
                    f"{_md_cell(row.get('potential_volume_upper_bound_m3'))} | "
                    f"{_md_cell(row.get('evidence'))} |")
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != PREFAB_BOOKLET_SCHEMA:
            continue
        book_summary = item.get("summary") or {}
        book_facts = item.get("design_facts") or {}
        book_probe = item.get("frame_label_probe") or {}
        lines += [
            "",
            "## 装配式计算书设计锚点",
            "",
            f"- 图纸版本自证：结构图两处副本 md5 相同 "
            f"`{str(bool(book_summary.get('drawing_copies_identical'))).lower()}`；"
            f"计算书口径恒等式 "
            f"`{_md_cell(book_summary.get('identity_checks_passed'))}/"
            f"{_md_cell(book_summary.get('identity_checks_total'))}` 成立。",
            f"- 设计书指标：水平构件 "
            f"`{_md_cell(book_summary.get('design_plate_area_m2'))}` m2/层、预制叠合板 "
            f"`{_md_cell(book_summary.get('design_prefab_area_m2'))}` m2/层、竖向构件 "
            f"`{_md_cell(book_facts.get('design_std_vertical_volume_m3'))}` m3/层、叠合板厚 "
            f"`{_md_cell(book_facts.get('design_composite_slab_thickness_mm'))}` mm、梁宽墙厚 "
            f"`{_md_cell(book_facts.get('design_vertical_and_beam_width_mm'))}` mm、装配率 "
            f"`{_md_cell(book_facts.get('design_assembly_ratio_pct'))}%`。",
            f"- CAD 对设计：板面域 "
            f"`{_md_cell(book_summary.get('cad_vs_design_plate_area_pct'))}%`；"
            f"预制面积按编号展开 `{_md_cell(book_summary.get('cad_vs_design_prefab_area_pct'))}%`"
            f"（缺口 `{_md_cell(book_summary.get('prefab_area_gap_m2'))}` m2 ≈ "
            f"`{_md_cell(book_summary.get('prefab_gap_volume_at_design_thickness_m3'))}` m3，"
            "整厚 130 mm 口径）。",
            f"- 实例倍率：设计书 "
            f"`{_md_cell(book_summary.get('prefab_expansion_multiplier_design'))}`、"
            f"广联达展开 `{_md_cell(book_summary.get('prefab_expansion_multiplier_glodon'))}`"
            f"（CAD 图面轮廓 `{_md_cell(book_summary.get('cad_prefab_outline_area_m2'))}` m2，"
            f"展开 `{_md_cell(book_summary.get('cad_prefab_expanded_area_m2'))}` m2）；"
            f"倍率来源仍是广联达模型块数，CAD 独立实例证据未闭合。",
            f"- 布置图邻域线索：S-PC 轮廓 `{int(_number(book_probe.get('rings')) or 0)}` 条 / "
            f"`{_md_cell(book_probe.get('ring_area_m2'))}` m2、编号文字 "
            f"`{int(_number(book_probe.get('labels')) or 0)}` 条、(W) 镜像系列 "
            f"`{int(_number(book_probe.get('w_series_labels')) or 0)}` 条、"
            f"无配对编号 `{int(_number(book_probe.get('labels_without_ring')) or 0)}` 条。",
            "",
            "| 对照项 | 设计书 | CAD | 广联达 | CAD对设计% | 说明 |",
            "|---|---:|---:|---:|---:|---|",
        ]
        for row in item.get("comparisons") or []:
            lines.append(
                f"| {_md_cell(row.get('item'))} | {_md_cell(row.get('design'))} | "
                f"{_md_cell(row.get('cad'))} | {_md_cell(row.get('glodon'))} | "
                f"{_md_cell(row.get('cad_vs_design_pct'))} | "
                f"{_md_cell(row.get('note'))} |")
        for note in item.get("sheet_internal_notes") or []:
            lines.append(f"- 计算书内部口径：{_md_cell(note)}")
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != GRADE_LEDGER_SCHEMA:
            continue
        grade_summary = item.get("summary") or {}
        lines += [
            "",
            "## 混凝土分标号台账",
            "",
            f"- 计入合计 `{_md_cell(grade_summary.get('counted_total_m3'))}` m3，"
            f"恒等式残差 `{_md_cell(grade_summary.get('identity_residual_m3'))}` m3；"
            f"剔除预制子层 `{_md_cell(grade_summary.get('excluded_sublayer_m3'))}` m3。",
            f"- 梁柱节点区按柱等级浇筑（梁端 500 mm）换算 "
            f"`{_md_cell(grade_summary.get('joint_zone_m3'))}` m3：从梁档移到竖向构件档，"
            "总量不变。" if grade_summary.get("joint_zone_m3") else
            f"- 未定 `{_md_cell(grade_summary.get('unconfirmed_m3'))}` m3、"
            f"需回图确认 `{_md_cell(grade_summary.get('needs_review_m3'))}` m3"
            f"（{_pct(grade_summary.get('needs_review_ratio'))}）。",
            "",
            "| 强度等级 | 体积m3 | 来源类型 |",
            "|---|---:|---|",
        ]
        for grade, volume in sorted((item.get("by_grade") or {}).items()):
            lines.append(f"| {grade} | {volume} | "
                         f"{_md_cell(', '.join((item.get('grade_source_types') or {}).get(grade) or []))} |")
        lines += [
            "",
            "| 构件 | 体积m3 | 等级 | 来源 | 计入 | 需复核 |",
            "|---|---:|---|---|---|---|",
        ]
        for row in item.get("rows") or []:
            excluded = row.get("treatment") in ("excluded-sublayer", "exclude")
            lines.append(
                f"| {_md_cell(row.get('component'))} | {_md_cell(row.get('volume_m3'))} | "
                f"{_md_cell(row.get('grade'))} | {_md_cell(row.get('source_type'))} | "
                f"{'否' if excluded else '是'} | {'是' if row.get('needs_review') else '否'} |")
    lines += [
        "",
        "## 边界",
        "",
        *(f"- **口径声明**：{row}" for row in (report.get("caveats") or [])),
        "- `formal_ready=false` 时不得把候选合计作为正式混凝土量。",
        "- 钢筋型号和根数是图面识别/构件型数候选，不是下料重量。",
        "- 板洞口只有成环图线参与扣减；待复核图线只给上限，不扣板面积。",
        "- 梁净跨、板洞口、材料体系和边缘构件空间闭合未通过前，梁钢筋翻样不开放。",
    ]
    return "\n".join(lines)


def csv_rows(report: dict[str, Any]) -> list[list[str]]:
    rows = [[
        "记录类型", "类别/型号", "编号", "尺寸/规格", "数量/根数",
        "长度mm", "面积m2", "体积m3", "状态", "详情",
    ]]
    for row in report.get("component_schedule") or []:
        rows.append([
            "构件规格", row["category"], row["code"], row["section"],
            str(row["estimated_count"]), _text(row.get("length_mm")), "",
            _text(row.get("concrete_candidate_m3")), row["status"],
            f"箍筋 {row.get('stirrup') or '-'}；纵筋 {row.get('longitudinal') or '-'}",
        ])
    for row in report.get("column_schedule") or []:
        rows.append([
            "柱规格", "柱", row["code"], row["section"],
            str(row["count"]), "", "", "", row["status"],
            f"箍筋 {row.get('stirrup') or '-'}；纵筋 {row.get('longitudinal') or '-'}",
        ])
    for row in report.get("rebar_schedule") or []:
        rows.append([
            "钢筋型号", row["kind"], row["model"], "", str(row["estimated_count"]),
            "", "", "", "identified-candidate", row["component_codes"],
        ])
    for row in report.get("slab_schedule") or []:
        opening_status = row.get("opening_status")
        opening_note = f"洞口 {row.get('opening_count', 0)} 个"
        if opening_status:
            opening_note += f"/{opening_status}"
        opening_note += f"；材料 {row.get('material_observation') or '-'}"
        rows.append([
            "板", "板", row["id"] or row["code"],
            f"h={row['thickness_mm']}" if row.get("thickness_mm") else "",
            "1", "", _text(row.get("area_m2")), _text(row.get("volume_m3")),
            row["status"],
            opening_note,
        ])
    for row in report.get("beam_schedule") or []:
        rows.append([
            "梁", "梁", row["code"], row["section"], "1",
            _text(row.get("clear_length_mm") or row.get("centerline_length_mm")),
            "", _text(row.get("clear_volume_m3") or row.get("gross_volume_m3")),
            row["quantity_status"], row["issue"],
        ])
    for gap in (report.get("closure_dashboard") or {}).get(
            "component_gaps") or []:
        if _text(gap.get("component")) != "广联达口径与算量范围":
            continue
        for row in gap.get("scope_rows") or []:
            rows.append([
                "算量范围", _text(row.get("bucket")),
                "清单内" if row.get("in_schedule") else "清单外",
                _text(row.get("cad_scope")), "1", "", "",
                _text(row.get("volume_m3")), _text(row.get("cad_scope")),
                _text(row.get("note")),
            ])
    for row in (report.get("concrete") or {}).get("comparisons") or []:
        rows.append([
            "混凝土分账", row["component"], "", row["scope"], "1",
            "", "", row["candidate_value_m3"], row["status"],
            f"对照 {row.get('reference_value_m3')}；"
            f"差异 {row.get('difference_m3')}",
        ])
    for row in (report.get("closure_dashboard") or {}).get("gates") or []:
        rows.append([
            "闭合门槛", row["title"] or row["id"], "", row.get("evidence"), "1",
            "", "", "", row.get("status") or "unknown", row.get("action"),
        ])
    for row in (report.get("closure_dashboard") or {}).get(
            "blocking_groups") or []:
        members = row.get("member_ids") or row.get("codes") or []
        rows.append([
            "阻断分组", row["area"], "、".join(map(str, members[:12])),
            "", str(row.get("count", 0)), "", "", "",
            row.get("status") or "blocking", "阻断分组统计",
        ])
    for row in report.get("anomalies") or []:
        rows.append([
            "异常", row["area"], row["member_id"] or row["code"], "",
            "1", "", "", "", row["status"],
            f"{row['severity']}；{row['message']}",
        ])
    for item in (report.get("supplemental_breakdown") or {}).values():
        if item.get("schema") != "cad-beam-reference-reconciliation/v0.1":
            continue
        for row in item.get("missing_by_code") or []:
            rows.append([
                "梁实例对账", "梁", row["code"],
                f"参考{row.get('reference_instance_count', 0)}实例；"
                f"缺{row.get('missing_equivalent_instance_count', 0)}",
                str(row.get("selected_equivalent_instance_count", 0)),
                "", "", _text(row.get("current_code_volume_m3")),
                row.get("status") or "missing-equivalent-instance",
                f"参考量 {row.get('reference_volume_m3')}",
            ])
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != BEAM_GAP_SCHEMA:
            continue
        audit_summary = item.get("summary") or {}
        for row in (item.get("gap_decomposition") or {}).get("components") or []:
            rows.append([
                "梁缺口分解", row.get("component"), "", row.get("note"), "", "",
                _text(row.get("reference_m3")), _text(row.get("difference_m3")),
                "attributed",
                f"参考 {row.get('reference_m3')} / 已定位 {row.get('located_m3')}",
            ])
        for row in item.get("search_targets") or []:
            rows.append([
                "梁检索目标", "梁", row.get("code"), row.get("section"), "",
                _text(row.get("needed_length_mm")), "",
                _text(row.get("missing_volume_m3")), "review-required",
                f"未归属同截面图线 {row.get('unassigned_candidate_count')} 条；"
                f"{row.get('prior_status')}",
            ])
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != BEAM_COVERAGE_SCHEMA:
            continue
        audit_summary = item.get("summary") or {}
        rows.append([
            "梁覆盖审计", "梁图层图线", "",
            f"窗口内 {audit_summary.get('in_frame_segment_count')} 条/"
            f"{audit_summary.get('in_frame_length_mm')} mm；"
            f"镜像 {audit_summary.get('mirrored_line_count')} 段/"
            f"平移 {audit_summary.get('duplicate_view_line_count')} 段",
            str(audit_summary.get("uncovered_in_frame_count", 0)), "",
            _text(audit_summary.get("uncovered_in_frame_length_mm")), "",
            "closed" if audit_summary.get("coverage_closed") else "review-required",
            f"覆盖率 {audit_summary.get('in_frame_coverage_ratio')}；"
            f"未解释 {audit_summary.get('residual_still_unexplained_m3')} m3",
        ])
        for row in item.get("candidates") or []:
            rows.append([
                "梁覆盖候选", "梁", "+".join(row.get("handles") or []),
                _text(row.get("view_zone")), _text(row.get("length_mm")),
                _text(row.get("width_mm")), _text(row.get("length_mm")),
                _text(row.get("volume_m3")), "review-required",
                f"假定高 {_text(row.get('assumed_height_mm'))} mm；"
                f"{_text(row.get('evidence'))}",
            ])
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != BEAM_ATTRIBUTION_SCHEMA:
            continue
        attr_summary = item.get("summary") or {}
        decomposition = item.get("residual_decomposition") or {}
        caliber = item.get("section_recheck") or {}
        rows.append([
            "梁候选归属", "梁实例", "",
            f"截面口径差 {caliber.get('run_recheck_delta_m3')} m3 / "
            f"不一致 {caliber.get('run_mismatch_count')} 条；"
            f"未归属 {decomposition.get('unattached_length_mm')} mm",
            str(attr_summary.get("no_coaxial_run_count", 0)), "",
            _text(attr_summary.get("unattached_candidate_m3")),
            _text(attr_summary.get("attached_to_existing_code_m3")),
            "closed" if decomposition.get("matches_identity")
            and not attr_summary.get("section_caliber_explains_gap")
            else "review-required",
            f"本图框无法解释 "
            f"{attr_summary.get('unexplained_by_this_frame_m3')} m3；"
            f"需跨图框 {attr_summary.get('under_code_count')} 个偏少编号",
        ])
        for row in item.get("candidate_attribution") or []:
            rows.append([
                "梁候选段", "梁", _text(row.get("handles")),
                _text(row.get("matched_code")) or "无同轴编号",
                _text(row.get("length_mm")), _text(row.get("width_mm")),
                _text(row.get("length_mm")),
                _text(row.get("candidate_volume_m3")),
                _text(row.get("status")),
                f"计入量 {_text(row.get('attributed_volume_m3'))} m3；"
                f"端头间隙 {_text(row.get('joint_gap_mm'))} mm；"
                f"轴偏 {_text(row.get('axis_offset_mm'))} mm；"
                f"证据 {_text(row.get('assignment_evidence')) or '无'}",
            ])
        for row in ((item.get("under_code_targets") or {}).get("codes") or []):
            rows.append([
                "梁跨图框目标", "梁", _text(row.get("code")),
                _text(row.get("reference_section")),
                _text(row.get("needed_length_mm")), "", "",
                _text(row.get("difference_m3")),
                _text(row.get("classification")), _text(row.get("action")),
            ])
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != BEAM_FRAME_INDEX_SCHEMA:
            continue
        index_summary = item.get("summary") or {}
        for key, count in sorted((index_summary.get("classification_counts")
                                  or {}).items()):
            rows.append([
                "梁图框归属", "梁", key, _text(
                    index_summary.get("frame_label_counts") and "整册"),
                str(count), "", "",
                _text((index_summary.get("classification_volume_m3") or {}).get(key)),
                "reference-only",
                f"整册 {index_summary.get('label_count')} 条标注/"
                f"{index_summary.get('frame_count')} 个图框",
            ])
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != BEAM_SPAN_CLOSURE_SCHEMA:
            continue
        closure_summary = item.get("summary") or {}
        rows.append([
            "梁净跨口径", "梁", "",
            f"中心线 {closure_summary.get('centerline_length_mm')} mm / "
            f"净长 {closure_summary.get('clear_length_mm')} mm / "
            f"推定端 {closure_summary.get('inferred_end_support_width_mm')} mm",
            str(closure_summary.get("beam_instance_count", 0)), "", "",
            _text(closure_summary.get("span_caliber_difference_m3")),
            "centerline-caliber-kept",
            f"与相交审计冲突 "
            f"{closure_summary.get('span_caliber_vs_intersection_conflict_m3')} m3",
        ])
        for row in item.get("code_closure") or []:
            rows.append([
                "梁长度定责", "梁", _text(row.get("code")),
                _text(row.get("verdict")),
                _text(row.get("model_beam_count")), "",
                _text(row.get("single_instance_deficit_mm")),
                _text(row.get("current_code_difference_m3")),
                _text(row.get("frame_classification")),
                _text(row.get("action")),
            ])
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != BEAM_MULTISPAN_SCHEMA:
            continue
        multi_summary = item.get("summary") or {}
        rows.append([
            "多跨梁续接", "梁", "",
            f"带宽≥2 共 {multi_summary.get('multispan_beam_count')} 根 / "
            f"续接 {multi_summary.get('continued_beam_count')} 根 / "
            f"缺口 {multi_summary.get('deficit_before_mm')}"
            f"→{multi_summary.get('deficit_after_mm')} mm",
            str(multi_summary.get("continued_beam_count", 0)), "",
            _text(multi_summary.get("added_axis_length_mm")),
            _text(multi_summary.get("added_volume_candidate_m3")),
            "candidate-only",
            f"闭合率 {multi_summary.get('deficit_closed_ratio')}；"
            "未回图确认不并入量",
        ])
        for row in item.get("beams") or []:
            rows.append([
                "多跨梁续接段", "梁", _text(row.get("code")),
                _text(row.get("beam_id")), _text(row.get("extensions")), "",
                _text(row.get("added_axis_length_mm")),
                _text(row.get("added_volume_candidate_m3")),
                _text(row.get("verdict")),
                f"现 {_text(row.get('current_centerline_mm'))} mm → "
                f"{_text(row.get('continued_centerline_mm'))} mm；剩余缺口 "
                f"{_text(row.get('remaining_deficit_mm'))} mm",
            ])
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != BEAM_DEDUP_SCHEMA:
            continue
        dedup_summary = item.get("summary") or {}
        overlap = item.get("run_self_overlap") or {}
        rows.append([
            "梁实例去重", "梁", "",
            f"模型梁 {dedup_summary.get('beam_count')} 根 vs run "
            f"{dedup_summary.get('run_count')} 条 / 配对 "
            f"{dedup_summary.get('matched_beam_count')} 根",
            str(dedup_summary.get("beam_only_count", 0)), "",
            _text(dedup_summary.get("beam_volume_m3")),
            _text(dedup_summary.get("double_count_volume_m3")),
            "candidate-only",
            f"模型梁净新增候选 "
            f"{_text(dedup_summary.get('model_beam_net_new_volume_m3'))} m3；"
            f"run 内部重叠 {overlap.get('pair_count')} 处/"
            f"{_text(overlap.get('overlapped_volume_m3'))} m3",
        ])
        for row in item.get("beam_only") or []:
            rows.append([
                "梁实例去重-无run梁", "梁", _text(row.get("code")),
                _text(row.get("beam_id")), "", "",
                _text(row.get("beam_length_mm")),
                _text(row.get("beam_volume_m3")),
                _text(row.get("beam_only_class")),
                "同编号未配对 run " + ("|".join(
                    row.get("unpaired_same_code_run_ids") or []) or "无"),
            ])
        for row in item.get("run_verdicts") or []:
            rows.append([
                "梁实例去重-未配对run", "梁", _text(row.get("code")),
                _text(row.get("run_id")), _text(row.get("orientation")), "",
                _text(row.get("length_mm")), _text(row.get("volume_m3")),
                _text(row.get("verdict")),
                "编号证据 " + _text(row.get("evidence")),
            ])
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != BEAM_CONFLICT_SCHEMA:
            continue
        conflict_summary = item.get("summary") or {}
        rows.append([
            "梁编号归属冲突", "梁", "",
            f"冲突 {conflict_summary.get('conflict_pair_count')} 对 / 涉及 run "
            f"{conflict_summary.get('conflict_run_count')} 条、模型梁 "
            f"{conflict_summary.get('conflict_beam_count')} 根",
            str(conflict_summary.get("conflict_pair_count", 0)), "",
            _text(conflict_summary.get("conflict_run_volume_m3")),
            _text(conflict_summary.get("double_count_risk_m3")),
            "label-adjudicated",
            "引线置信 " + json.dumps(
                conflict_summary.get("label_confidence_counts") or {},
                ensure_ascii=False),
        ])
        for row in item.get("conflicts") or []:
            rows.append([
                "梁编号归属冲突对", "梁", _text(row.get("run_code")),
                f'{row.get("run_id")} vs {row.get("beam_id")}='
                f'{row.get("beam_code")}', _text(row.get("orientation")), "",
                _text(row.get("overlap_mm")),
                _text(row.get("double_count_risk_m3")),
                f'{_text(row.get("verdict"))}/{_text(row.get("confidence"))}',
                "标注 " + ("|".join(row.get("label_leader_ids") or []) or "无")
                + "；回图 " + ",".join(str(value) for value in
                                       row.get("review_xy") or []),
            ])
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != SLAB_OPENING_SCHEMA:
            continue
        audit_summary = item.get("summary") or {}
        rows.append([
            "板洞口台账", "开洞图层图线", "",
            f"实体 {audit_summary.get('source_entity_count')}；"
            f"状态 {audit_summary.get('status_counts')}",
            str(audit_summary.get("confirmed_opening_count", 0)), "",
            _text(audit_summary.get("confirmed_opening_area_m2")), "",
            "closed" if audit_summary.get("openings_closed")
            else "evidence-audited",
            f"毛 {_text(audit_summary.get('gross_panel_area_m2'))} m2 / "
            f"净 {_text(audit_summary.get('net_panel_area_m2'))} m2；"
            f"待复核 {_text(audit_summary.get('review_required_count'))} 组",
        ])
        for row in item.get("review_records") or []:
            rows.append([
                "板待复核图线", "+".join(row.get("handles") or []),
                row.get("panel_id") or "", row.get("status"),
                str(row.get("segment_count", "")), "",
                _text(row.get("envelope_area_m2")),
                _text(row.get("potential_volume_upper_bound_m3")),
                "review-required", row.get("evidence") or "",
            ])
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) not in INTERSECTION_SCHEMAS:
            continue
        groups = (item.get("summary") or {}).get("groups") or {}
        for pair_type, group in sorted(groups.items()):
            rows.append([
                "构件相交审计", pair_type, "", "",
                str(group.get("overlap_count", 0)), "",
                _text(group.get("overlap_area_m2")),
                _text(group.get("potential_deduction_volume_m3")),
                "candidate-not-applied", "重叠汇总",
            ])
        for row in item.get("top_overlaps") or []:
            codes = row.get("codes") or row.get("member_ids") or ["", ""]
            rows.append([
                "构件相交审计", row.get("pair_type"), codes[0],
                codes[1] if len(codes) > 1 else "",
                "", "", _text(row.get("overlap_area_m2")),
                _text(row.get("potential_deduction_volume_m3")),
                row.get("confidence") or "potential",
                f"建议归属 {row.get('suggested_owner')}；"
                f"坐标 {row.get('overlap_bbox_mm')}",
            ])
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="合并 CAD 构件表、钢筋型号、梁板状态和混凝土分账")
    parser.add_argument("--model-json", required=True)
    parser.add_argument("--ledger-json")
    parser.add_argument("--scan-json")
    parser.add_argument("--beam-json")
    parser.add_argument("--supplement-json", action="append", default=[],
                        help="补充 JSON；可写 name=path，可重复")
    parser.add_argument("--floor-label", default="")
    parser.add_argument("--title", default="")
    parser.add_argument("--caveat", action="append", default=[],
                        help="口径声明（降级模式、缺输入等），写进报告边界一节")
    parser.add_argument("--format", default="all",
                        choices=["all", "json", "md", "csv"])
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()

    supplements: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(args.supplement_json, 1):
        if "=" in item:
            name, path = item.split("=", 1)
        else:
            path = item
            name = Path(path).stem or f"supplement-{index}"
        supplements[name] = _load_json(path)

    report = build_report(
        _load_json(args.model_json),
        _load_json(args.ledger_json),
        _load_json(args.scan_json),
        _load_json(args.beam_json),
        supplements,
        floor_label=args.floor_label,
        title=args.title,
        caveats=args.caveat,
    )
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.format in ("all", "json"):
        out.with_suffix(".json").write_text(
            json.dumps(report, ensure_ascii=False, indent=1),
            encoding="utf-8",
        )
    if args.format in ("all", "md"):
        out.with_suffix(".md").write_text(
            render_markdown(report), encoding="utf-8")
    if args.format in ("all", "csv"):
        with out.with_suffix(".csv").open(
                "w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerows(csv_rows(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
