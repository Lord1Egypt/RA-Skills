# QMD v1.1.6 Deep Analysis: What's New and What Memory Crystal Should Add

**Date:** 2026-03-09
**Author:** CC-Mini
**Context:** QMD (tobi/qmd) updated from v1.0.6 to v1.1.6. Memory Crystal already ported QMD's core search pipeline (RRF, strong-signal detection, query expansion, LLM reranking, position-aware blending). This analysis covers what QMD added since our port and what we should bring over.

---

## What QMD Added Since Our Port (v1.0.6 to v1.1.6)

### 1. SDK/Library Mode (v1.1.6)

`createStore()` API for programmatic access. No CLI needed.

```typescript
import { createStore } from '@tobilu/qmd'
const store = createStore({
  dbPath: './my-index.sqlite',
  config: {
    collections: {
      docs: { path: '/path/to/docs', pattern: '**/*.md' }
    }
  }
})
const results = await store.query("authentication flow", { limit: 5 })
```

Full API: `query()`, `search()`, `structuredSearch()`, `get()`, `multiGet()`, collection/context management, health checks.

**Why it matters:** Clean programmatic interface. No shelling out to CLI.

### 2. Intent Parameter (v1.1.5)

Single parameter that steers the entire pipeline without being a search term itself.

```bash
qmd query --intent "web performance" "performance"
```

How intent flows through the pipeline:
- **Query expansion:** added to LLM prompt, guides which variations get generated
- **Strong-signal bypass:** disabled when intent present (keyword match might not be what caller wants)
- **Chunk selection:** intent terms weighted at 0.5x alongside 1.0x query terms
- **Snippet extraction:** intent terms at 0.3x weight, nudges toward intent-relevant lines
- **Reranking:** intent prepended to query sent to reranker

**Why it matters:** "Remember what Parker said about performance" could mean system performance, financial performance, or job performance. Intent disambiguates without polluting the query.

### 3. Structured Search (v1.1.0)

Pre-expanded queries without calling the LLM. Caller does the expansion.

```typescript
const results = await store.structuredSearch([
  { type: 'lex', query: 'authentication' },
  { type: 'vec', query: 'how users log in' },
  { type: 'hyde', query: 'The system uses OAuth2 with PKCE flow...' }
])
```

Three sub-query types:
- `lex`: BM25 keyword search
- `vec`: vector semantic search
- `hyde`: hypothetical document embedding (vector search with a fake "ideal answer")

**Why it matters:** When the caller (an AI agent) already knows what it wants, skip the expansion LLM call entirely. Faster, cheaper, more predictable.

### 4. Score Traces / Explain Mode (v1.1.2)

`--explain` flag exposes per-document scoring breakdown:

```json
{
  "ftsScores": [0.67, 0.45],
  "vectorScores": [0.82, 0.71],
  "rrf": {
    "rank": 2,
    "baseScore": 0.034,
    "topRankBonus": 0.02,
    "contributions": [
      { "source": "fts", "queryType": "original", "rank": 1, "rrfContribution": 0.016 },
      { "source": "vec", "queryType": "vec", "rank": 3, "rrfContribution": 0.015 }
    ]
  },
  "rerankScore": 0.89,
  "blendedScore": 0.78
}
```

Per-list RRF contribution traces show exactly which search path found each result and how much it contributed.

**Why it matters:** Debugging search quality. When a result seems wrong, you can see exactly why it ranked where it did.

### 5. HTTP MCP Transport (v1.1.2)

Long-lived MCP server over HTTP instead of stdio subprocess per client.

```bash
qmd mcp --http --daemon    # Models stay warm in VRAM
qmd mcp stop               # Clean shutdown
```

Benefits: models stay loaded between requests (16s cold start avoided), multiple concurrent client sessions, liveness endpoint at `/health`.

**Why it matters:** Memory Crystal's MCP server currently starts fresh every time. A persistent HTTP server would keep embedding models warm.

### 6. Collection Management Improvements (v1.1.0-v1.1.2)

- YAML-based config (`~/.config/qmd/index.yml`) instead of SQLite-only
- `ignore` patterns per collection (exclude folders/files from indexing)
- `includeByDefault: false` for opt-in collections (hidden unless explicitly named in search)
- `update` command per collection (e.g., `git pull` before re-indexing)
- Named indexes (`--index work`) for separate knowledge bases on same machine

### 7. Content-Addressable Reranker Cache (v1.1.2)

Reranker results cached by content hash, not filepath. Identical chunks from different files share cached scores. This means:
- Duplicate content across sessions only gets reranked once
- Cache survives file moves/renames

### 8. Parallel Reranking with VRAM Cap (v1.1.2)

- Multiple reranking contexts created based on available VRAM and CPU cores
- Capped at 4 parallel contexts to prevent VRAM exhaustion
- Chunk deduplication before reranking (don't score the same text twice)

### 9. Lex Syntax for BM25 (v1.1.0)

Structured query syntax for full-text search:
- Quoted phrases: `"exact match"`
- Negation: `-unwanted` (maps to FTS5 NOT operator)
- Multiple terms combined with AND logic

### 10. Custom Embedding Model Support (v1.1.5)

`QMD_EMBED_MODEL` env var to swap embedding models:
```bash
export QMD_EMBED_MODEL="hf:Qwen/Qwen3-Embedding-0.6B-GGUF/qwen3-embedding-0.6b-q8_0.gguf"
qmd embed -f  # Re-embed everything with new model
```

---

## What Memory Crystal Already Has From QMD

| Feature | Status | Notes |
|---------|--------|-------|
| BM25 + Vector hybrid search | Done | FTS5 + sqlite-vec |
| RRF fusion | Done | k=60, BM25 weighted 2x |
| Strong-signal detection | Done | 0.85 threshold, 0.15 gap |
| Query expansion (lex, vec, HyDE) | Done | LLM-based, prompt parsing |
| LLM re-ranking | Done | Top 40 candidates |
| Position-aware blending | Done | 75/25, 60/40, 40/60 tiers |
| Recency weighting | Done | Exponential decay, floor 0.3 (QMD doesn't have this) |
| Multi-provider LLM cascade | Done | MLX, Ollama, Anthropic, OpenAI |
| File/source indexing | Done | crystal sources add/sync |

---

## Recommendations: What to Add to Memory Crystal

### HIGH PRIORITY (clear value, reasonable effort)

#### 1. Intent Parameter
**Effort:** Medium (touches expansion, reranking, snippet extraction)
**Value:** High

Memory Crystal serves AI agents searching conversational memory. Queries like "what did Parker say about security" are ambiguous: security audit? 1Password security? repo security? An intent parameter ("1Password automation") disambiguates without changing the query itself.

**Implementation:**
- Add `intent` param to `crystal_search` MCP tool
- Pass through to expansion prompt, reranker query, and snippet selection
- Disable strong-signal bypass when intent present
- Weight intent terms at 0.5x in chunk scoring

#### 2. Structured Search API
**Effort:** Low (the infrastructure is already there)
**Value:** High

Let callers skip LLM expansion when they already know what they want. An AI agent planning a complex memory retrieval can construct lex+vec+hyde queries directly.

**Implementation:**
- Add `structuredSearch()` method to core
- Accept array of `{ type: 'lex'|'vec'|'hyde', query: string }`
- Route each to appropriate search backend
- Fuse with existing RRF, rerank, blend

#### 3. Persistent Expansion/Rerank Cache
**Effort:** Low (add a table, key by content hash)
**Value:** Medium-High

Memory Crystal's expansion and reranker caches are in-memory only. Every process restart (gateway restart, CLI invocation) loses all cached scores. QMD persists these in SQLite keyed by (query, model, content_hash).

**Implementation:**
- Add `llm_cache` table: key (TEXT), value (TEXT), model (TEXT), created_at
- Key expansion cache by query+model+intent
- Key reranker cache by query+model+content_hash (not chunk_id)
- Prune stale entries periodically

#### 4. Score Traces / Explain Mode
**Effort:** Medium (plumbing through the pipeline)
**Value:** Medium-High

When search quality issues come up ("why didn't Crystal find X?"), there's currently no way to see how scoring worked. Adding explain traces to crystal_search would let us debug without reading code.

**Implementation:**
- Add `explain: boolean` param to search
- Return per-result scoring breakdown: FTS scores, vector scores, RRF rank/contributions, reranker score, blended score
- Log to search-metrics.jsonl for offline analysis

### MEDIUM PRIORITY (good value, more effort or less urgent)

#### 5. Content-Addressable Reranker Cache
**Effort:** Low (change cache key)
**Value:** Medium

Cache reranker results by content text hash instead of chunk ID. Identical content across different conversation sessions shares the same cached score. Especially valuable since conversation memory has lots of repeated patterns.

#### 6. Lex Query Syntax (Negation, Phrases)
**Effort:** Low (FTS5 supports this natively)
**Value:** Medium

Allow `crystal search "exact phrase" -unwanted` syntax. Useful for filtering out noise: `crystal search "Parker said" -debug -error` to find Parker's comments, not error logs containing "Parker."

#### 7. Named Indexes
**Effort:** Medium
**Value:** Medium

Separate indexes for different knowledge domains: `--index work` vs `--index personal`. Memory Crystal currently has one crystal.db. Multiple indexes would let agents maintain separate memory spaces.

#### 8. SDK/Library Mode (createStore API)
**Effort:** Medium-High
**Value:** Medium

Clean programmatic API without going through CLI or MCP. Other LDM OS components could directly query Memory Crystal as a library. Lower priority since MCP already provides this, but a direct API would be faster (no serialization overhead).

### LOW PRIORITY (nice to have, not urgent)

#### 9. HTTP MCP Transport
**Effort:** Medium
**Value:** Low-Medium

Memory Crystal's MCP server already runs as stdio via OpenClaw/Claude Code. HTTP transport would only matter if we had multiple clients connecting to the same server. Not needed yet.

#### 10. Custom Embedding Model Support
**Effort:** Medium
**Value:** Low

Memory Crystal already supports 3 providers (OpenAI, Ollama, Google). Adding env-var model override would be nice but not urgent since text-embedding-3-small works well.

#### 11. Collection Ignore Patterns
**Effort:** Low
**Value:** Low

`crystal sources add` could accept `--ignore` patterns. Minor convenience, not blocking anything.

---

## What Memory Crystal Has That QMD Doesn't

These are Memory Crystal advantages. Don't lose them.

| Feature | Notes |
|---------|-------|
| Recency weighting | Exponential decay. QMD treats all docs equally. Memory is time-sensitive. |
| Multi-agent support | agent_id per chunk. QMD is single-user. |
| Conversation ingestion | Structured capture from agent sessions. QMD only indexes files. |
| Relay/sync architecture | Core/Node roles, encrypted relay, delta sync. QMD is single-machine. |
| Category-aware memories | fact, preference, event, opinion, skill. QMD has no memory categories. |
| Private mode | Kill switch for capture. QMD has no privacy controls. |
| Capture watermarking | Tracks exactly what's been ingested. QMD re-indexes from scratch. |

---

## Suggested Implementation Order

1. **Persistent cache** (quick win, immediate search perf improvement)
2. **Intent parameter** (biggest search quality improvement for agent use)
3. **Structured search** (lets agents be smarter about queries)
4. **Explain mode** (debugging tool, helps us tune everything else)
5. **Lex syntax** (small quality-of-life improvement)
6. Everything else as needed
