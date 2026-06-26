# Move consumed RELEASE-NOTES files to _trash/

**Date:** 2026-03-11 09:30 PST
**Author:** Claude Code (cc-mini)

## Problem

`RELEASE-NOTES-v*.md` files accumulated in the repo root after each release. `wip-release` read them for the GitHub release and CHANGELOG but never cleaned them up.

## Fix

- `wip-release` now moves all `RELEASE-NOTES-v*.md` files to `_trash/` as part of the version bump commit, after consuming them for the changelog and GitHub release
- `deploy-public.sh` (both copies) now excludes `_trash/` so these files never reach the public repo
- Existing `RELEASE-NOTES-v1-8-0.md` and `RELEASE-NOTES-v1-8-1.md` moved to `_trash/`

## Files changed

- `tools/wip-release/core.mjs` ... added `trashReleaseNotes()`, called between changelog update and git commit
- `tools/deploy-public/deploy-public.sh` ... added `_trash/` exclusion
- `scripts/deploy-public.sh` ... added `_trash/` exclusion

Closes #88
