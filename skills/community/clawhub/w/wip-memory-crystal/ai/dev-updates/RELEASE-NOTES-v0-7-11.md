# Release Notes: Memory Crystal v0.7.11

**Date:** 2026-03-13

## What's new

### Silent LDM OS bootstrap
- `crystal init` now installs LDM OS automatically when `ldm` is not on PATH
- Runs `npm install -g @wipcomputer/wip-ldm-os` silently
- Falls back to standalone installer if npm is offline or permissions fail
- No more "tip" messages. Walk through any door, get the whole house.

### npm scoped to @wipcomputer/memory-crystal
- Package name changed from `memory-crystal` to `@wipcomputer/memory-crystal`
- Fixes GitHub Packages 404 (scoping requirement)
- Old name will be deprecated on npm
- Install instructions updated in SKILL.md

### Earlier changes (v0.7.7-v0.7.10)
- **v0.7.10:** Orphan cleanup, DELETE trigger, doctor embedding check fix
- **v0.7.9:** Fix doctor false reports (backup, bridge, init dry-run)
- **v0.7.8:** Add DELETE trigger, crystal cleanup command
- **v0.7.7:** Updated install prompt to new standard format (4 questions, dry-run first)
