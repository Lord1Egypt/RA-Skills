/**
 * noise_filter.js - 噪声过滤器 v2.0
 * 
 * 过滤低质量内容：
 * - 问候语
 * - 确认回复
 * - 简单问答
 * - Agent 拒绝
 * - 元问题
 */

import { log } from '../utils/logger.js';

// ============================================================
// 噪声模式定义
// ============================================================

// 问候语模式
const GREETING_PATTERNS = [
  /^(hi|hello|hey|你好|您好|嗨|嗨嗨|hi there|greetings)$/i,
  /^喂/,
  /^早上好|^下午好|^晚上好/,
  /^good (morning|afternoon|evening|day)/i,
];

// 确认回复模式
const CONFIRM_PATTERNS = [
  /^(好的|好|行|可以|yes|yep|yeah|ok|okay|sure|certainly|当然|没问题)$/i,
  /^收到/,
  /^明白/,
  /^了解/,
  /^👍|❤️|😊|😄/,
  /^[\s]*$/,  // 空白
];

// Agent 拒绝模式
const REFUSAL_PATTERNS = [
  /抱歉，我无法/i,
  /sorry, i can't/i,
  /i'm sorry, but i cannot/i,
  /作为一个.*?我无法/i,
  /对不起，我不能/i,
  /我无法提供/i,
  /cannot provide/i,
  /unable to/i,
];

// 元问题模式
const META_PATTERNS = [
  /你是谁/i,
  /what are you/i,
  /who are you/i,
  /你的名字/i,
  /what can you do/i,
  /你能做什么/i,
  /help me/i,
  /help with/i,
];

// 简单问答模式
const SIMPLE_QA_PATTERNS = [
  /^(是|否|对|错|yes|no)$/i,
  /^几点了/,
  /^今天几号/,
  /^天气怎么样/,
  /^\d+\+\d+=/,  // 数学题
];

// 合并所有模式
const ALL_PATTERNS = [
  ...GREETING_PATTERNS,
  ...CONFIRM_PATTERNS,
  ...REFUSAL_PATTERNS,
  ...META_PATTERNS,
  ...SIMPLE_QA_PATTERNS,
];

// ============================================================
// 噪声过滤器类
// ============================================================

export class NoiseFilter {
  /**
   * 判断是否为噪声
   * @param {string} text
   * @returns {boolean}
   */
  isNoise(text) {
    const trimmed = text.trim().toLowerCase();

    // 空内容
    if (!trimmed) {
      return true;
    }

    // 长度检查 - 过短
    if (trimmed.length < 3) {
      return true;
    }

    // 长度检查 - 过长的内容可能是转储
    if (trimmed.length > 5000) {
      return true;
    }

    // 模式匹配
    for (const pattern of ALL_PATTERNS) {
      if (pattern.test(trimmed)) {
        return true;
      }
    }

    return false;
  }

  /**
   * 获取噪声类型
   * @param {string} text
   * @returns {string}
   */
  getNoiseType(text) {
    const trimmed = text.trim().toLowerCase();

    for (const pattern of GREETING_PATTERNS) {
      if (pattern.test(trimmed)) return 'greeting';
    }

    for (const pattern of CONFIRM_PATTERNS) {
      if (pattern.test(trimmed)) return 'confirmation';
    }

    for (const pattern of REFUSAL_PATTERNS) {
      if (pattern.test(trimmed)) return 'refusal';
    }

    for (const pattern of META_PATTERNS) {
      if (pattern.test(trimmed)) return 'meta_question';
    }

    for (const pattern of SIMPLE_QA_PATTERNS) {
      if (pattern.test(trimmed)) return 'simple_qa';
    }

    if (trimmed.length < 3) return 'too_short';
    if (trimmed.length > 5000) return 'too_long';

    return 'unknown';
  }

  /**
   * 过滤列表
   * @param {string[]} texts
   * @returns {Array<[string, boolean]>}
   */
  filter(texts) {
    return texts.map(text => [text, this.isNoise(text)]);
  }

  /**
   * 只返回信号（过滤掉噪声）
   * @param {string[]} texts
   * @returns {string[]}
   */
  filterSignals(texts) {
    return texts.filter(text => !this.isNoise(text));
  }

  /**
   * 批量过滤结果
   * @param {string[]} texts
   * @returns {{ signals: string[], noises: string[], stats: object }}
   */
  filterBatch(texts) {
    const signals = [];
    const noises = [];
    /** @type {Map<string, number>} */
    const stats = new Map();

    for (const text of texts) {
      if (this.isNoise(text)) {
        const noiseType = this.getNoiseType(text);
        noises.push(text);
        stats.set(noiseType, (stats.get(noiseType) || 0) + 1);
      } else {
        signals.push(text);
      }
    }

    return {
      signals,
      noises,
      stats: Object.fromEntries(stats)
    };
  }
}

// ============================================================
// 导出 isNoise 函数（便捷接口）
// ============================================================

const _filter = new NoiseFilter();

/**
 * 判断是否为噪声（便捷函数）
 * @param {string} text
 * @returns {boolean}
 */
export function isNoise(text) {
  return _filter.isNoise(text);
}

/**
 * 获取噪声类型
 * @param {string} text
 * @returns {string}
 */
export function getNoiseType(text) {
  return _filter.getNoiseType(text);
}

/**
 * 过滤信号（只保留非噪声）
 * @param {string[]} texts
 * @returns {string[]}
 */
export function filterSignals(texts) {
  return _filter.filterSignals(texts);
}

// ============================================================
// CLI 命令
// ============================================================

/**
 * CLI: 测试噪声过滤
 * @param {object} args - { texts: string[] }
 * @returns {object}
 */
export function cmdFilter(args) {
  const { texts = [] } = args;
  
  const results = texts.map(text => ({
    text,
    is_noise: isNoise(text),
    noise_type: isNoise(text) ? getNoiseType(text) : 'signal'
  }));

  const batchResult = _filter.filterBatch(texts);

  return {
    content: [{
      type: 'text',
      text: JSON.stringify({
        results,
        summary: {
          signals: batchResult.signals.length,
          noises: batchResult.noises.length,
          stats: batchResult.stats
        }
      }, null, 2)
    }]
  };
}

export default _filter;
