#!/usr/bin/env node
const {
  buildDefaultRolloverState,
  buildDefaultSyncState,
  defaultNowContent,
  deriveRuntimePaths,
  exists,
  formatDateInTimeZone,
  loadJson,
  resolveRolloverStatePath,
  saveJson,
  writeText,
} = require('./_common');

function main() {
  const paths = deriveRuntimePaths();
  const today = formatDateInTimeZone(new Date(), process.env.AI_WORKLOG_TIMEZONE || 'Asia/Shanghai');
  const repaired = [];

  if (!exists(paths.configPath)) {
    throw new Error('Missing config.json: run init_system.js first');
  }

  const config = loadJson(paths.configPath, null);
  const dashboardPath = config && config.dashboardPath ? config.dashboardPath : paths.nowPath;
  const syncStatePath = config && config.syncStatePath ? config.syncStatePath : paths.syncStatePath;
  const rolloverStatePath = resolveRolloverStatePath(config, paths);

  if (!exists(dashboardPath)) {
    writeText(dashboardPath, defaultNowContent(paths));
    repaired.push('NOW.md');
  }

  if (!exists(syncStatePath)) {
    const agentNames = Array.isArray(config && config.agents)
      ? config.agents.map((agent) => agent.name).filter(Boolean)
      : ['main', 'cortex', 'trading'];
    saveJson(syncStatePath, buildDefaultSyncState(today, agentNames));
    repaired.push('sync-state.json');
  }

  if (!exists(rolloverStatePath)) {
    saveJson(rolloverStatePath, buildDefaultRolloverState());
    repaired.push('rollover-state.json');
  }

  process.stdout.write(`${JSON.stringify({ ok: true, repaired }, null, 2)}\n`);
}

main();
