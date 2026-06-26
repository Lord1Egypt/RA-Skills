# wip-branch-guard Installation

The guard now registers on two hook events. Add BOTH to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|NotebookEdit|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "node /Users/lesa/.ldm/extensions/wip-branch-guard/guard.mjs",
            "timeout": 5
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node /Users/lesa/.ldm/extensions/wip-branch-guard/guard.mjs",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

Both hook entries point at the same `guard.mjs`. The script auto-detects which event fired from its stdin payload (`hook_event_name`) and branches to the right handler.

Then copy the guard to the extensions directory:

```bash
mkdir -p ~/.ldm/extensions/wip-branch-guard
cp guard.mjs package.json ~/.ldm/extensions/wip-branch-guard/
```

## What it does

**PreToolUse (existing since 1.9.0):**
Blocks file writes, git commits, and other mutating operations when Claude Code is on main branch or a non-worktree feature branch. Agents must use a worktree before editing anything. Specific escape hatches are allowed via `ALLOWED_GIT_PATTERNS` and `ALLOWED_BASH_PATTERNS` (stash push, tag, etc.).

**SessionStart (new in 1.9.73):**
Fires once per session boot, including post-compaction resume. If the session's CWD is the main-branch working tree of a protected repo, injects a warning into the boot context with:
- The repo path
- A list of available linked worktrees (up to 10) with the ready-to-paste `cd <path>` command for each
- A template for creating a fresh worktree
- The native `git stash push` escape hatch in case an untracked file blocks `git pull`
- Pointers to the relevant bug plans

This prevents the "agent wakes up on main after compaction, tries to edit a file, hits the guard, loops" failure mode that wasted approximately $900 of tokens on 2026-04-05.

## What it allows on main (PreToolUse)

- Read, Glob, Grep (read-only tools)
- git status, git log, git diff, git branch, git checkout, git pull, git merge, git push
- git stash push / save / bare (non-destructive; drop/pop/clear still blocked)
- git tag (read-only and delete)
- git worktree
- gh commands (issues, PRs, releases)
- Opening files in browser/mdview
- Writes to deployed extension paths (`.openclaw/extensions/`, `.ldm/extensions/`) for hotfix flows

## What SessionStart does NOT do

- It does not block session boot. The warning is informational only.
- It does not enumerate every possible worktree path; it caps at the first 10 to keep the boot context readable.
- It does not differentiate "main tree" from "worktree on main" — both trigger the warning. This is intentional: a worktree on main is just as dangerous.
- It does not fire for non-git directories. Agents outside a repo get no warning (there is nothing to warn about).

## Test

```bash
# PreToolUse check (CLI mode)
node ~/.ldm/extensions/wip-branch-guard/guard.mjs --check

# SessionStart simulation
echo '{"hook_event_name":"SessionStart","cwd":"/path/to/main/repo","source":"startup"}' | node ~/.ldm/extensions/wip-branch-guard/guard.mjs
```
