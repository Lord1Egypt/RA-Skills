/**
 * Regression test for issue #126 (rc.20 finding F3) — `cleanupInstallStagingDirs`.
 *
 * What this asserts
 * -----------------
 *   1. After a "fresh install" simulation (extensions dir contains a real
 *      `totalreclaw/` directory and one or more orphaned
 *      `.openclaw-install-stage-*` siblings from an interrupted prior
 *      install), calling `cleanupInstallStagingDirs(pluginDir)` removes
 *      ONLY the staging-prefixed siblings. The real plugin directory
 *      stays untouched.
 *   2. The helper is idempotent — a second call on the cleaned-up
 *      directory is a no-op and returns an empty list.
 *   3. The helper accepts both the package root path
 *      (`<extensionsDir>/totalreclaw`) and the build dir
 *      (`<extensionsDir>/totalreclaw/dist`) — index.ts passes the latter
 *      after `tsc` outputs.
 *   4. Unrelated dotfile siblings (`.openclaw-cache/`, `.git/`) are NOT
 *      removed — only the precise `.openclaw-install-stage-` prefix.
 *   5. Non-directory entries with the prefix (a stray file) are skipped
 *      so the helper never deletes a regular file by accident.
 *
 * Run with: `npx tsx install-staging-cleanup.test.ts`
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import { cleanupInstallStagingDirs } from './fs-helpers.js';

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

function mkTmpExtensionsDir(): { extensionsDir: string; pluginRoot: string; pluginDist: string } {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-install-stage-'));
  const extensionsDir = path.join(root, 'extensions');
  const pluginRoot = path.join(extensionsDir, 'totalreclaw');
  const pluginDist = path.join(pluginRoot, 'dist');
  fs.mkdirSync(pluginDist, { recursive: true });
  fs.writeFileSync(path.join(pluginDist, 'index.js'), '// the real plugin entry');
  fs.writeFileSync(path.join(pluginRoot, 'package.json'), JSON.stringify({ name: '@totalreclaw/totalreclaw' }));
  return { extensionsDir, pluginRoot, pluginDist };
}

function mkOrphanStaging(extensionsDir: string, suffix: string): string {
  const stagingDir = path.join(extensionsDir, `.openclaw-install-stage-${suffix}`);
  fs.mkdirSync(path.join(stagingDir, 'dist'), { recursive: true });
  fs.writeFileSync(path.join(stagingDir, 'dist', 'index.js'), '// orphan staging copy');
  fs.writeFileSync(path.join(stagingDir, 'package.json'), JSON.stringify({ name: '@totalreclaw/totalreclaw' }));
  return stagingDir;
}

function rmrf(p: string): void {
  try { fs.rmSync(p, { recursive: true, force: true }); } catch { /* swallow */ }
}

// ---------------------------------------------------------------------------
// Test 1 — orphan staging dirs are removed; real plugin survives.
// ---------------------------------------------------------------------------
{
  const { extensionsDir, pluginRoot, pluginDist } = mkTmpExtensionsDir();
  const orphan1 = mkOrphanStaging(extensionsDir, 'aBc123');
  const orphan2 = mkOrphanStaging(extensionsDir, 'XYZ789');

  assert(fs.existsSync(orphan1) && fs.existsSync(orphan2), 'orphan staging dirs exist before cleanup');

  const removed = cleanupInstallStagingDirs(pluginDist);

  assert(removed.length === 2, 'cleanup returns the 2 removed orphan paths');
  assert(!fs.existsSync(orphan1), 'orphan #1 deleted');
  assert(!fs.existsSync(orphan2), 'orphan #2 deleted');
  assert(fs.existsSync(pluginRoot), 'real totalreclaw/ plugin dir survives');
  assert(fs.existsSync(path.join(pluginDist, 'index.js')), 'real dist/index.js survives');

  rmrf(path.dirname(extensionsDir));
}

// ---------------------------------------------------------------------------
// Test 2 — idempotent: a 2nd call on a clean tree is a no-op.
// ---------------------------------------------------------------------------
{
  const { extensionsDir, pluginDist } = mkTmpExtensionsDir();
  const removed = cleanupInstallStagingDirs(pluginDist);
  assert(removed.length === 0, 'no orphans → empty removed list');
  assert(fs.readdirSync(extensionsDir).length === 1, 'only the real totalreclaw/ remains');
  rmrf(path.dirname(extensionsDir));
}

// ---------------------------------------------------------------------------
// Test 3 — works when called with the package-root path (not just dist/).
// ---------------------------------------------------------------------------
{
  const { extensionsDir, pluginRoot } = mkTmpExtensionsDir();
  const orphan = mkOrphanStaging(extensionsDir, 'pkgRootCase');
  const removed = cleanupInstallStagingDirs(pluginRoot);
  assert(removed.length === 1, 'cleanup also accepts package-root pluginDir');
  assert(!fs.existsSync(orphan), 'orphan deleted via package-root call');
  rmrf(path.dirname(extensionsDir));
}

// ---------------------------------------------------------------------------
// Test 4 — unrelated dotfile siblings are NOT removed.
// ---------------------------------------------------------------------------
{
  const { extensionsDir, pluginDist } = mkTmpExtensionsDir();
  const unrelated1 = path.join(extensionsDir, '.openclaw-cache');
  const unrelated2 = path.join(extensionsDir, '.git');
  fs.mkdirSync(unrelated1, { recursive: true });
  fs.mkdirSync(unrelated2, { recursive: true });

  const orphan = mkOrphanStaging(extensionsDir, 'targeted');
  const removed = cleanupInstallStagingDirs(pluginDist);

  assert(removed.length === 1, 'only the staging-prefixed dir is removed');
  assert(!fs.existsSync(orphan), 'staging orphan removed');
  assert(fs.existsSync(unrelated1), '.openclaw-cache is not touched');
  assert(fs.existsSync(unrelated2), '.git is not touched');
  rmrf(path.dirname(extensionsDir));
}

// ---------------------------------------------------------------------------
// Test 5 — non-directory entries with the prefix are skipped.
// ---------------------------------------------------------------------------
{
  const { extensionsDir, pluginDist } = mkTmpExtensionsDir();
  const filePath = path.join(extensionsDir, '.openclaw-install-stage-leftover-lockfile');
  fs.writeFileSync(filePath, '');
  const removed = cleanupInstallStagingDirs(pluginDist);
  assert(removed.length === 0, 'stray file with the prefix is not deleted');
  assert(fs.existsSync(filePath), 'file with prefix still exists after cleanup');
  rmrf(path.dirname(extensionsDir));
}

// ---------------------------------------------------------------------------
console.log(`\n${passed}/${passed + failed} passed`);
if (failed > 0) {
  process.exit(1);
}
