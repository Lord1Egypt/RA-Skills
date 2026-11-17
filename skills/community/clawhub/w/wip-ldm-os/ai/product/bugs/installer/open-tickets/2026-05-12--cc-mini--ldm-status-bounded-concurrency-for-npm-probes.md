---
title: "ldm status: bounded concurrency for npm update probes"
status: fixed
priority: P2
owner: Installer Cody
repo: wip-ldm-os-private
created: 2026-05-12
---

# `ldm status` should probe npm with bounded concurrency

## Problem

PR #904 (alpha.21) bounded `ldm status` under a 60s total budget with a 5s per-check timeout. Probes still run serially. On a 37-extension install in steady state, serial 5s probes can sum to 185s in the absolute worst case (every probe stalls and hits its per-check timeout). The 60s total budget caps the wall-clock, but the cost of capping is that many checks are skipped as `budget` rather than completed.

On a healthy npm registry day, each probe usually returns in well under a second, so serial execution feels acceptable. On a slow day (npm registry latency spikes, regional CDN issue, the user's network is flaky), serial probing makes the difference between "all 37 checks reported in under 10s" and "the first 12 checks completed, the remaining 25 are skipped because the budget ran out."

Running probes concurrently (with a small parallelism cap) makes the common case faster and the slow case more useful (more checks actually complete instead of getting budget-skipped).

This was originally filed as P3. Dogfood on alpha.25 repriced it to P2 because `ldm status` skipped every npm update check on a slow-registry run, which forced the install agent into a five-minute manual rebuild from registry metadata and `npm view`.

## Proposal

Replace the serial loop in `cmdStatus` (around `bin/ldm.js:3340-3380`) with a bounded-concurrency probe runner. Each probe still has the per-check timeout via `npmViewVersionForStatus`. The total budget still applies as the outer cap.

- Concurrency limit: 8 by default. Configurable via `LDM_STATUS_NPM_CONCURRENCY`.
- Per-check timeout: unchanged (`LDM_STATUS_NPM_TIMEOUT_MS`, default 5s).
- Total budget: unchanged (`LDM_STATUS_TOTAL_BUDGET_MS`, default 60s).
- Progress output: each "checking npm" line still printed before that probe begins; ordering may interleave because probes overlap, but each line still appears before its probe call.

Implementation sketch:

```js
async function runStatusProbesWithConcurrency(items, concurrency, statusStartedAt) {
  const results = [];
  let i = 0;
  async function worker() {
    while (i < items.length) {
      const idx = i++;
      const item = items[idx];
      const remaining = remainingStatusBudgetMs(statusStartedAt);
      if (remaining <= 0) {
        results[idx] = { kind: 'skipped', name: item.name, npm: item.npm, reason: 'budget' };
        continue;
      }
      const timeout = Math.min(STATUS_NPM_TIMEOUT_MS, remaining);
      console.log(`    ${item.name}: checking npm`);
      try {
        const latest = npmViewVersionForStatus(item.npm, timeout);
        results[idx] = { kind: 'ok', name: item.name, npm: item.npm, latest, current: item.current };
      } catch (error) {
        results[idx] = { kind: 'skipped', name: item.name, npm: item.npm, reason: classifyStatusCheckError(error) };
      }
    }
  }
  await Promise.all(Array.from({ length: concurrency }, worker));
  return results;
}
```

`npmViewVersionForStatus` currently uses `execFileSync` which blocks the event loop. To get real concurrency, switch to the async `execFile` (`util.promisify`) or `spawn` + stdout collection. The synchronous form will not parallelize.

## Code path unification audit (added 2026-05-12 dogfood)

A 2026-05-12 dogfood showed `ldm status` budget-skipped all 31 of 31 update checks on a slow-registry day, while `ldm install --dry-run` (run minutes later, same machine, same npm registry) resolved every check and produced a clean update table in seconds. Both commands answer the same question (what's newer on npm than what's installed?) but they use different code in `bin/ldm.js`. The dry-run path lives in `cmdInstallCatalog`; the status path lives in `cmdStatus`.

Before patching concurrency into `cmdStatus` alone, audit `cmdInstallCatalog`'s update-detection. Either:

1. **Unify (preferred).** Extract one shared `getAvailableUpdates(extensions)` helper that both `cmdStatus` and `cmdInstallCatalog` call. The concurrency, per-check timeout, and total budget logic lives in that one function. Both commands share the same fix and any future bug-fix.

2. **Defer (fallback).** If unification is too big for this slice, file a follow-up ticket explicitly for it and call out the divergence in this PR's body. At minimum, do not let the concurrency fix to `cmdStatus` drift `cmdStatus` further from `cmdInstallCatalog`'s behavior than it already is today.

Either way, the post-fix invariant: running `ldm status` and `ldm install --dry-run` back-to-back against the same registry state should produce the same list of available updates.

## Acceptance

- 30+ extension probes complete in approximately 5-10s on a healthy npm day.
- Per-extension timeout still respected (5s default).
- Total budget still respected as backstop (60s default).
- Progress output still printed before each probe (ordering may interleave; each line still appears before its probe).
- `LDM_STATUS_NPM_CONCURRENCY=1` produces serial behavior identical to alpha.21 (regression-equivalence path).
- Regression test extending `scripts/test-ldm-status-timeout.mjs` (or a new test) that:
  - Stages N extensions where each fake-npm probe sleeps 1s
  - Asserts wall-clock completes near `ceil(N / concurrency)` seconds, not `N` seconds
  - Asserts `LDM_STATUS_NPM_CONCURRENCY=1` still works (serial fallback)
- `ldm status` and `ldm install --dry-run` produce the same list of available updates when run back-to-back against the same registry state. Either via the unified helper (option 1 above) or, if deferred, the divergence is documented and a follow-up ticket is filed.

## Fix

Implemented in this PR.

- `ldm status` now runs npm update probes through a bounded-concurrency runner.
- Default concurrency is 8, configurable through `LDM_STATUS_NPM_CONCURRENCY`.
- Per-check timeout remains `LDM_STATUS_NPM_TIMEOUT_MS`.
- Total command budget remains `LDM_STATUS_TOTAL_BUDGET_MS`.
- `LDM_STATUS_NPM_CONCURRENCY=1` keeps the serial fallback path available.
- Added `scripts/test-ldm-status-concurrency.mjs` and wired it into `prepublishOnly`.
- Audited `cmdInstallCatalog()` after dogfood showed `ldm install --dry-run` resolving updates while `ldm status` budget-skipped them. That path still has separate install-planning behavior, including different timeouts and track handling. Full unification is filed as a follow-up so this PR can stay focused on making `ldm status` useful again.

## Why this became P2

Correctness was handled by PR #904, but dogfood showed the installed-branch prompt does not feel correct when every check is budget-skipped. The CLI returned, but the agent had to reconstruct the table slowly and incompletely. The concurrency fix restores the intended install UX: one `ldm status` command should return a useful table without a manual fallback.

## Out of scope

- A `--fast` flag that skips update checks entirely. Different feature; file separately if needed.
- Caching npm-view results across calls. Different concern.
- Full `cmdStatus()` / `cmdInstallCatalog()` update-detection unification. Follow-up ticket filed.

## Recommendation

Alpha after fix. Dogfood validation needed because this is the first time `ldm status` runs probes concurrently; race conditions in the registry-iteration code or in `npmViewVersionForStatus` would surface only at runtime.

## Related

- Companion ticket filed same day: `ldm status` per-check elapsed time in skipped section.
- Parent fix: PR #904 (LDM OS alpha.21).
- Ticket closed by PR #904: `2026-05-12--cc-mini--ldm-status-hangs-on-installed-branch.md`.
- The async refactor of `npmViewVersionForStatus` may touch other callers of `execFileSync('npm', ...)` patterns; audit before refactoring.
