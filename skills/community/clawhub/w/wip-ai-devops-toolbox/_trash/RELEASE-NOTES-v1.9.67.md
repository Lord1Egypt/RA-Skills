# Release Notes: wip-ai-devops-toolbox v1.9.67

**Date:** 2026-03-30

## What changed

### Hardcoded path removal

Two files in the devops toolbox had paths that assumed a specific username or iCloud layout.

**ldm-jobs/backup.sh** referenced `/Users/lesa/Library/Mobile Documents/.../ldm/bin/` to find the `ldm` binary for scheduled backup jobs. This iCloud path was fragile (iCloud sync delays, different usernames). The script now uses `$HOME/.ldm/bin/` which is the standard LDM install location and works on any machine (#301).

**test.sh** (the branch guard test harness) had `/Users/lesa` hardcoded for creating temp directories. It now uses `$HOME` so tests run correctly under any user account (#301).

### Earlier changes included in this release

**v1.9.66** added auto-combine for release notes from batched PRs (#237). When multiple PRs are merged between releases, their individual RELEASE-NOTES files are automatically combined into a single changelog entry.

**v1.9.65** fixed the scaffold-on-main issue (#223) where scaffolding left untracked files that blocked `git pull` on the main working tree.

## Why

The backup job is scheduled via LaunchAgent and runs unattended. If the path to `ldm` is wrong, backups silently fail. Moving to `$HOME/.ldm/bin/` aligns with the standard LDM install path and eliminates the iCloud dependency. The test fix ensures CI and local test runs work for all contributors.

## Issues closed

- #301

## How to verify

```bash
grep -r "/Users/lesa" ldm-jobs/ tools/wip-branch-guard/test.sh
# Should return zero results
```
