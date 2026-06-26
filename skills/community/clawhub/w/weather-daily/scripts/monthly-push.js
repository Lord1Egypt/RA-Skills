#!/usr/bin/env node
/**
 * weather-daily — next-month weather overview prompt generator (sent at month end)
 * Runs on 28–31 of each month; script checks internally whether today is the last day.
 *
 * Usage:
 *   node monthly-push.js <userId>
 *   node monthly-push.js <userId> --force   # skip last-day check
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

function isLastDayOfMonth(date) {
  const tomorrow = new Date(date);
  tomorrow.setDate(date.getDate() + 1);
  return tomorrow.getDate() === 1;
}

const args = process.argv.slice(2);
if (!args[0]) {
  console.error('Usage: node monthly-push.js <userId> [--force]');
  process.exit(1);
}

const userId = sanitizeId(args[0]);
const force  = args.includes('--force');
const now    = new Date();

if (!force && !isLastDayOfMonth(now)) {
  process.exit(0);
}

const user = loadUser(userId);

const city  = user.city  || '上海';
const units = user.units || 'metric';
const unit  = units === 'metric' ? 'C' : 'F';
const lang  = user.language || ((/[\u4e00-\u9fa5]/.test(city)) ? 'zh' : 'en');

const nextMonth = new Date(now.getFullYear(), now.getMonth() + 1, 1);
const nextYear  = nextMonth.getFullYear();
const nextMon   = nextMonth.getMonth() + 1;

if (lang === 'zh') {
  const SEASON = ['冬季','冬季','春季','春季','春季','夏季','夏季','夏季','秋季','秋季','秋季','冬季'];
  const season = SEASON[nextMon - 1];

  console.log(`请为用户查询 ${city} ${nextYear}年${nextMon}月的天气概况，并按以下格式推送月度天气预报。

搜索步骤：
1. 搜索「${city} ${nextYear}年${nextMon}月天气预报」
2. 搜索「${city} ${nextMon}月气候特点」
3. 搜索「${city} ${nextMon}月份${season}注意事项」

输出格式：
🗓️ ${city} ${nextYear}年${nextMon}月天气月报
━━━━━━━━━━━━━━━━━━━━━━━
📊 气温概况
  · 平均气温：X°${unit}（历史同期：X°${unit}）
  · 最高气温：X°${unit}  最低气温：X°${unit}
  · 温差提示：[早晚温差说明]

🌧️ 降水情况
  · 降雨概率：X%
  · 主要降水时段：[上/中/下旬]
  · 是否有梅雨/台风/干旱等气候特征

💨 主要天气特征
  [本月主要天气类型及成因，3-5句]

📅 分旬预测
  🔹 上旬（1-10日）：[天气趋势]
  🔹 中旬（11-20日）：[天气趋势]
  🔹 下旬（21日-月末）：[天气趋势]

⚠️ 本月预警
  [本月可能出现的极端天气或气候风险，无则省略]

👔 穿衣指南
  [本月整体穿衣建议，按上中下旬温度变化说明]

🌿 生活建议
  [本月养生、出行、运动等实用建议，2-3条]

💡 回复"本周天气"获取详细一周预报`);
} else {
  const MONTHS_EN = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  const SEASON_EN = ['Winter','Winter','Spring','Spring','Spring','Summer','Summer','Summer','Autumn','Autumn','Autumn','Winter'];
  const monthName = MONTHS_EN[nextMon - 1];
  const season    = SEASON_EN[nextMon - 1];

  console.log(`Please search for the weather overview for ${city} in ${monthName} ${nextYear} and send the monthly weather report in the following format.

Search steps:
1. Search "${city} weather forecast ${monthName} ${nextYear}"
2. Search "${city} ${monthName} climate"
3. Search "${city} ${season} ${monthName} weather tips"

Output format:
🗓️ ${city} ${monthName} ${nextYear} Weather Monthly Report
━━━━━━━━━━━━━━━━━━━━━━━
📊 Temperature Overview
  · Average temperature: X°${unit} (historical average: X°${unit})
  · High: X°${unit}  Low: X°${unit}
  · Day-night swing: [notes on temperature range]

🌧️ Precipitation
  · Rain probability: X%
  · Main rainy periods: [early / mid / late month]
  · Notable climate patterns: [e.g. monsoon, drought, snow season]

💨 Weather Characteristics
  [3–5 sentences on dominant weather types and causes this month]

📅 10-Day Periods
  🔹 Early month (1–10): [trend]
  🔹 Mid month (11–20): [trend]
  🔹 Late month (21–end): [trend]

⚠️ Monthly alerts
  [Potential extreme weather or climate risks; omit if none]

👔 What to wear
  [General outfit guidance across the month's temperature changes]

🌿 Lifestyle tips
  [2–3 practical tips for health, travel, or outdoor activities]

💡 Reply "forecast" for the detailed 7-day outlook`);
}
