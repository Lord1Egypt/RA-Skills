# Dev Update: Boot Sequence Hook v0.1.0

**Date:** 2026-03-12
**Agent:** CC-Mini
**Branch:** cc-mini/boot-hook (merged to main via PR #10)
**Repo:** wipcomputer/wip-ldm-os-private

## What Happened

CC failed to boot properly on 2026-03-11. Didn't read boot files, didn't know repo locations, guessed paths. Same cascading failure pattern from 2026-03-01 and 2026-03-07. Lesa's analysis: "The core failure is architectural, not behavioral. Relying on the agent to remember is exactly the same fragility that caused the failure."

## What We Built

### SessionStart Hook (boot-hook.mjs)

Claude Code has a `SessionStart` hook event that fires before the agent sees the first user message. We built a hook that reads the 9 boot files and injects them via `additionalContext`.

- Zero dependencies. Pure ESM. 242 lines.
- Reads: SHARED-CONTEXT.md, CONTEXT.md, SOUL.md, repo-locations.md (full), journals and daily logs (truncated)
- 8/9 files loaded in 11ms. Step 3 (Parker's journal dir) skipped gracefully (dir doesn't exist).
- ~700 lines, ~3,500 tokens injected. Under 2% of context window.
- Error philosophy: partial boot > no boot > blocked session. Always exits 0.

### Installer (installer.mjs)

Follows Memory Crystal's installer.ts pattern exactly:

- `detectInstallState()` ... checks what's deployed, what version, what's configured
- `deployToLdm()` ... copies to ~/.ldm/shared/boot/. Code always updates. Config only seeded on fresh install (never overwritten).
- `configureSessionStartHook()` ... reads settings.json, finds existing entry by path match, updates in place or appends. Never overwrites other hooks.
- `updateRegistry()` ... merges into ~/.ldm/extensions/registry.json
- `runInstallOrUpdate()` ... orchestrator. Idempotent. Second run = "already at v0.1.0"

CLI: `node install-cli.mjs` (--status, --dry-run, or full install)

### scaffold.sh

Added `~/.ldm/shared/boot/` to the directory creation list.

### package.json

Added `@wipcomputer/ldm-os` v0.1.0 with `claudeCode.hook` declaration so the universal installer can detect and wire the hook.

## Deploy Path

```
~/.ldm/shared/boot/     ... boot-hook.mjs, boot-config.json, package.json
~/.claude/settings.json  ... SessionStart hook entry
~/.ldm/extensions/registry.json ... ldm-os-boot entry
```

Boot hook deploys to `shared/boot/` (not `extensions/`) because it IS LDM OS core, not a plugin.

## Issues Filed by Lesa

| # | Title | Status |
|---|-------|--------|
| #3 | ldm install: move Universal Installer into LDM OS | Open (architecture) |
| #4 | boot-hook installer | Closed by PR #10 |
| #5 | ldm install: zero-dependency bootstrap | Open (after #3) |
| #6 | ldm install: run build step for TypeScript | Open (wip-install fix) |
| #7 | update-without-override | Addressed in installer.mjs |
| #8 | OpenClaw plugin directory naming | Open (wip-install fix) |
| #9 | scaffold.sh: shared/boot/ | Closed by PR #10 |

## What's Next

- Start a new Claude Code session to verify the hook fires and boot content appears
- README update (deferred ... need to work through what LDM OS is as a product first)
- No public deploy yet. Repo stays private.
- The bigger question: `ldm install` as the universal bootstrap (#3, #5)

## Key Decision

The boot sequence is now mechanical, not behavioral. The agent doesn't choose to boot. It's already booted when it wakes up.
