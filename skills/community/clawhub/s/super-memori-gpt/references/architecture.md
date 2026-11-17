# Architecture

## Goal

Provide reliable continuity for long-running ChatGPT work without pretending that a skill can expand the model context window or control ChatGPT's internal memory engine.

## Four layers

### A. Native user memory
Durable cross-project user context handled by ChatGPT's own Memory/personalization when available. Best for stable preferences, recurring constraints, roles, and durable facts.

### B. Project ledger
A compact, inspectable, project-scoped source of truth. It should contain only current state plus enough superseded history to explain decisions. Prefer a persistent Library/file artifact when writable file tools exist.

### C. Session working set
A bounded selection from A+B+sources for the current request. This is what should consume context-window tokens.

### D. Source evidence
Original files, prior chats, connector records, test results, citations, or user statements. Evidence outranks summaries when they disagree.

## Design influences

The architecture intentionally combines several modern memory ideas:

- selective synthesis and freshness instead of retaining every historical detail;
- semantic / episodic / procedural separation;
- interconnected notes and memory evolution when new evidence arrives;
- temporal validity and supersession;
- bounded retrieval rather than whole-history replay;
- explicit provenance and confidence;
- project isolation to avoid cross-project contamination.

## Why no local vector database inside the plugin

The original Super Memori v4 was built around a local OpenClaw host and could own SQLite/Qdrant processes. A ChatGPT plugin skill cannot assume that machine-local daemon, filesystem layout, Python environment, or startup hook exists. Requiring those components would make the plugin non-portable and create false persistence claims.

Semantic retrieval should therefore use ChatGPT's available memory/file retrieval capabilities. The project ledger adds deterministic structure where semantic similarity alone is insufficient.

## Retrieval flow

`request -> scope -> recover candidates -> authority/freshness filter -> conflict resolution -> bounded working set -> execution`

## Writeback flow

`material change -> secret/privacy filter -> delta extraction -> status/version update -> provenance -> persist if supported -> verify write`

No write is considered complete until the persistence action actually succeeds.
