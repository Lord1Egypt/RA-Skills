# wip-ldm-os v0.4.76

## Installer fixes: Claude Code hook deploy is now complete and idempotent

Two installer bugs in `lib/deploy.mjs` fixed. Both exposed by the wip-branch-guard 1.9.77/1.9.78/1.9.79 rollout earlier today.

### Fix 1: `installClaudeCodeHookEvent` now recurses sibling subdirs

Previously copied only `guard.mjs` + `package.json` to `~/.ldm/extensions/<tool>/`. Any sibling directories (lib/, dist/, etc.) were silently dropped. Every hook before wip-branch-guard 1.9.77 was a flat single-file tool, so the bug was latent. When guard 1.9.77 shipped `lib/session-state.mjs` + `lib/approval-backend.mjs`, post-install those files were missing and guard.mjs threw `ERR_MODULE_NOT_FOUND` on every PreToolUse. Claude Code fail-open kept the system running but the branch-guard was effectively off.

Now: after copying guard.mjs + package.json, iterate `readdirSync(repoPath, { withFileTypes: true })` and `cpSync` each non-blacklisted subdir recursively. Skip list: `.git`, `node_modules`, `ai`, `_trash`, `.worktrees`, `logs`, `test`, `tests`, `__tests__`.

### Fix 2: `installClaudeCodeHookEvent` replaces instead of appending

Previously found existing entries in `~/.claude/settings.json` by matching BOTH command path AND matcher. When an extension bumped its matcher (wip-branch-guard 1.9.78 → 1.9.79 added `Read|Glob` to enable onboarding bootstrap), the finder missed the old entry and appended a new one. Result: two entries for the same extension + event, matcher "old" and "new", guard ran twice on any overlapping tool name.

Now: find by command path alone (same extension + same event). An orphan-cleanup pass in the same function removes any duplicate entries for the same extension in that event slot. Update matcher + command + timeout in place on the survivor. Upgrade-path: users who installed the broken versions will have their duplicate settings.json entries silently cleaned up on the next `ldm install`.

## Why these slipped

Both were latent bugs that no existing tool exercised. wip-branch-guard 1.9.77 was the first tool to:
1. Ship with a `lib/` subdir of nested imports (Fix 1 regression)
2. Change its matcher after initial install (Fix 2 regression)

The release sequence 1.9.77 → 1.9.78 (inline lib/ hotfix) → 1.9.79 (matcher fix) surfaced both. 1.9.78 is now redundant: once this LDM OS release ships, the inlined block in guard.mjs can move back to separate `lib/*.mjs` files. Deferred to a follow-up PR since the inlined version still works.

## Files changed

- `lib/deploy.mjs`: 68 insertions, 17 deletions total (PRs #621 + #622).

## Related

- `wip-ai-devops-toolbox-private` v1.9.79 (the guard) depends on Fix 2 to deploy its matcher correctly.
- Incident thread: the wip-branch-guard 1.9.77 ERR_MODULE_NOT_FOUND cliff-block on 2026-04-20.
- PR #621: installer-subdir-copy.
- PR #622: installer-settings-replace.

## Rollout

After merge: `wip-release patch` → `npm publish` → `ldm install` on dev machines. The install itself will exercise Fix 2 (cleaning up the duplicate settings.json entries left by the 1.9.78→1.9.79 chain).
