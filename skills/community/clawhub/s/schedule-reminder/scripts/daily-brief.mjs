#!/usr/bin/env node
/**
 * 幕僚简报系统 - 每日简报 Runner
 * 读取提醒台账，生成并发送当天的日程简报
 */

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const DATA_DIR = path.join(process.env.HOME, '.openclaw', 'data');
const CONFIG_FILE = path.join(DATA_DIR, 'schedule-reminder-config.json');
const REMINDERS_FILE = path.join(DATA_DIR, 'reminders.json');
const RUNTIME_FILE = path.join(DATA_DIR, 'schedule-reminder-runtime.json');

function loadConfig() {
  try {
    if (!fs.existsSync(CONFIG_FILE)) return null;
    return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
  } catch {
    return null;
  }
}

function loadRuntime() {
  try {
    if (!fs.existsSync(RUNTIME_FILE)) return {};
    return JSON.parse(fs.readFileSync(RUNTIME_FILE, 'utf-8'));
  } catch {
    return {};
  }
}

function loadReminders() {
  try {
    if (!fs.existsSync(REMINDERS_FILE)) {
      return { reminders: [] };
    }
    return JSON.parse(fs.readFileSync(REMINDERS_FILE, 'utf-8'));
  } catch {
    return { reminders: [] };
  }
}

function saveReminders(data) {
  fs.writeFileSync(REMINDERS_FILE, JSON.stringify(data, null, 2));
}

function isToday(timestamp) {
  const date = new Date(timestamp);
  const now = new Date();
  return (
    date.getDate() === now.getDate() &&
    date.getMonth() === now.getMonth() &&
    date.getFullYear() === now.getFullYear()
  );
}

function buildBriefingMessage(events) {
  if (events.length === 0) {
    return '🌅 早上好！今天暂无已排期的重要事项。\n如果是轻松的一天，可以用来整理思路。';
  }

  let text = '🌅 幕僚早报：今日日程概览\n\n';

  events.forEach((evt, idx) => {
    const timeStr = new Date(evt.time).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
    text += `${idx + 1}. [${timeStr}] ${evt.name}\n`;
    
    if (evt.advisor) {
      if (evt.advisor.goal) {
        text += `   🎯 目标：${evt.advisor.goal}\n`;
      }
      if (evt.advisor.suggestions && Array.isArray(evt.advisor.suggestions)) {
        evt.advisor.suggestions.forEach((s) => {
          text += `   💡 建议：${s}\n`;
        });
      }
    }
    text += '\n';
  });

  return text.trim();
}

function sendBriefing(message, to, channel, runtime) {
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
    execFileSync(openclawBin, args, { stdio: 'ignore' });
    return true;
  } catch (err) {
    console.error('简报发送失败:', err.message);
    return false;
  }
}

async function main() {
  const config = loadConfig();
  if (!config || !config.userId) {
    console.error('未配置 userId，无法发送简报');
    process.exit(1);
  }

  const runtime = loadRuntime();
  const data = loadReminders();
  const reminders = data.reminders || [];

  // 过滤出今天的，且未取消、未完成的日程
  const todayEvents = reminders
    .filter(r => isToday(r.time) && r.status !== 'done' && r.status !== 'cancelled')
    .sort((a, b) => a.time - b.time);

  const message = buildBriefingMessage(todayEvents);
  
  console.log('--- 准备发送今日简报 ---');
  console.log(message);
  console.log('------------------------');

  const success = sendBriefing(message, config.userId, config.primaryChannel, runtime);

  if (success) {
    // 标记已包含在今日简报中
    let updated = false;
    data.reminders = reminders.map(r => {
      if (todayEvents.find(e => e.id === r.id)) {
        updated = true;
        return { ...r, dailyBriefIncludedAt: Date.now() };
      }
      return r;
    });
    
    if (updated) saveReminders(data);
    console.log('✅ 简报发送成功');
  }
}

main();
