#!/usr/bin/env python3
"""Deterministic, local-only single-round interview state machine."""

import copy
import datetime as dt
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
INTERVIEW_SCHEMA_VERSION = "1.0"
DEFAULT_COUNT = 6
MIN_COUNT = 3
MAX_COUNT = 10
MAX_ANSWER_CHARS = 20000
QUESTION_KINDS = ("resume_followup", "knowledge", "scenario")

_PHONE_RE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_METRIC_RE = re.compile(
    r"\d+(?:\.\d+)?\s*(?:%|％|倍|x|X|次|个|条|台|天|小时|分钟|人|万|k|K|域|系统|周|月|年)"
)


class InterviewError(Exception):
    """A controlled interview input or state failure."""

    def __init__(
        self,
        message,
        exit_code=2,
        error_code="YRS-INTERVIEW-001",
    ):
        super().__init__(message)
        self.exit_code = exit_code
        self.error_code = error_code


def _now_iso(value=None):
    if value:
        return str(value)
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00",
        "Z",
    )


def _sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _canonical_hash(payload):
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return _sha256_text(canonical)


def _mask_contact(text):
    text = _PHONE_RE.sub("[电话]", text)
    return _EMAIL_RE.sub("[邮箱]", text)


def _contains_term(term, text):
    term = str(term or "").strip()
    if not term:
        return False
    if term.isascii():
        pattern = r"(?<![A-Za-z0-9]){}(?![A-Za-z0-9])".format(re.escape(term))
        return re.search(pattern, text, re.IGNORECASE) is not None
    return term.casefold() in text.casefold()


def _read_json(path, label):
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise InterviewError("{}不存在：{}".format(label, path), exit_code=3) from error
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise InterviewError("{}无法读取：{}".format(label, error), exit_code=5) from error
    if not isinstance(payload, dict):
        raise InterviewError("{}格式无效：根节点必须是对象。".format(label), exit_code=5)
    return payload


def _data_path(name):
    return SKILL_ROOT / "data" / name


def load_role_map(path=None):
    return _read_json(path or _data_path("security-role-map.json"), "岗位族映射")


def load_question_bank(path=None):
    return _read_json(path or _data_path("question-bank.json"), "题库")


def load_source_registry(path=None):
    return _read_json(path or _data_path("source-registry.json"), "来源注册表")


def _role_terms(role):
    terms = []
    for field in ("aliases", "nice_work_roles"):
        for item in role.get(field, []) or []:
            if isinstance(item, str) and item.strip():
                terms.append(item.strip())
    display = role.get("display_name", "")
    for part in re.split(r"[/|｜]", display):
        part = part.strip()
        if part:
            terms.append(part)
    seen = set()
    result = []
    for item in terms:
        key = item.casefold()
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def detect_role_family(resume_text, jd_text="", role_map=None, explicit=None):
    """Resolve one security role family or fail closed."""
    role_map = role_map or load_role_map()
    roles = [
        item for item in role_map.get("role_families", [])
        if isinstance(item, dict) and item.get("id")
    ]
    role_ids = {item["id"] for item in roles}
    if explicit:
        if explicit not in role_ids:
            raise InterviewError(
                "未知岗位族：{}；可选值：{}".format(
                    explicit,
                    ", ".join(sorted(role_ids)),
                )
            )
        return {
            "role_family": explicit,
            "role_source": "user",
            "score": None,
            "candidates": [],
        }

    scored = []
    for role in roles:
        score = 0
        matched_terms = []
        for term in _role_terms(role):
            hit = False
            if jd_text and _contains_term(term, jd_text):
                score += 3
                hit = True
            if resume_text and _contains_term(term, resume_text):
                score += 2
                hit = True
            if hit:
                matched_terms.append(term)
        if score:
            scored.append({
                "role_family": role["id"],
                "score": score,
                "matched_terms": sorted(set(matched_terms)),
            })

    scored.sort(key=lambda item: (-item["score"], item["role_family"]))
    if not scored:
        raise InterviewError(
            "无法从简历或 JD 唯一识别安全岗位族，请传入 --role-family。"
        )
    if len(scored) > 1 and scored[0]["score"] == scored[1]["score"]:
        names = [item["role_family"] for item in scored if item["score"] == scored[0]["score"]]
        raise InterviewError(
            "岗位族信号并列（{}），请传入 --role-family。".format(
                ", ".join(names)
            )
        )
    return {
        "role_family": scored[0]["role_family"],
        "role_source": "detected",
        "score": scored[0]["score"],
        "candidates": scored[:5],
    }


def _normalise_level(level, role_map):
    levels = [item for item in role_map.get("levels", []) if isinstance(item, str)]
    if level is None:
        return "mid", "default"
    if level not in levels:
        raise InterviewError(
            "未知职级：{}；可选值：{}".format(level, ", ".join(levels))
        )
    return level, "user"


def _validate_count(count):
    if isinstance(count, bool) or not isinstance(count, int):
        raise InterviewError("--count 必须是整数。")
    if count < MIN_COUNT or count > MAX_COUNT:
        raise InterviewError(
            "--count 必须在 {} 到 {} 之间。".format(MIN_COUNT, MAX_COUNT)
        )
    return count


def _target_distribution(count):
    base = count // len(QUESTION_KINDS)
    remainder = count % len(QUESTION_KINDS)
    result = {}
    for index, kind in enumerate(QUESTION_KINDS):
        result[kind] = base + (1 if index < remainder else 0)
    return result


def _parse_date(value, label):
    try:
        return dt.date.fromisoformat(str(value))
    except (TypeError, ValueError) as error:
        raise InterviewError("{}不是有效日期：{}".format(label, value), exit_code=5) from error


def _source_layers(sources):
    return {
        item.get("source_id"): item
        for item in sources.get("sources", [])
        if isinstance(item, dict) and item.get("source_id")
    }


def _question_is_eligible(question, role_family, sources, today):
    if question.get("role_family") != role_family:
        return False
    if question.get("status") != "active":
        return False
    verified = _parse_date(question.get("last_verified_at"), "题目校验日期")
    stale_after = question.get("stale_after_days")
    if not isinstance(stale_after, int) or (today - verified).days > stale_after:
        return False
    refs = question.get("source_refs") or []
    if not refs:
        return False
    for source_id in refs:
        source = sources.get(source_id)
        if not source or source.get("status") != "active":
            return False
        verified = _parse_date(source.get("last_verified_at"), "来源校验日期")
        stale_after = source.get("stale_after_days")
        if not isinstance(stale_after, int) or (today - verified).days > stale_after:
            return False
    return True


def _question_text(question):
    parts = [
        question.get("dimension", ""),
        question.get("prompt", ""),
    ]
    parts.extend(question.get("expected_evidence", []) or [])
    return "\n".join(str(item) for item in parts if item)


def _role_dimension_hits(question, role):
    text = _question_text(question)
    return [
        item for item in role.get("interview_dimensions", []) or []
        if isinstance(item, str) and _contains_term(item, text)
    ]


def _resume_finding_refs(question, audit_report):
    if question.get("kind") != "resume_followup":
        return []
    relevant = {
        "weak_claim",
        "missing_metric",
        "mixed_skill_levels",
        "image_text_gap",
        "missing_summary",
    }
    findings = [
        item for item in audit_report.get("issues", []) or []
        if item.get("code") in relevant
    ]
    findings.sort(key=lambda item: (
        0 if item.get("code") in {"weak_claim", "missing_metric"} else 1,
        item.get("id", ""),
    ))
    return [item.get("id") for item in findings[:3] if item.get("id")]


def _score_candidate(question, role, audit_report, sources, seed_hash, level):
    text = _question_text(question)
    missing = [
        item for item in audit_report.get("jd_match", {}).get("missing", []) or []
        if isinstance(item, str)
    ]
    jd_hits = [item for item in missing if _contains_term(item, text)]
    role_hits = _role_dimension_hits(question, role)
    finding_refs = _resume_finding_refs(question, audit_report)
    score = 0
    score += len(jd_hits) * 12
    score += len(role_hits) * 5
    if finding_refs:
        score += 10
    if question.get("level") == level:
        score += 20
    else:
        score -= 15
    source_layers = [
        sources.get(source_id, {}).get("layer")
        for source_id in question.get("source_refs", []) or []
    ]
    score += 3 if "A" in source_layers else 1 if "B" in source_layers else 0
    rank_hash = _sha256_text(seed_hash + ":" + question.get("question_id", ""))
    return {
        "relevance_points": score,
        "rank_hash": rank_hash,
        "jd_gaps": jd_hits,
        "role_dimensions": role_hits,
        "resume_findings": finding_refs,
        "level_match": question.get("level") == level,
    }


def _session_question(question, basis, index):
    return {
        "session_question_id": "Q{}".format(index),
        "bank_question_id": question["question_id"],
        "role_family": question["role_family"],
        "level": question["level"],
        "dimension": question["dimension"],
        "kind": question["kind"],
        "prompt": question["prompt"],
        "expected_evidence": list(question.get("expected_evidence", [])),
        "followups": list(question.get("followups", [])),
        "answer_boundary": question.get("answer_boundary", ""),
        "source_refs": list(question.get("source_refs", [])),
        "content_hash": question.get("content_hash"),
        "basis": basis,
        "followup_used": 0,
        "followup_prompt": None,
    }


def select_question_plan(
    audit_report,
    role_family,
    level,
    count=DEFAULT_COUNT,
    seed=None,
    today=None,
    bank=None,
    role_map=None,
    source_registry=None,
):
    """Select a deterministic question plan using resume, JD, and bank data."""
    count = _validate_count(count)
    role_map = role_map or load_role_map()
    bank = bank or load_question_bank()
    source_registry = source_registry or load_source_registry()
    today_value = _parse_date(today or dt.date.today().isoformat(), "--today")
    roles = {
        item.get("id"): item
        for item in role_map.get("role_families", [])
        if isinstance(item, dict) and item.get("id")
    }
    role = roles.get(role_family)
    if not role:
        raise InterviewError("未登记岗位族：{}".format(role_family))
    sources = _source_layers(source_registry)
    seed_hash = _sha256_text(str(seed))

    ranked = []
    for question in bank.get("questions", []) or []:
        if not isinstance(question, dict):
            continue
        if not _question_is_eligible(question, role_family, sources, today_value):
            continue
        basis = _score_candidate(
            question,
            role,
            audit_report,
            sources,
            seed_hash,
            level,
        )
        ranked.append((question, basis))

    if not ranked:
        raise InterviewError("题库没有可用于 {} / {} 的 active 题目。".format(
            role_family,
            level,
        ))

    def sort_key(item):
        question, basis = item
        return (
            -basis["relevance_points"],
            basis["rank_hash"],
            question["question_id"],
        )

    ranked.sort(key=sort_key)
    exact_ranked = [item for item in ranked if item[1].get("level_match")]
    expanded_ranked = [item for item in ranked if not item[1].get("level_match")]
    selected = []
    used = set()
    target = _target_distribution(count)
    for kind in QUESTION_KINDS:
        quota = target[kind]
        for item in exact_ranked:
            if quota <= 0:
                break
            question, basis = item
            if question["question_id"] in used or question.get("kind") != kind:
                continue
            selected.append(item)
            used.add(question["question_id"])
            quota -= 1
    for item in exact_ranked:
        if len(selected) >= count:
            break
        question, basis = item
        if question["question_id"] in used:
            continue
        selected.append(item)
        used.add(question["question_id"])
    for item in expanded_ranked:
        if len(selected) >= count:
            break
        question, basis = item
        if question["question_id"] in used:
            continue
        selected.append(item)
        used.add(question["question_id"])

    level_adjusted = any(
        question.get("level") != level for question, _ in selected
    )
    distribution = {
        kind: sum(1 for question, _ in selected if question.get("kind") == kind)
        for kind in QUESTION_KINDS
    }
    questions = [
        _session_question(question, basis, index)
        for index, (question, basis) in enumerate(selected, 1)
    ]
    selection_payload = {
        "bank_version": bank.get("bank_version"),
        "role_family": role_family,
        "level": level,
        "count": count,
        "seed_hash": seed_hash,
        "question_ids": [item["bank_question_id"] for item in questions],
        "distribution": distribution,
    }
    return {
        "seed": seed_hash,
        "count": count,
        "distribution": distribution,
        "target_distribution": target,
        "quota_adjusted": distribution != target,
        "level_adjusted": level_adjusted,
        "selection_hash": _canonical_hash(selection_payload),
        "questions": questions,
    }


def _analysis_summary(audit_report):
    issues = []
    for item in audit_report.get("issues", []) or []:
        if not isinstance(item, dict):
            continue
        issues.append({
            key: item.get(key)
            for key in (
                "id",
                "code",
                "section",
                "heading",
                "original",
                "reason",
                "severity",
                "source_type",
                "needs_confirmation",
            )
        })
    suggestions = []
    for item in audit_report.get("suggestions", []) or []:
        if not isinstance(item, dict):
            continue
        suggestions.append({
            key: item.get(key)
            for key in (
                "code",
                "finding_id",
                "original",
                "suggestion",
                "priority",
            )
        })
    detection = audit_report.get("industry_detection", {}) or {}
    return {
        "stats": copy.deepcopy(audit_report.get("stats", {})),
        "industry_detection": {
            key: detection.get(key)
            for key in (
                "status",
                "primary_industry",
                "display_name",
                "confidence",
                "needs_confirmation",
            )
        },
        "issues": issues,
        "suggestions": suggestions,
        "jd_missing": list(
            audit_report.get("jd_match", {}).get("missing", []) or []
        ),
        "disclaimer": audit_report.get("disclaimer", ""),
    }


def build_session(
    resume_text,
    jd_text,
    audit_report,
    role_family=None,
    level=None,
    count=DEFAULT_COUNT,
    seed=None,
    today=None,
    now=None,
    bank=None,
    role_map=None,
    source_registry=None,
):
    """Create an in-memory interview session; callers decide where to persist it."""
    role_map = role_map or load_role_map()
    bank = bank or load_question_bank()
    source_registry = source_registry or load_source_registry()
    detection = audit_report.get("industry_detection", {}) or {}
    industry = detection.get("primary_industry")
    if role_family:
        role_choice = detect_role_family(
            resume_text,
            jd_text,
            role_map=role_map,
            explicit=role_family,
        )
    elif detection.get("status") == "ambiguous" or detection.get("needs_confirmation"):
        raise InterviewError(
            "行业信号存在歧义，请显式传入 --role-family generic "
            "或对应安全岗位族后再开始。"
        )
    elif industry == "cybersecurity":
        role_choice = detect_role_family(
            resume_text,
            jd_text,
            role_map=role_map,
        )
    elif industry in {
        "software_engineering",
        "data_ai",
        "business_operations",
    }:
        role_choice = {
            "role_family": industry,
            "role_source": "industry_mapping",
            "score": None,
            "candidates": [],
        }
    else:
        role_choice = {
            "role_family": "generic",
            "role_source": "industry_fallback",
            "score": None,
            "candidates": [],
        }
    role_id = role_choice["role_family"]
    level_value, level_source = _normalise_level(level, role_map)
    count = _validate_count(count)
    resume_hash = _sha256_text(resume_text)
    jd_provided = bool(jd_text.strip())
    jd_hash = _sha256_text(jd_text) if jd_provided else None
    seed_source = "user" if seed else "derived"
    raw_seed = seed or "{}:{}:{}:{}:{}".format(
        resume_hash,
        jd_hash or "",
        role_id,
        level_value,
        count,
    )
    plan = select_question_plan(
        audit_report,
        role_id,
        level_value,
        count=count,
        seed=raw_seed,
        today=today,
        bank=bank,
        role_map=role_map,
        source_registry=source_registry,
    )
    created = _now_iso(now)
    session_id = "INT-" + _sha256_text(
        resume_hash + ":" + (jd_hash or "") + ":" + created
    )[:16]
    questions = plan["questions"]
    return {
        "schema_version": INTERVIEW_SCHEMA_VERSION,
        "session_id": session_id,
        "created_at": created,
        "updated_at": created,
        "status": "in_progress",
        "inputs": {
            "resume_sha256": resume_hash,
            "jd_sha256": jd_hash,
            "jd_provided": jd_provided,
            "industry": industry,
            "role_family": role_id,
            "role_source": role_choice["role_source"],
            "level": level_value,
            "level_source": level_source,
            "bank_version": bank.get("bank_version"),
            "seed_source": seed_source,
        },
        "selection": {
            "seed": plan["seed"],
            "count": plan["count"],
            "distribution": plan["distribution"],
            "target_distribution": plan["target_distribution"],
            "quota_adjusted": plan["quota_adjusted"],
            "level_adjusted": plan["level_adjusted"],
            "selection_hash": plan["selection_hash"],
        },
        "analysis": _analysis_summary(audit_report),
        "questions": questions,
        "answers": [],
        "current_question_id": questions[0]["session_question_id"],
        "current_phase": "primary",
        "review": None,
    }


def _question_by_id(session, question_id):
    for item in session.get("questions", []) or []:
        if item.get("session_question_id") == question_id:
            return item
    return None


_CATEGORY_PATTERNS = {
    "goal": ("目标", "目的", "为了", "需要解决"),
    "situation": ("场景", "背景", "当时", "问题", "任务"),
    "ownership": ("我负责", "我主导", "独立", "牵头", "owner", "个人负责", "负责"),
    "action": (
        "设计", "实施", "排查", "分析", "处置", "隔离", "恢复", "修复",
        "验证", "部署", "优化", "审计", "测试", "建模", "配置", "编写",
        "推动", "建立", "使用", "执行", "复核", "完成",
    ),
    "method": (
        "工具", "方法", "流程", "规则", "通过", "使用", "SIEM", "EDR",
        "SQL", "Python", "MITRE", "OWASP", "Terraform", "Kubernetes",
        "日志", "样本", "基线",
    ),
    "scale": ("规模", "范围", "覆盖", "每天", "每周", "系统", "告警量", "时间窗"),
    "result": (
        "降低", "提升", "减少", "缩短", "恢复", "避免", "阻断", "发现",
        "覆盖", "完成", "通过",
    ),
    "verification": ("验证", "复核", "指标", "基线", "样本", "证据", "复测", "日志"),
    "boundary": (
        "边界", "范围外", "限制", "例外", "未确认", "不能确认", "不确定",
        "取舍", "回滚", "风险", "未覆盖",
    ),
    "timeline": (
        "时间线", "发现时间", "确认时间", "遏制", "恢复时间", "小时",
        "分钟", "当天", "次日",
    ),
    "authorization": ("授权", "批准", "责任主体", "禁止动作", "授权范围"),
    "risk": ("风险", "影响", "回滚", "补偿", "取舍", "业务依赖"),
    "classification": ("分类", "分级", "等级", "定级"),
    "misconception": ("误区", "误报", "限制", "不能只凭", "人工确认"),
}


def _detect_categories(text):
    detected = set()
    lowered = text.casefold()
    for name, terms in _CATEGORY_PATTERNS.items():
        if any(str(term).casefold() in lowered for term in terms):
            detected.add(name)
    if _METRIC_RE.search(text):
        detected.add("scale")
        detected.add("result")
    return detected


def _expected_categories(expected):
    parts = [
        item for item in re.split(r"[与和/、；,，\s]+", str(expected))
        if item
    ]
    required = []
    for part in parts:
        candidates = []
        for name, terms in _CATEGORY_PATTERNS.items():
            if any(term in part or part in term for term in terms):
                candidates.append(name)
        if candidates:
            required.append(set(candidates))
    return required


def _assess_answer(question, answer_text):
    text = answer_text.strip()
    detected = _detect_categories(text)
    matched = []
    missing = []
    for expected in question.get("expected_evidence", []) or []:
        requirements = _expected_categories(expected)
        if requirements:
            ok = all(any(item in detected for item in group) for group in requirements)
        else:
            tokens = re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z][A-Za-z0-9+&./ -]{1,}", expected)
            ok = any(_contains_term(token.strip(), text) for token in tokens if token.strip())
        if ok:
            matched.append(expected)
        else:
            missing.append(expected)

    total = len(question.get("expected_evidence", []) or [])
    ratio = (len(matched) / total) if total else 0.0
    concrete = bool(detected & {"action", "method", "scale", "result", "verification"})
    accountable = bool(detected & {"ownership", "scale", "result", "verification", "boundary"})
    if len(text) < 12 or not matched:
        status = "missing"
    elif ratio >= 0.6 and concrete and accountable:
        status = "sufficient"
    else:
        status = "partial"
    if not missing and status != "missing":
        status = "sufficient"
    return {
        "evidence_status": status,
        "matched_evidence": matched,
        "missing_evidence": missing,
        "detected_categories": sorted(detected),
    }


def _choose_followup(question, missing_evidence):
    followups = [
        item for item in question.get("followups", []) or []
        if isinstance(item, str) and item.strip()
    ]
    if followups:
        return followups[0].strip()
    focus = "、".join(missing_evidence[:3]) if missing_evidence else "个人责任、规模和结果"
    return "请只补充你确认真实存在的证据：{}；无法确认的部分请明确说明。".format(focus)


def _advance_question(session, current_id):
    questions = session.get("questions", []) or []
    ids = [item.get("session_question_id") for item in questions]
    try:
        index = ids.index(current_id)
    except ValueError as error:
        raise InterviewError("当前问题不在会话中：{}".format(current_id), exit_code=5) from error
    if index + 1 >= len(questions):
        session["status"] = "completed"
        session["current_question_id"] = None
        session["current_phase"] = None
        return
    session["current_question_id"] = questions[index + 1]["session_question_id"]
    session["current_phase"] = "primary"


def record_answer(session, answer_text, now=None):
    """Record one primary or follow-up answer and advance the state machine."""
    updated = copy.deepcopy(session)
    _validate_session_shape(updated)
    if updated.get("status") == "completed":
        raise InterviewError("本轮面试已完成，不能继续回答。")
    raw = str(answer_text or "").strip()
    if not raw:
        raise InterviewError("回答不能为空。")
    if len(raw) > MAX_ANSWER_CHARS:
        raise InterviewError(
            "回答超过 {} 字符上限，请拆分为真实、具体的要点。".format(MAX_ANSWER_CHARS)
        )
    question_id = updated.get("current_question_id")
    phase = updated.get("current_phase")
    question = _question_by_id(updated, question_id)
    if not question:
        raise InterviewError("会话当前问题无效。", exit_code=5)
    if phase not in {"primary", "followup"}:
        raise InterviewError("会话当前回答阶段无效。", exit_code=5)

    masked = _mask_contact(raw)
    assessment = _assess_answer(question, masked)
    answer_record = {
        "answer_id": "A{}".format(len(updated.get("answers", [])) + 1),
        "question_id": question_id,
        "phase": phase,
        "text": masked,
        "text_sha256": _sha256_text(raw),
        "recorded_at": _now_iso(now),
        "evidence_status": assessment["evidence_status"],
        "matched_evidence": assessment["matched_evidence"],
        "missing_evidence": assessment["missing_evidence"],
        "detected_categories": assessment["detected_categories"],
        "triggered_followup": None,
    }
    updated.setdefault("answers", []).append(answer_record)
    updated["updated_at"] = _now_iso(now)

    if (
        phase == "primary"
        and assessment["evidence_status"] != "sufficient"
        and int(question.get("followup_used") or 0) < 1
    ):
        prompt = _choose_followup(question, assessment["missing_evidence"])
        question["followup_used"] = 1
        question["followup_prompt"] = prompt
        answer_record["triggered_followup"] = prompt
        updated["current_phase"] = "followup"
        return updated

    _advance_question(updated, question_id)
    if updated["status"] == "completed":
        updated["review"] = build_review(updated)
    return updated


def _validate_session_shape(session):
    if not isinstance(session, dict):
        raise InterviewError("会话状态必须是 JSON 对象。", exit_code=5)
    if session.get("schema_version") != INTERVIEW_SCHEMA_VERSION:
        raise InterviewError(
            "不支持的会话 schema_version：{}".format(
                session.get("schema_version")
            ),
            exit_code=5,
        )
    if session.get("status") not in {"in_progress", "completed"}:
        raise InterviewError("会话状态字段无效。", exit_code=5)
    inputs = session.get("inputs")
    if not isinstance(inputs, dict):
        raise InterviewError("会话 inputs 无效。", exit_code=5)
    questions = session.get("questions")
    if not isinstance(questions, list) or not questions:
        raise InterviewError("会话题目为空。", exit_code=5)
    question_ids = set()
    for item in questions:
        if not isinstance(item, dict):
            raise InterviewError("会话题目格式无效。", exit_code=5)
        question_id = item.get("session_question_id")
        if not isinstance(question_id, str) or not question_id:
            raise InterviewError("会话题目缺少 session_question_id。", exit_code=5)
        if question_id in question_ids:
            raise InterviewError("会话题目 ID 重复：{}".format(question_id), exit_code=5)
        question_ids.add(question_id)
    if session.get("status") == "in_progress":
        if session.get("current_question_id") not in question_ids:
            raise InterviewError("会话当前问题不存在。", exit_code=5)
        if session.get("current_phase") not in {"primary", "followup"}:
            raise InterviewError("会话当前阶段无效。", exit_code=5)
    if not isinstance(session.get("answers", []), list):
        raise InterviewError("会话 answers 必须是数组。", exit_code=5)


def write_session_atomic(path, session):
    """Write the session atomically and keep the previous file on failure."""
    _validate_session_shape(session)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(session, ensure_ascii=False, indent=2) + "\n"
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=str(target.parent),
            prefix=target.name + ".",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(str(temp_path), str(target))
        temp_path = None
        try:
            os.chmod(str(target), 0o600)
        except OSError:
            pass
    finally:
        if temp_path is not None:
            try:
                temp_path.unlink()
            except OSError:
                pass


def load_session(path, bank_version=None):
    """Load and validate a local session file."""
    session = _read_json(path, "面试会话")
    _validate_session_shape(session)
    if bank_version is not None:
        actual = session.get("inputs", {}).get("bank_version")
        if actual != bank_version:
            raise InterviewError(
                "会话题库版本 {} 与当前题库 {} 不一致，请重新开始。".format(
                    actual,
                    bank_version,
                )
            )
    return session


def _answer_for(session, question_id, phase):
    for item in session.get("answers", []) or []:
        if item.get("question_id") == question_id and item.get("phase") == phase:
            return item
    return None


def _unique(items):
    result = []
    seen = set()
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def build_review(session):
    """Build a rule-based evidence review without a subjective score."""
    questions = session.get("questions", []) or []
    answered_primary = 0
    review_questions = []
    gaps = {}
    learning_focus = []
    improvements = []
    suggestion_by_finding = {
        item.get("finding_id"): item
        for item in session.get("analysis", {}).get("suggestions", []) or []
        if item.get("finding_id")
    }
    for question in questions:
        primary = _answer_for(
            session,
            question["session_question_id"],
            "primary",
        )
        followup = _answer_for(
            session,
            question["session_question_id"],
            "followup",
        )
        if primary:
            answered_primary += 1
        matched = []
        missing = []
        if primary:
            matched.extend(primary.get("matched_evidence", []) or [])
            missing.extend(primary.get("missing_evidence", []) or [])
        if followup:
            matched.extend(followup.get("matched_evidence", []) or [])
            missing.extend(followup.get("missing_evidence", []) or [])
        matched = _unique(matched)
        missing = _unique(missing)
        for item in missing:
            gaps[item] = gaps.get(item, 0) + 1
        review_questions.append({
            "session_question_id": question["session_question_id"],
            "bank_question_id": question["bank_question_id"],
            "kind": question["kind"],
            "dimension": question["dimension"],
            "prompt": question["prompt"],
            "level": question["level"],
            "source_refs": list(question.get("source_refs", [])),
            "basis": copy.deepcopy(question.get("basis", {})),
            "primary_status": primary.get("evidence_status") if primary else None,
            "followup_prompt": question.get("followup_prompt"),
            "followup_status": followup.get("evidence_status") if followup else None,
            "matched_evidence": matched,
            "missing_evidence": missing,
            "answer_excerpt": (
                primary.get("text", "")[:200] if primary else None
            ),
        })
        learning_focus.append({
            "dimension": question["dimension"],
            "expected_evidence": list(question.get("expected_evidence", [])),
            "source_refs": list(question.get("source_refs", [])),
            "bank_question_id": question["bank_question_id"],
        })
        for finding_id in question.get("basis", {}).get("resume_findings", []) or []:
            suggestion = suggestion_by_finding.get(finding_id)
            if suggestion:
                improvements.append({
                    "finding_id": finding_id,
                    "original": suggestion.get("original"),
                    "suggestion": suggestion.get("suggestion"),
                    "priority": suggestion.get("priority"),
                    "basis_question_id": question["bank_question_id"],
                })

    unique_focus = []
    seen_focus = set()
    for item in learning_focus:
        key = (item["dimension"], item["bank_question_id"])
        if key not in seen_focus:
            seen_focus.add(key)
            unique_focus.append(item)
    evidence_gaps = [
        {"evidence": item, "question_count": count}
        for item, count in sorted(gaps.items(), key=lambda pair: (-pair[1], pair[0]))
    ]
    return {
        "schema_version": INTERVIEW_SCHEMA_VERSION,
        "session_id": session.get("session_id"),
        "session_status": session.get("status"),
        "summary": {
            "status_label": (
                "已完成" if session.get("status") == "completed" else "进行中"
            ),
            "role_family": session.get("inputs", {}).get("role_family"),
            "level": session.get("inputs", {}).get("level"),
            "bank_version": session.get("inputs", {}).get("bank_version"),
            "question_count": len(questions),
            "completed_questions": answered_primary,
            "answer_count": len(session.get("answers", []) or []),
            "followup_count": sum(
                1 for item in session.get("answers", []) or []
                if item.get("phase") == "followup"
            ),
            "jd_provided": bool(
                session.get("inputs", {}).get("jd_provided")
            ),
        },
        "questions": review_questions,
        "evidence_gaps": evidence_gaps,
        "resume_improvements": improvements,
        "jd_gaps": list(session.get("analysis", {}).get("jd_missing", []) or []),
        "learning_focus": unique_focus,
        "boundary": (
            "本复盘只检查回答中的可验证证据，不预测面试通过率或 Offer 结果，"
            "不替代真实面试官。"
        ),
    }


def _safe_markdown(value):
    text = str(value or "")
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    return text.replace("`", "'")


def render_session_markdown(session):
    """Render start or answer output as a human-readable interview turn."""
    lines = [
        "# 元简模拟面试",
        "",
        "- 会话：`{}`".format(session["session_id"]),
        "- 岗位族：`{}`".format(session["inputs"]["role_family"]),
        "- 职级：`{}`（{}）".format(
            session["inputs"]["level"],
            "用户指定" if session["inputs"]["level_source"] == "user" else "默认",
        ),
        "- 题库版本：`{}`".format(session["inputs"]["bank_version"]),
        "- 状态：{}".format(
            "已完成" if session["status"] == "completed" else "进行中"
        ),
    ]
    if session["status"] == "completed":
        lines.extend([
            "",
            "本轮题目已完成。运行 `interview review --session <文件>` 查看复盘。",
        ])
        return "\n".join(lines)
    question = _question_by_id(session, session["current_question_id"])
    lines.extend([
        "",
        "## 当前问题",
        "",
        "**{}** {}".format(
            question["session_question_id"],
            _safe_markdown(question["prompt"]),
        ),
        "",
        "回答阶段：{}".format(
            "追问" if session["current_phase"] == "followup" else "主题回答"
        ),
        "",
        "期望证据：{}".format(
            "、".join(_safe_markdown(item) for item in question["expected_evidence"])
        ),
        "",
        "回答边界：{}".format(_safe_markdown(question["answer_boundary"])),
        "",
        "使用 `interview answer --session <文件> --answer <回答文件>` 记录回答。",
    ])
    if session.get("answers"):
        latest = session["answers"][-1]
        lines.extend([
            "",
            "## 上一回答",
            "",
            "- 证据状态：`{}`".format(latest["evidence_status"]),
            "- 缺失证据：{}".format(
                "、".join(latest.get("missing_evidence", [])) or "无"
            ),
            "> " + _safe_markdown(latest.get("text", "")[:200]),
        ])
    return "\n".join(lines)


def render_review_markdown(review):
    """Render the evidence review as a copyable Markdown report."""
    summary = review["summary"]
    lines = [
        "# 元简模拟面试复盘",
        "",
        "## 会话摘要",
        "",
        "- 状态：{}".format(summary["status_label"]),
        "- 岗位族：`{}`".format(summary["role_family"]),
        "- 职级：`{}`".format(summary["level"]),
        "- 题库版本：`{}`".format(summary["bank_version"]),
        "- 已完成主题：{} / {}".format(
            summary["completed_questions"],
            summary["question_count"],
        ),
        "- 回答数 / 追问数：{} / {}".format(
            summary["answer_count"],
            summary["followup_count"],
        ),
        "",
        "## 逐题复盘",
    ]
    for item in review["questions"]:
        lines.extend([
            "",
            "### {}".format(item["session_question_id"]),
            "",
            "{}".format(_safe_markdown(item["prompt"])),
            "",
            "- 类型：`{}`".format(item["kind"]),
            "- 维度：{}".format(_safe_markdown(item["dimension"])),
            "- 主题回答：{}".format(item["primary_status"] or "未回答"),
            "- 追问回答：{}".format(item["followup_status"] or "未使用"),
            "- 缺失证据：{}".format(
                "、".join(item["missing_evidence"]) or "无"
            ),
        ])
        if item.get("answer_excerpt"):
            lines.append("> " + _safe_markdown(item["answer_excerpt"]))
    lines.extend(["", "## 证据缺口"])
    if review["evidence_gaps"]:
        for item in review["evidence_gaps"]:
            lines.append("- {}：{} 题".format(
                item["evidence"],
                item["question_count"],
            ))
    else:
        lines.append("- 当前规则未发现重复证据缺口。")
    lines.extend(["", "## 简历改写建议"])
    if review["resume_improvements"]:
        for item in review["resume_improvements"]:
            lines.append("- [{}] {}：{}".format(
                item["finding_id"],
                _safe_markdown(item["original"]),
                _safe_markdown(item["suggestion"]),
            ))
    else:
        lines.append("- 本轮没有关联到可改写的简历规则发现。")
    lines.extend(["", "## JD 缺口"])
    if review["jd_gaps"]:
        lines.append("- " + "、".join(review["jd_gaps"]))
        lines.append("- 关键词缺失只表示未在简历中找到明确术语，不等于能力不足。")
    else:
        lines.append("- 未提供 JD，不能判断岗位关键词缺口。")
    lines.extend(["", "## 学习重点"])
    for item in review["learning_focus"]:
        lines.append("- {}：{}（题库 {}）".format(
            _safe_markdown(item["dimension"]),
            "、".join(item["expected_evidence"]),
            item["bank_question_id"],
        ))
    lines.extend([
        "",
        "## 边界",
        "",
        review["boundary"],
    ])
    return "\n".join(lines)


def probe_state_support():
    """Check that a session-like payload can be written atomically."""
    with tempfile.TemporaryDirectory(prefix="yotta-resume-interview-doctor-") as tmp:
        target = Path(tmp) / "probe.json"
        payload = {"schema_version": INTERVIEW_SCHEMA_VERSION, "probe": True}
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                newline="\n",
                dir=tmp,
                prefix="probe.",
                suffix=".tmp",
                delete=False,
            ) as handle:
                temp_path = Path(handle.name)
                handle.write(json.dumps(payload))
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(str(temp_path), str(target))
            temp_path = None
            return json.loads(target.read_text(encoding="utf-8")) == payload
        finally:
            if temp_path is not None:
                try:
                    temp_path.unlink()
                except OSError:
                    pass
