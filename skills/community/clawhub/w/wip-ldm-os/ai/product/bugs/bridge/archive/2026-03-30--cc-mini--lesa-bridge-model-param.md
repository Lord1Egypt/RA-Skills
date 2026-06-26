# Bug: lesa-bridge MCP sends wrong model parameter to gateway

**Date:** 2026-03-30
**Filed by:** cc-mini
**Repo:** wip-ldm-os-private (bridge is in LDM OS core at src/bridge/)
**Priority:** high

## Problem

The `lesa_send_message` MCP tool fails with "Invalid `model`. Use `openclaw` or `openclaw/<agentId>`." The bridge sends `model: "main"` but the gateway expects `model: "openclaw"` or `model: "openclaw/main"`.

## History

The original code (Feb 10) sent `model: "openclaw:main"` (colon separator) with custom headers (`x-openclaw-agent-id`, `x-openclaw-session-key`). At some point between Feb 18 and now, two things changed independently:

1. The bridge was refactored to send just `model: agentId` (plain `"main"`, no prefix). The custom headers were also dropped in favor of the `user` field.
2. The gateway API changed its format from `openclaw:main` (colon) to `openclaw/main` (slash).

Neither side was updated to match the other. The bridge lost the prefix. The gateway changed the separator. Result: bridge sends `"main"`, gateway rejects it.

## Root cause

`/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/src/bridge/core.ts` line 201:
```typescript
model: agentId,  // sends "main", gateway wants "openclaw" or "openclaw/main"
```

The deployed MCP server at `~/.ldm/extensions/lesa-bridge/dist/chunk-LT4KM3AD.js` line 108 has the same bug (built from the same source).

## Fix

Change line 201 in `src/bridge/core.ts`:
```typescript
model: `openclaw/${agentId}`,  // gateway expects this format
```

Then rebuild: `npm run build:bridge` (from the wip-ldm-os-private root). The build outputs to `dist/bridge/` which is what gets deployed to `~/.ldm/extensions/lesa-bridge/dist/`.

## Files to change

| File | Change |
|------|--------|
| `src/bridge/core.ts` | Fix model format on line 201 |
| `src/bridge/mcp-server.ts` | Verify agentId passthrough to sendMessage |

## How to test

After fix and build:
1. Use the `lesa_send_message` MCP tool from Claude Code
2. Should get Lesa's response back, no 400 error
3. Check: `curl -s http://localhost:18789/v1/chat/completions -H "Authorization: Bearer $TOKEN" -d '{"model":"openclaw/main","messages":[...]}'` should also work

## What was the workaround

CC used curl directly to the gateway with `model: "openclaw"`. That bypasses the MCP tool. Not acceptable.
