const { normalizeError } = require('./errors');

const SCHEMA_VERSION = '2026-03-15';

function writeLine(stream, value) {
  stream.write(`${value}\n`);
}

function writeJson(stream, payload) {
  writeLine(stream, JSON.stringify(payload, null, 2));
}

function writeJsonSuccess({ script, meta = {}, data }) {
  writeJson(process.stdout, {
    meta: {
      script,
      schema_version: SCHEMA_VERSION,
      generated_at: new Date().toISOString(),
      ...meta,
    },
    data,
  });
}

function writeJsonError(error) {
  const normalized = normalizeError(error);
  const payload = {
    error: {
      code: normalized.code,
      message: normalized.message,
    },
  };

  if (normalized.details !== undefined) {
    payload.error.details = normalized.details;
  }

  writeJson(process.stderr, payload);
  process.exitCode = normalized.exitCode;
}

function writeText(value) {
  writeLine(process.stdout, value);
}

function writeHelp(helpText) {
  writeLine(process.stdout, helpText.trimEnd());
}

module.exports = {
  SCHEMA_VERSION,
  writeHelp,
  writeJsonError,
  writeJsonSuccess,
  writeText,
};
