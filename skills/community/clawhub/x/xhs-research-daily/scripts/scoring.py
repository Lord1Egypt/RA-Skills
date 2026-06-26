from __future__ import annotations

import math
import re
from typing import Any

RESEARCH_TERMS = {
    "diffusion", "llm", "language model", "reasoning", "inference", "sft", "rl",
    "rlhf", "dpo", "alignment", "safety", "agent", "memory", "multi-agent",
    "sampling", "test-time", "trace", "policy", "reward", "benchmark", "paper",
    "arxiv", "poster", "训练", "推理", "后训练", "安全", "对齐", "扩散", "记忆", "多智能体"
}

LOW_SIGNAL_TERMS = {
    "求助", "互关", "薯条", "涨粉", "宝子", "冲", "接单", "代发", "引流", "优惠", "课程", "培训"
}


def _text_blob(post: dict[str, Any]) -> str:
    card = post.get("noteCard", {})
    title = card.get("displayTitle") or ""
    desc = card.get("desc") or post.get("content") or ""
    return f"{title}\n{desc}".lower()


def score_post(post: dict[str, Any]) -> float:
    text = _text_blob(post)
    score = 0.0
    for term in RESEARCH_TERMS:
        if term in text:
            score += 2.5
    for term in LOW_SIGNAL_TERMS:
        if term in text:
            score -= 4.0
    card = post.get("noteCard", {})
    interact = card.get("interactInfo", {})
    raw_like = interact.get("likedCount") or "0"
    score += min(parse_count(raw_like) / 2000.0, 4.0)
    if card.get("type") == "normal":
        score += 0.6
    if len(text.strip()) < 12:
        score -= 2.0
    return round(score, 3)


def score_comment(comment: dict[str, Any]) -> float:
    text = (comment.get("content") or "").lower()
    if not text.strip():
        return -1.0
    score = 0.0
    for term in RESEARCH_TERMS:
        if term in text:
            score += 2.0
    for term in LOW_SIGNAL_TERMS:
        if term in text:
            score -= 3.0
    if len(text) > 30:
        score += 0.8
    return round(score, 3)


def parse_count(raw: Any) -> int:
    if raw is None:
        return 0
    text = str(raw).strip().lower().replace(",", "")
    if not text:
        return 0
    if text.endswith("万+"):
        return int(float(text[:-2]) * 10000)
    if text.endswith("万"):
        return int(float(text[:-1]) * 10000)
    match = re.search(r"\d+(?:\.\d+)?", text)
    if not match:
        return 0
    return int(math.floor(float(match.group(0))))
