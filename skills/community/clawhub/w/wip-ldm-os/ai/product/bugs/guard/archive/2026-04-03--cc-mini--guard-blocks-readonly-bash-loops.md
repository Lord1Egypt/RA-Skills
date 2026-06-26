# Bug: Guard blocks read-only bash for loops

**Date:** 2026-04-03
**Reporter:** CC Mini
**Component:** wip-branch-guard

## Description

The branch guard blocks bash `for` loops that are purely read-only (diff, ls, cat) because the loop syntax triggers the "file-modifying command" detection.

## Reproduction

```bash
for f in /some/path/*.md; do diff "$f" "/other/path/$(basename $f)"; done
```

This is blocked with: "BLOCKED: Cannot run file-modifying command on main branch."

The command is read-only. It only runs `diff`. But the `for` loop syntax is flagged.

## Expected behavior

Read-only commands inside `for` loops should not be blocked. The guard should check what commands are inside the loop, not just that a loop exists.

## Impact

Can't do batch file comparisons, batch reads, or any iterative read-only operations while on main. Have to use workarounds or switch to a branch for purely investigative work.

## Resolution

Status: Closed on 2026-04-24.

Closed by `wip-ai-devops-toolbox-private` PR #386. The guard now parses Bash loop bodies by command effect: read-only loops are allowed, while loops containing write effects such as `rm`, redirects, or `tee` are denied.

Verification:

- `bash tools/wip-branch-guard/test.sh`: 117 passed, 0 failed, 1 skipped.
- Covered by explicit read-only loop allow and write-effect loop deny tests.
