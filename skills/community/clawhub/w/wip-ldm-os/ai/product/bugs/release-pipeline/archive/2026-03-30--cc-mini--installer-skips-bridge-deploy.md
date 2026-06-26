# Bug: installer skips bridge deploy on CLI self-update

**Date:** 2026-03-30
**Filed by:** cc-mini
**Repo:** wip-ldm-os-private
**Priority:** high

## Problem

When `ldm install` updates the LDM OS CLI (e.g. v0.4.62 to v0.4.63), it runs `npm install -g @wipcomputer/wip-ldm-os@<latest>` which updates the binary at `/opt/homebrew/bin/ldm`. But it never deploys the bridge files from the npm package to `~/.ldm/extensions/lesa-bridge/dist/`.

This means bridge fixes (like the model param fix in v0.4.63) don't take effect until someone manually copies the files.

## Root cause

Two missing deploy steps in `bin/ldm.js`:

1. **Self-update gap (cmdInstallCatalog, line ~1161):** After `npm install -g`, the CLI re-execs itself with the new binary. But neither the old nor the new code copies `dist/bridge/*` from the npm package to `~/.ldm/extensions/lesa-bridge/dist/`. The new CLI starts running but the bridge extension still has the old files.

2. **Init gap (cmdInit, line ~396):** `cmdInit` deploys hooks, scripts, rules, boot-config, LaunchAgents, templates, and docs. It does not deploy bridge files. So even a fresh `ldm init` leaves the bridge stale if it was previously installed.

## Where the files are

| Location | Description |
|----------|-------------|
| `/opt/homebrew/lib/node_modules/@wipcomputer/wip-ldm-os/dist/bridge/` | npm package (source of truth after install) |
| `~/.ldm/extensions/lesa-bridge/dist/` | deployed bridge (what MCP servers and OpenClaw actually run) |

The npm package ships `dist/bridge/core.js`, `dist/bridge/mcp-server.js`, `dist/bridge/cli.js`, plus chunk files and `.d.ts` type declarations. The deploy target also has `index.js` and `openclaw.js` from the old standalone bridge build. Those are not in the LDM OS npm package. Overwriting just the files from the package is safe because the MCP server entry point is `mcp-server.js` and the CLI entry point is `cli.js`.

## Why it matters

The bridge is the communication layer between Claude Code and OpenClaw. Any fix to `src/bridge/` (model param, memory search, conversation search) only lands in the npm package. Without a deploy step, the fix never reaches the running extension. Parker has to manually `cp` files or the fix is invisible.

## Fix

Add a `deployBridge()` function that:
1. Resolves the npm package location via `require.resolve` or known path
2. Checks if `~/.ldm/extensions/lesa-bridge/` exists (only deploy if the extension is installed)
3. Copies all `dist/bridge/*` files to `~/.ldm/extensions/lesa-bridge/dist/`

Call it from:
- `cmdInit()` ... after the other deploy steps
- `cmdInstallCatalog()` ... after the self-update npm install, and also unconditionally during normal catalog install

## Files to change

| File | Change |
|------|--------|
| `bin/ldm.js` | Add `deployBridge()` function. Call from `cmdInit()` and `cmdInstallCatalog()`. |

## How to test

1. Make a change to `src/bridge/core.ts`
2. Build: `npm run build:bridge`
3. Publish: `wip-release patch`
4. Run: `ldm install`
5. Check: `diff ~/.ldm/extensions/lesa-bridge/dist/core.js /opt/homebrew/lib/node_modules/@wipcomputer/wip-ldm-os/dist/bridge/core.js`
6. Files should match. Before the fix, they would differ.
