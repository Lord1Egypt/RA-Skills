#!/usr/bin/env node

/**
 * 公告监控脚本
 * 监控持仓股的最新公告，分析利好/利空
 */

import { execSync } from 'child_process';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const STOCKS_DIR = join(__dirname, '../stocks');
const HOLDINGS_FILE = join(STOCKS_DIR, 'holdings.json');
const ANNOUNCEMENTS_FILE = join(STOCKS_DIR, 'announcements.json');

// QVeris CLI 路径
const QVERIS_CLI = 'node ~/.openclaw/skills/qveris-official/scripts/qveris_tool.mjs';

// Discovery IDs
const DISCOVERY_IDS = {
  announcements: '777b4129-5038-4448-9f06-5fe40e4bcb00'
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
 * 获取公司公告
 */
function getAnnouncements(code) {
  // 尝试调用公告 API
  const data = callQveris(
    `call ths_ifind.company_announcements.v1 --discovery-id ${DISCOVERY_IDS.announcements}`,
    { codes: code, startdate: formatDate(new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)), enddate: formatDate(new Date()) }
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
 * 分析公告类型
 */
function analyzeAnnouncementType(title) {
  const titleLower = title.toLowerCase();
  
  // 利好类型
  const positive = [
    '业绩预增', '预增', '扭亏', '盈利', '中标', '重大合同',
    '增持', '回购', '股权激励', '分红', '转让', '合作',
    '专利', '技术突破', '新产品', '产能扩张', '订单'
  ];
  
  // 利空类型
  const negative = [
    '业绩预减', '预减', '亏损', '减持', '处罚', '监管',
    '立案', '调查', '诉讼', '仲裁', '风险', '警示',
    'ST', '退市', '延期', '取消', '终止', '下滑', '下降'
  ];
  
  // 中性类型
  const neutral = [
    '股东大会', '董事会', '监事会', '选举', '聘任',
    '变更', '公告', '提示', '说明', '报告'
  ];
  
  for (const keyword of positive) {
    if (titleLower.includes(keyword)) {
      return { type: 'positive', level: 'good', label: '利好' };
    }
  }
  
  for (const keyword of negative) {
    if (titleLower.includes(keyword)) {
      return { type: 'negative', level: 'bad', label: '利空' };
    }
  }
  
  for (const keyword of neutral) {
    if (titleLower.includes(keyword)) {
      return { type: 'neutral', level: 'info', label: '中性' };
    }
  }
  
  return { type: 'unknown', level: 'info', label: '未知' };
}

/**
 * 分析公告影响
 */
function analyzeImpact(announcement) {
  const analysis = analyzeAnnouncementType(announcement.title || '');
  
  return {
    ...analysis,
    title: announcement.title,
    date: announcement.date,
    url: announcement.url,
    summary: announcement.summary || ''
  };
}

/**
 * 获取持仓股公告
 */
function getHoldingsAnnouncements() {
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
  
  const allAnnouncements = [];
  
  for (const holding of holdings) {
    console.log(`📢 获取 ${holding.name} (${holding.code}) 公告...`);
    
    const announcements = getAnnouncements(holding.code);
    
    if (announcements && announcements[0]) {
      for (const item of announcements[0]) {
        if (item && item.title) {
          const analysis = analyzeImpact({
            title: item.title,
            date: item.date || item.pubtime,
            url: item.url,
            summary: item.summary
          });
          
          allAnnouncements.push({
            code: holding.code,
            name: holding.name,
            ...analysis
          });
        }
      }
    }
  }
  
  // 按日期排序
  allAnnouncements.sort((a, b) => {
    if (a.date && b.date) {
      return b.date.localeCompare(a.date);
    }
    return 0;
  });
  
  return allAnnouncements;
}

/**
 * 生成公告报告
 */
function generateReport(announcements) {
  const now = new Date();
  const dateStr = now.toLocaleDateString('zh-CN', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit' 
  });
  
  let report = `# 📢 持仓股公告监控\n\n`;
  report += `**生成时间**: ${dateStr} ${now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })}\n\n`;
  
  if (announcements.length === 0) {
    report += `暂无公告数据\n\n`;
    return report;
  }
  
  // 分类统计
  const positive = announcements.filter(a => a.type === 'positive');
  const negative = announcements.filter(a => a.type === 'negative');
  const neutral = announcements.filter(a => a.type === 'neutral');
  const unknown = announcements.filter(a => a.type === 'unknown');
  
  report += `## 📊 公告统计\n\n`;
  report += `| 类型 | 数量 |\n`;
  report += `|------|------|\n`;
  report += `| ✅ 利好 | ${positive.length} |\n`;
  report += `| ❌ 利空 | ${negative.length} |\n`;
  report += `| ℹ️  中性 | ${neutral.length} |\n`;
  report += `| ❓ 未知 | ${unknown.length} |\n`;
  report += `| **总计** | **${announcements.length}** |\n\n`;
  
  // 利好公告
  if (positive.length > 0) {
    report += `## ✅ 利好公告\n\n`;
    for (const item of positive) {
      report += `### ${item.name} (${item.code})\n\n`;
      report += `- **标题**: ${item.title}\n`;
      report += `- **日期**: ${item.date || '未知'}\n`;
      report += `- **影响**: 正面\n\n`;
    }
  }
  
  // 利空公告
  if (negative.length > 0) {
    report += `## ❌ 利空公告\n\n`;
    report += `⚠️ **注意**: 以下公告可能影响股价，请密切关注！\n\n`;
    
    for (const item of negative) {
      report += `### ${item.name} (${item.code})\n\n`;
      report += `- **标题**: ${item.title}\n`;
      report += `- **日期**: ${item.date || '未知'}\n`;
      report += `- **影响**: 负面\n`;
      report += `- **建议**: 密切关注股价走势，必要时减仓\n\n`;
    }
  }
  
  // 中性公告
  if (neutral.length > 0) {
    report += `## ℹ️  中性公告\n\n`;
    for (const item of neutral.slice(0, 10)) { // 只显示前 10 条
      report += `### ${item.name} (${item.code})\n\n`;
      report += `- **标题**: ${item.title}\n`;
      report += `- **日期**: ${item.date || '未知'}\n\n`;
    }
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
  console.log('📢 Stock Master Pro - 公告监控\n');
  
  // 检查依赖
  try {
    const checkDepCmd = `node ${join(__dirname, 'check_dependency.mjs')}`;
    execSync(checkDepCmd, { encoding: 'utf8', stdio: 'pipe' });
  } catch (error) {
    console.log('❌ 依赖检查失败，请先安装 QVeris AI 技能');
    process.exit(1);
  }
  
  console.log('获取持仓股公告...\n');
  
  // 获取公告
  const announcements = getHoldingsAnnouncements();
  
  console.log(`\n共获取 ${announcements.length} 条公告\n`);
  
  // 生成报告
  const report = generateReport(announcements);
  
  // 输出到控制台
  console.log(report);
  
  // 保存到文件
  try {
    if (!existsSync(STOCKS_DIR)) {
      execSync(`mkdir -p ${STOCKS_DIR}`);
    }
    
    writeFileSync(ANNOUNCEMENTS_FILE, JSON.stringify({
      updateTime: new Date().toISOString(),
      count: announcements.length,
      announcements: announcements
    }, null, 2));
    
    const dateStr = new Date().toISOString().split('T')[0];
    const reportFile = join(STOCKS_DIR, `announcements_${dateStr}.md`);
    writeFileSync(reportFile, report);
    
    console.log(`\n💾 公告数据已保存：${ANNOUNCEMENTS_FILE}`);
    console.log(`💾 报告已保存：${reportFile}`);
  } catch (error) {
    console.log(`\n⚠️  保存失败：${error.message}`);
  }
  
  // 输出预警
  const negative = announcements.filter(a => a.type === 'negative');
  if (negative.length > 0) {
    console.log('\n' + '='.repeat(60));
    console.log('⚠️  利空公告预警');
    console.log('='.repeat(60));
    for (const item of negative) {
      console.log(`❌ ${item.name} (${item.code}): ${item.title}`);
    }
  }
}

main();
