# QMD v2.0 Analysis: What's New Since Our Last Review

**Date:** 2026-03-15
**Author:** CC-Mini
**Previous analysis:** `2026-03-09--cc-mini--qmd-v1.1.6-analysis-and-recommendations.md`
**Context:** QMD jumped from v1.1.6 (our last review) to v2.0.1. Major version bump. Our fork is at v1.1.6. Upstream is at v2.0.1.

---

## What Changed in QMD v2.0

### New in v2.0.0 (2026-03-10)

1. **Stable SDK API with `QMDStore` interface.** Search, retrieval, collection/context management, indexing, lifecycle. This is what v1.1.6 started (SDK mode). v2.0 declares it stable and makes it the primary interface.

2. **Unified `search()`.** Pass `query` for auto-expansion or `queries` for pre-expanded lex/vec/hyde. Replaces the old query/search/structuredSearch split. One method, two modes.

3. **New `getDocumentBody()`** for retrieving full document content by ID.

4. **New `getDefaultCollectionNames()`** for listing which collections are searched by default.

5. **`Maintenance` class.** Clean API for database cleanup:
   - `vacuum()` ... VACUUM the database
   - `cleanupOrphanedContent()` ... remove unreferenced content rows
   - `cleanupOrphanedVectors()` ... remove vectors for deleted content
   - `clearLLMCache()` ... wipe expansion/reranking cache
   - `deleteInactiveDocs()` ... remove filesystem-deleted documents
   - `clearAllEmbeddings()` ... force re-embed

   **This is exactly what we built with `crystal cleanup`.** QMD's Maintenance class does the same orphan cleanup we shipped in v0.7.8. Independent convergence.

6. **MCP server rewritten as SDK consumer.** Zero internal store access. Clean separation.

7. **Runtime-aware bin wrapper.** Detects bun vs node to avoid ABI mismatches.

8. **better-sqlite3 bumped to ^12.4.5** for Node 25 support.

### New in v2.0.1 (2026-03-10)

1. **`qmd skill install`** copies the QMD skill into `~/.claude/commands/` for one-command setup.
2. Fixes for Qwen3-Embedding GGUF filename case and symlinked global paths.

### Recap: What v1.1.2-v1.1.6 Added (from our previous analysis)

| Feature | Version | Our Status |
|---------|---------|------------|
| Intent parameter | v1.1.5 | NOT ported. Roadmap Priority 8b. |
| Structured search (pre-expanded queries) | v1.1.0 | NOT ported. Roadmap Priority 8b. |
| Score traces / explain mode | v1.1.2 | NOT ported. Roadmap Priority 8b. |
| Content-addressable reranker cache | v1.1.2 | NOT ported. Planned in Phase 3 as persistent cache. |
| Parallel reranking with VRAM cap | v1.1.2 | NOT needed (we use API, not local model for reranking). |
| Lex syntax (negation, phrases) | v1.1.0 | NOT ported. Low priority. |
| Collection management (ignore, include/exclude) | v1.1.0-v1.1.2 | PARTIAL. We have sources add/sync but deprecated raw scanning. |
| Custom embedding model (env var) | v1.1.5 | NOT ported. We support 3 providers but no per-model override. |
| HTTP MCP transport | v1.1.2 | NOT ported. Low priority. |
| SDK/Library mode | v1.1.6 | NOT ported. Our MCP serves this role. |
| GPU autoAttempt (node-llama-cpp) | v1.1.2 | NOT applicable. We use API providers, not local GGUF models. |
| Multilingual embeddings | v1.1.2 | NOT needed yet. |
| Configurable expansion context size | v1.1.2 | NOT ported. We use API, not local context windows. |
| candidateLimit exposed | v1.1.2 | NOT ported. Hardcoded at 40 in search-pipeline.ts. |

---

## What We Already Have That QMD v2.0 Independently Built

| Feature | Memory Crystal | QMD v2.0 |
|---------|---------------|----------|
| Orphan cleanup | `crystal cleanup` (v0.7.8) | `Maintenance.cleanupOrphanedContent/Vectors()` |
| DELETE trigger | Cascading trigger on chunks table (v0.7.8) | Not mentioned (cleanup is manual) |
| Score normalization | Relative normalization, top=95% (v0.7.19) | Not mentioned (still raw scores?) |
| Recency weighting | Exponential decay, floor 0.3 | QMD still doesn't have this |
| Multi-agent support | agent_id per chunk | Single user |
| Privacy controls | Private mode kill switch | None |
| Relay/sync | Core/Node, encrypted relay | Single machine |

**We're ahead on the data model.** QMD is a file indexer. Memory Crystal is a conversation memory system. Our advantages (recency, multi-agent, privacy, relay) are architectural, not feature gaps.

---

## What We Should Port from QMD v2.0

### Already Planned (from v1.1.6 analysis, still valid)

1. **Intent parameter** ... highest value for conversational search. "What did Parker say about security" needs disambiguation.

2. **Persistent expansion/reranking cache** ... already in our Phase 3 plan. QMD's `llm_cache` table keyed by content hash confirms the approach.

3. **Structured search API** ... let agents skip LLM expansion when they already know what they want.

4. **Explain mode / score traces** ... debugging tool for search quality issues. Lesa found the 100% scoring bug through usage. Explain mode would have caught it earlier.

### New from v2.0 (not in our previous analysis)

5. **Maintenance class pattern.** We built `cleanOrphans()` as a method on Crystal. QMD formalized it as a separate `Maintenance` class with clean methods. Our implementation is functional but the class pattern is cleaner for future operations (cache clear, re-embed, inactive doc cleanup).

6. **Unified search() with query vs queries.** QMD's v2.0 search accepts either a string (auto-expands) or an array of pre-expanded queries. This is cleaner than having separate `search()` and `structuredSearch()` methods. We could adopt the same pattern: `crystal.search("query")` auto-expands, `crystal.search({ queries: [...] })` skips expansion.

7. **`qmd skill install`** copying the skill to `~/.claude/commands/`. We have SKILL.md on wip.computer, but QMD also installs it locally. Worth considering for offline access.

8. **candidateLimit as parameter.** Our pipeline hardcodes `RERANK_CANDIDATE_LIMIT = 40`. QMD exposes it as a CLI flag and MCP param. Useful for tuning: more candidates = better recall but slower reranking.

### NOT worth porting

- **SDK/Library mode.** Our MCP server + Crystal class already serves this role. No need for a separate SDK layer.
- **Runtime-aware bin wrapper (bun vs node).** We only support node.
- **GPU/VRAM management.** We use API providers, not local GGUF models (until Phase 3 MLX, which is different).
- **Collection management improvements.** We deprecated raw file scanning. Conversations only.
- **HTTP MCP transport.** Not needed for our use case.
- **WSL path detection.** macOS only.

---

## Updated Priority List (combining v1.1.6 analysis + v2.0 review)

| Priority | Feature | Source | Effort | Value |
|----------|---------|--------|--------|-------|
| 1 | **Persistent cache** | v1.1.2 + Phase 3 plan | Low | High |
| 2 | **Intent parameter** | v1.1.5 | Medium | High |
| 3 | **Unified search (query vs queries)** | v2.0.0 | Low | Medium-High |
| 4 | **Explain mode / score traces** | v1.1.2 | Medium | Medium-High |
| 5 | **candidateLimit as parameter** | v1.1.2/v2.0 | Low | Medium |
| 6 | **Lex syntax (negation, phrases)** | v1.1.0 | Low | Medium |
| 7 | **Maintenance class refactor** | v2.0.0 | Low | Low (ours works) |

Items 1-2 are already in the Phase 3 plan. Items 3-6 are new additions worth tracking. Item 7 is a code quality improvement, not a feature.

---

## What Memory Crystal Has That QMD Will Never Have

These are our moat. QMD is a developer tool for indexing codebases. Memory Crystal is sovereign memory infrastructure for AI agents.

1. **Conversation-first.** Every chunk is a conversation turn with context, role, agent ID, and timestamps. QMD chunks files.
2. **Recency matters.** What Parker said yesterday matters more than what he said a month ago. QMD treats all content equally.
3. **Multi-agent.** Two agents share one database, tagged separately. QMD is single-user.
4. **Relay/sync.** Core/Node architecture with encrypted relay. QMD is single-machine.
5. **Dream Weaver.** Narrative consolidation. QMD has no equivalent.
6. **Privacy controls.** Kill switch for capture. QMD has no private mode.
7. **Install flow.** SKILL.md + agent.txt + dogfooding. QMD installs as a developer tool.

---

## Action Items

1. Update Phase 3 plan to include intent parameter and unified search API
2. Add candidateLimit as configurable param (quick win)
3. Consider adding explain mode to crystal_search MCP tool
4. Update the fork to v2.0.1 for reference (don't merge, just track)
5. Update roadmap with new priorities from this analysis
