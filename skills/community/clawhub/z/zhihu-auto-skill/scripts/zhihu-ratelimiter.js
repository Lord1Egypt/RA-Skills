/**
 * zhihu-ratelimiter.js — 分层速率控制器
 *
 * 三层速率控制:
 * 1. HTTP 读: 200-500ms 间隔
 * 2. 浏览器写: 5-10s 间隔 + 随机抖动
 * 3. 限流恢复: 指数退避
 *
 * I12 | I20 (Plan B 降级速率)
 *
 * @module zhihu-ratelimiter
 */

import { sleep } from './zhihu-core.js';
import { ratelimiterLog } from './zhihu-logger.js';

// ──────────────────────────────────────────
// 速率配置
// ──────────────────────────────────────────

/** @type {Record<string,{name:string, minInterval:number, maxInterval:number, description:string}>} 层级配置 */
const TIERS = {
  http: {
    name: 'http',
    minInterval: 200,    // ms
    maxInterval: 500,    // ms
    description: 'HTTP 读操作',
  },
  browser: {
    name: 'browser',
    minInterval: 5000,   // ms
    maxInterval: 10000,  // ms
    description: '浏览器写操作',
  },
  degraded: {
    name: 'degraded',
    minInterval: 5000,   // ms (Plan B 降级时 HTTP 通道切换到浏览器速率)
    maxInterval: 10000,
    description: 'Plan B 降级模式',
  },
};

// ──────────────────────────────────────────
// 指数退避
// ──────────────────────────────────────────

/** @type {{initial:number, multiplier:number, maxDelay:number}} 退避配置 */
const BACKOFF = {
  initial: 30_000,     // 30s
  multiplier: 2,        // 翻倍
  maxDelay: 600_000,    // 10min
};

// ──────────────────────────────────────────
// RateLimiter 类
// ──────────────────────────────────────────

/**
 * 分层速率控制器
 */
class RateLimiter {
  /**
   * @param {string} [tier='http'] - 初始层级
   */
  constructor(tier = 'http') {
    /** @type {string} 当前层级 */
    this.tier = tier;
    /** @type {number} 上次调用时间戳 */
    this._lastCallTime = 0;
    /** @type {number} 退避步数 */
    this._backoffStep = 0;
    /** @type {number} 退避结束时间戳 */
    this._backoffUntil = 0;
    /** @type {number} 总调用次数 */
    this._totalCalls = 0;
  }

  /**
   * 获取当前层级的配置
   * @returns {{name:string, minInterval:number, maxInterval:number}} 层级配置
   */
  _getConfig() {
    let config = TIERS[this.tier];
    if (!config) {
      ratelimiterLog.warn(`未知层级 ${this.tier}，回退到 http`);
      config = TIERS.http;
    }
    return config;
  }

  /**
   * 切换到指定层级
   * @param {string} tier - 层级名称
   * @returns {void}
   */
  setTier(tier) {
    if (TIERS[tier]) {
      this.tier = tier;
      ratelimiterLog.info(`切换到 ${TIERS[tier].name} 层级`);
    }
  }

  /**
   * 等待（阻塞直到允许下一次调用）
   * @returns {Promise<void>}
   */
  async wait() {
    // 检查是否在退避期
    if (this._backoffUntil > Date.now()) {
      const remaining = this._backoffUntil - Date.now();
      ratelimiterLog.info(`限流退避中，剩余 ${Math.round(remaining / 1000)}s`);
      await sleep(remaining);
    }

    const config = this._getConfig();
    const now = Date.now();
    const elapsed = now - this._lastCallTime;
    const interval = config.minInterval + Math.floor(
      Math.random() * (config.maxInterval - config.minInterval + 1)
    );

    if (elapsed < interval) {
      const waitTime = interval - elapsed;
      await sleep(waitTime);
    }

    this._lastCallTime = Date.now();
    this._totalCalls++;
  }

  /**
   * 触发限流退避
   * 当收到 429 状态码时调用
   * @returns {void}
   */
  triggerBackoff() {
    this._backoffStep = Math.min(this._backoffStep + 1, 10);
    const delay = Math.min(
      BACKOFF.initial * Math.pow(BACKOFF.multiplier, this._backoffStep - 1),
      BACKOFF.maxDelay
    );
    this._backoffUntil = Date.now() + delay;
    ratelimiterLog.warn(
      `🚨 触发退避 (step ${this._backoffStep})，等待 ${Math.round(delay / 1000)}s`
    );
  }

  /**
   * 重置退避（成功调用后）
   * @returns {void}
   */
  resetBackoff() {
    if (this._backoffStep > 0) {
      this._backoffStep = 0;
      this._backoffUntil = 0;
      ratelimiterLog.info('退避已重置');
    }
  }

  /**
   * 获取统计信息
   * @returns {{ tier: string, totalCalls: number, backoffStep: number, isBackingOff: boolean }}
   */
  getStats() {
    return {
      tier: this.tier,
      totalCalls: this._totalCalls,
      backoffStep: this._backoffStep,
      isBackingOff: this._backoffUntil > Date.now(),
    };
  }
}

// ──────────────────────────────────────────
// 预配置实例
// ──────────────────────────────────────────

/** @type {RateLimiter} HTTP 速率限制器 */
const httpRateLimiter = new RateLimiter('http');
/** @type {RateLimiter} 浏览器速率限制器 */
const browserRateLimiter = new RateLimiter('browser');

// ──────────────────────────────────────────
// 导出
// ──────────────────────────────────────────

export {
  RateLimiter,
  TIERS,
  httpRateLimiter,
  browserRateLimiter,
};
