#!/usr/bin/env node
// migrate-lance-to-sqlite.mjs — Copy all chunks + vectors from LanceDB to sqlite-vec.
// Reads vectors directly from LanceDB (no re-embedding needed).
// Deduplicates by SHA-256 hash of text content.
//
// Usage:
//   node scripts/migrate-lance-to-sqlite.mjs [--dry-run] [--batch-size N]
//
// Data dir: ~/.openclaw/memory-crystal/

import * as lancedb from '@lancedb/lancedb';
import Database from 'better-sqlite3';
import * as sqliteVec from 'sqlite-vec';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { homedir } from 'node:os';

const BATCH_SIZE = 500;

async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const batchSizeArg = args.find((_, i) => args[i - 1] === '--batch-size');
  const batchSize = batchSizeArg ? parseInt(batchSizeArg) : BATCH_SIZE;

  const openclawHome = process.env.OPENCLAW_HOME || join(process.env.HOME || homedir(), '.openclaw');
  const dataDir = join(openclawHome, 'memory-crystal');
  const lanceDir = join(dataDir, 'lance');
  const sqlitePath = join(dataDir, 'crystal.db');

  if (!existsSync(lanceDir)) {
    console.error(`LanceDB directory not found: ${lanceDir}`);
    process.exit(1);
  }

  // Open LanceDB
  const lanceDb = await lancedb.connect(lanceDir);
  const tableNames = await lanceDb.tableNames();
  if (!tableNames.includes('chunks')) {
    console.error('No "chunks" table in LanceDB');
    process.exit(1);
  }
  const lanceTable = await lanceDb.openTable('chunks');
  const totalLance = await lanceTable.countRows();
  console.log(`LanceDB chunks: ${totalLance.toLocaleString()}`);

  // Open SQLite + load sqlite-vec
  const db = new Database(sqlitePath);
  db.pragma('journal_mode = WAL');
  sqliteVec.load(db);

  // Ensure tables exist
  db.exec(`
    CREATE TABLE IF NOT EXISTS chunks (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      text TEXT NOT NULL,
      text_hash TEXT NOT NULL,
      role TEXT,
      source_type TEXT,
      source_id TEXT,
      agent_id TEXT,
      token_count INTEGER,
      created_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_chunks_agent ON chunks(agent_id);
    CREATE INDEX IF NOT EXISTS idx_chunks_source ON chunks(source_type);
    CREATE INDEX IF NOT EXISTS idx_chunks_hash ON chunks(text_hash);
    CREATE INDEX IF NOT EXISTS idx_chunks_created ON chunks(created_at);

    CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
      text,
      tokenize='porter unicode61'
    );

    CREATE TRIGGER IF NOT EXISTS chunks_fts_insert AFTER INSERT ON chunks
    BEGIN
      INSERT INTO chunks_fts(rowid, text) VALUES (NEW.id, NEW.text);
    END;
  `);

  const existingSqlite = (db.prepare('SELECT COUNT(*) as count FROM chunks').get()).count;
  console.log(`SQLite chunks (before): ${existingSqlite.toLocaleString()}`);

  if (dryRun) {
    // Sample some rows
    const sample = await lanceTable.query().limit(3).toArray();
    console.log('\nSample (3 rows):');
    for (const row of sample) {
      console.log(`  [${row.source_type}] [${row.agent_id}] ${row.text?.slice(0, 80)}...`);
      console.log(`    vector: ${row.vector?.length} dims, created: ${row.created_at}`);
    }
    console.log(`\nWould migrate ${totalLance.toLocaleString()} chunks.`);
    console.log(`Estimated crystal.db growth: ~${Math.round(totalLance * 1536 * 4 / 1024 / 1024)}MB vectors + text`);
    db.close();
    return;
  }

  // Detect dimensions from first row
  const [firstRow] = await lanceTable.query().limit(1).toArray();
  const dimensions = firstRow.vector?.length;
  if (!dimensions) {
    console.error('Could not determine vector dimensions from LanceDB');
    process.exit(1);
  }
  console.log(`Vector dimensions: ${dimensions}`);

  // Create vec table if needed
  const vecExists = db.prepare(`SELECT name FROM sqlite_master WHERE type='table' AND name='chunks_vec'`).get();
  if (!vecExists) {
    db.exec(`CREATE VIRTUAL TABLE chunks_vec USING vec0(
      chunk_id INTEGER PRIMARY KEY,
      embedding float[${dimensions}] distance_metric=cosine
    )`);
    console.log(`Created chunks_vec table (${dimensions} dims)`);
  }

  // Build hash set of existing chunks for dedup
  console.log('Building dedup hash set...');
  const existingHashes = new Set();
  const hashRows = db.prepare('SELECT text_hash FROM chunks').all();
  for (const row of hashRows) {
    existingHashes.add(row.text_hash);
  }
  console.log(`Existing unique hashes: ${existingHashes.size.toLocaleString()}`);

  // Prepare insert statements
  const insertChunk = db.prepare(`
    INSERT INTO chunks (text, text_hash, role, source_type, source_id, agent_id, token_count, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  `);
  const insertVec = db.prepare(`
    INSERT INTO chunks_vec (chunk_id, embedding) VALUES (?, ?)
  `);

  // Read all rows from LanceDB in batches using offset/limit
  let migrated = 0;
  let skippedDedup = 0;
  let offset = 0;
  const startTime = Date.now();

  while (offset < totalLance) {
    const rows = await lanceTable.query().limit(batchSize).offset(offset).toArray();
    if (rows.length === 0) break;

    const transaction = db.transaction(() => {
      for (const row of rows) {
        const text = row.text || '';
        const hash = createHash('sha256').update(text).digest('hex');

        if (existingHashes.has(hash)) {
          skippedDedup++;
          continue;
        }
        existingHashes.add(hash);

        const result = insertChunk.run(
          text,
          hash,
          row.role || null,
          row.source_type || null,
          row.source_id || null,
          row.agent_id || null,
          row.token_count || Math.ceil(text.length / 4),
          row.created_at || new Date().toISOString()
        );

        // sqlite-vec needs BigInt for integer primary keys
        const chunkId = typeof result.lastInsertRowid === 'bigint'
          ? result.lastInsertRowid
          : BigInt(result.lastInsertRowid);

        // Convert vector to Float32Array
        const vector = row.vector;
        const f32 = vector instanceof Float32Array ? vector : new Float32Array(Array.from(vector));
        insertVec.run(chunkId, f32);

        migrated++;
      }
    });
    transaction();

    offset += rows.length;
    const elapsed = (Date.now() - startTime) / 1000;
    const rate = Math.round(offset / elapsed);
    const eta = Math.round((totalLance - offset) / rate);
    process.stdout.write(
      `\r  ${offset.toLocaleString()}/${totalLance.toLocaleString()} (${Math.round(offset / totalLance * 100)}%) ` +
      `| migrated: ${migrated.toLocaleString()} | dedup: ${skippedDedup.toLocaleString()} ` +
      `| ${rate}/s | ETA: ${eta}s   `
    );
  }

  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
  console.log(`\n\nMigration complete in ${elapsed}s:`);
  console.log(`  Migrated:    ${migrated.toLocaleString()}`);
  console.log(`  Dedup skip:  ${skippedDedup.toLocaleString()}`);

  // Verify
  const finalCount = (db.prepare('SELECT COUNT(*) as count FROM chunks').get()).count;
  const ftsCount = (db.prepare('SELECT COUNT(*) as count FROM chunks_fts').get()).count;
  console.log(`  SQLite chunks: ${finalCount.toLocaleString()}`);
  console.log(`  FTS entries:   ${ftsCount.toLocaleString()}`);
  console.log(`  LanceDB:       ${totalLance.toLocaleString()}`);

  if (finalCount === ftsCount) {
    console.log('  FTS sync: OK');
  } else {
    console.warn(`  WARNING: FTS count mismatch (${ftsCount} vs ${finalCount})`);
  }

  db.close();
}

main().catch(err => {
  console.error(`Migration failed: ${err.message}`);
  process.exit(1);
});
