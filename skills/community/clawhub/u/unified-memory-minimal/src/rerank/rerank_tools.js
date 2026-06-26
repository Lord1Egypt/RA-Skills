/**
 * Rerank Tools v2 — LLM Cross-Encoder Reranking
 *
 * Provides:
 * - memory_rerank(query, memoryIds, topK): LLM rerank specified memories
 * - memory_search_reranked(query, topK, useRerank): Search + rerank pipeline
 */

import { z } from 'zod';
import { rerankWithLLM } from './cross_encoder.js';
import { getAllMemories } from '../storage.js';
import { hybridSearch } from '../fusion.js';

// ============================================================
// memory_rerank
// ============================================================

/**
 * Rerank specified memories by ID using LLM cross-encoder scoring
 *
 * @param {string} query - Search query
 * @param {string[]} memoryIds - Array of memory IDs to rerank
 * @param {number} [topK=5] - Number of top results to return
 * @returns {Promise<object>} - { reranked: [...], original_order: [...] }
 */
export async function memory_rerank({ query, memoryIds, topK = 5 }) {
  if (!memoryIds || memoryIds.length === 0) {
    return { reranked: [], original_order: [] };
  }

  const allMemories = await getAllMemories();
  const candidates = allMemories.filter((m) => memoryIds.includes(m.id));

  if (candidates.length === 0) {
    return { reranked: [], original_order: [] };
  }

  // Preserve original order for comparison
  const original_order = [...candidates];

  const reranked = await rerankWithLLM(query, candidates, topK);

  return { reranked, original_order };
}

// ============================================================
// memory_search_reranked
// ============================================================

/**
 * Hybrid search + LLM rerank pipeline
 *
 * @param {string} query - Search query
 * @param {number} [topK=10] - Number of results to return
 * @param {boolean} [useRerank=true] - Whether to apply LLM reranking
 * @returns {Promise<object>} - { results: [...], reranked: bool, search_time_ms: number }
 */
export async function memory_search_reranked({ query, topK = 10, useRerank = true }) {
  const startTime = Date.now();

  if (!query || query.trim() === '') {
    return { results: [], reranked: false, search_time_ms: Date.now() - startTime };
  }

  // Step 1: Initial search (vector + BM25 hybrid)
  let initialResults;
  try {
    if (hybridSearch) {
      const raw = await hybridSearch(query, topK * 3, 'hybrid');
      initialResults = Array.isArray(raw) ? raw : (raw?.results || []);
    } else {
      // Last fallback: simple text match from all memories
      const allMemories = await getAllMemories();
      initialResults = allMemories
        .filter((m) => {
          const text = (m.text || '').toLowerCase();
          const q = query.toLowerCase();
          return text.includes(q);
        })
        .slice(0, topK * 3)
        .map((m) => ({ memory: m, score: 1, text: m.text }));
    }
  } catch (err) {
    console.warn(`[RerankTools] Search failed: ${err.message}, falling back to all memories`);
    const allMemories = await getAllMemories();
    initialResults = allMemories.slice(0, topK * 3).map((m) => ({ memory: m, score: 0.5, text: m.text }));
  }

  if (!initialResults || initialResults.length === 0) {
    return { results: [], reranked: false, search_time_ms: Date.now() - startTime };
  }

  // Normalize: support both {memory: {...}} and direct memory object forms
  const candidates = initialResults.map((r) =>
    typeof r === 'object' && r.memory ? r.memory : r
  );

  // Step 2: Optional LLM reranking
  let finalResults = candidates;
  let reranked = false;

  if (useRerank && candidates.length > 1) {
    try {
      finalResults = await rerankWithLLM(query, candidates, topK);
      reranked = true;
    } catch (err) {
      console.warn(`[RerankTools] Reranking failed: ${err.message}, using search order`);
      finalResults = candidates.slice(0, topK);
    }
  } else {
    finalResults = candidates.slice(0, topK);
  }

  return {
    results: finalResults,
    reranked,
    search_time_ms: Date.now() - startTime,
  };
}

export default { memory_rerank, memory_search_reranked };

export function registerRerankTools(server) {
  server.registerTool('memory_rerank', {
    description: 'Rerank specified memories using LLM cross-encoder.',
    inputSchema: z.object({
      query: z.string().describe('Original search query'),
      memoryIds: z.array(z.string()).describe('Memory IDs to rerank'),
      topK: z.number().optional().default(5).describe('Return top K results'),
    }),
  }, memory_rerank);

  server.registerTool('memory_search_reranked', {
    description: 'Search memories with LLM reranking pipeline.',
    inputSchema: z.object({
      query: z.string().describe('Search query'),
      topK: z.number().optional().default(10).describe('Return top K results'),
      useRerank: z.boolean().optional().default(true),
    }),
  }, memory_search_reranked);
}
