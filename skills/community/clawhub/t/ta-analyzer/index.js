/**
 * TA Analyzer - Technical Analysis Skill for OpenClaw
 * Uses CCXT to fetch OHLCV data and calculate indicators
 * Supports multi-timeframe analysis
 */

const ccxt = require('ccxt');

// Simple technical indicators
const Indicators = {
  // Calculate RSI
  rsi: (prices, period = 14) => {
    if (prices.length < period + 1) return null;
    
    let gains = 0;
    let losses = 0;
    
    for (let i = prices.length - period; i < prices.length; i++) {
      const change = prices[i] - prices[i - 1];
      if (change > 0) gains += change;
      else losses -= change;
    }
    
    const avgGain = gains / period;
    const avgLoss = losses / period;
    
    if (avgLoss === 0) return 100;
    const rs = avgGain / avgLoss;
    return 100 - (100 / (1 + rs));
  },
  
  // Calculate SMA
  sma: (prices, period) => {
    if (prices.length < period) return null;
    const sum = prices.slice(-period).reduce((a, b) => a + b, 0);
    return sum / period;
  },
  
  // Calculate EMA
  ema: (prices, period) => {
    if (prices.length < period) return null;
    
    const multiplier = 2 / (period + 1);
    let ema = prices.slice(0, period).reduce((a, b) => a + b, 0) / period;
    
    for (let i = period; i < prices.length; i++) {
      ema = (prices[i] - ema) * multiplier + ema;
    }
    
    return ema;
  },
  
  // Calculate Bollinger Bands
  bollinger: (prices, period = 20, stdDev = 2) => {
    if (prices.length < period) return null;
    
    const sma = Indicators.sma(prices, period);
    const slice = prices.slice(-period);
    const variance = slice.reduce((sum, price) => sum + Math.pow(price - sma, 2), 0) / period;
    const std = Math.sqrt(variance);
    
    return {
      upper: sma + stdDev * std,
      middle: sma,
      lower: sma - stdDev * std
    };
  },
  
  // Calculate MACD
  macd: (prices, fast = 12, slow = 26, signal = 9) => {
    if (prices.length < slow + signal) return null;
    
    const fastEMA = Indicators.ema(prices, fast);
    const slowEMA = Indicators.ema(prices, slow);
    
    if (fastEMA === null || slowEMA === null) return null;
    
    const macdLine = fastEMA - slowEMA;
    
    // Calculate signal line (simplified)
    const macdValues = [];
    for (let i = slow; i < prices.length; i++) {
      const f = Indicators.ema(prices.slice(0, i + 1), fast);
      const s = Indicators.ema(prices.slice(0, i + 1), slow);
      if (f && s) macdValues.push(f - s);
    }
    
    const signalLine = Indicators.ema(macdValues, signal);
    
    return {
      macd: macdLine,
      signal: signalLine,
      histogram: macdLine - signalLine
    };
  },
  
  // Simple ATR calculation
  atr: (highs, lows, closes, period = 14) => {
    if (closes.length < period + 1) return null;
    
    let atr = 0;
    for (let i = 1; i <= period; i++) {
      const tr = Math.max(
        highs[highs.length - i] - lows[lows.length - i],
        Math.abs(highs[highs.length - i] - closes[closes.length - i - 1]),
        Math.abs(lows[lows.length - i] - closes[closes.length - i - 1])
      );
      atr += tr;
    }
    
    return atr / period;
  },
  
  // On Balance Volume (OBV)
  obv: (closes, volumes) => {
    if (closes.length < 2 || closes.length !== volumes.length) return null;
    
    let obv = 0;
    for (let i = 1; i < closes.length; i++) {
      if (closes[i] > closes[i - 1]) {
        obv += volumes[i];
      } else if (closes[i] < closes[i - 1]) {
        obv -= volumes[i];
      }
    }
    
    return obv;
  },
  
  // Volume SMA
  volumeSma: (volumes, period = 20) => {
    if (volumes.length < period) return null;
    const sum = volumes.slice(-period).reduce((a, b) => a + b, 0);
    return sum / period;
  },
  
  // Stochastic Oscillator
  stochastic: (highs, lows, closes, period = 14) => {
    if (closes.length < period) return null;
    
    const recentHighs = highs.slice(-period);
    const recentLows = lows.slice(-period);
    const currentClose = closes[closes.length - 1];
    
    const highest = Math.max(...recentHighs);
    const lowest = Math.min(...recentLows);
    
    if (highest === lowest) return 50;
    
    const k = ((currentClose - lowest) / (highest - lowest)) * 100;
    
    return k;
  },
  
  // ADX (Average Directional Index) - simplified
  adx: (highs, lows, closes, period = 14) => {
    if (closes.length < period * 2) return null;
    
    // Simplified ADX calculation
    let plusDM = 0, minusDM = 0;
    
    for (let i = closes.length - period; i < closes.length; i++) {
      const highDiff = highs[i] - highs[i - 1];
      const lowDiff = lows[i - 1] - lows[i];
      
      if (highDiff > lowDiff && highDiff > 0) plusDM += highDiff;
      if (lowDiff > highDiff && lowDiff > 0) minusDM += lowDiff;
    }
    
    const atr = Indicators.atr(highs, lows, closes, period);
    if (!atr || atr === 0) return null;
    
    const plusDI = (plusDM / atr) * 100;
    const minusDI = (minusDM / atr) * 100;
    
    const dx = (Math.abs(plusDI - minusDI) / (plusDI + minusDI)) * 100;
    
    return dx; // Simplified ADX (real ADX would need smoothing)
  },
  
  // Fibonacci Retracement
  fibonacci: (highs, lows) => {
    if (highs.length < 2 || lows.length < 2) return null;
    
    const high = Math.max(...highs);
    const low = Math.min(...lows);
    const diff = high - low;
    
    return {
      level0: high,
      level236: high - diff * 0.236,
      level382: high - diff * 0.382,
      level500: high - diff * 0.500,
      level618: high - diff * 0.618,
      level786: high - diff * 0.786,
      level100: low
    };
  },
  
  // VWAP (Volume Weighted Average Price)
  vwap: (highs, lows, closes, volumes) => {
    if (closes.length !== volumes.length) return null;
    
    let totalPV = 0;
    let totalV = 0;
    
    for (let i = 0; i < closes.length; i++) {
      const typicalPrice = (highs[i] + lows[i] + closes[i]) / 3;
      totalPV += typicalPrice * volumes[i];
      totalV += volumes[i];
    }
    
    return totalV > 0 ? totalPV / totalV : null;
  },
  
  // Supertrend
  supertrend: (highs, lows, closes, period = 10, multiplier = 3) => {
    if (closes.length < period) return null;
    
    const atr = Indicators.atr(highs, lows, closes, period);
    if (!atr) return null;
    
    // Simplified Supertrend calculation
    const upper = (highs[highs.length - 1] + lows[lows.length - 1]) / 2 + multiplier * atr;
    const lower = (highs[highs.length - 1] + lows[lows.length - 1]) / 2 - multiplier * atr;
    const currentClose = closes[closes.length - 1];
    
    let trend = 'bullish';
    if (currentClose < lower) {
      trend = 'bearish';
    }
    
    return {
      upper: parseFloat(upper.toFixed(2)),
      lower: parseFloat(lower.toFixed(2)),
      trend: trend
    };
  },
  
  // Williams %R
  williamsR: (highs, lows, closes, period = 14) => {
    if (closes.length < period) return null;
    
    const recentHighs = highs.slice(-period);
    const recentLows = lows.slice(-period);
    const currentClose = closes[closes.length - 1];
    
    const highest = Math.max(...recentHighs);
    const lowest = Math.min(...recentLows);
    
    if (highest === lowest) return -50;
    
    const wr = ((highest - currentClose) / (highest - lowest)) * -100;
    
    return wr;
  },
  
  // Pivot Points (Classic)
  pivotPoints: (highs, lows, closes) => {
    if (closes.length < 3) return null;
    
    const high = highs[highs.length - 1];
    const low = lows[lows.length - 1];
    const close = closes[closes.length - 1];
    
    const pp = (high + low + close) / 3;
    const r1 = 2 * pp - low;
    const s1 = 2 * pp - high;
    const r2 = pp + (high - low);
    const s2 = pp - (high - low);
    const r3 = high + 2 * (pp - low);
    const s3 = low - 2 * (high - pp);
    
    return {
      pp: parseFloat(pp.toFixed(2)),
      r1: parseFloat(r1.toFixed(2)),
      r2: parseFloat(r2.toFixed(2)),
      r3: parseFloat(r3.toFixed(2)),
      s1: parseFloat(s1.toFixed(2)),
      s2: parseFloat(s2.toFixed(2)),
      s3: parseFloat(s3.toFixed(2))
    };
  },
  
  // Ichimoku Cloud (simplified)
  ichimoku: (highs, lows, closes, conversionPeriod = 9, basePeriod = 26, spanBPeriod = 52, displacement = 26) => {
    if (closes.length < Math.max(spanBPeriod, basePeriod) + displacement) return null;
    
    // Tenkan-sen (Conversion Line)
    const recentHighsC = highs.slice(-conversionPeriod);
    const recentLowsC = lows.slice(-conversionPeriod);
    const tenkan = (Math.max(...recentHighsC) + Math.min(...recentLowsC)) / 2;
    
    // Kijun-sen (Base Line)
    const recentHighsB = highs.slice(-basePeriod);
    const recentLowsB = lows.slice(-basePeriod);
    const kijun = (Math.max(...recentHighsB) + Math.min(...recentLowsB)) / 2;
    
    // Senkou Span A (Leading Span A)
    const senkouA = (tenkan + kijun) / 2;
    
    // Senkou Span B (Leading Span B)
    const recentHighsS = highs.slice(-spanBPeriod);
    const recentLowsS = lows.slice(-spanBPeriod);
    const senkouB = (Math.max(...recentHighsS) + Math.min(...recentLowsS)) / 2;
    
    // Current price position relative to cloud
    const currentClose = closes[closes.length - 1];
    
    let cloudTrend = 'neutral';
    if (currentClose > senkouA && currentClose > senkouB) {
      cloudTrend = 'bullish';
    } else if (currentClose < senkouA && currentClose < senkouB) {
      cloudTrend = 'bearish';
    }
    
    return {
      tenkan: parseFloat(tenkan.toFixed(2)),
      kijun: parseFloat(kijun.toFixed(2)),
      senkouA: parseFloat(senkouA.toFixed(2)),
      senkouB: parseFloat(senkouB.toFixed(2)),
      cloudTrend: cloudTrend,
      priceAboveCloud: currentClose > Math.max(senkouA, senkouB)
    };
  },
  
  // MFI (Money Flow Index)
  mfi: (highs, lows, closes, volumes, period = 14) => {
    if (closes.length < period + 1) return null;
    
    let positiveFlow = 0;
    let negativeFlow = 0;
    
    for (let i = closes.length - period; i < closes.length; i++) {
      const typicalPrice = (highs[i] + lows[i] + closes[i]) / 3;
      const moneyFlow = typicalPrice * volumes[i];
      
      if (typicalPrice > closes[i - 1]) {
        positiveFlow += moneyFlow;
      } else if (typicalPrice < closes[i - 1]) {
        negativeFlow += moneyFlow;
      }
    }
    
    if (negativeFlow === 0) return 100;
    
    const moneyRatio = positiveFlow / negativeFlow;
    const mfi = 100 - (100 / (1 + moneyRatio));
    
    return mfi;
  },
  
  // CCI (Commodity Channel Index)
  cci: (highs, lows, closes, period = 20) => {
    if (closes.length < period) return null;
    
    const typicalPrices = highs.map((h, i) => (h + lows[i] + closes[i]) / 3);
    const recentTP = typicalPrices.slice(-period);
    const sma = recentTP.reduce((a, b) => a + b, 0) / period;
    
    let meanDeviation = 0;
    for (let i = 0; i < period; i++) {
      meanDeviation += Math.abs(recentTP[i] - sma);
    }
    meanDeviation /= period;
    
    if (meanDeviation === 0) return 0;
    
    const cci = (typicalPrices[typicalPrices.length - 1] - sma) / (0.015 * meanDeviation);
    
    return cci;
  },
  
  // Keltner Channel
  keltner: (highs, lows, closes, period = 20, multiplier = 2) => {
    if (closes.length < period) return null;
    
    const atr = Indicators.atr(highs, lows, closes, period);
    if (!atr) return null;
    
    const ema = Indicators.ema(closes, period);
    if (!ema) return null;
    
    return {
      middle: parseFloat(ema.toFixed(2)),
      upper: parseFloat((ema + multiplier * atr).toFixed(2)),
      lower: parseFloat((ema - multiplier * atr).toFixed(2))
    };
  },
  
  // Donchian Channel
  donchian: (highs, lows, period = 20) => {
    if (highs.length < period) return null;
    
    const recentHighs = highs.slice(-period);
    const recentLows = lows.slice(-period);
    
    return {
      upper: Math.max(...recentHighs),
      middle: (Math.max(...recentHighs) + Math.min(...recentLows)) / 2,
      lower: Math.min(...recentLows)
    };
  },
  
  // Support and Resistance (auto-detect)
  supportResistance: (highs, lows, closes, lookback = 50) => {
    if (closes.length < lookback) return null;
    
    const recentHighs = highs.slice(-lookback);
    const recentLows = lows.slice(-lookback);
    
    // Find local maxima and minima
    let resistanceLevels = [];
    let supportLevels = [];
    
    for (let i = 2; i < recentHighs.length - 2; i++) {
      // Resistance (local max)
      if (recentHighs[i] > recentHighs[i-1] && recentHighs[i] > recentHighs[i-2] &&
          recentHighs[i] > recentHighs[i+1] && recentHighs[i] > recentHighs[i+2]) {
        resistanceLevels.push(recentHighs[i]);
      }
      // Support (local min)
      if (recentLows[i] < recentLows[i-1] && recentLows[i] < recentLows[i-2] &&
          recentLows[i] < recentLows[i+1] && recentLows[i] < recentLows[i+2]) {
        supportLevels.push(recentLows[i]);
      }
    }
    
    // Cluster nearby levels
    const cluster = (levels, threshold = 0.02) => {
      if (levels.length === 0) return [];
      levels.sort((a, b) => a - b);
      const clusters = [[levels[0]]];
      for (let i = 1; i < levels.length; i++) {
        if (levels[i] - clusters[clusters.length-1][clusters[clusters.length-1].length-1] < threshold * levels[i]) {
          clusters[clusters.length-1].push(levels[i]);
        } else {
          clusters.push([levels[i]]);
        }
      }
      return clusters.map(c => c[Math.floor(c.length/2)]);
    };
    
    const clusteredResistance = cluster(resistanceLevels);
    const clusteredSupport = cluster(supportLevels);
    
    const currentPrice = closes[closes.length - 1];
    
    return {
      resistance: clusteredResistance.slice(-3).map(r => parseFloat(r.toFixed(2))),
      support: clusteredSupport.slice(-3).map(s => parseFloat(s.toFixed(2))),
      nearestResistance: clusteredResistance.length > 0 ? parseFloat(clusteredResistance[clusteredResistance.length-1].toFixed(2)) : null,
      nearestSupport: clusteredSupport.length > 0 ? parseFloat(clusteredSupport[0].toFixed(2)) : null,
      pricePosition: currentPrice > (clusteredResistance[clusteredResistance.length-1] || 0) ? 'near resistance' : 
                      currentPrice < (clusteredSupport[0] || 0) ? 'near support' : 'mid range'
    };
  }
};

// Pattern recognition
const Patterns = {
  // Detect Hammer (Bullish Pinbar)
  hammer: (candles) => {
    const c = candles[candles.length - 1];
    const body = Math.abs(c.close - c.open);
    const lowerWick = Math.min(c.open, c.close) - c.low;
    const upperWick = c.high - Math.max(c.open, c.close);
    
    if (lowerWick > body * 2 && upperWick < body && c.close > c.open) {
      return { type: 'hammer', direction: 'bullish' };
    }
    return null;
  },
  
  // Detect Shooting Star (Bearish Pinbar)
  shootingStar: (candles) => {
    const c = candles[candles.length - 1];
    const body = Math.abs(c.close - c.open);
    const upperWick = c.high - Math.max(c.open, c.close);
    const lowerWick = Math.min(c.open, c.close) - c.low;
    
    if (upperWick > body * 2 && lowerWick < body && c.close < c.open) {
      return { type: 'shooting_star', direction: 'bearish' };
    }
    return null;
  },
  
  // Detect Engulfing
  engulfing: (candles) => {
    if (candles.length < 2) return null;
    
    const current = candles[candles.length - 1];
    const previous = candles[candles.length - 2];
    
    // Bullish engulfing
    if (previous.close < previous.open && 
        current.close > current.open &&
        current.open < previous.close &&
        current.close > previous.open) {
      return { type: 'engulfing', direction: 'bullish' };
    }
    
    // Bearish engulfing
    if (previous.close > previous.open && 
        current.close < current.open &&
        current.open > previous.close &&
        current.close < previous.open) {
      return { type: 'engulfing', direction: 'bearish' };
    }
    
    return null;
  },
  
  // Detect Doji
  doji: (candles) => {
    const c = candles[candles.length - 1];
    const body = Math.abs(c.close - c.open);
    const range = c.high - c.low;
    
    if (body < range * 0.1 && range > 0) {
      return { type: 'doji', direction: 'neutral' };
    }
    return null;
  },
  
  // Detect Morning/Evening Star
  morningStar: (candles) => {
    if (candles.length < 3) return null;
    
    const c3 = candles[candles.length - 3];
    const c2 = candles[candles.length - 2];
    const c1 = candles[candles.length - 1];
    
    // Morning star: downtrend, big bearish, small body, big bullish
    const c3Bearish = c3.close < c3.open;
    const c2SmallBody = Math.abs(c2.close - c2.open) < Math.abs(c3.close - c3.open) * 0.3;
    const c1Bullish = c1.close > c1.open;
    const c1Engulfs = c1.close > c3.open && c1.open < c3.close;
    
    if (c3Bearish && c2SmallBody && c1Bullish && c1Engulfs) {
      return { type: 'morning_star', direction: 'bullish' };
    }
    
    return null;
  },
  
  // Detect all patterns
  detectAll: (candles) => {
    return [
      Patterns.hammer(candles),
      Patterns.shootingStar(candles),
      Patterns.engulfing(candles),
      Patterns.doji(candles),
      Patterns.morningStar(candles)
    ].filter(p => p !== null);
  },
  
  // Detect Double Top (M pattern)
  doubleTop: (candles, lookback = 20) => {
    if (candles.length < lookback) return null;
    
    const recent = candles.slice(-lookback);
    const highs = recent.map(c => c.high);
    const maxHigh = Math.max(...highs);
    const maxIndex = highs.indexOf(maxHigh);
    
    // Need two peaks roughly equal (within 2%)
    if (maxIndex < 5 || maxIndex > lookback - 5) return null;
    
    const firstPeak = recent[maxIndex].high;
    const secondPeakHigh = recent[recent.length - 1].high;
    
    // Check if forming second peak
    if (secondPeakHigh >= firstPeak * 0.98 && secondPeakHigh <= firstPeak * 1.02) {
      // Check neckline
      const minBetween = Math.min(...recent.slice(maxIndex + 1, -1).map(c => c.low));
      if (recent[recent.length - 1].low < minBetween) {
        return { type: 'double_top', direction: 'bearish', resistance: firstPeak, support: minBetween };
      }
    }
    return null;
  },
  
  // Detect Double Bottom (W pattern)
  doubleBottom: (candles, lookback = 20) => {
    if (candles.length < lookback) return null;
    
    const recent = candles.slice(-lookback);
    const lows = recent.map(c => c.low);
    const minLow = Math.min(...lows);
    const minIndex = lows.indexOf(minLow);
    
    if (minIndex < 5 || minIndex > lookback - 5) return null;
    
    const firstBottom = recent[minIndex].low;
    const secondBottomLow = recent[recent.length - 1].low;
    
    if (secondBottomLow >= firstBottom * 0.98 && secondBottomLow <= firstBottom * 1.02) {
      const maxBetween = Math.max(...recent.slice(minIndex + 1, -1).map(c => c.high));
      if (recent[recent.length - 1].high > maxBetween) {
        return { type: 'double_bottom', direction: 'bullish', support: firstBottom, resistance: maxBetween };
      }
    }
    return null;
  },
  
  // Detect Head and Shoulders
  headAndShoulders: (candles, lookback = 60) => {
    if (candles.length < lookback) return null;
    
    const recent = candles.slice(-lookback);
    const highs = recent.map(c => c.high);
    
    // Find three peaks
    let peaks = [];
    for (let i = 2; i < highs.length - 2; i++) {
      if (highs[i] > highs[i-1] && highs[i] > highs[i-2] && highs[i] > highs[i+1] && highs[i] > highs[i+2]) {
        peaks.push({ index: i, high: highs[i] });
      }
    }
    
    if (peaks.length < 3) return null;
    
    // Check for head and shoulders pattern
    const last3 = peaks.slice(-3);
    const leftShoulder = last3[0];
    const head = last3[1];
    const rightShoulder = last3[2];
    
    // Head should be highest, shoulders roughly equal
    if (head.high > leftShoulder.high && head.high > rightShoulder.high &&
        Math.abs(leftShoulder.high - rightShoulder.high) / leftShoulder.high < 0.03) {
      const neckline = Math.min(
        ...recent.slice(leftShoulder.index, head.index).map(c => c.low),
        ...recent.slice(head.index, rightShoulder.index).map(c => c.low)
      );
      return { type: 'head_shoulders', direction: 'bearish', head: head.high, neckline };
    }
    
    return null;
  },
  
  // Detect Inverse Head and Shoulders
  inverseHeadAndShoulders: (candles, lookback = 60) => {
    if (candles.length < lookback) return null;
    
    const recent = candles.slice(-lookback);
    const lows = recent.map(c => c.low);
    
    let bottoms = [];
    for (let i = 2; i < lows.length - 2; i++) {
      if (lows[i] < lows[i-1] && lows[i] < lows[i-2] && lows[i] < lows[i+1] && lows[i] < lows[i+2]) {
        bottoms.push({ index: i, low: lows[i] });
      }
    }
    
    if (bottoms.length < 3) return null;
    
    const last3 = bottoms.slice(-3);
    const leftShoulder = last3[0];
    const head = last3[1];
    const rightShoulder = last3[2];
    
    if (head.low < leftShoulder.low && head.low < rightShoulder.low &&
        Math.abs(leftShoulder.low - rightShoulder.low) / leftShoulder.low < 0.03) {
      const neckline = Math.max(
        ...recent.slice(leftShoulder.index, head.index).map(c => c.high),
        ...recent.slice(head.index, rightShoulder.index).map(c => c.high)
      );
      return { type: 'inverse_head_shoulders', direction: 'bullish', head: head.low, neckline };
    }
    
    return null;
  },
  
  // Detect Triangle (consolidating)
  triangle: (candles, lookback = 30) => {
    if (candles.length < lookback) return null;
    
    const recent = candles.slice(-lookback);
    const highs = recent.map(c => c.high);
    const lows = recent.map(c => c.low);
    
    // Linear regression for highs (resistance)
    const highSlope = (highs[highs.length-1] - highs[0]) / highs.length;
    const lowSlope = (lows[lows.length-1] - lows[0]) / lows.length;
    
    // Symmetrical triangle: converging lines
    if (Math.abs(highSlope) < Math.abs(lowSlope) * 1.5 && 
        Math.abs(lowSlope) < Math.abs(highSlope) * 1.5 &&
        (highSlope < 0 && lowSlope > 0)) {
      return { type: 'triangle', direction: 'neutral', pattern: 'symmetrical' };
    }
    
    // Ascending triangle: flat resistance, rising support
    if (Math.abs(highSlope) < Math.abs(lowSlope) * 0.3 && lowSlope > 0) {
      return { type: 'triangle', direction: 'bullish', pattern: 'ascending' };
    }
    
    // Descending triangle: falling resistance, flat support
    if (Math.abs(lowSlope) < Math.abs(highSlope) * 0.3 && highSlope < 0) {
      return { type: 'triangle', direction: 'bearish', pattern: 'descending' };
    }
    
    return null;
  },
  
  // Detect Flag (trend continuation)
  flag: (candles, lookback = 20) => {
    if (candles.length < lookback) return null;
    
    const recent = candles.slice(-lookback);
    
    // Calculate price change
    const startPrice = recent[0].close;
    const endPrice = recent[recent.length - 1].close;
    const change = (endPrice - startPrice) / startPrice;
    
    // Flag: small channel after strong move (>5%)
    if (Math.abs(change) > 0.05) {
      const highs = recent.map(c => c.high);
      const lows = recent.map(c => c.low);
      
      const highSlope = (highs[highs.length-1] - highs[0]) / highs.length;
      const lowSlope = (lows[lows.length-1] - lows[0]) / lows.length;
      
      // Small channel (both slopes similar direction, small magnitude)
      if (Math.abs(highSlope) < Math.abs(change) * 0.3 && 
          Math.abs(lowSlope) < Math.abs(change) * 0.3 &&
          ((change > 0 && highSlope > 0) || (change < 0 && highSlope < 0))) {
        return { 
          type: 'flag', 
          direction: change > 0 ? 'bullish' : 'bearish', 
          previousMove: change > 0 ? 'up' : 'down' 
        };
      }
    }
    
    return null;
  }
};

// Analyze single timeframe
async function analyzeTimeframe(symbol, timeframe, limit = 100) {
  try {
    const exchange = new ccxt.binance();
    const ohlcv = await exchange.fetchOHLCV(symbol, timeframe, undefined, limit);
    
    const closes = ohlcv.map(c => c[4]);
    const highs = ohlcv.map(c => c[2]);
    const lows = ohlcv.map(c => c[3]);
    const volumes = ohlcv.map(c => c[5]);
    
    const candles = ohlcv.map(c => ({
      open: c[1],
      high: c[2],
      low: c[3],
      close: c[4],
      volume: c[5]
    }));
    
    const rsi = Indicators.rsi(closes, 14);
    const sma20 = Indicators.sma(closes, 20);
    const sma50 = Indicators.sma(closes, 50);
    const ema9 = Indicators.ema(closes, 9);
    const ema21 = Indicators.ema(closes, 21);
    const bollinger = Indicators.bollinger(closes, 20, 2);
    const macd = Indicators.macd(closes);
    const atr = Indicators.atr(highs, lows, closes, 14);
    
    // Volume indicators
    const obv = Indicators.obv(closes, volumes);
    const volumeSma = Indicators.volumeSma(volumes, 20);
    const stochastic = Indicators.stochastic(highs, lows, closes, 14);
    const adx = Indicators.adx(highs, lows, closes, 14);
    const fibonacci = Indicators.fibonacci(highs, lows);
    const vwap = Indicators.vwap(highs, lows, closes, volumes);
    const supertrend = Indicators.supertrend(highs, lows, closes);
    const williamsR = Indicators.williamsR(highs, lows, closes);
    const pivotPoints = Indicators.pivotPoints(highs, lows, closes);
    const ichimoku = Indicators.ichimoku(highs, lows, closes);
    const mfi = Indicators.mfi(highs, lows, closes, volumes);
    const cci = Indicators.cci(highs, lows, closes);
    const keltner = Indicators.keltner(highs, lows, closes);
    const donchian = Indicators.donchian(highs, lows);
    const supportResistance = Indicators.supportResistance(highs, lows, closes);
    
    // Volume analysis
    const avgVolume = Indicators.volumeSma(volumes, 20);
    const currentVolume = volumes[volumes.length - 1];
    const volumeRatio = avgVolume ? (currentVolume / avgVolume) : 1;
    
    // Volume trend (last 5 candles)
    const recentVolumes = volumes.slice(-5);
    const volumeIncreasing = recentVolumes[4] > recentVolumes[0];
    
    // Price vs Volume divergence
    const priceChange = (closes[closes.length - 1] - closes[closes.length - 5]) / closes[closes.length - 5];
    let volumeAnalysis = 'normal';
    if (priceChange > 0 && volumeIncreasing) {
      volumeAnalysis = '健康上涨 (量价配合)';
    } else if (priceChange > 0 && !volumeIncreasing) {
      volumeAnalysis = '量价背离 (可能回落)';
    } else if (priceChange < 0 && volumeIncreasing) {
      volumeAnalysis = '恐慌抛售 (可能反转)';
    } else if (priceChange < 0 && !volumeIncreasing) {
      volumeAnalysis = '观望 (无量下跌)';
    }
    
    // Detect all patterns including classic patterns
    const patterns = [
      ...Patterns.detectAll(candles),
      Patterns.doubleTop(candles),
      Patterns.doubleBottom(candles),
      Patterns.headAndShoulders(candles),
      Patterns.inverseHeadAndShoulders(candles),
      Patterns.triangle(candles),
      Patterns.flag(candles)
    ].filter(p => p !== null);
    
    // Determine trend
    let trend = 'neutral';
    if (ema9 > ema21 && sma20 > sma50) {
      trend = 'bullish';
    } else if (ema9 < ema21 && sma20 < sma50) {
      trend = 'bearish';
    }
    
    const currentPrice = closes[closes.length - 1];
    
    return {
      timeframe,
      price: currentPrice,
      trend,
      rsi: rsi ? parseFloat(rsi.toFixed(2)) : null,
      ema9: ema9 ? parseFloat(ema9.toFixed(2)) : null,
      ema21: ema21 ? parseFloat(ema21.toFixed(2)) : null,
      sma20: sma20 ? parseFloat(sma20.toFixed(2)) : null,
      sma50: sma50 ? parseFloat(sma50.toFixed(2)) : null,
      bollinger: bollinger ? {
        upper: parseFloat(bollinger.upper.toFixed(2)),
        middle: parseFloat(bollinger.middle.toFixed(2)),
        lower: parseFloat(bollinger.lower.toFixed(2))
      } : null,
      macd: macd ? {
        line: parseFloat(macd.macd.toFixed(2)),
        signal: parseFloat(macd.signal.toFixed(2)),
        histogram: parseFloat(macd.histogram.toFixed(2)),
        goldenCross: macd.macd > macd.signal
      } : null,
      atr: atr ? parseFloat(atr.toFixed(2)) : null,
      atrPercent: atr ? parseFloat(((atr / currentPrice) * 100).toFixed(2)) : null,
      // Volume analysis
      volume: {
        obv: obv ? parseFloat(obv.toFixed(2)) : null,
        sma20: volumeSma ? parseFloat(volumeSma.toFixed(2)) : null,
        current: currentVolume,
        ratio: volumeRatio ? parseFloat(volumeRatio.toFixed(2)) : null,
        trend: volumeIncreasing ? 'increasing' : 'decreasing',
        analysis: volumeAnalysis
      },
      // Additional indicators
      stochastic: stochastic ? parseFloat(stochastic.toFixed(2)) : null,
      adx: adx ? parseFloat(adx.toFixed(2)) : null,
      // New indicators
      fibonacci: fibonacci ? {
        level236: parseFloat(fibonacci.level236.toFixed(2)),
        level382: parseFloat(fibonacci.level382.toFixed(2)),
        level500: parseFloat(fibonacci.level500.toFixed(2)),
        level618: parseFloat(fibonacci.level618.toFixed(2)),
        level786: parseFloat(fibonacci.level786.toFixed(2)),
      } : null,
      vwap: vwap ? parseFloat(vwap.toFixed(2)) : null,
      supertrend: supertrend ? {
        upper: supertrend.upper,
        lower: supertrend.lower,
        trend: supertrend.trend
      } : null,
      williamsR: williamsR ? parseFloat(williamsR.toFixed(2)) : null,
      pivotPoints: pivotPoints ? pivotPoints : null,
      // New indicators
      ichimoku: ichimoku ? {
        tenkan: ichimoku.tenkan,
        kijun: ichimoku.kijun,
        senkouA: ichimoku.senkouA,
        senkouB: ichimoku.senkouB,
        cloudTrend: ichimoku.cloudTrend,
        priceAboveCloud: ichimoku.priceAboveCloud
      } : null,
      mfi: mfi ? parseFloat(mfi.toFixed(2)) : null,
      cci: cci ? parseFloat(cci.toFixed(2)) : null,
      keltner: keltner ? {
        middle: keltner.middle,
        upper: keltner.upper,
        lower: keltner.lower
      } : null,
      donchian: donchian ? {
        upper: donchian.upper,
        middle: parseFloat(donchian.middle.toFixed(2)),
        lower: donchian.lower
      } : null,
      supportResistance: supportResistance ? {
        resistance: supportResistance.resistance,
        support: supportResistance.support,
        nearestResistance: supportResistance.nearestResistance,
        nearestSupport: supportResistance.nearestSupport,
        pricePosition: supportResistance.pricePosition
      } : null,
      // Current price vs key levels
      keyLevels: {
        vsFib618: currentPrice > fibonacci?.level618 ? 'above' : 'below',
        vsVWAP: currentPrice > vwap ? 'above' : 'below',
        vsPivotPP: currentPrice > pivotPoints?.pp ? 'above' : 'below',
      },
      patterns: patterns.length > 0 ? patterns : null,
      signals: {
        rsiOverbought: rsi > 70,
        rsiOversold: rsi < 30,
        priceAboveUpperBollinger: bollinger && currentPrice > bollinger.upper,
        priceBelowLowerBollinger: bollinger && currentPrice < bollinger.lower,
        stochasticOverbought: stochastic > 80,
        stochasticOversold: stochastic < 20,
        williamsROverbought: williamsR > -20,
        williamsROversold: williamsR < -80,
        supertrendBullish: supertrend?.trend === 'bullish',
        supertrendBearish: supertrend?.trend === 'bearish',
        // New signals
        mfiOverbought: mfi > 80,
        mfiOversold: mfi < 20,
        cciOverbought: cci > 100,
        cciOversold: cci < -100,
        ichimokuBullish: ichimoku?.cloudTrend === 'bullish',
        ichimokuBearish: ichimoku?.cloudTrend === 'bearish',
      }
    };
  } catch (error) {
    return { error: error.message, timeframe };
  }
}

// Multi-timeframe analysis
async function analyze(symbol, timeframes = ['15m', '1h', '4h', '1d'], limit = 100) {
  try {
    // Fetch all timeframes in parallel
    const results = await Promise.all(
      timeframes.map(tf => analyzeTimeframe(symbol, tf, limit))
    );
    
    // Create analysis object
    const analysis = {
      symbol,
      timestamp: new Date().toISOString(),
      timeframes: {}
    };
    
    // Store each timeframe result
    results.forEach(result => {
      if (!result.error) {
        analysis.timeframes[result.timeframe] = result;
      }
    });
    
    // Generate multi-timeframe signal
    const timeframeResults = Object.values(analysis.timeframes);
    
    if (timeframeResults.length === 0) {
      return { error: 'Failed to fetch data from all timeframes' };
    }
    
    // Count trends
    const trends = timeframeResults.map(t => t.trend);
    const bullishCount = trends.filter(t => t === 'bullish').length;
    const bearishCount = trends.filter(t => t === 'bearish').length;
    const neutralCount = trends.filter(t => t === 'neutral').length;
    
    // Multi-timeframe trend
    let overallTrend = 'neutral';
    if (bullishCount > bearishCount && bullishCount >= 2) {
      overallTrend = 'bullish';
    } else if (bearishCount > bullishCount && bearishCount >= 2) {
      overallTrend = 'bearish';
    }
    
    // Count RSI signals
    const rsiOverbought = timeframeResults.filter(t => t.signals && t.signals.rsiOverbought).length;
    const rsiOversold = timeframeResults.filter(t => t.signals && t.signals.rsiOversold).length;
    
    // Collect all patterns
    const allPatterns = timeframeResults
      .filter(t => t.patterns)
      .flatMap(t => t.patterns);
    
    const bullishPatterns = allPatterns.filter(p => p.direction === 'bullish');
    const bearishPatterns = allPatterns.filter(p => p.direction === 'bearish');
    
    // Get current price from 1h timeframe
    const h1Data = analysis.timeframes['1h'];
    const currentPrice = h1Data ? h1Data.price : timeframeResults[0].price;
    const atr = h1Data ? h1Data.atr : null;
    
    // Generate recommendation
    let recommendation = 'NEUTRAL';
    let reasons = [];
    
    // Trend-based signals
    if (overallTrend === 'bullish') {
      reasons.push('多周期趋势向上');
    } else if (overallTrend === 'bearish') {
      reasons.push('多周期趋势向下');
    }
    
    // Pattern signals
    if (bullishPatterns.length >= 2) {
      reasons.push(`出现${bullishPatterns.length}个看涨形态`);
    }
    if (bearishPatterns.length >= 2) {
      reasons.push(`出现${bearishPatterns.length}个看跌形态`);
    }
    
    // RSI signals
    if (rsiOversold >= 2) {
      reasons.push('多个周期RSI超卖');
      recommendation = 'BUY';
    } else if (rsiOverbought >= 2) {
      reasons.push('多个周期RSI超买');
      recommendation = 'SELL';
    }
    
    // Override based on patterns
    if (recommendation === 'NEUTRAL') {
      if (bullishPatterns.length > bearishPatterns.length) {
        recommendation = 'BUY';
      } else if (bearishPatterns.length > bullishPatterns.length) {
        recommendation = 'SELL';
      }
    }
    
    // Final recommendation
    if (recommendation === 'NEUTRAL') {
      if (overallTrend === 'bullish') {
        recommendation = 'BUY';
      } else if (overallTrend === 'bearish') {
        recommendation = 'SELL';
      }
    }
    
    analysis.summary = {
      overallTrend,
      trendBreakdown: {
        bullish: bullishCount,
        bearish: bearishCount,
        neutral: neutralCount
      },
      patterns: {
        bullish: bullishPatterns.length,
        bearish: bearishPatterns.length
      },
      rsiSignals: {
        overbought: rsiOverbought,
        oversold: rsiOversold
      }
    };
    
    analysis.recommendation = {
      action: recommendation,
      reason: reasons.length > 0 ? reasons.join(', ') : '等待更多信号',
      currentPrice: currentPrice,
      // For BUY: stopLoss below entry, takeProfit above entry
      // For SELL: stopLoss above entry, takeProfit below entry
      stopLoss: atr ? parseFloat((
        recommendation === 'BUY' 
          ? currentPrice - atr * 2 
          : currentPrice + atr * 2
      ).toFixed(2)) : null,
      takeProfit: atr ? parseFloat((
        recommendation === 'BUY' 
          ? currentPrice + atr * 3 
          : currentPrice - atr * 3
      ).toFixed(2)) : null
    };
    
    return analysis;
    
  } catch (error) {
    return { error: error.message };
  }
}

// Export functions
module.exports = {
  analyze,
  analyzeTimeframe,
  Indicators,
  Patterns
};
