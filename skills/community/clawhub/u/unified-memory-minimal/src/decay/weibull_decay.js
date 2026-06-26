/**
 * src/decay/weibull_decay.js
 * Weibull 衰减模型 - 比指数衰减更接近人类遗忘曲线
 * 
 * Weibull 分布参数:
 * - shape (k): 形状参数，通常 1.5-3.0。k 越大，衰减越慢（记忆越持久）
 * - scale (λ): 尺度参数，通常 30-90 天。决定"半衰期"附近的衰减速度
 * 
 * 公式: strength(t) = exp(-(t/λ)^k) + access_bonus
 * 
 * 访问奖励: 每次访问增加 5% 强度，上限 +50%
 */

import { config } from '../config.js';

export class WeibullDecayModel {
  /**
   * @param {Object} opts
   * @param {number} [opts.shape=1.5] - 形状参数 k
   * @param {number} [opts.scale=30] - 尺度参数 λ（天数）
   */
  constructor({ shape, scale } = {}) {
    const weibullCfg = config.weibull_decay || {};
    this.shape = shape ?? weibullCfg.shape ?? 1.5;
    this.scale = scale ?? weibullCfg.scale ?? 30;
  }

  /**
   * 计算单条记忆的当前强度 (0-1)
   * 
   * @param {Object} params
   * @param {number} params.created_at - 记忆创建时间 (ms 时间戳)
   * @param {number} [params.last_access] - 最后访问时间 (ms 时间戳)，默认 now
   * @param {number} [params.access_count=0] - 访问次数
   * @returns {number} 强度值 0-1
   */
  getStrength({ created_at, last_access, access_count = 0 } = {}) {
    const now = Date.now();
    const last = last_access || now;
    
    // 记忆年龄（天数）
    const T = (last - created_at) / (1000 * 60 * 60 * 24);

    // Weibull 衰减
    const decay = Math.exp(-Math.pow(T / this.scale, this.shape));

    // 访问奖励（每访问一次 +5%，上限 50%）
    const accessBonus = Math.min((access_count || 0) * 0.05, 0.5);

    return Math.min(decay + accessBonus, 1.0);
  }

  /**
   * 获取需要淘汰的记忆
   * 
   * @param {Array} memories - 记忆数组
   * @param {Object} opts
   * @param {number} [opts.threshold=0.1] - 强度阈值，低于此值淘汰
   * @param {number} [opts.max_age_days=365] - 最大年龄，超过直接淘汰
   * @returns {Array} 需要淘汰的记忆
   */
  getPruneCandidates(memories, { threshold = 0.1, max_age_days = 365 } = {}) {
    return memories.filter(m => {
      const age_days = (Date.now() - m.created_at) / (1000 * 60 * 60 * 24);
      
      // 超过最大年龄直接淘汰
      if (age_days > max_age_days) return true;
      
      // 计算强度
      const strength = this.getStrength(m);
      return strength < threshold;
    });
  }

  /**
   * 获取强度分布统计
   */
  getStats(memories) {
    const buckets = {
      strong: 0,     // > 0.7
      moderate: 0,  // 0.3 - 0.7
      weak: 0,      // 0.1 - 0.3
      prune: 0,     // < 0.1
    };

    const strengths = memories.map(m => this.getStrength(m));

    for (const s of strengths) {
      if (s > 0.7) buckets.strong++;
      else if (s > 0.3) buckets.moderate++;
      else if (s > 0.1) buckets.weak++;
      else buckets.prune++;
    }

    return {
      shape: this.shape,
      scale: this.scale,
      total: memories.length,
      buckets,
      avgStrength: strengths.length 
        ? strengths.reduce((a, b) => a + b, 0) / strengths.length 
        : 0,
    };
  }
}

// 导出单例
let _instance = null;
export function getWeibullDecayModel(opts = {}) {
  if (!_instance) {
    _instance = new WeibullDecayModel(opts);
  }
  return _instance;
}
