# Release Notes: AI DevOps Toolbox v1.9.11

**Date:** 2026-03-13

## What's new

### Silent LDM OS bootstrap in wip-install
- `wip-install` now installs LDM OS automatically when `ldm` is not on PATH
- Runs `npm install -g @wipcomputer/wip-ldm-os` silently
- Falls back to standalone installer if npm is offline or permissions fail
- Tip message updated to reflect that automatic install was already attempted

### Earlier changes (v1.9.9-v1.9.10)
- **v1.9.10:** publish-skill.sh added, merge/deploy/install bug fixes, product doc plans
- **v1.9.10:** Release notes files on disk always beat --notes flag
- **v1.9.9:** Git worktrees as default workflow. wip-release blocks from worktrees. wip-install auto-adds .claude/worktrees/ to .gitignore. Dev Guide worktree section.
