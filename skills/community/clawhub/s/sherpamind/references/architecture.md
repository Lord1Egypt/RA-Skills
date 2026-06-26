# Architecture

> SherpaDesk API reference: <https://github.com/sherpadesk/api/wiki>

## Storage choice

SherpaMind should use a **hybrid local storage architecture**.

### Canonical layer: SQLite
SQLite remains the primary system of record for:
- tickets and ticket lifecycle state
- accounts / users / technicians
- comments / notes metadata
- sync cursors and ingest runs
- structured analytical queries

### Retrieval layer: search/vector sidecar
A retrieval sidecar should sit beside SQLite for:
- full-text lookup across ticket/comment/problem/resolution text
- semantic retrieval of similar incidents and related fixes
- OpenClaw-friendly contextual recall over historical support knowledge

### Why hybrid beats vector-only
- SQL is better for exact counts, timings, ownership, and reproducible reporting
- full-text is better for exact string matching, IDs, product names, and error text
- vectors are better for fuzzy contextual/similarity lookups

SherpaMind needs all three behaviors, so the durable design is **SQLite + retrieval sidecar**, not one or the other.

## Data model (initial)

### Core tables
- `accounts`
- `users`
- `tickets`
- `ticket_details`
- `ticket_attachments` (metadata only by default)
- `ticket_logs`
- `ticket_time_logs`
- `ticket_documents`
- `ticket_document_chunks`
- `ticket_comments`
- `technicians`
- `sync_state`
- `ingest_runs`

### Adjacent local state
- `.SherpaMind/private/config/settings.env`
- `.SherpaMind/private/secrets/sherpadesk_api_key.txt`
- `.SherpaMind/private/secrets/sherpadesk_api_user.txt`
- `.SherpaMind/private/state/watch_state.json`
- `.SherpaMind/private/runtime/venv`
- `.SherpaMind/public/exports/`
- `.SherpaMind/public/docs/`

### Design principles
- preserve raw-ish source fields where useful
- normalize stable dimensions (accounts, users, technicians)
- track source timestamps and sync metadata
- make ticket lifecycle and response timing easy to query

## Sync model

### Initial seed
- full fetch of relevant core entities
- backfill local dimensions before ticket relationships where possible

### Delta sync
- use modified timestamps / cursors where supported
- upsert changed records
- record sync watermark/state locally

## Request-discipline model

Because SherpaDesk is known to be awkward, the client layer should stay conservative:
- request pacing enabled by default
- retry/backoff only for transient HTTP failures
- no optimistic assumptions about pagination or filtering until verified live
- live API quirks should be written into repo docs instead of left in chat memory

## Watch model

The watcher should:
- poll for new tickets on a schedule
- compare against stored known ticket ids or creation timestamps
- emit alert-ready structured summaries
- suggest likely next questions and possible response directions
