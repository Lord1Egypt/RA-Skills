"""一次完整的布置出图流水线：模型 -> 26 条规则 -> 道路 -> 周边 -> 六视角 -> DXF/PNG。

被 build_site_plan.py（人工/reader 设施）和 generate_site_layout.py（自动候选）
共用，保证两条入口的校核口径、文件命名和闸门完全一致。
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from .context import check_context, render_context_markdown
from .review_panel import build_panel, dump_panel, render_panel_markdown
from .road_geometry import check_roads, render_road_markdown
from .siteplan import build_stage_model, render_markdown, stage_changes
from .stage_draw import draw_stage
from .taxonomy import STAGE_NAMES, STAGES


def resolve_stages(raw: str) -> List[str]:
    text = str(raw or "all").strip().lower()
    if text == "all":
        return list(STAGES)
    stages = [item.strip() for item in text.split(",") if item.strip()]
    unknown = [item for item in stages if item not in STAGES]
    if unknown:
        raise ValueError(f"未知阶段 {unknown}；只接受 {list(STAGES)}")
    if not stages:
        raise ValueError("--stages 不能为空")
    return stages


def run_plan(
    *,
    base_map: Dict[str, Any],
    base_sha: str,
    facilities: Sequence[Dict[str, Any]],
    fac_source: Dict[str, Any],
    fac_data: Dict[str, Any],
    cranes: Sequence[Dict[str, Any]],
    crane_sources: Sequence[Dict[str, Any]],
    stages: Sequence[str],
    out_dir: str | Path,
    project: str = "",
    title_params: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, float]] = None,
    context: Optional[Dict[str, Any]] = None,
    allow_source_mismatch: bool = False,
    scheme: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """跑完所有阶段并落盘；返回 manifest、逐阶段结果和模型。"""
    title_params = dict(title_params or {})
    identities: Dict[str, Dict[str, str]] = {
        "base_map": {
            "sha256": str(base_map.get("drawing_sha256") or ""),
            "contract_id": str(base_map.get("reader_contract_id")
                               or base_map.get("contract_id") or ""),
        },
        "facilities": {
            "sha256": str(fac_source.get("source_sha256") or ""),
            "contract_id": str(fac_source.get("contract_id") or ""),
        },
    }
    for index, source in enumerate(crane_sources):
        identities[f"cranes[{index}]"] = {
            "sha256": str(source.get("source_sha256") or ""),
            "contract_id": str(source.get("contract_id") or ""),
        }
    present = {key: value["sha256"] for key, value in identities.items() if value["sha256"]}
    contracts = {key: value["contract_id"] for key, value in identities.items()
                 if value["contract_id"]}
    # 同源闸门优先比源图哈希；源图哈希缺失时（reader 只拿到 detail JSON 且原图已移动）
    # 退回比 cad-contract 契约号。两者都缺时标 unverified，不能默认写 same_source=true。
    same_source: Optional[bool]
    same_source_basis = "unverified"
    if len(present) >= 2:
        same_source = len(set(present.values())) <= 1
        same_source_basis = "sha256"
    elif len(contracts) >= 2:
        same_source = len(set(contracts.values())) <= 1
        same_source_basis = "contract_id"
    else:
        same_source = None
    mismatch_evidence = present if same_source_basis == "sha256" else contracts
    contract_evidence = contracts
    if same_source is False and not allow_source_mismatch:
        raise RuntimeError(
            "输入不同源（{} 不一致）：{}；请统一到同一张总平面图，"
            "或加 --allow-source-mismatch 只出比对草稿".format(
                same_source_basis, json.dumps(mismatch_evidence, ensure_ascii=False))
        )

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    resolved_project = project or str(fac_data.get("project") or base_map.get("project") or "")
    models: Dict[str, Dict[str, Any]] = {}
    results: List[Dict[str, Any]] = []
    context_results: Dict[str, Dict[str, Any]] = {}

    for stage in stages:
        model = build_stage_model(base_map, list(facilities), list(cranes), stage,
                                  project=resolved_project, params=params, context=context)
        model["source"] = {
            "base_map": str(base_map.get("source_file") or ""),
            "base_map_sha256": base_sha,
            "facilities": fac_source,
            "cranes": list(crane_sources),
            "drawing_sha256": present,
            "contract_id": contract_evidence,
            "same_source": same_source,
            "same_source_basis": same_source_basis,
        }
        if same_source is False:
            model["warnings"].append("输入不同源，图签按 DRAFT-SOURCE-MISMATCH 处理")
        elif same_source is None:
            model["warnings"].append(
                "输入同源身份无法核实：底座与设施/塔吊均无源图哈希或契约号，"
                "图签仅按 DRAFT 处理，须人工确认来自同一张总平面图"
            )
        for source in crane_sources:
            gate = source.get("coordinate_gate") or {}
            status = str(gate.get("status") or "")
            if status in ("different_source", "partial_different_source"):
                model["warnings"].append(
                    "塔吊坐标与底图不同源（{}，拒绝 {} 个中心）：不进入覆盖/碰撞检查，只留复核".format(
                        status, gate.get("rejected", 0))
                )
            source_reviews = list(source.get("reviews") or [])
            if source_reviews:
                model["warnings"].append(
                    "塔吊识图有 {} 条未定位/仅候选记录，详见来源审计".format(len(source_reviews))
                )
        model["warnings"] += [w for w in base_map.get("warnings") or [] if w not in model["warnings"]]

        road = check_roads(model["facilities"], model["rule_params"])
        context_result = None
        if context is not None:
            context_result = check_context(model["facilities"], model["cranes"], context)
            context_results[stage] = context_result
            model["context_summary"] = context_result["summary"]
        panel = build_panel(model, road, context_result=context_result)

        model["road_summary"] = road["summary"]
        model["road_failed"] = [c["name"] for c in road["checks"] if c["status"] == "fail"]
        if context_result is not None:
            model["context_failed"] = [c["name"] for c in context_result["checks"]
                                       if c["status"] == "fail"]
        model["review_summary"] = panel["gates"]

        road_path = out / "road-check-{}.json".format(stage)
        road_md = out / "road-check-{}.md".format(stage)
        panel_path = out / "review-panel-{}.json".format(stage)
        panel_md = out / "review-panel-{}.md".format(stage)
        road_path.write_text(json.dumps(road, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        road_md.write_text(render_road_markdown(road), encoding="utf-8")
        panel_path.write_text(dump_panel(panel), encoding="utf-8")
        panel_md.write_text(render_panel_markdown(panel), encoding="utf-8")

        model["road_check"] = str(road_path)
        model["context_check"] = ""
        if context_result is not None:
            ctx_path = out / "context-check-{}.json".format(stage)
            ctx_md = out / "context-check-{}.md".format(stage)
            ctx_path.write_text(json.dumps(context_result, ensure_ascii=False, indent=2) + "\n",
                                encoding="utf-8")
            ctx_md.write_text(render_context_markdown(context_result), encoding="utf-8")
            model["context_check"] = str(ctx_path)

        models[stage] = model
        scheme_meta = scheme or {}
        title_text = str(title_params.get("title") or "").replace(
            "{scheme}", str(scheme_meta.get("name") or ""))
        if not title_text.strip():
            title_text = "{}施工平面布置图".format(STAGE_NAMES[stage])
        drawing_no = str(title_params.get("drawing_no") or "SLP-{stage}")
        drawing_no = (drawing_no.replace("{stage}", stage[:1].upper())
                      .replace("{stage_name}", STAGE_NAMES[stage])
                      .replace("{scheme}", str(scheme_meta.get("key") or "")))
        result = draw_stage(
            model, base_map, out,
            title_params={
                "title": title_text,
                "drawing_no": drawing_no,
                "scale": title_params.get("scale") or "1:500",
                "revision": title_params.get("revision") or "0",
                "date": title_params.get("date") or "",
                "contract_id": base_map.get("contract_id") or "",
                "project": resolved_project,
                "disclaimer": title_params.get("disclaimer") or "",
            },
        )
        if same_source is False:
            result["draft_label"] = "DRAFT-SOURCE-MISMATCH"
        result["road_check"] = str(road_path)
        result["road_markdown"] = str(road_md)
        result["review_panel"] = str(panel_path)
        result["review_markdown"] = str(panel_md)
        if model["context_check"]:
            result["context_check"] = model["context_check"]
        md_path = out / "stage-{}.md".format(stage)
        md_path.write_text(render_markdown(model), encoding="utf-8")
        result["markdown"] = str(md_path)
        results.append(result)

    changes = stage_changes(models)
    (out / "stage-changes.json").write_text(
        json.dumps(changes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = ["# 阶段间设施变化", "", "> 只反映 active_stages 声明，不代表已审批的施工顺序。", ""]
    for item in changes["transitions"]:
        md += [
            "## {} → {}".format(item["from_name"], item["to_name"]),
            "- 新增：{}".format("、".join(item["added"]) or "无"),
            "- 撤销：{}".format("、".join(item["removed"]) or "无"),
            "- 延续：{} 项".format(item["unchanged"]),
            "- 塔吊进场：{}".format("、".join(item.get("cranes_added") or []) or "无"),
            "- 塔吊退场：{}".format("、".join(item.get("cranes_removed") or []) or "无"),
            "",
        ]
    (out / "stage-changes.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    manifest = {
        "schema": "site-plan-manifest/v1",
        "generated_at": models[stages[0]]["generated_at"],
        "project": resolved_project,
        "scheme": scheme,
        "stages": results,
        "source": {"base_map": str(base_map.get("source_file") or ""),
                   "facilities": fac_source, "cranes": list(crane_sources),
                   "same_source": same_source, "drawing_sha256": present,
                   "contract_id": contract_evidence, "same_source_basis": same_source_basis},
        "stage_changes": str(out / "stage-changes.json"),
        "final_check": False,
        "boundary": "布置草案与规则校核，不替代施工组织设计审批、设计签章和现场复核。",
    }
    if context is not None:
        manifest["context"] = {
            "source_path": context.get("source_path") or "",
            "source_sha256": context.get("source_sha256") or "",
            "constraints": len(context.get("constraints") or []),
            "summary": {stage: context_results[stage]["summary"] for stage in context_results},
        }
    (out / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    exit_code = 0
    for result in results:
        if result["exit_code"]:
            exit_code = result["exit_code"]
    return {
        "manifest": manifest,
        "results": results,
        "models": models,
        "contexts": context_results,
        "same_source": same_source,
        "same_source_basis": same_source_basis,
        "drawing_sha256": present,
        "contract_id": contract_evidence,
        "exit_code": exit_code,
        "out_dir": str(out),
    }
