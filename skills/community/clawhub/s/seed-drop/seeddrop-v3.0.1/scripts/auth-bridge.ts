// SECURITY MANIFEST:
//   Environment variables accessed: HOME, USERPROFILE
//   External endpoints called: none (SocialVault calls delegated to Agent)
//   Local files read: SocialVault SKILL.md (existence check only)
//   Local files written: none
//   Security: SocialVault is REQUIRED - no plaintext credential fallback

import { existsSync } from 'node:fs';
import { homedir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import type { Credential, AuthMode, CheckResult } from './types.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const BASE_DIR = join(__dirname, '..');

// ─── SocialVault Detection ──────────────────────────────────

const SOCIALVAULT_SEARCH_PATHS = [
  join(homedir(), '.openclaw', 'skills', 'socialvault', 'SKILL.md'),
  join(homedir(), '.openclaw', 'skills', 'social-vault', 'SKILL.md'),
  join(homedir(), '.openclaw', 'workspace', 'skills', 'socialvault', 'SKILL.md'),
  join(homedir(), '.openclaw', 'workspace', 'skills', 'social-vault', 'SKILL.md'),
  join(BASE_DIR, '..', 'socialvault', 'SKILL.md'),
  join(BASE_DIR, '..', 'social-vault', 'SKILL.md'),
  join(BASE_DIR, '..', 'SocialVault', 'socialvault', 'SKILL.md'),
];

function detectSocialVault(): string | null {
  for (const p of SOCIALVAULT_SEARCH_PATHS) {
    if (existsSync(p)) {
      console.error(`[auth-bridge] SocialVault detected at: ${dirname(p)}`);
      return p;
    }
  }
  return null;
}

export function getAuthMode(): AuthMode {
  return detectSocialVault() ? 'socialvault' : 'none';
}

// ─── SocialVault Mode ───────────────────────────────────────

function getSocialVaultInstruction(command: string, platform: string, profile: string): string {
  switch (command) {
    case 'use':
      return `socialvault use ${platform}-${profile}`;
    case 'token':
      return `socialvault token ${platform}-${profile}`;
    case 'release':
      return `socialvault release ${platform}-${profile}`;
    case 'check':
      return `socialvault check ${platform}-${profile}`;
    default:
      return `socialvault status`;
  }
}

// ─── Public API ─────────────────────────────────────────────

export function getCredential(platform: string, profile: string = 'default'): Credential | null {
  const mode = getAuthMode();

  if (mode === 'socialvault') {
    const instruction = getSocialVaultInstruction('token', platform, profile);
    console.error(`[auth-bridge] SocialVault mode — Agent should run: ${instruction}`);
    return {
      authType: 'oauth',
      value: `__socialvault_pending__:${instruction}`,
      profile,
      source: 'socialvault',
    };
  }

  console.error(`[auth-bridge] SocialVault is required but not detected. Please install: clawhub install socialvault`);
  return null;
}

export function checkCredential(platform: string, profile: string = 'default'): CheckResult {
  const cred = getCredential(platform, profile);
  if (!cred) {
    return { valid: false, error: `No credential found for ${platform}/${profile}` };
  }
  if (cred.source === 'socialvault') {
    return { valid: true, username: `(via SocialVault, run: socialvault check ${platform}-${profile})` };
  }
  return {
    valid: cred.value.length > 0,
    error: cred.value.length === 0 ? 'Credential value is empty' : undefined,
  };
}

// ─── CLI Entry Point ────────────────────────────────────────

const IS_MAIN = process.argv[1]?.replace(/\\/g, '/').endsWith('auth-bridge.ts');

function main(): void {
  if (!IS_MAIN) return;
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'mode':
      console.log(JSON.stringify({ mode: getAuthMode() }));
      break;

    case 'get': {
      const platform = args[1];
      const profile = args[2] ?? 'default';
      if (!platform) {
        console.error('Usage: auth-bridge.ts get <platform> [profile]');
        process.exit(1);
      }
      const cred = getCredential(platform, profile);
      if (!cred) {
        console.error(`[auth-bridge] Failed to get credential for ${platform}/${profile}`);
        process.exit(1);
      }
      console.log(JSON.stringify(cred));
      break;
    }

    case 'check': {
      const platform = args[1];
      const profile = args[2] ?? 'default';
      if (!platform) {
        console.error('Usage: auth-bridge.ts check <platform> [profile]');
        process.exit(1);
      }
      const result = checkCredential(platform, profile);
      console.log(JSON.stringify(result));
      break;
    }

    case 'test':
      console.log(JSON.stringify({
        script: 'auth-bridge',
        status: 'ok',
        mode: getAuthMode(),
        socialVaultDetected: detectSocialVault() !== null,
      }));
      break;

    default:
      console.error('Usage: auth-bridge.ts <mode|get|check|test> [args]');
      console.error('  mode                    — Show auth mode (local/socialvault)');
      console.error('  get <platform> [profile] — Get credential');
      console.error('  check <platform> [profile] — Check credential validity');
      console.error('  test                    — Self-test');
      process.exit(1);
  }
}

main();
