#!/usr/bin/env node

const { AppError, EXIT_CODES } = require('./lib/errors');
const {
  ensureNoPositionals,
  parseCli,
  parseDate,
  parseEnum,
  parseInteger,
  resolvePath,
} = require('./lib/cli/helpers');
const { writeHelp, writeJsonError, writeJsonSuccess } = require('./lib/output');
const { formatLocalDate, isValidDate } = require('./lib/core/fsrs-scheduler');
const { ensureSafeWord, normalizeWord } = require('./lib/core/input-guard');
const { createRepository, DEFAULT_WORKSPACE_DIR } = require('./lib/core/vocab-db');
const { ALL_QUESTION_TYPES } = require('./lib/services/question-plan');
const { buildNextQuestion } = require('./lib/services/next-question');

const HELP_TEXT = `
WordPal 下一题准备脚本

用法:
  node next-question.js --mode learn --word <word> --item-type <pending|due> [--status <0-7>] [--difficulty-level <I|II|III|IV|V>] [--last-type <Q1..Q17>] [--validate] [--today YYYY-MM-DD] [--workspace-dir <path>]

输出:
  成功时输出 { meta, data } JSON，data 内包含可选的暂存结果与紧凑题型规划。
`;

function parseInput(argv = process.argv.slice(2)) {
  const { values, positionals } = parseCli({
    argv,
    options: {
      help: { type: 'boolean', short: 'h' },
      mode: { type: 'string' },
      word: { type: 'string' },
      'item-type': { type: 'string' },
      status: { type: 'string' },
      'difficulty-level': { type: 'string' },
      'last-type': { type: 'string' },
      validate: { type: 'boolean' },
      today: { type: 'string' },
      'workspace-dir': { type: 'string' },
    },
  });
  ensureNoPositionals(positionals);

  if (values.help) {
    return { help: true };
  }

  const word = normalizeWord(values.word);
  try {
    ensureSafeWord(word);
  } catch (error) {
    throw new AppError('INVALID_WORD', error.message, EXIT_CODES.INVALID_INPUT);
  }

  return {
    help: false,
    mode: parseEnum(values.mode, '--mode', ['learn']),
    word,
    itemType: parseEnum(values['item-type'], '--item-type', ['pending', 'due']),
    status: typeof values.status === 'string'
      ? parseInteger(values.status, '--status', 0, 7)
      : null,
    difficultyLevel: typeof values['difficulty-level'] === 'string'
      ? parseEnum(values['difficulty-level'], '--difficulty-level', ['I', 'II', 'III', 'IV', 'V'])
      : null,
    lastType: typeof values['last-type'] === 'string'
      ? parseEnum(values['last-type'], '--last-type', ALL_QUESTION_TYPES)
      : null,
    validate: !!values.validate,
    today: values.today ? parseDate(values.today, '--today', isValidDate) : formatLocalDate(),
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
      const data = buildNextQuestion({
        repo,
        input,
      });
      writeJsonSuccess({
        script: 'next-question',
        meta: {
          mode: input.mode,
          item_type: input.itemType,
          validate: input.validate,
          today: input.today,
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
