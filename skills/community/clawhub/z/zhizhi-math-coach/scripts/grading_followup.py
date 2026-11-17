"""Normalize full-paper evidence and choose explainable follow-up actions."""

from __future__ import annotations

import copy
import datetime as dt
import hashlib
import re
from collections import defaultdict
from pathlib import Path


RESULTS = {"correct", "wrong", "unanswered", "need-confirmation"}
UNCERTAIN = {"need-confirmation", "unanswered"}


def normalize_payload(payload: dict) -> dict:
    result = copy.deepcopy(payload)
    items = result.get("items")
    if not isinstance(items, list):
        return result
    result.setdefault("coverage", "complete")
    result.setdefault("total_items", len(items) if result["coverage"] == "complete" else "unknown")
    result.setdefault("correct_items", sum(isinstance(item, dict) and item.get("result") == "correct" for item in items))
    mistakes = []
    for item in items:
        if not isinstance(item, dict) or item.get("result") == "correct":
            continue
        mistake = copy.deepcopy(item)
        defaults = {
            "question": "题目未能完整识别", "student_answer": "未作答/未识别",
            "correct_answer": "待确认", "error_type": "待确认", "cause": "待诊断",
            "confidence": "low", "remediation": "先核对原图或补充清晰图片，再判断原因。",
        }
        for key, value in defaults.items():
            if mistake.get(key) is None or mistake.get(key) == "":
                mistake[key] = value
        mistakes.append(mistake)
    result["mistakes"] = mistakes
    return result


def topic_slug(item: dict) -> str:
    raw = str(item.get("weak_point_slug") or "")
    if re.fullmatch(r"[a-z0-9]+(?:[._-][a-z0-9]+)*", raw):
        return raw
    cause = str(item.get("cause", "待诊断"))
    return "cause-" + hashlib.sha256(cause.encode()).hexdigest()[:12]


def plan_followup(workspace: Path, payload: dict, requested_mode: str) -> tuple[dict, dict]:
    result = copy.deepcopy(payload)
    groups: dict[str, list[dict]] = defaultdict(list)
    confirmation = []
    for item in result.get("mistakes") or []:
        if item.get("result") != "wrong" or item.get("confidence") in {"低", "low"}:
            confirmation.append(str(item["item_no"]))
        elif item.get("cause") not in {None, "", "待诊断", "unknown", "待确认"}:
            groups[topic_slug(item)].append(item)
    repeated = {key: items for key, items in groups.items() if len(items) >= 2}
    matched = {key for key in groups if (workspace / "weak-points" / f"{key}.md").is_file()}
    reasons = []
    if repeated:
        reasons.append("同一错因有至少两道已确认错题")
    if matched:
        reasons.append("已确认错题匹配已有薄弱项，需要对照历史证据")
    if result.get("source_type") in {"formal_test", "teacher_marked", "midterm", "final"}:
        reasons.append("正式测验或教师批改试卷")
    if result.get("weak_points"):
        reasons.append("诊断包含明确的薄弱项更新")
    mode = ("full_archive" if reasons else "fast_grade_light_record") if requested_mode == "auto" else requested_mode
    if not reasons:
        reasons.append("未发现需要深度归档的已确认重复证据")
    if requested_mode != "auto":
        reasons.append(f"使用显式模式：{requested_mode}")

    weak_points = result.get("weak_points") or []
    if mode == "fast_grade_light_record" and weak_points:
        raise ValueError("weak_points updates require --mode auto or full_archive")
    existing = {topic_slug({"weak_point_slug": wp.get("slug"), "cause": wp.get("title")}) for wp in weak_points}
    date = dt.date.fromisoformat(result["date"])
    if mode == "full_archive":
        for slug, items in repeated.items():
            if slug in existing or slug in matched:
                continue
            weak_points.append({
                "slug": slug, "title": items[0]["cause"], "status": "薄弱项",
                "likely_causes": [items[0]["cause"]],
                "history_note": "同批次已确认错题：" + "、".join(str(item["item_no"]) for item in items),
                "next_action": items[0]["remediation"],
                "next_review_date": (date + dt.timedelta(days=3)).isoformat(),
            })
        result["weak_points"] = weak_points

    reviews = []
    for slug, items in groups.items():
        wp = next((wp for wp in weak_points if wp.get("slug") == slug), {})
        reviews.append({
            "slug": slug, "topic": items[0]["cause"], "evidence_date": result["date"],
            "due_date": wp.get("next_review_date") or (date + dt.timedelta(days=3)).isoformat(),
            "strategy": "diagnostic_probe" if slug in matched else "wrong_question_variant",
            "question_count": 3, "item_nos": [str(item["item_no"]) for item in items],
            "action": items[0]["remediation"],
            "history_path": f"weak-points/{slug}.md" if slug in matched else "",
        })
    for wp in weak_points:
        if wp.get("next_review_date") and wp.get("slug") and not any(r["slug"] == wp["slug"] for r in reviews):
            reviews.append({"slug": wp["slug"], "topic": wp.get("title", wp["slug"]),
                            "evidence_date": result["date"], "due_date": wp["next_review_date"],
                            "strategy": "spaced_review", "question_count": 3,
                            "action": wp.get("next_action", "按复测标准复练"), "item_nos": []})
    return result, {"mode": mode, "reasons": reasons, "confirmation_items": confirmation, "reviews": reviews}
