
const fs = require("fs");
const path = require("path");
const axios = require("axios");
const dayjs = require("dayjs");

const weekOfYear = require("dayjs/plugin/weekOfYear");
const dayOfYear = require("dayjs/plugin/dayOfYear");
const isLeapYear = require("dayjs/plugin/isLeapYear");

dayjs.extend(weekOfYear);
dayjs.extend(dayOfYear);
dayjs.extend(isLeapYear);

const today = dayjs();
const year = today.year();
const cacheFile = path.join(__dirname, `holidays_${year}.json`);

async function fetchHolidays(year) {
  const url = `https://www.shuyz.com/githubfiles/china-holiday-calender/master/holidayAPI.json`;
  const res = await axios.get(url, { timeout: 10000 });
  return res.data;
}

async function loadHolidays(year) {
  if (fs.existsSync(cacheFile)) {
    return JSON.parse(fs.readFileSync(cacheFile, "utf-8"));
  }
  const data = await fetchHolidays(year);
  fs.writeFileSync(cacheFile, JSON.stringify(data, null, 2));
  return data;
}

const TARGETS = ["清明节","劳动节","端午节","中秋节","国庆节","元旦","春节","小年"];

function extractHolidays(data, year) {
  const result = {};
  const yearData = data.Years[year.toString()];
  if (!yearData) return result;
  
  for (const item of yearData) {
    // 匹配节日名称（支持"中秋节、国庆节"这种组合）
    for (const target of TARGETS) {
      if (item.Name.includes(target)) {
        result[target] = dayjs(item.StartDate);
        break;
      }
    }
  }
  return result;
}

function daysLeft(target) {
  return target.diff(today, "day");
}

function getWeekendDays() {
  const day = today.day();
  const diff = 6 - day;
  return diff >= 0 ? diff : diff + 7;
}

function getProgress() {
  const weekProgress = Math.floor(((today.day() || 7) / 7) * 100);
  const monthProgress = Math.floor((today.date() / today.daysInMonth()) * 100);
  const yearProgress = Math.floor(
    (today.dayOfYear() / (today.isLeapYear() ? 366 : 365)) * 100
  );
  return { weekProgress, monthProgress, yearProgress };
}

async function main() {
  try {
    const raw = await loadHolidays(year);
    const holidays = extractHolidays(raw, year);

    let text = `提醒您：${today.format("YYYY年MM月DD日")}，第${today.week()}周，周${"日一二三四五六"[today.day()]}，大家上午好，
工作虽然辛苦，但也不要忘了休息，起来走一走～`;

    text += `\n距离【周末】还有${getWeekendDays()}天`;

    for (const [name, d] of Object.entries(holidays)) {
      text += `\n距离【${name}】还有${daysLeft(d)}天`;
    }

    const { weekProgress, monthProgress, yearProgress } = getProgress();

    text += `\n距离【周一】过去${today.day()}天(${weekProgress}%)`;
    text += `\n距离【月初】过去${today.date() - 1}天(${monthProgress}%)`;
    text += `\n距离【年初】过去${today.dayOfYear()}天(${yearProgress}%)`;

    console.log(text);

  } catch (err) {
    console.error("运行失败:", err.message);
  }
}

main();
