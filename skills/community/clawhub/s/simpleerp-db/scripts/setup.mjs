/**
 * Bootstrap the simpleerp-db skill: install deps, export live DDL, regen references, smoke test.
 * Usage: node scripts/setup.mjs [--skip-export] [--quiet]
 */
import { spawnSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { SKILL_ROOT, LOCAL_TABLES_SQL, SETUP_STATUS_PATH, ensureDirForFile } from './lib/paths.mjs';

const quiet = process.argv.includes('--quiet');
const skipExport = process.argv.includes('--skip-export');
const log = (...args) => {
  if (!quiet) console.error(...args);
};

const REQUIRED_ENV = ['DB_USER', 'DB_PASSWORD', 'DB_CONNECT_STRING'];

function loadDotenv() {
  const envPath = path.join(SKILL_ROOT, '.env');
  if (!fs.existsSync(envPath)) return false;
  for (const line of fs.readFileSync(envPath, 'utf8').split(/\r?\n/)) {
    const m = line.match(/^([A-Z_]+)=(.*)$/);
    if (!m) continue;
    if (process.env[m[1]] === undefined) process.env[m[1]] = m[2];
  }
  return true;
}

function runNode(script, args = []) {
  const result = spawnSync(process.execPath, [path.join(SKILL_ROOT, 'scripts', script), ...args], {
    cwd: SKILL_ROOT,
    stdio: quiet ? 'pipe' : 'inherit',
    env: process.env,
  });
  if (result.status !== 0) {
    if (quiet && result.stderr) process.stderr.write(result.stderr);
    process.exit(result.status ?? 1);
  }
  return result;
}

function runNpmInstall() {
  log('setup: npm install');
  const result = spawnSync('npm', ['install'], {
    cwd: SKILL_ROOT,
    stdio: quiet ? 'pipe' : 'inherit',
    env: process.env,
    shell: true,
  });
  if (result.status !== 0) {
    if (quiet && result.stderr) process.stderr.write(result.stderr);
    process.exit(result.status ?? 1);
  }
}

function verifyCredentials() {
  const envPath = path.join(SKILL_ROOT, '.env');
  if (!fs.existsSync(envPath)) {
    console.error('setup: .env not found. Copy .env.example → .env and set DB_USER, DB_PASSWORD, DB_CONNECT_STRING.');
    process.exit(1);
  }
  const missing = REQUIRED_ENV.filter((k) => !process.env[k]);
  if (missing.length) {
    console.error(`setup: missing env keys: ${missing.join(', ')}`);
    process.exit(1);
  }
}

function writeSetupStatus(schema, tableCount) {
  const status = {
    completedAt: new Date().toISOString(),
    schema,
    tableCount,
    tablesSql: LOCAL_TABLES_SQL,
  };
  ensureDirForFile(SETUP_STATUS_PATH);
  fs.writeFileSync(SETUP_STATUS_PATH, `${JSON.stringify(status, null, 2)}\n`, 'utf8');
  log(`setup: wrote ${SETUP_STATUS_PATH}`);
}

function countTablesInSql(filePath) {
  if (!fs.existsSync(filePath)) return 0;
  const content = fs.readFileSync(filePath, 'utf8');
  return (content.match(/^\s*--\s+DDL for Table /gm) || []).length;
}

async function main() {
  log('setup: starting simpleerp-db bootstrap');
  runNpmInstall();
  loadDotenv();
  verifyCredentials();

  runNode('check-prereqs.mjs', ['--deps-only', '--quiet']);

  if (!skipExport) {
    log('setup: exporting live DDL');
    runNode('export-tables-sql.mjs');
  } else if (!fs.existsSync(LOCAL_TABLES_SQL)) {
    console.error('setup: --skip-export but schema/TABLES.sql does not exist.');
    process.exit(1);
  }

  log('setup: regenerating references');
  runNode('gen-table-index.mjs', ['--tables-sql', LOCAL_TABLES_SQL]);

  log('setup: smoke test');
  runNode('run-sql.mjs', ['SELECT 1 AS x FROM DUAL']);

  const schema = (process.env.DB_SCHEMA || process.env.DB_USER || 'SIMPLEERP').toUpperCase();
  const tableCount = countTablesInSql(LOCAL_TABLES_SQL);
  writeSetupStatus(schema, tableCount);
  log('setup: complete');
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
