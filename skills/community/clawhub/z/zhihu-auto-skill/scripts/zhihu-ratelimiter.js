/**
 * zhihu-ratelimiter.js — 分层速率控制器
 *
 * 三层速率控制:
 * 1. HTTP 读: 200-500ms 间隔
 * 2. 浏览器写: 5-10s 间隔 + 随机抖动
 * 3. 限流恢复: 指数退避
 *
 * I12 | I20 (Plan B 降级速率)
 */

import { sleep } from './zhihu-core.js';

// ──────────────────────────────────────────
// 速率配置
// ──────────────────────────────────────────

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

const BACKOFF = {
  initial: 30_000,     // 30s
  multiplier: 2,        // 翻倍
  maxDelay: 600_000,    // 10min
};

// ──────────────────────────────────────────
// RateLimiter 类
// ──────────────────────────────────────────

class RateLimiter {
  constructor(tier = 'http') {
    this.tier = tier;
    this._lastCallTime = 0;
    this._backoffStep = 0;
    this._backoffUntil = 0;
    this._totalCalls = 0;
  }

  /**
   * 获取当前层级的配置
   */
  _getConfig() {
    let config = TIERS[this.tier];
    if (!config) {
      console.warn(`[ratelimiter] 未知层级 ${this.tier}，回退到 http`);
      config = TIERS.http;
    }
    return config;
  }

  /**
   * 切换到指定层级
   */
  setTier(tier) {
    if (TIERS[tier]) {
      this.tier = tier;
      console.log(`[ratelimiter] 切换到 ${TIERS[tier].name} 层级`);
    }
  }

  /**
   * 等待（阻塞直到允许下一次调用）
   */
  async wait() {
    // 检查是否在退避期
    if (this._backoffUntil > Date.now()) {
      const remaining = this._backoffUntil - Date.now();
      console.log(`[ratelimiter] 限流退避中，剩余 ${Math.round(remaining / 1000)}s`);
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
   */
  triggerBackoff() {
    this._backoffStep = Math.min(this._backoffStep + 1, 10);
    const delay = Math.min(
      BACKOFF.initial * Math.pow(BACKOFF.multiplier, this._backoffStep - 1),
      BACKOFF.maxDelay
    );
    this._backoffUntil = Date.now() + delay;
    console.log(
      `[ratelimiter] 🚨 触发退避 (step ${this._backoffStep})，等待 ${Math.round(delay / 1000)}s`
    );
  }

  /**
   * 重置退避（成功调用后）
   */
  resetBackoff() {
    if (this._backoffStep > 0) {
      this._backoffStep = 0;
      this._backoffUntil = 0;
      console.log('[ratelimiter] 退避已重置');
    }
  }

  /**
   * 获取统计信息
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

const httpRateLimiter = new RateLimiter('http');
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
