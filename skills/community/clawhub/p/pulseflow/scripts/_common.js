const fs = require('fs');
const path = require('path');

const FALLBACK_ROOT = process.env.AI_WORKLOG_ROOT || path.resolve(process.cwd(), 'todo');
const DEFAULT_TIME_ZONE = process.env.AI_WORKLOG_TIMEZONE || 'Asia/Shanghai';
const DEFAULT_REPORT_DIRS = {
  main: process.env.AI_WORKLOG_MAIN_REPORTS || '/ABSOLUTE/PATH/TO/reports',
  cortex: process.env.AI_WORKLOG_CORTEX_REPORTS || '/ABSOLUTE/PATH/TO/reports',
  trading: process.env.AI_WORKLOG_TRADING_REPORTS || '/ABSOLUTE/PATH/TO/reports',
};

function deriveRuntimePaths() {
  const skillDir = process.env.AI_WORKLOG_SKILL_DIR || path.resolve(__dirname, '..');
  const configPath = process.env.AI_WORKLOG_CONFIG
    ? path.resolve(process.env.AI_WORKLOG_CONFIG)
    : path.join(path.resolve(process.env.AI_WORKLOG_ROOT || FALLBACK_ROOT), 'system', 'config.json');
  const systemDir = path.dirname(configPath);
  const rootDir = path.dirname(systemDir);

  return {
    skillDir,
    rootDir,
    systemDir,
    configPath,
    nowPath: path.join(rootDir, 'NOW.md'),
    historyDir: path.join(rootDir, 'history'),
    syncStatePath: path.join(systemDir, 'sync-state.json'),
    rolloverStatePath: path.join(systemDir, 'rollover-state.json'),
    templateDir: path.join(skillDir, 'references'),
  };
}

function exists(filePath) {
  return fs.existsSync(filePath);
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function readText(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

function writeText(filePath, content) {
  ensureDir(path.dirname(filePath));
  fs.writeFileSync(filePath, content, 'utf8');
}

function ensureFile(filePath, content) {
  if (exists(filePath)) {
    return false;
  }
  writeText(filePath, content);
  return true;
}

function loadJson(filePath, defaultValue) {
  if (!exists(filePath)) {
    return defaultValue;
  }
  return JSON.parse(readText(filePath));
}

function saveJson(filePath, value) {
  writeText(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

function fillTemplate(template, replacements) {
  return Object.entries(replacements)
    .sort((a, b) => b[0].length - a[0].length)
    .reduce((output, [needle, value]) => output.split(needle).join(value), template);
}

function formatDateInTimeZone(date = new Date(), timeZone = DEFAULT_TIME_ZONE) {
  const formatter = new Intl.DateTimeFormat('en-CA', {
    timeZone,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
  const parts = Object.fromEntries(
    formatter
      .formatToParts(date)
      .filter((part) => part.type !== 'literal')
      .map((part) => [part.type, part.value]),
  );
  return `${parts.year}-${parts.month}-${parts.day}`;
}

function defaultNowContent(paths) {
  const templatePath = path.join(paths.templateDir, 'now-template.md');
  if (exists(templatePath)) {
    return readText(templatePath);
  }
  return '## AI USAGE THIS WEEK\n| Date | Total Tokens | Input | Output | Cache | Hit Rate |\n| --- | ---: | ---: | ---: | ---: | ---: |\n| 2026-04-07 | 0 | 0 | 0 | 0 | 0.0% |\n| 2026-04-08 | 0 | 0 | 0 | 0 | 0.0% |\n| 2026-04-09 | 0 | 0 | 0 | 0 | 0.0% |\n| 2026-04-10 | 0 | 0 | 0 | 0 | 0.0% |\n| 2026-04-11 | 0 | 0 | 0 | 0 | 0.0% |\n| 2026-04-12 | 0 | 0 | 0 | 0 | 0.0% |\n| 2026-04-13 | 0 | 0 | 0 | 0 | 0.0% |\n| **Week Total** | **0** | **0** | **0** | **0** | **0.0%** |\n\n---\n## FOCUS\n- [ ]\n\n## TODAY\n- [ ]\n\n## UP NEXT\n- [ ]\n\n## DONE\n- [x]\n\n---\n## AI DONE TODAY\n- 暂无\n';
}

function defaultHistoryMonthContent(paths, month, date) {
  const templatePath = path.join(paths.templateDir, 'history-template.md');
  if (exists(templatePath)) {
    return fillTemplate(readText(templatePath), {
      'YYYY-MM-DD': date,
      'YYYY-MM': month,
    });
  }
  return `# History - ${month}\n\n## ${date}\n\n### Human Done\n- [x]\n\n### AI Done Today\n- agent: task\n`;
}

function historyMonthShell(paths, month) {
  const templatePath = path.join(paths.templateDir, 'history-template.md');
  if (exists(templatePath)) {
    const template = readText(templatePath);
    const firstLine = template.split(/\r?\n/, 1)[0] || '# History - YYYY-MM';
    return `${firstLine.replace('YYYY-MM', month)}\n\n`;
  }
  return `# History - ${month}\n\n`;
}

function buildDefaultConfig(paths, timeZone = DEFAULT_TIME_ZONE) {
  return {
    version: 1,
    timezone: timeZone,
    dashboardPath: paths.nowPath,
    historyDir: paths.historyDir,
    syncStatePath: paths.syncStatePath,
    agents: Object.entries(DEFAULT_REPORT_DIRS).map(([name, reportsDir]) => ({
      name,
      enabled: true,
      reportsDir,
      agentsFilePath: '/ABSOLUTE/PATH/TO/AGENTS.md',
    })),
    notifications: {
      summaryCrons: {
        enabled: false,
        agentId: 'main',
        timezone: timeZone,
        archiveDir: '/ABSOLUTE/PATH/TO/reports',
        delivery: {
          channel: 'telegram',
          to: 'telegram:CHAT_ID',
          accountId: 'default',
        },
        midday: {
          enabled: true,
          name: 'PulseFlow Midday Summary',
          description: '15:30 midday summary with analysis and next-step suggestions',
          cron: '30 15 * * *',
          thinking: 'medium',
        },
        dailyClose: {
          enabled: true,
          name: 'PulseFlow Previous-Day Report',
          description: '00:05 previous-day report before rollover',
          cron: '5 0 * * *',
          thinking: 'medium',
        },
      },
    },
  };
}

function buildDefaultSyncState(today, agentNames = ['main', 'cortex', 'trading']) {
  const agents = {};
  for (const name of agentNames) {
    agents[name] = { lastFile: null, lastLine: 0 };
  }
  return {
    version: 1,
    date: today,
    lastSyncAt: null,
    agents,
  };
}

function buildDefaultRolloverState() {
  return {
    lastRolloverDate: null,
    lastArchivedDate: null,
  };
}

function resolveRolloverStatePath(cfg, paths) {
  if (process.env.AI_WORKLOG_ROLLOVER_STATE) {
    return path.resolve(process.env.AI_WORKLOG_ROLLOVER_STATE);
  }
  const syncStatePath = cfg && cfg.syncStatePath ? cfg.syncStatePath : paths.syncStatePath;
  return path.join(path.dirname(syncStatePath), 'rollover-state.json');
}

function unique(values) {
  return [...new Set(values)];
}

function isPlaceholderPath(value) {
  return typeof value === 'string' && value.includes('/ABSOLUTE/PATH/TO/');
}

module.exports = {
  DEFAULT_TIME_ZONE,
  buildDefaultConfig,
  buildDefaultRolloverState,
  buildDefaultSyncState,
  defaultHistoryMonthContent,
  defaultNowContent,
  deriveRuntimePaths,
  ensureDir,
  ensureFile,
  exists,
  fillTemplate,
  formatDateInTimeZone,
  historyMonthShell,
  isPlaceholderPath,
  loadJson,
  readText,
  resolveRolloverStatePath,
  saveJson,
  unique,
  writeText,
};
