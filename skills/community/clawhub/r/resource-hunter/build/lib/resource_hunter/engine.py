from __future__ import annotations

import hashlib
import json
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from .adapters import (
    AliasResolver,
    AnimeToshoSource,
    DaliPanSource,
    DMHYSource,
    EZTVSource,
    HTTPClient,
    HunhepanSource,
    NyaaSource,
    OneThreeThreeSevenXSource,
    PansouVipSource,
    SourceAdapter,
    TorlockSource,
    TPBSource,
    TiebaSource,
    TwoFunSource,
    YTSSource,
    _profile_for,
)
from .cache import ResourceCache
from .intent import build_plan, enrich_intent_with_aliases
from .models import SearchIntent, SearchPlan, SearchResult, SourceStatus
from .ranking import (
    MATCH_BUCKET_ORDER,
    _source_is_degraded,
    classify_result,
    deduplicate_results,
    fuse_result_evidence,
    score_result,
)
from .retrieval_layers import layered_retrieval_summary, search_indexed_discovery


def _classify_failure_kind(error: str) -> str:
    lowered = (error or "").lower()
    if lowered.startswith("http 4"):
        return "http_4xx"
    if lowered.startswith("http 5"):
        return "http_5xx"
    if "invalid json" in lowered:
        return "json"
    if "unexpected pan payload shape" in lowered:
        return "shape"
    if "ssl" in lowered or "timed out" in lowered or "urlopen error" in lowered:
        return "network"
    if "circuit open" in lowered:
        return "circuit_open"
    return "unknown"


class ResourceHunterEngine:
    def __init__(self, cache: ResourceCache | None = None, http_client: HTTPClient | None = None) -> None:
        self.cache = cache or ResourceCache()
        self.http_client = http_client or HTTPClient(retries=1, default_timeout=10)
        self.alias_resolver = AliasResolver()
        self.pan_sources: list[SourceAdapter] = [TwoFunSource(), DaliPanSource(), HunhepanSource(), PansouVipSource(), TiebaSource()]
        self.torrent_sources: list[SourceAdapter] = [
            NyaaSource(),
            AnimeToshoSource(),
            DMHYSource(),
            EZTVSource(),
            TPBSource(),
            TorlockSource(),
            YTSSource(),
            OneThreeThreeSevenXSource(),
        ]

    def _resolve_aliases(self, intent: SearchIntent) -> SearchIntent:
        alias_resolution = self.alias_resolver.resolve(intent, self.cache, self.http_client)
        return enrich_intent_with_aliases(intent, alias_resolution)

    def _cache_key(self, intent: SearchIntent, plan: SearchPlan, page: int, limit: int) -> str:
        payload = json.dumps(
            {
                "schema_version": "precision_with_broad_recall_v4",
                "intent": intent.to_dict(),
                "plan": plan.to_dict(),
                "resolved_titles": intent.resolved_titles,
                "resolved_year": intent.resolved_year,
                "page": page,
                "limit": limit,
            },
            sort_keys=True,
            ensure_ascii=False,
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def _ordered_sources(self, channel: str, plan: SearchPlan) -> list[SourceAdapter]:
        if channel == "pan":
            preferred = {name: index for index, name in enumerate(plan.preferred_pan_sources)}
            catalog = self.pan_sources
        else:
            preferred = {name: index for index, name in enumerate(plan.preferred_torrent_sources)}
            catalog = self.torrent_sources
        return sorted(
            catalog,
            key=lambda item: (
                preferred.get(item.name, 999) + (100 if _source_is_degraded(self.cache, item.name) else 0),
                item.priority,
            ),
        )

    def _queries_for_source(self, source: SourceAdapter, channel: str, plan: SearchPlan) -> list[str]:
        if source.name in plan.source_query_plan:
            return list(plan.source_query_plan[source.name])
        return list(plan.pan_queries if channel == "pan" else plan.torrent_queries)

    def _query_budget_for_source(self, source: SourceAdapter, queries: list[str], *, degraded_before_search: bool, plan: SearchPlan) -> int:
        profile = _profile_for(source.name)
        explicit_budget = plan.query_budgets.get(source.name)
        if explicit_budget is not None:
            budget = explicit_budget
        elif profile.default_degraded or degraded_before_search:
            budget = 1
        else:
            budget = 2
        return max(1, min(budget, len(queries) or 1))

    def _has_confident_result(self, batch: list[SearchResult], intent: SearchIntent) -> bool:
        for result in batch:
            bucket, confidence, _, _, _ = classify_result(result, intent)
            if bucket in {"exact_title_episode", "title_family_match"} and confidence >= 0.62:
                return True
        return False

    def _search_source(
        self,
        source: SourceAdapter,
        channel: str,
        queries: list[str],
        intent: SearchIntent,
        page: int,
        limit: int,
        plan: SearchPlan,
    ) -> tuple[SourceStatus, list[SearchResult], list[dict[str, Any]]]:
        profile = _profile_for(source.name)
        degraded_before_search = _source_is_degraded(self.cache, source.name)
        attempt_log: list[dict[str, Any]] = []
        if self.cache.should_skip_source(source.name, profile.cooldown_seconds, profile.failure_threshold):
            status = SourceStatus(
                source=source.name,
                channel=channel,
                priority=source.priority,
                ok=False,
                skipped=True,
                degraded=degraded_before_search or profile.default_degraded,
                error="circuit open from recent failures",
                failure_kind="circuit_open",
            )
            self.cache.record_source_status(status)
            return status, [], attempt_log

        source_results: list[SearchResult] = []
        status = SourceStatus(
            source=source.name,
            channel=channel,
            priority=source.priority,
            ok=True,
            degraded=degraded_before_search,
        )
        client = HTTPClient(retries=profile.retries, default_timeout=profile.timeout)
        query_budget = self._query_budget_for_source(source, queries, degraded_before_search=degraded_before_search, plan=plan)
        last_batch_had_results = False
        for query in queries[:query_budget]:
            if not query:
                continue
            started = time.time()
            try:
                batch = source.search(query, intent, limit, page, client)
                latency_ms = int((time.time() - started) * 1000)
                status.latency_ms = latency_ms
                status.ok = True
                status.error = ""
                status.failure_kind = ""
                batch_count = len(batch)
                batch_confident = self._has_confident_result(batch, intent) if batch else False
                attempt_log.append(
                    {
                        "source": source.name,
                        "channel": channel,
                        "query": query,
                        "latency_ms": latency_ms,
                        "ok": True,
                        "result_count": batch_count,
                        "confident_result": batch_confident,
                    }
                )
                if batch:
                    status.degraded = degraded_before_search
                    source_results.extend(batch)
                    last_batch_had_results = True
                    if batch_confident:
                        break
                    continue
            except Exception as exc:
                status.ok = False
                latency_ms = int((time.time() - started) * 1000)
                status.latency_ms = latency_ms
                status.error = str(exc)[:200]
                status.failure_kind = getattr(exc, "failure_kind", _classify_failure_kind(status.error))
                status.degraded = profile.default_degraded or degraded_before_search
                attempt_log.append(
                    {
                        "source": source.name,
                        "channel": channel,
                        "query": query,
                        "latency_ms": latency_ms,
                        "ok": False,
                        "error": status.error,
                        "failure_kind": status.failure_kind,
                    }
                )
        if source_results and not status.ok and last_batch_had_results:
            status.ok = True
            status.error = ""
            status.failure_kind = ""
        self.cache.record_source_status(status)
        return status, source_results, attempt_log

    def _run_indexed_discovery(self, intent: SearchIntent) -> tuple[list[SearchResult], list[dict[str, Any]]]:
        started = time.time()
        try:
            results = search_indexed_discovery(intent, self.http_client, max_results=8)
            return results, [
                {
                    "layer": "indexed-discovery",
                    "ok": True,
                    "latency_ms": int((time.time() - started) * 1000),
                    "result_count": len(results),
                }
            ]
        except Exception as exc:
            return [], [
                {
                    "layer": "indexed-discovery",
                    "ok": False,
                    "latency_ms": int((time.time() - started) * 1000),
                    "error": str(exc)[:200],
                }
            ]

    def search(
        self,
        intent: SearchIntent,
        plan: SearchPlan | None = None,
        page: int = 1,
        limit: int = 8,
        use_cache: bool = True,
    ) -> dict[str, Any]:
        request_started = time.perf_counter()
        request_id = uuid.uuid4().hex[:12]
        alias_started = time.perf_counter()
        intent = self._resolve_aliases(intent)
        alias_ms = int((time.perf_counter() - alias_started) * 1000)
        plan_started = time.perf_counter()
        plan = plan or build_plan(intent)
        plan_ms = int((time.perf_counter() - plan_started) * 1000)
        cache_key = self._cache_key(intent, plan, page, limit)
        if use_cache:
            cached = self.cache.get_search_cache(cache_key)
            if cached:
                cached.setdefault("meta", {})
                cached["meta"]["cached"] = True
                cached["meta"]["request_id"] = request_id
                cached["meta"].setdefault("timings_ms", {})
                return cached

        results: list[SearchResult] = []
        statuses: list[SourceStatus] = []
        warnings: list[str] = []
        query_attempts: list[dict[str, Any]] = []
        retrieval_layers_used = layered_retrieval_summary()
        layer_attempts: list[dict[str, Any]] = []

        fetch_started = time.perf_counter()
        for channel in plan.channels:
            ordered_sources = self._ordered_sources(channel, plan)
            with ThreadPoolExecutor(max_workers=min(4, len(ordered_sources) or 1)) as executor:
                futures = [
                    executor.submit(
                        self._search_source,
                        source,
                        channel,
                        self._queries_for_source(source, channel, plan),
                        intent,
                        page,
                        limit,
                        plan,
                    )
                    for source in ordered_sources
                ]
                for future in as_completed(futures):
                    status, source_results, attempts = future.result()
                    statuses.append(status)
                    results.extend(source_results)
                    query_attempts.extend(attempts)

        if not self._has_confident_result(results, intent):
            discovery_results, discovery_attempts = self._run_indexed_discovery(intent)
            results.extend(discovery_results)
            layer_attempts.extend(discovery_attempts)
        fetch_ms = int((time.perf_counter() - fetch_started) * 1000)

        rank_started = time.perf_counter()
        results = deduplicate_results(results)
        results = [score_result(result, intent, cache=self.cache) for result in results]
        results = fuse_result_evidence(results)
        results.sort(
            key=lambda item: (
                item.actionability != "direct",
                item.actionability == "clue",
                item.validation_status != "validated",
                MATCH_BUCKET_ORDER.get(item.match_bucket, 9),
                -item.corroboration_count,
                -item.score,
                -item.seeders,
                item.source_degraded,
                item.title.lower(),
            )
        )
        statuses.sort(key=lambda item: (item.channel, item.priority, item.source))
        rank_ms = int((time.perf_counter() - rank_started) * 1000)

        if not results:
            warnings.append("no results returned from active sources")

        best_direct_results = [result.to_public_dict() for result in results if result.actionability == "direct"][:3]
        best_actionable_results = [
            result.to_public_dict() for result in results if result.actionability in {"direct", "actionable"}
        ][:5]
        best_clues = [result.to_public_dict() for result in results if result.actionability == "clue"][:5]

        response = {
            "query": intent.original_query,
            "intent": intent.to_dict(),
            "plan": plan.to_dict(),
            "results": [result.to_public_dict() for result in results],
            "warnings": warnings,
            "source_status": [status.to_dict() for status in statuses],
            "meta": {
                "cached": False,
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "limit": limit,
                "page": page,
                "candidate_count": len(results),
                "effective_limit": limit,
                "alias_resolution": intent.alias_resolution,
                "resolved_titles": intent.resolved_titles,
                "resolved_year": intent.resolved_year or intent.year,
                "request_id": request_id,
                "query_attempts": query_attempts,
                "layer_attempts": layer_attempts,
                "query_budgets": dict(plan.query_budgets),
                "source_query_plan": dict(plan.source_query_plan),
                "retrieval_layers": retrieval_layers_used,
                "best_direct_results": best_direct_results,
                "best_actionable_results": best_actionable_results,
                "best_clues": best_clues,
                "success_estimate": {
                    "has_direct": bool(best_direct_results),
                    "has_actionable": bool(best_actionable_results),
                    "has_clues": bool(best_clues),
                },
                "timings_ms": {
                    "alias": alias_ms,
                    "plan": plan_ms,
                    "fetch": fetch_ms,
                    "rank": rank_ms,
                    "total": int((time.perf_counter() - request_started) * 1000),
                },
            },
        }
        if use_cache:
            self.cache.set_search_cache(cache_key, response, ttl_seconds=300)
        return response

    def source_catalog(self, probe: bool = False) -> dict[str, Any]:
        sources: list[dict[str, Any]] = []
        cached_status = {row["source"]: row for row in self.cache.list_source_statuses()}
        all_sources = self.pan_sources + self.torrent_sources
        for adapter in sorted(all_sources, key=lambda item: (item.channel, item.priority, item.name)):
            status_info = cached_status.get(adapter.name, {})
            if probe:
                profile = _profile_for(adapter.name)
                started = time.time()
                ok, error = adapter.healthcheck(HTTPClient(retries=profile.retries, default_timeout=profile.timeout))
                status = SourceStatus(
                    source=adapter.name,
                    channel=adapter.channel,
                    priority=adapter.priority,
                    ok=ok,
                    degraded=False if ok else profile.default_degraded,
                    error=error,
                    failure_kind="probe_ok" if ok else _classify_failure_kind(error),
                    latency_ms=int((time.time() - started) * 1000),
                )
                self.cache.record_source_status(status)
                status_info = status.to_dict()
            sources.append(
                {
                    "source": adapter.name,
                    "channel": adapter.channel,
                    "priority": adapter.priority,
                    "recent_status": {
                        "ok": bool(status_info.get("ok")) if status_info else None,
                        "skipped": bool(status_info.get("skipped")) if status_info else False,
                        "degraded": bool(status_info.get("degraded")) if status_info else _source_is_degraded(self.cache, adapter.name),
                        "latency_ms": status_info.get("latency_ms"),
                        "error": status_info.get("error", ""),
                        "failure_kind": status_info.get("failure_kind", ""),
                        "checked_at": status_info.get("checked_at"),
                    },
                }
            )
        return {
            "sources": sources,
            "meta": {
                "probe": probe,
                "retrieval_layers": layered_retrieval_summary(),
            },
        }


__all__ = ["ResourceHunterEngine"]
