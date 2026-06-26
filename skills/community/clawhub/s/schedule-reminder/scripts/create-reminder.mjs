#!/usr/bin/env node
/**
 * 双保险提醒系统 - 创建提醒
 * 同时创建 OpenClaw cron 和本地备份
 */

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA_DIR = path.join(process.env.HOME, '.openclaw', 'data');
const CONFIG_FILE = path.join(DATA_DIR, 'schedule-reminder-config.json');
const REMINDERS_FILE = path.join(DATA_DIR, 'reminders.json');
const RUNTIME_FILE = path.join(DATA_DIR, 'schedule-reminder-runtime.json');

// 加载配置
function loadConfig() {
  try {
    if (!fs.existsSync(CONFIG_FILE)) {
      console.error('❌ 配置文件不存在，请先运行: node scripts/install.mjs');
      process.exit(1);
    }
    return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
  } catch (err) {
    console.error('❌ 加载配置失败:', err.message);
    process.exit(1);
  }
}

// 加载提醒列表
function loadReminders() {
  try {
    if (!fs.existsSync(REMINDERS_FILE)) {
      return { reminders: [], lastCheck: 0 };
    }
    return JSON.parse(fs.readFileSync(REMINDERS_FILE, 'utf-8'));
  } catch {
    return { reminders: [], lastCheck: 0 };
  }
}

// 加载运行时数据
function loadRuntime() {
  try {
    if (!fs.existsSync(RUNTIME_FILE)) {
      return {};
    }
    return JSON.parse(fs.readFileSync(RUNTIME_FILE, 'utf-8'));
  } catch {
    return {};
  }
}

// 保存提醒列表
function saveReminders(data) {
  fs.writeFileSync(REMINDERS_FILE, JSON.stringify(data, null, 2));
}

// 解析时间
function parseTime(time) {
  if (typeof time === 'number') return time;
  
  const relativeMatch = time.match(/^\+(\d+)([smhd])$/);
  if (relativeMatch) {
    const num = parseInt(relativeMatch[1]);
    const unit = relativeMatch[2];
    const now = Date.now();
    switch (unit) {
      case 's': return now + num * 1000;
      case 'm': return now + num * 60 * 1000;
      case 'h': return now + num * 60 * 60 * 1000;
      case 'd': return now + num * 24 * 60 * 60 * 1000;
    }
  }
  
  return new Date(time).getTime();
}

// 生成唯一 ID
function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
}

// 创建双保险提醒
async function createDualReminder(params) {
  const config = loadConfig();
  const runtime = loadRuntime();
  
  const {
    name,
    message,
    time,
    to,
    accountId,
    channel,
    advisorData
  } = params;

  const timeMs = parseTime(time);
  if (!Number.isFinite(timeMs)) {
    console.error('❌ 无法解析时间，请使用 +5m / +1h / +1d / ISO 时间');
    process.exit(1);
  }
  const timeIso = new Date(timeMs).toISOString();
  const openclawBin = process.env.OPENCLAW_BIN || runtime.openclawBin || 'openclaw';
  
  const targetTo = to || config.userId;
  const targetAccount = accountId || config.accountId;
  const targetChannel = channel || config.primaryChannel;
  
  if (!targetTo) {
    console.error('❌ 未设置 userId，请编辑配置文件');
    process.exit(1);
  }

  console.log(`创建提醒: ${name}`);
  console.log(`  时间: ${new Date(timeMs).toLocaleString('zh-CN')}`);
  console.log(`  渠道: ${targetChannel}`);

  let primary = {
    created: false,
    jobId: null,
    command: null,
    error: null,
    attemptedAt: Date.now(),
  };

  // 1. 创建 OpenClaw cron（主方案）
  if (targetChannel) {
    try {
      const args = [
        'cron',
        'add',
        '--name',
        `提醒: ${name}`,
        '--at',
        timeIso,
        '--message',
        message,
        '--session',
        'isolated',
        '--wake',
        'now',
        '--announce',
        '--channel',
        targetChannel,
        '--to',
        targetTo,
        '--best-effort-deliver',
        '--delete-after-run',
        '--json',
      ];

      if (targetAccount) {
        args.push('--account', targetAccount);
      }

      const output = execFileSync(openclawBin, args, {
        timeout: 30000,
        encoding: 'utf-8',
        stdio: ['ignore', 'pipe', 'pipe'],
      });
      primary.command = [openclawBin, ...args.filter((item) => item !== targetTo)].join(' ');
      try {
        const parsed = JSON.parse(output);
        primary.jobId = parsed?.job?.id || parsed?.id || null;
      } catch {
        primary.jobId = null;
      }
      primary.created = true;
      console.log('✅ 主方案 (OpenClaw cron) 已创建');
    } catch (err) {
      primary.error = err.stderr?.toString?.() || err.message;
      console.warn('⚠️  主方案创建失败:', primary.error);
    }
  }

  // 2. 创建本地备份（备用方案）
  if (config.backupEnabled !== false) {
    const data = loadReminders();
    const reminder = {
      id: generateId(),
      name,
      message,
      time: timeMs,
      to: targetTo,
      accountId: targetAccount,
      channel: targetChannel,
      createdAt: Date.now(),
      status: 'scheduled',
      retryCount: 0,
      primary,
      backupNotBefore: primary.created ? timeMs + 90 * 1000 : timeMs,
      advisor: advisorData || null,
    };
    
    data.reminders.push(reminder);
    saveReminders(data);
    console.log('✅ 备用方案 (本地存储) 已创建');
  }
  
  console.log('\n✅ 双保险提醒创建完成！');
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log('用法: node create-reminder.mjs "<名称>" "<消息>" <时间> [幕僚JSON参数]');
    console.log('');
    console.log('时间格式:');
    console.log('  +5m     - 5分钟后');
    console.log('  +1h     - 1小时后');
    console.log('  +1d     - 1天后');
    console.log('  ISO时间 - 2026-03-30T15:00:00+08:00');
    console.log('');
    console.log('示例:');
    console.log('  node create-reminder.mjs "喝水" "该喝水了" "+30m"');
    console.log(`  node create-reminder.mjs "开会" "准备开会" "+1h" '{"goal":"同步进度", "suggestions":["提前准备PPT"]}'`);
    process.exit(1);
  }
  
  const [name, message, time = '+5m', advisorJsonRaw] = args;
  
  let advisorData = null;
  if (advisorJsonRaw) {
    try {
      advisorData = JSON.parse(advisorJsonRaw);
      console.log('💡 已附加幕僚洞察数据');
    } catch (err) {
      console.warn('⚠️  幕僚 JSON 解析失败，将忽略附加洞察:', err.message);
    }
  }
  
  try {
    await createDualReminder({ name, message, time, advisorData });
  } catch (err) {
    console.error('❌ 创建失败:', err.message);
    process.exit(1);
  }
}

main();
