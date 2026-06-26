---
name: working-tree-governor
description: Govern dirty git working trees by classifying runtime noise vs real source changes, defaulting to selective staging, verifying staged scope, and asking the operator when scope is ambiguous.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Working-tree-governor

Use when a repo is dirty and you need to commit safely without dragging runtime noise, logs, cache, state files, or generated artifacts into history.

This skill exists for the common Hermes failure mode where `git status` becomes unreadable because code, tests, logs, runtime state, forensics, cached binaries, and generated outputs are all mixed together.

The goal is not cleanliness theater. The goal is to preserve signal and produce small, reviewable commits.

## When to trigger

Load this skill when any of these are true:
- the user asks to commit while the repo is dirty
- `git status --short` shows mixed code plus logs/state/cache/output noise
- more than ~25 changed or untracked files
- more than ~8 source or test files are modified
- the next action is risky: restart, deploy, cutover, refactor, or live-sensitive change
- runtime-critical files are dirty in a tree already full of noise

Treat these as high-risk triggers:
- more than 100 changed/untracked files
- live runtime files dirty and HEAD stale
- planned restart/deploy while mixed dirt is still present
- tracked state/log/output files continuously mutating and obscuring code changes

## Core principle

Never use `git add .` in this situation.
Never default to stash for this situation.
Default to selective staging.
If confidence is low, ask the operator before commit.

## Discovery workflow

Start read-only.

Run:
```bash
git status --short
git diff --name-only
git diff --cached --name-only
git rev-parse HEAD
git log -1 --format='%H %ad %s' --date=iso
```

Optional when useful:
```bash
git diff --stat
git diff -- <path>
```

Then bucket every changed path.

## Buckets

### Bucket A — core code and tests
Examples:
- `src/**/*.py`
- `tests/**/*.py`
- service scripts
- core config templates
- startup scripts
- bridge/runtime code

Default action:
`include_now`

### Bucket B — docs and plans
Examples:
- `docs/**`
- selected `*.md`
- intentionally authored design notes

Default action:
usually `needs_operator_decision` unless clearly part of the requested commit

### Bucket C — runtime state
Examples:
- `shared/risk/*.json`
- `shared/reports/strategy_pnl.json`
- `shared/risk/open_positions.json`
- `hermes_state.json`

Default action:
`preserve_but_exclude`

### Bucket D — generated outputs and artifacts
Examples:
- `results/**`
- backtest outputs
- parquet / duckdb
- generated summaries

Default action:
`preserve_but_exclude`

### Bucket E — logs
Examples:
- `*.log`
- `*.jsonl`
- `streamer.log*`
- monitor logs
- cron logs

Default action:
`ignore_for_now` or `preserve_but_exclude`

### Bucket F — caches and binaries
Examples:
- `__pycache__/`
- `*.pyc`
- `.metaapi/*.bin`

Default action:
`ignore_for_now`

### Bucket G — forensics and snapshots
Examples:
- `shared/forensics/**`
- `*.bak-*`
- incident snapshots

Default action:
`preserve_but_exclude`

### Bucket H — unknown
Anything not confidently classifiable.

Default action:
`needs_operator_decision`

## Heuristics

### High-confidence exclude
Exclude by default when path matches patterns like:
- `**/__pycache__/**`
- `**/*.pyc`
- `shared/hermes-acp/*.log`
- `shared/hermes-acp/*_log.jsonl`
- `shared/reports/*.jsonl`
- `shared/risk/*.json`
- `results/*.json`
- `memory/**/*.md`
- `src/.metaapi/*.bin`
- `shared/forensics/**`
- `*.bak`
- rotated logs / archives

### High-confidence include
Include by default when path matches patterns like:
- `src/**/*.py`
- `tests/**/*.py`
- skill files
- fixtures under `tests/fixtures/**`

### Important exception
Do not exclude real code just because it lives beside noisy runtime files.
For example, `shared/hermes-acp/*.py` may be real source code and must be inspected, not auto-excluded.

## Commit-governor flow

### 1. Summarize the tree
Report:
- total dirty file count
- bucket counts
- runtime-critical files dirty
- likely risk level: low / moderate / high / critical

### 2. Infer requested commit scope
Use the user’s requested commit intent to infer the include set.
Examples:
- execution-truth work → `shared/hermes-acp/execution_truth*.py`, matching tests, matching fixtures
- streamer fix → exact `src/hermes/streamer.py` plus targeted tests

Do not include unrelated source changes automatically just because they are code.

### 3. Stage selectively
Stage only the inferred relevant files.
Never stage all dirty files.

Use:
```bash
git add <explicit paths>
```

### 4. Verify staged scope before commit
Always run:
```bash
git diff --cached --name-only
git diff --cached --stat
git status --short
```

Verify explicitly:
- no logs staged
- no runtime state staged
- no cache/binaries staged
- no unrelated subsystem staged
- staged paths match the requested commit intent

If suspicious files appear, unstage them or stop.

### 5. Conventional commit message
Prefer these prefixes:
- `feat:`
- `fix:`
- `refactor:`
- `test:`
- `docs:`
- `chore:`

If the user’s message lacks a valid prefix, suggest a corrected version before commit.

### 6. Operator approval gate
Do not auto-commit if any of these are true:
- ambiguous file group present
- multiple unrelated subsystems staged
- runtime-sensitive file included unexpectedly
- a Bucket H file would be committed
- the staged set is larger than expected for the request

In those cases, ask a short scope question and wait.

### 7. Commit and post-commit verification
After commit, run:
```bash
git show --stat --oneline HEAD
git diff --cached --name-only
git status --short
```

Report:
- commit hash
- files included
- notable dirty files intentionally left out
- whether runtime noise remains uncommitted

## Risk policy

### Low risk
Small tree, mostly one category, no runtime-critical dirt.
Proceed normally but still summarize buckets.

### Moderate risk
Mixed categories, some core code dirty, risky action coming.
Recommend selective baseline before continuing.

### High risk
Large mixed tree, core runtime dirty, noise obscures real work.
Switch to hygiene-first mode before more feature work.

### Critical risk
Huge mixed tree plus stale HEAD plus runtime-critical dirt plus pending restart/deploy.
Strongly recommend immediate selective preservation before any risky next step.

## Edge cases

### Real code in noisy directories
Example:
- `shared/hermes-acp/execution_truth_slice.py`
This is real code. Inspect it. Do not auto-exclude it because of the directory.

### Fixtures that look like logs
Example:
- `tests/fixtures/execution_truth_streamer_2026_04_10_sample.log`
This is a committed test fixture, not runtime noise.

### Runtime-sensitive source files
Example:
- `src/hermes/streamer.py`
These require stricter operator confirmation before commit.

### Already-staged junk
If bad paths are already staged, verify and unstage before commit instead of proceeding.

## Fail-safe rule

If confidence is not high, do not commit.
Show:
- candidate include list
- suspicious/ambiguous list
- recommended commit message
- one short operator question

The fail-safe is simple:
when uncertain, ask before commit.

## Output style

When using this skill, report in this order:
1. dirty-tree summary
2. bucket classification
3. recommended include-now list
4. recommended exclude/preserve list
5. staged verification
6. commit recommendation or operator question

## What success looks like

The skill is successful when Hermes consistently does this:
- detects dirty tree risk early
- separates runtime noise from real changes
- stages only the requested source/test/config files
- verifies staged scope before commit
- uses conventional commit messages
- avoids dragging runtime junk into history
- asks the operator whenever scope is not obvious
