#!/usr/bin/env node
/**
 * Pre-uninstall script for ttc CLI.
 *
 * Removes the Claude Code skill symlink at ~/.claude/skills/ttc
 * (only if it points to this package).
 */

import { existsSync, unlinkSync, lstatSync, readlinkSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { homedir } from 'os';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const PACKAGE_ROOT = join(__dirname, '..');
const SKILL_LINK = join(homedir(), '.claude', 'skills', 'ttc');

function main() {
  console.log('[ttc] Running pre-uninstall...');

  if (!existsSync(SKILL_LINK)) {
    console.log('[ttc] No skill symlink found, nothing to clean up.');
    return;
  }

  try {
    const stats = lstatSync(SKILL_LINK);
    if (!stats.isSymbolicLink()) {
      console.log('[ttc] Skill path is not a symlink, leaving it alone.');
      return;
    }

    const target = readlinkSync(SKILL_LINK);
    if (target === PACKAGE_ROOT || target.includes('node_modules/@lucasygu/ttc')) {
      unlinkSync(SKILL_LINK);
      console.log('[ttc] Removed Claude Code skill symlink.');
    } else {
      console.log('[ttc] Skill symlink points elsewhere, leaving it alone.');
    }
  } catch (error) {
    console.error(`[ttc] Warning: Could not remove skill: ${error.message}`);
  }

  console.log('[ttc] Uninstall cleanup complete.');
}

main();
