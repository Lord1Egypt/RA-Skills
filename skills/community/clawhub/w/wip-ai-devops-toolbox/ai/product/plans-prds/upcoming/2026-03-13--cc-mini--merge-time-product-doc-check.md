# Plan: Enforce Product Doc Updates at Merge Time (not just release)

**Date:** 2026-03-13
**Author:** CC-Mini + Parker
**Priority:** 1 (before release-time check, this is the earlier gate)
**Related:** `2026-03-11--cc-mini--product-doc-enforcement.md` (release-time check, complements this)

## Context

Today (2026-03-13) we merged a significant PR to memory-crystal-private (DELETE trigger, cleanup command, doctor fix) and only updated the product docs (`readme-first.md`, `roadmap.md`) after the fact. The product docs should have been updated as part of the PR, not as a separate step.

The existing plan (`product-doc-enforcement.md`) adds a check at `wip-release` time. But by then the PR is already merged. The docs should be updated **when merging to main on the private repo**, because that's when the work is done and the context is fresh.

## What This Adds

A pre-merge check (or merge-time reminder) that verifies:

1. **`ai/product/plans-prds/roadmap.md`** was modified in the PR branch (compared to main)
2. **`ai/product/readme-first.md`** (or `readme-first-product.md`) was modified in the PR branch

If neither was touched, the merge should warn or block.

## When It Triggers

When running `gh pr merge` on a private repo that has an `ai/` directory. This is the natural point: you're about to merge to main, the work is done, the context is in your head.

## Implementation Options

### Option A: Pre-merge CLI wrapper (recommended)

Add a `wip-merge` command (or extend `wip-release` with a `--check-merge` flag) that:

1. Checks the diff between the PR branch and main
2. If `ai/product/plans-prds/roadmap.md` is not in the diff: WARN
3. If `ai/product/readme-first.md` is not in the diff: WARN
4. Shows the warning before running `gh pr merge`
5. Asks: "Product docs not updated. Merge anyway? (y/n)"

```bash
wip-merge 49              # checks product docs, then runs gh pr merge 49 --merge
wip-merge 49 --skip-docs  # bypass the check
```

### Option B: GitHub Actions (future)

A GitHub Action on the private repo that comments on PRs when product docs aren't updated. Non-blocking but visible. Requires GitHub Actions setup.

### Option C: Claude Code hook

A pre-commit or pre-push hook that checks if the current branch touches code files but not product docs. Lightweight but easy to bypass.

## Recommendation

Option A is the simplest. One wrapper script. Runs locally. No GitHub Actions setup needed. Follows the existing pattern of `wip-release` as the toolchain for release workflow.

## What the Warning Should Say

```
! Product docs not updated in this PR:
  - ai/product/plans-prds/roadmap.md (not modified)
  - ai/product/readme-first.md (not modified)

These docs help the next agent understand what changed and where things stand.
Update them now, or merge with --skip-docs.
```

## Files to Create/Modify

| File | Change |
|------|--------|
| `tools/wip-release/merge.mjs` (NEW) | Pre-merge product doc check |
| `tools/wip-release/cli.js` | Add `wip-merge` subcommand |
| `guide/DEV-GUIDE.md` | Add "update product docs before merging" to the PR checklist |
| `ai/DEV-GUIDE-FOR-WIP-ONLY-PRIVATE.md` | Same |

## Why This Matters

Today's session is the proof. We did great work (cleanup, doctor fix, DELETE trigger). But the product docs only got updated because Parker explicitly asked. Without that prompt, the roadmap and readme-first would still say v0.7.4 while the code was at v0.7.8. The next agent would start from stale context.

The check should happen at merge time because:
- The context is fresh (you just built it)
- The PR diff shows exactly what changed
- It's before the release, so there's no published artifact with stale docs
- It's a natural checkpoint in the workflow
