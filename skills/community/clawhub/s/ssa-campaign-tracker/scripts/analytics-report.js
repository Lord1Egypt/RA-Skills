#!/usr/bin/env node

/**
 * analytics-report.js - 开发信效果分析报告生成器
 * 
 * 功能：
 * 1. 读取 archive/ 目录的 sent_records（JSONL 格式）
 * 2. 读取 reply-tracking/ 目录的回复记录
 * 3. 计算核心指标：回复率、转化漏斗、按 campaign/template/sales_owner 分组统计
 * 4. 生成周报（--weekly）和月报（--monthly）模式
 * 5. 输出格式：Markdown（Obsidian）+ JSON（机器可读）
 * 6. 支持自定义时间范围（--from DATE --to DATE）
 * 7. 支持 dry-run 模式
 * 8. 记录报告生成日志
 * 
 * 用法：
 *   node analytics-report.js --weekly [--dry-run] [--from 2026-03-17 --to 2026-03-24]
 *   node analytics-report.js --monthly [--dry-run] [--from 2026-03-01 --to 2026-03-31]
 */

const fs = require('fs');
const path = require('path');

// ============ 配置 ============
const CONFIG = {
  baseDir: path.join(__dirname, '..'),
  archiveDir: path.join(__dirname, '..', 'archive'),
  replyTrackingDir: path.join(__dirname, '..', 'reply-tracking'),
  logsDir: path.join(__dirname, '..', 'logs', 'analytics'),
  obsidianDir: process.env.OBSIDIAN_VAULT ? path.join(process.env.OBSIDIAN_VAULT, 'Farreach 知识库/业务分析/开发信效果') : '<path-to-obsidian-vault>/Farreach 知识库/业务分析/开发信效果',
  outputDir: path.join(__dirname, '..', 'reports')
};

// ============ 工具函数 ============

/**
 * 日志记录
 */
function log(level, message, data = null) {
  const timestamp = new Date().toISOString();
  const logEntry = {
    timestamp,
    level,
    message,
    data
  };
  
  console.log(`[${timestamp}] [${level.toUpperCase()}] ${message}`);
  if (data) {
    console.log(JSON.stringify(data, null, 2));
  }
  
  // 写入日志文件
  try {
    if (!fs.existsSync(CONFIG.logsDir)) {
      fs.mkdirSync(CONFIG.logsDir, { recursive: true });
    }
    const logFile = path.join(CONFIG.logsDir, `${new Date().toISOString().split('T')[0]}.log`);
    fs.appendFileSync(logFile, JSON.stringify(logEntry) + '\n');
  } catch (err) {
    console.error('Failed to write log:', err.message);
  }
}

/**
 * 读取 JSONL 文件
 */
function readJsonlFile(filePath) {
  if (!fs.existsSync(filePath)) {
    return [];
  }
  
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.trim().split('\n').filter(line => line.trim());
  const records = [];
  
  for (const line of lines) {
    try {
      records.push(JSON.parse(line));
    } catch (err) {
      log('warn', `Failed to parse JSONL line: ${line.substring(0, 50)}...`, { error: err.message });
    }
  }
  
  return records;
}

/**
 * 读取目录下所有 JSONL 文件
 */
function readAllJsonlFiles(dirPath) {
  if (!fs.existsSync(dirPath)) {
    return [];
  }
  
  const files = fs.readdirSync(dirPath).filter(f => f.endsWith('.jsonl'));
  const allRecords = [];
  
  for (const file of files) {
    const filePath = path.join(dirPath, file);
    const records = readJsonlFile(filePath);
    allRecords.push(...records);
  }
  
  return allRecords;
}

/**
 * 解析日期参数
 */
function parseDate(dateStr) {
  if (!dateStr) return null;
  
  // 支持 YYYY-MM-DD 格式
  const match = dateStr.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (match) {
    return new Date(`${dateStr}T00:00:00.000Z`);
  }
  
  // 支持 ISO 格式
  return new Date(dateStr);
}

/**
 * 获取周报日期范围
 */
function getWeeklyRange(referenceDate = new Date()) {
  const ref = new Date(referenceDate);
  const dayOfWeek = ref.getUTCDay(); // 0 = Sunday
  const mondayOffset = dayOfWeek === 0 ? -6 : 1 - dayOfWeek;
  
  const monday = new Date(ref);
  monday.setUTCDate(ref.getUTCDate() + mondayOffset);
  monday.setUTCHours(0, 0, 0, 0);
  
  const sunday = new Date(monday);
  sunday.setUTCDate(monday.getUTCDate() + 6);
  sunday.setUTCHours(23, 59, 59, 999);
  
  return { from: monday, to: sunday };
}

/**
 * 获取月报日期范围
 */
function getMonthlyRange(referenceDate = new Date()) {
  const ref = new Date(referenceDate);
  
  const firstDay = new Date(ref.getUTCFullYear(), ref.getUTCMonth(), 1);
  firstDay.setUTCHours(0, 0, 0, 0);
  
  const lastDay = new Date(ref.getUTCFullYear(), ref.getUTCMonth() + 1, 0);
  lastDay.setUTCHours(23, 59, 59, 999);
  
  return { from: firstDay, to: lastDay };
}

/**
 * 过滤日期范围内的记录
 */
function filterByDateRange(records, fromDate, toDate, dateField = 'sent_timestamp') {
  return records.filter(record => {
    const recordDate = new Date(record[dateField]);
    return recordDate >= fromDate && recordDate <= toDate;
  });
}

/**
 * 计算转化漏斗
 */
function calculateFunnel(sentRecords, replyTracking) {
  const replyMap = new Map();
  for (const reply of replyTracking) {
    replyMap.set(reply.sent_record_id, reply);
  }
  
  const funnel = {
    sent: 0,
    opened: 0,
    replied: 0,
    qualified: 0,
    converted: 0,
    closed_won: 0
  };
  
  for (const record of sentRecords) {
    funnel.sent++;
    
    // 检查回复状态
    const reply = replyMap.get(record.record_id);
    if (reply && reply.reply_received) {
      funnel.replied++;
      
      // 合格线索：positive 或 inquiry 类型
      if (['positive', 'inquiry'].includes(reply.reply_type)) {
        funnel.qualified++;
      }
    }
    
    // 检查转化漏斗阶段（如果 sent_record 中有此字段）
    if (record.conversion_funnel_stage) {
      const stage = record.conversion_funnel_stage;
      if (['opened', 'replied', 'qualified', 'converted', 'closed_won'].includes(stage)) {
        funnel[stage]++;
      }
    }
  }
  
  return funnel;
}

/**
 * 按维度分组统计
 */
function groupByDimension(records, dimension, replyTracking) {
  const replyMap = new Map();
  for (const reply of replyTracking) {
    replyMap.set(reply.sent_record_id, reply);
  }
  
  const groups = new Map();
  
  for (const record of records) {
    const key = record[dimension] || 'unknown';
    if (!groups.has(key)) {
      groups.set(key, {
        sent: 0,
        replied: 0,
        qualified: 0,
        converted: 0,
        records: []
      });
    }
    
    const group = groups.get(key);
    group.sent++;
    group.records.push(record);
    
    const reply = replyMap.get(record.record_id);
    if (reply && reply.reply_received) {
      group.replied++;
      if (['positive', 'inquiry'].includes(reply.reply_type)) {
        group.qualified++;
      }
    }
    
    if (record.conversion_funnel_stage === 'converted') {
      group.converted++;
    }
  }
  
  // 计算每个组的指标
  const result = [];
  for (const [key, group] of groups) {
    result.push({
      [dimension]: key,
      sent_count: group.sent,
      replied_count: group.replied,
      reply_rate: group.sent > 0 ? (group.replied / group.sent).toFixed(3) : 0,
      qualified_count: group.qualified,
      qualified_rate: group.sent > 0 ? (group.qualified / group.sent).toFixed(3) : 0,
      converted_count: group.converted,
      conversion_rate: group.sent > 0 ? (group.converted / group.sent).toFixed(3) : 0
    });
  }
  
  // 按 sent_count 降序排序
  result.sort((a, b) => b.sent_count - a.sent_count);
  
  return result;
}

/**
 * 生成 Markdown 报告
 */
function generateMarkdownReport(reportData, reportType, dateRange) {
  const { metrics, funnel, byCampaign, byTemplate, bySalesOwner } = reportData;
  
  const dateStr = `${dateRange.from.toISOString().split('T')[0]} 至 ${dateRange.to.toISOString().split('T')[0]}`;
  const reportTitle = reportType === 'weekly' ? '周报' : '月报';
  
  let md = `# 开发信效果分析${reportTitle}\n\n`;
  md += `**报告期间：** ${dateStr}\n`;
  md += `**生成时间：** ${new Date().toISOString()}\n\n`;
  
  md += `---\n\n`;
  
  // 核心指标
  md += `## 📊 核心指标\n\n`;
  md += `| 指标 | 数值 | 目标值 | 状态 |\n`;
  md += `|------|------|--------|------|\n`;
  
  const replyRateStatus = metrics.reply_rate >= 0.15 ? '✅' : metrics.reply_rate >= 0.05 ? '⚠️' : '❌';
  const conversionRateStatus = metrics.conversion_rate >= 0.03 ? '✅' : metrics.conversion_rate >= 0.01 ? '⚠️' : '❌';
  
  md += `| 发送总数 | ${metrics.sent_count} | - | - |\n`;
  md += `| 回复总数 | ${metrics.replied_count} | - | - |\n`;
  md += `| 回复率 | ${(metrics.reply_rate * 100).toFixed(1)}% | 15% | ${replyRateStatus} |\n`;
  md += `| 转化数 | ${metrics.converted_count} | - | - |\n`;
  md += `| 转化率 | ${(metrics.conversion_rate * 100).toFixed(2)}% | 3% | ${conversionRateStatus} |\n`;
  md += `| 合格线索数 | ${metrics.qualified_count} | - | - |\n`;
  md += `| 合格线索率 | ${(metrics.qualified_rate * 100).toFixed(1)}% | - | - |\n\n`;
  
  // 转化漏斗
  md += `## 🔄 转化漏斗\n\n`;
  md += `| 阶段 | 数量 | 转化率 |\n`;
  md += `|------|------|--------|\n`;
  md += `| 已发送 (Sent) | ${funnel.sent} | 100% |\n`;
  md += `| 已回复 (Replied) | ${funnel.replied} | ${(funnel.replied / funnel.sent * 100).toFixed(1)}% |\n`;
  md += `| 合格线索 (Qualified) | ${funnel.qualified} | ${(funnel.qualified / funnel.sent * 100).toFixed(1)}% |\n`;
  md += `| 已转化 (Converted) | ${funnel.converted} | ${(funnel.converted / funnel.sent * 100).toFixed(2)}% |\n\n`;
  
  // 按营销活动分组
  if (byCampaign.length > 0) {
    md += `## 📧 按营销活动分析\n\n`;
    md += `| 活动 ID | 发送数 | 回复数 | 回复率 | 转化数 | 转化率 |\n`;
    md += `|---------|--------|--------|--------|--------|--------|\n`;
    for (const camp of byCampaign) {
      md += `| ${camp.campaign_id} | ${camp.sent_count} | ${camp.replied_count} | ${(camp.reply_rate * 100).toFixed(1)}% | ${camp.converted_count} | ${(camp.conversion_rate * 100).toFixed(2)}% |\n`;
    }
    md += `\n`;
  }
  
  // 按模板分组
  if (byTemplate.length > 0) {
    md += `## 📝 按模板分析\n\n`;
    md += `| 模板 ID | 发送数 | 回复数 | 回复率 | 转化数 | 转化率 |\n`;
    md += `|---------|--------|--------|--------|--------|--------|\n`;
    for (const tmpl of byTemplate) {
      md += `| ${tmpl.template_id} | ${tmpl.sent_count} | ${tmpl.replied_count} | ${(tmpl.reply_rate * 100).toFixed(1)}% | ${tmpl.converted_count} | ${(tmpl.conversion_rate * 100).toFixed(2)}% |\n`;
    }
    md += `\n`;
  }
  
  // 按销售人员分组
  if (bySalesOwner.length > 0) {
    md += `## 👤 按销售人员分析\n\n`;
    md += `| 销售人员 | 发送数 | 回复数 | 回复率 | 转化数 | 转化率 |\n`;
    md += `|----------|--------|--------|--------|--------|--------|\n`;
    for (const sales of bySalesOwner) {
      md += `| ${sales.sales_owner} | ${sales.sent_count} | ${sales.replied_count} | ${(sales.reply_rate * 100).toFixed(1)}% | ${sales.converted_count} | ${(sales.conversion_rate * 100).toFixed(2)}% |\n`;
    }
    md += `\n`;
  }
  
  // 洞察与建议
  md += `## 💡 洞察与建议\n\n`;
  
  // 最佳模板
  if (byTemplate.length > 0) {
    const bestTemplate = byTemplate.reduce((best, curr) => 
      parseFloat(curr.reply_rate) > parseFloat(best.reply_rate) ? curr : best
    );
    md += `**最佳模板：** ${bestTemplate.template_id}（回复率 ${(bestTemplate.reply_rate * 100).toFixed(1)}%）\n\n`;
  }
  
  // 最佳销售人员
  if (bySalesOwner.length > 1) {
    const bestSales = bySalesOwner.reduce((best, curr) => 
      parseFloat(curr.reply_rate) > parseFloat(best.reply_rate) ? curr : best
    );
    md += `**最佳表现：** ${bestSales.sales_owner}（回复率 ${(bestSales.reply_rate * 100).toFixed(1)}%）\n\n`;
  }
  
  // 改进建议
  if (metrics.reply_rate < 0.05) {
    md += `**⚠️ 警告：** 回复率低于 5%，建议：\n`;
    md += `- 检查邮件主题行吸引力\n`;
    md += `- 优化目标客户列表质量\n`;
    md += `- 考虑 A/B 测试不同模板\n\n`;
  }
  
  md += `---\n\n`;
  md += `_报告由 campaign-tracker 自动生成_\n`;
  
  return md;
}

/**
 * 生成 JSON 报告
 */
function generateJsonReport(reportData, reportType, dateRange) {
  return {
    report_type: reportType,
    generated_at: new Date().toISOString(),
    date_range: {
      from: dateRange.from.toISOString(),
      to: dateRange.to.toISOString()
    },
    metrics: reportData.metrics,
    funnel: reportData.funnel,
    breakdown: {
      by_campaign: reportData.byCampaign,
      by_template: reportData.byTemplate,
      by_sales_owner: reportData.bySalesOwner
    }
  };
}

// ============ 主函数 ============

async function main() {
  const args = process.argv.slice(2);
  
  // 解析参数
  const isWeekly = args.includes('--weekly');
  const isMonthly = args.includes('--monthly');
  const isDryRun = args.includes('--dry-run');
  
  const fromIdx = args.indexOf('--from');
  const toIdx = args.indexOf('--to');
  
  let fromDate = fromIdx > -1 ? parseDate(args[fromIdx + 1]) : null;
  let toDate = toIdx > -1 ? parseDate(args[toIdx + 1]) : null;
  
  // 确定报告类型
  let reportType;
  if (isWeekly) {
    reportType = 'weekly';
    if (!fromDate || !toDate) {
      const range = getWeeklyRange();
      fromDate = range.from;
      toDate = range.to;
    }
  } else if (isMonthly) {
    reportType = 'monthly';
    if (!fromDate || !toDate) {
      const range = getMonthlyRange();
      fromDate = range.from;
      toDate = range.to;
    }
  } else {
    console.log('用法：node analytics-report.js --weekly|--monthly [--dry-run] [--from YYYY-MM-DD] [--to YYYY-MM-DD]');
    process.exit(1);
  }
  
  log('info', `Starting analytics report generation`, {
    report_type: reportType,
    date_range: { from: fromDate.toISOString(), to: toDate.toISOString() },
    dry_run: isDryRun
  });
  
  // 读取数据
  log('info', 'Loading sent records from archive...');
  const sentRecords = readAllJsonlFiles(CONFIG.archiveDir);
  log('info', `Loaded ${sentRecords.length} sent records`);
  
  log('info', 'Loading reply tracking data...');
  const replyTracking = readAllJsonlFiles(CONFIG.replyTrackingDir);
  log('info', `Loaded ${replyTracking.length} reply tracking records`);
  
  // 过滤日期范围
  const filteredSent = filterByDateRange(sentRecords, fromDate, toDate);
  log('info', `Filtered to ${filteredSent.length} records in date range`);
  
  // 计算指标
  const funnel = calculateFunnel(filteredSent, replyTracking);
  
  const metrics = {
    sent_count: funnel.sent,
    replied_count: funnel.replied,
    reply_rate: funnel.sent > 0 ? funnel.replied / funnel.sent : 0,
    qualified_count: funnel.qualified,
    qualified_rate: funnel.sent > 0 ? funnel.qualified / funnel.sent : 0,
    converted_count: funnel.converted,
    conversion_rate: funnel.sent > 0 ? funnel.converted / funnel.sent : 0
  };
  
  // 按维度分组
  const byCampaign = groupByDimension(filteredSent, 'campaign_id', replyTracking);
  const byTemplate = groupByDimension(filteredSent, 'template_id', replyTracking);
  const bySalesOwner = groupByDimension(filteredSent, 'sales_owner', replyTracking);
  
  const reportData = { metrics, funnel, byCampaign, byTemplate, bySalesOwner };
  
  // 生成报告
  log('info', 'Generating Markdown report...');
  const mdReport = generateMarkdownReport(reportData, reportType, { from: fromDate, to: toDate });
  
  log('info', 'Generating JSON report...');
  const jsonReport = generateJsonReport(reportData, reportType, { from: fromDate, to: toDate });
  
  // Dry-run 模式：仅预览
  if (isDryRun) {
    console.log('\n========== DRY-RUN MODE ==========\n');
    console.log(mdReport);
    console.log('\n===================================\n');
    log('info', 'Dry-run complete. Report preview shown above.');
    return;
  }
  
  // 创建输出目录
  if (!fs.existsSync(CONFIG.outputDir)) {
    fs.mkdirSync(CONFIG.outputDir, { recursive: true });
  }
  
  // 创建 Obsidian 目录
  if (!fs.existsSync(CONFIG.obsidianDir)) {
    fs.mkdirSync(CONFIG.obsidianDir, { recursive: true });
  }
  
  // 保存报告
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('T')[0];
  const mdFilename = `${reportType}-report-${timestamp}.md`;
  const jsonFilename = `${reportType}-report-${timestamp}.json`;
  
  const mdPath = path.join(CONFIG.outputDir, mdFilename);
  const jsonPath = path.join(CONFIG.outputDir, jsonFilename);
  const obsidianPath = path.join(CONFIG.obsidianDir, mdFilename);
  
  fs.writeFileSync(mdPath, mdReport);
  log('info', `Markdown report saved to ${mdPath}`);
  
  fs.writeFileSync(jsonPath, JSON.stringify(jsonReport, null, 2));
  log('info', `JSON report saved to ${jsonPath}`);
  
  // 复制到 Obsidian
  fs.writeFileSync(obsidianPath, mdReport);
  log('info', `Markdown report copied to Obsidian: ${obsidianPath}`);
  
  // 总结
  log('info', 'Report generation completed', {
    sent_count: metrics.sent_count,
    replied_count: metrics.replied_count,
    reply_rate: `${(metrics.reply_rate * 100).toFixed(1)}%`,
    converted_count: metrics.converted_count,
    conversion_rate: `${(metrics.conversion_rate * 100).toFixed(2)}%`,
    output_files: [mdPath, jsonPath, obsidianPath]
  });
  
  console.log('\n✅ Report generation completed!');
  console.log(`   Markdown: ${mdPath}`);
  console.log(`   JSON: ${jsonPath}`);
  console.log(`   Obsidian: ${obsidianPath}`);
}

// 运行
main().catch(err => {
  log('error', 'Report generation failed', { error: err.message, stack: err.stack });
  console.error('Error:', err.message);
  process.exit(1);
});
