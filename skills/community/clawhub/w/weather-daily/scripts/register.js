#!/usr/bin/env node
/**
 * weather-daily — user registration / city setup
 *
 * Usage:
 *   node register.js <userId> <city> [units] [morningTime] [eveningTime] [language] [timezone]
 *
 * Parameters:
 *   userId      required, letters/digits/-/_, 1-128 chars
 *   city        required, 1-50 chars, supports Chinese/English/digits/spaces/hyphens
 *   units       optional, metric (default) or imperial
 *   morningTime optional, HH:MM format (default 07:00)
 *   eveningTime optional, HH:MM format (default 21:00)
 *   language    optional, zh or en (auto-detected from city name if omitted)
 *   timezone    optional, IANA timezone (e.g. America/New_York; default: Asia/Shanghai for zh, UTC for en)
 *
 * Examples:
 *   node register.js alice 上海
 *   node register.js bob "New York" imperial 08:00 22:00 en America/New_York
 *   node register.js carol London metric 07:00 21:00 en Europe/London
 */

const fs = require('fs');
const path = require('path');

const USERS_DIR = path.join(__dirname, '../data/users');

function sanitizeId(value) {
  if (typeof value !== 'string' || !/^[a-zA-Z0-9_-]{1,128}$/.test(value)) {
    console.error('❌ Invalid userId: only letters, digits, - and _ are allowed (1-128 chars)');
    process.exit(1);
  }
  return value;
}

function sanitizeCity(value) {
  if (typeof value !== 'string') {
    console.error('❌ Invalid city name');
    process.exit(1);
  }
  const stripped = value.replace(/[^\u4e00-\u9fa5a-zA-Z0-9\s\-]/g, '').trim();
  if (!/^[\u4e00-\u9fa5a-zA-Z0-9\s\-]{1,50}$/.test(stripped)) {
    console.error('❌ Invalid city name: use Chinese/English/digits/spaces/hyphens, length 1-50');
    process.exit(1);
  }
  return stripped;
}

function sanitizeUnits(value) {
  if (value !== 'metric' && value !== 'imperial') {
    console.error('❌ Invalid units: use metric or imperial');
    process.exit(1);
  }
  return value;
}

function sanitizeTime(value, label) {
  if (typeof value !== 'string' || !/^\d{1,2}:\d{2}$/.test(value)) {
    console.error(`❌ Invalid ${label}: format should be HH:MM, e.g. 07:00`);
    process.exit(1);
  }
  const [h, m] = value.split(':').map(Number);
  if (h < 0 || h > 23 || m < 0 || m > 59) {
    console.error(`❌ Invalid ${label}: hour 0-23, minute 0-59`);
    process.exit(1);
  }
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
}

function sanitizeLanguage(value) {
  if (value !== 'zh' && value !== 'en') {
    console.error('❌ Invalid language: use zh or en');
    process.exit(1);
  }
  return value;
}

// Simple IANA timezone format check (not exhaustive, prevents injection)
function sanitizeTimezone(value) {
  if (typeof value !== 'string' || !/^[A-Za-z][A-Za-z0-9_+\-\/]{0,49}$/.test(value)) {
    console.error('❌ Invalid timezone: use IANA format, e.g. America/New_York');
    process.exit(1);
  }
  return value;
}

function safeUserPath(userId) {
  const resolved = path.resolve(USERS_DIR, `${userId}.json`);
  if (!resolved.startsWith(path.resolve(USERS_DIR) + path.sep)) {
    console.error('❌ Illegal path');
    process.exit(1);
  }
  return resolved;
}

// Auto-detect language from city name: Chinese chars → zh, else → en
function detectLanguage(city) {
  return /[\u4e00-\u9fa5]/.test(city) ? 'zh' : 'en';
}

// --- Main ---
const args = process.argv.slice(2);

if (args.length < 2) {
  console.log(`Usage:
  node register.js <userId> <city> [units] [morningTime] [eveningTime] [language] [timezone]

Parameters:
  userId      letters/digits/-/_, 1-128 chars
  city        city name, supports Chinese/English (e.g. 上海, Beijing, New York)
  units       metric (default, °C) or imperial (°F)
  morningTime HH:MM format, morning push time (default 07:00)
  eveningTime HH:MM format, evening push time (default 21:00)
  language    zh or en (auto-detected from city name if omitted)
  timezone    IANA timezone (default: Asia/Shanghai for zh, UTC for en)

Examples:
  node register.js alice 上海
  node register.js bob "New York" imperial 08:00 22:00 en America/New_York
  node register.js carol London metric 07:00 21:00 en Europe/London`);
  process.exit(1);
}

const userId      = sanitizeId(args[0]);
const city        = sanitizeCity(args[1]);
const units       = sanitizeUnits(args[2] || 'metric');
const morningTime = sanitizeTime(args[3] || '07:00', 'morningTime');
const eveningTime = sanitizeTime(args[4] || '21:00', 'eveningTime');
const language    = args[5] ? sanitizeLanguage(args[5]) : detectLanguage(city);
const defaultTz   = language === 'zh' ? 'Asia/Shanghai' : 'UTC';
const timezone    = args[6] ? sanitizeTimezone(args[6]) : defaultTz;

fs.mkdirSync(USERS_DIR, { recursive: true });

const filePath = safeUserPath(userId);
const now = new Date().toISOString();

let createdAt = now;
if (fs.existsSync(filePath)) {
  try {
    const existing = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    if (existing.createdAt) createdAt = existing.createdAt;
  } catch (_) {}
}

const profile = {
  userId,
  city,
  units,
  language,
  preferences: {
    morningTime,
    eveningTime,
    timezone,
    channel: 'telegram',
    pushEnabled: false,
    alerts: {
      rain: true,
      snow: true,
      wind: true,
      extreme: true,
      airQuality: true
    }
  },
  createdAt,
  updatedAt: now
};

fs.writeFileSync(filePath, JSON.stringify(profile, null, 2), 'utf8');

const unitLabel = units === 'metric' ? '°C / metric' : '°F / imperial';

if (language === 'zh') {
  console.log(`
✅ 用户注册成功

👤 用户：${userId}
🌆 城市：${city}
🌡️ 单位：${unitLabel}
🌐 语言：中文
⏰ 早间推送：${morningTime}（今日天气）
🌙 晚间推送：${eveningTime}（明日预告）
🕐 时区：${timezone}

下一步：
  开启每日推送：node scripts/push-toggle.js on ${userId}
  查看今日天气：node scripts/morning-push.js ${userId}
  查看一周预报：node scripts/forecast.js ${userId}
  修改城市设置：node scripts/register.js ${userId} <新城市>`);
} else {
  console.log(`
✅ Registration successful

👤 User: ${userId}
🌆 City: ${city}
🌡️ Units: ${unitLabel}
🌐 Language: English
⏰ Morning push: ${morningTime} (today's weather)
🌙 Evening push: ${eveningTime} (tomorrow's preview)
🕐 Timezone: ${timezone}

Next steps:
  Enable daily push: node scripts/push-toggle.js on ${userId}
  Today's weather:   node scripts/morning-push.js ${userId}
  Weekly forecast:   node scripts/forecast.js ${userId}
  Change city:       node scripts/register.js ${userId} <new-city>`);
}
