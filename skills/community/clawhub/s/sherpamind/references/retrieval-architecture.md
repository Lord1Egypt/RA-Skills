# Retrieval Architecture

> SherpaDesk API reference: <https://github.com/sherpadesk/api/wiki>

## Goal

Make SherpaDesk data genuinely useful to OpenClaw, not just stored.

## Design stance

SherpaMind should use a **hybrid retrieval model**:
- **SQLite** for canonical structured truth
- **FTS / keyword search** for exact-text retrieval
- **vector retrieval** for fuzzy similarity and theme discovery

## Why this matters

OpenClaw will need to answer different kinds of questions:

### Structured questions
Examples:
- how many tickets did account X open this month?
- how long do technician Y's tickets wait for first response?
- which accounts have the highest reopen rate?

Best source:
- SQL against canonical tables

### Exact-text investigative questions
Examples:
- find tickets mentioning a specific error string
- find all incidents involving a product/version
- find tickets for an exact customer/domain/user name

Best source:
- keyword/full-text search

### Fuzzy problem-solving questions
Examples:
- have we seen something like this before?
- what past tickets look semantically similar to this new issue?
- what historical context is most relevant to this ticket?
- what differences show up in technician habits or client/technician interaction style?
- what recurring operational work should probably be formalized into scheduled service?

Best source:
- vector/semantic retrieval, ideally with SQL metadata filters layered on top

## Suggested pipeline

1. ingest canonical SherpaDesk data into SQLite
2. normalize linked entities and stable ticket/comment metadata
3. build retrieval documents from tickets, comments, accounts, users, and derived summaries
4. carry stable workflow/state metadata forward with those documents (subject cleanup, user/account/technician linkage, human-readable entity labels, label-source provenance, user/creator/technician email domains, participant email-domain rollups, recent log types, log-interaction counts/date summaries, distinct public/internal participant counts, latest/recent participant labels, mixed-visibility activity flags, next-step hints, derived action-cue text/source, explicit-followup-vs-waiting-log cue provenance, request-completion/follow-up cues, log-derived latest-response and closure cues, class/submission/resolution taxonomy, human-readable department labels, contract/confirmation context, account-location and department context, intake-channel/handling flags, project/scheduled-ticket linkage, effort-tracking signals, attachment presence plus normalized attachment extension/kind/size summaries (including size-known counts and broader kind-family counts), resolution highlights)
5. widen bounded detail enrichment in a retrieval-aware way so historical detail coverage spreads across under-covered categories/accounts/technicians instead of overfitting only to the most recent cold tickets
6. chunk long text where needed, rebalancing tiny leading/trailing leftovers when possible so vector rows stay retrieval-meaningful instead of collapsing into metadata-only fragments
7. index documents into:
   - FTS/keyword search
   - vector embeddings/index
8. expose hybrid query commands for OpenClaw/tooling

Current practical implementation now includes:
- keyword/full-text style search over references/chunks
- metadata-rich embedding-ready exports with filter-friendly ticket context, chunk-order/position sidecar fields, and inferred chunk-semantic section metadata
- a lightweight local vector index/search layer for immediate similarity retrieval without external embedding APIs

## Recommended retrieval document types

- ticket summary documents
- ticket conversation/comment chunks
- account-level factual summary documents
- user-level support history summaries
- technician-level factual summary documents

Avoid prematurely synthesizing strongly interpretive "known-fix" or theme conclusions until the retrieval layer and source coverage are strong enough to support them well.

## Important rule

Do not let the retrieval layer become the only source of truth.
Derived retrieval artifacts should be rebuildable from canonical local data.

That also means materialized docs/chunks need visible drift detection when the backend materializer changes. If metadata cleanup, chunking, or document-shape logic improves, SherpaMind should be able to detect stale derived artifacts and refresh them instead of quietly serving yesterday's retrieval shape.

Retrieval observability should also expose **materialization freshness lag** at the per-document level, not just coarse earliest/latest timestamps. Operators should be able to see how many documents are materially behind the latest ticket update, whether that lag concentrates in open versus closed tickets, which lag buckets dominate, and which concrete documents are the worst current outliers.

Retrieval observability should also expose **retrieval signal pressure** by account/category/technician so the backend can see where key prepared-signal families (detail, issue context, action cues, activity history, resolution context, attachment context) are still sparse instead of only knowing global coverage averages.

Retrieval observability should also separate **source absence** from **materialization drift** for source-backed metadata. If a field like support group, contract, location, department key, confirmation state, or a normalized email-domain facet reads as sparse, SherpaMind should make it clear whether SherpaDesk never supplied that field for the current corpus, supplied malformed values that could not be cleanly normalized, or whether the backend failed to carry it into retrieval artifacts.
