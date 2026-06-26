# OpenClaw upstreaming execution plan

**Date:** 2026-04-27
**Author:** Kody, with Parker
**Status:** active execution plan
**Related:**
- `ai/product/bugs/openclaw/2026-04-24--kody--upstream-memory-core-packet.md`
- `ai/product/bugs/openclaw/2026-04-27--kody--openclaw-upgrade-compatibility-master-plan.md`
- `ai/product/bugs/openclaw/2026-04-24--cc-mini--unified-reliability-triage.md`

## Goal

Stop carrying permanent WIP-only OpenClaw patches by fixing the generic runtime issues in the WIP fork first, proving them, and upstreaming them as small reviewable PRs.

Do not send one giant "Lēsa reliability" PR upstream. Each upstream PR should be narrow enough for OpenClaw maintainers to review, test, and merge independently.

## Ground rules

1. Verify upstream current source before each PR. Do not assume the local fork still knows the latest upstream state.
2. Patch WIP fork branches first, validate locally, then open upstream PRs only for generic OpenClaw fixes.
3. Keep Lēsa-specific policy, identity, boot payload, and LDM deploy pipeline work local to WIP repos.
4. Every upstream PR must include:
   - exact failure mode
   - production-scale evidence where available
   - focused tests
   - rollback-safe explanation
5. Retire a WIP carry patch only after upstream has equivalent source and a WIP rebase/live canary passes.

## PR sequence

### PR 1: memory-core seed cache stream/yield

**Status:** accepted upstream main after `v2026.4.26`: <https://github.com/openclaw/openclaw/pull/73067> -> maintainer PR #73118, commit `983fd775e2ca000d5c7b95e0281eeb19eb12059b`

**Intent:** upstream the already-proven WIP production fix.

Scope:
- `extensions/memory-core/src/memory/manager-sync-ops.ts`
- Replace unbounded `.all()` over `embedding_cache` with `.iterate()`.
- Yield to the event loop every bounded batch during large cache seeds.
- Preserve existing seed semantics.

Evidence:
- Local production `embedding_cache`: 435,136 rows, about 8.08 GiB serialized embedding payload.
- Old path crashed with V8 heap OOM inside `StatementSync::All`.
- Streamed/yielding path survived live Day 63 repro and kept gateway probes responsive.

Validation:
- memory-core focused tests
- relevant type/lint gate
- optional read-only production-size canary

### PR 2: memory-core `listChunks()` bounded top-K

**Status:** accepted upstream main after `v2026.4.26`: <https://github.com/openclaw/openclaw/pull/73069> -> maintainer PR #73100, commit `864c4f7ff492f0f514c12557d44f0d6b509231fc`

**Intent:** fix the secondary broad-recall OOM path instead of only filing an issue.

Scope:
- `extensions/memory-core/src/memory/manager-search.ts`
- Replace unbounded `.all()` over chunk rows/embeddings with streaming iteration.
- Preserve ranking semantics by maintaining a bounded top-K candidate heap instead of dropping candidates early.
- Avoid selecting embeddings when the caller does not need vector scoring, if the local API shape permits that cleanly.
- Avoid OFFSET pagination on large tables where this path paginates.

Evidence:
- Local production `chunks`: 323,249 rows.
- Text payload: about 424 MiB.
- Embedding payload: about 5.30 GiB.
- This remains the main known unfixed OpenClaw memory-core OOM path after PR 1.

Validation:
- Add small-fixture tests that compare old materialized ranking behavior to the new streaming top-K behavior.
- memory-core focused tests.
- production-size read-only canary if practical.

### PR 3: config mutation safety

**Intent:** stop config writers from silently stripping model/provider/plugin invariants during restart/doctor/migration.

Scope candidates:
- config validation/normalization paths
- restart/doctor mutation paths
- config writer metadata

Required behavior:
- fail closed on unknown model/provider/plugin keys
- preserve unknown fields unless an explicit migration owns them
- show or record a diff before mutation
- stamp writer identity/version/schema/source hash/reason
- treat model route as provider/auth/runtime resolution, not just a string name

Validation:
- config fixture tests for unknown fields and plugin hook keys
- restart/doctor dry-run tests if available
- WIP config invariant canary before live use

### PR 4: OpenAI-compatible chatCompletions next-turn queue

**Intent:** upstream the generic part of Bridge compatibility.

Scope:
- OpenAI-compatible chatCompletions route
- main-session routing via supported header/user semantics
- busy-session next-turn queue for streaming and non-streaming requests
- honest `x-openclaw-queued: next-turn` behavior

Do not frame this as Lēsa-specific Bridge work. Frame it as OpenAI-compatible API correctness for long-running embedded agents: requests should not silently vanish while a session is busy.

Validation:
- route-to-main tests
- busy-session queue tests
- streaming and non-streaming parity tests
- no reintroduction of the broad final-resync fallback superseded by upstream app-server lifecycle fixes

### Local-only track 5: WIP compatibility layer

These are not upstream PRs unless they expose a generic OpenClaw bug:

- boot payload inventory and identity kernel
- Memory Crystal R3 ingestion policy
- LDM config deploy pipeline
- WIP healthcheck policy
- `plugins.allow` provenance pins for local WIP plugins
- image-generation product workflow invariant checks
- stale local plugin/worktree cleanup

Output:
- thin WIP tickets where missing
- updates to `open-claw-upgrade-private` runbook/landmines
- live canary checklist updates

## Execution order

1. Verify upstream current source for PR 1 through PR 4.
2. If PR 1 is still needed, create upstream branch from current upstream main and open the seed cache stream/yield PR. Done and accepted upstream main after `v2026.4.26`: <https://github.com/openclaw/openclaw/pull/73067> -> #73118.
3. Implement PR 2 locally with tests; canary against the large DB path; then open upstream PR. Done and accepted upstream main after `v2026.4.26`: <https://github.com/openclaw/openclaw/pull/73069> -> #73100.
4. Read current config mutation code and split PR 3 into one or more minimal reviewable patches.
5. Read current chatCompletions queue code and split PR 4 if upstream already has part of it.
6. File or update local-only tickets for track 5.
7. After any upstream acceptance, rebase WIP fork, remove redundant carry patch, and re-run live canary before declaring the carry retired.

## Current live baseline before execution

- Live OpenClaw: `2026.4.25` WIP fork build
- Live merge commit: `c188a3647c11fde080f8e6475e20380aa9671f35`
- Gateway promotion path: `npm link` from built WIP worktree, then `launchctl kickstart -k`
- Protected probes: `/healthz` and `/readyz` green
- Main session: `gpt-5.5`
- Known remaining runtime issue: boot/context payload remains high; this is local-only track 5, not an upstream memory-core patch

## Verification log

### 2026-04-27 upstream source check

Checked `upstream/main` after fetching tags/main.

Findings:

- `extensions/memory-core/src/memory/manager-sync-ops.ts`
  - `seedEmbeddingCache()` still selects all rows from `embedding_cache` with `.all()`.
  - No cooperative yield exists in that seed loop.
  - PR 1 is still needed.
- `extensions/memory-core/src/memory/manager-search.ts`
  - `listChunks()` still selects `id, path, start_line, end_line, text, embedding, source` from `chunks` and calls `.all()`.
  - The fallback vector scoring path still maps every candidate through `parseEmbedding()` and cosine similarity before sorting.
  - PR 2 is still needed.

Conclusion: upstream has adjacent memory search improvements, including sqlite-vec KNN work, but it has not absorbed the two WIP production OOM fixes tracked here.

### 2026-04-27 upstream PRs opened

PR 1 was opened as <https://github.com/openclaw/openclaw/pull/73067> and accepted through maintainer PR #73118.

- Branch: `wipcomputer:kody/upstream-memory-core-seed-stream`
- Commit: `88aa75dee0 fix(memory-core): stream embedding cache seed during reindex`
- Landed commit: `983fd775e2ca000d5c7b95e0281eeb19eb12059b` on upstream `main` after `v2026.4.26`.
- CI: green as of 2026-04-27 after the upstream PR run.
- Scope: `seedEmbeddingCache()` now streams `embedding_cache` rows with `.iterate()`, yields every 1000 rows, and has a regression test that fails if the seed-copy query falls back to `.all()`.
- Validation run before PR:
  - `pnpm tsgo`
  - `pnpm test extensions/memory-core/src/memory/index.test.ts`
  - `pnpm test extensions/memory-core/src/memory/manager.sync-errors-do-not-crash.test.ts`
  - `pnpm test extensions/memory-core/src/memory`

PR 2 was opened as <https://github.com/openclaw/openclaw/pull/73069> and accepted through maintainer PR #73100.

- Branch: `wipcomputer:kody/upstream-memory-core-listchunks-topk`
- Commits after rebase onto current upstream main:
  - `5749e74ef1 fix(memory-core): bound fallback vector chunk scoring`
  - `d35153ac3e test(memory-core): loosen fallback search prepare spy type`
  - `85281a4cc2 test: update lint suppression allowlist for plugin runtime helper`
- Landed commit: `864c4f7ff492f0f514c12557d44f0d6b509231fc` on upstream `main` after `v2026.4.26`.
- CI: green as of 2026-04-27 after rebasing onto `upstream/main` `78d3fce5f9`.
- Scope: fallback vector search streams chunk candidates and keeps an exact bounded top-K instead of parsing/sorting the full candidate set; the legacy `listChunks()` helper now uses `.iterate()`.
- Note: the lint-suppression allowlist commit is a current-upstream CI compatibility fix for `src/test-utils/plugin-runtime-env.ts`; it is not part of the memory-core runtime behavior change.
- Validation run before PR:
  - `pnpm tsgo`
  - `pnpm test extensions/memory-core/src/memory/manager-search.test.ts`
  - `pnpm test extensions/memory-core/src/memory`
- Validation after rebase / CI fix:
  - `pnpm tsgo`
  - `pnpm check:test-types`
  - `pnpm test extensions/memory-core/src/memory/manager-search.test.ts`
  - `pnpm test test/scripts/lint-suppressions.test.ts`
  - `node scripts/run-vitest.mjs run --config test/vitest/vitest.full-core-support-boundary.config.ts test/scripts/lint-suppressions.test.ts`

Next execution target is PR 3, but only after WIP canaries a post-`v2026.4.26` OpenClaw build containing `983fd775e2` and `864c4f7ff4` so the fork carry can be retired deliberately instead of by accident.
