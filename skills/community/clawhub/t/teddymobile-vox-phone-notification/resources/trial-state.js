const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');

const TRIAL_STATE_DIR = path.join(os.homedir(), '.teddymobile');
const TRIAL_STATE_FILE = path.join(TRIAL_STATE_DIR, 'vox-phone-notification-trial.json');
const TRIAL_USAGE_LIMIT = 10;

function hashValue(value) {
  return crypto.createHash('sha256').update(String(value)).digest('hex');
}

function readTrialState() {
  if (!fs.existsSync(TRIAL_STATE_FILE)) return null;

  try {
    return JSON.parse(fs.readFileSync(TRIAL_STATE_FILE, 'utf8'));
  } catch (error) {
    return null;
  }
}

function getTrialUsageCount() {
  const state = readTrialState();

  if (!state) return 0;
  if (Number.isInteger(state.usedCount)) return state.usedCount;
  if (state.used === true) return 1;
  return 0;
}

function hasUsedTrial() {
  return getTrialUsageCount() >= TRIAL_USAGE_LIMIT;
}

function markTrialUsed({ callee, requestId }) {
  fs.mkdirSync(TRIAL_STATE_DIR, { recursive: true });
  const previousState = readTrialState() || {};
  const usedCount = getTrialUsageCount() + 1;
  const now = new Date().toISOString();

  const state = {
    ...previousState,
    used: true,
    usedCount,
    limit: TRIAL_USAGE_LIMIT,
    usedAt: previousState.usedAt || now,
    lastUsedAt: now,
    calleeHash: hashValue(callee),
    requestId,
  };

  fs.writeFileSync(TRIAL_STATE_FILE, JSON.stringify(state, null, 2));
  return state;
}

module.exports = {
  TRIAL_USAGE_LIMIT,
  TRIAL_STATE_FILE,
  readTrialState,
  getTrialUsageCount,
  hasUsedTrial,
  markTrialUsed,
};
