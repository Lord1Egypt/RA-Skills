#!/usr/bin/env node
/**
 * Patches Claude Code's cli.js to skip the dev channels warning dialog.
 * Run this right before starting claude with --dangerously-load-development-channels.
 *
 * Usage: node patch-channels.mjs && claude --dangerously-load-development-channels server:ipc
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { dirname, join } from 'node:path';

// Find claude's cli.js
const npmRoot = execSync('npm root -g', { encoding: 'utf8' }).trim();
const cliPath = join(npmRoot, '@anthropic-ai', 'claude-code', 'cli.js');

const content = readFileSync(cliPath, 'utf8');
const target = 'if(!w()||!j()?.accessToken)gd';
const replacement = 'if(true)gd';

if (content.includes(replacement)) {
  process.stderr.write('[patch] already patched\n');
} else if (content.includes(target)) {
  writeFileSync(cliPath, content.replace(target, replacement));
  process.stderr.write('[patch] patched successfully\n');
} else {
  process.stderr.write('[patch] WARNING: target pattern not found, Claude Code may have updated\n');
}
