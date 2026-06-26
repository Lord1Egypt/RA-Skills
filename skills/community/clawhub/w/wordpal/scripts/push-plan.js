#!/usr/bin/env node

const { ensureNoPositionals, parseCli, resolvePath } = require('./lib/cli/helpers');
const { writeHelp, writeJsonError, writeJsonSuccess } = require('./lib/output');
const { DEFAULT_WORKSPACE_DIR } = require('./lib/core/vocab-db');
const { buildPushPlan } = require('./lib/services/push-plan');

const HELP_TEXT = `
WordPal 推送注册规划脚本

用法:
  node push-plan.js [--workspace-dir <path>]

输出:
  成功时输出 { meta, data } JSON，data.registrations 为标准化注册规格数组。
`;

function parseInput(argv = process.argv.slice(2)) {
  const { values, positionals } = parseCli({
    argv,
    options: {
      help: { type: 'boolean', short: 'h' },
      'workspace-dir': { type: 'string' },
    },
  });
  ensureNoPositionals(positionals);

  if (values.help) {
    return { help: true };
  }

  return {
    help: false,
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

    const data = buildPushPlan({
      workspaceDir: input.workspaceDir,
    });

    writeJsonSuccess({
      script: 'push-plan',
      meta: {
        workspace_dir: input.workspaceDir,
      },
      data,
    });
  } catch (error) {
    writeJsonError(error);
  }
}

main();
