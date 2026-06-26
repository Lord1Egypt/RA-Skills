#!/usr/bin/env node

const path = require('path');

const { parseCli, ensureNoPositionals, parseDate, parseEnum, parseInteger, resolvePath } = require('./lib/cli/helpers');
const { writeHelp, writeJsonError, writeJsonSuccess } = require('./lib/output');
const { formatLocalDate, isValidDate } = require('./lib/core/fsrs-scheduler');
const { createRepository, DEFAULT_WORKSPACE_DIR } = require('./lib/core/vocab-db');
const { buildSessionContext } = require('./lib/services/session-context');

const DEFAULT_MEMORY_DIR = path.join(path.dirname(DEFAULT_WORKSPACE_DIR), 'memory');
const DEFAULT_MAX_DUE = 120;
const DEFAULT_MAX_PENDING = 120;

const HELP_TEXT = `
WordPal session context script
Usage:
  node session-context.js --mode <learn|report> [--today YYYY-MM-DD] [--workspace-dir <path>] [--memory-dir <path>] [--max-due 120] [--max-pending 120]

Output:
  Success prints { meta, data } JSON. data includes profile, progress, memory_digest, learner_memory, and mode-specific context.
`;

function parseInput(argv = process.argv.slice(2)) {
  const { values, positionals } = parseCli({
    argv,
    options: {
      help: { type: 'boolean', short: 'h' },
      mode: { type: 'string' },
      today: { type: 'string' },
      'workspace-dir': { type: 'string' },
      'memory-dir': { type: 'string' },
      'max-due': { type: 'string' },
      'max-pending': { type: 'string' },
      'max-orphan': { type: 'string' },
    },
  });
  ensureNoPositionals(positionals);

  if (values.help) {
    return { help: true };
  }

  return {
    help: false,
    mode: parseEnum(values.mode, '--mode', ['learn', 'report']),
    today: values.today ? parseDate(values.today, '--today', isValidDate) : formatLocalDate(),
    workspaceDir: values['workspace-dir']
      ? resolvePath(values['workspace-dir'], '--workspace-dir')
      : DEFAULT_WORKSPACE_DIR,
    memoryDir: values['memory-dir']
      ? resolvePath(values['memory-dir'], '--memory-dir')
      : DEFAULT_MEMORY_DIR,
    maxDue: values['max-due']
      ? parseInteger(values['max-due'], '--max-due', 10, 1000)
      : DEFAULT_MAX_DUE,
    maxPending: values['max-pending']
      ? parseInteger(values['max-pending'], '--max-pending', 10, 1000)
      : (
        values['max-orphan']
          ? parseInteger(values['max-orphan'], '--max-orphan', 10, 1000)
          : DEFAULT_MAX_PENDING
      ),
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
      const data = buildSessionContext({
        repo,
        today: input.today,
        mode: input.mode,
        memoryDir: input.memoryDir,
        maxDue: input.maxDue,
        maxPending: input.maxPending,
      });
      writeJsonSuccess({
        script: 'session-context',
        meta: {
          mode: input.mode,
          today: input.today,
          workspace_dir: input.workspaceDir,
          memory_dir: input.memoryDir,
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
