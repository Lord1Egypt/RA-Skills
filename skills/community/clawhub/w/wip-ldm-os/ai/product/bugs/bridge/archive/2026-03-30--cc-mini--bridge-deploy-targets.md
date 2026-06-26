# Bug: bridge deploys to one location but runs from another

**Date:** 2026-03-30
**Filed by:** cc-mini
**Repo:** wip-ldm-os-private
**Priority:** high

## Problem

The bridge exists in three locations, but `deployBridge()` (added in PR #249) only deploys to one of them. Bridge fixes never reach the locations where MCP and OpenClaw actually load the code.

| Location | What uses it | Deployed by installer? |
|----------|-------------|----------------------|
| `~/.ldm/extensions/lesa-bridge/dist/` | Nothing currently reads from here directly | Yes (PR #249) |
| `~/.openclaw/extensions/lesa-bridge/dist/` | OpenClaw plugin (`openclaw.js`) AND Claude Code MCP server (`mcp-server.js`) | No |
| `/opt/homebrew/lib/node_modules/@wipcomputer/wip-ldm-os/dist/bridge/` | npm package (source of truth after `npm install -g`) | N/A (npm manages this) |

Claude Code's MCP registration points to `~/.openclaw/extensions/lesa-bridge/dist/mcp-server.js`. OpenClaw loads the plugin from the same directory. The installer only copies files to `~/.ldm/extensions/lesa-bridge/dist/`. So bridge fixes land in a directory nobody reads from, while the two directories that actually run the bridge stay stale.

## Root cause

`deployBridge()` was written to deploy to `~/.ldm/extensions/lesa-bridge/dist/` only. The OpenClaw location (`~/.openclaw/extensions/lesa-bridge/dist/`) was not included as a deploy target. Additionally:

1. **Stale chunk files:** The function copies new `.js` files but does not remove old chunk files. Webpack/Rollup chunk hashes change between builds, so old chunks accumulate in the target directory.
2. **MCP registration drift:** The MCP server registration points to `~/.openclaw/extensions/lesa-bridge/dist/mcp-server.js`. Even after fixing the deploy, it should point to `~/.ldm/extensions/lesa-bridge/dist/mcp-server.js` (the canonical LDM path).

## Fix

Update `deployBridge()` to:
1. Deploy to both `~/.ldm/extensions/lesa-bridge/dist/` and `~/.openclaw/extensions/lesa-bridge/dist/`
2. Clean stale `.js` files from target directories before copying new files
3. Re-register the MCP server to point to the LDM path: `claude mcp add lesa-bridge --scope user -- node ~/.ldm/extensions/lesa-bridge/dist/mcp-server.js`

## Files to change

| File | Change |
|------|--------|
| `bin/ldm.js` | Update `deployBridge()` to deploy to both targets, clean stale files, re-register MCP |

## How to test

1. Make a change to `src/bridge/core.ts`
2. Build: `npm run build:bridge`
3. Publish: `wip-release patch`
4. Run: `ldm install`
5. Check both targets:
   - `diff ~/.ldm/extensions/lesa-bridge/dist/core.js /opt/homebrew/lib/node_modules/@wipcomputer/wip-ldm-os/dist/bridge/core.js`
   - `diff ~/.openclaw/extensions/lesa-bridge/dist/core.js /opt/homebrew/lib/node_modules/@wipcomputer/wip-ldm-os/dist/bridge/core.js`
6. Both should match. Before the fix, OpenClaw's copy would be stale.
7. Check MCP registration: `claude mcp list` should show `~/.ldm/extensions/lesa-bridge/dist/mcp-server.js`
