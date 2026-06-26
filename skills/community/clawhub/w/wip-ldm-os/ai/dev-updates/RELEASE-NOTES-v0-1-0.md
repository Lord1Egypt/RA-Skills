# LDM OS v0.1.0 - Boot Sequence Hook

**Date:** 2026-03-12
**PR:** #10 (cc-mini/boot-hook -> main)

First release. Implements the Boot Sequence pillar of LDM OS.

## What's New

### SessionStart Hook

Claude Code `SessionStart` hook that reads 9 boot files and injects them into the agent's context before the first user message. The agent wakes up already knowing who it is, what's happening, and where things live.

- Zero dependencies. Pure ESM. 11ms execution.
- Loads: SHARED-CONTEXT.md, SOUL.md, CONTEXT.md, daily logs, journals, repo-locations.md
- ~700 lines injected (~2% of context window)
- Graceful skip on missing files. Always exits 0.

### Installer

Follows Memory Crystal `installer.ts` pattern:

- Detects install state before touching anything
- Deploys incrementally (code updates, config preserved)
- Configures hook in settings.json without overwriting other hooks
- Updates ~/.ldm/extensions/registry.json
- Idempotent: second run = "already at v0.1.0"
- CLI: --status, --dry-run, full install

### scaffold.sh

Creates `~/.ldm/shared/boot/` alongside `~/.ldm/shared/dream-weaver/`.

### package.json

`@wipcomputer/ldm-os` v0.1.0. Declares `claudeCode.hook` for universal installer detection.

## Files

```
src/boot/boot-hook.mjs      - The SessionStart hook
src/boot/boot-config.json   - Boot step paths and limits
src/boot/installer.mjs      - Install/update logic
src/boot/install-cli.mjs    - CLI wrapper
src/boot/README.md           - Documentation
bin/scaffold.sh              - Updated with shared/boot/
package.json                 - Interface declarations
```

## Deploy

```bash
cd wip-ldm-os-private
node src/boot/install-cli.mjs
```

## Issues Closed

- #4: boot-hook installer
- #9: scaffold.sh creates shared/boot/
