---
title: "Phase 1 dedup reverts between installs (autoDetect re-adds removed duplicates)"
status: in-review
priority: P1
owner: unassigned
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-05-13
---

## Problem

PR #938 / alpha.28 shipped the Phase 1 source.npm migration including dedup of known duplicate registry entries (`session-export` → `cc-session-export`, `package` → `wip-branch-guard`). On 2026-05-13 dogfood, the migration ran and printed "Removed 2 duplicate entries" but the registry persistence did not stick: the dry-run during the alpha.29 dogfood re-detected the same duplicates as still present.

Verified on Parker's mac-mini-01:

- Registry still has `package` (v1.9.90, `source.npm` `@wipcomputer/wip-branch-guard`) and `session-export` (v1.0.0, `source.npm` `session-export`) entries.
- Their `installedAt` timestamps (2026-03-13 and 2026-04-30) confirm they were NOT freshly re-added today.
- Both duplicate directories exist on disk: `~/.ldm/extensions/package/` and `~/.ldm/extensions/session-export/`.
- Single backup file (`registry.json.bak-2026-05-13T22-32-25-747Z`) was written during the earlier validation install. Pre-migration registry already had the same duplicates with the same old timestamps.

## Likely cause

The migration removes entries from `newRegistry.extensions` in-memory and calls `writeJSON`. The install flow continues after the migration. `autoDetectExtensions` (`bin/ldm.js` around line 1810) scans `~/.ldm/extensions/*/` and auto-registers any directory not in the registry. The duplicate directories exist on disk, so auto-detect re-adds the entries after the migration deletes them.

## Fix

The migration MUST move duplicate directories to `~/.ldm/_trash/` after removing their registry entries. The trash path is the existing LDM OS convention for "kept for safety, not deleted" (per `ldm install` output: "Old versions move to `~/.ldm/_trash/`, not be deleted"). With the directory moved, `autoDetectExtensions` cannot re-register the duplicate on the next install pass within the same `ldm install` run, and the dedup persists.

Parker's call on 2026-05-13. The other two candidates considered (do-not-register list, marker file) are not the right shape: the registry should be the only source of truth for what's installed, and a parallel exclusion list creates a second source. Moving the directory is the cleanest.

## Acceptance

- `ldm install` on a registry with known duplicate pairs results in a persistent dedup that survives a second `ldm install` run.
- Regression test in `scripts/test-legacy-npm-sources-migration.mjs` adds an after-install simulation that asserts the duplicates do not re-appear after `autoDetectExtensions` runs on the same install.
- Dogfood (three-step path; dry-run alone does not commit the move):
  1. Optional preview: one `ldm install --alpha --dry-run` to show the planned dedup directory moves.
  2. Real install: one `ldm install --alpha` to commit the registry update and actually move the duplicate directories into `~/.ldm/_trash/`.
  3. Verification: one `ldm install --alpha --dry-run` (or `ldm status`) to confirm no duplicate re-registration. `~/.ldm/_trash/` contains the moved entries (look for `*-deduplicated-*`).

## Out of scope

- Fixing the `autoDetectExtensions` logic itself (it correctly auto-registers extension directories that lack registry entries). The fix is in the interaction between migration and auto-detect.
- The status-vs-dry-run discrepancy (see sibling ticket `2026-05-13--cc-mini--installer-status-vs-dryrun-update-detection-discrepancy.md`).
