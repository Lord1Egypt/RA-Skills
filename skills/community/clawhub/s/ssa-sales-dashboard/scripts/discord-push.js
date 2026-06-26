#!/usr/bin/env node

/**
 * discord-push.js - Discord 消息推送模块
 * 
 * 功能：
 *   1. 读取 Markdown 报告
 *   2. 分片（>1800 字符自动拆分）
 *   3. 通过 OpenClaw message tool 推送到指定频道
 *   4. 支持告警实时推送
 * 
 * 注意：此脚本输出推送指令，实际推送由 OpenClaw agent 执行
 * 
 * 用法：
 *   node discord-push.js --report data/reports/weekly-2026-03-24.md
 *   node discord-push.js --alert "⚠️ 回复率告警"
 *   node discord-push.js --latest-report weekly
 */

const fs = require('fs');
const path = require('path');

const BASE_DIR = path.join(__dirname, '..');
const REPORTS_DIR = path.join(BASE_DIR, 'data', 'reports');
const LATEST_PATH = path.join(BASE_DIR, 'data', 'latest.json');
const MAX_CHUNK = 1800;

// ============ 参数解析 ============
function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { report: null, alert: null, latestReport: null, dryRun: false };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--report' && args[i + 1]) opts.report = args[++i];
    if (args[i] === '--alert' && args[i + 1]) opts.alert = args[++i];
    if (args[i] === '--latest-report' && args[i + 1]) opts.latestReport = args[++i];
    if (args[i] === '--dry-run') opts.dryRun = true;
  }
  return opts;
}

// ============ 分片 ============
function splitMessage(text, maxLen = MAX_CHUNK) {
  if (text.length <= maxLen) return [text];
  
  const chunks = [];
  let remaining = text;
  
  while (remaining.length > 0) {
    if (remaining.length <= maxLen) {
      chunks.push(remaining);
      break;
    }
    
    // 尝试在段落边界分割
    let cutIdx = remaining.lastIndexOf('\n\n', maxLen);
    if (cutIdx < maxLen * 0.3) {
      // 退而求其次，在换行处分割
      cutIdx = remaining.lastIndexOf('\n', maxLen);
    }
    if (cutIdx < maxLen * 0.3) {
      // 硬切
      cutIdx = maxLen;
    }
    
    chunks.push(remaining.substring(0, cutIdx));
    remaining = remaining.substring(cutIdx).trimStart();
  }
  
  return chunks;
}

// ============ 查找最新报告 ============
function findLatestReport(period) {
  if (!fs.existsSync(REPORTS_DIR)) return null;
  
  const files = fs.readdirSync(REPORTS_DIR)
    .filter(f => f.startsWith(period + '-') && f.endsWith('.md'))
    .sort()
    .reverse();
  
  return files.length > 0 ? path.join(REPORTS_DIR, files[0]) : null;
}

// ============ 生成推送指令 ============
function generatePushInstructions(chunks, type = 'report') {
  const instructions = {
    action: 'discord_push',
    type,
    channel: '#🧠-hq-指挥中心',
    chunks: chunks.map((c, i) => ({
      index: i + 1,
      total: chunks.length,
      content: c
    })),
    total_chunks: chunks.length,
    generated_at: new Date().toISOString()
  };
  
  return instructions;
}

// ============ 告警推送 ============
function buildAlertPush() {
  if (!fs.existsSync(LATEST_PATH)) return null;
  
  const data = JSON.parse(fs.readFileSync(LATEST_PATH, 'utf-8'));
  const alerts = data.alerts || [];
  
  if (alerts.length === 0) return null;
  
  let msg = '🚨 **Sales Dashboard 异常告警**\n\n';
  msg += `**时间:** ${new Date().toISOString().replace('T', ' ').split('.')[0]}\n\n`;
  
  for (const a of alerts) {
    msg += `${a.message}\n\n`;
  }
  
  return msg;
}

// ============ 主流程 ============
function main() {
  const opts = parseArgs();
  
  let content = null;
  let pushType = 'report';
  
  if (opts.alert) {
    // 手动告警
    content = `🚨 **告警:** ${opts.alert}`;
    pushType = 'alert';
  } else if (opts.report) {
    // 指定报告文件
    if (!fs.existsSync(opts.report)) {
      console.error(`报告文件不存在: ${opts.report}`);
      process.exit(1);
    }
    content = fs.readFileSync(opts.report, 'utf-8');
  } else if (opts.latestReport) {
    // 查找最新报告
    const reportPath = findLatestReport(opts.latestReport);
    if (!reportPath) {
      console.error(`未找到 ${opts.latestReport} 报告`);
      process.exit(1);
    }
    content = fs.readFileSync(reportPath, 'utf-8');
    console.log(`使用报告: ${reportPath}`);
  } else {
    // 默认检查告警
    content = buildAlertPush();
    pushType = 'alert';
    if (!content) {
      console.log('无告警，无报告可推送');
      process.exit(0);
    }
  }
  
  const chunks = splitMessage(content);
  const instructions = generatePushInstructions(chunks, pushType);
  
  if (opts.dryRun) {
    console.log('[DRY-RUN] 推送预览：');
    console.log(JSON.stringify(instructions, null, 2));
    return;
  }
  
  // 输出 JSON 指令供 agent 读取
  console.log(JSON.stringify(instructions));
}

main();
