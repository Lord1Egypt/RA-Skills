#!/usr/bin/env node

/**
 * Remnawave 账号创建 - 日志记录脚本
 * 
 * 用途：记录每次账号创建的详细信息，用于审计和追踪
 * 
 * 用法:
 * node log-creation.js --username abel_pc --email abel@codeforce.tech --status success --uuid xxx
 */

const fs = require('fs');
const path = require('path');

// 日志目录
const LOG_BASE_DIR = path.join(__dirname, '../../logs/remnawave-account-creation');

// 解析命令行参数
const args = process.argv.slice(2);
const params = {
  username: null,
  email: null,
  squad: null,
  deviceLimit: null,
  trafficGb: null,
  trafficReset: null,
  expireDays: null,
  status: null,
  uuid: null,
  shortUuid: null,
  subscriptionUrl: null,
  emailSent: null,
  messageId: null,
  errorMessage: null,
  operator: 'AI Assistant (小 a)',
  cc: null
};

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--username' && args[i + 1]) params.username = args[++i];
  else if (args[i] === '--email' && args[i + 1]) params.email = args[++i];
  else if (args[i] === '--squad' && args[i + 1]) params.squad = args[++i];
  else if (args[i] === '--device-limit' && args[i + 1]) params.deviceLimit = parseInt(args[++i]);
  else if (args[i] === '--traffic-gb' && args[i + 1]) params.trafficGb = parseInt(args[++i]);
  else if (args[i] === '--traffic-reset' && args[i + 1]) params.trafficReset = args[++i];
  else if (args[i] === '--expire-days' && args[i + 1]) params.expireDays = parseInt(args[++i]);
  else if (args[i] === '--status' && args[i + 1]) params.status = args[++i];
  else if (args[i] === '--uuid' && args[i + 1]) params.uuid = args[++i];
  else if (args[i] === '--short-uuid' && args[i + 1]) params.shortUuid = args[++i];
  else if (args[i] === '--subscription-url' && args[i + 1]) params.subscriptionUrl = args[++i];
  else if (args[i] === '--email-sent' && args[i + 1]) params.emailSent = args[++i] === 'true';
  else if (args[i] === '--message-id' && args[i + 1]) params.messageId = args[++i];
  else if (args[i] === '--error-message' && args[i + 1]) params.errorMessage = args[++i];
  else if (args[i] === '--operator' && args[i + 1]) params.operator = args[++i];
  else if (args[i] === '--cc' && args[i + 1]) params.cc = args[++i];
}

// 创建日志目录
function ensureLogDir() {
  const now = new Date();
  const monthDir = path.join(LOG_BASE_DIR, `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`);
  
  if (!fs.existsSync(monthDir)) {
    fs.mkdirSync(monthDir, { recursive: true });
  }
  
  return monthDir;
}

// 生成日志内容
function generateLog(params) {
  const now = new Date();
  
  const logEntry = {
    timestamp: now.toISOString(),
    timestampLocal: now.toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' }),
    action: 'create_account',
    request: {
      username: params.username,
      email: params.email,
      squad: params.squad,
      deviceLimit: params.deviceLimit,
      trafficGb: params.trafficGb,
      trafficReset: params.trafficReset,
      expireDays: params.expireDays,
      cc: params.cc
    },
    result: {
      status: params.status,
      uuid: params.uuid,
      shortUuid: params.shortUuid,
      subscriptionUrl: params.subscriptionUrl,
      emailSent: params.emailSent,
      messageId: params.messageId,
      errorMessage: params.errorMessage
    },
    operator: params.operator
  };
  
  return JSON.stringify(logEntry, null, 2);
}

// 生成人类可读的日志摘要
function generateSummary(params) {
  const now = new Date();
  const statusEmoji = params.status === 'success' ? '✅' : '❌';
  
  let summary = `# ${statusEmoji} Remnawave 账号创建记录\n\n`;
  summary += `**时间:** ${now.toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}\n`;
  summary += `**操作员:** ${params.operator}\n\n`;
  
  summary += `## 请求信息\n\n`;
  summary += `| 参数 | 值 |\n`;
  summary += `|------|-----|\n`;
  summary += `| 用户名 | ${params.username} |\n`;
  summary += `| 邮箱 | ${params.email} |\n`;
  if (params.squad) summary += `| 分组 | ${params.squad} |\n`;
  if (params.deviceLimit) summary += `| 设备限制 | ${params.deviceLimit} |\n`;
  if (params.trafficGb) summary += `| 流量 | ${params.trafficGb}GB |\n`;
  if (params.trafficReset) summary += `| 流量重置 | ${params.trafficReset} |\n`;
  if (params.expireDays) summary += `| 过期天数 | ${params.expireDays} |\n`;
  if (params.cc) summary += `| 抄送 | ${params.cc} |\n`;
  
  summary += `\n## 结果\n\n`;
  summary += `**状态:** ${params.status}\n`;
  
  if (params.status === 'success') {
    summary += `**UUID:** ${params.uuid}\n`;
    summary += `**短 UUID:** ${params.shortUuid}\n`;
    summary += `**订阅地址:** ${params.subscriptionUrl}\n`;
    summary += `**邮件发送:** ${params.emailSent ? '成功' : '失败'}\n`;
    if (params.messageId) summary += `**邮件 ID:** ${params.messageId}\n`;
    summary += `\n> 💡 提示：Trojan 密码和 SS 密码已发送给用户邮箱，日志中不保存以增强安全性\n`;
  } else {
    summary += `**错误信息:** ${params.errorMessage}\n`;
  }
  
  return summary;
}

// 主函数
function main() {
  if (!params.username) {
    console.error('❌ 错误：缺少 --username 参数');
    process.exit(1);
  }
  
  if (!params.status) {
    console.error('❌ 错误：缺少 --status 参数');
    process.exit(1);
  }
  
  // 确保日志目录存在
  const logDir = ensureLogDir();
  
  // 生成日志文件名
  const now = new Date();
  const dateStr = now.toISOString().split('T')[0];
  const timeStr = now.toTimeString().split(' ')[0].replace(/:/g, '-');
  const logFileName = `${dateStr}-${timeStr}-${params.username}.log`;
  const logFilePath = path.join(logDir, logFileName);
  
  // 生成并写入 JSON 日志
  const logContent = generateLog(params);
  fs.writeFileSync(logFilePath, logContent, 'utf-8');
  
  console.log(`✅ 日志已保存：${logFilePath}`);
  
  // 同时生成人类可读的摘要（Markdown 格式）
  const summaryFileName = `${dateStr}-${timeStr}-${params.username}.md`;
  const summaryFilePath = path.join(logDir, summaryFileName);
  const summaryContent = generateSummary(params);
  fs.writeFileSync(summaryFilePath, summaryContent, 'utf-8');
  
  console.log(`✅ 摘要已保存：${summaryFilePath}`);
  
  // 如果是成功创建，更新月度统计
  if (params.status === 'success') {
    updateMonthlyStats(logDir, now);
  }
}

// 更新月度统计
function updateMonthlyStats(logDir, now) {
  const statsFile = path.join(logDir, 'monthly-stats.json');
  
  let stats = {
    month: `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`,
    totalCreated: 0,
    totalFailed: 0,
    emailSent: 0,
    bySquad: {},
    byDay: {}
  };
  
  // 读取现有统计
  if (fs.existsSync(statsFile)) {
    try {
      stats = JSON.parse(fs.readFileSync(statsFile, 'utf-8'));
    } catch (e) {
      // 忽略解析错误
    }
  }
  
  // 更新统计
  stats.totalCreated++;
  
  // 按组统计
  const squad = params.squad || 'Default-Squad';
  if (!stats.bySquad[squad]) {
    stats.bySquad[squad] = 0;
  }
  stats.bySquad[squad]++;
  
  // 按天统计
  const dayKey = now.toISOString().split('T')[0];
  if (!stats.byDay[dayKey]) {
    stats.byDay[dayKey] = 0;
  }
  stats.byDay[dayKey]++;
  
  // 邮件发送统计
  if (params.emailSent) {
    stats.emailSent++;
  }
  
  // 写入统计文件
  fs.writeFileSync(statsFile, JSON.stringify(stats, null, 2), 'utf-8');
}

// 运行主函数
main();
