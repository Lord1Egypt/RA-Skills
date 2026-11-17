#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Single-entry CAD quantity pipeline built on the existing audited scripts."""
from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass



import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import cad_quantity_report


SCHEMA = "cad-quantity-pipeline/v0.1"
SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
VENDOR_DIR = SKILL_DIR / "vendor"


def _find_cad_base() -> Path:
    env = os.environ.get("CAD_SKILL_DIR")
    candidates = [Path(env)] if env else []
    candidates += [SKILL_DIR.parent / "cad-file-reader",
                   *sorted(Path.home().glob(".workbuddy/skills/*/cad-file-reader")),
                   Path.home() / ".claude/skills/cad-file-reader",
                   Path.home() / ".codex/skills/cad-file-reader"]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    raise SystemExit("找不到底座技能 cad-file-reader：设 CAD_SKILL_DIR 指向它")


CAD_BASE_DIR = _find_cad_base()
BASE_SCRIPTS_DIR = CAD_BASE_DIR / "scripts"
BASE_VENDOR_DIR = CAD_BASE_DIR / "vendor"


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON 顶层必须是对象：{path}")
    return data


def _sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _artifact_details(paths: dict[str, str]) -> dict[str, dict[str, Any]]:
    details: dict[str, dict[str, Any]] = {}
    for name, raw_path in paths.items():
        if not raw_path:
            continue
        path = Path(raw_path)
        details[name] = {
            "path": raw_path,
            "exists": path.exists(),
            "size_bytes": path.stat().st_size if path.is_file() else None,
            "sha256": _sha256(path),
        }
    return details


def _has_text_records(path: Path) -> bool:
    try:
        return bool(_load_json(path).get("text_records"))
    except Exception:
        return False


def _resolve_detail(
        scan: Path,
        explicit: str | None,
        default: Path) -> Path | None:
    if explicit:
        return Path(explicit).expanduser().resolve()
    candidates = [
        scan.with_suffix(".detail.json"),
        scan.with_name(scan.stem + ".detail.json"),
        default,
    ]
    if _has_text_records(scan):
        candidates.insert(0, scan)
    for candidate in candidates:
        if _has_text_records(candidate):
            return candidate.resolve()
    return default


def _run(
        name: str,
        script: str,
        arguments: list[str],
        *,
        timeout_seconds: float,
        retries: int) -> dict[str, Any]:
    script_path = SCRIPTS_DIR / script
    if not script_path.exists():
        script_path = BASE_SCRIPTS_DIR / script
    if not script_path.exists():
        raise FileNotFoundError(f"缺少脚本：{script_path}")
    command = [sys.executable, str(script_path), *arguments]
    environment = os.environ.copy()
    current = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = os.pathsep.join(
        [str(SCRIPTS_DIR), str(BASE_SCRIPTS_DIR), str(VENDOR_DIR),
         str(BASE_VENDOR_DIR)]
        + ([current] if current else [])
    )
    started = time.time()
    attempts: list[dict[str, Any]] = []
    for attempt in range(1, retries + 2):
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                env=environment,
                cwd=str(SKILL_DIR),
            )
            stdout_tail = completed.stdout[-8000:]
            stderr_tail = completed.stderr[-8000:]
            attempts.append({
                "attempt": attempt,
                "returncode": completed.returncode,
                "stdout_tail": stdout_tail,
                "stderr_tail": stderr_tail,
            })
            if completed.returncode == 0:
                return {
                    "name": name,
                    "status": "ok",
                    "command": command,
                    "elapsed_seconds": round(time.time() - started, 3),
                    "attempts": attempts,
                }
        except subprocess.TimeoutExpired as exc:
            attempts.append({
                "attempt": attempt,
                "returncode": None,
                "stdout_tail": str(exc.stdout or "")[-8000:],
                "stderr_tail": (
                    str(exc.stderr or "")
                    + f"\n超时 {timeout_seconds:g}s"
                )[-8000:],
            })
    return {
        "name": name,
        "status": "failed",
        "command": command,
        "elapsed_seconds": round(time.time() - started, 3),
        "attempts": attempts,
    }


def _geometry_step(
        name: str,
        dwg: Path,
        scan: Path,
        detail: Path | None,
        label: str,
        out: Path,
        timeout_seconds: float,
        retries: int,
        bbox: str = "") -> dict[str, Any]:
    """几何展开：图名能自动定位图框就按图名，定位不了时必须显式给 bbox。"""
    detail_args = ["--detail", str(detail)] if detail else []
    arguments = [str(dwg), "--scan", str(scan), *detail_args]
    if str(bbox or "").strip():
        # 图框坐标可能是负数，argparse 必须用 --bbox=值 的形式传
        arguments += ["--bbox=" + str(bbox).strip()]
    arguments += [_opt("--floor-label", label), "--format", "all", "-o", str(out)]
    return _run(name, "cad_geometry.py", arguments,
                timeout_seconds=timeout_seconds, retries=retries)


def _opt(name: str, value: Any) -> str:
    """把 `--name value` 拼成单个 `--name=value` 参数。

    负楼层标签（如 `-1F`）作为独立列表元素传给子进程时，argparse 会把它当成
    选项而不是值，报 `argument --floor-label: expected one argument`——
    与 bbox 的负数问题同源（见 cad_geometry 调用处的 `--bbox=` 注释）。
    统一走等号形式，负值才能安全穿过。
    """
    return f"{name}={value}"


def _reused_step(name: str, source: Path, reason: str) -> dict[str, Any]:
    return {
        "name": name,
        "status": "reused",
        "reason": reason,
        "source": str(source.resolve()),
        "elapsed_seconds": 0.0,
        "attempts": [],
    }


def _step_stderr(step: dict[str, Any]) -> str:
    parts = []
    for attempt in step.get("attempts") or []:
        parts.append(str(attempt.get("stderr_tail") or ""))
    return "\n".join(parts)


def _skipped_step(name: str, reason: str) -> dict[str, Any]:
    """证据步骤缺输入时如实记账：不跑、不猜，报告里少一条门槛并写明原因。"""
    return {"name": name, "status": "skipped", "reason": reason,
            "elapsed_seconds": 0.0}


def _label_suffix(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8")).hexdigest()[:8]


def _write_manifest(manifest: dict[str, Any], out: Path) -> None:
    out.with_suffix(".json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    lines = [
        "# CAD 单入口算量流水线",
        "",
        f"- 状态：`{manifest.get('status')}`",
        f"- 图纸：`{manifest.get('floor', {}).get('beam_label') or '-'}`",
        f"- `formal_ready`：`{str(manifest.get('formal_ready')).lower()}`",
        f"- 输出目录：`{manifest.get('out_dir')}`",
        "",
        "## 步骤",
        "",
        "| 步骤 | 状态 | 秒 |",
        "|---|---|---:|",
    ]
    for step in manifest.get("steps") or []:
        lines.append(
            f"| {step.get('name')} | {step.get('status')} | "
            f"{step.get('elapsed_seconds', 0):.3f} |"
        )
    lines += [
        "",
        "## 产物",
        "",
        "| 名称 | 路径 |",
        "|---|---|",
    ]
    for name, path in (manifest.get("artifacts") or {}).items():
        lines.append(f"| {name} | `{path}` |")
    if manifest.get("error"):
        lines += ["", "## 错误", "", f"`{manifest['error']}`"]
    out.with_suffix(".md").write_text(
        "\n".join(lines), encoding="utf-8")


def _artifact_map(out: Path) -> dict[str, str]:
    return {
        "manifest_json": str(out.with_suffix(".json").resolve()),
        "manifest_md": str(out.with_suffix(".md").resolve()),
    }


def _copy_manifest_paths(
        artifacts: dict[str, str],
        scan: Path,
        detail: Path | None,
        beam_geometry: Path,
        support_geometry: Path,
        slab_geometry: Path,
        beam_objects: Path,
        model: Path,
        ledger: Path,
        report: Path,
        intersection: Path | None = None,
        slab_opening: Path | None = None,
        beam_gap: Path | None = None,
        beam_coverage: Path | None = None,
        beam_attribution: Path | None = None,
        frame_index: Path | None = None,
        span_closure: Path | None = None,
        multispan: Path | None = None,
        beam_dedup: Path | None = None,
        beam_conflict: Path | None = None,
        glodon_scope: Path | None = None,
        grade_ledger: Path | None = None) -> None:
    artifacts.update({
        "scan_json": str(scan.resolve()),
        "detail_json": str(detail.resolve()) if detail else "",
        "beam_geometry_dxf": str(beam_geometry.with_suffix(".dxf").resolve()),
        "beam_geometry_json": str(beam_geometry.with_suffix(".json").resolve()),
        "support_geometry_dxf": str(
            support_geometry.with_suffix(".dxf").resolve()),
        "slab_geometry_dxf": str(slab_geometry.with_suffix(".dxf").resolve()),
        "beam_objects_json": str(beam_objects.with_suffix(".json").resolve()),
        "structure_model_json": str(model.with_suffix(".json").resolve()),
        "concrete_ledger_json": str(ledger.with_suffix(".json").resolve()),
        "member_intersection_json": str(
            intersection.with_suffix(".json").resolve()) if intersection else "",
        "slab_opening_json": str(
            slab_opening.with_suffix(".json").resolve()) if slab_opening else "",
        "beam_gap_json": str(
            beam_gap.with_suffix(".json").resolve()) if beam_gap else "",
        "beam_coverage_json": str(
            beam_coverage.with_suffix(".json").resolve())
        if beam_coverage else "",
        "beam_candidate_attribution_json": str(
            beam_attribution.with_suffix(".json").resolve())
        if beam_attribution else "",
        "beam_frame_label_index_json": str(
            frame_index.with_suffix(".json").resolve()) if frame_index else "",
        "beam_span_closure_json": str(
            span_closure.with_suffix(".json").resolve())
        if span_closure else "",
        "beam_multispan_closure_json": str(
            multispan.with_suffix(".json").resolve()) if multispan else "",
        "beam_instance_dedup_json": str(
            beam_dedup.with_suffix(".json").resolve()) if beam_dedup else "",
        "beam_attribution_conflict_json": str(
            beam_conflict.with_suffix(".json").resolve())
        if beam_conflict else "",
        "glodon_indicator_scope_json": str(
            glodon_scope.with_suffix(".json").resolve())
        if glodon_scope else "",
        "concrete_grade_ledger_json": str(
            grade_ledger.with_suffix(".json").resolve())
        if grade_ledger else "",

        "quantity_report_json": str(report.with_suffix(".json").resolve()),
        "quantity_report_md": str(report.with_suffix(".md").resolve()),
        "quantity_report_csv": str(report.with_suffix(".csv").resolve()),
    })


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="从 DWG/DXF 一次生成几何、结构模型、混凝土分账和统一报告")
    parser.add_argument("--dwg", required=True, help="DWG/DXF 原始图纸")
    parser.add_argument("--scan", help="已有 cad_scan JSON；不传则自动扫描")
    parser.add_argument("--detail", help="已有 cad_scan detail JSON")
    parser.add_argument("--floor-label",
                        help="梁平法图框名称，如 二层梁平法施工图")
    parser.add_argument("--support-floor-label",
                        help="墙柱图框名称；默认与 --floor-label 相同")
    parser.add_argument("--slab-floor-label",
                        help="板图框名称；默认与 --floor-label 相同")
    parser.add_argument("--component-sheet", type=int)
    parser.add_argument("--slab-sheet", type=int)
    parser.add_argument("--out", required=True)
    parser.add_argument("--profile",
                        help="项目配置 JSON：图名与楼层映射、sheet 号、层高标高、"
                             "板厚、预制与等级规则文件路径等；命令行显式值优先")
    parser.add_argument("--cluster-mm", type=float, default=1500.0)
    parser.add_argument("--with-insert", action="store_true",
                        help="扫描时解码 INSERT 图框块，较慢但图框识别更稳")
    parser.add_argument("--timeout-seconds", type=float, default=1800.0)
    parser.add_argument("--retries", type=int, default=2,
                        help="失败后最多重试次数")
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--support-transform",
                        help="墙柱 DXF 到梁 DXF 的 dx,dy；默认在不同图框时 auto")
    parser.add_argument("--slab-transform",
                        help="板 DXF 到梁 DXF 的 dx,dy；默认在不同图框时 auto")
    parser.add_argument("--slab-thickness-mm", type=float)
    parser.add_argument("--slab-default-thickness-mm", type=float)
    parser.add_argument("--slab-hatch-source")
    parser.add_argument("--slab-hatch-rule", default="")
    parser.add_argument("--concrete-grade", default="")
    parser.add_argument("--elevation-mm", type=float)
    parser.add_argument("--story-height-mm", type=float)
    parser.add_argument("--assumed-end-support-width-mm",
                        type=float, default=0.0)
    parser.add_argument("--include-beam-intersections", action="store_true")
    parser.add_argument("--arbitrate-support-count", action="store_true")
    parser.add_argument("--endpoint-polygon-support-search-mm",
                        type=float, default=0.0)
    parser.add_argument("--reference", action="append", default=[],
                        help="广联达对照值，如 梁及连梁=32.6986")
    parser.add_argument("--reference-floor", default="")
    parser.add_argument("--floor-mapping-note", default="")
    parser.add_argument("--floor-mapping-source", default="")
    parser.add_argument("--ledger-report-title", default="")
    parser.add_argument("--prefab-dxf")
    parser.add_argument("--prefab-layer", default=r"S-PC-叠合板轮廓")
    parser.add_argument("--prefab-label-layer", default=r"S-PC-编号")
    parser.add_argument("--prefab-model-json")
    parser.add_argument("--prefab-transform", default="0,0")
    parser.add_argument("--prefab-gap-mm", type=float, default=5000.0)
    parser.add_argument("--prefab-reference-area-m2", type=float)
    parser.add_argument("--report-title", default="")
    parser.add_argument("--no-member-intersection-audit", action="store_true",
                        help="关闭构件相交重复计量审计")
    parser.add_argument("--intersection-phase20-json",
                        help="阶段二十连梁实例 JSON，用于连梁相交审计")
    parser.add_argument("--intersection-coupling-height-mm", type=float, default=500.0)
    parser.add_argument("--beam-gap-reconciliation-json",
                        help="梁编号参考对账 JSON，用于体积缺口归因")
    parser.add_argument("--beam-gap-endpoint-json",
                        help="梁端几何分级 JSON，随缺口归因一起展示")
    parser.add_argument("--beam-gap-volume-tolerance-m3", type=float, default=0.05)
    parser.add_argument("--beam-coverage-dxf", default=None,
                        help="梁图层覆盖审计用的几何 DXF，默认复用梁几何产物")
    parser.add_argument("--beam-coverage-residual-gap-m3", type=float, default=None,
                        help="覆盖审计对照的梁净缺口，默认取缺口归因结果")
    parser.add_argument("--beam-coverage-tolerance-m3", type=float, default=0.05,
                        help="覆盖审计未解释量的容差")
    parser.add_argument("--no-beam-gap-audit", action="store_true",
                        help="关闭梁体积缺口归因")
    parser.add_argument("--no-beam-coverage-audit", action="store_true",
                        help="关闭梁图层覆盖审计")
    parser.add_argument("--beam-candidate-reconciliation-json", default=None,
                        help="梁编号参考对账 JSON，缺省复用缺口归因的入参")
    parser.add_argument("--beam-candidate-joint-max-mm", type=float, default=400.0,
                        help="候选段归属实例时允许的最大端头间隙 mm")
    parser.add_argument("--beam-candidate-axis-tolerance-mm", type=float,
                        default=60.0, help="候选段归属实例时允许的最大轴偏 mm")
    parser.add_argument("--no-beam-candidate-attribution", action="store_true",
                        help="关闭梁候选段归属与截面口径复核")
    parser.add_argument("--frame-index-dxf", default=None,
                        help="整册展开 DXF，用于梁编号图框标签索引")
    parser.add_argument("--frame-index-target-frame", default=None,
                        help="目标图框名，缺省用 --floor-label")
    parser.add_argument("--span-closure-frame-index-json", default=None,
                        help="已有的梁编号图框标签索引 JSON，用于净跨口径对账")
    parser.add_argument("--no-beam-frame-index", action="store_true",
                        help="关闭梁编号图框标签索引")
    parser.add_argument("--no-beam-span-closure", action="store_true",
                        help="关闭梁净跨口径与支座扣减对账")
    parser.add_argument("--multispan-geometry-dxf", default=None,
                        help="多跨梁续接用的梁图层 DXF，缺省复用梁几何产物")
    parser.add_argument("--no-beam-multispan-closure", action="store_true",
                        help="关闭多跨梁跨支座续接候选台账")
    parser.add_argument("--no-beam-instance-dedup", action="store_true",
                        help="关闭梁实例双口径去重（run 与模型梁判同一根物理梁）")
    parser.add_argument("--no-beam-attribution-conflict", action="store_true",
                        help="关闭梁编号归属冲突定责台账")
    parser.add_argument("--glodon-indicator-xlsx",
                        help="广联达模型云指标 xlsx；与按构件导出 JSON 成对提供，"
                             "用于清单口径分解与算量范围边界")
    parser.add_argument("--glodon-component-export-json",
                        help="广联达按构件分混凝土工程量导出结果 JSON")
    parser.add_argument("--no-glodon-scope", action="store_true",
                        help="关闭广联达清单口径分解与算量范围边界")
    parser.add_argument("--no-slab-opening-audit", action="store_true",
                        help="关闭板图层洞口证据审计")
    parser.add_argument("--slab-opening-dxf",
                        help="板平面图展开 DXF；缺省复用流水线板几何 DXF")
    parser.add_argument("--slab-opening-prior-json",
                        help="历史洞口候选 JSON（阶段八模型）")
    parser.add_argument("--slab-opening-closure-layers", default=None,
                        help="洞口闭合探测图层，逗号分隔")
    parser.add_argument("--reference-gap-m3", type=float,
                        help="CAD 候选合计与参考量差额，用于洞口一致性判定")
    parser.add_argument("--grade-rules-json",
                        help="混凝土强度等级规则 JSON（cad-concrete-grade-rules/v0.1）；"
                             "提供时流水线内自动出分标号台账并并入统一报告")
    parser.add_argument("--no-grade-ledger", action="store_true",
                        help="关闭流水线内的混凝土分标号台账步骤")
    parser.add_argument("--supplement-json", action="append", default=[],
                        help="补充模型 JSON；可写 name=path，可重复")
    parser.add_argument("--no-beam-centerline-support", action="store_true",
                        help="跳过梁实例中心线图面支撑校验")
    parser.add_argument("--centerline-geometry-dxf", default="",
                        help="实测梁线所在 DXF，缺省用本层梁几何展开结果")
    parser.add_argument("--beam-bbox", default="",
                        help="梁平法图框 x0,y0,x1,y1；图名自动定位失败时显式给出")
    parser.add_argument("--support-bbox", default="",
                        help="墙柱/柱平法图框 x0,y0,x1,y1；图名自动定位失败时显式给出")
    parser.add_argument("--slab-bbox", default="",
                        help="板平法图框 x0,y0,x1,y1；图名自动定位失败时显式给出")
    parser.add_argument("--overlap-verdict-json", default="",
                        help="人工重叠判读 JSON，用于与支撑校验交叉核对")
    parser.add_argument("--no-wall-edge-closeout", action="store_true",
                        help="跳过墙身空间闭合与特殊构件定档")
    parser.add_argument("--wall-geometry-json", default="",
                        help="墙身面域与边缘构件轮廓 JSON（含 planar_faces/"
                             "wall_strip_rectangles/edge_member_polygons）")
    parser.add_argument("--no-slab-thickness-partition", action="store_true",
                        help="跳过板厚三档子面域拆分")
    parser.add_argument("--slab-panel-texts-json", default="",
                        help="板图文字台账 JSON（带模型坐标），用于按归属复核直接标注")
    parser.add_argument("--slab-note-frame-bbox", default="",
                        help="结构说明所在图框窗口 x0,y0,x1,y1，用于取板厚规则句")
    parser.add_argument("--no-deduction-ledger", action="store_true",
                        help="跳过洞口与构件相交统一扣减台账")
    parser.add_argument("--deduction-verdict-json", default="",
                        help="开洞看图结论 JSON（句柄+判定），缺省时该档为空")
    parser.add_argument("--deduction-sheet-json", default="",
                        help="报量表 JSON，用于核对同一笔洞口扣减是否重复入账")
    parser.add_argument("--deduction-remaining-gap-m3", type=float, default=0.0,
                        help="分账剩余不确定量，用于判断未入账洞口的量级")
    parser.add_argument("--no-prefab-expansion", action="store_true",
                        help="跳过预制底板图面实例展开")
    parser.add_argument("--prefab-expanded-dxf", default="",
                        help="整册展开 DXF（预制底板图框所在），缺省用 --prefab-dxf")
    parser.add_argument("--prefab-material-ledger-json", default="",
                        help="叠合板材料分账 JSON，取逐编号模型块数与单块面积")
    parser.add_argument("--no-single-sheet-fallback", action="store_true",
                        help="多图框配准失败时不许退回单图框模式（默认允许并记降级）")
    parser.add_argument("--slab-notes-json", default="",
                        help="板厚规则句 JSON（图例句与整板默认档句，含句柄与坐标）")
    parser.add_argument("--prefab-frame-title-key", default="预制底板平面布置图")
    parser.add_argument("--prefab-title-key", action="append", default=[],
                        help="预制图框图名关键字，可重复")



    return parser
PROFILE_KEYS = (
    "floor_label", "support_floor_label", "slab_floor_label",
    "component_sheet", "slab_sheet", "cluster_mm", "with_insert",
    "support_transform", "slab_transform", "slab_thickness_mm",
    "slab_default_thickness_mm", "slab_hatch_source", "slab_hatch_rule",
    "concrete_grade", "elevation_mm", "story_height_mm",
    "assumed_end_support_width_mm", "reference_floor", "floor_mapping_note",
    "floor_mapping_source", "prefab_dxf", "prefab_layer", "prefab_label_layer",
    "prefab_model_json", "prefab_transform", "prefab_gap_mm",
    "prefab_reference_area_m2", "grade_rules_json", "reference",
    "intersection_phase20_json", "beam_gap_reconciliation_json",
    "beam_gap_endpoint_json", "beam_coverage_dxf", "frame_index_dxf",
    "frame_index_target_frame", "span_closure_frame_index_json",
    "multispan_geometry_dxf", "slab_opening_dxf", "slab_opening_prior_json",
    "slab_opening_closure_layers", "glodon_indicator_xlsx",
    "glodon_component_export_json",
    "centerline_geometry_dxf", "overlap_verdict_json", "wall_geometry_json",
    "slab_panel_texts_json", "slab_note_frame_bbox", "deduction_verdict_json",
    "deduction_sheet_json", "deduction_remaining_gap_m3", "prefab_expanded_dxf",
    "prefab_material_ledger_json", "prefab_title_key", "slab_notes_json",
    "beam_bbox", "support_bbox", "slab_bbox",
)


def load_profile(path: str) -> dict:
    data = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("项目配置必须是 JSON 对象")
    return {key: value for key, value in data.items()
            if key not in ("schema", "notes", "grade_regions")}


def apply_profile(args: argparse.Namespace, parser: argparse.ArgumentParser,
                  profile: dict) -> list[str]:
    """命令行显式给过的值优先，其次项目配置，最后内置默认。"""
    applied = []
    for key, value in profile.items():
        if key not in PROFILE_KEYS:
            continue
        if not hasattr(args, key):
            continue
        if getattr(args, key) != parser.get_default(key):
            continue  # 命令行已经显式给过
        setattr(args, key, value)
        applied.append(key)
    args.profile_applied = applied
    return applied


def parse_args() -> argparse.Namespace:
    parser = build_parser()
    args = parser.parse_args()
    if args.profile:
        path = Path(args.profile).expanduser()
        if not path.exists():
            raise SystemExit(f"项目配置文件不存在：{path}")
        apply_profile(args, parser, load_profile(str(path)))
    else:
        args.profile_applied = []
    return args


def main() -> int:
    args = parse_args()
    # s9 起：历史 advanced pipeline（本技能内展开 DXF 再建模）彻底停用，
    # 不提供任何环境变量逃生。正式链路：cad-file-reader 出 cad-contract/v1 → qty_core.py。
    print("[cad_quantity_pipeline] 历史 advanced pipeline 已删除（含直读层），没有逃生开关。\n"
          "正式链路：cad-file-reader 产出 cad-contract/v1 → qty_core.py（本技能不解析 DWG/DXF）。",
          file=sys.stderr)
    return 23
    if not str(args.floor_label or "").strip():
        raise SystemExit("必须给 --floor-label，或在 --profile 项目配置里写 floor_label")
    dwg = Path(args.dwg).expanduser().resolve()
    if not dwg.exists():
        print(f"图纸不存在：{dwg}", file=sys.stderr)
        return 2

    out_dir = Path(args.out).expanduser().resolve()
    scan = Path(args.scan).expanduser().resolve() if args.scan else (
        out_dir / "cad_scan.json")
    detail_candidate = out_dir / "cad_scan.detail.json"
    detail = _resolve_detail(scan, args.detail, detail_candidate)
    beam_geometry = out_dir / "beam_geometry"
    support_label = args.support_floor_label or args.floor_label
    slab_label = args.slab_floor_label or args.floor_label
    support_geometry = out_dir / (
        "support_geometry_" + _label_suffix(support_label))
    slab_geometry = out_dir / (
        "slab_geometry_" + _label_suffix(slab_label))
    beam_objects = out_dir / "beam_objects"
    model = out_dir / "structure_model"
    ledger = out_dir / "concrete_ledger"
    intersection = out_dir / "member_intersection_audit"
    slab_opening = out_dir / "slab_opening_audit"
    beam_gap = out_dir / "beam_gap_attribution"
    beam_coverage = out_dir / "beam_coverage_audit"
    beam_attribution = out_dir / "beam_candidate_attribution"
    frame_index = out_dir / "beam_frame_label_index"
    span_closure = out_dir / "beam_span_closure"
    multispan = out_dir / "beam_multispan_closure"
    beam_dedup = out_dir / "beam_instance_dedup"
    beam_conflict = out_dir / "beam_attribution_conflict"
    glodon_scope = out_dir / "glodon_indicator_scope"
    grade_ledger = out_dir / "concrete_grade_ledger"
    centerline = out_dir / "beam_centerline_support"
    wall_closeout = out_dir / "wall_edge_closeout"
    slab_partition = out_dir / "slab_thickness_partition"
    deduction = out_dir / "deduction_ledger"
    prefab_expansion = out_dir / "prefab_instance_expansion"
    report = out_dir / "quantity_report"
    manifest_path = out_dir / "pipeline_manifest"
    manifest: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "running",
        "floor": {
            "beam_label": args.floor_label,
            "support_label": (
                args.support_floor_label or args.floor_label),
            "slab_label": args.slab_floor_label or args.floor_label,
            "component_sheet": args.component_sheet,
            "slab_sheet": args.slab_sheet,
        },
        "inputs": {
            "dwg": str(dwg),
            "profile": args.profile or "",
            "profile_applied_keys": list(getattr(args, "profile_applied", [])),
            "scan": str(scan) if args.scan else None,
            "detail": str(detail) if detail else None,
        },
        "out_dir": str(out_dir),
        "steps": [],
        "artifacts": {},
        "formal_ready": False,
        "error": "",
    }
    out_dir.mkdir(parents=True, exist_ok=True)

    support_transform = (
        args.support_transform
        or ("auto" if support_label != args.floor_label else "0,0")
    )
    slab_transform = (
        args.slab_transform
        or ("auto" if slab_label != args.floor_label else "0,0")
    )

    try:
        if args.scan:
            if not scan.exists():
                raise FileNotFoundError(str(scan))
            manifest["steps"].append(_reused_step(
                "scan", scan, "使用已有 cad_scan JSON"))
        else:
            scan_args = [
                str(dwg),
                "--with-mtext",
                "--with-geom",
                "--with-geom-layer",
                "--cluster", str(args.cluster_mm),
                "--spec-table",
                "--detail-json", str(detail),
                "--format", "json",
                "-o", str(scan.with_suffix("")),
            ]
            if args.with_insert:
                scan_args.insert(2, "--with-insert")
            if args.plan_only:
                manifest["status"] = "planned"
                manifest["steps"].append({
                    "name": "scan",
                    "status": "planned",
                    "command": [
                        sys.executable,
                        str(SCRIPTS_DIR / "cad_scan.py") if (SCRIPTS_DIR / "cad_scan.py").exists() else str(BASE_SCRIPTS_DIR / "cad_scan.py"),
                        *scan_args,
                    ],
                    "elapsed_seconds": 0.0,
                })
            else:
                step = _run(
                    "scan",
                    "cad_scan.py",
                    scan_args,
                    timeout_seconds=args.timeout_seconds,
                    retries=max(0, args.retries),
                )
                manifest["steps"].append(step)
                if step["status"] != "ok":
                    raise RuntimeError("CAD 扫描失败")

        if args.plan_only:
            manifest["status"] = "planned"
            manifest["artifacts"] = _artifact_map(manifest_path)
            _write_manifest(manifest, manifest_path)
            return 0

        beam_step = _geometry_step(
            "beam-geometry",
            dwg,
            scan,
            detail if detail and detail.exists() else None,
            args.floor_label,
            beam_geometry,
            args.timeout_seconds,
            max(0, args.retries),
            args.beam_bbox,
        )
        manifest["steps"].append(beam_step)
        if beam_step["status"] != "ok":
            raise RuntimeError("梁几何展开失败")

        if support_label == args.floor_label and not args.support_bbox:
            support_step = _reused_step(
                "support-geometry",
                beam_geometry,
                "墙柱图框与梁图框相同，复用梁几何",
            )
            # 必须把变量也重指向：下游 --support-dxf 取的是 support_geometry，
            # 只记一条 reused 而不改路径，就会去打开一个从未生成的
            # support_geometry_<hash>.dxf，报 FileNotFoundError。
            support_geometry = beam_geometry
        else:
            support_step = _geometry_step(
                "support-geometry",
                dwg,
                scan,
                detail if detail and detail.exists() else None,
                support_label,
                support_geometry,
                args.timeout_seconds,
                max(0, args.retries),
                args.support_bbox,
            )
        manifest["steps"].append(support_step)
        if support_step["status"] not in ("ok", "reused"):
            raise RuntimeError("墙柱几何展开失败")

        if slab_label == args.floor_label and not args.slab_bbox:
            slab_step = _reused_step(
                "slab-geometry",
                beam_geometry,
                "板图框与梁图框相同，复用梁几何",
            )
            # 同 support_geometry：--slab-dxf/--opening-dxf 都取这个变量
            slab_geometry = beam_geometry
        else:
            slab_step = _geometry_step(
                "slab-geometry",
                dwg,
                scan,
                detail if detail and detail.exists() else None,
                slab_label,
                slab_geometry,
                args.timeout_seconds,
                max(0, args.retries),
                args.slab_bbox,
            )
        manifest["steps"].append(slab_step)
        if slab_step["status"] not in ("ok", "reused"):
            raise RuntimeError("板几何展开失败")

        beam_objects_step = _run(
            "beam-objects",
            "cad_beam_objects.py",
            [
                "--dxf", str(beam_geometry.with_suffix(".dxf")),
                "--scan", str(scan),
                *(["--detail", str(detail)]
                  if detail and detail.exists() else []),
                _opt("--floor-label", args.floor_label),
                "--run-registry",
                "--format", "all",
                "-o", str(beam_objects),
            ],
            timeout_seconds=args.timeout_seconds,
            retries=max(0, args.retries),
        )
        manifest["steps"].append(beam_objects_step)
        if beam_objects_step["status"] != "ok":
            raise RuntimeError("梁对象生成失败")

        support_dxf = support_geometry.with_suffix(".dxf")
        slab_dxf = slab_geometry.with_suffix(".dxf")
        model_args = [
            "--beam-json", str(beam_objects.with_suffix(".json")),
            "--beam-dxf", str(beam_geometry.with_suffix(".dxf")),
            "--support-dxf", str(support_dxf),
            "--slab-dxf", str(slab_dxf),
            "--opening-dxf", str(slab_dxf),
            *(
                ["--text-json", str(detail)]
                if detail and detail.exists() else []
            ),
            "--support-transform", support_transform,
            "--slab-transform", slab_transform,
            _opt("--floor-label", args.floor_label),
            "--format", "all",
            "-o", str(model),
        ]
        if args.component_sheet is not None:
            model_args += ["--component-sheet", str(args.component_sheet)]
        if args.slab_sheet is not None:
            model_args += ["--slab-sheet", str(args.slab_sheet)]
        if args.slab_thickness_mm is not None:
            model_args += [
                "--slab-thickness-mm", str(args.slab_thickness_mm)]
        if args.slab_default_thickness_mm is not None:
            model_args += [
                "--slab-default-thickness-mm",
                str(args.slab_default_thickness_mm),
            ]
        if args.slab_hatch_source:
            model_args += [
                "--slab-hatch-source", args.slab_hatch_source]
        if args.slab_hatch_rule:
            model_args += ["--slab-hatch-rule", args.slab_hatch_rule]
        if args.concrete_grade:
            model_args += ["--concrete-grade", args.concrete_grade]
        if args.elevation_mm is not None:
            model_args += ["--elevation-mm", str(args.elevation_mm)]
        if args.story_height_mm is not None:
            model_args += [
                "--story-height-mm", str(args.story_height_mm)]
        if args.assumed_end_support_width_mm:
            model_args += [
                "--assumed-end-support-width-mm",
                str(args.assumed_end_support_width_mm),
            ]
        if args.include_beam_intersections:
            model_args.append("--include-beam-intersections")
        if args.arbitrate_support_count:
            model_args.append("--arbitrate-support-count")
        if args.endpoint_polygon_support_search_mm:
            model_args += [
                "--endpoint-polygon-support-search-mm",
                str(args.endpoint_polygon_support_search_mm),
            ]
        model_step = _run(
            "structure-model",
            "cad_structure_model.py",
            model_args,
            timeout_seconds=args.timeout_seconds,
            retries=max(0, args.retries),
        )
        manifest["steps"].append(model_step)
        if (model_step["status"] != "ok"
                and not args.no_single_sheet_fallback
                and "自动配准失败" in _step_stderr(model_step)):
            # 跨图框配准失败时退回单图框：柱墙与板都从梁图取，宁缺勿错配
            degraded = list(model_args)
            beam_dxf_path = str(beam_geometry.with_suffix(".dxf"))
            for key in ("--support-dxf", "--slab-dxf", "--opening-dxf"):
                index = degraded.index(key)
                degraded[index + 1] = beam_dxf_path
            for key in ("--support-transform", "--slab-transform"):
                index = degraded.index(key)
                degraded[index + 1] = "0,0"
            retry = _run(
                "structure-model-single-sheet", "cad_structure_model.py",
                degraded, timeout_seconds=args.timeout_seconds,
                retries=max(0, args.retries))
            manifest["steps"].append(retry)
            if retry["status"] == "ok":
                model_step = retry
                support_geometry = beam_geometry
                slab_geometry = beam_geometry
                manifest["degraded_mode"] = (
                    "跨图框自动配准失败，已退回单图框模式：柱墙与板拓扑取自梁图图框，"
                    "板洞口与墙柱轮廓需按 --support-transform/--slab-transform 或"
                    " --support-bbox/--slab-bbox 校准后重跑才可用于正式量")
                manifest["warnings"] = [manifest["degraded_mode"]]
        if model_step["status"] != "ok":
            raise RuntimeError("结构模型生成失败")

        ledger_args = [
            "--model-json", str(model.with_suffix(".json")),
            "--format", "all",
            "-o", str(ledger),
        ]
        for reference in args.reference:
            ledger_args += ["--reference", reference]
        if args.reference_floor:
            ledger_args += ["--reference-floor", args.reference_floor]
        if args.floor_mapping_note:
            ledger_args += [
                "--floor-mapping-note", args.floor_mapping_note]
        if args.floor_mapping_source:
            ledger_args += [
                "--floor-mapping-source", args.floor_mapping_source]
        if args.ledger_report_title:
            ledger_args += [
                "--report-title", args.ledger_report_title]
        if args.prefab_dxf:
            ledger_args += [
                "--prefab-dxf", args.prefab_dxf,
                "--prefab-layer", args.prefab_layer,
                "--prefab-label-layer", args.prefab_label_layer,
                "--prefab-transform", args.prefab_transform,
                "--prefab-gap-mm", str(args.prefab_gap_mm),
            ]
        if args.prefab_model_json:
            ledger_args += [
                "--prefab-model-json", args.prefab_model_json]
        if args.prefab_reference_area_m2 is not None:
            ledger_args += [
                "--prefab-reference-area-m2",
                str(args.prefab_reference_area_m2),
            ]
        ledger_step = _run(
            "concrete-ledger",
            "cad_concrete_ledger.py",
            ledger_args,
            timeout_seconds=args.timeout_seconds,
            retries=max(0, args.retries),
        )
        manifest["steps"].append(ledger_step)
        if ledger_step["status"] != "ok":
            raise RuntimeError("混凝土分账失败")

        if args.no_member_intersection_audit:
            intersection_step = {
                "name": "member-intersection-audit",
                "status": "skipped",
                "reason": "用户选择关闭",
                "elapsed_seconds": 0.0,
                "attempts": [],
            }
        else:
            model_data = _load_json(model.with_suffix(".json"))
            model_story_height = (model_data.get("floor") or {}).get(
                "story_height_mm")
            try:
                model_story_height = float(model_story_height or 0.0)
            except (TypeError, ValueError):
                model_story_height = 0.0
            story_height = (
                args.story_height_mm or model_story_height or 3870.0)
            intersection_args = [
                "--model-json", str(model.with_suffix(".json")),
                "--ledger-json", str(ledger.with_suffix(".json")),
                "--story-height-mm", str(story_height),
                "--coupling-height-mm", str(args.intersection_coupling_height_mm),
                "-o", str(intersection),
            ]
            if args.intersection_phase20_json:
                intersection_args += [
                    "--phase20-json", args.intersection_phase20_json]
            intersection_step = _run(
                "member-intersection-audit",
                "cad_member_intersection_audit.py",
                intersection_args,
                timeout_seconds=args.timeout_seconds,
                retries=max(0, args.retries),
            )
        manifest["steps"].append(intersection_step)
        if intersection_step["status"] not in ("ok", "skipped"):
            raise RuntimeError("构件相交重复计量审计失败")

        opening_source = Path(
            args.slab_opening_dxf
            or slab_geometry.with_suffix(".dxf")).expanduser()
        if args.no_slab_opening_audit:
            slab_opening_step = {
                "name": "slab-opening-audit",
                "status": "skipped",
                "reason": "用户选择关闭",
                "elapsed_seconds": 0.0,
                "attempts": [],
            }
        elif not opening_source.exists():
            slab_opening_step = {
                "name": "slab-opening-audit",
                "status": "skipped",
                "reason": f"未找到板几何 DXF：{opening_source}",
                "elapsed_seconds": 0.0,
                "attempts": [],
            }
        else:
            opening_args = [
                "--model-json", str(model.with_suffix(".json")),
                "--geometry-dxf", str(opening_source),
                "-o", str(slab_opening),
            ]
            if args.slab_opening_prior_json:
                opening_args += [
                    "--prior-json", args.slab_opening_prior_json]
            if args.slab_opening_closure_layers:
                opening_args += [
                    "--closure-layers", args.slab_opening_closure_layers]
            if args.reference_gap_m3 is not None:
                opening_args += [
                    "--reference-gap-m3", str(args.reference_gap_m3)]
            slab_opening_step = _run(
                "slab-opening-audit",
                "cad_slab_opening_audit.py",
                opening_args,
                timeout_seconds=args.timeout_seconds,
                retries=max(0, args.retries),
            )
        manifest["steps"].append(slab_opening_step)
        if slab_opening_step["status"] not in ("ok", "skipped"):
            raise RuntimeError("板洞口证据审计失败")

        if args.no_beam_gap_audit:
            beam_gap_step = {
                "name": "beam-gap-attribution",
                "status": "skipped",
                "reason": "用户选择关闭",
                "elapsed_seconds": 0.0,
                "attempts": [],
            }
        elif not args.beam_gap_reconciliation_json:
            beam_gap_step = {
                "name": "beam-gap-attribution",
                "status": "skipped",
                "reason": "未提供 --beam-gap-reconciliation-json",
                "elapsed_seconds": 0.0,
                "attempts": [],
            }
        else:
            gap_args = [
                "--reconciliation-json", args.beam_gap_reconciliation_json,
                "--model-json", str(model.with_suffix(".json")),
                "--volume-tolerance-m3", str(args.beam_gap_volume_tolerance_m3),
                "-o", str(beam_gap),
            ]
            if args.beam_gap_endpoint_json:
                gap_args += ["--endpoint-json", args.beam_gap_endpoint_json]
            beam_gap_step = _run(
                "beam-gap-attribution",
                "cad_beam_gap_attribution.py",
                gap_args,
                timeout_seconds=args.timeout_seconds,
                retries=max(0, args.retries),
            )
        manifest["steps"].append(beam_gap_step)
        if beam_gap_step["status"] not in ("ok", "skipped"):
            raise RuntimeError("梁体积缺口归因失败")

        coverage_source = (
            Path(args.beam_coverage_dxf).expanduser()
            if args.beam_coverage_dxf else beam_geometry.with_suffix(".dxf"))
        if args.no_beam_coverage_audit:
            beam_coverage_step = {
                "name": "beam-coverage-audit",
                "status": "skipped",
                "reason": "用户选择关闭",
                "elapsed_seconds": 0.0,
                "attempts": [],
            }
        elif not coverage_source.exists():
            beam_coverage_step = {
                "name": "beam-coverage-audit",
                "status": "skipped",
                "reason": f"未找到梁几何 DXF：{coverage_source}",
                "elapsed_seconds": 0.0,
                "attempts": [],
            }
        else:
            residual_gap = args.beam_coverage_residual_gap_m3
            if residual_gap is None and beam_gap_step["status"] == "ok":
                gap_data = json.loads(
                    beam_gap.with_suffix(".json").read_text(encoding="utf-8"))
                residual_gap = float((gap_data.get("summary") or {}).get(
                    "residual_needing_new_geometry_m3") or 0.0)
            coverage_args = [
                "--model-json", str(model.with_suffix(".json")),
                "--geometry-dxf", str(coverage_source),
                "--unexplained-tolerance-m3", str(args.beam_coverage_tolerance_m3),
                "-o", str(beam_coverage),
            ]
            if residual_gap is not None:
                coverage_args += ["--residual-gap-m3", str(residual_gap)]
            beam_coverage_step = _run(
                "beam-coverage-audit",
                "cad_beam_coverage_audit.py",
                coverage_args,
                timeout_seconds=args.timeout_seconds,
                retries=max(0, args.retries),
            )
        manifest["steps"].append(beam_coverage_step)
        if beam_coverage_step["status"] not in ("ok", "skipped"):
            raise RuntimeError("梁图层覆盖审计失败")

        candidate_recon = (
            Path(args.beam_candidate_reconciliation_json).expanduser()
            if args.beam_candidate_reconciliation_json
            else (Path(args.beam_gap_reconciliation_json).expanduser()
                  if args.beam_gap_reconciliation_json else None))
        skipped = {"elapsed_seconds": 0.0, "attempts": []}
        if args.no_beam_candidate_attribution:
            beam_attribution_step = dict(
                skipped, name="beam-candidate-attribution", status="skipped",
                reason="用户选择关闭")
        elif beam_coverage_step["status"] != "ok":
            beam_attribution_step = dict(
                skipped, name="beam-candidate-attribution", status="skipped",
                reason="梁图层覆盖审计未运行")
        elif not candidate_recon or not candidate_recon.exists():
            beam_attribution_step = dict(
                skipped, name="beam-candidate-attribution", status="skipped",
                reason="未提供梁编号参考对账 JSON")
        else:
            attribution_args = [
                "--model-json", str(model.with_suffix(".json")),
                "--coverage-json", str(beam_coverage.with_suffix(".json")),
                "--reconciliation-json", str(candidate_recon),
                "--axis-tolerance-mm",
                str(args.beam_candidate_axis_tolerance_mm),
                "--joint-max-mm", str(args.beam_candidate_joint_max_mm),
                _opt("--floor-label", args.floor_label),
                "-o", str(beam_attribution),
            ]
            if beam_gap_step["status"] == "ok":
                attribution_args += [
                    "--gap-json", str(beam_gap.with_suffix(".json"))]
            beam_attribution_step = _run(
                "beam-candidate-attribution",
                "cad_beam_candidate_attribution.py",
                attribution_args,
                timeout_seconds=args.timeout_seconds,
                retries=max(0, args.retries),
            )
        manifest["steps"].append(beam_attribution_step)
        if beam_attribution_step["status"] not in ("ok", "skipped"):
            raise RuntimeError("梁候选段归属复核失败")

        frame_index_source = (
            Path(args.frame_index_dxf).expanduser()
            if args.frame_index_dxf else None)
        frame_index_ready = frame_json = None
        if args.no_beam_frame_index:
            frame_index_step = dict(
                skipped, name="beam-frame-label-index", status="skipped",
                reason="用户选择关闭")
        elif not frame_index_source or not frame_index_source.exists():
            frame_index_step = dict(
                skipped, name="beam-frame-label-index", status="skipped",
                reason="未提供整册展开 DXF（--frame-index-dxf）")
        elif not args.beam_gap_reconciliation_json:
            frame_index_step = dict(
                skipped, name="beam-frame-label-index", status="skipped",
                reason="未提供梁编号参考对账 JSON")
        else:
            frame_index_step = _run(
                "beam-frame-label-index",
                "cad_beam_frame_label_index.py",
                ["--geometry-dxf", str(frame_index_source),
                 "--reconciliation-json",
                 args.beam_gap_reconciliation_json,
                 "--target-frame",
                 args.frame_index_target_frame or args.floor_label,
                 "-o", str(frame_index)],
                timeout_seconds=args.timeout_seconds,
                retries=max(0, args.retries),
            )
            if frame_index_step["status"] == "ok":
                frame_index_ready = frame_index
                frame_json = str(frame_index.with_suffix(".json"))
        manifest["steps"].append(frame_index_step)
        if frame_index_step["status"] not in ("ok", "skipped"):
            raise RuntimeError("梁编号图框标签索引失败")

        span_frame_json = (
            Path(args.span_closure_frame_index_json).expanduser()
            if args.span_closure_frame_index_json
            else (Path(frame_json) if frame_json else None))
        if args.no_beam_span_closure:
            span_closure_step = dict(
                skipped, name="beam-span-closure", status="skipped",
                reason="用户选择关闭")
        elif not span_frame_json or not span_frame_json.exists():
            span_closure_step = dict(
                skipped, name="beam-span-closure", status="skipped",
                reason="缺少梁编号图框标签索引 JSON")
        else:
            span_args = [
                "--model-json", str(model.with_suffix(".json")),
                "--reconciliation-json", args.beam_gap_reconciliation_json,
                "--frame-index-json", str(span_frame_json),
                _opt("--floor-label", args.floor_label),
                "-o", str(span_closure),
            ]
            if intersection_step["status"] == "ok":
                span_args += [
                    "--intersection-json", str(intersection.with_suffix(".json"))]
            span_closure_step = _run(
                "beam-span-closure", "cad_beam_span_closure.py", span_args,
                timeout_seconds=args.timeout_seconds,
                retries=max(0, args.retries),
            )
        manifest["steps"].append(span_closure_step)
        if span_closure_step["status"] not in ("ok", "skipped"):
            raise RuntimeError("梁净跨口径与支座扣减对账失败")

        multispan_source = (
            Path(args.multispan_geometry_dxf).expanduser()
            if args.multispan_geometry_dxf else beam_geometry.with_suffix(".dxf"))
        if args.no_beam_multispan_closure:
            multispan_step = dict(
                skipped, name="beam-multispan-closure", status="skipped",
                reason="用户选择关闭")
        elif not args.beam_gap_reconciliation_json:
            multispan_step = dict(
                skipped, name="beam-multispan-closure", status="skipped",
                reason="未提供梁编号参考对账 JSON")
        elif not multispan_source.exists():
            multispan_step = dict(
                skipped, name="beam-multispan-closure", status="skipped",
                reason=f"未找到梁图层 DXF：{multispan_source}")
        else:
            multispan_step = _run(
                "beam-multispan-closure", "cad_beam_multispan_closure.py",
                ["--model-json", str(model.with_suffix(".json")),
                 "--geometry-dxf", str(multispan_source),
                 "--reconciliation-json", args.beam_gap_reconciliation_json,
                 "-o", str(multispan)],
                timeout_seconds=args.timeout_seconds,
                retries=max(0, args.retries),
            )
        manifest["steps"].append(multispan_step)
        if multispan_step["status"] not in ("ok", "skipped"):
            raise RuntimeError("多跨梁跨支座续接候选失败")

        if args.no_beam_instance_dedup:
            dedup_step = dict(
                skipped, name="beam-instance-dedup", status="skipped",
                reason="用户选择关闭")
        else:
            dedup_step = _run(
                "beam-instance-dedup", "cad_beam_instance_dedup.py",
                ["--model-json", str(model.with_suffix(".json")),
                 _opt("--floor-label", args.floor_label),
                 "-o", str(beam_dedup)],
                timeout_seconds=args.timeout_seconds,
                retries=max(0, args.retries),
            )
        manifest["steps"].append(dedup_step)
        if dedup_step["status"] not in ("ok", "skipped"):
            raise RuntimeError("梁实例双口径去重失败")

        if args.no_beam_attribution_conflict:
            conflict_step = dict(
                skipped, name="beam-attribution-conflict", status="skipped",
                reason="用户选择关闭")
        else:
            conflict_step = _run(
                "beam-attribution-conflict",
                "cad_beam_attribution_conflict.py",
                ["--model-json", str(model.with_suffix(".json")),
                 _opt("--floor-label", args.floor_label),
                 "-o", str(beam_conflict)],
                timeout_seconds=args.timeout_seconds,
                retries=max(0, args.retries),
            )
        manifest["steps"].append(conflict_step)
        if conflict_step["status"] not in ("ok", "skipped"):
            raise RuntimeError("梁编号归属冲突定责失败")

        if args.no_glodon_scope:
            glodon_step = dict(
                skipped, name="glodon-indicator-scope", status="skipped",
                reason="用户选择关闭")
        elif bool(args.glodon_indicator_xlsx) != bool(
                args.glodon_component_export_json):
            glodon_step = dict(
                skipped, name="glodon-indicator-scope", status="skipped",
                reason="指标 xlsx 与按构件导出 JSON 必须成对提供")
        elif not args.glodon_indicator_xlsx:
            glodon_step = dict(
                skipped, name="glodon-indicator-scope", status="skipped",
                reason="未提供广联达指标报表")
        else:
            scope_ledger = _load_json(ledger.with_suffix(".json")) \
                if ledger.with_suffix(".json").exists() else {}
            scope_concrete = dict(scope_ledger.get("concrete_ledger")
                                  or scope_ledger)
            scope_model = _load_json(model.with_suffix(".json")) \
                if model.with_suffix(".json").exists() else {}
            scope_slab = dict((scope_model.get("phase15") or {})
                              .get("summary") or {})
            glodon_step = _run(
                "glodon-indicator-scope",
                "cad_glb_indicator_scope.py",
                ["--indicator-xlsx", str(args.glodon_indicator_xlsx),
                 "--component-export-json",
                 str(args.glodon_component_export_json),
                 "--floor", args.floor_label,
                 "--reference-total-m3", str(float(
                     scope_concrete.get("reference_total_m3") or 0.0)),
                 "--cad-slab-volume-m3", str(float(
                     scope_slab.get("slab_rough_volume_m3") or 0.0)),
                 "--cad-beam-independent-m3", str(
                     float(scope_concrete.get("main_beam_cad_m3") or 0.0)
                     + float(scope_concrete.get("stair_beam_cad_m3") or 0.0)),
                 "--cad-vertical-candidate-m3", str(float(
                     scope_concrete.get("vertical_candidate_m3") or 0.0)),
                 "-o", str(glodon_scope)],
                timeout_seconds=args.timeout_seconds,
                retries=max(0, args.retries),
            )
        manifest["steps"].append(glodon_step)
        if glodon_step["status"] not in ("ok", "skipped"):
            raise RuntimeError("广联达清单口径分解失败")

        if args.no_grade_ledger:
            grade_step = dict(
                skipped, name="concrete-grade-ledger", status="skipped",
                reason="用户选择关闭")
        elif not args.grade_rules_json:
            grade_step = dict(
                skipped, name="concrete-grade-ledger", status="skipped",
                reason="未提供 --grade-rules-json 等级规则")
        elif not Path(args.grade_rules_json).expanduser().exists():
            grade_step = dict(
                skipped, name="concrete-grade-ledger", status="skipped",
                reason=f"等级规则文件不存在：{args.grade_rules_json}")
        else:
            grade_step = _run(
                "concrete-grade-ledger", "cad_concrete_grade.py",
                ["--rules-json",
                 str(Path(args.grade_rules_json).expanduser().resolve()),
                 "--ledger-report-json", str(ledger.with_suffix(".json")),
                 "-o", str(grade_ledger)],
                timeout_seconds=args.timeout_seconds,
                retries=max(0, args.retries),
            )
        manifest["steps"].append(grade_step)
        if grade_step["status"] not in ("ok", "skipped"):
            raise RuntimeError("混凝土分标号台账失败")

        # ---- 证据层：同一条命令内跑完，缺输入的如实记 skipped，不猜不补 ----
        run_kwargs = {"timeout_seconds": args.timeout_seconds,
                      "retries": max(0, args.retries)}
        evidence: dict[str, dict[str, Any]] = {}
        if args.no_beam_centerline_support:
            evidence["centerline"] = _skipped_step(
                "beam-centerline-support", "开关 --no-beam-centerline-support")
        else:
            cl_dxf = Path(args.centerline_geometry_dxf
                          or str(beam_geometry.with_suffix(".dxf")))
            if not cl_dxf.exists():
                evidence["centerline"] = _skipped_step(
                    "beam-centerline-support", f"缺实测梁线 DXF：{cl_dxf}")
            else:
                cl_args = ["--model-json", str(model.with_suffix(".json")),
                           "--geometry-dxf", str(cl_dxf)]
                if args.overlap_verdict_json and Path(
                        args.overlap_verdict_json).exists():
                    cl_args += ["--overlap-verdict-json",
                                args.overlap_verdict_json]
                evidence["centerline"] = _run(
                    "beam-centerline-support",
                    "cad_beam_centerline_support.py",
                    cl_args + ["-o", str(centerline)], **run_kwargs)
        if args.no_wall_edge_closeout:
            evidence["wall_closeout"] = _skipped_step(
                "wall-edge-closeout", "开关 --no-wall-edge-closeout")
        elif not (args.wall_geometry_json and Path(args.wall_geometry_json).exists()):
            evidence["wall_closeout"] = _skipped_step(
                "wall-edge-closeout",
                "缺墙身面域几何：--wall-geometry-json 需指向含 planar_faces/"
                "wall_strip_rectangles/edge_member_polygons 的墙身重建结果")
        else:
            evidence["wall_closeout"] = _run(
                "wall-edge-closeout", "cad_wall_edge_closeout.py",
                ["--phase18-geometry", args.wall_geometry_json,
                 "--ledger-json", str(ledger.with_suffix(".json")),
                 "-o", str(wall_closeout)], **run_kwargs)
        if args.no_slab_thickness_partition:
            evidence["slab_partition"] = _skipped_step(
                "slab-thickness-partition", "开关 --no-slab-thickness-partition")
        else:
            sp_args = ["--model-json", str(model.with_suffix(".json"))]
            if args.slab_notes_json and Path(args.slab_notes_json).exists():
                sp_args += ["--notes-json", args.slab_notes_json]
            if args.slab_panel_texts_json and Path(
                    args.slab_panel_texts_json).exists():
                sp_args += ["--panel-texts-json", args.slab_panel_texts_json]
            if args.slab_note_frame_bbox:
                sp_args += ["--frame-bbox=" + args.slab_note_frame_bbox]
            evidence["slab_partition"] = _run(
                "slab-thickness-partition", "cad_slab_thickness_partition.py",
                sp_args + ["-o", str(slab_partition)], **run_kwargs)
        if args.no_deduction_ledger:
            evidence["deduction"] = _skipped_step(
                "deduction-ledger", "开关 --no-deduction-ledger")
        elif not (intersection_step["status"] == "ok"
                  and slab_opening_step["status"] == "ok"):
            evidence["deduction"] = _skipped_step(
                "deduction-ledger", "缺构件相交审计或板洞口审计输入")
        else:
            dl_args = ["--intersection-json",
                       str(intersection.with_suffix(".json")),
                       "--opening-json", str(slab_opening.with_suffix(".json"))]
            if args.deduction_verdict_json and Path(
                    args.deduction_verdict_json).exists():
                dl_args += ["--verdict-json", args.deduction_verdict_json]
            if args.deduction_sheet_json and Path(
                    args.deduction_sheet_json).exists():
                dl_args += ["--sheet-json", args.deduction_sheet_json]
            dl_args += ["--remaining-gap-m3",
                        str(args.deduction_remaining_gap_m3)]
            evidence["deduction"] = _run(
                "deduction-ledger", "cad_deduction_ledger.py",
                dl_args + ["-o", str(deduction)], **run_kwargs)
        if args.no_prefab_expansion:
            evidence["prefab_expansion"] = _skipped_step(
                "prefab-instance-expansion", "开关 --no-prefab-expansion")
        elif not (args.prefab_material_ledger_json and Path(
                args.prefab_material_ledger_json).exists()):
            evidence["prefab_expansion"] = _skipped_step(
                "prefab-instance-expansion",
                "缺叠合板材料分账 JSON：--prefab-material-ledger-json 提供逐编号模型块数")
        else:
            pe_dxf = Path(args.prefab_expanded_dxf or args.prefab_dxf or "")
            if not str(pe_dxf) or not pe_dxf.exists():
                evidence["prefab_expansion"] = _skipped_step(
                    "prefab-instance-expansion", "缺含预制图框的展开 DXF")
            else:
                pe_args = ["--expanded-dxf", str(pe_dxf),
                           "--material-ledger-json",
                           args.prefab_material_ledger_json,
                           "--frame-title-key", args.prefab_frame_title_key,
                           "--floor", args.reference_floor or args.floor_label]
                for key in args.prefab_title_key or []:
                    pe_args += ["--title-key", key]
                evidence["prefab_expansion"] = _run(
                    "prefab-instance-expansion",
                    "cad_prefab_instance_expansion.py",
                    pe_args + ["-o", str(prefab_expansion)], **run_kwargs)
        for step in evidence.values():
            manifest["steps"].append(step)
        manifest["skipped_steps"] = [
            {"name": step.get("name"), "reason": step.get("reason", "")}
            for step in evidence.values() if step["status"] == "skipped"]

        report_args = [
            "--model-json", str(model.with_suffix(".json")),
            "--ledger-json", str(ledger.with_suffix(".json")),
            "--scan-json", str(scan),
            "--beam-json", str(beam_objects.with_suffix(".json")),
            _opt("--floor-label", args.floor_label),
            "--format", "all",
            "-o", str(report),
        ]
        if args.report_title:
            report_args += ["--title", args.report_title]
        if manifest.get("degraded_mode"):
            report_args += ["--caveat", str(manifest["degraded_mode"])]
        if intersection_step["status"] == "ok":
            report_args += [
                "--supplement-json",
                f"构件相交={intersection.with_suffix('.json')}",
            ]
        if slab_opening_step["status"] == "ok":
            report_args += [
                "--supplement-json",
                f"板洞口={slab_opening.with_suffix('.json')}",
            ]
        if beam_gap_step["status"] == "ok":
            report_args += [
                "--supplement-json",
                "梁量差=" + str(beam_gap.with_suffix(".json")),
            ]
        if beam_coverage_step["status"] == "ok":
            report_args += [
                "--supplement-json",
                "梁覆盖=" + str(beam_coverage.with_suffix(".json")),
            ]
        if beam_attribution_step["status"] == "ok":
            report_args += [
                "--supplement-json",
                "梁候选归属=" + str(beam_attribution.with_suffix(".json")),
            ]
        if frame_index_ready is not None:
            report_args += [
                "--supplement-json",
                "梁图框索引=" + str(frame_index_ready.with_suffix(".json")),
            ]
        if span_closure_step["status"] == "ok":
            report_args += [
                "--supplement-json",
                "梁净跨口径=" + str(span_closure.with_suffix(".json")),
            ]
        if multispan_step["status"] == "ok":
            report_args += [
                "--supplement-json",
                "多跨梁续接=" + str(multispan.with_suffix(".json")),
            ]
        if dedup_step["status"] == "ok":
            report_args += [
                "--supplement-json",
                "梁实例去重=" + str(beam_dedup.with_suffix(".json")),
            ]
        if conflict_step["status"] == "ok":
            report_args += [
                "--supplement-json",
                "梁编号冲突=" + str(beam_conflict.with_suffix(".json")),
            ]
        if glodon_step["status"] == "ok":
            report_args += [
                "--supplement-json",
                "广联达口径=" + str(glodon_scope.with_suffix(".json")),
            ]
        if grade_step["status"] == "ok":
            report_args += [
                "--supplement-json",
                "分标号=" + str(grade_ledger.with_suffix(".json")),
            ]
        evidence_labels = (("centerline", "中心线支撑"), ("wall_closeout", "墙身闭合"),
                           ("slab_partition", "板厚分档"), ("deduction", "统一扣减"),
                           ("prefab_expansion", "预制展开"))
        evidence_paths = {"centerline": centerline, "wall_closeout": wall_closeout,
                          "slab_partition": slab_partition,
                          "deduction": deduction,
                          "prefab_expansion": prefab_expansion}
        for key, label in evidence_labels:
            if evidence[key]["status"] == "ok":
                report_args += ["--supplement-json",
                                f"{label}={evidence_paths[key].with_suffix('.json')}"]
        for supplement in args.supplement_json:
            report_args += ["--supplement-json", supplement]
        report_step = _run(
            "quantity-report",
            "cad_quantity_report.py",
            report_args,
            timeout_seconds=args.timeout_seconds,
            retries=max(0, args.retries),
        )
        manifest["steps"].append(report_step)
        if report_step["status"] != "ok":
            raise RuntimeError("统一报告生成失败")

        model_data = _load_json(model.with_suffix(".json"))
        ledger_data = _load_json(ledger.with_suffix(".json"))
        report_data = _load_json(report.with_suffix(".json"))
        manifest["formal_ready"] = bool(
            ledger_data.get("formal_ready"))
        manifest["metrics"] = {
            "beam_topology_volume_m3": (
                model_data.get("quantities", {})
                .get("beam", {})
                .get("topology_volume_m3")
            ),
            "candidate_total_volume_m3": (
                ledger_data.get("quantities", {})
                .get("candidate_total_volume_m3")
            ),
            "reference_total_volume_m3": round(sum(
                float(value or 0.0)
                for value in (
                    ledger_data.get("reference_values") or {}
                ).values()
            ), 4),
            "gate_summary": dict(
                ledger_data.get("gate_summary") or {}),
            "direct_outputs": dict(
                report_data.get("direct_outputs") or {}),
            "grade_ledger": dict(
                _load_json(grade_ledger.with_suffix(".json")).get("summary")
                or {}) if grade_step["status"] == "ok" else {},
        }
        _copy_manifest_paths(
            manifest["artifacts"],
            scan,
            detail if detail and detail.exists() else None,
            beam_geometry,
            (
                beam_geometry
                if support_step["status"] == "reused"
                else support_geometry
            ),
            (
                beam_geometry
                if slab_step["status"] == "reused"
                else slab_geometry
            ),
            beam_objects,
            model,
            ledger,
            report,
            intersection if intersection_step["status"] == "ok" else None,
            slab_opening if slab_opening_step["status"] == "ok" else None,
            beam_gap if beam_gap_step["status"] == "ok" else None,
            beam_coverage if beam_coverage_step["status"] == "ok" else None,
            beam_attribution if beam_attribution_step["status"] == "ok" else None,
            frame_index_ready,
            span_closure if span_closure_step["status"] == "ok" else None,
            multispan if multispan_step["status"] == "ok" else None,
            beam_dedup if dedup_step["status"] == "ok" else None,
            beam_conflict if conflict_step["status"] == "ok" else None,
            glodon_scope if glodon_step["status"] == "ok" else None,
            grade_ledger if grade_step["status"] == "ok" else None,
        )
        for evidence_key, _evidence_label in evidence_labels:
            if evidence[evidence_key]["status"] != "ok":
                continue
            base = evidence_paths[evidence_key]
            for suffix in (".json", ".csv", ".md"):
                manifest["artifacts"][base.name + suffix] = str(
                    base.with_suffix(suffix).resolve())
        manifest["artifact_checksums"] = _artifact_details(
            manifest["artifacts"])
        manifest["status"] = "complete"
        _write_manifest(manifest, manifest_path)
        return 0
    except Exception as exc:
        manifest["status"] = "failed"
        manifest["error"] = f"{type(exc).__name__}: {exc}"
        manifest["artifacts"] = _artifact_map(manifest_path)
        _write_manifest(manifest, manifest_path)
        print(manifest["error"], file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
