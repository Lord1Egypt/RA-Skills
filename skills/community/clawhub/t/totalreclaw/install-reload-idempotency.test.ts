/**
 * Regression test for rc.22 finding #6 — gateway/reload idempotency under
 * mid-install reload pressure.
 *
 * Background — rc.22 finding #6
 * ------------------------------
 * OpenClaw's config-watcher fires `gateway/reload` whenever
 * `plugins.entries.totalreclaw` mutates (e.g. an `openclaw plugins install`
 * rewrites the entry). In-flight CLI clients see `1006 abnormal closure (no
 * close frame)` and start a 600-second wait. The proper fix lives in
 * OpenClaw — the gateway needs an "install in progress" flag that defers
 * config-watcher reload signals during an active install (or, alternatively,
 * sends a graceful close-frame so the CLI reconnects immediately).
 *
 * This test asserts the **plugin-side mitigation** that we ship in rc.22:
 * the plugin's install-state self-heal helpers MUST be perfectly idempotent.
 * If OpenClaw fires `gateway/reload` mid-install AND mid-helper-run, calling
 * the helpers a second (or third) time must be:
 *   1. crash-safe
 *   2. observably equivalent to one call (no double-wipe of healthy data)
 *   3. internally consistent (state.json / marker / cleanup lists agree)
 *
 * The fix in rc.22 is necessarily plugin-side defensive — it does NOT close
 * the upstream issue. Tracking ticket: see rc.22 finding #6 in the QA
 * report. Upstream coordination required for the canonical fix.
 *
 * Run with: `npx tsx install-reload-idempotency.test.ts`
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import {
  detectPartialInstall,
  wipePartialInstall,
  writePartialInstallMarker,
  clearPartialInstallMarker,
  cleanupInstallStagingDirs,
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

function mkExtensionsDir(): { extensionsDir: string; pluginRoot: string; pluginDist: string } {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-reload-idempotency-'));
  const extensionsDir = path.join(root, 'extensions');
  const pluginRoot = path.join(extensionsDir, 'totalreclaw');
  const pluginDist = path.join(pluginRoot, 'dist');
  fs.mkdirSync(pluginDist, { recursive: true });
  fs.writeFileSync(path.join(pluginDist, 'index.js'), '// the real plugin entry');
  fs.writeFileSync(path.join(pluginRoot, 'package.json'), JSON.stringify({ name: PLUGIN_PACKAGE_NAME }));
  return { extensionsDir, pluginRoot, pluginDist };
}

function rmrf(p: string): void {
  try { fs.rmSync(p, { recursive: true, force: true }); } catch { /* swallow */ }
}

// ---------------------------------------------------------------------------
// Test 1 — clearPartialInstallMarker called repeatedly under reload pressure
//          MUST be a no-op after the first call.
//
// Scenario: gateway/reload fires twice mid-register. Both register passes
// each clear the marker. The second clear must return false and not throw.
// ---------------------------------------------------------------------------
{
  const { pluginRoot } = mkExtensionsDir();
  writePartialInstallMarker(pluginRoot);
  assert(fs.existsSync(path.join(pluginRoot, PARTIAL_INSTALL_MARKER)), 'marker dropped pre-reload');

  // Simulate first register → clear.
  const c1 = clearPartialInstallMarker(pluginRoot);
  assert(c1 === true, 'first clear returns true');

  // Simulate gateway/reload fires → second register → clear again.
  const c2 = clearPartialInstallMarker(pluginRoot);
  assert(c2 === false, 'second clear returns false (idempotent under reload)');

  // Third (and fourth) — still safe.
  const c3 = clearPartialInstallMarker(pluginRoot);
  const c4 = clearPartialInstallMarker(pluginRoot);
  assert(c3 === false && c4 === false, 'further clears are no-ops (no crash, no thrash)');

  rmrf(pluginRoot);
}

// ---------------------------------------------------------------------------
// Test 2 — cleanupInstallStagingDirs called twice in quick succession
//          MUST not double-delete or surface errors.
//
// Scenario: gateway/reload fires while we're mid-cleanup. The cleanup ran
// once, removed the orphans, then the helper is invoked a second time as
// the reload re-enters register(). The second call sees a clean dir.
// ---------------------------------------------------------------------------
{
  const { extensionsDir, pluginDist } = mkExtensionsDir();
  // Drop two orphan staging dirs to be cleaned.
  for (const suffix of ['aaa', 'bbb']) {
    const orphan = path.join(extensionsDir, `.openclaw-install-stage-${suffix}`);
    fs.mkdirSync(path.join(orphan, 'dist'), { recursive: true });
    fs.writeFileSync(path.join(orphan, 'dist', 'index.js'), '// orphan');
    fs.writeFileSync(path.join(orphan, 'package.json'), JSON.stringify({ name: PLUGIN_PACKAGE_NAME }));
  }

  // First cleanup pass — both orphans removed.
  const removed1 = cleanupInstallStagingDirs(pluginDist);
  assert(removed1.length === 2, 'first cleanup pass removes both orphans');

  // Reload-driven second pass — no orphans left, helper returns empty list.
  const removed2 = cleanupInstallStagingDirs(pluginDist);
  assert(removed2.length === 0, 'second cleanup pass under gateway/reload is a no-op');

  // Real plugin dir untouched.
  assert(fs.existsSync(pluginDist), 'real totalreclaw/dist survives reload-driven double cleanup');

  rmrf(extensionsDir);
}

// ---------------------------------------------------------------------------
// Test 3 — detectPartialInstall called in rapid succession returns stable
//          verdict. No state mutation; a reload mid-detection cannot turn
//          a clean install into a partial one.
// ---------------------------------------------------------------------------
{
  const { pluginRoot } = mkExtensionsDir();

  const verdicts: string[] = [];
  for (let i = 0; i < 5; i++) {
    verdicts.push(detectPartialInstall(pluginRoot).status);
  }
  const allClean = verdicts.every((v) => v === 'clean');
  assert(allClean, 'detectPartialInstall is stable under repeated calls (gateway/reload safe)');

  rmrf(pluginRoot);
}

// ---------------------------------------------------------------------------
// Test 4 — wipePartialInstall is single-shot. Once a partial dir is wiped,
//          a reload-triggered second wipe attempt sees `'absent'` and is a
//          no-op. CRITICALLY: it does NOT recreate or error on the missing
//          dir.
// ---------------------------------------------------------------------------
{
  const { pluginRoot } = mkExtensionsDir();
  // Manually break the install: drop dist/index.js → partial.
  fs.unlinkSync(path.join(pluginRoot, 'dist', 'index.js'));
  assert(detectPartialInstall(pluginRoot).status === 'partial', 'baseline: partial');

  // First wipe — succeeds.
  const w1 = wipePartialInstall(pluginRoot);
  assert(w1 === true, 'first wipe succeeds');
  assert(!fs.existsSync(pluginRoot), 'plugin dir gone after first wipe');

  // Reload fires another wipe attempt. Must be a no-op (status absent).
  const w2 = wipePartialInstall(pluginRoot);
  assert(w2 === false, 'second wipe attempt on absent dir returns false (idempotent)');
  assert(!fs.existsSync(pluginRoot), 'no rogue recreation after reload-driven re-wipe attempt');

  rmrf(path.dirname(pluginRoot));
}

// ---------------------------------------------------------------------------
// Test 5 — Concurrent fire-and-forget reload attempts. We can't simulate
//          true OS-level concurrency in a unit test, but we can confirm
//          serial back-to-back invocations of all helpers stay coherent.
// ---------------------------------------------------------------------------
{
  const { pluginRoot } = mkExtensionsDir();

  // Burst: marker write, reload, clear, reload, write, clear, detect.
  writePartialInstallMarker(pluginRoot);
  clearPartialInstallMarker(pluginRoot);
  writePartialInstallMarker(pluginRoot);
  clearPartialInstallMarker(pluginRoot);
  clearPartialInstallMarker(pluginRoot);

  const final = detectPartialInstall(pluginRoot);
  assert(
    final.status === 'clean',
    'after a write/clear burst (simulating gateway/reload chatter), final state is clean',
  );

  rmrf(pluginRoot);
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
