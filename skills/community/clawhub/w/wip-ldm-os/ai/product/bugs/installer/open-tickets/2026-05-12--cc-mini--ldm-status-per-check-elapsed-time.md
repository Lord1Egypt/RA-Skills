---
title: "ldm status: show per-check elapsed time in skipped section"
status: fixed
priority: P3
owner: Installer Cody
repo: wip-ldm-os-private
created: 2026-05-12
---

# `ldm status` should show per-check elapsed time in the skipped section

## Problem

PR #904 (alpha.21) added a bounded `ldm status` that reports slow npm probes in an "Update checks skipped:" section. Each row currently shows the extension name, the reason (`timeout`, `budget`, `unavailable`), and the npm package:

```
  Update checks skipped:
    wip-branch-guard: [timeout] @wipcomputer/wip-branch-guard
    wip-release: [budget] @wipcomputer/wip-release
```

What is missing is *how long* each probe actually took before being killed or skipped. When npm is having a slow day, the user cannot tell from this output which probe burned the most of the 60s total budget, or whether the timeout fires consistently at the 5s per-check ceiling or earlier.

This is diagnostic polish, not a correctness gap. Today the section is correct; it could be more useful.

## Expected behavior

Each skipped row includes the elapsed wall-clock time measured for that probe (or `0ms` for budget-exhausted entries that never started):

```
  Update checks skipped:
    wip-branch-guard: [timeout 5.0s] @wipcomputer/wip-branch-guard
    wip-release: [budget 0ms] @wipcomputer/wip-release
    wip-xai-grok: [unavailable 0.4s] @wipcomputer/wip-xai-grok
```

Elapsed time helps a user (or an agent dogfooding the install prompt) decide whether to re-run with a longer `LDM_STATUS_NPM_TIMEOUT_MS`, file an npm-registry incident, or move on.

## Acceptance

- Each row in the "Update checks skipped:" section shows elapsed time after the reason: `[timeout 5.0s]`, `[budget 0ms]`, `[unavailable 0.4s]`.
- Elapsed time is captured from a single `Date.now()` pair around the `npmViewVersionForStatus` call site, so it covers the actual probe wall-clock including the timeout SIGTERM.
- Existing regression test `scripts/test-ldm-status-timeout.mjs` updated to assert the elapsed pattern in the skipped row (e.g., regex `\[timeout \d+(\.\d+)?s\]`).
- No change to the "all up to date" / "X update(s) available" path; this is only for the skipped section.

## Fix

Implemented in this PR.

- Skipped update-check rows now include elapsed wall-clock time in the bracketed reason.
- Budget-exhausted checks that never start report `0ms`.
- Timeout and unavailable checks report the measured probe duration.
- `scripts/test-ldm-status-timeout.mjs` now asserts the elapsed-time shape.

## Why this is P3

The bounded-status fix from PR #904 is the load-bearing piece. This is post-fix diagnostic polish. The install prompt's installed branch works fine without it.

## Recommendation

Alpha after fix. Bundle with the bounded-concurrency follow-up (same date) if landing together; either order is fine since they touch the same function but different code paths.

## Related

- Companion ticket filed same day: `ldm status` bounded concurrency for npm probes.
- Parent fix: PR #904 (LDM OS alpha.21).
- Ticket closed by PR #904: `2026-05-12--cc-mini--ldm-status-hangs-on-installed-branch.md`.
