#!/usr/bin/env node

const path = require('path');

const { parseCli, parseDate, parseInteger, resolvePath } = require('./lib/cli/helpers');
const { AppError, EXIT_CODES } = require('./lib/errors');
const { writeHelp, writeJsonError, writeJsonSuccess } = require('./lib/output');
const { DEFAULT_WORKSPACE_DIR } = require('./lib/core/vocab-db');
const { isValidDate } = require('./lib/core/fsrs-scheduler');
const {
  DIFFICULTY_LEVELS,
  LEARNING_GOALS,
  PROFILE_FILENAME,
  loadUserProfile,
  normalizePushTimesInput,
  toScriptProfile,
  writeUserProfile,
} = require('./lib/services/user-profile');

const HELP_TEXT = `
WordPal 用户画像脚本

用法:
  node profile.js get [--workspace-dir <path>]
  node profile.js set [--workspace-dir <path>] [--created YYYY-MM-DD] [--learning-goal <goal>] [--push-times "08:00, 20:00"] [--difficulty-level <I|II|III|IV|V>] [--daily-target <1-100>]

输出:
  成功时输出 { meta, data } JSON。get 返回 exists/profile，set 返回更新后的 profile 和 updated_fields。
`;

function parseSubcommand(positionals) {
  if (positionals.length === 0) {
    throw new AppError('INVALID_ARGUMENTS', 'Missing required subcommand: expected get or set', EXIT_CODES.INVALID_INPUT);
  }

  const [subcommand, ...rest] = positionals;
  if (!['get', 'set'].includes(subcommand)) {
    throw new AppError('INVALID_ARGUMENTS', `Unknown subcommand: "${subcommand}"`, EXIT_CODES.INVALID_INPUT);
  }
  if (rest.length > 0) {
    throw new AppError('INVALID_ARGUMENTS', `Unknown positional argument: "${rest[0]}"`, EXIT_CODES.INVALID_INPUT);
  }
  return subcommand;
}

function parseUpperEnum(value, label, allowedValues) {
  const normalized = typeof value === 'string' ? value.trim().toUpperCase() : '';
  if (!allowedValues.includes(normalized)) {
    throw new AppError(
      'INVALID_ARGUMENTS',
      `Invalid ${label}: expected one of ${allowedValues.join(', ')}`,
      EXIT_CODES.INVALID_INPUT,
    );
  }
  return normalized;
}

function parseSetPatch(values) {
  const patch = {};

  if (values.created) {
    patch.created = parseDate(values.created, '--created', isValidDate);
  }
  if (values['learning-goal']) {
    patch.learningGoal = parseUpperEnum(values['learning-goal'], '--learning-goal', LEARNING_GOALS);
  }
  if (values['push-times']) {
    patch.pushTimes = normalizePushTimesInput(values['push-times']);
  }
  if (values['difficulty-level']) {
    patch.difficultyLevel = parseUpperEnum(values['difficulty-level'], '--difficulty-level', DIFFICULTY_LEVELS);
  }
  if (values['daily-target']) {
    patch.dailyTarget = parseInteger(values['daily-target'], '--daily-target', 1, 100);
  }

  if (Object.keys(patch).length === 0) {
    throw new AppError(
      'INVALID_ARGUMENTS',
      'profile set requires at least one field to update',
      EXIT_CODES.INVALID_INPUT,
    );
  }

  return patch;
}

function parseInput(argv = process.argv.slice(2)) {
  const { values, positionals } = parseCli({
    argv,
    allowPositionals: true,
    options: {
      help: { type: 'boolean', short: 'h' },
      created: { type: 'string' },
      'daily-target': { type: 'string' },
      'difficulty-level': { type: 'string' },
      'learning-goal': { type: 'string' },
      'push-times': { type: 'string' },
      'workspace-dir': { type: 'string' },
    },
  });

  if (values.help) {
    return { help: true };
  }

  const action = parseSubcommand(positionals);
  return {
    help: false,
    action,
    workspaceDir: values['workspace-dir']
      ? resolvePath(values['workspace-dir'], '--workspace-dir')
      : DEFAULT_WORKSPACE_DIR,
    patch: action === 'set' ? parseSetPatch(values) : null,
  };
}

function main() {
  try {
    const input = parseInput();
    if (input.help) {
      writeHelp(HELP_TEXT);
      return;
    }

    const profileFile = path.join(input.workspaceDir, PROFILE_FILENAME);

    if (input.action === 'get') {
      const result = loadUserProfile(profileFile);
      writeJsonSuccess({
        script: 'profile',
        meta: {
          action: input.action,
          workspace_dir: input.workspaceDir,
          profile_file: profileFile,
        },
        data: {
          exists: result.exists,
          profile: toScriptProfile(result.profile),
        },
      });
      return;
    }

    const result = writeUserProfile(profileFile, input.patch);
    writeJsonSuccess({
      script: 'profile',
      meta: {
        action: input.action,
        workspace_dir: input.workspaceDir,
        profile_file: profileFile,
      },
      data: {
        exists: true,
        created: result.created,
        updated_fields: result.updatedFields,
        profile: toScriptProfile(result.profile),
      },
    });
  } catch (error) {
    writeJsonError(error);
  }
}

main();
