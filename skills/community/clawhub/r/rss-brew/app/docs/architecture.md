# RSS-Brew App Architecture (V1)

## Intent
RSS-Brew is being converted from a skill-hosted collection of scripts into an app-shaped system **in place** inside the existing `skills/rss-brew/` directory.

V1 does **not** rewrite business semantics. It creates a reliable application container around the current working pipeline.

---

## Architectural state in V1

### App entrypoint
- `app/src/rss_brew/cli.py`

### Path/config helper
- `app/src/rss_brew/paths.py`

### Compatibility layer
- `app/src/rss_brew/compat/`
- contains copied legacy scripts for packaging/migration purposes

### Legacy execution layer (still active)
- `scripts/*.py`
- this remains the source of truth for runtime behavior in V1

### Runtime data root
Default:
- `/root/workplace/2 Areas/rss-brew-data`

This contains operational state such as:
- `run-records/`
- `daily/`
- `.staging/`
- `processed-index.json`
- `metadata.json`
- digest outputs

---

## Execution model in V1

The current runtime path is:

```text
rss_brew.cli
  -> delegates to legacy scripts under scripts/
  -> legacy orchestrator executes pipeline stages
  -> pipeline writes manifests/staging/published outputs in data root
```

### Important implication
V1 is a **wrapper architecture**, not a rewritten application core.

That is intentional.

---

## Why this design was chosen

### Goals achieved
- preserve working pipeline behavior
- avoid high-risk semantic rewrites during container migration
- create a package boundary that future refactors can target
- make CLI-based execution possible now
- keep rollback simple

### Problems avoided
- no winner-selection rewrite
- no delivery redesign
- no data layout migration
- no orchestrator decomposition in the same pass

---

## Current module responsibilities

### `rss_brew.cli`
Responsible for:
- command parsing
- route dispatch (`run`, `dry-run`, `inspect latest`, `delivery update`)
- selecting the correct Python interpreter for delegation

### `rss_brew.paths`
Responsible for:
- package root resolution
- app root resolution
- skill root resolution
- legacy scripts root resolution
- default data-root resolution

### `scripts/run_pipeline_v2.py`
Still responsible for:
- orchestrating the pipeline
- manifest state transitions
- staging/publish flow
- winner selection
- promotion to canonical outputs
- finalize logic

### `app/src/rss_brew/compat/*`
Current purpose:
- preserve copied legacy code inside the app boundary
- support future migration work
- provide a package-local landing zone for gradual internalization

---

## Interpreter model

A key V1 requirement is that delegated legacy scripts must run using the existing RSS-Brew virtual environment.

Preferred interpreter:
- `/root/.openclaw/workspace/skills/rss-brew/venv/bin/python`

Fallback:
- `sys.executable`

This avoids dependency mismatches during real execution.

---

## Proven in V1

The following are confirmed to work:
- CLI boot/help
- CLI inspect latest
- CLI dry-run
- CLI real small-run execution via venv
- commit/publish/CURRENT update through the new CLI wrapper

---

## Non-goals in V1
- do not remove legacy scripts
- do not make compat the primary runtime layer yet
- do not refactor the orchestrator into smaller modules yet
- do not introduce a new storage layout
- do not change retry semantics or delivery semantics

---

## Expected Phase 2 direction
Phase 2 should focus on:
1. regression tests for retry/winner behavior
2. reducing dependence on direct `scripts/` delegation
3. deciding when to switch operational default to the app CLI
4. preparing orchestrator decomposition with safety tests already in place
