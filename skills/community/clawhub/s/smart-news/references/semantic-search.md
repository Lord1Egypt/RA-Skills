# Semantic Search Reference

This document describes the asynchronous semantic search HTTP API for AI agents and operators.

## Authentication

All semantic search endpoints require Bearer token authentication:

```
Authorization: Bearer <API_KEY>
```

Requests without a valid token receive HTTP 401.

## Overview

Unified semantic search retrieves from both News (`content_items`) and Intelligence (`raw_intelligence_items`) domains via UNION ALL over pgvector HNSW indexes (`idx_content_embedding_hnsw` and `idx_intelligence_embedding_hnsw`). Both tables use `embedding vector(1536)` columns. Each hit carries a `source_domain` discriminator; the response includes a `source_breakdown` with per-domain `matched_count` and `retained_count`.

Semantic search is asynchronous and follows the same three-step pattern as `/analyze`:

1. **Create**: `POST /semantic-search` with `hours`, `query`, and `user_id`
2. **Poll**: `GET /semantic-search/{job_id}` until the job reaches a terminal state
3. **Fetch**: `GET /semantic-search/{job_id}/result` to retrieve the final Markdown report

The POST response returns immediately. It does not include the final report.

## Request Contract

### Endpoint

```
POST /semantic-search
```

### Required Parameters

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `hours` | integer | `> 0` | Search time window in hours. Values below server minimum return HTTP 400. Values above the semantic search maximum (default 720h = 30d) are capped and the response includes a `warning` field. The semantic search hours cap is separate from the analyze cap (24h). |
| `query` | string | non-blank, max 300 chars | Natural-language topic query for semantic retrieval. |
| `user_id` | string | `^[A-Za-z0-9_-]{1,128}$` | Requesting user identifier. Server trims whitespace before validation. |

### Success Response (HTTP 202 Accepted)

The response body includes:

- `success`
- `job_id`
- `status`
- `time_window_hours`
- `status_url`
- `result_url`
- `warning` (present when `hours` exceeds the max; `null` otherwise)

Response headers include:

- `Location`
- `Retry-After`

Job IDs use the prefix `semantic_search_job_`.

`query`, `normalized_intent`, `matched_count`, `retained_count`, and `source_breakdown` are only available on the status and result endpoints — they are `0`, empty, or `null` at acceptance time and are therefore excluded from the 202 response.

## Job Status Contract

### Endpoint

```
GET /semantic-search/{job_id}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | `true` only when `status` is `completed` |
| `job_id` | string | The semantic search job identifier |
| `status` | string | Current state: `queued`, `running`, `completed`, or `failed` |
| `query` | string | Original normalized query |
| `normalized_intent` | string | Search intent (equals original query when `query_planning_enabled` is false, which is the default; LLM-normalized only when query planning is explicitly enabled) |
| `matched_count` | integer | Total matched items before final retention |
| `retained_count` | integer | Final retained items used for synthesis |
| `source_breakdown` | object | Per-domain hit counts: `{"news": {"matched_count": N, "retained_count": M}, "intelligence": {"matched_count": N, "retained_count": M}}` |
| `time_window_hours` | integer | Search time window after server caps |
| `created_at` | string (ISO 8601) | Job creation timestamp |
| `started_at` | string (ISO 8601) or null | When execution began |
| `completed_at` | string (ISO 8601) or null | When execution finished |
| `error` | string or null | Error message if failed |
| `processing_step` | string or null | Current processing stage: `"embedding"`, `"retrieving"`, `"ranking"`, or `null`. Used to distinguish "still processing" from a stuck job. |
| `result_available` | boolean | `true` when status is `completed` or `failed` |

Use the `status` field as the source of truth, not the `success` boolean.

## Result Contract

### Endpoint

```
GET /semantic-search/{job_id}/result
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | `true` only when `status` is `completed` |
| `job_id` | string | The semantic search job identifier |
| `status` | string | Terminal state: `completed` or `failed` |
| `query` | string | Original query |
| `normalized_intent` | string | Search intent (equals original query when `query_planning_enabled` is false, which is the default; LLM-normalized only when query planning is explicitly enabled) |
| `matched_count` | integer | Total matched items |
| `retained_count` | integer | Final retained items |
| `source_breakdown` | object | Per-domain hit counts: `{"news": {"matched_count": N, "retained_count": M}, "intelligence": {"matched_count": N, "retained_count": M}}` |
| `report` | string | Markdown semantic search report |
| `time_window_hours` | integer | Search time window |
| `error` | string or null | Error text when failed |

## Report Structure

The Markdown report follows this structure:

```markdown
# Topic Search Report

- Normalized intent: ...
- Original query: ...
- Time window: N hours
- Matched items: N
- Retained items: N

## Key Signals

### Signal 1
Concise synthesized paragraph.
Sources: [Source Name](https://example.com/article)
```

The live service currently returns the headings in Chinese (`# 主题检索报告`, `## 关键信号`). Treat the exact report string as implementation-defined content and preserve it as returned.

## Limits and Dependencies

- Requires PostgreSQL with pgvector; SQLite is unsupported
- Both `content_items` and `raw_intelligence_items` tables require `embedding vector(1536)` columns with HNSW indexes (`idx_content_embedding_hnsw`, `idx_intelligence_embedding_hnsw`) for performance
- Query length is capped at 300 characters
- LLM query decomposition is disabled by default (`query_planning_enabled: false`). The `max_subqueries` cap (4) only applies when query planning is explicitly re-enabled. When disabled, the raw user query is embedded directly as a single subquery
- Final retained results are capped at 200 unique items per domain before merging
- `OPENAI_API_KEY` is required for embedding generation
- `KIMI_API_KEY` or `GROK_API_KEY` is required for report synthesis (and for query planning only when explicitly enabled)
- **Time window**: Semantic search uses a separate, higher limit from `/analyze`. Default max is 720h (30 days), configured via `max_semantic_search_window_hours` in `analysis_config`. The analyze endpoint uses `max_analysis_window_hours` (default 24h). If `hours` exceeds the max, the response `warning` field indicates the cap was applied
- **Timeout**: Jobs that do not complete within 5 minutes (300 seconds) are automatically marked as `failed` with the error `"Semantic search timed out after 300s"`. The `processing_step` field in the status response helps track progress before timeout

## Telegram and Backfill Notes

- Telegram command: `/semantic_search <hours> <topic>`
- Historical embedding backfill for News content:

```bash
uv run python -m crypto_news_analyzer.main --mode embedding-backfill --config ./config.jsonc --batch-size 100
```

Optional: add `--limit 1000` to process only part of the backlog.

- To also backfill Intelligence embeddings:

```bash
uv run python -m crypto_news_analyzer.main --mode embedding-backfill --include-intelligence --intelligence-days 7 --config ./config.jsonc --batch-size 100
```

## Updating

Canonical sources for this reference:

1. `crypto_news_analyzer/api_server.py`
2. `crypto_news_analyzer/models.py`
3. `crypto_news_analyzer/semantic_search/models.py` (UnifiedSemanticSearchHit DTO, source_breakdown contracts)
4. `crypto_news_analyzer/domain/models.py`
5. `docs/SEMANTIC_SEARCH_API_GUIDE.md`
6. `migrations/postgresql/012_intelligence_embedding_schema.sql` (HNSW index creation)
7. `tests/test_api_server_semantic_search.py`
8. `tests/test_semantic_search_contracts.py`
9. `tests/shared/test_openclaw_skill_smart_news.py`

When sources disagree, trust code and tests over prose.
