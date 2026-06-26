/**
 * BM25搜索引擎 - 完全本地，不调用LLM
 * 参考: memory_bm25.py (274行)
 * 
 * v3.2: 支持 scope 过滤 + index 缓存
 * v4.0: 集成 @node-rs/jieba 中文分词
 */

import { getAllMemories, getAllMemoriesRaw } from './storage.js';
import { log } from './logger.js';

// ─── 中文分词支持 ───────────────────────────────────────────────────────────

let jiebaCut = null;
let jiebaLoaded = false;

/**
 * 初始化 Jieba 分词器
 */
async function initJieba() {
  if (jiebaLoaded) return jiebaCut !== null;
  
  try {
    const jieba = await import('@node-rs/jieba');
    jiebaCut = jieba.cut;
    jiebaLoaded = true;
    log.info('[BM25] Jieba tokenizer loaded successfully');
    return true;
  } catch (err) {
    log.warn('[BM25] Jieba not available, using fallback tokenizer:', err.message);
    jiebaLoaded = true;
    return false;
  }
}

// 异步初始化
initJieba();

// BM25 parameters
const B = 0.75;  // field length normalization
const K1 = 1.5;  // term frequency saturation

// Index cache (invalidated when memories change)
let _cachedIndex = null;
let _cachedMemCount = -1;
let _cachedScope = null;

/**
 * 中文停用词表
 */
const STOP_WORDS = new Set([
  // 常用停用词
  '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '么',
  '他', '她', '它', '们', '这个', '那个', '什么', '怎么', '为什么', '哪里', '那里', '这里',
  '可以', '可能', '应该', '需要', '能够', '已经', '还是', '但是', '因为', '所以', '如果',
  '或者', '而且', '然后', '虽然', '比如', '通过', '进行', '使用', '关于', '对于', '根据',
  // 英文停用词
  'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
  'may', 'might', 'must', 'shall', 'can', 'need', 'dare', 'ought', 'used',
  'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
  'through', 'during', 'before', 'after', 'above', 'below', 'between', 'under',
  'and', 'but', 'or', 'nor', 'so', 'yet', 'both', 'either', 'neither',
  'not', 'only', 'own', 'same', 'than', 'too', 'very', 'just', 'also',
  'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
  'you', 'your', 'yours', 'yourself', 'yourselves',
  'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself',
  'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
  'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those',
  'am', 'been', 'being', 'here', 'there', 'when', 'where', 'why', 'how',
  'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some',
]);

/**
 * Enhanced tokenizer - 支持 Jieba 中文分词
 * @param {string} text
 * @returns {string[]}
 */
function tokenize(text) {
  if (!text) return [];
  
  const tokens = [];
  
  // 移除HTML标签
  text = text.replace(/<[^>]+>/g, ' ');
  
  // 使用 Jieba 分词（如果可用）
  if (jiebaCut) {
    try {
      const chineseTokens = jiebaCut(text, false); // false = 不返回 HMM 结果
      for (const token of chineseTokens) {
        const trimmed = token.trim();
        if (trimmed.length > 1 && !STOP_WORDS.has(trimmed.toLowerCase())) {
          tokens.push(trimmed.toLowerCase());
        }
      }
    } catch (err) {
      // Jieba 失败，使用 fallback
      log.warn('[BM25] Jieba cut failed, using fallback:', err.message);
    }
  }
  
  // Fallback 或补充：英文单词分词
  const english = text.match(/[a-zA-Z_]+/g) || [];
  for (const word of english) {
    const lower = word.toLowerCase();
    if (lower.length > 1 && !STOP_WORDS.has(lower)) {
      tokens.push(lower);
    }
  }
  
  // 如果 Jieba 不可用，使用简单的中文字符分词
  if (!jiebaCut) {
    const chinese = text.match(/[\u4e00-\u9fa5]+/g) || [];
    for (const phrase of chinese) {
      // 简单分词：每 2-4 个字符作为一个 token
      if (phrase.length <= 4) {
        if (!STOP_WORDS.has(phrase)) {
          tokens.push(phrase);
        }
      } else {
        // 滑动窗口
        for (let i = 0; i <= phrase.length - 2; i++) {
          for (let len = 2; len <= Math.min(4, phrase.length - i); len++) {
            const ngram = phrase.substring(i, i + len);
            if (!STOP_WORDS.has(ngram)) {
              tokens.push(ngram);
            }
          }
        }
      }
    }
  }
  
  // 去重
  return [...new Set(tokens)];
}

/**
 * BM25 Ranking Function
 * @param {string} query
 * @param {string} text
 * @param {object} index - { docLengths, avgDocLength, invertedIndex, docCount, idfCache }
 * @param {object} [options]
 * @returns {number}
 */
function bm25Score(query, text, index, options = {}) {
  const { k1 = 1.5, b = 0.75 } = options;
  const tokens = tokenize(text);
  const docLength = tokens.length;
  if (docLength === 0) return 0;

  const queryTokens = tokenize(query);
  let score = 0;

  for (const qtoken of queryTokens) {
    const termPostings = index.invertedIndex.get(qtoken);
    if (!termPostings) continue;

    const tf = termPostings.get(text) || 0;
    if (tf === 0) continue;

    // IDF
    let idf = index.idfCache.get(qtoken);
    if (idf === undefined) {
      const docWithTerm = termPostings.size;
      idf = Math.log((index.docCount - docWithTerm + 0.5) / (docWithTerm + 0.5) + 1);
      index.idfCache.set(qtoken, idf);
    }

    // TF normalization
    const tfNorm = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (docLength / index.avgDocLength)));
    score += idf * tfNorm;
  }

  return score;
}

/**
 * Build BM25 index from all memories (with scope filtering and caching)
 * @param {string} [scope] - Scope to filter by (USER/TEAM/AGENT/GLOBAL/null for all)
 * @returns {object}
 */
export function buildBM25Index(scope = null) {
  // Check cache (valid for same scope + same memory count)
  const memCount = getAllMemoriesRaw().length;
  if (_cachedIndex && _cachedScope === scope && _cachedMemCount === memCount) {
    return _cachedIndex;
  }

  const memories = getAllMemoriesRaw().filter(m => !scope || m.scope === scope || !m.scope);
  const invertedIndex = new Map();
  const docLengths = new Map();
  const idfCache = new Map();
  let totalLength = 0;

  for (const mem of memories) {
    const text = mem.text || '';
    const tokens = tokenize(text);
    docLengths.set(text, tokens.length);
    totalLength += tokens.length;

    for (const token of tokens) {
      if (!invertedIndex.has(token)) {
        invertedIndex.set(token, new Map());
      }
      const postings = invertedIndex.get(token);
      postings.set(text, (postings.get(text) || 0) + 1);
    }
  }

  const docCount = memories.length;
  const avgDocLength = docCount > 0 ? totalLength / docCount : 1;

  _cachedIndex = { invertedIndex, docLengths, avgDocLength, docCount, idfCache };
  _cachedScope = scope;
  _cachedMemCount = memCount;

  return _cachedIndex;
}

/**
 * Search using BM25 (with optional scope filtering)
 * @param {string} query
 * @param {number} [topK=10]
 * @param {string} [scope] - Optional scope filter
 * @returns {Array<{memory: object, score: number, highlight: string}>}
 */
export function bm25Search(query, topK = 10, scope = null) {
  if (!query) return [];
  
  // Get memories filtered by scope
  const allMemories = getAllMemoriesRaw();
  const memories = scope ? allMemories.filter(m => m.scope === scope || (!m.scope && scope === 'USER')) : allMemories;
  if (memories.length === 0) return [];

  const index = buildBM25Index(scope);
  const results = [];

  for (const mem of memories) {
    const score = bm25Score(query, mem.text, index);
    if (score > 0) {
      let highlight = mem.text.slice(0, 150);
      if (mem.text.length > 150) highlight += '...';

      results.push({ memory: mem, score, highlight });
    }
  }

  // Sort by score descending
  results.sort((a, b) => b.score - a.score);
  return results.slice(0, topK);
}

/** Invalidate BM25 cache (call after adding/deleting memories) */
export function invalidateBM25Cache() {
  _cachedIndex = null;
  _cachedMemCount = -1;
  _cachedScope = null;
}
