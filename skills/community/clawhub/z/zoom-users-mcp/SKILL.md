---
name: zoom-users-mcp
description: MCP server for the Zoom Users API. Exposes Zoom Users' REST API as read-only MCP tools.
metadata: { "openclaw": { "requires": { "bins": ["mcporter", "zoom-users-mcp"], "env": ["NODE_MCP_SECRET_KEY"] } } }
---

# Zoom Users MCP Server

Read-only MCP server for the Zoom Users API.

## Usage

Use mcporter to interact with this server via stdio:

- **List available tools:** `mcporter list --stdio zoom-users-mcp`
- **Call a tool:** `mcporter call --stdio zoom-users-mcp <tool_name> [args]`

## Links

- **npm:** https://www.npmjs.com/package/@mjquinlan2000/zoom-users-mcp
