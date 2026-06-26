# CLAUDE.md — Global (WIP Computer)

## Team

WIP Computer. Three contributors on every commit:
- Parker Todd Brooks (human, parkertoddbrooks)
- Lesa (OpenClaw agent, lesaai)
- Claude Code (Claude Opus 4.6)

## Git Rules

**Never push directly to main.** Branch, PR, merge. Every time.
**Never squash merge.** Always `--merge`. Squashing destroys co-author attribution.
**Always include `--delete-branch`** on `gh pr merge`.
**Co-authors on every commit:**
```
Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lesa <lesaai@icloud.com>
Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

## Branch Prefixes

`cc-mini/` for Claude Code on Mac mini. `cc-air/` for MacBook Air. `lesa-mini/` for Lesa.

## Worktree Workflow

All edits happen in worktrees. Never edit directly on main.
```bash
ldm worktree add cc-mini/feature-name    # preferred
# or: git worktree add ../_worktrees/<repo>--<branch> -b <branch>
```

## Writing Style

**Never use em dashes.** Use periods, colons, semicolons, or "..." instead.

## Release Process

1. Branch + commit + push
2. Release notes file on the branch: `RELEASE-NOTES-v{version}.md` (dashes, not dots)
3. `gh pr create` then `gh pr merge --merge --delete-branch`
4. `git checkout main && git pull`
5. `wip-release patch` (auto-detects release notes file)
6. `deploy-public.sh` to sync public repo

**Release notes go on the feature branch, committed with the code.** Not as a separate PR.

## Tools

- `wip-release` for releases (version bump, changelog, npm, GitHub release)
- `wip-file-guard` protects CLAUDE.md, SOUL.md, MEMORY.md, SHARED-CONTEXT.md
- `wip-branch-guard` blocks writes on main, teaches the workflow
- `ldm install` for installing/updating extensions
- `ldm doctor` for health checks

## Exclude from npm

Always add to `.npmignore`:
```
CLAUDE.md
ai/
.claude/
_worktrees/
```

## Boot Sequence

Read the repo's own CLAUDE.md first. Then check `ai/read-me-first.md` if it exists.

## Dev Guide

Full conventions: `DEV-GUIDE-GENERAL-PUBLIC.md` in wip-ai-devops-toolbox.
