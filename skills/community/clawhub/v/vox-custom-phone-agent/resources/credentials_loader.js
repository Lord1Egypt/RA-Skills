'use strict';

const fs = require('fs');
const path = require('path');

function loadCredentials(env = process.env) {
  const localEnv = loadLocalDotEnv();
  let fileCredentials = {};
  const filePath = env.VOX_CREDENTIALS_FILE || localEnv.VOX_CREDENTIALS_FILE;
  if (filePath && fs.existsSync(filePath)) {
    fileCredentials = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  }

  const credentials = {
    appId: env.VOX_APP_ID || localEnv.VOX_APP_ID || fileCredentials.appId || fileCredentials.VOX_APP_ID || '',
    secret: env.VOX_SECRET || localEnv.VOX_SECRET || fileCredentials.secret || fileCredentials.VOX_SECRET || '',
    botId: env.VOX_BOT_ID || localEnv.VOX_BOT_ID || fileCredentials.botId || fileCredentials.VOX_BOT_ID || '',
    baseUrl: env.VOX_OUTBOUND_BASE_URL || localEnv.VOX_OUTBOUND_BASE_URL || fileCredentials.baseUrl || 'https://vox.teddymobile.cn',
    callQueryBaseUrl: env.VOX_CALL_QUERY_BASE_URL || localEnv.VOX_CALL_QUERY_BASE_URL || fileCredentials.callQueryBaseUrl || fileCredentials.VOX_CALL_QUERY_BASE_URL || '',
    trialMode: isTruthy(env.VOX_TRIAL_MODE || localEnv.VOX_TRIAL_MODE || fileCredentials.trialMode || fileCredentials.VOX_TRIAL_MODE),
    registerUrl: env.VOX_REGISTER_URL || localEnv.VOX_REGISTER_URL || fileCredentials.registerUrl || fileCredentials.VOX_REGISTER_URL || 'https://vox-ai.teddymobile.cn/trial/apply'
  };

  const missing = [];
  if (!credentials.appId) missing.push('VOX_APP_ID');
  if (!credentials.secret) missing.push('VOX_SECRET');

  return { credentials, missing, ok: missing.length === 0 };
}

function isTruthy(value) {
  return /^(1|true|yes|y|on)$/i.test(String(value || '').trim());
}

function loadLocalDotEnv() {
  const envPath = path.resolve(__dirname, '..', '.env');
  if (!fs.existsSync(envPath)) return {};
  const result = {};
  const content = fs.readFileSync(envPath, 'utf8');
  for (const line of content.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const index = trimmed.indexOf('=');
    if (index < 0) continue;
    const key = trimmed.slice(0, index).trim();
    const value = trimmed.slice(index + 1).trim().replace(/^['"]|['"]$/g, '');
    result[key] = value;
  }
  return result;
}

module.exports = { loadCredentials, loadLocalDotEnv };
