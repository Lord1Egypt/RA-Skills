/**
 * Verify Node version, npm dependencies, credentials presence, and setup freshness.
 * Usage: node scripts/check-prereqs.mjs [--quiet] [--deps-only]
 */
import fs from 'fs';
import path from 'path';
import { SKILL_ROOT, SETUP_STATUS_PATH } from './lib/paths.mjs';

const quiet = process.argv.includes('--quiet');
const depsOnly = process.argv.includes('--deps-only');
const log = (...args) => {
  if (!quiet) console.error(...args);
};

const REQUIRED_ENV = ['DB_USER', 'DB_PASSWORD', 'DB_CONNECT_STRING'];

function loadDotenv() {
  const envPath = path.join(SKILL_ROOT, '.env');
  if (!fs.existsSync(envPath)) return;
  for (const line of fs.readFileSync(envPath, 'utf8').split(/\r?\n/)) {
    const m = line.match(/^([A-Z_]+)=(.*)$/);
    if (!m || process.env[m[1]] !== undefined) continue;
    process.env[m[1]] = m[2];
  }
}

function checkSetupFreshness() {
  if (!fs.existsSync(SETUP_STATUS_PATH)) {
    return { ok: false, reason: 'missing', message: 'Run: npm run setup' };
  }
  let status;
  try {
    status = JSON.parse(fs.readFileSync(SETUP_STATUS_PATH, 'utf8'));
  } catch {
    return { ok: false, reason: 'invalid', message: 'Run: npm run setup' };
  }
  const maxAgeDays = Number(process.env.SETUP_MAX_AGE_DAYS || 7);
  const completedAt = new Date(status.completedAt);
  if (Number.isNaN(completedAt.getTime())) {
    return { ok: false, reason: 'invalid', message: 'Run: npm run setup' };
  }
  const ageMs = Date.now() - completedAt.getTime();
  const maxMs = maxAgeDays * 24 * 60 * 60 * 1000;
  if (ageMs > maxMs) {
    return {
      ok: false,
      reason: 'stale',
      message: `Setup is older than ${maxAgeDays} days. Run: npm run setup`,
      status,
    };
  }
  return { ok: true, status };
}

loadDotenv();

const nodeMajor = Number(process.versions.node.split('.')[0]);
if (nodeMajor < 18) {
  log(`simpleerp-db: Node ${process.versions.node} detected; Node 18+ is required.`);
  process.exit(1);
}

const oracledbDir = path.join(SKILL_ROOT, 'node_modules', 'oracledb');
if (!fs.existsSync(oracledbDir)) {
  log('simpleerp-db: dependencies missing. Run from the skill root:');
  log(`  cd "${SKILL_ROOT}"`);
  log('  npm install');
  process.exit(1);
}

const envPath = path.join(SKILL_ROOT, '.env');
if (!fs.existsSync(envPath)) {
  log('simpleerp-db: .env not found. Copy .env.example → .env and set DB_USER, DB_PASSWORD, DB_CONNECT_STRING.');
} else {
  const missing = REQUIRED_ENV.filter((k) => !process.env[k]);
  if (missing.length) {
    log(`simpleerp-db: .env missing keys: ${missing.join(', ')}`);
  }
}

if (!depsOnly) {
  const setup = checkSetupFreshness();
  if (!setup.ok) {
    log(`simpleerp-db: setup not ready (${setup.reason}). ${setup.message}`);
    process.exit(1);
  } else if (!quiet && setup.status) {
    log(`  setup: ${setup.status.tableCount ?? '?'} tables, schema ${setup.status.schema ?? '?'}`);
  }
}

if (!quiet) {
  log(`simpleerp-db: OK (Node ${process.versions.node}, oracledb installed)`);
}
