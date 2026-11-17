# Migration from Super Memori 4.0.23

## Retained concepts

- hybrid relevance mindset;
- temporal reranking/freshness;
- relation-aware memory;
- degraded-mode honesty;
- lessons and operational memory;
- truth precedence;
- project continuity and startup recovery;
- verification before claiming success.

## Replaced for ChatGPT portability

### Removed machine-local infrastructure
The GPT branch does not require:

- Qdrant localhost service;
- SQLite/FTS runtime owned by the skill;
- sentence-transformers installation;
- shell entrypoints;
- OpenClaw startup hooks;
- hard-coded `/home/...` paths;
- host-specific health scripts.

Those components are appropriate for a self-hosted agent, not for a portable ChatGPT plugin skill.

### Replaced automatic command-log learning
The GPT branch does not ingest raw shell/command history. This avoids credential leakage and noisy lessons. Reusable lessons are extracted only from task outcomes that are relevant to the project.

### Replaced daemon-style background consolidation
ChatGPT's own native Memory may perform platform-managed synthesis. This skill itself performs project-ledger consolidation synchronously at meaningful checkpoints and never claims to run its own background daemon.

## New in 5.0.0

- explicit native-memory/project-ledger/session/evidence separation;
- project IDs and isolation;
- structured semantic/episodic/procedural/decision/artifact/task memory types;
- temporal validity and explicit supersession;
- provenance-first conflict resolution;
- bounded working-set retrieval;
- delta writeback with persistence verification states;
- secret-redaction gate;
- functional evaluation checklist;
- no machine-specific paths or executable-bit dependency.
