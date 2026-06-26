/**
 * Relic Capture Hook for OpenClaw
 *
 * Automatically captures observations about the user from conversations.
 * Fires on agent:stop event when the agent session ends.
 */

const { execFileSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const SKILL_PATH = path.resolve(__dirname, '..', '..');
const DEFAULT_VAULT_PATH = path.join(os.homedir(), '.openclaw', 'workspace', 'projects', 'relic', 'vault');
const VAULT_PATH = process.env.RELIC_VAULT_PATH || DEFAULT_VAULT_PATH;
const SCRIPT_PATH = path.join(SKILL_PATH, 'hooks', 'auto_capture.py');

const readTranscript = (context) => {
  if (!context || typeof context !== 'object') {
    return '';
  }

  if (typeof context.transcript === 'string') {
    return context.transcript;
  }

  if (typeof context.messages === 'string') {
    return context.messages;
  }

  if (Array.isArray(context.messages)) {
    return JSON.stringify(context.messages);
  }

  return '';
};

const parseCaptureResult = (raw) => {
  const trimmed = raw.trim();
  if (!trimmed) {
    return null;
  }

  try {
    return JSON.parse(trimmed);
  } catch {
    const lines = trimmed.split('\n').filter(Boolean);
    const lastLine = lines.length > 0 ? lines[lines.length - 1] : undefined;
    if (!lastLine) {
      return null;
    }
    try {
      return JSON.parse(lastLine);
    } catch {
      return null;
    }
  }
};

const handler = async (event) => {
  if (!event || typeof event !== 'object') {
    return;
  }

  if (event.type !== 'agent' || event.action !== 'stop') {
    return;
  }

  const sessionKey = typeof event.sessionKey === 'string' ? event.sessionKey : '';
  if (sessionKey.includes(':subagent:')) {
    return;
  }

  const transcript = readTranscript(event.context);
  if (!transcript || transcript.length < 100) {
    return;
  }

  if (!fs.existsSync(VAULT_PATH)) {
    return;
  }

  if (!fs.existsSync(SCRIPT_PATH)) {
    return;
  }

  try {
    const result = execFileSync('python3', [SCRIPT_PATH], {
      input: JSON.stringify({ transcript }),
      encoding: 'utf-8',
      timeout: 30000,
      cwd: VAULT_PATH,
      env: { ...process.env, RELIC_VAULT_PATH: VAULT_PATH },
    });

    const parsed = parseCaptureResult(result);
    if (!parsed || parsed.status !== 'success') {
      console.error('[relic] Capture failed');
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error('[relic] Capture failed:', message);
  }
};

module.exports = handler;
module.exports.default = handler;
