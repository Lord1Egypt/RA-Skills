import { createRequire } from 'node:module';
import { loadConfig, saveConfig, getFrontendUrl } from './config.js';

const require = createRequire(import.meta.url);
const { version: currentVersion } = require('../package.json');

export interface UpdateManifest {
  name: string;
  version: string;
  skill_url: string;
  changelog_url: string | null;
  message: string | null;
}

const CHECK_INTERVAL_MS = 24 * 60 * 60 * 1000;
const FETCH_TIMEOUT_MS = 3000;

function manifestUrl(): string {
  const frontendUrl = getFrontendUrl();
  return `${frontendUrl}/.well-known/skills/tokenrip/manifest.json`;
}

export async function fetchManifest(): Promise<UpdateManifest | null> {
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
    const res = await fetch(manifestUrl(), { signal: controller.signal });
    clearTimeout(timer);
    if (!res.ok) return null;
    return await res.json() as UpdateManifest;
  } catch {
    return null;
  }
}

function isNewer(remote: string, local: string): boolean {
  const r = remote.split('.').map(Number);
  const l = local.split('.').map(Number);
  for (let i = 0; i < 3; i++) {
    if ((r[i] ?? 0) > (l[i] ?? 0)) return true;
    if ((r[i] ?? 0) < (l[i] ?? 0)) return false;
  }
  return false;
}

export function getCurrentVersion(): string {
  return currentVersion;
}

export async function checkForUpdate(): Promise<void> {
  const config = loadConfig();
  const lastCheck = config.lastUpdateCheck;
  if (lastCheck) {
    const elapsed = Date.now() - new Date(lastCheck).getTime();
    if (elapsed < CHECK_INTERVAL_MS) {
      if (config.latestVersion && isNewer(config.latestVersion, currentVersion)) {
        printBanner(currentVersion, config.latestVersion);
      }
      return;
    }
  }

  const manifest = await fetchManifest();
  const now = new Date().toISOString();

  if (manifest) {
    try {
      saveConfig({ ...config, lastUpdateCheck: now, latestVersion: manifest.version });
    } catch {}
    if (isNewer(manifest.version, currentVersion)) {
      printBanner(currentVersion, manifest.version);
    }
  } else {
    try {
      saveConfig({ ...config, lastUpdateCheck: now });
    } catch {}
  }
}

function printBanner(current: string, latest: string): void {
  if (process.stderr.isTTY) {
    console.error(`\nUpdate available: ${current} → ${latest} — run \`rip update\` to upgrade\n`);
  }
}
