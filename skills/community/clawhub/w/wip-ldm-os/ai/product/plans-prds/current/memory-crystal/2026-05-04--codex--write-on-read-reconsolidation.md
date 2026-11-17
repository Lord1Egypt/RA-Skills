# PRD: Memory Crystal Write-On-Read Reconsolidation

**Date:** 2026-05-04
**Author:** Codex
**Status:** Product spec. No implementation in this pass.
**Product:** Memory Crystal
**Related research:**
- `ai/research/mnemos/2026-05-01--codex--mnemos-ldm-os-synthesis.md`
- `ai/product/plans-prds/current/memory-crystal/2026-04-12--cc-mini--crystal-resilience-plan.md`
- `ai/product/plans-prds/current/memory-crystal/2026-04-24--cody--memory-audit-ledger.md`

## Executive Decision

If Memory Crystal adopts one idea from the Mnemos review, it should be write-on-read reconsolidation.

Today Memory Crystal is excellent at capture, hybrid search, local storage, encryption posture, multi-device architecture, and Dream Weaver integration. The missing layer is memory dynamics: memories should not stay static after retrieval. When a memory is retrieved and used, Crystal should record that use, strengthen the memory, make it more accessible in near-term search, and connect it to memories retrieved beside it.

This PRD specifies that behavior in WIP's own architecture and vocabulary.

## Clean-Room Boundary

Mnemos is MIT-licensed public prior art. The reviewed Mnemos behavior makes the product idea clear: retrieved memories can be reconsolidated by updating access metadata, strength, stability, accessibility, and co-retrieval connections.

WIP should implement the product behavior from first principles. Do not copy Mnemos code. Do not vendor Mnemos modules. Do not translate Python functions line-by-line. Do not use MLP wire format or `MLP-compatible` language.

Allowed:
- Cite Mnemos by Riley Ralmuto as MIT prior art for memory dynamics.
- Reuse the general concepts: access tracking, strength, stability, accessibility, decay, co-retrieval edges, original-content preservation, and version/audit events.
- Write new TypeScript implementation inside Memory Crystal using existing Crystal schema, sqlite-vec, FTS5, RRF, deep search, and audit ledger patterns.

Not allowed:
- No copied source code from Mnemos.
- No Mnemos package dependency.
- No MLP envelope format.
- No ledger pointers.
- No token, Solana, IPFS, Cartouche, MLP-PLUS, MLP-ADV, or `$POLYPHONIC` surface.
- No external positioning that Memory Crystal is MLP-compatible.

Suggested attribution if implemented:

```text
Memory Crystal write-on-read reconsolidation was informed by public MIT prior art in Mnemos by Riley Ralmuto. The implementation is original WIP Computer code and does not copy Mnemos source.
Source reviewed: https://github.com/Riley-Coyote/mnemos
```

## Problem

Search currently treats memory chunks mostly as static records. A chunk can be fresh or stale by timestamp, and it can rank higher or lower by BM25, vector similarity, RRF, recency, and LLM reranking. But the act of retrieval does not become part of memory.

That misses a core signal: a memory that keeps getting retrieved in useful contexts is probably important. A memory retrieved alongside another memory may be related even if that relation was not known at ingestion time. A memory that has not been used in months should become less accessible without being deleted. A memory used repeatedly across different sessions should become more stable.

The product version: Memory Crystal should learn from what gets used.

## Goals

1. Make retrieved memories become stronger and more searchable over time.
2. Add explicit access tracking for chunks and structured memories.
3. Add a small, explainable memory-dynamics model: strength, stability, accessibility.
4. Add co-retrieval connections between chunks that repeatedly appear together.
5. Preserve original captured content. Reconsolidation must never rewrite raw transcript text.
6. Emit audit events so memory mutation is inspectable.
7. Keep the behavior local-first, deterministic enough to test, and cheap enough to run on every search.

## Non-Goals

- Do not change raw transcript archives.
- Do not mutate `chunks.text`.
- Do not re-embed chunks on every read.
- Do not introduce a new vector database.
- Do not implement Mnemos as a package or import its code.
- Do not add protocol conformance to MLP or any crypto-linked memory standard.
- Do not create a public portability protocol in this phase.
- Do not model every claim as a belief.

## User Experience

The user should not have to think about reconsolidation. Search should just get better.

Expected visible effects:
- Frequently useful memories stay easy to find.
- Recently used project context remains accessible even if the original source is older.
- Old, unused memory still exists, but stops crowding top results.
- Related memories begin clustering because they were repeatedly retrieved together.
- `crystal search --explain` can show that a result was boosted by usage, stability, or graph connection.
- `crystal status` or a future `crystal dynamics status` can report reconsolidation health without exposing private text.

## Existing Crystal Fit

This should extend current Memory Crystal rather than replace it.

Current strengths to keep:
- `chunks` is the source table for searchable captured content.
- `chunks_vec` remains sqlite-vec vector search.
- `chunks_fts` remains FTS5 keyword search.
- Hybrid search remains BM25 plus vector plus RRF.
- Deep search remains query expansion plus LLM rerank plus blending.
- Recency weighting remains part of ranking, but becomes one signal beside accessibility.
- The audit ledger plan remains the right place for metadata about mutation events.

## Proposed Data Model

### Chunk Dynamics Columns

Add nullable or defaulted columns to `chunks`:

| Column | Type | Default | Meaning |
|---|---:|---:|---|
| `last_accessed_at` | TEXT | null | Last time this chunk appeared in returned search results and was reconsolidated |
| `access_count` | INTEGER | 0 | Number of reconsolidated accesses |
| `reconsolidation_count` | INTEGER | 0 | Number of times dynamics were updated |
| `strength` | REAL | 0.5 | Storage strength. Builds with use and deep encoding |
| `stability` | REAL | 0.1 | Resistance to decay. Builds slowly with repeated use and graph connectivity |
| `accessibility` | REAL | 0.5 | Current retrievability. Moves quickly with recency, usage, and decay |
| `dynamics_updated_at` | TEXT | null | Last write by reconsolidation or decay |

Defaults should be conservative. Existing chunks should backfill lazily on first read or via migration.

### Original Content Boundary

For `chunks`, original content is already the raw searchable text. Do not mutate `chunks.text`.

If later we add evolved summaries or impact fields, store them separately:

| Column or table | Meaning |
|---|---|
| `chunk_annotations.current_summary` | Optional evolved summary |
| `chunk_annotations.impact` | Why this memory mattered |
| `chunk_annotations.original_chunk_id` | Stable link back to raw chunk |

Phase 1 should not add these annotations unless needed. The first slice can be pure dynamics.

### Co-Retrieval Connections

Add a table for chunk-to-chunk memory graph edges:

```sql
CREATE TABLE IF NOT EXISTS chunk_connections (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_chunk_id INTEGER NOT NULL REFERENCES chunks(id) ON DELETE CASCADE,
  target_chunk_id INTEGER NOT NULL REFERENCES chunks(id) ON DELETE CASCADE,
  relation TEXT NOT NULL DEFAULT 'co_retrieved',
  strength REAL NOT NULL DEFAULT 0.1,
  formed_by TEXT NOT NULL DEFAULT 'retrieval',
  formed_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  access_count INTEGER NOT NULL DEFAULT 1,
  UNIQUE(source_chunk_id, target_chunk_id, relation)
);
```

Direction is not semantically important for `co_retrieved`, but storing directed rows keeps future relation types simple. Either write both directions or normalize `(min_id, max_id)` behind helper functions. The implementation should choose one convention and enforce it.

Initial relation vocabulary:

| Relation | Meaning | Written by |
|---|---|---|
| `co_retrieved` | Returned in the same search result set | Search reconsolidation |
| `same_source` | Same transcript, file, or manual memory source | Optional backfill |
| `same_session` | Same conversation session | Optional backfill |
| `dream_weaver_related` | Dream Weaver identified relation | Later phase |
| `supports` | Explicit semantic support | Later phase |
| `contradicts` | Explicit semantic contradiction | Later phase |

Phase 1 only needs `co_retrieved`.

## Retrieval Flow

### Current Flow

1. Query FTS5 and sqlite-vec.
2. Fuse with RRF.
3. Apply recency weighting.
4. Optionally deep-search with expansion and rerank.
5. Return top results.

### New Flow

1. Query FTS5 and sqlite-vec.
2. Fuse with RRF.
3. Apply recency and accessibility weighting.
4. Optionally deep-search with expansion and rerank.
5. Return top results.
6. Reconsolidate returned chunk IDs after the result set is chosen.
7. Emit audit events for reconsolidation writes.

Reconsolidation should happen after ranking, not before ranking, for the current query. The current query should not boost itself mid-flight.

## Ranking Changes

Add a dynamics weight after RRF and before normalization:

```text
dynamics_weight =
  0.70
  + 0.20 * accessibility
  + 0.07 * strength
  + 0.03 * stability
```

Then:

```text
score = base_rrf_score * recency_weight * dynamics_weight
```

This keeps dynamics useful but bounded. A highly used memory should not beat an obviously irrelevant memory. The lexical and vector layers still decide candidate relevance.

For Phase 1, cap total dynamics influence:

```text
0.70 <= dynamics_weight <= 1.00
```

Later, graph-aware expansion can add candidate discovery through `chunk_connections`, but Phase 1 should only reweight candidates already found by existing search.

## Reconsolidation Write

For each returned chunk that is eligible:

1. Set `last_accessed_at` to now.
2. Increment `access_count`.
3. Increment `reconsolidation_count`.
4. Increase `strength` by a small capped amount.
5. Increase `stability` by a smaller capped amount.
6. Raise `accessibility` to at least a configurable floor.
7. Create or strengthen `co_retrieved` edges with other returned chunks.
8. Write one audit event.

Suggested initial constants:

| Config key | Initial value | Purpose |
|---|---:|---|
| `reconsolidation.enabled` | false | Feature flag |
| `reconsolidation.resultLimit` | 10 | Only update top N returned chunks |
| `reconsolidation.strengthDelta` | 0.03 | Retrieval rehearsal boost |
| `reconsolidation.stabilityDelta` | 0.005 | Slower durability boost |
| `reconsolidation.accessibilityFloor` | 0.70 | Freshly used memories become findable |
| `reconsolidation.connectionDelta` | 0.05 | Co-retrieval edge boost |
| `reconsolidation.maxWritesPerSearch` | 20 | Protect hot search loops |

Do not tune these as if they are neuroscience. They are product heuristics. Keep them explainable and adjust by measurement.

## Decay Pass

Reconsolidation needs decay or everything eventually becomes important.

Add a scheduled or manual decay pass:

```text
effective_decay = decay_rate * exp(-stability_factor * stability)
accessibility = accessibility * exp(-effective_decay * age_hours)
strength = strength - strength * (1 - exp(-effective_decay * 0.1 * age_hours))
```

Recommended initial values:

| Config key | Initial value |
|---|---:|
| `decay.enabled` | false |
| `decay.rate` | 0.01 |
| `decay.stabilityFactor` | 3.0 |
| `decay.batchSize` | 5000 |
| `decay.minAccessibility` | 0.05 |
| `decay.strengthFloor` | 0.05 |

Do not delete decayed chunks. Lower accessibility only changes ranking. Forgetting and deletion remain explicit user-controlled operations.

Special floors:
- Manual `crystal_remember` memories should have a higher minimum accessibility than raw chunks.
- Active project context can have a temporary floor while the project is active.
- User-stated preferences should not decay below a safety threshold unless superseded or forgotten.

## Audit Events

Integrate with the Memory Crystal audit ledger plan.

Reconsolidation event:

```json
{
  "time": "2026-05-04T18:12:00Z",
  "event": "memory.reconsolidated",
  "chunk_id": 123,
  "source_type": "openclaw-session-jsonl",
  "source_id": "019...",
  "agent_id": "cc-mini",
  "query_hash": "sha256:...",
  "result_rank": 3,
  "strength_before": 0.5,
  "strength_after": 0.53,
  "stability_before": 0.1,
  "stability_after": 0.105,
  "accessibility_before": 0.42,
  "accessibility_after": 0.70,
  "co_retrieved_count": 4,
  "schema_version": 1
}
```

Rules:
- Do not write raw query text to the audit event. Store `query_hash`.
- Do not write raw chunk text.
- Event write failure should not break search.
- Repeated searches in tight loops should coalesce events or obey write limits.

## Concurrency And Performance

Write-on-read introduces writes into search. That is the biggest engineering risk.

Rules:
- Keep the returned search path fast. Results should be available before or independent from reconsolidation writes.
- Use SQLite transactions for batch updates.
- Use WAL mode as today.
- Put reconsolidation behind a feature flag.
- Limit writes per search.
- Consider async or deferred reconsolidation if MCP latency regresses.
- Avoid write-on-read on read-only mirror nodes unless the node can sync dynamics back to Core safely.

Core/Node rule:
- Crystal Core owns dynamics mutation.
- Crystal Nodes may read dynamics fields from mirrored chunks.
- Nodes should not independently mutate dynamics in Phase 1, because that creates split-brain usage signals.

If Node-local usage matters later, sync usage events to Core as append-only metadata and let Core apply them.

## Privacy And Security

This feature must preserve Memory Crystal's sovereignty posture.

- No cloud dependency.
- No public protocol.
- No ledger.
- No token.
- No external attestation service.
- No raw text in audit events.
- No raw query text in audit events.
- No new API keys.
- No provider calls solely for reconsolidation.

## Implementation Phases

### Phase 0: Schema And Flag

- Add migration for dynamics columns on `chunks`.
- Add `chunk_connections`.
- Add config flags, default off.
- Add `crystal dynamics status` or extend `crystal status` with dynamics counters.

Acceptance:
- Existing databases migrate without re-embedding.
- Existing search results are unchanged when the feature flag is off.
- `crystal doctor` can report whether dynamics schema exists.

### Phase 1: Reconsolidate Search Results

- Add post-search reconsolidation for top N results.
- Update access metadata, strength, stability, accessibility.
- Add or strengthen `co_retrieved` edges.
- Emit redacted audit events.

Acceptance:
- A search increments `access_count` for returned chunks when enabled.
- Repeated retrieval increases strength and accessibility up to caps.
- Co-retrieved chunks create one stable edge per pair.
- Search latency increase stays under 10 percent for typical result sets.

### Phase 2: Dynamics-Aware Ranking

- Add `dynamics_weight` into fast search and deep search scoring.
- Add `--explain` fields: `strength`, `stability`, `accessibility`, `dynamics_weight`.
- Keep candidate generation unchanged.

Acceptance:
- Existing strong lexical matches still win.
- Repeatedly useful memories rise within relevant candidate sets.
- Explain output makes the boost visible.

### Phase 3: Decay Pass

- Add `crystal dynamics decay --dry-run`.
- Add scheduled Core-only decay option.
- Decay accessibility and strength, resisted by stability.
- Do not delete chunks.

Acceptance:
- Dry run shows changed counts and averages.
- Active, recently used memories decay slower.
- Manual memories and active project context respect configured floors.

### Phase 4: Graph-Aware Retrieval

- Use `chunk_connections` to add related candidates after FTS/vector seed retrieval.
- Keep graph expansion shallow and bounded.
- Add relation-type weights only after enough data exists.

Acceptance:
- Related memories surface when directly relevant seed chunks are found.
- Graph expansion does not swamp lexical and vector relevance.
- Explain output shows graph contribution.

## Test Plan

Unit tests:
- Migration adds dynamics fields without dropping data.
- Reconsolidation increments counters and caps values.
- Co-retrieval edge insert is idempotent and strengthens existing edges.
- Decay lowers accessibility for unused chunks.
- Decay respects floors.
- Feature flag off means no writes.

Integration tests:
- Search with flag on returns same visible results as before on first query.
- Second repeated query shows updated dynamics fields.
- Deep search explain includes dynamics fields.
- Core/Node mirror import preserves dynamics fields but Node mutation is disabled.

Performance tests:
- Search latency before and after reconsolidation on 10k, 100k, and 500k chunks.
- Write amplification per search.
- WAL growth under repeated searches.

Privacy tests:
- Audit events contain no raw query text.
- Audit events contain no raw chunk text.
- Export and manifest outputs do not leak private content.

## Metrics

Track:
- Average search latency with dynamics off and on.
- Reconsolidation writes per day.
- Average accessibility by source type.
- Percent of chunks never accessed.
- Top co-retrieval pairs.
- Query repeat success: whether repeated work sessions find the same project context faster.
- User correction rate after search: if users say "not that" less often, dynamics is helping.

## Open Questions

1. Should `crystal_remember` structured memories get separate dynamics fields, or should their backing chunks be enough for Phase 1?
2. Should dynamic usage be mirrored to Nodes as part of chunk delta sync or as a separate metadata delta?
3. Should Dream Weaver produce `impact` annotations for frequently accessed chunks?
4. What is the right minimum accessibility for explicit user preferences?
5. Should private-mode searches skip reconsolidation writes, or is local-only metadata acceptable?

## Recommendation

Build this as the next Memory Crystal product slice after the current reliability and audit-ledger foundations.

The first implementation should be deliberately small:
- schema fields
- feature flag
- post-search access updates
- co-retrieval edges
- explain output
- audit events

Do not start with graph-aware retrieval or Dream Weaver annotations. Those are valuable, but the first milestone is proving that Memory Crystal can learn from retrieval without harming search quality, latency, privacy, or the Core/Node sync model.

## Bottom Line

Memory Crystal is already ahead as a sovereign memory product. Mnemos points to one narrow layer we should add: living memory dynamics.

The WIP implementation should be original code. The idea is simple and strong: every useful retrieval should leave a trace. Memories that matter become easier to reach. Memories that stop mattering fade in accessibility but remain owned, searchable, and recoverable.
