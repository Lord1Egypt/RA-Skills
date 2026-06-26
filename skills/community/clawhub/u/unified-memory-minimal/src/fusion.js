/**
 * RRF (Reciprocal Rank Fusion) - 混合 BM25 和向量搜索结果
 *
 * v3.0: 使用 vector_lancedb.js (LanceDB 持久化存储 + Ollama HTTP embedding)
 *       替代旧的 vector.js (Transformers.js 本地模型，每次都重新 embed 全量数据)
 * v3.1: 加入 rerank() 多信号重排 (keyword/entity/importance/recency/scope)
 */

import { config } from './config.js';
import { bm25Search } from './bm25.js';
import { vectorSearch } from './vector_lancedb.js';
import { rerank } from './rerank.js';

/**
 * Reciprocal Rank Fusion
 * @param {Array<{memory: object, score: number}>[]} resultLists
 * @param {number} [k=60]
 * @returns {Array<{memory: object, fusionScore: number, highlight: string}>}
 */
function reciprocalRankFusion(resultLists, k = 60) {
  const scores = new Map();

  for (const results of resultLists) {
    for (let i = 0; i < results.length; i++) {
      const mem = results[i].memory;
      const memId = mem.id;
      const rank = i + 1;
      const rrfScore = 1 / (k + rank);

      if (scores.has(memId)) {
        scores.get(memId).fusionScore += rrfScore;
      } else {
        scores.set(memId, {
          memory: mem,
          fusionScore: rrfScore,
          highlight: results[i].highlight || mem.text?.slice(0, 150),
        });
      }
    }
  }

  return Array.from(scores.values()).sort((a, b) => b.fusionScore - a.fusionScore);
}

/**
 * Hybrid search: BM25 + Vector with RRF fusion
 *
 * @param {string} query
 * @param {number} [topK=10]
 * @param {string} [mode='hybrid'] - 'hybrid', 'bm25', 'vector'
 * @param {string} [scope=null] - AGENT, USER, TEAM, GLOBAL
 * @returns {Promise<Array>}
 */
export async function hybridSearch(query, topK = 10, mode = 'hybrid', scope = null) {
  const k = config.rrfK || 60;
  const vectorEnabled = config.vectorEngine !== 'none';

  if (mode === 'bm25') {
    const results = bm25Search(query, topK * 2, scope);
    const mapped = results.map((r, i) => ({
      memory: r.memory,
      fusionScore: 1 / (k + i + 1),
      highlight: r.highlight,
      bm25Score: r.score,
    }));
    return rerank(query, mapped, { topK });
  }

  if (mode === 'vector') {
    if (!vectorEnabled) {
      // Fall back to BM25 when vector is disabled
      return hybridSearch(query, topK, 'bm25', scope);
    }
    const results = await vectorSearch(query, topK * 2, scope);
    const mapped = results.map((r, i) => ({
      memory: r.memory,
      fusionScore: 1 / (k + i + 1),
      highlight: r.highlight,
      vectorScore: r.score,
    }));
    return rerank(query, mapped, { topK });
  }

  // Hybrid: BM25 + Vector RRF (or BM25-only when vector disabled)
  let bm25Results, vectorResults;
  if (vectorEnabled) {
    [bm25Results, vectorResults] = await Promise.all([
      bm25Search(query, topK * 2, scope),
      vectorSearch(query, topK * 2, scope),
    ]);
  } else {
    bm25Results = bm25Search(query, topK * 2, scope);
    vectorResults = [];
  }

  const fused = reciprocalRankFusion([bm25Results, vectorResults], k);
  const preRerank = fused.slice(0, topK).map((r) => ({
    ...r,
    highlight: r.highlight || r.memory.text?.slice(0, 150),
  }));

  // v3.1: Re-rank using keyword overlap, entity match, recency, importance, scope
  const reranked = rerank(query, preRerank, { topK });
  // Normalize: use score (alias of rerankScore) for consistent API
  return reranked.map(r => ({
    ...r,
    score: r.rerankScore ?? r.score ?? r.fusionScore,
    fusionScore: r.fusionScore ?? r.score,
  }));
}
