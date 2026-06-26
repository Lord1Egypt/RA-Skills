'use strict';

const fs = require('fs');
const path = require('path');

const DEFAULT_LIMIT = 10;

function getTrialStatePath(env = process.env) {
  return env.VOX_TRIAL_STATE_FILE || path.resolve(__dirname, '..', '.trial-state.json');
}

function getTrialLimit(env = process.env) {
  const value = Number(env.VOX_TRIAL_LIMIT || DEFAULT_LIMIT);
  return Number.isFinite(value) && value > 0 ? value : DEFAULT_LIMIT;
}

function readTrialState(env = process.env) {
  const filePath = getTrialStatePath(env);
  if (!fs.existsSync(filePath)) {
    return { used: 0, limit: getTrialLimit(env), calls: [] };
  }
  const state = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  return {
    used: Number(state.used || 0),
    limit: Number(state.limit || getTrialLimit(env)),
    calls: Array.isArray(state.calls) ? state.calls : []
  };
}

function writeTrialState(state, env = process.env) {
  const filePath = getTrialStatePath(env);
  fs.writeFileSync(filePath, JSON.stringify(state, null, 2));
}

function recordTrialCall({ requestId, callee, status }, env = process.env) {
  const state = readTrialState(env);
  const next = {
    used: state.used + 1,
    limit: state.limit,
    calls: [
      ...state.calls,
      {
        requestId,
        callee,
        status,
        createdAt: new Date().toISOString()
      }
    ].slice(-100)
  };
  writeTrialState(next, env);
  return next;
}

function formatTrialUsage(state) {
  if (!state) return '';
  const remaining = Math.max(0, Number(state.limit || DEFAULT_LIMIT) - Number(state.used || 0));
  return `试用额度：已使用 ${state.used}/${state.limit} 次，剩余 ${remaining} 次。`;
}

function formatTrialUsageWithRegistration(state, registerUrl = 'https://vox-ai.teddymobile.cn/trial/apply') {
  const usage = formatTrialUsage(state);
  if (!usage) return '';
  return `${usage} 下一步可选择：[注册正式账号] ${registerUrl} ｜ [继续试用] ｜ [我已有正式凭证]。`;
}

module.exports = {
  DEFAULT_LIMIT,
  formatTrialUsage,
  getTrialLimit,
  getTrialStatePath,
  readTrialState,
  recordTrialCall,
  writeTrialState,
  formatTrialUsageWithRegistration
};
