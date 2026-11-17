---
title: "ldm status npm probes time out under execFile"
status: fixed
priority: P1
owner: Installer Cody
repo: wip-ldm-os-private
created: 2026-05-12
---

# `ldm status` should not spawn npm CLIs for each probe

## Problem

Alpha.26 proved bounded concurrency was active, but dogfood still was not clean:

- `ldm status` returned in about 20 seconds.
- It had no `[budget]` rows.
- Every npm probe still timed out at the 5s per-check limit.
- Merge/Deploy K isolated the repro: `execFile('npm', ['view', ...])` timed out, while direct `npm view ...` returned quickly.

The problem is the probe mechanism. Starting many npm CLI child processes is too expensive and unreliable for `ldm status`, even with a concurrency cap.

## Fix

Implemented in this PR.

- `ldm status` now fetches package metadata directly from the npm registry instead of spawning `npm view` for each status probe.
- `LDM_STATUS_NPM_REGISTRY_URL` lets tests point status at a local registry server.
- The timeout and concurrency controls remain:
  - `LDM_STATUS_NPM_TIMEOUT_MS`
  - `LDM_STATUS_TOTAL_BUDGET_MS`
  - `LDM_STATUS_NPM_CONCURRENCY`
- The timeout and concurrency regression tests now use a local HTTP registry fixture instead of a fake npm binary, so they exercise the production probe path.

## Acceptance

- `ldm status` returns without `[budget]` rows on Parker's 30+ extension install.
- Npm probes populate the update table instead of timing out every row.
- `scripts/test-ldm-status-timeout.mjs` proves slow registry responses are bounded.
- `scripts/test-ldm-status-concurrency.mjs` proves registry probes actually run concurrently and that `LDM_STATUS_NPM_CONCURRENCY=1` remains serial.

## Recommendation

Cut alpha after merge and dogfood `ldm status` again on mac-mini-01.
