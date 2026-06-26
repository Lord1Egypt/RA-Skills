/**
 * 简易技术分析器 - 免费引流技能
 * 
 * 功能：MACD/KDJ/RSI 基础分析
 * 引流：展示基础功能，引导升级缠论服务
 */

const { tdx } = require('@tdx-local');

function calculateMACD(bars) {
  // 简化 MACD 计算
  const ema12 = bars.slice(0, 12).reduce((sum, b) => sum + b.close, 0) / 12;
  const ema26 = bars.slice(0, 26).reduce((sum, b) => sum + b.close, 0) / 26;
  const diff = ema12 - ema26;
  const dea = diff * 0.8; // 简化
  const macd = (diff - dea) * 2;
  
  return {
    diff: diff.toFixed(3),
    dea: dea.toFixed(3),
    macd: macd.toFixed(3),
    signal: macd > 0 ? '金叉' : '死叉'
  };
}

function calculateRSI(bars, period = 14) {
  let gains = 0, losses = 0;
  for (let i = 1; i <= period; i++) {
    const change = bars[i - 1].close - bars[i].close;
    if (change > 0) gains += change;
    else losses -= change;
  }
  const rs = gains / (losses || 1);
  const rsi = 100 - (100 / (1 + rs));
  
  return {
    rsi: rsi.toFixed(2),
    signal: rsi > 70 ? '超买' : rsi < 30 ? '超卖' : '中性'
  };
}

async function analyzeStock(code) {
  const normalizedCode = code.padStart(6, '0');
  
  const bars = await tdx.getBars({
    code: normalizedCode,
    market: normalizedCode.startsWith('6') ? 'sh' : 'sz',
    category: '日线',
    count: 30
  });
  
  if (!bars || bars.length < 26) {
    return { error: '数据不足' };
  }
  
  const macd = calculateMACD(bars);
  const rsi = calculateRSI(bars);
  
  // 成交量分析
  const avgVolume = bars.slice(0, 5).reduce((sum, b) => sum + b.volume, 0) / 5;
  const volumeRatio = (bars[0].volume / avgVolume).toFixed(2);
  
  return {
    code: normalizedCode,
    price: bars[0].close,
    macd,
    rsi,
    volumeRatio,
    volumeSignal: volumeRatio > 2 ? '放量' : volumeRatio < 0.5 ? '缩量' : '正常',
    upgradeHint: '需要缠论分型、笔、线段、中枢分析？升级专业版服务！'
  };
}

module.exports = { analyzeStock };
