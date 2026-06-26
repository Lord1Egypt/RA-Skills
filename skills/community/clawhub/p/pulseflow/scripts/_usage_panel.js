const cp = require('child_process');
const path = require('path');
const {
  ensureFile,
  exists,
  formatDateInTimeZone,
  readText,
  writeText,
} = require('./_common');

const USAGE_HEADER = '## AI USAGE THIS WEEK';
const MONTHLY_DAILY_START = '<!-- AI_MONTHLY_DAILY_USAGE_START -->';
const MONTHLY_DAILY_END = '<!-- AI_MONTHLY_DAILY_USAGE_END -->';
const MONTHLY_WEEKLY_START = '<!-- AI_MONTHLY_WEEKLY_USAGE_START -->';
const MONTHLY_WEEKLY_END = '<!-- AI_MONTHLY_WEEKLY_USAGE_END -->';

function isoDateFromLocalDate(date) {
  return `${date}T12:00:00.000Z`;
}

function shiftDate(date, deltaDays) {
  const base = new Date(isoDateFromLocalDate(date));
  base.setUTCDate(base.getUTCDate() + deltaDays);
  return base.toISOString().slice(0, 10);
}

function weekdayIndex(date) {
  return new Date(isoDateFromLocalDate(date)).getUTCDay();
}

function weekStart(date) {
  const sundayBased = weekdayIndex(date);
  const mondayOffset = sundayBased === 0 ? 6 : sundayBased - 1;
  return shiftDate(date, -mondayOffset);
}

function weekDates(date) {
  const start = weekStart(date);
  return Array.from({ length: 7 }, (_, index) => shiftDate(start, index));
}

function monthDates(month) {
  const [year, mon] = month.split('-').map(Number);
  const daysInMonth = new Date(Date.UTC(year, mon, 0)).getUTCDate();
  return Array.from({ length: daysInMonth }, (_, index) => `${month}-${String(index + 1).padStart(2, '0')}`);
}

function hitRate(entry) {
  const input = Number(entry.input || 0);
  const cacheRead = Number(entry.cacheRead || 0);
  const denominator = input + cacheRead;
  if (denominator <= 0) return '0.0%';
  return `${((cacheRead / denominator) * 100).toFixed(1)}%`;
}

function formatInt(value) {
  return Number(value || 0).toLocaleString('en-US');
}

function summarizeDay(entry = {}) {
  const input = Number(entry.input || 0);
  const output = Number(entry.output || 0);
  const cacheRead = Number(entry.cacheRead || 0);
  const cacheWrite = Number(entry.cacheWrite || 0);
  const freshTokens = input + output;
  return {
    input,
    output,
    cacheRead,
    cacheWrite,
    cache: cacheRead + cacheWrite,
    totalTokens: freshTokens,
    rawTotalTokens: Number(entry.totalTokens || 0),
    totalCost: Number(entry.totalCost || 0),
    hitRate: hitRate({ input, cacheRead }),
  };
}

function usageSummary(days = 14) {
  if (process.env.AI_WORKLOG_USAGE_JSON && exists(process.env.AI_WORKLOG_USAGE_JSON)) {
    return JSON.parse(readText(process.env.AI_WORKLOG_USAGE_JSON));
  }

  const raw = cp.execFileSync('openclaw', ['gateway', 'usage-cost', '--days', String(days), '--json'], {
    encoding: 'utf8',
  });
  return JSON.parse(raw);
}

function usageMap(summary) {
  const map = new Map();
  for (const item of summary.daily || []) {
    map.set(item.date, summarizeDay(item));
  }
  return map;
}

function weeklyRows(summary, anchorDate) {
  const map = usageMap(summary);
  return weekDates(anchorDate).map((date) => ({
    date,
    ...(map.get(date) || summarizeDay({})),
  }));
}

function rowsTotal(rows) {
  const total = rows.reduce((acc, row) => ({
    input: acc.input + row.input,
    output: acc.output + row.output,
    cacheRead: acc.cacheRead + row.cacheRead,
    cacheWrite: acc.cacheWrite + row.cacheWrite,
    cache: acc.cache + row.cache,
    totalTokens: acc.totalTokens + row.totalTokens,
    rawTotalTokens: acc.rawTotalTokens + Number(row.rawTotalTokens || 0),
    totalCost: acc.totalCost + row.totalCost,
  }), {
    input: 0,
    output: 0,
    cacheRead: 0,
    cacheWrite: 0,
    cache: 0,
    totalTokens: 0,
    rawTotalTokens: 0,
    totalCost: 0,
  });
  return {
    ...total,
    hitRate: hitRate({ input: total.input, cacheRead: total.cacheRead }),
  };
}

function buildUsageSection(rows) {
  const lines = [
    USAGE_HEADER,
    '| Date | Total Tokens | Input | Output | Cache | Hit Rate |',
    '| --- | ---: | ---: | ---: | ---: | ---: |',
  ];

  for (const row of rows) {
    lines.push(`| ${row.date} | ${formatInt(row.totalTokens)} | ${formatInt(row.input)} | ${formatInt(row.output)} | ${formatInt(row.cache)} | ${row.hitRate} |`);
  }

  const total = rowsTotal(rows);
  lines.push(`| **Week Total** | **${formatInt(total.totalTokens)}** | **${formatInt(total.input)}** | **${formatInt(total.output)}** | **${formatInt(total.cache)}** | **${total.hitRate}** |`);
  lines.push('', '---');
  return `${lines.join('\n')}\n`;
}

function buildUsageTable(rows, totalLabel = 'Week Total') {
  const lines = [
    '| Date | Total Tokens | Input | Output | Cache | Hit Rate |',
    '| --- | ---: | ---: | ---: | ---: | ---: |',
  ];

  if (!rows.length) {
    lines.push('| 暂无 | 0 | 0 | 0 | 0 | 0.0% |');
  } else {
    for (const row of rows) {
      lines.push(`| ${row.date} | ${formatInt(row.totalTokens)} | ${formatInt(row.input)} | ${formatInt(row.output)} | ${formatInt(row.cache)} | ${row.hitRate} |`);
    }
  }

  const total = rowsTotal(rows);
  lines.push(`| **${totalLabel}** | **${formatInt(total.totalTokens)}** | **${formatInt(total.input)}** | **${formatInt(total.output)}** | **${formatInt(total.cache)}** | **${total.hitRate}** |`);
  return lines.join('\n');
}

function monthlyRows(summary, month, finalDate) {
  const map = usageMap(summary);
  return monthDates(month)
    .filter((date) => date <= finalDate && map.has(date))
    .map((date) => ({ date, ...map.get(date) }));
}

function buildMonthlyDailyUsageBlock(summary, month, finalDate) {
  const rows = monthlyRows(summary, month, finalDate);
  return [
    '## AI Usage Daily Summary',
    buildUsageTable(rows, 'Month Total'),
  ].join('\n');
}

function upsertManagedBlock(text, startMarker, endMarker, blockContent) {
  const wrapped = `${startMarker}\n${blockContent.trimEnd()}\n${endMarker}`;
  if (text.includes(startMarker) && text.includes(endMarker)) {
    const pattern = new RegExp(`${startMarker}[\\s\\S]*?${endMarker}`, 'm');
    return text.replace(pattern, wrapped);
  }

  const trimmed = text.replace(/\s*$/, '');
  return `${trimmed}\n\n${wrapped}\n`;
}

function removeManagedBlock(text, startMarker, endMarker) {
  if (!text.includes(startMarker) || !text.includes(endMarker)) {
    return text;
  }
  const pattern = new RegExp(`\\n?${startMarker}[\\s\\S]*?${endMarker}\\n?`, 'm');
  return text.replace(pattern, '\n').replace(/\n{3,}/g, '\n\n');
}

function updateMonthlyUsageArchive(monthFile, summary, month, finalDate) {
  const current = exists(monthFile) ? readText(monthFile) : '';
  const withoutWeekly = removeManagedBlock(current, MONTHLY_WEEKLY_START, MONTHLY_WEEKLY_END);
  const withDaily = upsertManagedBlock(withoutWeekly, MONTHLY_DAILY_START, MONTHLY_DAILY_END, buildMonthlyDailyUsageBlock(summary, month, finalDate));
  writeText(monthFile, `${withDaily.replace(/\s*$/, '')}\n`);
  return { ok: true, path: monthFile, month };
}

function replaceUsageSection(nowText, usageSection) {
  const marker = `${USAGE_HEADER}\n`;
  if (nowText.includes(marker)) {
    const start = nowText.indexOf(marker);
    const nextSectionIndex = nowText.indexOf('\n## ', start + marker.length);
    const head = nowText.slice(0, start).replace(/\s*$/, '');
    const tail = nextSectionIndex >= 0 ? nowText.slice(nextSectionIndex).replace(/^\s*/, '') : '';
    const separator = usageSection.trimEnd().endsWith('---') ? '\n' : '\n\n';
    const prefix = head ? `${head}\n\n` : '';
    return `${prefix}${usageSection.trimEnd()}${tail ? `${separator}${tail}` : '\n'}`;
  }

  const focusMarker = '\n## FOCUS\n';
  if (nowText.includes(focusMarker)) {
    const idx = nowText.indexOf(focusMarker);
    const head = nowText.slice(0, idx).replace(/\s*$/, '');
    const tail = nowText.slice(idx).replace(/^\s*/, '');
    const separator = usageSection.trimEnd().endsWith('---') ? '\n' : '\n\n';
    const prefix = head ? `${head}\n\n` : '';
    return `${prefix}${usageSection.trimEnd()}${separator}${tail}`;
  }

  const trimmed = nowText.replace(/\s*$/, '');
  return trimmed ? `${trimmed}\n\n${usageSection.trimEnd()}\n` : `${usageSection.trimEnd()}\n`;
}

function weekLabel(rows) {
  return `${rows[0].date} → ${rows[rows.length - 1].date}`;
}

function todayUsage(summary, today) {
  return usageMap(summary).get(today) || summarizeDay({});
}

module.exports = {
  MONTHLY_DAILY_END,
  MONTHLY_DAILY_START,
  USAGE_HEADER,
  buildUsageSection,
  buildUsageTable,
  monthlyRows,
  replaceUsageSection,
  summarizeDay,
  todayUsage,
  updateMonthlyUsageArchive,
  usageSummary,
  monthDates,
  weekDates,
  weekStart,
  weeklyRows,
};
