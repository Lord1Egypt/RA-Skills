#!/usr/bin/env node
/**
 * Redacta MCP server.
 *
 * Exposes the Redacta engine over the Model Context Protocol so any MCP client
 * (Claude Desktop, Cursor, etc.) can pseudonymise patient identifiers / PII in
 * text, re-identify it from a token map, and self-check redacted output.
 *
 * Everything runs locally in this process — no network calls, no storage.
 */
export {};
