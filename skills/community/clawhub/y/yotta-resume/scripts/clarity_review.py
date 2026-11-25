#!/usr/bin/env python3
"""Deterministic expression clarity checks without semantic AI."""

import re


CLARITY_VERSION = "1.0"
_METRIC_RE = re.compile(
    r"\d+(?:\.\d+)?\s*(?:%|％|倍|x|X|次|个|条|台|天|小时|分钟|人|万|k|K|ms|秒|元)"
)
_RESULT_RE = re.compile(
    r"(显著|明显|大幅|有效|良好|较强|较好|大幅|极大)?"
    r"(提升|提高|改善|增强|降低|减少|优化|稳定|增长|缩短)"
)
_UNVERIFIABLE_PHRASES = (
    "效果良好",
    "取得良好效果",
    "显著提升",
    "大幅提升",
    "明显改善",
    "有效改善",
    "较强能力",
    "较好效果",
    "提升系统稳定性",
    "优化用户体验",
)
_PARTICIPATION_RE = re.compile(r"(参与|协助|配合|支持|跟进)")
_OWNERSHIP_RE = re.compile(r"(独立负责|主导|牵头|负责)")
_SKILL_LEVEL_RE = re.compile(r"(精通|熟练掌握|熟练|掌握|熟悉)")
_EVIDENCE_RE = re.compile(
    r"(项目|上线|生产|覆盖|样本|验证|复测|监控|基线|结果|指标|"
    r"从\s*\d|下降|提升|降低|减少|\d)"
)


def _signal(section, heading, text, code, reason):
    return {
        "id": "",
        "code": code,
        "section": section,
        "heading": heading,
        "original": text.strip(),
        "reason": reason,
        "needs_confirmation": True,
    }


def _unique_questions(items):
    result = []
    seen = set()
    for item in items:
        key = (item["target"], item["question"])
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def build_clarity_review(bullets):
    """Return deterministic clarity signals and confirmation questions."""
    signals = []
    questions = []
    for section, heading, text in bullets:
        raw = str(text or "").strip()
        if not raw:
            continue
        has_metric = bool(_METRIC_RE.search(raw))
        has_result = bool(_RESULT_RE.search(raw)) or any(
            phrase in raw for phrase in _UNVERIFIABLE_PHRASES
        )
        has_evidence = bool(_EVIDENCE_RE.search(raw))

        if has_result and not has_metric:
            signals.append(_signal(
                section,
                heading,
                raw,
                "unverifiable_result",
                "结果词没有基线、规模、指标或验证方式，读者无法复核变化是否真实成立。",
            ))
            questions.append({
                "target": "result_evidence",
                "question": (
                    "请补充这项结果的基线、统计时间窗、覆盖规模和验证方式；"
                    "无法确认的数字必须删除，不能推测。"
                ),
                "why": "把“效果良好”一类结论改成可复核证据。",
            })

        if _PARTICIPATION_RE.search(raw) and not _OWNERSHIP_RE.search(raw):
            signals.append(_signal(
                section,
                heading,
                raw,
                "unclear_responsibility",
                "只写了参与、协助或配合，未说明独立负责、牵头和参与之间的责任边界。",
            ))
            questions.append({
                "target": "ownership",
                "question": "请说明你在其中是独立负责、牵头还是参与，并分别列出个人动作和协作边界。",
                "why": "避免把团队成果写成个人成果。",
            })

        if _SKILL_LEVEL_RE.search(raw) and not has_evidence:
            signals.append(_signal(
                section,
                heading,
                raw,
                "unsupported_skill_level",
                "能力等级没有对应项目、上线、验证或结果证据。",
            ))
            questions.append({
                "target": "skill_evidence",
                "question": "请为这项能力补充至少一个真实项目、交付物或验证证据；没有证据时下调能力等级。",
                "why": "避免无证据使用“精通”“熟练”等高位表述。",
            })

    for index, item in enumerate(signals, 1):
        item["id"] = "CLR-{:03d}".format(index)
    questions = _unique_questions(questions)
    return {
        "schema_version": CLARITY_VERSION,
        "status": "attention" if signals else "clear",
        "signals": signals,
        "questions": questions,
        "limitations": (
            "固定规则只识别结果不可验证、责任边界不清和技能等级缺少证据等"
            "显式表达，不做语义模型判断，也不生成新的主观分数。"
        ),
    }
