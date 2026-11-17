#!/usr/bin/env node
// Start the CDP proxy server as a standalone process.
// Usage: node start-cdp-proxy.mjs [port]

process.env.CDP_PROXY_PORT = process.argv[2] || '3456';
await import('./cdp-proxy.mjs');
