# Plan: Enforce Product Doc Updates in wip-release

**Date:** 2026-03-11
**Author:** cc-mini
**Priority:** 2 (after License Guard CC Hook)

## Context

Product doc updates (dev update, roadmap, readme-first-product.md) are required by the Dev Guide but not enforced by any tool. Agents forget to update them. Parker wants wip-release to check for these updates before publishing, so the gap gets caught before a release ships.

## What gets checked

Three product docs, in order of importance:

1. **Dev update** ... `ai/dev-updates/YYYY-MM-DD--*--description.md` exists with today's date (or within last 3 days for weekend releases)
2. **Roadmap** ... `ai/product/plans-prds/roadmap.md` was modified in commits since last tag
3. **Readme-first** ... `ai/product/readme-first-product.md` was modified in commits since last tag

## Behavior

| Release level | Product docs exist | Missing docs | Action |
|---|---|---|---|
| patch | ai/ exists | any missing | WARN (non-blocking) |
| minor/major | ai/ exists | any missing | BLOCK (fail release) |
| any | no ai/ dir | n/a | SKIP silently |
| any (--skip-product-check) | any | any | SKIP with note |

This follows the existing pattern: license guard blocks, thin notes warn. Product docs block on minor/major because those are the releases that matter. Patches get a warning so hotfixes aren't blocked.

## Implementation

### 1. Add `checkProductDocs()` to `core.mjs`

After `warnIfNotesAreThin()` (~line 225). Checks:
- `ai/dev-updates/` has a file from today or last 3 days
- `ai/product/plans-prds/roadmap.md` was modified since last git tag
- `ai/product/readme-first-product.md` was modified since last git tag

Only runs if `ai/` directory exists. Returns `{ missing: string[], ok: boolean, skipped: boolean }`.

### 2. Add `fileModifiedSinceLastTag()` helper

Uses `git describe --tags --abbrev=0` to find last tag, then `git diff --name-only {tag} HEAD` to check if a file was modified.

### 3. Integrate into `release()` pipeline

After the license compliance gate (line 461), before dry-run block (line 463):
- If missing + patch: WARN with `!` prefix (non-blocking)
- If missing + minor/major: BLOCK with `✗` prefix and `{ failed: true }` return
- `--skip-product-check` bypasses everything

### 4. Add `--skip-product-check` CLI flag

Parse in `cli.js`, pass to `release()`, document in help text.

### 5. Add to dry-run output

Show product doc status in `--dry-run` mode so agents can see what would happen.

## Files to modify

| File | Change |
|------|--------|
| `tools/wip-release/core.mjs` | Add `checkProductDocs()`, `fileModifiedSinceLastTag()`, integrate into `release()` and dry-run |
| `tools/wip-release/cli.js` | Add `--skip-product-check` flag, pass to `release()`, update help text |
| `tools/wip-release/SKILL.md` | Document the new check and flag |
| `tools/wip-release/README.md` | Document the new check |

## Verification

1. `wip-release patch --dry-run` ... should show product docs status
2. `wip-release minor --dry-run` ... should show BLOCK warning if docs not updated
3. `wip-release minor --dry-run --skip-product-check` ... should skip check
4. Test on a repo WITHOUT `ai/` directory ... should skip silently

## Estimate

Small. ~80 lines of code in core.mjs, ~5 lines in cli.js, doc updates. One function, one gate, follows existing patterns exactly.
