/**
 * MCP Server Core Infrastructure
 * Entry point: MCP server setup, transport, and core configuration
 */
import { McpServer } from '/root/.openclaw/node_modules/@modelcontextprotocol/sdk/dist/cjs/server/mcp.js';
import { StdioServerTransport } from '/root/.openclaw/node_modules/@modelcontextprotocol/sdk/dist/cjs/server/stdio.js';
import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export { McpServer, StdioServerTransport, http, fs, path, fileURLToPath };
export { __dirname };
