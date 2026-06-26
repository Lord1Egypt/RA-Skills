#!/usr/bin/env node
/**
 * gate.js — Universal pre-send sleep gate.
 *
 * Call this INSTEAD of sending a message directly. It checks the current
 * time against the sleep schedule and either queues the message or lets
 * it through.
 *
 * Usage:
 *   node gate.js --provider telegram --sender-id mybot --sender-name "Stock Bot" --message "your text"
 *
 * Exit codes:
 *   0 — sleeping, message was QUEUED — caller must NOT send
 *   2 — sleeping but URGENT — caller should send with 🚨 prefix
 *   3 — awake — caller is clear to send normally
 *   1 — error (gate failed; caller should send anyway to avoid data loss)
 */

const path = require('path');
const { loadSleepState } = require('../lib/sleep-check');

const QUEUE_SCRIPT = path.join(__dirname, 'queue-message.js');

// ── Parse CLI args ────────────────────────────────────────────────────────────
const args     = process.argv.slice(2);
const get      = (flag) => { const i = args.indexOf(flag); return i !== -1 ? args[i + 1] : null; };
const provider  = get('--provider')    || 'unknown';
const senderId  = get('--sender-id')   || 'unknown';
const senderName = get('--sender-name') || senderId;
const message   = get('--message')     || '';

if (!message) {
  console.error('gate.js: --message is required');
  process.exit(1);
}

// ── Check sleep state ─────────────────────────────────────────────────────────
let isSleeping;
try {
  ({ isSleeping } = loadSleepState());
} catch {
  // Not configured — let the message through
  console.log(JSON.stringify({ action: 'send', reason: 'not_configured' }));
  process.exit(3);
}

if (!isSleeping) {
  console.log(JSON.stringify({ action: 'send', reason: 'awake' }));
  process.exit(3);
}

// ── Sleeping — delegate to queue-message.js ───────────────────────────────────
const { spawnSync } = require('child_process');
const result = spawnSync('node', [
  QUEUE_SCRIPT,
  '--provider',    provider,
  '--sender-id',   senderId,
  '--sender-name', senderName,
  '--message',     message,
], { encoding: 'utf8' });

if (result.stdout) {
  process.stdout.write(result.stdout);
}

// Mirror queue-message.js exit codes (0 = queued, 2 = urgent)
process.exit(result.status ?? 1);
