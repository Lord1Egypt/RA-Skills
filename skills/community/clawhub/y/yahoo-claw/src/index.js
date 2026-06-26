/**
 * YahooClaw 主文件
 * 统一导出所有模块
 */

import { QuoteModule } from './modules/Quote.js';
import { HistoryModule } from './modules/History.js';
import { TechnicalModule } from './modules/Technical.js';
import { NewsModule } from './modules/News.js';

/**
 * YahooClaw 主类
 */
export class YahooClaw {
  constructor(options = {}) {
    this.options = {
      lang: options.lang || 'zh-CN',
      region: options.region || 'US',
      ...options
    };

    // 初始化各模块
    this.quote = new QuoteModule(this.options);
    this.history = new HistoryModule(this.options);
    this.technical = new TechnicalModule(this.options);
    this.news = new NewsModule(this.options);
  }

  /**
   * 获取实时股价（兼容旧 API）
   */
  async getQuote(symbol) {
    return this.quote.getQuote(symbol);
  }

  /**
   * 获取历史数据（兼容旧 API）
   */
  async getHistory(symbol, period = '1mo') {
    return this.history.getHistory(symbol, period);
  }

  /**
   * 获取技术指标（兼容旧 API）
   */
  async getTechnicalIndicators(symbol, period = '1mo', indicators = ['MA', 'RSI', 'MACD']) {
    // 先获取历史数据
    const historyResult = await this.history.getHistory(symbol, period);
    
    if (!historyResult.success) {
      return historyResult;
    }

    const quotes = historyResult.data.quotes;
    const closes = quotes.map(q => q.close);
    const highs = quotes.map(q => q.high);
    const lows = quotes.map(q => q.low);

    // 计算技术指标
    const technicalData = this.technical.calculate(closes, highs, lows, indicators);

    return {
      success: true,
      data: {
        symbol: symbol,
        period: period,
        timestamp: new Date().toISOString(),
        ...technicalData
      },
      message: `成功获取 ${symbol} 技术指标分析`
    };
  }

  /**
   * 获取新闻（兼容旧 API）
   */
  async getNews(symbol, options = {}) {
    return this.news.getNews(symbol, options);
  }
}

// 导出默认实例
const yahooclaw = new YahooClaw();

export default yahooclaw;
