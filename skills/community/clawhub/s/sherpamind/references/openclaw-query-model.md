# OpenClaw Query Model

## Goal

Make SherpaMind naturally usable from OpenClaw for open-ended questions without forcing the LLM to reverse-engineer raw SherpaDesk payloads every time.

## Runtime stance

SherpaMind’s background syncing/enrichment should come from its local Python backend service.
OpenClaw’s job is to query, inspect, compare, summarize, and reason over SherpaMind outputs — not to burn tokens on acting like the periodic backend scheduler.

OpenClaw should be able to answer questions like:
- how does one technician's ticket handling differ from another's?
- what habits show up in client-versus-technician voice on a given account?
- what recurring work should likely become proactive or scheduled?

Those remain query-time reasoning problems over prepared history, not backend-side canned dashboards.

## Current local data layers

### 1. Canonical structured tables
Use for exact facts, counts, filters, state, and time-based analysis:
- `accounts`
- `users`
- `technicians`
- `tickets`
- `ticket_details`
- `ticket_attachments` (metadata only; no blob download by default)
- `ticket_logs`
- `ticket_time_logs`
- `sync_state`
- `ingest_runs`

The `accounts`, `users`, and `technicians` tables may include stable ticket-observed stub rows when the standalone entity endpoints do not cover everything exposed in ticket history. That is intentional backend cleanup so account/user/technician filters and summaries stay human-readable instead of falling back to raw numeric IDs.

### 2. Materialized retrieval documents
Use for natural-language recall and fuzzy investigation:
- `ticket_documents`
- `ticket_document_chunks`

These are derived from canonical tables and are **replaceable caches**, not source-of-truth memory.

### 3. Public markdown artifacts
Use for quick human/agent inspection under `.SherpaMind/public/docs/`, including:
- `index.md`
- `insight-snapshot.md`
- `retrieval-readiness.md`
- `stale-open-tickets.md`
- `recent-account-activity.md`
- `recent-technician-load.md`
- `accounts/index.md`
- `technicians/index.md`
- `tickets/index.md`
- `runtime/status.md`

These are generated/replaced artifacts, not append-only memory files.

## How OpenClaw should reason about SherpaMind data

### For exact questions
Examples:
- how many tickets does account X have?
- how many open tickets exist right now?
- which technician has the highest recent load?
- which tickets have the most attachments?

Best path:
- structured analysis commands or direct SQL-backed analysis functions

### For fuzzy/support-history questions
Examples:
- have we seen a problem like this before?
- what kinds of issues keep happening for account X?
- which tickets mention printer issues and what happened?

Best path:
- search materialized ticket documents/chunks first
- then drill into structured rows or enriched ticket details as needed

## Staleness rule for derived artifacts

OpenClaw-facing NL artifacts must never become unmanaged side files.

Rules:
- canonical truth lives in structured SQLite tables
- materialized references/chunks/public snapshots are derived caches
- when a ticket changes, regenerate its references/chunks/artifacts by stable identity
- replace old references/chunks for that ticket
- delete stale chunks that no longer belong to the current materialization
- when per-account, per-technician, or per-ticket public docs are regenerated, remove stale entity docs that no longer belong to the current dataset-derived entity set

This prevents old stale natural-language support artifacts from lingering after ticket updates.

## Attachment rule

By default, SherpaMind stores **attachment metadata only**:
- attachment id
- filename
- URL/reference
- size
- recorded/upload timestamp

Do **not** auto-download attachment bodies by default.
Possible future exception:
- explicitly targeted screenshot/image retrieval for specific tickets when visual context is genuinely needed

## Current OpenClaw-friendly command surface

### Service/lifecycle commands
- `python3 scripts/run.py doctor`
- `python3 scripts/run.py service-status`
- `python3 scripts/run.py service-run-once`
- `python3 scripts/run.py backfill-technician-stubs`
- `python3 scripts/run.py generate-public-snapshot`

### Structured insight commands
- `python3 scripts/run.py insight-snapshot`
- `python3 scripts/run.py report-enrichment-coverage` (now includes detail-gap pressure across under-covered accounts/categories/technicians so enrichment breadth can be inspected directly)
- `python3 scripts/run.py report-ticket-counts`
- `python3 scripts/run.py report-status-counts`
- `python3 scripts/run.py report-priority-counts`
- `python3 scripts/run.py report-technician-counts`
- `python3 scripts/run.py report-ticket-log-types`
- `python3 scripts/run.py report-attachment-summary`
- `python3 scripts/run.py open-ticket-ages`
- `python3 scripts/run.py recent-account-activity`
- `python3 scripts/run.py recent-technician-load`
- `python3 scripts/run.py ticket-summary "<ticket-id|ticket-number|ticket-key>"`

### Retrieval-oriented commands
- `python3 scripts/run.py materialize-ticket-docs`
- `python3 scripts/run.py search-ticket-docs "printer"`
- `python3 scripts/run.py search-ticket-docs "printer" --account "<account>" --status Open --department "<department>"`
- `python3 scripts/run.py search-ticket-chunks "printer"`
- `python3 scripts/run.py search-ticket-chunks "printer" --priority High --category Hardware --class-name "<class>"`
- `python3 scripts/run.py search-vector-index "printer"`
- `python3 scripts/run.py search-vector-index "printer" --account "<account>" --status Open`
- `python3 scripts/run.py search-vector-index "printer" --technician "<technician>" --priority High --category Hardware`
- `python3 scripts/run.py search-vector-index "printer" --department "<department>" --class-name "<class>" --submission-category "<channel>" --resolution-category "<resolution>"`
- `python3 scripts/run.py report-vector-index-status`
- `python3 scripts/run.py report-retrieval-readiness`
- `python3 scripts/run.py export-ticket-docs`
- `python3 scripts/run.py export-embedding-chunks`
- `python3 scripts/run.py export-embedding-manifest`
- `python3 scripts/run.py generate-public-snapshot`
- `python3 scripts/run.py generate-runtime-status`

## Design rule

Do not force the LLM to parse raw SherpaDesk JSON blobs unless necessary.
Whenever a field becomes operationally useful more than once, promote it into:

SherpaMind should also expose enough observability that OpenClaw can trust the retrieval layer before leaning on it heavily. In practice that means coverage/freshness/readiness outputs should make it easy to see:
- how much of the corpus has detail enrichment
- whether ticket references/chunks cover the full ticket set
- whether important retrieval metadata (category, class/submission/resolution taxonomy, cleaned subject, issue summary, stable ticket identifiers, technician/creator contact context, normalized user/creator/technician email domains, participant email-domain rollups, waiting/age timing signals, next-step hints, derived action cues, explicit-followup vs waiting-log cue provenance, follow-up/request-completion cues, log-derived latest-response and closure cues, log-interaction counts/date summaries, participant-count/name visibility metadata, confirmation/contract context, account-location and human-readable department context, intake-channel/handling flags, project/scheduled-ticket linkage, effort-tracking signals, recent log types, resolution summary, attachment presence, normalized attachment extensions/kinds, attachment total-size signals, attachment size-known coverage, and broader attachment kind-family counts) is materially populated
- whether low coverage on source-backed metadata reflects real upstream absence in SherpaDesk payloads, malformed upstream values that cannot be cleanly normalized (for example broken email strings that cannot yield a domain), versus a backend promotion/materialization gap
- whether account/user/technician labels are arriving as human-readable names versus raw-ID fallbacks so metadata filters stay clean
- explicit entity-label quality summaries showing readable-vs-identifier-like label ratios and fallback-source pressure for account/user/technician/department facets
- whether participant metadata is materially populated enough to reason later about who is speaking publicly vs internally on a ticket without the backend inventing narrative
- which accounts/categories/technicians are still metadata-poor across key retrieval signals (detail, issue/action/activity/resolution/attachment context) so enrichment work can target the thinnest high-value slices first
- whether chunk sizes and chunk fanout per document look sane for vector/semantic use
- whether embedding-ready exports preserve chunk order/position metadata cleanly enough for vector-sidecar consumers to reconstruct nearby context without guessing, while also surfacing chunk-semantic section cues so downstream retrieval can tell identity/setup chunks from issue/action/resolution/attachment evidence
- whether materialized chunks are actually keeping up with ticket-update freshness at the per-document level, including lagging-document counts, open-vs-closed splits, lag buckets, and top stale samples
- whether important retrieval metadata is materially populated at both the chunk level and the document level so a few multi-chunk tickets do not distort coverage reads
- a real SQLite column/table
- a reusable structural query
- the ticket document/chunk materialization layer
- or a generated public artifact if it helps OpenClaw/humans inspect the state quickly

If a proposed feature mainly hardcodes conclusions that OpenClaw could derive at query time from well-prepared data, prefer better data preparation over baking that interpretation into SherpaMind.

That is how SherpaMind becomes naturally queryable instead of technically queryable only in theory.
