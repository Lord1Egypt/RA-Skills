from __future__ import annotations

from .common import *
from .scoring import *

RISK_REVIEW_GUIDANCE = {
    "base64-payload": "Decoded payloads can hide behavior; review the decoded content before trusting the skill.",
    "curl-pipe-shell": "Downloaded code is executed immediately; verify the source and prefer pinned local scripts.",
    "dynamic-exec": "Dynamic execution makes behavior harder to audit; check whether it is required.",
    "external-post": "The skill may send data out; confirm the destination and data type.",
    "install-hook": "Install-time hooks can run before the user invokes the skill; inspect the hook body.",
    "network-download": "The skill downloads remote content; confirm it is pinned and trusted.",
    "packaging-exec-surface": "Packaging files can execute local build code; inspect before installing.",
    "protected-path-access": "The skill references private local paths; review whether that access is necessary.",
    "private-content-artifact": "The bundle appears to contain credential-like content; remove or rotate it before trusting the skill.",
    "script-exec-call": "The script invokes a child process; inspect the called command and arguments.",
}

RISK_REVIEW_GUIDANCE_ZH_CN = {
    "base64-payload": "存在可解码载荷，使用前先看解码后的真实内容。",
    "curl-pipe-shell": "下载内容会被直接执行，先确认来源可信且最好固定到本地脚本。",
    "dynamic-exec": "动态执行会降低可审计性，确认它是否真的必要。",
    "external-post": "技能可能向外部发送数据，确认目的地和发送的数据类型。",
    "install-hook": "安装阶段钩子可能在用户调用前执行，先检查钩子内容。",
    "network-download": "技能会下载远程内容，确认来源可信且版本固定。",
    "packaging-exec-surface": "打包配置可能触发本地构建代码，安装前先检查。",
    "protected-path-access": "技能引用了受保护的本地路径，确认这种访问是否必要。",
    "private-content-artifact": "包内疑似包含凭证类内容，信任前应删除或轮换。",
    "script-exec-call": "脚本会调用子进程，检查具体命令和参数。",
}

ACTION_ADVICE = {
    "delete": "Remove it after a quick human check; the evidence says it is not earning its place.",
    "merge-delete": "Merge any useful parts into the stronger overlapping skill, then remove this one after review.",
    "merge-or-review": "Compare it with the overlapping skill before deciding whether to merge or keep it.",
    "observe-30d": "Keep it for now and collect better usage evidence before making a removal decision.",
    "quarantine-review": "Do not trust it yet; inspect the risky files before using or keeping it.",
    "review-risk": "Review the risky behavior before deciding whether it should stay installed.",
    "review-system": "Review this system skill carefully because it carries higher-risk signals.",
    "keep-review-risk": "It looks useful, but keep it only after checking the risk signals.",
    "keep-review-burden": "It looks useful, but simplify it because it is expensive to load or maintain.",
    "review-burden": "Review and simplify it before treating it as worth keeping.",
    "review-vs-community": "Check community evidence and run a benchmark before replacing or removing it.",
    "review": "Review it with better evidence before making a keep or delete decision.",
    "keep-narrow": "Keep it, but narrow the trigger or scope if it overlaps with another skill.",
    "keep": "Keep it; the evidence is strong enough.",
    "keep-system": "Keep it as a system skill.",
}

ACTION_ADVICE_ZH_CN = {
    "delete": "人工快速确认后移除；现有证据显示它没有赚回维护成本。",
    "merge-delete": "先把有用部分合并到更强的重叠技能，再人工确认后移除这个技能。",
    "merge-or-review": "先和重叠技能对比，再决定合并还是保留。",
    "observe-30d": "暂时保留，先收集更好的使用证据，不要现在删除。",
    "quarantine-review": "暂时不要信任；先检查高风险文件再决定是否使用或保留。",
    "review-risk": "先复核风险行为，再决定是否继续安装。",
    "review-system": "这是系统技能且有较高风险信号，需要谨慎复核。",
    "keep-review-risk": "看起来有用，但保留前需要检查风险信号。",
    "keep-review-burden": "看起来有用，但上下文或维护负担偏高，应该简化。",
    "review-burden": "先复核并简化，再判断是否值得保留。",
    "review-vs-community": "先检查社区证据并跑基准，再考虑替换或移除。",
    "review": "补充更好的证据后再决定保留还是删除。",
    "keep-narrow": "建议保留，但如果和其他技能重叠，应收窄触发或范围。",
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
        "recommended_actions": "Recommended actions",
        "delete_candidates": "Delete candidates",
        "decision_summary": "Decision Summary",
        "decision_intro": "Start with the decisions. Use the tables below for human verification and agent follow-up.",
        "useful_count": "Useful enough to keep",
        "observe_count": "Watch for more evidence",
        "review_count": "Needs human review before trusting",
        "removal_count": "Merge or remove candidates",
        "install_gate_count": "New-install gates",
        "useful_group": "Useful enough to keep",
        "observe_group": "Watch for more evidence",
        "review_group": "Needs human review before trusting",
        "removal_group": "Merge or remove candidates",
        "install_gate_group": "New-install gates",
        "none": "None.",
        "more": "+{count} more in the evidence tables.",
        "score_word": "score",
        "call": "call",
        "calls": "calls",
        "recent_call": "recent call",
        "recent_calls": "recent calls",
        "no_usage": "no matched usage data",
        "missing_ablation": "missing ablation",
        "risk": "risk",
        "quality": "quality",
        "missing_env": "missing env",
        "install_gate": "install gate",
        "score_table": "Score Table",
        "cost_ablation_plan": "Cost-Efficient Ablation Plan",
        "strategy": "Strategy",
        "eligible_general_skills": "Eligible general skills",
        "candidate_skills": "Candidate skills",
        "deferred_general_skills": "Deferred general skills",
        "expected_model_cost_reduction": "Expected model-cost reduction vs {baseline_policy}-case full protocol",
        "expected_accuracy_impact": "Expected accuracy impact",
        "community_signal_breakdown": "Community Signal Breakdown",
        "quality_burden": "Quality Burden",
        "risk_review": "Risk Review",
        "recommended_actions_heading": "Recommended Actions",
        "delete_candidates_heading": "Delete Candidates",
        "missing_evidence": "Missing Evidence",
    },
    "zh-CN": {
        "title": "技能有用性审计",
        "skills_audited": "已审计技能",
        "usage_files": "使用数据文件",
        "history_files": "历史记录文件",
        "ablation_files": "消融数据文件",
        "community_files": "社区数据文件",
        "report_mode": "报告模式",
        "recommended_actions": "需处理建议数",
        "delete_candidates": "删除候选数",
        "decision_summary": "决策摘要",
        "decision_intro": "先看结论；后面的表格用于人工复核和 agent 二次分析。",
        "useful_count": "建议保留",
        "observe_count": "继续观察并补证据",
        "review_count": "需要人工复核后再信任",
        "removal_count": "合并或移除候选",
        "install_gate_count": "新安装门禁",
        "useful_group": "建议保留",
        "observe_group": "继续观察并补证据",
        "review_group": "需要人工复核后再信任",
        "removal_group": "合并或移除候选",
        "install_gate_group": "新安装门禁",
        "none": "无。",
        "more": "其余 {count} 个见后面的证据表。",
        "score_word": "分数",
        "call": "次调用",
        "calls": "次调用",
        "recent_call": "次调用",
        "recent_calls": "次调用",
        "no_usage": "没有匹配的使用数据",
        "missing_ablation": "缺少消融证据",
        "risk": "风险",
        "quality": "质量信号",
        "missing_env": "缺少环境变量",
        "install_gate": "安装门禁",
        "score_table": "评分表",
        "cost_ablation_plan": "低成本消融计划",
        "strategy": "策略",
        "eligible_general_skills": "符合条件的通用技能",
        "candidate_skills": "候选技能",
        "deferred_general_skills": "暂缓的通用技能",
        "expected_model_cost_reduction": "相对 {baseline_policy} 例完整协议的预计模型成本降低",
        "expected_accuracy_impact": "预计准确性影响",
        "community_signal_breakdown": "社区信号拆解",
        "quality_burden": "质量负担",
        "risk_review": "风险复核",
        "recommended_actions_heading": "处理建议",
        "delete_candidates_heading": "删除候选",
        "missing_evidence": "缺失证据",
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
            "Recent30",
            "Usage",
            "Unique",
            "Impact",
            "Comm",
            "Conf",
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
        "en": ["Skill", "Burden", "Uncapped", "Flags", "Evidence"],
        "zh-CN": ["技能", "负担", "未封顶", "标记", "证据"],
    },
    "risk": {
        "en": ["Skill", "Risk", "Flags", "Install Gate", "Review"],
        "zh-CN": ["技能", "风险", "标记", "安装门禁", "复核意见"],
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
        "en": ["Skill", "Kind", "Missing"],
        "zh-CN": ["技能", "类型", "缺失证据"],
    },
}

MISSING_EVIDENCE_LABELS = {
    "en": {"usage": "usage", "ablation": "ablation", "community": "community"},
    "zh-CN": {"usage": "使用数据", "ablation": "消融数据", "community": "社区数据"},
}


def normalize_report_language(value: object) -> str:
    raw = str(value or "auto").strip()
    if not raw:
        return "en"
    normalized = raw.lower().replace("_", "-")
    if normalized in {"zh", "zh-cn", "zh-hans", "cn", "chinese", "中文", "简体中文"}:
        return "zh-CN"
    if normalized in {"en", "en-us", "en-gb", "english"}:
        return "en"
    return "en"


def report_text(language: str, key: str) -> str:
    normalized = normalize_report_language(language)
    return REPORT_TEXT.get(normalized, REPORT_TEXT["en"]).get(key, REPORT_TEXT["en"][key])


def report_headers(language: str, table: str) -> list[str]:
    normalized = normalize_report_language(language)
    return REPORT_TABLE_HEADERS[table].get(normalized, REPORT_TABLE_HEADERS[table]["en"])


def missing_evidence_label(value: str, language: str) -> str:
    normalized = normalize_report_language(language)
    return MISSING_EVIDENCE_LABELS.get(normalized, MISSING_EVIDENCE_LABELS["en"]).get(value, value)


def action_advice(action: str, reason: str) -> str:
    if action in ACTION_ADVICE:
        return ACTION_ADVICE[action]
    normalized_reason = reason.strip().rstrip(".")
    if normalized_reason:
        return f"Review it before changing anything: {normalized_reason}."
    return "Review it before changing anything."


def action_advice_for_report(action: str, reason: str, language: str = "en") -> str:
    if normalize_report_language(language) != "zh-CN":
        return action_advice(action, reason)
    if action in ACTION_ADVICE_ZH_CN:
        return ACTION_ADVICE_ZH_CN[action]
    normalized_reason = reason.strip().rstrip(".")
    if normalized_reason:
        return f"修改前先人工复核：{normalized_reason}。"
    return "修改前先人工复核。"


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
    final_score = coerce_float(item.get("final_score"))
    if final_score is not None:
        parts.append(f"{report_text(normalized_language, 'score_word')} {final_score:.1f}")

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

    if item.get("missing_ablation"):
        parts.append(report_text(normalized_language, "missing_ablation"))

    risk_level = str(item.get("risk_level") or "none")
    risk_flags = list(item.get("risk_flags") or [])
    if risk_level != "none":
        flags = short_risk_flags([str(flag) for flag in risk_flags])
        if normalized_language == "zh-CN":
            risk_label = {"high": "高", "medium": "中", "low": "低"}.get(risk_level, risk_level)
            parts.append(f"{risk_label}{report_text(normalized_language, 'risk')}" + (f": {flags}" if flags else ""))
        else:
            parts.append(f"{risk_level} {report_text(normalized_language, 'risk')}" + (f": {flags}" if flags else ""))

    quality_flags = [str(flag) for flag in list(item.get("quality_flags") or [])]
    if quality_flags:
        parts.append(f"{report_text(normalized_language, 'quality')}: {short_risk_flags(quality_flags)}")

    missing_env = [str(name) for name in list(item.get("missing_required_env") or [])]
    if missing_env:
        suffix = f"+{len(missing_env) - 2} more" if len(missing_env) > 2 else ""
        env_summary = ",".join(missing_env[:2])
        parts.append(f"{report_text(normalized_language, 'missing_env')}: {env_summary}" + (f",{suffix}" if suffix else ""))

    install_gate = _item_install_gate_verdict(item)
    if install_gate in SUMMARY_INSTALL_GATE_VERDICTS:
        parts.append(f"{report_text(normalized_language, 'install_gate')}: {install_gate}")

    action = _item_action(item)
    if not parts:
        parts.append(action_advice_for_report(action, str(item.get("action_reason") or ""), normalized_language))
    return "; ".join(dict.fromkeys(part for part in parts if part))


def _summary_group(title_key: str, items: list[dict[str, object]], limit: int, language: str) -> list[str]:
    normalized_language = normalize_report_language(language)
    lines = [f"### {report_text(normalized_language, title_key)}", ""]
    if not items:
        lines.append(f"- {report_text(normalized_language, 'none')}")
        return lines
    sentence_end = "。" if normalized_language == "zh-CN" else "."
    for item in items[:limit]:
        lines.append(f"- {_item_display_name(item)}: `{_item_action(item)}`. {_summary_reason(item, normalized_language)}{sentence_end}")
    if len(items) > limit:
        lines.append(f"- {report_text(normalized_language, 'more').format(count=len(items) - limit)}")
    return lines


def decision_summary(ranked: list[dict[str, object]], limit: int = 8, language: str = "en") -> list[str]:
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
        f"- {report_text(normalized_language, 'useful_count')}: {len(useful)}",
        f"- {report_text(normalized_language, 'observe_count')}: {len(observe)}",
        f"- {report_text(normalized_language, 'review_count')}: {len(review)}",
        f"- {report_text(normalized_language, 'removal_count')}: {len(removal)}",
        f"- {report_text(normalized_language, 'install_gate_count')}: {len(install_gate)}",
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


def risk_review_summary(level: str, evidence: list[dict[str, object]]) -> str:
    if not evidence:
        return ""
    labels = [str(item.get("label", "")) for item in evidence if item.get("label")]
    guidance = [RISK_REVIEW_GUIDANCE.get(label, "Review this signal before trusting the skill.") for label in labels[:3]]
    prefix = {
        "high": "High risk: review before use.",
        "medium": "Medium risk: inspect before trusting.",
        "low": "Low risk: check if expected.",
    }.get(level, "Review recommended.")
    return f"{prefix} " + " ".join(dict.fromkeys(guidance))


def risk_review_summary_for_report(level: str, evidence: list[dict[str, object]], language: str = "en") -> str:
    if normalize_report_language(language) != "zh-CN":
        return risk_review_summary(level, evidence)
    if not evidence:
        return ""
    labels = [str(item.get("label", "")) for item in evidence if item.get("label")]
    guidance = [
        RISK_REVIEW_GUIDANCE_ZH_CN.get(label, "信任这个技能前先复核该风险信号。")
        for label in labels[:3]
    ]
    prefix = {
        "high": "高风险：使用前先复核。",
        "medium": "中风险：信任前先检查。",
        "low": "低风险：确认是否符合预期。",
    }.get(level, "建议复核。")
    return f"{prefix} " + " ".join(dict.fromkeys(guidance))


def install_gate_summary(level: str, evidence: list[dict[str, object]]) -> dict[str, str]:
    flags = [str(item.get("label", "")) for item in evidence if item.get("label")]
    if level == "high":
        return {
            "verdict": "block-before-install",
            "reason": "High-risk static signals should block a new install until human review clears them.",
        }
    if level == "medium":
        return {
            "verdict": "review-before-install",
            "reason": "Medium-risk static signals need human review before a new install is trusted.",
        }
    if level == "low":
        return {
            "verdict": "warn-before-install",
            "reason": "Low-risk static signals should be checked before a new install is trusted.",
        }
    if flags:
        return {
            "verdict": "review-before-install",
            "reason": "Static signals were present but unclassified; review before a new install is trusted.",
        }
    return {
        "verdict": "no-static-risk-gate",
        "reason": "No static risk gate was triggered; still review the source before installing.",
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


def summarize_quality_evidence(evidence: list[dict[str, object]], limit: int = 3) -> str:
    if not evidence:
        return "-"
    parts = []
    for item in evidence[:limit]:
        label = str(item.get("label", "quality"))
        reason = str(item.get("reason", "")).strip()
        penalty = fmt_optional_float(item.get("penalty"))
        parts.append(f"{label}({penalty}): {reason}" if reason else f"{label}({penalty})")
    if len(evidence) > limit:
        parts.append(f"+{len(evidence) - limit} more")
    return "; ".join(parts)


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
        float(item["final_score"]) < 6.0
        or float(item["overlap_value"]) >= 0.65
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
        if consistency >= 0.85 and better <= 0.10:
            score += 1.0
            reasons.append("prior no-impact ablation")
    if item["missing_ablation"]:
        score += 2
        reasons.append("missing ablation")
    if float(item["final_score"]) < 6.0:
        score += 2
        reasons.append("weak final score")
    if float(item["overlap_value"]) >= 0.65:
        score += 2
        reasons.append("high overlap")
    if float(item["quality_penalty"]) >= 0.6:
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
    if float(item["confidence_score"]) < 0.55:
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
        and (float(item["final_score"]) < 6.0 or float(item["overlap_value"]) >= 0.65 or float(item["quality_penalty"]) >= 0.6)
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
