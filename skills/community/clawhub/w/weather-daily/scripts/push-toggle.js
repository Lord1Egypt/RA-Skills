#!/usr/bin/env node
/**
 * weather-daily — 推送开关（无文件写入版）
 *
 * 用户资料存于原生 MEMORY.md，由 Agent 维护；本脚本不读写任何文件。
 * 开启推送所需的城市/单位/语言/时区由 Agent 从 MEMORY.md 读出后作为参数传入，
 * 并被烘焙进各条 cron 任务的推送命令中，使无头推送无需读取任何文件。
 * cron 任务通过 openclaw 运行时协议（__OPENCLAW_CRON_ADD__ / __OPENCLAW_CRON_RM__）管理。
 *
 * 用法:
 *   node push-toggle.js on <userId> --city <城市> [--units metric|imperial] [--lang zh|en] \
 *        [--morning 07:00] [--evening 21:00] [--channel telegram] [--timezone Asia/Shanghai]
 *   node push-toggle.js off <userId>
 *   node push-toggle.js status <userId>
 */

const path = require('path');

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

function sanitizeCity(value) {
  if (typeof value !== 'string') {
    console.error('❌ 无效的城市名');
    process.exit(1);
  }
  const stripped = value.replace(/[^一-龥a-zA-Z0-9\s\-]/g, '').trim();
  if (!/^[一-龥a-zA-Z0-9\s\-]{1,50}$/.test(stripped)) {
    console.error('❌ 无效的城市名：使用中文/英文/数字/空格/连字符，长度 1-50');
    process.exit(1);
  }
  return stripped;
}

function sanitizeUnits(value) {
  if (value !== 'metric' && value !== 'imperial') {
    console.error('❌ 无效的 units：使用 metric 或 imperial');
    process.exit(1);
  }
  return value;
}

function sanitizeLang(value) {
  if (value !== 'zh' && value !== 'en') {
    console.error('❌ 无效的 lang：使用 zh 或 en');
    process.exit(1);
  }
  return value;
}

function sanitizeTimezone(value) {
  if (typeof value !== 'string' || !/^[A-Za-z][A-Za-z0-9_+\-\/]{0,49}$/.test(value)) {
    console.error('❌ 无效的 timezone：使用 IANA 格式，如 America/New_York');
    process.exit(1);
  }
  return value;
}

const ALLOWED_CHANNELS = new Set(['telegram', 'feishu', 'slack', 'discord']);

// 把资料字段烘焙进推送命令，使无头推送脚本无需读取任何文件
function pushCommand(script, userId, city, units, lang) {
  const scriptPath = path.join(__dirname, script);
  return `node ${scriptPath} ${userId} --city "${city}" --units ${units} --lang ${lang}`;
}

function enablePush(userId, opts = {}) {
  userId = sanitizeId(userId, 'userId');

  if (!opts.city) {
    console.error('❌ 缺少 --city 参数。请先让 Agent 从 MEMORY.md 读取资料（城市/单位/语言），或运行 register.js 生成。');
    process.exit(1);
  }
  const city  = sanitizeCity(opts.city);
  const units = sanitizeUnits(opts.units || 'metric');
  const lang  = opts.lang ? sanitizeLang(opts.lang) : (/[一-龥]/.test(city) ? 'zh' : 'en');
  const timezone = opts.timezone ? sanitizeTimezone(opts.timezone) : 'Asia/Shanghai';

  const { h: mh, m: mm } = sanitizeTime(opts.morning || '07:00', 'morning');
  const { h: eh, m: em } = sanitizeTime(opts.evening || '21:00', 'evening');

  const rawChannel = opts.channel || 'telegram';
  if (!ALLOWED_CHANNELS.has(rawChannel)) {
    console.error(`❌ 不支持的渠道：${rawChannel}。支持：${[...ALLOWED_CHANNELS].join(', ')}`);
    process.exit(1);
  }
  const channel = rawChannel;

  const morningCron = `${mm} ${mh} * * *`;
  const eveningCron = `${em} ${eh} * * *`;

  const sessionKey = `agent:main:${channel}:direct:${userId}`;

  // 早间天气 cron（城市/单位/语言已烘焙进命令）
  const morningConfig = {
    name: `weather-morning-${userId}`,
    cronExpr: morningCron,
    tz: timezone,
    session: 'isolated',
    sessionKey,
    channel,
    to: userId,
    announce: true,
    timeoutSeconds: 120,
    message: pushCommand('morning-push.js', userId, city, units, lang)
  };
  console.log(`__OPENCLAW_CRON_ADD__:${JSON.stringify(morningConfig)}`);

  // 晚间预告 cron
  const eveningConfig = {
    name: `weather-evening-${userId}`,
    cronExpr: eveningCron,
    tz: timezone,
    session: 'isolated',
    sessionKey,
    channel,
    to: userId,
    announce: true,
    timeoutSeconds: 120,
    message: pushCommand('evening-push.js', userId, city, units, lang)
  };
  console.log(`__OPENCLAW_CRON_ADD__:${JSON.stringify(eveningConfig)}`);

  // 周末下周天气周报 cron（每周六 20:00）
  const weeklyConfig = {
    name: `weather-weekly-${userId}`,
    cronExpr: '0 20 * * 6',
    tz: timezone,
    session: 'isolated',
    sessionKey,
    channel,
    to: userId,
    announce: true,
    timeoutSeconds: 120,
    message: pushCommand('weekly-push.js', userId, city, units, lang)
  };
  console.log(`__OPENCLAW_CRON_ADD__:${JSON.stringify(weeklyConfig)}`);

  // 月末下月天气概览 cron（每月 28-31 日 20:00，脚本内判断是否月末）
  const monthlyConfig = {
    name: `weather-monthly-${userId}`,
    cronExpr: '0 20 28-31 * *',
    tz: timezone,
    session: 'isolated',
    sessionKey,
    channel,
    to: userId,
    announce: true,
    timeoutSeconds: 120,
    message: pushCommand('monthly-push.js', userId, city, units, lang)
  };
  console.log(`__OPENCLAW_CRON_ADD__:${JSON.stringify(monthlyConfig)}`);

  const morningDisplay = `${String(mh).padStart(2,'0')}:${String(mm).padStart(2,'0')}`;
  const eveningDisplay = `${String(eh).padStart(2,'0')}:${String(em).padStart(2,'0')}`;

  console.log(`
✅ 天气推送已开启

🌆 城市：${city}
🌡️ 单位：${units === 'metric' ? '°C / metric' : '°F / imperial'}
🌐 语言：${lang}
⏰ 早间推送：每天 ${morningDisplay}（今日天气）
🌙 晚间推送：每天 ${eveningDisplay}（明日预告）
📅 周报推送：每周六 20:00（下周天气）
🗓️ 月报推送：每月末 20:00（下月概况）
📡 渠道：${channel}
🕐 时区：${timezone}

💡 请在 MEMORY.md 的资料区块记下：推送已开启（${channel}，${morningDisplay}/${eveningDisplay}）。
关闭推送：node scripts/push-toggle.js off ${userId}`);
}

function disablePush(userId) {
  userId = sanitizeId(userId, 'userId');
  // cron 名称可由 userId 推导，无需读取任何文件
  console.log(`__OPENCLAW_CRON_RM__:weather-morning-${userId}`);
  console.log(`__OPENCLAW_CRON_RM__:weather-evening-${userId}`);
  console.log(`__OPENCLAW_CRON_RM__:weather-weekly-${userId}`);
  console.log(`__OPENCLAW_CRON_RM__:weather-monthly-${userId}`);
  console.log(`
✅ 天气推送已关闭（已请求删除 ${userId} 的早/晚/周/月定时任务）
💡 请在 MEMORY.md 的资料区块记下：推送已关闭。`);
}

function showStatus(userId) {
  userId = sanitizeId(userId, 'userId');
  console.log(`
🔔 推送状态由 MEMORY.md 资料记录 —— 请读取 MEMORY.md 中 <!-- weather-daily:profile:${userId} --> 区块查看开启/时间/渠道。
   如需重新开启：node scripts/push-toggle.js on ${userId} --city <城市> --units <metric|imperial> --lang <zh|en>`);
}

module.exports = { enablePush, disablePush, showStatus };

if (require.main !== module) return;

const args = process.argv.slice(2);
const command = args[0];
const userId  = args[1];

function flag(name) {
  const i = args.indexOf(name);
  return (i !== -1 && args[i + 1]) ? args[i + 1] : undefined;
}

if (!command || !userId) {
  console.log(`用法:
  node push-toggle.js on <userId> --city <城市> [--units metric|imperial] [--lang zh|en] \\
       [--morning 07:00] [--evening 21:00] [--channel telegram] [--timezone Asia/Shanghai]
  node push-toggle.js off <userId>
  node push-toggle.js status <userId>

说明:
  资料存于原生 MEMORY.md，由 Agent 维护并在开启推送时把城市/单位/语言作为参数传入。
  这些字段会被烘焙进定时任务命令，使无头推送无需读取任何文件。`);
  process.exit(1);
}

const opts = {
  city: flag('--city'),
  units: flag('--units'),
  lang: flag('--lang'),
  morning: flag('--morning'),
  evening: flag('--evening'),
  channel: flag('--channel'),
  timezone: flag('--timezone'),
};

switch (command) {
  case 'on':     enablePush(userId, opts); break;
  case 'off':    disablePush(userId); break;
  case 'status': showStatus(userId); break;
  default:
    console.log(`❌ 未知命令: ${command}`);
    process.exit(1);
}
