const path = require('path');
const { parseArgs } = require('node:util');

const { AppError, EXIT_CODES } = require('../errors');

function parseCli({ argv = process.argv.slice(2), options, allowPositionals = false }) {
  try {
    return parseArgs({
      args: argv,
      options,
      allowPositionals,
      strict: true,
    });
  } catch (error) {
    throw new AppError('INVALID_ARGUMENTS', error.message, EXIT_CODES.INVALID_INPUT);
  }
}

function ensureNoPositionals(positionals) {
  if (positionals.length > 0) {
    throw new AppError(
      'INVALID_ARGUMENTS',
      `Unknown positional argument: "${positionals[0]}"`,
      EXIT_CODES.INVALID_INPUT,
    );
  }
}

function requireString(value, label) {
  if (typeof value !== 'string' || value.trim() === '') {
    throw new AppError(
      'INVALID_ARGUMENTS',
      `Missing required ${label}`,
      EXIT_CODES.INVALID_INPUT,
    );
  }
  return value.trim();
}

function parseInteger(value, label, min, max) {
  const parsed = Number.parseInt(requireString(value, label), 10);
  if (!Number.isInteger(parsed) || parsed < min || parsed > max) {
    throw new AppError(
      'INVALID_ARGUMENTS',
      `Invalid ${label}: expected integer in [${min}, ${max}]`,
      EXIT_CODES.INVALID_INPUT,
    );
  }
  return parsed;
}

function parseDate(value, label, isValidDate, allowNever = false) {
  const raw = requireString(value, label);
  if (!isValidDate(raw, allowNever)) {
    throw new AppError(
      'INVALID_DATE',
      `Invalid ${label} date, expected YYYY-MM-DD${allowNever ? ' or never' : ''}`,
      EXIT_CODES.INVALID_INPUT,
    );
  }
  return raw;
}

function parseEnum(value, label, allowedValues) {
  const raw = requireString(value, label);
  if (!allowedValues.includes(raw)) {
    throw new AppError(
      'INVALID_ARGUMENTS',
      `Invalid ${label}: expected one of ${allowedValues.join(', ')}`,
      EXIT_CODES.INVALID_INPUT,
    );
  }
  return raw;
}

function resolvePath(value, label) {
  return path.resolve(requireString(value, label));
}

module.exports = {
  ensureNoPositionals,
  parseCli,
  parseDate,
  parseEnum,
  parseInteger,
  requireString,
  resolvePath,
};
