#!/usr/bin/env node
/**
 * weather-daily — 7-day forecast prompt generator
 * Output is fulfilled by Claude via WebSearch
 *
 * Profile fields (city/units/language) are passed as CLI flags by the agent
 * from MEMORY.md. This script performs NO filesystem reads or writes.
 *
 * Usage:
 *   node forecast.js <userId> [--city <city>] [--units metric|imperial] [--lang zh|en]
 */

function sanitizeId(value) {
  if (typeof value !== 'string' || !/^[a-zA-Z0-9_-]{1,128}$/.test(value)) {
    console.error('❌ Invalid userId');
    process.exit(1);
  }
  return value;
}

function flag(args, name) {
  const i = args.indexOf(name);
  return (i !== -1 && args[i + 1]) ? args[i + 1] : undefined;
}

const args = process.argv.slice(2);
if (!args[0]) {
  console.error('Usage: node forecast.js <userId> [--city <city>] [--units metric|imperial] [--lang zh|en]');
  process.exit(1);
}

const userId = sanitizeId(args[0]);
const city  = flag(args, '--city')  || '上海';
const units = flag(args, '--units') || 'metric';
const unit  = units === 'metric' ? 'C' : 'F';
const lang  = flag(args, '--lang')  || ((/[一-龥]/.test(city)) ? 'zh' : 'en');

const now = new Date();
const year  = now.getFullYear();
const month = now.getMonth() + 1;
const day   = now.getDate();

if (lang === 'zh') {
  const WEEKDAYS_ZH = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
  const todayDisplay = `${year}年${month}月${day}日（${WEEKDAYS_ZH[now.getDay()]}）`;

  console.log(`请为用户查询 ${city} 未来7天的天气预报（从 ${todayDisplay} 起），并按以下格式输出。

搜索步骤：
1. 搜索「${city} 未来7天天气预报」
2. 搜索「${city} 本周天气」

输出格式：
📅 ${city} 一周天气预报
━━━━━━━━━━━━━━━━━━━━━━━
从 ${todayDisplay} 起，未来7天：

[每天一行]
{星期} {日期}  {天气图标} {天气}  🌡️{低温}~{高温}°${unit}  💧{湿度}%  🌬️{风力}

━━━━━━━━━━━━━━━━━━━━━━━
📌 本周趋势：[整体天气趋势描述，2-3句]
⚠️ 重要提醒：[本周内任何极端天气预警]
👔 本周穿衣趋势：[整体穿衣建议]

💡 回复"今天天气"获取今日详细天气`);
} else {
  const WEEKDAYS_EN = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const MONTHS_EN = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  const todayDisplay = `${WEEKDAYS_EN[now.getDay()]}, ${MONTHS_EN[now.getMonth()]} ${day}, ${year}`;

  console.log(`Please search for the 7-day weather forecast for ${city} starting from ${todayDisplay} and present it in the following format.

Search steps:
1. Search "${city} 7-day weather forecast"
2. Search "${city} weather this week"

Output format:
📅 ${city} 7-Day Weather Forecast
━━━━━━━━━━━━━━━━━━━━━━━
Starting ${todayDisplay}:

[One line per day]
{Day} {Date}  {icon} {conditions}  🌡️{low}~{high}°${unit}  💧{humidity}%  🌬️{wind}

━━━━━━━━━━━━━━━━━━━━━━━
📌 Weekly trend: [2–3 sentences on overall weather pattern]
⚠️ Alerts: [any extreme weather warnings this week]
👔 What to wear this week: [general outfit guidance]

💡 Reply "today's weather" for today's detailed report`);
}
