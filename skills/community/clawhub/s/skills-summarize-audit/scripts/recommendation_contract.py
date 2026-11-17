"""Attach reviewable action plans without executing recommended operations."""
from __future__ import annotations

MARKET_FIELDS = ("source_url", "license", "stars", "last_commit", "last_release", "maintenance_status", "security_statement", "price", "price_verified", "checked_at", "confidence", "scoring_basis")
EXPOSURE_FIELDS = ("executes_local_commands", "requires_network", "requires_token", "arbitrary_shell", "offline_review", "upstream_overwrite")


def action_plan(target, judgment, evidence, problem=None, steps=None, priority="P2"):
    return {
        "target": target, "priority": priority, "problem": problem or "需补齐推荐依据",
        "evidence": evidence, "judgment": judgment, "suggested_action": judgment,
        "steps": steps or ["核对目标的真实来源与作用域。", "补齐当前项目、使用时间窗、维护与许可证证据后复评。"],
        "execution_agent": "具备目标客户端文件读取与验证能力的 Agent；实施变更另行按用户授权执行",
        "verification": "以同一目标和来源重新审查；运行相关 CLI/测试；涉及显示变化时验收实际 UI。",
        "rollback": "本建议未执行；实施前由执行 Agent 保存目标快照与 SHA256，失败按快照恢复并复验。",
        "status": "suggested", "fact_status": "inferred" if evidence else "unavailable",
        "install_scope": "defer", "target_path": None, "scope_reason": "需由目标路径及项目使用证据确认",
        "market": {field: None for field in MARKET_FIELDS},
        "exposure": {field: {"status": "unavailable", "value": None} for field in EXPOSURE_FIELDS},
        "prompt": f"请核对 {target} 的下列证据后处理建议：{judgment}。先给出精确文件、步骤、验证和回滚方案；仅执行已有授权覆盖的变更。",
    }


def enrich_report(report):
    """Keep raw evidence intact and expose the same action contract in both scopes."""
    if report.get("scope") == "ecosystem":
        opt = report["ecosystem_assessment"]["optimization"]
        recs = opt.get("skill_recommendations", []) + opt.get("mcp_recommendations", [])
        actions = []
        gap_groups = {}
        for rec in recs:
            gaps = rec.get("missing_evidence", [])
            judgment = "补充证据，暂不变更" if gaps else rec["layer"]
            plan = action_plan(rec["target"], judgment, rec["evidence"],
                               "缺少 " + ", ".join(gaps) if gaps else "根据完整证据复核工具价值")
            market = rec["evidence"].get("market_evidence")
            if isinstance(market, dict):
                plan["market"].update({key: market.get(key) for key in MARKET_FIELDS})
            rec["action_plan"] = plan
            if gaps:
                gap_groups.setdefault((rec.get("type", "unknown"), tuple(sorted(gaps))), []).append(rec)
            else:
                actions.append(plan)
        for (kind, gaps), members in gap_groups.items():
            labels = {"usage": "使用记录", "alignment": "项目匹配", "market": "市场来源", "health": "健康检查"}
            gap_text = "、".join(labels.get(g, g) for g in gaps)
            plan = action_plan(f"{len(members)} 项 {kind} 的共同证据缺口", "补充证据，暂不变更",
                               {"type": kind, "missing_dimensions": list(gaps), "targets": [r["target"] for r in members]},
                               f"缺少{gap_text}；不能据此判定低价值",
                               ["先选择当前确有优化需求的目标，不为全部安装项强行补分。",
                                "核对项目匹配；经用户同意采集限定客户端、时间窗的调用记录，只保留统计。",
                                "如仍需选型，经授权比较 2–3 个同类项目的维护、许可证和成本。"])
            plan["fact_status"] = "unavailable"
            actions.append(plan)
        # Health/source defects remain actionable even when usage evidence is absent.
        for entry in report["ecosystem_assessment"].get("skill_layer", {}).get("issues", []):
            if entry.get("severity") in {"critical", "warning"}:
                actions.append(issue_plan(entry))
    else:
        actions = [issue_plan(entry) for entry in report.get("issues", []) if entry.get("severity") in {"critical", "warning"}]
        paths = {item["id"]: item.get("source_paths", []) for item in report.get("items", [])}
        for rec in report.get("recommendations", []):
            evidence = {"source_paths": paths.get(rec["target"], []), "rules": rec.get("evidence", [])}
            rec["action_plan"] = action_plan(rec["target"], rec["decision"], evidence, rec["reason"])
        # Avoid repeating every healthy installation on the first screen.
        actions += [r["action_plan"] for r in report.get("recommendations", []) if r["decision"] in {"边界调整", "共存"}]
    report["actions"] = sorted(actions, key=lambda a: a["priority"])
    report["evidence_contract"] = {"unknown_value": None, "market_max_age_days": 30,
                                   "installation_is_not_execution": True, "observed_absence_requires_coverage": True}
    return report


def issue_plan(entry):
    plan = action_plan(entry["id"], entry["remediation"], entry["evidence"], entry["message"],
                       ["回读证据来源，确认当前生效项。", entry["remediation"], "按同一来源复跑审查并验证实际行为。"],
                       "P0" if entry["severity"] == "critical" else "P1")
    plan["fact_status"] = "observed"
    return plan


def render_actions(report, detail=False):
    actions = report.get("actions", [])
    lines = ["", "建议执行（尚未执行）", ""]
    for action in actions if detail else actions[:5]:
        evidence = action['evidence']
        if not detail and isinstance(evidence, dict) and "targets" in evidence:
            evidence = "示例 " + "、".join(evidence["targets"][:3]) + f"；完整 {len(evidence['targets'])} 项见 --json"
        lines.extend([f"- {action['priority']} {action['target']}: {action['suggested_action']}",
                      f"  依据: {action['problem']}；证据: {evidence}",
                      "  步骤: " + " → ".join(action["steps"]),
                      f"  执行 Agent: {action['execution_agent']}",
                      f"  验证: {action['verification']}", f"  回滚: {action['rollback']}",
                      f"  状态: {action['status']}"])
    if not actions:
        lines.append("未发现有足够证据支持的变更建议；未测项目不等于运行正常。")
    if len(actions) > 5 and not detail:
        lines.append(f"另有 {len(actions) - 5} 条建议，使用 --detail 或 --json 查看。")
    return "\n".join(lines)


def render_footer(report):
    lines = []
    scan = report.get("scan", {})
    if scan:
        lines.append(f"扫描: {scan['mode']}；新查 {scan['checked']} 项，复用 {scan['reused']} 项。")
    if report.get("scope") == "visible":
        lines.append("Codex 命令栏与侧边栏中文翻译清单：已按输入可见 ID 检查说明；候选详见 collect_codex_display_candidates.py 输出，未宣称 UI 已翻译。")
    else:
        lines.append("Codex 命令栏与侧边栏中文翻译清单：未提供本次可见 UI 集合，未执行候选验收；安装项不能替代可见项。可提供完整技能链接或 UI 清单后继续，未宣称 UI 已翻译。")
    lines.append("深度分析：可继续逐项核验版本、真实运行、来源冲突与同类 GitHub 项目；按需提供目标、使用时间窗和联网授权。")
    if scan.get("suggest_full_scan"):
        lines.append("建议进行全景扫描（" + "、".join(scan["reasons"]) + "）。是否进行一次全景扫描？")
    return "\n" + "\n".join(lines)
