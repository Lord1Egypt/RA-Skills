#!/usr/bin/env node
// wip-repo-init: scaffold the standard ai/ directory structure in any repo.
//
// New repo (no ai/ folder):
//   Copies the template as-is.
//
// Existing repo (ai/ folder exists):
//   1. Creates the new ai/ structure
//   2. Moves old ai/ contents into ai/_sort/ai_old/
//   3. You sort from there at your own pace.

import { existsSync, mkdirSync, cpSync, renameSync, readdirSync, statSync, readFileSync } from 'node:fs';
import { join, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createInterface } from 'node:readline';

const __dirname = dirname(fileURLToPath(import.meta.url));

if (process.argv.includes('--version') || process.argv.includes('-v')) {
  const pkg = JSON.parse(readFileSync(join(__dirname, 'package.json'), 'utf8'));
  console.log(pkg.version);
  process.exit(0);
}
const TEMPLATE = join(__dirname, 'templates');

const targetRepo = resolve(process.argv[2] || process.cwd());
const aiDir = join(targetRepo, 'ai');
const dryRun = process.argv.includes('--dry-run');

const forceYes = process.argv.includes('--yes') || process.argv.includes('-y');

function log(msg) { console.log(`  ${msg}`); }
function ok(msg) { console.log(`  ✓ ${msg}`); }
function skip(msg) { console.log(`  - ${msg}`); }

async function confirm(question) {
  if (forceYes) return true;
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => {
    rl.question(`  ${question} (y/N) `, answer => {
      rl.close();
      resolve(answer.trim().toLowerCase() === 'y');
    });
  });
}

// Recursively copy template, skipping files that already exist
function scaffoldDir(src, dest) {
  if (!existsSync(dest)) {
    if (!dryRun) mkdirSync(dest, { recursive: true });
    ok(`Created ${dest.replace(targetRepo + '/', '')}`);
  }

  for (const entry of readdirSync(src)) {
    if (entry === '.DS_Store') continue;
    const srcPath = join(src, entry);
    const destPath = join(dest, entry);
    const stat = statSync(srcPath);

    if (stat.isDirectory()) {
      scaffoldDir(srcPath, destPath);
    } else {
      if (existsSync(destPath)) {
        skip(`${destPath.replace(targetRepo + '/', '')} already exists`);
      } else {
        if (!dryRun) cpSync(srcPath, destPath);
        ok(`${destPath.replace(targetRepo + '/', '')}`);
      }
    }
  }
}

console.log('');
console.log(`  wip-repo-init${dryRun ? ' (dry run)' : ''}`);
console.log(`  Target: ${targetRepo}`);
console.log(`  ${'─'.repeat(40)}`);

if (!existsSync(targetRepo)) {
  console.log(`  ✗ Target directory does not exist: ${targetRepo}`);
  process.exit(1);
}

if (existsSync(aiDir)) {
  // Existing ai/ folder: explain what will happen, then confirm
  log('Found existing ai/ folder.');
  console.log('');
  log('Here\'s what will happen:');
  log('  1. Your current ai/ contents will be moved to ai/_sort/ai_old/');
  log('  2. The standard ai/ structure will be scaffolded');
  log('  3. You can sort files from ai_old/ into the new structure at your own pace');
  console.log('');
  log('Nothing is deleted. Your old files will all be in ai/_sort/ai_old/.');
  console.log('');

  const sortDir = join(aiDir, '_sort');
  const aiOldDir = join(sortDir, 'ai_old');

  if (existsSync(aiOldDir)) {
    console.log(`  ✗ ai/_sort/ai_old/ already exists. A previous init was run but not sorted yet.`);
    console.log(`    Sort the files in ai/_sort/ai_old/ first, then run again.`);
    process.exit(1);
  }

  if (dryRun) {
    log('[dry run] Would move old ai/ contents to ai/_sort/ai_old/');
    log('[dry run] Would scaffold new ai/ structure:');
    console.log('');
    scaffoldDir(TEMPLATE, aiDir);
    console.log(`\n  ${'─'.repeat(40)}`);
    console.log('  Dry run complete. No changes made.\n');
    process.exit(0);
  }

  const proceed = await confirm('Proceed?');
  if (!proceed) {
    console.log('  Cancelled.\n');
    process.exit(0);
  }

  console.log('');
  const tmpOld = join(targetRepo, '_ai_old_tmp');
  renameSync(aiDir, tmpOld);
  ok('Moved old ai/ to temporary location');

  scaffoldDir(TEMPLATE, aiDir);

  mkdirSync(join(aiDir, '_sort'), { recursive: true });
  renameSync(tmpOld, aiOldDir);
  ok('Moved old ai/ contents to ai/_sort/ai_old/');
} else {
  // No ai/ folder: scaffold from scratch
  log('No existing ai/ folder. Scaffolding from template.');
  console.log('');
  scaffoldDir(TEMPLATE, aiDir);
}

console.log(`  ${'─'.repeat(40)}`);
if (dryRun) {
  console.log('  Dry run complete. No changes made.');
} else {
  ok('Done.');
  if (existsSync(join(aiDir, '_sort', 'ai_old'))) {
    console.log('');
    log('Your old ai/ contents are in ai/_sort/ai_old/');
    log('Sort them into the new structure at your own pace.');
  }
}
console.log('');
