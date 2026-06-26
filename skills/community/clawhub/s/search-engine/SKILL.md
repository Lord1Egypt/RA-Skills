---
name: Search Engine
slug: search-engine
version: 1.0.0
homepage: https://clawic.com/skills/search-engine
description: Design and build any search engine with robust indexing, retrieval logic, relevance controls, and evaluation workflows for production systems.
changelog: Initial release with indexing pipeline guidance, query handling patterns, and quality evaluation checklists for reliable engine delivery.
metadata: {"clawdbot":{"emoji":"S","requires":{"bins":[]},"os":["darwin","linux","win32"]}}
---

## Setup

On first use, read `setup.md` and establish activation behavior, system scope, and data constraints before proposing implementation steps.

## When to Use

User needs to create, redesign, or scale a search engine for applications, documentation, products, or internal knowledge bases. Agent handles architecture planning, indexing strategy, retrieval design, relevance controls, evaluation loops, and rollout safety.

## Architecture

Memory lives in `~/search-engine/`. See `memory-template.md` for baseline structure and status values.

```text
~/search-engine/
|-- memory.md              # Persistent context, constraints, and active priorities
|-- requirements.md        # Retrieval goals, latency targets, and relevance expectations
|-- experiments.md         # Offline experiments and tuning decisions
`-- incidents.md           # Production issues, root cause, and remediation notes
```

## Quick Reference

Use the smallest relevant file for the task.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory template and status model | `memory-template.md` |
| Architecture options and component choices | `architecture-blueprint.md` |
| Retrieval and ranking strategy patterns | `retrieval-patterns.md` |
| Quality measurement and evaluation loops | `evaluation-metrics.md` |
| Delivery and rollout gates | `implementation-checklist.md` |

## Data Storage

Local notes stay in `~/search-engine/`:
- requirements and relevance objectives
- data source assumptions and indexing decisions
- experiment outcomes and deployment safeguards

## Core Rules

### 1. Start with a Retrieval Contract, Not with Tools
Before selecting engines, define the contract:
- query types to support (keyword, phrase, semantic, hybrid)
- response format, latency budget, and freshness target
- error tolerance and fallback behavior

A search engine without a contract becomes an untestable collection of features.

### 2. Design Ingestion and Indexing as a Deterministic Pipeline
Every document should pass explicit stages:
- ingestion source validation and deduplication
- normalization and field extraction
- chunking policy with stable identifiers
- indexing with repeatable transforms

Deterministic pipelines reduce drift between environments and simplify debugging.

### 3. Separate Recall Layers from Precision Layers
Treat retrieval as a staged system:
- broad candidate retrieval first (lexical, vector, or hybrid)
- reranking and business rules second
- formatting and explanation last

Mixing all concerns in one step hides failures and makes tuning unpredictable.

### 4. Define Relevance Features as Versioned Policy
Relevance changes must be tracked as policy versions:
- feature weights and boosts
- typo tolerance and synonym policy
- filtering, faceting, and tie-break rules

Never ship silent relevance changes without versioned notes and measured deltas.

### 5. Evaluate Offline Before Production Writes
For each relevance or indexing change:
- run benchmark queries with labeled expectations
- measure hit quality, ordering quality, and coverage
- compare against current baseline and note regressions

If evaluation evidence is weak, keep the current configuration and iterate.

### 6. Build Idempotent Index Operations and Safe Rollback
Index updates must be replay-safe:
- stable document ids and version checks
- resumable batch jobs with checkpoints
- alias-based or dual-index rollback plan

Without idempotency and rollback, incident recovery becomes guesswork.

### 7. Match Complexity to Workload Reality
Use the minimum architecture that meets requirements:
- avoid distributed complexity for small datasets
- avoid simplistic models for multilingual or high-noise corpora
- revisit design as scale and usage patterns change

Over-engineering and under-engineering both create expensive rework.

## Common Traps

- Starting with vendor selection before defining retrieval requirements -> architecture lock-in with unclear success criteria
- Indexing raw data without field-level normalization -> poor filters, weak facets, and noisy matching
- Tuning relevance on one happy-path query set -> brittle results in real user traffic
- Applying business boosts without guardrails -> top results become commercially biased and less useful
- Shipping retrieval changes without offline baseline comparison -> regressions discovered only by users
- Running full reindex jobs without resumability -> long outages and partial data corruption
- Ignoring multilingual tokenization differences -> severe precision drop for non-English users

## Security & Privacy

Data that leaves your machine:
- none by default in this instruction set
- only user-approved integration traffic when the user explicitly connects external services

Data that stays local:
- planning notes and experiment logs under `~/search-engine/`
- constraints, relevance decisions, and rollback records

This skill does NOT:
- collect unrelated files or credentials
- require hidden network calls
- bypass user-confirmed environment boundaries

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `api` - Define stable APIs for indexing, querying, and retrieval orchestration
- `elasticsearch` - Implement production indexing and query execution on Elasticsearch
- `meilisearch` - Ship lightweight retrieval stacks with fast iteration cycles
- `engineering` - Structure implementation workstreams and technical decision logs
- `software-engineer` - Improve delivery quality with testable architecture and rollout discipline

## Feedback

- If useful: `clawhub star search-engine`
- Stay updated: `clawhub sync`
