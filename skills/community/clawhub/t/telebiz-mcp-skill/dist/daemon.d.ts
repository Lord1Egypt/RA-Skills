#!/usr/bin/env node
/**
 * Telebiz MCP Daemon
 *
 * Keeps telebiz-mcp running persistently and exposes an HTTP API for tool calls.
 * This solves the browser reconnection timing issue.
 *
 * Usage:
 *   node daemon.js start   - Start the daemon
 *   node daemon.js stop    - Stop the daemon
 *   node daemon.js status  - Check status
 *   node daemon.js call <tool> [args]  - Call a tool
 */
export {};
