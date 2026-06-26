# Bug: ldm install silently upgrades OpenClaw, overwrites dist patches

**Date:** 2026-03-30
**Filed by:** cc-mini
**Repo:** wip-ldm-os-private
**Priority:** critical

## Problem

`ldm install` upgraded OpenClaw from v2026.2.22-2 to v2026.3.28 without warning. This overwrote three dist patches (EMFILE fix, walkDir fix, cron catch-up guard) and changed the gateway's model validation (breaking the lesa-bridge MCP tool).

The upgrade happened on Mar 29 at 12:27 PST as part of a routine `ldm install`. Nobody noticed until Mar 30 when `lesa_send_message` failed.

## What broke

1. **Three dist patches overwritten.** The EMFILE chokidar fix, walkDir ignore set, and cron catch-up guard are all gone. These are documented in `open-claw-upgrade-private/KNOWN-LANDMINES.md` under "Dist Patches (overwritten on every upgrade)."

2. **Gateway model validation tightened.** Old gateway accepted `model: "main"`. New gateway requires `model: "openclaw"` or `model: "openclaw/main"`. The bridge sends `model: "main"` and gets a 400 error.

3. **No patch re-application.** `post-upgrade-patches.sh` was not run. The patches need manual re-application after every OpenClaw upgrade, but `ldm install` doesn't know about them.

## Timeline

- **Mar 15:** Bridge absorbed into LDM OS with `model: agentId` (just `"main"`)
- **Before Mar 29:** Gateway running v2026.2.22-2, accepted `model: "main"`
- **Mar 29 12:27:** `ldm install` upgraded OpenClaw to v2026.3.28 silently
- **Mar 30 07:00:** Gateway restarted with new binary (KeepAlive), picked up v2026.3.28
- **Mar 30:** `lesa_send_message` MCP tool fails with "Invalid model"

## Root cause

OpenClaw is in the `ldm install` catalog as a managed component. The installer sees a newer version on npm and installs it like any other extension. But OpenClaw is the runtime, not an extension. Upgrading it:
- Overwrites dist patches
- Can change API behavior (model validation)
- Can break plugins
- Requires post-upgrade steps documented in KNOWN-LANDMINES.md

## Fix (three parts)

### Part 1: Re-apply patches now
```bash
bash /Users/lesa/wipcomputerinc/repos/ldm-os/devops/open-claw-upgrade-private/post-upgrade-patches.sh
```

### Part 2: Fix the bridge model param
In `src/bridge/core.ts` line 201, change:
```typescript
model: agentId,
```
to:
```typescript
model: `openclaw/${agentId}`,
```

### Part 3: Prevent auto-upgrade
In `bin/ldm.js`, remove OpenClaw from the auto-update catalog. OpenClaw upgrades should be explicit and separate:
```
ldm upgrade openclaw          # explicit command
ldm upgrade openclaw --check  # check what would change
```

The upgrade command should:
1. Show what version is available
2. Show KNOWN-LANDMINES warnings
3. Run post-upgrade-patches.sh after install
4. Restart the gateway
5. Test the bridge connection

### Part 4: Retire cc-watcher
Unload and disable the broken cc-watcher LaunchAgent. Add to dead trigger cleanup in `ldm install`.

## Files to change

| File | Change |
|------|--------|
| `src/bridge/core.ts` | Fix model format (line 201) |
| `bin/ldm.js` | Remove OpenClaw from auto-update catalog, add dead trigger for cc-watcher |
| `catalog.json` | Mark OpenClaw as pinned/manual-only |

## How to test

1. `lesa_send_message("test")` returns Lesa's response (no 400 error)
2. `ldm install --dry-run` does NOT show OpenClaw as an update
3. `ldm upgrade openclaw --check` shows available version
4. `post-upgrade-patches.sh --check` confirms patches are applied
5. `launchctl list | grep cc-watcher` returns nothing
