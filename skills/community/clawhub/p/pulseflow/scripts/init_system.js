#!/usr/bin/env node
const path = require('path');
const {
  buildDefaultConfig,
  buildDefaultRolloverState,
  buildDefaultSyncState,
  defaultNowContent,
  deriveRuntimePaths,
  ensureDir,
  ensureFile,
  exists,
  formatDateInTimeZone,
  historyMonthShell,
  isPlaceholderPath,
  loadJson,
  saveJson,
} = require('./_common');
const { installAgentLogRules } = require('./_agent_log_rules');

function createMonthHistoryFile(paths, month, today) {
  const monthFile = path.join(paths.historyDir, `${month}.md`);
  const content = historyMonthShell(paths, month);
  const created = ensureFile(monthFile, content);
  return { monthFile, created };
}

function main() {
  const paths = deriveRuntimePaths();
  const today = formatDateInTimeZone(new Date(), process.env.AI_WORKLOG_TIMEZONE || 'Asia/Shanghai');
  const month = today.slice(0, 7);
  const created = [];
  let config = null;

  ensureDir(paths.rootDir);
  ensureDir(paths.historyDir);
  ensureDir(paths.systemDir);

  if (ensureFile(paths.nowPath, defaultNowContent(paths))) {
    created.push(paths.nowPath);
  }

  const { monthFile, created: historyCreated } = createMonthHistoryFile(paths, month, today);
  if (historyCreated) {
    created.push(monthFile);
  }

  if (!exists(paths.configPath)) {
    config = buildDefaultConfig(paths, process.env.AI_WORKLOG_TIMEZONE || 'Asia/Shanghai');
    saveJson(paths.configPath, config);
    created.push(paths.configPath);
  }

  if (!config) {
    config = loadJson(paths.configPath, null);
  }

  if (!exists(paths.syncStatePath)) {
    const agentNames = Array.isArray(config && config.agents)
      ? config.agents.map((agent) => agent.name).filter(Boolean)
      : undefined;
    saveJson(paths.syncStatePath, buildDefaultSyncState(today, agentNames));
    created.push(paths.syncStatePath);
  }

  if (!exists(paths.rolloverStatePath)) {
    saveJson(paths.rolloverStatePath, buildDefaultRolloverState());
    created.push(paths.rolloverStatePath);
  }

  for (const agent of (config && config.agents) || []) {
    if (!agent || agent.enabled === false || !agent.name || !agent.reportsDir || isPlaceholderPath(agent.reportsDir)) {
      continue;
    }
    const logPath = path.join(agent.reportsDir, `${agent.name}-ai-log-${today}.jsonl`);
    if (ensureFile(logPath, '')) {
      created.push(logPath);
    }
  }

  const ruleInstallResults = installAgentLogRules({ config, paths });

  process.stdout.write(`${JSON.stringify({ ok: true, created, ruleInstallResults }, null, 2)}\n`);
}

main();
