#!/usr/bin/env node
/**
 * HIIC 产业日报订阅管理脚本
 * 
 * 用法:
 *   node subscription-manager.mjs list                    # 列出所有订阅
 *   node subscription-manager.mjs add --industry "石油" --keywords "油价,石油" --time "09:00"
 *   node subscription-manager.mjs remove <id>             # 删除订阅
 *   node subscription-manager.mjs pause <id>              # 暂停订阅
 *   node subscription-manager.mjs resume <id>             # 恢复订阅
 */

import { parseArgs } from 'util';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { execSync } from 'child_process';
import { homedir } from 'os';
import { join } from 'path';

const { values, positionals } = parseArgs({
  options: {
    industry: { type: 'string', short: 'i' },
    keywords: { type: 'string', short: 'k' },
    time: { type: 'string', short: 't', default: '09:00' },
    frequency: { type: 'string', short: 'f', default: 'daily' }
  },
  allowPositionals: true
});

const SUBSCRIPTIONS_FILE = join(homedir(), '.openclaw', 'workspace', 'hiic-subscriptions.json');
const SCRIPT_DIR = join(homedir(), '.openclaw', 'workspace', 'skills', 'hiic-industry-daily-report', 'scripts');

// 加载订阅列表
function loadSubscriptions() {
  if (!existsSync(SUBSCRIPTIONS_FILE)) {
    return { subscriptions: [] };
  }
  
  try {
    return JSON.parse(readFileSync(SUBSCRIPTIONS_FILE, 'utf-8'));
  } catch (err) {
    console.error('❌ 加载订阅列表失败:', err.message);
    return { subscriptions: [] };
  }
}

// 保存订阅列表
function saveSubscriptions(data) {
  writeFileSync(SUBSCRIPTIONS_FILE, JSON.stringify(data, null, 2), 'utf-8');
}

// 列出所有订阅
function listSubscriptions() {
  const data = loadSubscriptions();
  
  if (data.subscriptions.length === 0) {
    console.log('📭 暂无订阅');
    return;
  }
  
  console.log('📋 订阅列表');
  console.log('================================\n');
  
  data.subscriptions.forEach((sub, idx) => {
    const status = sub.paused ? '⏸️  已暂停' : '✅ 运行中';
    console.log(`${idx + 1}. ${sub.industry}`);
    console.log(`   状态: ${status}`);
    console.log(`   关键词: ${sub.keywords}`);
    console.log(`   时间: 每天 ${sub.time}`);
    console.log(`   频率: ${sub.frequency}`);
    console.log(`   ID: ${sub.id}`);
    console.log(`   创建时间: ${sub.createdAt}\n`);
  });
  
  console.log('================================');
  console.log(`共 ${data.subscriptions.length} 个订阅\n`);
}

// 添加订阅
function addSubscription() {
  if (!values.industry) {
    console.error('❌ 请提供产业名称');
    console.error('用法: node subscription-manager.mjs add --industry "石油" --keywords "油价,石油" --time "09:00"');
    process.exit(1);
  }
  
  const industry = values.industry;
  const keywords = values.keywords || industry;
  const time = values.time;
  const frequency = values.frequency;
  
  // 生成唯一ID
  const id = `hiic-${industry.toLowerCase().replace(/\s+/g, '-')}-${Date.now()}`;
  
  const subscription = {
    id,
    industry,
    keywords,
    time,
    frequency,
    paused: false,
    createdAt: new Date().toISOString()
  };
  
  // 保存到订阅列表
  const data = loadSubscriptions();
  data.subscriptions.push(subscription);
  saveSubscriptions(data);
  
  // 添加到 crontab
  const [hour, minute] = time.split(':');
  const cronExpr = `${minute} ${hour} * * *`;
  
  const pushScript = join(SCRIPT_DIR, `push-${id}.sh`);
  const outputPath = join(homedir(), '.openclaw', 'workspace', 'hiic-reports');
  
  // 创建推送脚本
  const scriptContent = `#!/bin/bash
# 自动生成的推送脚本 - ${industry}

set -e

INDUSTRY="${industry}"
KEYWORDS="${keywords}"
DATE=$(date +%Y-%m-%d)
OUTPUT_FILE="${outputPath}/\${INDUSTRY}-\${DATE}.md"

echo "📰 生成 $INDUSTRY 产业日报..."

node ${join(SCRIPT_DIR, 'generate-report-v7.3.mjs')} \\
  --industry "\$INDUSTRY" \\
  --keywords "\$KEYWORDS" \\
  --maxResults 30 \\
  --output "\$OUTPUT_FILE" \\
  --saveToBitable true

if [ $? -eq 0 ]; then
  echo "✅ 日报已生成: \$OUTPUT_FILE"
else
  echo "❌ 日报生成失败"
  exit 1
fi
`;
  
  writeFileSync(pushScript, scriptContent, 'utf-8');
  execSync(`chmod +x "${pushScript}"`);
  
  // 添加到 crontab
  const currentCron = execSync('crontab -l 2>/dev/null || echo ""', { encoding: 'utf-8' });
  const newCron = currentCron.trim() + `\n${cronExpr} ${pushScript} >> ${outputPath}/${id}.log 2>&1 # ${id}`;
  execSync(`echo "${newCron}" | crontab -`);
  
  console.log('✅ 订阅添加成功！\n');
  console.log('📋 订阅信息:');
  console.log(`   产业: ${industry}`);
  console.log(`   关键词: ${keywords}`);
  console.log(`   时间: 每天 ${time}`);
  console.log(`   频率: ${frequency}`);
  console.log(`   ID: ${id}`);
  console.log(`   推送脚本: ${pushScript}\n`);
  console.log('🔍 查看定时任务: crontab -l');
  console.log('📝 查看日志: tail -f ' + join(outputPath, `${id}.log`) + '\n');
}

// 删除订阅
function removeSubscription(id) {
  if (!id) {
    console.error('❌ 请提供订阅ID');
    console.error('用法: node subscription-manager.mjs remove <id>');
    process.exit(1);
  }
  
  const data = loadSubscriptions();
  const index = data.subscriptions.findIndex(s => s.id === id);
  
  if (index === -1) {
    console.error('❌ 订阅不存在');
    process.exit(1);
  }
  
  const subscription = data.subscriptions[index];
  
  // 从 crontab 中删除
  const currentCron = execSync('crontab -l 2>/dev/null || echo ""', { encoding: 'utf-8' });
  const newCron = currentCron
    .split('\n')
    .filter(line => !line.includes(id))
    .join('\n');
  execSync(`echo "${newCron}" | crontab -`);
  
  // 删除推送脚本
  const pushScript = join(SCRIPT_DIR, `push-${id}.sh`);
  if (existsSync(pushScript)) {
    execSync(`rm -f "${pushScript}"`);
  }
  
  // 从订阅列表中删除
  data.subscriptions.splice(index, 1);
  saveSubscriptions(data);
  
  console.log('✅ 订阅已删除');
  console.log(`   产业: ${subscription.industry}`);
  console.log(`   ID: ${id}\n`);
}

// 暂停订阅
function pauseSubscription(id) {
  if (!id) {
    console.error('❌ 请提供订阅ID');
    process.exit(1);
  }
  
  const data = loadSubscriptions();
  const subscription = data.subscriptions.find(s => s.id === id);
  
  if (!subscription) {
    console.error('❌ 订阅不存在');
    process.exit(1);
  }
  
  if (subscription.paused) {
    console.log('⚠️  订阅已经暂停');
    return;
  }
  
  // 更新状态
  subscription.paused = true;
  saveSubscriptions(data);
  
  // 从 crontab 中删除
  const currentCron = execSync('crontab -l 2>/dev/null || echo ""', { encoding: 'utf-8' });
  const newCron = currentCron
    .split('\n')
    .filter(line => !line.includes(id))
    .join('\n');
  execSync(`echo "${newCron}" | crontab -`);
  
  console.log('⏸️  订阅已暂停');
  console.log(`   产业: ${subscription.industry}`);
  console.log(`   ID: ${id}\n`);
}

// 恢复订阅
function resumeSubscription(id) {
  if (!id) {
    console.error('❌ 请提供订阅ID');
    process.exit(1);
  }
  
  const data = loadSubscriptions();
  const subscription = data.subscriptions.find(s => s.id === id);
  
  if (!subscription) {
    console.error('❌ 订阅不存在');
    process.exit(1);
  }
  
  if (!subscription.paused) {
    console.log('⚠️  订阅已经在运行');
    return;
  }
  
  // 更新状态
  subscription.paused = false;
  saveSubscriptions(data);
  
  // 重新添加到 crontab
  const [hour, minute] = subscription.time.split(':');
  const cronExpr = `${minute} ${hour} * * *`;
  
  const pushScript = join(SCRIPT_DIR, `push-${id}.sh`);
  const outputPath = join(homedir(), '.openclaw', 'workspace', 'hiic-reports');
  
  const currentCron = execSync('crontab -l 2>/dev/null || echo ""', { encoding: 'utf-8' });
  const newCron = currentCron.trim() + `\n${cronExpr} ${pushScript} >> ${outputPath}/${id}.log 2>&1 # ${id}`;
  execSync(`echo "${newCron}" | crontab -`);
  
  console.log('▶️  订阅已恢复');
  console.log(`   产业: ${subscription.industry}`);
  console.log(`   ID: ${id}\n`);
}

// 主函数
const action = positionals[0];

switch (action) {
  case 'list':
    listSubscriptions();
    break;
  case 'add':
    addSubscription();
    break;
  case 'remove':
    removeSubscription(positionals[1]);
    break;
  case 'pause':
    pauseSubscription(positionals[1]);
    break;
  case 'resume':
    resumeSubscription(positionals[1]);
    break;
  default:
    console.error('❌ 未知操作:', action);
    console.error('');
    console.error('用法:');
    console.error('  node subscription-manager.mjs list');
    console.error('  node subscription-manager.mjs add --industry "石油" --keywords "油价,石油" --time "09:00"');
    console.error('  node subscription-manager.mjs remove <id>');
    console.error('  node subscription-manager.mjs pause <id>');
    console.error('  node subscription-manager.mjs resume <id>');
    process.exit(1);
}
