# v1.9.71-alpha.11

## wip-branch-guard: SessionStart hook for main-CWD detection (Phase 13)

The guard now runs on two hook events, not just one:

1. **PreToolUse** (existing since 1.9.0): blocks file writes, git commits, and other mutating operations on main branch. Specific escape hatches via `ALLOWED_GIT_PATTERNS` and `ALLOWED_BASH_PATTERNS`.
2. **SessionStart** (new in 1.9.73): fires once per session boot, including startup, resume, and post-compaction resume. If the session's CWD is the main-branch working tree of a protected git repo, injects a warning into the boot context with actionable recovery commands.

## Why SessionStart matters

Earlier today's session ($900 of Opus tokens, 60 minutes of wall time) began with the agent waking up on main-branch CWD, trying to edit a file, hitting the PreToolUse guard, and entering a retry loop because the abstract error message did not give the agent the specific command it needed to unblock. The same class of failure had trapped at least two prior sessions earlier in the week.

The fix was multi-layered:

- Phase 1 (shipped in 1.9.72): make the `git stash push` escape hatch available so there's always a native way out
- Phase 2, 4, 6-11 (shipped today): fix the release pipeline so guard fixes actually reach the runtime
- **Phase 13 (this release): prevent the loop from starting in the first place by warning at session boot**

## What the SessionStart hook does

On every session boot, the guard checks if the CWD is in a git repo, reads the current branch, and:

- **Not in a git repo** → silent exit (nothing to warn about).
- **Not on main or master** → silent exit (feature branches are fine).
- **On main or master** → emits a warning via `hookSpecificOutput.additionalContext` that includes:
  - The repo path
  - A list of existing linked worktrees (first 10) with ready-to-paste `cd <path>` commands for each, annotated with the branch name
  - The template for creating a fresh worktree: `git worktree add .worktrees/<repo>--cc-mini--<feature> -b cc-mini/<feature>`
  - The native `git stash push` escape hatch instructions in case an untracked file blocks `git pull`
  - Pointers to the guard master plan and the bugs-plan-04-05-2026-002 master plan

The warning is informational. It does NOT block session boot. An agent that wakes up on main gets the warning in its initial context so the first time it reaches for a write operation, it already knows the recovery path.

## Implementation

Single-file change to `guard.mjs`. The existing `main()` function now dispatches on `hook_event_name` (falling back to shape detection for older payloads). A new `handleSessionStart(input)` function handles the SessionStart path, exiting the process when it's done.

`package.json` `claudeCode.hooks` now advertises both events. `INSTALL.md` updated with the new two-event wiring.

## New hook wiring

Both events point at the same `guard.mjs` script. Add both to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|NotebookEdit|Bash",
        "hooks": [
          { "type": "command", "command": "node /Users/lesa/.ldm/extensions/wip-branch-guard/guard.mjs", "timeout": 5 }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          { "type": "command", "command": "node /Users/lesa/.ldm/extensions/wip-branch-guard/guard.mjs", "timeout": 5 }
        ]
      }
    ]
  }
}
```

## Files changed

- `tools/wip-branch-guard/guard.mjs`: new `handleSessionStart(input)`, event dispatcher in `main()`, worktree enumeration helper
- `tools/wip-branch-guard/package.json`: 1.9.72 -> 1.9.73, `claudeCode.hook` -> `claudeCode.hooks` (array of two entries)
- `tools/wip-branch-guard/INSTALL.md`: complete rewrite with new two-event wiring, what each event does, and test invocations for both
- `tools/wip-branch-guard/test.sh`: three new SessionStart test cases (main tree warns, feature branch silent, non-git silent)
- `CHANGELOG.md`: entry for 1.9.73

## Verified

- 36/36 test cases pass (33 existing PreToolUse + 3 new SessionStart)
- Manual injection with `echo '{"hook_event_name":"SessionStart","cwd":"...","source":"startup"}' | node guard.mjs` produces expected output
- Manual injection with feature-branch CWD exits silently
- Manual injection with /tmp (non-git) exits silently
- Existing PreToolUse tests unchanged, no regressions

## Cross-references

- `ai/product/bugs/guard/2026-04-05--cc-mini--guard-master-plan.md` Phase 7 (guard master plan's Phase 7 maps to this release)
- `ai/product/bugs/master-plans/bugs-plan-04-05-2026-002.md` Wave 2 phase 13
- Prior guard ships today: 1.9.72 (stash allow), 1.9.73 (this release)
- Settings.json wiring needs to be deployed to `~/.claude/settings.json` for the SessionStart hook to activate. `ldm install` should handle this.
