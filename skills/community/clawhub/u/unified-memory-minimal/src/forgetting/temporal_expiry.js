/**
 * Temporal Expiry - 临时事实过期管理
 * 
 * 检测和清理临时事实（有过期时间的记忆）
 * 例如："明天我有考试"、"下周一开会"
 * 
 * 功能：
 * - 使用正则或 LLM 提取过期时间
 * - 定期检查并删除过期记忆
 * - 集成到 memory-cleaner 中
 */

import { log } from '../logger.js';
import { config } from '../config.js';
import { llmCall } from '../config.js';

// ─── 配置 ───────────────────────────────────────────────────────────────────
const DEFAULT_CONFIG = {
  checkInterval: 60 * 60 * 1000,    // 检查间隔：1 小时
  defaultExpiryHours: 24,            // 默认过期时间：24 小时
  maxFutureDays: 365,                // 最大未来天数
  minConfidence: 0.7,                // 最小置信度
};

// ─── 时间表达式模式（正则）────────────────────────────────────────────────────

/**
 * 中文时间表达式模式
 */
const CN_TIME_PATTERNS = [
  // 明天/昨天/今天
  { pattern: /明天/, offset: 1, unit: 'day' },
  { pattern: /昨天/, offset: -1, unit: 'day' },
  { pattern: /今天/, offset: 0, unit: 'day' },
  
  // 下周/上周
  { pattern: /下周([一二三四五六日天])/, offset: 'next-week', unit: 'day-of-week' },
  { pattern: /上周([一二三四五六日天])/, offset: 'last-week', unit: 'day-of-week' },
  { pattern: /本周([一二三四五六日天])/, offset: 'this-week', unit: 'day-of-week' },
  
  // N 天后/前
  { pattern: /(\d+)\s*天[之以]?后/, offset: 'future', unit: 'days' },
  { pattern: /(\d+)\s*天前/, offset: 'past', unit: 'days' },
  
  // N 小时后/前
  { pattern: /(\d+)\s*小时[之以]?后/, offset: 'future', unit: 'hours' },
  { pattern: /(\d+)\s*小时前/, offset: 'past', unit: 'hours' },
  
  // 具体日期：X月X日
  { pattern: /(\d{1,2})\s*月\s*(\d{1,2})\s*[日号]/, offset: 'specific', unit: 'date' },
  
  // 具体时间：X点X分
  { pattern: /(\d{1,2})\s*[点时](\d{1,2})?\s*分?/, offset: 'specific', unit: 'time' },
];

/**
 * 英文时间表达式模式
 */
const EN_TIME_PATTERNS = [
  // tomorrow/yesterday/today
  { pattern: /\btomorrow\b/i, offset: 1, unit: 'day' },
  { pattern: /\byesterday\b/i, offset: -1, unit: 'day' },
  { pattern: /\btoday\b/i, offset: 0, unit: 'day' },
  
  // next/last week
  { pattern: /\bnext\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b/i, offset: 'next-week', unit: 'day-of-week' },
  { pattern: /\blast\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b/i, offset: 'last-week', unit: 'day-of-week' },
  
  // in N days/hours
  { pattern: /\bin\s+(\d+)\s+days?\b/i, offset: 'future', unit: 'days' },
  { pattern: /\bin\s+(\d+)\s+hours?\b/i, offset: 'future', unit: 'hours' },
  
  // N days ago
  { pattern: /(\d+)\s+days?\s+ago\b/i, offset: 'past', unit: 'days' },
  { pattern: /(\d+)\s+hours?\s+ago\b/i, offset: 'past', unit: 'hours' },
];

/**
 * 临时事实关键词（暗示有过期时间）
 */
const TEMPORAL_KEYWORDS = [
  '明天', '后天', '下周', '今晚', '明天早上', '明天下午',
  'tomorrow', 'next week', 'tonight', 'later today',
  '考试', '会议', '约会', '面试', 'deadline', '到期',
  'exam', 'meeting', 'appointment', 'interview', 'deadline',
];

// ─── 时间解析 ────────────────────────────────────────────────────────────────

/**
 * 解析中文星期几
 */
function parseChineseDayOfWeek(day) {
  const map = {
    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '日': 7, '天': 7,
  };
  return map[day] || 0;
}

/**
 * 解析英文星期几
 */
function parseEnglishDayOfWeek(day) {
  const map = {
    'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4,
    'friday': 5, 'saturday': 6, 'sunday': 7,
  };
  return map[day.toLowerCase()] || 0;
}

/**
 * 计算到指定星期几的时间
 */
function getDayOfWeekOffset(targetDay, weekOffset = 0) {
  const now = new Date();
  const currentDay = now.getDay() || 7; // 1-7
  
  let diff = targetDay - currentDay;
  if (weekOffset === 'next') {
    diff += 7;
  } else if (weekOffset === 'last') {
    diff -= 7;
  }
  
  const target = new Date(now);
  target.setDate(target.getDate() + diff);
  target.setHours(23, 59, 59, 999);
  
  return target.getTime();
}

/**
 * 使用正则提取过期时间
 */
function extractExpiryByRegex(text) {
  const now = Date.now();
  const allPatterns = [...CN_TIME_PATTERNS, ...EN_TIME_PATTERNS];
  
  for (const { pattern, offset, unit } of allPatterns) {
    const match = text.match(pattern);
    if (!match) continue;
    
    let expiryTime = null;
    
    switch (unit) {
      case 'day':
        expiryTime = now + offset * 24 * 60 * 60 * 1000;
        break;
        
      case 'day-of-week': {
        const dayNum = parseChineseDayOfWeek(match[1]) || parseEnglishDayOfWeek(match[1]);
        if (dayNum > 0) {
          const weekOffset = offset === 'next-week' ? 'next' : offset === 'last-week' ? 'last' : 0;
          expiryTime = getDayOfWeekOffset(dayNum, weekOffset);
        }
        break;
      }
        
      case 'days':
        if (offset === 'future') {
          expiryTime = now + parseInt(match[1]) * 24 * 60 * 60 * 1000;
        } else if (offset === 'past') {
          expiryTime = now - parseInt(match[1]) * 24 * 60 * 60 * 1000;
        }
        break;
        
      case 'hours':
        if (offset === 'future') {
          expiryTime = now + parseInt(match[1]) * 60 * 60 * 1000;
        } else if (offset === 'past') {
          expiryTime = now - parseInt(match[1]) * 60 * 60 * 1000;
        }
        break;
        
      case 'date': {
        const month = parseInt(match[1]);
        const day = parseInt(match[2]);
        const target = new Date();
        target.setMonth(month - 1, day);
        target.setHours(23, 59, 59, 999);
        
        // 如果日期已过，算明年
        if (target.getTime() < now) {
          target.setFullYear(target.getFullYear() + 1);
        }
        
        expiryTime = target.getTime();
        break;
      }
        
      case 'time': {
        const hour = parseInt(match[1]);
        const minute = match[2] ? parseInt(match[2]) : 0;
        const target = new Date();
        target.setHours(hour, minute, 0, 0);
        
        // 如果时间已过，算明天
        if (target.getTime() < now) {
          target.setDate(target.getDate() + 1);
        }
        
        expiryTime = target.getTime();
        break;
      }
    }
    
    if (expiryTime) {
      return {
        expiryTime,
        confidence: 0.8,
        method: 'regex',
        matched: match[0],
      };
    }
  }
  
  return null;
}

/**
 * 使用 LLM 提取过期时间
 */
async function extractExpiryByLLM(text) {
  const prompt = `你是一个时间分析专家。从以下文本中提取过期时间。

文本: ${text}

请判断：
1. 这段文本是否包含临时事实（有过期时间的信息）？
2. 如果有，过期时间是什么时候？

输出 JSON 格式：
{
  "is_temporal": true/false,
  "expiry_time": "ISO 8601 格式的时间，如 2024-01-15T18:00:00",
  "confidence": 0.0-1.0,
  "reason": "简短解释"
}

如果无法确定具体时间，设置 expiry_time 为 null。只输出 JSON。`;

  try {
    const response = await llmCall(prompt);
    const jsonMatch = response.match(/\{[\s\S]*\}/);
    if (!jsonMatch) return null;
    
    const result = JSON.parse(jsonMatch[0]);
    
    if (!result.is_temporal || !result.expiry_time) {
      return null;
    }
    
    const expiryTime = new Date(result.expiry_time).getTime();
    if (isNaN(expiryTime)) return null;
    
    return {
      expiryTime,
      confidence: result.confidence,
      method: 'llm',
      reason: result.reason,
    };
  } catch (e) {
    log('warn', `[temporal_expiry] LLM extraction failed: ${e.message}`);
    return null;
  }
}

// ─── 核心接口 ────────────────────────────────────────────────────────────────

/**
 * 检测记忆是否包含临时事实
 */
export function isTemporalMemory(memory) {
  const text = memory.text || memory.content || '';
  return TEMPORAL_KEYWORDS.some(kw => text.includes(kw));
}

/**
 * 提取记忆的过期时间
 */
export async function extractExpiryTime(memory, options = {}) {
  const text = memory.text || memory.content || '';
  
  // 如果已经有 expiryTime，直接返回
  if (memory.expiryTime) {
    return {
      expiryTime: memory.expiryTime,
      confidence: 1.0,
      method: 'existing',
    };
  }
  
  // Step 1: 正则提取
  const regexResult = extractExpiryByRegex(text);
  if (regexResult && regexResult.confidence >= DEFAULT_CONFIG.minConfidence) {
    return regexResult;
  }
  
  // Step 2: LLM 提取（如果启用）
  if (options.useLLM !== false) {
    const llmResult = await extractExpiryByLLM(text);
    if (llmResult) {
      return llmResult;
    }
  }
  
  // Step 3: 默认过期时间（如果包含临时关键词）
  if (isTemporalMemory(memory)) {
    const defaultExpiry = Date.now() + DEFAULT_CONFIG.defaultExpiryHours * 60 * 60 * 1000;
    return {
      expiryTime: defaultExpiry,
      confidence: 0.5,
      method: 'default',
    };
  }
  
  return null;
}

/**
 * 检查记忆是否已过期
 */
export function isExpired(memory, now = Date.now()) {
  if (!memory.expiryTime) return false;
  return now >= memory.expiryTime;
}

/**
 * 批量提取过期时间
 */
export async function extractExpiryTimes(memories, options = {}) {
  const results = new Map();
  
  for (const memory of memories) {
    // 只处理包含临时关键词的记忆
    if (!isTemporalMemory(memory)) continue;
    
    const expiry = await extractExpiryTime(memory, options);
    if (expiry) {
      results.set(memory.id, expiry);
    }
  }
  
  return results;
}

/**
 * 清理过期记忆
 */
export async function cleanExpiredMemories(memories, storage = null) {
  const now = Date.now();
  const expired = [];
  const kept = [];
  
  for (const memory of memories) {
    // 提取过期时间（如果还没有）
    if (!memory.expiryTime && isTemporalMemory(memory)) {
      const expiry = await extractExpiryTime(memory);
      if (expiry) {
        memory.expiryTime = expiry.expiryTime;
      }
    }
    
    // 检查是否过期
    if (isExpired(memory, now)) {
      expired.push(memory);
      
      // 实际删除（如果提供了 storage）
      if (storage && typeof storage.deleteMemory === 'function') {
        try {
          await storage.deleteMemory(memory.id);
        } catch (e) {
          log('warn', `[temporal_expiry] Failed to delete expired memory: ${e.message}`);
        }
      }
    } else {
      kept.push(memory);
    }
  }
  
  log('info', `[temporal_expiry] Cleaned ${expired.length} expired memories`);
  
  return {
    expired,
    kept,
    total: memories.length,
    expiredCount: expired.length,
  };
}

/**
 * 定时清理任务
 */
export function startExpiryChecker(storage, interval = DEFAULT_CONFIG.checkInterval) {
  const checker = async () => {
    try {
      log('info', '[temporal_expiry] Running expiry check');
      
      // 获取所有记忆
      const allMemories = await storage.getAllMemories?.() || [];
      const result = await cleanExpiredMemories(allMemories, storage);
      
      log('info', `[temporal_expiry] Check complete: ${result.expiredCount} expired`);
    } catch (e) {
      log('error', `[temporal_expiry] Check failed: ${e.message}`);
    }
  };
  
  // 启动定时器
  const timer = setInterval(checker, interval);
  
  // 立即执行一次
  checker();
  
  return {
    stop: () => clearInterval(timer),
    runNow: checker,
  };
}

export default {
  isTemporalMemory,
  extractExpiryTime,
  isExpired,
  extractExpiryTimes,
  cleanExpiredMemories,
  startExpiryChecker,
};
