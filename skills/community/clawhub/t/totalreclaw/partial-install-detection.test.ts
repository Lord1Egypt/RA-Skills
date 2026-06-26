/**
 * Regression test for rc.22 finding #5 — partial-install detection.
 *
 * Background
 * ----------
 * After an interrupted `openclaw plugins install @totalreclaw/totalreclaw`,
 * `~/.openclaw/extensions/totalreclaw/` survives in a corrupt half-state
 * (package.json present, dist/ empty or missing). On the next install retry,
 * OpenClaw's plugin loader treats the half-state as a candidate, fails the
 * manifest check, and surfaces a confusing
 *
 *     Also not a valid hook pack: Error: package.json missing openclaw.hooks
 *
 * error. The fix: detect the half-state with a precise rule set BEFORE the
 * loader gets confused, and let the recovery path wipe-and-reinstall.
 *
 * Decision rules under test (mirrors fs-helpers.ts JSDoc):
 *   1. absent dir            → 'absent'
 *   2. foreign package name  → 'foreign'
 *   3. unparsable package    → 'foreign'
 *   4. .tr-partial-install   → 'partial'  (canonical signal)
 *   5. dist/index.js missing → 'partial'  (build never finished)
 *   6. otherwise             → 'clean'
 *
 * Run with: `npx tsx partial-install-detection.test.ts`
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import {
  detectPartialInstall,
  wipePartialInstall,
  writePartialInstallMarker,
  clearPartialInstallMarker,
  PARTIAL_INSTALL_MARKER,
  PLUGIN_PACKAGE_NAME,
} from './fs-helpers.js';

let passed = 0;
let failed = 0;

function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) {
    console.log(`ok ${n} - ${name}`);
    passed++;
  } else {
    console.log(`not ok ${n} - ${name}`);
    failed++;
  }
}

function mkPluginDir(opts: {
  withPackageJson?: boolean;
  packageName?: string;
  withDistIndex?: boolean;
  withMarker?: boolean;
  invalidJson?: boolean;
}): string {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-partial-install-'));
  const pluginRoot = path.join(root, 'totalreclaw');
  fs.mkdirSync(pluginRoot, { recursive: true });
  if (opts.withPackageJson) {
    const body = opts.invalidJson
      ? '{ this is not json'
      : JSON.stringify({ name: opts.packageName ?? PLUGIN_PACKAGE_NAME, version: '3.3.1-rc.22' });
    fs.writeFileSync(path.join(pluginRoot, 'package.json'), body);
  }
  if (opts.withDistIndex) {
    fs.mkdirSync(path.join(pluginRoot, 'dist'), { recursive: true });
    fs.writeFileSync(path.join(pluginRoot, 'dist', 'index.js'), '// the real plugin entry');
  }
  if (opts.withMarker) {
    fs.writeFileSync(path.join(pluginRoot, PARTIAL_INSTALL_MARKER), '');
  }
  return pluginRoot;
}

function rmrf(p: string): void {
  try { fs.rmSync(p, { recursive: true, force: true }); } catch { /* swallow */ }
}

// ---------------------------------------------------------------------------
// Rule 1 — absent dir
// ---------------------------------------------------------------------------
{
  const detection = detectPartialInstall('/tmp/this-path-does-not-exist-xyz-rc22');
  assert(detection.status === 'absent', 'absent dir → status absent');
}

// ---------------------------------------------------------------------------
// Rules 2-3 — foreign package name + missing package.json
// ---------------------------------------------------------------------------
{
  const pluginRoot = mkPluginDir({ withPackageJson: true, packageName: '@someone/else', withDistIndex: true });
  const detection = detectPartialInstall(pluginRoot);
  assert(detection.status === 'foreign', 'foreign package.json name → status foreign');
  assert(
    detection.reasons.some((r) => r.includes('not')),
    'foreign reason names the mismatch',
  );
  rmrf(path.dirname(pluginRoot));
}

{
  const pluginRoot = mkPluginDir({ withPackageJson: false, withDistIndex: true });
  const detection = detectPartialInstall(pluginRoot);
  assert(detection.status === 'foreign', 'missing package.json → status foreign (do not touch)');
  rmrf(path.dirname(pluginRoot));
}

{
  const pluginRoot = mkPluginDir({ withPackageJson: true, invalidJson: true, withDistIndex: true });
  const detection = detectPartialInstall(pluginRoot);
  assert(detection.status === 'foreign', 'unparsable package.json → status foreign');
  rmrf(path.dirname(pluginRoot));
}

// ---------------------------------------------------------------------------
// Rule 4 — .tr-partial-install marker present → partial
// ---------------------------------------------------------------------------
{
  const pluginRoot = mkPluginDir({ withPackageJson: true, withDistIndex: true, withMarker: true });
  const detection = detectPartialInstall(pluginRoot);
  assert(detection.status === 'partial', 'marker present → status partial (rc.22 finding #5 canonical signal)');
  assert(
    detection.reasons.some((r) => r.includes(PARTIAL_INSTALL_MARKER)),
    'partial reason names the marker file',
  );
  rmrf(path.dirname(pluginRoot));
}

// ---------------------------------------------------------------------------
// Rule 5 — package.json claims us BUT dist/index.js missing → partial
// ---------------------------------------------------------------------------
{
  const pluginRoot = mkPluginDir({ withPackageJson: true, withDistIndex: false });
  const detection = detectPartialInstall(pluginRoot);
  assert(detection.status === 'partial', 'our package.json + missing dist/index.js → status partial');
  assert(
    detection.reasons.some((r) => r.includes('dist/index.js')),
    'partial reason names dist/index.js',
  );
  rmrf(path.dirname(pluginRoot));
}

// ---------------------------------------------------------------------------
// Rule 6 — fully populated → clean
// ---------------------------------------------------------------------------
{
  const pluginRoot = mkPluginDir({ withPackageJson: true, withDistIndex: true });
  const detection = detectPartialInstall(pluginRoot);
  assert(detection.status === 'clean', 'package.json + dist/index.js + no marker → status clean');
  assert(detection.reasons.length === 0, 'clean install yields zero reasons');
  rmrf(path.dirname(pluginRoot));
}

// ---------------------------------------------------------------------------
// wipePartialInstall — only acts on partial state.
// ---------------------------------------------------------------------------
{
  const pluginRoot = mkPluginDir({ withPackageJson: true, withDistIndex: false });
  assert(fs.existsSync(pluginRoot), 'partial install present pre-wipe');
  const wiped = wipePartialInstall(pluginRoot);
  assert(wiped === true, 'wipePartialInstall returns true on partial');
  assert(!fs.existsSync(pluginRoot), 'plugin dir wiped clean');
  rmrf(path.dirname(pluginRoot));
}

{
  const pluginRoot = mkPluginDir({ withPackageJson: true, withDistIndex: true });
  const wiped = wipePartialInstall(pluginRoot);
  assert(wiped === false, 'wipePartialInstall refuses to act on clean dir');
  assert(fs.existsSync(pluginRoot), 'clean dir survives wipe attempt');
  rmrf(path.dirname(pluginRoot));
}

{
  const pluginRoot = mkPluginDir({ withPackageJson: true, packageName: '@someone/else', withDistIndex: true });
  const wiped = wipePartialInstall(pluginRoot);
  assert(wiped === false, 'wipePartialInstall refuses to act on foreign dir');
  assert(fs.existsSync(pluginRoot), 'foreign dir survives wipe attempt (safety guarantee)');
  rmrf(path.dirname(pluginRoot));
}

// ---------------------------------------------------------------------------
// Marker round-trip — write then clear.
// ---------------------------------------------------------------------------
{
  const pluginRoot = mkPluginDir({ withPackageJson: true, withDistIndex: true });
  const wrote = writePartialInstallMarker(pluginRoot);
  assert(wrote === true, 'writePartialInstallMarker returns true');
  const detection = detectPartialInstall(pluginRoot);
  assert(detection.status === 'partial', 'after writing marker, detector flips clean → partial');

  const cleared = clearPartialInstallMarker(pluginRoot);
  assert(cleared === true, 'clearPartialInstallMarker returns true after write');
  const detection2 = detectPartialInstall(pluginRoot);
  assert(detection2.status === 'clean', 'after clearing marker, detector returns to clean');

  // Idempotent — second clear is a no-op.
  const cleared2 = clearPartialInstallMarker(pluginRoot);
  assert(cleared2 === false, 'clearPartialInstallMarker returns false on second call (idempotent)');
  rmrf(path.dirname(pluginRoot));
}

// ---------------------------------------------------------------------------
// Cryptic loader error path — confirm baseline reproduces and fix prevents.
//
// The failure mode rc.22 finding #5 prescribes the fix for: a corrupt
// half-state where dist/ is missing causes OpenClaw's loader to fall through
// to "hook pack" validation and emit
//   "Also not a valid hook pack: Error: package.json missing openclaw.hooks"
// We can't actually run the OpenClaw loader in unit tests, so the proxy
// assertion is: the helper correctly classifies the half-state as `partial`
// (so the install path can wipe-and-retry instead of crashing).
// ---------------------------------------------------------------------------
{
  // Reproduction of the corrupt half-state per rc.22 finding #5.
  const pluginRoot = mkPluginDir({ withPackageJson: true, withDistIndex: false });
  // Add a partial node_modules to mirror what a half-finished `npm install` leaves.
  fs.mkdirSync(path.join(pluginRoot, 'node_modules'), { recursive: true });
  fs.writeFileSync(path.join(pluginRoot, 'node_modules', '.placeholder'), '');

  const detection = detectPartialInstall(pluginRoot);
  assert(
    detection.status === 'partial',
    'corrupt half-state from rc.22 finding #5 reproducer is detected as partial',
  );
  assert(
    detection.reasons.length > 0,
    'detector returns at least one human-readable reason for the partial verdict',
  );

  // Fix path: wipe + retry.
  const wiped = wipePartialInstall(pluginRoot);
  assert(wiped === true, 'wipe path executes on the rc.22 finding #5 reproducer');
  assert(
    !fs.existsSync(pluginRoot),
    'after wipe, dir is gone — the next `openclaw plugins install` starts fresh',
  );
  rmrf(path.dirname(pluginRoot));
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------
console.log(`\n${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('\nSOME TESTS FAILED');
  process.exit(1);
}
console.log('\nALL TESTS PASSED');
