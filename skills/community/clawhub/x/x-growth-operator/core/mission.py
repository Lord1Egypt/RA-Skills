from __future__ import annotations

import re
from typing import Any

from scripts.common import normalize_text, utc_now_iso


SECTION_ALIASES = {
    "goals": "goals",
    "goal": "goals",
    "运营目标是": "goals",
    "audience": "audience",
    "target audience": "audience",
    "voice": "voice",
    "tone": "voice",
    "priority topics": "priority topics",
    "topics": "priority topics",
    "focus topics": "priority topics",
    "watch keywords": "watch keywords",
    "keywords": "watch keywords",
    "watch accounts": "watch accounts",
    "accounts": "watch accounts",
    "watchlist": "watch accounts",
    "banned topics": "banned topics",
    "avoid": "banned topics",
    "preferred cta": "preferred cta",
    "cta": "preferred cta",
    "call to action": "preferred cta",
    "risk tolerance": "risk tolerance",
    "risk": "risk tolerance",
    "目标": "goals",
    "运营目标": "goals",
    "受众": "audience",
    "目标受众": "audience",
    "语气": "voice",
    "风格": "voice",
    "重点话题": "priority topics",
    "重点话题包括": "priority topics",
    "核心话题": "priority topics",
    "话题": "priority topics",
    "关注关键词": "watch keywords",
    "关键词": "watch keywords",
    "关注账号": "watch accounts",
    "账号": "watch accounts",
    "禁区": "banned topics",
    "避免话题": "banned topics",
    "行动号召": "preferred cta",
    "行动号召是": "preferred cta",
    "转化动作": "preferred cta",
    "风险偏好": "risk tolerance",
    "风险": "risk tolerance",
}

TOPIC_HINTS = (
    "ai",
    "agent",
    "agents",
    "beauty",
    "b2b",
    "climate",
    "commerce",
    "community",
    "creator",
    "devtools",
    "education",
    "enterprise",
    "fashion",
    "fintech",
    "fitness",
    "health",
    "infra",
    "ingredient",
    "launch",
    "local",
    "luxury",
    "marketplace",
    "media",
    "parenting",
    "productivity",
    "refillable",
    "saas",
    "security",
    "skincare",
    "software",
    "sustainable",
    "wellness",
    "workflow",
    "护肤",
    "美妆",
    "母婴",
    "本地",
    "智能体",
    "效率",
    "教育",
    "健康",
    "增长",
    "内容",
    "电商",
    "品牌",
    "视频",
    "营销",
)


def dedupe_keep_order(values: list[str], *, lower: bool = True) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        cleaned = normalize_text(value)
        if not cleaned:
            continue
        key = cleaned.lower() if lower else cleaned
        if key in seen:
            continue
        seen.add(key)
        result.append(cleaned)
    return result


def contains_cjk(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text or ""))


def split_phrase_list(text: str) -> list[str]:
    normalized = normalize_text(text)
    if not normalized:
        return []
    normalized = re.sub(r"\band\b", ",", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"[、，；;和及/|]+", ",", normalized)
    parts = [part.strip(" .,:;") for part in normalized.split(",")]
    return [part for part in parts if part]


def parse_sections(raw_text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {"summary": []}
    current = "summary"

    for line in raw_text.splitlines():
        stripped = line.strip()
        lowered = stripped.lower().rstrip(":：")
        canonical = SECTION_ALIASES.get(lowered)
        if canonical:
            current = canonical
            sections.setdefault(current, [])
            continue

        inline_match = re.match(r"^([^:：]{1,40})[:：]\s*(.+)$", stripped)
        if inline_match:
            key = inline_match.group(1).strip().lower()
            value = inline_match.group(2).strip()
            canonical_inline = SECTION_ALIASES.get(key)
            if canonical_inline:
                sections.setdefault(canonical_inline, [])
                if value:
                    sections[canonical_inline].append(value)
                current = canonical_inline
                continue
        if stripped.startswith(("语气要", "语气应", "风格要", "风格应")):
            value = re.sub(r"^(语气|风格)[要应]?", "", stripped).strip("：: ")
            sections.setdefault("voice", [])
            if value:
                sections["voice"].append(value)
            current = "voice"
            continue
        if stripped.startswith("- "):
            sections.setdefault(current, []).append(stripped[2:].strip())
        elif stripped:
            sections.setdefault(current, []).append(stripped)

    return sections


def first_sentence(text: str) -> str:
    parts = re.split(r"(?<=[.!?。！？])\s+", normalize_text(text))
    return parts[0] if parts else normalize_text(text)


def compact_name(text: str) -> str:
    sentence = first_sentence(text).lstrip("# ").strip()
    words = sentence.split()
    if len(words) <= 8:
        return sentence
    return " ".join(words[:8]).rstrip(" ,.;:!?")


def find_goal(summary: str) -> str:
    patterns = [
        r"(?:the goal(?: over [^.]*)? is to|goal is to)\s+([^.!?]+)",
        r"(?:we want to|we need to|we're trying to|we are trying to)\s+([^.!?]+)",
        r"(?:increase|grow|drive|earn|build|improve)\s+([^.!?]+)",
        r"(?:目标是|我们的目标是|运营目标是)\s*([^。！？.!?]+)",
        r"(?:提升|增长|扩大|建立|提高)\s*([^。！？.!?]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, summary, flags=re.IGNORECASE)
        if match:
            return normalize_text(match.group(0)).rstrip(".")
    return first_sentence(summary)


def find_risk(summary: str) -> str:
    match = re.search(r"risk tolerance should stay (low|medium|high)", summary, flags=re.IGNORECASE)
    if match:
        return match.group(1).lower()
    match = re.search(r"\b(low|medium|high)\s+risk tolerance\b", summary, flags=re.IGNORECASE)
    if match:
        return match.group(1).lower()
    if "stay conservative" in summary.lower():
        return "low"
    if re.search(r"(低风险|保守)", summary):
        return "low"
    if re.search(r"(高风险|激进)", summary):
        return "high"
    return "medium"


def find_cta(summary: str) -> str:
    patterns = [
        r"(?:steer readers toward|invite readers to|encourage people to)\s+([^.!?]+)",
        r"(?:cta is to|call to action is to)\s+([^.!?]+)",
        r"(?:引导用户|行动号召|希望用户)\s*(?:去|做|为)?\s*([^。！？.!?]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, summary, flags=re.IGNORECASE)
        if match:
            phrase = normalize_text(match.group(0)).rstrip(".")
            return phrase[0].upper() + phrase[1:] if phrase else ""
    return ""


def find_voice(summary: str) -> list[str]:
    match = re.search(r"(?:voice|tone)\s+(?:should|to)?\s*(?:feel|be)?\s*([^.!?]+)", summary, flags=re.IGNORECASE)
    if match:
        raw = match.group(1)
        raw = re.sub(r"^(like|as)\s+", "", raw.strip(), flags=re.IGNORECASE)
        return dedupe_keep_order(split_phrase_list(raw))
    match = re.search(r"(?:语气|风格)(?:应|要|是)?\s*([^。！？.!?]+)", summary)
    if match:
        return dedupe_keep_order(split_phrase_list(match.group(1)))
    return []


def find_topics(summary: str) -> list[str]:
    patterns = [
        r"(?:monitor discussions around|watch discussions around|focus on|prioritize|priority topics include)\s+([^.!?]+)",
        r"(?:topics include|keywords include)\s+([^.!?]+)",
        r"(?:关注|重点话题|核心话题|话题包括)\s*([^。！？.!?]+)",
    ]
    results: list[str] = []
    for pattern in patterns:
        for match in re.finditer(pattern, summary, flags=re.IGNORECASE):
            results.extend(split_phrase_list(match.group(1)))

    if results:
        return dedupe_keep_order(results)

    candidates: list[str] = []
    lowered = summary.lower()
    for phrase in re.findall(r"\b[a-z][a-z0-9-]*(?:\s+[a-z0-9-]+){0,3}\b", lowered):
        phrase = phrase.strip()
        if any(hint in phrase for hint in TOPIC_HINTS):
            candidates.append(phrase)
    return dedupe_keep_order(candidates)[:8]


def find_accounts(summary: str) -> list[str]:
    accounts = re.findall(r"@([A-Za-z0-9_]{2,30})", summary)
    text_matches = re.search(r"(?:keep an eye on)\s+([^.!?]+)", summary, flags=re.IGNORECASE)
    if not text_matches:
        text_matches = re.search(r"(?:关注账号|重点关注|关注)\s*([^。！？.!?]+)", summary)
    text_accounts: list[str] = []
    if text_matches:
        for part in split_phrase_list(text_matches.group(1)):
            normalized = part.strip()
            if " " not in normalized and 2 <= len(normalized) <= 30:
                text_accounts.append(normalized.lstrip("@"))
    return dedupe_keep_order(accounts + text_accounts)


def find_audience(summary: str) -> list[str]:
    patterns = [
        r"(?:among|for)\s+([^.!?]+?)(?:\s+who\b|\.|,)",
        r"(?:target audience is|audience is)\s+([^.!?]+)",
        r"(?:目标受众是|受众是|面向)\s*([^。！？.!?]+)",
    ]
    results: list[str] = []
    for pattern in patterns:
        for match in re.finditer(pattern, summary, flags=re.IGNORECASE):
            chunk = match.group(1)
            if len(chunk.split()) < 2 and not contains_cjk(chunk):
                continue
            results.extend(split_phrase_list(chunk))
    filtered = [
        item for item in dedupe_keep_order(results)
        if "launch" not in item.lower() and (len(item.split()) >= 2 or contains_cjk(item))
    ]
    return filtered[:6]


def find_banned_topics(summary: str) -> list[str]:
    patterns = [
        r"(?:avoid|do not touch|don't touch|never touch)\s+([^.!?]+)",
        r"(?:stay away from)\s+([^.!?]+)",
        r"(?:不要碰|禁区|避免)\s*([^。！？.!?]+)",
    ]
    results: list[str] = []
    for pattern in patterns:
        for match in re.finditer(pattern, summary, flags=re.IGNORECASE):
            results.extend(split_phrase_list(match.group(1)))
    return dedupe_keep_order(results)


def fill_from_freeform(sections: dict[str, list[str]], raw_text: str) -> dict[str, list[str]]:
    summary = normalize_text(" ".join(sections.get("summary", [])) or raw_text)
    filled = {key: list(value) for key, value in sections.items()}

    if not filled.get("goals"):
        filled["goals"] = [find_goal(summary)]
    if not filled.get("audience"):
        filled["audience"] = find_audience(summary)
    if not filled.get("voice"):
        filled["voice"] = find_voice(summary)
    if not filled.get("priority topics"):
        filled["priority topics"] = find_topics(summary)
    if not filled.get("watch keywords"):
        filled["watch keywords"] = list(filled.get("priority topics", []))
    if not filled.get("watch accounts"):
        filled["watch accounts"] = find_accounts(summary)
    if not filled.get("banned topics"):
        filled["banned topics"] = find_banned_topics(summary)
    if not filled.get("preferred cta"):
        cta = find_cta(summary)
        filled["preferred cta"] = [cta] if cta else []
    if not filled.get("risk tolerance"):
        filled["risk tolerance"] = [find_risk(summary)]
    return filled


def mission_from_text(raw_text: str) -> dict[str, Any]:
    sections = fill_from_freeform(parse_sections(raw_text), raw_text)
    summary = " ".join(sections.get("summary", []))
    goals = dedupe_keep_order(sections.get("goals", []))
    audience = dedupe_keep_order(sections.get("audience", []))
    voice = dedupe_keep_order(sections.get("voice", []))
    topics = dedupe_keep_order(sections.get("priority topics", []))
    keywords = dedupe_keep_order(sections.get("watch keywords", []))
    accounts = dedupe_keep_order(sections.get("watch accounts", []))
    banned = dedupe_keep_order(sections.get("banned topics", []))
    cta = " ".join(dedupe_keep_order(sections.get("preferred cta", [])))
    risk_tolerance = normalize_text(" ".join(sections.get("risk tolerance", ["medium"]))).lower().rstrip("。.")
    if risk_tolerance in {"低风险", "保守"}:
        risk_tolerance = "low"
    elif risk_tolerance in {"中风险", "中等"}:
        risk_tolerance = "medium"
    elif risk_tolerance in {"高风险", "激进"}:
        risk_tolerance = "high"

    headline = sections.get("summary", ["Untitled mission"])[0].lstrip("# ").strip()
    if headline and len(headline.split()) > 12:
        headline = compact_name(headline)
    goal = goals[0] if goals else normalize_text(summary)

    return {
        "name": headline or "Untitled mission",
        "goal": goal or "Grow targeted X awareness",
        "account_handle": "",
        "audience": audience,
        "voice": ", ".join(voice) if voice else "direct, clear, credible",
        "primary_topics": topics,
        "watch_keywords": keywords or topics,
        "watch_accounts": accounts,
        "banned_topics": banned,
        "cta": cta or "Invite qualified readers to learn more",
        "risk_tolerance": risk_tolerance if risk_tolerance in {"low", "medium", "high"} else "medium",
        "autonomy_mode": "review",
        "source_summary": normalize_text(summary),
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }


def mission_focus_terms(mission: dict[str, Any], limit: int = 8) -> list[str]:
    phrases: list[str] = []
    for field in ("primary_topics", "watch_keywords", "audience"):
        value = mission.get(field, [])
        if isinstance(value, list):
            phrases.extend(normalize_text(str(item)) for item in value if normalize_text(str(item)))

    seen: set[str] = set()
    ordered: list[str] = []
    for phrase in phrases:
        lowered = phrase.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        ordered.append(phrase)
        if len(ordered) >= limit:
            break
    return ordered


def mission_search_query(mission: dict[str, Any], limit: int = 6) -> str:
    phrases = mission_focus_terms(mission, limit=limit)
    if not phrases:
        fallback = normalize_text(mission.get("goal", ""))
        if fallback:
            phrases = [fallback]

    query_parts: list[str] = []
    for phrase in phrases[:limit]:
        if " " in phrase:
            query_parts.append(f'"{phrase}"')
        else:
            query_parts.append(phrase)
    return " OR ".join(query_parts)


def mission_markers(mission: dict[str, Any]) -> set[str]:
    markers: set[str] = set()
    handle = normalize_text(str(mission.get("account_handle", ""))).lower().lstrip("@")
    if handle:
        markers.add(handle)
        markers.add(f"@{handle}")

    for phrase in mission_focus_terms(mission, limit=12):
        lowered = phrase.lower()
        if len(lowered) >= 3:
            markers.add(lowered)
        for token in lowered.replace("/", " ").replace("-", " ").split():
            token = token.strip()
            if len(token) >= 4:
                markers.add(token)
    return markers
