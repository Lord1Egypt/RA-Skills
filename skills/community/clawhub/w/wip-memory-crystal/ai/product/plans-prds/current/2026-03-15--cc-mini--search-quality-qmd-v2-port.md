# Plan: Search Quality ... QMD v2.0 Port (Intent, Cache, Unified API, Explain)

**Date:** 2026-03-15
**Author:** CC-Mini + Parker
**Status:** Ready to build
**Related:** `current/search-quality-full-plan.md` (Phase 1-4), `../notes/2026-03-15--cc-mini--qmd-v2.0-analysis.md`, `upcoming/2026-03-13--cc-mini--phase3-mlx-local-llm-and-search-caching.md`

---

## Context

QMD went from v1.1.6 to v2.0.1. We ported the core search pipeline (RRF, expansion, reranking, blending) in Phase 1-2. Score normalization was fixed in v0.7.19. Phase 3 (MLX local LLM) is planned separately.

This plan covers the remaining search quality features from QMD that we should port. These are independent of Phase 3 (MLX). They work with any LLM provider.

## What We're Building

Four features, ordered by priority. Each can ship independently.

---

### 1. Intent Parameter

**Priority:** Highest
**Effort:** Medium
**Source:** QMD v1.1.5

#### What it does

A string parameter that disambiguates search queries without being a search term itself. Flows through the entire pipeline.

Example: `crystal search "security" --intent "1Password automation"`

Without intent: returns everything mentioning "security" (audit, repo permissions, plaintext tokens, agent secrets, etc.)
With intent: steers toward 1Password-related security results.

#### How intent flows through the pipeline

| Stage | How intent is used |
|-------|-------------------|
| **Query expansion** | Added to LLM prompt: "Query intent: {intent}". Guides which variations get generated. |
| **Strong-signal bypass** | Disabled when intent present. The obvious keyword match might not be what the caller wants. |
| **Reranking** | Intent prepended to the query sent to the LLM reranker. |
| **Score blending** | No change (intent already influenced expansion and reranking). |

#### Files to modify

| File | Change |
|------|--------|
| `src/core.ts` | Add `intent?: string` to search filter param. Pass through to deep search. |
| `src/search-pipeline.ts` | Add intent to expansion prompt, disable strong-signal when intent present, prepend to rerank query. |
| `src/llm.ts` | Modify `EXPAND_PROMPT` to include intent context. Modify `RERANK_PROMPT` to include intent. |
| `src/mcp-server.ts` | Add `intent` param to `crystal_search` tool. |
| `src/cli.ts` | Add `--intent` flag to `crystal search`. |

#### Implementation

In `llm.ts`, modify `EXPAND_PROMPT`:
```
// When intent is provided, add to the system prompt:
"Query intent: {intent}. Use this to guide your variations toward the intended domain."
```

In `search-pipeline.ts`:
```typescript
// Disable strong-signal bypass when intent is present
const hasStrongSignal = !intent && initialFts.length > 0
  && topScore >= STRONG_SIGNAL_MIN_SCORE
  && (topScore - secondScore) >= STRONG_SIGNAL_MIN_GAP;
```

In reranking:
```typescript
// Prepend intent to the rerank query
const rerankQuery = intent ? `${intent}: ${query}` : query;
```

---

### 2. Persistent Expansion + Reranking Cache

**Priority:** High
**Effort:** Low
**Source:** QMD v1.1.2 + Phase 3 plan

#### What it does

Cache LLM expansion and reranking results in crystal.db so repeated queries are instant. Currently in-memory only (Map in llm.ts, lost every process restart).

#### Database table

```sql
CREATE TABLE IF NOT EXISTS llm_cache (
  cache_key TEXT PRIMARY KEY,
  cache_type TEXT NOT NULL,     -- 'expansion' | 'rerank'
  query TEXT NOT NULL,
  intent TEXT,                  -- null if no intent
  result TEXT NOT NULL,         -- JSON (expansion variations or rerank scores)
  provider TEXT NOT NULL,       -- which LLM produced this
  created_at TEXT NOT NULL,
  hit_count INTEGER DEFAULT 0,
  last_hit_at TEXT
);
CREATE INDEX idx_llm_cache_type ON llm_cache(cache_type);
CREATE INDEX idx_llm_cache_created ON llm_cache(created_at);
```

#### Cache keys

- **Expansion:** SHA-256 of `query + intent + provider`
- **Reranking:** SHA-256 of `query + intent + sorted(passage_hashes) + provider`

Content-addressable (by text hash, not chunk ID). Identical content from different sessions shares the same cached score. This is what QMD does.

#### TTL

- Default: 7 days
- `crystal cleanup` should also prune expired cache entries
- Configurable via env var `CRYSTAL_CACHE_TTL_DAYS`

#### Files to modify

| File | Change |
|------|--------|
| `src/core.ts` | Add `llm_cache` table to `initSqliteTables()` |
| `src/llm.ts` | Replace in-memory Map with DB lookup/store. Accept db handle. |
| `src/cli.ts` | Pass db to llm functions. Add cache stats to `crystal status`. |
| `src/mcp-server.ts` | Pass db to llm functions. |

---

### 3. Unified Search API (query vs queries)

**Priority:** Medium-High
**Effort:** Low
**Source:** QMD v2.0.0

#### What it does

Single `search()` method accepts either a string (auto-expands via LLM) or an array of pre-expanded queries (skips LLM). Currently we have `search()` (auto) and would need a separate `structuredSearch()` for pre-expanded. QMD unified these in v2.0.

#### API

```typescript
// Auto-expand (current behavior)
crystal.search("what did Parker say about security", 5)

// Pre-expanded (new, skips LLM)
crystal.search({
  queries: [
    { type: 'lex', text: 'Parker security 1password' },
    { type: 'vec', text: 'Parker discussing password management security' },
    { type: 'hyde', text: 'Parker said we should move secrets to 1Password...' }
  ]
}, 5)
```

#### Why it matters

AI agents are smart enough to construct their own queries. When the agent already knows what it wants, skipping the LLM expansion saves time and cost. The agent can pass pre-expanded queries directly.

#### Files to modify

| File | Change |
|------|--------|
| `src/core.ts` | Overload `search()` to accept string or `{ queries, intent? }` object |
| `src/search-pipeline.ts` | Accept pre-expanded queries, skip expansion step |
| `src/mcp-server.ts` | Add `queries` array param to `crystal_search` tool (optional, alternative to `query`) |

---

### 4. Explain Mode / Score Traces

**Priority:** Medium
**Effort:** Medium
**Source:** QMD v1.1.2

#### What it does

`crystal search --explain "query"` returns per-result scoring breakdown: FTS score, vector score, RRF rank, RRF contributions per list, reranker score, recency weight, final blended score.

#### Why it matters

When search quality issues come up ("why didn't Crystal find X?"), there's no way to debug without reading code. Explain mode makes scoring transparent. Lesa found the 100% scoring bug through usage. Explain mode would have caught it in one query.

#### Output format

```json
{
  "text": "Parker said we should move secrets...",
  "score": 0.85,
  "explain": {
    "fts_score": 0.67,
    "vec_score": 0.82,
    "rrf_rank": 2,
    "rrf_score": 0.034,
    "rrf_contributions": [
      { "source": "fts", "rank": 1, "contribution": 0.016 },
      { "source": "vec", "rank": 3, "contribution": 0.015 }
    ],
    "rerank_score": 0.89,
    "recency_weight": 0.90,
    "final_score": 0.85
  }
}
```

#### Files to modify

| File | Change |
|------|--------|
| `src/core.ts` | Add `explain?: boolean` to search params. Thread through to RRF, recency. Return trace data. |
| `src/search-pipeline.ts` | Collect per-stage scores when explain=true. |
| `src/cli.ts` | Add `--explain` flag. Print trace table. |
| `src/mcp-server.ts` | Add `explain` param to crystal_search. Return traces in response. |

---

### 5. candidateLimit as Parameter (Quick Win)

**Priority:** Medium
**Effort:** Very low (one line + param plumbing)
**Source:** QMD v1.1.2/v2.0

Currently hardcoded at 40 in `search-pipeline.ts`:
```typescript
const RERANK_CANDIDATE_LIMIT = 40;
```

Expose as a parameter:
- CLI: `--candidates 60`
- MCP: `candidate_limit: 60`
- Default stays 40

More candidates = better recall, slower reranking. Useful for tuning.

---

## Implementation Order

1. **candidateLimit** (15 min, quick win, ship immediately)
2. **Persistent cache** (1-2 hours, biggest perf improvement)
3. **Intent parameter** (2-3 hours, biggest quality improvement)
4. **Unified search API** (1 hour, enables smarter agent queries)
5. **Explain mode** (2-3 hours, debugging tool)

Total: ~8 hours of implementation. Each ships independently as a patch release.

## Testing

- `crystal search "security" --intent "1Password"` returns 1Password-related results
- `crystal search "security"` (no intent) returns broad results
- Second identical search hits cache (check stderr for "cache hit")
- `crystal search --explain "Parker"` shows score breakdown
- `crystal search --candidates 10 "test"` uses 10 candidates instead of 40
- `crystal cleanup` prunes expired cache entries

## Relationship to Phase 3 (MLX)

These features are independent of MLX. They work with any LLM provider (OpenAI, Anthropic, Ollama, future MLX). Phase 3 changes WHICH LLM runs the expansion/reranking. This plan changes HOW the search pipeline works. Both can be built in parallel.

When MLX ships (Phase 3), the persistent cache becomes even more valuable: local inference is fast but not free (VRAM, power). Caching avoids redundant local LLM calls too.
