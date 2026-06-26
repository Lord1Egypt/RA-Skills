/**
 * Contradiction Resolver - 矛盾记忆检测与解决
 * 
 * 检测并解决记忆中的矛盾陈述
 * 例如："我住在 NYC" vs "我刚搬到 SF"
 * 
 * 功能：
 * - 使用 LLM 判断两条记忆是否矛盾
 * - 检测矛盾记忆对
 * - 保留较新的记忆，标记较旧的为过期
 * - 集成到 dedup 流程中
 */

import { log } from '../logger.js';
import { config } from '../config.js';
import { llmCall } from '../config.js';

// ─── 配置 ───────────────────────────────────────────────────────────────────
const DEFAULT_CONFIG = {
  similarityThreshold: 0.7,      // 语义相似度阈值（判断是否需要检查矛盾）
  contradictionThreshold: 0.8,   // LLM 矛盾判断阈值
  batchSize: 10,                 // 批量处理大小
  maxLLMCalls: 50,               // 单次最多 LLM 调用次数
  cacheResults: true,            // 是否缓存结果
};

// ─── 缓存 ────────────────────────────────────────────────────────────────────
const contradictionCache = new Map();

// ─── 矛盾模式检测（基于规则）──────────────────────────────────────────────────

/**
 * 常见矛盾模式
 * 这些模式可以快速检测，无需调用 LLM
 */
const CONTRADICTION_PATTERNS = [
  // 地点矛盾
  {
    type: 'location',
    pattern: /(?:住在|居住在|live in|based in|located in)\s*([^，。,\.]+)/gi,
    conflict: (a, b) => {
      const locations = ['nyc', 'new york', 'sf', 'san francisco', 'beijing', '北京', 'shanghai', '上海', 
                         'shenzhen', '深圳', 'hangzhou', '杭州', 'london', 'tokyo', 'tokyo'];
      const aLower = a.toLowerCase();
      const bLower = b.toLowerCase();
      for (const loc of locations) {
        if (aLower.includes(loc) && bLower.includes(loc)) continue;
        if ((aLower.includes(loc) || bLower.includes(loc)) && aLower !== bLower) {
          return true;
        }
      }
      return false;
    },
  },
  // 时间矛盾
  {
    type: 'temporal',
    pattern: /(?:明天|昨天|下周|上周|tomorrow|yesterday|next week|last week)/gi,
    conflict: (a, b) => {
      const timeWords = ['明天', '昨天', 'tomorrow', 'yesterday', '下周', '上周', 'next week', 'last week'];
      const aHasTime = timeWords.some(w => a.includes(w));
      const bHasTime = timeWords.some(w => b.includes(w));
      return aHasTime && bHasTime && a !== b;
    },
  },
  // 状态矛盾
  {
    type: 'status',
    pattern: /(?:是|不是|在|不在|有|没有|is|is not|has|has no)/gi,
    conflict: (a, b) => {
      // 检测否定词
      const negationPattern = /(?:不|not|no|没有|无)/gi;
      const aHasNegation = negationPattern.test(a);
      const bHasNegation = negationPattern.test(b);
      return aHasNegation !== bHasNegation;
    },
  },
];

/**
 * 使用规则快速检测矛盾
 */
function detectContradictionByRule(textA, textB) {
  for (const { type, pattern, conflict } of CONTRADICTION_PATTERNS) {
    const matchesA = textA.match(pattern);
    const matchesB = textB.match(pattern);
    
    if (matchesA && matchesB) {
      if (conflict(textA, textB)) {
        return {
          hasContradiction: true,
          type,
          confidence: 0.7,
          method: 'rule',
        };
      }
    }
  }
  
  return null;
}

// ─── LLM 矛盾检测 ────────────────────────────────────────────────────────────

/**
 * 使用 LLM 判断两条记忆是否矛盾
 */
async function detectContradictionByLLM(textA, textB, metadata = {}) {
  const cacheKey = `${textA}|||${textB}`;
  
  // 检查缓存
  if (DEFAULT_CONFIG.cacheResults && contradictionCache.has(cacheKey)) {
    return contradictionCache.get(cacheKey);
  }
  
  const prompt = `你是一个记忆分析专家。判断以下两条记忆是否存在矛盾。

记忆 A: ${textA}
记忆 B: ${textB}

请判断：
1. 这两条记忆是否描述同一主题？
2. 如果是，它们是否存在矛盾？

输出 JSON 格式：
{
  "same_topic": true/false,
  "has_contradiction": true/false,
  "confidence": 0.0-1.0,
  "reason": "简短解释原因"
}

只输出 JSON，不要其他内容。`;

  try {
    const response = await llmCall(prompt);
    
    // 解析 JSON
    const jsonMatch = response.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      log('warn', '[contradiction_resolver] LLM response is not valid JSON');
      return null;
    }
    
    const result = JSON.parse(jsonMatch[0]);
    
    // 缓存结果
    if (DEFAULT_CONFIG.cacheResults) {
      contradictionCache.set(cacheKey, result);
    }
    
    return {
      hasContradiction: result.has_contradiction,
      sameTopic: result.same_topic,
      confidence: result.confidence,
      reason: result.reason,
      method: 'llm',
    };
  } catch (e) {
    log('warn', `[contradiction_resolver] LLM call failed: ${e.message}`);
    return null;
  }
}

// ─── 核心接口 ────────────────────────────────────────────────────────────────

/**
 * 检测两条记忆是否矛盾
 * @param {object} memoryA - 记忆 A
 * @param {object} memoryB - 记忆 B
 * @param {object} [options] - 配置选项
 * @returns {Promise<object|null>}
 */
export async function detectContradiction(memoryA, memoryB, options = {}) {
  const textA = memoryA.text || memoryA.content || '';
  const textB = memoryB.text || memoryB.content || '';
  
  if (!textA || !textB) return null;
  
  // Step 1: 规则快速检测
  const ruleResult = detectContradictionByRule(textA, textB);
  if (ruleResult && ruleResult.confidence >= 0.8) {
    return {
      ...ruleResult,
      memoryA: memoryA.id,
      memoryB: memoryB.id,
    };
  }
  
  // Step 2: LLM 深度检测
  if (options.useLLM !== false) {
    const llmResult = await detectContradictionByLLM(textA, textB);
    if (llmResult) {
      return {
        ...llmResult,
        memoryA: memoryA.id,
        memoryB: memoryB.id,
      };
    }
  }
  
  return null;
}

/**
 * 批量检测记忆中的矛盾
 * @param {Array} memories - 记忆列表
 * @param {object} [options] - 配置选项
 * @returns {Promise<Array>} - 矛盾对列表
 */
export async function detectContradictions(memories, options = {}) {
  const contradictions = [];
  const checked = new Set();
  let llmCalls = 0;
  
  log('info', `[contradiction_resolver] Checking ${memories.length} memories for contradictions`);
  
  for (let i = 0; i < memories.length; i++) {
    for (let j = i + 1; j < memories.length; j++) {
      const key = `${memories[i].id}-${memories[j].id}`;
      if (checked.has(key)) continue;
      checked.add(key);
      
      // 快速检查：时间跨度太大不太可能矛盾
      const timeA = memories[i].created || 0;
      const timeB = memories[j].created || 0;
      const timeDiff = Math.abs(timeA - timeB);
      const maxTimeDiff = options.maxTimeDiff || 30 * 24 * 60 * 60 * 1000; // 30 天
      
      if (timeDiff > maxTimeDiff) continue;
      
      // 检测矛盾
      const result = await detectContradiction(memories[i], memories[j], {
        useLLM: llmCalls < DEFAULT_CONFIG.maxLLMCalls,
      });
      
      if (result && result.hasContradiction) {
        contradictions.push({
          ...result,
          memoryA: memories[i],
          memoryB: memories[j],
        });
      }
      
      if (result?.method === 'llm') {
        llmCalls++;
      }
    }
  }
  
  log('info', `[contradiction_resolver] Found ${contradictions.length} contradictions`);
  return contradictions;
}

/**
 * 解决矛盾：保留新的，标记旧的为过期
 * @param {Array} contradictions - 矛盾对列表
 * @param {object} [options] - 配置选项
 * @returns {Promise<object>} - 解决结果
 */
export async function resolveContradictions(contradictions, options = {}) {
  const resolved = [];
  const expired = [];
  
  for (const c of contradictions) {
    const memA = c.memoryA;
    const memB = c.memoryB;
    
    // 根据时间决定保留哪个
    const timeA = memA.created || memA.lastAccessed || 0;
    const timeB = memB.created || memB.lastAccessed || 0;
    
    let keep, expire;
    if (timeA >= timeB) {
      keep = memA;
      expire = memB;
    } else {
      keep = memB;
      expire = memA;
    }
    
    // 标记过期
    if (expire) {
      expired.push({
        id: expire.id,
        reason: `contradiction with ${keep.id}`,
        type: c.type,
        confidence: c.confidence,
      });
      
      // 实际标记（如果提供了 storage）
      if (options.storage && typeof options.storage.updateMemory === 'function') {
        try {
          await options.storage.updateMemory(expire.id, {
            expired: true,
            expiredAt: Date.now(),
            expiredReason: `contradiction with ${keep.id}`,
          });
        } catch (e) {
          log('warn', `[contradiction_resolver] Failed to mark memory as expired: ${e.message}`);
        }
      }
    }
    
    resolved.push({
      kept: keep.id,
      expired: expire.id,
      type: c.type,
      confidence: c.confidence,
    });
  }
  
  return {
    total: contradictions.length,
    resolved: resolved.length,
    expired,
    details: resolved,
  };
}

/**
 * 集成到 dedup 流程
 * @param {Array} memories - 记忆列表
 * @param {object} [storage] - 存储实例
 * @returns {Promise<Array>} - 去重后的记忆列表
 */
export async function dedupWithContradictionResolution(memories, storage = null) {
  // 先检测矛盾
  const contradictions = await detectContradictions(memories, { storage });
  
  // 解决矛盾
  if (contradictions.length > 0) {
    await resolveContradictions(contradictions, { storage });
  }
  
  // 过滤掉过期的记忆
  const expiredIds = new Set(
    contradictions
      .filter(c => c.memoryA.expired || c.memoryB.expired)
      .flatMap(c => [c.memoryA.id, c.memoryB.id])
  );
  
  return memories.filter(m => !expiredIds.has(m.id));
}

export default {
  detectContradiction,
  detectContradictions,
  resolveContradictions,
  dedupWithContradictionResolution,
};
