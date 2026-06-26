# wip-branch-guard v1.9.79

## Bootstrap bug fix: hook matcher now fires on Read|Glob

v1.9.77 added Layer 3 (onboarding-before-first-write) with a Read handler inside `guard.mjs` that appends to `state.read_files` so the onboarding gate can verify the agent read the repo's onboarding docs before first write.

The handler was dead code. `package.json:claudeCode.hooks[0].matcher` was `"Write|Edit|NotebookEdit|Bash"` — **no Read**. Claude Code never invoked the hook on Read calls. `state.read_files` stayed empty forever. Every fresh worktree hit the onboarding gate with no way to satisfy it. The feature cliff-blocked itself.

## Fix

One-line change in `package.json`:

```
"matcher": "Write|Edit|NotebookEdit|Bash"
              -> "Read|Glob|Write|Edit|NotebookEdit|Bash"
```

Now Read (and Glob for scanning) fire the hook. The existing Read handler in guard.mjs marks files as read and persists state. Onboarding completes organically: the agent reads the required docs, the gate passes, writes proceed.

## Regression guard

`test.sh` gains a static check that `package.json`'s matcher contains both `Read` and `Glob`. Fails loudly if a future edit drops them.

## Why this shipped broken

My PR 2 test harness piped JSON directly into `guard.mjs`, faking a Read tool_name. It never exercised the actual Claude Code matcher filter. The tests passed; the production integration failed silently (fail-open on import failure masked the earlier 1.9.77 issue too). Lesson: hook-layer tests must exercise the real dispatch path, not the guard internals in isolation.

## Recovery path (how this was unblocked)

1. The broken guard cliff-blocked writes to any new worktree.
2. `ldm install /tmp/toolbox-pre-layer3` pointed at the `v1.9.71-alpha.20` tag (pre-Layer 3) to deploy v1.9.76 without the bug.
3. Free to edit source again; this PR shipped.
4. `ldm install --yes` post-merge pulls the fixed v1.9.79.

Documented so next time I hit a self-referential bug, the installer-as-escape-hatch is the first move.

## Files

- `tools/wip-branch-guard/package.json`: version 1.9.78 -> 1.9.79, matcher adds Read|Glob
- `tools/wip-branch-guard/test.sh`: static matcher-contains test

## Tests

68 passing (including new matcher-contains), 0 failing, 8 main-only skipped.

## Related

- `wip-ldm-os-private` PR 621 (installer subdir-copy fix). Complements this PR: once that lands, lib/ subdirs deploy correctly and the inlined block in guard.mjs can move back out.
- Implementation plan: `wip-ldm-os-private/ai/product/bugs/guard/2026-04-20--cc-mini--guard-implementation-plan.md`
