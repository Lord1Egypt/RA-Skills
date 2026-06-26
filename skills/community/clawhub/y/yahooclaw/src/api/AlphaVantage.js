/**
 * Alpha Vantage API 模块
 * 备用数据源，提供股票数据查询
 * 免费额度：500 次/天
 */

// API Key 必须从环境变量获取，不能硬编码
const API_KEY = process.env.ALPHA_VANTAGE_API_KEY;

if (!API_KEY) {
  console.warn('⚠️  ALPHA_VANTAGE_API_KEY not set. Please set environment variable.');
}

const BASE_URL = 'https://www.alphavantage.co/query';

export class AlphaVantageAPI {
  constructor(options = {}) {
    this.options = {
      apiKey: API_KEY,
      timeout: 10000,
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
      const url = `${BASE_URL}?function=GLOBAL_QUOTE&symbol=${symbol}&apikey=${this.options.apiKey}`;
      const response = await fetch(url);
      const data = await response.json();

      if (data['Global Quote'] && data['Global Quote']['05. price']) {
        const quote = data['Global Quote'];
        return {
          success: true,
          source: 'AlphaVantage',
          data: {
            symbol: quote['01. symbol'],
            price: parseFloat(quote['05. price']),
            change: parseFloat(quote['09. change']),
            changePercent: quote['10. change percent'],
            open: parseFloat(quote['02. open']),
            high: parseFloat(quote['03. high']),
            low: parseFloat(quote['04. low']),
            previousClose: parseFloat(quote['08. previous close']),
            volume: parseInt(quote['06. volume']),
            timestamp: new Date().toISOString()
          },
          message: `成功获取 ${symbol} 股价数据 (Alpha Vantage)`
        };
      } else if (data['Note']) {
        return {
          success: false,
          source: 'AlphaVantage',
          data: null,
          message: `Alpha Vantage API 限流：${data['Note']}`,
          error: 'RATE_LIMIT'
        };
      } else {
        return {
          success: false,
          source: 'AlphaVantage',
          data: null,
          message: `获取 ${symbol} 股价失败：数据格式错误`,
          error: 'INVALID_DATA'
        };
      }
    } catch (error) {
      return {
        success: false,
        source: 'AlphaVantage',
        data: null,
        message: `获取 ${symbol} 股价失败：${error.message}`,
        error: error.message
      };
    }
  }

  /**
   * 获取历史数据
   * @param {string} symbol - 股票代码
   * @param {string} period - 时间周期
   * @returns {Promise<Object>} 历史数据
   */
  async getHistory(symbol, period = '1mo') {
    try {
      const interval = this._getInterval(period);
      const url = `${BASE_URL}?function=TIME_SERIES_DAILY&symbol=${symbol}&outputsize=compact&apikey=${this.options.apiKey}`;
      
      const response = await fetch(url);
      const data = await response.json();

      // 调试输出
      console.log(`[AlphaVantage] 请求 ${symbol} 历史数据...`);
      console.log(`[AlphaVantage] 返回数据结构:`, Object.keys(data));

      if (data['Time Series (Daily)']) {
        const timeSeries = data['Time Series (Daily)'];
        
        // 更健壮的数据解析
        const quotes = Object.entries(timeSeries).map(([date, values]) => {
          try {
            return {
              date: date,
              open: parseFloat(values['1. open'] || '0'),
              high: parseFloat(values['2. high'] || '0'),
              low: parseFloat(values['3. low'] || '0'),
              close: parseFloat(values['4. close'] || '0'),
              volume: parseInt(values['5. volume'] || '0')
            };
          } catch (error) {
            console.warn(`[AlphaVantage] 解析 ${date} 数据失败:`, error.message);
            return null;
          }
        }).filter(q => q !== null && q.close > 0); // 过滤无效数据

        // 根据周期限制返回数据量
        const limit = this._getLimit(period);
        const limitedQuotes = quotes.slice(0, limit);

        console.log(`[AlphaVantage] ✅ 成功获取 ${symbol} ${limitedQuotes.length} 条记录`);

        return {
          success: true,
          source: 'AlphaVantage',
          data: {
            symbol: symbol,
            period: period,
            quotes: limitedQuotes,
            count: limitedQuotes.length
          },
          message: `成功获取 ${symbol} 历史数据，共 ${limitedQuotes.length} 条记录 (Alpha Vantage)`
        };
      } else if (data['Note']) {
        console.warn(`[AlphaVantage] ⚠️ 限流：${data['Note']}`);
        return {
          success: false,
          source: 'AlphaVantage',
          data: null,
          message: `Alpha Vantage API 限流：${data['Note']}`,
          error: 'RATE_LIMIT'
        };
      } else if (data['Information']) {
        console.warn(`[AlphaVantage] ⚠️ API 信息：${data['Information']}`);
        return {
          success: false,
          source: 'AlphaVantage',
          data: null,
          message: `API 限制：${data['Information']}`,
          error: 'API_LIMIT'
        };
      } else if (data['Error Message']) {
        console.error(`[AlphaVantage] ❌ 错误：${data['Error Message']}`);
        return {
          success: false,
          source: 'AlphaVantage',
          data: null,
          message: `API 错误：${data['Error Message']}`,
          error: 'API_ERROR'
        };
      } else {
        console.error(`[AlphaVantage] ❌ 未知数据格式:`, JSON.stringify(data, null, 2));
        return {
          success: false,
          source: 'AlphaVantage',
          data: null,
          message: `获取 ${symbol} 历史数据失败：未知数据格式`,
          error: 'INVALID_DATA',
          debug: data
        };
      }
    } catch (error) {
      console.error(`[AlphaVantage] ❌ 异常：${error.message}`);
      return {
        success: false,
        source: 'AlphaVantage',
        data: null,
        message: `获取 ${symbol} 历史数据失败：${error.message}`,
        error: error.message
      };
    }
  }

  /**
   * 获取技术指标
   * @param {string} symbol - 股票代码
   * @param {string} indicator - 指标类型
   * @param {Object} params - 指标参数
   * @returns {Promise<Object>} 技术指标数据
   */
  async getTechnicalIndicator(symbol, indicator, params = {}) {
    try {
      const url = `${BASE_URL}?function=${indicator}&symbol=${symbol}&apikey=${this.options.apiKey}${this._buildParams(params)}`;
      
      const response = await fetch(url);
      const data = await response.json();

      return {
        success: true,
        source: 'AlphaVantage',
        data: data,
        message: `成功获取 ${symbol} ${indicator} 指标 (Alpha Vantage)`
      };
    } catch (error) {
      return {
        success: false,
        source: 'AlphaVantage',
        data: null,
        message: `获取 ${symbol} ${indicator} 指标失败：${error.message}`,
        error: error.message
      };
    }
  }

  /**
   * 获取时间间隔
   * @private
   */
  _getInterval(period) {
    const intervals = {
      '1d': '1min',
      '5d': '5min',
      '1mo': 'daily',
      '3mo': 'daily',
      '6mo': 'daily',
      '1y': 'weekly',
      '2y': 'weekly',
      '5y': 'monthly'
    };
    return intervals[period] || 'daily';
  }

  /**
   * 获取数据量限制
   * @private
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
      '5y': 1825
    };
    return limits[period] || 30;
  }

  /**
   * 构建参数字符串
   * @private
   */
  _buildParams(params) {
    return Object.entries(params)
      .map(([key, value]) => `&${key}=${value}`)
      .join('');
  }
}
