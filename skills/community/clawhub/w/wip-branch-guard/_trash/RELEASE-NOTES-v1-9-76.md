# wip-branch-guard v1.9.76

## Worktree-bootstrap allowlist

Extends `ALLOWED_BASH_PATTERNS` to cover `cp` / `mv` / `rm` / `touch` / redirect / `tee` with `.worktrees/` destinations. Before this, only `mkdir` into `.worktrees/` was allowed, so the standard worktree-bootstrap compound:

```
git worktree add .worktrees/<name> -b <branch> origin/main \
  && mkdir -p .worktrees/<name>/ai/... \
  && cp /src/file .worktrees/<name>/ai/file
```

... failed at the `cp` step. The 2026-04-19 session hit this block and forced an awkward workaround (run the `cp` from an unrelated existing worktree to dodge the main-tree guard check). This fix removes that friction.

## Changes

- `tools/wip-branch-guard/guard.mjs`: three new regex entries in `ALLOWED_BASH_PATTERNS` (cp/mv/rm/touch, redirect, tee; each against `.worktrees/` path). Symmetric with the existing `mkdir .worktrees` entry and mirrors the temp-dir pattern style.
- `tools/wip-branch-guard/test.sh`: 8 new test cases covering allow on all six verbs into `.worktrees/`, plus two regressions confirming non-`.worktrees` main-tree writes still deny.

## Tests

53 passing, 0 failing, 5 main-only skipped when run from worktree (expected). Up from 45 before this change.

## Why now

This was flagged as a prerequisite for the Layer 3 guard implementation (onboarding-before-first-write + blocked-file tracking) per `wip-ldm-os-private/ai/product/bugs/guard/2026-04-20--cc-mini--guard-implementation-plan.md`. Layer 3's tests create worktrees via the bootstrap compound, so the allowlist has to land first.

## Related

- Triggering incident: `wip-ldm-os-private/ai/product/bugs/code/lesa/2026-04-19--cc-mini--pr-89-process-violation-postmortem.md`
- Implementation plan: `wip-ldm-os-private/ai/product/bugs/guard/2026-04-20--cc-mini--guard-implementation-plan.md`
- Parent guard master plan: `wip-ldm-os-private/ai/product/bugs/guard/2026-04-05--cc-mini--guard-master-plan.md`

## Known limitation

The regex matches `.worktrees` appearing anywhere in the command, not strictly the destination arg. A `cp .worktrees/foo/bar.md /main-tree/somewhere.md` would be allowed even though the destination is in main. This matches the imprecision of the existing `mkdir .worktrees` precedent. A strictly-destination regex would require argument-order parsing; deferred unless it causes a real problem.
