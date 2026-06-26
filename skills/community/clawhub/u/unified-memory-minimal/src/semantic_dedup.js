/**
 * semantic_dedup.js - Semantic Deduplication using Embeddings
 *
 * Given a new memory, find semantically similar existing memories using
 * cosine similarity on embedding vectors. Uses Ollama embeddings via
 * the existing embedding infrastructure.
 *
 * Thresholds:
 *   > 0.95 → Absorb (near-identical)
 *   0.85–0.95 → Merge candidate
 *   < 0.85 → Keep both
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { getEmbeddingCached } from './vector.js';
import { getAllMemories, getAllMemoriesRaw } from './storage.js';
import { config } from './config.js';

// ─── Configurable thresholds ────────────────────────────────────────────────
export const DEFAULT_SIMILARITY_THRESHOLD = 0.85;
export const ABSORB_THRESHOLD = 0.95;      // >0.95 → silently absorb
export const MERGE_THRESHOLD = 0.85;       // 0.85–0.95 → ask/merge
export const MIN_SCORE = 0.10;             // Minimum similarity to even report

// ─── Dedup log path ────────────────────────────────────────────────────────
export const DEDUP_LOG_PATH = join(config.memoryDir, 'dedup_log.json');

function ensureDedupLog() {
  const dir = config.memoryDir;
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  if (!existsSync(DEDUP_LOG_PATH)) {
    writeFileSync(DEDUP_LOG_PATH, JSON.stringify({ merges: [], scans: [] }, null, 2));
  }
}

/**
 * Compute cosine similarity between two vectors.
 * @param {number[]} a
 * @param {number[]} b
 * @returns {number}
 */
export function cosineSimilarity(a, b) {
  if (!a || !b || a.length !== b.length) return 0;
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  if (normA === 0 || normB === 0) return 0;
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

/**
 * Load dedup log from disk.
 * @returns {{ merges: object[], scans: object[] }}
 */
export function loadDedupLog() {
  ensureDedupLog();
  try {
    return JSON.parse(readFileSync(DEDUP_LOG_PATH, 'utf8'));
  } catch {
    return { merges: [], scans: [] };
  }
}

/**
 * Append an entry to the dedup log.
 * @param {'merge'|'absorb'|'scan'} type
 * @param {object} entry
 */
export function appendDedupLog(type, entry) {
  ensureDedupLog();
  try {
    const log = loadDedupLog();
    const timestamp = new Date().toISOString();
    if (type === 'merge' || type === 'absorb') {
      log.merges.push({ ...entry, timestamp });
    } else {
      log.scans.push({ ...entry, timestamp });
    }
    writeFileSync(DEDUP_LOG_PATH, JSON.stringify(log, null, 2));
  } catch (err) {
    console.warn('[semantic_dedup] Failed to write dedup log:', err.message);
  }
}

/**
 * Get a memory's embedding. Uses cached file if available, otherwise generates.
 * Embeddings are cached under config.vectorCacheDir keyed by text hash.
 *
 * @param {object} memory - Memory object with `text` field
 * @returns {Promise<number[]|null>}
 */
async function getMemoryEmbedding(memory) {
  if (!memory || !memory.text) return null;
  try {
    return await getEmbeddingCached(memory.text);
  } catch (err) {
    console.warn(`[semantic_dedup] Embedding failed for ${memory.id}:`, err.message);
    return null;
  }
}

/**
 * Find duplicate candidates for a given text/memory against all stored memories.
 *
 * @param {object} newMemory - Memory object with `id` and `text`
 * @param {object} opts
 * @param {number} opts.threshold - Minimum similarity to return (default 0.85)
 * @param {number} opts.topK - Max candidates to return (default 10)
 * @returns {Promise<Array<{ memory: object, similarity: number }>>}
 */
export async function findDuplicateCandidates(newMemory, opts = {}) {
  const { threshold = DEFAULT_SIMILARITY_THRESHOLD, topK = 10 } = opts;

  if (!newMemory || !newMemory.text) {
    return [];
  }

  const existingMemories = (await getAllMemories()).filter(m => m.id !== newMemory.id);
  if (existingMemories.length === 0) return [];

  // Embed the new memory once
  const newEmbedding = await getMemoryEmbedding(newMemory);
  if (!newEmbedding) {
    console.warn('[semantic_dedup] Could not generate embedding for new memory');
    return [];
  }

  const candidates = [];

  // Compare against all existing memories
  // Process in batches to avoid hammering the embedding API
  const BATCH_SIZE = 20;
  for (let i = 0; i < existingMemories.length; i += BATCH_SIZE) {
    const batch = existingMemories.slice(i, i + BATCH_SIZE);
    await Promise.all(batch.map(async (existing) => {
      if (!existing.text) return;
      try {
        const existingEmbedding = await getMemoryEmbedding(existing);
        if (!existingEmbedding) return;
        const sim = cosineSimilarity(newEmbedding, existingEmbedding);
        if (sim >= threshold) {
          candidates.push({ memory: existing, similarity: sim });
        }
      } catch (err) {
        // Skip individual comparison failures
      }
    }));
  }

  // Sort by similarity descending, take topK
  candidates.sort((a, b) => b.similarity - a.similarity);
  return candidates.slice(0, topK);
}

/**
 * Classify a similarity score into a merge strategy.
 * @param {number} similarity - Cosine similarity 0–1
 * @returns {'absorb'|'merge'|'keep_both'}
 */
export function classifySimilarity(similarity) {
  if (similarity > ABSORB_THRESHOLD) return 'absorb';
  if (similarity >= MERGE_THRESHOLD) return 'merge';
  return 'keep_both';
}

/**
 * Determine merge strategy for a pair of memories.
 * @param {number} similarity
 * @returns {{ strategy: string, reason: string }}
 */
export function getMergeStrategy(similarity) {
  const strategy = classifySimilarity(similarity);
  const reasons = {
    absorb: `Similarity ${(similarity * 100).toFixed(1)}% > ${(ABSORB_THRESHOLD * 100).toFixed(0)}%: near-identical, keep older`,
    merge: `Similarity ${(similarity * 100).toFixed(1)}% in [${(MERGE_THRESHOLD * 100).toFixed(0)}%–${(ABSORB_THRESHOLD * 100).toFixed(0)}%]: merge unique details`,
    keep_both: `Similarity ${(similarity * 100).toFixed(1)}% < ${(MERGE_THRESHOLD * 100).toFixed(0)}%: different aspects, keep both`,
  };
  return { strategy, reason: reasons[strategy] };
}

/**
 * Full semantic scan: find all duplicate pairs across all memories.
 * Used by memory_dedup_full_scan tool.
 *
 * @param {object} opts
 * @param {number} opts.threshold - Minimum similarity (default 0.85)
 * @param {number} opts.maxPairs - Max pairs to return (default 100)
 * @returns {Promise<{ pairs: Array, stats: object }>}
 */
export async function findAllDuplicatePairs(opts = {}) {
  const { threshold = DEFAULT_SIMILARITY_THRESHOLD, maxPairs = 100 } = opts;

  const memories = getAllMemoriesRaw();
  if (memories.length < 2) {
    return { pairs: [], stats: { total: 0, pairsFound: 0 } };
  }

  // Generate embeddings for all memories
  const embeddingMap = new Map(); // id → embedding

  await Promise.all(memories.map(async (mem) => {
    if (!mem.text) return;
    const emb = await getMemoryEmbedding(mem);
    if (emb) embeddingMap.set(mem.id, emb);
  }));

  const pairs = [];
  const seen = new Set();

  for (let i = 0; i < memories.length; i++) {
    const memA = memories[i];
    const embA = embeddingMap.get(memA.id);
    if (!embA) continue;

    for (let j = i + 1; j < memories.length; j++) {
      const memB = memories[j];
      const embB = embeddingMap.get(memB.id);
      if (!embB) continue;

      const sim = cosineSimilarity(embA, embB);
      if (sim >= threshold) {
        const key = [memA.id, memB.id].sort().join('__');
        if (!seen.has(key)) {
          seen.add(key);
          const { strategy, reason } = getMergeStrategy(sim);
          pairs.push({
            memoryA: { id: memA.id, text: memA.text.slice(0, 100), category: memA.category, created_at: memA.created_at },
            memoryB: { id: memB.id, text: memB.text.slice(0, 100), category: memB.category, created_at: memB.created_at },
            similarity: Math.round(sim * 10000) / 10000,
            strategy,
            reason,
          });
          if (pairs.length >= maxPairs) break;
        }
      }
    }
    if (pairs.length >= maxPairs) break;
  }

  // Sort by similarity descending
  pairs.sort((a, b) => b.similarity - a.similarity);

  const absorbCount = pairs.filter(p => p.strategy === 'absorb').length;
  const mergeCount = pairs.filter(p => p.strategy === 'merge').length;

  return {
    pairs,
    stats: {
      total: memories.length,
      pairsFound: pairs.length,
      absorbCandidates: absorbCount,
      mergeCandidates: mergeCount,
      threshold,
    },
  };
}

export default {
  cosineSimilarity,
  findDuplicateCandidates,
  findAllDuplicatePairs,
  classifySimilarity,
  getMergeStrategy,
  loadDedupLog,
  appendDedupLog,
  DEFAULT_SIMILARITY_THRESHOLD,
  ABSORB_THRESHOLD,
  MERGE_THRESHOLD,
};
