/**
 * API 管理器模块
 * 统一管理多个数据源，自动故障转移
 */

import { AlphaVantageAPI } from './AlphaVantage.js';

// Yahoo Finance (需要动态导入)
let YahooFinanceAPI = null;

export class APIManager {
  constructor(options = {}) {
    this.options = {
      primary: 'YahooFinance',  // 首选 API
      fallback: ['AlphaVantage'],  // 备用 API 列表
      timeout: 10000,  // 超时时间
      cache: true,  // 启用缓存
      cacheTTL: 300000,  // 缓存有效期 5 分钟
      ...options
    };

    // 初始化 API 实例
    this.apis = {
      AlphaVantage: new AlphaVantageAPI(options.alphaVantage)
    };

    // 缓存存储
    this.cache = new Map();

    // 请求统计
    this.stats = {
      total: 0,
      success: 0,
      failed: 0,
      byAPI: {}
    };
  }

  /**
   * 获取实时股价（自动故障转移）
   * @param {string} symbol - 股票代码
   * @returns {Promise<Object>} 股价数据
   */
  async getQuote(symbol) {
    return this._executeWithFallback('getQuote', symbol);
  }

  /**
   * 获取历史数据（自动故障转移）
   * @param {string} symbol - 股票代码
   * @param {string} period - 时间周期
   * @returns {Promise<Object>} 历史数据
   */
  async getHistory(symbol, period = '1mo') {
    return this._executeWithFallback('getHistory', symbol, period);
  }

  /**
   * 执行请求并自动故障转移
   * @private
   */
  async _executeWithFallback(method, ...args) {
    this.stats.total++;
    const symbol = args[0];

    // 尝试缓存
    if (this.options.cache) {
      const cacheKey = `${method}:${args.join(':')}`;
      const cached = this._getFromCache(cacheKey);
      if (cached) {
        return cached;
      }
    }

    // 构建 API 尝试列表
    const apiOrder = [this.options.primary, ...this.options.fallback];
    let lastError = null;

    for (const apiName of apiOrder) {
      try {
        // 动态加载 Yahoo Finance
        if (apiName === 'YahooFinance' && !YahooFinanceAPI) {
          try {
            const module = await import('../modules/YahooFinanceAdapter.js');
            YahooFinanceAPI = module.YahooFinanceAdapter;
          } catch (error) {
            console.warn(`无法加载 Yahoo Finance: ${error.message}`);
            continue;
          }
        }

        const api = this.apis[apiName] || new YahooFinanceAPI();
        
        // 记录 API 统计
        if (!this.stats.byAPI[apiName]) {
          this.stats.byAPI[apiName] = { total: 0, success: 0, failed: 0 };
        }
        this.stats.byAPI[apiName].total++;

        // 执行请求
        const result = await Promise.race([
          api[method](...args),
          this._timeout(this.options.timeout)
        ]);

        if (result.success) {
          this.stats.success++;
          this.stats.byAPI[apiName].success++;
          
          // 缓存结果
          if (this.options.cache) {
            const cacheKey = `${method}:${args.join(':')}`;
            this._saveToCache(cacheKey, result);
          }

          // 添加数据源标记
          result.source = apiName;
          return result;
        } else {
          this.stats.failed++;
          this.stats.byAPI[apiName].failed++;
          lastError = result.error;
          
          // 如果是限流错误，继续尝试下一个 API
          if (result.error === 'RATE_LIMIT') {
            console.warn(`${apiName} 限流，尝试下一个 API...`);
            continue;
          }
        }
      } catch (error) {
        console.warn(`${apiName} 执行失败：${error.message}`);
        lastError = error.message;
        continue;
      }
    }

    // 所有 API 都失败
    return {
      success: false,
      data: null,
      message: `所有数据源都失败，最后错误：${lastError}`,
      error: 'ALL_FAILED',
      stats: this.stats
    };
  }

  /**
   * 从缓存获取
   * @private
   */
  _getFromCache(key) {
    const cached = this.cache.get(key);
    if (cached && Date.now() - cached.timestamp < this.options.cacheTTL) {
      console.log(`✅ 使用缓存数据：${key}`);
      return cached.data;
    }
    this.cache.delete(key);
    return null;
  }

  /**
   * 保存到缓存
   * @private
   */
  _saveToCache(key, data) {
    this.cache.set(key, {
      data: data,
      timestamp: Date.now()
    });
    console.log(`💾 缓存数据：${key}`);
  }

  /**
   * 超时控制
   * @private
   */
  _timeout(ms) {
    return new Promise((_, reject) => {
      setTimeout(() => reject(new Error(`请求超时 (${ms}ms)`)), ms);
    });
  }

  /**
   * 清除缓存
   */
  clearCache() {
    this.cache.clear();
    console.log('🗑️  缓存已清除');
  }

  /**
   * 获取统计信息
   */
  getStats() {
    return {
      total: this.stats.total,
      success: this.stats.success,
      failed: this.stats.failed,
      successRate: ((this.stats.success / this.stats.total) * 100).toFixed(2) + '%',
      byAPI: this.stats.byAPI,
      cacheSize: this.cache.size
    };
  }
}
