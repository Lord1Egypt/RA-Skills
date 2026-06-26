# MCP Setup

Use this file when MCP connectivity is missing or inconsistent.

## ClawHub Context
- Registry site: `https://clawhub.ai`
- ClawHub is the public OpenClaw skill registry.
- Skills installed via `clawhub` CLI are loaded by OpenClaw in the next session.

Quick checks:
- `clawhub whoami`
- `clawhub list`

## WhiteBIT Docs MCP Server
WhiteBIT documents an MCP server URL for documentation search:
- `https://docs.whitebit.com/mcp`

Example config pattern (`mcp.json` style):

```json
{
  "mcpServers": {
    "whitebit-docs": {
      "url": "https://docs.whitebit.com/mcp"
    }
  }
}
```

Validation prompts:
- `What MCP tools do you have available?`
- `Search for information about authentication in the WhiteBIT documentation.`

## OpenClaw MCP Server
Use the OpenClaw MCP server configured in the user's environment for actual trading actions.

Required behavior:
- Discover tools at runtime.
- Map tools to capabilities before execution (`market data`, `balances`, `place order`, `cancel order`, `order status`).
- If required trading capability is missing, stop and report exactly which capability is unavailable.

## Troubleshooting Shortlist
1. Confirm server URL and connector name are correct.
2. Restart the AI client after config changes.
3. Re-check tool listing before retrying trade logic.
