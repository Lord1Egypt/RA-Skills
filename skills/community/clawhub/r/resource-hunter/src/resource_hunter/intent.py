from __future__ import annotations

from dataclasses import replace
from typing import Any

from .common import (
    compact_spaces,
    detect_kind,
    extract_chinese_alias,
    extract_english_alias,
    extract_season_episode,
    extract_year,
    is_video_url,
    title_core,
    title_tokens,
    unique_preserve,
)
from .models import QueryPlanEntry, SearchIntent, SearchPlan


_SOURCE_FAMILIES: dict[str, list[str]] = {
    "pan": ["2fun", "dalipan", "hunhepan", "pansou.vip", "tieba"],
    "torrent": ["nyaa", "animetosho", "dmhy", "eztv", "tpb", "torlock", "yts", "1337x"],
}


def _as_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item or "").strip()]


def _build_query_entries(
    *,
    channel: str,
    intent: SearchIntent,
    base_queries: list[tuple[str, str, float]],
) -> list[QueryPlanEntry]:
    entries: list[QueryPlanEntry] = []
    for query, stage, confidence in base_queries:
        normalized_query = compact_spaces(query)
        if not normalized_query:
            continue
        reasons = [f"{channel}:{stage}"]
        sources = list(_SOURCE_FAMILIES.get(channel, []))
        if channel == "torrent":
            if intent.kind == "anime":
                if stage == "strict":
                    sources = ["nyaa", "animetosho", "dmhy", "tpb", "torlock", "1337x"]
                elif stage == "alias":
                    sources = ["nyaa", "animetosho", "dmhy", "1337x", "tpb", "torlock"]
                else:
                    sources = ["animetosho", "dmhy", "torlock", "tpb", "1337x", "nyaa"]
            elif intent.kind == "tv":
                if stage == "strict":
                    sources = ["eztv", "tpb", "torlock", "1337x", "animetosho"]
                elif stage == "alias":
                    sources = ["eztv", "tpb", "torlock", "1337x", "animetosho"]
                else:
                    sources = ["tpb", "torlock", "1337x", "eztv", "nyaa"]
            elif intent.kind == "movie":
                if stage == "strict":
                    sources = ["yts", "tpb", "torlock", "1337x"]
                elif stage == "alias":
                    sources = ["yts", "tpb", "torlock", "1337x"]
                else:
                    sources = ["tpb", "torlock", "1337x", "yts", "eztv"]
        else:
            if stage == "strict":
                sources = ["2fun", "dalipan", "hunhepan", "pansou.vip"]
            elif stage == "alias":
                sources = ["2fun", "dalipan", "hunhepan", "pansou.vip", "tieba"]
            else:
                sources = ["tieba", "dalipan", "2fun", "hunhepan", "pansou.vip"]
        entries.append(
            QueryPlanEntry(
                query=normalized_query,
                stage=stage,
                reasons=reasons,
                sources=sources,
                confidence=confidence,
            )
        )
    deduped: list[QueryPlanEntry] = []
    seen_queries: set[str] = set()
    for entry in entries:
        key = entry.query.lower()
        if key in seen_queries:
            continue
        seen_queries.add(key)
        deduped.append(entry)
    return deduped


def _build_source_query_plan(entries: list[QueryPlanEntry], preferred_sources: list[str]) -> dict[str, list[str]]:
    ordered_sources = preferred_sources + [source for source in _SOURCE_FAMILIES.get("pan", []) + _SOURCE_FAMILIES.get("torrent", []) if source not in preferred_sources]
    plan: dict[str, list[str]] = {source: [] for source in ordered_sources}
    for entry in entries:
        for source in entry.sources:
            plan.setdefault(source, [])
            if entry.query not in plan[source]:
                plan[source].append(entry.query)
    return {source: queries for source, queries in plan.items() if queries}


def _build_query_budgets(entries: list[QueryPlanEntry], *, preferred_sources: list[str], kind: str, channel: str) -> dict[str, int]:
    budgets: dict[str, int] = {}
    strict_count = sum(1 for entry in entries if entry.stage == "strict")
    alias_count = sum(1 for entry in entries if entry.stage == "alias")
    salvage_count = sum(1 for entry in entries if entry.stage == "salvage")
    for source in preferred_sources:
        budget = 2
        if channel == "torrent" and kind in {"anime", "tv", "movie"} and source in {"nyaa", "animetosho", "dmhy", "eztv", "yts"}:
            budget = 3
        if source in {"tieba", "pansou.vip", "hunhepan", "1337x", "torlock", "dalipan"}:
            budget = 2 if salvage_count else 1
        budgets[source] = max(1, min(budget, strict_count + alias_count + salvage_count or 1))
    return budgets


def parse_intent(
    query: str,
    explicit_kind: str | None = None,
    channel: str = "both",
    quick: bool = False,
    wants_sub: bool = False,
    wants_4k: bool = False,
) -> SearchIntent:
    season, episode = extract_season_episode(query)
    english_alias = extract_english_alias(query)
    chinese_alias = extract_chinese_alias(query)
    kind = detect_kind(query, explicit_kind)
    query_title_core = title_core(query) or title_core(english_alias) or title_core(chinese_alias)
    return SearchIntent(
        query=compact_spaces(query),
        original_query=query,
        kind=kind,
        channel=channel,
        english_alias=english_alias,
        chinese_alias=chinese_alias,
        year=extract_year(query),
        season=season,
        episode=episode,
        wants_sub=wants_sub,
        wants_4k=wants_4k,
        quick=quick,
        is_video_url=is_video_url(query),
        title_core=query_title_core,
        title_tokens=title_tokens(query_title_core or query),
        english_title_core=title_core(english_alias),
        chinese_title_core=title_core(chinese_alias),
        resolved_titles=[],
        resolved_year="",
        alias_resolution={},
    )


def enrich_intent_with_aliases(intent: SearchIntent, alias_resolution: dict[str, Any]) -> SearchIntent:
    if not alias_resolution:
        return intent
    resolved_titles = unique_preserve(
        [
            str(alias_resolution.get("english_title", "") or ""),
            str(alias_resolution.get("romanized_title", "") or ""),
            *_as_string_list(alias_resolution.get("alternate_titles")),
        ]
    )
    english_alias = intent.english_alias or str(alias_resolution.get("english_title", "") or "")
    resolved_year = str(alias_resolution.get("resolved_year") or intent.year)
    return replace(
        intent,
        kind="movie" if intent.kind == "general" else intent.kind,
        english_alias=english_alias,
        english_title_core=title_core(english_alias),
        resolved_titles=resolved_titles,
        resolved_year=resolved_year,
        alias_resolution=dict(alias_resolution),
    )


def build_plan(intent: SearchIntent) -> SearchPlan:
    if intent.is_video_url:
        return SearchPlan(channels=["video"], notes=["url routed to video pipeline"])

    if intent.channel == "pan":
        channels = ["pan"]
    elif intent.channel == "torrent":
        channels = ["torrent"]
    elif intent.kind in {"anime", "tv"}:
        channels = ["torrent", "pan"]
    else:
        channels = ["pan", "torrent"]

    title_variant = intent.title_core
    english_variant = intent.english_title_core or intent.english_alias
    chinese_variant = intent.chinese_title_core or intent.chinese_alias
    resolved_variants = unique_preserve(
        [*intent.resolved_titles, *[title_core(item) or item for item in intent.resolved_titles]]
    )

    pan_bases: list[tuple[str, str, float]] = [
        (intent.query, "strict", 1.0),
        (title_variant, "strict", 0.98),
        (chinese_variant, "strict", 0.95),
        (english_variant, "alias", 0.9),
        *((variant, "alias", 0.85) for variant in resolved_variants),
    ]
    if intent.year and english_variant:
        pan_bases.append((f"{english_variant} {intent.year}", "alias", 0.92))
    for variant in resolved_variants:
        if intent.year:
            pan_bases.append((f"{variant} {intent.resolved_year or intent.year}", "alias", 0.88))
    if intent.wants_sub:
        pan_bases.extend(
            [
                (f"{title_variant or intent.query} subtitles", "salvage", 0.68),
                (f"{chinese_variant or intent.query} 中文字幕", "salvage", 0.72),
            ]
        )
    if intent.wants_4k:
        pan_bases.extend(
            [
                (f"{title_variant or intent.query} 4K", "salvage", 0.74),
                (f"{title_variant or intent.query} 2160p", "salvage", 0.76),
            ]
        )
    if intent.kind == "music" and "无损" not in intent.query:
        pan_bases.append((f"{intent.query} 无损", "salvage", 0.7))

    torrent_bases: list[tuple[str, str, float]] = [
        (intent.query, "strict", 1.0),
        (english_variant or intent.query, "strict", 0.98),
        (title_variant, "strict", 0.97),
        (english_variant, "alias", 0.92),
        *((variant, "alias", 0.86) for variant in resolved_variants),
    ]
    if intent.year and title_variant:
        torrent_bases.append((f"{title_variant} {intent.year}", "strict", 0.94))
    for variant in resolved_variants:
        if intent.year:
            torrent_bases.append((f"{variant} {intent.resolved_year or intent.year}", "alias", 0.89))
    if intent.wants_4k:
        torrent_bases.append((f"{title_variant or english_variant or intent.query} 2160p", "salvage", 0.78))
    if intent.wants_sub:
        torrent_bases.append((f"{title_variant or english_variant or intent.query} subtitles", "salvage", 0.7))
    if intent.kind in {"tv", "anime"} and intent.season is not None and intent.episode is not None:
        episode_label = f"S{intent.season:02d}E{intent.episode:02d}"
        torrent_bases.append((f"{english_variant or title_variant or intent.query} {episode_label}", "strict", 0.99))
    if intent.kind == "anime" and english_variant:
        torrent_bases.append((f"{english_variant} sub", "salvage", 0.69))

    plan = SearchPlan(channels=channels, notes=[])

    if intent.kind == "anime":
        plan.preferred_pan_sources = ["dalipan", "2fun", "hunhepan", "pansou.vip", "tieba"]
        plan.preferred_torrent_sources = ["nyaa", "animetosho", "dmhy", "torlock", "tpb", "1337x", "yts", "eztv"]
        plan.notes.append("anime prefers nyaa before pan sources")
    elif intent.kind == "tv":
        plan.preferred_pan_sources = ["dalipan", "2fun", "hunhepan", "pansou.vip", "tieba"]
        plan.preferred_torrent_sources = ["eztv", "torlock", "tpb", "1337x", "nyaa", "yts"]
        plan.notes.append("tv prefers eztv/tpb before pan sources")
    elif intent.kind == "movie":
        plan.preferred_pan_sources = ["dalipan", "2fun", "hunhepan", "pansou.vip", "tieba"]
        plan.preferred_torrent_sources = ["yts", "torlock", "tpb", "1337x", "eztv", "nyaa"]
        plan.notes.append("movie prefers pan results, then yts/tpb torrents")
    else:
        plan.preferred_pan_sources = ["dalipan", "2fun", "hunhepan", "pansou.vip", "tieba"]
        plan.preferred_torrent_sources = ["tpb", "1337x", "nyaa", "eztv", "yts"]
        plan.notes.append("general/software/music/book prefer pan results first")

    if "pan" in channels:
        plan.pan_query_graph = _build_query_entries(channel="pan", intent=intent, base_queries=pan_bases)
        plan.pan_queries = [entry.query for entry in plan.pan_query_graph]
    if "torrent" in channels:
        plan.torrent_query_graph = _build_query_entries(channel="torrent", intent=intent, base_queries=torrent_bases)
        plan.torrent_queries = [entry.query for entry in plan.torrent_query_graph]

    pan_source_plan = _build_source_query_plan(plan.pan_query_graph, plan.preferred_pan_sources)
    torrent_source_plan = _build_source_query_plan(plan.torrent_query_graph, plan.preferred_torrent_sources)
    plan.source_query_plan = {**pan_source_plan, **torrent_source_plan}
    plan.query_budgets = {
        **_build_query_budgets(plan.pan_query_graph, preferred_sources=plan.preferred_pan_sources, kind=intent.kind, channel="pan"),
        **_build_query_budgets(plan.torrent_query_graph, preferred_sources=plan.preferred_torrent_sources, kind=intent.kind, channel="torrent"),
    }
    return plan


__all__ = ["build_plan", "enrich_intent_with_aliases", "parse_intent"]
