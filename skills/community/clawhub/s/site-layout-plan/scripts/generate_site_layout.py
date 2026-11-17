#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""总工视角的自动布置候选：A/B/C 三套 + 全套校核 + 比选。

链路：
  base-map（prepare_site 产出）+ site-context（周边）+ requirements（项目需求）
  -> generator 生成候选设施（source=auto-layout、confidence=candidate）
  -> 每套跑 26 条规则 + 道路 R1~R4 + 周边约束 + 六视角 + 三阶段 DXF/PNG
  -> comparison.json/md：八维评分、硬伤、待办、推荐意见

边界：自动布置只出“可讨论的候选”，不选型、不替代审批。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.bootstrap import ensure_runtime  # noqa: E402

ensure_runtime(__file__)

from site_layout.context import ContextError, load_context  # noqa: E402
from site_layout.generator import (  # noqa: E402
    PROFILES, GeneratorError, compare_schemes, evaluate_scheme, generate_layout,
    load_requirements, render_comparison_markdown, render_generated_markdown,
)
from site_layout.pipeline import resolve_stages, run_plan  # noqa: E402
from site_layout.road_geometry import check_roads  # noqa: E402
from site_layout.siteplan import (  # noqa: E402
    SitePlanError, load_base_map, load_cranes, load_facilities,
)

ALIASES = {"A": "compact", "B": "balanced", "C": "safe",
           "compact": "compact", "balanced": "balanced", "safe": "safe",
           "all": "all"}


def _facility_payload(row: dict) -> dict:
    """内部统一用 points_mm；写 cad-site-facility/v1 时转成 xy/points 标准写法。"""
    out = dict(row)
    geom = row.get("geometry") or {}
    points = geom.get("points_mm") or []
    if geom.get("type") == "point" and points:
        out["geometry"] = {"type": "point", "xy": [points[0][0], points[0][1]]}
    elif points:
        out["geometry"] = {"type": geom.get("type"), "points": [list(p) for p in points],
                           "closed": bool(geom.get("closed"))}
    return out


def _crane_payload(row: dict) -> dict:
    """内部 crane 用 center_mm/jib_mm；写成 build_site_plan.py 可复用的 m 制契约。"""
    center = row.get("center_mm") or []
    jib = row.get("jib_mm")
    return {
        "crane_id": str(row.get("id") or ""),
        "model": str(row.get("model") or ""),
        "center_xy_m": [round(float(center[0]) / 1000.0, 3),
                        round(float(center[1]) / 1000.0, 3)],
        "center_status": "insert_point",
        "transform_status": "same_source",
        "jib_length_m": round(float(jib) / 1000.0, 3) if jib not in (None, "") else None,
        "rotation_deg": row.get("rotation_deg"),
        "active_stages": list(row.get("active_stages") or ["structure"]),
        "source": str(row.get("source") or "auto-layout"),
        "confidence": str(row.get("confidence") or "candidate"),
    }


def _parse_params(values: list[str]) -> dict:
    params = {}
    for item in values or []:
        if "=" not in item:
            raise SitePlanError(f"--rule-param 需要 key=value，收到 {item!r}")
        key, value = item.split("=", 1)
        params[key.strip()] = value.strip()
    return params


def _schemes(raw: str) -> list[str]:
    text = str(raw or "all").strip()
    chosen: list[str] = []
    for token in text.replace("，", ",").split(","):
        token = token.strip()
        if not token:
            continue
        key = ALIASES.get(token) or ALIASES.get(token.upper())
        if key is None:
            raise GeneratorError(f"未知方案 {token!r}；只接受 A/B/C/all 或 compact/balanced/safe")
        if key == "all":
            return list(PROFILES)
        if key not in chosen:
            chosen.append(key)
    return chosen or list(PROFILES)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="总工视角自动布置候选：A/B/C 三套比选并出图")
    parser.add_argument("--base-map", required=True, help="prepare_site.py 产出的 base-map.json")
    parser.add_argument("--context", default="", help="周边环境 site-context/v1")
    parser.add_argument("--requirements", default="", help="项目需求 site-layout-requirements/v1")
    parser.add_argument("--cranes", action="append", default=[], help="reader *.crane.json（可选）")
    parser.add_argument("--scheme", default="all", help="A/B/C（可逗号组合）或 all")
    parser.add_argument("--stages", default="all")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--project", default="")
    parser.add_argument("--title", default="")
    parser.add_argument("--scale", default="1:500")
    parser.add_argument("--revision", default="0")
    parser.add_argument("--date", default="")
    parser.add_argument("--rule-param", action="append", default=[])
    parser.add_argument("--allow-assumed-building", action="store_true",
                        help="底图/需求无主体轮廓时，允许按 42%%×32%% 假定矩形出草案；"
                             "输出会标 building_source=assumed，不得当真实布置")
    args = parser.parse_args(argv)

    try:
        base_map, base_sha = load_base_map(args.base_map)
        context = load_context(args.context, base_map=base_map) if args.context else \
            load_context(None, base_map=base_map)
        requirements = load_requirements(args.requirements)
        cranes, crane_sources = load_cranes(args.cranes, base_map.get("extents_mm"))
        stages = resolve_stages(args.stages)
        params = _parse_params(args.rule_param)
        schemes = _schemes(args.scheme)
        out = Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=True)
        project = args.project or str(requirements.get("project") or base_map.get("project") or "")

        evaluations = []
        scheme_outputs = []
        building_source = ""
        for key in schemes:
            result = generate_layout(base_map, context, requirements, cranes, key,
                                     allow_assumed_building=args.allow_assumed_building)
            building_source = result.get("building_source") or building_source
            folder = out / "scheme-{}".format(PROFILES[key]["key"])
            folder.mkdir(parents=True, exist_ok=True)

            payload = {
                "schema": "cad-site-facility/v1",
                "project": project,
                "coord_unit": "mm",
                "contract": {
                    "contract_id": base_map.get("contract_id") or "",
                    "source_sha256": base_map.get("drawing_sha256") or "",
                    "generator": "site-layout-plan/generate_site_layout",
                },
                "facilities": [_facility_payload(row) for row in result["facilities"]],
            }
            fac_path = folder / "generated-facilities.json"
            fac_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                                encoding="utf-8")
            crane_path = folder / "generated-cranes.json"
            crane_payload = {
                "schema": "cad-crane-layout/v1",
                "project": project,
                "coord_unit": "m",
                "units": {"drawing_unit": "m", "basis": "explicit", "mm_per_unit": 1000.0},
                "contract": payload["contract"],
                "crane_layout": [_crane_payload(row) for row in result["cranes"]],
                "final_check": False,
                "boundary": "自动布置塔吊为候选位置，必须完成选型、基础、附着、群塔与现场复核后才能用于正式施工。",
            }
            crane_path.write_text(json.dumps(crane_payload, ensure_ascii=False, indent=2) + "\n",
                                   encoding="utf-8")
            (folder / "scheme.json").write_text(
                json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            (folder / "scheme.md").write_text(render_generated_markdown(result), encoding="utf-8")

            facilities, fac_source, fac_data = load_facilities(fac_path)
            outcome = run_plan(
                base_map=base_map, base_sha=base_sha,
                facilities=facilities, fac_source=fac_source, fac_data=fac_data,
                cranes=result["cranes"],
                crane_sources=crane_sources if cranes else [],
                stages=stages, out_dir=folder, project=project,
                title_params={"title": args.title or "{scheme}施工平面布置图",
                              "drawing_no": "SLP-{}-{}".format(PROFILES[key]["key"], "{stage}"),
                              "scale": args.scale, "revision": args.revision, "date": args.date},
                params=params, context=context,
                scheme={"key": key, "name": result["scheme_name"],
                        "tag": PROFILES[key]["tag"]},
            )
            model_map = outcome["models"]
            road_map = {stage: check_roads(model["facilities"], model["rule_params"])
                        for stage, model in model_map.items()}
            ctx_map = outcome["contexts"] or {}
            evaluation = evaluate_scheme(result, model_map, road_map, ctx_map, stages=stages)
            evaluation["evaluated_stages"] = list(model_map.keys())
            evaluation["out_dir"] = str(folder)
            evaluations.append(evaluation)
            scheme_outputs.append({
                "scheme": key, "name": result["scheme_name"], "out_dir": str(folder),
                "features": str(fac_path),
                "crane_file": str(crane_path),
                "stages": [{"stage": item["stage"], "dxf": item["dxf"], "png": item["png"],
                            "draft_label": item["draft_label"]} for item in outcome["results"]],
                "evaluation": evaluation,
            })

        comparison = compare_schemes(evaluations)
        (out / "comparison.json").write_text(
            json.dumps(comparison, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (out / "comparison.md").write_text(render_comparison_markdown(comparison), encoding="utf-8")

        manifest = {
            "schema": "site-scheme-library/v1",
            "generated_at": comparison["generated_at"],
            "project": project,
            "base_map": str(Path(args.base_map).resolve()),
            "context": {"path": context.get("source_path") or "",
                        "constraints": len(context.get("constraints") or []),
                        "warnings": context.get("warnings") or []},
            "requirements": requirements.get("_path") or "",
            "stages": list(stages),
            "schemes": scheme_outputs,
            "recommended": comparison.get("recommended"),
            "building_source": building_source,
            "comparison": str(out / "comparison.json"),
            "final_check": False,
            "boundary": "自动布置为候选方案，不是确认位置；不替代施工组织设计审批、消防审查与现场复核。",
        }
        (out / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        for item in comparison["rows"]:
            print("{} {} 综合{} {}".format(item["scheme"], item["scheme_name"],
                                          item["total"], item["verdict"]))
        if comparison.get("recommended"):
            print("推荐: {} - {}".format(comparison["recommended"]["scheme_name"],
                                        comparison["recommended"]["reason"]))
        print("building_source: {}".format(building_source or "unknown"))
        print("comparison: {}".format(out / "comparison.md"))
        print("manifest: {}".format(out / "manifest.json"))
        return 0 if comparison["usable"] else 5
    except (GeneratorError, ContextError, SitePlanError) as exc:
        print("[{}] {}".format(exc.__class__.__name__, exc), file=sys.stderr)
        return int(getattr(exc, "exit_code", 2))
    except RuntimeError as exc:
        print("[PipelineError] {}".format(exc), file=sys.stderr)
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
