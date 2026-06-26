---
name: forge-setup
description: Install and configure the Forge MCP server for the first time, or verify an existing setup. Use when forge_health_check fails or when setting up a new agent environment.
---

# Forge — Setup

One-time installation and configuration of the Forge MCP server.

## Install

```bash
npx -y @xferops/forge-mcp
```

## Configure

Add to your MCP client config (e.g. `~/.mcporter/mcporter.json`):

```json
{
  "mcpServers": {
    "forge": {
      "command": "npx",
      "args": ["-y", "@xferops/forge-mcp"],
      "env": {
        "FORGE_URL": "https://forge.xferops.dev",
        "FORGE_TOKEN": "your-api-token"
      }
    }
  }
}
```

Get your API token: **Forge → Settings → API Tokens**

## Verify

```
forge_health_check
```

A `200 OK` response means you're connected and authenticated. Any other result:
- **401** — token is wrong or expired; generate a new one in Forge settings
- **Connection refused / timeout** — `FORGE_URL` is wrong, or the service is down

## Legacy env vars

If migrating from the old Flower app, `FLOWER_URL` and `FLOWER_TOKEN` are accepted as fallbacks but deprecated. Update to `FORGE_URL` / `FORGE_TOKEN`.

## Tools used by this skill

| Tool | When |
|------|------|
| `forge_health_check` | Verify the MCP server can reach the Forge API |
