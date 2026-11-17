"""多视角审查：项目总工、安全、消防临建、文明环保、商务、甲方报建。

同一份校核结果，按角色关注点重新组织，输出"谁该看什么、谁该改什么"。
不产生新的结论，不替代审批；角色意见来自固定映射，可复算。
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Sequence

SCHEMA = "site-review-panel/v1"

ROLES: List[Dict[str, Any]] = [
    {"id": "chief", "name": "项目总工", "focus": "总体可行性、骨架与阶段衔接",
     "checks": ["1", "2", "4", "11", "13", "14", "R1", "R2", "R3", "R4"]},
    {"id": "safety", "name": "安全总监", "focus": "塔吊、临建、用电、交通冲突",
     "checks": ["6", "7", "14", "R2", "R3"]},
    {"id": "fire", "name": "消防/临建", "focus": "消防车道、消火栓、净空、回车",
     "checks": ["3", "4", "5", "15", "R1", "R3", "R4"]},
    {"id": "civil", "name": "文明环保", "focus": "加工区隔离、九牌一图、垃圾与扬尘",
     "checks": ["8", "9", "10", "R1"]},
    {"id": "commercial", "name": "商务成本", "focus": "道路规模、永临结合、配电距离",
     "checks": ["3", "7", "11", "R1"]},
    {"id": "client", "name": "甲方/报建", "focus": "红线、出入口、阶段必备与公示",
     "checks": ["1", "2", "4", "9", "13"]},
]

# 周边环境约束（C1..）默认挂到哪些角色：安全/文明/报建都关心，总工兜底。
CONTEXT_ROLES = ("chief", "safety", "civil", "client")

STATUS_WEIGHT = {"fail": 0, "manual": 1, "pass": 2}


def _index(checks: Sequence[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {str(item.get("id")): item for item in checks}


def build_panel(model: Dict[str, Any], road_result: Dict[str, Any],
                context_result: Dict[str, Any] | None = None) -> Dict[str, Any]:
    merged: List[Dict[str, Any]] = []
    for item in model.get("checks") or []:
        merged.append({
            "id": str(item.get("id")), "name": item.get("name"),
            "status": item.get("status"), "message": item.get("message"),
            "action": item.get("action") or "",
            "basis": item.get("basis") or "",
        })
    for item in road_result.get("checks") or []:
        merged.append({
            "id": str(item.get("id")), "name": item.get("name"),
            "status": item.get("status"), "message": item.get("message"),
            "action": item.get("action") or "",
            "basis": item.get("basis") or "",
        })
    context_ids: List[str] = []
    for item in (context_result or {}).get("checks") or []:
        cid = str(item.get("id") or "")
        if not cid:
            continue
        context_ids.append(cid)
        merged.append({
            "id": cid, "name": item.get("name"),
            "status": item.get("status"), "message": item.get("message"),
            "action": "退场或调整位置；补产权单位/管线探测/专项方案" if item.get("status") != "pass" else "",
            "basis": item.get("basis") or "",
        })
    index = _index(merged)

    roles_out: List[Dict[str, Any]] = []
    for role in ROLES:
        findings = []
        counts = {"pass": 0, "fail": 0, "manual": 0}
        check_ids = list(role["checks"])
        if role["id"] in CONTEXT_ROLES:
            check_ids += context_ids
        for cid in check_ids:
            item = index.get(cid)
            if not item:
                continue
            counts[item["status"]] = counts.get(item["status"], 0) + 1
            if item["status"] in ("fail", "manual"):
                findings.append({
                    "id": item["id"], "name": item["name"],
                    "status": item["status"], "message": item["message"],
                    "action": item["action"], "basis": item["basis"],
                })
        verdict = "fail" if counts["fail"] else ("review" if counts["manual"] else "pass")
        findings.sort(key=lambda f: STATUS_WEIGHT.get(f["status"], 9))
        roles_out.append({
            "role": role["id"], "name": role["name"], "focus": role["focus"],
            "verdict": verdict, "counts": counts,
            "findings": findings[:8],
            "top_actions": [f["action"] or f["message"] for f in findings if f["action"]][:4],
        })

    hard_fail = any(role["verdict"] == "fail" for role in roles_out)
    manual = any(role["verdict"] == "review" for role in roles_out)
    summary = {"pass": 0, "fail": 0, "manual": 0}
    for item in merged:
        if item["status"] in summary:
            summary[item["status"]] += 1
    return {
        "schema": SCHEMA,
        "stage": model.get("stage"),
        "stage_name": model.get("stage_name"),
        "summary": summary,
        "roles": roles_out,
        "gates": {
            "hard_fail": hard_fail,
            "manual_review": manual,
            "ready_for_review": not hard_fail,
        },
        "final_check": False,
        "boundary": "多视角审查是内部校核意见，不替代施工组织设计审批、消防审查和项目总工签字。",
    }


def render_panel_markdown(panel: Dict[str, Any]) -> str:
    lines = [
        "# 多视角审查（{}）".format(panel.get("stage_name") or panel.get("stage") or ""),
        "",
        "> 同一份校核结果按角色重排；意见可复算，不替代审批与签字。",
        "",
        "| 角色 | 结论 | 通过 | 不通过 | 待人工 | 关注点 |",
        "|---|---|---:|---:|---:|---|",
    ]
    for role in panel["roles"]:
        c = role["counts"]
        lines.append("| {} | {} | {} | {} | {} | {} |".format(
            role["name"], role["verdict"], c["pass"], c["fail"], c["manual"], role["focus"]))
    lines += ["", "## 待处理", ""]
    any_item = False
    for role in panel["roles"]:
        if not role["findings"]:
            continue
        any_item = True
        lines += ["### {}（{}）".format(role["name"], role["verdict"]), ""]
        for item in role["findings"]:
            lines.append("- [{}] {}：{}".format(item["status"], item["name"], item["message"]))
            if item["action"]:
                lines.append("  - 处理：{}".format(item["action"]))
        lines.append("")
    if not any_item:
        lines += ["无待处理项。", ""]
    gates = panel["gates"]
    lines += [
        "## 闸门",
        "",
        "- 硬伤：{}".format("有" if gates["hard_fail"] else "无"),
        "- 待人工：{}".format("有" if gates["manual_review"] else "无"),
        "- 可提交内部评审：{}".format("是（仍需人工确认）" if gates["ready_for_review"] else "否"),
        "",
    ]
    return "\n".join(lines)


def dump_panel(panel: Dict[str, Any]) -> str:
    return json.dumps(panel, ensure_ascii=False, indent=2) + "\n"
