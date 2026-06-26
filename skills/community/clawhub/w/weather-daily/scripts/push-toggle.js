#!/usr/bin/env node
/**
 * weather-daily — 推送开关
 *
 * 用法:
 *   node push-toggle.js on <userId>   开启推送
 *   node push-toggle.js off <userId>  关闭推送
 *   node push-toggle.js status <userId>  查看状态
 *
 * 选项:
 *   --morning HH:MM   早报时间（覆盖用户设置，默认 07:00）
 *   --evening HH:MM   晚报时间（覆盖用户设置，默认 21:00）
 *   --channel <name>  推送渠道（默认 telegram）
 */

const fs = require('fs');
const path = require('path');

const USERS_DIR = path.join(__dirname, '../data/users');

// 只允许字母、数字、连字符、下划线，最长 128 字符
function sanitizeId(value, label) {
  if (typeof value !== 'string' || !/^[a-zA-Z0-9_-]{1,128}$/.test(value)) {
    console.error(`❌ 无效的 ${label}：只允许字母、数字、- 和 _，长度 1-128`);
    process.exit(1);
  }
  return value;
}

// 校验 HH:MM 格式，返回 { h, m } 整数
function sanitizeTime(value, label) {
  if (typeof value !== 'string' || !/^\d{1,2}:\d{2}$/.test(value)) {
    console.error(`❌ 无效的 ${label}：格式应为 HH:MM，如 07:00`);
    process.exit(1);
  }
  const [h, m] = value.split(':').map(Number);
  if (h < 0 || h > 23 || m < 0 || m > 59) {
    console.error(`❌ 无效的 ${label}：小时 0-23，分钟 0-59`);
    process.exit(1);
  }
  return { h, m };
}

// 验证文件路径确实在 USERS_DIR 内（防路径穿越）
function safeUserPath(userId) {
  const resolved = path.resolve(USERS_DIR, `${userId}.json`);
  if (!resolved.startsWith(path.resolve(USERS_DIR) + path.sep)) {
    console.error('❌ 非法路径');
    process.exit(1);
  }
  return resolved;
}

function loadUser(userId) {
  const f = safeUserPath(userId);
  if (!fs.existsSync(f)) return null;
  return JSON.parse(fs.readFileSync(f, 'utf8'));
}

function saveUser(userId, data) {
  fs.mkdirSync(USERS_DIR, { recursive: true });
  fs.writeFileSync(safeUserPath(userId), JSON.stringify(data, null, 2), 'utf8');
}

const ALLOWED_CHANNELS = new Set(['telegram', 'feishu', 'slack', 'discord']);

function enablePush(userId, opts = {}) {
  userId = sanitizeId(userId, 'userId');

  // 加载用户资料获取默认推送时间
  const userProfile = loadUser(userId);
  const defaultMorning = (userProfile && userProfile.preferences && userProfile.preferences.morningTime) || '07:00';
  const defaultEvening = (userProfile && userProfile.preferences && userProfile.preferences.eveningTime) || '21:00';

  const { h: mh, m: mm } = sanitizeTime(opts.morning || defaultMorning, 'morning');
  const { h: eh, m: em } = sanitizeTime(opts.evening || defaultEvening, 'evening');

  const rawChannel = opts.channel || (userProfile && userProfile.preferences && userProfile.preferences.channel) || 'telegram';
  if (!ALLOWED_CHANNELS.has(rawChannel)) {
    console.error(`❌ 不支持的渠道：${rawChannel}。支持：${[...ALLOWED_CHANNELS].join(', ')}`);
    process.exit(1);
  }
  const channel = rawChannel;

  const morningCron = `${mm} ${mh} * * *`;
  const eveningCron = `${em} ${eh} * * *`;

  const sessionKey = `agent:main:${channel}:direct:${userId}`;

  // 早间天气 cron
  const morningConfig = {
    name: `weather-morning-${userId}`,
    cronExpr: morningCron,
    tz: 'Asia/Shanghai',
    session: 'isolated',
    sessionKey,
    channel,
    to: userId,
    announce: true,
    timeoutSeconds: 120,
    message: `node ${path.join(__dirname, 'morning-push.js')} ${userId}`
  };
  console.log(`__OPENCLAW_CRON_ADD__:${JSON.stringify(morningConfig)}`);

  // 晚间预告 cron
  const eveningConfig = {
    name: `weather-evening-${userId}`,
    cronExpr: eveningCron,
    tz: 'Asia/Shanghai',
    session: 'isolated',
    sessionKey,
    channel,
    to: userId,
    announce: true,
    timeoutSeconds: 120,
    message: `node ${path.join(__dirname, 'evening-push.js')} ${userId}`
  };
  console.log(`__OPENCLAW_CRON_ADD__:${JSON.stringify(eveningConfig)}`);

  // 周末下周天气周报 cron（每周六 20:00）
  const weeklyConfig = {
    name: `weather-weekly-${userId}`,
    cronExpr: '0 20 * * 6',
    tz: 'Asia/Shanghai',
    session: 'isolated',
    sessionKey,
    channel,
    to: userId,
    announce: true,
    timeoutSeconds: 120,
    message: `node ${path.join(__dirname, 'weekly-push.js')} ${userId}`
  };
  console.log(`__OPENCLAW_CRON_ADD__:${JSON.stringify(weeklyConfig)}`);

  // 月末下月天气概览 cron（每月 28-31 日 20:00，脚本内判断是否月末）
  const monthlyConfig = {
    name: `weather-monthly-${userId}`,
    cronExpr: '0 20 28-31 * *',
    tz: 'Asia/Shanghai',
    session: 'isolated',
    sessionKey,
    channel,
    to: userId,
    announce: true,
    timeoutSeconds: 120,
    message: `node ${path.join(__dirname, 'monthly-push.js')} ${userId}`
  };
  console.log(`__OPENCLAW_CRON_ADD__:${JSON.stringify(monthlyConfig)}`);

  const morningDisplay = `${String(mh).padStart(2,'0')}:${String(mm).padStart(2,'0')}`;
  const eveningDisplay = `${String(eh).padStart(2,'0')}:${String(em).padStart(2,'0')}`;

  // 更新用户资料中的推送设置
  const updatedProfile = userProfile ? {
    ...userProfile,
    preferences: {
      ...userProfile.preferences,
      morningTime: morningDisplay,
      eveningTime: eveningDisplay,
      channel,
      pushEnabled: true
    },
    pushEnabledAt: new Date().toISOString()
  } : {
    userId,
    preferences: {
      morningTime: morningDisplay,
      eveningTime: eveningDisplay,
      channel,
      pushEnabled: true
    },
    pushEnabledAt: new Date().toISOString()
  };

  saveUser(userId, updatedProfile);

  const city = (updatedProfile.city) || '（未设置）';

  console.log(`
✅ 天气推送已开启

🌆 城市：${city}
⏰ 早间推送：每天 ${morningDisplay}（今日天气）
🌙 晚间推送：每天 ${eveningDisplay}（明日预告）
📅 周报推送：每周六 20:00（下周天气）
🗓️ 月报推送：每月末 20:00（下月概况）
📡 渠道：${channel}

关闭推送：node push-toggle.js off ${userId}`);
}

function disablePush(userId) {
  userId = sanitizeId(userId, 'userId');
  const user = loadUser(userId);
  if (!user) {
    console.log(`❌ 未找到用户 ${userId} 的推送记录`);
    return;
  }

  console.log(`__OPENCLAW_CRON_RM__:weather-morning-${userId}`);
  console.log(`__OPENCLAW_CRON_RM__:weather-evening-${userId}`);
  console.log(`__OPENCLAW_CRON_RM__:weather-weekly-${userId}`);
  console.log(`__OPENCLAW_CRON_RM__:weather-monthly-${userId}`);

  const updated = {
    ...user,
    preferences: {
      ...user.preferences,
      pushEnabled: false
    },
    pushDisabledAt: new Date().toISOString()
  };
  saveUser(userId, updated);
  console.log(`✅ 天气推送已关闭`);
}

function showStatus(userId) {
  userId = sanitizeId(userId, 'userId');
  const user = loadUser(userId);
  if (!user) {
    console.log(`❌ 未找到用户 ${userId} 的推送记录`);
    return;
  }

  const prefs = user.preferences || {};
  const city         = user.city || '（未设置）';
  const pushEnabled  = prefs.pushEnabled || false;
  const morningTime  = prefs.morningTime || '07:00';
  const eveningTime  = prefs.eveningTime || '21:00';
  const channel      = prefs.channel || 'telegram';
  const enabledAt    = user.pushEnabledAt ? user.pushEnabledAt.split('T')[0] : '未知';

  console.log(`
📡 推送状态 — ${userId}
━━━━━━━━━━━━━━━━━━━━━━━
城市：${city}
状态：${pushEnabled ? '✅ 开启中' : '❌ 已关闭'}
早间推送：${morningTime}（今日天气）
晚间推送：${eveningTime}（明日预告）
周报推送：每周六 20:00（下周天气）
月报推送：每月末 20:00（下月概况）
渠道：${channel}
开启于：${enabledAt}
━━━━━━━━━━━━━━━━━━━━━━━`);
}

module.exports = { enablePush, disablePush, showStatus };

if (require.main !== module) return;

const args = process.argv.slice(2);
const command = args[0];
const userId  = args[1];

if (!command || !userId) {
  console.log(`用法:
  node push-toggle.js on <userId> [--morning 07:00] [--evening 21:00] [--channel telegram]
  node push-toggle.js off <userId>
  node push-toggle.js status <userId>`);
  process.exit(1);
}

const opts = {};
const mi = args.indexOf('--morning');
if (mi !== -1) opts.morning = args[mi + 1];
const ei = args.indexOf('--evening');
if (ei !== -1) opts.evening = args[ei + 1];
const ci = args.indexOf('--channel');
if (ci !== -1) opts.channel = args[ci + 1];

switch (command) {
  case 'on':     enablePush(userId, opts); break;
  case 'off':    disablePush(userId); break;
  case 'status': showStatus(userId); break;
  default:
    console.log(`❌ 未知命令: ${command}`);
    process.exit(1);
}
