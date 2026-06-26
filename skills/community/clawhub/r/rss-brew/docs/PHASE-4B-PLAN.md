# RSS-Brew Phase 4B Plan

## Goal
Continue runtime internalization conservatively after Phase 4A.

Primary purpose:
- reduce drift between `scripts/` and `app/src/rss_brew/compat/`
- continue small, low-risk helper internalization
- keep tests and CLI behavior stable

## Scope

### In scope
1. sync compat orchestrator helper ownership with app-native state helpers
2. extract one more small publish/CURRENT-related helper step if safe
3. re-run regression tests and CLI sanity checks
4. update docs if ownership boundaries change materially

### Out of scope
- delivery redesign
- stale lock recovery / finalize resume
- full orchestrator decomposition
- deleting legacy scripts
- moving project outside current folder
- major runtime semantic changes

## Priority

### 4B.1 — Compat sync (highest priority)
Make `app/src/rss_brew/compat/run_pipeline_v2.py` use the same app-native helper modules introduced in Phase 4A:
- `rss_brew.state.winner`
- `rss_brew.state.manifests`
- `rss_brew.state.publish`

Goal:
- remove duplicated helper ownership from compat orchestrator
- reduce drift risk between `scripts/` and `compat/`

### 4B.2 — Small publish helper internalization
If safe, extract one more CURRENT/publish-related helper into app-native module(s), but do not move the full publish flow.

Preferred candidates:
- CURRENT pointer payload assembly helper
- CURRENT/CURRENT.json write helper

## Validation requirements
- `cd app && ../venv/bin/python -m pytest -q`
- CLI inspect latest sanity check
- CLI dry-run sanity check
- optional: small real run only if helper extraction touched runtime behavior more than expected

## Acceptance criteria
Phase 4B is successful if:
- compat orchestrator no longer carries duplicate copies of app-native state helpers
- tests remain green
- CLI sanity checks still pass
- no runtime semantic drift was introduced

## Stop rule
Do not continue into broader orchestrator slimming in this pass. If compat sync and one small publish helper extraction are complete, stop and report.
