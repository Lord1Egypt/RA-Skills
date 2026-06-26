#!/usr/bin/env node
/**
 * Telebiz HTTP MCP Server
 *
 * Wraps telebiz-mcp in an HTTP server so mcporter can connect without spawning
 * a new process. This keeps the browser connection persistent.
 *
 * Usage:
 *   node http-server.js [port]
 *
 * mcporter config:
 *   { "telebiz": { "url": "http://localhost:9718/mcp" } }
 */
export {};
