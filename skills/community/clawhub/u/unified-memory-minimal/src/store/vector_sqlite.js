/**
 * VectorStore: SQLite-based vector storage using sqlite-vec extension.
 * Migrated from memory-tencentdb (TypeScript → JavaScript)
 *
 * Manages two layers of vector-indexed data in a single SQLite database:
 *
 * **L1 (structured memories):**
 * 1. `l1_records` — relational metadata table (content, type, priority, scene, timestamps)
 * 2. `l1_vec` — vec0 virtual table for cosine similarity search
 *
 * **L0 (raw conversations):**
 * 3. `l0_conversations` — relational metadata table (session_key, role, message text, timestamps)
 * 4. `l0_vec` — vec0 virtual table for cosine similarity search on individual messages
 *
 * Design:
 * - All operations are synchronous (DatabaseSync API).
 * - Writes use manual BEGIN/COMMIT transactions for atomicity (metadata + vector).
 * - vec0 virtual table does NOT support ON CONFLICT, so upsert = delete + insert.
 * - Thread-safe via WAL mode.
 */

import { createRequire } from "node:module";

// Use createRequire to load the experimental node:sqlite module
const require = createRequire(import.meta.url);

function requireNodeSqlite() {
  return require("node:sqlite");
}

// ============================
// FTS5 helpers (adapted from openclaw core hybrid.ts)
// ============================

// ── Chinese word segmentation (jieba) ──
// Lazy-loaded singleton: initialised on first call to `buildFtsQuery`.
// If @node-rs/jieba is unavailable, falls back to Unicode-regex splitting.

/** @type {Object|null|undefined} */
let _jieba = undefined; // undefined = not yet tried

function getJieba() {
  if (_jieba !== undefined) return _jieba;
  try {
    const { Jieba } = require("@node-rs/jieba");
    const { dict } = require("@node-rs/jieba/dict");
    _jieba = Jieba.withDict(dict);
  } catch {
    _jieba = null; // mark as unavailable
  }
  return _jieba;
}

/**
 * Common Chinese stop-words that add noise to FTS5 queries.
 */
const ZH_STOP_WORDS = new Set([
  "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一",
  "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着",
  "没有", "看", "好", "自己", "这", "他", "她", "它", "们", "那",
  "吗", "吧", "呢", "啊", "呀", "哦", "嗯",
]);

/**
 * Build an FTS5 MATCH query from raw text.
 */
export function buildFtsQuery(raw) {
  const jieba = getJieba();

  let tokens;
  if (jieba) {
    tokens = jieba
      .cutForSearch(raw, true)
      .map((t) => t.trim())
      .filter((t) => {
        if (!t) return false;
        if (!/[\p{L}\p{N}]/u.test(t)) return false;
        if (ZH_STOP_WORDS.has(t)) return false;
        return true;
      });
    tokens = [...new Set(tokens)];
  } else {
    tokens =
      raw
        .match(/[\p{L}\p{N}_]+/gu)
        ?.map((t) => t.trim())
        .filter(Boolean) ?? [];
  }

  if (tokens.length === 0) return null;
  const quoted = tokens.map((t) => `"${t.replaceAll('"', "")}"`);
  return quoted.join(" OR ");
}

/**
 * Tokenize text for FTS5 indexing (write-side).
 */
export function tokenizeForFts(raw) {
  const jieba = getJieba();
  if (!jieba) return raw;
  const tokens = jieba.cutForSearch(raw, true);
  return tokens.join(" ");
}

/**
 * Reset jieba state for testing.
 */
export function _resetJiebaForTest() {
  _jieba = undefined;
}

/**
 * Override jieba instance for testing.
 * @param {Object|null} instance
 */
export function _setJiebaForTest(instance) {
  _jieba = instance;
}

/**
 * Convert a BM25 rank (negative = more relevant) to a 0–1 score.
 */
export function bm25RankToScore(rank) {
  if (!Number.isFinite(rank)) return 1 / (1 + 999);
  if (rank < 0) {
    const relevance = -rank;
    return relevance / (1 + relevance);
  }
  return 1 / (1 + rank);
}

/** @type {string} */
const TAG = "[memory-unified][vector-sqlite]";

// ============================
// VectorStore class
// ============================

export class VectorStore {
  /**
   * @param {string} dbPath
   * @param {number} dimensions
   * @param {Object} [logger]
   */
  constructor(dbPath, dimensions, logger) {
    this.dimensions = dimensions;
    this.logger = logger;

    /** @type {boolean} */
    this.degraded = false;

    /** @type {boolean} */
    this.closed = false;

    /** @type {boolean} */
    this.vecTablesReady = false;

    // Open database with extension support enabled
    const { DatabaseSync: DbSync } = requireNodeSqlite();
    this.db = new DbSync(dbPath, { allowExtension: true });

    // Performance pragmas
    this.db.exec("PRAGMA busy_timeout = 5000");
    this.db.exec("PRAGMA journal_mode = WAL");
    this.db.exec("PRAGMA cache_size = -65536");
    this.db.exec("PRAGMA mmap_size = 134217728");
    this.db.exec("PRAGMA wal_autocheckpoint = 1000");

    // Prepared statements — initialized in initSchema
    /** @type {Object} */
    this.statements = {};
  }

  isDegraded() {
    return this.degraded;
  }

  /**
   * Load sqlite-vec extension and initialize database schema.
   * @param {Object} [providerInfo]
   * @returns {{ needsReindex: boolean, reason?: string }}
   */
  init(providerInfo) {
    try {
      const sqliteVec = require("sqlite-vec");
      this.db.enableLoadExtension(true);
      sqliteVec.load(this.db);
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      this.logger?.error(
        `${TAG} Failed to load sqlite-vec extension: ${message}. ` +
        `VectorStore entering degraded mode.`,
      );
      this.degraded = true;
      return { needsReindex: false, reason: `sqlite-vec load failed: ${message}` };
    }

    try {
      return this.initSchema(providerInfo);
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      this.logger?.error(
        `${TAG} Schema initialization failed: ${message}. ` +
        `VectorStore entering degraded mode.`,
      );
      this.degraded = true;
      return { needsReindex: false, reason: `schema init failed: ${message}` };
    }
  }

  /**
   * Internal schema initialization.
   * @param {Object} [providerInfo]
   * @returns {{ needsReindex: boolean, reason?: string }}
   */
  initSchema(providerInfo) {
    // Track which provider/model/dimensions were used to generate vectors
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS embedding_meta (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
      )
    `);

    let needsReindex = false;
    let reindexReason;

    const savedMeta = this.readEmbeddingMeta();

    if (providerInfo) {
      if (savedMeta) {
        const providerChanged = savedMeta.provider !== providerInfo.provider;
        const modelChanged = savedMeta.model !== providerInfo.model;
        const dimsChanged = savedMeta.dimensions !== this.dimensions;

        if (providerChanged || modelChanged || dimsChanged) {
          const reasons = [];
          if (providerChanged) reasons.push(`provider: ${savedMeta.provider} → ${providerInfo.provider}`);
          if (modelChanged) reasons.push(`model: ${savedMeta.model} → ${providerInfo.model}`);
          if (dimsChanged) reasons.push(`dimensions: ${savedMeta.dimensions} → ${this.dimensions}`);
          reindexReason = reasons.join(", ");

          this.logger?.info(
            `${TAG} Embedding config changed (${reindexReason}). ` +
            `Dropping vector tables for rebuild...`,
          );
          this.dropVectorTables();
          needsReindex = true;
        }
      } else {
        const l1Count = this.tableRowCount("l1_records");
        const l0Count = this.tableRowCount("l0_conversations");
        const existingVecDims = this.getVecTableDimensions();

        if (l1Count > 0 || l0Count > 0) {
          this.logger?.info(
            `${TAG} No embedding_meta found but existing data exists ` +
            `(L1=${l1Count}, L0=${l0Count}). Dropping vector tables for safety...`,
          );
          this.dropVectorTables();
          needsReindex = true;
          reindexReason = "legacy DB without embedding_meta";
        } else if (existingVecDims !== null && existingVecDims !== this.dimensions) {
          this.logger?.info(
            `${TAG} vec0 table dimension mismatch (existing=${existingVecDims}, ` +
            `required=${this.dimensions}). Dropping vector tables for rebuild...`,
          );
          this.dropVectorTables();
        }
      }
    }

    // ── L1 schema ──────────────────────────────────

    this.db.exec(`
      CREATE TABLE IF NOT EXISTS l1_records (
        record_id TEXT PRIMARY KEY,
        content TEXT NOT NULL,
        type TEXT DEFAULT '',
        priority INTEGER DEFAULT 50,
        scene_name TEXT DEFAULT '',
        session_key TEXT DEFAULT '',
        session_id TEXT DEFAULT '',
        timestamp_str TEXT DEFAULT '',
        timestamp_start TEXT DEFAULT '',
        timestamp_end TEXT DEFAULT '',
        created_time TEXT DEFAULT '',
        updated_time TEXT DEFAULT '',
        metadata_json TEXT DEFAULT '{}'
      )
    `);

    this.db.exec("CREATE INDEX IF NOT EXISTS idx_l1_type ON l1_records(type)");
    this.db.exec("CREATE INDEX IF NOT EXISTS idx_l1_session_key ON l1_records(session_key)");
    this.db.exec("CREATE INDEX IF NOT EXISTS idx_l1_session_id ON l1_records(session_id)");
    this.db.exec("CREATE INDEX IF NOT EXISTS idx_l1_scene ON l1_records(scene_name)");
    this.db.exec("CREATE INDEX IF NOT EXISTS idx_l1_ts_start ON l1_records(timestamp_start)");
    this.db.exec("CREATE INDEX IF NOT EXISTS idx_l1_ts_end ON l1_records(timestamp_end)");
    this.db.exec("CREATE INDEX IF NOT EXISTS idx_l1_session_updated ON l1_records(session_id, updated_time)");
    this.db.exec("CREATE INDEX IF NOT EXISTS idx_l1_sessionkey_updated ON l1_records(session_key, updated_time)");

    if (this.dimensions > 0) {
      this.db.exec(`
        CREATE VIRTUAL TABLE IF NOT EXISTS l1_vec USING vec0(
          record_id TEXT PRIMARY KEY,
          embedding float[${this.dimensions}] distance_metric=cosine,
          updated_time TEXT DEFAULT ''
        )
      `);
    }

    // L1 prepared statements
    this.statements.l1UpsertMeta = this.db.prepare(`
      INSERT INTO l1_records (
        record_id, content, type, priority, scene_name, session_key, session_id,
        timestamp_str, timestamp_start, timestamp_end,
        created_time, updated_time, metadata_json
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      ON CONFLICT(record_id) DO UPDATE SET
        content=excluded.content,
        type=excluded.type,
        priority=excluded.priority,
        scene_name=excluded.scene_name,
        timestamp_str=excluded.timestamp_str,
        timestamp_start=excluded.timestamp_start,
        timestamp_end=excluded.timestamp_end,
        updated_time=excluded.updated_time,
        metadata_json=excluded.metadata_json
    `);

    if (this.dimensions > 0) {
      this.statements.l1DeleteVec = this.db.prepare("DELETE FROM l1_vec WHERE record_id = ?");
      this.statements.l1InsertVec = this.db.prepare("INSERT INTO l1_vec (record_id, embedding, updated_time) VALUES (?, ?, ?)");
    }
    this.statements.l1DeleteMeta = this.db.prepare("DELETE FROM l1_records WHERE record_id = ?");

    this.statements.l1GetMeta = this.db.prepare(`
      SELECT content, type, priority, scene_name, session_key, session_id,
             timestamp_str, timestamp_start, timestamp_end, metadata_json
      FROM l1_records WHERE record_id = ?
    `);

    if (this.dimensions > 0) {
      this.statements.l1SearchVec = this.db.prepare(`
        SELECT record_id, distance
        FROM l1_vec
        WHERE embedding MATCH ?
          AND k = ?
        ORDER BY distance
      `);
    }

    // ── L0 schema ──────────────────────────────────

    this.db.exec(`
      CREATE TABLE IF NOT EXISTS l0_conversations (
        record_id TEXT PRIMARY KEY,
        session_key TEXT NOT NULL,
        session_id TEXT DEFAULT '',
        role TEXT NOT NULL DEFAULT '',
        message_text TEXT NOT NULL,
        recorded_at TEXT DEFAULT '',
        timestamp INTEGER DEFAULT 0
      )
    `);

    try {
      this.db.exec("ALTER TABLE l0_conversations ADD COLUMN timestamp INTEGER DEFAULT 0");
    } catch {
      // Column already exists
    }

    this.db.exec("CREATE INDEX IF NOT EXISTS idx_l0_session ON l0_conversations(session_key)");
    this.db.exec("CREATE INDEX IF NOT EXISTS idx_l0_session_id ON l0_conversations(session_id)");
    this.db.exec("CREATE INDEX IF NOT EXISTS idx_l0_recorded ON l0_conversations(recorded_at)");
    this.db.exec("CREATE INDEX IF NOT EXISTS idx_l0_timestamp ON l0_conversations(timestamp)");

    if (this.dimensions > 0) {
      this.db.exec(`
        CREATE VIRTUAL TABLE IF NOT EXISTS l0_vec USING vec0(
          record_id TEXT PRIMARY KEY,
          embedding float[${this.dimensions}] distance_metric=cosine,
          recorded_at TEXT DEFAULT ''
        )
      `);
    }

    // L0 prepared statements
    this.statements.l0UpsertMeta = this.db.prepare(`
      INSERT INTO l0_conversations (
        record_id, session_key, session_id, role, message_text, recorded_at, timestamp
      ) VALUES (?, ?, ?, ?, ?, ?, ?)
      ON CONFLICT(record_id) DO UPDATE SET
        message_text=excluded.message_text,
        recorded_at=excluded.recorded_at,
        timestamp=excluded.timestamp
    `);

    if (this.dimensions > 0) {
      this.statements.l0DeleteVec = this.db.prepare("DELETE FROM l0_vec WHERE record_id = ?");
      this.statements.l0InsertVec = this.db.prepare("INSERT INTO l0_vec (record_id, embedding, recorded_at) VALUES (?, ?, ?)");
    }
    this.statements.l0DeleteMeta = this.db.prepare("DELETE FROM l0_conversations WHERE record_id = ?");

    this.statements.l0GetMeta = this.db.prepare(`
      SELECT session_key, session_id, role, message_text, recorded_at, timestamp
      FROM l0_conversations WHERE record_id = ?
    `);

    if (this.dimensions > 0) {
      this.statements.l0SearchVec = this.db.prepare(`
        SELECT record_id, distance
        FROM l0_vec
        WHERE embedding MATCH ?
          AND k = ?
        ORDER BY distance
      `);
    }

    this.statements.l0QueryAll = this.db.prepare(`
      SELECT record_id, session_key, session_id, role, message_text, recorded_at, timestamp
      FROM l0_conversations
      WHERE session_key = ?
      ORDER BY timestamp DESC
      LIMIT ?
    `);

    this.statements.l0QueryAfter = this.db.prepare(`
      SELECT record_id, session_key, session_id, role, message_text, recorded_at, timestamp
      FROM l0_conversations
      WHERE session_key = ? AND timestamp > ?
      ORDER BY timestamp DESC
      LIMIT ?
    `);

    // ── FTS5 tables ──────────────────────────────────
    const needsFtsRebuild = this.migrateFtsTablesIfNeeded();

    try {
      this.db.exec(`
        CREATE VIRTUAL TABLE IF NOT EXISTS l1_fts USING fts5(
          content,
          content_original UNINDEXED,
          record_id UNINDEXED,
          type UNINDEXED,
          priority UNINDEXED,
          scene_name UNINDEXED,
          session_key UNINDEXED,
          session_id UNINDEXED,
          timestamp_str UNINDEXED,
          timestamp_start UNINDEXED,
          timestamp_end UNINDEXED,
          metadata_json UNINDEXED
        )
      `);

      this.db.exec(`
        CREATE VIRTUAL TABLE IF NOT EXISTS l0_fts USING fts5(
          message_text,
          message_text_original UNINDEXED,
          record_id UNINDEXED,
          session_key UNINDEXED,
          session_id UNINDEXED,
          role UNINDEXED,
          recorded_at UNINDEXED,
          timestamp UNINDEXED
        )
      `);

      this.statements.l1FtsInsert = this.db.prepare(`
        INSERT INTO l1_fts (content, content_original, record_id, type, priority, scene_name,
          session_key, session_id, timestamp_str, timestamp_start, timestamp_end, metadata_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `);

      this.statements.l1FtsDelete = this.db.prepare("DELETE FROM l1_fts WHERE record_id = ?");

      this.statements.l1FtsSearch = this.db.prepare(`
        SELECT record_id, content_original AS content, type, priority, scene_name,
               session_key, session_id, timestamp_str, timestamp_start, timestamp_end,
               metadata_json,
               bm25(l1_fts) AS rank
        FROM l1_fts
        WHERE l1_fts MATCH ?
        ORDER BY rank ASC
        LIMIT ?
      `);

      this.statements.l0FtsInsert = this.db.prepare(`
        INSERT INTO l0_fts (message_text, message_text_original, record_id, session_key, session_id, role, recorded_at, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      `);

      this.statements.l0FtsDelete = this.db.prepare("DELETE FROM l0_fts WHERE record_id = ?");

      this.statements.l0FtsSearch = this.db.prepare(`
        SELECT record_id, message_text_original AS message_text, session_key, session_id, role, recorded_at, timestamp,
               bm25(l0_fts) AS rank
        FROM l0_fts
        WHERE l0_fts MATCH ?
        ORDER BY rank ASC
        LIMIT ?
      `);

      this.ftsAvailable = true;
      this.logger?.info(`${TAG} FTS5 tables initialized (l1_fts, l0_fts) [schema v2 — jieba segmented]`);

      if (needsFtsRebuild) {
        this.rebuildFtsIndex();
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      this.ftsAvailable = false;
      this.logger?.warn(
        `${TAG} FTS5 tables NOT available (fts5 may not be compiled in): ${message}. ` +
        `FTS-based keyword search will be unavailable.`,
      );
    }

    // Save embedding meta
    if (providerInfo) {
      this.writeEmbeddingMeta({
        provider: providerInfo.provider,
        model: providerInfo.model,
        dimensions: this.dimensions,
      });
    }

    this.vecTablesReady = this.dimensions > 0;

    // L1 query statements
    const l1QueryCols = `record_id, content, type, priority, scene_name, session_key, session_id,
      timestamp_str, timestamp_start, timestamp_end,
      created_time, updated_time, metadata_json`;

    this.statements.l1QueryBySessionId = this.db.prepare(`
      SELECT ${l1QueryCols} FROM l1_records
      WHERE session_id = ?
      ORDER BY updated_time ASC
    `);

    this.statements.l1QueryBySessionIdSince = this.db.prepare(`
      SELECT ${l1QueryCols} FROM l1_records
      WHERE session_id = ? AND updated_time > ?
      ORDER BY updated_time ASC
    `);

    this.statements.l1QueryBySessionKey = this.db.prepare(`
      SELECT ${l1QueryCols} FROM l1_records
      WHERE session_key = ?
      ORDER BY updated_time ASC
    `);

    this.statements.l1QueryBySessionKeySince = this.db.prepare(`
      SELECT ${l1QueryCols} FROM l1_records
      WHERE session_key = ? AND updated_time > ?
      ORDER BY updated_time ASC
    `);

    this.statements.l1QueryAll = this.db.prepare(`
      SELECT ${l1QueryCols} FROM l1_records
      ORDER BY updated_time ASC
    `);

    this.statements.l1QueryAllSince = this.db.prepare(`
      SELECT ${l1QueryCols} FROM l1_records
      WHERE updated_time > ?
      ORDER BY updated_time ASC
    `);

    this.logger?.info(`${TAG} Initialized (dimensions=${this.dimensions})`);

    return { needsReindex, reason: reindexReason };
  }

  // ── Embedding meta helpers ──────────────────────────────

  readEmbeddingMeta() {
    try {
      const row = this.db
        .prepare("SELECT value FROM embedding_meta WHERE key = ?")
        .get("embedding_provider_info");
      if (!row) return null;
      return JSON.parse(row.value);
    } catch {
      return null;
    }
  }

  writeEmbeddingMeta(meta) {
    this.db.prepare(
      "INSERT INTO embedding_meta (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
    ).run("embedding_provider_info", JSON.stringify(meta));
  }

  /** Allowed table names for row counting. */
  static get COUNTABLE_TABLES() {
    return new Set(["l1_records", "l0_conversations"]);
  }

  /** Extra rows to retrieve from vec0 KNN to compensate for legacy zero-vector placeholders. */
  static get ZERO_VEC_BUFFER() {
    return 10;
  }

  /** Default result limit for FTS5 keyword searches. */
  static get FTS_DEFAULT_LIMIT() {
    return 20;
  }

  tableRowCount(table) {
    if (!VectorStore.COUNTABLE_TABLES.has(table)) {
      this.logger?.warn(`${TAG} tableRowCount: rejected unknown table name "${table}"`);
      return 0;
    }
    try {
      const row = this.db
        .prepare(`SELECT COUNT(*) AS cnt FROM ${table}`)
        .get();
      return row?.cnt ?? 0;
    } catch {
      return 0;
    }
  }

  getVecTableDimensions() {
    try {
      const row = this.db
        .prepare("SELECT sql FROM sqlite_master WHERE type='table' AND name=?")
        .get("l1_vec");
      if (!row?.sql) return null;
      const match = row.sql.match(/float\[(\d+)\]/);
      return match ? Number(match[1]) : null;
    } catch {
      return null;
    }
  }

  dropVectorTables() {
    this.db.exec("DROP TABLE IF EXISTS l1_vec");
    this.db.exec("DROP TABLE IF EXISTS l0_vec");
    this.logger?.info(`${TAG} Dropped vector tables (l1_vec, l0_vec)`);
  }

  // ── L1 operations ──────────────────────────────────

  /**
   * Write or update a memory record (metadata + vector).
   * @param {Object} record - Memory record with id, content, type, priority, scene_name, sessionKey, sessionId, timestamps, metadata, createdAt, updatedAt
   * @param {Float32Array|undefined} embedding
   * @returns {boolean}
   */
  upsert(record, embedding) {
    if (this.degraded) {
      this.logger?.warn(`${TAG} [L1-upsert] SKIPPED (degraded mode) id=${record.id}`);
      return false;
    }
    try {
      const { id: recordId, timestamps } = record;
      const tsStr = timestamps?.[0] ?? "";
      const tsStart = timestamps?.length > 0 ? timestamps.reduce((a, b) => (a < b ? a : b)) : tsStr;
      const tsEnd = timestamps?.length > 0 ? timestamps.reduce((a, b) => (a > b ? a : b)) : tsStr;

      const skipVec = !embedding || embedding.every((v) => v === 0) || !this.vecTablesReady;

      this.db.exec("BEGIN");
      try {
        this.statements.l1UpsertMeta.run(
          recordId,
          record.content,
          record.type || "",
          record.priority ?? 50,
          record.scene_name || "",
          record.sessionKey || "",
          record.sessionId || "",
          tsStr,
          tsStart,
          tsEnd,
          record.createdAt || "",
          record.updatedAt || "",
          JSON.stringify(record.metadata || {}),
        );

        if (!skipVec) {
          this.statements.l1DeleteVec.run(recordId);
          this.statements.l1InsertVec.run(recordId, Buffer.from(embedding.buffer), record.updatedAt || "");
        }

        if (this.ftsAvailable) {
          try {
            this.statements.l1FtsDelete.run(recordId);
            this.statements.l1FtsInsert.run(
              tokenizeForFts(record.content),
              record.content,
              recordId,
              record.type || "",
              record.priority ?? 50,
              record.scene_name || "",
              record.sessionKey || "",
              record.sessionId || "",
              tsStr,
              tsStart,
              tsEnd,
              JSON.stringify(record.metadata || {}),
            );
          } catch (ftsErr) {
            this.logger?.warn(
              `${TAG} [L1-upsert] FTS write failed (non-fatal) id=${recordId}: ${ftsErr instanceof Error ? ftsErr.message : String(ftsErr)}`,
            );
          }
        }

        this.db.exec("COMMIT");
      } catch (err) {
        try { this.db.exec("ROLLBACK"); } catch { /* ignore */ }
        throw err;
      }
      return true;
    } catch (err) {
      this.logger?.warn(
        `${TAG} [L1-upsert] FAILED (non-fatal) id=${record.id}: ${err instanceof Error ? err.message : String(err)}`,
      );
      return false;
    }
  }

  /**
   * Vector similarity search (cosine distance).
   * @param {Float32Array} queryEmbedding
   * @param {number} [topK=5]
   * @returns {Array<Object>}
   */
  search(queryEmbedding, topK = 5) {
    if (this.degraded || !this.vecTablesReady) {
      if (this.degraded) this.logger?.warn(`${TAG} [L1-search] SKIPPED (degraded mode)`);
      return [];
    }
    try {
      const retrieveCount = topK + VectorStore.ZERO_VEC_BUFFER;

      const rows = this.statements.l1SearchVec.all(
        Buffer.from(queryEmbedding.buffer),
        retrieveCount,
      );

      if (rows.length === 0) return [];

      const results = [];
      for (const { record_id, distance } of rows) {
        if (distance == null || Number.isNaN(distance)) {
          this.logger?.warn(
            `${TAG} [L1-search] record_id=${record_id} has null/NaN distance — skipping`,
          );
          continue;
        }

        const meta = this.statements.l1GetMeta.get(record_id);
        if (!meta) {
          this.logger?.warn(`${TAG} [L1-search] record_id=${record_id} has vector but NO metadata`);
          continue;
        }

        const score = 1.0 - distance;
        results.push({
          record_id,
          content: meta.content,
          type: meta.type,
          priority: meta.priority,
          scene_name: meta.scene_name,
          score,
          timestamp_str: meta.timestamp_str,
          timestamp_start: meta.timestamp_start,
          timestamp_end: meta.timestamp_end,
          session_key: meta.session_key,
          session_id: meta.session_id,
          metadata_json: meta.metadata_json,
        });
      }

      return results.slice(0, topK);
    } catch (err) {
      this.logger?.warn(
        `${TAG} [L1-search] FAILED (non-fatal): ${err instanceof Error ? err.message : String(err)}`,
      );
      return [];
    }
  }

  /**
   * Delete a single record.
   * @param {string} recordId
   * @returns {boolean}
   */
  delete(recordId) {
    if (this.degraded) return false;
    try {
      this.db.exec("BEGIN");
      try {
        this.statements.l1DeleteMeta.run(recordId);
        if (this.vecTablesReady) this.statements.l1DeleteVec.run(recordId);
        if (this.ftsAvailable) {
          try { this.statements.l1FtsDelete.run(recordId); } catch { /* non-fatal */ }
        }
        this.db.exec("COMMIT");
      } catch (err) {
        try { this.db.exec("ROLLBACK"); } catch { /* ignore */ }
        throw err;
      }
      return true;
    } catch (err) {
      this.logger?.warn(
        `${TAG} delete failed (non-fatal): ${err instanceof Error ? err.message : String(err)}`,
      );
      return false;
    }
  }

  /**
   * Delete multiple records.
   * @param {string[]} recordIds
   * @returns {boolean}
   */
  deleteBatch(recordIds) {
    if (this.degraded) return false;
    if (recordIds.length === 0) return true;

    try {
      this.db.exec("BEGIN");
      try {
        for (const id of recordIds) {
          this.statements.l1DeleteMeta.run(id);
          if (this.vecTablesReady) this.statements.l1DeleteVec.run(id);
          if (this.ftsAvailable) {
            try { this.statements.l1FtsDelete.run(id); } catch { /* non-fatal */ }
          }
        }
        this.db.exec("COMMIT");
      } catch (err) {
        try { this.db.exec("ROLLBACK"); } catch { /* ignore */ }
        throw err;
      }
      return true;
    } catch (err) {
      this.logger?.warn(
        `${TAG} deleteBatch failed (non-fatal): ${err instanceof Error ? err.message : String(err)}`,
      );
      return false;
    }
  }

  /**
   * TTL cleanup by updated_time.
   * @param {string} cutoffIso
   * @returns {number}
   */
  deleteL1ExpiredByUpdatedTime(cutoffIso) {
    if (this.degraded) return 0;
    try {
      const row = this.db.prepare(
        "SELECT COUNT(*) AS cnt FROM l1_records WHERE updated_time != '' AND updated_time < ?",
      ).get(cutoffIso);
      const expiredCount = row?.cnt ?? 0;
      if (expiredCount <= 0) return 0;

      this.db.exec("BEGIN");
      try {
        if (this.vecTablesReady) {
          this.db.prepare(
            "DELETE FROM l1_vec WHERE updated_time != '' AND updated_time < ?",
          ).run(cutoffIso);
        }
        this.db.prepare(
          "DELETE FROM l1_records WHERE updated_time != '' AND updated_time < ?",
        ).run(cutoffIso);
        this.db.exec("COMMIT");
        return expiredCount;
      } catch (err) {
        try { this.db.exec("ROLLBACK"); } catch { /* ignore */ }
        throw err;
      }
    } catch (err) {
      this.logger?.warn(
        `${TAG} deleteL1ExpiredByUpdatedTime failed (non-fatal): ${err instanceof Error ? err.message : String(err)}`,
      );
      return 0;
    }
  }

  /**
   * Get total L1 record count.
   * @returns {number}
   */
  count() {
    if (this.degraded) return 0;
    try {
      const row = this.db
        .prepare("SELECT COUNT(*) AS cnt FROM l1_records")
        .get();
      return row?.cnt ?? 0;
    } catch {
      return 0;
    }
  }

  /**
   * Query L1 records with optional filters.
   * @param {Object} [filter]
   * @param {string} [filter.sessionKey]
   * @param {string} [filter.sessionId]
   * @param {string} [filter.updatedAfter]
   * @returns {Array<Object>}
   */
  queryL1Records(filter) {
    if (this.degraded) return [];
    try {
      const { sessionKey, sessionId, updatedAfter } = filter || {};

      let raw;
      if (sessionId && updatedAfter) {
        raw = this.statements.l1QueryBySessionIdSince.all(sessionId, updatedAfter);
      } else if (sessionId) {
        raw = this.statements.l1QueryBySessionId.all(sessionId);
      } else if (sessionKey && updatedAfter) {
        raw = this.statements.l1QueryBySessionKeySince.all(sessionKey, updatedAfter);
      } else if (sessionKey) {
        raw = this.statements.l1QueryBySessionKey.all(sessionKey);
      } else if (updatedAfter) {
        raw = this.statements.l1QueryAllSince.all(updatedAfter);
      } else {
        raw = this.statements.l1QueryAll.all();
      }

      return raw;
    } catch (err) {
      this.logger?.warn(
        `${TAG} [L1-query] FAILED (non-fatal): ${err instanceof Error ? err.message : String(err)}`,
      );
      return [];
    }
  }

  // ── L0 operations ──────────────────────────────────

  /**
   * Write or update an L0 single-message record.
   * @param {Object} record - L0 record with id, sessionKey, sessionId, role, messageText, recordedAt, timestamp
   * @param {Float32Array|undefined} embedding
   * @returns {boolean}
   */
  upsertL0(record, embedding) {
    if (this.degraded) {
      this.logger?.warn(`${TAG} [L0-upsert] SKIPPED (degraded mode) id=${record.id}`);
      return false;
    }
    try {
      const skipVec = !embedding || embedding.every((v) => v === 0) || !this.vecTablesReady;

      this.db.exec("BEGIN");
      try {
        this.statements.l0UpsertMeta.run(
          record.id,
          record.sessionKey,
          record.sessionId || "",
          record.role,
          record.messageText,
          record.recordedAt || "",
          record.timestamp || 0,
        );

        if (!skipVec) {
          this.statements.l0DeleteVec.run(record.id);
          this.statements.l0InsertVec.run(record.id, Buffer.from(embedding.buffer), record.recordedAt || "");
        }

        if (this.ftsAvailable) {
          try {
            this.statements.l0FtsDelete.run(record.id);
            this.statements.l0FtsInsert.run(
              tokenizeForFts(record.messageText),
              record.messageText,
              record.id,
              record.sessionKey,
              record.sessionId || "",
              record.role,
              record.recordedAt || "",
              record.timestamp || 0,
            );
          } catch (ftsErr) {
            this.logger?.warn(
              `${TAG} [L0-upsert] FTS write failed (non-fatal) id=${record.id}: ${ftsErr instanceof Error ? ftsErr.message : String(ftsErr)}`,
            );
          }
        }

        this.db.exec("COMMIT");
      } catch (err) {
        try { this.db.exec("ROLLBACK"); } catch { /* ignore */ }
        throw err;
      }
      return true;
    } catch (err) {
      this.logger?.warn(
        `${TAG} [L0-upsert] FAILED (non-fatal) id=${record.id}: ${err instanceof Error ? err.message : String(err)}`,
      );
      return false;
    }
  }

  /**
   * Update ONLY the vector embedding for an existing L0 record.
   * @param {string} recordId
   * @param {Float32Array} embedding
   * @returns {boolean}
   */
  updateL0Embedding(recordId, embedding) {
    if (this.degraded || !this.vecTablesReady) return false;
    if (!embedding || embedding.every((v) => v === 0)) return false;
    try {
      const meta = this.statements.l0GetMeta.get(recordId);
      if (!meta) return false;

      this.db.exec("BEGIN");
      try {
        this.statements.l0DeleteVec.run(recordId);
        this.statements.l0InsertVec.run(recordId, Buffer.from(embedding.buffer), meta.recorded_at);
        this.db.exec("COMMIT");
      } catch (err) {
        try { this.db.exec("ROLLBACK"); } catch { /* ignore */ }
        throw err;
      }
      return true;
    } catch (err) {
      this.logger?.warn(
        `${TAG} [L0-update-embedding] FAILED (non-fatal) id=${recordId}: ${err instanceof Error ? err.message : String(err)}`,
      );
      return false;
    }
  }

  /**
   * Vector similarity search on L0.
   * @param {Float32Array} queryEmbedding
   * @param {number} [topK=5]
   * @returns {Array<Object>}
   */
  searchL0(queryEmbedding, topK = 5) {
    if (this.degraded || !this.vecTablesReady) {
      if (this.degraded) this.logger?.warn(`${TAG} [L0-search] SKIPPED (degraded mode)`);
      return [];
    }
    try {
      const retrieveCount = topK + VectorStore.ZERO_VEC_BUFFER;

      const rows = this.statements.l0SearchVec.all(
        Buffer.from(queryEmbedding.buffer),
        retrieveCount,
      );

      if (rows.length === 0) return [];

      const results = [];
      for (const { record_id, distance } of rows) {
        if (distance == null || Number.isNaN(distance)) continue;

        const meta = this.statements.l0GetMeta.get(record_id);
        if (!meta) continue;

        const score = 1.0 - distance;
        results.push({
          record_id,
          session_key: meta.session_key,
          session_id: meta.session_id,
          role: meta.role,
          message_text: meta.message_text,
          score,
          recorded_at: meta.recorded_at,
          timestamp: meta.timestamp ?? 0,
        });
      }

      return results.slice(0, topK);
    } catch (err) {
      this.logger?.warn(
        `${TAG} [L0-search] FAILED (non-fatal): ${err instanceof Error ? err.message : String(err)}`,
      );
      return [];
    }
  }

  /**
   * Delete a single L0 record.
   * @param {string} recordId
   * @returns {boolean}
   */
  deleteL0(recordId) {
    if (this.degraded) return false;
    try {
      this.db.exec("BEGIN");
      try {
        this.statements.l0DeleteMeta.run(recordId);
        if (this.vecTablesReady) this.statements.l0DeleteVec.run(recordId);
        if (this.ftsAvailable) {
          try { this.statements.l0FtsDelete.run(recordId); } catch { /* non-fatal */ }
        }
        this.db.exec("COMMIT");
      } catch (err) {
        try { this.db.exec("ROLLBACK"); } catch { /* ignore */ }
        throw err;
      }
      return true;
    } catch (err) {
      this.logger?.warn(
        `${TAG} deleteL0 failed (non-fatal): ${err instanceof Error ? err.message : String(err)}`,
      );
      return false;
    }
  }

  /**
   * TTL cleanup by recorded_at for L0 records.
   * @param {string} cutoffIso
   * @returns {number}
   */
  deleteL0ExpiredByRecordedAt(cutoffIso) {
    if (this.degraded) return 0;
    try {
      const row = this.db.prepare(
        "SELECT COUNT(*) AS cnt FROM l0_conversations WHERE recorded_at != '' AND recorded_at < ?",
      ).get(cutoffIso);
      const expiredCount = row?.cnt ?? 0;
      if (expiredCount <= 0) return 0;

      this.db.exec("BEGIN");
      try {
        if (this.vecTablesReady) {
          this.db.prepare(
            "DELETE FROM l0_vec WHERE recorded_at != '' AND recorded_at < ?",
          ).run(cutoffIso);
        }
        this.db.prepare(
          "DELETE FROM l0_conversations WHERE recorded_at != '' AND recorded_at < ?",
        ).run(cutoffIso);
        this.db.exec("COMMIT");
        return expiredCount;
      } catch (err) {
        try { this.db.exec("ROLLBACK"); } catch { /* ignore */ }
        throw err;
      }
    } catch (err) {
      this.logger?.warn(
        `${TAG} deleteL0ExpiredByRecordedAt failed (non-fatal): ${err instanceof Error ? err.message : String(err)}`,
      );
      return 0;
    }
  }

  /**
   * Get total L0 record count.
   * @returns {number}
   */
  countL0() {
    if (this.degraded) return 0;
    try {
      const row = this.db
        .prepare("SELECT COUNT(*) AS cnt FROM l0_conversations")
        .get();
      return row?.cnt ?? 0;
    } catch {
      return 0;
    }
  }

  // ── Re-index operations ──────────────────────────────────

  /**
   * Get all L1 record texts for re-embedding.
   * @returns {Array<{record_id: string, content: string, updated_time: string}>}
   */
  getAllL1Texts() {
    if (this.degraded) return [];
    try {
      return this.db
        .prepare("SELECT record_id, content, updated_time FROM l1_records")
        .all();
    } catch (err) {
      this.logger?.warn(
        `${TAG} getAllL1Texts failed (non-fatal): ${err instanceof Error ? err.message : String(err)}`,
      );
      return [];
    }
  }

  /**
   * Get all L0 message texts for re-embedding.
   * @returns {Array<{record_id: string, message_text: string, recorded_at: string}>}
   */
  getAllL0Texts() {
    if (this.degraded) return [];
    try {
      return this.db
        .prepare("SELECT record_id, message_text, recorded_at FROM l0_conversations")
        .all();
    } catch (err) {
      this.logger?.warn(
        `${TAG} getAllL0Texts failed (non-fatal): ${err instanceof Error ? err.message : String(err)}`,
      );
      return [];
    }
  }

  /**
   * Re-embed all existing L1 and L0 texts with a new embedding function.
   * @param {(text: string) => Promise<Float32Array>} embedFn
   * @param {Function} [onProgress]
   * @returns {Promise<{l1Count: number, l0Count: number}>}
   */
  async reindexAll(embedFn, onProgress) {
    if (this.degraded || !this.vecTablesReady) {
      if (this.degraded) this.logger?.warn(`${TAG} reindexAll skipped: VectorStore is in degraded mode`);
      return { l1Count: 0, l0Count: 0 };
    }

    try {
      const l1Rows = this.getAllL1Texts();
      let l1Done = 0;
      for (const { record_id, content, updated_time } of l1Rows) {
        try {
          const embedding = await embedFn(content);
          this.db.exec("BEGIN");
          try {
            this.statements.l1DeleteVec.run(record_id);
            this.statements.l1InsertVec.run(record_id, Buffer.from(embedding.buffer), updated_time);
            this.db.exec("COMMIT");
          } catch (txErr) {
            try { this.db.exec("ROLLBACK"); } catch { /* ignore */ }
            throw txErr;
          }
        } catch (err) {
          this.logger?.warn?.(
            `${TAG} reindex L1 skip ${record_id}: ${err instanceof Error ? err.message : String(err)}`,
          );
        }
        l1Done++;
        onProgress?.(l1Done, l1Rows.length, "L1");
      }

      const l0Rows = this.getAllL0Texts();
      let l0Done = 0;
      for (const { record_id, message_text, recorded_at } of l0Rows) {
        try {
          const embedding = await embedFn(message_text);
          this.db.exec("BEGIN");
          try {
            this.statements.l0DeleteVec.run(record_id);
            this.statements.l0InsertVec.run(record_id, Buffer.from(embedding.buffer), recorded_at);
            this.db.exec("COMMIT");
          } catch (txErr) {
            try { this.db.exec("ROLLBACK"); } catch { /* ignore */ }
            throw txErr;
          }
        } catch (err) {
          this.logger?.warn?.(
            `${TAG} reindex L0 skip ${record_id}: ${err instanceof Error ? err.message : String(err)}`,
          );
        }
        l0Done++;
        onProgress?.(l0Done, l0Rows.length, "L0");
      }

      this.logger?.info(
        `${TAG} Reindex complete: L1=${l1Done}/${l1Rows.length}, L0=${l0Done}/${l0Rows.length}`,
      );

      return { l1Count: l1Done, l0Count: l0Done };
    } catch (err) {
      this.logger?.error(
        `${TAG} reindexAll failed (non-fatal): ${err instanceof Error ? err.message : String(err)}`,
      );
      return { l1Count: 0, l0Count: 0 };
    }
  }

  // ── L0 query operations (for L1 runner) ──────────────────────────────────

  /**
   * Query L0 messages for a given session key.
   * Returns messages ordered by timestamp ASC (chronological).
   * @param {string} sessionKey
   * @param {number} [afterTimestamp]
   * @param {number} [limit=50]
   * @returns {Array<Object>}
   */
  queryL0ForL1(sessionKey, afterTimestamp, limit = 50) {
    if (this.degraded) return [];
    try {
      let rows;
      if (afterTimestamp && afterTimestamp > 0) {
        rows = this.statements.l0QueryAfter.all(sessionKey, afterTimestamp, limit);
      } else {
        rows = this.statements.l0QueryAll.all(sessionKey, limit);
      }

      // Reverse: SQL returns newest-first (DESC), callers expect chronological order
      return rows.map((r) => ({
        record_id: r.record_id,
        session_key: r.session_key,
        session_id: r.session_id || "",
        role: r.role,
        message_text: r.message_text,
        recorded_at: r.recorded_at || "",
        timestamp: r.timestamp || 0,
      })).reverse();
    } catch (err) {
      this.logger?.warn(
        `${TAG} [L0-query] FAILED (non-fatal): ${err instanceof Error ? err.message : String(err)}`,
      );
      return [];
    }
  }

  /**
   * Query L0 messages grouped by session_id.
   * @param {string} sessionKey
   * @param {number} [afterTimestamp]
   * @param {number} [limit=50]
   * @returns {Array<{sessionId: string, messages: Array}>}
   */
  queryL0GroupedBySessionId(sessionKey, afterTimestamp, limit = 50) {
    if (this.degraded) return [];
    try {
      const rows = this.queryL0ForL1(sessionKey, afterTimestamp, limit);

      const groupMap = new Map();
      for (const row of rows) {
        const sid = row.session_id || "";
        let group = groupMap.get(sid);
        if (!group) {
          group = [];
          groupMap.set(sid, group);
        }
        group.push({
          id: row.record_id,
          role: row.role,
          content: row.message_text,
          timestamp: row.timestamp,
        });
      }

      const groups = [];
      for (const [sessionId, messages] of groupMap) {
        if (messages.length > 0) {
          groups.push({ sessionId, messages });
        }
      }
      groups.sort((a, b) => a.messages[0].timestamp - b.messages[0].timestamp);

      return groups;
    } catch (err) {
      this.logger?.warn(
        `${TAG} [L0-query-grouped] FAILED (non-fatal): ${err instanceof Error ? err.message : String(err)}`,
      );
      return [];
    }
  }

  // ── FTS5 search operations ──────────────────────────────────

  /**
   * Whether FTS5 full-text search is available.
   */
  isFtsAvailable() {
    return this.ftsAvailable;
  }

  /**
   * FTS5 keyword search on L1 records.
   * @param {string} ftsQuery
   * @param {number} [limit=20]
   * @returns {Array<Object>}
   */
  ftsSearchL1(ftsQuery, limit = 20) {
    if (this.degraded || !this.ftsAvailable) return [];
    try {
      const rows = this.statements.l1FtsSearch.all(ftsQuery, limit);
      return rows.map((r) => ({
        record_id: r.record_id,
        content: r.content,
        type: r.type,
        priority: r.priority,
        scene_name: r.scene_name,
        score: bm25RankToScore(r.rank),
        timestamp_str: r.timestamp_str,
        timestamp_start: r.timestamp_start,
        timestamp_end: r.timestamp_end,
        session_key: r.session_key,
        session_id: r.session_id,
        metadata_json: r.metadata_json,
      }));
    } catch (err) {
      this.logger?.warn(
        `${TAG} [L1-fts-search] FAILED (non-fatal): ${err instanceof Error ? err.message : String(err)}`,
      );
      return [];
    }
  }

  /**
   * FTS5 keyword search on L0 conversation messages.
   * @param {string} ftsQuery
   * @param {number} [limit]
   * @returns {Array<Object>}
   */
  ftsSearchL0(ftsQuery, limit = VectorStore.FTS_DEFAULT_LIMIT) {
    if (this.degraded || !this.ftsAvailable) return [];
    try {
      const rows = this.statements.l0FtsSearch.all(ftsQuery, limit);
      return rows.map((r) => ({
        record_id: r.record_id,
        session_key: r.session_key,
        session_id: r.session_id,
        role: r.role,
        message_text: r.message_text,
        score: bm25RankToScore(r.rank),
        recorded_at: r.recorded_at,
        timestamp: r.timestamp ?? 0,
      }));
    } catch (err) {
      this.logger?.warn(
        `${TAG} [L0-fts-search] FAILED (non-fatal): ${err instanceof Error ? err.message : String(err)}`,
      );
      return [];
    }
  }

  // ── FTS5 migration & rebuild ──────────────────────────────────

  /**
   * Detect old FTS5 v1 schema and drop tables for v2 recreation.
   * @returns {boolean} true if migration was performed
   */
  migrateFtsTablesIfNeeded() {
    try {
      const l1Exists = this.db
        .prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name='l1_fts'")
        .get();
      if (!l1Exists) {
        const hasData = this.db.prepare("SELECT 1 FROM l1_records LIMIT 1").get();
        return !!hasData;
      }

      const cols = this.db
        .prepare("SELECT name FROM pragma_table_info('l1_fts')")
        .all();
      const hasV2Col = cols.some((c) => c.name === "content_original");

      if (hasV2Col) return false;

      this.logger?.info(`${TAG} Migrating FTS5 tables from v1 to v2 (jieba segmented)`);
      this.db.exec("DROP TABLE IF EXISTS l1_fts");
      this.db.exec("DROP TABLE IF EXISTS l0_fts");
      return true;
    } catch (err) {
      this.logger?.warn(
        `${TAG} FTS migration check failed (non-fatal): ${err instanceof Error ? err.message : String(err)}`,
      );
      return false;
    }
  }

  /**
   * Rebuild the FTS5 index from scratch.
   */
  rebuildFtsIndex() {
    if (!this.ftsAvailable) return;

    try {
      this.logger?.info(`${TAG} Rebuilding FTS5 index with jieba segmentation…`);

      this.db.exec("DELETE FROM l1_fts");

      const l1Rows = this.db
        .prepare(`
          SELECT record_id, content, type, priority, scene_name,
                 session_key, session_id, timestamp_str, timestamp_start, timestamp_end, metadata_json
          FROM l1_records
        `)
        .all();

      let l1Count = 0;
      for (const r of l1Rows) {
        try {
          this.statements.l1FtsInsert.run(
            tokenizeForFts(r.content),
            r.content,
            r.record_id,
            r.type,
            r.priority,
            r.scene_name,
            r.session_key,
            r.session_id,
            r.timestamp_str,
            r.timestamp_start,
            r.timestamp_end,
            r.metadata_json,
          );
          l1Count++;
        } catch (err) {
          this.logger?.warn?.(
            `${TAG} FTS rebuild skip L1 ${r.record_id}: ${err instanceof Error ? err.message : String(err)}`,
          );
        }
      }

      this.db.exec("DELETE FROM l0_fts");

      const l0Rows = this.db
        .prepare(`
          SELECT record_id, message_text, session_key, session_id, role, recorded_at, timestamp
          FROM l0_conversations
        `)
        .all();

      let l0Count = 0;
      for (const r of l0Rows) {
        try {
          this.statements.l0FtsInsert.run(
            tokenizeForFts(r.message_text),
            r.message_text,
            r.record_id,
            r.session_key,
            r.session_id,
            r.role,
            r.recorded_at,
            r.timestamp,
          );
          l0Count++;
        } catch (err) {
          this.logger?.warn?.(
            `${TAG} FTS rebuild skip L0 ${r.record_id}: ${err instanceof Error ? err.message : String(err)}`,
          );
        }
      }

      this.logger?.info(
        `${TAG} FTS5 rebuild complete: L1=${l1Count}/${l1Rows.length}, L0=${l0Count}/${l0Rows.length}`,
      );
    } catch (err) {
      this.logger?.warn(
        `${TAG} FTS5 rebuild failed (non-fatal): ${err instanceof Error ? err.message : String(err)}`,
      );
    }
  }

  /**
   * Close the database connection.
   */
  close() {
    if (this.closed) return;
    this.closed = true;
    try {
      this.db.close();
      this.logger?.info(`${TAG} Database closed`);
    } catch (err) {
      this.logger?.warn?.(
        `${TAG} Error closing database: ${err instanceof Error ? err.message : String(err)}`,
      );
    }
  }
}

