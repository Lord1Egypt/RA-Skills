#!/usr/bin/env node
// Regression test: `ldm doctor` cron-target health check.
//
// Walks the crontab, verifies each ~/.ldm/bin/<file> referenced by a
// cron entry exists and is executable, classifies failures, and offers
// restore-from-extension-dist for known shims (--fix). This is the
// LDM-side parallel to crystal doctor's checkCaptureShim.
//
// Each case sets a fake `crontab` shim on PATH so the operator's real
// crontab is never read. Real bin/ldm.js doctor runs against a temp
// HOME with version.json + registry.json seeded so the rest of the
// doctor flow doesn't crash.

import { chmodSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs';
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
    if (output) console.log(`         --- ldm output (last lines) ---\n         ${output.trim().split('\n').slice(-30).join('\n         ')}`);
    failed++;
  }
}

function setupHome(crontabContent, { withCanonicalShim = true, shimMode = 0o755, shimContent = '#!/bin/sh\necho hi\n' } = {}) {
  const home = mkdtempSync(join(tmpdir(), 'ldm-doctor-cron-'));
  const ldmRoot = join(home, '.ldm');
  const binDir = join(ldmRoot, 'bin');
  const extDir = join(ldmRoot, 'extensions');
  const stateDir = join(ldmRoot, 'state');
  const fakeBin = join(home, 'fakebin');

  mkdirSync(binDir, { recursive: true });
  mkdirSync(extDir, { recursive: true });
  mkdirSync(stateDir, { recursive: true });
  mkdirSync(fakeBin, { recursive: true });

  writeFileSync(join(ldmRoot, 'version.json'), JSON.stringify({ version: pkg.version }, null, 2) + '\n');

  // Canonical extension dist for crystal-capture.sh (so "Run: ldm doctor --fix" hint fires).
  // Also register memory-crystal in the registry and declare binFiles so the
  // manifest-driven knownSources lookup can find it. Mirrors the post-merge
  // state once memory-crystal-private declares its binFiles.
  const registryExtensions = {};
  if (withCanonicalShim) {
    const mcDir = join(extDir, 'memory-crystal');
    const mcDist = join(mcDir, 'dist');
    mkdirSync(mcDist, { recursive: true });
    writeFileSync(join(mcDist, 'crystal-capture.sh'), shimContent);
    chmodSync(join(mcDist, 'crystal-capture.sh'), 0o755);
    writeFileSync(join(mcDir, 'openclaw.plugin.json'), JSON.stringify({
      id: 'memory-crystal',
      name: 'Memory Crystal',
      binFiles: [{ name: 'crystal-capture.sh', source: 'dist/crystal-capture.sh' }],
    }));
    registryExtensions['memory-crystal'] = {};
  }
  writeFileSync(join(extDir, 'registry.json'), JSON.stringify({ _format: 'v2', extensions: registryExtensions }, null, 2) + '\n');

  // Fake crontab on PATH. -l prints the supplied content; anything else is a no-op.
  const crontabScript = join(fakeBin, 'crontab');
  const escaped = crontabContent.replace(/'/g, `'\\''`);
  writeFileSync(crontabScript, `#!/bin/sh\nif [ "$1" = "-l" ]; then\n  printf '%s' '${escaped}'\nfi\n`);
  chmodSync(crontabScript, 0o755);

  // npm shim (avoid network).
  const npmShim = join(fakeBin, 'npm');
  writeFileSync(npmShim, `#!/bin/sh\nexit 0\n`);
  chmodSync(npmShim, 0o755);

  return { home, ldmRoot, binDir, extDir, fakeBin, shimMode };
}

function runDoctor({ home, fakeBin, fix = false }) {
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

const CRON_CRYSTAL = '* * * * * ~/.ldm/bin/crystal-capture.sh >> ~/.ldm/logs/crystal-capture.log 2>&1\n';
const CRON_FOREIGN = '*/5 * * * * ~/.ldm/bin/foreign-tool.sh\n';

// ── Test 1: cron present, target exists and executable ──
console.log('Test 1: cron present, target healthy');
{
  const w = setupHome(CRON_CRYSTAL);
  // Seed a working shim at the cron target.
  const target = join(w.binDir, 'crystal-capture.sh');
  writeFileSync(target, '#!/bin/sh\necho ok\n');
  chmodSync(target, 0o755);
  const out = runDoctor(w);
  assert(/Cron targets under ~\/\.ldm\/bin\/: 1 entry, all exist and executable/.test(out), 'reports healthy summary', out);
  rmSync(w.home, { recursive: true, force: true });
}

// ── Test 2: cron references missing target (known shim) ──
console.log('Test 2: cron target missing, known shim');
{
  const w = setupHome(CRON_CRYSTAL);
  const out = runDoctor(w);
  assert(/cron target missing: .*crystal-capture\.sh/.test(out), 'reports "cron target missing"', out);
  assert(/Run: ldm doctor --fix to restore from/.test(out), 'suggests --fix because canonical source exists', out);
  rmSync(w.home, { recursive: true, force: true });
}

// ── Test 3: --fix restores from extension dist ──
console.log('Test 3: --fix restores from canonical source');
{
  const w = setupHome(CRON_CRYSTAL);
  const target = join(w.binDir, 'crystal-capture.sh');
  const out = runDoctor({ ...w, fix: true });
  assert(/Restored crystal-capture\.sh from/.test(out), 'announces restore', out);
  assert(existsSync(target), 'shim now exists at cron target', out);
  assert((statSync(target).mode & 0o111) !== 0, 'restored shim is executable', out);
  rmSync(w.home, { recursive: true, force: true });
}

// ── Test 4: cron target exists but not executable ──
console.log('Test 4: cron target not executable');
{
  const w = setupHome(CRON_CRYSTAL);
  const target = join(w.binDir, 'crystal-capture.sh');
  writeFileSync(target, '#!/bin/sh\necho ok\n');
  chmodSync(target, 0o644);
  const out = runDoctor(w);
  assert(/cron target not executable: .*crystal-capture\.sh/.test(out), 'reports "cron target not executable"', out);
  rmSync(w.home, { recursive: true, force: true });
}

// ── Test 5: cron references unknown target with no canonical source ──
console.log('Test 5: cron target missing, owner unknown');
{
  const w = setupHome(CRON_FOREIGN, { withCanonicalShim: false });
  const out = runDoctor(w);
  assert(/cron target missing: .*foreign-tool\.sh/.test(out), 'reports "cron target missing"', out);
  assert(/Owner unknown/.test(out), 'admits owner is unknown when no canonical source exists', out);
  rmSync(w.home, { recursive: true, force: true });
}

// ── Test 6: empty crontab ──
console.log('Test 6: empty crontab');
{
  const w = setupHome('');
  const out = runDoctor(w);
  assert(!/cron target/.test(out), 'no cron target diagnostic when crontab is empty', out);
  rmSync(w.home, { recursive: true, force: true });
}

console.log('');
if (failed > 0) {
  console.log(`${failed} test(s) failed.`);
  process.exit(1);
}
console.log('All ldm doctor cron-target tests passed.');
