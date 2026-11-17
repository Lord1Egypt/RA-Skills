/**
 * Export live Oracle table DDL to schema/TABLES.sql using DBMS_METADATA.
 * Format matches gen-table-index.mjs parser (--  DDL for Table NAME).
 *
 * Usage: node scripts/export-tables-sql.mjs [--schema SIMPLEERP] [--out path]
 */
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { SKILL_ROOT, LOCAL_TABLES_SQL, ensureDirForFile } from './lib/paths.mjs';

function parseArgs(argv) {
  let schema = process.env.DB_SCHEMA?.trim() || null;
  let outPath = LOCAL_TABLES_SQL;
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === '--schema' && argv[i + 1]) {
      schema = argv[++i];
    } else if (argv[i] === '--out' && argv[i + 1]) {
      outPath = path.resolve(argv[++i]);
    }
  }
  return { schema, outPath };
}

function loadModules() {
  const pkgJson = path.join(SKILL_ROOT, 'package.json');
  const require = createRequire(pkgJson);
  const dotenv = require('dotenv');
  const oracledb = require('oracledb');
  const skillEnv = path.join(SKILL_ROOT, '.env');
  if (fs.existsSync(skillEnv)) dotenv.config({ path: skillEnv });
  return { oracledb };
}

async function configureMetadata(conn) {
  const transforms = [
    "DBMS_METADATA.SET_TRANSFORM_PARAM(DBMS_METADATA.SESSION_TRANSFORM,'STORAGE',FALSE)",
    "DBMS_METADATA.SET_TRANSFORM_PARAM(DBMS_METADATA.SESSION_TRANSFORM,'TABLESPACE',FALSE)",
    "DBMS_METADATA.SET_TRANSFORM_PARAM(DBMS_METADATA.SESSION_TRANSFORM,'SEGMENT_ATTRIBUTES',FALSE)",
    "DBMS_METADATA.SET_TRANSFORM_PARAM(DBMS_METADATA.SESSION_TRANSFORM,'SQLTERMINATOR',TRUE)",
  ];
  for (const stmt of transforms) {
    await conn.execute(`BEGIN ${stmt}; END;`);
  }
}

async function readClob(value) {
  if (value === null || value === undefined) return '';
  if (typeof value === 'string') return value;
  if (typeof value.getData === 'function') {
    const data = await value.getData();
    return data == null ? '' : String(data);
  }
  return String(value);
}

async function listTables(conn, oracledb, schema) {
  const result = await conn.execute(
    `SELECT table_name FROM all_tables WHERE owner = :owner ORDER BY table_name`,
    { owner: schema },
    { outFormat: oracledb.OUT_FORMAT_OBJECT }
  );
  return (result.rows || []).map((r) => r.TABLE_NAME);
}

async function getTableDdl(conn, oracledb, schema, tableName) {
  const result = await conn.execute(
    `SELECT DBMS_METADATA.GET_DDL('TABLE', :tableName, :owner) AS ddl FROM DUAL`,
    { tableName, owner: schema },
    {
      outFormat: oracledb.OUT_FORMAT_OBJECT,
      fetchInfo: { DDL: { type: oracledb.STRING } },
    }
  );
  const row = result.rows?.[0];
  if (!row) return '';
  const ddl = await readClob(row.DDL ?? row.ddl);
  return ddl.trim();
}

function formatTableBlock(tableName, ddl) {
  const lines = [
    '--------------------------------------------------------',
    `--  DDL for Table ${tableName}`,
    '--------------------------------------------------------',
    '',
    ddl,
    '',
  ];
  return lines.join('\n');
}

async function main() {
  const { schema: schemaArg, outPath } = parseArgs(process.argv);
  const { oracledb } = loadModules();

  const user = process.env.DB_USER;
  const password = process.env.DB_PASSWORD;
  const connectString = process.env.DB_CONNECT_STRING;
  if (!user || !password || !connectString) {
    console.error('export-tables-sql.mjs: missing DB_USER, DB_PASSWORD, or DB_CONNECT_STRING.');
    process.exit(1);
  }

  const schema = (schemaArg || process.env.DB_SCHEMA || user).toUpperCase();

  let conn;
  try {
    conn = await oracledb.getConnection({ user, password, connectString });
    await configureMetadata(conn);

    const tables = await listTables(conn, oracledb, schema);
    if (!tables.length) {
      console.error(`export-tables-sql.mjs: no tables found for schema ${schema}.`);
      process.exit(1);
    }

    const blocks = [];
    for (const tableName of tables) {
      const ddl = await getTableDdl(conn, oracledb, schema, tableName);
      if (!ddl) continue;
      blocks.push(formatTableBlock(tableName, ddl));
    }

    ensureDirForFile(outPath);
    fs.writeFileSync(outPath, `${blocks.join('\n')}\n`, 'utf8');
    console.error(`Wrote ${outPath} (${blocks.length} tables, schema ${schema})`);
  } finally {
    if (conn) await conn.close();
  }
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
