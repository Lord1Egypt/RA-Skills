#!/usr/bin/env node
/**
 * weather-daily — user registration / city setup (no filesystem writes)
 *
 * The profile lives in the agent's native MEMORY.md, not on disk. This script
 * only validates input and prints a `<!-- weather-daily:profile:<userId> -->`
 * markdown block for the agent to store in MEMORY.md, plus a push-toggle hint.
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
  const stripped = value.replace(/[^一-龥a-zA-Z0-9\s\-]/g, '').trim();
  if (!/^[一-龥a-zA-Z0-9\s\-]{1,50}$/.test(stripped)) {
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

// Auto-detect language from city name: Chinese chars → zh, else → en
function detectLanguage(city) {
  return /[一-龥]/.test(city) ? 'zh' : 'en';
}

/**
 * Render the profile as a MEMORY.md block (agent stores it in native memory;
 * this script never writes to disk).
 */
function renderMemoryBlock(profile) {
  const unitLabel = profile.units === 'metric' ? '°C / metric' : '°F / imperial';
  const langLabel = profile.language === 'zh' ? '中文 (zh)' : 'English (en)';
  return `<!-- weather-daily:profile:${profile.userId} -->
## Weather profile · ${profile.userId}
- userId: ${profile.userId}
- city: ${profile.city}
- units: ${unitLabel}
- language: ${langLabel}
- morningTime: ${profile.morningTime}
- eveningTime: ${profile.eveningTime}
- timezone: ${profile.timezone}
- push: disabled (run push-toggle.js on to enable)
<!-- /weather-daily:profile -->`;
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

const profile = { userId, city, units, language, morningTime, eveningTime, timezone };

const unitLabel = units === 'metric' ? '°C / metric' : '°F / imperial';

if (language === 'zh') {
  console.log(`
✅ 用户资料已生成（未写入磁盘，请存入 MEMORY.md）

👤 用户：${userId}
🌆 城市：${city}
🌡️ 单位：${unitLabel}
🌐 语言：中文
⏰ 早间推送：${morningTime}（今日天气）
🌙 晚间推送：${eveningTime}（明日预告）
🕐 时区：${timezone}

📇 请将以下档案写入 MEMORY.md（原生记忆，跨会话保留）：
\`\`\`markdown
${renderMemoryBlock(profile)}
\`\`\`

下一步：
  开启每日推送（把上面的城市/单位作为参数传入）：
    node scripts/push-toggle.js on ${userId} --city "${city}" --units ${units} --lang ${language} \\
      --morning ${morningTime} --evening ${eveningTime} --timezone ${timezone} --channel telegram
  查看今日天气：node scripts/morning-push.js ${userId} --city "${city}" --units ${units} --lang ${language}
  查看一周预报：node scripts/forecast.js ${userId} --city "${city}" --units ${units} --lang ${language}`);
} else {
  console.log(`
✅ Profile generated (NOT written to disk — store it in MEMORY.md)

👤 User: ${userId}
🌆 City: ${city}
🌡️ Units: ${unitLabel}
🌐 Language: English
⏰ Morning push: ${morningTime} (today's weather)
🌙 Evening push: ${eveningTime} (tomorrow's preview)
🕐 Timezone: ${timezone}

📇 Store this block in MEMORY.md (native memory, persists across sessions):
\`\`\`markdown
${renderMemoryBlock(profile)}
\`\`\`

Next steps:
  Enable daily push (pass city/units read back from MEMORY.md):
    node scripts/push-toggle.js on ${userId} --city "${city}" --units ${units} --lang ${language} \\
      --morning ${morningTime} --evening ${eveningTime} --timezone ${timezone} --channel telegram
  Today's weather:  node scripts/morning-push.js ${userId} --city "${city}" --units ${units} --lang ${language}
  Weekly forecast:  node scripts/forecast.js ${userId} --city "${city}" --units ${units} --lang ${language}`);
}

module.exports = { renderMemoryBlock };
