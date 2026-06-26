# Bug: ldm install --dry-run misses its own updates and parent package updates

## Context

After releasing memory-crystal v0.7.28, LDM OS v0.4.30, and wip-ai-devops-toolbox v1.9.45, `ldm install --dry-run` only detected 3 updates: wip-xai-grok, wip-xai-grok-private (ghost), and wip-release. It missed LDM OS itself, the full toolbox, and showed a ghost private extension.

This broke when universal installer was moved internally into LDM OS (last night, v0.4.29).

## Observed behavior

```
ldm install --dry-run

3 updates available:
  wip-xai-grok         v1.0.2 -> v1.0.3
  wip-xai-grok-private v1.0.2 -> v1.0.3   <-- ghost, shouldn't exist
  wip-release          v1.9.44 -> v1.9.45  <-- should be wip-ai-devops-toolbox

LDM OS CLI is at v0.4.30 (latest)          <-- was v0.4.29, should show update
```

Missing:
- LDM OS CLI v0.4.29 -> v0.4.30
- wip-ai-devops-toolbox v1.9.44 -> v1.9.45 (shows as wip-release instead)
- memory-crystal update (happened to be current, but the detection path is correct for this one)

## Root Cause

Three bugs in `cmdInstallCatalog()` at `bin/ldm.js`:

### Bug 1: CLI self-update is display-only (lines 857-886)

Dry-run checks `npm view @wipcomputer/wip-ldm-os version` but only uses the result for console output. Never added to `npmUpdates[]`. Real installs update the CLI separately (lines 704-725) but only when `!DRY_RUN`.

### Bug 2: Parent packages not detected (line 774)

Update loop iterates extensions from `~/.ldm/extensions/` directories. The toolbox installs 12 individual sub-tool dirs but no parent `wip-ai-devops-toolbox` dir. Parent is never checked. Only `wip-release` gets caught (it has `@wipcomputer/wip-ai-devops-toolbox` in its package.json), so the update shows attributed to wip-release, not the parent.

### Bug 3: Ghost -private extensions in registry

Pre-v0.4.30 `ldm install wipcomputer/wip-xai-grok-private` created registry entries with `-private` suffix and `ldm-install-` prefix. The v0.4.30 redirect fix prevents new ones but doesn't clean existing ghosts.

## Fix

### 1. CLI self-update: add to npmUpdates[]

Before the extension loop (~line 773), check CLI version and add to `npmUpdates[]` with `isCLI: true`.

### 2. Parent package detection

After the extension loop, iterate catalog entries with `registryMatches`. If any match is installed, check the parent npm package. Report as parent name.

### 3. Registry cleanup

At start of `cmdInstallCatalog()`, scan registry for `-private` duplicates and `ldm-install-` prefixed entries. Remove them.

### 4. Install actions

- `isCLI: true` -> `npm install -g @wipcomputer/wip-ldm-os@${latest}`
- `isParent: true` -> update ALL registryMatches sub-tools, not just one

## Files

- `wip-ldm-os-private/bin/ldm.js` (cmdInstallCatalog function, ~line 666)

## Related

- v0.4.29 moved universal installer into LDM OS
- v0.4.30 added catalog lookup, private redirect, staging dir fixes
- This is the next fix in that sequence
