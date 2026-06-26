/**
 * LanceDB Vector Store - v4.0 (LanceDB 0.27 compatible)
 *
 * Key fixes for LanceDB 0.27:
 * - query().execute() returns AsyncGenerator yielding Arrow IPC Tables
 * - Need to parse Arrow batches to get row data
 * - WHERE clause is broken (use in-memory filtering)
 * - LanceDB v0.27 schema inference issue: store vectors as base64 strings
 *
 * Architecture:
 * - LanceDB for persistent columnar storage
 * - Vectors cached in memory as Float32Array for fast JS-based ANN
 * - Ollama HTTP API for embeddings
 */

import { connect } from '@lancedb/lancedb';
import { dirname, join } from 'path';
import { existsSync, mkdirSync } from 'fs';
import { fileURLToPath } from 'url';
import { embedCache } from './embed_cache.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const VECTOR_DB_DIR = join(process.env.HOME || '/root', '.unified-memory', 'vector.lance');
const TABLE_NAME = 'memories';
const DIMENSIONS = 768;

// ── Embedding via config-active provider ──────────────────────
// P2-3: Check text-hash embedding cache before calling Ollama
async function getEmbeddingFromProvider(text) {
  // P2-3: check text-hash cache first
  const cached = embedCache.get(text);
  if (cached) return cached;

  const { config } = await import('./config.js');
  const p = config.activeEmbedProvider;
  if (!p) return null; // VECTOR_ENGINE=none

  let embedding = null;
  try {
    const res = await fetch(`${p.baseURL}/api/embed`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: p.model, input: text }),
      signal: AbortSignal.timeout(15000),
    });
    if (!res.ok) return null;
    const data = await res.json();
    embedding = data.embeddings?.[0] || data.embedding || null;
    if (embedding) {
      // P2-3: store in text-hash cache for future lookups
      try { embedCache.set(text, embedding); } catch (_) { /* cache full, non-fatal */ }
    }
    return embedding;
  } catch (e) {
    console.warn(`[vector_lancedb] Embed error (${p.name}):`, e.message);
    return null;
  }
}

// Backward compat alias (used by fusion.js)
const ollamaEmbed = getEmbeddingFromProvider;
export { ollamaEmbed as getEmbedding };

// ── Vector <-> Base64 encoding (for LanceDB storage without Float32 type issues) ──
function vecToBase64(vec) {
  const buf = Buffer.alloc(vec.length * 4);
  for (let i = 0; i < vec.length; i++) buf.writeFloatLE(vec[i], i * 4);
  return buf.toString('base64');
}

function base64ToVec(b64) {
  if (!b64) return null;
  try {
    const buf = Buffer.from(b64, 'base64');
    const vec = new Float32Array(buf.length / 4);
    for (let i = 0; i < vec.length; i++) vec[i] = buf.readFloatLE(i * 4);
    return vec;
  } catch { return null; }
}

function cosineSim(a, b) {
  let dot = 0, na = 0, nb = 0;
  for (let i = 0; i < a.length; i++) { dot += a[i] * b[i]; na += a[i] * a[i]; nb += b[i] * b[i]; }
  return dot / (Math.sqrt(na) * Math.sqrt(nb) + 1e-10);
}

// ── LanceDB 0.27: parse Arrow batches into row objects ──────────────
/**
 * Execute a query and return all rows as plain objects.
 * Handles LanceDB 0.27's AsyncGenerator yielding Arrow IPC Tables.
 */
async function queryRows(table, limit = 10000) {
  const results = [];
  try {
    for await (const batch of table.query().limit(limit).execute()) {
      // batch is an Arrow IPC Table
      const schema = batch.schema;
      const colNames = schema?.fields?.map(f => f.name) || [];
      const rows = batch.numRows;
      for (let i = 0; i < rows; i++) {
        const row = {};
        for (let c = 0; c < batch.numCols; c++) {
          const col = batch.getChildAt(c);
          const name = colNames[c] || `col_${c}`;
          row[name] = col?.get?.(i) ?? null;
        }
        results.push(row);
      }
    }
  } catch (e) {
    console.warn('[vector_lancedb] queryRows error:', e.message);
  }
  return results;
}

// 优化的查询函数，支持过滤
async function queryRowsWithFilter(table, filter = null, limit = 10000) {
  const results = [];
  try {
    // 构建查询
    let query = table.query();
    
    // 注意：LanceDB 0.27 的 WHERE 子句有 bug，所以我们先获取所有数据
    // 然后在内存中过滤
    for await (const batch of query.limit(limit).execute()) {
      const schema = batch.schema;
      const colNames = schema?.fields?.map(f => f.name) || [];
      const rows = batch.numRows;
      
      for (let i = 0; i < rows; i++) {
        const row = {};
        for (let c = 0; c < batch.numCols; c++) {
          const col = batch.getChildAt(c);
          const name = colNames[c] || `col_${c}`;
          row[name] = col?.get?.(i) ?? null;
        }
        
        // 应用内存过滤
        if (!filter || passesFilter(row, filter)) {
          results.push(row);
        }
      }
    }
  } catch (e) {
    console.warn('[vector_lancedb] queryRowsWithFilter error:', e.message);
  }
  return results;
}

// 过滤函数
function passesFilter(row, filter) {
  if (!filter) return true;
  
  if (typeof filter === 'function') {
    return filter(row);
  }
  
  if (typeof filter === 'object') {
    // 支持简单的对象过滤
    for (const [key, value] of Object.entries(filter)) {
      if (row[key] !== value) {
        return false;
      }
    }
    return true;
  }
  
  return true;
}

// ── VectorMemory ─────────────────────────────────────────────────
export class VectorMemory {
  constructor(uri = VECTOR_DB_DIR) {
    this.uri = uri;
    this._db = null;
    this._table = null;
    this._initialized = false;
    // In-memory cache: id → Float32Array vector
    this._cache = {};
  }

  async initialize() {
    if (this._initialized) return;
    if (!existsSync(this.uri)) mkdirSync(this.uri, { recursive: true });

    this._db = await connect(this.uri);
    const tableNames = await this._db.tableNames();

    if (!tableNames.includes(TABLE_NAME)) {
      // Create table with base64-encoded vector strings
      this._table = await this._db.createTable(TABLE_NAME, [
        { id: '__init__', text: '__init__', category: 'general', scope: 'USER', importance: 0.0, created_at: Date.now(), vec_json: '' },
      ]);
      await this._table.delete('id = "__init__"');
    } else {
      this._table = await this._db.openTable(TABLE_NAME);
    }

    // Pre-load all vectors into memory cache
    await this._refreshCache();
    this._initialized = true;
    console.log(`[vector_lancedb] Ready at ${this.uri} (${Object.keys(this._cache).length} records cached)`);
  }

  async _refreshCache() {
    this._cache = {};
    const rows = await queryRows(this._table);
    for (const row of rows) {
      if (row.vec_json) {
        const vec = base64ToVec(row.vec_json);
        if (vec) this._cache[row.id] = vec;
      }
    }
  }

  /** Add or update a memory record */
  async upsert({ id, text, category = 'general', scope = 'USER', importance = 0.5, created_at: ca }) {
    await this.initialize();
    const embedding = await ollamaEmbed(text);
    if (!embedding) throw new Error('Ollama embedding failed for: ' + text.slice(0, 30));
    const vecB64 = vecToBase64(embedding);
    const createdMs = ca ? (typeof ca === 'number' ? ca : new Date(ca).getTime()) : Date.now();

    try { await this._table.delete(`id = "${id}"`); } catch { /* ignore */ }
    await this._table.add([{ id, text, category, scope, importance, created_at: createdMs, vec_json: vecB64 }]);
    this._cache[id] = embedding;
    // Sync embedding back to JSON so health check sees it (fixes dual-storage consistency bug)
    try {
      const { getAllMemories, updateMemory } = await import('./storage.js');
      const memories = await getAllMemories();
      const mem = memories.find(m => m.id === id);
      if (mem) updateMemory({ id, embedding: vecB64 });
    } catch { /* non-fatal: JSON may be locked or in use */ }
    return id;
  }

  /** Delete by id */
  async delete(id) {
    await this.initialize();
    try { await this._table.delete(`id = "${id}"`); } catch { /* ignore */ }
    delete this._cache[id];
  }

  /** ANN search using in-memory cosine similarity with optimized filtering */
  async search(query, topK = 10, scope = null) {
    await this.initialize();
    const qEmb = await ollamaEmbed(query);
    if (!qEmb) return [];

    // 构建过滤条件
    const filter = scope ? { scope } : null;
    
    // 获取所有行（带过滤）
    const allRows = await queryRowsWithFilter(this._table, filter);
    
    // 计算相似度
    const scored = [];
    for (const row of allRows) {
      const id = row.id;
      const vec = this._cache[id];
      if (vec) {
        const score = cosineSim(qEmb, vec);
        scored.push({ id, score, row });
      }
    }

    // 排序并取前 topK
    scored.sort((a, b) => b.score - a.score);
    const topResults = scored.slice(0, topK);

    return topResults.map(result => ({
      id: result.id,
      text: result.row.text,
      score: result.score,
      metadata: {
        category: result.row.category,
        scope: result.row.scope,
        importance: result.row.importance,
        created_at: result.row.created_at,
      },
    }));
  }

  async count() { return Object.keys(this._cache).length; }
}

// ── Singleton ──────────────────────────────────────────────────
let _instance = null;
export function getVectorStore() {
  if (!_instance) _instance = new VectorMemory();
  return _instance;
}

// ── Compatibility layer ─────────────────────────────────────────
// getEmbedding is exported via the export {} statement above

export async function vectorSearch(query, topK = 10, scope = null) {
  const store = getVectorStore();
  const results = await store.search(query, topK, scope);
  return results.map(r => ({
    memory: {
      id: r.id, text: r.text,
      category: r.metadata.category, scope: r.metadata.scope,
      importance: r.metadata.importance, created_at: r.metadata.created_at,
    },
    score: r.score,
    highlight: (r.text || '').slice(0, 150),
  }));
}
