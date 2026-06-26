#!/usr/bin/env node

/**
 * 选股器脚本
 * 根据右侧交易策略筛选股票
 */

import { execSync } from 'child_process';
import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const QVERIS_CLI = 'node ~/.openclaw/skills/qveris-official/scripts/qveris_tool.mjs';

// Discovery IDs
const DISCOVERY_IDS = {
  real_time: '81d10584-cf1b-4229-afa2-54b9c84b7342',
  history: '777b4129-5038-4448-9f06-5fe40e4bcb00'
};

/**
 * 调用 QVeris CLI
 */
function callQveris(command, params) {
  try {
    const cmd = `${QVERIS_CLI} ${command} --params '${JSON.stringify(params)}'`;
    const output = execSync(cmd, { encoding: 'utf8', timeout: 30000 });
    const result = JSON.parse(output);
    
    if (result.status_code === 200) {
      return result.data;
    }
    return null;
  } catch (error) {
    console.error(`QVeris API error: ${error.message}`);
    return null;
  }
}

/**
 * 获取实时行情
 */
function getRealTimeQuotes(codes) {
  return callQveris(
    `call ths_ifind.real_time_quotation.v1 --discovery-id ${DISCOVERY_IDS.real_time}`,
    { codes: codes }
  );
}

/**
 * 获取历史行情（用于计算均线和 MACD）
 */
function getHistoryQuotes(code, startDate, endDate) {
  return callQveris(
    `call fast_fin.history_quotation.v1 --discovery-id ${DISCOVERY_IDS.history}`,
    { codes: code, startdate: startDate, enddate: endDate, interval: 'day' }
  );
}

/**
 * 计算均线
 */
function calculateMA(prices, period) {
  if (prices.length < period) return null;
  const slice = prices.slice(-period);
  return slice.reduce((a, b) => a + b, 0) / period;
}

/**
 * 计算 MACD
 */
function calculateMACD(prices) {
  if (prices.length < 26) return null;
  
  // 简化版 MACD 计算
  const ema12 = calculateEMA(prices, 12);
  const ema26 = calculateEMA(prices, 26);
  const dif = ema12 - ema26;
  
  // 简化处理，实际需要更复杂的计算
  return {
    dif: dif,
    dea: dif * 0.8, // 简化
    macd: (dif - dif * 0.8) * 2
  };
}

function calculateEMA(prices, period) {
  const k = 2 / (period + 1);
  let ema = prices[0];
  for (let i = 1; i < prices.length; i++) {
    ema = prices[i] * k + ema * (1 - k);
  }
  return ema;
}

/**
 * 评分系统
 */
function scoreStock(stock) {
  let score = 0;
  const reasons = [];
  
  const quote = stock.quote;
  const ma = stock.ma;
  const macd = stock.macd;
  
  // 趋势向上（25 分）
  if (ma && ma.ma5 > ma.ma10 && ma.ma10 > ma.ma20 && ma.ma20 > ma.ma60) {
    score += 25;
    reasons.push('均线多头排列');
  }
  
  if (quote.latest > ma?.ma60 * 1.1) {
    score += 5;
    reasons.push('股价在 60 日线上方');
  }
  
  // 温和放量（20 分）
  const volumeRatio = quote.vol_ratio;
  if (volumeRatio > 1.2 && volumeRatio < 2.5) {
    score += 20;
    reasons.push('温和放量');
  } else if (volumeRatio > 1.0 && volumeRatio <= 1.2) {
    score += 10;
    reasons.push('量能温和');
  }
  
  // MACD 金叉（15 分）
  if (macd && macd.dif > macd.dea && macd.macd > 0) {
    score += 15;
    reasons.push('MACD 金叉');
  }
  
  // 板块共振（5 分）- 简化处理
  if (quote.changeRatio > 0) {
    score += 5;
    reasons.push('今日上涨');
  }
  
  // 业绩增长（10 分）- 需要额外 API
  // 暂时跳过
  
  // 市值适中（5 分）
  const marketCap = quote.mv;
  if (marketCap && marketCap > 50e8 && marketCap < 500e8) {
    score += 5;
    reasons.push('市值适中');
  }
  
  // 非 ST、非科创板
  if (!stock.code.startsWith('688')) {
    score += 5;
    reasons.push('非科创板');
  }
  
  return {
    score: score,
    reasons: reasons,
    rating: score >= 80 ? '⭐⭐⭐⭐⭐' :
            score >= 70 ? '⭐⭐⭐⭐' :
            score >= 60 ? '⭐⭐⭐' : '观望'
  };
}

/**
 * 筛选股票
 */
function screenStocks(stockPool) {
  const results = [];
  
  // 获取实时行情
  const codes = stockPool.map(s => s.code).join(',');
  const quotesData = getRealTimeQuotes(codes);
  
  if (!quotesData) {
    console.log('❌ 获取行情失败');
    return [];
  }
  
  // 处理每只股票
  for (let i = 0; i < quotesData.length; i++) {
    const quoteList = quotesData[i];
    if (!quoteList || !quoteList[0]) continue;
    
    const quote = quoteList[0];
    const code = quote.thscode;
    const stockInfo = stockPool.find(s => s.code === code);
    
    // 基础筛选
    // 排除 ST
    if (stockInfo?.is_st) continue;
    
    // 排除科创板
    if (code.startsWith('688')) continue;
    
    // 排除停牌
    if (quote.tradeStatus !== '交易') continue;
    
    // 获取历史数据（用于计算均线和 MACD）
    const endDate = new Date().toISOString().split('T')[0].replace(/-/g, '');
    const startDate = new Date(Date.now() - 90 * 24 * 60 * 60 * 1000).toISOString().split('T')[0].replace(/-/g, '');
    
    const historyData = getHistoryQuotes(code, startDate, endDate);
    
    // 计算技术指标
    let ma = null;
    let macd = null;
    
    if (historyData && historyData[0]) {
      const closes = historyData[0].map(d => d.close).filter(c => c !== null);
      
      if (closes.length >= 60) {
        ma = {
          ma5: calculateMA(closes, 5),
          ma10: calculateMA(closes, 10),
          ma20: calculateMA(closes, 20),
          ma60: calculateMA(closes, 60)
        };
        
        macd = calculateMACD(closes);
      }
    }
    
    // 评分
    const stockData = {
      code: code,
      name: quote.ths_corp_cn_name_stock || stockInfo?.name || '未知',
      quote: quote,
      ma: ma,
      macd: macd
    };
    
    const evaluation = scoreStock(stockData);
    
    if (evaluation.score >= 60) {
      results.push({
        ...stockData,
        evaluation: evaluation
      });
    }
  }
  
  // 按评分排序
  results.sort((a, b) => b.evaluation.score - a.evaluation.score);
  
  return results;
}

/**
 * 主函数
 */
function main() {
  console.log('🔍 Stock Master Pro - 趋势选股器\n');
  console.log('策略：右侧交易 + 温和放量 + 趋势向上\n');
  
  // 检查依赖
  try {
    const checkDepCmd = `node ${join(__dirname, 'check_dependency.mjs')}`;
    execSync(checkDepCmd, { encoding: 'utf8', stdio: 'pipe' });
  } catch (error) {
    console.log('❌ 依赖检查失败，请先安装 QVeris AI 技能');
    process.exit(1);
  }
  
  // 示例股票池（实际应该从全市场筛选）
  const stockPool = [
    { code: '603259.SH', name: '药明康德' },
    { code: '002466.SZ', name: '天齐锂业' },
    { code: '600585.SH', name: '海螺水泥' },
    { code: '601398.SH', name: '工商银行' },
    { code: '000776.SZ', name: '广发证券' },
    { code: '600519.SH', name: '贵州茅台' },
    { code: '000858.SZ', name: '五粮液' },
    { code: '601318.SH', name: '中国平安' },
    { code: '600036.SH', name: '招商银行' },
    { code: '300750.SZ', name: '宁德时代' }
  ];
  
  console.log(`📊 筛选 ${stockPool.length} 只股票...\n`);
  
  const results = screenStocks(stockPool);
  
  if (results.length === 0) {
    console.log('❌ 未找到符合条件的股票');
    return;
  }
  
  console.log('='.repeat(80));
  console.log('📈 选股结果（按评分排序）');
  console.log('='.repeat(80));
  console.log('');
  
  // 显示 Top 10
  const topStocks = results.slice(0, 10);
  
  for (let i = 0; i < topStocks.length; i++) {
    const stock = topStocks[i];
    const quote = stock.quote;
    const evalData = stock.evaluation;
    
    console.log(`${i + 1}. ${stock.name} (${stock.code}) ${evalData.rating}`);
    console.log(`   评分：${evalData.score}/100`);
    console.log(`   现价：${quote.latest} 元  (${quote.changeRatio >= 0 ? '+' : ''}${quote.changeRatio.toFixed(2)}%)`);
    console.log(`   量比：${quote.vol_ratio.toFixed(2)}  换手：${quote.turnoverRatio?.toFixed(2) || 'N/A'}%`);
    console.log(`   市值：${(quote.mv / 1e8).toFixed(1)}亿`);
    console.log(`   亮点：${evalData.reasons.join('、')}`);
    console.log('');
  }
  
  console.log('='.repeat(80));
  console.log('⚠️  免责声明：以上分析仅供参考，不构成投资建议。股市有风险，投资需谨慎。');
  console.log('='.repeat(80));
}

main();
