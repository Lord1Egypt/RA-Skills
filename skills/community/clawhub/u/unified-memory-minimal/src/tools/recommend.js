/**
 * Memory Recommend - 智能关联推荐
 * 
 * 功能:
 * - 向量相似度推荐
 * - 共现关系推荐
 * - 标签关联推荐
 * - 综合推荐
 * 
 * Ported from memory_recommend.py
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const VECTOR_DB_DIR = join(MEMORY_DIR, 'vector');
const HISTORY_FILE = join(MEMORY_DIR, 'access_history.json');
const RECOMMEND_CACHE = join(MEMORY_DIR, 'recommend_cache.json');

const OLLAMA_HOST = process.env.OLLAMA_HOST || 'http://localhost:11434';
const OLLAMA_EMBED_MODEL = process.env.OLLAMA_EMBED_MODEL || 'nomic-embed-text:latest';

// ============================================================
// AccessHistory
// ============================================================

class AccessHistory {
  constructor() {
    this.history = this._loadHistory();
  }

  _loadHistory() {
    if (existsSync(HISTORY_FILE)) {
      try {
        return JSON.parse(readFileSync(HISTORY_FILE, 'utf-8'));
      } catch { /* ignore */ }
    }
    return { accesses: [], co_occurrences: {} };
  }

  save() {
    mkdirSync(MEMORY_DIR, { recursive: true });
    writeFileSync(HISTORY_FILE, JSON.stringify(this.history, null, 2), 'utf-8');
  }

  recordAccess(memId, context = '') {
    this.history.accesses.push({
      id: memId,
      timestamp: new Date().toISOString(),
      context
    });
    if (this.history.accesses.length > 1000) {
      this.history.accesses = this.history.accesses.slice(-1000);
    }
    this.save();
  }

  recordCoOccurrence(memIds) {
    for (let i = 0; i < memIds.length; i++) {
      for (let j = i + 1; j < memIds.length; j++) {
        const id1 = memIds[i];
        const id2 = memIds[j];
        const key = id1 < id2 ? `${id1}|${id2}` : `${id2}|${id1}`;
        this.history.co_occurrences[key] = (this.history.co_occurrences[key] || 0) + 1;
      }
    }
    this.save();
  }

  getCoOccurrences(memId) {
    const result = {};
    for (const [key, count] of Object.entries(this.history.co_occurrences || {})) {
      const ids = key.split('|');
      if (ids.includes(memId)) {
        const otherId = ids[0] === memId ? ids[1] : ids[0];
        result[otherId] = count;
      }
    }
    return result;
  }
}

// ============================================================
// MemoryRecommender
// ============================================================

class MemoryRecommender {
  constructor() {
    this.memories = this._loadMemories();
    this.history = new AccessHistory();
    this.embeddings = new Map();
  }

  _loadMemories() {
    try {
      const { getAllMemories } = require('../storage.js');
      return getAllMemories();
    } catch {
      const memoryFile = join(MEMORY_DIR, 'memories.json');
      if (existsSync(memoryFile)) {
        try {
          const data = JSON.parse(readFileSync(memoryFile, 'utf-8'));
          return Array.isArray(data) ? data : (data.memories || []);
        } catch { /* ignore */ }
      }
      return [];
    }
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

  async recommendByVector(query, k = 5) {
    try {
      // Use LanceDB ANN index instead of brute-force full memory scan
      const { vectorSearch } = await import('../vector_lancedb.js');
      const results = await vectorSearch(query, k, null);
      return results.map(r => ({
        memory: r.memory,
        score: Math.round((r.score || 0.5) * 1000) / 1000,
        type: 'vector'
      }));
    } catch {
      // Fallback to embedding-based scan
      const queryVec = await this._getEmbedding(query);
      if (!queryVec) return [];

      const scores = [];
      for (const mem of this.memories) {
        const memVec = mem.vector || mem.embedding;
        if (!memVec) continue;
        const sim = this._cosineSimilarity(queryVec, memVec);
        if (sim > 0) scores.push({ mem, sim });
      }

      scores.sort((a, b) => b.sim - a.sim);
      return scores.slice(0, k).map(({ mem, sim }) => ({
        memory: mem,
        score: Math.round(sim * 1000) / 1000,
        type: 'vector'
      }));
    }
  }

  recommendByCoOccurrence(memId, k = 5) {
    const coMem = this.history.getCoOccurrences(memId);
    if (!coMem || Object.keys(coMem).length === 0) return [];

    const sorted = Object.entries(coMem)
      .sort(([, a], [, b]) => b - a)
      .slice(0, k);

    return sorted.map(([otherId, count]) => {
      const mem = this.memories.find(m => m.id === otherId);
      if (!mem) return null;
      return {
        memory: mem,
        score: Math.round((count / 10) * 1000) / 1000,
        type: 'co_occurrence',
        co_count: count
      };
    }).filter(Boolean);
  }

  recommendByTags(tags, k = 5) {
    if (!tags || tags.length === 0) return [];
    const queryTags = new Set(tags.map(t => t.toLowerCase()));

    const scores = [];
    for (const mem of this.memories) {
      const memTags = new Set((mem.tags || []).map(t => t.toLowerCase()));
      const intersection = new Set([...queryTags].filter(t => memTags.has(t)));
      const union = new Set([...queryTags, ...memTags]);
      if (union.size > 0 && intersection.size > 0) {
        scores.push({ mem, jaccard: intersection.size / union.size });
      }
    }

    scores.sort((a, b) => b.jaccard - a.jaccard);
    return scores.slice(0, k).map(({ mem, jaccard }) => ({
      memory: mem,
      score: Math.round(jaccard * 1000) / 1000,
      type: 'tag'
    }));
  }

  async recommendCombined(query, contextIds = null, k = 5) {
    /** @type {Map<string, {memory: object, scores: object}>} */
    const results = new Map();

    // Vector
    const vectorResults = await this.recommendByVector(query, k * 2);
    for (const r of vectorResults) {
      results.set(r.memory.id, { memory: r.memory, scores: { vector: r.score } });
    }

    // Tags
    const queryTags = this._extractTags(query);
    const tagResults = this.recommendByTags(queryTags, k * 2);
    for (const r of tagResults) {
      if (results.has(r.memory.id)) {
        results.get(r.memory.id).scores.tag = r.score;
      } else {
        results.set(r.memory.id, { memory: r.memory, scores: { tag: r.score } });
      }
    }

    // Co-occurrence
    if (contextIds && contextIds.length > 0) {
      for (const ctxId of contextIds.slice(0, 3)) {
        const coResults = this.recommendByCoOccurrence(ctxId, k);
        for (const r of coResults) {
          if (results.has(r.memory.id)) {
            results.get(r.memory.id).scores.co_occurrence = r.score;
          } else {
            results.set(r.memory.id, { memory: r.memory, scores: { co_occurrence: r.score } });
          }
        }
      }
    }

    // Combine scores
    /** @type {Array} */
    const finalResults = [];
    for (const [, data] of results) {
      const scores = data.scores;
      const combined =
        (scores.vector || 0) * 0.5 +
        (scores.tag || 0) * 0.3 +
        (scores.co_occurrence || 0) * 0.2;
      const importance = data.memory.importance || 0.5;
      const finalScore = combined * 0.7 + importance * 0.3;
      finalResults.push({
        memory: data.memory,
        score: Math.round(finalScore * 1000) / 1000,
        type: 'combined',
        breakdown: scores
      });
    }

    finalResults.sort((a, b) => b.score - a.score);

    // Record co-occurrence
    if (finalResults.length > 1) {
      const ids = finalResults.slice(0, 5).map(r => r.memory.id);
      this.history.recordCoOccurrence(ids);
    }

    return finalResults.slice(0, k);
  }

  _extractTags(text) {
    const keywords = new Set([
      '飞书', '微信', 'QQ', '龙宫', '项目', '电商',
      '偏好', '协作', '管理', '记忆系统', 'EvoMap',
      '刘总', '会议', '任务', '决策'
    ]);
    const found = [];
    for (const kw of keywords) {
      if (text.includes(kw)) found.push(kw);
    }
    return found;
  }

  getHotMemories(days = 7, k = 5) {
    const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;
    /** @type {Map<string, number>} */
    const accessCount = new Map();

    for (const acc of this.history.history.accesses || []) {
      const ts = acc.timestamp;
      if (!ts) continue;
      const accMs = new Date(ts).getTime();
      if (accMs > cutoff) {
        accessCount.set(acc.id, (accessCount.get(acc.id) || 0) + 1);
      }
    }

    const hotIds = [...accessCount.entries()]
      .sort(([, a], [, b]) => b - a)
      .slice(0, k)
      .map(([id]) => id);

    return hotIds.map(memId => {
      const mem = this.memories.find(m => m.id === memId);
      if (!mem) return null;
      return { memory: mem, access_count: accessCount.get(memId) || 0, type: 'hot' };
    }).filter(Boolean);
  }

  getRecommendationsForContext(context, currentMemories = null, k = 3) {
    // Sync wrapper
    return this._getRecommendationsForContext(context, currentMemories, k);
  }

  async _getRecommendationsForContext(context, currentMemories = null, k = 3) {
    const recommendations = await this.recommendCombined(context, currentMemories, k);
    return {
      query: context,
      recommendations: recommendations.map(r => ({
        id: r.memory.id,
        text: ((r.memory.text || '').slice(0, 100)) + (((r.memory.text || '').length > 100) ? '...' : ''),
        score: r.score,
        type: r.type,
        reason: this._explainRecommendation(r)
      })),
      timestamp: new Date().toISOString()
    };
  }

  _explainRecommendation(result) {
    const scores = result.breakdown || {};
    const reasons = [];
    if ((scores.vector || 0) > 0.5) reasons.push('语义相似');
    if ((scores.tag || 0) > 0.3) reasons.push('标签关联');
    if ((scores.co_occurrence || 0) > 0.1) reasons.push('经常一起出现');
    if ((result.memory.importance || 0) > 0.7) reasons.push('重要性高');
    return reasons.join('、') || '综合推荐';
  }
}

// ============================================================
// CLI Handler
// ============================================================

/**
 * @param {string} command
 * @param {object} args
 * @returns {Promise<object>}
 */
export async function cmdRecommend(command, args) {
  const recommender = new MemoryRecommender();

  switch (command) {
    case 'recommend': {
      if (!args.query) return { error: '请提供 --query' };
      const results = await recommender.recommendCombined(args.query, null, parseInt(args.k) || 5);
      if (args.json) return { type: 'json', data: results };
      const lines = [`🔍 智能推荐: ${args.query}`, `\n找到 ${results.length} 条推荐:`];
      results.forEach((r, i) => {
        lines.push(`\n${i + 1}. [${r.type}] ${((r.memory.text || '').slice(0, 80))}...`);
        lines.push(`   评分: ${r.score.toFixed(3)}`);
      });
      return { type: 'text', text: lines.join('\n') };
    }

    case 'hot': {
      const results = recommender.getHotMemories(7, parseInt(args.k) || 5);
      if (args.json) return { type: 'json', data: results };
      const lines = [`🔥 热点记忆 (最近 7 天)`];
      results.forEach((r, i) => {
        lines.push(`${i + 1}. [访问 ${r.access_count} 次] ${((r.memory.text || '').slice(0, 60))}...`);
      });
      return { type: 'text', text: lines.join('\n') };
    }

    case 'related': {
      if (!args.id) return { error: '请提供 --id' };
      const results = recommender.recommendByCoOccurrence(args.id, parseInt(args.k) || 5);
      if (args.json) return { type: 'json', data: results };
      const lines = [`🔗 相关记忆: ${args.id.slice(0, 8)}...`];
      results.forEach((r, i) => {
        lines.push(`${i + 1}. [共现 ${r.co_count} 次] ${((r.memory.text || '').slice(0, 60))}...`);
      });
      return { type: 'text', text: lines.join('\n') };
    }

    case 'context': {
      if (!args.query) return { error: '请提供 --query' };
      const result = await recommender.getRecommendationsForContext(args.query, null, parseInt(args.k) || 3);
      return { type: 'json', data: result };
    }

    default:
      return { error: `未知命令: ${command}` };
  }
}

export default { cmdRecommend };
