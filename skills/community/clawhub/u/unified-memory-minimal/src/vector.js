/**
 * Ollama 向量搜索 - 使用 nomic-embed-text 生成嵌入
 * 参考: memory_qmd_search.py 的向量搜索部分
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { config } from './config.js';
import { log } from './config.js';
import { getAllMemories, touchMemory } from './storage.js';
import { EmbeddingClient } from './embedding_providers.js';

// 全局 EmbeddingClient 实例（多provider自动切换）
const embeddingClient = new EmbeddingClient();

/**
 * Get embedding for text using the available embedding provider
 * @param {string} text
 * @returns {Promise<number[]|null>}
 */
export async function getEmbedding(text) {
  return await embeddingClient.embed(text);
}

/**
 * Get embedding (with caching) - 保留原有接口，兼容其他模块
 * @param {string} text
 * @returns {Promise<number[]|null>}
 */
const embeddingCache = new Map();

export async function getEmbeddingCached(text) {
  const hash = hashText(text);
  const cacheFile = join(config.vectorCacheDir, `${hash}.json`);

  if (existsSync(cacheFile)) {
    try {
      const cached = JSON.parse(readFileSync(cacheFile, 'utf8'));
      return cached.embedding;
    } catch {
      // ignore
    }
  }

  const embedding = await getEmbedding(text);
  if (embedding) {
    try {
      writeFileSync(cacheFile, JSON.stringify({ embedding, text: text.slice(0, 100) }), 'utf8');
    } catch {
      // ignore
    }
  }
  return embedding;
}

function hashText(text) {
  let hash = 0;
  for (let i = 0; i < text.length; i++) {
    const char = text.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return Math.abs(hash).toString(36);
}

/**
 * Cosine similarity
 * @param {number[]} a
 * @param {number[]} b
 * @returns {number}
 */
function cosineSimilarity(a, b) {
  if (a.length !== b.length) return 0;
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
 * Search by vector similarity
 * @param {string} query
 * @param {number} [topK=10]
 * @returns {Promise<Array<{memory: object, score: number, highlight: string}>>}
 */
export async function vectorSearch(query, topK = 10) {
  const memories = getAllMemories();
  if (!query || memories.length === 0) return [];

  const queryEmbedding = await getEmbeddingCached(query);
  if (!queryEmbedding) return [];

  const results = [];
  for (const mem of memories) {
    if (!mem.text) continue;
    const memEmbedding = await getEmbeddingCached(mem.text);
    if (!memEmbedding) continue;

    const score = cosineSimilarity(queryEmbedding, memEmbedding);
    if (score > 0.1) {
      let highlight = mem.text.slice(0, 150);
      if (mem.text.length > 150) highlight += '...';
      results.push({ memory: mem, score, highlight });
    }
  }

  results.sort((a, b) => b.score - a.score);
  return results.slice(0, topK);
}
