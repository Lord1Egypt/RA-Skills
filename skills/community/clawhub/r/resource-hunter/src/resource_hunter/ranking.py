from __future__ import annotations

import hashlib
import re
import time
from typing import Any

from .adapters import SOURCE_RUNTIME_PROFILES, SourceRuntimeProfile
from .cache import ResourceCache
from .common import (
    extract_year,
    normalize_key,
    parse_quality_tags,
    quality_display_from_tags,
    source_priority,
    title_core,
    title_tokens,
    token_overlap_score,
    unique_preserve,
)
from .models import SearchIntent, SearchResult

PAN_PROVIDER_SCORE = {
    "aliyun": 12,
    "quark": 11,
    "115": 10,
    "pikpak": 9,
    "uc": 8,
    "baidu": 7,
    "123": 6,
    "xunlei": 5,
    "tianyi": 4,
    "other": 1,
}

MATCH_BUCKET_ORDER = {
    "exact_title_episode": 0,
    "title_family_match": 1,
    "episode_only_match": 2,
    "weak_context_match": 3,
}

BUCKET_LABELS = {
    "exact_title_episode": "Top matches",
    "title_family_match": "Related matches",
    "episode_only_match": "Loose matches",
    "weak_context_match": "Loose matches",
}

RESULT_YEAR_RE = re.compile(r"\b(?:19|20)\d{2}\b")


def _profile_for(source_name: str) -> SourceRuntimeProfile:
    return SOURCE_RUNTIME_PROFILES.get(
        source_name,
        SourceRuntimeProfile(timeout=10, retries=1, degraded_score_penalty=0, cooldown_seconds=180, failure_threshold=2),
    )


def _target_title_cores(intent: SearchIntent) -> list[str]:
    cores = [
        intent.title_core,
        intent.english_title_core,
        intent.chinese_title_core,
    ]
    cores.extend([title_core(item) or item for item in intent.resolved_titles])
    return unique_preserve([core for core in cores if core])


def _result_title_signals(intent: SearchIntent, title: str) -> dict[str, Any]:
    title_core_value = title_core(title)
    title_tokens_value = title_tokens(title_core_value or title)
    target_cores = _target_title_cores(intent)
    target_token_sets = [title_tokens(core) for core in target_cores]
    target_core_keys = [normalize_key(core) for core in target_cores if normalize_key(core)]
    title_core_key = normalize_key(title_core_value or title)
    query_overlap = max((token_overlap_score(title_tokens(core), title_tokens_value) for core in target_cores), default=0.0)
    overlap = query_overlap
    exact_core_match = bool(title_core_key and title_core_key in target_core_keys)
    alias_match = bool(title_core_key and not exact_core_match and overlap >= 0.82)
    starts_with_target = any(tokens and title_tokens_value[: len(tokens)] == tokens for tokens in target_token_sets)
    season_match = bool(
        intent.season is None
        or re.search(rf"s0?{intent.season}(?:e|\b)", title, re.I)
        or re.search(rf"season\s*0?{intent.season}\b", title, re.I)
        or re.search(rf"\u7b2c\s*0?{intent.season}\s*\u5b63", title)
    )
    episode_match = bool(
        intent.episode is None
        or re.search(rf"(?:e|x)0?{intent.episode}\b", title, re.I)
        or re.search(rf"episode\s*0?{intent.episode}\b", title, re.I)
        or re.search(rf"\u7b2c\s*0?{intent.episode}\s*\u96c6", title)
    )
    year_match = bool(intent.year and extract_year(title) == intent.year)
    result_years = unique_preserve(RESULT_YEAR_RE.findall(title or ""))
    year_conflict = bool(intent.year and result_years and intent.year not in result_years)
    year_missing = bool(intent.year and not result_years)

    title_only_mentions_target = not starts_with_target and overlap >= 0.35 and not exact_core_match
    return {
        "title_core": title_core_value,
        "title_tokens": title_tokens_value,
        "overlap": overlap,
        "exact_core_match": exact_core_match,
        "alias_match": alias_match,
        "season_match": season_match,
        "episode_match": episode_match,
        "year_match": year_match,
        "target_cores": target_cores,
        "result_years": result_years,
        "year_conflict": year_conflict,
        "year_missing": year_missing,
        "starts_with_target": starts_with_target,
        "title_only_mentions_target": title_only_mentions_target,
    }


def classify_result(result: SearchResult, intent: SearchIntent) -> tuple[str, float, list[str], list[str], dict[str, Any]]:
    signals = _result_title_signals(intent, result.title)
    reasons: list[str] = []
    penalties: list[str] = []

    if signals["exact_core_match"]:
        reasons.append("canonical title match")
    elif signals["alias_match"]:
        reasons.append("alias match")
    elif signals["overlap"] >= 0.8:
        reasons.append("strong title-family match")
    elif signals["overlap"] >= 0.45:
        reasons.append("partial title-family match")
    elif signals["overlap"] > 0:
        reasons.append("weak context match")

    if signals["year_match"]:
        reasons.append("year match")
    if intent.season is not None and signals["season_match"]:
        reasons.append("season match")
    if intent.episode is not None and signals["episode_match"]:
        reasons.append("episode match")
    if signals["year_conflict"]:
        penalties.append(f"year mismatch: expected {intent.year}, got {', '.join(signals['result_years'])}")

    if intent.kind in {"tv", "anime"} and (intent.season is not None or intent.episode is not None):
        if (signals["exact_core_match"] or (signals["starts_with_target"] and signals["overlap"] >= 0.55) or signals["overlap"] >= 0.94) and signals["episode_match"] and signals["season_match"]:
            return "exact_title_episode", 0.96, reasons, penalties, signals
        if signals["exact_core_match"] or signals["alias_match"] or signals["overlap"] >= 0.45:
            return "title_family_match", 0.78 if signals["overlap"] >= 0.6 else 0.62, reasons, penalties, signals
        if signals["episode_match"] or signals["season_match"]:
            penalties.append("episode without title-family match")
            return "episode_only_match", 0.28, reasons, penalties, signals
        penalties.append("weak context only")
        return "weak_context_match", 0.12, reasons, penalties, signals

    if signals["exact_core_match"] or signals["alias_match"] or signals["overlap"] >= 0.78:
        return "title_family_match", 0.9 if signals["exact_core_match"] else 0.74, reasons, penalties, signals
    if signals["overlap"] >= 0.35:
        return "title_family_match", 0.52, reasons, penalties, signals
    penalties.append("weak context only")
    return "weak_context_match", 0.14, reasons, penalties, signals


def _source_is_degraded(cache: ResourceCache, source_name: str) -> bool:
    profile = _profile_for(source_name)
    if not profile.default_degraded:
        latest = cache.latest_source_status(source_name)
        return bool(latest and latest.get("degraded"))
    latest = cache.latest_source_status(source_name)
    if latest and latest.get("ok") and latest.get("failure_kind") == "probe_ok":
        return False
    last_failure = cache.latest_failure_epoch(source_name, within_seconds=900)
    recovery_since = last_failure if last_failure is not None else (time.time() - 900)
    if cache.count_real_successes_since(source_name, recovery_since, within_seconds=900) >= 2:
        return False
    return True


def validate_result(result: SearchResult, intent: SearchIntent) -> SearchResult:
    validation_signals: list[str] = []
    status = "speculative"
    actionability = "speculative"
    score_bonus = 0
    signals = _result_title_signals(intent, result.title)

    if signals["year_conflict"]:
        status = "conflict"
        actionability = "speculative"
        validation_signals.append(
            f"year mismatch: expected {intent.year}, got {', '.join(signals['result_years'])}"
        )
        score_bonus -= 40
    elif signals["year_missing"]:
        validation_signals.append("query year not confirmed in result title")
        score_bonus -= 4

    if result.match_bucket == "exact_title_episode":
        if status != "conflict":
            status = "validated"
            actionability = "direct"
            validation_signals.append("exact title/episode alignment")
            score_bonus += 14
    elif result.match_bucket == "title_family_match":
        if status != "conflict":
            status = "validated"
            actionability = "direct"
            validation_signals.append("title-family alignment")
            score_bonus += 8
    elif result.match_bucket == "episode_only_match":
        if status != "conflict":
            status = "partial"
            actionability = "actionable"
            validation_signals.append("episode alignment without full title-family confidence")
    elif status != "conflict":
        validation_signals.append("weak context only")

    if status == "conflict":
        result.penalties.append("year-conflict validation downgrade")
    elif signals["year_missing"] and status == "validated":
        status = "partial"
        actionability = "actionable"
        validation_signals.append("year missing: downgraded from direct to actionable")

    if result.raw.get("manual_follow_up"):
        status = "clue"
        actionability = "clue"
        validation_signals.append("manual follow-up clue")
        score_bonus -= 8
    if result.raw.get("layer") == "indexed-discovery":
        validation_signals.append("indexed discovery fallback")
        actionability = "actionable" if actionability == "speculative" else actionability
        score_bonus -= 4
    if result.raw.get("retrieval_role") == "clue":
        status = "clue"
        actionability = "clue"
        validation_signals.append("clue-only retrieval role")
        score_bonus -= 6
    if result.password:
        validation_signals.append("includes extraction code")
        if actionability in {"speculative", "clue"}:
            actionability = "actionable"
        score_bonus += 3
    if result.source == "search-index":
        validation_signals.append("search-index result")
        score_bonus -= 3
    if result.source == "dalipan" and result.raw.get("delivery") == "token_only":
        status = "clue"
        actionability = "clue"
        validation_signals.append("dalipan token-only result")
        score_bonus -= 10
    if result.provider in {"tieba_thread", "baidu_clue"}:
        validation_signals.append("community thread clue")
        if status == "validated":
            status = "clue"
        if actionability == "direct":
            actionability = "clue"
        score_bonus -= 5

    title_conflict = result.raw.get("retrieval_role") == "clue" or result.raw.get("manual_follow_up")
    if title_conflict:
        result.penalties.append("clue result requires follow-up")
    if result.match_bucket == "weak_context_match" and result.source not in {"search-index", "tieba"}:
        result.penalties.append("result lacks sufficient alignment")
        score_bonus -= 8
    if result.match_bucket == "title_family_match" and result.provider == "other":
        validation_signals.append("provider unresolved")
        score_bonus -= 4

    result.validation_status = status
    result.actionability = actionability
    result.validation_signals = unique_preserve(validation_signals)
    result.score += score_bonus
    return result


def _result_cluster_key(result: SearchResult) -> str:
    if result.channel == "pan":
        if result.share_id_or_info_hash:
            return f"pan:{result.provider}:{result.share_id_or_info_hash}"
    else:
        if result.share_id_or_info_hash:
            return f"torrent:{result.share_id_or_info_hash}"
    return f"title:{normalize_key(result.title)}"


def fuse_result_evidence(results: list[SearchResult]) -> list[SearchResult]:
    if not results:
        return []
    clusters: dict[str, list[SearchResult]] = {}
    for result in results:
        cluster_key = _result_cluster_key(result)
        clusters.setdefault(cluster_key, []).append(result)

    fused: list[SearchResult] = []
    for cluster_key, cluster_results in clusters.items():
        source_names = unique_preserve([item.source for item in cluster_results if item.source])
        corroboration_count = max(0, len(source_names) - 1)
        support_payload = []
        for item in cluster_results:
            support_payload.append(
                {
                    "source": item.source,
                    "provider": item.provider,
                    "title": item.title,
                    "actionability": item.actionability,
                    "validation_status": item.validation_status,
                    "score": item.score,
                }
            )
        primary = max(
            cluster_results,
            key=lambda item: (
                item.actionability == "direct",
                item.actionability == "actionable",
                item.validation_status == "validated",
                item.score,
                bool(item.password),
                item.seeders,
            ),
        )
        primary.cluster_id = hashlib.sha256(cluster_key.encode("utf-8")).hexdigest()[:12]
        primary.evidence_count = len(cluster_results)
        primary.corroboration_count = corroboration_count
        primary.corroborated_sources = source_names
        primary.supporting_results = support_payload
        if corroboration_count:
            primary.reasons.append(f"corroborated by {len(source_names)} sources")
            primary.score += min(18, 6 * corroboration_count)
            if primary.actionability == "speculative":
                primary.actionability = "actionable"
        fused.append(primary)
    return fused


def score_result(result: SearchResult, intent: SearchIntent, cache: ResourceCache | None = None) -> SearchResult:
    bucket, confidence, reasons, penalties, signals = classify_result(result, intent)
    result.match_bucket = bucket
    result.confidence = round(confidence, 3)
    result.reasons = unique_preserve(reasons)
    result.penalties = unique_preserve(penalties)

    tags = result.quality_tags or parse_quality_tags(result.title)
    result.quality_tags = tags
    result.quality = quality_display_from_tags(tags)

    score = {
        "exact_title_episode": 145,
        "title_family_match": 95,
        "episode_only_match": 20,
        "weak_context_match": -5,
    }[bucket]

    if signals["exact_core_match"]:
        score += 28
    if signals["alias_match"]:
        score += 16
    score += int(signals["overlap"] * 30)
    if signals["year_match"]:
        score += 10
    if intent.season is not None and signals["season_match"]:
        score += 8
    if intent.episode is not None and signals["episode_match"]:
        score += 12
    if signals["year_conflict"]:
        score -= 90
        result.penalties.append(f"year mismatch: expected {intent.year}, got {', '.join(signals['result_years'])}")
    elif signals["year_missing"]:
        score -= 8

    resolution = tags.get("resolution")
    if resolution == "2160p":
        score += 18
        result.reasons.append("4k resolution")
    elif resolution == "1080p":
        score += 10
        result.reasons.append("1080p resolution")
    elif resolution == "720p":
        score += 4
        result.reasons.append("720p resolution")

    source_type = tags.get("source")
    if source_type == "bluray":
        score += 8
        result.reasons.append("bluray source")
    elif source_type == "web-dl":
        score += 5
        result.reasons.append("web-dl source")
    elif source_type in {"webrip", "hdtv"}:
        score += 2
        result.reasons.append(f"{source_type} source")
    elif source_type == "cam":
        score -= 30
        result.penalties.append("cam-quality release")

    if tags.get("pack") == "remux":
        score += 4
        result.reasons.append("remux pack")
    if tags.get("hdr_flags"):
        score += min(8, 4 * len(tags["hdr_flags"]))
        result.reasons.append("hdr flags")
    if intent.wants_sub and tags.get("subtitle"):
        score += 12
        result.reasons.append("subtitle requested")
    if intent.wants_4k and resolution == "2160p":
        score += 20
        result.reasons.append("4k requested")

    if result.channel == "pan":
        score += PAN_PROVIDER_SCORE.get(result.provider, PAN_PROVIDER_SCORE["other"])
        if result.password:
            score += 6
            result.reasons.append("has extraction code")
    if result.channel == "torrent" and result.seeders:
        score += min(result.seeders, 240) // 6
        result.reasons.append("seeders")

    score += max(0, 12 - source_priority(result.source))
    result.reasons.append(f"source priority {source_priority(result.source)}")

    if bucket == "episode_only_match":
        score -= 55
        result.penalties.append("episode-only match penalty")
    elif bucket == "weak_context_match":
        score -= 30
        result.penalties.append("weak-context penalty")

    if cache and _source_is_degraded(cache, result.source):
        penalty = _profile_for(result.source).degraded_score_penalty
        if penalty:
            score -= penalty
            result.source_degraded = True
            result.penalties.append(f"degraded source penalty ({penalty})")

    result.score = score
    result.reasons = unique_preserve(result.reasons)
    result.penalties = unique_preserve(result.penalties)
    result = validate_result(result, intent)
    return result


def deduplicate_results(results: list[SearchResult]) -> list[SearchResult]:
    chosen: dict[str, SearchResult] = {}
    for result in results:
        if result.channel == "pan":
            key = f"pan:{result.provider}:{result.share_id_or_info_hash}"
        else:
            fallback = result.share_id_or_info_hash or normalize_key(result.title)[:64]
            key = f"torrent:{fallback}"
        current = chosen.get(key)
        if not current:
            chosen[key] = result
            continue
        if result.password and not current.password:
            chosen[key] = result
            continue
        if result.seeders > current.seeders:
            chosen[key] = result
    return list(chosen.values())


__all__ = [
    "BUCKET_LABELS",
    "MATCH_BUCKET_ORDER",
    "PAN_PROVIDER_SCORE",
    "classify_result",
    "deduplicate_results",
    "fuse_result_evidence",
    "score_result",
    "validate_result",
    "_source_is_degraded",
]
