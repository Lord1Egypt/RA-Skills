# Plan: Search Quality Fix ... Port QMD Features to Memory Crystal

**Created:** 2026-03-04
**Updated:** 2026-03-05
**Status:** Phase 1 + Phase 2 core complete. Tuning + local models remaining.
**Agent:** CC-Mini
**Dev Update:** `ai/dev-updates/2026-03-05--00-50--cc-mini--search-quality-qmd-port.md`

## Context

After consolidating 3 memory stores into 1 crystal.db (207K chunks), search quality degraded. Recent content gets buried by older semantically similar content. The recency weight (`Math.max(0.5, 1.0 - ageDays * 0.01)`) is too weak for a corpus this size. With 16K chunks, mediocre ranking was fine. With 207K, it's not.

QMD (Tobi Lutke's query tool, MIT license) has battle-tested search quality features we already partially ported (RRF, BM25, FTS5). The remaining features address exactly our problem.

## What We're Building

Two phases. Phase 1 is a quick fix (recency + time filter). Phase 2 ports QMD's LLM-powered features.

---

### Phase 1: Quick Fix (recency boost + time filter) ... DONE

**Goal:** Make recent content competitive again without any new dependencies.
**Status:** Complete. Deployed 2026-03-05.

**Files to modify:**
- `src/core.ts` (search method, recencyWeight method, search signature)
- `src/mcp.ts` (add time_filter parameter to crystal_search tool)
- `src/cli.ts` (add --since flag to crystal search command)

**Changes:**

1. **Stronger recency curve** in `recencyWeight()` (core.ts:607-611)
   - Current: linear decay, floor 0.5, ~50 days to floor
   - New: exponential decay with corpus-aware boost
   ```typescript
   private recencyWeight(ageDays: number): number {
     // Exponential decay: fresh content gets strong boost, rapid falloff
     // Floor 0.3 (was 0.5) so recent content wins more decisively
     // Half-life ~7 days (was ~25 days effective)
     return Math.max(0.3, Math.exp(-ageDays * 0.1));
   }
   ```
   - Day 0: 1.0, Day 1: 0.90, Day 3: 0.74, Day 7: 0.50, Day 14: 0.25 (floor 0.3), Day 30: 0.3

2. **Time-filtered search** ... add optional `since` parameter to search()
   - Add `since?: string` to filter parameter (ISO date or relative like "7d", "24h")
   - Apply as SQL WHERE clause: `AND created_at >= ?`
   - Expose in MCP tool schema and CLI

3. **Fetch more candidates** ... increase fetchLimit
   - Current: `Math.max(limit * 3, 30)`
   - New: `Math.max(limit * 5, 50)` to give recency weighting more candidates to work with

**Verification:**
- `crystal search "bridge conversation"` should surface today's content in top 3
- `crystal search "bridge conversation" --since 24h` should return only recent results
- MCP: `crystal_search` with `time_filter: "7d"` should work

---

### Phase 2: QMD Port (query expansion + LLM re-ranking) ... CORE DONE, TUNING REMAINING

**Goal:** Port QMD's LLM-powered search quality features.
**Status:** Core pipeline built and deployed. Deep search is the default. Tuning and local model setup remaining.

**New files:**
- `src/llm.ts` ... LLM client with provider cascade (query expansion + re-ranking)
- `src/search-pipeline.ts` ... advanced search pipeline (orchestrates expansion, search, rerank, blend)

**Files to modify:**
- `src/core.ts` ... wire in the new pipeline as an optional upgrade path
- `src/mcp.ts` ... add `quality` parameter ("fast" | "deep") to crystal_search
- `src/cli.ts` ... add --deep flag to crystal search

**Features ported from QMD:**

1. [x] **Query expansion** (QMD store.ts:2204-2231, llm.ts:936-1017)
   - Generates 3 search variations: lexical, vector-optimized, hypothetical document (HyDE)
   - ~~Grammar-constrained output for reliable JSON parsing~~ ... uses prompt-based parsing (see remaining)
   - Cache expanded queries (same query = same expansions) ... in-memory only (see remaining)

2. [x] **Strong signal detection** (QMD store.ts:2806-2820)
   - Before expanding: run BM25 probe
   - If top BM25 score >= 0.85 AND gap to #2 >= 0.15, skip expansion (already found the answer)
   - Saves LLM call latency on obvious matches

3. [x] **LLM re-ranking** (QMD store.ts:2237-2272, llm.ts:1019-1071)
   - Takes top 40 RRF candidates, re-ranks by relevance
   - ~~Parallel context evaluation for speed~~ ... single prompt, sequential (see remaining)

4. [x] **Position-aware score blending** (QMD store.ts:2250-2270)
   - Top 3 results: 75% RRF + 25% reranker
   - Results 4-10: 60% RRF + 40% reranker
   - Results 11+: 40% RRF + 60% reranker
   - Rationale: trust RRF for top positions, let reranker fix ordering in the tail

5. [x] **Tiered RRF weights** (QMD store.ts:2278-2321)
   - Changed from [1.0, 1.0] to [2.0, 1.0] ... BM25 gets double weight

6. [x] **Deep as default** (Parker's feedback: "I have to do --deep? I don't get it.")
   - CLI and MCP both run deepSearch by default
   - No flags needed. Falls back silently if no LLM provider

7. [x] **Op-secrets integration** for API keys
   - `getOpSecret()` in llm.ts reads SA token from `~/.openclaw/secrets/op-sa-token`
   - No env vars needed for CLI usage

**LLM Provider Cascade:**

The LLM features (expansion + re-ranking) use a cascading provider strategy. Try each in order, use the first available:

| Priority | Provider | Models | Cost | Speed | Where it works |
|----------|----------|--------|------|-------|----------------|
| 1 | MLX (local) | Qwen3.5-2B / Qwen3-4B-Instruct via mlx_lm.server | Free | Fastest (2x Ollama on Apple Silicon) | Any Mac with Apple Silicon |
| 2 | Ollama (local) | Qwen3-1.7B + Qwen3-Reranker-0.6B | Free | Fast | Any machine with Ollama |
| 3 | Anthropic API | Haiku 4.5 (expansion + rerank) | ~$0.001/search | Network-dependent | Everywhere with API key |
| 4 | OpenAI API | GPT-4o-mini (expansion + rerank) | ~$0.001/search | Network-dependent | Everywhere with API key |
| 5 | None | Skip LLM features | Free | N/A | Falls back to Phase 1 |

**Why MLX first:** Apple's MLX framework is 2x faster than Ollama for generation and uses 50% less memory on Apple Silicon. `mlx_lm.server` exposes an OpenAI-compatible HTTP API on localhost:8080 (`/v1/chat/completions`). Our Node.js code talks to it like any OpenAI endpoint. No native bindings needed.

**MLX setup:** `pip install mlx-lm && mlx_lm.server --model mlx-community/Qwen3.5-2B-Instruct-4bit`

Detection logic in `llm.ts`:
- Check `http://localhost:8080/v1/models` ... MLX server
- Check `http://localhost:11434/api/tags` ... Ollama (filters out embedding-only models)
- Check env var or 1Password for OpenAI key ... `getOpSecret('OpenAI API', 'api key')`
- Check env var for Anthropic key ... skips OAuth tokens (`sk-ant-oat01-`)
- None found ... log once, use fast path

Local-first by default. API keys are the fallback, not the primary path. This keeps search free, fast, and sovereign.

**Current working provider:** OpenAI API via op-secrets (confirmed working 2026-03-05).

**Dependencies:**
- At least one of: MLX server, Ollama, Anthropic API key, or OpenAI API key
- For MLX: `pip install mlx-lm` then `mlx_lm.server --model mlx-community/Qwen3.5-2B-Instruct-4bit`
- For Ollama: `ollama pull qwen3:1.7b` (need a chat model, not just embedding)
- Graceful degradation: if no LLM provider found, falls back to Phase 1 silently

**Verification:**
- `crystal search "bridge conversation"` ... deep search runs by default
- `crystal search "query" --since 24h` ... time-filtered search
- MCP: `crystal_search` with `time_filter: "7d"` works
- Without any LLM provider, falls back to Phase 1 silently

---

## Platform Support

| Platform | Phase 1 (recency + time filter) | Phase 2 (LLM expansion + rerank) | Best provider |
|----------|------|------|------|
| Mac Mini (CC + OC) | Yes | Yes | MLX (fastest, free, local) |
| MacBook Air (CC) | Yes | Yes | MLX (fastest, free, local) |
| iOS apps (Claude Desktop, etc.) | Yes (via Cloud MCP) | Yes | API keys (Anthropic/OpenAI) |
| Cloud MCP (Cloudflare Worker) | Yes | Yes | API keys (Worker secrets) |

Local-first: MLX on any Apple Silicon Mac. API fallback for non-local platforms.

## Execution Order

1. Phase 1 implementation (core.ts, mcp.ts, cli.ts changes)
2. Test Phase 1 against the known failure case (recent bridge conversation)
3. Phase 2 implementation (llm.ts, search-pipeline.ts, wire into core)
4. Test Phase 2 with and without Ollama
5. Build and deploy to both targets
6. Dev update + roadmap update + PR

## Remaining Work

### Quality Tuning (high priority)

- [ ] **Score normalization** ... 100% match scores appearing. The blending math produces scores that exceed 1.0 in some cases. The rescaling factor in search-pipeline.ts needs adjustment.
- [ ] **Expansion cache persisted to DB** ... currently in-memory Map, resets each process. QMD caches expansions to DB so repeated queries across sessions are instant.
- [ ] **Reranking cache persisted to DB** ... QMD caches per-doc relevance scores. Avoids re-ranking the same docs for similar queries.

### QMD Feature Parity (medium priority)

- [ ] **Grammar-constrained output for expansion** ... QMD uses GBNF grammar to guarantee valid output format. We use prompt-based parsing which can fail on unusual LLM responses. Consider structured output (OpenAI) or tool_use (Anthropic) as alternatives.
- [ ] **Parallel context evaluation for reranking** ... QMD evaluates passages in parallel batches. We send all passages in one prompt. For large candidate sets, batched evaluation may be faster.

### Local Model Setup (medium priority)

- [ ] **MLX server setup + LaunchAgent** ... install mlx-lm, pull a model, create LaunchAgent for always-on local inference. This moves us from OpenAI API (~$0.001/search) to free, local, sovereign search.
- [ ] **Ollama chat model pull + test** ... currently only nomic-embed-text is installed. Need a chat model (e.g. qwen3:1.7b) for expansion/reranking via Ollama.

### Provider Issues (low priority)

- [ ] **Anthropic OAuth token exchange flow** ... sk-ant-oat01- tokens (from 1Password) don't work with the direct Messages API. They need an OAuth exchange flow to get a session token. Currently skipped in detection.
- [ ] **1Password as configurable setting** ... Parker said "the 1P needs to be a settings... people should be prompted to use 1P." Deferred.

### Integration (low priority)

- [ ] **Verify deep search in OC plugin context** ... the gateway process has env vars set by op-secrets plugin. Verify that the memory-crystal extension's deepSearch works in that context (it should, since it also checks op-secrets directly).
- [ ] **PR to memory-crystal-private** ... create PR for all the Phase 1 + Phase 2 changes.
- [ ] **Deploy to public repo** ... after PR is merged and tested.

---

## Critical Files

| File | Role |
|------|------|
| `src/core.ts` | Search implementation, recencyWeight, parseSince, deepSearch |
| `src/mcp-server.ts` | MCP server tool definitions (time_filter, quality params) |
| `src/cli.ts` | CLI command definitions (--since flag) |
| `src/llm.ts` | **NEW** ... provider cascade, op-secrets, query expansion, re-ranking |
| `src/search-pipeline.ts` | **NEW** ... deep search pipeline (expand, search, RRF, rerank, blend) |
| QMD `src/store.ts` | Reference: lines 2204-2321, 2806-2985 |
| QMD `src/llm.ts` | Reference: lines 936-1071 |
