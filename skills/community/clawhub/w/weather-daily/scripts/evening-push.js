#!/usr/bin/env node
/**
 * weather-daily — evening weather push prompt generator (tomorrow preview)
 * Driven by openclaw cron; output is fulfilled by Claude via WebSearch
 *
 * Usage:
 *   node evening-push.js <userId>
 */

const fs = require('fs');
const path = require('path');

const USERS_DIR = path.join(__dirname, '../data/users');

function sanitizeId(value) {
  if (typeof value !== 'string' || !/^[a-zA-Z0-9_-]{1,128}$/.test(value)) {
    console.error('❌ Invalid userId');
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

function loadUser(userId) {
  const f = safeUserPath(userId);
  if (!fs.existsSync(f)) {
    console.error(`❌ User ${userId} not found. Run: node register.js ${userId} <city>`);
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(f, 'utf8'));
}

const args = process.argv.slice(2);
if (!args[0]) {
  console.error('Usage: node evening-push.js <userId>');
  process.exit(1);
}

const userId = sanitizeId(args[0]);
const user   = loadUser(userId);

const city  = user.city  || '上海';
const units = user.units || 'metric';
const unit  = units === 'metric' ? '°C' : '°F';
const lang  = user.language || ((/[\u4e00-\u9fa5]/.test(city)) ? 'zh' : 'en');

const now = new Date();
const tomorrow = new Date(now);
tomorrow.setDate(tomorrow.getDate() + 1);

const tmYear  = tomorrow.getFullYear();
const tmMonth = tomorrow.getMonth() + 1;
const tmDay   = tomorrow.getDate();
const tomorrowISO = `${tmYear}-${String(tmMonth).padStart(2,'0')}-${String(tmDay).padStart(2,'0')}`;

if (lang === 'zh') {
  const WEEKDAYS_ZH = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
  const todayDisplay    = `${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日 ${WEEKDAYS_ZH[now.getDay()]}`;
  const tomorrowDisplay = `${tmYear}年${tmMonth}月${tmDay}日 ${WEEKDAYS_ZH[tomorrow.getDay()]}`;

  console.log(`请为用户查询 ${city} 明天（${tomorrowDisplay}）的天气预报，并按以下格式推送晚间天气预告。

搜索步骤：
1. 搜索「${city} 明天天气 ${tomorrowISO}」
2. 搜索「${city} 未来天气 是否有极端天气」

输出格式：
🌙 ${city} 明日天气预告 · ${todayDisplay}晚间
━━━━━━━━━━━━━━━━━━━━━━━
📅 明天 ${tomorrowDisplay}

🌡️ 预计温度：低温X${unit} ~ 高温X${unit}
☁️ 天气：[天气状况]
💧 湿度：X%  🌬️ 风力：X级

⏰ 明日提醒
[根据天气提供出行/穿衣/携带雨伞等具体建议]

⚠️ 重要预警：[如有极端天气则高亮提示，无则省略]

🗓️ 后天预览：[一句话说明后天大致天气]

💡 回复"本周预报"查看7天天气`);
} else {
  const WEEKDAYS_EN = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const MONTHS_EN = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  const todayDisplay    = `${WEEKDAYS_EN[now.getDay()]}, ${MONTHS_EN[now.getMonth()]} ${now.getDate()}, ${now.getFullYear()}`;
  const tomorrowDisplay = `${WEEKDAYS_EN[tomorrow.getDay()]}, ${MONTHS_EN[tomorrow.getMonth()]} ${tmDay}, ${tmYear}`;

  console.log(`Please search for tomorrow's weather in ${city} (${tomorrowDisplay}) and send the evening preview in the following format.

Search steps:
1. Search "${city} weather tomorrow ${tomorrowISO}"
2. Search "${city} weather outlook extreme weather warning"

Output format:
🌙 ${city} Tomorrow's Weather Preview · ${todayDisplay} Evening
━━━━━━━━━━━━━━━━━━━━━━━
📅 Tomorrow: ${tomorrowDisplay}

🌡️ Temperature: Low X${unit} ~ High X${unit}
☁️ Conditions: [weather description]
💧 Humidity: X%  🌬️ Wind: [speed & direction]

⏰ Tomorrow's reminders
[Specific commute / outfit / umbrella advice based on the forecast]

⚠️ Weather alert: [highlight any extreme weather warnings; omit if none]

🗓️ Day after tomorrow: [one-line outlook]

💡 Reply "forecast" for the 7-day outlook`);
}
