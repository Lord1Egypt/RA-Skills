import { homedir } from 'os';
import { join } from 'path';
import { readFileSync, writeFileSync, existsSync } from 'fs';

const CREDENTIALS_FILE = join(homedir(), '.twit-mcp-credentials.json');

export type TwitterCredentials = {
  authToken: string;
  ct0: string;
  username?: string;
};

export function loadCredentials(): TwitterCredentials | null {
  // 1. Check env vars (set by client config on startup — backward compat)
  const authToken = process.env.TWITTER_AUTH_TOKEN;
  const ct0 = process.env.TWITTER_CT0;
  if (authToken && ct0) {
    return { authToken, ct0, username: process.env.TWITTER_USERNAME };
  }

  // 2. Check credentials file (works for all clients without restart)
  try {
    if (existsSync(CREDENTIALS_FILE)) {
      const creds = JSON.parse(readFileSync(CREDENTIALS_FILE, 'utf8'));
      if (creds.authToken && creds.ct0) return creds;
    }
  } catch {
    // ignore
  }

  return null;
}

export function saveCredentials(creds: TwitterCredentials): void {
  writeFileSync(CREDENTIALS_FILE, JSON.stringify(creds, null, 2), 'utf8');
}

export function clearCredentials(): void {
  writeFileSync(CREDENTIALS_FILE, '{}', 'utf8');
}

export { CREDENTIALS_FILE as CREDS_PATH };
