#!/usr/bin/env node

/**
 * 龙虎榜分析脚本
 * 分析持仓股的龙虎榜数据，追踪机构/游资动向
 */

import { execSync } from 'child_process';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const STOCKS_DIR = join(__dirname, '../stocks');
const HOLDINGS_FILE = join(STOCKS_DIR, 'holdings.json');
const DRAGON_TIGER_FILE = join(STOCKS_DIR, 'dragon_tiger.json');

// QVeris CLI 路径
const QVERIS_CLI = 'node ~/.openclaw/skills/qveris-official/scripts/qveris_tool.mjs';

// Discovery IDs
const DISCOVERY_IDS = {
  dragon_tiger: '7e6c7f26-9201-42ed-8ef0-21e526dfcef2'
};

/**
 * 调用 QVeris CLI
 */
function callQveris(command, params) {
  try {
    const cmd = `${QVERIS_CLI} ${command} --params '${JSON.stringify(params)}' 2>&1`;
    const output = execSync(cmd, { encoding: 'utf8', timeout: 30000 });
    
    // 提取 JSON 部分
    const jsonStart = output.indexOf('{');
    const jsonEnd = output.lastIndexOf('}');
    
    if (jsonStart === -1 || jsonEnd === -1) {
      return null;
    }
    
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
 * 获取龙虎榜数据
 */
function getDragonTigerData(code, date) {
  const data = callQveris(
    `call ths_ifind.dragon_tiger.v1 --discovery-id ${DISCOVERY_IDS.dragon_tiger}`,
    { mode: 'detail', codes: code, edate: date }
  );
  
  return data;
}

/**
 * 格式化日期
 */
function formatDate(date) {
  return date.toISOString().split('T')[0].replace(/-/g, '');
}

/**
 * 分析席位类型
 */
function analyzeSeatType(seatName) {
  const name = seatName.toLowerCase();
  
  // 机构席位
  if (name.includes('机构') || name.includes('institutional')) {
    return { type: 'institution', label: '机构' };
  }
  
  // 游资席位（知名营业部）
  const hotMoneySeats = [
    '中信证券上海分公司', '国泰君安上海江苏路', '华泰证券上海武定路',
    '中信证券杭州延安路', '中国银河绍兴', '华泰证券深圳益田路',
    '光大证券杭州庆春路', '海通证券深圳分公司华富路'
  ];
  
  for (const seat of hotMoneySeats) {
    if (name.includes(seat.toLowerCase())) {
      return { type: 'hot_money', label: '游资' };
    }
  }
  
  // 沪深股通（北向资金）
  if (name.includes('沪深股通') || name.includes('深股通') || name.includes('沪股通')) {
    return { type: 'northbound', label: '北向资金' };
  }
  
  // 营业部
  if (name.includes('营业部') || name.includes('证券')) {
    return { type: 'brokerage', label: '营业部' };
  }
  
  return { type: 'other', label: '其他' };
}

/**
 * 分析龙虎榜数据
 */
function analyzeDragonTiger(data, code, name) {
  if (!data || !data[0] || data[0].length === 0) {
    return null;
  }
  
  const items = data[0];
  const result = {
    code: code,
    name: name,
    date: items[0]?.trade_date || items[0]?.date,
    closePrice: items[0]?.close,
    changePct: items[0]?.change_pct,
    turnover: items[0]?.turnover,
    buyAmount: 0,
    sellAmount: 0,
    netAmount: 0,
    institutionalBuy: 0,
    institutionalSell: 0,
    hotMoneyBuy: 0,
    hotMoneySell: 0,
    northboundBuy: 0,
    northboundSell: 0,
    buySeats: [],
    sellSeats: [],
    summary: ''
  };
  
  // 分析买入席位
  const buySeats = items.filter(item => item.side === 'buy' || item.type === '买入');
  const sellSeats = items.filter(item => item.side === 'sell' || item.type === '卖出');
  
  for (const seat of buySeats) {
    const amount = seat.amount || seat.net_amount || 0;
    result.buyAmount += amount;
    
    const seatType = analyzeSeatType(seat.seat_name || seat.name || '');
    
    if (seatType.type === 'institution') {
      result.institutionalBuy += amount;
    } else if (seatType.type === 'hot_money') {
      result.hotMoneyBuy += amount;
    } else if (seatType.type === 'northbound') {
      result.northboundBuy += amount;
    }
    
    result.buySeats.push({
      name: seat.seat_name || seat.name,
      amount: amount,
      type: seatType.label
    });
  }
  
  // 分析卖出席位
  for (const seat of sellSeats) {
    const amount = seat.amount || seat.net_amount || 0;
    result.sellAmount += amount;
    
    const seatType = analyzeSeatType(seat.seat_name || seat.name || '');
    
    if (seatType.type === 'institution') {
      result.institutionalSell += amount;
    } else if (seatType.type === 'hot_money') {
      result.hotMoneySell += amount;
    } else if (seatType.type === 'northbound') {
      result.northboundSell += amount;
    }
    
    result.sellSeats.push({
      name: seat.seat_name || seat.name,
      amount: amount,
      type: seatType.label
    });
  }
  
  result.netAmount = result.buyAmount - result.sellAmount;
  
  // 生成总结
  if (result.netAmount > 0) {
    result.summary = `净买入 ${(result.netAmount / 1e4).toFixed(2)} 万元`;
    
    if (result.institutionalBuy > result.institutionalSell) {
      result.summary += '，机构净买入';
    }
    
    if (result.hotMoneyBuy > result.hotMoneySell) {
      result.summary += '，游资净买入';
    }
    
    if (result.northboundBuy > result.northboundSell) {
      result.summary += '，北向资金净买入';
    }
  } else {
    result.summary = `净卖出 ${(Math.abs(result.netAmount) / 1e4).toFixed(2)} 万元`;
    
    if (result.institutionalSell > result.institutionalBuy) {
      result.summary += '，机构净卖出';
    }
    
    if (result.hotMoneySell > result.hotMoneyBuy) {
      result.summary += '，游资净卖出';
    }
    
    if (result.northboundSell > result.northboundBuy) {
      result.summary += '，北向资金净卖出';
    }
  }
  
  return result;
}

/**
 * 获取持仓股龙虎榜
 */
function getHoldingsDragonTiger() {
  if (!existsSync(HOLDINGS_FILE)) {
    console.log('⚠️ 持仓配置文件不存在');
    return [];
  }
  
  const holdingsData = JSON.parse(readFileSync(HOLDINGS_FILE, 'utf8'));
  const holdings = holdingsData.holdings || [];
  
  if (holdings.length === 0) {
    console.log('⚠️ 持仓列表为空');
    return [];
  }
  
  const allData = [];
  const today = formatDate(new Date());
  const yesterday = formatDate(new Date(Date.now() - 24 * 60 * 60 * 1000));
  
  for (const holding of holdings) {
    console.log(`🐉 获取 ${holding.name} (${holding.code}) 龙虎榜...`);
    
    // 尝试获取今日和昨日数据
    let data = getDragonTigerData(holding.code, today);
    
    if (!data) {
      data = getDragonTigerData(holding.code, yesterday);
    }
    
    if (data) {
      const analysis = analyzeDragonTiger(data, holding.code, holding.name);
      if (analysis) {
        allData.push(analysis);
      }
    }
  }
  
  return allData;
}

/**
 * 生成龙虎榜报告
 */
function generateReport(data) {
  const now = new Date();
  const dateStr = now.toLocaleDateString('zh-CN', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit' 
  });
  
  let report = `# 🐉 持仓股龙虎榜分析\n\n`;
  report += `**生成时间**: ${dateStr} ${now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })}\n\n`;
  
  if (data.length === 0) {
    report += `今日持仓股无龙虎榜数据\n\n`;
    report += `**说明**: 只有涨跌幅偏离值达 7%、换手率超 20% 等情况下才会上龙虎榜\n\n`;
    return report;
  }
  
  // 统计
  const netBuy = data.filter(d => d.netAmount > 0);
  const netSell = data.filter(d => d.netAmount < 0);
  
  report += `## 📊 数据统计\n\n`;
  report += `| 类型 | 数量 |\n`;
  report += `|------|------|\n`;
  report += `| ✅ 净买入 | ${netBuy.length} |\n`;
  report += `| ❌ 净卖出 | ${netSell.length} |\n`;
  report += `| **总计** | **${data.length}** |\n\n`;
  
  // 详细数据
  report += `## 📈 详细分析\n\n`;
  
  for (const item of data) {
    const emoji = item.netAmount > 0 ? '✅' : '❌';
    
    report += `### ${item.name} (${item.code}) ${emoji}\n\n`;
    report += `- **日期**: ${item.date}\n`;
    report += `- **收盘价**: ${item.closePrice} 元\n`;
    report += `- **涨跌幅**: ${item.changePct}%\n`;
    report += `- **成交额**: ${(item.turnover / 1e4).toFixed(2)} 万元\n`;
    report += `- **净买卖**: ${item.summary}\n`;
    report += `- **机构买卖**: 买 ${(item.institutionalBuy / 1e4).toFixed(2)} 万 / 卖 ${(item.institutionalSell / 1e4).toFixed(2)} 万\n`;
    report += `- **游资买卖**: 买 ${(item.hotMoneyBuy / 1e4).toFixed(2)} 万 / 卖 ${(item.hotMoneySell / 1e4).toFixed(2)} 万\n`;
    report += `- **北向买卖**: 买 ${(item.northboundBuy / 1e4).toFixed(2)} 万 / 卖 ${(item.northboundSell / 1e4).toFixed(2)} 万\n`;
    
    if (item.buySeats.length > 0) {
      report += `\n**买入席位**:\n`;
      for (let i = 0; i < Math.min(item.buySeats.length, 5); i++) {
        const seat = item.buySeats[i];
        report += `- ${seat.name} (${seat.type}): ${(seat.amount / 1e4).toFixed(2)} 万元\n`;
      }
    }
    
    if (item.sellSeats.length > 0) {
      report += `\n**卖出席位**:\n`;
      for (let i = 0; i < Math.min(item.sellSeats.length, 5); i++) {
        const seat = item.sellSeats[i];
        report += `- ${seat.name} (${seat.type}): ${(seat.amount / 1e4).toFixed(2)} 万元\n`;
      }
    }
    
    // 操作建议
    report += `\n**分析**: `;
    if (item.netAmount > 0 && item.institutionalBuy > item.institutionalSell) {
      report += `✅ 机构净买入，看好后市\n`;
    } else if (item.netAmount > 0 && item.hotMoneyBuy > item.hotMoneySell) {
      report += `🔥 游资主导，注意波动\n`;
    } else if (item.netAmount < 0 && item.institutionalSell > item.institutionalBuy) {
      report += `⚠️ 机构净卖出，注意风险\n`;
    } else if (item.netAmount < 0) {
      report += `❌ 资金净流出，谨慎观望\n`;
    } else {
      report += `😐 资金博弈，方向不明\n`;
    }
    
    report += `\n---\n\n`;
  }
  
  // 免责声明
  report += `---\n\n`;
  report += `⚠️ **免责声明**: 以上分析仅供参考，不构成投资建议。股市有风险，投资需谨慎。\n`;
  
  return report;
}

/**
 * 主函数
 */
function main() {
  console.log('🐉 Stock Master Pro - 龙虎榜分析\n');
  
  // 检查依赖
  try {
    const checkDepCmd = `node ${join(__dirname, 'check_dependency.mjs')}`;
    execSync(checkDepCmd, { encoding: 'utf8', stdio: 'pipe' });
  } catch (error) {
    console.log('❌ 依赖检查失败，请先安装 QVeris AI 技能');
    process.exit(1);
  }
  
  console.log('获取持仓股龙虎榜数据...\n');
  
  // 获取数据
  const data = getHoldingsDragonTiger();
  
  console.log(`\n共获取 ${data.length} 只股票的龙虎榜数据\n`);
  
  // 生成报告
  const report = generateReport(data);
  
  // 输出到控制台
  console.log(report);
  
  // 保存到文件
  try {
    if (!existsSync(STOCKS_DIR)) {
      execSync(`mkdir -p ${STOCKS_DIR}`);
    }
    
    writeFileSync(DRAGON_TIGER_FILE, JSON.stringify({
      updateTime: new Date().toISOString(),
      count: data.length,
      data: data
    }, null, 2));
    
    const dateStr = new Date().toISOString().split('T')[0];
    const reportFile = join(STOCKS_DIR, `dragon_tiger_${dateStr}.md`);
    writeFileSync(reportFile, report);
    
    console.log(`\n💾 数据已保存：${DRAGON_TIGER_FILE}`);
    console.log(`💾 报告已保存：${reportFile}`);
  } catch (error) {
    console.log(`\n⚠️  保存失败：${error.message}`);
  }
}

main();
