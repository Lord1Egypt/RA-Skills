---
name: zoom-phone-mcp
description: MCP server for the Zoom Phone API. Exposes Zoom Phone's REST API as read-only MCP tools.
metadata: { "openclaw": { "requires": { "bins": ["mcporter", "zoom-phone-mcp"], "env": ["NODE_MCP_SECRET_KEY"] } } }
---

# Zoom Phone MCP Server

Read-only MCP server for the Zoom Phone API.

## Usage

Use mcporter to interact with this server via stdio:

- **List available tools:** `mcporter list --stdio zoom-phone-mcp`
- **Call a tool:** `mcporter call --stdio zoom-phone-mcp <tool_name> [args]`

## Links

- **npm:** https://www.npmjs.com/package/@mjquinlan2000/zoom-phone-mcp
