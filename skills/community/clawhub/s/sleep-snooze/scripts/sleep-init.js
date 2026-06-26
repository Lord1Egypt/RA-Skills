#!/usr/bin/env node
/**
 * sleep-init.js
 * One-time setup: write config, create SQLite DB, register cron jobs.
 * Called by OpenClaw when the user runs /snooze-setup.
 *
 * Usage:
 *   node sleep-init.js --sleep-start 22:00 --wake-time 06:00 --timezone Asia/Kolkata
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const DATA_DIR = path.join(process.env.HOME, '.openclaw', 'skills', 'sleep-snooze', 'data');
const STATE_FILE = path.join(DATA_DIR, 'state.json');
const DB_FILE = path.join(DATA_DIR, 'queue.db');
const VIP_FILE = path.join(DATA_DIR, 'vip-contacts.json');

// ── Parse CLI args ────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
const get = (flag) => {
  const idx = args.indexOf(flag);
  return idx !== -1 ? args[idx + 1] : null;
};

const sleepStart = get('--sleep-start') || process.env.SLEEP_START || '22:00';
const wakeTime   = get('--wake-time')   || process.env.WAKE_TIME   || '06:00';
const timezone   = get('--timezone')    || process.env.TIMEZONE    || 'UTC';

// ── Create data directory ─────────────────────────────────────────────────────
fs.mkdirSync(DATA_DIR, { recursive: true });

// ── Write state.json ──────────────────────────────────────────────────────────
const state = {
  sleepStart,
  wakeTime,
  timezone,
  manualOverride: false,
  isSleeping: false,
  lastDigestAt: null,
};
fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
console.log(`✅ Config saved: sleep ${sleepStart} → wake ${wakeTime} (${timezone})`);

// ── Bootstrap SQLite queue ────────────────────────────────────────────────────
try {
  const Database = require('better-sqlite3');
  const db = new Database(DB_FILE);
  db.exec(`
    CREATE TABLE IF NOT EXISTS queue (
      id          INTEGER PRIMARY KEY AUTOINCREMENT,
      provider    TEXT    NOT NULL,
      sender_id   TEXT    NOT NULL,
      sender_name TEXT,
      message     TEXT    NOT NULL,
      received_at TEXT    NOT NULL DEFAULT (datetime('now')),
      delivered   INTEGER NOT NULL DEFAULT 0
    );
    CREATE INDEX IF NOT EXISTS idx_delivered ON queue(delivered);
  `);
  db.close();
  console.log(`✅ Queue database ready: ${DB_FILE}`);
} catch (err) {
  console.error('⚠️  Could not initialise SQLite (is better-sqlite3 installed?)', err.message);
  process.exit(1);
}

// ── Write empty VIP contacts if not present ───────────────────────────────────
if (!fs.existsSync(VIP_FILE)) {
  fs.writeFileSync(VIP_FILE, JSON.stringify({ contacts: [] }, null, 2));
  console.log(`✅ VIP contacts file created: ${VIP_FILE}`);
}

// ── Register cron jobs ────────────────────────────────────────────────────────
const scriptDir = path.join(process.env.HOME, '.openclaw', 'skills', 'sleep-snooze', 'scripts');

// Parse HH:MM into cron fields
const toCron = (hhmm) => {
  const [h, m] = hhmm.split(':').map(Number);
  return `${m} ${h} * * *`;
};

const sleepCron = toCron(sleepStart);
const wakeCron  = toCron(wakeTime);

const sleepJob = `${sleepCron} node ${scriptDir}/set-sleep-mode.js --mode sleep`;
const wakeJob  = `${wakeCron}  node ${scriptDir}/digest.js && node ${scriptDir}/set-sleep-mode.js --mode wake`;

try {
  // Read existing crontab, strip any old sleep-snooze entries, append new ones
  let existing = '';
  try { existing = execSync('crontab -l 2>/dev/null').toString(); } catch { /* no crontab yet */ }

  const filtered = existing
    .split('\n')
    .filter(line => !line.includes('sleep-snooze'))
    .join('\n')
    .trim();

  const newCrontab = [
    filtered,
    `# sleep-snooze: activate sleep mode`,
    sleepJob,
    `# sleep-snooze: deliver morning digest and deactivate sleep mode`,
    wakeJob,
    '',
  ].join('\n');

  const tmpFile = `/tmp/sleep-snooze-cron-${Date.now()}.txt`;
  fs.writeFileSync(tmpFile, newCrontab);
  execSync(`crontab ${tmpFile}`);
  fs.unlinkSync(tmpFile);

  console.log(`✅ Cron jobs registered:`);
  console.log(`   Sleep  → ${sleepCron} (${sleepStart})`);
  console.log(`   Digest → ${wakeCron}  (${wakeTime})`);
} catch (err) {
  console.error('⚠️  Could not update crontab:', err.message);
  console.log('   Add these lines to your crontab manually:');
  console.log(`   ${sleepJob}`);
  console.log(`   ${wakeJob}`);
}

console.log('\n🌙 Sleep Snooze is ready! Notifications will be queued during your sleep window.');
