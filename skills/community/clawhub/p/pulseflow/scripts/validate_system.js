#!/usr/bin/env node
const fs = require('fs');
const os = require('os');
const path = require('path');
const cp = require('child_process');

const SCRIPT_DIR = __dirname;
const NODE = process.execPath;

function runScript(scriptName, extraEnv = {}) {
  const env = { ...process.env, ...extraEnv };
  const output = cp.execFileSync(NODE, [path.join(SCRIPT_DIR, scriptName)], {
    env,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  return JSON.parse(output);
}

function runScriptArgs(scriptName, args = [], extraEnv = {}) {
  const env = { ...process.env, ...extraEnv };
  const output = cp.execFileSync(NODE, [path.join(SCRIPT_DIR, scriptName), ...args], {
    env,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  return JSON.parse(output);
}

function write(filePath, content) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, content, 'utf8');
}

function read(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function shiftDate(date, deltaDays) {
  const base = new Date(`${date}T12:00:00.000Z`);
  base.setUTCDate(base.getUTCDate() + deltaDays);
  return base.toISOString().slice(0, 10);
}

function weekStart(date) {
  const base = new Date(`${date}T12:00:00.000Z`);
  const day = base.getUTCDay();
  const offset = day === 0 ? 6 : day - 1;
  return shiftDate(date, -offset);
}

function weekDates(date) {
  return Array.from({ length: 7 }, (_, index) => shiftDate(weekStart(date), index));
}

function clippedWeekLabel(date) {
  const monthPrefix = `${date.slice(0, 7)}-`;
  const dates = weekDates(date).filter((item) => item.startsWith(monthPrefix));
  return `## Week ${dates[0]} → ${dates[dates.length - 1]}`;
}

function main() {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'PulseFlow-'));
  const env = {
    AI_WORKLOG_ROOT: tempRoot,
    AI_WORKLOG_TIMEZONE: 'Asia/Shanghai',
  };

  const initResult = runScript('init_system.js', env);
  assert(initResult.ok === true, 'init_system.js did not return ok=true');

  const systemDir = path.join(tempRoot, 'system');
  const configPath = path.join(systemDir, 'config.json');
  const syncStatePath = path.join(systemDir, 'sync-state.json');
  const rolloverStatePath = path.join(systemDir, 'rollover-state.json');
  const dashboardPath = path.join(tempRoot, 'NOW.md');
  const historyDir = path.join(tempRoot, 'history');
  const reportsDir = path.join(tempRoot, 'reports');
  const mainAgentsPath = path.join(tempRoot, 'main-AGENTS.md');
  const cortexAgentsPath = path.join(tempRoot, 'cortex-AGENTS.md');
  const tradingAgentsPath = path.join(tempRoot, 'trading-AGENTS.md');
  const usageFixturePath = path.join(tempRoot, 'usage-summary.json');
  const today = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date());
  const currentWeek = Array.from({ length: 7 }, (_, index) => shiftDate(weekStart(today), index));
  const usageFixture = {
    updatedAt: Date.now(),
    days: 14,
    daily: currentWeek.map((date) => ({
      date,
      input: date === today ? 100 : 0,
      output: date === today ? 150 : 0,
      cacheRead: date === today ? 50 : 0,
      cacheWrite: date === today ? 200 : 0,
      totalTokens: date === today ? 500 : 0,
      totalCost: 0,
      inputCost: 0,
      outputCost: 0,
      cacheReadCost: 0,
      cacheWriteCost: 0,
      missingCostEntries: 0,
    })),
    totals: {
      input: 100,
      output: 150,
      cacheRead: 50,
      cacheWrite: 200,
      totalTokens: 500,
      totalCost: 0,
      inputCost: 0,
      outputCost: 0,
      cacheReadCost: 0,
      cacheWriteCost: 0,
      missingCostEntries: 0,
    },
  };
  write(usageFixturePath, `${JSON.stringify(usageFixture, null, 2)}\n`);
  const envWithUsage = { ...env, AI_WORKLOG_USAGE_JSON: usageFixturePath };

  const config = JSON.parse(read(configPath));
  const initHistoryPath = path.join(historyDir, `${today.slice(0, 7)}.md`);
  const initHistoryText = read(initHistoryPath);
  assert(initHistoryText.trim() === `# History - ${today.slice(0, 7)}`, 'init_system.js should create an empty month history shell');
  write(mainAgentsPath, '# Main AGENTS\n');
  write(cortexAgentsPath, '# Cortex AGENTS\n');
  write(tradingAgentsPath, '# Trading AGENTS\n');

  config.agents = [
    { name: 'main', enabled: true, reportsDir, agentsFilePath: mainAgentsPath },
    { name: 'cortex', enabled: true, reportsDir, agentsFilePath: cortexAgentsPath },
    { name: 'trading', enabled: false, reportsDir, agentsFilePath: tradingAgentsPath },
  ];
  config.syncStatePath = path.join(tempRoot, 'custom-system', 'sync-state.json');
  write(configPath, `${JSON.stringify(config, null, 2)}\n`);
  fs.mkdirSync(path.dirname(config.syncStatePath), { recursive: true });
  fs.renameSync(syncStatePath, config.syncStatePath);

  const customRolloverStatePath = path.join(path.dirname(config.syncStatePath), 'rollover-state.json');
  fs.renameSync(rolloverStatePath, customRolloverStatePath);
  const initReplay = runScript('init_system.js', { ...envWithUsage, AI_WORKLOG_CONFIG: configPath });
  assert(initReplay.ruleInstallResults.some((item) => item.agent === 'main' && item.status === 'updated'), 'init_system.js should install main AGENTS rule');
  assert(fs.existsSync(path.join(reportsDir, `main-ai-log-${today}.jsonl`)), 'init_system.js should create today main log file');
  assert(read(mainAgentsPath).includes('AI_WORKLOG_RULE_START'), 'main AGENTS missing managed AI log block');

  runScriptArgs('append_ai_log.js', [
    '--agent', 'main',
    '--reports-dir', reportsDir,
    '--task', '完成 JS 同步脚本',
    '--tokens', '120',
    '--ts', `${today}T09:00:00+08:00`,
  ], envWithUsage);
  fs.appendFileSync(path.join(reportsDir, `main-ai-log-${today}.jsonl`), '{bad json}\n', 'utf8');
  runScriptArgs('append_ai_log.js', [
    '--agent', 'main',
    '--reports-dir', reportsDir,
    '--task', '补验证脚本',
    '--tokens', '80',
    '--ts', `${today}T09:10:00+08:00`,
  ], envWithUsage);
  write(path.join(reportsDir, `cortex-ai-log-${today}.jsonl`), [
    JSON.stringify({ ts: `${today}T09:05:00+08:00`, agent: 'cortex', task: '整理文档入口', tokens: 50 }),
    JSON.stringify({ ts: `1999-01-01T00:00:00+08:00`, agent: 'cortex', task: '旧记录', tokens: 999 }),
    '',
  ].join('\n'));

  const syncResult = runScript('sync_ai_done.js', { ...envWithUsage, AI_WORKLOG_CONFIG: configPath });
  assert(syncResult.items === 3, 'sync_ai_done.js should keep exactly 3 valid items');
  assert(syncResult.total_tokens === 250, 'sync_ai_done.js should use fresh input+output total for today');
  assert(syncResult.sync_state === config.syncStatePath, 'sync_ai_done.js should honor custom syncStatePath');

  const syncedDashboard = read(dashboardPath);
  assert(syncedDashboard.includes('## AI USAGE THIS WEEK'), 'dashboard missing weekly usage panel');
  assert(syncedDashboard.includes(`| ${today} | 250 | 100 | 150 | 250 | 33.3% |`), 'usage panel row missing today usage');
  assert(syncedDashboard.includes('- main: 完成 JS 同步脚本'), 'main log entry missing');
  assert(syncedDashboard.includes('- cortex: 整理文档入口'), 'cortex log entry missing');
  assert(!/Total\s+tokens\s+today/i.test(syncedDashboard), 'AI DONE TODAY should not render the old total line');

  fs.unlinkSync(dashboardPath);
  fs.unlinkSync(config.syncStatePath);
  const repairResult = runScript('repair_system.js', { ...envWithUsage, AI_WORKLOG_CONFIG: configPath });
  assert(repairResult.ok === true, 'repair_system.js did not return ok=true');
  assert(fs.existsSync(dashboardPath), 'repair_system.js did not recreate NOW.md');
  assert(fs.existsSync(config.syncStatePath), 'repair_system.js did not recreate custom sync-state.json');
  assert(fs.existsSync(customRolloverStatePath), 'repair_system.js did not recreate rollover-state.json next to custom sync-state.json');

  write(dashboardPath, [
    '## AI USAGE THIS WEEK',
    '| Date | Total Tokens | Input | Output | Cache | Hit Rate |',
    '| --- | ---: | ---: | ---: | ---: | ---: |',
    `| ${today} | 250 | 100 | 150 | 250 | 33.3% |`,
    '| **Week Total** | **250** | **100** | **150** | **250** | **33.3%** |',
    '',
    '---',
    '## FOCUS',
    '- [ ] 保留到明天',
    '- [x] 已完成焦点任务',
    '',
    '## TODAY',
    '- [ ] 今日未完成',
    '- [x] 今日已完成',
    '',
    '## UP NEXT',
    '- [ ] 下周再做',
    '- [x] 不常见但已完成',
    '',
    '## DONE',
    '- [x] 原 DONE 事项',
    '',
    '---',
    '## AI DONE TODAY',
    '- main: 完成 JS 同步脚本',
    '- cortex: 整理文档入口',
    '',
  ].join('\n'));
  write(customRolloverStatePath, `${JSON.stringify({ lastRolloverDate: null, lastArchivedDate: null }, null, 2)}\n`);

  const rolloverFirst = runScript('rollover_now.js', { ...envWithUsage, AI_WORKLOG_CONFIG: configPath });
  assert(rolloverFirst.ok === true, 'rollover_now.js did not return ok=true on first run');
  const rolledDashboard = read(dashboardPath);
  assert(rolledDashboard.includes('## AI USAGE THIS WEEK'), 'rollover should preserve usage panel');
  assert(rolledDashboard.includes('## TODAY\n- [ ] 保留到明天\n- [ ] 今日未完成'), 'rollover did not carry pending FOCUS/TODAY into TODAY');
  assert(!rolledDashboard.includes('## TODAY\n- [ ]\n- [ ] 保留到明天'), 'rollover should not carry placeholder checkboxes into TODAY');
  assert(rolledDashboard.includes('## UP NEXT\n- [ ] 下周再做'), 'rollover did not preserve pending UP NEXT');
  assert(rolledDashboard.includes('## AI DONE TODAY\n- 暂无'), 'rollover did not reset AI DONE TODAY');
  const historyMonthPath = path.join(historyDir, `${rolloverFirst.archivedDate.slice(0, 7)}.md`);
  const historyText = read(historyMonthPath);
  assert(!historyText.includes('## YYYY-MM-DD'), 'history should not contain template placeholder sections');
  assert(historyText.includes(clippedWeekLabel(rolloverFirst.archivedDate)), 'history missing clipped week section');
  assert(historyText.includes('### AI Usage Weekly Summary'), 'history missing weekly usage summary block');
  assert(historyText.includes(`### ${rolloverFirst.archivedDate}`), 'history missing archived day section');
  assert(historyText.includes('#### Human Done'), 'history missing Human Done subsection');
  assert(historyText.includes('#### AI Done Today'), 'history missing AI Done Today subsection');
  assert(historyText.includes('- [x] 原 DONE 事项'), 'history missing archived DONE item');
  assert(historyText.includes('- [x] 已完成焦点任务'), 'history missing archived FOCUS item');
  assert(historyText.includes('- main: 完成 JS 同步脚本'), 'history missing AI snapshot');
  assert(!historyText.includes('## AI Usage Daily Summary'), 'history should no longer contain the old monthly daily usage summary block');

  const rolloverSecond = runScript('rollover_now.js', { ...envWithUsage, AI_WORKLOG_CONFIG: configPath });
  assert(rolloverSecond.skipped === true, 'rollover_now.js should skip repeated rollover on same day');

  const summary = {
    ok: true,
    tempRoot,
    checks: {
      init: true,
      append: true,
      installRules: true,
      sync: true,
      repair: true,
      rollover: true,
      idempotentRollover: true,
    },
  };

  process.stdout.write(`${JSON.stringify(summary, null, 2)}\n`);
}

main();
