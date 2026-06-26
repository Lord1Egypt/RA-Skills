# Development Roadmap

## Phase 0 — Bootstrap
- repository scaffold
- local storage model
- CLI entrypoints
- developer/operator docs

## Phase 1 — API verification
- verify auth pattern against live SherpaDesk account
- identify exact endpoint set required for accounts, users, technicians, tickets, comments
- document actual endpoint behavior and quirks
- first live milestone: token-only org discovery plus a minimal tickets-list probe

## Phase 2 — Seed pipeline
- implement initial seed for core entities
- persist sync metadata
- verify data integrity in SQLite
- current live slice: accounts + users + technicians + tickets
- next seed expansions: comments/notes/history and any missing relational surfaces

## Phase 3 — Delta sync
- implement incremental sync using verified update/change signals
- add idempotent upsert behavior
- verify low-noise repeated sync runs
- first likely shape: watcher + hot open-ticket rescans + warm recent-closed reconciliation + cold rolling audit lane

## Phase 4 — Analysis surface
- add reusable analytical queries and reporting commands
- support operator/AI-facing questions against the local database
- define the normalized document/export layer that feeds retrieval

## Phase 5 — Retrieval layer
- add keyword/full-text search over ticket/comment knowledge
- add vector/semantic retrieval over chunked support documents
- support OpenClaw-friendly hybrid retrieval workflows (SQL + FTS + vector)

## Phase 6 — New-ticket watcher
- detect new tickets on a schedule
- produce structured summaries and next-step suggestions
- route alerts to the chosen channel
