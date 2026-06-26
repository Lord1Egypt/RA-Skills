/**
 * 历史数据模块
 * 提供股票历史价格查询功能
 */

import yahooFinance from 'yahoo-finance2';

export class HistoryModule {
  constructor(options = {}) {
    this.options = options;
  }

  /**
   * 获取历史股价数据
   * @param {string} symbol - 股票代码
   * @param {string} period - 时间周期
   * @returns {Promise<Object>} 历史数据
   */
  async getHistory(symbol, period = '1mo') {
    try {
      const period1 = this._calculatePeriodStart(period);
      const history = await yahooFinance.chart(symbol, {
        period1: period1,
        interval: this._getInterval(period)
      });

      const quotes = history.quotes.map(q => ({
        date: q.date.toISOString().split('T')[0],
        open: q.open,
        high: q.high,
        low: q.low,
        close: q.close,
        volume: q.volume
      }));

      return {
        success: true,
        data: {
          symbol: symbol,
          period: period,
          quotes: quotes,
          count: quotes.length
        },
        message: `成功获取 ${symbol} 过去 ${period} 历史数据，共 ${quotes.length} 条记录`
      };
    } catch (error) {
      return {
        success: false,
        data: null,
        message: `获取 ${symbol} 历史数据失败：${error.message}`,
        error: error.message
      };
    }
  }

  /**
   * 计算周期起始时间
   * @private
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
      'ytd': this._getDaysSinceYearStart(),
      'max': 36500
    };
    
    const days = periods[period] || 30;
    now.setDate(now.getDate() - days);
    return now;
  }

  /**
   * 获取时间间隔
   * @private
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
      'ytd': '1d',
      'max': '1mo'
    };
    
    return intervals[period] || '1d';
  }

  /**
   * 获取年初至今的天数
   * @private
   */
  _getDaysSinceYearStart() {
    const now = new Date();
    const start = new Date(now.getFullYear(), 0, 1);
    const diff = now - start;
    return Math.floor(diff / (1000 * 60 * 60 * 24));
  }
}
