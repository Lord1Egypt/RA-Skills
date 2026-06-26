import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

export function getConfigDir(): string {
  return process.env.TOKENRIP_CONFIG_DIR ?? path.join(os.homedir(), '.config', 'tokenrip');
}

export const CONFIG_DIR = process.env.TOKENRIP_CONFIG_DIR ?? path.join(os.homedir(), '.config', 'tokenrip');
export const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json');

export interface TokenripConfig {
  configVersion?: number;
  currentAgent?: string;
  apiKey?: string;
  apiUrl?: string;
  frontendUrl?: string;
  lastUpdateCheck?: string;
  latestVersion?: string;
  preferences: Record<string, unknown>;
}

function defaultConfig(): TokenripConfig {
  return { preferences: {} };
}

export function loadConfig(): TokenripConfig {
  try {
    const raw = fs.readFileSync(path.join(getConfigDir(), 'config.json'), 'utf-8');
    return JSON.parse(raw) as TokenripConfig;
  } catch {
    return defaultConfig();
  }
}

export function saveConfig(config: TokenripConfig): void {
  const dir = getConfigDir();
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'config.json'), JSON.stringify(config, null, 2), 'utf-8');
}

export function getApiUrl(config: TokenripConfig): string {
  return process.env.TOKENRIP_API_URL || config.apiUrl || 'https://api.tokenrip.com';
}

export function getApiKey(config: TokenripConfig): string | undefined {
  return process.env.TOKENRIP_API_KEY || config.apiKey;
}

function deriveFrontendUrl(apiUrl: string): string {
  try {
    const parsed = new URL(apiUrl);
    if (parsed.hostname === 'api.tokenrip.com') {
      return 'https://tokenrip.com';
    }
    if (parsed.hostname.startsWith('api.')) {
      parsed.hostname = parsed.hostname.slice(4);
    }
    return parsed.origin;
  } catch {
    return 'https://tokenrip.com';
  }
}

export function getFrontendUrl(config?: TokenripConfig): string {
  const resolved = config ?? loadConfig();
  return process.env.TOKENRIP_FRONTEND_URL || resolved.frontendUrl || deriveFrontendUrl(getApiUrl(resolved));
}
