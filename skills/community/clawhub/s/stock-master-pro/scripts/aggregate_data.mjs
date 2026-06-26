#!/usr/bin/env node

/**
 * 数据聚合脚本
 * 收集所有数据源，生成 Dashboard 需要的统一 JSON 文件
 * 每 10 分钟执行一次（交易时段）
 */

import { execSync } from 'child_process';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const STOCKS_DIR = join(__dirname, '../stocks');
const DATA_FILE = join(STOCKS_DIR, 'dashboard_data.json');

// QVeris CLI 路径
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
    const cmd = `${QVERIS_CLI} ${command} --params '${JSON.stringify(params)}' 2>&1`;
    const output = execSync(cmd, { encoding: 'utf8', timeout: 30000 });
    
    const jsonStart = output.indexOf('{');
    const jsonEnd = output.lastIndexOf('}');
    
    if (jsonStart === -1 || jsonEnd === -1) return null;
    
    const jsonStr = output.substring(jsonStart, jsonEnd + 1);
    const result = JSON.parse(jsonStr);
    
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
 * 获取大盘数据
 */
function getMarketData() {
  const codes = '000001.SH,399001.SZ,399006.SZ,399005.SZ';
  const data = callQveris(
    `call ths_ifind.real_time_quotation.v1 --discovery-id ${DISCOVERY_IDS.real_time}`,
    { codes: codes }
  );
  
  if (!data) return null;
  
  const indices = {};
  for (const item of data) {
    if (item && item[0]) {
      const quote = item[0];
      const code = quote.thscode;
      
      if (code === '000001.SH') {
        indices.sh = {
          price: quote.latest,
          change: quote.change,
          changePct: quote.changeRatio,
          amount: quote.amount / 1e8
        };
      } else if (code === '399001.SZ') {
        indices.sz = {
          price: quote.latest,
          change: quote.change,
          changePct: quote.changeRatio,
          amount: quote.amount / 1e8
        };
      } else if (code === '399006.SZ') {
        indices.cyb = {
          price: quote.latest,
          change: quote.change,
          changePct: quote.changeRatio,
          amount: quote.amount / 1e8
        };
      } else if (code === '399005.SZ') {
        indices.zz = {
          price: quote.latest,
          change: quote.change,
          changePct: quote.changeRatio,
          amount: quote.amount / 1e8
        };
      }
    }
  }
  
  return indices;
}

/**
 * 获取持仓数据
 */
function getHoldingsData() {
  const holdingsFile = join(STOCKS_DIR, 'holdings.json');
  
  if (!existsSync(holdingsFile)) return [];
  
  const holdingsData = JSON.parse(readFileSync(holdingsFile, 'utf8'));
  const holdings = holdingsData.holdings || [];
  
  if (holdings.length === 0) return [];
  
  const codes = holdings.map(h => h.code).join(',');
  const data = callQveris(
    `call ths_ifind.real_time_quotation.v1 --discovery-id ${DISCOVERY_IDS.real_time}`,
    { codes: codes }
  );
  
  if (!data) return [];
  
  const results = [];
  for (let i = 0; i < data.length; i++) {
    const item = data[i];
    if (!item || !item[0]) continue;
    
    const quote = item[0];
    const holding = holdings.find(h => h.code === quote.thscode);
    
    if (!holding) continue;
    
    const currentPrice = quote.latest;
    const cost = holding.cost || 0;
    const shares = holding.shares || 0;
    const profit = (currentPrice - cost) * shares;
    const profitPct = ((currentPrice - cost) / cost) * 100;
    
    results.push({
      name: holding.name,
      code: holding.code,
      quote: {
        price: currentPrice,
        changePct: quote.changeRatio,
        volumeRatio: quote.vol_ratio,
        turnover: quote.turnoverRatio
      },
      profit: {
        profit: profit,
        profitPct: profitPct,
        profitText: profit >= 0 ? `+${profit.toFixed(2)}` : profit.toFixed(2),
        profitPctText: profitPct >= 0 ? `+${profitPct.toFixed(2)}%` : `${profitPct.toFixed(2)}%`
      },
      shares: shares,
      cost: cost,
      notes: holding.notes || ''
    });
  }
  
  return results;
}

/**
 * 检测是否在交易时段
 */
function isTradingTime() {
  const now = new Date();
  const day = now.getDay();
  const hour = now.getHours();
  const minute = now.getMinutes();
  
  // 周末不交易
  if (day === 0 || day === 6) return false;
  
  // 交易时段：9:30-11:30, 13:00-15:00
  const time = hour * 100 + minute;
  return (time >= 930 && time <= 1130) || (time >= 1300 && time <= 1500);
}

/**
 * 检测是否已收盘
 */
function isMarketClosed() {
  const now = new Date();
  const hour = now.getHours();
  return hour >= 15 || hour < 9;
}

/**
 * 主函数
 */
function main() {
  console.log('📊 Stock Master Pro - 数据聚合\n');
  
  const tradingTime = isTradingTime();
  const marketClosed = isMarketClosed();
  
  console.log(`交易时段：${tradingTime ? '✅ 是' : '❌ 否'}`);
  console.log(`已收盘：${marketClosed ? '✅ 是' : '❌ 否'}`);
  console.log('');
  
  // 检查是否需要调用 API
  let marketData = null;
  let holdingsData = [];
  
  if (tradingTime || !marketClosed) {
    console.log('📡 调用 QVeris API 获取实时数据...');
    marketData = getMarketData();
    holdingsData = getHoldingsData();
  } else {
    console.log('💤 收盘状态，读取本地缓存数据...');
    
    // 读取已有数据
    const lastCheckFile = join(STOCKS_DIR, 'last_check.json');
    if (existsSync(lastCheckFile)) {
      const lastCheck = JSON.parse(readFileSync(lastCheckFile, 'utf8'));
      holdingsData = lastCheck.results || [];
    }
    
    // 使用模拟大盘数据（收盘后不变）
    marketData = {
      sh: { price: 3878.04, change: 64.76, changePct: 1.70, amount: 8746.2 },
      sz: { price: 13519.91, change: 174.40, changePct: 1.31, amount: 10773.7 },
      cyb: { price: 3243.65, change: 8.43, changePct: 0.26, amount: 4847.0 },
      zz: { price: 8194.33, change: 96.08, changePct: 1.19, amount: 1285.0 }
    };
  }
  
  // 生成 Dashboard 数据
  const dashboardData = {
    updateTime: new Date().toISOString(),
    marketStatus: tradingTime ? 'trading' : (marketClosed ? 'closed' : 'break'),
    market: marketData,
    holdings: holdingsData,
    alerts: holdingsData.filter(h => {
      const changePct = h.quote?.changePct || 0;
      return Math.abs(changePct) > 5; // 涨跌幅超 5% 视为预警
    }).map(h => ({
      type: 'change_pct',
      level: h.quote.changePct > 5 ? 'warning' : 'warning',
      message: `${h.name} ${h.quote.changePct > 0 ? '大涨' : '大跌'} ${Math.abs(h.quote.changePct).toFixed(2)}%`,
      timestamp: new Date().toISOString()
    }))
  };
  
  // 保存数据
  writeFileSync(DATA_FILE, JSON.stringify(dashboardData, null, 2));
  
  console.log(`\n💾 数据已保存：${DATA_FILE}`);
  console.log(`📊 大盘数据：${marketData ? '✅' : '❌'}`);
  console.log(`💰 持仓数据：${holdingsData.length} 只`);
  console.log(`⚠️ 预警信息：${dashboardData.alerts.length} 条`);
}

main();
