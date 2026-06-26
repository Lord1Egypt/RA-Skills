# Dev Update: npm Content Leak, Fix, and Clean Publish

**Date:** 2026-03-02 21:00 PST
**Author:** CC-Mini
**Branch:** main (via cc-mini/cloud-mcp and cc-mini/npmignore-fix)

---

## What Happened

### The Leak

`wip-release minor` published `memory-crystal@0.3.0` to npm. The tarball included the entire `ai/` folder: plans, todos, dev updates, product ideas, research notes. 156 files, 503KB.

Root cause: npm does not use `.gitignore` when a `.npmignore` file exists. We had no `.npmignore`. npm published everything not in `.gitignore`. The `ai/` folder is not in `.gitignore` because it's supposed to be in the repo (the private repo). It's just not supposed to be on npm.

Audit revealed `memory-crystal@0.2.0` had the same leak. Also `@wipcomputer/markdown-viewer@1.2.5` leaked `ai/bugs/stale-sse-connections.md`.

### The Fix

1. Unpublished all three leaked versions from npm (0.2.0, 0.3.0, 1.2.5)
2. Added `.npmignore` to memory-crystal excluding `ai/`, `.wrangler/`, `.claude/`, source `.ts` files
3. Published `memory-crystal@0.3.1` clean (74 files, 135KB)
4. Added `.npmignore` to markdown-viewer-private (PR #1 merged)
5. Created `.npmignore` files for 5 other at-risk repos (grok, x, universal-installer, file-guard, agent-pay)
6. Documented the `.npmignore` requirement in Dev Guide private
7. Saved a memory crystal entry for future sessions

### Squash Merge Incident

Also during this session: PR #11 was merged with `--squash`, which collapsed 20+ commits into one and destroyed co-author attribution. Fixed by:
1. Reset main to before the squash (via API: temporarily enabled force push, pushed, re-disabled)
2. Regular merge preserved all commits
3. Added "Never squash merge" rule to both CLAUDE.md files and Dev Guide private

## Current State

- `memory-crystal@0.3.1` live on npm, clean
- GitHub release v0.3.1 created
- All commits preserved on main with full co-author attribution
- `.npmignore` deployed across 6 repos
- No-squash rule documented everywhere

## Files Changed

| File | Change |
|------|--------|
| `.npmignore` | New. Excludes ai/, .wrangler/, .claude/, .ts source |
| `CHANGELOG.md` | v0.3.0 and v0.3.1 entries |
| `package.json` | Version 0.3.1 |
| `wip-dev-tools-private/ai/DEV-GUIDE-private.md` | .npmignore requirement, no-squash rule |
| Both `CLAUDE.md` files | No-squash rule |

## Lessons

1. Every repo with `ai/` needs `.npmignore`. No exceptions.
2. `npm pack --dry-run` before every publish to verify contents.
3. Never squash merge. Every commit tells the story.
4. Consider adding an `ai/` pre-publish check to `wip-release` itself.
