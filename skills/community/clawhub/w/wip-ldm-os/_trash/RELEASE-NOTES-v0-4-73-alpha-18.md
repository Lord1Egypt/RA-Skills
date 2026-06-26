# v0.4.73-alpha.18

## Installer: multi-hook support for extensions registering on multiple events

The LDM OS installer now supports extensions that register Claude Code hooks on multiple events. Previously each extension was limited to a single `claudeCode.hook` entry with one event (usually PreToolUse). Some extensions legitimately need to register on more than one event; the branch guard for example benefits from PreToolUse (block writes on main) AND SessionStart (warn at session boot when CWD is main-branch).

## What changed

### detect.mjs

New shape support for the extension manifest:

- **Legacy (still supported):** `pkg.claudeCode.hook = { event, matcher, ... }` (single door, single event)
- **New:** `pkg.claudeCode.hooks = [{ event, matcher, ... }, { event, matcher, ... }]` (array of doors, one per event)
- **Implicit:** a bare `guard.mjs` file defaults to a single PreToolUse door on Edit|Write (unchanged)

All three shapes are normalized internally to an array so `deploy.mjs` has one code path.

### deploy.mjs

`installClaudeCodeHook(repoPath, doorOrDoors)` now accepts either a single door object (legacy callers) or an array of doors. Iterates each door and calls the renamed inner helper `installClaudeCodeHookEvent(repoPath, door)`.

The existing-entry matching logic now includes the `matcher` field in its lookup key. Before this change, two doors from the same extension on different matchers would collide on the same hook slot in settings.json. Now each door creates its own entry per event+matcher tuple.

### detect.mjs describeInterfaces

The human-readable interface summary now lists all events a hook registers on, not just the first. Example: `Claude Code Hook: PreToolUse, SessionStart`.

## Why this matters

The branch guard (wip-branch-guard 1.9.73, shipped today) registers on two events:

1. **PreToolUse** (existing): blocks file writes, git commits, and other mutating operations on main branch
2. **SessionStart** (new): fires once per session boot, warns when CWD is main-branch with actionable recovery commands (worktree list, stash escape hatch, pointers to bug plans)

Without the installer update in this release, the guard's new `claudeCode.hooks` array was invisible to `detect.mjs` (which only looked at the legacy singular `claudeCode.hook`), so `ldm install --alpha` would deploy the guard binary to `~/.ldm/extensions/wip-branch-guard/` but not add the SessionStart entry to `~/.claude/settings.json`. The SessionStart hook would never fire.

This release closes that gap. `ldm install --alpha` after this release will detect both doors and add both hook entries.

## Backwards compatibility

Every extension currently shipping with `claudeCode.hook` (singular) continues to work unchanged. The detector normalizes the singular form into a one-element array internally, and the deploy function handles arrays natively. No extension needs to migrate unless it wants to register on multiple events.

## Files changed

- `lib/detect.mjs`: array normalization in the `claudeCodeHook` detection path, updated `describeInterfaces` output
- `lib/deploy.mjs`: renamed inner helper to `installClaudeCodeHookEvent`, new top-level `installClaudeCodeHook` wrapper that iterates arrays; matcher field added to existing-entry lookup key

## Verified

- Detection test: wip-branch-guard (new plural shape) returns a 2-element array with PreToolUse + SessionStart
- Backwards compat test: wip-file-guard (legacy singular shape) returns a 1-element array
- describeInterfaces output for wip-branch-guard now prints `Claude Code Hook: PreToolUse, SessionStart`

## Cross-references

- `ai/product/bugs/guard/2026-04-05--cc-mini--guard-master-plan.md` Phase 7
- `ai/product/bugs/master-plans/bugs-plan-04-05-2026-002.md` Wave 2 phase 13
- Dependency: requires wip-branch-guard 1.9.73 or later (already published to npm via wip-ai-devops-toolbox alpha.11)
