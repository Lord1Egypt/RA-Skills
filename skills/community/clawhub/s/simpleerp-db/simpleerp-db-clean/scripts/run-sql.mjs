/**
 * Run one read-only Oracle query using this skill’s npm dependencies (oracledb, dotenv).
 * Only SELECT / WITH / EXPLAIN PLAN — no DML or DDL (this skill is query-only).
 *
 * Credentials (any OS): workspace .env and/or --db-user / --db-password / --db-connect-string
 * Output file: -o path, --out=path, --output=path, or env SQL_OUTPUT
 *
 * Usage:
 *   npm install
 *   npm run sql -- "SELECT 1 FROM DUAL"
 *   npm run sql -- -o output/last-query.json "SELECT COUNT(*) AS c FROM PRODUCT"
 *   npm run sql -- --db-user=U --db-password=P --db-connect-string=host:1521/SVC "SELECT ..."
 *   echo "SELECT ..." | npm run sql --
 */
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import readline from 'readline';
import { SKILL_ROOT, resolveFromSkillRoot, ensureDirForFile } from './lib/paths.mjs';

const DB_FLAGS = {
  '--db-user': 'DB_USER',
  '--db-password': 'DB_PASSWORD',
  '--db-connect-string': 'DB_CONNECT_STRING',
};

function parseArgs(argv) {
  const sqlParts = [];
  let outPath = process.env.SQL_OUTPUT?.trim() || null;
  const dbOverrides = {};

  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];

    if (arg === '-o' || arg === '--out' || arg === '--output') {
      outPath = argv[++i];
      continue;
    }
    if (arg.startsWith('--out=')) {
      outPath = arg.slice('--out='.length);
      continue;
    }
    if (arg.startsWith('--output=')) {
      outPath = arg.slice('--output='.length);
      continue;
    }

    let matchedFlag = false;
    for (const [flag, envKey] of Object.entries(DB_FLAGS)) {
      if (arg === flag) {
        dbOverrides[envKey] = argv[++i];
        matchedFlag = true;
        break;
      }
      if (arg.startsWith(`${flag}=`)) {
        dbOverrides[envKey] = arg.slice(flag.length + 1);
        matchedFlag = true;
        break;
      }
    }
    if (matchedFlag) continue;

    sqlParts.push(arg);
  }

  return { sql: sqlParts.join(' ').trim(), outPath, dbOverrides };
}

function checkNodeVersion() {
  const major = Number(process.versions.node.split('.')[0]);
  if (major < 18) {
    console.error(
      `run-sql.mjs: Node ${process.versions.node} is too old; Node 18+ is required (see package.json engines).`
    );
    process.exit(1);
  }
}

function missingDepsHelp() {
  return [
    '',
    'run-sql.mjs: oracledb (and dotenv) are not installed in this skill folder.',
    '',
    `  Skill directory: ${SKILL_ROOT}`,
    '',
    '  Run once (Windows, macOS, or Linux):',
    `    cd "${SKILL_ROOT}"`,
    '    npm install',
    '',
    '  Requires Node 18+; Oracle Instant Client only if oracledb thin mode cannot reach your DB.',
    '',
  ].join('\n');
}

function loadSkillModulesSync() {
  const pkgJson = path.join(SKILL_ROOT, 'package.json');
  if (!fs.existsSync(pkgJson)) {
    throw new Error(missingDepsHelp());
  }
  const oracledbDir = path.join(SKILL_ROOT, 'node_modules', 'oracledb');
  if (!fs.existsSync(oracledbDir)) {
    throw new Error(missingDepsHelp());
  }

  const require = createRequire(pkgJson);
  const dotenv = require('dotenv');
  let oracledb;
  try {
    oracledb = require('oracledb');
  } catch (e) {
    if (e && (e.code === 'MODULE_NOT_FOUND' || /Cannot find module/.test(String(e.message)))) {
      throw new Error(missingDepsHelp());
    }
    throw e;
  }

  const skillEnv = path.join(SKILL_ROOT, '.env');
  if (fs.existsSync(skillEnv)) {
    dotenv.config({ path: skillEnv });
  }
  return { oracledb };
}

function applyDbOverrides(dbOverrides) {
  for (const [key, value] of Object.entries(dbOverrides)) {
    if (value !== undefined && value !== '') process.env[key] = value;
  }
}

function stripSqlComments(sql) {
  return sql.replace(/^\s*--.*$/gm, '').trim();
}

/** This skill allows only read-only queries (SELECT / WITH / EXPLAIN PLAN). */
function isQueryOnlySql(sql) {
  const s = stripSqlComments(sql);
  if (!s) return false;
  const upper = s.toUpperCase();
  if (upper.startsWith('EXPLAIN PLAN')) return true;
  const head = upper.split(/\s+/)[0];
  return head === 'SELECT' || head === 'WITH';
}

function queryOnlyRejectionMessage() {
  return [
    '',
    'run-sql.mjs: this skill allows queries only (SELECT, WITH … SELECT, or EXPLAIN PLAN FOR …).',
    '  INSERT, UPDATE, DELETE, MERGE, DDL, and PL/SQL blocks are not supported here.',
    '  Use SQLcl, SQL*Plus, or another DBA tool for changes.',
    '',
  ].join('\n');
}

async function readStdin() {
  if (process.stdin.isTTY) return '';
  return new Promise((resolve, reject) => {
    let data = '';
    const rl = readline.createInterface({ input: process.stdin });
    rl.on('line', (line) => {
      data += line + '\n';
    });
    rl.on('close', () => resolve(data.trim()));
    rl.on('error', reject);
  });
}

function writeOutputFile(outPath, body) {
  const resolved = resolveFromSkillRoot(outPath);
  ensureDirForFile(resolved);
  fs.writeFileSync(resolved, body, 'utf8');
  console.error(`Wrote ${resolved}`);
}

async function main() {
  checkNodeVersion();
  const { sql: sqlFromArgv, outPath, dbOverrides } = parseArgs(process.argv);
  const { oracledb } = loadSkillModulesSync();
  applyDbOverrides(dbOverrides);

  let sql = sqlFromArgv;
  if (!sql) sql = await readStdin();
  if (!sql) {
    console.error('Usage: npm run sql -- [options] "<SELECT ...>"');
    console.error('Options: -o <file>  --db-user=  --db-password=  --db-connect-string=');
    console.error('   or: echo "SELECT ..." | npm run sql --');
    console.error('Env: SQL_OUTPUT=<file>  DB_* in .env or environment');
    process.exit(1);
  }

  if (!isQueryOnlySql(sql)) {
    console.error(queryOnlyRejectionMessage());
    process.exit(1);
  }

  const user = process.env.DB_USER;
  const password = process.env.DB_PASSWORD;
  const connectString = process.env.DB_CONNECT_STRING;
  if (!user || !password || !connectString) {
    console.error(
      'Missing DB_USER, DB_PASSWORD, or DB_CONNECT_STRING.',
      'Use workspace .env, shell env vars, or --db-user / --db-password / --db-connect-string on npm run sql.'
    );
    process.exit(1);
  }

  let conn;
  try {
    conn = await oracledb.getConnection({ user, password, connectString });
    const options = {
      outFormat: oracledb.OUT_FORMAT_OBJECT,
    };
    const result = await conn.execute(sql, {}, options);
    if (result.rows) {
      const body = JSON.stringify(result.rows, null, 2);
      console.log(body);
      if (result.rows.length === 0) console.error('(0 rows)');
      if (outPath) writeOutputFile(outPath, body);
    } else {
      const body = JSON.stringify({ rowsAffected: result.rowsAffected ?? null }, null, 2);
      console.log(body);
      if (outPath) writeOutputFile(outPath, body);
    }
  } finally {
    if (conn) await conn.close();
  }
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
