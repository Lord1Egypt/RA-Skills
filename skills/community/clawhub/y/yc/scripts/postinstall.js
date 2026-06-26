#!/usr/bin/env node
/**
 * Post-install script for yc-cli.
 *
 * Sets up Claude Code skill by creating a symlink:
 *   ~/.claude/skills/yc-cli -> <npm-package-location>
 */

import { existsSync, mkdirSync, unlinkSync, symlinkSync, lstatSync, readlinkSync, rmSync, readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { homedir } from 'os';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const PACKAGE_ROOT = join(__dirname, '..');
const SKILL_DIR = join(homedir(), '.claude', 'skills');
const SKILL_LINK = join(SKILL_DIR, 'yc-cli');

function setupClaudeSkill() {
  try {
    if (!existsSync(SKILL_DIR)) {
      mkdirSync(SKILL_DIR, { recursive: true });
    }

    if (existsSync(SKILL_LINK)) {
      try {
        const stats = lstatSync(SKILL_LINK);
        if (stats.isSymbolicLink()) {
          const currentTarget = readlinkSync(SKILL_LINK);
          if (currentTarget === PACKAGE_ROOT) {
            console.log('[yc-cli] Claude Code skill already configured.');
            return true;
          }
          unlinkSync(SKILL_LINK);
        } else {
          rmSync(SKILL_LINK, { recursive: true });
        }
      } catch (err) {
        console.log(`[yc-cli] Warning: ${err.message}`);
      }
    }

    symlinkSync(PACKAGE_ROOT, SKILL_LINK);
    console.log('[yc-cli] Claude Code skill installed:');
    console.log(`[yc-cli]   ~/.claude/skills/yc-cli -> ${PACKAGE_ROOT}`);
    return true;
  } catch (error) {
    console.error(`[yc-cli] Failed to set up skill: ${error.message}`);
    console.log('[yc-cli] You can manually create the symlink:');
    console.log(`[yc-cli]   ln -s "${PACKAGE_ROOT}" "${SKILL_LINK}"`);
    return false;
  }
}

/**
 * Patch @steipete/sweet-cookie keychain timeout bug.
 */
function patchSweetCookieTimeout() {
  const target = join(
    PACKAGE_ROOT,
    'node_modules',
    '@steipete',
    'sweet-cookie',
    'dist',
    'providers',
    'chromeSqliteMac.js'
  );

  if (!existsSync(target)) return;

  try {
    const content = readFileSync(target, 'utf-8');
    const needle = 'timeoutMs: 3_000,';
    if (!content.includes(needle)) return;
    const patched = content.replace(needle, 'timeoutMs: options.timeoutMs ?? 30_000,');
    writeFileSync(target, patched, 'utf-8');
    console.log('[yc-cli] Patched sweet-cookie keychain timeout (3s -> 30s).');
  } catch (err) {
    console.log(`[yc-cli] Warning: could not patch sweet-cookie: ${err.message}`);
  }
}

/**
 * Patch node:sqlite BigInt overflow on Node < 24.4.
 */
function patchSweetCookieBigInt() {
  const target = join(
    PACKAGE_ROOT,
    'node_modules',
    '@steipete',
    'sweet-cookie',
    'dist',
    'providers',
    'chromeSqlite',
    'shared.js'
  );

  if (!existsSync(target)) return;

  try {
    const content = readFileSync(target, 'utf-8');
    const needle = 'SELECT name, value, host_key, path, expires_utc, samesite, encrypted_value,';
    if (!content.includes(needle)) return;
    const patched = content.replace(
      needle,
      'SELECT name, value, host_key, path, CAST(expires_utc AS TEXT) AS expires_utc, samesite, encrypted_value,'
    );
    writeFileSync(target, patched, 'utf-8');
    console.log('[yc-cli] Patched sweet-cookie BigInt overflow.');
  } catch (err) {
    console.log(`[yc-cli] Warning: could not patch sweet-cookie BigInt: ${err.message}`);
  }
}

function main() {
  console.log('[yc-cli] Running post-install...');
  const success = setupClaudeSkill();
  patchSweetCookieTimeout();
  patchSweetCookieBigInt();
  console.log('');
  console.log('[yc-cli] Installation complete!');
  if (success) {
    console.log('[yc-cli] Use /yc in Claude Code, or run: yc --help');
  }
}

main();
