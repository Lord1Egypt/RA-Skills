// scanner-sim: allow — postinstall validation script; not part of plugin runtime; excluded from npm package by !**/*.test.ts is not needed here since it's *.mjs, but the files allowlist in package.json explicitly includes it.
/**
 * postinstall.mjs — runs after `npm install` of @totalreclaw/totalreclaw.
 *
 * Why this script exists (issue #188 / umbrella #182 F5)
 * ------------------------------------------------------
 * Prior postinstall was a one-liner that just unlinked `.tr-partial-install`.
 * It never validated that critical-path transitive deps were resolvable.
 * Failure mode: npm reports success, marker is cleared, OpenClaw enables the
 * plugin — and only at LOAD time (when `dist/pair-page.js` requires
 * `@scure/bip39/wordlists/english.js`) does the user see
 *
 *   Cannot find module '@scure/bip39/wordlists/english.js'
 *   Require stack:
 *     - .../totalreclaw/dist/pair-page.js
 *
 * Re-running the install always works because partial node_modules + npm cache
 * complete on the second pass.
 *
 * Dev / CI bypass
 * ---------------
 * This script runs as an npm postinstall hook. In development and CI the
 * package is installed from source, NOT from the published tarball, so
 * `dist/` does not exist at `npm install` time (it is created by
 * `npm run build`, which runs AFTER tests in CI). When `dist/index.js` is
 * absent we skip all validation and exit 0 — there is nothing to validate
 * yet, and a dev install should never fail loudly here.
 *
 * The validation only fires when `dist/index.js` is already present, which
 * in practice means the package was installed from the published npm tarball
 * (which always includes the built `dist/` tree).
 *
 * Fix: import the plugin's own entry (`./dist/index.js`) AND the specific
 * top-level transitive that bit users in the wild (`@scure/bip39/wordlists/english.js`).
 * If either fails to resolve, exit non-zero AND leave the marker in place so
 * `detectPartialInstall` (in fs-helpers.ts) classifies the dir as `'partial'`
 * on the next attempt and triggers the wipe-and-retry path.
 *
 * Idempotent: a healthy install runs this script every time `npm install`
 * completes; on success the marker is cleared and the script exits 0.
 *
 * Scanner-safe: pure import + filesystem; no outbound-request word markers.
 *
 * @see fs-helpers.ts (detectPartialInstall, PARTIAL_INSTALL_MARKER)
 * @see issue https://github.com/p-diogo/totalreclaw-internal/issues/188
 */

import { unlinkSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const PARTIAL_INSTALL_MARKER = '.tr-partial-install';

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const MARKER_PATH = path.join(SCRIPT_DIR, PARTIAL_INSTALL_MARKER);
const DIST_ENTRY = path.join(SCRIPT_DIR, 'dist', 'index.js');

// Dev / CI bypass: if dist/ hasn't been built yet, skip validation entirely.
// The published tarball always ships dist/; absence means we're in a dev or
// CI context where the build step hasn't run yet. Clear any stale marker and
// exit cleanly so `npm install` succeeds for contributors and CI alike.
if (!existsSync(DIST_ENTRY)) {
  try {
    if (existsSync(MARKER_PATH)) unlinkSync(MARKER_PATH);
  } catch {
    // best-effort
  }
  process.exit(0);
}

// Critical-path transitive deps that the plugin requires at LOAD time. If any
// of these fail to resolve from the plugin's node_modules, the plugin will
// crash when OpenClaw loads `dist/index.js`. Validate at install-time so the
// failure surfaces as a loud npm error, not a silent install + load crash.
//
// Keep this list minimal and aligned with actual top-level imports in the
// shipped `dist/*.js` files. Adding an entry here means: "if this can't be
// resolved, the install is broken, fail npm install."
const CRITICAL_PATH_IMPORTS = [
  // The dep that flaked in umbrella #182 F5 user QA. Direct top-level import
  // in pair-page.ts (line 46), reached via dist/index.js's import graph.
  '@scure/bip39/wordlists/english.js',
];

async function validateCriticalDeps() {
  const failures = [];

  // Validate the plugin's own entry — exercises the full transitive
  // resolution graph as it will run under OpenClaw.
  try {
    await import(DIST_ENTRY);
  } catch (err) {
    failures.push({ target: './dist/index.js', error: String(err && err.message ? err.message : err) });
  }

  // Validate each critical transitive explicitly so the diagnostic on failure
  // names the exact missing module rather than a deep import-chain stack.
  for (const spec of CRITICAL_PATH_IMPORTS) {
    try {
      await import(spec);
    } catch (err) {
      failures.push({ target: spec, error: String(err && err.message ? err.message : err) });
    }
  }

  return failures;
}

const failures = await validateCriticalDeps();

if (failures.length > 0) {
  console.error('');
  console.error('@totalreclaw/totalreclaw postinstall validation FAILED');
  console.error('---------------------------------------------------');
  for (const f of failures) {
    console.error(`  - cannot resolve: ${f.target}`);
    console.error(`      ${f.error}`);
  }
  console.error('');
  console.error('This usually means npm install left node_modules in a partial state.');
  console.error('Re-run the install (npm cache + partial state will let it complete):');
  console.error('  openclaw plugins install @totalreclaw/totalreclaw');
  console.error('');
  console.error(`Leaving ${PARTIAL_INSTALL_MARKER} marker in place so the next attempt`);
  console.error('detects the partial install and wipes before retrying.');
  process.exit(1);
}

// Success — clear the marker. Best-effort: if unlink fails (already gone,
// permission, etc.) we still exit 0 because the import validations above
// confirmed the plugin is loadable.
try {
  if (existsSync(MARKER_PATH)) unlinkSync(MARKER_PATH);
} catch {
  // swallow — see comment above
}

process.exit(0);
