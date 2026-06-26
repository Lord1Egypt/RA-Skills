# Bug: Installer fails to build repos with file: dependencies

**Date:** 2026-03-31
**Filed by:** cc-mini
**Priority:** high
**GitHub issue:** wipcomputer/wip-ldm-os#255

## Problem

When the installer clones a repo and tries to build it, the build fails if the repo has `file:` dependencies pointing to sibling repos. These sibling paths don't exist in the clone context.

Example: memory-crystal depends on `"dream-weaver-protocol": "file:../dream-weaver-protocol-private"`. When cloned to `/tmp/ldm-install-memory-crystal/`, the sibling path `../dream-weaver-protocol-private` doesn't exist, so `npm install` (and the build) fails.

PR #271 added a band-aid: skip the build when `dist/` already has files. That works for npm-published packages (which include pre-built dist/), but fails for:
- Local development installs
- GitHub clones without pre-built artifacts
- Any new repo that uses `file:` deps

## Root cause

`runBuildIfNeeded()` in `lib/deploy.mjs` runs `npm install` then `npm run build` without resolving `file:` dependencies first. The `npm install` step fails because the `file:` paths are relative to the repo's original location, not the clone location.

## Fix

Add `resolveLocalDeps(repoPath)` to `lib/deploy.mjs`. Before building, scan `package.json` for `file:` dependencies and symlink them from `~/.ldm/extensions/` if installed. This resolves dependencies from what's already on disk (the local LDM installation), not from npm and not from sibling directories. No internet needed.

Called before `npm install` inside `runBuildIfNeeded()`.

## Files changed

- `lib/deploy.mjs`: Added `resolveLocalDeps()`, added `symlinkSync` import, call before build step.

## Test

1. Verify `dream-weaver-protocol` is at `~/.ldm/extensions/dream-weaver-protocol/`
2. Run the installer on a fresh clone of memory-crystal (with no sibling repos)
3. The build should succeed because `resolveLocalDeps()` symlinks the dependency from the installed extensions directory
