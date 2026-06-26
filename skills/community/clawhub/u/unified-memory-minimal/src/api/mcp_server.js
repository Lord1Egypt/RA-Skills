/**
 * MCP Server - Python Implementation [DEPRECATED]
 * 
 * ⚠️  DEPRECATED - This is the Python implementation of the MCP server.
 * 
 * For Node.js, MCP is already implemented via the official SDK.
 * Use `openclaw mcp` or the TypeScript MCP implementation instead.
 */

export const DEPRECATED_NOTICE = `
⚠️  DEPRECATED: memory_mcp_server.py

The MCP (Model Context Protocol) server functionality has been migrated to
the Node.js/TypeScript implementation in the OpenClaw MCP SDK.

To use MCP with unified-memory-ts:

1. Configure MCP in openclaw config
2. Use the built-in memory tools via MCP protocol

This Python file is kept for reference only.
`;

export function printDeprecationNotice() {
  console.log(DEPRECATED_NOTICE);
}

if (require.main === module) {
  printDeprecationNotice();
}
