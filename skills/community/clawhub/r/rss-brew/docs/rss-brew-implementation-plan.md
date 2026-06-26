# RSS-Brew Implementation Plan

**Project:** RSS-Brew in-place app-ification inside `skills/rss-brew/`  
**Last updated:** 2026-03-09  
**Current status:** Phase 0 ✅ | Phase 1 ✅ | Phase 2 ✅ | Phase 3 ✅ | Phase 4 🟡 in progress (4A ✅, 4B ✅)

---

## 1. Objective

Convert RSS-Brew from a skill-hosted collection of runtime scripts into a cleaner app-shaped system **without breaking the currently working pipeline**.

This migration is intentionally staged.

### Primary goals
- preserve the working pipeline
- keep rollback easy
- create an app container inside the existing `rss-brew/` directory first
- avoid semantic rewrites too early
- add operational and testing guardrails before deeper refactors

### Non-goals for current phases
- no winner-selection redesign
- no delivery redesign
- no stale-lock recovery / finalize resume yet
- no full orchestrator decomposition yet
- no move outside the existing `skills/rss-brew/` directory yet

---

## 2. Current Architecture Snapshot

Current working structure:

```text
skills/rss-brew/
├── SKILL.md
├── scripts/                     # current runtime source of truth
├── app/                         # new app wrapper/container
│   ├── pyproject.toml
│   ├── src/rss_brew/
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   ├── paths.py
│   │   └── compat/
│   ├── tests/
│   └── docs/
├── references/
├── assets/
├── docs/
└── venv/
```

### Runtime truth today
- `scripts/*.py` still hold runtime semantics
- `app/src/rss_brew/cli.py` is the new app entrypoint/wrapper
- CLI currently delegates to legacy scripts
- CLI now prefers the skill venv interpreter for real execution
- cron pipeline execution has been switched to the app CLI wrapper (`rss_brew.cli run`) while delivery remains message-driven

---

## 3. Phase Definitions

### Phase 0
- baseline
- backup
- smoke validation

### Phase 1
- `app/` skeleton
- `app/src/rss_brew/compat/`
- `paths.py`
- `pyproject.toml`
- `__init__.py`

### Phase 2
- `cli.py` stub
- old entrypoint compatibility
- docs skeleton
- references cleanup

### Phase 3
- minimal tests
- dry run regression
- real small run regression

### Phase 4+
- decide whether to split orchestrator
- decide whether to extract state modules
- decide whether to move project outside current skill directory

---

## 4. Phase Status Update

## Phase 0 — Baseline / Backup / Smoke
**Status:** ✅ Complete

Completed:
- baseline thinking established
- smoke validation performed repeatedly during migration
- pre/post migration behavior checked through dry-runs and real runs

---

## Phase 1 — App Skeleton
**Status:** ✅ Complete

Completed:
- created `app/`
- created `app/src/rss_brew/`
- created `app/src/rss_brew/compat/`
- added `app/pyproject.toml`
- added `app/src/rss_brew/__init__.py`
- added `app/src/rss_brew/paths.py`
- copied legacy runtime scripts into `app/src/rss_brew/compat/`

Notes:
- this created a proper app-shaped container without removing legacy runtime files

---

## Phase 2 — CLI / Compatibility / Docs / References
**Status:** ✅ Complete

Completed:
- added `app/src/rss_brew/cli.py`
- established old entrypoint compatibility through legacy script delegation
- fixed venv interpreter selection for real execution
- created docs skeleton:
  - `app/docs/architecture.md`
  - `app/docs/migration-v1.md`
  - `app/docs/ops-runbook.md`
- completed references set:
  - `references/pipeline-spec.md`
  - `references/usage.md`
  - `references/ops.md`
  - `references/retry-architecture.md`
- normalized `SKILL.md` to point to app CLI + references + implementation plan

---

## Phase 3 — Tests / Regression / Real Validation
**Status:** ✅ Complete

Completed:
- made pytest runnable in the current environment
- added pytest configuration to `app/pyproject.toml`
- converted the major test skeletons/placeholders into real tests
- validated winner selection ranking behavior
- validated committed-only / manifest compatibility behavior
- validated CURRENT pointer behavior inside retry tests
- added temp-data-root orchestrator-level regression tests for same-day non-zero run followed by zero-new retry
- validated new CLI dry-run path ✅
- validated new CLI real small-run path ✅
- documented test-running instructions in `app/docs/ops-runbook.md`
- confirmed local test run passes (`10 passed`)

Notes:
- current regression suite focuses on deterministic orchestrator/state behavior
- live model/network behavior is still validated operationally through real runs rather than mocked pytest integration tests

---

## Phase 4+ — Runtime Internalization / Deferred Architecture Decisions
**Status:** 🟡 In progress

Phase 4 has started with two conservative internalization passes completed so far:
- **Phase 4A:** app-native helper extraction for winner/manifests/publish primitives ✅
- **Phase 4B:** compat sync + additional CURRENT/publish helper internalization ✅

Broader architecture decisions remain deferred until a clear Phase 4C scope is chosen.

---

## 5. Verified Milestones So Far

### Milestone A — App wrapper exists
Confirmed:
- package skeleton exists under `app/`
- CLI exists
- paths helper exists
- compat layer exists

### Milestone B — Legacy compatibility preserved
Confirmed:
- legacy scripts still remain present
- app wrapper does not require deleting old runtime entrypoints

### Milestone C — CLI path and interpreter chain works
Confirmed after fixes:
- `inspect latest` works
- `dry-run` works
- delegated scripts use the skill venv interpreter

### Milestone D — Real execution via new CLI works
Confirmed with real small run:
- new CLI successfully executed a real small run
- run committed successfully
- CURRENT pointer updated
- published output written

Reference successful run:
- `run_id = 20260309T172911Z-1092041`
- `status = committed`
- `new_articles = 32`
- `deep_set_count = 1`
- elapsed ≈ `2m46.72s`

---

## 6. Current Task Checklist

## Phase 2 wrap-up checklist
- [x] `cli.py` stub created
- [x] old entrypoint compatibility established
- [x] docs skeleton created
- [x] `references/usage.md` added
- [x] `references/ops.md` added
- [x] `references/retry-architecture.md` added
- [x] normalized `SKILL.md` → references navigation

## Phase 3 checklist
- [x] make pytest runnable in this environment
- [x] convert winner selection skeleton into real test
- [x] convert manifest compatibility skeleton into real test
- [x] add CURRENT pointer coverage via retry tests
- [x] implement same-day zero-new guardrail regression test
- [x] implement one temp-data-root E2E retry-preservation test
- [x] document test command in runbook
- [x] confirm test suite passes locally

## Phase 4 progress / backlog

### Completed in Phase 4 so far
- [x] create app-native state package under `app/src/rss_brew/state/`
- [x] move helper ownership for winner/ranking into app-native modules
- [x] move helper ownership for manifest IO/update/listing into app-native modules
- [x] move atomic text write helper into app-native publish module
- [x] wire `scripts/run_pipeline_v2.py` to consume app-native state helpers
- [x] sync `app/src/rss_brew/compat/run_pipeline_v2.py` to consume the same app-native state helpers
- [x] extract `write_current_pointers(...)` into app-native publish helper ownership
- [x] keep pytest green after Phase 4A / 4B
- [x] keep CLI inspect/dry-run sanity checks green after Phase 4A / 4B
- [x] fix NextDraft PDF digest parser so `Other New Articles` preserves all items and parses indented skim fields correctly
- [x] wire Scoring V2 / shadow run pipeline to emit and publish NextDraft HTML/PDF digest artifacts alongside markdown digest output

### Remaining Phase 4 backlog
- [ ] decide whether `scripts/run_pipeline_v2.py` should be decomposed further
- [ ] decide whether more publish/staging helpers should become app-native modules
- [x] switch cron pipeline execution to the app CLI wrapper
- [ ] decide whether project should eventually move outside `skills/rss-brew/`
- [ ] decide whether compat should remain migration scaffolding or become thinner/fallback-only
- [ ] decide how much of `scripts/` should be retired versus preserved as fallback wrappers
- [ ] decide whether delivery should also move from message-driven execution to an app-native CLI path
- [x] migrate Phase A scoring to direct DeepSeek API (`deepseek-reasoner`) while preserving current output contract

---

## 7. Recommended Next Step

### Immediate next step
**Finish Phase 2 cleanly, then enter Phase 3 deliberately.**

That means:
1. finish references cleanup
2. stabilize test harness
3. convert skeleton tests into real regression protection

### Why
Because the system already has:
- an app container
- a functioning CLI wrapper
- successful real execution through the new CLI

What it does **not** yet have is strong automated protection for further refactors.

---

## 8. Decision Rule Going Forward

### Do now
- finish Phase 2 references/doc cleanup
- begin Phase 3 regression/testing work
- keep validating through the new CLI

### Do not do yet
- do not deeply refactor orchestrator
- do not redesign delivery
- do not migrate storage layout
- do not remove legacy scripts
- do not move the project outside current skill directory yet

---

## 9. Current next-step direction

RSS-Brew has successfully moved beyond the "just scripts in a skill folder" stage.

It is now in a **working app-wrapper + early runtime-internalization state**:
- app shell exists
- CLI exists
- compatibility with legacy runtime exists
- tests/regressions exist
- Phase 4A / 4B internalization has begun
- cron pipeline execution now goes through the app CLI

The next concrete engineering direction is:
- continue bounded runtime internalization where useful
- and begin a **bounded Phase A direct API migration** for scoring

### Phase A direct API migration notes
This migration should:
- target `deepseek-reasoner`
- preserve the current `scored-articles.json` contract
- preserve downstream compatibility with Phase B
- keep mock mode working
- start with one-article-per-call behavior
- be evaluated carefully for score drift, since score changes can alter deep-set selection and final digest composition

Reference docs:
- `docs/PHASE-A-DIRECT-API-MIGRATION-PLAN.md`
- `docs/PHASE-A-PREFLIGHT-AUDIT.md`
