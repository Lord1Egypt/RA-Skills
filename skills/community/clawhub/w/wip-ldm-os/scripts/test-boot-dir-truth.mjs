#!/usr/bin/env node
// Regression test: `ldm doctor` boot-hook stale-at-execution-path check.
//
// Covers:
//   ai/product/bugs/installer/open-tickets/2026-07-05--cc-mini--shared-library-split-brain-boot-deploy.md
//
// The split-brain bug: syncBootHook() deployed boot-hook.mjs to
// ~/.ldm/library/boot while the registered SessionStart hook executed
// ~/.ldm/shared/boot. New code landed in library/, sessions ran the stale
// copy in shared/, and the install reported success. This test drives the
// doctor check that makes the drift visible (and the --fix that repairs the
// execution path), plus the no-false-positive cases.
//
// Follows the test-doctor-hook-dedupe.mjs pattern: real bin/ldm.js doctor
// against a temp HOME, crontab/npm shimmed on PATH so operator state and the
// network are never touched. LDM_SELF_UPDATED=1 skips CLI self-update.

import { chmodSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';

const repo = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const cli = join(repo, 'bin', 'ldm.js');
const pkg = JSON.parse(readFileSync(join(repo, 'package.json'), 'utf8'));
// The current boot hook this CLI would deploy: doctor compares against it.
const srcBootContent = readFileSync(join(repo, 'src', 'boot', 'boot-hook.mjs'), 'utf8');

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

// Build a fixture HOME. The registered SessionStart hook points at
// ~/.ldm/shared/boot/boot-hook.mjs (the execution path). `execContent`
// seeds that file; `libraryContent` seeds the parallel ~/.ldm/library/boot
// copy (null to skip).
function setupHome({ execContent, libraryContent }) {
  const home = mkdtempSync(join(tmpdir(), 'ldm-bootdir-'));
  const ldmRoot = join(home, '.ldm');
  const fakeBin = join(home, 'fakebin');
  mkdirSync(join(ldmRoot, 'extensions'), { recursive: true });
  mkdirSync(join(home, '.claude'), { recursive: true });
  mkdirSync(fakeBin, { recursive: true });

  writeFileSync(join(ldmRoot, 'version.json'), JSON.stringify({ version: pkg.version }, null, 2) + '\n');
  writeFileSync(join(ldmRoot, 'extensions', 'registry.json'), JSON.stringify({ _format: 'v2', extensions: {} }, null, 2) + '\n');

  const execTarget = join(ldmRoot, 'shared', 'boot', 'boot-hook.mjs');
  mkdirSync(dirname(execTarget), { recursive: true });
  writeFileSync(execTarget, execContent);
  if (libraryContent !== null && libraryContent !== undefined) {
    const lib = join(ldmRoot, 'library', 'boot', 'boot-hook.mjs');
    mkdirSync(dirname(lib), { recursive: true });
    writeFileSync(lib, libraryContent);
  }

  // Registered SessionStart hook runs the shared/boot (execution) copy.
  const settings = {
    hooks: {
      SessionStart: [
        { matcher: '*', hooks: [{ type: 'command', command: `node ${execTarget}`, timeout: 15 }] },
      ],
    },
  };
  const settingsPath = join(home, '.claude', 'settings.json');
  writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');

  writeFileSync(join(fakeBin, 'crontab'), '#!/bin/sh\nexit 0\n');
  chmodSync(join(fakeBin, 'crontab'), 0o755);
  writeFileSync(join(fakeBin, 'npm'), '#!/bin/sh\nexit 0\n');
  chmodSync(join(fakeBin, 'npm'), 0o755);

  return { home, fakeBin, execTarget };
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

const STALE = '// stale boot hook code (pre-trim)\nprocess.exit(0);\n';

console.log('Test 1: stale execution path is reported, not written without --fix');
{
  const w = setupHome({ execContent: STALE, libraryContent: srcBootContent });
  const before = readFileSync(w.execTarget, 'utf-8');
  const out = runDoctor(w);
  const after = readFileSync(w.execTarget, 'utf-8');
  assert(/boot hook stale at execution path/.test(out), 'reports stale at execution path', out);
  assert(/a current copy exists at:.*library\/boot/.test(out), 'points at the fresh library/boot copy', out);
  assert(before === after, 'execution-path file untouched without --fix');
  rmSync(w.home, { recursive: true, force: true });
}

console.log('Test 2: --fix redeploys the current boot hook to the execution path');
{
  const w = setupHome({ execContent: STALE, libraryContent: srcBootContent });
  const out = runDoctor(w, true);
  const after = readFileSync(w.execTarget, 'utf-8');
  const backups = readdirSync(dirname(w.execTarget)).filter((f) => f.startsWith('boot-hook.mjs.bak-'));
  assert(/Redeployed the current boot hook to the execution path/.test(out), 'reports redeploy under --fix', out);
  assert(after === srcBootContent, 'execution-path file now matches current src/boot/boot-hook.mjs');
  assert(backups.length === 1, `stale copy backed up before overwrite (found ${backups.length})`);
  const again = runDoctor(w, true);
  assert(!/boot hook stale at execution path/.test(again), 'second --fix run finds nothing stale', again);
  rmSync(w.home, { recursive: true, force: true });
}

console.log('Test 3: in-sync execution path is not flagged');
{
  const w = setupHome({ execContent: srcBootContent, libraryContent: null });
  const out = runDoctor(w);
  assert(!/boot hook stale at execution path/.test(out), 'no stale report when exec path matches src', out);
  rmSync(w.home, { recursive: true, force: true });
}

console.log('Test 4: no registered boot hook is a no-op (no crash, no false positive)');
{
  const home = mkdtempSync(join(tmpdir(), 'ldm-bootdir-none-'));
  const ldmRoot = join(home, '.ldm');
  const fakeBin = join(home, 'fakebin');
  mkdirSync(join(ldmRoot, 'extensions'), { recursive: true });
  mkdirSync(join(home, '.claude'), { recursive: true });
  mkdirSync(fakeBin, { recursive: true });
  writeFileSync(join(ldmRoot, 'version.json'), JSON.stringify({ version: pkg.version }, null, 2) + '\n');
  writeFileSync(join(ldmRoot, 'extensions', 'registry.json'), JSON.stringify({ _format: 'v2', extensions: {} }, null, 2) + '\n');
  writeFileSync(join(home, '.claude', 'settings.json'), JSON.stringify({ hooks: {} }, null, 2) + '\n');
  writeFileSync(join(fakeBin, 'crontab'), '#!/bin/sh\nexit 0\n');
  chmodSync(join(fakeBin, 'crontab'), 0o755);
  writeFileSync(join(fakeBin, 'npm'), '#!/bin/sh\nexit 0\n');
  chmodSync(join(fakeBin, 'npm'), 0o755);
  const out = runDoctor({ home, fakeBin });
  assert(!/boot hook stale at execution path/.test(out), 'no stale report when no boot hook is registered', out);
  rmSync(home, { recursive: true, force: true });
}

if (failed > 0) {
  console.log(`\n${failed} assertion(s) failed`);
  process.exit(1);
}
console.log('\nAll boot-dir-truth tests passed');
