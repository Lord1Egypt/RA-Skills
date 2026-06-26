# Plan: Memory Crystal Audit Ledger

**Date:** 2026-04-24
**Author:** Cody, with Parker
**Status:** plan
**Related:**
- `ai/product/plans-prds/current/openclaw/2026-04-24--cody--openclaw-config-runtime-split.md`
- `ai/product/plans-prds/current/ldmos-core/2026-04-24--cody--runtime-config-audit-boundaries-ticket.md`
- `ai/product/bugs/memory-crystal/2026-04-24--cc-mini--unified-reliability-triage.md`

## Problem

Memory has to be auditable, but raw memory stores should not be git-tracked.

Raw memory databases are too large, too mutable, too private, and too entangled with runtime state to live safely in git. The April 24 OpenClaw incident made the risk concrete: runtime DBs, temp files, auth state, and session state can accidentally enter source history when a mutable app home is treated as a source-of-truth repo.

Memory Crystal needs a separate audit layer that proves what was captured without committing the private contents or giant SQLite files.

## Principle

Git tracks intent and manifests. Runtime stores data. Audit ledgers track provenance and integrity. Backups preserve recoverability.

## Goals

1. Make Memory Crystal ingestion auditable without committing `crystal.db`.
2. Answer whether a source conversation/file was captured, when, by which pipeline, and with which embedding model.
3. Track failures and retries without replaying private content into git.
4. Support cross-source dedupe across session JSONL, iMessage `chat.db`, gateway logs, and manual memories.
5. Provide daily manifests that can be committed safely because they contain metadata and hashes, not raw conversation text.

## Non-goals

- Do not commit `crystal.db`, embeddings, raw session JSONL, iMessage contents, gateway logs, or auth/runtime state.
- Do not make git the backup mechanism for raw memory.
- Do not expose private text in plan files, public mirrors, release notes, or audit manifests.

## Architecture

Memory Crystal gets three distinct layers:

| Layer | Location | Purpose |
|---|---|---|
| Runtime store | `~/.ldm/memory/crystal.db` | Private searchable memory, chunks, embeddings, capture state |
| Audit ledger | `~/.ldm/memory/audit/*.jsonl` | Append-only metadata about ingest attempts, success, failure, hash, chunk count |
| Git-safe manifest | repo or `~/.ldm/manifests/` | Periodic redacted summary: table counts, schema hash, source hashes, status totals |

The runtime store is authoritative for search. The audit ledger is authoritative for provenance. The manifest is the git-safe integrity view.

## Ledger event schema

Each ingest attempt writes one append-only JSON line:

```json
{
  "time": "2026-04-24T18:12:00Z",
  "event": "ingest.completed",
  "source": "agent:main:main/session/019dbcf7",
  "source_type": "openclaw-session-jsonl",
  "source_id": "019dbcf7-ab13-777e-87ae-589ba42ab0f3",
  "content_hash": "sha256:...",
  "chunk_count": 42,
  "provider": "openai",
  "embedding_model": "text-embedding-3-large",
  "agent_id": "main",
  "schema_version": 7,
  "status": "ingested",
  "error_kind": null
}
```

Failure event example:

```json
{
  "time": "2026-04-24T18:13:00Z",
  "event": "ingest.failed",
  "source": "workspace/lesa-full-history.md",
  "source_type": "workspace-file",
  "content_hash": "sha256:...",
  "chunk_count": 0,
  "provider": "openai",
  "embedding_model": "text-embedding-3-large",
  "agent_id": "main",
  "schema_version": 7,
  "status": "failed",
  "error_kind": "embedding-too-large"
}
```

## Required fields

| Field | Why |
|---|---|
| `time` | Proves when capture happened |
| `event` | Separates started, completed, failed, skipped, backfilled |
| `source_type` | Session JSONL, iMessage, gateway log, workspace file, manual |
| `source_id` | Stable pointer to the source without raw text |
| `content_hash` | Integrity check and dedupe key |
| `chunk_count` | Confirms how much was captured |
| `provider` / `embedding_model` | Cross-model audit and reproducibility |
| `agent_id` | Which agent produced or owned the source |
| `schema_version` | Makes migrations auditable |
| `status` / `error_kind` | Failure tracking and retry policy |

## Hashing policy

Use normalized content hashes for dedupe and integrity:

```text
sha256(normalize(text) + "|" + iso_timestamp + "|" + sender_or_agent)
```

Rules:

- Never store raw text in the ledger.
- Store `source_hash` for the full source and `chunk_hash` for each chunk.
- Keep source-specific identifiers stable enough to trace back locally.
- If a source can be re-exported, the same normalized input should produce the same hash.

## Daily manifest

A daily manifest is safe to commit if it contains only metadata:

```json
{
  "date": "2026-04-24",
  "database": "memory-crystal",
  "schema_hash": "sha256:...",
  "table_counts": {
    "memories": 1234,
    "chunks": 323249,
    "capture_state": 17
  },
  "sources": {
    "openclaw-session-jsonl": { "completed": 18, "failed": 0 },
    "workspace-file": { "completed": 12, "failed": 3 },
    "imessage": { "completed": 0, "failed": 0 }
  },
  "failures": {
    "embedding-too-large": 3
  }
}
```

## Implementation phases

### Phase 1: Ledger writer

- Add `MemoryAuditLedger` with append-only JSONL writes.
- Write events for `ingest.started`, `ingest.completed`, `ingest.failed`, and `ingest.skipped`.
- Keep ledger writes non-blocking: ingestion should continue if audit append fails, but emit one warning.

### Phase 2: Ingest integration

- Emit audit events from session JSONL ingest, workspace file ingest, manual `remember()`, and backfill jobs.
- Include `ingestVersion` and skip-cursor metadata from the R1 reliability work.
- Ensure `embedding-too-large` failures write one durable event and do not spam every cycle.

### Phase 3: Manifest generator

- Add `crystal audit manifest --date YYYY-MM-DD`.
- Include table counts, schema hash, source counts, failure counts, and chunk totals.
- Do not include raw text or embeddings.

### Phase 4: Integrity checks

- Add `crystal audit verify --date YYYY-MM-DD`.
- Verify ledger event hashes match DB rows where local source data still exists.
- Report missing rows, duplicate chunks, and failed sources.

### Phase 5: Backup integration

- Keep raw DB backups encrypted and outside git.
- Store manifest hashes in git or a signed append-only log.
- Document restore flow: restore DB, replay or verify ledger, regenerate manifest.

## Acceptance criteria

- A new conversation turn produces an ingest ledger event without writing raw text to git.
- A failed workspace-file ingest produces one durable failure event and does not retry every minute unchanged.
- `crystal audit manifest` produces a git-safe JSON file.
- `crystal audit verify` can identify a missing or duplicated source.
- No raw memory DB, session JSONL, embedding, auth state, or temp file is introduced into source history.
