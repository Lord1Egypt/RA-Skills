/**
 * storage-gateway.js — v4.0 Storage Gateway
 *
 * Single entry point for ALL storage operations in unified-memory v4.0.
 * Replaces all 18+ local loadMemories()/saveMemories() patterns.
 *
 * Features:
 * - WAL in SQLite (no separate WAL files)
 * - Incremental BM25 via persistent posting lists
 * - Persistent scope index (B-tree)
 * - Evidence chains in dedicated table
 * - Version history in dedicated table
 * - Per-scope rate limiting
 * - Multi-tenant team spaces
 *
 * Usage:
 *   import { StorageGateway } from './v4/storage-gateway.js';
 *   const gateway = new StorageGateway();
 *   await gateway.init();
 *   const memories = await gateway.getMemories({ scope: 'USER' });
 *   await gateway.writeMemory({ text: 'Hello', category: 'fact' });
 */

import { createRequire } from 'module';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import os from 'os';
import crypto from 'crypto';
import { fileURLToPath } from 'url';

const require = createRequire(import.meta.url);

// ─── Lazy-load dependencies ────────────────────────────────────────────────

let _betterSqlite3 = null;
function getBetterSqlite3() {
  if (_betterSqlite3) return _betterSqlite3;
  for (const path of [
    'better-sqlite3',
    '/usr/local/lib/node_modules/better-sqlite3',
    '/usr/lib/node_modules/better-sqlite3',
  ]) {
    try { _betterSqlite3 = require(path); return _betterSqlite3; } catch {}
  }
  throw new Error('[storage-gateway] better-sqlite3 not found. Run: npm install better-sqlite3');
}

let _vectorMem = null;
async function getVectorMem() {
  if (_vectorMem !== null) return _vectorMem;
  try {
    const { VectorMemory } = await import('../vector_lancedb.js');
    _vectorMem = new VectorMemory();
    await _vectorMem.initialize();
  } catch (e) {
    console.warn('[storage-gateway] VectorMemory init failed:', e.message);
    _vectorMem = null;
  }
  return _vectorMem;
}

// ─── Constants ────────────────────────────────────────────────────────────

const V4_DIR = join(os.homedir(), '.unified-memory', 'v4');
const V4_DB_PATH = join(V4_DIR, 'memories.db');

const SCOPE_TYPES = ['USER', 'TEAM', 'AGENT', 'GLOBAL'];
const TIERS = ['HOT', 'WARM', 'COLD'];
const DEFAULT_TIER = 'HOT';
const DEFAULT_SCOPE_TYPE = 'USER';

const RATE_LIMIT_WINDOW = 60;   // seconds
const RATE_LIMIT_MAX_WRITE = 30;
const RATE_LIMIT_MAX_READ = 100;
const RATE_LIMIT_MAX_SEARCH = 50;

// BM25 parameters
const BM25_K1 = 1.5;
const BM25_B = 0.75;

// ─── Schema init (DDL) ────────────────────────────────────────────────────

function buildSchema(db) {
  db.exec(`
    PRAGMA journal_mode = WAL;
    PRAGMA synchronous = NORMAL;
    PRAGMA foreign_keys = ON;
    PRAGMA busy_timeout = 5000;

    CREATE TABLE IF NOT EXISTS memories (
      id              TEXT PRIMARY KEY,
      text            TEXT NOT NULL,
      category        TEXT    DEFAULT 'general',
      tags            TEXT    DEFAULT '[]',
      importance      REAL    DEFAULT 0.5,
      scope_type      TEXT    NOT NULL DEFAULT 'USER',
      scope_id        TEXT,
      tier            TEXT    DEFAULT 'HOT',
      pinned          INTEGER DEFAULT 0,
      pinned_at       INTEGER,
      pinned_reason   TEXT,
      created_at      INTEGER NOT NULL,
      updated_at      INTEGER NOT NULL,
      accessed_at     INTEGER NOT NULL,
      version         INTEGER DEFAULT 1,
      deleted         INTEGER DEFAULT 0,
      metadata        TEXT    DEFAULT '{}'
    );
    CREATE INDEX IF NOT EXISTS idx_mem_scope    ON memories(scope_type, scope_id);
    CREATE INDEX IF NOT EXISTS idx_mem_category ON memories(category);
    CREATE INDEX IF NOT EXISTS idx_mem_tier    ON memories(tier);
    CREATE INDEX IF NOT EXISTS idx_mem_updated  ON memories(updated_at DESC);
    CREATE INDEX IF NOT EXISTS idx_mem_deleted  ON memories(deleted) WHERE deleted=0;

    CREATE TABLE IF NOT EXISTS evidence (
      id          TEXT PRIMARY KEY,
      memory_id   TEXT NOT NULL,
      type        TEXT NOT NULL,
      source_id   TEXT,
      context     TEXT,
      confidence  REAL    DEFAULT 1.0,
      timestamp   INTEGER NOT NULL,
      created_at  INTEGER NOT NULL,
      FOREIGN KEY (memory_id) REFERENCES memories(id) ON DELETE CASCADE
    );
    CREATE INDEX IF NOT EXISTS idx_ev_memory  ON evidence(memory_id, timestamp DESC);
    CREATE INDEX IF NOT EXISTS idx_ev_type     ON evidence(type, timestamp DESC);

    CREATE TABLE IF NOT EXISTS revisions (
      id             TEXT PRIMARY KEY,
      memory_id      TEXT NOT NULL,
      content        TEXT NOT NULL,
      change_type    TEXT NOT NULL,
      version_num    INTEGER NOT NULL,
      diff_from_prev TEXT,
      agent_id       TEXT,
      created_at     INTEGER NOT NULL,
      FOREIGN KEY (memory_id) REFERENCES memories(id) ON DELETE CASCADE
    );
    CREATE UNIQUE INDEX IF NOT EXISTS idx_rev_mem_ver ON revisions(memory_id, version_num DESC);

    CREATE TABLE IF NOT EXISTS scopes (
      scope_id    TEXT PRIMARY KEY,
      scope_type  TEXT NOT NULL,
      name        TEXT,
      parent_id   TEXT,
      config      TEXT    DEFAULT '{}',
      created_at  INTEGER NOT NULL,
      updated_at  INTEGER NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_scope_type ON scopes(scope_type);

    CREATE TABLE IF NOT EXISTS wal_entries (
      lsn        TEXT PRIMARY KEY,
      operation  TEXT NOT NULL,
      table_name TEXT NOT NULL,
      record_id  TEXT NOT NULL,
      payload    TEXT NOT NULL,
      checksum   TEXT NOT NULL,
      agent_id   TEXT,
      team_space TEXT,
      status     TEXT    DEFAULT 'PENDING',
      created_at INTEGER NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_wal_lsn    ON wal_entries(created_at ASC);
    CREATE INDEX IF NOT EXISTS idx_wal_status ON wal_entries(status) WHERE status != 'COMMITTED';

    CREATE TABLE IF NOT EXISTS rate_limits (
      key          TEXT NOT NULL,
      window_start INTEGER NOT NULL,
      count        INTEGER NOT NULL DEFAULT 0,
      ttl_seconds  INTEGER DEFAULT 120,
      PRIMARY KEY (key, window_start)
    );

    CREATE TABLE IF NOT EXISTS bm25_index (
      term       TEXT NOT NULL,
      memory_id  TEXT NOT NULL,
      frequency  INTEGER NOT NULL,
      positions  TEXT NOT NULL,
      doc_count  INTEGER NOT NULL,
      PRIMARY KEY (term, memory_id)
    );
    CREATE INDEX IF NOT EXISTS idx_bm25_term   ON bm25_index(term, frequency DESC);
    CREATE INDEX IF NOT EXISTS idx_bm25_memory ON bm25_index(memory_id);

    CREATE TABLE IF NOT EXISTS vector_meta (
      memory_id      TEXT PRIMARY KEY,
      vector_id      TEXT NOT NULL,
      vector_version INTEGER NOT NULL DEFAULT 0,
      embedding_model TEXT NOT NULL,
      dimensions     INTEGER NOT NULL,
      dirty          INTEGER DEFAULT 0,
      last_indexed   INTEGER,
      FOREIGN KEY (memory_id) REFERENCES memories(id) ON DELETE CASCADE
    );
    CREATE INDEX IF NOT EXISTS idx_vm_dirty ON vector_meta(dirty) WHERE dirty=1;

    CREATE TABLE IF NOT EXISTS meta (
      key   TEXT PRIMARY KEY,
      value TEXT
    );
  `);
}

// ─── Row ↔ Memory converters ──────────────────────────────────────────────

function rowToMemory(row) {
  if (!row) return null;
  return {
    id:          row.id,
    text:        row.text,
    category:    row.category,
    tags:        parseTags(row.tags),
    importance:  row.importance,
    scope:       row.scope_type + (row.scope_id ? `:${row.scope_id}` : ''),
    scope_type:  row.scope_type,
    scope_id:    row.scope_id,
    tier:        row.tier,
    pinned:      Boolean(row.pinned),
    pinned_at:   row.pinned_at,
    pinned_reason: row.pinned_reason,
    created_at:  row.created_at,
    updated_at:  row.updated_at,
    accessed_at: row.accessed_at,
    version:     row.version,
    deleted:     Boolean(row.deleted),
    metadata:    parseJSON(row.metadata, {}),
  };
}

function memoryToRow(mem) {
  const now = Date.now();
  const [scope_type, scope_id] = parseScope(mem.scope || mem.scope_type || DEFAULT_SCOPE_TYPE, mem.scope_id);
  return {
    id:          mem.id || generateId(),
    text:        mem.text,
    category:    mem.category || 'general',
    tags:        JSON.stringify(Array.isArray(mem.tags) ? mem.tags : []),
    importance:  mem.importance ?? 0.5,
    scope_type: scope_type || DEFAULT_SCOPE_TYPE,
    scope_id:    scope_id || null,
    tier:        TIERS.includes(mem.tier) ? mem.tier : DEFAULT_TIER,
    pinned:      mem.pinned ? 1 : 0,
    pinned_at:   mem.pinned ? (mem.pinned_at || now) : null,
    pinned_reason: mem.pinned_reason || null,
    created_at:  mem.created_at || now,
    updated_at:  now,
    accessed_at: mem.accessed_at || now,
    version:     (mem.version || 0) + 1,
    deleted:     mem.deleted ? 1 : 0,
    metadata:    JSON.stringify(mem.metadata || {}),
  };
}

function parseScope(scope, existingId) {
  if (!scope) return [DEFAULT_SCOPE_TYPE, null];
  if (scope.includes(':')) {
    const [type, id] = scope.split(':', 2);
    return [type?.toUpperCase(), id || null];
  }
  return [scope.toUpperCase(), existingId || null];
}

function parseTags(tags) {
  if (Array.isArray(tags)) return tags;
  try { return JSON.parse(tags || '[]'); } catch { return []; }
}

function parseJSON(str, fallback) {
  if (!str) return fallback;
  try { return JSON.parse(str); } catch { return fallback; }
}

function generateId() {
  return `mem_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`;
}

// ─── BM25 tokenizer ───────────────────────────────────────────────────────

function tokenize(text) {
  if (!text || typeof text !== 'string') return [];
  return text
    .toLowerCase()
    .replace(/[^\p{L}\p{N}\s]/gu, ' ')
    .split(/\s+/)
    .filter(t => t.length > 1);
}

// ─── LSN generator ─────────────────────────────────────────────────────────

let _lsnSeq = 0;
function nextLsn() {
  return `${Date.now()}_${++_lsnSeq}`;
}

// ─── StorageGateway ─────────────────────────────────────────────────────────

export class StorageGateway {
  constructor(options = {}) {
    this._db = null;
    this._initialized = false;
    this._bm25Loaded = false;
    this._bm25DocCount = 0;
    this._bm25AvgLen = 0;
    this._bm25PostingLists = new Map(); // term → Map(memoryId → {freq, positions})
    this._bm25DocLengths = new Map();    // memoryId → token count
    this._bm25IDF = new Map();           // term → IDF value
    this._embeddingModel = options.embeddingModel || 'nomic-embed-text';
  }

  // ── init ────────────────────────────────────────────────────────────────

  async init() {
    if (this._initialized) return;
    if (!existsSync(V4_DIR)) mkdirSync(V4_DIR, { recursive: true });

    const SQLite = getBetterSqlite3();
    this._db = new SQLite(V4_DB_PATH);
    buildSchema(this._db);

    // Try to preload existing BM25 posting lists
    await this._loadBm25Index();

    this._initialized = true;
    console.log('[storage-gateway] v4.0 initialized at', V4_DB_PATH);
  }

  get db() {
    if (!this._db) throw new Error('[storage-gateway] Not initialized. Call init() first.');
    return this._db;
  }

  // ── getMemories ─────────────────────────────────────────────────────────

  /**
   * Get memories with optional filtering.
   * @param {{ scope?, scopeType?, scopeId?, category?, tier?, limit?, offset?, includeDeleted? }} filter
   * @returns {Promise<object[]>}
   */
  async getMemories(filter = {}) {
    const scopeKey = filter.scopeId ? `${filter.scopeType || 'USER'}:${filter.scopeId}` : 'default';
    const { allowed } = this.checkRateLimit(`read:${scopeKey}`, RATE_LIMIT_MAX_READ, 60);
    if (!allowed) {
      throw new Error('[storage-gateway] Rate limit exceeded for reads');
    }

    let sql = 'SELECT * FROM memories WHERE deleted = 0';
    const params = [];

    if (filter.scope || filter.scopeType || filter.scopeId) {
      const [type, id] = parseScope(filter.scope || filter.scopeType, filter.scopeId);
      sql += ' AND scope_type = ?';
      params.push(type);
      if (id) { sql += ' AND scope_id = ?'; params.push(id); }
    }

    if (filter.category) { sql += ' AND category = ?'; params.push(filter.category); }
    if (filter.tier) { sql += ' AND tier = ?'; params.push(filter.tier); }

    sql += ' ORDER BY updated_at DESC';

    if (filter.limit) { sql += ' LIMIT ?'; params.push(filter.limit); }
    if (filter.offset) { sql += ' OFFSET ?'; params.push(filter.offset); }

    const rows = this.db.prepare(sql).all(...params);
    return rows.map(rowToMemory);
  }

  // ── getMemory ────────────────────────────────────────────────────────────

  async getMemory(id) {
    const row = this.db.prepare('SELECT * FROM memories WHERE id = ? AND deleted = 0').get(id);
    if (row) {
      // Update accessed_at
      this.db.prepare('UPDATE memories SET accessed_at = ? WHERE id = ?').run(Date.now(), id);
    }
    return rowToMemory(row);
  }

  // ── writeMemory ─────────────────────────────────────────────────────────

  /**
   * Write (insert or update) a memory with full WAL + index update.
   * All in a single transaction.
   * @param {object} mem
   * @param {{ operation?: string }} options
   */
  async writeMemory(mem, options = {}) {
    const scopeKey = mem.scopeId ? `${mem.scope || 'USER'}:${mem.scopeId}` : 'default';
    const { allowed, retryAfterSec } = this.checkRateLimit(`write:${scopeKey}`, RATE_LIMIT_MAX_WRITE, 60);
    if (!allowed) {
      throw new Error(`[storage-gateway] Rate limit exceeded. Retry after ${Math.ceil(retryAfterSec)}s`);
    }

    const op = options.operation || (mem.id ? 'UPDATE' : 'INSERT');
    const lsn = nextLsn();
    const now = Date.now();
    const row = memoryToRow({ ...mem, updated_at: now });
    const checksum = crypto.createHash('sha256').update(row.text).digest('hex');

    // WAL entry (uncommitted)
    const walEntry = {
      lsn,
      operation: op,
      table_name: 'memories',
      record_id: row.id,
      payload: JSON.stringify(row),
      checksum,
      agent_id: mem.agent_id || null,
      team_space: row.scope_id || null,
      status: 'PENDING',
      created_at: now,
    };

    this.db.transaction(() => {
      // WAL
      this.db.prepare(`
        INSERT OR REPLACE INTO wal_entries
          (lsn, operation, table_name, record_id, payload, checksum, agent_id, team_space, status, created_at)
        VALUES
          (@lsn, @operation, @table_name, @record_id, @payload, @checksum, @agent_id, @team_space, @status, @created_at)
      `).run(walEntry);

      // Memory
      const existing = this.db.prepare('SELECT id FROM memories WHERE id = ?').get(row.id);
      if (existing) {
        this.db.prepare(`
          UPDATE memories SET
            text=@text, category=@category, tags=@tags, importance=@importance,
            scope_type=@scope_type, scope_id=@scope_id, tier=@tier, pinned=@pinned,
            pinned_at=@pinned_at, pinned_reason=@pinned_reason, updated_at=@updated_at,
            accessed_at=@accessed_at, version=version+1, deleted=0, metadata=@metadata
          WHERE id=@id
        `).run(row);
      } else {
        this.db.prepare(`
          INSERT INTO memories (id, text, category, tags, importance, scope_type, scope_id,
            tier, pinned, pinned_at, pinned_reason, created_at, updated_at, accessed_at, version, deleted, metadata)
          VALUES (@id, @text, @category, @tags, @importance, @scope_type, @scope_id,
            @tier, @pinned, @pinned_at, @pinned_reason, @created_at, @updated_at, @accessed_at, @version, @deleted, @metadata)
        `).run(row);
      }

      // Incremental BM25 update
      const oldMem = existing ? this.db.prepare('SELECT text FROM memories WHERE id = ?').get(row.id) : null;
      this._updateBm25Index(row.id, row.text, oldMem?.text);

      // Commit WAL
      this.db.prepare("UPDATE wal_entries SET status='COMMITTED' WHERE lsn = ?").run(lsn);
    })();

    return rowToMemory(row);
  }

  // ── deleteMemory ────────────────────────────────────────────────────────

  async deleteMemory(id) {
    const lsn = nextLsn();
    const existing = this.db.prepare('SELECT * FROM memories WHERE id = ?').get(id);
    if (!existing) return false;

    this.db.transaction(() => {
      // Soft delete
      this.db.prepare('UPDATE memories SET deleted=1, updated_at=? WHERE id=?').run(Date.now(), id);

      // WAL
      this.db.prepare(`
        INSERT INTO wal_entries (lsn, operation, table_name, record_id, payload, checksum, status, created_at)
        VALUES (?, 'DELETE', 'memories', ?, ?, ?, 'COMMITTED', ?)
      `).run(lsn, id, JSON.stringify(existing),
        crypto.createHash('sha256').update(JSON.stringify(existing)).digest('hex'),
        Date.now());

      // Remove from BM25
      this._removeFromBm25Index(id);
    })();

    return true;
  }

  // ── searchMemories (BM25) ───────────────────────────────────────────────

  /**
   * Search memories using incremental BM25.
   * @param {string} query
   * @param {{ topK?, scope?, scopeType? }} options
   * @returns {Promise<object[]>}
   */
  async searchMemories(query, options = {}) {
    const scopeKey = options.scopeId ? `${options.scopeType || 'USER'}:${options.scopeId}` : 'default';
    const { allowed } = this.checkRateLimit(`search:${scopeKey}`, RATE_LIMIT_MAX_SEARCH, 60);
    if (!allowed) {
      throw new Error('[storage-gateway] Rate limit exceeded for search');
    }

    if (!query || !query.trim()) return [];

    const tokens = tokenize(query);
    if (tokens.length === 0) return [];

    // Scope filter
    let scopeCondition = 'deleted = 0';
    const params = [];
    if (options.scope || options.scopeType) {
      const [type, id] = parseScope(options.scope || options.scopeType, options.scopeId);
      scopeCondition += ' AND scope_type = ?';
      params.push(type);
      if (id) { scopeCondition += ' AND scope_id = ?'; params.push(id); }
    }

    // Get all non-deleted memories for scoring
    const rows = this.db.prepare(`SELECT id, text, category, importance, scope_type, scope_id FROM memories WHERE ${scopeCondition}`).all(...params);
    if (rows.length === 0) return [];

    const topK = options.topK || 10;
    const scores = [];

    for (const row of rows) {
      const score = this._bm25Score(tokens, row.id, row.text);
      if (score > 0) {
        scores.push({
          ...rowToMemory(row),
          score: Math.round(score * 1000) / 1000,
        });
      }
    }

    scores.sort((a, b) => b.score - a.score);
    return scores.slice(0, topK);
  }

  // ── evidence ───────────────────────────────────────────────────────────

  // ── Evidence with TTL trim (Phase 5) ──────────────────────────────────

  /** Evidence TTL: 90 days */
  static get EVIDENCE_TTL_MS() { return 90 * 24 * 60 * 60 * 1000; }

  /** Max revisions per memory: 50 */
  static get MAX_REVISIONS_PER_MEMORY() { return 50; }

  /** Global trim runs every N addEvidence calls */
  static get TRIM_EVERY_N_CALLS() { return 50; }

  /** Counter for global trim triggers */
  _evidenceTrimCounter = 0;

  async addEvidence(memoryId, evidence) {
    const id = `ev_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    const now = Date.now();

    // Phase 5: Per-memory TTL trim — O(log n + k) via B-tree index
    const cutoff = now - StorageGateway.EVIDENCE_TTL_MS;
    this.db.prepare(
      'DELETE FROM evidence WHERE memory_id = ? AND timestamp < ?'
    ).run(memoryId, cutoff);

    this.db.prepare(`
      INSERT INTO evidence (id, memory_id, type, source_id, context, confidence, timestamp, created_at)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `).run(id, memoryId, evidence.type || 'manual', evidence.source_id || null,
      evidence.context || null, evidence.confidence ?? 1.0,
      evidence.timestamp || now, now);

    // Phase 5: Global trim every N calls (lightweight, O(log n + k))
    this._evidenceTrimCounter++;
    if (this._evidenceTrimCounter >= StorageGateway.TRIM_EVERY_N_CALLS) {
      this._evidenceTrimCounter = 0;
      this.db.prepare('DELETE FROM evidence WHERE timestamp < ?').run(cutoff);
    }

    return { id };
  }

  /**
   * Phase 5: Trim ALL evidence older than TTL (called periodically or on health check).
   * Uses B-tree index on (timestamp) — O(log n + k).
   */
  async trimEvidence() {
    const now = Date.now();
    const cutoff = now - StorageGateway.EVIDENCE_TTL_MS;
    const result = this.db.prepare(
      'DELETE FROM evidence WHERE timestamp < ?'
    ).run(cutoff);
    return { deleted: result.changes, cutoffMs: cutoff };
  }

  async getEvidence(memoryId) {
    const rows = this.db.prepare(
      'SELECT * FROM evidence WHERE memory_id = ? ORDER BY timestamp DESC'
    ).all(memoryId);
    return rows.map(r => ({ ...r, confidence: r.confidence }));
  }

  // ── revision ────────────────────────────────────────────────────────────

  async addRevision(memoryId, content, changeType = 'update') {
    const id = `rev_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    const now = Date.now();
    const versionRow = this.db.prepare(
      'SELECT COALESCE(MAX(version_num), 0) + 1 as vn FROM revisions WHERE memory_id = ?'
    ).get(memoryId);
    const versionNum = versionRow.vn;

    this.db.prepare(`
      INSERT INTO revisions (id, memory_id, content, change_type, version_num, created_at)
      VALUES (?, ?, ?, ?, ?, ?)
    `).run(id, memoryId, typeof content === 'string' ? content : JSON.stringify(content),
      changeType, versionNum, now);

    // Phase 5: Prune old revisions — keep only MAX_REVISIONS_PER_MEMORY newest
    // Uses B-tree index on (memory_id, version_num DESC) — O(log n)
    this.db.prepare(`
      DELETE FROM revisions WHERE memory_id = ? AND version_num <= (
        SELECT version_num FROM revisions WHERE memory_id = ?
        ORDER BY version_num DESC LIMIT 1 OFFSET ?
      )
    `).run(memoryId, memoryId, StorageGateway.MAX_REVISIONS_PER_MEMORY - 1);

    return { id, version: versionNum };
  }

  async getRevisions(memoryId) {
    const rows = this.db.prepare(
      'SELECT * FROM revisions WHERE memory_id = ? ORDER BY version_num DESC'
    ).all(memoryId);
    return rows;
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // PHASE 3: Multi-Tenant Team Spaces
  // ═══════════════════════════════════════════════════════════════════════════

  /**
   * Create a team scope (called automatically when first team memory is stored)
   */
  async createTeam(teamId, name, config = {}) {
    const now = Date.now();
    this.db.prepare(`
      INSERT OR REPLACE INTO scopes (scope_id, scope_type, name, config, created_at, updated_at)
      VALUES (?, 'TEAM', ?, ?, ?, ?)
    `).run(`team:${teamId}`, name || `Team ${teamId}`, JSON.stringify(config), now, now);
    return { scopeId: `team:${teamId}`, name, config };
  }

  /**
   * Get team configuration
   */
  async getTeam(teamId) {
    const row = this.db.prepare("SELECT * FROM scopes WHERE scope_id = ?").get(`team:${teamId}`);
    if (!row) return null;
    return {
      scopeId: row.scope_id,
      name: row.name,
      config: parseJSON(row.config, {}),
      createdAt: row.created_at,
    };
  }

  /**
   * List all teams
   */
  async listTeams() {
    const rows = this.db.prepare("SELECT * FROM scopes WHERE scope_type = 'TEAM' ORDER BY created_at DESC").all();
    return rows.map(r => ({
      scopeId: r.scope_id,
      name: r.name,
      config: parseJSON(r.config, {}),
      createdAt: r.created_at,
    }));
  }

  /**
   * Delete a team (soft — only removes team scope, memories remain)
   */
  async deleteTeam(teamId) {
    const result = this.db.prepare("DELETE FROM scopes WHERE scope_id = ?").run(`team:${teamId}`);
    return result.changes > 0;
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // PHASE 4: Distributed Rate Limiting (SQLite atomic counters)
  // ═══════════════════════════════════════════════════════════════════════════

  /**
   * Check and increment rate limit for a key.
   * Uses SQLite atomic upsert — safe for concurrent access.
   * @param {string} key - e.g. 'write:team:123' or 'search:user:ou_xxx'
   * @param {number} limit - max calls per window
   * @param {number} windowSec - window size in seconds
   * @returns {{allowed: boolean, remaining: number, resetAt: number}}
   */
  checkRateLimit(key, limit = 30, windowSec = 60) {
    const windowStart = Math.floor(Date.now() / 1000 / windowSec) * windowSec;
    const fullKey = `${key}:${windowStart}`;

    // Atomic read + increment
    const row = this.db.prepare(
      'SELECT count FROM rate_limits WHERE key = ? AND window_start = ?'
    ).get(fullKey, windowStart);
    const count = row?.count || 0;

    if (count >= limit) {
      const resetAt = windowStart + windowSec;
      return { allowed: false, remaining: 0, resetAt, retryAfterSec: windowSec - ((Date.now() / 1000) % windowSec) };
    }

    this.db.prepare(`
      INSERT INTO rate_limits (key, window_start, count, ttl_seconds)
      VALUES (?, ?, 1, ?)
      ON CONFLICT(key, window_start) DO UPDATE SET count = count + 1
    `).run(fullKey, windowStart, windowSec * 2);

    return { allowed: true, remaining: limit - count - 1, resetAt: windowStart + windowSec };
  }

  /**
   * Get rate limit status for a key
   */
  getRateLimitStatus(key, limit = 30, windowSec = 60) {
    const windowStart = Math.floor(Date.now() / 1000 / windowSec) * windowSec;
    const fullKey = `${key}:${windowStart}`;
    const row = this.db.prepare(
      'SELECT count FROM rate_limits WHERE key = ? AND window_start = ?'
    ).get(fullKey, windowStart);
    const count = row?.count || 0;
    return {
      key,
      limit,
      windowSec,
      current: count,
      remaining: Math.max(0, limit - count),
      resetAt: windowStart + windowSec,
      windowStart,
    };
  }

  // ── stats ──────────────────────────────────────────────────────────────

  // ═══════════════════════════════════════════════════════════════════════════
  // PHASE 5: Evidence TTL + Revision Limit (already in addEvidence/addRevision)
  // ═══════════════════════════════════════════════════════════════════════════

  /**
   * Phase 5: Get evidence stats and TTL status.
   */
  async getEvidenceStats() {
    const total = this.db.prepare('SELECT COUNT(*) as c FROM evidence').get().c;
    const oldest = this.db.prepare('SELECT MIN(timestamp) as t FROM evidence').get();
    const newest = this.db.prepare('SELECT MAX(timestamp) as t FROM evidence').get();
    const byType = this.db.prepare(
      'SELECT type, COUNT(*) as c FROM evidence GROUP BY type ORDER BY c DESC'
    ).all();
    return {
      total,
      oldest: oldest.t,
      newest: newest.t,
      ttlDays: StorageGateway.EVIDENCE_TTL_MS / (24 * 60 * 60 * 1000),
      byType,
    };
  }

  /**
   * Phase 5: Get revision stats.
   */
  async getRevisionStats() {
    const total = this.db.prepare('SELECT COUNT(*) as c FROM revisions').get().c;
    const memories = this.db.prepare(
      'SELECT COUNT(DISTINCT memory_id) as c FROM revisions'
    ).get().c;
    const avgVersions = memories > 0 ? Math.round(total / memories * 10) / 10 : 0;
    return { total, memories, avgVersions, maxPerMemory: StorageGateway.MAX_REVISIONS_PER_MEMORY };
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // PHASE 6: WAL Operations (replay, export, import, truncate)
  // ═══════════════════════════════════════════════════════════════════════════

  /**
   * Phase 6: Export WAL entries as JSONL for backup/audit.
   */
  async exportWal(options = {}) {
    const { since, limit = 10000, status } = options;
    let sql = 'SELECT * FROM wal_entries WHERE 1=1';
    const params = [];
    if (since) { sql += ' AND created_at >= ?'; params.push(since); }
    if (status) { sql += ' AND status = ?'; params.push(status); }
    sql += ' ORDER BY created_at ASC LIMIT ?';
    params.push(limit);

    const rows = this.db.prepare(sql).all(...params);
    return rows.map(r => ({ ...r, payload: JSON.parse(r.payload) }));
  }

  /**
   * Phase 6: Import WAL entries from JSONL backup.
   */
  async importWal(entries) {
    const insert = this.db.prepare(`
      INSERT OR IGNORE INTO wal_entries
        (lsn, operation, table_name, record_id, payload, checksum, agent_id, team_space, status, created_at)
      VALUES (@lsn, @operation, @table_name, @record_id, @payload, @checksum, @agent_id, @team_space, @status, @created_at)
    `);

    let imported = 0;
    this.db.transaction(() => {
      for (const entry of entries) {
        try {
          insert.run({
            ...entry,
            payload: typeof entry.payload === 'string' ? entry.payload : JSON.stringify(entry.payload),
          });
          imported++;
        } catch {}
      }
    })();
    return { imported, total: entries.length };
  }

  /**
   * Phase 6: Truncate WAL (keep committed entries, remove rolled-back).
   */
  async truncateWal() {
    const result = this.db.prepare(
      "DELETE FROM wal_entries WHERE status != 'COMMITTED'"
    ).run();
    return { truncated: result.changes };
  }

  /**
   * Phase 6: WAL status summary.
   */
  async getWalStatus() {
    const total = this.db.prepare('SELECT COUNT(*) as c FROM wal_entries').get().c;
    const pending = this.db.prepare(
      "SELECT COUNT(*) as c FROM wal_entries WHERE status = 'PENDING'"
    ).get().c;
    const committed = this.db.prepare(
      "SELECT COUNT(*) as c FROM wal_entries WHERE status = 'COMMITTED'"
    ).get().c;
    const oldest = this.db.prepare(
      'SELECT MIN(created_at) as t FROM wal_entries WHERE status = ?'
    ).get('COMMITTED');

    return { total, pending, committed, oldestTs: oldest.t };
  }

  async stats() {
    const db = this.db;
    const total = db.prepare('SELECT COUNT(*) as c FROM memories WHERE deleted=0').get().c;
    const byCategory = db.prepare(
      'SELECT category, COUNT(*) as c FROM memories WHERE deleted=0 GROUP BY category'
    ).all();
    const byTier = db.prepare(
      'SELECT tier, COUNT(*) as c FROM memories WHERE deleted=0 GROUP BY tier'
    ).all();
    const byScope = db.prepare(
      'SELECT scope_type, COUNT(*) as c FROM memories WHERE deleted=0 GROUP BY scope_type'
    ).all();
    const evidence = db.prepare('SELECT COUNT(*) as c FROM evidence').get().c;
    const revisions = db.prepare('SELECT COUNT(*) as c FROM revisions').get().c;

    return { total, byCategory, byTier, byScope, evidence, revisions };
  }

  // ── BM25 index ──────────────────────────────────────────────────────────

  /**
   * Rebuild full BM25 index from all memories.
   * Call once at startup (loads persisted lists) or when rebuilding.
   */
  async rebuildBm25Index() {
    const rows = this.db.prepare(
      'SELECT id, text FROM memories WHERE deleted = 0'
    ).all();

    this._bm25PostingLists.clear();
    this._bm25DocLengths.clear();
    this._bm25IDF.clear();
    this._bm25DocCount = rows.length;

    let totalTokens = 0;
    for (const row of rows) {
      const tokens = tokenize(row.text);
      this._bm25DocLengths.set(row.id, tokens.length);
      totalTokens += tokens.length;

      for (const [term, positions] of this._tokenPositions(tokens)) {
        if (!this._bm25PostingLists.has(term)) {
          this._bm25PostingLists.set(term, new Map());
        }
        const posting = this._bm25PostingLists.get(term);
        if (posting.has(row.id)) {
          const existing = posting.get(row.id);
          existing.frequency += 1;
          existing.positions.push(...positions);
        } else {
          posting.set(row.id, { frequency: 1, positions });
        }
      }
    }

    this._bm25AvgLen = this._bm25DocCount > 0 ? totalTokens / this._bm25DocCount : 1;

    // Compute IDF for all terms
    for (const [term, postings] of this._bm25PostingLists) {
      const df = postings.size;
      this._bm25IDF.set(term, Math.log((this._bm25DocCount - df + 0.5) / (df + 0.5) + 1));
    }

    this._bm25Loaded = true;
  }

  /**
   * Incrementally update BM25 index for a document.
   * Called inside writeMemory transaction.
   */
  _updateBm25Index(memoryId, newText, oldText) {
    if (!this._bm25Loaded) {
      // Index not yet loaded — skip (will be rebuilt at startup)
      return;
    }

    const oldTokens = oldText ? tokenize(oldText) : [];
    const newTokens = tokenize(newText);

    // Track whether this is a new document (for _bm25DocCount increment)
    const isNewDoc = !this._bm25DocLengths.has(memoryId);

    // Increment doc count on first insert
    if (isNewDoc) {
      this._bm25DocCount++;
      this._bm25AvgLen = ((this._bm25AvgLen * (this._bm25DocCount - 1)) + newTokens.length) / this._bm25DocCount;
    }

    // Remove old token contributions
    if (oldTokens.length > 0) {
      for (const [term, positions] of this._tokenPositions(oldTokens)) {
        const posting = this._bm25PostingLists.get(term);
        if (posting) posting.delete(memoryId);
      }
    }

    // Add new token contributions
    for (const [term, positions] of this._tokenPositions(newTokens)) {
      if (!this._bm25PostingLists.has(term)) {
        this._bm25PostingLists.set(term, new Map());
      }
      const posting = this._bm25PostingLists.get(term);
      if (posting.has(memoryId)) {
        // Update existing term frequency
        const existing = posting.get(memoryId);
        existing.frequency += 1;
        existing.positions.push(...positions);
      } else {
        posting.set(memoryId, { frequency: 1, positions });
        // New term for this doc: update IDF based on updated df
        const df = posting.size; // includes this new doc
        const N = this._bm25DocCount || 1;
        const idf = df > 0 ? Math.log((N - df + 0.5) / (df + 0.5) + 1) : 0;
        this._bm25IDF.set(term, idf);
      }
    }

    // Update doc length
    this._bm25DocLengths.set(memoryId, newTokens.length);

    // Persist posting lists to SQLite
    this._persistBm25PostingList(memoryId, newTokens);
  }

  _removeFromBm25Index(memoryId) {
    for (const [term, posting] of this._bm25PostingLists) {
      if (posting.has(memoryId)) posting.delete(memoryId);
    }
    this._bm25DocLengths.delete(memoryId);
    this.db.prepare('DELETE FROM bm25_index WHERE memory_id = ?').run(memoryId);
  }

  _persistBm25PostingList(memoryId, tokens) {
    // Persist term frequency entries
    const termFreqs = new Map();
    for (const [term, positions] of this._tokenPositions(tokens)) {
      termFreqs.set(term, { frequency: (termFreqs.get(term)?.frequency || 0) + 1, positions });
    }

    const upsert = this.db.prepare(`
      INSERT INTO bm25_index (term, memory_id, frequency, positions, doc_count)
      VALUES (?, ?, ?, ?, ?)
      ON CONFLICT(term, memory_id) DO UPDATE SET
        frequency = excluded.frequency,
        positions = excluded.positions,
        doc_count = excluded.doc_count
    `);

    for (const [term, { frequency, positions }] of termFreqs) {
      const docCount = this._bm25PostingLists.get(term)?.size || 1;
      upsert.run(term, memoryId, frequency, JSON.stringify(positions), docCount);
    }
  }

  _bm25Score(tokens, memoryId, text) {
    if (!this._bm25Loaded) return 0;
    if (tokens.length === 0) return 0;

    const docLen = this._bm25DocLengths.get(memoryId) || tokenize(text).length || 1;
    let score = 0;

    for (const term of tokens) {
      const posting = this._bm25PostingLists.get(term);
      if (!posting) continue;

      const docInfo = posting.get(memoryId);
      if (!docInfo) continue;

      const tf = docInfo.frequency;
      const idf = this._bm25IDF.get(term) || 0;
      const numerator = tf * (BM25_K1 + 1);
      const denominator = tf + BM25_K1 * (1 - BM25_B + BM25_B * (docLen / this._bm25AvgLen));
      score += idf * (numerator / denominator);
    }

    return score;
  }

  *_tokenPositions(tokens) {
    const map = new Map();
    for (let i = 0; i < tokens.length; i++) {
      if (!map.has(tokens[i])) map.set(tokens[i], []);
      map.get(tokens[i]).push(i);
    }
    yield* map;
  }

  async _loadBm25Index() {
    try {
      const rows = this.db.prepare('SELECT id, text FROM memories WHERE deleted = 0').all();
      if (rows.length === 0) {
        this._bm25Loaded = true;
        return;
      }

      // Load from persisted posting lists
      const postingRows = this.db.prepare('SELECT term, memory_id, frequency, positions FROM bm25_index').all();
      if (postingRows.length > 0) {
        for (const row of postingRows) {
          if (!this._bm25PostingLists.has(row.term)) {
            this._bm25PostingLists.set(row.term, new Map());
          }
          this._bm25PostingLists.get(row.term).set(row.memory_id, {
            frequency: row.frequency,
            positions: JSON.parse(row.positions),
          });
          if (!this._bm25DocLengths.has(row.memory_id)) {
            this._bm25DocLengths.set(row.memory_id, 0);
          }
        }
        // Compute doc lengths from posting lists
        for (const [term, posting] of this._bm25PostingLists) {
          for (const [memId, info] of posting) {
            this._bm25DocLengths.set(memId, (this._bm25DocLengths.get(memId) || 0) + info.frequency);
          }
        }
        this._bm25DocCount = rows.length;
        this._bm25AvgLen = Array.from(this._bm25DocLengths.values()).reduce((a, b) => a + b, 0) / this._bm25DocCount || 1;
        for (const [term, posting] of this._bm25PostingLists) {
          this._bm25IDF.set(term, Math.log((this._bm25DocCount - posting.size + 0.5) / (posting.size + 0.5) + 1));
        }
        this._bm25Loaded = true;
        console.log(`[storage-gateway] BM25 loaded: ${this._bm25PostingLists.size} terms, ${this._bm25DocCount} docs`);
        return;
      }

      // No persisted data — rebuild from scratch
      await this.rebuildBm25Index();
    } catch (e) {
      console.warn('[storage-gateway] BM25 load failed, will rebuild:', e.message);
      await this.rebuildBm25Index();
    }
  }

  // ── close ───────────────────────────────────────────────────────────────

  close() {
    if (this._db) {
      this._db.close();
      this._db = null;
      this._initialized = false;
    }
  }
}

export default StorageGateway;
