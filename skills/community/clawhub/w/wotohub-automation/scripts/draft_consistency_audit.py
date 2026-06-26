#!/usr/bin/env python3
from __future__ import annotations

import re
from typing import Any, Optional

from email_send_guardrails import normalize_email_artifact_for_send


_PLATFORM_PATTERNS = {
    "tiktok": [r"\btiktok\b", r"\btik tok\b"],
    "youtube": [r"\byoutube\b", r"\byt\b"],
    "instagram": [r"\binstagram\b", r"\binsta\b"],
    "amazon": [r"\bamazon\b"],
    "shopify": [r"\bshopify\b"],
}

_COUNTRY_PATTERNS = {
    "us": [r"\bus\b", r"\bu\.s\.\b", r"\busa\b", r"\bamerican\b"],
    "uk": [r"\buk\b", r"\bu\.k\.\b", r"\bbritish\b", r"\bunited kingdom\b"],
    "jp": [r"\bjapan\b", r"\bjapanese\b"],
    "kr": [r"\bkorea\b", r"\bkorean\b", r"\bsouth korea\b"],
    "de": [r"\bgermany\b", r"\bgerman\b"],
    "fr": [r"\bfrance\b", r"\bfrench\b"],
    "es": [r"\bspain\b", r"\bspanish\b"],
    "it": [r"\bitaly\b", r"\bitalian\b"],
    "ca": [r"\bcanada\b", r"\bcanadian\b"],
    "au": [r"\baustralia\b", r"\baustralian\b"],
}

_LANGUAGE_PATTERNS = {
    "en": [r"\benglish\b", r"\benglish-speaking\b"],
    "es": [r"\bspanish\b", r"\bspanish-speaking\b"],
    "ja": [r"\bjapanese\b", r"\bjapanese-speaking\b"],
    "ko": [r"\bkorean\b", r"\bkorean-speaking\b"],
    "fr": [r"\bfrench\b", r"\bfrench-speaking\b"],
    "de": [r"\bgerman\b", r"\bgerman-speaking\b"],
}

_CATEGORY_PATTERNS = {
    "beauty": [r"\bbeauty\b", r"\bskincare\b", r"\bmakeup\b", r"\bcosmetic\b"],
    "fitness": [r"\bfitness\b", r"\bworkout\b", r"\bgym\b"],
    "tech": [r"\btech\b", r"\bgadget\b", r"\belectronics\b"],
    "gaming": [r"\bgaming\b", r"\bgamer\b", r"\bgameplay\b"],
    "fashion": [r"\bfashion\b", r"\bstyle\b", r"\boutfit\b"],
    "food": [r"\bfood\b", r"\brecipe\b", r"\bcooking\b"],
    "parenting": [r"\bparenting\b", r"\bmom\b", r"\bdad\b", r"\bfamily\b"],
    "travel": [r"\btravel\b", r"\btrip\b", r"\btourism\b"],
}

_AUDIENCE_CONTEXT_PATTERNS = [
    re.compile(r"\byour\s+([a-z\- ]{2,40})\s+(audience|followers|community|content|channel|videos|page)\b", re.I),
    re.compile(r"\bas\s+(a|an)\s+([a-z\- ]{2,40})\s+creator\b", re.I),
]


def _norm(value: Any) -> str:
    return str(value or "").strip().lower()


def _collect_text(email: dict[str, Any]) -> str:
    parts = [
        str(email.get("subject") or ""),
        str(email.get("plainTextBody") or email.get("body") or ""),
    ]
    return "\n".join(part for part in parts if part).lower()


def _canonical_key(value: Any, patterns: dict[str, list[str]]) -> str:
    text = _norm(value)
    if not text:
        return ""
    if text in patterns:
        return text
    for key, regexes in patterns.items():
        for regex in regexes:
            if re.search(regex, text, flags=re.I):
                return key
    return text


def _extract_mentions(text: str, patterns: dict[str, list[str]]) -> set[str]:
    hits: set[str] = set()
    for key, regexes in patterns.items():
        for regex in regexes:
            if re.search(regex, text, flags=re.I):
                hits.add(key)
                break
    return hits


def _profile_topics(profile: dict[str, Any]) -> str:
    values: list[str] = []
    for key in ("category", "contentStyle", "bloggerName", "channelName", "nickname", "platform", "country", "language"):
        value = profile.get(key)
        if value:
            values.append(str(value))
    for key in ("tagList", "recentTopics"):
        for item in (profile.get(key) or []):
            if item:
                values.append(str(item))
    return " ".join(values).lower()


def _extract_audience_descriptors(text: str) -> set[str]:
    hits: set[str] = set()
    for pattern in _AUDIENCE_CONTEXT_PATTERNS:
        for match in pattern.finditer(text):
            phrase = " ".join(group for group in match.groups() if group).strip().lower()
            if phrase:
                hits.add(phrase)
    return hits


def _pick_profile(email: dict[str, Any], creator_profiles_by_id: Optional[dict[str, dict[str, Any]]]= None) -> dict[str, Any]:
    blogger_id = str(email.get("bloggerId") or email.get("besId") or email.get("bEsId") or email.get("id") or "").strip()
    profile = dict((creator_profiles_by_id or {}).get(blogger_id) or {})
    for key in (
        "bloggerId", "nickname", "bloggerName", "channelName", "platform", "country", "language", "category", "contentStyle",
        "tagList", "recentTopics", "followers", "fansNum", "avgViews", "matchTier", "matchScore",
    ):
        if email.get(key) not in (None, "", []):
            profile.setdefault(key, email.get(key))
    if blogger_id and not profile.get("bloggerId"):
        profile["bloggerId"] = blogger_id
    return profile


def audit_email_against_creator_profile(
    email: dict[str, Any],
    *,
    expected_language: str = "en",
    creator_profile: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    send_guard = normalize_email_artifact_for_send(email, expected_language=expected_language)
    text = _collect_text(email)
    profile = dict(creator_profile or {})
    errors = list(send_guard.get("errors") or [])
    warnings = list(send_guard.get("warnings") or [])
    checks: list[dict[str, Any]] = []

    if not profile:
        return {
            "ok": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "checks": checks,
            "profileSnapshot": {},
            "normalizedEmail": send_guard,
        }

    platform = _canonical_key(profile.get("platform"), _PLATFORM_PATTERNS)
    country = _canonical_key(profile.get("country"), _COUNTRY_PATTERNS)
    language = _canonical_key(profile.get("language"), _LANGUAGE_PATTERNS)
    profile_topics = _profile_topics(profile)

    mentioned_platforms = _extract_mentions(text, _PLATFORM_PATTERNS)
    if platform and mentioned_platforms and platform not in mentioned_platforms:
        errors.append("platform_profile_conflict")
        checks.append({"type": "platform", "expected": platform, "mentioned": sorted(mentioned_platforms)})

    audience_descriptors = _extract_audience_descriptors(text)
    mentioned_countries = _extract_mentions(text, _COUNTRY_PATTERNS)
    if country and mentioned_countries and country not in mentioned_countries:
        errors.append("audience_country_profile_conflict")
        checks.append({"type": "country", "expected": country, "mentioned": sorted(mentioned_countries), "audienceDescriptors": sorted(audience_descriptors)})

    mentioned_languages = _extract_mentions(text, _LANGUAGE_PATTERNS)
    if language and mentioned_languages and language not in mentioned_languages:
        errors.append("audience_language_profile_conflict")
        checks.append({"type": "language", "expected": language, "mentioned": sorted(mentioned_languages), "audienceDescriptors": sorted(audience_descriptors)})

    mentioned_categories = _extract_mentions(text, _CATEGORY_PATTERNS)
    if mentioned_categories:
        matched_profile_categories = _extract_mentions(profile_topics, _CATEGORY_PATTERNS)
        if matched_profile_categories and mentioned_categories.isdisjoint(matched_profile_categories):
            warnings.append("audience_category_profile_conflict")
            checks.append({"type": "category", "expected": sorted(matched_profile_categories), "mentioned": sorted(mentioned_categories), "audienceDescriptors": sorted(audience_descriptors)})

    return {
        "ok": len(errors) == 0,
        "errors": list(dict.fromkeys(errors)),
        "warnings": list(dict.fromkeys(warnings)),
        "checks": checks,
        "profileSnapshot": {
            "bloggerId": profile.get("bloggerId"),
            "nickname": profile.get("nickname") or profile.get("bloggerName") or profile.get("channelName"),
            "platform": profile.get("platform"),
            "country": profile.get("country"),
            "language": profile.get("language"),
            "category": profile.get("category"),
            "contentStyle": profile.get("contentStyle"),
            "tagList": profile.get("tagList") or [],
            "recentTopics": profile.get("recentTopics") or [],
        },
        "normalizedEmail": send_guard,
    }


def build_creator_profile_map(items: Optional[list[dict[str, Any]]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for item in (items or []):
        if not isinstance(item, dict):
            continue
        blogger_id = str(item.get("bloggerId") or item.get("besId") or item.get("bEsId") or item.get("id") or "").strip()
        if not blogger_id:
            continue
        out[blogger_id] = {
            "bloggerId": blogger_id,
            "nickname": item.get("nickname") or item.get("bloggerName") or item.get("channelName") or item.get("username"),
            "bloggerName": item.get("bloggerName") or item.get("nickname") or item.get("channelName"),
            "channelName": item.get("channelName") or item.get("nickname") or item.get("bloggerName"),
            "platform": item.get("platform"),
            "country": item.get("country"),
            "language": item.get("language") or item.get("blogLang"),
            "category": item.get("category"),
            "contentStyle": item.get("contentStyle") or item.get("category"),
            "tagList": item.get("tagList") or [],
            "recentTopics": item.get("recentTopics") or item.get("tagList") or [],
            "followers": item.get("followers") or item.get("fansNum"),
            "avgViews": item.get("avgViews") or item.get("averageViews"),
        }
    return out


def audit_email_collection(
    emails: list[dict[str, Any]],
    *,
    expected_language: str = "en",
    creator_profiles_by_id: Optional[dict[str, dict[str, Any]]] = None,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for email in emails or []:
        profile = _pick_profile(email, creator_profiles_by_id=creator_profiles_by_id)
        results.append(audit_email_against_creator_profile(email, expected_language=expected_language, creator_profile=profile))
    return results
