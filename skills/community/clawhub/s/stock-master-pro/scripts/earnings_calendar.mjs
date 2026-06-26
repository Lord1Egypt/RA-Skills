#!/usr/bin/env node

/**
 * 财报日历脚本
 * 监控持仓股的财报发布日期，提前预警
 */

import { execSync } from 'child_process';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const STOCKS_DIR = join(__dirname, '../stocks');
const HOLDINGS_FILE = join(STOCKS_DIR, 'holdings.json');
const EARNINGS_FILE = join(STOCKS_DIR, 'earnings_calendar.json');

// QVeris CLI 路径
const QVERIS_CLI = 'node ~/.openclaw/skills/qveris-official/scripts/qveris_tool.mjs';

// Discovery IDs
const DISCOVERY_IDS = {
  company: '777b4129-5038-4448-9f06-5fe40e4bcb00'
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
 * 获取财报数据
 */
function getEarningsData(code) {
  // 尝试调用财报 API
  const data = callQveris(
    `call ths_ifind.earnings_forecast.v1 --discovery-id ${DISCOVERY_IDS.company}`,
    { codes: code }
  );
  
  return data;
}

/**
 * 获取公司基本信息（包含财报日期）
 */
function getCompanyInfo(code) {
  const data = callQveris(
    `call ths_ifind.company_basics.v1 --discovery-id ${DISCOVERY_IDS.company}`,
    { codes: code }
  );
  
  return data;
}

/**
 * 估算财报发布日期
 */
function estimateEarningsDate(code) {
  // A 股财报披露时间规则：
  // 年报：1 月 1 日 - 4 月 30 日
  // 一季报：4 月 1 日 - 4 月 30 日
  // 中报：7 月 1 日 - 8 月 31 日
  // 三季报：10 月 1 日 - 10 月 31 日
  
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth() + 1;
  const day = now.getDate();
  
  let nextEarningsType = '';
  let estimatedDate = null;
  
  // 根据当前日期估算下一个财报类型和日期
  if (month <= 4) {
    // 1-4 月：年报 + 一季报
    nextEarningsType = '年报/一季报';
    estimatedDate = new Date(year, 3, 15); // 估算 4 月 15 日
  } else if (month <= 8) {
    // 5-8 月：中报
    nextEarningsType = '中报';
    estimatedDate = new Date(year, 7, 15); // 估算 8 月 15 日
  } else if (month <= 10) {
    // 9-10 月：三季报
    nextEarningsType = '三季报';
    estimatedDate = new Date(year, 9, 15); // 估算 10 月 15 日
  } else {
    // 11-12 月：等待年报
    nextEarningsType = '年报';
    estimatedDate = new Date(year + 1, 3, 15); // 估算明年 4 月 15 日
  }
  
  return {
    type: nextEarningsType,
    estimatedDate: estimatedDate,
    daysUntil: Math.ceil((estimatedDate - now) / (1000 * 60 * 60 * 24))
  };
}

/**
 * 获取持仓股财报日历
 */
function getHoldingsEarningsCalendar() {
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
  
  const calendar = [];
  
  for (const holding of holdings) {
    console.log(`📅 获取 ${holding.name} (${holding.code}) 财报信息...`);
    
    // 尝试获取财报数据
    let earningsData = getEarningsData(holding.code);
    
    // 如果 API 无数据，使用估算
    if (!earningsData) {
      const estimated = estimateEarningsDate(holding.code);
      
      calendar.push({
        code: holding.code,
        name: holding.name,
        earningsType: estimated.type,
        estimatedDate: estimated.estimatedDate.toISOString().split('T')[0],
        daysUntil: estimated.daysUntil,
        isEstimated: true,
        forecast: '未知',
        riskLevel: estimated.daysUntil < 5 ? 'high' : 'normal'
      });
    } else {
      // 处理 API 返回的数据
      for (const item of earningsData[0] || []) {
        if (item && item.report_date) {
          const reportDate = new Date(item.report_date);
          const now = new Date();
          const daysUntil = Math.ceil((reportDate - now) / (1000 * 60 * 60 * 24));
          
          calendar.push({
            code: holding.code,
            name: holding.name,
            earningsType: item.report_type || '定期报告',
            estimatedDate: item.report_date,
            daysUntil: daysUntil,
            isEstimated: false,
            forecast: item.forecast_type || '未知',
            riskLevel: daysUntil < 5 ? 'high' : 'normal'
          });
        }
      }
    }
  }
  
  // 按日期排序
  calendar.sort((a, b) => a.daysUntil - b.daysUntil);
  
  return calendar;
}

/**
 * 生成财报日历报告
 */
function generateReport(calendar) {
  const now = new Date();
  const dateStr = now.toLocaleDateString('zh-CN', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit' 
  });
  
  let report = `# 📅 持仓股财报日历\n\n`;
  report += `**生成时间**: ${dateStr} ${now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })}\n\n`;
  
  if (calendar.length === 0) {
    report += `暂无财报数据\n\n`;
    return report;
  }
  
  // 分类
  const urgent = calendar.filter(c => c.daysUntil <= 5);
  const soon = calendar.filter(c => c.daysUntil > 5 && c.daysUntil <= 15);
  const normal = calendar.filter(c => c.daysUntil > 15);
  
  report += `## 📊 统计\n\n`;
  report += `| 类型 | 数量 |\n`;
  report += `|------|------|\n`;
  report += `| 🚨 临近 (<5 天) | ${urgent.length} |\n`;
  report += `| ⚠️ 近期 (5-15 天) | ${soon.length} |\n`;
  report += `| 📅 远期 (>15 天) | ${normal.length} |\n`;
  report += `| **总计** | **${calendar.length}** |\n\n`;
  
  // 临近财报
  if (urgent.length > 0) {
    report += `## 🚨 临近财报（<5 天）\n\n`;
    report += `⚠️ **注意**: 以下股票即将发布财报，建议降低仓位规避不确定性！\n\n`;
    
    for (const item of urgent) {
      const date = new Date(item.estimatedDate);
      const dateStr = `${date.getMonth() + 1}月${date.getDate()}日`;
      
      report += `### ${item.name} (${item.code})\n\n`;
      report += `- **财报类型**: ${item.earningsType}\n`;
      report += `- **预计日期**: ${dateStr}（${item.daysUntil}天后）\n`;
      report += `- **数据来源**: ${item.isEstimated ? '估算' : '官方'}\n`;
      report += `- **业绩预报**: ${item.forecast}\n`;
      
      if (item.forecast === '预增' || item.forecast === '预盈') {
        report += `- **预期**: ✅ 向好\n`;
      } else if (item.forecast === '预减' || item.forecast === '预亏') {
        report += `- **预期**: ❌ 向差\n`;
      } else {
        report += `- **预期**: 😐 未知\n`;
      }
      
      report += `- **建议**: 🚨 财报前降低仓位，待财报发布后再决策\n\n`;
    }
  }
  
  // 近期财报
  if (soon.length > 0) {
    report += `## ⚠️ 近期财报（5-15 天）\n\n`;
    
    for (const item of soon) {
      const date = new Date(item.estimatedDate);
      const dateStr = `${date.getMonth() + 1}月${date.getDate()}日`;
      
      report += `### ${item.name} (${item.code})\n\n`;
      report += `- **财报类型**: ${item.earningsType}\n`;
      report += `- **预计日期**: ${dateStr}（${item.daysUntil}天后）\n`;
      report += `- **建议**: ⚠️ 关注财报预告\n\n`;
    }
  }
  
  // 远期财报
  if (normal.length > 0) {
    report += `## 📅 远期财报（>15 天）\n\n`;
    
    for (const item of normal.slice(0, 10)) { // 只显示前 10 条
      const date = new Date(item.estimatedDate);
      const dateStr = `${date.getMonth() + 1}月${date.getDate()}日`;
      
      report += `- **${item.name}** (${item.code}): ${item.earningsType} - ${dateStr}\n`;
    }
    
    if (normal.length > 10) {
      report += `\n... 还有 ${normal.length - 10} 只股票\n`;
    }
    report += `\n`;
  }
  
  // 财报季提示
  const currentMonth = now.getMonth() + 1;
  if ([1, 2, 3, 4].includes(currentMonth)) {
    report += `## 📌 财报季提示\n\n`;
    report += `当前是**年报 + 一季报**披露期（1-4 月）。\n\n`;
    report += `- 1 月：年报预约披露开始\n`;
    report += `- 3-4 月：年报密集披露\n`;
    report += `- 4 月：一季报密集披露\n\n`;
    report += `**策略**: 财报季波动加大，建议控制仓位，规避业绩不确定个股。\n\n`;
  } else if ([7, 8].includes(currentMonth)) {
    report += `## 📌 财报季提示\n\n`;
    report += `当前是**中报**披露期（7-8 月）。\n\n`;
    report += `- 7 月：中报预约披露开始\n`;
    report += `- 8 月：中报密集披露\n\n`;
    report += `**策略**: 关注业绩预增个股，规避业绩暴雷风险。\n\n`;
  } else if ([10].includes(currentMonth)) {
    report += `## 📌 财报季提示\n\n`;
    report += `当前是**三季报**披露期（10 月）。\n\n`;
    report += `- 10 月：三季报密集披露\n\n`;
    report += `**策略**: 三季报决定全年预期，重点关注。\n\n`;
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
  console.log('📅 Stock Master Pro - 财报日历\n');
  
  // 检查依赖
  try {
    const checkDepCmd = `node ${join(__dirname, 'check_dependency.mjs')}`;
    execSync(checkDepCmd, { encoding: 'utf8', stdio: 'pipe' });
  } catch (error) {
    console.log('❌ 依赖检查失败，请先安装 QVeris AI 技能');
    process.exit(1);
  }
  
  console.log('获取持仓股财报信息...\n');
  
  // 获取财报日历
  const calendar = getHoldingsEarningsCalendar();
  
  console.log(`\n共获取 ${calendar.length} 只股票的财报信息\n`);
  
  // 生成报告
  const report = generateReport(calendar);
  
  // 输出到控制台
  console.log(report);
  
  // 保存到文件
  try {
    if (!existsSync(STOCKS_DIR)) {
      execSync(`mkdir -p ${STOCKS_DIR}`);
    }
    
    writeFileSync(EARNINGS_FILE, JSON.stringify({
      updateTime: new Date().toISOString(),
      count: calendar.length,
      calendar: calendar
    }, null, 2));
    
    const dateStr = new Date().toISOString().split('T')[0];
    const reportFile = join(STOCKS_DIR, `earnings_calendar_${dateStr}.md`);
    writeFileSync(reportFile, report);
    
    console.log(`\n💾 数据已保存：${EARNINGS_FILE}`);
    console.log(`💾 报告已保存：${reportFile}`);
  } catch (error) {
    console.log(`\n⚠️  保存失败：${error.message}`);
  }
  
  // 输出预警
  const urgent = calendar.filter(c => c.daysUntil <= 5);
  if (urgent.length > 0) {
    console.log('\n' + '='.repeat(60));
    console.log('🚨 财报临近预警');
    console.log('='.repeat(60));
    for (const item of urgent) {
      console.log(`⚠️ ${item.name} (${item.code}): ${item.earningsType} 还有 ${item.daysUntil} 天`);
    }
    console.log('\n建议：财报前降低仓位，规避不确定性');
  }
}

main();
