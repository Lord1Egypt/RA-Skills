#!/usr/bin/env node
// Start the relay server as a standalone process.
// Usage: node start-relay.mjs [port]

import { Relay } from './relay.mjs';

const port = parseInt(process.argv[2] || '3459', 10);
const relay = new Relay({ wsPort: port });

console.log(`[relay] started on :${port}, waiting for extension...`);

await relay.waitForExtension({ timeout: 0 }).catch(() => {});
console.log('[relay] extension connected (or timed out)');

process.on('SIGINT', async () => { await relay.close(); process.exit(0); });
process.on('SIGTERM', async () => { await relay.close(); process.exit(0); });

// Keep process alive
setInterval(() => {}, 1 << 30);
