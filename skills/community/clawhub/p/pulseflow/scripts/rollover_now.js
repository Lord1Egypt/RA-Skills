#!/usr/bin/env node
const path = require('path');
const {
  buildDefaultRolloverState,
  deriveRuntimePaths,
  exists,
  formatDateInTimeZone,
  historyMonthShell,
  loadJson,
  readText,
  resolveRolloverStatePath,
  saveJson,
  writeText,
} = require('./_common');
const {
  buildUsageSection,
  buildUsageTable,
  usageSummary,
  weeklyRows,
  weekDates,
} = require('./_usage_panel');

const SECTIONS = ['AI USAGE THIS WEEK', 'FOCUS', 'TODAY', 'UP NEXT', 'DONE', 'AI DONE TODAY'];

function splitSections(text) {
  const lines = text.split(/\r?\n/);
  const sections = {};
  let current = null;
  let buffer = [];
  let preamble = [];

  for (const line of lines) {
    const matched = SECTIONS.find((name) => line.startsWith(`## ${name}`));
    if (matched) {
      if (current === null) {
        preamble = [...buffer];
      } else {
        sections[current] = [...buffer];
      }
      current = matched;
      buffer = [];
    } else {
      buffer.push(line);
    }
  }

  if (current === null) {
    preamble = [...lines];
  } else {
    sections[current] = [...buffer];
  }

  return { preamble, sections };
}

function isPlaceholderCheckbox(line) {
  return /^- \[[ x]\]\s*$/.test(line.trim());
}

function classifyItems(lines) {
  const done = [];
  const pending = [];

  for (const raw of lines || []) {
    const line = raw.replace(/\s+$/, '');
    if (!line.trim()) continue;
    if (isPlaceholderCheckbox(line)) continue;
    if (line.trimStart().startsWith('- [x]')) {
      done.push(line);
    } else {
      pending.push(line);
    }
  }

  return { done, pending };
}

function aiSnapshot(lines) {
  return (lines || []).filter((line) => line.trim());
}

function ensureMonthHistoryFile(historyDir, month, paths) {
  const monthFile = path.join(historyDir, `${month}.md`);
  if (!exists(monthFile)) {
    writeText(monthFile, historyMonthShell(paths, month));
  }
  return monthFile;
}

function buildNow(preamble, usageSection, todayPending, upNextPending) {
  const pre = (preamble || []).join('\n').replace(/\s*$/, '');
  const out = [];

  if (pre) {
    out.push(pre);
  }

  out.push(usageSection.trimEnd(), '');

  out.push(
    '## FOCUS',
    '',
    '- [ ]',
    '',
    '## TODAY',
  );

  if (todayPending.length) {
    out.push(...todayPending);
  } else {
    out.push('- [ ]');
  }

  out.push('', '## UP NEXT');
  if (upNextPending.length) {
    out.push(...upNextPending);
  } else {
    out.push('- [ ]');
  }

  out.push(
    '',
    '## DONE',
    '',
    '- [x]',
    '',
    '---',
    '## AI DONE TODAY',
    '- 暂无',
    '',
  );

  return out.join('\n');
}

function weekTitleForDate(date) {
  const monthPrefix = `${date.slice(0, 7)}-`;
  const dates = weekDates(date).filter((item) => item.startsWith(monthPrefix));
  return `## Week ${dates[0]} → ${dates[dates.length - 1]}`;
}

function extractWeekStart(header) {
  const matched = header.match(/^## Week (\d{4}-\d{2}-\d{2}) →/);
  return matched ? matched[1] : '9999-99-99';
}

function buildDayEntry(archivedDate, humanDone, aiLines) {
  const lines = [];
  lines.push(`### ${archivedDate}`, '');
  lines.push('#### Human Done');
  if (humanDone.length) {
    lines.push(...humanDone);
  } else {
    lines.push('- [x] 暂无');
  }
  lines.push('', '#### AI Done Today');
  if (aiLines.length) {
    lines.push(...aiLines);
  } else {
    lines.push('- 暂无');
  }
  return lines.join('\n').replace(/\s*$/, '');
}

function parseWeekSections(text, month) {
  const lines = text.split(/\r?\n/);
  const headerLine = lines.find((line) => /^# History - /.test(line)) || `# History - ${month}`;
  const sections = [];
  let currentHeader = null;
  let buffer = [];

  for (const line of lines) {
    if (/^## Week /.test(line)) {
      if (currentHeader) {
        sections.push({ header: currentHeader, lines: [...buffer] });
      }
      currentHeader = line;
      buffer = [];
      continue;
    }

    if (currentHeader) {
      buffer.push(line);
    }
  }

  if (currentHeader) {
    sections.push({ header: currentHeader, lines: [...buffer] });
  }

  return { preamble: [headerLine], sections };
}

function parseDayEntries(lines) {
  const entries = new Map();
  let currentDate = null;
  let buffer = [];

  for (const line of lines || []) {
    const matched = line.match(/^### (\d{4}-\d{2}-\d{2})$/);
    if (matched) {
      if (currentDate) {
        entries.set(currentDate, buffer.join('\n').replace(/\s*$/, ''));
      }
      currentDate = matched[1];
      buffer = [line];
      continue;
    }

    if (currentDate) {
      buffer.push(line);
    }
  }

  if (currentDate) {
    entries.set(currentDate, buffer.join('\n').replace(/\s*$/, ''));
  }

  return entries;
}

function weekRowsForDate(summary, archivedDate) {
  const monthPrefix = `${archivedDate.slice(0, 7)}-`;
  return weeklyRows(summary, archivedDate).filter((row) => row.date.startsWith(monthPrefix) && row.date <= archivedDate);
}

function buildWeekBody(summary, archivedDate, dayEntries) {
  const rows = weekRowsForDate(summary, archivedDate);
  const out = [
    '### AI Usage Weekly Summary',
    buildUsageTable(rows, 'Week Total'),
  ];

  const orderedDates = Array.from(dayEntries.keys()).sort();
  for (const date of orderedDates) {
    out.push('', dayEntries.get(date).trimEnd());
  }

  return out.join('\n').replace(/\s*$/, '');
}

function upsertHistory(monthFile, archivedDate, humanDone, aiLines, summary, month) {
  const current = exists(monthFile) ? readText(monthFile) : `# History - ${month}\n`;
  const { preamble, sections } = parseWeekSections(current, month);
  const targetHeader = weekTitleForDate(archivedDate);
  const sectionMap = new Map(sections.map((section) => [section.header, section.lines]));
  const dayEntries = parseDayEntries(sectionMap.get(targetHeader) || []);
  dayEntries.set(archivedDate, buildDayEntry(archivedDate, humanDone, aiLines));
  sectionMap.set(targetHeader, buildWeekBody(summary, archivedDate, dayEntries).split('\n'));

  const orderedHeaders = Array.from(sectionMap.keys()).sort((a, b) => extractWeekStart(a).localeCompare(extractWeekStart(b)));
  const out = [...preamble.filter(Boolean)];

  for (const header of orderedHeaders) {
    out.push('', header, '', ...sectionMap.get(header));
  }

  writeText(monthFile, `${out.join('\n').replace(/\s*$/, '')}\n`);
}

function main() {
  const paths = deriveRuntimePaths();
  const config = loadJson(paths.configPath, null);
  if (!config) {
    throw new Error('Missing config.json: run init_system.js first');
  }

  const timeZone = config.timezone || process.env.AI_WORKLOG_TIMEZONE || 'Asia/Shanghai';
  const now = new Date();
  const today = formatDateInTimeZone(now, timeZone);
  const yesterday = formatDateInTimeZone(new Date(now.getTime() - 24 * 60 * 60 * 1000), timeZone);
  const rolloverStatePath = resolveRolloverStatePath(config, paths);
  const rolloverState = loadJson(rolloverStatePath, buildDefaultRolloverState());

  if (rolloverState.lastRolloverDate === today) {
    process.stdout.write(`${JSON.stringify({ ok: true, skipped: true, date: today }, null, 2)}\n`);
    return;
  }

  const dashboardPath = config.dashboardPath || paths.nowPath;
  const historyDir = config.historyDir || paths.historyDir;
  const text = readText(dashboardPath);
  const { preamble, sections } = splitSections(text);
  const usage = usageSummary(14);

  const focus = classifyItems(sections.FOCUS || []);
  const todaySection = classifyItems(sections.TODAY || []);
  const upNext = classifyItems(sections['UP NEXT'] || []);
  const doneSection = classifyItems(sections.DONE || []);
  const aiLines = aiSnapshot(sections['AI DONE TODAY'] || []);

  const humanDone = [
    ...doneSection.done,
    ...focus.done,
    ...todaySection.done,
    ...upNext.done,
  ];
  const nextToday = [...focus.pending, ...todaySection.pending];

  const month = yesterday.slice(0, 7);
  const monthFile = ensureMonthHistoryFile(historyDir, month, paths);
  upsertHistory(monthFile, yesterday, humanDone, aiLines, usage, month);

  writeText(dashboardPath, buildNow(preamble, buildUsageSection(weeklyRows(usage, today)), nextToday, upNext.pending));

  const nextState = {
    ...rolloverState,
    lastRolloverDate: today,
    lastArchivedDate: yesterday,
  };
  saveJson(rolloverStatePath, nextState);

  process.stdout.write(`${JSON.stringify({
    ok: true,
    rolledOverTo: today,
    archivedDate: yesterday,
    humanDone: humanDone.length,
  }, null, 2)}\n`);
}

main();
