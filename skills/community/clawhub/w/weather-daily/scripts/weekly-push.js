#!/usr/bin/env node
/**
 * weather-daily — next-week forecast prompt generator (sent every weekend)
 * Output is fulfilled by Claude via WebSearch
 *
 * Usage:
 *   node weekly-push.js <userId>
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
  console.error('Usage: node weekly-push.js <userId>');
  process.exit(1);
}

const userId = sanitizeId(args[0]);
const user   = loadUser(userId);

const city  = user.city  || '上海';
const units = user.units || 'metric';
const unit  = units === 'metric' ? 'C' : 'F';
const lang  = user.language || ((/[\u4e00-\u9fa5]/.test(city)) ? 'zh' : 'en');

const now = new Date();
// Next Monday
const dayOfWeek = now.getDay();
const daysUntilMonday = dayOfWeek === 0 ? 1 : 8 - dayOfWeek;
const nextMonday = new Date(now);
nextMonday.setDate(now.getDate() + daysUntilMonday);
const nextSunday = new Date(nextMonday);
nextSunday.setDate(nextMonday.getDate() + 6);

const year = now.getFullYear();

if (lang === 'zh') {
  const MONTHS = ['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月'];
  const fmtZh = d => `${d.getMonth()+1}月${d.getDate()}日`;
  const weekRange = `${fmtZh(nextMonday)}～${fmtZh(nextSunday)}`;

  console.log(`请为用户查询 ${city} 下周（${weekRange}）的天气预报，并按以下格式推送周报。

搜索步骤：
1. 搜索「${city} 下周天气预报」
2. 搜索「${city} ${year}年${nextMonday.getMonth()+1}月天气」

输出格式：
📅 ${city} 下周天气周报 · ${weekRange}
━━━━━━━━━━━━━━━━━━━━━━━

[每天一行，周一到周日]
{星期}（{日期}）  {天气图标} {天气}  🌡️{低温}~{高温}°${unit}  {简短提示}

━━━━━━━━━━━━━━━━━━━━━━━
📌 下周天气趋势：[整体天气变化，2-3句]
⚠️ 重要预警：[下周内极端天气，无则省略]
☂️ 本周备雨建议：[哪几天需要带伞]
👔 穿衣趋势：[温差变化与穿衣建议]
📅 最佳出行日：[下周最适合户外活动的1-2天]

💡 回复"今天天气"获取今日实况`);
} else {
  const WEEKDAYS_EN = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const MONTHS_EN   = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  const fmtEn = d => `${MONTHS_EN[d.getMonth()]} ${d.getDate()}`;
  const weekRange = `${fmtEn(nextMonday)} – ${fmtEn(nextSunday)}`;

  console.log(`Please search for next week's weather forecast for ${city} (${weekRange}) and send the weekly report in the following format.

Search steps:
1. Search "${city} next week weather forecast"
2. Search "${city} ${MONTHS_EN[nextMonday.getMonth()]} ${year} weather"

Output format:
📅 ${city} Next Week Weather · ${weekRange}
━━━━━━━━━━━━━━━━━━━━━━━

[One line per day, Monday to Sunday]
{Day} ({Date})  {icon} {conditions}  🌡️{low}~{high}°${unit}  {brief tip}

━━━━━━━━━━━━━━━━━━━━━━━
📌 Weekly trend: [2–3 sentences on overall pattern]
⚠️ Alerts: [any extreme weather warnings; omit if none]
☂️ Umbrella days: [which days to carry an umbrella]
👔 What to wear: [temperature swings and outfit advice]
📅 Best day out: [1–2 best days for outdoor activities]

💡 Reply "today's weather" for today's detailed report`);
}
