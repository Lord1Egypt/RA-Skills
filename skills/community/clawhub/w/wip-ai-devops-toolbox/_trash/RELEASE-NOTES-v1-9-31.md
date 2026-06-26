# Release Notes: wip-ai-devops-toolbox v1.9.31

Branch guard no longer blocks global npm operations on main.

## What changed

Moved `npm install -g` and `npm link` from BLOCKED_BASH_PATTERNS to ALLOWED_BASH_PATTERNS in `wip-branch-guard/guard.mjs`. Global npm operations modify `/opt/homebrew/`, not the repo. Local `npm install` (no -g flag) remains blocked.

## Why

During LDM OS v0.4.0 dogfood, a CC session couldn't run `npm install -g @wipcomputer/wip-ldm-os@0.4.0` even after Parker explicitly said "install." The guard was too aggressive. Original intent (issue #137) was to block repo writes on main, not system-level package installs.

## Issues closed

- Closes #188 (branch guard blocks npm install -g)
- Cross-ref: wipcomputer/wip-ldm-os#44

## How to verify

```bash
# On main branch, these should now succeed:
npm install -g @wipcomputer/wip-ldm-os@0.4.0
npm link
# This should still be blocked on main:
npm install
```
