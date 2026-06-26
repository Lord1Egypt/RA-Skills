#!/usr/bin/env node
/**
 * weather-daily — morning weather push prompt generator
 * Driven by openclaw cron; output is fulfilled by Claude via WebSearch
 *
 * Usage:
 *   node morning-push.js <userId>
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
  console.error('Usage: node morning-push.js <userId>');
  process.exit(1);
}

const userId = sanitizeId(args[0]);
const user   = loadUser(userId);

const city  = user.city  || '上海';
const units = user.units || 'metric';
const unit  = units === 'metric' ? '°C' : '°F';
const lang  = user.language || ((/[\u4e00-\u9fa5]/.test(city)) ? 'zh' : 'en');

const now = new Date();
const year  = now.getFullYear();
const month = now.getMonth() + 1;
const day   = now.getDate();
const dateISO = `${year}-${String(month).padStart(2,'0')}-${String(day).padStart(2,'0')}`;

if (lang === 'zh') {
  const WEEKDAYS_ZH = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
  const weekday = WEEKDAYS_ZH[now.getDay()];
  const dateDisplay = `${year}年${month}月${day}日 ${weekday}`;

  console.log(`请为用户查询 ${city} 今天（${dateDisplay}）的天气，并按以下格式推送早间天气报告。

搜索步骤：
1. 搜索「${city} 今天天气 ${dateISO}」
2. 搜索「${city} 今日空气质量」
3. 如有极端天气预警，搜索「${city} 天气预警」

输出格式：
🌤️ ${city} 早间天气 · ${dateDisplay}
━━━━━━━━━━━━━━━━━━━━━━━
🌡️ 温度：低温X${unit} ~ 高温X${unit}
☁️ 天气：[天气状况]
💧 湿度：X%  🌬️ 风力：X级（风向）
🌅 日出：XX:XX  🌇 日落：XX:XX

📊 分时预报
🌅 早晨(6-9点)：[温度+状况]
☀️ 上午(9-12点)：[温度+状况]
🌤️ 下午(12-18点)：[温度+状况]
🌙 夜间(18-24点)：[温度+状况]

🌍 空气质量：AQI X（[等级]）[提示]

🎽 穿衣建议：[根据温度给出具体建议]
🚗 出行建议：[根据天气给出出行提示]

⚠️ 今日提醒：[重要天气注意事项，无则省略]

💡 查看本周预报：回复"天气预报"`);
} else {
  const WEEKDAYS_EN = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const MONTHS_EN = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  const weekday = WEEKDAYS_EN[now.getDay()];
  const dateDisplay = `${weekday}, ${MONTHS_EN[now.getMonth()]} ${day}, ${year}`;

  console.log(`Please search for today's weather in ${city} (${dateDisplay}) and send the morning weather report in the following format.

Search steps:
1. Search "${city} weather today ${dateISO}"
2. Search "${city} air quality today"
3. If extreme weather is possible, search "${city} weather warning"

Output format:
🌤️ ${city} Morning Weather · ${dateDisplay}
━━━━━━━━━━━━━━━━━━━━━━━
🌡️ Temperature: Low X${unit} ~ High X${unit}
☁️ Conditions: [weather description]
💧 Humidity: X%  🌬️ Wind: [speed & direction]
🌅 Sunrise: XX:XX  🌇 Sunset: XX:XX

📊 Hourly Forecast
🌅 Morning (6–9 AM): [temp + conditions]
☀️ Late Morning (9 AM–12 PM): [temp + conditions]
🌤️ Afternoon (12–6 PM): [temp + conditions]
🌙 Evening (6 PM–midnight): [temp + conditions]

🌍 Air Quality: AQI X ([level]) [note]

🎽 What to wear: [outfit suggestion based on temperature]
🚗 Commute tip: [travel advice based on conditions]

⚠️ Today's alert: [important weather warnings, omit if none]

💡 Reply "forecast" for the weekly outlook`);
}
