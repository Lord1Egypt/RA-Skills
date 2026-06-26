/**
 * YahooClaw 核心模块
 * 提供股票数据查询功能
 */

import yahooFinance from 'yahoo-finance2';

export class QuoteModule {
  constructor(options = {}) {
    this.options = {
      lang: options.lang || 'zh-CN',
      region: options.region || 'US',
      ...options
    };
  }

  /**
   * 获取实时股价
   * @param {string} symbol - 股票代码
   * @returns {Promise<Object>} 股价数据
   */
  async getQuote(symbol) {
    try {
      const quote = await yahooFinance.quote(symbol);
      
      return {
        success: true,
        data: {
          symbol: quote.symbol,
          name: quote.shortName || quote.longName,
          price: quote.regularMarketPrice,
          change: quote.regularMarketChange,
          changePercent: quote.regularMarketChangePercent,
          previousClose: quote.regularMarketPreviousClose,
          open: quote.regularMarketOpen,
          dayHigh: quote.regularMarketDayHigh,
          dayLow: quote.regularMarketDayLow,
          volume: quote.regularMarketVolume,
          marketCap: quote.marketCap,
          pe: quote.trailingPE,
          eps: quote.trailingEps,
          dividend: quote.trailingAnnualDividendRate,
          yield: quote.trailingAnnualDividendYield,
          currency: quote.currency,
          exchange: quote.exchange,
          marketState: quote.marketState,
          timestamp: new Date().toISOString()
        },
        message: `成功获取 ${symbol} 股价数据`
      };
    } catch (error) {
      return {
        success: false,
        data: null,
        message: `获取 ${symbol} 股价失败：${error.message}`,
        error: error.message
      };
    }
  }

  /**
   * 批量获取股价
   * @param {Array<string>} symbols - 股票代码数组
   * @returns {Promise<Object>} 股价数据数组
   */
  async getQuotes(symbols) {
    const results = await Promise.all(
      symbols.map(symbol => this.getQuote(symbol))
    );
    
    return {
      success: true,
      data: results.filter(r => r.success).map(r => r.data),
      failed: results.filter(r => !r.success).map(r => ({
        symbol: symbols[results.indexOf(r)],
        error: r.error
      })),
      message: `成功获取 ${results.filter(r => r.success).length}/${symbols.length} 个股票数据`
    };
  }
}
