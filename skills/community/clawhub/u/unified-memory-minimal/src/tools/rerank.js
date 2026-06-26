/**
 * Memory Rerank - Cross-Encoder 重排序
 * 
 * QMD 的核心优势：对 BM25+Vector 结果进行 Rerank
 * 
 * Ported from memory_rerank.py
 */

import { existsSync, readFileSync, writeFileSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');

const OLLAMA_HOST = process.env.OLLAMA_HOST || 'http://localhost:11434';
const OLLAMA_EMBED_MODEL = process.env.OLLAMA_EMBED_MODEL || 'nomic-embed-text:latest';

// ============================================================
// CrossEncoderRerank
// ============================================================

export class CrossEncoderRerank {
  constructor() {
    this.model = null;
    this.embeddings = new Map();
  }

  async _loadModel() {
    // No external model loading in Node.js environment
    // Fall back to simple reranking
    this.model = null;
  }

  /**
   * Rerank search results using cross-encoder
   * @param {string} query
   * @param {Array<object>} results - BM25+Vector hybrid search results
   * @param {number} topK
   * @returns {Promise<Array<object>>}
   */
  async rerank(query, results, topK = 10) {
    if (!results || results.length === 0) return [];

    await this._loadModel();

    if (this.model === null) {
      return this._simpleRerank(query, results, topK);
    }

    try {
      // Cross-encoder scoring would go here
      // For now, fall back to simple reranking
      return this._simpleRerank(query, results, topK);
    } catch (e) {
      return results.slice(0, topK);
    }
  }

  _simpleRerank(query, results, topK) {
    const queryWords = new Set(query.toLowerCase().split(/\s+/));

    for (const r of results) {
      const text = (r.text || '').toLowerCase();
      const textWords = new Set(text.split(/\s+/));

      // Keyword overlap
      let overlap = 0;
      for (const w of queryWords) {
        if (text.includes(w)) overlap++;
      }

      const originalScore = r.score || r.fusionScore || r.hybrid_score || 0;
      r.cross_score = overlap / Math.max(queryWords.size, 1);
      r.final_score = originalScore * 0.5 + r.cross_score * 0.5;
    }

    results.sort((a, b) => (b.final_score || 0) - (a.final_score || 0));
    return results.slice(0, topK);
  }

  /**
   * Async rerank with Ollama embeddings
   * @param {string} query
   * @param {Array<object>} results
   * @param {number} topK
   * @returns {Promise<Array<object>>}
   */
  async rerankWithEmbeddings(query, results, topK = 10) {
    if (!results || results.length === 0) return [];

    // Get query embedding
    let queryVec = null;
    try {
      queryVec = await this._getEmbedding(query);
    } catch { /* ignore */ }

    for (const r of results) {
      let simScore = 0;
      if (queryVec && r.embedding) {
        simScore = this._cosineSimilarity(queryVec, r.embedding);
      }

      // Keyword overlap
      const queryWords = new Set(query.toLowerCase().split(/\s+/));
      const textWords = new Set(((r.text || '').toLowerCase()).split(/\s+/));
      const overlap = [...queryWords].filter(w => textWords.has(w)).length / Math.max(queryWords.size, 1);

      const originalScore = r.score || r.fusionScore || r.hybrid_score || 0;

      // Hybrid: original 30% + cross-encoder-style 70%
      r.cross_score = Math.max(simScore, overlap);
      r.final_score = originalScore * 0.3 + r.cross_score * 0.7;
    }

    results.sort((a, b) => (b.final_score || 0) - (a.final_score || 0));
    return results.slice(0, topK);
  }

  async _getEmbedding(text) {
    const cacheKey = text.slice(0, 50);
    if (this.embeddings.has(cacheKey)) {
      return this.embeddings.get(cacheKey);
    }

    try {
      const response = await fetch(`${OLLAMA_HOST}/api/embeddings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model: OLLAMA_EMBED_MODEL, prompt: text }),
        signal: AbortSignal.timeout(10000)
      });
      if (response.ok) {
        const data = await response.json();
        const embedding = data.embedding || null;
        if (embedding) this.embeddings.set(cacheKey, embedding);
        return embedding;
      }
    } catch { /* ignore */ }
    return null;
  }

  _cosineSimilarity(v1, v2) {
    if (!v1 || !v2 || v1.length !== v2.length) return 0;
    const dot = v1.reduce((s, a, i) => s + a * v2[i], 0);
    const norm1 = Math.sqrt(v1.reduce((s, a) => s + a * a, 0));
    const norm2 = Math.sqrt(v2.reduce((s, b) => s + b * b, 0));
    if (norm1 === 0 || norm2 === 0) return 0;
    return dot / (norm1 * norm2);
  }
}

// ============================================================
// Convenience function
// ============================================================

/**
 * Rerank results
 * @param {string} query
 * @param {Array<object>} results
 * @param {number} topK
 * @returns {Promise<Array<object>>}
 */
export async function rerankResults(query, results, topK = 10) {
  const reranker = new CrossEncoderRerank();
  return reranker.rerankWithEmbeddings(query, results, topK);
}

export default { CrossEncoderRerank, rerankResults };