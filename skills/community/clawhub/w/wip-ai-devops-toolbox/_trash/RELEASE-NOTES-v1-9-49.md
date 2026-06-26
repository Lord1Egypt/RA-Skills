# Release Notes: wip-ai-devops-toolbox v1.9.49

**TECHNICAL.md audit: 2 weeks of undocumented features now documented.**

## What changed

Full TECHNICAL.md audit covering v1.9.15 through v1.9.48. Two passes. Key additions:

- **wip-release quality gates:** Technical docs gate, interface coverage gate, product docs auto-sync, all skip flags documented.
- **deploy-public.sh:** Full 8-step pipeline including GitHub Packages publishing, repo URL rewrite, co-author sync.
- **wip-license-guard:** Now documented as both CLI and Claude Code PreToolUse hook (guard.mjs). Enforcement details.
- **wip-branch-guard:** Worktree requirement on branches, non-repo file passthrough, workflow teaching messages.
- **wip-repos claude:** Cross-repo CLAUDE.md ecosystem generator fully documented.
- **Source code table:** Missing files added (guard.mjs, claude.mjs, mcp-server.mjs).
- **Log paths:** Fixed stale /tmp/ references to ~/.ldm/logs/.

## Why

15 releases shipped without TECHNICAL.md updates. Agents reading the docs were missing critical features: release gates, license enforcement hooks, deploy pipeline details.

## Issues closed

- #218

## How to verify

```bash
grep "Interface coverage" TECHNICAL.md    # new gate
grep "guard.mjs" TECHNICAL.md             # license-guard hook
grep "GitHub Packages" TECHNICAL.md       # deploy pipeline
```
