from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from core.mission import mission_markers


RISK_PENALTIES = {
    "low": 30,
    "medium": 18,
    "high": 8,
}


def _lower_list(values: list[str]) -> list[str]:
    return [value.lower() for value in values]


def _mission_lexicon(mission: dict[str, Any]) -> list[str]:
    phrases = []
    for field in ("primary_topics", "watch_keywords", "audience"):
        value = mission.get(field, [])
        if isinstance(value, list):
            phrases.extend(str(item).lower() for item in value)
    voice = mission.get("voice")
    if isinstance(voice, str):
        phrases.extend(part.strip().lower() for part in voice.split(",") if part.strip())

    lexicon: list[str] = []
    for phrase in phrases:
        if len(phrase) >= 3:
            lexicon.append(phrase)
        for token in phrase.replace("/", " ").replace("-", " ").split():
            token = token.strip().lower()
            if len(token) >= 3:
                lexicon.append(token)
    return list(dict.fromkeys(lexicon))


def recency_bonus(posted_at: str | None) -> tuple[float, str | None]:
    if not posted_at:
        return 0.0, None
    try:
        dt = datetime.fromisoformat(posted_at.replace("Z", "+00:00"))
        age_hours = max(0.0, (datetime.now(timezone.utc) - dt.astimezone(timezone.utc)).total_seconds() / 3600.0)
    except Exception:
        return 0.0, None

    if age_hours <= 2:
        return 14.0, "within the critical first two hours"
    if age_hours <= 6:
        return 6.0, "still relatively fresh"
    return 0.0, None


def link_penalty(text: str) -> tuple[float, bool]:
    has_link = "http://" in text or "https://" in text
    return (6.0 if has_link else 0.0, has_link)


def interaction_penalty(mission: dict[str, Any], item: dict[str, Any]) -> tuple[float, list[str], str]:
    reasons: list[str] = []
    penalty = 0.0
    reply_settings = str(item.get("reply_settings") or "everyone").lower()
    is_reply_tweet = bool(item.get("is_reply_tweet"))
    mentions = {str(value).lower().lstrip("@") for value in item.get("mentions", [])}
    handle = str(mission.get("account_handle") or "").lower().lstrip("@")

    readiness = "open"
    if reply_settings != "everyone":
        penalty += 18.0
        readiness = "restricted"
        reasons.append(f"reply settings are {reply_settings}")
        if reply_settings == "mentionedusers" and handle and handle.lstrip("@") not in mentions:
            penalty += 10.0
            reasons.append("mission account is not mentioned in the target tweet")

    if is_reply_tweet:
        penalty += 14.0
        readiness = "thread_reply" if readiness == "open" else readiness
        reasons.append("target is already a reply inside another conversation")
        if handle and handle not in mentions:
            penalty += 6.0
            reasons.append("mission account is not part of that reply sub-thread")

    return penalty, reasons, readiness


def choose_action(mission: dict[str, Any], total_score: float, risk_level: str, item: dict[str, Any]) -> str:
    text = (item.get("text") or "").lower()
    direct_conversation = "@" in text
    relevant_markers = mission_markers(mission)
    mission_signal = any(marker in text for marker in relevant_markers)
    question_signal = "?" in text or any(
        phrase in text
        for phrase in [
            "how ",
            "how do",
            "how to",
            "issue",
            "problem",
            "anyone",
            "would love to hear",
            "should",
        ]
    )
    experience_signal = any(
        phrase in text
        for phrase in [
            "i use",
            "i tried",
            "i run",
            "works for me",
            "i had to",
            "after installing",
            "setup",
        ]
    )
    restrictive_conversation = direct_conversation and not any(
        phrase in text for phrase in relevant_markers
    )
    interaction_readiness = (item.get("algorithm_hints") or {}).get("interaction_readiness")

    if risk_level == "high":
        return "observe"
    if interaction_readiness == "restricted" and total_score < 60:
        return "post" if total_score >= 35 else "observe"
    if interaction_readiness == "thread_reply" and total_score < 55:
        return "post" if total_score >= 35 else "observe"
    if restrictive_conversation and total_score < 45:
        return "observe"
    if direct_conversation and not mission_signal and total_score < 42:
        return "observe"
    if direct_conversation and total_score < 38 and not question_signal and not experience_signal:
        return "observe"
    if direct_conversation and (question_signal or experience_signal) and total_score >= 30:
        return "reply"
    if total_score >= 70:
        return "reply" if item.get("source_type") in {"kol", "brand"} else "quote_post"
    if total_score >= 50:
        return "quote_post"
    if total_score >= 35:
        return "post"
    return "observe"


def score_opportunity(mission: dict[str, Any], item: dict[str, Any], memory: dict[str, Any] | None = None) -> dict[str, Any]:
    mission_topics = _lower_list(mission.get("primary_topics", []))
    mission_keywords = _lower_list(mission.get("watch_keywords", []))
    mission_lexicon = _mission_lexicon(mission)
    watched_accounts = set(_lower_list(mission.get("watch_accounts", [])))
    banned_topics = _lower_list(mission.get("banned_topics", []))
    memory = memory or {}
    successful_topics = {key.lower(): value for key, value in memory.get("successful_topics", {}).items()}
    high_signal_accounts = {key.lower(): value for key, value in memory.get("high_signal_accounts", {}).items()}
    avoid_accounts = {key.lower(): value for key, value in memory.get("avoid_accounts", {}).items()}

    text = (item.get("text") or "").lower()
    item_topics = _lower_list(item.get("topics", []))
    source_account = (item.get("source_account") or "").lower()

    topic_hits = sum(1 for topic in mission_topics if topic in item_topics or topic in text)
    keyword_hits = sum(1 for keyword in mission_keywords if keyword in text)
    lexicon_hits = sum(1 for token in mission_lexicon if token in text)
    watched_bonus = 18 if source_account in watched_accounts else 0
    memory_topic_bonus = sum(min(6, successful_topics.get(topic, 0) * 2) for topic in item_topics)
    memory_account_bonus = min(10, high_signal_accounts.get(source_account, 0) * 3)
    memory_account_penalty = min(15, avoid_accounts.get(source_account, 0) * 4)
    recent_bonus, recent_reason = recency_bonus(item.get("posted_at"))
    off_platform_penalty, has_link = link_penalty(text)
    source_bonus = 8 if item.get("source_type") == "kol" else 4 if item.get("source_type") == "brand" else 0
    weak_relevance_penalty = 22 if watched_bonus and topic_hits == 0 and keyword_hits == 0 and lexicon_hits < 2 else 0
    interaction_risk_penalty, interaction_risk_reasons, interaction_readiness = interaction_penalty(mission, item)
    velocity_score = round(float(item.get("growth_velocity", 0)) * 25, 2)
    engagement_score = min(
        20,
        (
            int(item.get("likes", 0))
            + int(item.get("replies", 0)) * 2
            + int(item.get("quotes", 0)) * 2
            + int(item.get("reposts", 0)) * 2
        ) / 100,
    )

    risk_hits = [topic for topic in banned_topics if topic in item_topics or topic in text]
    sentiment = (item.get("sentiment") or "").lower()
    sentiment_penalty = 10 if sentiment in {"heated", "negative"} else 0
    base_penalty = RISK_PENALTIES[mission.get("risk_tolerance", "medium")]
    risk_penalty = base_penalty if risk_hits else 0
    total_score = round(
        topic_hits * 16
        + keyword_hits * 10
        + min(12, lexicon_hits * 3)
        + watched_bonus
        + memory_topic_bonus
        + memory_account_bonus
        + recent_bonus
        + source_bonus
        + velocity_score
        + engagement_score
        - memory_account_penalty
        - weak_relevance_penalty
        - interaction_risk_penalty
        - off_platform_penalty
        - risk_penalty
        - sentiment_penalty,
        2,
    )

    reasons: list[str] = []
    if topic_hits:
        reasons.append(f"matches {topic_hits} mission topic(s)")
    if keyword_hits:
        reasons.append(f"mentions {keyword_hits} watched keyword(s)")
    if lexicon_hits:
        reasons.append(f"matches {lexicon_hits} mission lexicon hit(s)")
    if watched_bonus:
        reasons.append("comes from a watched account")
    if memory_topic_bonus:
        reasons.append("similar topics performed well historically")
    if memory_account_bonus:
        reasons.append("source account has produced good prior outcomes")
    if memory_account_penalty:
        reasons.append("source account has low-value history")
    if recent_reason:
        reasons.append(recent_reason)
    if weak_relevance_penalty:
        reasons.append("weak topical relevance despite watched-account status")
    if interaction_risk_reasons:
        reasons.extend(interaction_risk_reasons)
    if velocity_score >= 15:
        reasons.append("showing strong growth velocity")
    if engagement_score >= 10:
        reasons.append("already has strong engagement")
    if has_link:
        reasons.append("contains an off-platform link")
    if risk_hits:
        reasons.append(f"touches banned topic(s): {', '.join(risk_hits)}")
    if sentiment_penalty:
        reasons.append(f"sentiment is {sentiment}")

    risk_level = "high" if risk_hits or sentiment_penalty >= 10 else "medium" if total_score < 35 else "low"
    item_for_action = {
        **item,
        "algorithm_hints": {
            "reply_window_open": recent_bonus >= 14.0,
            "avoid_link_in_main_post": has_link,
            "interaction_readiness": interaction_readiness,
        },
    }
    recommended_action = choose_action(mission, total_score, risk_level, item_for_action)

    return {
        **item_for_action,
        "score": total_score,
        "risk_level": risk_level,
        "recommended_action": recommended_action,
        "reasons": reasons,
    }
