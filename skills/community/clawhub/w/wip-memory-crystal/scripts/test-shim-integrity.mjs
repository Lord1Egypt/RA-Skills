#!/usr/bin/env node
// Integration test: capture-shim integrity
//
// Exercises the four states of `crystal doctor`'s capture check against a
// real subprocess running the built CLI. Uses a temp HOME and a fake
// `crontab` shim on PATH so we can drive the diagnostic without touching
// the user's real crontab.
//
// Run from repo root: node scripts/test-shim-integrity.mjs
//
// What it covers (the regression we are guarding against):
//   1. cron missing                       -> warn "cron missing"
//   2. cron installed, target missing     -> fail "cron installed but target missing"
//   3. cron installed, target not exec    -> fail "cron target exists but not executable"
//   4. heal via `crystal doctor --fix`    -> restores from extensions/dist
//   5. all healthy                        -> ok "cron + target ok"

import { mkdirSync, writeFileSync, chmodSync, copyFileSync, existsSync, mkdtempSync, rmSync, statSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';

const REPO = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const CLI = join(REPO, 'dist', 'cli.js');
const SOURCE_SCRIPT = join(REPO, 'scripts', 'crystal-capture.sh');

if (!existsSync(CLI)) {
  console.error(`FAIL: built CLI not found at ${CLI}. Run 'npm run build' first.`);
  process.exit(1);
}
if (!existsSync(SOURCE_SCRIPT)) {
  console.error(`FAIL: source script not found at ${SOURCE_SCRIPT}.`);
  process.exit(1);
}

let failed = 0;
function assert(condition, label) {
  if (condition) {
    console.log(`  [PASS] ${label}`);
  } else {
    console.log(`  [FAIL] ${label}`);
    failed++;
  }
}

function makeWorld(crontabContent) {
  const home = mkdtempSync(join(tmpdir(), 'mc-shim-test-'));
  const fakeBin = join(home, 'fakebin');
  mkdirSync(fakeBin, { recursive: true });

  // Fake crontab shim. `crontab -l` prints crontabContent. Anything else: noop.
  const crontabScript = join(fakeBin, 'crontab');
  const escaped = crontabContent.replace(/'/g, `'\\''`);
  writeFileSync(crontabScript, `#!/bin/bash\nif [ "$1" = "-l" ]; then\n  printf '%s' '${escaped}'\nfi\n`);
  chmodSync(crontabScript, 0o755);

  // Seed canonical script in extension dist (the real install layout).
  const extDist = join(home, '.ldm', 'extensions', 'memory-crystal', 'dist');
  mkdirSync(extDist, { recursive: true });
  copyFileSync(SOURCE_SCRIPT, join(extDist, 'crystal-capture.sh'));
  chmodSync(join(extDist, 'crystal-capture.sh'), 0o755);

  return { home, fakeBin };
}

function runDoctor({ home, fakeBin, fix = false }) {
  const args = ['doctor'];
  if (fix) args.push('--fix');
  try {
    return execFileSync('node', [CLI, ...args], {
      env: { ...process.env, HOME: home, PATH: `${fakeBin}:${process.env.PATH}`, CRYSTAL_AGENT_ID: 'cc-test' },
      encoding: 'utf-8',
    });
  } catch (err) {
    // doctor exits non-zero on failures; we still want stdout
    return (err.stdout || '') + (err.stderr || '');
  }
}

const CRON_LINE = '* * * * * ~/.ldm/bin/crystal-capture.sh >> ~/.ldm/logs/crystal-capture.log 2>&1\n';

// ── Test 1: cron missing ──
console.log('Test 1: cron missing');
{
  const w = makeWorld('');
  const out = runDoctor(w);
  assert(/Capture: cron missing/.test(out), 'reports "cron missing"');
  rmSync(w.home, { recursive: true, force: true });
}

// ── Test 2: cron present but target missing ──
console.log('Test 2: cron installed, target missing');
{
  const w = makeWorld(CRON_LINE);
  const out = runDoctor(w);
  assert(/cron installed but target missing/.test(out), 'reports "cron installed but target missing"');
  assert(!existsSync(join(w.home, '.ldm', 'bin', 'crystal-capture.sh')), 'shim is absent (no silent write)');
  rmSync(w.home, { recursive: true, force: true });
}

// ── Test 3: --fix restores from extensions/dist ──
console.log('Test 3: doctor --fix restores the shim');
{
  const w = makeWorld(CRON_LINE);
  const out = runDoctor({ ...w, fix: true });
  const shim = join(w.home, '.ldm', 'bin', 'crystal-capture.sh');
  assert(/Applying fixes/.test(out), 'announces fix application');
  assert(existsSync(shim), `restored shim exists at ${shim}`);
  rmSync(w.home, { recursive: true, force: true });
}

// ── Test 4: target exists but not executable ──
console.log('Test 4: cron installed, target not executable');
{
  const w = makeWorld(CRON_LINE);
  const shim = join(w.home, '.ldm', 'bin', 'crystal-capture.sh');
  mkdirSync(dirname(shim), { recursive: true });
  copyFileSync(SOURCE_SCRIPT, shim);
  chmodSync(shim, 0o644);
  const out = runDoctor(w);
  assert(/cron target exists but not executable/.test(out), 'reports "cron target exists but not executable"');
  rmSync(w.home, { recursive: true, force: true });
}

// ── Test 5: healthy ──
console.log('Test 5: cron + shim present and executable');
{
  const w = makeWorld(CRON_LINE);
  const shim = join(w.home, '.ldm', 'bin', 'crystal-capture.sh');
  mkdirSync(dirname(shim), { recursive: true });
  copyFileSync(SOURCE_SCRIPT, shim);
  chmodSync(shim, 0o755);
  const out = runDoctor(w);
  assert(/cron \+ target ok/.test(out), 'reports "cron + target ok"');
  rmSync(w.home, { recursive: true, force: true });
}

// ── Test 6: --fix restores executable bit on non-executable shim ──
console.log('Test 6: doctor --fix on non-executable shim');
{
  const w = makeWorld(CRON_LINE);
  const shim = join(w.home, '.ldm', 'bin', 'crystal-capture.sh');
  mkdirSync(dirname(shim), { recursive: true });
  copyFileSync(SOURCE_SCRIPT, shim);
  chmodSync(shim, 0o644);
  const out = runDoctor({ ...w, fix: true });
  assert(/Applying fixes/.test(out), 'announces fix application');
  assert((statSync(shim).mode & 0o111) !== 0, 'shim is now executable after --fix');
  rmSync(w.home, { recursive: true, force: true });
}

console.log('');
if (failed > 0) {
  console.log(`${failed} test(s) failed.`);
  process.exit(1);
}
console.log('All capture-shim integrity tests passed.');
