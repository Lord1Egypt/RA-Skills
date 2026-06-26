#!/usr/bin/env node
const path = require('path');
const {
  buildDefaultSyncState,
  defaultNowContent,
  deriveRuntimePaths,
  exists,
  formatDateInTimeZone,
  loadJson,
  readText,
  saveJson,
  writeText,
} = require('./_common');
const {
  buildUsageSection,
  replaceUsageSection,
  todayUsage,
  usageSummary,
  weeklyRows,
} = require('./_usage_panel');

const AI_HEADER = '## AI DONE TODAY';
function parseJsonl(logPath, expectedAgent, expectedDate) {
  if (!exists(logPath)) {
    return [];
  }

  const lines = readText(logPath).split(/\r?\n/);
  const items = [];

  for (let index = 0; index < lines.length; index += 1) {
    const raw = lines[index].trim();
    if (!raw) continue;

    let obj;
    try {
      obj = JSON.parse(raw);
    } catch {
      continue;
    }

    const agent = String(obj.agent || '').trim();
    const task = String(obj.task || '').trim().replace(/\s*\n\s*/g, ' ');
    const ts = String(obj.ts || '').trim();
    const tokens = Number.isFinite(Number(obj.tokens)) ? Math.max(0, parseInt(obj.tokens, 10) || 0) : 0;

    if (agent !== expectedAgent || !task || !ts.includes(expectedDate)) {
      continue;
    }

    items.push({
      agent,
      task,
      ts,
      tokens,
      line: index + 1,
      file: logPath,
    });
  }

  return items;
}

function buildAiSection(items, usage) {
  const lines = [AI_HEADER];

  if (!items.length) {
    lines.push('');
    lines.push('- 暂无');
    return `${lines.join('\n')}\n`;
  }

  const sorted = [...items].sort((a, b) => {
    if (a.ts !== b.ts) return a.ts.localeCompare(b.ts);
    if (a.agent !== b.agent) return a.agent.localeCompare(b.agent);
    return a.line - b.line;
  });

  lines.push('');
  for (const item of sorted) {
    lines.push(`- ${item.agent}: ${item.task}`);
  }

  return `${lines.join('\n')}\n`;
}

function replaceAiSection(nowText, aiSection) {
  const marker = `\n${AI_HEADER}\n`;
  if (nowText.includes(`${AI_HEADER}\n`)) {
    const head = nowText.split(marker, 1)[0].replace(/\s*$/, '');
    const separator = head.endsWith('---') ? '\n' : '\n\n';
    return `${head}${separator}${aiSection.trimEnd()}\n`;
  }

  const trimmed = nowText.replace(/\s*$/, '');
  const separator = trimmed.endsWith('---') ? '\n' : '\n\n';
  return `${trimmed}${separator}${aiSection.trimEnd()}\n`;
}

function main() {
  const paths = deriveRuntimePaths();
  const config = loadJson(paths.configPath, null);
  if (!config) {
    throw new Error('Missing config.json: run init_system.js first');
  }

  const timeZone = config.timezone || process.env.AI_WORKLOG_TIMEZONE || 'Asia/Shanghai';
  const today = formatDateInTimeZone(new Date(), timeZone);
  const syncStatePath = config.syncStatePath || paths.syncStatePath;
  const existingState = loadJson(syncStatePath, buildDefaultSyncState(today));

  const allItems = [];
  const agentState = {};

  for (const agent of config.agents || []) {
    if (!agent || agent.enabled === false || !agent.name || !agent.reportsDir) {
      continue;
    }

    const logPath = path.join(agent.reportsDir, `${agent.name}-ai-log-${today}.jsonl`);
    const items = parseJsonl(logPath, agent.name, today);
    allItems.push(...items);
    agentState[agent.name] = {
      lastFile: exists(logPath) ? logPath : null,
      lastLine: items.length ? items[items.length - 1].line : 0,
    };
  }

  const dashboardPath = config.dashboardPath || paths.nowPath;
  const nowText = exists(dashboardPath) ? readText(dashboardPath) : defaultNowContent(paths);
  const usage = usageSummary(14);
  const todayUsageStats = todayUsage(usage, today);
  const usageSection = buildUsageSection(weeklyRows(usage, today));
  const aiSection = buildAiSection(allItems, todayUsageStats);
  const withUsage = replaceUsageSection(nowText, usageSection);
  const nextText = replaceAiSection(withUsage, aiSection);

  if (nextText !== nowText) {
    writeText(dashboardPath, nextText);
  }

  const nextState = {
    ...existingState,
    version: 1,
    date: today,
    lastSyncAt: new Date().toISOString(),
    agents: agentState,
  };
  saveJson(syncStatePath, nextState);

  process.stdout.write(`${JSON.stringify({
    date: today,
    items: allItems.length,
    total_tokens: todayUsageStats.totalTokens,
    dashboard: dashboardPath,
    sync_state: syncStatePath,
  }, null, 2)}\n`);
}

main();
