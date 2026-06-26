/**
 * cache_semantic.js — Semantic query cache for unified-memory
 * P2-1: Semantic Cache
 * 
 * Caches semantically similar query results using embeddings.
 * - Key: SHA256(normalized_query)
 * - Similarity threshold: 0.95 (very high precision)
 * - TTL: configurable (default 3600s), auto-cleanup on access
 * - Storage: JSON file (no external DB dependency)
 */

import { createRequire } from 'module';
import { existsSync, readFileSync, writeFileSync, mkdirSync, unlinkSync } from 'fs';
import { join, dirname } from 'path';
import { createHash } from 'crypto';
import { fileURLToPath } from 'url';

const req = createRequire(import.meta.url);
const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = process.env.HOME || '/root';
const CACHE_DIR = join(HOME, '.unified-memory', 'cache');
const CACHE_FILE = join(CACHE_DIR, 'semantic_cache.json');

// ============================================================
// Embedding support (reuse LanceDB's embedding or Ollama)
// ============================================================

let _embeddingFn = null;

async function getEmbedding(text) {
  if (_embeddingFn) return _embeddingFn(text);

  // Try LanceDB's VectorMemory
  try {
    const { VectorMemory } = await import('./vector_lancedb.js');
    const vm = new VectorMemory();
    await vm.initialize();
    _embeddingFn = async (t) => {
      const emb = await vm.embed(t);
      return emb;
    };
    const emb = await _embeddingFn(text);
    return emb;
  } catch {
    // Fallback: use Ollama directly
  }

  // Direct Ollama
  const OLLAMA_BASE = process.env.OLLAMA_BASE || 'http://192.168.2.155:11434';
  const EMBED_MODEL = process.env.EMBED_MODEL || 'nomic-embed-text';

  try {
    const resp = await fetch(`${OLLAMA_BASE}/api/embeddings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: EMBED_MODEL, prompt: text }),
      signal: AbortSignal.timeout(15000),
    });
    if (!resp.ok) throw new Error(`Ollama ${resp.status}`);
    const data = await resp.json();
    return data.embedding || [];
  } catch (err) {
    console.error('[semantic_cache] Embedding failed:', err.message);
    return null;
  }
}

function cosineSimilarity(a, b) {
  if (!a || !b || a.length !== b.length) return 0;
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  return dot / (Math.sqrt(normA) * Math.sqrt(normB) + 1e-8);
}

// ============================================================
// Cache storage
// ============================================================

/**
 * Normalize query string for consistent key generation
 */
function normalizeQuery(query) {
  return query
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .replace(/[^\w\u4e00-\u9fff\s]/g, '')
    .trim();
}

/**
 * SHA256 hash of normalized query
 */
function cacheKey(query) {
  const normalized = normalizeQuery(query);
  return createHash('sha256').update(normalized).digest('hex');
}

/**
 * Load cache from disk
 */
function loadCache() {
  if (!existsSync(CACHE_FILE)) {
    return { entries: {}, stats: { hits: 0, misses: 0, evictions: 0 } };
  }
  try {
    const data = JSON.parse(readFileSync(CACHE_FILE, 'utf-8'));
    return data;
  } catch {
    return { entries: {}, stats: { hits: 0, misses: 0, evictions: 0 } };
  }
}

/**
 * Persist cache to disk (atomic write)
 */
function saveCache(cache) {
  try {
    mkdirSync(CACHE_DIR, { recursive: true });
    writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2), 'utf-8');
  } catch (err) {
    console.error('[semantic_cache] Save failed:', err.message);
  }
}

// ============================================================
// Public API
// ============================================================

/**
 * Get a cached response for a query.
 * Returns null if no matching entry found (similarity < 0.95 or TTL expired).
 * @param {string} query
 * @param {object} options
 * @param {number} options.ttlSeconds - TTL in seconds (default 3600)
 * @param {number} options.similarityThreshold - Min similarity (default 0.95)
 * @returns {Promise<object|null>}
 */
export async function cacheGet(query, { ttlSeconds = 3600, similarityThreshold = 0.95 } = {}) {
  const cache = loadCache();
  const key = cacheKey(query);
  const now = Date.now();

  // Try exact key match first
  const entry = cache.entries[key];
  if (entry) {
    const ageSeconds = (now - entry.cached_at) / 1000;
    if (ageSeconds <= ttlSeconds) {
      cache.stats.hits++;
      saveCache(cache);
      return {
        hit: 'exact',
        response: entry.response,
        similarity: 1.0,
        age_seconds: Math.round(ageSeconds),
        cached_at: new Date(entry.cached_at).toISOString(),
      };
    } else {
      // TTL expired — remove
      delete cache.entries[key];
      cache.stats.evictions++;
      saveCache(cache);
    }
  }

  // Try semantic similarity with other entries
  const queryEmb = await getEmbedding(query);
  if (!queryEmb) {
    cache.stats.misses++;
    saveCache(cache);
    return null;
  }

  let bestEntry = null;
  let bestSimilarity = similarityThreshold;

  for (const [k, e] of Object.entries(cache.entries)) {
    const ageSeconds = (now - e.cached_at) / 1000;
    if (ageSeconds > ttlSeconds) {
      // Clean expired entries during scan
      delete cache.entries[k];
      cache.stats.evictions++;
      continue;
    }
    if (!e.embedding) continue;
    const sim = cosineSimilarity(queryEmb, e.embedding);
    if (sim >= bestSimilarity) {
      bestSimilarity = sim;
      bestEntry = e;
    }
  }

  if (bestEntry) {
    cache.stats.hits++;
    saveCache(cache);
    return {
      hit: 'semantic',
      response: bestEntry.response,
      similarity: Math.round(bestSimilarity * 1000) / 1000,
      age_seconds: Math.round((now - bestEntry.cached_at) / 1000),
      cached_at: new Date(bestEntry.cached_at).toISOString(),
    };
  }

  cache.stats.misses++;
  saveCache(cache);
  return null;
}

/**
 * Store a query + response in the cache.
 * @param {string} query
 * @param {object} response - the response to cache
 * @param {object} options
 * @param {number} options.ttlSeconds - TTL in seconds (default 3600)
 * @returns {Promise<{stored: true, key: string, entry_count: number}>}
 */
export async function cacheSet(query, response, { ttlSeconds = 3600 } = {}) {
  const cache = loadCache();
  const key = cacheKey(query);
  const now = Date.now();

  // Store entry with optional embedding
  const embedding = await getEmbedding(query).catch(() => null);

  cache.entries[key] = {
    query: normalizeQuery(query),
    response,
    embedding,
    cached_at: now,
    ttl_seconds: ttlSeconds,
  };

  // Evict expired entries
  const expiredCount = Object.entries(cache.entries).filter(([, e]) => {
    return (now - e.cached_at) / 1000 > (e.ttl_seconds || 3600);
  }).length;

  for (const [k, e] of Object.entries(cache.entries)) {
    if ((now - e.cached_at) / 1000 > (e.ttl_seconds || 3600)) {
      delete cache.entries[k];
    }
  }

  saveCache(cache);

  return {
    stored: true,
    key,
    entry_count: Object.keys(cache.entries).length,
    evicted_count: expiredCount,
  };
}

/**
 * Invalidate a specific query from cache
 * @param {string} query
 */
export function cacheDelete(query) {
  const cache = loadCache();
  const key = cacheKey(query);
  if (cache.entries[key]) {
    delete cache.entries[key];
    saveCache(cache);
    return { deleted: true, key };
  }
  return { deleted: false, key };
}

/**
 * Clear entire cache
 */
export function cacheClear() {
  const cache = loadCache();
  const count = Object.keys(cache.entries).length;
  cache.entries = {};
  saveCache(cache);
  return { cleared: true, entries_removed: count };
}

/**
 * Get cache statistics
 */
export function cacheStats() {
  const cache = loadCache();
  const now = Date.now();
  const entries = Object.values(cache.entries);

  let expired = 0;
  let totalAge = 0;
  for (const e of entries) {
    const age = (now - e.cached_at) / 1000;
    if (age > (e.ttl_seconds || 3600)) expired++;
    totalAge += age;
  }

  return {
    entry_count: entries.length,
    expired_count: expired,
    stats: cache.stats,
    avg_age_seconds: entries.length ? Math.round(totalAge / entries.length) : 0,
    cache_file: CACHE_FILE,
  };
}

/**
 * MCP tool: memory_cache
 * Actions: get, set, delete, clear, stats
 */
export function memoryCacheTool({ action, query, response, ttlSeconds } = {}) {
  if (action === 'stats') {
    const stats = cacheStats();
    return { content: [{ type: 'text', text: JSON.stringify(stats, null, 2) }] };
  }

  if (action === 'clear') {
    const result = cacheClear();
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }

  if (action === 'get') {
    if (!query) {
      return { content: [{ type: 'text', text: '{"error": "query is required for get action"}' }], isError: true };
    }
    return cacheGet(query, { ttlSeconds }).then(result => {
      if (!result) {
        return { content: [{ type: 'text', text: JSON.stringify({ hit: false, message: 'No cache entry found' }, null, 2) }] };
      }
      return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
    }).catch(err => {
      return { content: [{ type: 'text', text: `Cache get error: ${err.message}` }], isError: true };
    });
  }

  if (action === 'set') {
    if (!query || response === undefined) {
      return { content: [{ type: 'text', text: '{"error": "query and response are required for set action"}' }], isError: true };
    }
    return cacheSet(query, response, { ttlSeconds }).then(result => {
      return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
    }).catch(err => {
      return { content: [{ type: 'text', text: `Cache set error: ${err.message}` }], isError: true };
    });
  }

  if (action === 'delete') {
    if (!query) {
      return { content: [{ type: 'text', text: '{"error": "query is required for delete action"}' }], isError: true };
    }
    const result = cacheDelete(query);
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }

  return {
    content: [{ type: 'text', text: '{"error": "Unknown action. Use: get, set, delete, clear, stats"}' }],
    isError: true,
  };
}

export default {
  cacheGet,
  cacheSet,
  cacheDelete,
  cacheClear,
  cacheStats,
  memoryCacheTool,
};
