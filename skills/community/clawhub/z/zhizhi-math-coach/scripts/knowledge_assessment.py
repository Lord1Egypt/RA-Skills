"""Evidence counts and conservative knowledge-point assessments; no image OCR."""

from __future__ import annotations

import datetime as dt
from collections import defaultdict


def assess_knowledge(previous: dict, payload: dict, record_path: str) -> dict:
    concepts = dict(previous.get("concepts", {}))
    groups = defaultdict(list)
    titles = {}
    for item in payload.get("items", []):
        for point in item.get("knowledge_points", []):
            evidence = dict(item)
            if point.get("result"):
                evidence["result"] = point["result"]
            elif item.get("result") == "wrong" and len(item.get("knowledge_points", [])) > 1:
                # A wrong final answer does not identify which step/concept failed.
                evidence["result"] = "need-confirmation"
            if point.get("confidence") in {"low", "低"}:
                evidence["recognition_confidence"] = "low"
            groups[point["id"]].append(evidence)
            titles[point["id"]] = point["title"]
    for key, items in groups.items():
        # Recognition certainty and assistance gate performance evidence. Cause
        # confidence is separate: a visible wrong answer may have an unknown cause.
        scored = [item for item in items if item.get("result") in {"correct", "wrong"}
                  and item.get("recognition_confidence", "low") in {"high", "medium", "高", "中"}
                  and not item.get("assisted", False)]
        event = {
            "date": payload["date"], "record": record_path, "observed": len(items),
            "scored": len(scored), "correct": sum(item["result"] == "correct" for item in scored),
            "uncertain": sum(item.get("result") == "need-confirmation" or item.get("recognition_confidence", "low") in {"low", "低"} for item in items),
            "unanswered": sum(item.get("result") == "unanswered" for item in items),
            "assisted": sum(bool(item.get("assisted")) for item in items),
            "item_nos": [str(item["item_no"]) for item in items],
        }
        history = [e for e in concepts.get(key, {}).get("recent_evidence", []) if e["record"] != record_path]
        history = sorted([*history, event], key=lambda e: e["date"])[-8:]
        count = sum(e["scored"] for e in history)
        correct = sum(e["correct"] for e in history)
        latest = history[-1]
        scored_dates = sorted({e["date"] for e in history if e["scored"]})
        span = (dt.date.fromisoformat(scored_dates[-1]) - dt.date.fromisoformat(scored_dates[0])).days if scored_dates else 0
        accuracy = correct / count if count else None
        if not latest["scored"]:
            status, reason = "待确认", "本次存在无法确认的知识点证据，需核对图片或进行验证题"
        elif latest["correct"] < latest["scored"] or (accuracy is not None and accuracy < .9):
            status, reason = "需要巩固", "本次存在确认错题，或近期观察正确率低于90%"
        elif latest["uncertain"]:
            status, reason = "待确认", "本次部分题目或知识点证据尚未确认"
        elif count >= 5 and len(scored_dates) >= 2 and span >= 7:
            status, reason = "稳定掌握", "近期至少5道独立作答、跨至少7天的两次检查，观察正确率不低于90%且本次无错题"
        elif count >= 2:
            status, reason = "初步掌握", "已出现多题正确证据，仍需间隔复测"
        else:
            status, reason = "待观察", "仅有单题证据，样本不足"
        due = (dt.date.fromisoformat(latest["date"]) + dt.timedelta(days=7 if status in {"稳定掌握", "初步掌握"} else 3)).isoformat()
        concepts[key] = {
            "title": titles[key], "status": status, "reason": reason,
            "observed_accuracy": round(accuracy, 3) if accuracy is not None else None,
            "scored_items": count, "evidence_dates": len(scored_dates), "latest_date": latest["date"],
            "next_review_date": due, "recent_evidence": history,
        }
    latest_date = max(str(previous.get("updated", "")), payload["date"])
    topics = [{"id": key, "title": titles[key]} for key in groups]
    if payload["date"] < previous.get("updated", ""):
        topics = previous.get("current_paper_topics", topics)
    return {"version": 1, "updated": latest_date, "concepts": concepts, "current_paper_topics": topics}


def render_knowledge(state: dict) -> str:
    def cell(value: object) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")
    lines = ["# 知识点掌握情况", "", "依据近期独立作答证据估计，不将正确率视为掌握概率；复杂题的知识点标签需结合步骤复核。", "",
             "| 知识点 | 状态 | 观察正确率 | 有效题数 | 检查日期数 | 最近证据 | 建议复测 | 判断依据 |",
             "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for point in sorted(state["concepts"].values(), key=lambda p: (p["next_review_date"], p["title"])):
        accuracy = point["observed_accuracy"]
        values = [point["title"], point["status"], f"{accuracy:.0%}" if accuracy is not None else "待确认",
                  point["scored_items"], point["evidence_dates"], point["latest_date"], point["next_review_date"], point["reason"]]
        lines.append("| " + " | ".join(cell(value) for value in values) + " |")
    return "\n".join(lines) + "\n"
