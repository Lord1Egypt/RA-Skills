# Release Notes: wip-ldm-os v0.4.32

**Fix parent package detection so toolbox updates show correctly.**

## What changed

Parent package detection in `ldm install --dry-run` was skipping packages already checked by the extension loop. This caused `wip-ai-devops-toolbox` to never appear as a parent update. Instead, only `wip-release` (one of 12 sub-tools) showed.

The root cause: `checkedNpm` was pre-populated from the extension loop results. When the parent detection loop ran, `@wipcomputer/wip-ai-devops-toolbox` was already in the set, so it was skipped. The parent loop is supposed to REPLACE sub-tool entries with the parent name, not skip them.

## Why

Follow-up fix for v0.4.31. The parent detection logic was correct in intent but had a data flow bug.

## Issues closed

- #132

## How to verify

```bash
ldm install --dry-run
# Should show: wip-ai-devops-toolbox (not wip-release) for toolbox updates
```
