# Plan: LDM OS Boot Hook with Proper Installer (v2)

## Context

CC's boot sequence failed again on 2026-03-11. The agent didn't read its boot files, causing cascading failures (no repo locations, guessed paths, forgot identity). We built a `SessionStart` hook (`boot-hook.mjs`) that mechanically injects boot content. But we deployed it manually (cp + edit settings.json), which bypasses the entire installer infrastructure.

This plan adds the proper installer, following the Memory Crystal `installer.ts` pattern. The installer detects what's deployed, compares versions, deploys incrementally (never nuke and replace), and registers the hook in `~/.claude/settings.json` without overwriting existing entries.

Lesa filed issues #3-#9 on wip-ldm-os-private. This plan addresses #4 (installer) and #9 (scaffold) directly. Issues #3, #5, #6, #7, #8 are architecture/wip-install fixes that stay filed for later.

## Branch

`cc-mini/boot-hook` on `wipcomputer/wip-ldm-os-private` (already pushed, has boot-hook.mjs + boot-config.json + plan PRD).

## What to Build (in order)

### 1. Update scaffold.sh (issue #9)

Add `~/.ldm/shared/boot/` to the directory creation list. One line change.

**File:** `bin/scaffold.sh`
**Change:** Add `"${LDM_HOME}/shared/boot"` to the `dirs` array (line 22-27), next to `shared/dream-weaver`.

### 2. Add package.json (issue #4)

Repo root needs a `package.json` so the universal installer can detect it.

**File:** `package.json` (new, at repo root)
```json
{
  "name": "@wipcomputer/ldm-os",
  "version": "0.1.0",
  "type": "module",
  "description": "LDM OS: identity, memory, and sovereignty infrastructure for AI agents",
  "main": "src/boot/boot-hook.mjs",
  "bin": {
    "ldm-scaffold": "./bin/scaffold.sh"
  },
  "claudeCode": {
    "hook": {
      "event": "SessionStart",
      "matcher": "*",
      "command": "node ${installedPath}/src/boot/boot-hook.mjs",
      "timeout": 15
    }
  },
  "files": [
    "src/boot/",
    "bin/",
    "templates/"
  ],
  "license": "MIT"
}
```

### 3. Build installer.mjs (issue #4, core work)

Follow Memory Crystal's `installer.ts` as the reference pattern. Pure ESM, zero dependencies.

**File:** `src/boot/installer.mjs` (new)

**Functions to implement (matching Memory Crystal pattern):**

#### `detectInstallState()`
Checks:
- Does `~/.ldm/shared/boot/` exist?
- Does `~/.ldm/shared/boot/boot-hook.mjs` exist?
- What version is deployed? (read `~/.ldm/shared/boot/package.json` if present)
- Is the SessionStart hook registered in `~/.claude/settings.json`?
- Is `boot-config.json` deployed?

Returns: `{ bootDirExists, hookDeployed, hookConfigured, configDeployed, installedVersion, repoVersion, needsUpdate }`

#### `deployToLdm()`
- Creates `~/.ldm/shared/boot/` if missing
- Copies `boot-hook.mjs` to `~/.ldm/shared/boot/`
- Copies `package.json` to `~/.ldm/shared/boot/` (version tracking)
- For `boot-config.json`: **only copy if not present**. If it exists, leave it alone (user may have customized paths/limits). This is the "update without override" principle (issue #7).

#### `configureSessionStartHook()`
Following `configureCCHook()` from Memory Crystal (lines 289-332):
- Reads `~/.claude/settings.json`
- Ensures `hooks.SessionStart` array exists
- Searches existing entries for one whose command includes `boot-hook` or `ldm-os`
- If found: update in place (new path, new timeout)
- If not found: append new entry
- Writes back. Never overwrites other hook entries.

#### `updateRegistry()`
- Reads `~/.ldm/extensions/registry.json`
- Adds/updates entry for `ldm-os-boot` with version, interfaces, paths
- Writes back

#### `runInstallOrUpdate()`
Orchestrator (matching Memory Crystal lines 499-744):
1. Detect install state
2. If up-to-date, return early
3. Run scaffold (call `scaffold.sh` or create dirs directly)
4. `deployToLdm()`
5. `configureSessionStartHook()`
6. `updateRegistry()`
7. Return `{ action, version, steps }`

### 4. Add CLI entry point

**File:** `src/boot/install-cli.mjs` (new, ~30 lines)

Simple CLI wrapper that calls `runInstallOrUpdate()` and prints results. Allows:
```bash
node src/boot/install-cli.mjs           # install/update
node src/boot/install-cli.mjs --status  # show install state
node src/boot/install-cli.mjs --dry-run # preview without changes
```

This is what an agent or human runs after building/pulling.

## Critical Files Reference

| File | Purpose | Pattern Source |
|------|---------|---------------|
| `src/boot/installer.mjs` | Installer logic | `memory-crystal-private/src/installer.ts` (lines 1-744) |
| `src/boot/boot-hook.mjs` | The SessionStart hook | Already built, deployed |
| `src/boot/boot-config.json` | Boot step paths/limits | Already built, deployed |
| `bin/scaffold.sh` | LDM directory structure | Already exists, needs 1 line |
| `package.json` | Interface declarations | New file at repo root |

## Deploy Path Architecture

```
~/.ldm/shared/boot/          ... LDM OS core (boot hook)
~/.ldm/shared/dream-weaver/  ... LDM OS core (consolidation)
~/.ldm/extensions/            ... plugins (memory-crystal, bridge, etc.)
~/.openclaw/extensions/       ... OpenClaw symlinks to ~/.ldm/extensions/
```

Boot hook goes to `shared/boot/` (not `extensions/`) because it IS LDM OS, not a plugin.

## Settings.json Hook Entry

The installer writes this (matching what's already manually deployed):

```json
"SessionStart": [
  {
    "matcher": "*",
    "hooks": [
      {
        "type": "command",
        "command": "node /Users/lesa/.ldm/shared/boot/boot-hook.mjs",
        "timeout": 15
      }
    ]
  }
]
```

## "Update Without Override" Rules (issue #7)

1. **boot-hook.mjs**: Always overwrite. This is code. New version = new code.
2. **boot-config.json**: Only deploy if not present. User customizations survive updates.
3. **settings.json**: Read, merge, write. Find existing entry by command path match, update in place. Never remove other hooks.
4. **registry.json**: Read, merge, write. Update the `ldm-os-boot` entry only.
5. **~/.ldm/shared/boot/ directory**: Create if missing. Never delete contents.

## Open Issues (filed on wip-ldm-os-private)

| # | Title | Status |
|---|-------|--------|
| #3 | ldm install: move Universal Installer into LDM OS | Architecture (future) |
| #4 | boot-hook: installer that detects, deploys, registers without overriding | **BUILD NOW** |
| #5 | ldm install: zero-dependency bootstrap | Architecture (after #3) |
| #6 | ldm install: run build step for TypeScript extensions | wip-install fix (later) |
| #7 | ldm install: update-without-override | **Addressed in installer.mjs** |
| #8 | ldm install: handle OpenClaw plugin directory naming | wip-install fix (later) |
| #9 | scaffold.sh: create ~/.ldm/shared/boot/ | **BUILD NOW** |

## Verification

After building, test the full chain:

```bash
# 1. Test installer detection
node src/boot/install-cli.mjs --status

# 2. Test dry run
node src/boot/install-cli.mjs --dry-run

# 3. Run actual install (should detect existing manual deploy and update cleanly)
node src/boot/install-cli.mjs

# 4. Verify hook still works
echo '{"session_id":"test","hook_event_name":"SessionStart"}' | node ~/.ldm/shared/boot/boot-hook.mjs > /dev/null && echo "OK"

# 5. Verify settings.json has exactly one SessionStart entry (no duplicates)
python3 -c "import json; s=json.load(open('$HOME/.claude/settings.json')); print(len(s['hooks']['SessionStart']), 'SessionStart entries')"

# 6. Start new Claude Code session, verify boot content appears
```

## Implementation Sequence

1. Update `bin/scaffold.sh` (add `shared/boot/` to dirs)
2. Create `package.json` at repo root
3. Write `src/boot/installer.mjs` (detect, deploy, configure, registry)
4. Write `src/boot/install-cli.mjs` (CLI wrapper)
5. Test locally (--status, --dry-run, full install)
6. Commit all changes to `cc-mini/boot-hook` branch
7. Push, PR to main
