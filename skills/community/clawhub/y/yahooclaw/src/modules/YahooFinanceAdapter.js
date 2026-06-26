/**
 * Yahoo Finance API 适配器
 * 统一接口格式，供 API Manager 调用
 */

import yahooFinance from 'yahoo-finance2';

export class YahooFinanceAdapter {
  constructor(options = {}) {
    this.options = options;
  }

  /**
   * 获取实时股价
   */
  async getQuote(symbol) {
    try {
      const quote = await yahooFinance.quote(symbol);
      
      return {
        success: true,
        source: 'YahooFinance',
        data: {
          symbol: quote.symbol,
          name: quote.shortName || quote.longName,
          price: quote.regularMarketPrice,
          change: quote.regularMarketChange,
          changePercent: quote.regularMarketChangePercent,
          open: quote.regularMarketOpen,
          high: quote.regularMarketDayHigh,
          low: quote.regularMarketDayLow,
          previousClose: quote.regularMarketPreviousClose,
          volume: quote.regularMarketVolume,
          marketCap: quote.marketCap,
          timestamp: new Date().toISOString()
        },
        message: `成功获取 ${symbol} 股价数据 (Yahoo Finance)`
      };
    } catch (error) {
      if (error.message.includes('429')) {
        return {
          success: false,
          source: 'YahooFinance',
          data: null,
          message: 'Yahoo Finance API 限流',
          error: 'RATE_LIMIT'
        };
      }
      
      return {
        success: false,
        source: 'YahooFinance',
        data: null,
        message: `获取 ${symbol} 股价失败：${error.message}`,
        error: error.message
      };
    }
  }

  /**
   * 获取历史数据
   */
  async getHistory(symbol, period = '1mo') {
    try {
      const period1 = this._calculatePeriodStart(period);
      const interval = this._getInterval(period);
      
      const history = await yahooFinance.chart(symbol, {
        period1: period1,
        interval: interval
      });

      const quotes = history.quotes.map(q => ({
        date: q.date.toISOString().split('T')[0],
        open: q.open,
        high: q.high,
        low: q.low,
        close: q.close,
        volume: q.volume
      }));

      const limit = this._getLimit(period);
      const limitedQuotes = quotes.slice(0, limit);

      return {
        success: true,
        source: 'YahooFinance',
        data: {
          symbol: symbol,
          period: period,
          quotes: limitedQuotes,
          count: limitedQuotes.length
        },
        message: `成功获取 ${symbol} 历史数据，共 ${limitedQuotes.length} 条记录 (Yahoo Finance)`
      };
    } catch (error) {
      if (error.message.includes('429') || error.message.includes('Too Many Requests')) {
        return {
          success: false,
          source: 'YahooFinance',
          data: null,
          message: 'Yahoo Finance API 限流',
          error: 'RATE_LIMIT'
        };
      }
      
      return {
        success: false,
        source: 'YahooFinance',
        data: null,
        message: `获取 ${symbol} 历史数据失败：${error.message}`,
        error: error.message
      };
    }
  }

  /**
   * 计算周期起始时间
   */
  _calculatePeriodStart(period) {
    const now = new Date();
    const periods = {
      '1d': 1,
      '5d': 5,
      '1mo': 30,
      '3mo': 90,
      '6mo': 180,
      '1y': 365,
      '2y': 730,
      '5y': 1825,
      '10y': 3650,
      'max': 36500
    };
    
    const days = periods[period] || 30;
    now.setDate(now.getDate() - days);
    return now;
  }

  /**
   * 获取时间间隔
   */
  _getInterval(period) {
    const intervals = {
      '1d': '1m',
      '5d': '15m',
      '1mo': '1d',
      '3mo': '1d',
      '6mo': '1d',
      '1y': '1d',
      '2y': '1d',
      '5y': '1wk',
      '10y': '1mo',
      'max': '1mo'
    };
    return intervals[period] || '1d';
  }

  /**
   * 获取数据量限制
   */
  _getLimit(period) {
    const limits = {
      '1d': 1,
      '5d': 5,
      '1mo': 30,
      '3mo': 90,
      '6mo': 180,
      '1y': 365,
      '2y': 730,
      '5y': 1825,
      '10y': 3650,
      'max': 10000
    };
    return limits[period] || 30;
  }
}
