---
name: structured-memory
description: Build and maintain a structured memory system for OpenClaw workspaces using layered storage: daily memory as the source of truth, domain/module/entity/tag indexing, critical-facts extraction, and retrieval planning. Use when designing, initializing, updating, or operating a memory system that must scale across work topics such as business, finance, legal, HR, projects, operations, tech, routines, and personal context.
---

# Structured Memory

Version: `1.0.1`

Use this skill to initialize and maintain a layered memory system in the OpenClaw workspace.

## What it does

- Uses `memory/YYYY-MM-DD.md` as the source of truth
- Builds rebuildable indexes by date, module, and entity
- Extracts reusable execution-critical facts into `critical-facts/`
- Rebuilds object-style cards under `critical-facts/cards/`
- On first initialization, backfills existing `memory/*.md` history automatically
- Maintains a frozen summary baseline with `preview + topic_summaries`

## Default operating rule

For agents that have this skill installed, structured-memory should not be treated only as an on-demand utility. When the day produced meaningful task progress, decisions, blockers, risks, reusable execution-critical facts, or other meaningful updates to `memory/YYYY-MM-DD.md`, the agent should treat structured-memory rebuild as part of its default memory maintenance workflow.

## Work-cycle maintenance rule

After meaningful updates are written into `memory/YYYY-MM-DD.md`, the agent should normally rebuild the current day into the structured layer before the work cycle ends. This keeps indexes, modules, entities, critical-facts, and cards aligned with the source-of-truth daily memory.

## Core rules

1. Treat `memory/YYYY-MM-DD.md` as the source of truth.
2. Keep first-level `domain` fixed and small.
3. Create second-level `module` files only on demand.
4. Prefer `entities` for stable objects and `free_tags` for one-off concepts.
5. Store reusable execution-critical facts under `critical-facts/`.
6. Never store high-sensitivity secrets in plain text unless the user explicitly requires it.
7. Indexes are rebuildable caches, not the truth.
8. A short daily preview is only for quick glance; it must not replace topic-level summaries for multi-topic days.

## Fixed first-level domains

Use these exact domains:
- `strategy`
- `business`
- `organization`
- `finance`
- `legal`
- `project`
- `operations`
- `tech`
- `routines`
- `personal`
- `meta`
- `misc`

## When creating modules

Before creating a new module:
1. Check whether an equivalent module already exists.
2. Check whether the concept should instead be an entity.
3. Check whether the concept is too specific and should remain a free tag.
4. Create a module only if it is a reusable topic bucket.

## Retrieval order

Default retrieval order:
1. `MEMORY.md`
2. `projects/*.md`
3. `critical-facts/cards/` for execution-critical lookups about servers, services, paths, IDs, endpoints, repositories, dependencies, or stable operational objects
4. `critical-facts/*.md` for raw fact scanning when the cards are missing or too sparse
5. `memory-index/by-date.json`
6. `memory-modules/` and `memory-entities/`
7. candidate `memory/YYYY-MM-DD.md` files

## Recall priority rule

When the agent needs to recall cross-day work, historical decisions, stable identifiers, paths, endpoints, repositories, service names, project dependencies, or other execution-critical facts, it should prefer checking the structured-memory layer before relying only on current chat context.

## Files to consult

Read these references as needed:
- `references/taxonomy.md` for domain and module rules
- `references/write-rules.md` for write/update behavior
- `references/retrieval-planner.md` for query routing
- `references/index-schema.md` for JSON and entry schemas
- `references/critical-facts-policy.md` for sensitive-fact handling

## Scripts

### Operating modes

#### 1. First-time setup
Run once when enabling the skill in a workspace:

```bash
python3 skills/structured-memory/scripts/init_structure.py
```

#### 2. Daily maintenance
Run after meaningful updates to the current day:

```bash
python3 skills/structured-memory/scripts/rebuild_one_day.py YYYY-MM-DD
```

#### 3. Validation / diagnostics
Use when checking stability or searching execution-critical facts:

```bash
python3 skills/structured-memory/scripts/check_idempotency.py YYYY-MM-DD
python3 skills/structured-memory/scripts/search_critical_facts.py <query>
```

- `scripts/init_structure.py` initializes the workspace structure safely and, on first run, backfills existing `memory/*.md` history into indexes / critical-facts / cards unless explicitly skipped.
- `scripts/parse_daily_memory.py` converts a daily memory file into a normalized index entry, supporting both structured entries and legacy bullet-style notes.
- `scripts/upsert_by_date_index.py` updates `memory-index/by-date.json` deterministically.
- `scripts/update_topic_indexes.py` appends module and entity index entries from a parsed daily memory result.
- `scripts/rebuild_one_day.py` reparses a single daily memory file and refreshes its by-date/module/entity indexes plus the corresponding `critical-facts/` entries for that day.
- `scripts/check_idempotency.py` verifies that rebuilding the same day twice produces a stable result.
- `scripts/summarize_daily_memory.py` generates the frozen summary layer in the current stable baseline: short `preview` plus `topic_summaries` for multi-topic days.
- `scripts/extract_critical_facts.py` extracts reusable execution-critical facts (IPs, paths, endpoints, service names, stable ids) and can write them into `critical-facts/*.md`.
- `scripts/rebuild_critical_fact_cards.py` rebuilds object-style fact cards under `critical-facts/cards/` by grouping facts around related entities/projects. Its parser is intentionally tolerant of malformed property lines, empty values, fullwidth colons, and odd spacing so one bad fact line does not crash the whole rebuild.
- `scripts/search_critical_facts.py` searches critical-fact cards first, then raw `critical-facts/*.md` files.
- `tests/run_tests.py` runs the regression suite across representative memory samples.

### Common commands

```bash
python3 skills/structured-memory/tests/run_tests.py
python3 skills/structured-memory/scripts/init_structure.py
python3 skills/structured-memory/scripts/rebuild_one_day.py 2026-03-10
python3 skills/structured-memory/scripts/check_idempotency.py 2026-03-10
python3 skills/structured-memory/scripts/search_critical_facts.py structured-memory
```

## Source-of-truth reminder

Do not skip or weaken `memory/YYYY-MM-DD.md`. Structured-memory depends on daily memory and improves retrieval on top of it; it does not replace the source-of-truth record.

Use scripts for deterministic structure work; use manual edits for small, obvious updates.

## Stability note

As of 2026-03-10, `1.0.1` is the current published baseline. The current implementation is frozen after the regression suite reached 206/206 passing. Before changing summary behavior again, update tests first and preserve compatibility with `preview + topic_summaries`.
