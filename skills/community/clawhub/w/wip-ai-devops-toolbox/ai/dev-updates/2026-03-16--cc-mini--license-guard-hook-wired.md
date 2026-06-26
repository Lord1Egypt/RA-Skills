# Wire license-guard as Claude Code PreToolUse hook

**Date:** 2026-03-16
**Closes:** #130

## What changed

license-guard now registers as a Claude Code PreToolUse hook on install. Previously the hook code existed (hook.mjs) but was never wired into the deploy system. Now:

- Renamed hook.mjs to guard.mjs (matches file-guard/branch-guard convention that LDM OS deploy.mjs expects)
- Added `claudeCode.hook` config to package.json (event: PreToolUse, matcher: Bash, timeout: 5)
- On next `ldm install`, the hook auto-registers in ~/.claude/settings.json

The hook blocks git commit and git push when license compliance fails:
- LICENSE file missing
- Copyright doesn't match .license-guard.json config
- CLA.md missing
- README.md missing ## License section
- MIT+AGPL config but LICENSE or README only mentions MIT

Repos without .license-guard.json are not affected (the hook silently passes).

## Also done

- Updated plan statuses: license guard Phase 1 complete, bootstrap LDM OS complete
- Bootstrap LDM OS was already shipped in install.js (lines 740-812)
