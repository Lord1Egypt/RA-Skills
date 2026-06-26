const crypto = require('crypto');

const SAFE_WORD_PATTERN = /^[a-z][a-z0-9'-]{0,63}$/;
const HINT_TOKEN_PATTERN = /^[0-9a-f]{24}$/;
const RESERVED_WORD_KEYS = new Set([
  '__proto__',
  'prototype',
  'constructor',
  'toString',
  'valueOf',
  '__defineGetter__',
  '__defineSetter__',
  '__lookupGetter__',
  '__lookupSetter__',
  'hasOwnProperty',
  'isPrototypeOf',
  'propertyIsEnumerable',
]);

const VALID_EVENTS = new Set(['correct', 'wrong', 'remembered_after_hint', 'skip', 'unreviewed']);
const OP_ID_PATTERN = /^[A-Za-z0-9._:-]{1,128}$/;

const UPGRADE_MAP = {
  1: 2,
  2: 3,
  3: 4,
  4: 5,
  5: 6,
  6: 7,
  7: 8,
};

const DOWNGRADE_MAP = {
  1: 1,
  2: 1,
  3: 2,
  4: 3,
  5: 3,
  6: 3,
  7: 3,
};

const DEFAULT_NEW_WORD_STATUS = 3; // virtual baseline for pending words; status 3 = ❌

function normalizeWord(raw) {
  return String(raw || '')
    .trim()
    .toLowerCase()
    .replace(/[\u2018\u2019]/g, "'")
    .replace(/[\u2010-\u2015]/g, '-');
}

function isSafeWord(word) {
  if (!word) return false;
  if (RESERVED_WORD_KEYS.has(word)) return false;
  return SAFE_WORD_PATTERN.test(word);
}

function ensureSafeWord(word) {
  if (!isSafeWord(word)) {
    throw new Error(`invalid word key: "${String(word)}"`);
  }
}

function ensureValidEvent(event) {
  if (!VALID_EVENTS.has(event)) {
    throw new Error(`invalid event: "${String(event)}"`);
  }
}

function ensureValidOpId(opId) {
  if (!OP_ID_PATTERN.test(opId)) {
    throw new Error('invalid --op-id format');
  }
}

function ensureValidHintToken(token) {
  if (!HINT_TOKEN_PATTERN.test(token)) {
    throw new Error('invalid --hint-token format');
  }
}

function resolveStatusFromEvent(previousStatus, event, fallbackStatus = DEFAULT_NEW_WORD_STATUS) {
  ensureValidEvent(event);

  const baseStatus = Number.isInteger(previousStatus) ? previousStatus : fallbackStatus;

  if (event === 'skip') {
    return 8;
  }

  if (event === 'unreviewed') {
    return fallbackStatus;
  }

  if (event === 'remembered_after_hint') {
    return 4;
  }

  if (event === 'correct') {
    const nextStatus = UPGRADE_MAP[baseStatus];
    if (Number.isInteger(nextStatus)) return nextStatus;
    throw new Error(`event "correct" expects an upgradable status, got ${String(baseStatus)}`);
  }

  if (event === 'wrong') {
    const nextStatus = DOWNGRADE_MAP[baseStatus];
    if (Number.isInteger(nextStatus)) return nextStatus;
    throw new Error(`event "wrong" expects a downgradeable status, got ${String(baseStatus)}`);
  }

  throw new Error(`unsupported event: "${String(event)}"`);
}

function validateEventTransition(input) {
  const {
    previousStatus,
    nextStatus,
    event,
    lastReviewed,
  } = input;

  ensureValidEvent(event);

  if (!Number.isInteger(nextStatus) || nextStatus < 1 || nextStatus > 8) {
    throw new Error(`invalid status transition target: ${String(nextStatus)}`);
  }

  if (event === 'skip') {
    if (nextStatus !== 8) {
      throw new Error('event "skip" must set status=8');
    }
    return;
  }

  if (event === 'unreviewed') {
    return;
  }

  if (lastReviewed === 'never') {
    throw new Error(`event "${event}" requires a reviewed date, not "never"`);
  }

  if (event === 'remembered_after_hint') {
    if (nextStatus !== 4) {
      throw new Error('event "remembered_after_hint" must set status=4');
    }
    return;
  }

  if (!Number.isInteger(previousStatus)) {
    return;
  }

  if (event === 'correct') {
    const expected = UPGRADE_MAP[previousStatus];
    if (!Number.isInteger(expected) || nextStatus !== expected) {
      throw new Error(`event "correct" expects status ${expected}, got ${nextStatus}`);
    }
    return;
  }

  if (event === 'wrong') {
    const expected = DOWNGRADE_MAP[previousStatus];
    if (!Number.isInteger(expected) || nextStatus !== expected) {
      throw new Error(`event "wrong" expects status ${expected}, got ${nextStatus}`);
    }
  }
}

function deriveOpId(input) {
  return crypto.createHash('sha256').update(input).digest('hex').slice(0, 24);
}

module.exports = {
  VALID_EVENTS,
  OP_ID_PATTERN,
  HINT_TOKEN_PATTERN,
  deriveOpId,
  normalizeWord,
  isSafeWord,
  ensureSafeWord,
  ensureValidEvent,
  ensureValidOpId,
  ensureValidHintToken,
  resolveStatusFromEvent,
  validateEventTransition,
};
