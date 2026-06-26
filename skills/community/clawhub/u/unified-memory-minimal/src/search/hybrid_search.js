/**
 * Hybrid Search - 混合搜索系统
 * 
 * 支持多种搜索模式：
 * - memories: 只搜索记忆
 * - documents: 只搜索文档（RAG）
 * - hybrid: 合并两者结果
 * 
 * 功能：
 * - 统一的搜索接口
 * - 结果合并与重排序
 * - 支持多种后端（记忆 + 文档）
 */

import { log } from '../logger.js';
import { config } from '../config.js';
import { search as memorySearch } from '../search.js';

// ─── 配置 ───────────────────────────────────────────────────────────────────
const DEFAULT_CONFIG = {
  defaultMode: 'hybrid',
  memoryWeight: 0.6,       // 记忆结果权重
  documentWeight: 0.4,     // 文档结果权重
  maxResults: 20,          // 最大结果数
  rerankResults: true,     // 是否重排序
  dedupThreshold: 0.85,    // 去重阈值
};

// ─── 搜索后端 ─────────────────────────────────────────────────────────────────

/**
 * 记忆搜索后端
 */
async function searchMemories(query, options = {}) {
  try {
    const results = await memorySearch(query, options);
    return {
      results: (results || []).map(r => ({
        ...r,
        source: 'memory',
        score: r.score || r.similarity || 0.5,
      })),
      source: 'memory',
      count: results?.length || 0,
    };
  } catch (e) {
    log('warn', `[hybrid_search] Memory search failed: ${e.message}`);
    return { results: [], source: 'memory', count: 0, error: e.message };
  }
}

/**
 * 文档搜索后端（RAG）
 * 这个是占位实现，实际需要连接文档索引系统
 */
async function searchDocuments(query, options = {}) {
  // TODO: 实现文档搜索
  // 可能的后端：
  // - QMD (Quick Markdown Docs)
  // - 向量数据库（存储文档片段）
  // - 外部 RAG 服务
  
  // 占位实现：返回空结果
  log('debug', '[hybrid_search] Document search not implemented yet');
  return {
    results: [],
    source: 'document',
    count: 0,
  };
}

// ─── 结果合并与重排序 ─────────────────────────────────────────────────────────

/**
 * 计算文本相似度（简单的 Jaccard）
 */
function textSimilarity(a, b) {
  const wordsA = new Set(
    (a || '').toLowerCase().replace(/[^\p{L}\p{N}\s]/gu, ' ').split(/\s+/).filter(w => w.length > 2)
  );
  const wordsB = new Set(
    (b || '').toLowerCase().replace(/[^\p{L}\p{N}\s]/gu, ' ').split(/\s+/).filter(w => w.length > 2)
  );
  
  if (!wordsA.size || !wordsB.size) return 0;
  
  let intersection = 0;
  for (const w of wordsA) {
    if (wordsB.has(w)) intersection++;
  }
  
  return intersection / (wordsA.size + wordsB.size - intersection);
}

/**
 * 去重结果
 */
function dedupResults(results, threshold = DEFAULT_CONFIG.dedupThreshold) {
  const deduped = [];
  
  for (const result of results) {
    const text = result.text || result.content || '';
    let isDup = false;
    
    for (const existing of deduped) {
      const existingText = existing.text || existing.content || '';
      if (textSimilarity(text, existingText) >= threshold) {
        isDup = true;
        break;
      }
    }
    
    if (!isDup) {
      deduped.push(result);
    }
  }
  
  return deduped;
}

/**
 * 合并搜索结果
 */
function mergeResults(memoryResults, documentResults, options = {}) {
  const memoryWeight = options.memoryWeight || DEFAULT_CONFIG.memoryWeight;
  const documentWeight = options.documentWeight || DEFAULT_CONFIG.documentWeight;
  
  const merged = [];
  
  // 添加记忆结果
  for (const result of memoryResults) {
    merged.push({
      ...result,
      source: 'memory',
      finalScore: result.score * memoryWeight,
    });
  }
  
  // 添加文档结果
  for (const result of documentResults) {
    merged.push({
      ...result,
      source: 'document',
      finalScore: result.score * documentWeight,
    });
  }
  
  // 按分数排序
  merged.sort((a, b) => b.finalScore - a.finalScore);
  
  // 去重
  const deduped = dedupResults(merged);
  
  // 限制结果数
  const maxResults = options.maxResults || DEFAULT_CONFIG.maxResults;
  return deduped.slice(0, maxResults);
}

/**
 * 重排序结果（可选）
 */
function rerankResults(results, query) {
  // 简单的重排序：基于查询词频
  const queryWords = new Set(
    query.toLowerCase().split(/\s+/).filter(w => w.length > 2)
  );
  
  return results.map(result => {
    const text = (result.text || result.content || '').toLowerCase();
    let matchCount = 0;
    
    for (const word of queryWords) {
      if (text.includes(word)) {
        matchCount++;
      }
    }
    
    const queryBoost = queryWords.size > 0 ? matchCount / queryWords.size : 0;
    const rerankedScore = result.finalScore * (1 + queryBoost * 0.2);
    
    return {
      ...result,
      rerankedScore,
      finalScore: rerankedScore,
    };
  }).sort((a, b) => b.finalScore - a.finalScore);
}

// ─── 核心接口 ────────────────────────────────────────────────────────────────

/**
 * 混合搜索
 * @param {string} query - 搜索查询
 * @param {object} [options] - 搜索选项
 * @param {'memories'|'documents'|'hybrid'} [options.searchMode='hybrid'] - 搜索模式
 * @returns {Promise<Array>} - 搜索结果
 */
export async function hybridSearch(query, options = {}) {
  const mode = options.searchMode || DEFAULT_CONFIG.defaultMode;
  const maxResults = options.maxResults || DEFAULT_CONFIG.maxResults;
  const rerank = options.rerankResults !== false && DEFAULT_CONFIG.rerankResults;
  
  log('info', `[hybrid_search] Searching with mode: ${mode}, query: "${query.slice(0, 50)}..."`);
  
  let results = [];
  
  switch (mode) {
    case 'memories': {
      const memoryRes = await searchMemories(query, options);
      results = memoryRes.results;
      break;
    }
      
    case 'documents': {
      const docRes = await searchDocuments(query, options);
      results = docRes.results;
      break;
    }
      
    case 'hybrid':
    default: {
      // 并行搜索
      const [memoryRes, docRes] = await Promise.all([
        searchMemories(query, options),
        searchDocuments(query, options),
      ]);
      
      // 合并结果
      results = mergeResults(memoryRes.results, docRes.results, options);
      break;
    }
  }
  
  // 重排序
  if (rerank && query) {
    results = rerankResults(results, query);
  }
  
  log('info', `[hybrid_search] Found ${results.length} results`);
  
  return results;
}

/**
 * 仅搜索记忆
 */
export async function searchMemoriesOnly(query, options = {}) {
  return hybridSearch(query, { ...options, searchMode: 'memories' });
}

/**
 * 仅搜索文档
 */
export async function searchDocumentsOnly(query, options = {}) {
  return hybridSearch(query, { ...options, searchMode: 'documents' });
}

/**
 * 获取搜索统计
 */
export async function getSearchStats() {
  return {
    mode: DEFAULT_CONFIG.defaultMode,
    memoryWeight: DEFAULT_CONFIG.memoryWeight,
    documentWeight: DEFAULT_CONFIG.documentWeight,
    maxResults: DEFAULT_CONFIG.maxResults,
    rerankEnabled: DEFAULT_CONFIG.rerankResults,
  };
}

export default {
  hybridSearch,
  searchMemoriesOnly,
  searchDocumentsOnly,
  getSearchStats,
};
