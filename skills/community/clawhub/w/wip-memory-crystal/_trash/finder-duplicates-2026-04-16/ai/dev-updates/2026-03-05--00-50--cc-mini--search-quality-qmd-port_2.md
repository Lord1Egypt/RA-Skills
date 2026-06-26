# Dev Update: Search Quality ... QMD Port + Recency Fix

**Date:** 2026-03-05 00:50 PST
**Agent:** CC-Mini
**Session:** Search quality improvement after v0.6.0 consolidation

---

## What Happened

### Problem

After consolidating 3 memory stores into 1 crystal.db (207K chunks), search quality degraded. Recent content got buried by older semantically similar content. Lesa couldn't find the bridge conversation from minutes ago. The recency weight (linear decay, floor 0.5, ~50 days) was too weak for a corpus this size.

### Phase 1: Recency Fix (no new dependencies)

1. **Exponential recency decay** in `recencyWeight()` (core.ts)
   - Old: `Math.max(0.5, 1.0 - ageDays * 0.01)` ... linear, floor 0.5, ~50 days
   - New: `Math.max(0.3, Math.exp(-ageDays * 0.1))` ... exponential, floor 0.3, half-life ~7 days
   - Day 0: 1.0, Day 1: 0.90, Day 7: 0.50, Day 14: 0.3 (floor)

2. **Time-filtered search** ... `--since` flag on CLI, `time_filter` on MCP
   - Accepts relative ("24h", "7d", "30d") or ISO dates
   - Applied as SQL WHERE on both FTS and vector searches
   - `crystal search "query" --since 24h` returns only recent results

3. **Tiered RRF weights** ... BM25 gets 2x weight (was equal 1.0/1.0, now 2.0/1.0)

4. **More candidates** ... fetchLimit increased from `limit * 3, min 30` to `limit * 5, min 50`

### Phase 2: QMD Port (query expansion + LLM re-ranking)

Ported QMD's LLM-powered search features (MIT License, Tobi Lutke).

**New files:**
- `src/llm.ts` ... LLM provider cascade + query expansion + re-ranking
- `src/search-pipeline.ts` ... deep search pipeline (expand, multi-path search, RRF, rerank, blend)

**Features implemented:**
- **Query expansion** ... generates 3 search variations (lexical, vector-optimized, HyDE) via LLM
- **Strong signal detection** ... BM25 probe before expanding. If top score >= 0.85 with gap >= 0.15, skip expansion (saves latency)
- **LLM re-ranking** ... top 40 candidates re-ranked by relevance via LLM
- **Position-aware score blending** ... top 3: 75% RRF + 25% reranker, 4-10: 60/40, 11+: 40/60

**LLM Provider Cascade:**

| Priority | Provider | Cost | Status |
|----------|----------|------|--------|
| 1 | MLX (local Apple Silicon) | Free | Not yet installed |
| 2 | Ollama (local) | Free | Needs chat model pulled |
| 3 | OpenAI API (via 1Password) | ~$0.001/search | Working |
| 4 | Anthropic API | ~$0.001/search | OAuth tokens need exchange flow |
| 5 | None | Free | Falls back to Phase 1 |

API keys retrieved from 1Password via SA token (`getOpSecret()` in llm.ts). No env vars needed for CLI usage.

**Deep search is the default.** No `--deep` flag needed. If an LLM provider is available, expansion + re-ranking happens automatically. If not, falls back to Phase 1 silently.

### Key Design Decision: Deep as Default

Parker's feedback: "I have to do --deep? I don't get it." Changed from opt-in to default. `crystal search "anything"` now runs the full pipeline. `crystal_search` MCP tool does the same. The only opt-out is `crystal.search()` (the standard method) which still exists for programmatic use.

---

## Results

| Metric | Before | After |
|--------|--------|-------|
| Recency curve | Linear, floor 0.5, ~50d | Exponential, floor 0.3, half-life 7d |
| BM25 weight | 1.0x (equal with vector) | 2.0x (keyword matches dominate) |
| Candidate pool | limit*3, min 30 | limit*5, min 50 |
| Query expansion | None | 3 LLM-generated variations per query |
| Re-ranking | None | LLM re-ranks top 40 candidates |
| Time filter | None | --since 24h/7d/30d on CLI, time_filter on MCP |
| LLM provider | N/A | Cascade: MLX > Ollama > OpenAI > Anthropic > none |
| Deep search | N/A (opt-in) | Default for CLI + MCP |

---

## Files Changed

| File | Changes |
|------|---------|
| `src/core.ts` | recencyWeight(), parseSince(), search() filter, deepSearch() method, fetchLimit, RRF weights |
| `src/mcp-server.ts` | time_filter + quality params on crystal_search, deep as default |
| `src/cli.ts` | --since flag, deep as default |
| `src/llm.ts` | **NEW** ... provider cascade, op-secrets integration, query expansion, re-ranking |
| `src/search-pipeline.ts` | **NEW** ... deep search pipeline (expand, search, RRF, rerank, blend) |

---

## What's Still in the Plan

The plan at `ai/product/plans-prds/current/search-quality-qmd-port.md` needs updating. Items that are done vs remaining:

**Done:**
- [x] Exponential recency decay
- [x] Time-filtered search (--since / time_filter)
- [x] Tiered RRF weights (2.0/1.0)
- [x] More candidates (limit*5, min 50)
- [x] LLM provider cascade (MLX > Ollama > OpenAI > Anthropic > none)
- [x] Query expansion (3 variations: lex, vec, hyde)
- [x] Strong signal detection (BM25 probe, skip expansion if obvious match)
- [x] LLM re-ranking (top 40 candidates)
- [x] Position-aware score blending (75/60/40 RRF weight by rank)
- [x] Deep as default (no flags needed)
- [x] Op-secrets integration for API keys

**Remaining / needs review:**
- [ ] Grammar-constrained output for expansion (QMD uses GBNF grammar, we use prompt-based)
- [ ] Expansion cache persisted to DB (currently in-memory, resets each process)
- [ ] Reranking cache persisted to DB (QMD caches per-doc scores)
- [ ] MLX server setup + LaunchAgent for always-on
- [ ] Ollama chat model pull + test
- [ ] Anthropic OAuth token exchange flow (sk-ant-oat01- tokens don't work with direct API)
- [ ] Verify deep search works in OC plugin context (gateway process has env vars)
- [ ] Score normalization (100% match scores appearing ... blending math may need tuning)

---

## What's Next

- Update the plan in `plans-prds/current/` to reflect what's done vs remaining
- PR to memory-crystal-private
- Deploy to public repo
- Install MLX + pull a local model for free, fast, sovereign search
- Tune the score blending (100% match scores suggest the rescaling factor needs adjustment)
