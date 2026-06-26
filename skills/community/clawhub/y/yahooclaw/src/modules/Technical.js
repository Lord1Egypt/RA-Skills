/**
 * 技术指标模块
 * 提供 7 大主流技术分析指标
 */

export class TechnicalModule {
  constructor(options = {}) {
    this.options = options;
  }

  /**
   * 获取技术指标分析
   * @param {Array<number>} closes - 收盘价数组
   * @param {Array<number>} highs - 最高价数组
   * @param {Array<number>} lows - 最低价数组
   * @param {Array<string>} indicators - 指标列表
   * @returns {Object} 技术指标数据
   */
  calculate(closes, highs, lows, indicators = ['MA', 'RSI', 'MACD']) {
    const result = {
      indicators: {},
      analysis: null
    };

    // 计算各个技术指标
    if (indicators.includes('MA')) {
      result.indicators.MA = {
        MA5: this._calculateMA(closes, 5),
        MA10: this._calculateMA(closes, 10),
        MA20: this._calculateMA(closes, 20),
        MA50: this._calculateMA(closes, 50),
        MA200: this._calculateMA(closes, 200)
      };
    }

    if (indicators.includes('EMA')) {
      result.indicators.EMA = {
        EMA12: this._calculateEMA(closes, 12),
        EMA26: this._calculateEMA(closes, 26),
        EMA50: this._calculateEMA(closes, 50)
      };
    }

    if (indicators.includes('RSI')) {
      const rsi = this._calculateRSI(closes, 14);
      result.indicators.RSI = {
        RSI14: rsi,
        signal: this._getRSISignal(rsi)
      };
    }

    if (indicators.includes('MACD')) {
      result.indicators.MACD = this._calculateMACD(closes);
    }

    if (indicators.includes('BOLL')) {
      result.indicators.BOLL = this._calculateBollingerBands(closes);
    }

    if (indicators.includes('KDJ')) {
      result.indicators.KDJ = this._calculateKDJ(highs, lows, closes);
    }

    // 综合信号分析
    result.analysis = this._getTechnicalAnalysis(result.indicators);

    return result;
  }

  /**
   * 计算简单移动平均线 (MA)
   * @private
   */
  _calculateMA(data, period) {
    if (data.length < period) return null;
    
    const slice = data.slice(-period);
    const sum = slice.reduce((a, b) => a + b, 0);
    const ma = sum / period;
    
    return {
      value: parseFloat(ma.toFixed(2)),
      period: period,
      trend: data[data.length - 1] > ma ? 'BULLISH' : 'BEARISH'
    };
  }

  /**
   * 计算指数移动平均线 (EMA)
   * @private
   */
  _calculateEMA(data, period) {
    if (data.length < period) return null;

    const multiplier = 2 / (period + 1);
    let ema = data.slice(0, period).reduce((a, b) => a + b, 0) / period;

    for (let i = period; i < data.length; i++) {
      ema = (data[i] - ema) * multiplier + ema;
    }

    return {
      value: parseFloat(ema.toFixed(2)),
      period: period,
      trend: data[data.length - 1] > ema ? 'BULLISH' : 'BEARISH'
    };
  }

  /**
   * 计算相对强弱指数 (RSI)
   * @private
   */
  _calculateRSI(data, period = 14) {
    if (data.length < period + 1) return null;

    let gains = 0;
    let losses = 0;

    for (let i = 1; i <= period; i++) {
      const change = data[i] - data[i - 1];
      if (change > 0) gains += change;
      else losses += Math.abs(change);
    }

    let avgGain = gains / period;
    let avgLoss = losses / period;

    for (let i = period + 1; i < data.length; i++) {
      const change = data[i] - data[i - 1];
      const gain = change > 0 ? change : 0;
      const loss = change < 0 ? Math.abs(change) : 0;

      avgGain = (avgGain * (period - 1) + gain) / period;
      avgLoss = (avgLoss * (period - 1) + loss) / period;
    }

    const rs = avgGain / avgLoss;
    const rsi = 100 - (100 / (1 + rs));

    return parseFloat(rsi.toFixed(2));
  }

  /**
   * 获取 RSI 信号
   * @private
   */
  _getRSISignal(rsi) {
    if (rsi >= 70) return 'OVERBOUGHT';
    if (rsi <= 30) return 'OVERSOLD';
    if (rsi >= 50) return 'BULLISH';
    return 'BEARISH';
  }

  /**
   * 计算 MACD
   * @private
   */
  _calculateMACD(data) {
    const ema12 = this._calculateEMA(data, 12);
    const ema26 = this._calculateEMA(data, 26);

    if (!ema12 || !ema26) return null;

    const macdLine = ema12.value - ema26.value;
    
    const macdValues = [];
    for (let i = 26; i < data.length; i++) {
      const slice = data.slice(0, i + 1);
      const e12 = this._calculateEMA(slice, 12);
      const e26 = this._calculateEMA(slice, 26);
      if (e12 && e26) {
        macdValues.push(e12.value - e26.value);
      }
    }

    const signalLine = this._calculateEMA(macdValues, 9);
    const histogram = macdLine - (signalLine ? signalLine.value : 0);

    return {
      macdLine: parseFloat(macdLine.toFixed(2)),
      signalLine: signalLine ? parseFloat(signalLine.value.toFixed(2)) : null,
      histogram: parseFloat(histogram.toFixed(2)),
      trend: macdLine > 0 ? 'BULLISH' : 'BEARISH',
      crossover: signalLine ? (macdLine > signalLine.value ? 'GOLDEN' : 'DEATH') : null
    };
  }

  /**
   * 计算布林带
   * @private
   */
  _calculateBollingerBands(data, period = 20, stdDev = 2) {
    if (data.length < period) return null;

    const slice = data.slice(-period);
    const middle = slice.reduce((a, b) => a + b, 0) / period;
    
    const variance = slice.reduce((sum, price) => {
      return sum + Math.pow(price - middle, 2);
    }, 0) / period;
    
    const std = Math.sqrt(variance);
    const upper = middle + (stdDev * std);
    const lower = middle - (stdDev * std);
    const currentPrice = data[data.length - 1];

    let position = 'MIDDLE';
    if (currentPrice >= upper) position = 'OVERBOUGHT';
    else if (currentPrice <= lower) position = 'OVERSOLD';
    else if (currentPrice > middle) position = 'UPPER_HALF';
    else position = 'LOWER_HALF';

    return {
      upper: parseFloat(upper.toFixed(2)),
      middle: parseFloat(middle.toFixed(2)),
      lower: parseFloat(lower.toFixed(2)),
      bandwidth: parseFloat(((upper - lower) / middle * 100).toFixed(2)),
      percentB: parseFloat(((currentPrice - lower) / (upper - lower) * 100).toFixed(2)),
      position: position,
      period: period
    };
  }

  /**
   * 计算 KDJ
   * @private
   */
  _calculateKDJ(highs, lows, closes, period = 9) {
    if (closes.length < period) return null;

    const kValues = [];

    for (let i = period - 1; i < closes.length; i++) {
      const sliceHighs = highs.slice(i - period + 1, i + 1);
      const sliceLows = lows.slice(i - period + 1, i + 1);
      const currentClose = closes[i];

      const highestHigh = Math.max(...sliceHighs);
      const lowestLow = Math.min(...sliceLows);
      const rsv = ((currentClose - lowestLow) / (highestHigh - lowestLow)) * 100;
      kValues.push(rsv);
    }

    const k = kValues.length >= 3 
      ? kValues.slice(-3).reduce((a, b) => a + b, 0) / 3 
      : kValues[kValues.length - 1];

    const d = kValues.length >= 3 
      ? kValues.slice(-3).reduce((a, b) => a + b, 0) / 3 
      : k;

    const j = 3 * k - 2 * d;

    return {
      k: parseFloat(k.toFixed(2)),
      d: parseFloat(d.toFixed(2)),
      j: parseFloat(j.toFixed(2)),
      signal: k > 80 ? 'OVERBOUGHT' : k < 20 ? 'OVERSOLD' : k > d ? 'BULLISH' : 'BEARISH',
      crossover: k > d ? 'GOLDEN' : 'DEATH'
    };
  }

  /**
   * 获取综合技术分析
   * @private
   */
  _getTechnicalAnalysis(indicators) {
    const signals = { bullish: 0, bearish: 0, neutral: 0 };
    const details = [];

    // 分析 MA 趋势
    if (indicators.MA && indicators.MA.MA5) {
      if (indicators.MA.MA5.trend === 'BULLISH') {
        signals.bullish++;
        details.push('MA5: 看涨');
      } else {
        signals.bearish++;
        details.push('MA5: 看跌');
      }
    }

    // 分析 RSI
    if (indicators.RSI) {
      if (indicators.RSI.signal === 'OVERBOUGHT') {
        signals.bearish++;
        details.push(`RSI: 超买 (${indicators.RSI.RSI14})`);
      } else if (indicators.RSI.signal === 'OVERSOLD') {
        signals.bullish++;
        details.push(`RSI: 超卖 (${indicators.RSI.RSI14})`);
      } else if (indicators.RSI.signal === 'BULLISH') {
        signals.bullish++;
        details.push('RSI: 看涨');
      } else {
        signals.bearish++;
        details.push('RSI: 看跌');
      }
    }

    // 分析 MACD
    if (indicators.MACD) {
      if (indicators.MACD.trend === 'BULLISH') {
        signals.bullish++;
        details.push('MACD: 看涨');
      } else {
        signals.bearish++;
        details.push('MACD: 看跌');
      }
      
      if (indicators.MACD.crossover === 'GOLDEN') {
        signals.bullish++;
        details.push('MACD: 金叉');
      } else if (indicators.MACD.crossover === 'DEATH') {
        signals.bearish++;
        details.push('MACD: 死叉');
      }
    }

    // 分析布林带
    if (indicators.BOLL) {
      if (indicators.BOLL.position === 'OVERSOLD') {
        signals.bullish++;
        details.push('布林带：超卖');
      } else if (indicators.BOLL.position === 'OVERBOUGHT') {
        signals.bearish++;
        details.push('布林带：超买');
      }
    }

    // 分析 KDJ
    if (indicators.KDJ) {
      if (indicators.KDJ.signal === 'OVERSOLD' || indicators.KDJ.crossover === 'GOLDEN') {
        signals.bullish++;
        details.push('KDJ: 看涨信号');
      } else if (indicators.KDJ.signal === 'OVERBOUGHT' || indicators.KDJ.crossover === 'DEATH') {
        signals.bearish++;
        details.push('KDJ: 看跌信号');
      }
    }

    // 综合判断
    let overallSignal = 'NEUTRAL';
    let confidence = 50;

    const total = signals.bullish + signals.bearish;
    if (total > 0) {
      const bullishPercent = signals.bullish / total;
      
      if (bullishPercent >= 0.7) {
        overallSignal = 'STRONG_BUY';
        confidence = Math.round(bullishPercent * 100);
      } else if (bullishPercent >= 0.6) {
        overallSignal = 'BUY';
        confidence = Math.round(bullishPercent * 100);
      } else if (bullishPercent <= 0.3) {
        overallSignal = 'STRONG_SELL';
        confidence = Math.round((1 - bullishPercent) * 100);
      } else if (bullishPercent <= 0.4) {
        overallSignal = 'SELL';
        confidence = Math.round((1 - bullishPercent) * 100);
      }
    }

    return {
      signal: overallSignal,
      confidence: confidence,
      bullish: signals.bullish,
      bearish: signals.bearish,
      neutral: signals.neutral,
      details: details,
      recommendation: this._getRecommendation(overallSignal, confidence)
    };
  }

  /**
   * 获取投资建议
   * @private
   */
  _getRecommendation(signal, confidence) {
    const recommendations = {
      'STRONG_BUY': `强烈建议买入 (置信度：${confidence}%) - 多个技术指标显示上涨信号`,
      'BUY': `建议买入 (置信度：${confidence}%) - 多数技术指标看涨`,
      'NEUTRAL': `观望 - 技术指标分化，建议等待更明确信号`,
      'SELL': `建议卖出 (置信度：${confidence}%) - 多数技术指标看跌`,
      'STRONG_SELL': `强烈建议卖出 (置信度：${confidence}%) - 多个技术指标显示下跌信号`
    };

    return recommendations[signal] || recommendations['NEUTRAL'];
  }
}
