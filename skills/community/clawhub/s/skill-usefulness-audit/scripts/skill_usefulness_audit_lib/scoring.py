from __future__ import annotations

from .common import *

from .risk_quality import quality_issue

DOCUMENTATION_ONLY_TERMS = {
    "concept",
    "concepts",
    "doc",
    "docs",
    "documentation",
    "explain",
    "explainer",
    "guide",
    "guides",
    "note",
    "notes",
    "tip",
    "tips",
    "tutorial",
    "tutorials",
}

OPERATIONAL_CAPABILITY_TERMS = {
    "automate",
    "call",
    "connect",
    "control",
    "convert",
    "create",
    "deploy",
    "download",
    "fetch",
    "install",
    "manage",
    "query",
    "read",
    "run",
    "search",
    "send",
    "update",
    "upload",
    "use",
    "write",
}
DOCUMENTATION_OBJECT_TERMS = {
    "concept",
    "concepts",
    "doc",
    "docs",
    "documentation",
    "explainer",
    "guide",
    "guides",
    "note",
    "notes",
    "tip",
    "tips",
    "tutorial",
    "tutorials",
}
OPERATIONAL_TERM_PATTERN = "|".join(sorted(OPERATIONAL_CAPABILITY_TERMS))
OPERATIONAL_LEAD_PATTERN = re.compile(
    rf"^\s*(?:please\s+)?(?P<operation>{OPERATIONAL_TERM_PATTERN})\b",
    re.IGNORECASE,
)
CJK_API_CAPABILITY_PATTERNS = (
    re.compile(r"(?:调用|连接|查询|搜索|发送|管理|读取|更新).{0,12}(?:api|接口|邮箱|邮件|日历|数据库|github)", re.I),
    re.compile(r"(?:api|接口|邮箱|邮件|日历|数据库|github).{0,12}(?:调用|连接|查询|搜索|发送|管理|读取|更新)", re.I),
)
CJK_TOOL_CAPABILITY_PATTERNS = (
    re.compile(r"(?:控制|操作|自动化|打开|访问|浏览|填写|抓取|截图).{0,12}(?:浏览器|网页)", re.I),
    re.compile(r"(?:浏览器|网页).{0,12}(?:控制|操作|自动化|打开|访问|浏览|填写|抓取|截图)", re.I),
    re.compile(r"(?:读取|编辑|修改|创建|分析|处理|生成|转换).{0,12}(?:表格|工作簿|电子表格|文档|幻灯片|演示文稿|图片|图像)", re.I),
    re.compile(r"(?:表格|工作簿|电子表格|文档|幻灯片|演示文稿|图片|图像).{0,12}(?:读取|编辑|修改|创建|分析|处理|生成|转换)", re.I),
)
CJK_DOCUMENTATION_TERMS = re.compile(r"教程|指南|说明|介绍|示例|笔记|概念")
CJK_CLAUSE_BOUNDARY = re.compile(r"[,，;；.!?。！？]")
OBJECT_PHRASE_BOUNDARY_PATTERN = re.compile(
    r"\b(?:about|and|following|for|or|then|to|using|via|with)\b|[;,.!?]",
    re.IGNORECASE,
)
DOCUMENTATION_ACTION_BOUNDARY_PATTERN = re.compile(
    r"\b(?:about|and|following|or|then|to|using|via|with)\b|[;,.!?]",
    re.IGNORECASE,
)
DOCUMENTATION_ACTION_TERMS = {"create", "read", "update", "write"}


def has_local_tool_surface(skill: dict[str, object]) -> bool:
    return (coerce_int(skill.get("scripts_count")) or 0) > 0


def operational_lead_targets_capability(description: str, capability_terms: set[str]) -> bool:
    lead = OPERATIONAL_LEAD_PATTERN.search(description)
    if not lead:
        return False
    operation = lead.group("operation").lower()
    remainder = description[lead.end() :]
    object_phrase = OBJECT_PHRASE_BOUNDARY_PATTERN.split(remainder, maxsplit=1)[0]
    object_terms = extract_terms(object_phrase)
    if object_terms & DOCUMENTATION_OBJECT_TERMS:
        return False
    if object_terms & capability_terms or operation in capability_terms:
        return True
    if operation not in DOCUMENTATION_ACTION_TERMS:
        return False
    extended_phrase = DOCUMENTATION_ACTION_BOUNDARY_PATTERN.split(remainder, maxsplit=1)[0]
    extended_terms = extract_terms(extended_phrase)
    if extended_terms & DOCUMENTATION_OBJECT_TERMS:
        return False
    return bool(extended_terms & capability_terms)


def looks_documentation_only(skill: dict[str, object], terms: set[str]) -> bool:
    if not terms & DOCUMENTATION_ONLY_TERMS or has_local_tool_surface(skill):
        return False
    capability_terms = API_STRONG_KEYWORDS | API_SUPPORT_KEYWORDS | TOOL_KEYWORDS
    description = str(skill.get("description", "") or "")
    if description and operational_lead_targets_capability(description, capability_terms):
        return False
    return True


def looks_cjk_documentation_only(skill: dict[str, object]) -> bool:
    if has_local_tool_surface(skill):
        return False
    description = str(skill.get("description", "") or "")
    match = CJK_DOCUMENTATION_TERMS.search(description)
    if not match:
        return False
    return CJK_CLAUSE_BOUNDARY.search(description[: match.start()]) is None


def classify_skill(skill: dict[str, object]) -> str:
    terms = set(skill["terms"])
    description = str(skill.get("description", "") or "")
    if looks_documentation_only(skill, terms) or looks_cjk_documentation_only(skill):
        return "general"
    if any(pattern.search(description) for pattern in CJK_API_CAPABILITY_PATTERNS):
        return "api"
    if any(pattern.search(description) for pattern in CJK_TOOL_CAPABILITY_PATTERNS):
        return "tool"
    if terms & API_STRONG_KEYWORDS:
        return "api"
    if len(terms & API_SUPPORT_KEYWORDS) >= 2:
        return "api"
    if terms & TOOL_KEYWORDS:
        return "tool"
    return "general"


def usage_evidence_weight(source: str) -> float:
    if source == "usage":
        return 1.0
    if source == "history":
        return HISTORY_EVIDENCE_WEIGHT
    return 0.0


def usage_score(usage_record: dict[str, object], evidence_weight: float) -> float:
    if evidence_weight <= 0:
        return 0.0

    calls = int(usage_record.get("calls", 0) or 0)
    evidence_count = calls
    if calls <= 0 and "suspected_invocations" in usage_record:
        evidence_count = int(usage_record.get("suspected_invocations", 0) or 0)
    recent_30d_calls = coerce_int(usage_record.get("recent_30d_calls"))
    recent_90d_calls = coerce_int(usage_record.get("recent_90d_calls"))
    active_days = coerce_int(usage_record.get("active_days"))
    last_used_days = days_since(usage_record.get("last_used_at"))

    if recent_30d_calls is not None:
        if recent_30d_calls >= 8:
            base = 3.0
        elif recent_30d_calls >= 3:
            base = 2.0
        elif recent_30d_calls >= 1:
            base = 1.0
        else:
            base = 0.0
    elif recent_90d_calls is not None:
        if recent_90d_calls >= 10:
            base = 2.5
        elif recent_90d_calls >= 3:
            base = 1.5
        elif recent_90d_calls >= 1:
            base = 0.75
        else:
            base = 0.0
    elif evidence_count <= 0:
        base = 0.0
    elif evidence_count <= 2:
        base = 1.0
    elif evidence_count <= 9:
        base = 2.0
    else:
        base = 3.0

    if last_used_days is not None:
        if last_used_days <= 7:
            base += 0.5
        elif last_used_days <= 30:
            base += 0.25
        elif last_used_days > 180:
            base -= 0.5

    if active_days is not None:
        if active_days >= 10:
            base += 0.25
        elif active_days >= 3:
            base += 0.10

    return round(clamp(base * evidence_weight, 0.0, 3.0), 2)


def uniqueness_score(overlap: float) -> float:
    if overlap >= NEAR_DUPLICATE_OVERLAP_THRESHOLD:
        return 0.0
    if overlap >= HIGH_OVERLAP_THRESHOLD:
        return 1.0
    if overlap >= 0.40:
        return 2.0
    return 3.0


def impact_score(
    kind: str,
    calls: int,
    overlap: float,
    skill: dict[str, object],
    ablation: dict[str, float] | None,
) -> float:
    if kind in {"api", "tool"}:
        score = 2.0
        if int(skill["scripts_count"]) > 0 or int(skill["references_count"]) > 0:
            score += 1.0
        if overlap < 0.35:
            score += 0.5
        if calls >= 3:
            score += 0.5
        if overlap >= DUPLICATE_OVERLAP_THRESHOLD:
            score -= 1.0
        if calls == 0:
            score -= 0.5
        return clamp(round(score, 2), 0.0, 4.0)

    if not ablation or ablation.get("cases", 0) <= 0:
        return 1.0 if calls <= 0 else 2.0

    consistency = ablation["consistency_rate"]
    better = ablation["better_rate"]
    worse = ablation["worse_rate"]
    if consistency >= 0.85:
        score = 0.0
    elif consistency >= 0.70:
        score = 1.0
    elif consistency >= 0.55:
        score = 2.0
    elif consistency >= 0.35:
        score = 3.0
    else:
        score = 4.0

    if better - worse >= 0.30:
        score += 1.0
    elif worse > better:
        score -= 1.0
    return clamp(round(score, 2), 0.0, 4.0)


def runtime_quality_evidence(
    usage_record: dict[str, object],
    ablation: dict[str, float] | None,
) -> list[dict[str, object]]:
    evidence: list[dict[str, object]] = []
    calls = int(usage_record.get("calls", 0) or 0)
    executions = coerce_int(usage_record.get("executions"))
    script_failures = coerce_int(usage_record.get("script_failures"))
    repair_turns = coerce_int(usage_record.get("repair_turns"))
    reference_loads = coerce_int(usage_record.get("reference_loads"))
    false_triggers = coerce_int(usage_record.get("false_triggers"))

    if calls >= 8 and executions is not None:
        execution_rate = executions / max(calls, 1)
        if execution_rate < 0.25:
            evidence.append(
                quality_issue(
                    "overtrigger-low-execution",
                    0.45,
                    "many activations did not lead to real execution",
                    metrics={"calls": calls, "executions": executions, "execution_rate": round(execution_rate, 2)},
                )
            )

    if calls >= 5 and false_triggers:
        false_rate = false_triggers / max(calls, 1)
        if false_triggers >= 3 or false_rate >= 0.25:
            evidence.append(
                quality_issue(
                    "overtrigger-misfire",
                    0.35,
                    "usage evidence shows frequent accidental activations",
                    metrics={"calls": calls, "false_triggers": false_triggers, "false_rate": round(false_rate, 2)},
                )
            )

    if calls >= 5 and ablation and ablation.get("cases", 0) > 0:
        consistency = float(ablation.get("consistency_rate", 0.0))
        better = float(ablation.get("better_rate", 0.0))
        if consistency >= NO_IMPACT_CONSISTENCY_THRESHOLD and better <= NO_IMPACT_BETTER_THRESHOLD:
            evidence.append(
                quality_issue(
                    "overtrigger-no-impact",
                    0.40,
                    "frequent activation shows little measured gain in ablation",
                    metrics={"calls": calls, "consistency_rate": round(consistency, 2), "better_rate": round(better, 2)},
                )
            )

    if calls > 0 and reference_loads is not None:
        loads_per_call = reference_loads / max(calls, 1)
        if reference_loads >= 10 and loads_per_call >= 3.0:
            evidence.append(
                quality_issue(
                    "reference-overload",
                    0.30,
                    "usage evidence shows heavy reference loading",
                    metrics={
                        "calls": calls,
                        "reference_loads": reference_loads,
                        "reference_loads_per_call": round(loads_per_call, 2),
                    },
                )
            )

    if script_failures:
        if executions is not None:
            denominator = max(executions, script_failures, 1)
            denominator_source = "executions"
        elif calls:
            denominator = max(calls, 1)
            denominator_source = "calls"
        else:
            denominator = max(script_failures, 1)
            denominator_source = "script_failures"
        failure_rate = script_failures / denominator
        if script_failures >= 3 or failure_rate >= 0.30:
            evidence.append(
                quality_issue(
                    "script-failure-burden",
                    0.45,
                    "usage evidence shows script failures",
                    metrics={
                        "script_failures": script_failures,
                        "executions": executions,
                        "denominator_source": denominator_source,
                        "failure_rate": round(failure_rate, 2),
                    },
                )
            )
        else:
            evidence.append(
                quality_issue(
                    "script-failure-burden",
                    0.20,
                    "usage evidence shows occasional script failure",
                    metrics={
                        "script_failures": script_failures,
                        "executions": executions,
                        "denominator_source": denominator_source,
                    },
                )
            )

    if repair_turns and repair_turns >= 3:
        evidence.append(
            quality_issue(
                "agent-repair-burden",
                0.30,
                "usage evidence shows repeated repair turns",
                metrics={"repair_turns": repair_turns},
            )
        )

    return evidence


def readiness_quality_evidence(skill: dict[str, object]) -> list[dict[str, object]]:
    missing_env = [str(item) for item in skill.get("missing_required_env", []) if item]
    if not missing_env:
        return []
    return [
        quality_issue(
            "missing-required-env",
            0.90,
            "required environment variables are not configured",
            metrics={"missing_env": missing_env, "missing_env_count": len(missing_env)},
        )
    ]


def quality_penalty(
    skill: dict[str, object],
    usage_record: dict[str, object],
    ablation: dict[str, float] | None,
    additional_evidence: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    evidence = list(skill.get("static_quality_evidence", []))
    evidence.extend(readiness_quality_evidence(skill))
    evidence.extend(runtime_quality_evidence(usage_record, ablation))
    if additional_evidence:
        evidence.extend(additional_evidence)
    penalty_uncapped = round(sum(float(item["penalty"]) for item in evidence), 2)
    penalty = round(clamp(penalty_uncapped, 0.0, 2.5), 2)
    return {
        "penalty": penalty,
        "penalty_uncapped": penalty_uncapped,
        "flags": [str(item["label"]) for item in evidence],
        "evidence": evidence,
    }


def catalog_quality_evidence(overlap_peer: str | None, overlap_value: float) -> list[dict[str, object]]:
    if not overlap_peer or overlap_value < NEAR_DUPLICATE_OVERLAP_THRESHOLD:
        return []
    return [
        quality_issue(
            "near-duplicate-instructions",
            0.10,
            "instructions closely match another installed skill",
            metrics={"peer": overlap_peer, "overlap": round(overlap_value, 2)},
        )
    ]


def health_cap_from_quality(evidence: list[dict[str, object]]) -> float | None:
    labels = {str(item.get("label", "")) for item in evidence}
    if "script-syntax-error" in labels:
        return 4.0
    if "empty-skill-contract" in labels or "script-import-error" in labels:
        return 5.5
    for item in evidence:
        if item.get("label") != "script-failure-burden":
            continue
        if float(item.get("penalty", 0.0) or 0.0) >= 0.45:
            return 4.0
    return None


def confidence_score(
    usage_source: str,
    usage_record: dict[str, object],
    kind: str,
    ablation: dict[str, float] | None,
    community_entry: dict[str, object] | None,
    skill_count: int,
) -> float:
    score = 0.0
    if usage_source == "usage":
        score += 0.35
    elif usage_source == "history":
        score += 0.15

    if usage_record.get("recent_30d_calls") is not None or usage_record.get("last_used_at") is not None:
        score += 0.20
    elif int(usage_record.get("calls", 0) or 0) > 0 and usage_source == "usage":
        score += 0.10

    if kind == "general":
        cases = int((ablation or {}).get("cases", 0))
        if cases >= 5:
            score += 0.25
        elif cases >= 1:
            score += 0.15
    else:
        score += 0.25

    score += 0.10 if skill_count > 1 else 0.05
    if community_entry:
        score += 0.10
    return round(clamp(score, 0.0, 1.0), 2)


def verdict(total: float, confidence: float | None = None) -> str:
    if confidence is not None and confidence < LOW_CONFIDENCE_THRESHOLD and total < SCORE_REVIEW_THRESHOLD:
        return "insufficient-evidence"
    if total >= SCORE_KEEP_THRESHOLD:
        return "keep"
    if total >= SCORE_KEEP_NARROW_THRESHOLD:
        return "keep-narrow"
    if total >= SCORE_REVIEW_THRESHOLD:
        return "review"
    if total >= SCORE_MERGE_DELETE_THRESHOLD:
        return "merge-delete"
    return "delete"


def recommend_action(
    source: str,
    kind: str,
    total: float,
    confidence: float,
    risk_level: str,
    quality_penalty_value: float,
    calls: int,
    overlap: float,
    community_prior: float | None,
) -> tuple[str, str, bool]:
    if source == "system":
        if risk_level == "high":
            return "review-system", "system skill with high-risk patterns", False
        return "keep-system", "system skill", False

    if risk_level == "high":
        return "quarantine-review", "high-risk patterns need a closer check", False
    if risk_level == "medium" and total >= SCORE_KEEP_NARROW_THRESHOLD:
        return "keep-review-risk", "useful locally with medium-risk patterns", False
    if quality_penalty_value >= QUALITY_BURDEN_REVIEW_THRESHOLD and total >= SCORE_KEEP_NARROW_THRESHOLD:
        return "keep-review-burden", "useful locally but expensive to maintain or load", False
    if quality_penalty_value >= QUALITY_BURDEN_REVIEW_THRESHOLD and total >= SCORE_REVIEW_THRESHOLD:
        return "review-burden", "maintenance cost lowers the final score", False

    if total >= SCORE_KEEP_THRESHOLD:
        return "keep", "high final score", False
    if total >= SCORE_KEEP_NARROW_THRESHOLD:
        if overlap >= HIGH_OVERLAP_THRESHOLD and calls <= 1:
            return "keep-narrow", "high overlap suggests narrower scope", False
        return "keep-narrow", "good final score", False

    if risk_level == "medium":
        return "review-risk", "medium-risk patterns require review", False

    if confidence < LOW_CONFIDENCE_THRESHOLD:
        return "observe-30d", "evidence confidence is low", False

    if total >= SCORE_REVIEW_THRESHOLD:
        if overlap >= HIGH_OVERLAP_THRESHOLD:
            return "merge-or-review", "mid score with high overlap", False
        if community_prior is not None and community_prior >= STRONG_COMMUNITY_PRIOR_THRESHOLD:
            return "review-vs-community", "community signal is stronger than final score", False
        return "review", "mid final score", False

    if kind in {"api", "tool"}:
        if calls == 0 and overlap >= DUPLICATE_OVERLAP_THRESHOLD:
            return "merge-delete", "unused duplicate protected skill", True
        if community_prior is not None and community_prior >= STRONG_COMMUNITY_PRIOR_THRESHOLD:
            return "review-vs-community", "protected skill has strong community signal", False
        return "merge-or-review", "protected skill scores low after burden", False

    if community_prior is not None and community_prior >= STRONG_COMMUNITY_PRIOR_THRESHOLD:
        return "review-vs-community", "community signal suggests benchmark before removal", False
    if total < SCORE_MERGE_DELETE_THRESHOLD:
        return "delete", "very low final score", True
    if overlap >= HIGH_OVERLAP_THRESHOLD and calls <= 1:
        return "merge-delete", "low usage plus high overlap", True
    return "merge-delete", "low final score", True
