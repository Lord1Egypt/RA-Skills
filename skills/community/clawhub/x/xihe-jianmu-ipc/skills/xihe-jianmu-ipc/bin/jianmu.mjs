#!/usr/bin/env node
/**
 * bin/jianmu.mjs — CLI for xihe-jianmu-ipc
 *
 * Usage:
 *   jianmu hub     — start the hub server
 *   jianmu status  — show connected sessions
 */

import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const cmd = process.argv[2];

if (cmd === 'hub') {
  // Import and run hub directly
  await import(join(root, 'hub.mjs'));
} else if (cmd === 'status') {
  const port = process.env.IPC_PORT || 3179;
  const host = process.env.IPC_HUB_HOST || '127.0.0.1';
  try {
    const res = await fetch(`http://${host}:${port}/health`);
    const data = await res.json();
    console.log(`Hub uptime: ${Math.floor(data.uptime)}s`);
    if (data.sessions.length === 0) {
      console.log('No sessions connected.');
    } else {
      for (const s of data.sessions) {
        const ago = Math.floor((Date.now() - s.connectedAt) / 1000);
        const topics = s.topics.length ? ` [${s.topics.join(', ')}]` : '';
        console.log(`  ${s.name} — connected ${ago}s ago${topics}`);
      }
    }
  } catch {
    console.error('Hub is not running.');
    process.exit(1);
  }
} else {
  console.log('Usage: jianmu <command>');
  console.log('  hub      Start the hub server');
  console.log('  status   Show connected sessions');
  process.exit(1);
}
