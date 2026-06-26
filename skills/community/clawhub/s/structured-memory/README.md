# Structured Memory

Structured Memory is an OpenClaw skill for long-horizon agent memory maintenance.

It keeps `memory/YYYY-MM-DD.md` as the source of truth, then builds a structured retrieval layer on top of it:

- rebuildable indexes by date, module, and entity
- execution-critical fact extraction
- object-style fact cards for recall
- card-first retrieval for paths, services, IDs, endpoints, repositories, and other operational facts

## Current release

- Version: `1.0.1`
- Regression baseline: `206 / 206 passing`

## What this repository contains

- `skills/structured-memory/` — the published skill package
- `projects/structured-memory-spec.md` — design/spec notes
- `projects/structured-memory-stable-baseline-2026-03-10.md` — frozen baseline snapshot

## Core idea

Structured Memory does **not** replace daily memory.
It depends on daily memory and improves retrieval on top of it.

Source of truth:

- `memory/YYYY-MM-DD.md`

Structured layers built from it:

- `memory-index/`
- `memory-modules/`
- `memory-entities/`
- `critical-facts/`
- `critical-facts/cards/`

## Typical workflow

### 1. First-time setup

```bash
python3 skills/structured-memory/scripts/init_structure.py
```

### 2. Daily maintenance

```bash
python3 skills/structured-memory/scripts/rebuild_one_day.py YYYY-MM-DD
```

### 3. Validation / diagnostics

```bash
python3 skills/structured-memory/scripts/check_idempotency.py YYYY-MM-DD
python3 skills/structured-memory/scripts/search_critical_facts.py <query>
python3 skills/structured-memory/tests/run_tests.py
```

## Default operating model

For agents that have this skill installed, structured-memory should not be treated only as an on-demand utility.

When the day produced meaningful task progress, decisions, blockers, risks, reusable execution-critical facts, or other meaningful updates to `memory/YYYY-MM-DD.md`, the agent should treat structured-memory rebuild as part of its default memory maintenance workflow.

## Publishing

Published skill bundle examples:

- `structured-memory-1.0.1.zip`

The canonical skill content lives under:

- `skills/structured-memory/`
