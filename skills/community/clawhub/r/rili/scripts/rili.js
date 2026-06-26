#!/usr/bin/env node

import path from "node:path";
import { fileURLToPath } from "node:url";

const MS_PER_DAY = 24 * 60 * 60 * 1000;

const GREGORIAN_WEEKDAY_FORMATTER = new Intl.DateTimeFormat("zh-Hans-CN", {
  timeZone: "UTC",
  weekday: "long",
});

const CHINESE_LUNAR_FORMATTER = new Intl.DateTimeFormat("zh-Hans-CN-u-ca-chinese", {
  timeZone: "UTC",
  year: "numeric",
  month: "long",
  day: "numeric",
});

const CHINESE_ZONED_DATE_FORMATTER_CACHE = new Map();

const LUNAR_MONTH_NUMBER = {
  正月: 1,
  二月: 2,
  三月: 3,
  四月: 4,
  五月: 5,
  六月: 6,
  七月: 7,
  八月: 8,
  九月: 9,
  十月: 10,
  十一月: 11,
  十二月: 12,
  冬月: 11,
  腊月: 12,
};

const ZODIAC_BY_BRANCH = {
  子: "鼠",
  丑: "牛",
  寅: "虎",
  卯: "兔",
  辰: "龙",
  巳: "蛇",
  午: "马",
  未: "羊",
  申: "猴",
  酉: "鸡",
  戌: "狗",
  亥: "猪",
};

const FESTIVAL_DEFINITIONS = [
  { name: "春节", aliases: ["春节", "农历新年", "新春", "过年"], month: 1, day: 1 },
  { name: "元宵", aliases: ["元宵", "元宵节"], month: 1, day: 15 },
  { name: "龙抬头", aliases: ["龙抬头", "二月二"], month: 2, day: 2 },
  { name: "上巳", aliases: ["上巳", "上巳节", "三月三"], month: 3, day: 3 },
  { name: "端午", aliases: ["端午", "端午节"], month: 5, day: 5 },
  { name: "七夕", aliases: ["七夕", "七夕节"], month: 7, day: 7 },
  { name: "中元", aliases: ["中元", "中元节", "鬼节"], month: 7, day: 15 },
  { name: "中秋", aliases: ["中秋", "中秋节"], month: 8, day: 15 },
  { name: "重阳", aliases: ["重阳", "重阳节"], month: 9, day: 9 },
  { name: "腊八", aliases: ["腊八", "腊八节"], month: 12, day: 8 },
  { name: "除夕", aliases: ["除夕", "大年三十"], special: "chuxi" },
];

const FESTIVAL_ALIAS_LOOKUP = new Map(
  FESTIVAL_DEFINITIONS.flatMap((festival) =>
    festival.aliases.map((alias) => [normalizeFestivalName(alias), festival]),
  ),
);

function getZonedDateFormatter(timeZone) {
  let formatter = CHINESE_ZONED_DATE_FORMATTER_CACHE.get(timeZone);
  if (!formatter) {
    formatter = new Intl.DateTimeFormat("en-CA", {
      timeZone,
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    });
    CHINESE_ZONED_DATE_FORMATTER_CACHE.set(timeZone, formatter);
  }
  return formatter;
}

function makeUtcDate(year, month, day) {
  const date = new Date(Date.UTC(year, month - 1, day));
  if (
    Number.isNaN(date.getTime()) ||
    date.getUTCFullYear() !== year ||
    date.getUTCMonth() !== month - 1 ||
    date.getUTCDate() !== day
  ) {
    throw new Error(`无效日期: ${year}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`);
  }
  return date;
}

function addDays(date, days) {
  return new Date(date.getTime() + days * MS_PER_DAY);
}

function formatIsoDate(date) {
  return date.toISOString().slice(0, 10);
}

function getWeekdayName(date) {
  return GREGORIAN_WEEKDAY_FORMATTER.format(date);
}

function validateTimeZone(timeZone) {
  try {
    new Intl.DateTimeFormat("en-US", { timeZone }).format(new Date());
    return timeZone;
  } catch {
    throw new Error(`无效时区: ${timeZone}`);
  }
}

function getResolvedTimeZone(timeZone) {
  return validateTimeZone(timeZone ?? Intl.DateTimeFormat().resolvedOptions().timeZone ?? "UTC");
}

function getTodayInTimeZone(timeZone) {
  const parts = getZonedDateFormatter(timeZone).formatToParts(new Date());
  const values = Object.fromEntries(
    parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]),
  );
  return makeUtcDate(Number(values.year), Number(values.month), Number(values.day));
}

function parseDateToken(token, timeZone) {
  const normalized = (token ?? "today").trim().toLowerCase();
  if (normalized === "today") {
    return getTodayInTimeZone(getResolvedTimeZone(timeZone));
  }
  if (normalized === "tomorrow") {
    return addDays(getTodayInTimeZone(getResolvedTimeZone(timeZone)), 1);
  }
  if (normalized === "yesterday") {
    return addDays(getTodayInTimeZone(getResolvedTimeZone(timeZone)), -1);
  }
  const match = normalized.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (!match) {
    throw new Error(`不支持的日期参数: ${token}`);
  }
  return makeUtcDate(Number(match[1]), Number(match[2]), Number(match[3]));
}

function parseMonthToken(token, timeZone) {
  if (!token || token === "today" || token === "tomorrow" || token === "yesterday") {
    const date = parseDateToken(token ?? "today", timeZone);
    return { year: date.getUTCFullYear(), month: date.getUTCMonth() + 1 };
  }
  const monthMatch = token.match(/^(\d{4})-(\d{2})$/);
  if (monthMatch) {
    const year = Number(monthMatch[1]);
    const month = Number(monthMatch[2]);
    if (month < 1 || month > 12) {
      throw new Error(`无效月份: ${token}`);
    }
    return { year, month };
  }
  const date = parseDateToken(token, timeZone);
  return { year: date.getUTCFullYear(), month: date.getUTCMonth() + 1 };
}

function formatLunarDay(dayNumber) {
  const names = {
    1: "初一",
    2: "初二",
    3: "初三",
    4: "初四",
    5: "初五",
    6: "初六",
    7: "初七",
    8: "初八",
    9: "初九",
    10: "初十",
    11: "十一",
    12: "十二",
    13: "十三",
    14: "十四",
    15: "十五",
    16: "十六",
    17: "十七",
    18: "十八",
    19: "十九",
    20: "二十",
    21: "廿一",
    22: "廿二",
    23: "廿三",
    24: "廿四",
    25: "廿五",
    26: "廿六",
    27: "廿七",
    28: "廿八",
    29: "廿九",
    30: "三十",
  };
  const dayName = names[dayNumber];
  if (!dayName) {
    throw new Error(`无效农历日: ${dayNumber}`);
  }
  return dayName;
}

function parseLunarMonth(monthName) {
  const leapMonth = monthName.startsWith("闰");
  const baseMonthName = leapMonth ? monthName.slice(1) : monthName;
  const monthNumber = LUNAR_MONTH_NUMBER[baseMonthName];
  if (!monthNumber) {
    throw new Error(`无法识别的农历月份: ${monthName}`);
  }
  return { monthNumber, leapMonth };
}

function getLunarInfo(date) {
  const parts = CHINESE_LUNAR_FORMATTER.formatToParts(date);
  const values = Object.fromEntries(
    parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]),
  );
  const monthName = values.month;
  const dayNumber = Number(values.day);
  const { monthNumber, leapMonth } = parseLunarMonth(monthName);
  const yearName = values.yearName;
  const zodiac = ZODIAC_BY_BRANCH[yearName.slice(-1)];
  return {
    relatedYear: Number(values.relatedYear),
    yearName,
    zodiac,
    monthName,
    monthNumber,
    leapMonth,
    dayNumber,
    dayName: formatLunarDay(dayNumber),
  };
}

function normalizeFestivalName(name) {
  return name.replace(/[\s节]/g, "").trim();
}

function getFestivalNamesForDate(date) {
  const info = getLunarInfo(date);
  const festivals = FESTIVAL_DEFINITIONS.filter((festival) => {
    if (festival.special) {
      return false;
    }
    return (
      info.leapMonth === false &&
      info.monthNumber === festival.month &&
      info.dayNumber === festival.day
    );
  }).map((festival) => festival.name);

  const nextDay = getLunarInfo(addDays(date, 1));
  if (
    info.monthNumber === 12 &&
    nextDay.relatedYear === info.relatedYear + 1 &&
    nextDay.monthNumber === 1 &&
    nextDay.dayNumber === 1
  ) {
    festivals.push("除夕");
  }

  return festivals;
}

export function buildDateInfo(date) {
  const lunar = getLunarInfo(date);
  return {
    isoDate: formatIsoDate(date),
    weekday: getWeekdayName(date),
    lunar,
    festivals: getFestivalNamesForDate(date),
  };
}

function iterDates(start, endExclusive) {
  const dates = [];
  for (let cursor = start; cursor < endExclusive; cursor = addDays(cursor, 1)) {
    dates.push(cursor);
  }
  return dates;
}

export function findGregorianDatesByLunar({
  lunarYear,
  month,
  day,
  leapMonth,
}) {
  if (!Number.isInteger(lunarYear) || lunarYear < 1900 || lunarYear > 2100) {
    throw new Error(`不支持的农历年: ${lunarYear}`);
  }
  if (!Number.isInteger(month) || month < 1 || month > 12) {
    throw new Error(`无效农历月份: ${month}`);
  }
  if (!Number.isInteger(day) || day < 1 || day > 30) {
    throw new Error(`无效农历日期: ${day}`);
  }

  const start = makeUtcDate(lunarYear, 1, 1);
  const end = makeUtcDate(lunarYear + 1, 3, 1);

  return iterDates(start, end)
    .map((date) => buildDateInfo(date))
    .filter((info) => {
      if (info.lunar.relatedYear !== lunarYear) {
        return false;
      }
      if (info.lunar.monthNumber !== month || info.lunar.dayNumber !== day) {
        return false;
      }
      if (typeof leapMonth === "boolean" && info.lunar.leapMonth !== leapMonth) {
        return false;
      }
      return true;
    });
}

export function findFestivalDates(lunarYear, rawFestivalName) {
  if (rawFestivalName === "list") {
    return FESTIVAL_DEFINITIONS.map((festival) => ({
      name: festival.name,
      aliases: festival.aliases,
    }));
  }

  const normalized = normalizeFestivalName(rawFestivalName);
  const festival = FESTIVAL_ALIAS_LOOKUP.get(normalized);
  if (!festival) {
    throw new Error(`不支持的节日: ${rawFestivalName}`);
  }

  if (festival.special === "chuxi") {
    const nextLunarNewYear = findGregorianDatesByLunar({
      lunarYear: lunarYear + 1,
      month: 1,
      day: 1,
      leapMonth: false,
    })[0];
    if (!nextLunarNewYear) {
      return [];
    }
    const chuxiDate = addDays(parseDateToken(nextLunarNewYear.isoDate), -1);
    return [buildDateInfo(chuxiDate)];
  }

  return findGregorianDatesByLunar({
    lunarYear,
    month: festival.month,
    day: festival.day,
    leapMonth: false,
  });
}

export function buildMonthData(year, month) {
  if (!Number.isInteger(year) || !Number.isInteger(month) || month < 1 || month > 12) {
    throw new Error(`无效月份: ${year}-${month}`);
  }
  const firstDay = makeUtcDate(year, month, 1);
  const daysInMonth = new Date(Date.UTC(year, month, 0)).getUTCDate();
  const mondayFirstOffset = (firstDay.getUTCDay() + 6) % 7;
  const weeks = [];
  let currentWeek = Array.from({ length: 7 }, () => null);

  for (let index = 0; index < mondayFirstOffset; index += 1) {
    currentWeek[index] = null;
  }

  const days = [];
  for (let day = 1; day <= daysInMonth; day += 1) {
    const date = makeUtcDate(year, month, day);
    const info = buildDateInfo(date);
    days.push(info);
    currentWeek[(mondayFirstOffset + day - 1) % 7] = day;
    if ((mondayFirstOffset + day) % 7 === 0 || day === daysInMonth) {
      weeks.push(currentWeek);
      currentWeek = Array.from({ length: 7 }, () => null);
    }
  }

  const highlights = days
    .filter((info) => info.lunar.dayNumber === 1 || info.festivals.length > 0)
    .map((info) => ({
      isoDate: info.isoDate,
      summary:
        info.festivals.length > 0
          ? info.festivals.join("、")
          : `农历${info.lunar.monthName}${info.lunar.dayName}`,
      lunar: info.lunar,
      festivals: info.festivals,
    }));

  return {
    year,
    month,
    title: `${year}年${String(month).padStart(2, "0")}月`,
    weeks,
    days,
    highlights,
  };
}

function renderMonthText(data) {
  const header = `${data.title}\n一  二  三  四  五  六  日`;
  const weekLines = data.weeks.map((week) =>
    week.map((day) => (day == null ? "  " : String(day).padStart(2, " "))).join("  "),
  );
  const highlightLines =
    data.highlights.length === 0
      ? []
      : [
          "",
          "农历节点:",
          ...data.highlights.map((item) => `${item.isoDate} ${item.summary}`),
        ];
  return [header, ...weekLines, ...highlightLines].join("\n");
}

function renderDateText(info) {
  const lines = [
    `公历: ${info.isoDate} ${info.weekday}`,
    `农历: ${info.lunar.yearName}年 ${info.lunar.monthName}${info.lunar.dayName}`,
  ];
  if (info.lunar.zodiac) {
    lines.push(`生肖: ${info.lunar.zodiac}`);
  }
  if (info.festivals.length > 0) {
    lines.push(`节日: ${info.festivals.join("、")}`);
  }
  return lines.join("\n");
}

function renderLunarLookupText(results) {
  if (results.length === 0) {
    return "未找到对应的公历日期。";
  }
  return results
    .map((info) => {
      return `${info.isoDate} ${info.weekday} -> 农历${info.lunar.monthName}${info.lunar.dayName}`;
    })
    .join("\n");
}

function parseNumber(value, label) {
  const parsed = Number(value);
  if (!Number.isInteger(parsed)) {
    throw new Error(`${label} 必须是整数: ${value}`);
  }
  return parsed;
}

function consumeCommonFlags(args) {
  const rest = [];
  let json = false;
  let leapMonth;
  let timeZone;

  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    if (arg === "--json") {
      json = true;
      continue;
    }
    if (arg === "--leap") {
      leapMonth = true;
      continue;
    }
    if (arg === "--tz" || arg === "--time-zone") {
      const value = args[index + 1];
      if (!value) {
        throw new Error(`${arg} 需要一个时区参数`);
      }
      timeZone = validateTimeZone(value);
      index += 1;
      continue;
    }
    if (arg === "--help" || arg === "-h") {
      rest.push("help");
      continue;
    }
    rest.push(arg);
  }

  return { rest, json, leapMonth, timeZone };
}

export function usageText() {
  return [
    "用法:",
    "  rili.js today [--json] [--tz Asia/Shanghai]",
    "  rili.js date <YYYY-MM-DD|today|tomorrow|yesterday> [--json] [--tz Asia/Shanghai]",
    "  rili.js month <YYYY-MM|YYYY-MM-DD|today> [--json] [--tz Asia/Shanghai]",
    "  rili.js find-lunar <lunarYear> <month> <day> [--leap] [--json]",
    "  rili.js festival <lunarYear> <name> [--json]",
    "  rili.js festival list",
  ].join("\n");
}

export async function main(rawArgv = process.argv.slice(2)) {
  const { rest, json, leapMonth, timeZone } = consumeCommonFlags(rawArgv);
  const [command = "today", ...args] = rest;

  if (command === "help") {
    console.log(usageText());
    return;
  }

  if (command === "today" || command === "date" || command === "lunar") {
    const token = command === "today" ? "today" : args[0] ?? "today";
    const info = buildDateInfo(parseDateToken(token, timeZone));
    console.log(json ? JSON.stringify(info, null, 2) : renderDateText(info));
    return;
  }

  if (command === "month") {
    const token = args[0] ?? "today";
    const { year, month } = parseMonthToken(token, timeZone);
    const data = buildMonthData(year, month);
    console.log(json ? JSON.stringify(data, null, 2) : renderMonthText(data));
    return;
  }

  if (command === "find-lunar") {
    if (args.length < 3) {
      throw new Error("find-lunar 需要 <lunarYear> <month> <day>");
    }
    const results = findGregorianDatesByLunar({
      lunarYear: parseNumber(args[0], "农历年"),
      month: parseNumber(args[1], "农历月"),
      day: parseNumber(args[2], "农历日"),
      leapMonth,
    });
    console.log(json ? JSON.stringify(results, null, 2) : renderLunarLookupText(results));
    return;
  }

  if (command === "festival") {
    if (args.length === 0) {
      throw new Error("festival 需要 <lunarYear> <name>，或使用 festival list");
    }
    if (args[0] === "list") {
      const list = findFestivalDates(0, "list");
      console.log(json ? JSON.stringify(list, null, 2) : list.map((item) => item.name).join("\n"));
      return;
    }

    let lunarYear;
    let festivalName;
    if (/^\d+$/.test(args[0])) {
      lunarYear = parseNumber(args[0], "农历年");
      festivalName = args.slice(1).join("");
    } else {
      lunarYear = getLunarInfo(getTodayInTimeZone(getResolvedTimeZone(timeZone))).relatedYear;
      festivalName = args.join("");
    }
    if (!festivalName) {
      throw new Error("festival 缺少节日名称");
    }
    const results = findFestivalDates(lunarYear, festivalName);
    console.log(json ? JSON.stringify(results, null, 2) : renderLunarLookupText(results));
    return;
  }

  throw new Error(`不支持的命令: ${command}`);
}

const isMain = path.resolve(process.argv[1] ?? "") === fileURLToPath(import.meta.url);

if (isMain) {
  main().catch((error) => {
    console.error(`rili: ${error.message}`);
    console.error("");
    console.error(usageText());
    process.exitCode = 1;
  });
}
