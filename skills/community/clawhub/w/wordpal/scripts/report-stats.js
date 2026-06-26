#!/usr/bin/env node

const { ensureNoPositionals, parseCli, parseDate, parseInteger, resolvePath } = require('./lib/cli/helpers');
const { writeHelp, writeJsonError, writeJsonSuccess } = require('./lib/output');
const { formatLocalDate, isValidDate } = require('./lib/core/fsrs-scheduler');
const { createRepository, DEFAULT_WORKSPACE_DIR } = require('./lib/core/vocab-db');
const { buildReportStats } = require('./lib/services/report-stats');

const HELP_TEXT = `
WordPal 报告统计脚本

用法:
  node report-stats.js [--today YYYY-MM-DD] [--days 7] [--top-risk 10] [--workspace-dir <path>]

输出:
  成功时输出 { meta, data } JSON，data 内包含 totals/due/trend_7d/risk_words/next_action。
`;

function parseInput(argv = process.argv.slice(2)) {
  const { values, positionals } = parseCli({
    argv,
    options: {
      help: { type: 'boolean', short: 'h' },
      today: { type: 'string' },
      days: { type: 'string' },
      'top-risk': { type: 'string' },
      'workspace-dir': { type: 'string' },
    },
  });
  ensureNoPositionals(positionals);

  if (values.help) {
    return { help: true };
  }

  return {
    help: false,
    today: values.today ? parseDate(values.today, '--today', isValidDate) : formatLocalDate(),
    days: values.days ? parseInteger(values.days, '--days', 1, 30) : 7,
    topRisk: values['top-risk'] ? parseInteger(values['top-risk'], '--top-risk', 1, 200) : 10,
    workspaceDir: values['workspace-dir']
      ? resolvePath(values['workspace-dir'], '--workspace-dir')
      : DEFAULT_WORKSPACE_DIR,
  };
}

function main() {
  try {
    const input = parseInput();
    if (input.help) {
      writeHelp(HELP_TEXT);
      return;
    }

    const repo = createRepository(input.workspaceDir);
    try {
      const data = buildReportStats({
        repo,
        today: input.today,
        days: input.days,
        topRisk: input.topRisk,
      });
      writeJsonSuccess({
        script: 'report-stats',
        meta: {
          today: input.today,
          days: input.days,
          top_risk: input.topRisk,
          workspace_dir: input.workspaceDir,
        },
        data,
      });
    } finally {
      repo.close();
    }
  } catch (error) {
    writeJsonError(error);
  }
}

main();
