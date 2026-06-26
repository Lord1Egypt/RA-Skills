#!/usr/bin/env node
/**
 * Pre-uninstall script for yc-cli.
 *
 * Removes the Claude Code skill symlink at ~/.claude/skills/yc-cli
 * (only if it points to this package).
 */

import { existsSync, unlinkSync, lstatSync, readlinkSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { homedir } from 'os';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const PACKAGE_ROOT = join(__dirname, '..');
const SKILL_LINK = join(homedir(), '.claude', 'skills', 'yc-cli');

function main() {
  console.log('[yc-cli] Running pre-uninstall...');

  if (!existsSync(SKILL_LINK)) {
    console.log('[yc-cli] No skill symlink found, nothing to clean up.');
    return;
  }

  try {
    const stats = lstatSync(SKILL_LINK);
    if (!stats.isSymbolicLink()) {
      console.log('[yc-cli] Skill path is not a symlink, leaving it alone.');
      return;
    }

    const target = readlinkSync(SKILL_LINK);
    if (target === PACKAGE_ROOT || target.includes('node_modules/@lucasygu/yc')) {
      unlinkSync(SKILL_LINK);
      console.log('[yc-cli] Removed Claude Code skill symlink.');
    } else {
      console.log('[yc-cli] Skill symlink points elsewhere, leaving it alone.');
    }
  } catch (error) {
    console.error(`[yc-cli] Warning: Could not remove skill: ${error.message}`);
  }

  console.log('[yc-cli] Uninstall cleanup complete.');
}

main();
