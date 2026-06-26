#!/usr/bin/env node

/**
 * 市场复盘脚本
 * 生成午盘/尾盘/收盘复盘报告
 */

import { execSync } from 'child_process';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const STOCKS_DIR = join(__dirname, '../stocks');
const REVIEWS_DIR = join(STOCKS_DIR, 'reviews');
const HOLDINGS_FILE = join(STOCKS_DIR, 'holdings.json');

// QVeris CLI 路径
const QVERIS_CLI = 'node ~/.openclaw/skills/qveris-official/scripts/qveris_tool.mjs';

// Discovery IDs
const DISCOVERY_IDS = {
  real_time: '81d10584-cf1b-4229-afa2-54b9c84b7342',
  history: '777b4129-5038-4448-9f06-5fe40e4bcb00',
  money_flow: 'db1539a3-17b7-4ecb-bbb4-f53dbf59ff14'
};

/**
 * 调用 QVeris CLI
 */
function callQveris(command, params) {
  try {
    const cmd = `${QVERIS_CLI} ${command} --params '${JSON.stringify(params)}' 2>&1`;
    const output = execSync(cmd, { encoding: 'utf8', timeout: 30000 });
    
    // 提取 JSON 部分（跳过 Success/Failed 等前缀）
    const jsonStart = output.indexOf('{');
    const jsonEnd = output.lastIndexOf('}');
    
    if (jsonStart === -1 || jsonEnd === -1) {
      console.error('QVeris API error: No JSON found in output');
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
 * 获取大盘指数
 */
function getMarketIndices() {
  const codes = '000001.SH,399001.SZ,399006.SZ,399005.SZ'; // 上证、深证、创业板、中证 500
  const data = callQveris(
    `call ths_ifind.real_time_quotation.v1 --discovery-id ${DISCOVERY_IDS.real_time}`,
    { codes: codes }
  );
  
  if (!data) return null;
  
  const indices = [];
  for (const item of data) {
    if (item && item[0]) {
      const quote = item[0];
      indices.push({
        name: getIndexName(quote.thscode),
        code: quote.thscode,
        price: quote.latest,
        change: quote.change,
        changePct: quote.changeRatio,
        amount: quote.amount,
        volume: quote.volume
      });
    }
  }
  
  return indices;
}

/**
 * 获取指数名称
 */
function getIndexName(code) {
  const names = {
    '000001.SH': '上证指数',
    '399001.SZ': '深证成指',
    '399006.SZ': '创业板指',
    '399005.SZ': '中证 500'
  };
  return names[code] || code;
}

/**
 * 获取板块涨幅排行
 */
function getSectorRank() {
  // 使用资金流向 API 获取板块数据
  const data = callQveris(
    `call ths_ifind.money_flow.v1 --discovery-id ${DISCOVERY_IDS.money_flow}`,
    { scope: 'sector', startdate: formatDate(new Date()) }
  );
  
  if (!data || !data[0]) return [];
  
  const sectors = data[0]
    .filter(item => item && item.thscode)
    .slice(0, 10)
    .map(item => ({
      name: item.thsname || item.thscode,
      code: item.thscode,
      changePct: item.change_pct || 0,
      netInflow: item.main_net_inflow || 0,
      netInflowPct: item.main_net_inflow_pct || 0
    }))
    .sort((a, b) => b.changePct - a.changePct);
  
  return sectors.slice(0, 10);
}

/**
 * 获取持仓股表现
 */
function getHoldingsPerformance() {
  if (!existsSync(HOLDINGS_FILE)) {
    return [];
  }
  
  const holdingsData = JSON.parse(readFileSync(HOLDINGS_FILE, 'utf8'));
  const holdings = holdingsData.holdings || [];
  
  if (holdings.length === 0) return [];
  
  const codes = holdings.map(h => h.code).join(',');
  const data = callQveris(
    `call ths_ifind.real_time_quotation.v1 --discovery-id ${DISCOVERY_IDS.real_time}`,
    { codes: codes }
  );
  
  if (!data) return [];
  
  const performance = [];
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
    
    performance.push({
      name: holding.name,
      code: holding.code,
      price: currentPrice,
      changePct: quote.changeRatio,
      volumeRatio: quote.vol_ratio,
      turnover: quote.turnoverRatio,
      profit: profit,
      profitPct: profitPct,
      notes: holding.notes || ''
    });
  }
  
  return performance;
}

/**
 * 格式化日期
 */
function formatDate(date) {
  return date.toISOString().split('T')[0].replace(/-/g, '');
}

/**
 * 生成复盘报告
 */
function generateReview(sessionType = 'noon') {
  const now = new Date();
  const dateStr = now.toLocaleDateString('zh-CN', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit' 
  });
  const timeStr = now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
  
  // 获取数据
  console.log('📊 获取大盘数据...');
  const indices = getMarketIndices();
  
  console.log('🔥 获取板块数据...');
  const sectors = getSectorRank();
  
  console.log('💰 获取持仓表现...');
  const holdings = getHoldingsPerformance();
  
  // 生成报告
  let report = `# 【${getSessionName(sessionType)}】${dateStr} ${timeStr}\n\n`;
  
  // 大盘概览
  report += `## 📊 大盘概览\n\n`;
  report += `| 指数 | 现价 | 涨跌 | 幅度 | 成交额 |\n`;
  report += `|------|------|------|------|--------|\n`;
  
  if (indices) {
    for (const idx of indices) {
      const changeSign = idx.change >= 0 ? '+' : '';
      const changePctSign = idx.changePct >= 0 ? '+' : '';
      report += `| ${idx.name} | ${idx.price?.toFixed(2) || 'N/A'} | ${changeSign}${idx.change?.toFixed(2) || 'N/A'} | ${changePctSign}${idx.changePct?.toFixed(2) || 'N/A'}% | ${(idx.amount / 1e8).toFixed(1)}亿 |\n`;
    }
  }
  report += `\n`;
  
  // 热点板块
  report += `## 🔥 热点板块\n\n`;
  report += `| 排名 | 板块 | 涨幅 | 资金净流入 |\n`;
  report += `|------|------|------|------------|\n`;
  
  if (sectors && sectors.length > 0) {
    for (let i = 0; i < Math.min(sectors.length, 10); i++) {
      const sector = sectors[i];
      const sign = sector.changePct >= 0 ? '+' : '';
      const inflowUnit = Math.abs(sector.netInflow) > 1e8 ? '亿' : '万';
      const inflowValue = Math.abs(sector.netInflow) / (inflowUnit === '亿' ? 1e8 : 1e4);
      report += `| ${i + 1} | ${sector.name} | ${sign}${sector.changePct.toFixed(2)}% | ${sector.netInflow >= 0 ? '+' : ''}${inflowValue.toFixed(2)}${inflowUnit} |\n`;
    }
  } else {
    report += `| - | 数据暂缺 | - | - |\n`;
  }
  report += `\n`;
  
  // 持仓表现
  report += `## 💰 持仓表现\n\n`;
  
  if (holdings.length > 0) {
    for (const h of holdings) {
      const emoji = h.changePct >= 0 ? '📈' : '📉';
      const profitEmoji = h.profit >= 0 ? '✅' : '❌';
      const sign = h.changePct >= 0 ? '+' : '';
      const profitSign = h.profit >= 0 ? '+' : '';
      
      report += `### ${emoji} ${h.name} (${h.code})\n\n`;
      report += `- **现价**: ${h.price.toFixed(2)} 元\n`;
      report += `- **今日**: ${sign}${h.changePct.toFixed(2)}%\n`;
      report += `- **量比**: ${h.volumeRatio?.toFixed(2) || 'N/A'}\n`;
      report += `- **换手**: ${h.turnover?.toFixed(2) || 'N/A'}%\n`;
      report += `- **盈亏**: ${profitEmoji}${profitSign}${h.profit.toFixed(2)} 元 (${profitSign}${h.profitPct.toFixed(2)}%)\n`;
      const costPrice = h.cost || 0;
      report += `- **成本**: ${costPrice.toFixed(2)} 元\n`;
      
      if (h.notes) {
        report += `- **备注**: ${h.notes}\n`;
      }
      
      // 操作建议
      report += `\n**操作建议**: `;
      if (h.changePct > 5) {
        report += `🔥 强势，继续持有\n`;
      } else if (h.changePct > 2) {
        report += `✅ 正常，持有\n`;
      } else if (h.changePct > -2) {
        report += `😐 震荡，观望\n`;
      } else if (h.changePct > -5) {
        report += `⚠️ 走弱，注意止损\n`;
      } else {
        report += `🚨 大跌，检查是否触及止损\n`;
      }
      report += `\n---\n\n`;
    }
  } else {
    report += `暂无持仓数据\n\n`;
  }
  
  // 下午策略
  if (sessionType === 'noon') {
    report += `## 📌 下午策略\n\n`;
    
    // 根据大盘情况给出建议
    const shIndex = indices?.find(i => i.code === '000001.SH');
    if (shIndex && shIndex.changePct > 0.5) {
      report += `- **仓位建议**: 6-7 成\n`;
      report += `- **关注方向**: 热点板块持续性\n`;
      report += `- **风险提示**: 避免追高，逢低布局\n`;
    } else if (shIndex && shIndex.changePct < -0.5) {
      report += `- **仓位建议**: 4-5 成\n`;
      report += `- **关注方向**: 防御板块\n`;
      report += `- **风险提示**: 控制仓位，等待企稳\n`;
    } else {
      report += `- **仓位建议**: 5-6 成\n`;
      report += `- **关注方向**: 结构性机会\n`;
      report += `- **风险提示**: 震荡行情，高抛低吸\n`;
    }
    report += `\n`;
  }
  
  // 晚间总结（收盘后）
  if (sessionType === 'close') {
    report += `## 📊 全天总结\n\n`;
    report += `- **市场情绪**: ${getMarketSentiment(indices)}\n`;
    report += `- **成交量**: ${getVolumeAssessment(indices)}\n`;
    report += `- **明日展望**: 待定\n`;
    report += `\n`;
  }
  
  // 免责声明
  report += `---\n\n`;
  report += `⚠️ **免责声明**: 以上分析仅供参考，不构成投资建议。股市有风险，投资需谨慎。\n`;
  
  return report;
}

/**
 * 获取会话名称
 */
function getSessionName(type) {
  const names = {
    'noon': '午盘复盘',
    'afternoon': '尾盘复盘',
    'close': '收盘总结'
  };
  return names[type] || '复盘';
}

/**
 * 市场情绪评估
 */
function getMarketSentiment(indices) {
  if (!indices || indices.length === 0) return '未知';
  
  const avgChange = indices.reduce((sum, i) => sum + (i.changePct || 0), 0) / indices.length;
  
  if (avgChange > 1) return '🔥 火热';
  if (avgChange > 0.5) return '😊 偏强';
  if (avgChange > -0.5) return '😐 震荡';
  if (avgChange > -1) return '😟 偏弱';
  return '🥶 冰点';
}

/**
 * 成交量评估
 */
function getVolumeAssessment(indices) {
  if (!indices || indices.length === 0) return '未知';
  
  const totalAmount = indices.reduce((sum, i) => sum + (i.amount || 0), 0);
  const totalAmountBillion = totalAmount / 1e8;
  
  if (totalAmountBillion > 15000) return '🔥 放量';
  if (totalAmountBillion > 10000) return '😊 正常';
  if (totalAmountBillion > 8000) return '😐 缩量';
  return '🥶 严重缩量';
}

/**
 * 主函数
 */
function main() {
  console.log('📝 Stock Master Pro - 市场复盘\n');
  
  // 检查依赖
  try {
    const checkDepCmd = `node ${join(__dirname, 'check_dependency.mjs')}`;
    execSync(checkDepCmd, { encoding: 'utf8', stdio: 'pipe' });
  } catch (error) {
    console.log('❌ 依赖检查失败，请先安装 QVeris AI 技能');
    process.exit(1);
  }
  
  // 获取会话类型
  const sessionType = process.argv[2] || 'noon';
  const validTypes = ['noon', 'afternoon', 'close'];
  
  if (!validTypes.includes(sessionType)) {
    console.log(`❌ 无效的会话类型：${sessionType}`);
    console.log('有效类型：noon, afternoon, close');
    process.exit(1);
  }
  
  console.log(`生成 ${getSessionName(sessionType)} 报告...\n`);
  
  // 生成报告
  const report = generateReview(sessionType);
  
  // 输出到控制台
  console.log(report);
  
  // 保存到文件
  try {
    if (!existsSync(REVIEWS_DIR)) {
      execSync(`mkdir -p ${REVIEWS_DIR}`);
    }
    
    const dateStr = new Date().toISOString().split('T')[0];
    const reviewFile = join(REVIEWS_DIR, `${dateStr}_${sessionType}.md`);
    writeFileSync(reviewFile, report);
    
    console.log(`\n💾 报告已保存：${reviewFile}`);
  } catch (error) {
    console.log(`\n⚠️  保存报告失败：${error.message}`);
  }
}

main();
