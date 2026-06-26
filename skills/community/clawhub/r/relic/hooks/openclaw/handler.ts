/**
 * Relic Capture Hook for OpenClaw
 *
 * Automatically captures observations about the user from conversations.
 * Fires on agent:stop event when the agent session ends.
 */

type HookEvent = {
  type?: string;
  action?: string;
  sessionKey?: string;
  context?: unknown;
};

type HookHandler = (event: HookEvent) => Promise<void> | void;

import { execFileSync } from 'child_process';
import { existsSync } from 'fs';
import * as os from 'os';
import * as path from 'path';

const SKILL_PATH = path.resolve(__dirname, '..', '..');
const DEFAULT_VAULT_PATH = path.join(os.homedir(), '.openclaw', 'workspace', 'projects', 'relic', 'vault');
const VAULT_PATH = process.env.RELIC_VAULT_PATH || DEFAULT_VAULT_PATH;
const SCRIPT_PATH = path.join(SKILL_PATH, 'hooks', 'auto_capture.py');

const readTranscript = (context: unknown): string => {
  if (!context || typeof context !== 'object') {
    return '';
  }

  const record = context as { transcript?: unknown; messages?: unknown };

  if (typeof record.transcript === 'string') {
    return record.transcript;
  }

  if (typeof record.messages === 'string') {
    return record.messages;
  }

  if (Array.isArray(record.messages)) {
    return JSON.stringify(record.messages);
  }

  return '';
};

const parseCaptureResult = (raw: string): { status?: string } | null => {
  const trimmed = raw.trim();
  if (!trimmed) {
    return null;
  }

  try {
    return JSON.parse(trimmed) as { status?: string };
  } catch {
    const lines = trimmed.split('\n').filter(Boolean);
    const lastLine = lines.length > 0 ? lines[lines.length - 1] : undefined;
    if (!lastLine) {
      return null;
    }
    try {
      return JSON.parse(lastLine) as { status?: string };
    } catch {
      return null;
    }
  }
};

const handler: HookHandler = async (event: HookEvent) => {
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

  if (!existsSync(VAULT_PATH)) {
    return;
  }

  if (!existsSync(SCRIPT_PATH)) {
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

export default handler;
