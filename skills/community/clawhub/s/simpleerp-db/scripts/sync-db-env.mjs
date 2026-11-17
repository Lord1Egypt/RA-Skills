/**
 * Write or update DB_* lines in workspace .env from CLI flags or process.env.
 * Cross-platform alternative to shell-specific $env: / export syntax.
 *
 * Usage:
 *   node scripts/sync-db-env.mjs --db-user=U --db-password=P --db-connect-string=host:1521/SVC
 *   DB_USER=U DB_PASSWORD=P DB_CONNECT_STRING=... node scripts/sync-db-env.mjs
 *
 * Never prints secret values.
 */
import fs from 'fs';
import path from 'path';
import { SKILL_ROOT } from './lib/paths.mjs';

const ENV_PATH = path.join(SKILL_ROOT, '.env');

const FLAG_MAP = {
  '--db-user': 'DB_USER',
  '--db-password': 'DB_PASSWORD',
  '--db-connect-string': 'DB_CONNECT_STRING',
};

function parseArgs(argv) {
  const values = {};
  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    for (const [flag, key] of Object.entries(FLAG_MAP)) {
      if (arg === flag) {
        values[key] = argv[++i];
        continue;
      }
      if (arg.startsWith(`${flag}=`)) {
        values[key] = arg.slice(flag.length + 1);
      }
    }
  }
  for (const key of Object.values(FLAG_MAP)) {
    if (!values[key] && process.env[key]) values[key] = process.env[key];
  }
  return values;
}

function upsertEnvFile(updates) {
  let lines = [];
  if (fs.existsSync(ENV_PATH)) {
    lines = fs.readFileSync(ENV_PATH, 'utf8').split(/\r?\n/);
  }

  const seen = new Set();
  const out = lines.map((line) => {
    const m = line.match(/^([A-Z_]+)=/);
    if (m && updates[m[1]] !== undefined) {
      seen.add(m[1]);
      return `${m[1]}=${updates[m[1]]}`;
    }
    return line;
  });

  for (const key of Object.values(FLAG_MAP)) {
    if (updates[key] !== undefined && !seen.has(key)) {
      out.push(`${key}=${updates[key]}`);
    }
  }

  while (out.length > 0 && out[out.length - 1] === '') out.pop();
  fs.writeFileSync(ENV_PATH, `${out.join('\n')}\n`, 'utf8');
}

const updates = parseArgs(process.argv);
const missing = Object.values(FLAG_MAP).filter((k) => !updates[k]);
if (missing.length) {
  console.error(
    `sync-db-env.mjs: missing ${missing.join(', ')}. Pass --db-user, --db-password, --db-connect-string or set env vars.`
  );
  process.exit(1);
}

upsertEnvFile(updates);
console.error(`Wrote ${ENV_PATH} (DB_USER, DB_PASSWORD, DB_CONNECT_STRING updated; values not shown).`);
