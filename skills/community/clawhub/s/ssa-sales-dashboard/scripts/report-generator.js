#!/usr/bin/env node

/**
 * report-generator.js - 参数化销售报告生成器
 * 
 * 用法：
 *   node report-generator.js --period weekly [--date 2026-03-24] [--dry-run]
 *   node report-generator.js --period monthly [--date 2026-03-01] [--dry-run]
 * 
 * 输出：
 *   data/reports/{period}-{date}.md   (Markdown 报告)
 *   stdout (预览)
 */

const fs = require('fs');
const path = require('path');

const BASE_DIR = path.join(__dirname, '..');
const LATEST_PATH = path.join(BASE_DIR, 'data', 'latest.json');
const CALCULATED_PATH = path.join(BASE_DIR, 'data', 'calculated.json');
const REPORTS_DIR = path.join(BASE_DIR, 'data', 'reports');
const CONFIG_PATH = path.join(BASE_DIR, 'config', 'dashboard-config.json');

// ============ 参数解析 ============
function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { period: 'weekly', date: null, dryRun: false };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--period' && args[i + 1]) opts.period = args[++i];
    if (args[i] === '--date' && args[i + 1]) opts.date = args[++i];
    if (args[i] === '--dry-run') opts.dryRun = true;
  }
  return opts;
}

// ============ 格式化工具 ============
function fmtNum(val, unit) {
  if (val === 'N/A' || val === undefined || val === null) return 'N/A';
  if (unit === 'USD') return `$${Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  if (unit === '%') return `${val}%`;
  return `${val}`;
}

function fmtChange(change) {
  if (change === 'N/A' || change === undefined || change === null) return '';
  const sign = change > 0 ? '📈 +' : change < 0 ? '📉 ' : '➡️ ';
  return ` ${sign}${change}%`;
}

// ============ 报告生成 ============
function generateReport(period) {
  // 优先读 calculated.json，其次 latest.json
  const dataPath = fs.existsSync(CALCULATED_PATH) ? CALCULATED_PATH : LATEST_PATH;
  if (!fs.existsSync(dataPath)) {
    console.error('数据文件不存在，请先运行 data-collector.js');
    process.exit(1);
  }
  
  const data = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));
  const kpis = data.kpis || {};
  const comp = data.comparison || {};
  const funnel = data.funnel || [];
  const alerts = data.alerts || [];
  const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
  
  const periodLabel = period === 'weekly' ? '周报' : '月报';
  const range = data.metadata ? data.metadata.date_range : {};
  const sources = data.metadata ? data.metadata.sources_available : [];
  
  let md = '';
  
  // 标题
  md += `# 📊 Farreach 销售${periodLabel}\n\n`;
  md += `**周期:** ${range.start || '?'} ~ ${range.end || '?'}\n`;
  md += `**生成时间:** ${new Date().toISOString().replace('T', ' ').split('.')[0]}\n`;
  md += `**数据源:** ${sources.join(', ') || 'N/A'}\n\n`;
  
  // 告警区域
  if (alerts.length > 0) {
    md += `## 🚨 异常告警\n\n`;
    for (const a of alerts) {
      md += `${a.message}\n\n`;
    }
  }
  
  // KPI 概览
  md += `## 📈 核心指标\n\n`;
  
  const kpiList = [
    { key: 'new_leads', label: '新线索', unit: '条' },
    { key: 'new_customers', label: '新客户', unit: '个' },
    { key: 'opportunity_count', label: '商机', unit: '个' },
    { key: 'quotation_count', label: '报价单', unit: '份' },
    { key: 'quotation_amount', label: '报价金额', unit: 'USD' },
    { key: 'order_count', label: '订单', unit: '份' },
    { key: 'order_amount', label: '订单金额', unit: 'USD' },
    { key: 'conversion_rate', label: '报价转化率', unit: '%' },
    { key: 'email_sent', label: '邮件发送', unit: '封' },
    { key: 'email_reply_rate', label: '回复率', unit: '%' }
  ];
  
  for (const item of kpiList) {
    const val = kpis[item.key];
    let changeStr = '';
    if (comp.available && comp.changes && comp.changes[item.key]) {
      changeStr = fmtChange(comp.changes[item.key].change_percent);
    }
    md += `**${item.label}:** ${fmtNum(val, item.unit)}${changeStr}\n\n`;
  }
  
  // 转化漏斗
  if (funnel.length > 0) {
    md += `## 🔄 转化漏斗\n\n`;
    for (const s of funnel) {
      const rate = s.rate_from_prev !== undefined && s.rate_from_prev !== 'N/A'
        ? ` → ${s.rate_from_prev}%`
        : '';
      md += `**${s.stage}:** ${s.count}${rate}\n\n`;
    }
  }
  
  // 建议
  md += `## 💡 建议\n\n`;
  
  if (alerts.some(a => a.type === 'zero_orders')) {
    md += `1. 本周零订单，建议：检查报价跟进情况，主动联系高意向客户\n\n`;
  }
  if (alerts.some(a => a.type === 'reply_rate_low')) {
    md += `2. 邮件回复率偏低，建议：优化邮件标题和开头，检查发送对象精准度\n\n`;
  }
  if (alerts.some(a => a.type === 'low_conversion')) {
    md += `3. 报价转化率偏低，建议：分析失败报价原因（价格/交期/规格），优化报价策略\n\n`;
  }
  if (alerts.some(a => a.type === 'leads_no_opportunity')) {
    md += `4. 线索转商机率低，建议：加快线索初筛和首次响应速度\n\n`;
  }
  if (alerts.length === 0) {
    md += `各项指标正常，继续保持当前节奏。\n\n`;
  }
  
  md += `---\n*由 Sales Dashboard 自动生成*\n`;
  
  return md;
}

// ============ 主流程 ============
function main() {
  const opts = parseArgs();
  
  const report = generateReport(opts.period);
  
  if (opts.dryRun) {
    console.log('[DRY-RUN] 报告预览：\n');
    console.log(report);
    return;
  }
  
  // 保存报告
  if (!fs.existsSync(REPORTS_DIR)) fs.mkdirSync(REPORTS_DIR, { recursive: true });
  
  const dateStr = opts.date || new Date().toISOString().split('T')[0];
  const filename = `${opts.period}-${dateStr}.md`;
  const filepath = path.join(REPORTS_DIR, filename);
  
  fs.writeFileSync(filepath, report);
  console.log(`报告已保存: ${filepath}`);
  console.log('\n' + report);
  
  // 同时输出报告内容到 stdout（供 discord-push.js 读取）
}

main();
