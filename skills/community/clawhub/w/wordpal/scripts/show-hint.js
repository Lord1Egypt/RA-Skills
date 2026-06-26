#!/usr/bin/env node

const { AppError, EXIT_CODES } = require('./lib/errors');
const { ensureNoPositionals, parseCli, resolvePath } = require('./lib/cli/helpers');
const { writeHelp, writeJsonError, writeJsonSuccess } = require('./lib/output');
const { ensureSafeWord, normalizeWord } = require('./lib/core/input-guard');
const { createRepository, DEFAULT_WORKSPACE_DIR } = require('./lib/core/vocab-db');
const { showHint } = require('./lib/services/show-hint');

const HELP_TEXT = `
WordPal 显示提示脚本

用法:
  node show-hint.js --word <word> [--workspace-dir <path>]

说明:
  答错时必须先调用本脚本获取 hint_token，再向用户展示解析，
  完成 B-3 子流程后才可调用 submit-answer.js。

输出:
  成功时输出 { meta, data } JSON。
  data.hint_token 为一次性令牌，提交 wrong / remembered_after_hint 时必须携带。
`;

function parseInput(argv = process.argv.slice(2)) {
  const { values, positionals } = parseCli({
    argv,
    options: {
      help: { type: 'boolean', short: 'h' },
      word: { type: 'string' },
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
    word,
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
      const data = showHint({ repo, input });
      writeJsonSuccess({
        script: 'show-hint',
        meta: { workspace_dir: input.workspaceDir },
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
