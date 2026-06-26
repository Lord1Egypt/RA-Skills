/**
 * storage-schema.js — v4.0 Database Schema Definitions
 * 
 * Complete SQLite schema for Unified Memory v4.0
 * All tables use WAL mode for concurrent reads + durability.
 * 
 * Tables:
 *   - memories       Primary memory storage
 *   - evidence      Evidence chain store (B-tree indexed)
 *   - revisions     Version history (B-tree indexed)
 *   - scopes        Persistent scope registry
 *   - wal_entries    Write-Ahead Log
 *   - rate_limits   Distributed sliding-window rate limits
 *   - bm25_index    Persistent BM25 posting lists
 *   - vector_meta   LanceDB vector metadata + dirty tracking
 */

import Database from 'better-sqlite3';
import { existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import os from 'os';

const SCHEMA_VERSION = 4;

let _db = null;

/**
 * Get the v4.0 database handle (lazy singleton)
 */
export function getV4Db() {
  if (_db) return _db;

  const dir = join(os.homedir(), '.unified-memory', 'v4');
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }

  const dbPath = join(dir, 'memories.db');
  _db = new Database(dbPath);

  // WAL mode: concurrent reads, durable writes, no lock contention
  _db.pragma('journal_mode = WAL');
  _db.pragma('synchronous = NORMAL');
  _db.pragma('foreign_keys = ON');
  _db.pragma('busy_timeout = 5000');

  initSchema(_db);

  return _db;
}

/**
 * Initialize all v4.0 tables and indexes
 */
function initSchema(db) {
  // ── memories ──────────────────────────────────────────────
  db.exec(`
    CREATE TABLE IF NOT EXISTS memories (
      id              TEXT PRIMARY KEY,
      text            TEXT NOT NULL,
      category        TEXT    DEFAULT 'general',
      tags            TEXT    DEFAULT '[]',        -- JSON array
      importance      REAL    DEFAULT 0.5,
      scope_type      TEXT    NOT NULL DEFAULT 'USER',  -- USER|TEAM|AGENT|GLOBAL
      scope_id        TEXT,                           -- team_id or agent_id
      tier            TEXT    DEFAULT 'HOT',           -- HOT|WARM|COLD
      pinned          INTEGER DEFAULT 0,
      pinned_at       INTEGER,
      pinned_reason   TEXT,
      created_at      INTEGER NOT NULL,
      updated_at      INTEGER NOT NULL,
      accessed_at     INTEGER NOT NULL,
      version         INTEGER DEFAULT 1,               -- Optimistic lock
      deleted         INTEGER DEFAULT 0,               -- Soft delete
      metadata        TEXT    DEFAULT '{}'            -- JSON extensibility
    );

    CREATE INDEX IF NOT EXISTS idx_mem_scope
      ON memories(scope_type, scope_id);
    CREATE INDEX IF NOT EXISTS idx_mem_category
      ON memories(category);
    CREATE INDEX IF NOT EXISTS idx_mem_tier
      ON memories(tier);
    CREATE INDEX IF NOT EXISTS idx_mem_updated
      ON memories(updated_at DESC);
    CREATE INDEX IF NOT EXISTS idx_mem_deleted
      ON memories(deleted) WHERE deleted=0;
    CREATE INDEX IF NOT EXISTS idx_mem_importance
      ON memories(importance DESC) WHERE deleted=0;
  `);

  // ── evidence ──────────────────────────────────────────────
  db.exec(`
    CREATE TABLE IF NOT EXISTS evidence (
      id          TEXT PRIMARY KEY,
      memory_id   TEXT NOT NULL,
      type        TEXT NOT NULL,              -- transcript|interaction|fact|manual
      source_id   TEXT,
      context     TEXT,
      confidence  REAL    DEFAULT 1.0,
      timestamp   INTEGER NOT NULL,
      created_at  INTEGER NOT NULL,
      FOREIGN KEY (memory_id) REFERENCES memories(id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_ev_memory
      ON evidence(memory_id, timestamp DESC);
    CREATE INDEX IF NOT EXISTS idx_ev_type
      ON evidence(type, timestamp DESC);
    CREATE INDEX IF NOT EXISTS idx_ev_source
      ON evidence(source_id) WHERE source_id IS NOT NULL;
  `);

  // ── revisions ─────────────────────────────────────────────
  db.exec(`
    CREATE TABLE IF NOT EXISTS revisions (
      id             TEXT PRIMARY KEY,
      memory_id      TEXT NOT NULL,
      content        TEXT NOT NULL,
      change_type    TEXT NOT NULL,           -- create|update|delete
      version_num    INTEGER NOT NULL,
      diff_from_prev TEXT,
      agent_id       TEXT,
      created_at     INTEGER NOT NULL,
      FOREIGN KEY (memory_id) REFERENCES memories(id) ON DELETE CASCADE
    );

    CREATE UNIQUE INDEX IF NOT EXISTS idx_rev_memory_version
      ON revisions(memory_id, version_num DESC);
    CREATE INDEX IF NOT EXISTS idx_rev_created
      ON revisions(created_at DESC);
  `);

  // ── scopes ─────────────────────────────────────────────────
  db.exec(`
    CREATE TABLE IF NOT EXISTS scopes (
      scope_id    TEXT PRIMARY KEY,          -- 'user:ou_xxx' | 'team:xxx' | 'agent:xxx'
      scope_type  TEXT NOT NULL,
      name        TEXT,
      parent_id   TEXT,
      config      TEXT    DEFAULT '{}',       -- JSON: rate_limits, ttl, tier_policy
      created_at  INTEGER NOT NULL,
      updated_at  INTEGER NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_scope_type
      ON scopes(scope_type);
    CREATE INDEX IF NOT EXISTS idx_scope_parent
      ON scopes(parent_id) WHERE parent_id IS NOT NULL;
  `);

  // ── wal_entries ────────────────────────────────────────────
  db.exec(`
    CREATE TABLE IF NOT EXISTS wal_entries (
      lsn          TEXT PRIMARY KEY,         -- '<timestamp>_<sequence>'
      operation    TEXT NOT NULL,            -- INSERT|UPDATE|DELETE
      table_name   TEXT NOT NULL,
      record_id    TEXT NOT NULL,
      payload      TEXT NOT NULL,            -- JSON before/after image
      checksum     TEXT NOT NULL,           -- SHA-256 of payload
      agent_id     TEXT,
      team_space   TEXT,
      status       TEXT DEFAULT 'PENDING',  -- PENDING|COMMITTED|ROLLED_BACK
      created_at   INTEGER NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_wal_lsn
      ON wal_entries(created_at ASC);
    CREATE INDEX IF NOT EXISTS idx_wal_status
      ON wal_entries(status) WHERE status != 'COMMITTED';
  `);

  // ── rate_limits ────────────────────────────────────────────
  db.exec(`
    CREATE TABLE IF NOT EXISTS rate_limits (
      key          TEXT NOT NULL,            -- '<scope_type>:<scope_id>:<op>:<window>'
      window_start INTEGER NOT NULL,         -- Unix second (aligned)
      count        INTEGER NOT NULL DEFAULT 0,
      ttl_seconds  INTEGER DEFAULT 120,
      PRIMARY KEY (key, window_start)
    );

    CREATE INDEX IF NOT EXISTS idx_rl_window
      ON rate_limits(window_start ASC);
  `);

  // ── bm25_index ─────────────────────────────────────────────
  db.exec(`
    CREATE TABLE IF NOT EXISTS bm25_index (
      term       TEXT NOT NULL,
      memory_id  TEXT NOT NULL,
      frequency  INTEGER NOT NULL,           -- TF (term frequency in doc)
      positions  TEXT NOT NULL,              -- JSON array of token positions
      doc_count  INTEGER NOT NULL,          -- IDF: number of docs containing term
      PRIMARY KEY (term, memory_id)
    );

    CREATE INDEX IF NOT EXISTS idx_bm25_term_freq
      ON bm25_index(term, frequency DESC);
    CREATE INDEX IF NOT EXISTS idx_bm25_memory
      ON bm25_index(memory_id);
  `);

  // ── vector_meta ───────────────────────────────────────────
  db.exec(`
    CREATE TABLE IF NOT EXISTS vector_meta (
      memory_id      TEXT PRIMARY KEY,
      vector_id      TEXT NOT NULL,
      vector_version INTEGER NOT NULL DEFAULT 0,
      embedding_model TEXT NOT NULL,
      dimensions     INTEGER NOT NULL,
      dirty          INTEGER DEFAULT 0,     -- 0=clean, 1=needs_reindex
      last_indexed   INTEGER,
      FOREIGN KEY (memory_id) REFERENCES memories(id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_vm_dirty
      ON vector_meta(dirty) WHERE dirty=1;
  `);

  // ── meta (key-value store) ────────────────────────────────
  db.exec(`
    CREATE TABLE IF NOT EXISTS meta (
      key   TEXT PRIMARY KEY,
      value TEXT
    );
  `);
}

/**
 * Check if v4.0 schema is initialized
 */
export function isV4Initialized() {
  try {
    const db = getV4Db();
    const row = db.prepare("SELECT value FROM meta WHERE key='schema_version'").get();
    return row?.value === String(SCHEMA_VERSION);
  } catch {
    return false;
  }
}

/**
 * Mark v4.0 schema as initialized
 */
export function markV4Initialized() {
  const db = getV4Db();
  db.prepare("INSERT OR REPLACE INTO meta (key, value) VALUES ('schema_version', ?)").run(String(SCHEMA_VERSION));
}

/**
 * Close the database handle
 */
export function closeV4Db() {
  if (_db) {
    _db.close();
    _db = null;
  }
}

export default {
  getV4Db,
  isV4Initialized,
  markV4Initialized,
  closeV4Db,
  SCHEMA_VERSION,
};
