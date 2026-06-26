/**
 * Memory Search - 增强搜索体验
 * 
 * 功能:
 * - 自然语言搜索
 * - 多维度过滤器
 * - 搜索历史
 * - 模糊匹配
 * 
 * Ported from memory_search.py
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'fs';
import { join } from 'path';
import { cosineSimilarity, getEmbedding } from '../utils/text.js';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const VECTOR_DB_DIR = join(MEMORY_DIR, 'vector');
const SEARCH_HISTORY_FILE = join(MEMORY_DIR, 'search_history.json');
const OLLAMA_HOST = process.env.OLLAMA_HOST || 'http://localhost:11434';
const OLLAMA_EMBED_MODEL = process.env.OLLAMA_EMBED_MODEL || 'nomic-embed-text:latest';

// ============================================================
// Search History
// ============================================================

/**
 * @typedef {Object} SearchHistory
 * @property {Array<{query: string, timestamp: string, results: number}>} searches
 * @property {string[]} recent
 */

/**
 * Load search history from disk
 * @returns {SearchHistory}
 */
export function loadHistory() {
  if (existsSync(SEARCH_HISTORY_FILE)) {
    try {
      return JSON.parse(readFileSync(SEARCH_HISTORY_FILE, 'utf-8'));
    } catch {
      // ignore
    }
  }
  return { searches: [], recent: [] };
}

/**
 * Save search history to disk
 * @param {SearchHistory} history
 */
export function saveHistory(history) {
  try {
    mkdirSync(MEMORY_DIR, { recursive: true });
    writeFileSync(SEARCH_HISTORY_FILE, JSON.stringify(history, null, 2), 'utf-8');
  } catch (e) {
    // ignore
  }
}

/**
 * Record a search in history
 * @param {string} query
 * @param {number} resultCount
 */
export function recordSearch(query, resultCount) {
  const history = loadHistory();
  history.searches.push({
    query,
    timestamp: new Date().toISOString(),
    results: resultCount
  });
  // Keep last 50
  if (history.searches.length > 50) {
    history.searches = history.searches.slice(-50);
  }
  // Update recent
  if (!history.recent.includes(query)) {
    history.recent = [query, ...history.recent.slice(0, 9)];
  }
  saveHistory(history);
}

// ============================================================
// Core Search
// ============================================================

/**
 * Text similarity (Jaccard word overlap)
 * @param {string} query
 * @param {string} text
 * @returns {number}
 */
export function textSimilarity(query, text) {
  const queryWords = new Set(query.toLowerCase().split(/\s+/));
  const textWords = new Set(text.toLowerCase().split(/\s+/));
  if (queryWords.size === 0 || textWords.size === 0) return 0;
  const intersection = new Set([...queryWords].filter(w => textWords.has(w)));
  const union = new Set([...queryWords, ...textWords]);
  return intersection.size / union.size;
}

/**
 * Fallback keyword search
 * @param {Array} memories
 * @param {string} query
 * @param {number} k
 * @returns {Array}
 */
export function fallbackSearch(memories, query, k = 10) {
  const queryLower = query.toLowerCase();
  const results = [];

  for (const mem of memories) {
    const textLower = (mem.text || '').toLowerCase();
    let score = 0;

    // Exact contains
    if (textLower.includes(queryLower)) {
      score = 1.0;
    } else {
      const queryWords = new Set(queryLower.split(/\s+/));
      const textWords = new Set(textLower.split(/\s+/));
      const overlap = queryWords.size > 0
        ? [...queryWords].filter(w => textWords.has(w)).length / queryWords.size
        : 0;
      score = overlap;
    }

    if (score > 0.1) {
      results.push({
        id: mem.id,
        text: mem.text,
        category: mem.category || '',
        importance: mem.importance || 0.5,
        score: Math.round(score * 1000) / 1000,
        timestamp: mem.created_at || mem.timestamp || ''
      });
    }
  }

  results.sort((a, b) => b.score - a.score);
  return results.slice(0, k);
}

/**
 * Semantic search using Ollama embeddings
 * @param {Array} memories
 * @param {string} query
 * @param {number} k
 * @param {number} minScore
 * @returns {Promise<Array>}
 */
export async function semanticSearch(memories, query, k = 10, minScore = 0.3) {
  let queryVec = null;
  try {
    queryVec = await getEmbedding(query, OLLAMA_HOST, OLLAMA_EMBED_MODEL);
  } catch {
    // Fall back to keyword search
  }

  if (!queryVec) {
    return fallbackSearch(memories, query, k);
  }

  const results = [];

  for (const mem of memories) {
    const memVec = mem.embedding;
    if (!memVec) {
      // Use text similarity as fallback
      const textSim = textSimilarity(query, mem.text || '');
      if (textSim >= minScore) {
        results.push({
          id: mem.id,
          text: mem.text,
          category: mem.category || '',
          importance: mem.importance || 0.5,
          score: Math.round(textSim * 1000) / 1000,
          timestamp: mem.created_at || mem.timestamp || ''
        });
      }
      continue;
    }

    const sim = cosineSimilarity(queryVec, memVec);
    if (sim >= minScore) {
      results.push({
        id: mem.id,
        text: mem.text,
        category: mem.category || '',
        importance: mem.importance || 0.5,
        score: Math.round(sim * 1000) / 1000,
        timestamp: mem.created_at || mem.timestamp || ''
      });
    }
  }

  results.sort((a, b) => b.score - a.score);
  return results.slice(0, k);
}

/**
 * Filter search by multiple dimensions
 * @param {Array} memories
 * @param {object} filters
 * @returns {Array}
 */
export function filterSearch(memories, {
  category = null,
  minImportance = null,
  maxAgeDays = null,
  tags = null,
  hasTags = false,
  limit = 50
} = {}) {
  const cutoff = maxAgeDays
    ? Date.now() - maxAgeDays * 24 * 60 * 60 * 1000
    : null;

  const results = [];

  for (const mem of memories) {
    // Category filter
    if (category && (mem.category || '') !== category) continue;

    // Importance filter
    if (minImportance != null && (mem.importance || 0.5) < minImportance) continue;

    // Time filter
    if (cutoff) {
      const memTime = mem.created_at || mem.timestamp;
      if (memTime && memTime < cutoff) continue;
    }

    // Tag filter
    const memTags = new Set(mem.tags || []);
    if (hasTags && memTags.size === 0) continue;
    if (tags && !tags.some(t => memTags.has(t))) continue;

    results.push({
      id: mem.id,
      text: mem.text,
      category: mem.category || '',
      importance: mem.importance || 0.5,
      tags: mem.tags || [],
      timestamp: mem.created_at || mem.timestamp || ''
    });
  }

  return results.slice(0, limit);
}

/**
 * Get search suggestions based on history and memory content
 * @param {Array} memories
 * @param {string} prefix
 * @returns {string[]}
 */
export function getSearchSuggestions(memories, prefix) {
  const history = loadHistory();
  const suggestions = [];

  // From history
  for (const s of history.recent || []) {
    if (s.toLowerCase().includes(prefix.toLowerCase())) {
      suggestions.push(s);
    }
  }

  // From memory content words
  if (suggestions.length < 5) {
    for (const mem of (memories || []).slice(0, 20)) {
      const words = (mem.text || '').split(/\s+/).slice(0, 5);
      for (const word of words) {
        if (word.length > 2 && word.toLowerCase().includes(prefix.toLowerCase())) {
          if (!suggestions.includes(word)) {
            suggestions.push(word);
          }
        }
      }
    }
  }

  return [...new Set(suggestions)].slice(0, 10);
}

/**
 * Get search statistics
 * @returns {object}
 */
export function getSearchStats() {
  const history = loadHistory();
  const searches = history.searches || [];

  if (searches.length === 0) {
    return { total_searches: 0, popular_queries: [] };
  }

  /** @type {Map<string, number>} */
  const queryCounts = new Map();
  for (const s of searches) {
    queryCounts.set(s.query, (queryCounts.get(s.query) || 0) + 1);
  }

  const popular = [...queryCounts.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([query, count]) => ({ query, count }));

  return {
    total_searches: searches.length,
    popular_queries: popular,
    recent_searches: searches.slice(-10)
  };
}

// ============================================================
// CLI Command Handler
// ============================================================

/**
 * Execute a search command
 * @param {string} command
 * @param {object} args
 * @param {Array} memories - loaded memories array
 * @returns {Promise<object>}
 */
export async function cmdSearch(command, args, memories) {
  const history = loadHistory();

  switch (command) {
    case 'search': {
      const { query, k = 10, json: asJson = false } = args;
      if (!query) return { error: '请提供搜索内容' };
      const results = await semanticSearch(memories, query, k);
      recordSearch(query, results.length);
      if (asJson) {
        return { type: 'json', data: results };
      }
      return {
        type: 'text',
        text: `🔍 搜索: ${query}\n   找到 ${results.length} 条结果\n\n` +
          results.map((r, i) =>
            `${i + 1}. [${r.category}] ${r.text.slice(0, 80)}...\n   评分: ${r.score.toFixed(3)} | 重要性: ${r.importance}`
          ).join('\n\n')
      };
    }

    case 'filter': {
      const { category, minImportance, maxAge, tags, hasTags, k = 50, json: asJson = false } = args;
      const results = filterSearch(memories, {
        category,
        minImportance: minImportance != null ? parseFloat(minImportance) : null,
        maxAgeDays: maxAge ? parseInt(maxAge) : null,
        tags,
        hasTags,
        limit: parseInt(k)
      });
      if (asJson) {
        return { type: 'json', data: results };
      }
      return {
        type: 'text',
        text: `🔍 过滤结果: ${results.length} 条\n\n` +
          results.map((r, i) =>
            `${i + 1}. [${r.category}] ${r.text.slice(0, 60)}...\n   重要性: ${r.importance} | 标签: ${JSON.stringify(r.tags || [])}`
          ).join('\n\n')
      };
    }

    case 'history': {
      const { json: asJson = false } = args;
      const recent = (history.searches || []).slice(-10);
      if (asJson) {
        return { type: 'json', data: recent };
      }
      return {
        type: 'text',
        text: '📜 搜索历史:\n' +
          [...recent].reverse().map(r =>
            `   ${r.timestamp.slice(0, 19)} - ${r.query} (${r.results}结果)`
          ).join('\n')
      };
    }

    case 'suggestions': {
      const { query } = args;
      if (!query) return { error: '请提供前缀' };
      const suggestions = getSearchSuggestions(memories, query);
      return {
        type: 'text',
        text: '💡 搜索建议:\n' + suggestions.map(s => `   ${s}`).join('\n')
      };
    }

    case 'stats': {
      const stats = getSearchStats();
      const { json: asJson = false } = args;
      if (asJson) {
        return { type: 'json', data: stats };
      }
      return {
        type: 'text',
        text: `📊 搜索统计\n   总搜索次数: ${stats.total_searches}\n\n   热门搜索:\n` +
          (stats.popular_queries || []).slice(0, 5).map(q => `     ${q.query}: ${q.count}次`).join('\n')
      };
    }

    default:
      return { error: `未知命令: ${command}` };
  }
}

export default {
  semanticSearch,
  fallbackSearch,
  filterSearch,
  getSearchSuggestions,
  getSearchStats,
  loadHistory,
  recordSearch,
  cmdSearch
};
