#!/usr/bin/env node

/**
 * 持仓检查脚本
 * 每 10 分钟执行一次，检查持仓股票的实时行情和预警
 */

import { execSync } from 'child_process';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const STOCKS_DIR = join(__dirname, '../stocks');
const HOLDINGS_FILE = join(STOCKS_DIR, 'holdings.json');
const LAST_CHECK_FILE = join(STOCKS_DIR, 'last_check.json');
const ALERTS_FILE = join(STOCKS_DIR, 'alerts.json');

// QVeris CLI 路径
const QVERIS_CLI = 'node ~/.openclaw/skills/qveris-official/scripts/qveris_tool.mjs';

// Discovery IDs（从之前的测试中获取）
const DISCOVERY_IDS = {
  real_time: '81d10584-cf1b-4229-afa2-54b9c84b7342',
  history: '777b4129-5038-4448-9f06-5fe40e4bcb00',
  company: '777b4129-5038-4448-9f06-5fe40e4bcb00',
  money_flow: 'db1539a3-17b7-4ecb-bbb4-f53dbf59ff14',
  dragon_tiger: '7e6c7f26-9201-42ed-8ef0-21e526dfcef2'
};

/**
 * 调用 QVeris CLI 获取数据
 */
function callQveris(command, params) {
  try {
    const cmd = `${QVERIS_CLI} ${command} --params '${JSON.stringify(params)}'`;
    const output = execSync(cmd, { encoding: 'utf8', timeout: 30000 });
    const result = JSON.parse(output);
    
    if (result.status_code === 200) {
      return result.data;
    } else {
      console.error(`QVeris API error: ${result.error_type || 'unknown error'}`);
      return null;
    }
  } catch (error) {
    console.error(`Failed to call QVeris: ${error.message}`);
    return null;
  }
}

/**
 * 获取实时行情
 */
function getRealTimeQuote(code) {
  const data = callQveris(
    `call ths_ifind.real_time_quotation.v1 --discovery-id ${DISCOVERY_IDS.real_time}`,
    { codes: code }
  );
  
  if (data && data[0] && data[0][0]) {
    return data[0][0];
  }
  return null;
}

/**
 * 检查预警条件
 */
function checkAlerts(holding, quote) {
  const alerts = [];
  const currentPrice = quote.latest;
  const changePct = quote.changeRatio;
  const volumeRatio = quote.vol_ratio;
  
  // 目标价预警
  if (holding.alerts?.target_price && currentPrice >= holding.alerts.target_price) {
    alerts.push({
      type: 'target_price',
      level: 'info',
      message: `🎯 ${holding.name} 达到目标价 ${currentPrice} 元（目标：${holding.alerts.target_price} 元）`,
      timestamp: new Date().toISOString()
    });
  }
  
  // 止损预警
  if (holding.alerts?.stop_loss && currentPrice <= holding.alerts.stop_loss) {
    alerts.push({
      type: 'stop_loss',
      level: 'urgent',
      message: `⚠️ ${holding.name} 触及止损价 ${currentPrice} 元（止损：${holding.alerts.stop_loss} 元）`,
      timestamp: new Date().toISOString()
    });
  }
  
  // 涨跌幅预警
  if (holding.alerts?.change_pct && Math.abs(changePct) >= holding.alerts.change_pct) {
    const direction = changePct > 0 ? '📈' : '📉';
    alerts.push({
      type: 'change_pct',
      level: 'warning',
      message: `${direction} ${holding.name} 涨跌幅 ${changePct.toFixed(2)}%（阈值：${holding.alerts.change_pct}%）`,
      timestamp: new Date().toISOString()
    });
  }
  
  // 放量预警
  if (volumeRatio >= 3) {
    alerts.push({
      type: 'volume',
      level: 'warning',
      message: `🔥 ${holding.name} 放量！量比 ${volumeRatio.toFixed(2)}`,
      timestamp: new Date().toISOString()
    });
  }
  
  return alerts;
}

/**
 * 计算盈亏
 */
function calculateProfit(holding, currentPrice) {
  const profit = (currentPrice - holding.cost) * holding.shares;
  const profitPct = ((currentPrice - holding.cost) / holding.cost) * 100;
  
  return {
    profit: profit,
    profitPct: profitPct,
    profitText: profit >= 0 ? `+${profit.toFixed(2)}` : profit.toFixed(2),
    profitPctText: profitPct >= 0 ? `+${profitPct.toFixed(2)}%` : `${profitPct.toFixed(2)}%`
  };
}

/**
 * 主函数
 */
function main() {
  console.log(`[${new Date().toISOString()}] 🚀 开始检查持仓...\n`);
  
  // 检查依赖
  try {
    const checkDepCmd = `node ${join(__dirname, 'check_dependency.mjs')}`;
    execSync(checkDepCmd, { encoding: 'utf8', stdio: 'pipe' });
  } catch (error) {
    console.log('❌ 依赖检查失败，请先安装 QVeris AI 技能');
    console.log('\n运行以下命令检查依赖：');
    console.log(`node ${join(__dirname, 'check_dependency.mjs')}`);
    process.exit(1);
  }
  
  // 检查持仓配置文件
  if (!existsSync(HOLDINGS_FILE)) {
    console.log('❌ 持仓配置文件不存在：' + HOLDINGS_FILE);
    console.log('\n请先创建持仓配置文件，参考模板：');
    console.log('https://github.com/stock-master-pro#holdingsjson');
    process.exit(1);
  }
  
  // 读取持仓配置
  let holdingsData;
  try {
    holdingsData = JSON.parse(readFileSync(HOLDINGS_FILE, 'utf8'));
  } catch (error) {
    console.log('❌ 读取持仓配置文件失败：' + error.message);
    process.exit(1);
  }
  
  const holdings = holdingsData.holdings || [];
  
  if (holdings.length === 0) {
    console.log('⚠️ 持仓列表为空，请先添加持仓股票');
    process.exit(0);
  }
  
  console.log(`📊 共 ${holdings.length} 只持仓股票\n`);
  
  const allAlerts = [];
  const checkResults = [];
  
  // 检查每只持仓
  for (const holding of holdings) {
    console.log(`📈 检查：${holding.name} (${holding.code})`);
    
    // 获取实时行情
    const quote = getRealTimeQuote(holding.code);
    if (!quote) {
      console.log(`  ❌ 获取行情失败\n`);
      continue;
    }
    
    const currentPrice = quote.latest;
    const changePct = quote.changeRatio;
    const volumeRatio = quote.vol_ratio;
    
    // 计算盈亏
    const profitInfo = calculateProfit(holding, currentPrice);
    
    console.log(`  现价：${currentPrice} 元`);
    console.log(`  今日：${changePct >= 0 ? '+' : ''}${changePct.toFixed(2)}%`);
    console.log(`  盈亏：${profitInfo.profitText} 元 (${profitInfo.profitPctText})`);
    console.log(`  量比：${volumeRatio.toFixed(2)}`);
    
    // 检查预警
    const alerts = checkAlerts(holding, quote);
    if (alerts.length > 0) {
      console.log(`  ⚠️ 触发 ${alerts.length} 条预警`);
      allAlerts.push(...alerts);
    } else {
      console.log(`  ✅ 无预警`);
    }
    console.log('');
    
    // 保存检查结果
    checkResults.push({
      code: holding.code,
      name: holding.name,
      checkTime: new Date().toISOString(),
      quote: {
        price: currentPrice,
        changePct: changePct,
        volumeRatio: volumeRatio
      },
      profit: profitInfo,
      alerts: alerts
    });
  }
  
  // 输出预警汇总
  if (allAlerts.length > 0) {
    console.log('\n' + '='.repeat(60));
    console.log('⚠️  预警汇总');
    console.log('='.repeat(60));
    
    const urgentAlerts = allAlerts.filter(a => a.level === 'urgent');
    const warningAlerts = allAlerts.filter(a => a.level === 'warning');
    const infoAlerts = allAlerts.filter(a => a.level === 'info');
    
    if (urgentAlerts.length > 0) {
      console.log('\n🚨 紧急预警：');
      for (const alert of urgentAlerts) {
        console.log(`  ${alert.message}`);
      }
    }
    
    if (warningAlerts.length > 0) {
      console.log('\n⚠️  警告：');
      for (const alert of warningAlerts) {
        console.log(`  ${alert.message}`);
      }
    }
    
    if (infoAlerts.length > 0) {
      console.log('\nℹ️  提示：');
      for (const alert of infoAlerts) {
        console.log(`  ${alert.message}`);
      }
    }
  } else {
    console.log('\n✅ 无预警信息');
  }
  
  // 保存检查结果
  const checkResult = {
    checkTime: new Date().toISOString(),
    holdingsCount: holdings.length,
    alertsCount: allAlerts.length,
    alerts: allAlerts,
    results: checkResults
  };
  
  try {
    writeFileSync(LAST_CHECK_FILE, JSON.stringify(checkResult, null, 2));
    console.log(`\n💾 检查结果已保存：${LAST_CHECK_FILE}`);
  } catch (error) {
    console.log(`\n⚠️  保存检查结果失败：${error.message}`);
  }
  
  // 保存预警记录（追加）
  if (allAlerts.length > 0) {
    try {
      let alertsData = { alerts: [] };
      if (existsSync(ALERTS_FILE)) {
        alertsData = JSON.parse(readFileSync(ALERTS_FILE, 'utf8'));
      }
      
      alertsData.alerts.push(...allAlerts);
      // 保留最近 100 条预警
      if (alertsData.alerts.length > 100) {
        alertsData.alerts = alertsData.alerts.slice(-100);
      }
      
      writeFileSync(ALERTS_FILE, JSON.stringify(alertsData, null, 2));
    } catch (error) {
      console.log(`⚠️  保存预警记录失败：${error.message}`);
    }
  }
  
  console.log(`\n✅ 检查完成，共 ${holdings.length} 只持仓，${allAlerts.length} 条预警`);
  console.log(`⏱️  下次检查时间：${new Date(Date.now() + 10 * 60 * 1000).toLocaleTimeString()}`);
}

main();
