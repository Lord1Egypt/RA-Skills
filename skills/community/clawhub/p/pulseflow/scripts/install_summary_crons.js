#!/usr/bin/env node
const cp = require('child_process');
const path = require('path');
const {
  DEFAULT_TIME_ZONE,
  deriveRuntimePaths,
  ensureDir,
  isPlaceholderPath,
  loadJson,
} = require('./_common');

const DEFAULTS = {
  midday: {
    name: 'PulseFlow Midday Summary',
    description: '15:30 midday summary with analysis and next-step suggestions',
    cron: '30 15 * * *',
    thinking: 'medium',
  },
  dailyClose: {
    name: 'PulseFlow Previous-Day Report',
    description: '00:05 previous-day report before rollover',
    cron: '5 0 * * *',
    thinking: 'medium',
  },
};

function parseArgs(argv) {
  const options = { dryRun: false };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--dry-run') {
      options.dryRun = true;
      continue;
    }
    if (arg === '--config') {
      const value = argv[index + 1];
      if (!value) throw new Error('Missing value for --config');
      process.env.AI_WORKLOG_CONFIG = value;
      index += 1;
      continue;
    }
    throw new Error(`Unknown argument: ${arg}`);
  }
  return options;
}

function isUnset(value) {
  return value == null || String(value).trim() === '';
}

function looksPlaceholder(value) {
  if (isUnset(value)) return true;
  const text = String(value).trim();
  return text.includes('/ABSOLUTE/PATH/TO/') || text.includes('CHAT_ID') || text.includes('CHANGE_ME');
}

function mustString(value, name) {
  if (isUnset(value) || looksPlaceholder(value)) {
    throw new Error(`Missing or placeholder config value: ${name}`);
  }
  return String(value).trim();
}

function readConfig() {
  const paths = deriveRuntimePaths();
  const config = loadJson(paths.configPath, null);
  if (!config) {
    throw new Error('Missing config.json: run init_system.js first or pass --config');
  }
  return { paths, config };
}

function resolveSummaryConfig(config) {
  const settings = config && config.notifications && config.notifications.summaryCrons;
  if (!settings || settings.enabled !== true) {
    return { enabled: false };
  }

  const timezone = String(settings.timezone || config.timezone || DEFAULT_TIME_ZONE).trim();
  const agentId = mustString(settings.agentId, 'notifications.summaryCrons.agentId');
  const archiveDir = mustString(settings.archiveDir, 'notifications.summaryCrons.archiveDir');
  if (isPlaceholderPath(archiveDir)) {
    throw new Error('notifications.summaryCrons.archiveDir still contains a placeholder path');
  }

  const delivery = settings.delivery || {};
  const channel = mustString(delivery.channel, 'notifications.summaryCrons.delivery.channel');
  const to = mustString(delivery.to, 'notifications.summaryCrons.delivery.to');
  const accountId = looksPlaceholder(delivery.accountId) ? null : String(delivery.accountId || '').trim() || null;

  return {
    enabled: true,
    agentId,
    timezone,
    archiveDir,
    delivery: { channel, to, accountId },
    midday: {
      enabled: settings.midday ? settings.midday.enabled !== false : true,
      ...DEFAULTS.midday,
      ...(settings.midday || {}),
    },
    dailyClose: {
      enabled: settings.dailyClose ? settings.dailyClose.enabled !== false : true,
      ...DEFAULTS.dailyClose,
      ...(settings.dailyClose || {}),
    },
  };
}

function archivePaths(archiveDir) {
  return {
    root: archiveDir,
    dailyReports: path.join(archiveDir, 'daily-reports'),
    midday: path.join(archiveDir, 'cron-summaries', 'midday'),
    dailyClose: path.join(archiveDir, 'cron-summaries', 'daily-close'),
  };
}

function execJson(args) {
  const raw = cp.execFileSync('openclaw', args, { encoding: 'utf8' });
  return JSON.parse(raw);
}

function enabledAgents(config) {
  return (config.agents || []).filter((agent) => agent && agent.enabled !== false && !looksPlaceholder(agent.reportsDir));
}

function buildOptionalStatusHints(config) {
  return enabledAgents(config)
    .map((agent) => `- ${path.join(agent.reportsDir, `${agent.name}-status.json`)}`)
    .join('\n');
}

function buildLogHints(config, dateToken) {
  return enabledAgents(config)
    .map((agent) => `- ${path.join(agent.reportsDir, `${agent.name}-ai-log-${dateToken}.jsonl`)}`)
    .join('\n');
}

function buildMiddayMessage({ paths, config, summary, archives }) {
  const dashboardPath = config.dashboardPath || paths.nowPath;
  const statusHints = buildOptionalStatusHints(config);
  const logHints = buildLogHints(config, 'YYYY-MM-DD');
  return [
    'First call session_status to confirm the current date and local time.',
    `Read the template at ${path.join(paths.templateDir, 'midday-summary-template.md')}.`,
    `Read the current PulseFlow dashboard at ${dashboardPath}.`,
    `Read today's enabled-agent AI logs using these path patterns:\n${logHints || '- (none configured)'}`,
    statusHints ? `If these optional same-day status files exist, use them only as supplementary context:\n${statusHints}` : 'Optional agent status files may be used only if they exist.',
    'Read current OpenClaw usage data for today when needed (for example via openclaw gateway usage-cost --days 1 --json).',
    'Stay inside the PulseFlow runtime only. Do not read old task systems, migration leftovers, or unrelated registries.',
    'Generate one midday summary using the template structure, but write naturally and with judgment.',
    `Write the final markdown body to ${path.join(archives.midday, 'YYYY-MM-DD.md')} using today\'s date.`,
    'Do not use the message tool. Cron delivery will announce your final response.',
    'Return only the final user-facing summary body as your final answer.',
  ].join(' ');
}

function buildDailyCloseMessage({ paths, config, summary, archives }) {
  const dashboardPath = config.dashboardPath || paths.nowPath;
  const statusHints = buildOptionalStatusHints(config);
  const logHints = buildLogHints(config, 'YYYY-MM-DD');
  return [
    'First call session_status to confirm the current date and local time, then determine yesterday\'s date.',
    'Treat the current NOW.md as yesterday\'s end-of-day snapshot because this job is meant to run before rollover.',
    `Read the template at ${path.join(paths.templateDir, 'daily-close-template.md')}.`,
    `Read the current PulseFlow dashboard at ${dashboardPath}.`,
    `Read yesterday\'s enabled-agent AI logs using these path patterns:\n${logHints || '- (none configured)'}`,
    statusHints ? `If these optional same-day status files exist, use them only as supplementary context for AI completions and remarks, never for task lists:\n${statusHints}` : 'Optional agent status files may be used only as supplementary context for AI completions and remarks.',
    'Read yesterday\'s usage data when needed (for example via openclaw gateway usage-cost --days 2 --json).',
    'Keep task sourcing strict: pending and long-term task lists must come from NOW.md only. Do not pull blockers, pending items, or next steps out of status files and write them back as task-list items.',
    'Generate one previous-day report using the template structure, but write naturally and with judgment.',
    `Write the final markdown body to ${path.join(archives.dailyReports, 'YYYY-MM-DD.md')} using the date being summarized.`,
    'Do not use the message tool. Cron delivery will announce your final response.',
    'Return only the final user-facing report body as your final answer.',
  ].join(' ');
}

function currentJobsByName() {
  const listed = execJson(['cron', 'list', '--json']);
  const map = new Map();
  for (const job of listed.jobs || []) {
    if (job && job.name) {
      map.set(job.name, job);
    }
  }
  return map;
}

function ensureArchiveDirs(archives, dryRun) {
  const dirs = [archives.root, archives.dailyReports, archives.midday, archives.dailyClose];
  if (!dryRun) {
    dirs.forEach((dirPath) => ensureDir(dirPath));
  }
  return dirs;
}

function jobArgs({ existing, agentId, timezone, delivery, spec, message }) {
  const args = existing ? ['cron', 'edit', existing.id] : ['cron', 'add'];
  args.push('--json');
  args.push('--agent', agentId);
  args.push('--name', spec.name);
  args.push('--description', spec.description);
  args.push('--cron', spec.cron);
  args.push('--tz', timezone);
  args.push('--exact');
  args.push('--session', 'isolated');
  args.push('--announce');
  args.push('--channel', delivery.channel);
  args.push('--to', delivery.to);
  if (delivery.accountId) {
    args.push('--account', delivery.accountId);
  }
  if (spec.thinking) {
    args.push('--thinking', String(spec.thinking));
  }
  args.push('--message', message);
  if (existing) {
    args.push('--enable');
  }
  return args;
}

function disableArgs(existing) {
  return ['cron', 'edit', existing.id, '--json', '--disable'];
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  const { paths, config } = readConfig();
  const summary = resolveSummaryConfig(config);

  if (!summary.enabled) {
    process.stdout.write(`${JSON.stringify({ ok: true, skipped: true, reason: 'summary crons disabled or missing' }, null, 2)}\n`);
    return;
  }

  const archives = archivePaths(summary.archiveDir);
  const preparedDirs = ensureArchiveDirs(archives, options.dryRun);
  const jobsByName = currentJobsByName();
  const results = [];

  const specs = [
    {
      key: 'midday',
      spec: summary.midday,
      message: buildMiddayMessage({ paths, config, summary, archives }),
    },
    {
      key: 'dailyClose',
      spec: summary.dailyClose,
      message: buildDailyCloseMessage({ paths, config, summary, archives }),
    },
  ];

  for (const item of specs) {
    const existing = jobsByName.get(item.spec.name);
    if (item.spec.enabled === false) {
      if (existing) {
        if (options.dryRun) {
          results.push({ name: item.spec.name, action: 'disable', id: existing.id });
        } else {
          results.push({ name: item.spec.name, action: 'disabled', ...(execJson(disableArgs(existing))) });
        }
      } else {
        results.push({ name: item.spec.name, action: 'skipped-disabled-not-found' });
      }
      continue;
    }

    const args = jobArgs({
      existing,
      agentId: summary.agentId,
      timezone: summary.timezone,
      delivery: summary.delivery,
      spec: item.spec,
      message: item.message,
    });

    if (options.dryRun) {
      results.push({
        name: item.spec.name,
        action: existing ? 'edit' : 'add',
        command: ['openclaw', ...args].join(' '),
      });
    } else {
      const output = execJson(args);
      results.push({ name: item.spec.name, action: existing ? 'updated' : 'created', id: output.id || existing?.id || null });
    }
  }

  process.stdout.write(`${JSON.stringify({
    ok: true,
    dryRun: options.dryRun,
    configPath: paths.configPath,
    preparedDirs,
    results,
  }, null, 2)}\n`);
}

main();
