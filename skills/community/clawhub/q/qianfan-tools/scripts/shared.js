const fs = require('fs');
const path = require('path');

const SKILL_ROOT = path.resolve(__dirname, '..');
const CONFIG_PATH = path.join(SKILL_ROOT, 'config.json');

/**
 * Resolve apiKey with priority:
 * 1. BAIDU_API_KEY env var (injected by OpenClaw/ClawHub platform)
 * 2. Local config.json (for local / self-hosted use)
 */
function resolveApiKey() {
  const envKey = (process.env.BAIDU_API_KEY || '').trim();
  if (envKey) return envKey;

  if (!fs.existsSync(CONFIG_PATH)) return '';
  try {
    const cfg = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    return (cfg.apiKey || '').trim();
  } catch (e) {
    return '';
  }
}

function emptyResult(errorMsg) {
  return { error: errorMsg };
}

function successResult(data) {
  return { success: true, ...data };
}

module.exports = {
  resolveApiKey,
  emptyResult,
  successResult,
  BASE_URL: 'https://qianfan.baidubce.com/v2',
  TIMEOUT_MS: 15000
};
