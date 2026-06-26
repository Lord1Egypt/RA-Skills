# Release Notes: AI DevOps Toolbox v1.9.9

**Enforce git worktrees as default workflow (#86)**

Agents forget rules. Code doesn't. Three incidents in 48 hours (mixed commits from parallel subagents, wrong-branch writes, directory collisions) all caused by agents sharing a working tree. This release makes the safe behavior structural.

## What changed

### wip-release: Worktree guard (Phase 5)

`wip-release` now blocks if you're running from inside a git worktree. Releases must happen from the main working tree, on `main`, after PRs are merged. Running from a worktree would create a tag on the wrong branch.

```
✗ wip-release must run from the main working tree, not a worktree.
  Current: /path/to/repo/.claude/worktrees/fix-search/
  Main working tree: /path/to/repo/
  Switch to the main working tree and run again.
```

Detection: `git rev-parse --git-dir` returns a path containing `/worktrees/` for linked worktrees. Override with `--skip-worktree-check`.

### wip-install: Auto-gitignore (Phase 3)

`wip-install` now adds `.claude/worktrees/` to every repo's `.gitignore` during installation. Worktrees are local and ephemeral. They should never be committed.

- Skips `/tmp/` clones (URL installs)
- Skips non-git directories
- Respects `--dry-run`
- Idempotent (won't duplicate if already present)

### Dev Guide: Worktree Workflow section (Phase 2)

New section in the Dev Guide covering the full worktree workflow:

- Every session starts in a worktree
- Branch naming follows harness prefix convention (`cc-mini/`, `lesa-mini/`)
- Subagents use `isolation: "worktree"` for parallel work
- Commit and push before session ends (worktree cleanup deletes uncommitted work)
- `wip-release` must run from the main working tree

### .gitignore

Added `.claude/worktrees/` to this repo's `.gitignore`.

## What's next

- **Phase 4:** Boot hook warning when session is in main working tree (separate PR on wip-ldm-os-private)
- **Phase 6:** Lesa integration (worktrees for spawned parallel work within her agent)

## Fixes

- Closes #86 (phases 2, 3, 5)

## Files changed

```
 .gitignore                               |  1 +
 DEV-GUIDE-GENERAL-PUBLIC.md              | 66 +++
 ai/DEV-GUIDE-FOR-WIP-ONLY-PRIVATE.md    | 12 +
 tools/wip-release/cli.js                 |  3 +
 tools/wip-release/core.mjs               | 32 ++
 tools/wip-universal-installer/install.js | 32 ++
 RELEASE-NOTES-v1-9-9.md                  | (this file)
```

## Install

```bash
git pull origin main
```

## Attribution

Built by Parker Todd Brooks, Lesa, and Claude Opus 4.6 at WIP.computer.
Three parallel agents, each in its own worktree. Phase 1 of the plan, proving itself.
