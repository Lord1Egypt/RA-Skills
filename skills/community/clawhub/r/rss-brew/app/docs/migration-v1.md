# RSS-Brew Migration V1 Notes

## Status
**Phase 1 in-place app-ification: complete and validated**

This phase created an app-shaped container **inside** the existing `skills/rss-brew/` directory without changing the core pipeline semantics.

## What was completed

### Structure
- Created `app/`
- Created `app/src/rss_brew/`
- Created `app/src/rss_brew/compat/`
- Created `app/tests/`
- Created `app/docs/`

### Package/bootstrap
- Added `app/pyproject.toml`
- Added `app/src/rss_brew/__init__.py`
- Added `app/src/rss_brew/paths.py`
- Added `app/src/rss_brew/cli.py`
- Added `app/src/rss_brew/compat/__init__.py`

### Compatibility layer
Copied legacy runtime scripts into:
- `app/src/rss_brew/compat/`

Original scripts under `scripts/` were retained.

### Tests/docs skeleton
Added initial tests and docs scaffolding for:
- CLI routing
- manifest compatibility
- winner selection skeleton
- guardrail TODO placeholder

## Fixes applied during validation

### 1) Legacy `run_pipeline_v2.py` syntax repair
A duplicated `else` block in `scripts/run_pipeline_v2.py` caused a syntax error. This was removed as a minimal repair.

### 2) App path resolution fix
`app/src/rss_brew/paths.py` initially calculated the skill root incorrectly, which caused the CLI to look for legacy scripts in the wrong directory. This was corrected.

### 3) Legacy script local path fix
`scripts/run_pipeline_v2.py` had an incorrect `SCRIPT_DIR` assumption during validation, causing it to look for sibling scripts in the wrong place. This was corrected.

### 4) CLI interpreter fix
`rss_brew.cli` originally delegated using `sys.executable`, which failed on real runs due to missing dependencies (for example `pydantic`) in the system Python environment.

The CLI now prefers:
- `/root/.openclaw/workspace/skills/rss-brew/venv/bin/python`

and falls back to `sys.executable` only if the venv interpreter is unavailable.

## Validation completed

### Validation A — app package health
Verified:
- `python3 -m py_compile app/src/rss_brew/*.py`
- `python3 -m py_compile app/src/rss_brew/compat/*.py`
- `python3 -m py_compile scripts/*.py`

### Validation B — CLI boot
Verified:
- `PYTHONPATH=app/src python3 -m rss_brew.cli --help`

### Validation C — CLI inspect path
Verified:
- `PYTHONPATH=app/src python3 -m rss_brew.cli inspect latest --data-root /root/workplace/2 Areas/rss-brew-data`

### Validation D — CLI dry-run path
Verified:
- new CLI can execute `dry-run`
- delegate chain reaches legacy scripts correctly
- orchestrator completes successfully via CLI

### Validation E — CLI real small-run path
Verified with:
- `PYTHONPATH=app/src`
- `RSS_BREW_PHASE_A_LIMIT=5`
- `RSS_BREW_ENV=dev`
- `python3 -m rss_brew.cli run --data-root /root/workplace/2 Areas/rss-brew-data --debug`

Observed result:
- run completed with `status=committed`
- `CURRENT` updated to the new run
- published output written under `daily/YYYY-MM-DD/<run_id>/`
- real execution path succeeded using the venv interpreter

Reference successful run:
- `run_id = 20260309T172911Z-1092041`
- `status = committed`
- `new_articles = 32`
- `deep_set_count = 1`
- elapsed time ≈ `2m46.72s`

## What V1 means now

V1 is no longer just a skeleton. It is a **working app wrapper** around the existing RSS-Brew pipeline with:
- a package container
- a CLI entrypoint
- centralized path resolution
- compatibility delegation to legacy scripts
- successful real execution through the new CLI

## What is intentionally deferred
- full migration of runtime logic from `scripts/` into package-native modules
- replacement of compat delegation with package-internal execution
- full regression/E2E suite
- stale-lock recovery / finalize resume
- delivery architecture redesign
- orchestrator decomposition into state/publish/winner modules
- removal of old legacy entrypoints

## Recommended next step
Proceed to Phase 2 only after preserving this V1 milestone.

Recommended Phase 2 focus:
1. strengthen tests (especially guardrail and E2E retry preservation)
2. prepare default execution switch to app CLI
3. gradually reduce dependence on legacy `scripts/`
