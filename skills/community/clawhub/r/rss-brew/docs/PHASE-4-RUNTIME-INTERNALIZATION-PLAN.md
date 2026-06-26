# RSS-Brew Phase 4 Plan — Runtime Internalization

## Goal
Move RSS-Brew from a working **app wrapper around legacy runtime scripts** to a state where the app package begins to own core runtime structure.

Phase 4 is **not** a delivery redesign and **not** a full app rewrite. It is the first internalization step.

## Primary objective
Shift the ownership of core runtime helpers from `scripts/` toward `app/src/rss_brew/` while preserving existing behavior and keeping regression tests green.

---

## Scope

### In scope
1. extract winner/ranking logic into app-native module(s)
2. extract manifest helpers into app-native module(s)
3. extract CURRENT/publish-pointer helper logic into app-native module(s)
4. update orchestrator to call app-native helpers where safe
5. keep semantics unchanged
6. re-run existing Phase 3 tests and basic CLI sanity validation

### Out of scope
- delivery redesign
- stale lock recovery / finalize resume
- data-root layout migration
- full orchestrator decomposition in one pass
- moving the project outside `skills/rss-brew/`
- deleting legacy scripts entirely

---

## Proposed target modules

```text
app/src/rss_brew/
├── state/
│   ├── __init__.py
│   ├── manifests.py
│   ├── winner.py
│   └── publish.py
```

### Module responsibilities

#### `state/winner.py`
- `rank_key(...)`
- `select_winner(...)`
- any pure helper needed for winner choice

#### `state/manifests.py`
- `read_json(...)`
- `write_json(...)`
- `update_manifest(...)`
- `list_committed_manifests(...)`

#### `state/publish.py`
- `atomic_write_text(...)`
- `write CURRENT` helper(s)
- small publish/pointer helpers that do not require broad runtime redesign

---

## Execution sequence

### Step 1 — Create state package
Create:
- `app/src/rss_brew/state/__init__.py`
- `app/src/rss_brew/state/manifests.py`
- `app/src/rss_brew/state/winner.py`
- `app/src/rss_brew/state/publish.py`

### Step 2 — Move pure helpers first
Start with pure / low-risk logic:
- ranking
- winner selection
- manifest list/filtering
- JSON read/write helpers
- CURRENT write helper(s)

### Step 3 — Wire legacy orchestrator to app-native helpers
Update `scripts/run_pipeline_v2.py` conservatively to import and use app-native helpers where safe.

Important:
- do not change runtime semantics
- do not redesign flow
- only replace local helper ownership

### Step 4 — Keep compat layer coherent
If needed, mirror small import adjustments in copied compat files, but do not make compat the primary runtime in this phase.

### Step 5 — Re-run validations
- `cd app && ../venv/bin/python -m pytest -q`
- CLI inspect latest
- CLI dry-run sanity check

### Step 6 — Document Phase 4A outcome
Update plan/docs only if module ownership changed materially.

---

## Acceptance criteria

Phase 4A is successful if:
- state package exists under `app/src/rss_brew/state/`
- winner/manifests/publish helper ownership is moved into app-native modules
- `scripts/run_pipeline_v2.py` still behaves the same
- pytest remains green
- CLI sanity checks still pass
- no delivery or retry semantics were changed

---

## Risks

### Risk 1 — Import path confusion
Mitigation:
- keep modules small
- prefer pure helper extraction first

### Risk 2 — Hidden semantic drift while “just extracting helpers”
Mitigation:
- do not rewrite logic while moving it
- compare behavior using existing tests

### Risk 3 — Over-expanding Phase 4 into architecture surgery
Mitigation:
- explicitly stop after winner/manifests/publish helper extraction
- defer deeper orchestrator breakup until after this phase lands cleanly

---

## Recommended first-pass execution scope
Execute only **Phase 4A** now:
1. create `state/` package
2. extract helper ownership
3. wire orchestrator conservatively
4. run tests + sanity checks

Do **not** start Phase 4B (bigger orchestrator slimming) in the same task.
