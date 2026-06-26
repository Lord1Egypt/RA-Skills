// scanner-sim: allow — test spawns the postinstall.mjs script under controlled fixtures to verify exit codes + marker state. Not part of plugin runtime; excluded from npm package via `!**/*.test.ts` in package.json files allowlist.
/**
 * postinstall-validate.test.ts — regression test for issue #188 / umbrella #182 F5.
 *
 * Background
 * ----------
 * The plugin's prior `postinstall` was a one-liner that unlinked
 * `.tr-partial-install` and called it a day. It never validated that
 * critical-path transitive deps actually resolved. Failure mode: npm reports
 * success, marker is cleared, OpenClaw enables the plugin — and only at LOAD
 * time (when `dist/pair-page.js` requires `@scure/bip39/wordlists/english.js`)
 * does the user see "Cannot find module". Re-running always works.
 *
 * Fix: `postinstall.mjs` validates that the plugin's own `dist/index.js` AND
 * the specific top-level transitive that bit users (`@scure/bip39/wordlists/english.js`)
 * are importable. On any failure, exit non-zero and leave the marker in place
 * so `detectPartialInstall` flags the dir as `'partial'` on the next attempt.
 *
 * Dev / CI bypass
 * ---------------
 * `postinstall.mjs` skips validation entirely when `dist/index.js` does not
 * exist. This covers the dev and CI cases where `npm install` runs before
 * `npm run build`. Test 3 below validates this bypass explicitly.
 *
 * What this test asserts
 * ----------------------
 *   1. With present `dist/index.js` AND `@scure/bip39/wordlists/english.js`
 *      reachable via node_modules: script exits 0 AND removes the marker.
 *   2. With a missing `@scure/bip39/wordlists/english.js`: script exits non-zero,
 *      stderr names the missing module, AND the marker is preserved.
 *   3. With a missing `dist/index.js` (dev/CI bypass): script exits 0 AND
 *      removes the marker (no dist means we're in dev context, skip validation).
 *   4. Production failure mode mimic: `dist/index.js` exists but transitively
 *      requires `@scure/bip39/wordlists/english.js` which is absent.
 *      Script exits non-zero, stderr names the missing transitive, marker preserved.
 *   5. No marker present on a healthy install: exit 0, marker stays absent.
 *
 * Run with: `npx tsx postinstall-validate.test.ts`
 */

import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SCRIPT_SRC = path.join(__dirname, 'postinstall.mjs');

const PARTIAL_INSTALL_MARKER = '.tr-partial-install';

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

interface FixtureOpts {
  withDistIndex?: boolean;
  withBip39Wordlist?: boolean;
  withMarker?: boolean;
}

/**
 * Build a tmp dir that mimics a plugin install root: a copy of the
 * `postinstall.mjs` script at the root, a `dist/index.js` (optional), and a
 * `node_modules/@scure/bip39/wordlists/english.js` shim (optional).
 *
 * The shim's package.json is wired so `import('@scure/bip39/wordlists/english.js')`
 * resolves to the shim. The shim exports a `wordlist` symbol matching the
 * real package's surface — enough for postinstall.mjs to validate it.
 */
function mkPluginFixture(opts: FixtureOpts): string {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-postinstall-validate-'));

  // Copy the script under test
  fs.copyFileSync(SCRIPT_SRC, path.join(root, 'postinstall.mjs'));

  // dist/index.js — optional
  if (opts.withDistIndex) {
    const distDir = path.join(root, 'dist');
    fs.mkdirSync(distDir, { recursive: true });
    // Minimal valid ESM module — exports a default plugin object so
    // `await import('./dist/index.js')` resolves cleanly.
    fs.writeFileSync(
      path.join(distDir, 'index.js'),
      `export default { id: 'totalreclaw' };\n`,
    );
  }

  // node_modules/@scure/bip39/wordlists/english.js shim
  if (opts.withBip39Wordlist) {
    const bip39Root = path.join(root, 'node_modules', '@scure', 'bip39');
    const wordlistsDir = path.join(bip39Root, 'wordlists');
    fs.mkdirSync(wordlistsDir, { recursive: true });
    // package.json with `exports` mapping so node resolves the subpath.
    fs.writeFileSync(
      path.join(bip39Root, 'package.json'),
      JSON.stringify({
        name: '@scure/bip39',
        version: '0.0.0-test',
        type: 'module',
        exports: {
          '.': './index.js',
          './wordlists/english.js': './wordlists/english.js',
        },
      }),
    );
    fs.writeFileSync(path.join(bip39Root, 'index.js'), `export {};\n`);
    fs.writeFileSync(
      path.join(wordlistsDir, 'english.js'),
      `export const wordlist = ['abandon','ability','able'];\n`,
    );
  }

  // partial-install marker — optional
  if (opts.withMarker) {
    fs.writeFileSync(path.join(root, PARTIAL_INSTALL_MARKER), '');
  }

  return root;
}

function rmrf(p: string): void {
  try { fs.rmSync(p, { recursive: true, force: true }); } catch { /* swallow */ }
}

function runPostinstall(root: string): { code: number; stderr: string; stdout: string } {
  const result = spawnSync(process.execPath, [path.join(root, 'postinstall.mjs')], {
    cwd: root,
    encoding: 'utf-8',
  });
  return {
    code: result.status ?? -1,
    stderr: result.stderr,
    stdout: result.stdout,
  };
}

// ---------------------------------------------------------------------------
// Test 1 — happy path: dist + bip39 wordlist + marker → exit 0, marker removed
// ---------------------------------------------------------------------------
{
  const root = mkPluginFixture({
    withDistIndex: true,
    withBip39Wordlist: true,
    withMarker: true,
  });
  const markerPath = path.join(root, PARTIAL_INSTALL_MARKER);
  assert(fs.existsSync(markerPath), 'pre-run: marker present');

  const result = runPostinstall(root);
  assert(result.code === 0, `happy path: exit 0 (got ${result.code}, stderr=${result.stderr.slice(0, 200)})`);
  assert(!fs.existsSync(markerPath), 'happy path: marker removed after success');

  rmrf(root);
}

// ---------------------------------------------------------------------------
// Test 2 — missing bip39 wordlist → exit non-zero, marker preserved, stderr cites the dep
// ---------------------------------------------------------------------------
{
  const root = mkPluginFixture({
    withDistIndex: true,
    withBip39Wordlist: false,
    withMarker: true,
  });
  const markerPath = path.join(root, PARTIAL_INSTALL_MARKER);

  const result = runPostinstall(root);
  assert(result.code !== 0, `missing bip39: exit non-zero (got ${result.code})`);
  assert(fs.existsSync(markerPath), 'missing bip39: marker preserved on failure');
  assert(
    result.stderr.includes('@scure/bip39/wordlists/english.js'),
    'missing bip39: stderr names the missing module',
  );
  assert(
    result.stderr.includes('postinstall validation FAILED'),
    'missing bip39: stderr surfaces a clear "validation FAILED" header',
  );

  rmrf(root);
}

// ---------------------------------------------------------------------------
// Test 3 — dev/CI bypass: missing dist/index.js → exit 0, marker cleared
//
// When dist/ doesn't exist the script assumes a dev/CI context (build hasn't
// run yet) and skips all validation. The marker is cleared so the install
// doesn't linger as "partial" from the npm preinstall hook.
// ---------------------------------------------------------------------------
{
  const root = mkPluginFixture({
    withDistIndex: false,
    withBip39Wordlist: true,
    withMarker: true,
  });
  const markerPath = path.join(root, PARTIAL_INSTALL_MARKER);

  const result = runPostinstall(root);
  assert(result.code === 0, `dev/CI bypass (no dist): exit 0 (got ${result.code}, stderr=${result.stderr.slice(0, 200)})`);
  assert(!fs.existsSync(markerPath), 'dev/CI bypass (no dist): marker cleared on bypass');

  rmrf(root);
}

// ---------------------------------------------------------------------------
// Test 4 — production failure mode mimic:
//   dist/index.js EXISTS and imports @scure/bip39/wordlists/english.js, but
//   the wordlist is NOT in node_modules. This is exactly umbrella #182 F5 —
//   the dist artifact is fine, but a transitive failed to install. Validates
//   that the dist/index.js import in postinstall.mjs propagates the
//   underlying ERR_MODULE_NOT_FOUND.
// ---------------------------------------------------------------------------
{
  const root = mkPluginFixture({
    withDistIndex: false, // we'll write a custom dist/index.js below
    withBip39Wordlist: false,
    withMarker: true,
  });
  const distDir = path.join(root, 'dist');
  fs.mkdirSync(distDir, { recursive: true });
  fs.writeFileSync(
    path.join(distDir, 'index.js'),
    // Mirrors the real plugin: dist/index.js's transitive graph reaches
    // @scure/bip39/wordlists/english.js (via pair-page.js).
    `import './pair-page.js';\nexport default { id: 'totalreclaw' };\n`,
  );
  fs.writeFileSync(
    path.join(distDir, 'pair-page.js'),
    `import { wordlist } from '@scure/bip39/wordlists/english.js';\nexport const BIP39_ENGLISH_WORDLIST = wordlist;\n`,
  );

  const markerPath = path.join(root, PARTIAL_INSTALL_MARKER);
  const result = runPostinstall(root);
  assert(result.code !== 0, `production-mimic: exit non-zero (got ${result.code})`);
  assert(fs.existsSync(markerPath), 'production-mimic: marker preserved on failure');
  assert(
    result.stderr.includes('@scure/bip39/wordlists/english.js'),
    'production-mimic: stderr names the missing transitive',
  );

  rmrf(root);
}

// ---------------------------------------------------------------------------
// Test 5 — happy path with no marker present → still exit 0 (idempotent)
// ---------------------------------------------------------------------------
{
  const root = mkPluginFixture({
    withDistIndex: true,
    withBip39Wordlist: true,
    withMarker: false,
  });

  const result = runPostinstall(root);
  assert(result.code === 0, `no marker: exit 0 (got ${result.code}, stderr=${result.stderr.slice(0, 200)})`);
  assert(
    !fs.existsSync(path.join(root, PARTIAL_INSTALL_MARKER)),
    'no marker: dir does not gain a marker',
  );

  rmrf(root);
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
