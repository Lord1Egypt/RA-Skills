from __future__ import annotations

import locale

from .common import *
from .scoring import *

RISK_REVIEW_GUIDANCE = {
    "base64-payload": "Decoded payloads can hide behavior; inspect the decoded content before using the skill.",
    "curl-pipe-shell": "Downloaded code is executed immediately; verify the source and prefer pinned local scripts.",
    "dynamic-exec": "Dynamic execution makes behavior harder to audit; check whether it is required.",
    "external-post": "The skill may send data out; confirm the destination and data type.",
    "install-hook": "Install-time hooks can run before the user invokes the skill; inspect the hook body.",
    "network-download": "The skill downloads remote content; confirm the source and pin the version.",
    "packaging-exec-surface": "Packaging files can execute local build code; inspect before relying on the package.",
    "protected-path-access": "The skill references private local paths; confirm that access is needed.",
    "private-content-artifact": "The bundle appears to contain credential-like content; remove it or rotate the key before using the skill.",
    "script-exec-call": "The script invokes a child process; inspect the called command and arguments.",
}

RISK_REVIEW_GUIDANCE_ZH_CN = {
    "base64-payload": "存在可解码载荷，使用前先看解码后的真实内容。",
    "curl-pipe-shell": "下载内容会被直接执行，先确认来源可信且最好固定到本地脚本。",
    "dynamic-exec": "动态执行会降低可审计性，确认它是否真的必要。",
    "external-post": "技能可能向外部发送数据，确认目的地和发送的数据类型。",
    "install-hook": "安装阶段钩子可能在用户调用前执行，先检查钩子内容。",
    "network-download": "技能会下载远程内容，确认来源可信且版本固定。",
    "packaging-exec-surface": "打包配置可能触发本地构建代码，继续使用前先检查。",
    "protected-path-access": "技能引用了受保护的本地路径，确认这种访问是否必要。",
    "private-content-artifact": "包内疑似包含凭证类内容，使用前应删除或轮换。",
    "script-exec-call": "脚本会调用子进程，检查具体命令和参数。",
}

ACTION_ADVICE = {
    "delete": "After agent review, remove it if the evidence still holds.",
    "merge-delete": "After agent review, move any useful parts into the stronger overlapping skill, then remove this one.",
    "merge-or-review": "Compare it with the overlapping skill, then decide which one should stay.",
    "observe-30d": "Keep it for now and watch real usage.",
    "quarantine-review": "Pause use for now; inspect the high-risk files before deciding whether to keep it.",
    "review-risk": "Check the risky behavior before continuing to use it.",
    "review-system": "Check this system skill because it carries higher-risk signals.",
    "keep-review-risk": "It looks useful; keep it after checking the risk signals.",
    "keep-review-burden": "It looks useful; simplify it to lower load or maintenance cost.",
    "review-burden": "Simplify it before deciding whether to keep it.",
    "review-vs-community": "Check community evidence and run a benchmark before changing it.",
    "review": "There is not enough evidence to decide yet; add usage or ablation results first.",
    "keep-narrow": "Keep it, but narrow the trigger or scope if it overlaps with another skill.",
    "keep": "Keep it; the evidence is strong enough.",
    "keep-system": "Keep it as a system skill.",
}

ACTION_ADVICE_ZH_CN = {
    "delete": "人工复核后建议移除；先按报告里的证据再确认一遍。",
    "merge-delete": "人工复核后建议合并再移除；先把有用部分并到更强的重叠技能。",
    "merge-or-review": "先和重叠技能对比，再决定留下哪一个。",
    "observe-30d": "建议暂时保留，继续看真实使用情况。",
    "quarantine-review": "建议先暂停使用；查清高风险文件后，再决定是否保留。",
    "review-risk": "建议先查风险行为，再决定是否继续使用。",
    "review-system": "系统技能带较高风险信号，建议先查清楚。",
    "keep-review-risk": "看起来有用，建议查清风险信号后再保留。",
    "keep-review-burden": "建议保留，同时压缩上下文和维护成本。",
    "review-burden": "建议先简化，再判断是否保留。",
    "review-vs-community": "建议先看社区证据并跑基准，再决定是否调整。",
    "review": "证据不足以支撑判断，先补使用或消融结果。",
    "keep-narrow": "建议保留；和其他技能重叠时，收窄触发或范围。",
    "keep": "建议保留；证据已经足够强。",
    "keep-system": "作为系统技能保留。",
}

KEEP_ACTIONS = {"keep", "keep-narrow", "keep-system"}
REVIEW_ACTIONS = {
    "merge-or-review",
    "quarantine-review",
    "review-risk",
    "review-system",
    "keep-review-risk",
    "keep-review-burden",
    "review-burden",
    "review-vs-community",
    "review",
}
REMOVE_ACTIONS = {"delete", "merge-delete"}
SUMMARY_INSTALL_GATE_VERDICTS = {
    "block-before-install",
    "review-before-install",
    "warn-before-install",
}

REPORT_TEXT = {
    "en": {
        "title": "Skill Usefulness Audit",
        "skills_audited": "Skills audited",
        "usage_files": "Usage files",
        "history_files": "History files",
        "ablation_files": "Ablation files",
        "community_files": "Community files",
        "report_mode": "Report mode",
        "recommended_actions": "Skills needing follow-up",
        "delete_candidates": "Recommended deletion candidates",
        "decision_summary": "Decision Summary",
        "decision_intro": "Start with the findings; the evidence tables explain each one.",
        "useful_count": "Useful enough to keep",
        "observe_count": "Keep watching for now",
        "review_count": "Needs manual review",
        "removal_count": "Possible duplicates or low-value skills",
        "install_gate_count": "Of these, risk needs attention",
        "useful_group": "Useful enough to keep",
        "observe_group": "Keep watching for now",
        "review_group": "Needs manual review",
        "removal_group": "Possible duplicates or low-value skills",
        "install_gate_group": "Risk subset requiring attention",
        "none": "None.",
        "more": "{count} more skills are listed in the evidence tables.",
        "score_word": "score",
        "call": "call",
        "calls": "calls",
        "recent_call": "recent call",
        "recent_calls": "recent calls",
        "no_usage": "no matching usage record",
        "missing_ablation": "no ablation result yet",
        "risk": "risk",
        "quality": "quality",
        "missing_env": "missing env",
        "install_gate": "risk note",
        "score_table": "Score Table",
        "score_axes_note": "Verdict is the score and evidence band. Action is the recommended next step after confidence, risk, and burden rules.",
        "cost_ablation_plan": "Cost-Efficient Ablation Plan",
        "strategy": "Strategy",
        "eligible_general_skills": "Eligible general skills",
        "candidate_skills": "Candidate skills",
        "deferred_general_skills": "Deferred general skills",
        "expected_model_cost_reduction": "Expected model-cost reduction vs {baseline_policy}-case full protocol",
        "expected_accuracy_impact": "Expected accuracy impact",
        "community_signal_breakdown": "Community Signal Breakdown",
        "quality_burden": "Maintenance Cost",
        "risk_review": "Risk Notes",
        "recommended_actions_heading": "Skills Needing Follow-Up",
        "delete_candidates_heading": "Recommended Delete Candidates",
        "missing_evidence": "Not Enough Evidence Yet",
        "not_audited_count": "Directories not audited",
        "not_audited": "Not Audited",
    },
    "zh-CN": {
        "title": "技能有用性审计",
        "skills_audited": "已审计技能",
        "usage_files": "使用数据文件",
        "history_files": "历史记录文件",
        "ablation_files": "消融数据文件",
        "community_files": "社区数据文件",
        "report_mode": "报告模式",
        "recommended_actions": "需进一步判断的技能",
        "delete_candidates": "建议删除候选数",
        "decision_summary": "决策摘要",
        "decision_intro": "先看判断结果；详细依据见后面的表格。",
        "useful_count": "建议保留",
        "observe_count": "建议暂时观察",
        "review_count": "建议人工复核",
        "removal_count": "疑似重复或低价值技能",
        "install_gate_count": "其中需注意风险",
        "useful_group": "建议保留",
        "observe_group": "建议暂时观察",
        "review_group": "建议人工复核",
        "removal_group": "疑似重复或低价值技能",
        "install_gate_group": "需注意的风险",
        "none": "无。",
        "more": "其余 {count} 个见后面的证据表。",
        "score_word": "分数",
        "call": "次调用",
        "calls": "次调用",
        "recent_call": "次调用",
        "recent_calls": "次调用",
        "no_usage": "没有匹配的使用记录",
        "missing_ablation": "还没有消融结果",
        "risk": "风险",
        "quality": "质量信号",
        "missing_env": "缺少环境变量",
        "install_gate": "风险提示",
        "score_table": "评分表",
        "score_axes_note": "结论表示分数和证据所处区间；建议是在此基础上结合置信度、风险和维护负担给出的下一步。",
        "cost_ablation_plan": "低成本消融计划",
        "strategy": "策略",
        "eligible_general_skills": "符合条件的通用技能",
        "candidate_skills": "候选技能",
        "deferred_general_skills": "暂缓的通用技能",
        "expected_model_cost_reduction": "相对 {baseline_policy} 例完整协议的预计模型成本降低",
        "expected_accuracy_impact": "预计准确性影响",
        "community_signal_breakdown": "社区信号拆解",
        "quality_burden": "维护负担",
        "risk_review": "风险提示",
        "recommended_actions_heading": "需进一步判断的技能",
        "delete_candidates_heading": "建议删除的候选",
        "missing_evidence": "证据不足以支撑判断",
        "not_audited_count": "未审查目录数",
        "not_audited": "未审查的目录",
    },
}

REPORT_TABLE_HEADERS = {
    "score": {
        "en": [
            "Rank",
            "Skill",
            "Source",
            "Kind",
            "Calls",
            "30-day calls",
            "Usage",
            "Unique",
            "Impact",
            "Community",
            "Confidence",
            "Risk",
            "Local",
            "Burden",
            "Final",
            "Verdict",
            "Action",
            "Basis",
        ],
        "zh-CN": [
            "排名",
            "技能",
            "来源",
            "类型",
            "调用",
            "近30天",
            "使用",
            "独特性",
            "影响",
            "社区",
            "置信度",
            "风险",
            "本地分",
            "负担",
            "最终分",
            "结论",
            "建议",
            "依据",
        ],
    },
    "ablation": {
        "en": ["Skill", "Priority", "Initial", "Expand", "Max", "Reasons"],
        "zh-CN": ["技能", "优先级", "初始例数", "扩展例数", "最大例数", "原因"],
    },
    "community": {
        "en": ["Skill", "Comm", "Confidence", "Components"],
        "zh-CN": ["技能", "社区分", "置信度", "组成"],
    },
    "quality": {
        "en": ["Skill", "Cost", "Raw cost", "Main flags", "Notes"],
        "zh-CN": ["技能", "成本", "原始成本", "主要问题", "说明"],
    },
    "risk": {
        "en": ["Skill", "Risk", "Flags", "Risk note", "Note"],
        "zh-CN": ["技能", "风险", "问题", "风险提示", "说明"],
    },
    "actions": {
        "en": ["Skill", "Local", "Burden", "Final", "Confidence", "Risk", "Action", "Advice"],
        "zh-CN": ["技能", "本地分", "负担", "最终分", "置信度", "风险", "建议", "说明"],
    },
    "delete": {
        "en": ["Skill", "Local", "Burden", "Final", "Kind", "Action", "Trigger", "Advice"],
        "zh-CN": ["技能", "本地分", "负担", "最终分", "类型", "建议", "触发原因", "说明"],
    },
    "missing": {
        "en": ["Skill", "Kind", "Needed evidence"],
        "zh-CN": ["技能", "类型", "需要补充的证据"],
    },
    "not_audited": {
        "en": ["Path", "Reason"],
        "zh-CN": ["路径", "原因"],
    },
}

MISSING_EVIDENCE_LABELS = {
    "en": {"usage": "usage", "ablation": "ablation", "community": "community"},
    "zh-CN": {"usage": "使用数据", "ablation": "消融数据", "community": "社区数据"},
}

INSTALL_GATE_LABELS = {
    "en": {
        "block-before-install": "high risk; pause use and fix it",
        "review-before-install": "risk present; check before continuing",
        "warn-before-install": "low risk; confirm it is expected",
        "no-static-risk-gate": "no static-risk block",
    },
    "zh-CN": {
        "block-before-install": "高风险，先暂停使用并处理",
        "review-before-install": "有风险，查清楚后再继续用",
        "warn-before-install": "低风险，确认符合预期",
        "no-static-risk-gate": "未发现静态风险拦截项",
    },
}

NOT_AUDITED_REASON_LABELS = {
    "en": {
        "no-skill-entry": "No SKILL.md; this audit only scores directories with a skill entry file.",
        "system-skipped": "System or built-in skill; skipped unless --include-system is used.",
        "duplicate-skill-install": "Same skill package was already audited once; use --show-duplicate-installs to list every installed copy.",
    },
    "zh-CN": {
        "no-skill-entry": "没有 SKILL.md；当前只审查有技能入口文件的目录。",
        "system-skipped": "系统或内置技能；默认跳过，需要时可加 --include-system。",
        "duplicate-skill-install": "同一个技能包已经审查过一次；如需列出每个安装位置，可加 --show-duplicate-installs。",
    },
}

ACTION_REASON_LABELS = {
    "zh-CN": {
        "system skill with high-risk patterns": "系统技能带高风险信号",
        "system skill": "系统技能",
        "high-risk patterns need a closer check": "高风险信号需要先查清楚",
        "useful locally with medium-risk patterns": "本地看起来有用，但存在中风险信号",
        "useful locally but expensive to maintain or load": "本地看起来有用，但维护或加载成本偏高",
        "maintenance cost lowers the final score": "维护成本拉低了最终分",
        "high final score": "最终分很高",
        "high overlap suggests narrower scope": "和其他技能重叠较高，适合收窄范围",
        "good final score": "最终分较好",
        "medium-risk patterns require review": "中风险信号需要先排查",
        "evidence confidence is low": "证据置信度偏低",
        "mid score with high overlap": "分数中等，且和其他技能重叠较高",
        "community signal is stronger than final score": "社区信号强于本地最终分",
        "mid final score": "最终分中等",
        "unused duplicate protected skill": "受保护技能未使用，且疑似重复",
        "protected skill has strong community signal": "受保护技能有较强社区信号",
        "protected skill scores low after burden": "受保护技能扣除负担后分数偏低",
        "community signal suggests benchmark before removal": "社区信号提示先跑基准再决定是否移除",
        "very low final score": "最终分很低",
        "low usage plus high overlap": "使用少，且和其他技能重叠较高",
        "low final score": "最终分偏低",
    },
}

QUALITY_REASON_ZH_CN = {
    "empty-skill-contract": "SKILL.md 没说清楚这个技能具体怎么用",
    "prompt-bloat": "SKILL.md 偏长，会占用较多共享上下文",
    "broad-trigger-surface": "入口说明的触发范围偏宽",
    "description-bloat": "入口说明偏长，路由不够清爽",
    "reference-disclosure-gap": "SKILL.md 没说清参考文件的加载路径",
    "reference-link-broken": "SKILL.md 指向了不存在的参考文件",
    "reference-bloat": "参考文件偏大，加载时容易浪费上下文",
    "long-reference-without-toc": "较长的参考文件缺少目录",
    "reference-content-pollution": "参考文件里混入了广告、推荐或无关内容",
    "asset-bloat": "assets 目录偏重",
    "vague-resource-names": "资源文件名太泛，不利于按需加载",
    "private-bundle-artifact": "包里有疑似私有或环境相关文件",
    "private-content-artifact": "包里有疑似凭证或密钥内容",
    "executable-asset": "assets 里包含可执行文件或安装器",
    "script-count-bloat": "脚本数量偏多",
    "script-maintenance-smell": "脚本可能需要本地修补",
    "script-syntax-error": "Python 脚本有语法错误",
    "script-import-error": "Python 脚本依赖的模块在本地或包内缺失",
    "overtrigger-low-execution": "触发很多，但真正执行很少",
    "overtrigger-misfire": "使用记录显示误触发偏多",
    "overtrigger-no-impact": "经常触发，但消融里收益不明显",
    "reference-overload": "使用记录显示参考文件加载偏重",
    "script-failure-burden": "使用记录显示脚本失败",
    "agent-repair-burden": "使用记录显示需要反复修补",
    "missing-required-env": "必需环境变量没有配置",
    "near-duplicate-instructions": "说明和另一个已安装技能高度相似",
}


def active_report_profile() -> str:
    profile_path = Path(__file__).resolve().parents[2] / REPORT_PROFILE_FILE
    try:
        if not profile_path.is_file():
            return ""
        return read_text(profile_path).strip().lower().replace("_", "-")
    except OSError:
        return ""


def chinese_only_report_profile_enabled() -> bool:
    return active_report_profile() == REPORT_PROFILE_ZH_CN_ONLY.lower()


def normalize_report_language(value: object) -> str:
    if chinese_only_report_profile_enabled():
        return "zh-CN"
    raw = str(value or "auto").strip()
    if not raw:
        return "en"
    normalized = raw.lower().replace("_", "-")
    if normalized == "auto":
        hint = ""
        for name in ("SKILL_AUDIT_REPORT_LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
            candidate = str(os.environ.get(name, "") or "").strip()
            if not candidate or candidate.lower().replace("_", "-") in {"c", "c.utf-8", "posix"}:
                continue
            hint = candidate
            break
        if not hint:
            hint = str(locale.getlocale()[0] or "")
        normalized = hint.lower().replace("_", "-") if hint else "en"
    if normalized in {"zh", "zh-cn", "zh-hans", "zh-sg", "cn", "chinese", "中文", "简体中文"}:
        return "zh-CN"
    if normalized.startswith("chinese (simplified)"):
        return "zh-CN"
    if normalized.startswith(("zh-cn.", "zh-hans.", "zh-sg.")):
        return "zh-CN"
    if normalized in {"en", "en-us", "en-gb", "english"}:
        return "en"
    if normalized.startswith("en-"):
        return "en"
    return "en"


def description_load_notice(
    skill_count: int,
    character_count: int,
    context_units: int,
    language: str,
) -> str:
    if normalize_report_language(language) == "zh-CN":
        return (
            f"> 本次审计纳入 {skill_count} 个 Skill；当前因这些 Skill 加载的入口描述共 "
            f"{character_count} 个字符，约合 {context_units} 个 token。"
        )
    skill_label = "skill" if skill_count == 1 else "skills"
    prompt_label = "Its loaded entry description contains" if skill_count == 1 else "Their loaded entry descriptions total"
    return (
        f"> This audit covers {skill_count} {skill_label}. {prompt_label} {character_count} characters, "
        f"about {context_units} tokens."
    )


def report_text(language: str, key: str) -> str:
    normalized = normalize_report_language(language)
    return REPORT_TEXT.get(normalized, REPORT_TEXT["en"]).get(key, REPORT_TEXT["en"][key])


def report_pair(language: str, label: str, value: object) -> str:
    separator = "：" if normalize_report_language(language) == "zh-CN" else ": "
    return f"{label}{separator}{value}"


def report_headers(language: str, table: str) -> list[str]:
    normalized = normalize_report_language(language)
    return REPORT_TABLE_HEADERS[table].get(normalized, REPORT_TABLE_HEADERS[table]["en"])


def missing_evidence_label(value: str, language: str) -> str:
    normalized = normalize_report_language(language)
    return MISSING_EVIDENCE_LABELS.get(normalized, MISSING_EVIDENCE_LABELS["en"]).get(value, value)


def not_audited_reason_label(value: str, language: str) -> str:
    normalized = normalize_report_language(language)
    return NOT_AUDITED_REASON_LABELS.get(normalized, NOT_AUDITED_REASON_LABELS["en"]).get(value, value)


def action_reason_for_report(value: str, language: str) -> str:
    normalized = normalize_report_language(language)
    reason = str(value or "").strip()
    if not reason:
        return "-"
    return ACTION_REASON_LABELS.get(normalized, {}).get(reason, reason)


def install_gate_label(value: str, language: str) -> str:
    normalized = normalize_report_language(language)
    return INSTALL_GATE_LABELS.get(normalized, INSTALL_GATE_LABELS["en"]).get(value, value)


def action_advice(action: str, reason: str) -> str:
    if action in ACTION_ADVICE:
        return ACTION_ADVICE[action]
    normalized_reason = reason.strip().rstrip(".")
    if normalized_reason:
        return f"Check the reason before changing anything: {normalized_reason}."
    return "Check the reason before changing anything."


def action_advice_for_report(action: str, reason: str, language: str = "en") -> str:
    if normalize_report_language(language) != "zh-CN":
        return action_advice(action, reason)
    if action in ACTION_ADVICE_ZH_CN:
        return ACTION_ADVICE_ZH_CN[action]
    normalized_reason = reason.strip().rstrip(".")
    if normalized_reason:
        return f"先看清原因，再改：{normalized_reason}。"
    return "先看清原因，再改。"


def _item_ablation_summary(item: dict[str, object]) -> dict[str, object] | None:
    score_breakdown = item.get("score_breakdown")
    if not isinstance(score_breakdown, dict):
        return None
    impact = score_breakdown.get("impact")
    if not isinstance(impact, dict):
        return None
    ablation = impact.get("ablation")
    return ablation if isinstance(ablation, dict) else None


def _quality_reason_parts(item: dict[str, object], language: str, limit: int = 2) -> list[str]:
    normalized_language = normalize_report_language(language)
    flags = [str(flag) for flag in list(item.get("quality_flags") or [])]
    if not flags:
        return []
    if normalized_language == "zh-CN":
        labels = [QUALITY_REASON_ZH_CN.get(flag, flag) for flag in flags[:limit]]
        return ["质量问题：" + "、".join(labels)]
    return ["quality issues: " + ", ".join(flags[:limit])]


def _deletion_evidence_parts(
    item: dict[str, object],
    language: str = "en",
    include_score_fallback: bool = True,
) -> list[str]:
    normalized_language = normalize_report_language(language)
    parts: list[str] = []

    calls = coerce_int(item.get("calls")) or 0
    usage_missing = bool(item.get("missing_usage")) or str(item.get("usage_source") or "") == "missing"
    if calls == 0 and not usage_missing:
        parts.append("没有使用记录" if normalized_language == "zh-CN" else "no recorded use")

    overlap = coerce_float(item.get("overlap_value"))
    peer = str(item.get("overlap_peer") or "").strip()
    if overlap is not None and overlap >= HIGH_OVERLAP_THRESHOLD:
        if normalized_language == "zh-CN":
            parts.append(f"和 {peer} 高度重叠" if peer else "和其他技能高度重叠")
        else:
            parts.append(f"high overlap with {peer}" if peer else "high overlap with another skill")

    ablation = _item_ablation_summary(item)
    if ablation:
        cases = coerce_int(ablation.get("cases")) or 0
        consistency = coerce_float(ablation.get("consistency_rate")) or 0.0
        better = coerce_float(ablation.get("better_rate")) or 0.0
        if cases and consistency >= NO_IMPACT_CONSISTENCY_THRESHOLD and better <= NO_IMPACT_BETTER_THRESHOLD:
            parts.append(
                "消融结果没有看到收益"
                if normalized_language == "zh-CN"
                else "ablation shows no clear gain"
            )

    parts.extend(_quality_reason_parts(item, normalized_language))

    final_score = coerce_float(item.get("final_score"))
    if include_score_fallback and not parts and final_score is not None and final_score < 4.0:
        parts.append("最终分偏低" if normalized_language == "zh-CN" else "low final score")

    return list(dict.fromkeys(part for part in parts if part))


def action_advice_for_item(item: dict[str, object], language: str = "en") -> str:
    normalized_language = normalize_report_language(language)
    action = _item_action(item)
    if action in REMOVE_ACTIONS or bool(item.get("delete_candidate")):
        parts = _deletion_evidence_parts(item, normalized_language)
        if normalized_language == "zh-CN":
            prefix = "人工复核后建议合并后移除" if action == "merge-delete" else "人工复核后建议移除"
            return f"{prefix}：{'；'.join(parts)}。" if parts else action_advice_for_report(action, str(item.get("action_reason") or ""), normalized_language)
        prefix = "After agent review, merge then remove it" if action == "merge-delete" else "After agent review, remove it"
        return f"{prefix}: {'; '.join(parts)}." if parts else action_advice_for_report(action, str(item.get("action_reason") or ""), normalized_language)
    return action_advice_for_report(action, str(item.get("action_reason") or ""), normalized_language)


def short_risk_flags(flags: list[str]) -> str:
    if not flags:
        return ""
    return ",".join(flags[:2])


def _item_display_name(item: dict[str, object]) -> str:
    return str(item.get("display_name") or item.get("name") or "unknown-skill")


def _item_action(item: dict[str, object]) -> str:
    return str(item.get("action") or "review")


def _item_install_gate_verdict(item: dict[str, object]) -> str:
    install_gate = item.get("install_gate")
    if isinstance(install_gate, dict):
        return str(install_gate.get("verdict") or "")
    return ""


def _summary_reason(item: dict[str, object], language: str = "en") -> str:
    normalized_language = normalize_report_language(language)
    parts: list[str] = []
    action = _item_action(item)
    removal_action = action in REMOVE_ACTIONS or bool(item.get("delete_candidate"))
    final_score = coerce_float(item.get("final_score"))
    if final_score is not None:
        parts.append(f"{report_text(normalized_language, 'score_word')} {fmt_score(final_score)}")

    calls = coerce_int(item.get("calls")) or 0
    recent_30d = coerce_int(item.get("recent_30d_calls"))
    if calls:
        call_key = "call" if calls == 1 else "calls"
        if normalized_language == "zh-CN":
            parts.append(f"{calls}{report_text(normalized_language, call_key)}")
        else:
            parts.append(f"{calls} {report_text(normalized_language, call_key)}")
    elif item.get("missing_usage"):
        parts.append(report_text(normalized_language, "no_usage"))
    if recent_30d:
        recent_key = "recent_call" if recent_30d == 1 else "recent_calls"
        if normalized_language == "zh-CN":
            parts.append(f"近30天 {recent_30d}{report_text(normalized_language, recent_key)}")
        else:
            parts.append(f"{recent_30d} {report_text(normalized_language, recent_key)}")

    if removal_action:
        parts.extend(_deletion_evidence_parts(item, normalized_language, include_score_fallback=False))

    if item.get("missing_ablation"):
        parts.append(report_text(normalized_language, "missing_ablation"))

    risk_level = str(item.get("risk_level") or "none")
    risk_flags = list(item.get("risk_flags") or [])
    if risk_level != "none":
        flags = short_risk_flags([str(flag) for flag in risk_flags])
        if normalized_language == "zh-CN":
            risk_label = {"high": "高", "medium": "中", "low": "低"}.get(risk_level, risk_level)
            parts.append(f"{risk_label}{report_text(normalized_language, 'risk')}" + (f"：{flags}" if flags else ""))
        else:
            parts.append(f"{risk_level} {report_text(normalized_language, 'risk')}" + (f": {flags}" if flags else ""))

    quality_flags = [str(flag) for flag in list(item.get("quality_flags") or [])]
    if quality_flags and not removal_action:
        parts.append(report_pair(normalized_language, report_text(normalized_language, "quality"), short_risk_flags(quality_flags)))

    missing_env = [str(name) for name in list(item.get("missing_required_env") or [])]
    if missing_env:
        suffix = f"+{len(missing_env) - 2} more" if len(missing_env) > 2 else ""
        env_summary = ",".join(missing_env[:2])
        parts.append(
            report_pair(normalized_language, report_text(normalized_language, "missing_env"), env_summary)
            + (f",{suffix}" if suffix else "")
        )

    install_gate = _item_install_gate_verdict(item)
    if install_gate in SUMMARY_INSTALL_GATE_VERDICTS:
        parts.append(
            report_pair(
                normalized_language,
                report_text(normalized_language, "install_gate"),
                install_gate_label(install_gate, normalized_language),
            )
        )

    if not parts:
        parts.append(action_advice_for_report(action, str(item.get("action_reason") or ""), normalized_language))
    separator = "；" if normalized_language == "zh-CN" else "; "
    return separator.join(dict.fromkeys(part for part in parts if part))


def _summary_group(title_key: str, items: list[dict[str, object]], limit: int, language: str) -> list[str]:
    normalized_language = normalize_report_language(language)
    lines = [f"### {report_text(normalized_language, title_key)}", ""]
    if not items:
        lines.append(f"- {report_text(normalized_language, 'none')}")
        return lines
    sentence_end = "。" if normalized_language == "zh-CN" else "."
    action_separator = "。" if normalized_language == "zh-CN" else ". "
    name_separator = "：" if normalized_language == "zh-CN" else ": "
    for item in items[:limit]:
        reason = _summary_reason(item, normalized_language)
        if normalized_language == "en" and reason:
            reason = reason[:1].upper() + reason[1:]
        lines.append(
            f"- {_item_display_name(item)}{name_separator}`{_item_action(item)}`"
            f"{action_separator}{reason}{sentence_end}"
        )
    if len(items) > limit:
        lines.append(f"- {report_text(normalized_language, 'more').format(count=len(items) - limit)}")
    return lines


def decision_summary(ranked: list[dict[str, object]], limit: int = 5, language: str = "en") -> list[str]:
    normalized_language = normalize_report_language(language)
    useful = [item for item in ranked if _item_action(item) in KEEP_ACTIONS]
    observe = [item for item in ranked if _item_action(item) == "observe-30d"]
    review = [item for item in ranked if _item_action(item) in REVIEW_ACTIONS]
    removal = [
        item
        for item in ranked
        if _item_action(item) in REMOVE_ACTIONS or bool(item.get("delete_candidate"))
    ]
    install_gate = [
        item
        for item in ranked
        if _item_install_gate_verdict(item) in SUMMARY_INSTALL_GATE_VERDICTS
    ]

    lines = [
        f"## {report_text(normalized_language, 'decision_summary')}",
        "",
        report_text(normalized_language, "decision_intro"),
        "",
        f"- {report_pair(normalized_language, report_text(normalized_language, 'useful_count'), len(useful))}",
        f"- {report_pair(normalized_language, report_text(normalized_language, 'observe_count'), len(observe))}",
        f"- {report_pair(normalized_language, report_text(normalized_language, 'review_count'), len(review))}",
        f"- {report_pair(normalized_language, report_text(normalized_language, 'removal_count'), len(removal))}",
        f"- {report_pair(normalized_language, report_text(normalized_language, 'install_gate_count'), len(install_gate))}",
        "",
    ]
    for group in (
        _summary_group("useful_group", useful, limit, normalized_language),
        _summary_group("observe_group", observe, limit, normalized_language),
        _summary_group("review_group", review, limit, normalized_language),
        _summary_group("removal_group", removal, limit, normalized_language),
        _summary_group("install_gate_group", install_gate, limit, normalized_language),
    ):
        lines.extend(group)
        lines.append("")
    return lines[:-1]


def _has_direct_usage(item: dict[str, object]) -> bool:
    if str(item.get("usage_source") or "") != "usage":
        return False
    calls = coerce_int(item.get("calls")) or 0
    recent_calls = coerce_int(item.get("recent_30d_calls")) or 0
    return calls > 0 or recent_calls > 0


def _concise_name_list(items: list[dict[str, object]], language: str, limit: int = 3) -> str:
    names = [_item_display_name(item) for item in items[:limit]]
    remaining = len(items) - len(names)
    if normalize_report_language(language) == "zh-CN":
        text = "、".join(names)
        return f"{text}等{len(items)}个技能" if remaining > 0 else text
    if len(names) == 2:
        text = f"{names[0]} and {names[1]}"
    elif len(names) > 2:
        text = ", ".join(names[:-1]) + f", and {names[-1]}"
    else:
        text = names[0] if names else ""
    return f"{text}, among {len(items)} skills" if remaining > 0 else text


def _concise_usage_item(item: dict[str, object], language: str) -> str:
    name = _item_display_name(item)
    recent_calls = coerce_int(item.get("recent_30d_calls"))
    calls = coerce_int(item.get("calls")) or 0
    if normalize_report_language(language) == "zh-CN":
        if recent_calls is not None and recent_calls > 0:
            return f"{name}（近30天使用{recent_calls}次）"
        return f"{name}（累计使用{calls}次）"
    if recent_calls is not None and recent_calls > 0:
        use_word = "use" if recent_calls == 1 else "uses"
        return f"{name} ({recent_calls} {use_word} in the last 30 days)"
    use_word = "use" if calls == 1 else "uses"
    return f"{name} ({calls} recorded {use_word})"


def _concise_usage_list(items: list[dict[str, object]], language: str, limit: int = 3) -> str:
    labels = [_concise_usage_item(item, language) for item in items[:limit]]
    remaining = len(items) - len(labels)
    if normalize_report_language(language) == "zh-CN":
        text = "、".join(labels)
        return f"{text}等{len(items)}个技能" if remaining > 0 else text
    if len(labels) == 2:
        text = f"{labels[0]} and {labels[1]}"
    elif len(labels) > 2:
        text = ", ".join(labels[:-1]) + f", and {labels[-1]}"
    else:
        text = labels[0] if labels else ""
    return f"{text}, among {len(items)} skills" if remaining > 0 else text


def _concise_review_reason(item: dict[str, object], language: str) -> str:
    normalized_language = normalize_report_language(language)
    parts = _deletion_evidence_parts(item, normalized_language, include_score_fallback=False)
    allowed: list[str] = []
    for part in parts:
        lowered = part.lower()
        if lowered.startswith(("质量问题", "quality issues")):
            continue
        if normalized_language == "zh-CN" and part == "消融结果没有看到收益":
            allowed.append("对照结果没有显示明显收益")
            continue
        if normalized_language == "en" and lowered == "ablation shows no clear gain":
            allowed.append("the comparison showed no clear benefit")
            continue
        allowed.append(part)
    if allowed:
        separator = "，" if normalized_language == "zh-CN" else "; "
        return separator.join(allowed)
    return "现有记录显示作用有限" if normalized_language == "zh-CN" else "the current evidence shows limited value"


def concise_report(
    ranked: list[dict[str, object]],
    language: str = "en",
    markdown_path: Path | None = None,
    not_audited_count: int = 0,
    entry_prompt_characters: int = 0,
    entry_prompt_tokens: int = 0,
    limit: int = 3,
) -> str:
    """Render a short usefulness-focused stdout summary without internal action codes."""
    normalized_language = normalize_report_language(language)
    review = [item for item in ranked if bool(item.get("delete_candidate"))]
    used = [item for item in ranked if _has_direct_usage(item)]
    undecided = [item for item in ranked if item not in review and item not in used]
    headline_args = (len(ranked), len(used), len(undecided), len(review), entry_prompt_characters, entry_prompt_tokens)
    if normalized_language == "zh-CN":
        headline = _concise_headline_zh_cn(*headline_args)
    else:
        headline = _concise_headline_en(*headline_args)
    lines = [headline]
    lines.extend(
        _concise_section_lines(used, undecided, review, not_audited_count, markdown_path, limit, normalized_language)
    )
    return "\n".join(lines)


def _concise_headline_zh_cn(
    ranked_count: int,
    used_count: int,
    undecided_count: int,
    review_count: int,
    entry_prompt_characters: int,
    entry_prompt_tokens: int,
) -> str:
    headline = (
        f"本次审计了{ranked_count}个技能。当前因这些技能加载的入口描述共"
        f"{entry_prompt_characters}个字符，约合{entry_prompt_tokens}个token。"
    )
    status_present = False
    if used_count and used_count == ranked_count:
        headline += "这个技能有明确使用记录。" if ranked_count == 1 else "这些技能都有明确使用记录。"
        status_present = True
    elif undecided_count and undecided_count == ranked_count:
        headline += "这个技能的使用情况目前还不清楚。" if ranked_count == 1 else "这些技能的使用情况目前都不清楚。"
        status_present = True
    else:
        status_parts = []
        if used_count:
            status_parts.append(f"{used_count}个有明确使用记录")
        if undecided_count:
            status_parts.append(f"{undecided_count}个的使用情况仍不清楚")
        if status_parts:
            headline += "其中" + "，".join(status_parts) + "。"
            status_present = True
    if review_count:
        connector = "同时有" if status_present else "其中有"
        headline += f"{connector}{review_count}个达到重点复查条件。"
    return headline


def _concise_headline_en(
    ranked_count: int,
    used_count: int,
    undecided_count: int,
    review_count: int,
    entry_prompt_characters: int,
    entry_prompt_tokens: int,
) -> str:
    skill_word = "skill" if ranked_count == 1 else "skills"
    description_noun = "description contains" if ranked_count == 1 else "descriptions contain"
    headline = (
        f"This audit reviewed {ranked_count} {skill_word}. The loaded skill entry {description_noun} "
        f"{entry_prompt_characters} characters, about {entry_prompt_tokens} tokens."
    )
    status_present = False
    if used_count and used_count == ranked_count:
        headline += " It has clear usage evidence." if ranked_count == 1 else " All of them have clear usage evidence."
        status_present = True
    elif undecided_count and undecided_count == ranked_count:
        headline += " Its usage remains unclear." if ranked_count == 1 else " Their usage remains unclear."
        status_present = True
    elif used_count:
        used_word = "skill has" if used_count == 1 else "skills have"
        headline += f" {used_count} {used_word} clear usage evidence."
        status_present = True
    if undecided_count:
        if undecided_count != ranked_count:
            undecided_word = "skill remains" if undecided_count == 1 else "skills remain"
            headline += f" {undecided_count} {undecided_word} undecided."
            status_present = True
    if review_count:
        review_noun = "skill" if review_count == 1 else "skills"
        review_verb = "needs" if review_count == 1 else "need"
        adverb = " also" if status_present else ""
        headline += f" {review_count} {review_noun}{adverb} {review_verb} closer review."
    return headline


def _concise_section_lines(
    used: list[dict[str, object]],
    undecided: list[dict[str, object]],
    review: list[dict[str, object]],
    not_audited_count: int,
    markdown_path: Path | None,
    limit: int,
    normalized_language: str,
) -> list[str]:
    lines: list[str] = []
    if used:
        usage_list = _concise_usage_list(used, normalized_language, limit)
        if normalized_language == "zh-CN":
            lines.append(f"常用技能：{usage_list}。")
        else:
            lines.append(f"Frequently used skills: {usage_list}.")
    if undecided:
        name_list = _concise_name_list(undecided, normalized_language, limit)
        if normalized_language == "zh-CN":
            lines.append(f"暂时无法判断：{name_list}。现有记录不足，暂不建议移除。")
        else:
            lines.append(f"Undecided: {name_list}. The available records are not enough to support removal.")
    for item in review[:limit]:
        reason = _concise_review_reason(item, normalized_language)
        if normalized_language == "zh-CN":
            lines.append(f"建议复查：{_item_display_name(item)}。{reason}；是否移除仍需人工确认。")
        else:
            reason = reason[:1].upper() + reason[1:]
            lines.append(
                f"Review closely: {_item_display_name(item)}. {reason}; "
                "confirm the evidence before removing it."
            )
    if len(review) > limit:
        extra = len(review) - limit
        if normalized_language == "zh-CN":
            lines.append(f"另外{extra}个复查对象见完整依据。")
        else:
            extra_word = "skill" if extra == 1 else "skills"
            lines.append(f"The full evidence lists {extra} more {extra_word} for review.")
    if not_audited_count:
        if normalized_language == "zh-CN":
            lines.append(f"另有{not_audited_count}个目录未纳入判断，原因见完整依据。")
        else:
            directory_word = "directory was" if not_audited_count == 1 else "directories were"
            lines.append(f"{not_audited_count} {directory_word} not included; the full evidence explains why.")
    if markdown_path is not None:
        if normalized_language == "zh-CN":
            lines.append(f"完整依据已保存到：{markdown_path}。")
        else:
            lines.append(f"Full evidence: {markdown_path}.")
    return lines


def risk_review_summary(level: str, evidence: list[dict[str, object]]) -> str:
    if not evidence:
        return ""
    labels = [str(item.get("label", "")) for item in evidence if item.get("label")]
    guidance = [RISK_REVIEW_GUIDANCE.get(label, "Check this signal before using or keeping the skill.") for label in labels[:3]]
    prefix = {
        "high": "High risk: fix the flagged issue before using or keeping it.",
        "medium": "Medium risk: check the flagged behavior before using or keeping it.",
        "low": "Low risk: check if expected.",
    }.get(level, "Check the flagged behavior.")
    return f"{prefix} " + " ".join(dict.fromkeys(guidance))


def risk_review_summary_for_report(level: str, evidence: list[dict[str, object]], language: str = "en") -> str:
    if normalize_report_language(language) != "zh-CN":
        return risk_review_summary(level, evidence)
    if not evidence:
        return ""
    labels = [str(item.get("label", "")) for item in evidence if item.get("label")]
    guidance = [
        RISK_REVIEW_GUIDANCE_ZH_CN.get(label, "使用或保留前先看这个风险信号。")
        for label in labels[:3]
    ]
    prefix = {
        "high": "高风险：先处理风险，再考虑使用或保留。",
        "medium": "中风险：先查清楚风险，再决定是否使用或保留。",
        "low": "低风险：确认这是预期行为。",
    }.get(level, "建议先查清楚。")
    return prefix + "".join(dict.fromkeys(guidance))


def install_gate_summary(level: str, evidence: list[dict[str, object]]) -> dict[str, str]:
    flags = [str(item.get("label", "")) for item in evidence if item.get("label")]
    if level == "high":
        return {
            "verdict": "block-before-install",
            "reason": "High-risk static signals should pause use until the flagged issue is fixed.",
        }
    if level == "medium":
        return {
            "verdict": "review-before-install",
            "reason": "Medium-risk static signals need a check before continued use.",
        }
    if level == "low":
        return {
            "verdict": "warn-before-install",
            "reason": "Low-risk static signals should be checked before continued use.",
        }
    if flags:
        return {
            "verdict": "review-before-install",
            "reason": "Static signals were present but unclassified; check them before continued use.",
        }
    return {
        "verdict": "no-static-risk-gate",
        "reason": "No static risk gate was triggered; still inspect the source before relying on it.",
    }


def build_basis(
    usage_record: dict[str, object],
    usage_source: str,
    evidence_weight: float,
    overlap_peer: str | None,
    overlap_value: float,
    kind: str,
    ablation: dict[str, float] | None,
    community_prior: float | None,
    risk_flags: list[str],
    quality_penalty_value: float,
    quality_flags: list[str],
    evidence_note: str | None,
) -> str:
    parts = [f"calls={int(usage_record.get('calls', 0) or 0)}"]
    history_mentions = int(usage_record.get("history_mentions", 0) or 0)
    if history_mentions:
        parts.append(f"history_mentions={history_mentions}")
    recent_30d_calls = coerce_int(usage_record.get("recent_30d_calls"))
    if recent_30d_calls is not None:
        parts.append(f"30d={recent_30d_calls}")
    if usage_record.get("last_used_at"):
        parts.append(f"last={usage_record['last_used_at']}")
    parts.append(f"usage={usage_source}@{evidence_weight:.2f}")
    if overlap_peer:
        parts.append(f"overlap={overlap_peer}({overlap_value:.2f})")
    if kind == "general":
        if ablation and ablation.get("cases", 0) > 0:
            parts.append(f"same={ablation['consistency_rate']:.2f}")
            parts.append(f"better={ablation['better_rate']:.2f}")
        else:
            parts.append("ablation=missing")
    else:
        parts.append("impact=protected-capability")
    if community_prior is not None:
        parts.append(f"community={community_prior:.2f}")
    if risk_flags:
        parts.append(f"risk={short_risk_flags(risk_flags)}")
    if quality_penalty_value > 0:
        parts.append(f"burden={quality_penalty_value:.2f}")
    if quality_flags:
        parts.append(f"quality={short_risk_flags(quality_flags)}")
    if evidence_note:
        parts.append(f"note={evidence_note}")
    return "; ".join(parts)


def escape_markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    escaped_headers = [escape_markdown_cell(header) for header in headers]
    lines = ["| " + " | ".join(escaped_headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    lines.extend("| " + " | ".join(escape_markdown_cell(cell) for cell in row) + " |" for row in rows)
    return "\n".join(lines)


def fmt_optional_int(value) -> str:
    coerced = coerce_int(value)
    return "-" if coerced is None else str(coerced)


def fmt_optional_float(value, digits: int = 2) -> str:
    coerced = coerce_float(value)
    return "-" if coerced is None else f"{coerced:.{digits}f}"


def fmt_score(value) -> str:
    coerced = coerce_float(value)
    if coerced is None:
        return "-"
    one_decimal = f"{coerced:.1f}"
    if abs(coerced - float(one_decimal)) < 1e-9:
        return one_decimal
    return f"{coerced:.2f}"


def fmt_breakdown_components(breakdown: dict[str, float]) -> str:
    if not breakdown:
        return "-"
    order = [
        "rating",
        "current_installs_or_downloads",
        "installs_all_time",
        "trending_7d",
        "stars",
        "comments_count",
        "maintenance",
    ]
    ordered_keys = [key for key in order if key in breakdown]
    ordered_keys.extend(sorted(key for key in breakdown if key not in set(order)))
    return ", ".join(f"{key}={breakdown[key]:.3f}" for key in ordered_keys)


def summarize_quality_evidence(evidence: list[dict[str, object]], limit: int = 3, language: str = "en") -> str:
    if not evidence:
        return "-"
    normalized_language = normalize_report_language(language)
    parts = []
    for item in evidence[:limit]:
        label = str(item.get("label", "quality"))
        if normalized_language == "zh-CN":
            reason = QUALITY_REASON_ZH_CN.get(label, str(item.get("reason", "")).strip())
        else:
            reason = str(item.get("reason", "")).strip()
        penalty = fmt_optional_float(item.get("penalty"))
        detail_separator = "：" if normalized_language == "zh-CN" else ": "
        parts.append(
            f"{label}({penalty}){detail_separator}{reason}"
            if reason
            else f"{label}({penalty})"
        )
    if len(evidence) > limit:
        suffix = f"+{len(evidence) - limit} 项" if normalized_language == "zh-CN" else f"+{len(evidence) - limit} more"
        parts.append(suffix)
    separator = "；" if normalized_language == "zh-CN" else "; "
    return separator.join(parts)


def determine_report_mode(
    usage_paths: list[Path],
    history_paths: list[Path],
    ablation_paths: list[Path],
    results: list[dict[str, object]],
) -> str:
    if not usage_paths and not history_paths and not ablation_paths:
        return "structure-only"
    if any(item["missing_usage"] or item["missing_ablation"] for item in results):
        return "partial-evidence"
    return "strong-evidence"


def ablation_priority(item: dict[str, object]) -> tuple[float, list[str]]:
    if item["kind"] != "general":
        return 0, []
    ablation = item.get("score_breakdown", {}).get("impact", {}).get("ablation")  # type: ignore[union-attr]
    cases = int((ablation or {}).get("cases", 0)) if isinstance(ablation, dict) else 0
    consistency = float((ablation or {}).get("consistency_rate", 0.0)) if isinstance(ablation, dict) else 0.0
    better = float((ablation or {}).get("better_rate", 0.0)) if isinstance(ablation, dict) else 0.0
    has_review_signal = (
        float(item["final_score"]) < SCORE_KEEP_NARROW_THRESHOLD
        or float(item["overlap_value"]) >= HIGH_OVERLAP_THRESHOLD
        or float(item["quality_penalty"]) > 0
        or str(item["action"]) not in {"keep", "keep-narrow", "keep-system"}
    )
    if not has_review_signal:
        return 0, ["clean keep recommendation"]

    score = 0.0
    reasons: list[str] = []
    if cases >= 5:
        score += 1.0
        reasons.append("refresh existing ablation")
        if consistency >= NO_IMPACT_CONSISTENCY_THRESHOLD and better <= NO_IMPACT_BETTER_THRESHOLD:
            score += 1.0
            reasons.append("prior no-impact ablation")
    if item["missing_ablation"]:
        score += 2
        reasons.append("missing ablation")
    if float(item["final_score"]) < SCORE_KEEP_NARROW_THRESHOLD:
        score += 2
        reasons.append("weak final score")
    if float(item["overlap_value"]) >= HIGH_OVERLAP_THRESHOLD:
        score += 2
        reasons.append("high overlap")
    if float(item["quality_penalty"]) >= QUALITY_BURDEN_HIGH_THRESHOLD:
        score += 2
        reasons.append("high quality burden")
    elif float(item["quality_penalty"]) > 0:
        score += 1
        reasons.append("some quality burden")
    if int(item["calls"]) >= 5:
        score += 1
        reasons.append("frequent activation")
    if str(item["usage_source"]) == "missing":
        score += 1
        reasons.append("missing usage evidence")
    elif str(item["usage_source"]) == "history":
        score += 0.5
        reasons.append("history-only usage evidence")
    if float(item["confidence_score"]) < LOW_CONFIDENCE_THRESHOLD:
        score += 1
        reasons.append("low confidence")
    if str(item["action"]) not in {"keep", "keep-narrow", "keep-system"}:
        score += 1
        reasons.append(f"action={item['action']}")
    return score, reasons


def estimate_model_cost(case_count: int) -> dict[str, int]:
    return {name: case_count * per_case for name, per_case in ABLATION_COST_PROFILES.items()}


def reduction_percent(planned: int, baseline: int) -> float:
    if baseline <= 0:
        return 0.0
    return round(clamp(1.0 - planned / baseline, 0.0, 1.0) * 100, 1)


def accuracy_impact(candidates: list[dict[str, object]], deferred: list[dict[str, object]]) -> dict[str, object]:
    risky_deferred = [
        item
        for item in deferred
        if item["kind"] == "general"
        and item["missing_ablation"]
        and (
            float(item["final_score"]) < SCORE_KEEP_NARROW_THRESHOLD
            or float(item["overlap_value"]) >= HIGH_OVERLAP_THRESHOLD
            or float(item["quality_penalty"]) >= QUALITY_BURDEN_HIGH_THRESHOLD
        )
    ]
    if not candidates:
        level = "high"
        reason = "no general skill was selected for ablation"
    elif risky_deferred:
        level = "medium"
        reason = f"{len(risky_deferred)} deferred general skills still carry weak-score, overlap, or burden signals"
    else:
        level = "low"
        reason = "deferred skills have stronger local evidence or lower ablation priority"
    return {
        "expected_accuracy_impact": level,
        "reason": reason,
        "mitigations": [
            "use pairwise A/B comparison instead of single-output grading",
            "expand from 3 to 5 cases when the first batch is mixed",
            "expand to 10 cases only for decision-boundary skills",
            "cache replay outputs by skill, case, model, prompt, and artifact hash",
            "review deferred skills when new usage or quality-burden evidence appears",
        ],
    }


def ablation_result_identity(item: dict[str, object]) -> str:
    return ablation_result_identities(item)[0]


def ablation_result_identities(item: dict[str, object]) -> list[str]:
    install_identities = item.get("install_identities")
    if isinstance(install_identities, list):
        identities = [f"install:{identity}" for identity in install_identities if identity]
        if identities:
            return identities
    install_identity = str(item.get("install_identity") or "")
    if install_identity:
        return [f"install:{install_identity}"]
    return [f"path:{item['path']}"]


def unique_ablation_results(results: list[dict[str, object]]) -> list[dict[str, object]]:
    unique: list[dict[str, object]] = []
    seen: set[str] = set()
    for item in results:
        identities = ablation_result_identities(item)
        if any(identity in seen for identity in identities):
            continue
        seen.update(identities)
        unique.append(item)
    return unique


def build_ablation_plan(
    results: list[dict[str, object]],
    max_candidates: int = ABLATION_DEFAULT_MAX_CANDIDATES,
    baseline_cases_per_skill: int = ABLATION_BASELINE_CASES,
    initial_cases_per_candidate: int = ABLATION_INITIAL_CASES,
    expand_to_cases: int = ABLATION_EXPAND_CASES,
    max_cases_per_candidate: int = ABLATION_MAX_CASES,
) -> dict[str, object]:
    baseline_cases_per_skill = max(1, baseline_cases_per_skill)
    initial_cases_per_candidate = max(1, initial_cases_per_candidate)
    expand_to_cases = max(initial_cases_per_candidate, expand_to_cases)
    max_cases_per_candidate = max(expand_to_cases, max_cases_per_candidate)
    general = unique_ablation_results([item for item in results if item["kind"] == "general"])
    scored: list[tuple[float, dict[str, object], list[str]]] = []
    for item in general:
        score, reasons = ablation_priority(item)
        scored.append((score, item, reasons))

    scored.sort(key=lambda entry: (-entry[0], float(entry[1]["final_score"]), str(entry[1]["display_name"])))
    positive = [entry for entry in scored if entry[0] >= 3]
    if not positive:
        positive = [entry for entry in scored if entry[0] > 0][:ABLATION_MIN_CANDIDATES]
    candidate_entries = positive[:max_candidates]
    candidate_paths = {str(entry[1]["path"]) for entry in candidate_entries}

    candidates = []
    for priority, item, reasons in candidate_entries:
        candidates.append(
            {
                "skill": item["display_name"],
                "path": item["path"],
                "priority_score": priority,
                "priority_reasons": reasons,
                "initial_cases": initial_cases_per_candidate,
                "expand_to": expand_to_cases,
                "max_cases": max_cases_per_candidate,
                "recommended_judge": "pairwise A/B comparison with pass/fail and same/better/worse labels",
                "case_selection": [
                    "prefer real production/history prompts where the skill triggered",
                    "include tasks near the skill boundary or with prior repair burden",
                    "deduplicate prompts by normalized text and artifact hash",
                ],
            }
        )

    deferred = []
    deferred_entries = [entry for entry in scored if str(entry[1]["path"]) not in candidate_paths]
    deferred_items = [entry[1] for entry in deferred_entries]
    for priority, item, reasons in deferred_entries:
        deferred.append(
            {
                "skill": item["display_name"],
                "path": item["path"],
                "priority_score": priority,
                "defer_reasons": reasons or ["low ablation priority"],
                "local_score": item["local_score"],
                "quality_penalty": item["quality_penalty"],
                "final_score": item["final_score"],
            }
        )

    eligible_count = len(general)
    candidate_count = len(candidates)
    baseline_cases = eligible_count * baseline_cases_per_skill
    initial_cases = candidate_count * initial_cases_per_candidate
    expected_cases = candidate_count * expand_to_cases
    max_cases = candidate_count * max_cases_per_candidate
    baseline_cost = estimate_model_cost(baseline_cases)
    initial_cost = estimate_model_cost(initial_cases)
    expected_cost = estimate_model_cost(expected_cases)
    max_cost = estimate_model_cost(max_cases)

    return {
        "strategy": "triage-pairwise-early-stop",
        "eligible_general_skills": eligible_count,
        "candidate_skills": candidate_count,
        "deferred_general_skills": len(deferred),
        "case_policy": {
            "baseline_cases_per_general_skill": baseline_cases_per_skill,
            "initial_cases_per_candidate": initial_cases_per_candidate,
            "expand_to_cases": expand_to_cases,
            "max_cases_per_candidate": max_cases_per_candidate,
        },
        "stop_rules": {
            "stop_delete_candidate": f"{initial_cases_per_candidate}/{initial_cases_per_candidate} cases are same and better_rate is 0",
            "stop_keep_candidate": f"{math.ceil(initial_cases_per_candidate * 2 / 3)}/{initial_cases_per_candidate} or better show clear improvement and no worse cases",
            "expand": "mixed first batch or final_score is between 3.0 and 6.5",
            "max": "only for high-impact or deletion-boundary decisions",
        },
        "judge_protocol": {
            "mode": "pairwise",
            "bias_control": "randomize A/B order and spot-check reversed order on boundary cases",
            "labels": ["better", "same", "worse"],
            "deterministic_metrics": ["pass", "score", "tool_cost", "latency", "repair_turns"],
        },
        "cache_keys": ["skill", "case_id", "model", "prompt_hash", "artifact_hash", "skill_version"],
        "model_cost_estimates": {
            "unit": ABLATION_COST_UNIT,
            "profiles_per_case_units": ABLATION_COST_PROFILES,
            "baseline_full_protocol": {
                "cases": baseline_cases,
                "model_cost_units": baseline_cost,
            },
            "planned_initial": {
                "cases": initial_cases,
                "model_cost_units": initial_cost,
                "reduction_vs_baseline_percent": {
                    name: reduction_percent(initial_cost[name], baseline_cost[name]) for name in ABLATION_COST_PROFILES
                },
            },
            "planned_expected": {
                "cases": expected_cases,
                "model_cost_units": expected_cost,
                "reduction_vs_baseline_percent": {
                    name: reduction_percent(expected_cost[name], baseline_cost[name]) for name in ABLATION_COST_PROFILES
                },
            },
            "planned_max": {
                "cases": max_cases,
                "model_cost_units": max_cost,
                "reduction_vs_baseline_percent": {
                    name: reduction_percent(max_cost[name], baseline_cost[name]) for name in ABLATION_COST_PROFILES
                },
            },
        },
        "accuracy_tradeoff": accuracy_impact([entry[1] for entry in candidate_entries], deferred_items),
        "candidates": candidates,
        "deferred": deferred,
    }
