# Release Notes: memory-crystal v0.7.30

**Date:** 2026-03-30

## What changed

### Hardcoded path removal

Two files had `/Users/lesa` hardcoded as a fallback path. Both now use portable alternatives.

**migrate-lance-to-sqlite.mjs** had a fallback that resolved the OpenClaw workspace to `/Users/lesa/.openclaw`. The migration script now calls `os.homedir()` to build the path dynamically, so it works on any machine without assuming a specific username. This was the last remaining hardcoded path in the migration pipeline (#99).

**dev-update.ts** (the ai/dev-updates scanner) had an iCloud path baked in for reading team documents. It now calls `resolveWorkspace()` to read the workspace root from LDM config (`~/.ldm/config.json`), making it portable across machines and user accounts (#98).

## Why

These paths broke on any machine where the username is not `lesa`. Part of a broader audit across all LDM OS repos to eliminate hardcoded user paths and make everything portable.

## Issues closed

- #98
- #99

## How to verify

```bash
grep -r "/Users/lesa" src/ scripts/ --include="*.ts" --include="*.mjs"
# Should return zero results
```
