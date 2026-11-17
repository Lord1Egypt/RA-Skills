#!/usr/bin/env node
// Regression test: `ldm doctor` duplicate-hook + invalid-model checks.
//
// Covers the 2026-07-04 tickets:
//   ai/product/bugs/installer/open-tickets/2026-07-04--cc-mini--installer-sessionstart-hook-duplicate-registration.md
//   ai/product/bugs/guard/2026-07-04--cc-mini--no-blessed-recipe-for-live-settings-remediation.md
//
// Cases:
//   1. Duplicate-laden settings: doctor reports, does NOT write without --fix.
//   2. --fix collapses duplicates to 1, writes a timestamped backup first,
//      preserves unrelated hooks and unknown keys.
//   3. Invalid model value ("opus" + real ESC 0x1B + "[1m"): reported, removed under --fix.
//   4. Malformed settings.json: warns and skips, file untouched, no crash.
//
// Follows the test-doctor-cron-target.mjs pattern: real bin/ldm.js doctor
// against a temp HOME, crontab/npm shimmed on PATH so the operator's real
// state is never read.

import { chmodSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';

const repo = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const cli = join(repo, 'bin', 'ldm.js');
const pkg = JSON.parse(readFileSync(join(repo, 'package.json'), 'utf8'));

let failed = 0;
function assert(cond, label, output = '') {
  if (cond) {
    console.log(`  [PASS] ${label}`);
  } else {
    console.log(`  [FAIL] ${label}`);
    if (output) console.log(`         --- output (last lines) ---\n         ${output.trim().split('\n').slice(-25).join('\n         ')}`);
    failed++;
  }
}

function setupHome(settingsFactory) {
  const home = mkdtempSync(join(tmpdir(), 'ldm-doctor-dedupe-'));
  const ldmRoot = join(home, '.ldm');
  const fakeBin = join(home, 'fakebin');
  mkdirSync(join(ldmRoot, 'extensions'), { recursive: true });
  mkdirSync(join(home, '.claude'), { recursive: true });
  mkdirSync(fakeBin, { recursive: true });

  writeFileSync(join(ldmRoot, 'version.json'), JSON.stringify({ version: pkg.version }, null, 2) + '\n');
  writeFileSync(join(ldmRoot, 'extensions', 'registry.json'), JSON.stringify({ _format: 'v2', extensions: {} }, null, 2) + '\n');

  // Hook scripts must exist on disk: doctor --fix runs the stale-path
  // cleanup (#30) before the dedupe pass, and missing targets would be
  // removed as stale instead of collapsed as duplicates.
  const bootScript = join(ldmRoot, 'shared', 'boot', 'boot-hook.mjs');
  const guardScript = join(ldmRoot, 'extensions', 'wip-branch-guard', 'guard.mjs');
  const stopScript = join(ldmRoot, 'extensions', 'stop-hook.mjs');
  for (const f of [bootScript, guardScript, stopScript]) {
    mkdirSync(dirname(f), { recursive: true });
    writeFileSync(f, 'process.exit(0);\n');
  }

  const paths = { bootScript, guardScript, stopScript };
  const settingsContent = settingsFactory(paths);
  const settingsPath = join(home, '.claude', 'settings.json');
  writeFileSync(settingsPath, typeof settingsContent === 'string'
    ? settingsContent
    : JSON.stringify(settingsContent, null, 2) + '\n');

  // Empty crontab + no-op npm on PATH (never touch operator state/network).
  writeFileSync(join(fakeBin, 'crontab'), '#!/bin/sh\nexit 0\n');
  chmodSync(join(fakeBin, 'crontab'), 0o755);
  writeFileSync(join(fakeBin, 'npm'), '#!/bin/sh\nexit 0\n');
  chmodSync(join(fakeBin, 'npm'), 0o755);

  return { home, fakeBin, settingsPath, paths };
}

function runDoctor({ home, fakeBin }, fix = false) {
  const args = ['doctor'];
  if (fix) args.push('--fix');
  try {
    return execFileSync('node', [cli, ...args], {
      env: { ...process.env, HOME: home, PATH: `${fakeBin}:${process.env.PATH}`, LDM_SELF_UPDATED: '1' },
      encoding: 'utf-8',
      timeout: 30000,
    });
  } catch (err) {
    return (err.stdout || '') + (err.stderr || '');
  }
}

const bootCmd = (paths) => `node ${paths.bootScript}`;
const bootEntry = (paths) => ({ matcher: '*', hooks: [{ type: 'command', command: bootCmd(paths), timeout: 15 }] });
const guardEntry = (paths) => ({ hooks: [{ type: 'command', command: `node ${paths.guardScript}`, timeout: 10 }] });

function dupeLadenSettings(paths) {
  return {
    unknownTopLevelKey: { keep: 'me' },
    permissions: { defaultMode: 'default' },
    hooks: {
      SessionStart: [
        ...Array.from({ length: 5 }, () => bootEntry(paths)),
        guardEntry(paths),
        ...Array.from({ length: 5 }, () => bootEntry(paths)),
      ],
      Stop: [{ hooks: [{ type: 'command', command: `node ${paths.stopScript}` }] }],
    },
  };
}

console.log('Test 1: duplicates reported, no write without --fix');
{
  const w = setupHome(dupeLadenSettings);
  const before = readFileSync(w.settingsPath, 'utf-8');
  const out = runDoctor(w);
  const after = readFileSync(w.settingsPath, 'utf-8');
  assert(/SessionStart: 10 identical hook entries/.test(out), 'reports 10 identical SessionStart entries', out);
  assert(/ldm doctor --fix to collapse 9 duplicate hook entries/.test(out), 'suggests --fix with count', out);
  assert(before === after, 'settings.json untouched without --fix');
  rmSync(w.home, { recursive: true, force: true });
}

console.log('Test 2: --fix collapses, backs up first, preserves everything else');
{
  const w = setupHome(dupeLadenSettings);
  const out = runDoctor(w, true);
  const s = JSON.parse(readFileSync(w.settingsPath, 'utf-8'));
  const bootCount = s.hooks.SessionStart.filter((e) => e.hooks?.[0]?.command === bootCmd(w.paths)).length;
  const backups = readdirSync(join(w.home, '.claude')).filter((f) => f.startsWith('settings.json.bak-'));
  assert(/Collapsed 9 duplicate hook entries/.test(out), 'reports 9 collapsed', out);
  assert(bootCount === 1, `boot-hook entries collapsed to 1 (got ${bootCount})`);
  assert(s.hooks.SessionStart.length === 2, 'boot hook + branch guard remain');
  assert(s.hooks.Stop.length === 1, 'unrelated Stop hook preserved');
  assert(s.unknownTopLevelKey?.keep === 'me', 'unknown top-level key preserved');
  assert(backups.length === 1, `timestamped backup written (found ${backups.length})`);
  if (backups.length === 1) {
    const bak = JSON.parse(readFileSync(join(w.home, '.claude', backups[0]), 'utf-8'));
    assert(bak.hooks.SessionStart.length === 11, 'backup holds the pre-fix state');
  }
  const again = runDoctor(w, true);
  assert(!/Collapsed/.test(again), 'second --fix run finds nothing to collapse', again);
  rmSync(w.home, { recursive: true, force: true });
}

console.log('Test 3: invalid model value reported and removed under --fix');
{
  // The corruption fixture carries a REAL ESC control char (0x1B): "opus"
  // plus an ANSI bold fragment, which is what a terminal paste persists.
  // Printable brackets alone are NOT corruption (see Test 4).
  const w = setupHome((paths) => ({ model: 'opus\x1b[1m', hooks: { SessionStart: [bootEntry(paths)] } }));
  const out = runDoctor(w);
  assert(/model value is invalid/.test(out), 'reports invalid model', out);
  const before = JSON.parse(readFileSync(w.settingsPath, 'utf-8'));
  assert(typeof before.model === 'string', 'model untouched without --fix');
  const fixOut = runDoctor(w, true);
  const s = JSON.parse(readFileSync(w.settingsPath, 'utf-8'));
  assert(/Removed invalid model value/.test(fixOut), 'reports removal under --fix', fixOut);
  assert(!('model' in s), 'model key removed from disk');
  assert(s.hooks.SessionStart.length === 1, 'hooks untouched by model fix');
  rmSync(w.home, { recursive: true, force: true });
}

console.log('Test 4: valid model values are left alone (including bracketed 1M-context IDs)');
{
  const w = setupHome(() => ({ model: 'claude-fable-5[1m]', hooks: {} }));
  const out = runDoctor(w, true);
  const s = JSON.parse(readFileSync(w.settingsPath, 'utf-8'));
  assert(!/model value is invalid/.test(out), 'no invalid-model report for bracketed 1M id', out);
  assert(s.model === 'claude-fable-5[1m]', 'legitimate 1M-context model preserved');
  rmSync(w.home, { recursive: true, force: true });
}

console.log('Test 5: malformed settings.json warns, skips, file untouched');
{
  const w = setupHome(() => '{ this is not json\n');
  const before = readFileSync(w.settingsPath, 'utf-8');
  const out = runDoctor(w, true);
  const after = readFileSync(w.settingsPath, 'utf-8');
  assert(/not valid JSON; skipping hook\/model checks/.test(out), 'warns about malformed JSON', out);
  assert(before === after, 'malformed file untouched');
  rmSync(w.home, { recursive: true, force: true });
}

if (failed > 0) {
  console.log(`\n${failed} assertion(s) failed`);
  process.exit(1);
}
console.log('\nAll doctor hook-dedupe tests passed');
