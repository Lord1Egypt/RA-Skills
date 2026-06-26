# Resource Hunter v2 Architecture

## Layout

- `src/resource_hunter/`: installable Python package
- `src/resource_hunter/config.py`: path and environment resolution
- `src/resource_hunter/errors.py`: shared error types
- `src/resource_hunter/intent.py`: intent parsing, alias enrichment, query graphs, source-aware budgets
- `src/resource_hunter/adapters.py`: source adapters and runtime profiles
- `src/resource_hunter/ranking.py`: ranking, validation, evidence fusion, and success-first ordering
- `src/resource_hunter/rendering.py`: text and JSON rendering exports
- `src/resource_hunter/retrieval_layers.py`: layered retrieval model and indexed discovery fallback
- `src/resource_hunter/engine.py`: main search engine
- `src/resource_hunter/precision_core.py`: compatibility implementation layer for the current v2 core
- `src/resource_hunter/video_core.py`: yt-dlp workflow and manifest handling
- `src/resource_hunter/cli.py`: unified CLI surface
- `scripts/hunt.py`: primary legacy CLI wrapper
- `scripts/pansou.py`: legacy pan wrapper
- `scripts/torrent.py`: legacy torrent wrapper
- `scripts/video.py`: legacy video wrapper

## Search flow

1. Parse query into `SearchIntent`
2. Resolve aliases for movie-like Chinese queries when applicable
3. Build a `SearchPlan`
4. Expand source-aware query graphs and budgets
5. Route to pan/torrent pipelines
6. Query registered direct sources
7. If no confident result is found, run indexed discovery fallback
8. Normalize all results into `SearchResult`
9. Deduplicate
10. Score, validate, and fuse corroborating evidence
11. Render text output or JSON
12. Cache response and source health

## Retrieval model

### Retrieval layers
- `direct-structured-pan`
  - `2fun`, `dalipan`, `hunhepan`, `pansou.vip`
- `direct-structured-torrent`
  - `nyaa`, `animetosho`, `dmhy`, `eztv`, `tpb`, `torlock`, `yts`, `1337x`
- `community-clue`
  - `tieba`
- `indexed-discovery`
  - `search-index:ddg`, `search-index:bing`, `search-index:brave`
- `authenticated-connector`
  - reserved

### Layer roles
- `direct`: sources intended to produce immediately usable or near-usable structured results
- `clue`: sources intended to produce thread-level or follow-up hints
- `discovery`: search-engine fallback used when direct retrieval does not produce confident matches
- `auth`: reserved for future authenticated connectors

## Source adapter contract

Each adapter implements:

- `search(query, intent, limit, page, http_client) -> list[SearchResult]`
- `healthcheck(http_client) -> (ok, error)`

All adapter outputs must already be normalized into the shared `SearchResult` structure.

## Important release semantics

- `AnimeTosho`, `DMHY`, and most torrent adapters produce direct magnet-ready results
- `Bing` and `Brave` are indexed-discovery fallback providers, not the same stability class as structured direct sources
- `DaliPan` is currently a **structured token-only clue source** in runtime semantics:
  - anonymous search is confirmed via the public search API
  - final anonymous detail/url resolution is still incomplete
  - runtime therefore exposes `dalipan://provider/eu-token` placeholders and marks them as clue/follow-up results rather than guaranteed final share URLs

## Cache

SQLite database stores:

- `search_cache`: short-TTL normalized responses
- `source_status`: rolling source health results and circuit-breaker input
- `video_manifest`: recent download artifacts

The circuit breaker skips sources that have failed repeatedly in the recent cooldown window.

## JSON schema

Top level search payload:

```json
{
  "query": "...",
  "intent": {},
  "plan": {},
  "results": [],
  "warnings": [],
  "source_status": [],
  "meta": {}
}
```

### Important search `meta` fields

- `query_attempts`
- `layer_attempts`
- `query_budgets`
- `source_query_plan`
- `retrieval_layers`
- `best_direct_results`
- `best_actionable_results`
- `best_clues`
- `success_estimate`
- `timings_ms`

### Search result notes

Each `SearchResult` can carry:

- `validation_status`
- `actionability`
- `validation_signals`
- `corroboration_count`
- `supporting_results`
- `raw`

The runtime uses these fields to separate:

- direct matches
- actionable but not fully direct matches
- clue-only results that still require manual follow-up

### Dalipan-specific note

Dalipan results currently preserve follow-up data in `raw`, including:

- `dalipan_id`
- `dalipan_eu`
- `filelist`
- `delivery=token_only`
- `retrieval_role=clue`
- `requires_follow_up=true`

This makes current behavior explicit to downstream consumers.

## Top level doctor payload

```json
{
  "version": "...",
  "python": "...",
  "packaging_python": "...",
  "packaging_python_source": "current",
  "packaging_python_candidates": [],
  "packaging_python_auto_selected": false,
  "stdout_encoding": "...",
  "cache_db": "...",
  "storage_root": "...",
  "project_root": "...",
  "project_root_source": "discovered",
  "binaries": {},
  "packaging": {
    "project_root": "...",
    "project_root_source": "discovered",
    "pip": true,
    "venv": true,
    "setuptools_build_meta": true,
    "wheel": true,
    "wheel_build_ready": true,
    "python_module_smoke_ready": true,
    "console_script_smoke_ready": true,
    "full_packaging_smoke_ready": true,
    "blockers": [],
    "optional_gaps": [],
    "console_script_strategy": "venv"
  },
  "recent_sources": {},
  "recent_manifests": [],
  "advice": []
}
```

## Packaging / installability notes

Packaging, report, gate, and verify flows remain part of the project and are still available, but they are not the focus of the current sync-prep wave. The current sync-prep effort is mainly about making the retrieval/runtime state, source matrix, and release limitations match reality.
