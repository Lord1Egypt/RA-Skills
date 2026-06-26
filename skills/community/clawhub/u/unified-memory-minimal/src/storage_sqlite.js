/**
 * SQLite Storage Backend for unified-memory
 * Uses better-sqlite3 (synchronous API, ideal for embedded/CLI use)
 * Implements the same interface as JSON storage: readMemories / writeMemories / appendMemory
 * Supports concurrent writes via WAL mode
 * 
 * P0-2: Optimistic locking via version field on all write operations.
 * Storage path: ~/.unified-memory/memories.db
 * Env: STORAGE_MODE=json|sqlite (default: json)
 */

import { createRequire } from 'module';
import { existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import os from 'os';

// Load better-sqlite3 via createRequire (available globally from @tobilu/qmd dependency)
const req = createRequire(import.meta.url);
let Database;
try {
  Database = req('better-sqlite3');
} catch {
  // Try global path fallback
  try {
    Database = req('/usr/local/lib/node_modules/@tobilu/qmd/node_modules/better-sqlite3');
  } catch {
    Database = null;
  }
}

const DB_PATH = join(os.homedir(), '.unified-memory', 'memories.db');

// Lazy-initialized database handle
let _db = null;

function getDb() {
  if (_db) return _db;

  if (!Database) {
    throw new Error('[storage_sqlite] better-sqlite3 not available. Install it or ensure it is in NODE_PATH.');
  }

  const dir = join(os.homedir(), '.unified-memory');
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }

  _db = new Database(DB_PATH);

  // Enable WAL mode for better concurrent write performance
  _db.pragma('journal_mode = WAL');
  _db.pragma('synchronous = NORMAL');
  _db.pragma('foreign_keys = ON');

  // Create schema — v2 adds `version` column for optimistic locking
  _db.exec(`
    CREATE TABLE IF NOT EXISTS memories (
      id          TEXT PRIMARY KEY,
      text        TEXT NOT NULL,
      category    TEXT NOT NULL DEFAULT 'general',
      importance  REAL NOT NULL DEFAULT 0.5,
      tags        TEXT NOT NULL DEFAULT '[]',
      scope       TEXT NOT NULL DEFAULT 'USER',
      pinned      INTEGER NOT NULL DEFAULT 0,
      pinned_at   INTEGER,
      pinned_reason TEXT,
      created_at  INTEGER NOT NULL,
      updated_at  INTEGER NOT NULL,
      access_count INTEGER NOT NULL DEFAULT 0,
      last_access INTEGER,
      embedding   TEXT,
      agent_id    TEXT,
      source      TEXT DEFAULT 'manual',
      version     INTEGER NOT NULL DEFAULT 0
    );

    CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(category);
    CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance);
    CREATE INDEX IF NOT EXISTS idx_memories_created_at ON memories(created_at);
    CREATE INDEX IF NOT EXISTS idx_memories_scope ON memories(scope);
    CREATE INDEX IF NOT EXISTS idx_memories_pinned ON memories(pinned);
  `);

  // Migrate: add version column if it doesn't exist (existing DBs before v2)
  try {
    _db.exec("ALTER TABLE memories ADD COLUMN version INTEGER NOT NULL DEFAULT 0");
  } catch {
    // Column already exists — ignore
  }

  return _db;
}

// ============================================================
// Public API — mirrors JSON storage interface
// ============================================================

/**
 * Read all memories from SQLite
 * @returns {Array} memories
 */
export function readMemories() {
  const db = getDb();
  const rows = db.prepare(`
    SELECT id, text, category, importance, tags, scope, pinned, pinned_at,
           pinned_reason, created_at, updated_at, access_count, last_access,
           embedding, agent_id, source, version
    FROM memories
    ORDER BY created_at ASC
  `).all();

  return rows.map(rowToMemory);
}

/**
 * Write ALL memories (full overwrite — replaces entire table)
 * Used by saveMemories() to do atomic full-sync writes
 * @param {Array} memories
 */
export function writeMemories(memories) {
  const db = getDb();

  // Use transaction for atomicity
  const writeTx = db.transaction(() => {
    // Clear existing
    db.prepare('DELETE FROM memories').run();

    if (memories.length === 0) return;

    const insert = db.prepare(`
      INSERT INTO memories (
        id, text, category, importance, tags, scope, pinned, pinned_at,
        pinned_reason, created_at, updated_at, access_count, last_access,
        embedding, agent_id, source, version
      ) VALUES (
        @id, @text, @category, @importance, @tags, @scope, @pinned, @pinned_at,
        @pinned_reason, @created_at, @updated_at, @access_count, @last_access,
        @embedding, @agent_id, @source, @version
      )
    `);

    for (const mem of memories) {
      insert.run(memoryToRow(mem));
    }
  });

  writeTx();
}

/**
 * Append a single memory to SQLite (insert-only, used for real-time adds)
 * @param {object} mem - memory object
 * @returns {object} the inserted memory
 */
export function appendMemory(mem) {
  const db = getDb();
  const insert = db.prepare(`
    INSERT INTO memories (
      id, text, category, importance, tags, scope, pinned, pinned_at,
      pinned_reason, created_at, updated_at, access_count, last_access,
      embedding, agent_id, source, version
    ) VALUES (
      @id, @text, @category, @importance, @tags, @scope, @pinned, @pinned_at,
      @pinned_reason, @created_at, @updated_at, @access_count, @last_access,
      @embedding, @agent_id, @source, @version
    )
  `);

  insert.run(memoryToRow(mem));
  return mem;
}

/**
 * Update a memory by id (standard — no version check)
 * @param {string} id
 * @param {object} updates - partial memory fields
 * @returns {boolean} success
 */
export function updateMemoryById(id, updates) {
  const db = getDb();

  // Build dynamic SET clause
  const allowedFields = [
    'text', 'category', 'importance', 'tags', 'scope', 'pinned',
    'pinned_at', 'pinned_reason', 'access_count', 'last_access', 'updated_at', 'embedding'
  ];

  const sets = [];
  const params = { id };

  for (const field of allowedFields) {
    if (field in updates) {
      const colName = fieldToColumn(field);
      sets.push(`${colName} = @${field}`);
      params[field] = field === 'tags' ? JSON.stringify(updates[field])
        : field === 'pinned' ? (updates[field] ? 1 : 0)
        : updates[field];
    }
  }

  if (sets.length === 0) return false;

  params.updated_at = Date.now();
  sets.push('updated_at = @updated_at');

  const sql = `UPDATE memories SET ${sets.join(', ')} WHERE id = @id`;
  const result = db.prepare(sql).run(params);
  return result.changes > 0;
}

/**
 * P0-2: Optimistic-lock update.
 * Updates only if the current version matches expectedVersion.
 * Returns { success: true } on success, or { conflict: true, memory_id, current_version, your_version }.
 * @param {string} id
 * @param {object} updates - partial memory fields
 * @param {number} expectedVersion - the version the caller expects
 * @returns {{ success: boolean } | { conflict: true, memory_id: string, current_version: number, your_version: number }}
 */
export function updateMemoryByIdOptimistic(id, updates, expectedVersion) {
  const db = getDb();

  const allowedFields = [
    'text', 'category', 'importance', 'tags', 'scope', 'pinned',
    'pinned_at', 'pinned_reason', 'access_count', 'last_access', 'embedding'
  ];

  const sets = [];
  const params = { id, expectedVersion };

  for (const field of allowedFields) {
    if (field in updates) {
      const colName = fieldToColumn(field);
      sets.push(`${colName} = @${field}`);
      params[field] = field === 'tags' ? JSON.stringify(updates[field])
        : field === 'pinned' ? (updates[field] ? 1 : 0)
        : updates[field];
    }
  }

  if (sets.length === 0) return { success: false };

  params.updated_at = Date.now();
  sets.push('updated_at = @updated_at');
  sets.push('version = version + 1');

  const sql = `UPDATE memories SET ${sets.join(', ')} WHERE id = @id AND version = @expectedVersion`;
  const result = db.prepare(sql).run(params);

  if (result.changes === 0) {
    // Either row doesn't exist or version mismatch — fetch current version
    const row = db.prepare('SELECT version FROM memories WHERE id = ?').get(id);
    const currentVersion = row ? row.version : null;
    return {
      conflict: true,
      memory_id: id,
      current_version: currentVersion,
      your_version: expectedVersion,
    };
  }

  return { success: true };
}

/**
 * P0-2: Optimistic-lock delete.
 * Deletes only if the current version matches expectedVersion.
 * @param {string} id
 * @param {number} expectedVersion
 * @returns {{ success: boolean } | { conflict: true, memory_id: string, current_version: number, your_version: number }}
 */
export function deleteMemoryByIdOptimistic(id, expectedVersion) {
  const db = getDb();
  const result = db.prepare(
    'DELETE FROM memories WHERE id = ? AND version = ?'
  ).run(id, expectedVersion);

  if (result.changes === 0) {
    const row = db.prepare('SELECT version FROM memories WHERE id = ?').get(id);
    const currentVersion = row ? row.version : null;
    return {
      conflict: true,
      memory_id: id,
      current_version: currentVersion,
      your_version: expectedVersion,
    };
  }

  return { success: true };
}

/**
 * Delete a memory by id (standard — no version check)
 * @param {string} id
 * @returns {boolean} success
 */
export function deleteMemoryById(id) {
  const db = getDb();
  const result = db.prepare('DELETE FROM memories WHERE id = ?').run(id);
  return result.changes > 0;
}

/**
 * Get a single memory by id
 * @param {string} id
 * @returns {object|null}
 */
export function getMemoryById(id) {
  const db = getDb();
  const row = db.prepare('SELECT * FROM memories WHERE id = ?').get(id);
  return row ? rowToMemory(row) : null;
}

/**
 * Touch a memory (increment access_count, update last_access)
 * @param {string} id
 */
export function touchMemoryById(id) {
  const db = getDb();
  db.prepare(`
    UPDATE memories
    SET access_count = access_count + 1, last_access = @now, updated_at = @now
    WHERE id = @id
  `).run({ id, now: Date.now() });
}

/**
 * Get pinned memories
 * @returns {Array}
 */
export function getPinnedMemories() {
  const db = getDb();
  const rows = db.prepare('SELECT * FROM memories WHERE pinned = 1 ORDER BY created_at ASC').all();
  return rows.map(rowToMemory);
}

/**
 * Pin a memory
 * @param {string} id
 * @param {string} reason
 * @returns {boolean}
 */
export function pinMemoryById(id, reason = '') {
  const db = getDb();
  const result = db.prepare(`
    UPDATE memories SET pinned = 1, pinned_at = @now, pinned_reason = @reason, updated_at = @now
    WHERE id = @id
  `).run({ id, now: Date.now(), reason: String(reason).slice(0, 200) });
  return result.changes > 0;
}

/**
 * Unpin a memory
 * @param {string} id
 * @returns {boolean}
 */
export function unpinMemoryById(id) {
  const db = getDb();
  const result = db.prepare(`
    UPDATE memories SET pinned = 0, pinned_at = NULL, pinned_reason = NULL, updated_at = @now
    WHERE id = @id
  `).run({ id, now: Date.now() });
  return result.changes > 0;
}

/**
 * Get memory count
 * @returns {number}
 */
export function getMemoryCount() {
  const db = getDb();
  const row = db.prepare('SELECT COUNT(*) as count FROM memories').get();
  return row.count;
}

/**
 * Get DB path
 * @returns {string}
 */
export function getDbPath() {
  return DB_PATH;
}

/**
 * Close database connection (for graceful shutdown)
 */
export function closeDb() {
  if (_db) {
    _db.close();
    _db = null;
  }
}

// ============================================================
// Internal helpers
// ============================================================

/**
 * Map memory object to SQLite row
 */
function memoryToRow(mem) {
  return {
    id: mem.id,
    text: mem.text || '',
    category: mem.category || 'general',
    importance: mem.importance ?? 0.5,
    tags: JSON.stringify(Array.isArray(mem.tags) ? mem.tags : []),
    scope: mem.scope || 'USER',
    pinned: mem.pinned ? 1 : 0,
    pinned_at: mem.pinnedAt || null,
    pinned_reason: mem.pinnedReason || null,
    created_at: mem.created_at || Date.now(),
    updated_at: mem.updated_at || Date.now(),
    access_count: mem.access_count || 0,
    last_access: mem.last_access || null,
    embedding: mem.embedding ? JSON.stringify(mem.embedding) : null,
    agent_id: mem.agent_id || null,
    source: mem.source || 'manual',
    version: mem.version ?? 0,
  };
}

/**
 * Map SQLite row to memory object
 */
function rowToMemory(row) {
  return {
    id: row.id,
    text: row.text,
    category: row.category,
    importance: row.importance,
    tags: parseTags(row.tags),
    scope: row.scope,
    pinned: row.pinned === 1,
    pinnedAt: row.pinned_at || null,
    pinnedReason: row.pinned_reason || null,
    created_at: row.created_at,
    updated_at: row.updated_at,
    access_count: row.access_count,
    last_access: row.last_access || null,
    ...(row.embedding ? { embedding: JSON.parse(row.embedding) } : {}),
    ...(row.agent_id ? { agent_id: row.agent_id } : {}),
    source: row.source,
    version: row.version ?? 0,
  };
}

/**
 * Parse tags from JSON string or array
 */
function parseTags(tags) {
  if (Array.isArray(tags)) return tags;
  if (typeof tags === 'string') {
    try { return JSON.parse(tags); } catch { return []; }
  }
  return [];
}

/**
 * Map memory field name to column name
 */
function fieldToColumn(field) {
  const map = {
    pinnedAt: 'pinned_at',
    pinnedReason: 'pinned_reason',
    access_count: 'access_count',
    last_access: 'last_access',
    created_at: 'created_at',
    updated_at: 'updated_at',
    agent_id: 'agent_id',
  };
  return map[field] || field;
}

export default {
  readMemories,
  writeMemories,
  appendMemory,
  updateMemoryById,
  updateMemoryByIdOptimistic,
  deleteMemoryById,
  deleteMemoryByIdOptimistic,
  getMemoryById,
  touchMemoryById,
  getPinnedMemories,
  pinMemoryById,
  unpinMemoryById,
  getMemoryCount,
  getDbPath,
  closeDb,
};
