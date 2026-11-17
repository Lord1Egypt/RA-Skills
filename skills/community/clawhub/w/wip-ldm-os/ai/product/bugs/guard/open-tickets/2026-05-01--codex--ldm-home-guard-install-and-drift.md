# LDM Home Guard Install And Drift Follow-Up

**Date:** 2026-05-01
**Filed by:** Codex
**Area:** guard
**Status:** open
**Priority:** medium
**Public issue:** `wipcomputer/wip-ldm-os#127`

## Summary

The public issue `wipcomputer/wip-ldm-os#127` asks for branch-guard coverage of `~/.ldm/`, including the tracked ldm-home repo state and the normal worktree/PR workflow there.

The 2026-05-01 reconciliation pass verified that the deployed guard blocks shared-main operations in `~/.ldm/` when the hook is invoked. It did not close the full issue because the local `~/.ldm` checkout is still a large dirty main checkout, and the issue also asks for actual ldm-home cleanup and durable hook/install coverage.

## Current Evidence

Simulated guard payload from `/Users/lesa/.ldm` on `main`:

```text
tool: Bash
command: git commit -m test
result: denied, git commit on shared main is blocked
```

Current local state observed during the reconciliation pass:

```text
repo: /Users/lesa/.ldm
branch: main
state: large dirty checkout with many deletions and untracked message/runtime files
```

Do not clean, stash, reset, or commit this checkout without a dedicated ldm-home recovery plan. It may contain active runtime state.

## Remaining Work

1. Inventory the dirty `~/.ldm` main checkout and separate runtime-generated files from tracked source files.
2. Decide which `~/.ldm` files belong in git history, which belong in ignore rules, and which belong under runtime state outside the repo.
3. Create an ldm-home worktree and commit any legitimate source/config changes through PR.
4. Verify the deployed guard hook path protects `~/.ldm` Write/Edit/Bash writes in normal agent operation, not only direct guard simulation.
5. Comment on and close `wipcomputer/wip-ldm-os#127` once the dirty-state recovery and durable hook coverage are complete.

## Related

- Public issue reconciliation archive: `ai/product/bugs/guard/archive/2026-05-01--cc-mini--public-guard-issue-reconciliation.md`
- Public issue: `https://github.com/wipcomputer/wip-ldm-os/issues/127`
