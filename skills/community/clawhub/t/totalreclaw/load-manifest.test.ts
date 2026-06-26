/**
 * Regression test for issue #186 — `.loaded.json` / `.error.json` manifest writes.
 *
 * Asserts:
 *   1. `writePluginManifest` writes `.loaded.json` with the expected schema
 *      to the plugin root (parent of `dist/`).
 *   2. The manifest captures the tools array verbatim (caller controls
 *      collection — helper does not filter).
 *   3. A successful `.loaded.json` write clears any pre-existing
 *      `.error.json` from a prior failed boot.
 *   4. `writePluginError` writes `.error.json` with `loadedAt` + `error`
 *      + `stack`. It does NOT clear `.loaded.json` from a prior good boot
 *      (so the agent sees both: "last successful boot was X, current
 *      boot failed at Y").
 *   5. Both helpers accept either the plugin root OR the `dist/` subdir
 *      and resolve to the package root in both cases.
 *   6. Helpers are best-effort: writing into a missing dir returns false,
 *      never throws.
 *
 * Run with: `npx tsx load-manifest.test.ts`
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import {
  writePluginManifest,
  writePluginError,
  PLUGIN_LOADED_MANIFEST,
  PLUGIN_ERROR_MANIFEST,
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

function mkPluginTree(): { pluginRoot: string; pluginDist: string } {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-load-manifest-'));
  const pluginRoot = path.join(root, 'totalreclaw');
  const pluginDist = path.join(pluginRoot, 'dist');
  fs.mkdirSync(pluginDist, { recursive: true });
  fs.writeFileSync(path.join(pluginDist, 'index.js'), '// stub');
  fs.writeFileSync(path.join(pluginRoot, 'package.json'), JSON.stringify({ name: '@totalreclaw/totalreclaw', version: '3.3.2-rc.1' }));
  return { pluginRoot, pluginDist };
}

function rmrf(p: string): void {
  try { fs.rmSync(p, { recursive: true, force: true }); } catch { /* swallow */ }
}

// ---------------------------------------------------------------------------
// Test 1 — manifest written to plugin root with correct schema
// ---------------------------------------------------------------------------
{
  const { pluginRoot, pluginDist } = mkPluginTree();
  const ok = writePluginManifest(pluginDist, {
    loadedAt: 1234567890,
    tools: ['totalreclaw_remember', 'totalreclaw_recall', 'totalreclaw_pair'],
    version: '3.3.2-rc.1',
  });
  assert(ok === true, 'writePluginManifest returns true on success');
  const manifestPath = path.join(pluginRoot, PLUGIN_LOADED_MANIFEST);
  assert(fs.existsSync(manifestPath), '.loaded.json exists at plugin root');
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
  assert(manifest.loadedAt === 1234567890, 'loadedAt persisted');
  assert(Array.isArray(manifest.tools) && manifest.tools.length === 3, 'tools array persisted');
  assert(manifest.tools.includes('totalreclaw_pair'), 'pair tool name in manifest');
  assert(manifest.version === '3.3.2-rc.1', 'version persisted');
  rmrf(path.dirname(pluginRoot));
}

// ---------------------------------------------------------------------------
// Test 2 — successful .loaded.json clears any pre-existing .error.json
// ---------------------------------------------------------------------------
{
  const { pluginRoot, pluginDist } = mkPluginTree();
  // Seed a stale error file from a prior failed boot.
  fs.writeFileSync(path.join(pluginRoot, PLUGIN_ERROR_MANIFEST), JSON.stringify({ error: 'stale' }));
  const ok = writePluginManifest(pluginDist, {
    loadedAt: 999,
    tools: [],
    version: '3.3.2-rc.1',
  });
  assert(ok === true, 'manifest write succeeds');
  assert(!fs.existsSync(path.join(pluginRoot, PLUGIN_ERROR_MANIFEST)), 'stale .error.json was cleared');
  assert(fs.existsSync(path.join(pluginRoot, PLUGIN_LOADED_MANIFEST)), '.loaded.json present');
  rmrf(path.dirname(pluginRoot));
}

// ---------------------------------------------------------------------------
// Test 3 — error manifest is written with the expected schema
// ---------------------------------------------------------------------------
{
  const { pluginRoot, pluginDist } = mkPluginTree();
  const ok = writePluginError(pluginDist, {
    loadedAt: 555,
    error: 'register() blew up',
    stack: 'at foo (bar.js:1:1)',
    version: '3.3.2-rc.1',
  });
  assert(ok === true, 'writePluginError returns true on success');
  const errPath = path.join(pluginRoot, PLUGIN_ERROR_MANIFEST);
  assert(fs.existsSync(errPath), '.error.json exists');
  const err = JSON.parse(fs.readFileSync(errPath, 'utf-8'));
  assert(err.loadedAt === 555, 'error timestamp persisted');
  assert(err.error === 'register() blew up', 'error message persisted');
  assert(typeof err.stack === 'string' && err.stack.includes('foo'), 'stack persisted');
  rmrf(path.dirname(pluginRoot));
}

// ---------------------------------------------------------------------------
// Test 4 — error manifest does NOT clear .loaded.json from prior boot
// ---------------------------------------------------------------------------
{
  const { pluginRoot, pluginDist } = mkPluginTree();
  // Seed a successful prior-boot manifest.
  fs.writeFileSync(
    path.join(pluginRoot, PLUGIN_LOADED_MANIFEST),
    JSON.stringify({ loadedAt: 100, tools: ['x'], version: '3.3.1' }),
  );
  // Now record a failure.
  writePluginError(pluginDist, {
    loadedAt: 200,
    error: 'second boot died',
  });
  // Both should exist — agent can compare timestamps.
  assert(fs.existsSync(path.join(pluginRoot, PLUGIN_LOADED_MANIFEST)), 'prior .loaded.json survives');
  assert(fs.existsSync(path.join(pluginRoot, PLUGIN_ERROR_MANIFEST)), 'new .error.json present');
  rmrf(path.dirname(pluginRoot));
}

// ---------------------------------------------------------------------------
// Test 5 — both helpers work when called with the package root path
// ---------------------------------------------------------------------------
{
  const { pluginRoot } = mkPluginTree();
  const ok1 = writePluginManifest(pluginRoot, {
    loadedAt: 1,
    tools: ['a'],
    version: '3.3.2-rc.1',
  });
  const ok2 = writePluginError(pluginRoot, { loadedAt: 2, error: 'x' });
  // Note: in Test 5 the success-write happens first then the error-write,
  // and writePluginError does NOT clear .loaded.json — but writePluginManifest
  // DOES clear .error.json. So order matters. Reset between calls:
  rmrf(pluginRoot);
  fs.mkdirSync(path.join(pluginRoot, 'dist'), { recursive: true });
  fs.writeFileSync(path.join(pluginRoot, 'package.json'), JSON.stringify({ name: '@totalreclaw/totalreclaw' }));

  const okm = writePluginManifest(pluginRoot, { loadedAt: 1, tools: ['a'], version: 'v' });
  assert(okm === true, 'manifest write via package-root path');
  assert(fs.existsSync(path.join(pluginRoot, PLUGIN_LOADED_MANIFEST)), 'manifest at root');

  const oke = writePluginError(pluginRoot, { loadedAt: 2, error: 'x' });
  assert(oke === true, 'error write via package-root path');
  assert(fs.existsSync(path.join(pluginRoot, PLUGIN_ERROR_MANIFEST)), 'error at root');
  // Suppress unused warnings.
  void ok1; void ok2;
  rmrf(path.dirname(pluginRoot));
}

// ---------------------------------------------------------------------------
// Test 6 — best-effort: writing into a non-existent dir returns false
// ---------------------------------------------------------------------------
{
  const ghost = path.join(os.tmpdir(), 'tr-load-manifest-ghost-' + Date.now(), 'totalreclaw', 'dist');
  const okm = writePluginManifest(ghost, { loadedAt: 0, tools: [], version: 'v' });
  assert(okm === false, 'manifest write returns false (not throw) on missing dir');
  const oke = writePluginError(ghost, { loadedAt: 0, error: 'x' });
  assert(oke === false, 'error write returns false (not throw) on missing dir');
}

// ---------------------------------------------------------------------------
// Test 7 — 3.3.7-rc.1 (issue #216): bootCount increments on every register()
// + bootAt + pid are populated. Lets the user diagnose whether register()
// actually ran on container restart.
// ---------------------------------------------------------------------------
{
  const { pluginRoot, pluginDist } = mkPluginTree();
  // First boot
  writePluginManifest(pluginDist, { loadedAt: 1000, tools: ['a'], version: '3.3.7-rc.1' });
  const m1Path = path.join(pluginRoot, PLUGIN_LOADED_MANIFEST);
  const m1 = JSON.parse(fs.readFileSync(m1Path, 'utf-8'));
  assert(m1.bootCount === 1, 'first boot: bootCount = 1');
  assert(typeof m1.bootAt === 'string' && m1.bootAt.includes('T'), 'first boot: bootAt is ISO timestamp');
  assert(typeof m1.pid === 'number' && m1.pid > 0, 'first boot: pid populated');

  // Second boot (simulated)
  writePluginManifest(pluginDist, { loadedAt: 2000, tools: ['a', 'b'], version: '3.3.7-rc.1' });
  const m2 = JSON.parse(fs.readFileSync(m1Path, 'utf-8'));
  assert(m2.bootCount === 2, 'second boot: bootCount = 2 (preserved + incremented)');
  assert(m2.tools.length === 2, 'second boot: new tools captured');
  assert(m2.pid === m1.pid, 'second boot: pid stable in same process');

  // Third boot
  writePluginManifest(pluginDist, { loadedAt: 3000, tools: ['a'], version: '3.3.7-rc.1' });
  const m3 = JSON.parse(fs.readFileSync(m1Path, 'utf-8'));
  assert(m3.bootCount === 3, 'third boot: bootCount = 3');

  rmrf(path.dirname(pluginRoot));
}

// ---------------------------------------------------------------------------
// Test 8 — register() runs idempotently — repeated writes don't corrupt the
// manifest schema (regression: shape stays identical over many boots).
// ---------------------------------------------------------------------------
{
  const { pluginRoot, pluginDist } = mkPluginTree();
  for (let i = 0; i < 10; i++) {
    writePluginManifest(pluginDist, {
      loadedAt: 1000 + i,
      tools: ['totalreclaw_remember', 'totalreclaw_recall'],
      version: '3.3.7-rc.1',
    });
  }
  const m = JSON.parse(fs.readFileSync(path.join(pluginRoot, PLUGIN_LOADED_MANIFEST), 'utf-8'));
  assert(m.bootCount === 10, 'idempotent: 10 boots → bootCount = 10');
  assert(Array.isArray(m.tools) && m.tools.length === 2, 'idempotent: tools shape preserved');
  assert(m.version === '3.3.7-rc.1', 'idempotent: version preserved');
  rmrf(path.dirname(pluginRoot));
}

// ---------------------------------------------------------------------------
// Test 9 — corrupt prior manifest does NOT crash; bootCount restarts from 1.
// ---------------------------------------------------------------------------
{
  const { pluginRoot, pluginDist } = mkPluginTree();
  fs.writeFileSync(path.join(pluginRoot, PLUGIN_LOADED_MANIFEST), '{ corrupt json');
  const ok = writePluginManifest(pluginDist, { loadedAt: 1, tools: [], version: 'v' });
  assert(ok === true, 'corrupt prior manifest: write still succeeds');
  const m = JSON.parse(fs.readFileSync(path.join(pluginRoot, PLUGIN_LOADED_MANIFEST), 'utf-8'));
  assert(m.bootCount === 1, 'corrupt prior manifest: bootCount restarts at 1');
  rmrf(path.dirname(pluginRoot));
}

// ---------------------------------------------------------------------------
console.log(`\n${passed}/${passed + failed} passed`);
if (failed > 0) {
  process.exit(1);
}
