#!/usr/bin/env node
/**
 * Post-install script for ttc CLI.
 *
 * Sets up Claude Code skill by creating a symlink:
 *   ~/.claude/skills/ttc -> <npm-package-location>
 */

import { existsSync, mkdirSync, unlinkSync, symlinkSync, lstatSync, readlinkSync, rmSync, copyFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { homedir, platform } from 'os';
import { execSync } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const PACKAGE_ROOT = join(__dirname, '..');
const SKILL_DIR = join(homedir(), '.claude', 'skills');
const SKILL_LINK = join(SKILL_DIR, 'ttc');

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
            console.log('[ttc] Claude Code skill already configured.');
            return true;
          }
          unlinkSync(SKILL_LINK);
        } else {
          rmSync(SKILL_LINK, { recursive: true });
        }
      } catch (err) {
        console.log(`[ttc] Warning: ${err.message}`);
      }
    }

    symlinkSync(PACKAGE_ROOT, SKILL_LINK);
    console.log('[ttc] Claude Code skill installed:');
    console.log(`[ttc]   ~/.claude/skills/ttc -> ${PACKAGE_ROOT}`);
    return true;
  } catch (error) {
    console.error(`[ttc] Failed to set up skill: ${error.message}`);
    console.log('[ttc] You can manually create the symlink:');
    console.log(`[ttc]   ln -s "${PACKAGE_ROOT}" "${SKILL_LINK}"`);
    return false;
  }
}

function buildLocationHelper() {
  if (platform() !== 'darwin') {
    console.log('[ttc] Skipping location helper (macOS only).');
    return false;
  }

  try {
    execSync('which swiftc', { stdio: 'ignore' });
  } catch {
    console.log('[ttc] Skipping location helper (Swift compiler not found).');
    console.log('[ttc] Install Xcode Command Line Tools for location support:');
    console.log('[ttc]   xcode-select --install');
    return false;
  }

  const appDir = join(PACKAGE_ROOT, 'helpers', 'TTC Location.app', 'Contents');
  const macosDir = join(appDir, 'MacOS');
  const swiftSrc = join(PACKAGE_ROOT, 'scripts', 'get-location.swift');
  const plistSrc = join(PACKAGE_ROOT, 'scripts', 'Info.plist');
  const binary = join(macosDir, 'ttc-location');

  try {
    mkdirSync(macosDir, { recursive: true });
    copyFileSync(plistSrc, join(appDir, 'Info.plist'));
    // All paths are hardcoded constants, not user input — safe to use execSync
    execSync(`swiftc -O -o "${binary}" "${swiftSrc}"`, { stdio: 'pipe' });
    console.log('[ttc] Location helper compiled (macOS CoreLocation).');
    return true;
  } catch (err) {
    console.log(`[ttc] Warning: Could not compile location helper: ${err.message}`);
    return false;
  }
}

function main() {
  console.log('[ttc] Running post-install...');
  const success = setupClaudeSkill();
  const location = buildLocationHelper();
  console.log('');
  console.log('[ttc] Installation complete!');
  if (success) {
    console.log('[ttc] Use /ttc in Claude Code, or run: ttc --help');
  }
  if (location) {
    console.log('[ttc] Location support enabled. First "ttc nearby" will prompt for permission.');
  }
}

main();
