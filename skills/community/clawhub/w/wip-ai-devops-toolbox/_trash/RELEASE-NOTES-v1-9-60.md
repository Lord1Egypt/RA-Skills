# Release Notes: wip-ai-devops-toolbox v1.9.60

**Fix npm package bloat: exclude worktrees and _trash from published tarball.**

## The story

v1.9.59 published 869 files (3.9 MB) to npm because leftover worktree directories and _trash/ were included in the tarball. The .npmignore only excluded ai/ and .DS_Store. Added _trash/, .worktrees/, _worktrees/, .claude/, .wrangler/ to .npmignore. Also cleaned up 10 stale worktrees from previous sessions.

## Issues closed

- #232 (continued cleanup)

## How to verify

```bash
npm pack --dry-run 2>&1 | tail -5
# Should show ~200 files, not 869
```
