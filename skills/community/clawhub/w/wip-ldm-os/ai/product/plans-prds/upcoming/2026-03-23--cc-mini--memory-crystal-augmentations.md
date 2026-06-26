# Plan: Memory Crystal Augmentations (OpenViking-inspired)

**Date:** 2026-03-23
**Author:** cc-mini (with Parker)
**Status:** Tickets filed, not started. Heavy caveats on each. Re-evaluate before implementing.

## Context

Reviewed OpenViking (Volcengine, Apache 2.0) and mapped their ideas against Dream Weaver + Memory Crystal. Four augmentation opportunities identified. None replace existing systems. All are additive.

Dream Weaver handles narrative consolidation (meaning). Crystal handles storage and search (recall). OpenViking's ideas improve efficiency and signal-to-noise at specific points in the pipeline.

## Augmentations (priority order)

### 1. Structured memory categories with merge rules (MC #59)

**What:** Upgrade Dream Weaver's 5 categories to 6 with merge vs non-merge distinction.
**Where:** `dream-weaver-protocol/prompts.ts`
**Caveat:** Might not matter if dedup (#60) handles duplicates with existing categories. Don't add taxonomy for taxonomy's sake.

### 2. Memory dedup before storing (MC #60)

**What:** Search Crystal for similar memories before storing. LLM decides: skip/merge/create.
**Where:** `memory-crystal/dream-weaver.ts` (onMemoryExtracted hook)
**Caveat:** Adds LLM cost per memory. Consider batch dedup as alternative. Start with skip-only (no merge). Better extraction might eliminate the need.

### 3. Tiered content loading L0/L1/L2 (MC #61)

**What:** Store three resolution levels per chunk. Search returns smallest useful level first.
**Where:** `memory-crystal/core.ts` (ingestion + search)
**Caveat:** Defer until Crystal relay (#163) is real. Token savings matter on iOS, not desktop. Massive backfill cost for 208K existing chunks. Try simple truncation first.

### 4. Virtual hierarchy in search (MC #62)

**What:** Navigate agent -> source_type -> date range before searching within scope.
**Where:** `memory-crystal/search-pipeline.ts`
**Caveat:** Lowest confidence. Deep search already works well. Recency tuning is a simpler fix. Crystal is fundamentally flat. Skip unless search quality degrades at scale.

## How they fit with Dream Weaver

Dream Weaver is the consolidation engine. Crystal is the storage and search layer. These augmentations touch specific points:

```
Transcripts -> Dream Weaver -> [#59: better categories] -> [#60: dedup] -> Crystal ingest -> [#61: L0/L1/L2] -> Crystal search -> [#62: hierarchy] -> Results
```

Dream Weaver's narrative output (journals, SOUL.md, IDENTITY.md, CONTEXT.md) is untouched. OpenViking has no narrative layer. That's our differentiator.

## Decision rule

Before implementing any of these: is the current system actually failing at this? If search quality is good and chunk count isn't causing problems, defer. Don't optimize for hypothetical scale.

## Notes: Supermemory Critique (2026-03-23)

Parker shared a critique of Dhravya Shah's Supermemory benchmarks. Key points and how they apply to Memory Crystal:

### What the critique says

1. **115k tokens is not "long-term memory"** — with 1M+ context windows in production, calling retrieval over 115k tokens a breakthrough is misleading.
2. **LongMemEval is outdated** — doesn't capture real agent workflows, real-time updates, noisy tool outputs, or cost/latency constraints.
3. **"99% accuracy" is sampling inflation** — 8 parallel prompts counting any correct answer as success is not improving memory, it's spray-and-pray. The 12-agent voting setup is majority voting that inflates benchmarks.
4. **"No vector DB needed" is not an unlock** — it replaces retrieval with multiple LLM passes (higher compute, latency, cost). Shifts complexity, doesn't remove it. Not production-viable.
5. **"Agentic retrieval beats vector search" is oversimplified** — the real problems are relevance filtering, temporal consistency, memory lifecycle (what to store/forget), and grounding vs hallucination. None solved.
6. **No consistency guarantees** — assumes perfect extraction during ingestion, relies on prompt engineering, no guarantees across runs.

### How this applies to Memory Crystal

| Critique | Crystal's position |
|---|---|
| Token count ≠ memory | Crystal stores 208K+ chunks across sessions/agents. Actual long-term, not context-window tricks. |
| Benchmark gaming via parallel sampling | Crystal uses a single search pipeline. No multi-prompt inflation. |
| "No vector DB" as a feature | Crystal uses vector search AND narrative consolidation (Dream Weaver). Both layers serve different purposes. Don't remove one to claim simplicity. |
| Ignoring memory lifecycle | Dream Weaver handles consolidation/narrative. Dedup (#60) addresses what to store/skip/merge. This is the real problem and we're working on it. |
| Temporal consistency | Crystal tracks timestamps, source agents, session IDs. Recency tuning is a known lever. |
| Production viability | Crystal runs locally, single search pass, no multi-agent voting overhead. Designed for real cost/latency constraints. |

### TODO: Reconcile with memory-crystal-private

There may be an existing Supermemory analysis in `wipcomputer/memory-crystal-private` (likely in `ai/` or on an unmerged branch). CC CLI should check that repo and reconcile any prior thinking with these notes. This session was scoped to `wip-ldm-os-private` only and couldn't access it.

### Takeaway for us

- Don't chase benchmark scores. Our differentiator is the narrative layer (Dream Weaver) + lifecycle management, not retrieval accuracy on synthetic benchmarks.
- The dedup work (#60) and category improvements (#59) are the right investments — they address the real problems (what to store, what to forget).
- If we ever publish benchmarks, use real agent workflows, not LongMemEval. Design our own eval that tests what actually matters: temporal consistency, cross-agent memory, lifecycle, and cost.
- "Memory solved" claims are a red flag. Memory is an ongoing systems problem, not a benchmark to clear.

## Acknowledgements

OpenViking (Apache 2.0, Volcengine): `~/wipcomputer/settings/docs/acknowledgements.md`
