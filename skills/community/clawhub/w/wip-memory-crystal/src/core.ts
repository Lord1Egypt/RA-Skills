// memory-crystal/core.ts — Pure logic layer. Zero framework dependencies.
// Hybrid search: sqlite-vec (vectors) + FTS5 (BM25) + RRF fusion + recency.
// Dual-writes to LanceDB (safety net) and sqlite-vec (source of truth).
// Search algorithms ported from QMD (MIT, Tobi Lutke, 2024-2026).
// Config via function params, not globals. Errors: throw, callers catch.

import * as lancedb from '@lancedb/lancedb';
import Database from 'better-sqlite3';
import * as sqliteVec from 'sqlite-vec';
import { readFileSync, existsSync, mkdirSync, readdirSync, statSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { join, relative, extname, basename } from 'node:path';
import { createHash } from 'node:crypto';
import http from 'node:http';
import https from 'node:https';

// ─── Types ─────────────────────────────────────────────────────────────────

export interface CrystalConfig {
  /** Root directory for all crystal data */
  dataDir: string;
  /** Embedding provider: 'openai' | 'ollama' | 'google' */
  embeddingProvider: 'openai' | 'ollama' | 'google';
  /** OpenAI API key (required if provider is 'openai') */
  openaiApiKey?: string;
  /** OpenAI embedding model (default: text-embedding-3-small) */
  openaiModel?: string;
  /** Ollama host (default: http://localhost:11434) */
  ollamaHost?: string;
  /** Ollama model (default: nomic-embed-text) */
  ollamaModel?: string;
  /** Google API key (required if provider is 'google') */
  googleApiKey?: string;
  /** Google embedding model (default: text-embedding-004) */
  googleModel?: string;
  /** Remote Worker URL for cloud mirror mode */
  remoteUrl?: string;
  /** Remote auth token */
  remoteToken?: string;
}

export interface Chunk {
  id?: number;
  text: string;
  embedding?: number[];
  role: 'user' | 'assistant' | 'system';
  source_type: string;         // 'conversation' | 'file' | 'imessage' | 'manual'
  source_id: string;           // session key, file path, etc.
  agent_id: string;            // 'main' (Lēsa), 'claude-code', etc.
  token_count: number;
  created_at: string;          // ISO timestamp
  model_id?: string;           // model that generated this chunk
}

/** Pre-embedded chunk for delta sync. Includes embedding vector so Nodes don't re-embed. */
export interface ExportedChunk {
  id: number;
  text: string;
  text_hash: string;
  role: string;
  source_type: string;
  source_id: string;
  agent_id: string;
  token_count: number;
  created_at: string;
  embedding: number[] | null;
  model_id: string | null;
}

export interface Memory {
  id?: number;
  text: string;
  embedding?: number[];
  category: 'fact' | 'preference' | 'event' | 'opinion' | 'skill' | 'user' | 'feedback' | 'project' | 'reference';
  confidence: number;          // 0-1, decays over time
  source_ids: string;          // JSON array of chunk IDs
  status: 'active' | 'deprecated' | 'deleted';
  created_at: string;
  updated_at: string;
}

export interface SearchResult {
  text: string;
  role: string;
  score: number;
  source_type: string;
  source_id: string;
  agent_id: string;
  created_at: string;
  freshness?: "fresh" | "recent" | "aging" | "stale";
}

/** Pre-expanded query for unified search API. Skip LLM expansion when you know what you want. */
export interface StructuredQuery {
  type: 'lex' | 'vec' | 'hyde';
  text: string;
}

export interface CrystalStatus {
  chunks: number;
  memories: number;
  sources: number;
  agents: string[];
  oldestChunk: string | null;
  newestChunk: string | null;
  embeddingProvider: string;
  dataDir: string;
  capturedSessions: number;
  latestCapture: string | null;
}

// ─── Source Indexing Types (optional feature) ─────────────────────────────

export interface SourceCollection {
  id?: number;
  name: string;
  root_path: string;
  glob_patterns: string;     // JSON array of include globs
  ignore_patterns: string;   // JSON array of ignore globs
  file_count: number;
  chunk_count: number;
  last_sync_at: string | null;
  created_at: string;
}

export interface SourceFile {
  id?: number;
  collection_id: number;
  file_path: string;         // relative to collection root
  file_hash: string;         // SHA-256 of content
  file_size: number;
  chunk_count: number;
  last_indexed_at: string;
}

export interface SourcesStatus {
  collections: Array<{
    name: string;
    root_path: string;
    file_count: number;
    chunk_count: number;
    last_sync_at: string | null;
  }>;
  total_files: number;
  total_chunks: number;
}

export interface SyncResult {
  collection: string;
  added: number;
  updated: number;
  removed: number;
  chunks_added: number;
  duration_ms: number;
}

// ─── Embedding Providers ───────────────────────────────────────────────────

async function embedOpenAI(texts: string[], apiKey: string, model: string): Promise<number[][]> {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({ input: texts, model });
    const req = https.request({
      hostname: 'api.openai.com',
      path: '/v1/embeddings',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'Content-Length': Buffer.byteLength(body),
      },
      timeout: 30000,
    }, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        if (res.statusCode !== 200) {
          reject(new Error(`OpenAI API error ${res.statusCode}: ${data.slice(0, 200)}`));
          return;
        }
        const parsed = JSON.parse(data);
        resolve(parsed.data.map((d: any) => d.embedding));
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('OpenAI timeout')); });
    req.write(body);
    req.end();
  });
}

async function embedOllama(texts: string[], host: string, model: string): Promise<number[][]> {
  const results: number[][] = [];
  for (const text of texts) {
    const result = await new Promise<number[]>((resolve, reject) => {
      const url = new URL('/api/embeddings', host);
      const body = JSON.stringify({ model, prompt: text });
      const req = http.request({
        hostname: url.hostname,
        port: url.port,
        path: url.pathname,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(body),
        },
        timeout: 15000,
      }, (res) => {
        let data = '';
        res.on('data', (chunk) => data += chunk);
        res.on('end', () => {
          if (res.statusCode !== 200) {
            reject(new Error(`Ollama error ${res.statusCode}: ${data.slice(0, 200)}`));
            return;
          }
          resolve(JSON.parse(data).embedding);
        });
      });
      req.on('error', reject);
      req.on('timeout', () => { req.destroy(); reject(new Error('Ollama timeout')); });
      req.write(body);
      req.end();
    });
    results.push(result);
  }
  return results;
}

async function embedGoogle(texts: string[], apiKey: string, model: string): Promise<number[][]> {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      requests: texts.map(text => ({ model: `models/${model}`, content: { parts: [{ text }] } })),
    });
    const req = https.request({
      hostname: 'generativelanguage.googleapis.com',
      path: `/v1beta/models/${model}:batchEmbedContents?key=${apiKey}`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
      timeout: 30000,
    }, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        if (res.statusCode !== 200) {
          reject(new Error(`Google API error ${res.statusCode}: ${data.slice(0, 200)}`));
          return;
        }
        const parsed = JSON.parse(data);
        resolve(parsed.embeddings.map((e: any) => e.values));
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Google timeout')); });
    req.write(body);
    req.end();
  });
}

// ─── Crystal Core ──────────────────────────────────────────────────────────

export class Crystal {
  private config: CrystalConfig;
  private lanceDb: lancedb.Connection | null = null;
  private sqliteDb: Database.Database | null = null;
  private chunksTable: lancedb.Table | null = null;
  private vecDimensions: number | null = null;

  constructor(config: CrystalConfig) {
    this.config = config;
    if (!existsSync(config.dataDir)) {
      mkdirSync(config.dataDir, { recursive: true });
    }
  }

  // ── Initialization ──

  async init(): Promise<void> {
    const lanceDir = join(this.config.dataDir, 'lance');
    const sqlitePath = join(this.config.dataDir, 'crystal.db');

    if (!existsSync(lanceDir)) mkdirSync(lanceDir, { recursive: true });

    this.lanceDb = await lancedb.connect(lanceDir);
    this.sqliteDb = new Database(sqlitePath);
    this.sqliteDb.pragma('journal_mode = WAL');

    // Load sqlite-vec extension for vector search
    sqliteVec.load(this.sqliteDb);

    this.initSqliteTables();
    this.initChunksTables();
    await this.initLanceTables();
  }

  private initSqliteTables(): void {
    const db = this.sqliteDb!;

    db.exec(`
      CREATE TABLE IF NOT EXISTS sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        uri TEXT NOT NULL,
        title TEXT,
        agent_id TEXT NOT NULL,
        metadata TEXT DEFAULT '{}',
        ingested_at TEXT NOT NULL,
        chunk_count INTEGER DEFAULT 0
      );

      CREATE TABLE IF NOT EXISTS capture_state (
        agent_id TEXT NOT NULL,
        source_id TEXT NOT NULL,
        last_message_count INTEGER DEFAULT 0,
        capture_count INTEGER DEFAULT 0,
        last_capture_at TEXT,
        PRIMARY KEY (agent_id, source_id)
      );

      CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        category TEXT NOT NULL DEFAULT 'fact',
        confidence REAL NOT NULL DEFAULT 1.0,
        source_ids TEXT DEFAULT '[]',
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS entities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        type TEXT NOT NULL DEFAULT 'concept',
        description TEXT,
        properties TEXT DEFAULT '{}',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id INTEGER NOT NULL REFERENCES entities(id),
        target_id INTEGER NOT NULL REFERENCES entities(id),
        type TEXT NOT NULL,
        description TEXT,
        weight REAL DEFAULT 1.0,
        valid_from TEXT NOT NULL,
        valid_until TEXT,
        created_at TEXT NOT NULL
      );

      CREATE INDEX IF NOT EXISTS idx_sources_agent ON sources(agent_id);
      CREATE INDEX IF NOT EXISTS idx_memories_status ON memories(status);
      CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name);
      CREATE INDEX IF NOT EXISTS idx_relationships_source ON relationships(source_id);
      CREATE INDEX IF NOT EXISTS idx_relationships_target ON relationships(target_id);

      -- LLM cache (persistent expansion + reranking results)
      CREATE TABLE IF NOT EXISTS llm_cache (
        cache_key TEXT PRIMARY KEY,
        cache_type TEXT NOT NULL,
        query TEXT NOT NULL,
        intent TEXT,
        result TEXT NOT NULL,
        provider TEXT NOT NULL,
        created_at TEXT NOT NULL,
        hit_count INTEGER DEFAULT 0,
        last_hit_at TEXT
      );
      CREATE INDEX IF NOT EXISTS idx_llm_cache_type ON llm_cache(cache_type);
      CREATE INDEX IF NOT EXISTS idx_llm_cache_created ON llm_cache(created_at);

      -- Source file indexing (optional feature)
      CREATE TABLE IF NOT EXISTS source_collections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        root_path TEXT NOT NULL,
        glob_patterns TEXT NOT NULL DEFAULT '["**/*"]',
        ignore_patterns TEXT NOT NULL DEFAULT '[]',
        file_count INTEGER DEFAULT 0,
        chunk_count INTEGER DEFAULT 0,
        last_sync_at TEXT,
        created_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS source_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        collection_id INTEGER NOT NULL REFERENCES source_collections(id) ON DELETE CASCADE,
        file_path TEXT NOT NULL,
        file_hash TEXT NOT NULL,
        file_size INTEGER NOT NULL,
        chunk_count INTEGER DEFAULT 0,
        last_indexed_at TEXT NOT NULL
      );

      CREATE UNIQUE INDEX IF NOT EXISTS idx_source_files_path ON source_files(collection_id, file_path);
      CREATE INDEX IF NOT EXISTS idx_source_files_collection ON source_files(collection_id);
    `);
  }

  private initChunksTables(): void {
    const db = this.sqliteDb!;

    // Chunks table: text + metadata (replaces LanceDB for search reads)
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
        created_at TEXT NOT NULL,
        model_id TEXT
      );

      CREATE INDEX IF NOT EXISTS idx_chunks_agent ON chunks(agent_id);
      CREATE INDEX IF NOT EXISTS idx_chunks_source ON chunks(source_type);
      CREATE INDEX IF NOT EXISTS idx_chunks_hash ON chunks(text_hash);
      CREATE INDEX IF NOT EXISTS idx_chunks_created ON chunks(created_at);

      -- FTS5 full-text search table
      CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
        text,
        tokenize='porter unicode61'
      );

      -- Sync trigger: populate FTS on chunk insert
      CREATE TRIGGER IF NOT EXISTS chunks_fts_insert AFTER INSERT ON chunks
      BEGIN
        INSERT INTO chunks_fts(rowid, text) VALUES (NEW.id, NEW.text);
      END;

      -- Sync trigger: clean up FTS and vec on chunk delete
      CREATE TRIGGER IF NOT EXISTS chunks_cleanup AFTER DELETE ON chunks
      BEGIN
        DELETE FROM chunks_vec WHERE chunk_id = OLD.id;
        INSERT INTO chunks_fts(chunks_fts, rowid, text) VALUES('delete', OLD.id, OLD.text);
      END;
    `);

    // Backward-compat: add model_id to pre-existing chunks tables.
    try { db.exec('ALTER TABLE chunks ADD COLUMN model_id TEXT'); } catch {}

    // Check if chunks_vec exists and get its dimensions
    const vecTable = db.prepare(
      `SELECT name FROM sqlite_master WHERE type='table' AND name='chunks_vec'`
    ).get() as any;

    if (vecTable) {
      // Vec table exists, figure out its dimensions from existing data
      try {
        const row = db.prepare('SELECT embedding FROM chunks_vec LIMIT 1').get() as any;
        if (row?.embedding) {
          // Float32Array: 4 bytes per dimension
          this.vecDimensions = (row.embedding as Buffer).length / 4;
        }
      } catch {
        // Empty table or error, dimensions will be set on first ingest
      }
    }
  }

  private ensureVecTable(dimensions: number): void {
    const db = this.sqliteDb!;
    const existing = db.prepare(
      `SELECT name FROM sqlite_master WHERE type='table' AND name='chunks_vec'`
    ).get();

    if (!existing) {
      db.exec(`
        CREATE VIRTUAL TABLE chunks_vec USING vec0(
          chunk_id INTEGER PRIMARY KEY,
          embedding float[${dimensions}] distance_metric=cosine
        );
      `);
    }
    this.vecDimensions = dimensions;
  }

  private async initLanceTables(): Promise<void> {
    const db = this.lanceDb!;
    const tableNames = await db.tableNames();

    if (tableNames.includes('chunks')) {
      this.chunksTable = await db.openTable('chunks');
    }
    // Table created on first ingest (needs embedding dimensions)
  }

  // ── Embedding ──

  async embed(texts: string[]): Promise<number[][]> {
    if (texts.length === 0) return [];
    const cfg = this.config;

    switch (cfg.embeddingProvider) {
      case 'openai': {
        if (!cfg.openaiApiKey) throw new Error('OpenAI API key required');
        const model = cfg.openaiModel || 'text-embedding-3-small';
        // OpenAI has a 300K token limit per request. Sub-batch to stay safe.
        // ~4 chars per token, cap at ~200K tokens (~800K chars) per batch.
        const maxCharsPerBatch = 800000;
        const results: number[][] = [];
        let batch: string[] = [];
        let batchChars = 0;

        for (const text of texts) {
          if (batchChars + text.length > maxCharsPerBatch && batch.length > 0) {
            results.push(...await embedOpenAI(batch, cfg.openaiApiKey!, model));
            batch = [];
            batchChars = 0;
          }
          batch.push(text);
          batchChars += text.length;
        }
        if (batch.length > 0) {
          results.push(...await embedOpenAI(batch, cfg.openaiApiKey!, model));
        }
        return results;
      }

      case 'ollama':
        return embedOllama(texts, cfg.ollamaHost || 'http://localhost:11434', cfg.ollamaModel || 'nomic-embed-text');

      case 'google':
        if (!cfg.googleApiKey) throw new Error('Google API key required');
        return embedGoogle(texts, cfg.googleApiKey, cfg.googleModel || 'text-embedding-004');

      default:
        throw new Error(`Unknown embedding provider: ${cfg.embeddingProvider}`);
    }
  }

  // ── Chunking ──

  chunkText(text: string, targetTokens = 400, overlapTokens = 80): string[] {
    const targetChars = targetTokens * 4;
    const overlapChars = overlapTokens * 4;
    const chunks: string[] = [];
    let start = 0;

    while (start < text.length) {
      let end = Math.min(start + targetChars, text.length);

      if (end < text.length) {
        // Try paragraph boundary first
        const minBreak = start + Math.floor(targetChars * 0.5);
        const paraBreak = text.lastIndexOf('\n\n', end);
        if (paraBreak > minBreak) {
          end = paraBreak;
        } else {
          // Try sentence boundary
          const sentBreak = text.lastIndexOf('. ', end);
          if (sentBreak > minBreak) {
            end = sentBreak + 1;
          }
        }
      }

      const chunk = text.slice(start, end).trim();
      if (chunk.length > 0) chunks.push(chunk);

      if (end >= text.length) break;
      start = end - overlapChars;
      if (start <= (chunks.length > 0 ? end - targetChars : 0)) {
        start = end;
      }
    }

    return chunks;
  }

  // ── Ingest ──

  async ingest(chunks: Chunk[]): Promise<number> {
    if (chunks.length === 0) return 0;
    const db = this.sqliteDb!;

    // 1. Dedup: skip chunks whose text already exists (by SHA-256 hash)
    const newChunks = chunks.filter(c => {
      const hash = createHash('sha256').update(c.text).digest('hex');
      return !db.prepare('SELECT 1 FROM chunks WHERE text_hash = ?').get(hash);
    });

    if (newChunks.length === 0) return 0;

    // 2. Embed
    const texts = newChunks.map(c => c.text);
    const embeddings = await this.embed(texts);

    // 3. Ensure vec table exists (lazy... needs dimensions from first embedding)
    if (!this.vecDimensions && embeddings.length > 0) {
      this.ensureVecTable(embeddings[0].length);
    }

    // 4. Write to sqlite-vec (chunks table trigger populates FTS automatically)
    const insertChunk = db.prepare(`
      INSERT INTO chunks (text, text_hash, role, source_type, source_id, agent_id, token_count, created_at, model_id)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);
    const insertVec = db.prepare(`
      INSERT INTO chunks_vec (chunk_id, embedding) VALUES (?, ?)
    `);

    const transaction = db.transaction(() => {
      for (let i = 0; i < newChunks.length; i++) {
        const c = newChunks[i];
        const hash = createHash('sha256').update(c.text).digest('hex');
        const result = insertChunk.run(
          c.text, hash, c.role, c.source_type, c.source_id,
          c.agent_id, c.token_count, c.created_at || new Date().toISOString(),
          c.model_id ?? null
        );
        // sqlite-vec requires BigInt for INTEGER PRIMARY KEY
        const chunkId = typeof result.lastInsertRowid === 'bigint'
          ? result.lastInsertRowid
          : BigInt(result.lastInsertRowid);
        insertVec.run(chunkId, new Float32Array(embeddings[i]));
      }
    });
    transaction();

    // 5. Dual-write: also write to LanceDB (safety net during transition)
    const records = newChunks.map((chunk, i) => ({
      text: chunk.text,
      vector: embeddings[i],
      role: chunk.role,
      source_type: chunk.source_type,
      source_id: chunk.source_id,
      agent_id: chunk.agent_id,
      token_count: chunk.token_count,
      created_at: chunk.created_at || new Date().toISOString(),
    }));

    try {
      if (!this.chunksTable) {
        this.chunksTable = await this.lanceDb!.createTable('chunks', records);
      } else {
        await this.chunksTable.add(records);
      }
    } catch (err) {
      // LanceDB write failure is non-fatal during transition
      console.warn('LanceDB dual-write failed (non-fatal):', (err as Error).message);
    }

    return newChunks.length;
  }

  // ── Delta Sync (export/import pre-embedded chunks) ──

  /** Export interface for delta sync payloads. */
  static readonly DELTA_VERSION = 1;

  /** Export chunks with IDs greater than sinceId. Returns pre-embedded chunks for delta sync.
   *  Core calls this to build delta payloads for Nodes. */
  exportChunksSince(sinceId: number): ExportedChunk[] {
    const db = this.sqliteDb!;

    // Get chunks with metadata
    const rows = db.prepare(`
      SELECT c.id, c.text, c.text_hash, c.role, c.source_type, c.source_id,
             c.agent_id, c.token_count, c.created_at, c.model_id, v.embedding
      FROM chunks c
      LEFT JOIN chunks_vec v ON v.chunk_id = c.id
      WHERE c.id > ?
      ORDER BY c.id ASC
    `).all(sinceId) as Array<{
      id: number; text: string; text_hash: string; role: string;
      source_type: string; source_id: string; agent_id: string;
      token_count: number; created_at: string; model_id: string | null; embedding: Buffer | null;
    }>;

    return rows.map(row => ({
      id: row.id,
      text: row.text,
      text_hash: row.text_hash,
      role: row.role,
      source_type: row.source_type,
      source_id: row.source_id,
      agent_id: row.agent_id,
      token_count: row.token_count,
      created_at: row.created_at,
      // Convert Float32Array buffer to number[] for JSON serialization
      embedding: row.embedding ? Array.from(new Float32Array(row.embedding.buffer, row.embedding.byteOffset, row.embedding.byteLength / 4)) : null,
      model_id: row.model_id,
    }));
  }

  /** Get the highest chunk ID in the database. Used for watermark tracking. */
  getMaxChunkId(): number {
    const db = this.sqliteDb!;
    const row = db.prepare('SELECT MAX(id) as maxId FROM chunks').get() as { maxId: number | null };
    return row.maxId || 0;
  }

  /** Import pre-embedded chunks from Core. Node calls this to apply delta payloads.
   *  Skips chunks that already exist (by text_hash). Does NOT re-embed. */
  importChunks(exported: ExportedChunk[]): number {
    if (exported.length === 0) return 0;
    const db = this.sqliteDb!;

    // Ensure vec table exists (use first chunk's embedding dimensions)
    const firstWithEmbed = exported.find(c => c.embedding && c.embedding.length > 0);
    if (firstWithEmbed && !this.vecDimensions) {
      this.ensureVecTable(firstWithEmbed.embedding!.length);
    }

    const insertChunk = db.prepare(`
      INSERT INTO chunks (text, text_hash, role, source_type, source_id, agent_id, token_count, created_at, model_id)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);
    const insertVec = db.prepare(`
      INSERT INTO chunks_vec (chunk_id, embedding) VALUES (?, ?)
    `);
    const checkHash = db.prepare('SELECT 1 FROM chunks WHERE text_hash = ?');

    let imported = 0;

    const transaction = db.transaction(() => {
      for (const chunk of exported) {
        // Dedup by hash
        if (checkHash.get(chunk.text_hash)) continue;

        const result = insertChunk.run(
          chunk.text, chunk.text_hash, chunk.role, chunk.source_type,
          chunk.source_id, chunk.agent_id, chunk.token_count, chunk.created_at,
          chunk.model_id ?? null
        );

        if (chunk.embedding && chunk.embedding.length > 0) {
          const chunkId = typeof result.lastInsertRowid === 'bigint'
            ? result.lastInsertRowid
            : BigInt(result.lastInsertRowid);
          insertVec.run(chunkId, new Float32Array(chunk.embedding));
        }

        imported++;
      }
    });
    transaction();

    return imported;
  }

  // ── Recency helpers ──

  private recencyWeight(ageDays: number): number {
    // Exponential decay: fresh content gets strong boost, rapid falloff.
    // Floor 0.3 so old stuff never fully disappears.
    // Half-life ~7 days. Day 0: 1.0, Day 1: 0.90, Day 3: 0.74, Day 7: 0.50, Day 14: 0.25 (floor 0.3)
    return Math.max(0.3, Math.exp(-ageDays * 0.1));
  }

  /** Parse relative time strings ("24h", "7d", "30d") or ISO dates into ISO date strings. */
  private parseSince(since: string): string | undefined {
    // Relative: "24h", "7d", "30d"
    const match = since.match(/^(\d+)(h|d)$/);
    if (match) {
      const [, num, unit] = match;
      const ms = unit === 'h' ? parseInt(num) * 3600000 : parseInt(num) * 86400000;
      return new Date(Date.now() - ms).toISOString();
    }
    // ISO date or datetime
    const parsed = new Date(since);
    if (!isNaN(parsed.getTime())) return parsed.toISOString();
    return undefined;
  }

  private freshnessLabel(ageDays: number): "fresh" | "recent" | "aging" | "stale" {
    if (ageDays < 3) return "fresh";
    if (ageDays < 7) return "recent";
    if (ageDays < 14) return "aging";
    return "stale";
  }

  // ── Search (Hybrid: BM25 + Vector + RRF fusion + Recency) ──

  async search(query: string, limit = 5, filter?: { agent_id?: string; source_type?: string; since?: string; until?: string }): Promise<SearchResult[]> {
    const db = this.sqliteDb!;

    // Check if sqlite-vec has been populated (migration complete)
    const sqliteChunks = (db.prepare('SELECT COUNT(*) as count FROM chunks').get() as any)?.count || 0;
    let lanceChunks = 0;
    if (this.chunksTable) {
      try { lanceChunks = await this.chunksTable.countRows(); } catch {}
    }

    // Use LanceDB fallback if sqlite-vec is empty OR has far fewer chunks than LanceDB
    // (migration not yet done). Once migration runs, sqlite-vec count will match.
    if (sqliteChunks === 0 || (lanceChunks > 0 && sqliteChunks < lanceChunks * 0.5)) {
      return this.searchLanceFallback(query, limit, filter);
    }

    // Parse since/until filters into ISO date strings
    const sinceDate = filter?.since ? this.parseSince(filter.since) : undefined;
    const untilDate = filter?.until ? this.parseSince(filter.until) : undefined;

    const [embedding] = await this.embed([query]);
    const fetchLimit = Math.max(limit * 5, 50);

    // Run FTS and vector search, then fuse with RRF. BM25 gets 2x weight.
    const vecResults = this.searchVec(embedding, fetchLimit, { ...filter, sinceDate, untilDate });
    const ftsResults = this.searchFTS(query, fetchLimit, { ...filter, sinceDate, untilDate });
    const fused = this.reciprocalRankFusion([ftsResults, vecResults], [2.0, 1.0]);

    // Apply recency weighting on top of fused scores
    const now = Date.now();
    const scored = fused.map(r => {
      const ageDays = r.created_at ? (now - new Date(r.created_at).getTime()) / 86400000 : 0;
      const recency = r.created_at ? this.recencyWeight(ageDays) : 1;
      // Apply recency to raw RRF score. Normalization happens after sorting.
      const rescaled = r.score * recency;
      return {
        ...r,
        score: rescaled,
        freshness: r.created_at ? this.freshnessLabel(ageDays) : undefined,
      };
    });

    const sorted = scored.sort((a, b) => b.score - a.score).slice(0, limit);
    // Normalize: top result = 0.95, others relative to it
    const topScore = sorted[0]?.score || 1;
    return sorted.map(r => ({ ...r, score: Math.min(r.score / topScore * 0.95, 0.95) }));
  }

  /** Deep search: query expansion + LLM re-ranking + position-aware blending.
   *  Falls back to standard search if no LLM provider is available.
   *  Supports intent disambiguation, candidateLimit tuning, and explain traces. */
  async deepSearch(query: string, limit = 5, filter?: { agent_id?: string; source_type?: string; since?: string; until?: string }, options?: { intent?: string; candidateLimit?: number; explain?: boolean }): Promise<SearchResult[]> {
    const { deepSearch: deepSearchFn } = await import('./search-pipeline.js');
    return deepSearchFn(this, query, { limit, filter, ...options });
  }

  /** Structured search: pass pre-expanded queries to skip LLM expansion.
   *  Each query is typed (lex, vec, hyde) and searched independently, then fused with RRF. */
  async structuredSearch(queries: StructuredQuery[], limit = 5, filter?: { agent_id?: string; source_type?: string; since?: string; until?: string }): Promise<SearchResult[]> {
    const db = this.sqliteDb!;
    const sinceDate = filter?.since ? this.parseSince(filter.since) : undefined;
    const untilDate = filter?.until ? this.parseSince(filter.until) : undefined;
    const internalFilter = { ...filter, sinceDate, untilDate };
    const allResultLists: SearchResult[][] = [];

    for (const q of queries) {
      if (q.type === 'lex') {
        const fts = this.searchFTS(q.text, Math.max(limit * 5, 50), internalFilter);
        if (fts.length > 0) allResultLists.push(fts);
      } else {
        const [embedding] = await this.embed([q.text]);
        const vec = this.searchVec(embedding, Math.max(limit * 5, 50), internalFilter);
        if (vec.length > 0) allResultLists.push(vec);
      }
    }

    // First list gets 2x weight (put your strongest signal first)
    const weights = allResultLists.map((_, i) => i === 0 ? 2.0 : 1.0);
    const fused = this.reciprocalRankFusion(allResultLists, weights);

    const now = Date.now();
    const scored = fused.map(r => {
      const ageDays = r.created_at ? (now - new Date(r.created_at).getTime()) / 86400000 : 0;
      const recency = r.created_at ? this.recencyWeight(ageDays) : 1;
      return { ...r, score: r.score * recency, freshness: r.created_at ? this.freshnessLabel(ageDays) : undefined };
    });

    const sorted = scored.sort((a, b) => b.score - a.score).slice(0, limit);
    const topScore = sorted[0]?.score || 1;
    return sorted.map(r => ({ ...r, score: Math.min(r.score / topScore * 0.95, 0.95) }));
  }

  /** Vector search via sqlite-vec. Two-step pattern: MATCH first, then JOIN. */
  private searchVec(embedding: number[], limit: number, filter?: { agent_id?: string; source_type?: string; sinceDate?: string; untilDate?: string }): SearchResult[] {
    const db = this.sqliteDb!;

    if (!this.vecDimensions) return [];

    // Step 1: sqlite-vec MATCH (no JOINs! Virtual tables hang with JOINs.)
    // See: https://github.com/tobi/qmd/pull/23
    const vecRows = db.prepare(`
      SELECT chunk_id, distance
      FROM chunks_vec
      WHERE embedding MATCH ? AND k = ?
    `).all(new Float32Array(embedding), limit) as Array<{ chunk_id: number; distance: number }>;

    if (vecRows.length === 0) return [];

    // Step 2: Look up chunk metadata with a separate query
    const ids = vecRows.map(r => r.chunk_id);
    const distMap = new Map(vecRows.map(r => [r.chunk_id, r.distance]));

    const placeholders = ids.map(() => '?').join(',');
    let sql = `SELECT id, text, role, source_type, source_id, agent_id, created_at FROM chunks WHERE id IN (${placeholders})`;
    const params: any[] = [...ids];

    if (filter?.agent_id) { sql += ' AND agent_id = ?'; params.push(filter.agent_id); }
    if (filter?.source_type) { sql += ' AND source_type = ?'; params.push(filter.source_type); }
    if (filter?.sinceDate) { sql += ' AND created_at >= ?'; params.push(filter.sinceDate); }
    if (filter?.untilDate) { sql += ' AND created_at < ?'; params.push(filter.untilDate); }

    const rows = db.prepare(sql).all(...params) as Array<{
      id: number; text: string; role: string; source_type: string;
      source_id: string; agent_id: string; created_at: string;
    }>;

    return rows.map(row => ({
      text: row.text,
      role: row.role,
      score: 1 - (distMap.get(row.id) || 1),  // cosine similarity from distance
      source_type: row.source_type,
      source_id: row.source_id,
      agent_id: row.agent_id,
      created_at: row.created_at,
    }));
  }

  /** Full-text search via FTS5 with BM25 scoring. */
  private searchFTS(query: string, limit: number, filter?: { agent_id?: string; source_type?: string; sinceDate?: string; untilDate?: string }): SearchResult[] {
    const db = this.sqliteDb!;
    const ftsQuery = this.buildFTS5Query(query);
    if (!ftsQuery) return [];

    let sql = `
      SELECT c.id, c.text, c.role, c.source_type, c.source_id, c.agent_id, c.created_at,
             bm25(chunks_fts) as bm25_score
      FROM chunks_fts f
      JOIN chunks c ON c.id = f.rowid
      WHERE chunks_fts MATCH ?
    `;
    const params: any[] = [ftsQuery];

    if (filter?.agent_id) { sql += ' AND c.agent_id = ?'; params.push(filter.agent_id); }
    if (filter?.source_type) { sql += ' AND c.source_type = ?'; params.push(filter.source_type); }
    if (filter?.sinceDate) { sql += ' AND c.created_at >= ?'; params.push(filter.sinceDate); }
    if (filter?.untilDate) { sql += ' AND c.created_at < ?'; params.push(filter.untilDate); }

    sql += ' ORDER BY bm25_score LIMIT ?';
    params.push(limit);

    const rows = db.prepare(sql).all(...params) as Array<{
      id: number; text: string; role: string; source_type: string;
      source_id: string; agent_id: string; created_at: string; bm25_score: number;
    }>;

    return rows.map(row => ({
      text: row.text,
      role: row.role,
      // BM25 scores are negative (lower = better). Normalize to [0..1).
      // |x| / (1 + |x|) maps: strong(-10)->0.91, medium(-2)->0.67, weak(-0.5)->0.33
      score: Math.abs(row.bm25_score) / (1 + Math.abs(row.bm25_score)),
      source_type: row.source_type,
      source_id: row.source_id,
      agent_id: row.agent_id,
      created_at: row.created_at,
    }));
  }

  /** Build a safe FTS5 query from user input. */
  private buildFTS5Query(query: string): string | null {
    const terms = query.split(/\s+/)
      .map(t => t.replace(/[^\p{L}\p{N}']/gu, '').toLowerCase())
      .filter(t => t.length > 0);
    if (terms.length === 0) return null;
    if (terms.length === 1) return `"${terms[0]}"*`;
    return terms.map(t => `"${t}"*`).join(' AND ');
  }

  /**
   * Reciprocal Rank Fusion. Ported from QMD (MIT License, Tobi Lutke, 2024-2026).
   * Fuses multiple ranked result lists into one using RRF scoring.
   * Uses text content as dedup key (instead of QMD's file path).
   */
  private reciprocalRankFusion(
    resultLists: SearchResult[][],
    weights: number[] = [],
    k: number = 60
  ): SearchResult[] {
    const scores = new Map<string, { result: SearchResult; rrfScore: number; topRank: number }>();

    for (let listIdx = 0; listIdx < resultLists.length; listIdx++) {
      const list = resultLists[listIdx];
      if (!list) continue;
      const weight = weights[listIdx] ?? 1.0;

      for (let rank = 0; rank < list.length; rank++) {
        const result = list[rank];
        if (!result) continue;
        const rrfContribution = weight / (k + rank + 1);
        // Dedup by text content (truncated for perf)
        const dedup = result.text.slice(0, 200);
        const existing = scores.get(dedup);

        if (existing) {
          existing.rrfScore += rrfContribution;
          existing.topRank = Math.min(existing.topRank, rank);
        } else {
          scores.set(dedup, {
            result,
            rrfScore: rrfContribution,
            topRank: rank,
          });
        }
      }
    }

    // Top-rank bonus: reward results that appear at or near the top of any list
    for (const entry of scores.values()) {
      if (entry.topRank === 0) {
        entry.rrfScore += 0.05;
      } else if (entry.topRank <= 2) {
        entry.rrfScore += 0.02;
      }
    }

    return Array.from(scores.values())
      .sort((a, b) => b.rrfScore - a.rrfScore)
      .map(e => ({ ...e.result, score: e.rrfScore }));
  }

  /** LanceDB fallback for search (used when sqlite-vec tables are empty, pre-migration). */
  private async searchLanceFallback(query: string, limit: number, filter?: { agent_id?: string; source_type?: string }): Promise<SearchResult[]> {
    if (!this.chunksTable) return [];

    const [embedding] = await this.embed([query]);
    const fetchLimit = Math.max(limit * 3, 30);
    let queryBuilder = this.chunksTable.vectorSearch(embedding).distanceType('cosine').limit(fetchLimit);

    if (filter?.agent_id) {
      queryBuilder = queryBuilder.where(`agent_id = '${filter.agent_id}'`);
    }
    if (filter?.source_type) {
      queryBuilder = queryBuilder.where(`source_type = '${filter.source_type}'`);
    }

    const results = await queryBuilder.toArray();
    const now = Date.now();

    return results.map((row: any) => {
      const cosine = row._distance != null ? 1 - row._distance : 0;
      const createdAt = row.created_at || '';
      const ageDays = createdAt ? (now - new Date(createdAt).getTime()) / 86400000 : 0;
      const weight = createdAt ? this.recencyWeight(ageDays) : 1;

      return {
        text: row.text,
        role: row.role,
        score: cosine * weight,
        source_type: row.source_type,
        source_id: row.source_id,
        agent_id: row.agent_id,
        created_at: createdAt,
        freshness: createdAt ? this.freshnessLabel(ageDays) : undefined,
      };
    })
    .sort((a, b) => b.score - a.score)
    .slice(0, limit);
  }

  // ── Remember (explicit fact storage) ──

  async remember(text: string, category: Memory['category'] = 'fact'): Promise<number> {
    const db = this.sqliteDb!;
    const now = new Date().toISOString();

    const stmt = db.prepare(`
      INSERT INTO memories (text, category, confidence, source_ids, status, created_at, updated_at)
      VALUES (?, ?, 1.0, '[]', 'active', ?, ?)
    `);
    const result = stmt.run(text, category, now, now);
    const memoryId = result.lastInsertRowid as number;
    const textChunks = this.chunkText(text, 400, 80);

    // Also ingest as chunks for vector search. Pre-chunked so large inputs
    // (e.g. whole workspace .md files) stay under the 8192-token provider cap.
    await this.ingest(textChunks.map((chunkText, i) => ({
      text: chunkText,
      role: 'system' as const,
      source_type: 'manual',
      source_id: textChunks.length > 1 ? `memory:${memoryId}:${i}` : `memory:${memoryId}`,
      agent_id: 'system',
      token_count: Math.ceil(chunkText.length / 4),
      created_at: now,
    })));

    return memoryId;
  }

  // ── Forget (deprecate a memory) ──

  forget(memoryId: number): boolean {
    const db = this.sqliteDb!;
    const now = new Date().toISOString();
    const result = db.prepare(`
      UPDATE memories SET status = 'deprecated', updated_at = ? WHERE id = ? AND status = 'active'
    `).run(now, memoryId);
    return result.changes > 0;
  }

  // ── Status ──

  async status(): Promise<CrystalStatus> {
    const db = this.sqliteDb!;

    // Show the higher of sqlite-vec or LanceDB count during transition
    const sqliteChunks = (db.prepare('SELECT COUNT(*) as count FROM chunks').get() as any)?.count || 0;
    let lanceChunks = 0;
    if (this.chunksTable) {
      try { lanceChunks = await this.chunksTable.countRows(); } catch {}
    }
    const chunks = Math.max(sqliteChunks, lanceChunks);

    // Time range from sqlite chunks table
    const oldest = (db.prepare('SELECT MIN(created_at) as ts FROM chunks').get() as any)?.ts || null;
    const newest = (db.prepare('SELECT MAX(created_at) as ts FROM chunks').get() as any)?.ts || null;

    const memories = (db.prepare('SELECT COUNT(*) as count FROM memories WHERE status = ?').get('active') as any)?.count || 0;
    const sources = (db.prepare('SELECT COUNT(*) as count FROM sources').get() as any)?.count || 0;

    // Get agents from chunks, sources, and capture_state tables
    const chunkAgentRows = db.prepare('SELECT DISTINCT agent_id FROM chunks WHERE agent_id IS NOT NULL').all() as any[];
    const sourceAgentRows = db.prepare('SELECT DISTINCT agent_id FROM sources').all() as any[];
    const captureAgentRows = db.prepare('SELECT DISTINCT agent_id FROM capture_state').all() as any[];
    const agents = [...new Set([
      ...chunkAgentRows.map((r: any) => r.agent_id),
      ...sourceAgentRows.map((r: any) => r.agent_id),
      ...captureAgentRows.map((r: any) => r.agent_id),
    ])];

    // Capture state summary
    const captureInfo = db.prepare(
      'SELECT COUNT(*) as count, MAX(last_capture_at) as latest FROM capture_state'
    ).get() as any;

    return {
      chunks,
      memories,
      sources,
      agents,
      oldestChunk: oldest,
      newestChunk: newest,
      embeddingProvider: this.config.embeddingProvider,
      dataDir: this.config.dataDir,
      capturedSessions: captureInfo?.count || 0,
      latestCapture: captureInfo?.latest || null,
    };
  }

  // ── Capture State (for incremental ingestion) ──

  getCaptureState(agentId: string, sourceId: string): { lastMessageCount: number; captureCount: number } {
    const db = this.sqliteDb!;
    const row = db.prepare('SELECT last_message_count, capture_count FROM capture_state WHERE agent_id = ? AND source_id = ?')
      .get(agentId, sourceId) as any;
    if (!row) return { lastMessageCount: 0, captureCount: 0 };
    return {
      lastMessageCount: row.last_message_count,
      captureCount: row.capture_count,
    };
  }

  setCaptureState(agentId: string, sourceId: string, messageCount: number, captureCount: number): void {
    const db = this.sqliteDb!;
    db.prepare(`
      INSERT OR REPLACE INTO capture_state (agent_id, source_id, last_message_count, capture_count, last_capture_at)
      VALUES (?, ?, ?, ?, ?)
    `).run(agentId, sourceId, messageCount, captureCount, new Date().toISOString());
  }

  // ── Source File Indexing (optional feature) ──
  //
  // Add directories as "collections", sync to index/re-index changed files.
  // All source chunks get source_type='file' so they're searchable alongside
  // conversations and memories. Nothing here is required... you can use MC
  // without ever touching sources.

  // Default patterns for files worth indexing
  private static readonly DEFAULT_INCLUDE = [
    '**/*.ts', '**/*.js', '**/*.tsx', '**/*.jsx',
    '**/*.py', '**/*.rs', '**/*.go', '**/*.java',
    '**/*.md', '**/*.txt', '**/*.json', '**/*.yaml', '**/*.yml',
    '**/*.toml', '**/*.sh', '**/*.bash', '**/*.zsh',
    '**/*.css', '**/*.html', '**/*.svg',
    '**/*.sql', '**/*.graphql',
    '**/*.c', '**/*.cpp', '**/*.h', '**/*.hpp',
    '**/*.swift', '**/*.kt', '**/*.rb',
    '**/*.env.example', '**/*.gitignore',
    '**/Makefile', '**/Dockerfile', '**/Cargo.toml',
    '**/package.json', '**/tsconfig.json',
  ];

  private static readonly DEFAULT_IGNORE = [
    '**/node_modules/**', '**/.git/**', '**/dist/**', '**/build/**',
    '**/.next/**', '**/.cache/**', '**/coverage/**', '**/__pycache__/**',
    '**/target/**', '**/vendor/**', '**/.venv/**',
    '**/*.lock', '**/package-lock.json', '**/yarn.lock', '**/bun.lockb',
    '**/*.min.js', '**/*.min.css', '**/*.map',
    '**/*.png', '**/*.jpg', '**/*.jpeg', '**/*.gif', '**/*.ico', '**/*.webp',
    '**/*.woff', '**/*.woff2', '**/*.ttf', '**/*.eot',
    '**/*.mp3', '**/*.mp4', '**/*.wav', '**/*.ogg', '**/*.webm',
    '**/*.zip', '**/*.tar', '**/*.gz', '**/*.br',
    '**/*.sqlite', '**/*.db', '**/*.lance/**',
    '**/*.jsonl',
    '**/secrets/**', '**/.env',
  ];

  /** Add a directory as a source collection for indexing. */
  async sourcesAdd(rootPath: string, name: string, options?: {
    include?: string[];
    ignore?: string[];
  }): Promise<SourceCollection> {
    const db = this.sqliteDb!;
    const now = new Date().toISOString();
    const includePatterns = JSON.stringify(options?.include || Crystal.DEFAULT_INCLUDE);
    const ignorePatterns = JSON.stringify(options?.ignore || Crystal.DEFAULT_IGNORE);

    // Check if collection already exists
    const existing = db.prepare('SELECT * FROM source_collections WHERE name = ?').get(name) as any;
    if (existing) {
      throw new Error(`Collection "${name}" already exists. Use sourcesSync() to update it.`);
    }

    db.prepare(`
      INSERT INTO source_collections (name, root_path, glob_patterns, ignore_patterns, created_at)
      VALUES (?, ?, ?, ?, ?)
    `).run(name, rootPath, includePatterns, ignorePatterns, now);

    const row = db.prepare('SELECT * FROM source_collections WHERE name = ?').get(name) as any;
    return row as SourceCollection;
  }

  /** Remove a source collection and its file records. Chunks remain in LanceDB. */
  sourcesRemove(name: string): boolean {
    const db = this.sqliteDb!;
    const col = db.prepare('SELECT id FROM source_collections WHERE name = ?').get(name) as any;
    if (!col) return false;
    db.prepare('DELETE FROM source_files WHERE collection_id = ?').run(col.id);
    db.prepare('DELETE FROM source_collections WHERE id = ?').run(col.id);
    return true;
  }

  /** Sync a collection: scan files, detect changes, re-index what changed. */
  async sourcesSync(name: string, options?: { dryRun?: boolean; batchSize?: number }): Promise<SyncResult> {
    const db = this.sqliteDb!;
    const startTime = Date.now();
    const batchSize = options?.batchSize || 20;

    const col = db.prepare('SELECT * FROM source_collections WHERE name = ?').get(name) as any;
    if (!col) throw new Error(`Collection "${name}" not found. Add it first with sourcesAdd().`);

    const includePatterns: string[] = JSON.parse(col.glob_patterns);
    const ignorePatterns: string[] = JSON.parse(col.ignore_patterns);

    // Scan the directory for matching files
    const files = this.scanDirectory(col.root_path, includePatterns, ignorePatterns);

    // Get existing file records
    const existingFiles = new Map<string, { id: number; file_hash: string }>();
    const rows = db.prepare('SELECT id, file_path, file_hash FROM source_files WHERE collection_id = ?').all(col.id) as any[];
    for (const row of rows) {
      existingFiles.set(row.file_path, { id: row.id, file_hash: row.file_hash });
    }

    let added = 0;
    let updated = 0;
    let removed = 0;
    let chunksAdded = 0;
    const now = new Date().toISOString();

    // Collect files that need indexing
    const toIndex: Array<{ relPath: string; absPath: string; hash: string; size: number; isUpdate: boolean }> = [];

    for (const absPath of files) {
      const relPath = relative(col.root_path, absPath);
      let content: string;
      try {
        content = readFileSync(absPath, 'utf-8');
      } catch {
        continue; // skip binary or unreadable files
      }

      // Skip files > 500KB (likely generated or data)
      const stat = statSync(absPath);
      if (stat.size > 500 * 1024) continue;

      const hash = createHash('sha256').update(content).digest('hex');
      const existing = existingFiles.get(relPath);

      if (existing) {
        existingFiles.delete(relPath); // mark as seen
        if (existing.file_hash === hash) continue; // unchanged
        toIndex.push({ relPath, absPath, hash, size: stat.size, isUpdate: true });
      } else {
        toIndex.push({ relPath, absPath, hash, size: stat.size, isUpdate: false });
      }
    }

    if (options?.dryRun) {
      const newFiles = toIndex.filter(f => !f.isUpdate).length;
      const updatedFiles = toIndex.filter(f => f.isUpdate).length;
      return {
        collection: name,
        added: newFiles,
        updated: updatedFiles,
        removed: existingFiles.size,
        chunks_added: 0,
        duration_ms: Date.now() - startTime,
      };
    }

    // Process files in batches
    for (let i = 0; i < toIndex.length; i += batchSize) {
      const batch = toIndex.slice(i, i + batchSize);
      const allChunks: Chunk[] = [];

      for (const file of batch) {
        const content = readFileSync(file.absPath, 'utf-8');
        const ext = extname(file.absPath);
        const fileName = basename(file.absPath);

        // Prepend file path context to help search
        const header = `File: ${file.relPath}\n\n`;
        const textChunks = this.chunkText(header + content, 400, 80);
        const fileChunks: Chunk[] = textChunks.map(text => ({
          text,
          role: 'system' as const,
          source_type: 'file',
          source_id: `file:${name}:${file.relPath}`,
          agent_id: 'system',
          token_count: Math.ceil(text.length / 4),
          created_at: now,
        }));

        allChunks.push(...fileChunks);

        // Update or insert file record
        if (file.isUpdate) {
          db.prepare(`
            UPDATE source_files SET file_hash = ?, file_size = ?, chunk_count = ?, last_indexed_at = ?
            WHERE collection_id = ? AND file_path = ?
          `).run(file.hash, file.size, fileChunks.length, now, col.id, file.relPath);
          updated++;
        } else {
          db.prepare(`
            INSERT INTO source_files (collection_id, file_path, file_hash, file_size, chunk_count, last_indexed_at)
            VALUES (?, ?, ?, ?, ?, ?)
          `).run(col.id, file.relPath, file.hash, file.size, fileChunks.length, now);
          added++;
        }
      }

      // Embed and ingest the batch
      if (allChunks.length > 0) {
        const ingested = await this.ingest(allChunks);
        chunksAdded += ingested;
      }
    }

    // Remove files that no longer exist on disk
    for (const [relPath, { id }] of existingFiles) {
      db.prepare('DELETE FROM source_files WHERE id = ?').run(id);
      removed++;
    }

    // Update collection stats
    const fileCount = (db.prepare('SELECT COUNT(*) as count FROM source_files WHERE collection_id = ?').get(col.id) as any).count;
    const chunkCount = (db.prepare('SELECT SUM(chunk_count) as total FROM source_files WHERE collection_id = ?').get(col.id) as any).total || 0;
    db.prepare('UPDATE source_collections SET file_count = ?, chunk_count = ?, last_sync_at = ? WHERE id = ?')
      .run(fileCount, chunkCount, now, col.id);

    return {
      collection: name,
      added,
      updated,
      removed,
      chunks_added: chunksAdded,
      duration_ms: Date.now() - startTime,
    };
  }

  /** Get status of all source collections. */
  sourcesStatus(): SourcesStatus {
    const db = this.sqliteDb!;
    const collections = db.prepare('SELECT name, root_path, file_count, chunk_count, last_sync_at FROM source_collections').all() as any[];
    const totalFiles = collections.reduce((sum, c) => sum + c.file_count, 0);
    const totalChunks = collections.reduce((sum, c) => sum + c.chunk_count, 0);

    return {
      collections: collections.map(c => ({
        name: c.name,
        root_path: c.root_path,
        file_count: c.file_count,
        chunk_count: c.chunk_count,
        last_sync_at: c.last_sync_at,
      })),
      total_files: totalFiles,
      total_chunks: totalChunks,
    };
  }

  /** Scan a directory recursively, matching include/ignore patterns. */
  private scanDirectory(rootPath: string, includePatterns: string[], ignorePatterns: string[]): string[] {
    const results: string[] = [];

    // Build sets of allowed extensions and ignored directory names for fast filtering
    const allowedExtensions = new Set<string>();
    const allowedExactNames = new Set<string>();
    for (const pattern of includePatterns) {
      // Extract extension from patterns like "**/*.ts"
      const extMatch = pattern.match(/\*\*\/\*(\.\w+)$/);
      if (extMatch) {
        allowedExtensions.add(extMatch[1]);
      }
      // Exact filenames like "**/Makefile"
      const nameMatch = pattern.match(/\*\*\/([^*]+)$/);
      if (nameMatch && !nameMatch[1].startsWith('*.')) {
        allowedExactNames.add(nameMatch[1]);
      }
    }

    const ignoreDirs = new Set<string>();
    for (const pattern of ignorePatterns) {
      // Extract directory names from patterns like "**/node_modules/**"
      const dirMatch = pattern.match(/\*\*\/([^/*]+)\/\*\*$/);
      if (dirMatch) {
        ignoreDirs.add(dirMatch[1]);
      }
    }

    const ignoreFiles = new Set<string>();
    for (const pattern of ignorePatterns) {
      // Extract filenames/extensions to ignore
      const fileMatch = pattern.match(/\*\*\/\*(\.\w+)$/);
      if (fileMatch) {
        ignoreFiles.add(fileMatch[1]);
      }
      const exactMatch = pattern.match(/\*\*\/([^*]+)$/);
      if (exactMatch && !exactMatch[1].includes('/')) {
        ignoreFiles.add(exactMatch[1]);
      }
    }

    const walk = (dir: string) => {
      let entries: string[];
      try {
        entries = readdirSync(dir);
      } catch {
        return;
      }

      for (const entry of entries) {
        const fullPath = join(dir, entry);
        let stat;
        try {
          stat = statSync(fullPath);
        } catch {
          continue;
        }

        if (stat.isDirectory()) {
          if (ignoreDirs.has(entry)) continue;
          if (entry.startsWith('.')) continue; // skip hidden dirs
          walk(fullPath);
        } else if (stat.isFile()) {
          const ext = extname(entry);
          if (ignoreFiles.has(ext)) continue;
          if (ignoreFiles.has(entry)) continue;

          if (allowedExtensions.has(ext) || allowedExactNames.has(entry)) {
            results.push(fullPath);
          }
        }
      }
    };

    walk(rootPath);
    return results;
  }

  // ── Orphan Cleanup ──

  /** Clean orphaned entries in chunks_vec and chunks_fts that no longer have
   *  corresponding rows in the chunks table. Returns counts of what was found/cleaned. */
  cleanOrphans(options?: { dryRun?: boolean }): {
    orphanedVec: number; orphanedFts: number;
    cleanedVec: number; cleanedFts: number; dryRun: boolean;
  } {
    const db = this.sqliteDb!;
    const dryRun = options?.dryRun ?? false;

    const orphanedVec = (db.prepare(
      'SELECT COUNT(*) as cnt FROM chunks_vec WHERE chunk_id NOT IN (SELECT id FROM chunks)'
    ).get() as any).cnt;

    const orphanedFts = (db.prepare(
      'SELECT COUNT(*) as cnt FROM chunks_fts WHERE rowid NOT IN (SELECT id FROM chunks)'
    ).get() as any).cnt;

    if (dryRun) {
      return { orphanedVec, orphanedFts, cleanedVec: 0, cleanedFts: 0, dryRun: true };
    }

    let cleanedVec = 0;
    if (orphanedVec > 0) {
      const ids = db.prepare(
        'SELECT chunk_id FROM chunks_vec WHERE chunk_id NOT IN (SELECT id FROM chunks)'
      ).all() as Array<{ chunk_id: number }>;
      const del = db.prepare('DELETE FROM chunks_vec WHERE chunk_id = ?');
      const BATCH = 1000;
      for (let i = 0; i < ids.length; i += BATCH) {
        const batch = ids.slice(i, i + BATCH);
        db.transaction(() => { for (const r of batch) { del.run(r.chunk_id); cleanedVec++; } })();
      }
    }

    let cleanedFts = 0;
    if (orphanedFts > 0) {
      db.exec('DELETE FROM chunks_fts');
      db.exec('INSERT INTO chunks_fts(rowid, text) SELECT id, text FROM chunks');
      cleanedFts = orphanedFts;
    }

    return { orphanedVec, orphanedFts, cleanedVec, cleanedFts, dryRun: false };
  }

  // ── Cleanup ──

  close(): void {
    this.sqliteDb?.close();
    // LanceDB connection doesn't need explicit close
  }
}

// ─── Config Resolution ─────────────────────────────────────────────────────
//
// Key resolution order:
//   1. Explicit overrides (programmatic)
//   2. process.env (set by op-secrets plugin inside OpenClaw, or by user)
//   3. .env file in data dir (~/.ldm/memory/.env)
//   4. 1Password via op CLI (if SA token exists)
//
// Two setup paths:
//   • .env file:    cp .env.example ~/.ldm/memory/.env && edit
//   • 1Password:    keys auto-resolved from "Agent Secrets" vault

export function resolveConfig(overrides?: Partial<CrystalConfig>): CrystalConfig {
  const HOME = process.env.HOME || '';
  const ldmMemory = join(HOME, '.ldm', 'memory');

  // dataDir resolution order:
  // 1. Explicit override (always wins)
  // 2. CRYSTAL_DATA_DIR env var (for testing)
  // 3. ~/.ldm/memory/ (canonical LDM path)
  // 4. Legacy ~/.openclaw/memory-crystal/ (pre-LDM migration fallback)
  let dataDir = overrides?.dataDir || process.env.CRYSTAL_DATA_DIR;
  if (!dataDir) {
    if (existsSync(join(ldmMemory, 'crystal.db'))) {
      dataDir = ldmMemory;
    } else {
      const legacyDir = join(HOME, '.openclaw', 'memory-crystal');
      if (existsSync(join(legacyDir, 'crystal.db'))) {
        dataDir = legacyDir;
      } else {
        dataDir = ldmMemory; // default: new LDM install
      }
    }
  }

  // Load .env file if it exists (doesn't override existing env vars)
  loadEnvFile(join(dataDir, '.env'));

  // Resolve API keys: env/.env first, then 1Password fallback
  const openaiApiKey = overrides?.openaiApiKey || process.env.OPENAI_API_KEY || opRead('OpenAI API', 'api key');
  const googleApiKey = overrides?.googleApiKey || process.env.GOOGLE_API_KEY || opRead('Google AI', 'api key');
  const remoteToken = overrides?.remoteToken || process.env.CRYSTAL_REMOTE_TOKEN || opRead('Memory Crystal Remote', 'token');

  return {
    dataDir,
    embeddingProvider: (overrides?.embeddingProvider || process.env.CRYSTAL_EMBEDDING_PROVIDER || 'openai') as CrystalConfig['embeddingProvider'],
    openaiApiKey,
    openaiModel: overrides?.openaiModel || process.env.CRYSTAL_OPENAI_MODEL || 'text-embedding-3-small',
    ollamaHost: overrides?.ollamaHost || process.env.CRYSTAL_OLLAMA_HOST || 'http://localhost:11434',
    ollamaModel: overrides?.ollamaModel || process.env.CRYSTAL_OLLAMA_MODEL || 'nomic-embed-text',
    googleApiKey,
    googleModel: overrides?.googleModel || process.env.CRYSTAL_GOOGLE_MODEL || 'text-embedding-004',
    remoteUrl: overrides?.remoteUrl || process.env.CRYSTAL_REMOTE_URL,
    remoteToken,
  };
}

/** Load a .env file into process.env. Does NOT override existing vars. */
function loadEnvFile(path: string): void {
  if (!existsSync(path)) return;
  const content = readFileSync(path, 'utf8');
  for (const line of content.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eqIdx = trimmed.indexOf('=');
    if (eqIdx === -1) continue;
    const key = trimmed.slice(0, eqIdx).trim();
    let value = trimmed.slice(eqIdx + 1).trim();
    // Strip surrounding quotes
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    if (key && !process.env[key]) {
      process.env[key] = value;
    }
  }
}

/** Read a secret from 1Password via op CLI. Falls back silently on failure.
 *  Checks ~/.ldm/secrets/op-sa-token first, then ~/.openclaw/secrets/op-sa-token. */
function opRead(item: string, field: string): string | undefined {
  try {
    const HOME = process.env.HOME || '';
    // Check LDM path first, then legacy OpenClaw path
    let saTokenPath = join(HOME, '.ldm', 'secrets', 'op-sa-token');
    if (!existsSync(saTokenPath)) {
      saTokenPath = join(HOME, '.openclaw', 'secrets', 'op-sa-token');
    }
    if (!existsSync(saTokenPath)) return undefined;
    const saToken = readFileSync(saTokenPath, 'utf8').trim();
    // Prefer an absolute op binary path (scoped-hook pattern: no reliance on PATH inherited by
    // child processes, no global shell-env exposure of the SA token); fall back to bare `op`.
    const opPath = [
      '/opt/homebrew/bin/op',
      '/usr/local/bin/op',
      '/usr/bin/op',
    ].find((p) => existsSync(p)) || 'op';
    return execSync(`${opPath} read "op://Agent Secrets/${item}/${field}" 2>/dev/null`, {
      encoding: 'utf8',
      env: { ...process.env, OP_SERVICE_ACCOUNT_TOKEN: saToken },
      timeout: 10000,
    }).trim() || undefined;
  } catch {
    return undefined;
  }
}

// ─── Remote Crystal (Cloud Mirror Mode) ────────────────────────────────────
// When remoteUrl is set, this class talks to the Cloudflare Worker instead
// of local SQLite. Same interface as Crystal for search/remember/forget/status/ingest.

export class RemoteCrystal {
  private url: string;
  private token: string;

  constructor(url: string, token: string) {
    this.url = url.replace(/\/$/, '');
    this.token = token;
  }

  async init(): Promise<void> {
    // No local DB to initialize — just verify the Worker is reachable
    const resp = await fetch(`${this.url}/health`);
    if (!resp.ok) {
      throw new Error(`Remote crystal unreachable: ${resp.status}`);
    }
  }

  private async request(path: string, body?: any): Promise<any> {
    const resp = await fetch(`${this.url}${path}`, {
      method: body ? 'POST' : 'GET',
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json',
      },
      ...(body ? { body: JSON.stringify(body) } : {}),
    });

    if (!resp.ok) {
      const err = await resp.text();
      throw new Error(`Remote crystal error ${resp.status}: ${err}`);
    }

    return resp.json();
  }

  async search(query: string, limit = 5, filter?: { agent_id?: string }): Promise<SearchResult[]> {
    const data = await this.request('/search', { query, limit, agent_id: filter?.agent_id });
    return data.results || [];
  }

  async ingest(chunks: Chunk[]): Promise<number> {
    const data = await this.request('/ingest', { chunks });
    return data.ingested || 0;
  }

  async remember(text: string, category: Memory['category'] = 'fact'): Promise<number> {
    const data = await this.request('/remember', { text, category });
    return data.id;
  }

  forget(memoryId: number): Promise<boolean> {
    return this.request('/forget', { id: memoryId }).then(d => d.ok);
  }

  async status(): Promise<CrystalStatus> {
    const data = await this.request('/status');
    return {
      chunks: data.chunks || 0,
      memories: data.memories || 0,
      sources: 0,
      agents: data.agents || [],
      oldestChunk: data.oldestChunk,
      newestChunk: data.newestChunk,
      embeddingProvider: 'remote',
      dataDir: this.url,
      capturedSessions: data.capturedSessions || 0,
      latestCapture: data.newestChunk,
    };
  }

  // Expose chunkText from a local Crystal instance for cc-hook to use
  chunkText(text: string): string[] {
    // Simple chunking for remote mode — matches Crystal.chunkText() logic
    const targetChars = 400 * 4; // 400 tokens * ~4 chars
    const overlapChars = 80 * 4;

    if (text.length <= targetChars) return [text];

    const chunks: string[] = [];
    let start = 0;
    while (start < text.length) {
      let end = start + targetChars;
      if (end >= text.length) {
        chunks.push(text.slice(start));
        break;
      }
      // Try to break at paragraph
      const paraBreak = text.lastIndexOf('\n\n', end);
      if (paraBreak > start + targetChars * 0.5) end = paraBreak;
      else {
        // Try sentence break
        const sentBreak = text.lastIndexOf('. ', end);
        if (sentBreak > start + targetChars * 0.5) end = sentBreak + 1;
      }
      chunks.push(text.slice(start, end));
      start = end - overlapChars;
    }
    return chunks;
  }
}

/** Create the appropriate Crystal instance based on config. */
export function createCrystal(config: CrystalConfig): Crystal | RemoteCrystal {
  if (config.remoteUrl && config.remoteToken) {
    return new RemoteCrystal(config.remoteUrl, config.remoteToken);
  }
  return new Crystal(config);
}
