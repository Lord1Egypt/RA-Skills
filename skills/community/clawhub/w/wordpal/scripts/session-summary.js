#!/usr/bin/env node

const {
  ensureNoPositionals,
  parseCli,
  parseDate,
  parseEnum,
  parseInteger,
  requireString,
  resolvePath,
} = require('./lib/cli/helpers');
const { writeHelp, writeJsonError, writeJsonSuccess } = require('./lib/output');
const { formatLocalDate, isValidDate } = require('./lib/core/fsrs-scheduler');
const { ensureValidOpId } = require('./lib/core/input-guard');
const { createRepository, DEFAULT_WORKSPACE_DIR } = require('./lib/core/vocab-db');
const { buildSessionSummary } = require('./lib/services/session-summary');
const { AppError, EXIT_CODES } = require('./lib/errors');

const HELP_TEXT = `
WordPal 会话汇总脚本

用法:
  node session-summary.js --mode <learn> --op-ids "id1,id2,..." [--today YYYY-MM-DD] [--top-risk 5] [--workspace-dir <path>]

输出:
  成功时输出 { meta, data } JSON，data 内包含本轮事件计数、升级词、风险词和下次复习汇总。
`;

function parseOpIds(raw) {
  const values = requireString(raw, '--op-ids')
    .split(',')
    .map((value) => value.trim())
    .filter(Boolean);

  if (values.length === 0) {
    throw new AppError('INVALID_ARGUMENTS', 'Missing required --op-ids', EXIT_CODES.INVALID_INPUT);
  }

  const seen = new Set();
  const opIds = [];
  for (const value of values) {
    try {
      ensureValidOpId(value);
    } catch (error) {
      throw new AppError('INVALID_OP_ID', error.message, EXIT_CODES.INVALID_INPUT);
    }
    if (seen.has(value)) continue;
    seen.add(value);
    opIds.push(value);
  }

  return opIds;
}

function parseInput(argv = process.argv.slice(2)) {
  const { values, positionals } = parseCli({
    argv,
    options: {
      help: { type: 'boolean', short: 'h' },
      mode: { type: 'string' },
      'op-ids': { type: 'string' },
      today: { type: 'string' },
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
    mode: parseEnum(values.mode, '--mode', ['learn']),
    opIds: parseOpIds(values['op-ids']),
    today: values.today ? parseDate(values.today, '--today', isValidDate) : formatLocalDate(),
    topRisk: values['top-risk'] ? parseInteger(values['top-risk'], '--top-risk', 1, 20) : 5,
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
      const data = buildSessionSummary({
        repo,
        mode: input.mode,
        opIds: input.opIds,
        today: input.today,
        topRisk: input.topRisk,
      });
      writeJsonSuccess({
        script: 'session-summary',
        meta: {
          mode: input.mode,
          op_ids_count: input.opIds.length,
          today: input.today,
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
