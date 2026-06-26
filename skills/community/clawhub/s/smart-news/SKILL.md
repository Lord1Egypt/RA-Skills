---
name: smart-news
description: Use when calling the Crypto News Analyzer HTTP API for async analysis jobs, semantic search, datasource management, intelligence operations, or health checks from OpenClaw.
metadata: { openclaw: { skillKey: smart-news, primaryEnv: API_KEY } }
---

# Crypto News HTTP API Skill

Use this skill to call the Crypto News Analyzer HTTP API from OpenClaw.

## When to Use

Use this skill when you need to call `https://news.tradao.xyz` or a compatible private deployment.

Typical triggers:

- Run asynchronous crypto news analysis over a time window
- Run asynchronous unified semantic search (News + Intelligence) for a freeform topic query
- Poll an API job until it finishes and then fetch the final result
- Create, list, or delete datasources through the HTTP API
- Query and manage intelligence topics through the topic-first API (create, revise, confirm, merge findings, detail, list, archive)
- View and manage topic-datasource associations (get, set, add, remove) to scope topic research
- List intelligence topic research run logs per-topic or globally
- Check service health before or after an API workflow

## Quick Reference

Authentication is Bearer token style: send `Authorization: Bearer <API_KEY>` with every request.

`POST /analyze` creates a job and returns immediately. It does **not** return the final report. Poll status, then fetch the result.

Workflow: `POST /analyze` -> `GET /analyze/{job_id}` -> `GET /analyze/{job_id}/result`

Jobs move through these states: `queued`, `running`, `completed`, `failed`.

`POST /semantic-search` creates a job, returns `202 Accepted`, and includes `status_url`, `result_url`, plus a `Retry-After` header. When `hours` exceeds the server max (720h default), a `warning` field describes the truncation. Semantic search jobs that do not complete within 5 minutes are automatically failed with a timeout error.

Semantic workflow: `POST /semantic-search` -> `GET /semantic-search/{job_id}` -> `GET /semantic-search/{job_id}/result`

Unified semantic search retrieves from both `content_items` and `raw_intelligence_items` via PostgreSQL with pgvector HNSW indexes (`embedding vector(1536)`). SQLite runtime is unsupported.

For detailed guides, see:

- [Analyze Workflow Reference](references/analyze-workflow.md)
- [Semantic Search Reference](references/semantic-search.md)
- [Datasource Management Reference](references/datasource-management.md)
- [Intelligence Query Reference](references/intelligence-query.md)
- [Operations and Maintenance Reference](references/operations-and-maintenance.md)

## OpenClaw Runtime

This skill declares `metadata.openclaw.primaryEnv: API_KEY`. In OpenClaw, inject the bearer token through `~/.openclaw/openclaw.json`:

```json5
{
  skills: {
    entries: {
      "smart-news": {
        enabled: true,
        apiKey: "YOUR_API_KEY"
      }
    }
  }
}
```

If `apiKey` is unavailable, do not send unauthenticated requests. Ask the operator to configure the token first.

If you are using a non-production deployment, replace `https://news.tradao.xyz` with the correct base URL before issuing requests.

## Analyze Workflow

Create an analysis job by posting to `/analyze` with `hours` and `user_id`. The server responds with `202 Accepted`, a `job_id`, `status_url`, and `result_url`.

Poll the status endpoint until the job reaches `completed` or `failed`. Do not expect the analysis report in the initial POST response. Once completed, fetch the result URL.

## Semantic Search

Unified semantic search retrieves from both News (`content_items`) and Intelligence (`raw_intelligence_items`) domains via UNION ALL over pgvector HNSW indexes. The response includes a `source_breakdown` with per-domain `matched_count` and `retained_count`. Each hit carries a `source_domain` discriminator (`"news"` or `"intelligence"`).

Create a semantic search job by posting to `/semantic-search` with `hours`, `query`, and `user_id`. The server responds with `202 Accepted`, a `job_id`, `status_url`, and `result_url`. Semantic search job IDs start with `semantic_search_job_`.

Poll the status endpoint until the job reaches `completed` or `failed`, then fetch the report from the result URL. Use the `status` field as the source of truth for lifecycle state; `success` becomes `true` only when the job is completed successfully.

Request rules:

- `hours` must be a positive integer
- `query` is required, trimmed, and capped at 300 characters
- `query` cannot be blank or whitespace-only
- `user_id` must match `^[A-Za-z0-9_-]{1,128}$`

Operational constraints:

- Semantic search is PostgreSQL-only and returns `503` when the backend does not support pgvector
- Both `content_items` and `raw_intelligence_items` tables have `embedding vector(1536)` columns with HNSW indexes (`idx_content_embedding_hnsw` and `idx_intelligence_embedding_hnsw`)
- The API uses vector similarity over stored content embeddings and combines that with deterministic local keyword fallback (no LLM-driven keyword expansion)
- LLM query decomposition is disabled by default (`query_planning_enabled: false`); when disabled the raw user query is embedded directly as the only subquery. The `max_subqueries` cap (4) only applies when query planning is explicitly re-enabled
- Final retained results are capped at 200 unique items per domain before merging
- Embedding generation requires `OPENAI_API_KEY`; report synthesis requires `KIMI_API_KEY` or `GROK_API_KEY` (query planning also requires an LLM key but is disabled by default)

The result body returns a Markdown report with `query`, `normalized_intent`, `matched_count`, `retained_count`, `time_window_hours`, `source_breakdown`, and `report`.

## Datasource Management

Configure news and intelligence sources through the datasource API. Create sources with `POST /datasources`, list them with `GET /datasources`, and remove them with `DELETE /datasources/{id}`. All datasource routes require Bearer auth.

Each datasource has a `purpose` field: `news` (RSS/X/REST feeds for analysis) or `intelligence` (Telegram groups, V2EX for topic research). The `GET /datasources` endpoint supports optional `purpose` and `source_type` query parameters for filtering. Results are sorted by purpose, source type, then name.

Tags help organize sources. Each datasource accepts up to 16 unique tags. Each tag is capped at 32 characters. Tags are normalized to lowercase and deduplicated automatically.

List and create responses include only safe summaries. For `rest_api` type datasources, secrets are redacted and counts replace raw credential fields. This prevents accidental credential exposure when reviewing configurations.

## Intelligence Query (Topic-First)

All intelligence routes require Bearer auth. The deprecated entry-based routes (`/intelligence/entries*`, `/intelligence/discovery`, `/intelligence/labels`, `/intelligence/search`) have been removed in the topic-only refactor. Topics are the sole first-class intelligence objects, driving scheduled LLM research from raw ingested messages and storing findings with merge support.

Synchronous topic workflow endpoints:

- `POST /intelligence/topics` — Create a topic draft from a user theme (returns AI-generated prompt draft)
- `POST /intelligence/topics/{topic_id}/revise` — Revise the draft prompt with feedback
- `PUT /intelligence/topics/{topic_id}/prompt` — Manually set/replace the prompt text (context-aware: edits active prompt if one exists, otherwise creates draft revision)
- `POST /intelligence/topics/{topic_id}/confirm` — Confirm and activate the topic for research (requires `prompt_version_id`)
- `GET /intelligence/topics` — List topics with pagination and `active_only` filter (default: true)
- `GET /intelligence/topics/{topic_id}` — Get topic metadata and merge availability
- `GET /intelligence/topics/{topic_id}/findings` — Get paginated active findings with citations and source URLs
- `GET /intelligence/topics/{topic_id}/prompts` — Get prompt versions and current active prompt
- `POST /intelligence/topics/{topic_id}/archive` — Archive a topic
- `GET /intelligence/topics/{topic_id}/runs` — List topic research run logs
- `GET /intelligence/topic-runs` — List all topic research runs globally

These endpoints are synchronous; there is no async job/poll flow. Results return immediately.

Async topic merge endpoint:

- `POST /intelligence/topics/{topic_id}/merge` — Start an async merge job (returns 202 Accepted with `job_id`, `status_url`, `result_url`)
- `GET /intelligence/topics/{topic_id}/merge/{job_id}` — Check merge job status
- `GET /intelligence/topics/{topic_id}/merge/{job_id}/result` — Retrieve completed merge results

Merge workflow: `POST /intelligence/topics/{id}/merge` → poll `GET .../merge/{job_id}` → `GET .../merge/{job_id}/result`. Jobs move through states: `queued`, `running`, `completed`, `failed`. The merge LLM call may take several minutes, so polling is required — do not block on the POST response.

Topics have lifecycle states: `draft`, `active`, `archived`. Only `active` topics are researched by the ingestion scheduler. Finding merge is available through both the async HTTP endpoint and the Telegram `/topic_merge` command.

## Telegram Webhook

The webhook endpoint exists for maintainer-level Telegram integration. It is not the primary path for day-to-day operators. Regular users should interact through the API routes or Telegram slash commands instead.

When processing webhook updates, validate the `X-Telegram-Bot-Api-Secret-Token` header to confirm the request originates from Telegram.

## Endpoint Index

Supported HTTP routes:

- `GET /health` - Service health check
- `POST /analyze` - Create an analysis job (async, returns 202)
- `GET /analyze/{job_id}` - Check job status
- `GET /analyze/{job_id}/result` - Retrieve completed job results
- `POST /semantic-search` - Create a semantic search job (async, returns 202)
- `GET /semantic-search/{job_id}` - Check semantic search job status
- `GET /semantic-search/{job_id}/result` - Retrieve completed semantic search results
- `POST /datasources` - Create a datasource
- `GET /datasources` - List all datasources
- `DELETE /datasources/{id}` - Delete a datasource
- `POST /telegram/webhook` - Telegram webhook receiver
- `POST /intelligence/topics` - Create topic draft (synchronous, Bearer-protected)
- `POST /intelligence/topics/{id}/revise` - Revise topic prompt
- `PUT /intelligence/topics/{id}/prompt` - Manually set topic prompt
- `POST /intelligence/topics/{id}/confirm` - Confirm and activate topic
- `GET /intelligence/topics` - List topics with status filters
- `GET /intelligence/topics/{id}` - Get topic metadata and merge availability
- `GET /intelligence/topics/{id}/findings` - Get paginated findings with citations
- `GET /intelligence/topics/{id}/prompts` - Get prompt versions and active prompt
- `POST /intelligence/topics/{id}/archive` - Archive topic
- `POST /intelligence/topics/{id}/merge` - Start async merge job (returns 202)
- `GET /intelligence/topics/{id}/merge/{job_id}` - Check merge job status
- `GET /intelligence/topics/{id}/merge/{job_id}/result` - Retrieve completed merge results
- `GET /intelligence/topics/{id}/datasources` - List datasource associations for a topic
- `PUT /intelligence/topics/{id}/datasources` - Replace all datasource associations atomically
- `POST /intelligence/topics/{id}/datasources/{datasource_id}` - Add a datasource association (idempotent)
- `DELETE /intelligence/topics/{id}/datasources/{datasource_id}` - Remove a datasource association (idempotent)
- `GET /intelligence/topics/{id}/runs` - List topic research run logs
- `GET /intelligence/topic-runs` - List all topic research runs globally

## Non-Goals

This skill does not cover:

- Telegram slash commands (use the Telegram bot directly)
- Autogenerated documentation routes (`/docs`, `/redoc`, `/openapi.json`)
- Deprecated compatibility aliases are not part of the active runtime surface
- Direct embedding backfill operations beyond pointing you to the documented command

These surfaces exist but are intentionally excluded from this API-focused skill.

## Updating

Keep this skill aligned with the live HTTP routes in `api_server.py`, the AI Analyze API Guide at `docs/AI_ANALYZE_API_GUIDE.md`, the semantic search guide at `docs/SEMANTIC_SEARCH_API_GUIDE.md`, and the domain repository contracts in `domain/repositories.py`.

When documentation disagrees with implementation, trust the code and tests over prose docs. Source precedence: code first, then reference files, then guides.
