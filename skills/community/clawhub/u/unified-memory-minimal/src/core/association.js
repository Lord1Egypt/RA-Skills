/**
 * Memory Association - 记忆关联推荐
 * 
 * 功能:
 * - 基于向量相似度推荐相关记忆
 * - 基于共现关系推荐关联记忆
 * - 基于标签关联推荐
 * 
 * Ported from memory_association.py
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const VECTOR_DB_DIR = join(MEMORY_DIR, 'vector');
const ASSOCIATION_GRAPH_FILE = join(MEMORY_DIR, 'associations', 'graph.json');

const OLLAMA_URL = process.env.OLLAMA_HOST || 'http://localhost:11434';
const OLLAMA_EMBED_MODEL = process.env.OLLAMA_EMBED_MODEL || 'nomic-embed-text:latest';

// ============================================================
// Utilities
// ============================================================

/**
 * @typedef {Object} Memory
 * @property {string} id
 * @property {string} text
 * @property {string} category
 * @property {number} importance
 * @property {string[]} tags
 * @property {string} timestamp
 * @property {string} created_at
 * @property {number[]} embedding
 */

/**
 * @typedef {Object} AssociationResult
 * @property {Memory} memory
 * @property {number} score
 * @property {string[]} reasons
 */

/**
 * Get embedding from Ollama
 * @param {string} text
 * @returns {Promise<number[]|null>}
 */
async function getEmbedding(text) {
  try {
    const response = await fetch(`${OLLAMA_URL}/api/embeddings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: OLLAMA_EMBED_MODEL, prompt: text }),
      signal: AbortSignal.timeout(10000)
    });
    if (response.ok) {
      const data = await response.json();
      return data.embedding || null;
    }
  } catch {
    // ignore
  }
  return null;
}

/**
 * Cosine similarity between two vectors
 * @param {number[]} vec1
 * @param {number[]} vec2
 * @returns {number}
 */
function cosineSimilarity(vec1, vec2) {
  if (!vec1 || !vec2 || vec1.length !== vec2.length) return 0;
  const dot = vec1.reduce((sum, a, i) => sum + a * vec2[i], 0);
  const norm1 = Math.sqrt(vec1.reduce((s, a) => s + a * a, 0));
  const norm2 = Math.sqrt(vec2.reduce((s, b) => s + b * b, 0));
  if (norm1 === 0 || norm2 === 0) return 0;
  return dot / (norm1 * norm2);
}

// ============================================================
// MemoryAssociation
// ============================================================

export class MemoryAssociation {
  constructor() {
    /** @type {Memory[]} */
    this.memories = this._loadMemories();
    /** @type {{ nodes: object, edges: object }} */
    this.graph = this._loadGraph();
    /** @type {Map<string, Map<string, number>>} */
    this.coOccurrence = new Map();
  }

  /**
   * Load memories
   * @returns {Memory[]}
   */
  _loadMemories() {
    try {
      const { getAllMemories } = require('../storage.js');
      return getAllMemories();
    } catch {
      // fallback
    }

    const memoryFile = join(MEMORY_DIR, 'memories.json');
    if (existsSync(memoryFile)) {
      try {
        const data = JSON.parse(readFileSync(memoryFile, 'utf-8'));
        return Array.isArray(data) ? data : (data.memories || []);
      } catch {
        // ignore
      }
    }
    return [];
  }

  /**
   * Load association graph
   * @returns {{ nodes: object, edges: object }}
   */
  _loadGraph() {
    if (existsSync(ASSOCIATION_GRAPH_FILE)) {
      try {
        return JSON.parse(readFileSync(ASSOCIATION_GRAPH_FILE, 'utf-8'));
      } catch {
        // ignore
      }
    }
    return { nodes: {}, edges: {} };
  }

  /**
   * Save association graph
   */
  _saveGraph() {
    mkdirSync(join(MEMORY_DIR, 'associations'), { recursive: true });
    writeFileSync(ASSOCIATION_GRAPH_FILE, JSON.stringify(this.graph, null, 2), 'utf-8');
  }

  /**
   * Build co-occurrence matrix (memories from same day)
   */
  _buildCoOccurrence() {
    if (this.coOccurrence.size > 0) return; // already built

    /** @type {Map<string, string[]>} */
    const byDate = new Map();
    for (const mem of this.memories) {
      const createdAt = mem.created_at || mem.timestamp;
      if (!createdAt) continue;
      const dateKey = createdAt.slice(0, 10); // YYYY-MM-DD
      if (!byDate.has(dateKey)) byDate.set(dateKey, []);
      byDate.get(dateKey).push(mem.id);
    }

    for (const [, memIds] of byDate) {
      for (let i = 0; i < memIds.length; i++) {
        for (let j = i + 1; j < memIds.length; j++) {
          const id1 = memIds[i];
          const id2 = memIds[j];
          if (!this.coOccurrence.has(id1)) this.coOccurrence.set(id1, new Map());
          if (!this.coOccurrence.has(id2)) this.coOccurrence.set(id2, new Map());
          this.coOccurrence.get(id1).set(id2, (this.coOccurrence.get(id1).get(id2) || 0) + 1);
          this.coOccurrence.get(id2).set(id1, (this.coOccurrence.get(id2).get(id1) || 0) + 1);
        }
      }
    }
  }

  /**
   * Find memory by ID
   * @param {string} memoryId
   * @returns {Memory|null}
   */
  _findMemory(memoryId) {
    return this.memories.find(m => m.id === memoryId) || null;
  }

  // ============================================================
  // Recommendation Strategies
  // ============================================================

  /**
   * Recommend by vector similarity
   * @param {string} memoryId
   * @param {number} topK
   * @returns {Promise<Array<{memory: Memory, score: number, reason: string}>>}
   */
  async recommendBySimilarity(memoryId, topK = 5) {
    const target = this._findMemory(memoryId);
    if (!target) return [];

    let targetEmbedding = target.embedding;
    if (!targetEmbedding) {
      targetEmbedding = await getEmbedding(target.text || '');
    }
    if (!targetEmbedding) return [];

    /** @type {Array<{memory: Memory, score: number, reason: string}>} */
    const similarities = [];

    for (const mem of this.memories) {
      if (mem.id === memoryId) continue;

      let memEmbedding = mem.embedding;
      if (!memEmbedding) {
        memEmbedding = await getEmbedding(mem.text || '');
      }
      if (!memEmbedding) continue;

      const sim = cosineSimilarity(targetEmbedding, memEmbedding);
      if (sim > 0.5) {
        similarities.push({ memory: mem, score: sim, reason: 'vector_similarity' });
      }
    }

    similarities.sort((a, b) => b.score - a.score);
    return similarities.slice(0, topK);
  }

  /**
   * Recommend by co-occurrence
   * @param {string} memoryId
   * @param {number} topK
   * @returns {Array<{memory: Memory, score: number, reason: string}>}
   */
  recommendByCoOccurrence(memoryId, topK = 5) {
    this._buildCoOccurrence();

    const target = this._findMemory(memoryId);
    if (!target) return [];

    const coMem = this.coOccurrence.get(memoryId);
    if (!coMem) return [];

    const results = [];
    const sorted = [...coMem.entries()].sort((a, b) => b[1] - a[1]).slice(0, topK);

    for (const [relatedId, count] of sorted) {
      const mem = this._findMemory(relatedId);
      if (mem) {
        results.push({ memory: mem, score: count, reason: 'co_occurrence' });
      }
    }

    return results;
  }

  /**
   * Recommend by tag similarity
   * @param {string} memoryId
   * @param {number} topK
   * @returns {Array<{memory: Memory, score: number, reason: string}>}
   */
  recommendByTags(memoryId, topK = 5) {
    const target = this._findMemory(memoryId);
    if (!target) return [];

    const targetText = (target.text || '').toLowerCase();

    // Extract target tags (keywords)
    const keywords = ['飞书', '微信', '项目', '协作', '任务', '记忆', '系统', '偏好', '决策'];
    const targetTags = new Set();
    for (const kw of keywords) {
      if (targetText.includes(kw)) targetTags.add(kw);
    }

    const targetCategory = target.category || '';

    /** @type {Array<{memory: Memory, score: number, reason: string}>} */
    const results = [];

    for (const mem of this.memories) {
      if (mem.id === memoryId) continue;

      let score = 0;

      // Same category bonus
      if ((mem.category || '') === targetCategory) {
        score += 0.5;
      }

      // Tag overlap bonus
      const memText = (mem.text || '').toLowerCase();
      let overlap = 0;
      for (const tag of targetTags) {
        if (memText.includes(tag)) overlap++;
      }
      score += overlap * 0.3;

      if (score > 0) {
        results.push({ memory: mem, score, reason: 'tag_similarity' });
      }
    }

    results.sort((a, b) => b.score - a.score);
    return results.slice(0, topK);
  }

  /**
   * Comprehensive recommendation (fuse multiple strategies)
   * @param {string} memoryId
   * @param {number} topK
   * @returns {Promise<Array<{memory: Memory, score: number, reasons: string[]}>>}
   */
  async recommend(memoryId, topK = 5) {
    // Get results from all strategies
    const bySim = await this.recommendBySimilarity(memoryId, topK * 2);
    const byCo = this.recommendByCoOccurrence(memoryId, topK);
    const byTag = this.recommendByTags(memoryId, topK * 2);

    // Merge scores
    /** @type {Map<string, {score: number, reasons: Set<string>, memory: Memory}>} */
    const scores = new Map();

    for (const item of bySim) {
      const id = item.memory.id;
      if (!scores.has(id)) scores.set(id, { score: 0, reasons: new Set(), memory: item.memory });
      scores.get(id).score += item.score * 0.5;
      scores.get(id).reasons.add('相似度');
    }

    for (const item of byCo) {
      const id = item.memory.id;
      if (!scores.has(id)) scores.set(id, { score: 0, reasons: new Set(), memory: item.memory });
      scores.get(id).score += item.score * 0.3;
      scores.get(id).reasons.add('共现');
    }

    for (const item of byTag) {
      const id = item.memory.id;
      if (!scores.has(id)) scores.set(id, { score: 0, reasons: new Set(), memory: item.memory });
      scores.get(id).score += item.score * 0.2;
      scores.get(id).reasons.add('标签');
    }

    // Sort and dedupe
    /** @type {Array<{memory: Memory, score: number, reasons: string[]}>} */
    const results = [];
    for (const [, v] of scores) {
      if (v.memory && v.memory.id !== memoryId) {
        results.push({
          memory: v.memory,
          score: Math.round(v.score * 1000) / 1000,
          reasons: [...v.reasons]
        });
      }
    }

    results.sort((a, b) => b.score - a.score);
    return results.slice(0, topK);
  }

  /**
   * Build the association graph
   * @returns {{ nodes: number, edges: number, saved: string }}
   */
  buildGraph() {
    this._buildCoOccurrence();

    /** @type {object} */
    const nodes = {};
    /** @type {object} */
    const edges = {};

    for (const mem of this.memories) {
      const memId = mem.id;
      nodes[memId] = {
        text: (mem.text || '').slice(0, 50),
        category: mem.category,
        importance: mem.importance || 0.5
      };
    }

    for (const [memId, coMap] of this.coOccurrence) {
      for (const [relatedId, count] of coMap) {
        const edgeKey = `${memId}_${relatedId}`;
        if (!edges[edgeKey]) {
          edges[edgeKey] = {
            source: memId,
            target: relatedId,
            weight: count,
            type: 'co_occurrence'
          };
        }
      }
    }

    this.graph = { nodes, edges };
    this._saveGraph();

    return {
      nodes: Object.keys(nodes).length,
      edges: Object.keys(edges).length,
      saved: ASSOCIATION_GRAPH_FILE
    };
  }

  /**
   * Find related memories for a query (with association expansion)
   * @param {string} query
   * @param {number} topK
   * @returns {Promise<Array<{memory: Memory, score: number, reasons: string[]}>>}
   */
  async relatedToQuery(query, topK = 5) {
    const queryLower = query.toLowerCase();
    /** @type {Array<{memory: Memory, score: number, reasons: string[]}>} */
    let results = [];

    // Direct match
    for (const mem of this.memories) {
      if ((mem.text || '').toLowerCase().includes(queryLower)) {
        results.push({ memory: mem, score: 1.0, reasons: ['直接匹配'] });
      }
    }

    // If we have results, expand with associations
    if (results.length > 0) {
      const topResult = results[0];
      const related = await this.recommend(topResult.memory.id, topK);

      const seenIds = new Set(results.map(r => r.memory.id));
      for (const rel of related) {
        if (!seenIds.has(rel.memory.id)) {
          rel.reasons.push('关联推荐');
          results.push(rel);
          seenIds.add(rel.memory.id);
        }
      }
    }

    results.sort((a, b) => b.score - a.score);
    return results.slice(0, topK);
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
export async function cmdAssociation(command, args) {
  const association = new MemoryAssociation();

  switch (command) {
    case 'recommend': {
      if (!args.memoryId) return { error: '请指定 --memory-id' };
      const results = await association.recommend(args.memoryId, parseInt(args.topK) || 5);
      const lines = [`📋 推荐关联记忆 (top ${results.length}):`];
      results.forEach((item, i) => {
        const text = (item.memory.text || '').slice(0, 60);
        const reasons = item.reasons.join('+');
        lines.push(`  ${i + 1}. [${reasons}] ${text}... (score: ${item.score.toFixed(2)})`);
      });
      return { type: 'text', text: lines.join('\n') };
    }

    case 'related': {
      if (!args.query) return { error: '请指定 --query' };
      const results = await association.relatedToQuery(args.query, parseInt(args.topK) || 5);
      const lines = [`📋 相关记忆 (top ${results.length}):`];
      results.forEach((item, i) => {
        const text = (item.memory.text || '').slice(0, 60);
        const reasons = item.reasons.join('+');
        lines.push(`  ${i + 1}. [${reasons}] ${text}...`);
      });
      return { type: 'text', text: lines.join('\n') };
    }

    case 'build-graph': {
      const result = association.buildGraph();
      return {
        type: 'text',
        text: `✅ 关联图已构建:\n  节点: ${result.nodes}\n  边: ${result.edges}\n  保存到: ${result.saved}`
      };
    }

    default:
      return { error: `未知命令: ${command}` };
  }
}

export default {
  MemoryAssociation,
  cmdAssociation
};
