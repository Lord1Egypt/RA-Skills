---
title: "ldm doctor --fix crashes with `src.startsWith is not a function` on plist drift"
status: open
priority: P2
owner: unassigned
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-05-14
---

## What it does

`ldm doctor --fix` completes ALL fix passes without crashing. The LaunchAgent plist drift fix runs to completion.

## What it fixes

Today (alpha.30), after running `ldm doctor --fix`, the first pass (stale-hook removal) succeeded and the command crashed with `x src.startsWith is not a function` and exit 1. The LaunchAgent plist fix never ran, so the plist drift persists and `ldm doctor` keeps reporting the same issue every run.

## How to dogfood

1. Paste the install prompt; install if needed.
2. Run `ldm doctor --fix`.
3. Should complete successfully (exit 0) with all fixes applied.
4. Re-run `ldm doctor`. Should report fewer issues than before, ideally 0.

## Problem

Some variable named `src` in the doctor's fix logic is expected to be a string (calling `.startsWith()` on it) but is being passed something else. Likely the plist-fix path, since stale-hook removal succeeded before the crash. Repro: any machine where `ldm doctor` reports the LaunchAgent plist drift will likely trigger this on `--fix`.

## Acceptance

- `ldm doctor --fix` on a machine with LaunchAgent plist drift exits 0 after applying the fix.
- Regression test simulates the plist-drift fix path with a representative input that previously triggered the crash; asserts no `TypeError`.
- Dogfood: Parker runs `ldm doctor --fix` on his machine (alpha.30 state); command completes; subsequent `ldm doctor` reports no plist drift.

## Out of scope

- The 10-issues-vs-1-visible reporting bug (sibling ticket `2026-05-14--cc-mini--ldm-doctor-issue-count-vs-visible-mismatch.md`).
- A broader refactor of the doctor fix-pass dispatch. This ticket just fixes the immediate crash.

## Related

- `2026-05-14--cc-mini--ldm-doctor-issue-count-vs-visible-mismatch.md` (sibling, same 2026-05-13/14 dogfood, same `ldm doctor` surface).
- `2026-05-14--cc-mini--installer-dedup-orphans-hook-configs.md` (the stale-hook cleanup; that ticket's first fix pass works correctly per the same dogfood).
