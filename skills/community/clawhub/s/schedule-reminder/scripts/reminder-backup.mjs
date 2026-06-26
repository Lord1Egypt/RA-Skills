#!/usr/bin/env node
/**
 * 双保险提醒系统 - 备用检查脚本
 * 由系统 crontab 每分钟触发，不依赖 Gateway
 */

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const DATA_DIR = path.join(process.env.HOME, '.openclaw', 'data');
const CONFIG_FILE = path.join(DATA_DIR, 'schedule-reminder-config.json');
const REMINDERS_FILE = path.join(DATA_DIR, 'reminders.json');
const LOG_FILE = path.join(DATA_DIR, 'reminder-backup.log');
const RUNTIME_FILE = path.join(DATA_DIR, 'schedule-reminder-runtime.json');

// 日志
function log(level, message) {
  const timestamp = new Date().toISOString();
  const line = `[${timestamp}] [${level}] ${message}\n`;
  fs.appendFileSync(LOG_FILE, line);
  console.log(line.trim());
}

// 加载配置
function loadConfig() {
  try {
    if (!fs.existsSync(CONFIG_FILE)) return null;
    return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
  } catch (err) {
    log('ERROR', `加载配置失败: ${err.message}`);
    return null;
  }
}

// 加载运行时配置
function loadRuntime() {
  try {
    if (!fs.existsSync(RUNTIME_FILE)) return {};
    return JSON.parse(fs.readFileSync(RUNTIME_FILE, 'utf-8'));
  } catch (err) {
    log('ERROR', `加载运行时配置失败: ${err.message}`);
    return {};
  }
}

// 加载提醒
function loadReminders() {
  try {
    if (!fs.existsSync(REMINDERS_FILE)) {
      return { reminders: [], lastCheck: 0 };
    }
    return JSON.parse(fs.readFileSync(REMINDERS_FILE, 'utf-8'));
  } catch (err) {
    log('ERROR', `加载提醒失败: ${err.message}`);
    return { reminders: [], lastCheck: 0 };
  }
}

// 保存提醒
function saveReminders(data) {
  fs.writeFileSync(REMINDERS_FILE, JSON.stringify(data, null, 2));
}

// 尝试发送消息
async function trySendMessage(message, to, channel, accountId, runtime) {
  const openclawBin = process.env.OPENCLAW_BIN || runtime.openclawBin || 'openclaw';

  try {
    const args = [
      'message',
      'send',
      '--channel',
      channel || 'openclaw-weixin',
      '--target',
      to,
      '--message',
      message,
    ];

    if (accountId) {
      args.push('--account', accountId);
    }

    execFileSync(openclawBin, args, {
      timeout: 30000,
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    log('INFO', `消息已发送 (CLI): ${to}`);
    return true;
  } catch (err) {
    const detail = err.stderr?.toString?.().trim() || err.message;
    log('DEBUG', `CLI 发送失败: ${detail}`);
  }

  return false;
}

// 检查 Gateway 状态
function checkGatewayAlive(openclawBin) {
  try {
    execFileSync(openclawBin, ['cron', 'status'], { timeout: 5000, stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

// 检查并发送提醒
async function checkAndSendReminders() {
  const config = loadConfig();
  const runtime = loadRuntime();
  if (!config || config.backupEnabled === false) {
    return;
  }

  const openclawBin = process.env.OPENCLAW_BIN || runtime.openclawBin || 'openclaw';
  const gatewayAlive = checkGatewayAlive(openclawBin);

  const now = Date.now();
  const data = loadReminders();
  const reminders = data.reminders || [];
  const remaining = [];
  const sent = [];

  if (reminders.length > 0 && !gatewayAlive) {
    log('WARN', 'Gateway 疑似失联！备用系统处于接管状态');
  }

  for (const reminder of reminders) {
    const backupNotBefore = Number.isFinite(reminder.backupNotBefore)
      ? reminder.backupNotBefore
      : reminder.time;

    if (backupNotBefore > now + 30000) {
      remaining.push(reminder);
      continue;
    }

    // 检查是否到期（允许 30 秒误差）
    if (reminder.time <= now + 30000) {
      // 如果 Gateway 活着，且当时主方案创建成功了，就直接放过，不触发备用发送
      if (gatewayAlive && reminder.primary && reminder.primary.created) {
        log('INFO', `Gateway 正常运行，跳过备用发送并清理任务: ${reminder.name}`);
        continue;
      }

      log('INFO', `处理提醒: ${reminder.name}`);
      
      const message = `⏰ [备用触发] ${reminder.message}`;
      const success = await trySendMessage(
        message,
        reminder.to,
        reminder.channel,
        reminder.accountId,
        runtime,
      );

      if (success) {
        sent.push({ ...reminder, status: 'backup_sent', backupSentAt: now });
      } else {
        // 重试机制
        const retryCount = reminder.retryCount || 0;
        if (retryCount < 3) {
          remaining.push({
            ...reminder,
            status: 'retrying',
            retryCount: retryCount + 1,
            time: now + 5 * 60 * 1000  // 5分钟后重试
          });
          log('WARN', `发送失败，5分钟后重试 (${retryCount + 1}/3)`);
        } else {
          log('ERROR', `发送失败超过3次，放弃: ${reminder.name}`);
        }
      }
    } else {
      remaining.push(reminder);
    }
  }

  data.reminders = remaining;
  data.lastCheck = now;
  saveReminders(data);

  if (sent.length > 0) {
    log('INFO', `发送 ${sent.length} 个提醒，剩余 ${remaining.length} 个`);
  }
}

// 主函数
async function main() {
  try {
    await checkAndSendReminders();
  } catch (err) {
    log('ERROR', `意外错误: ${err.message}`);
    process.exit(1);
  }
}

main();
