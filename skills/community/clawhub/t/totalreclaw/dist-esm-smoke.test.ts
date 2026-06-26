// scanner-sim: allow — CI-only smoke test, child_process used to spawn clean Node and verify dist ESM-loads. Not part of plugin runtime.
/**
 * dist-esm-smoke.test.ts — regression guard for issue #124.
 *
 * Background (rc.20 ship-stopper)
 *   The shipped `dist/index.js` declared `"type":"module"` but contained
 *   three runtime `require()` calls left over from an unfinished migration:
 *
 *     - `require('@totalreclaw/core')` — lazy WASM loader (smart-import path)
 *     - `require('node:url')`          — plugin-version reader fallback
 *     - `require('node:path')`         — plugin-version reader fallback
 *
 *   Bare `require` is undefined under pure-ESM Node. Every code path that
 *   touched these helpers died with `require is not defined` — including
 *   the `before_agent_start` hook (universal), the `agent_end` extraction
 *   pipeline, every `totalreclaw_*` tool, and credentials hot-reload. The
 *   plugin appeared to register cleanly but stored zero memories.
 *
 *   The pre-publish gate that should have caught this — `verify-tarball.mjs`
 *   — only ran `node --check`, which is a syntax-only inspection and does
 *   NOT execute the file. This test fills the gap by actually importing
 *   `dist/index.js` in a bare Node ESM process.
 *
 * What this test asserts
 *   1. `dist/index.js` exists (i.e. `npm run build` was run before tests).
 *   2. `node --input-type=module --eval "await import('./dist/index.js')"`
 *      completes without throwing. This proves the bundle is syntactically
 *      valid AND every top-level statement runs (including any future
 *      module-init code that may add new createRequire shapes).
 *   3. The default export resolves to a plugin object with `id === 'totalreclaw'`,
 *      matching what the OpenClaw loader expects.
 *   4. Grep guard: no bare `require(` call appears outside comments in the
 *      built dist files. This is the ESM-shape contract — every CJS-style
 *      load MUST go through createRequire (or be replaced with a static
 *      `import`). Catches the regression at the source level even before
 *      the runtime smoke fires.
 *
 * What this test does NOT do
 *   It does not invoke the OpenClaw plugin lifecycle (api.registerTool,
 *   api.registerHttpRoute, api.registerHook). Doing so would require a
 *   stub of the full OpenClaw plugin API + a faked workspace tree. The
 *   import-side smoke covers the failure mode that bit rc.20 — a `require`
 *   call evaluated at module init or during the lazy-loader path that the
 *   `before_agent_start` hook trips on every turn.
 *
 * Runtime
 *   `npx tsx dist-esm-smoke.test.ts` — wired into the npm test script.
 *   Requires `npm run build` to have been run first; the `prepack` hook
 *   builds dist/, but the test script does not auto-build, so the CI
 *   step order is:
 *     1. npm install
 *     2. npm test         (this includes import-time-smoke against ./index.ts source)
 *     3. npm run build    (emits dist/)
 *     4. npm run verify-tarball  (runs node --check on dist + tarball ship list)
 *
 *   This test belongs AFTER step 3 because it inspects dist/. We add it as
 *   a separate `npm run smoke:dist` script invoked from the publish workflow
 *   immediately after build.
 *
 * Why both this AND verify-tarball?
 *   verify-tarball is a syntax check — fast, catches mis-paths and broken
 *   parses. dist-esm-smoke is an execution check — catches runtime
 *   ReferenceErrors like the rc.20 `require is not defined`. Both are
 *   cheap (sub-second) and target different failure surfaces.
 */

import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import * as nodePath from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = nodePath.dirname(fileURLToPath(import.meta.url));
const DIST_DIR = nodePath.join(HERE, 'dist');
const DIST_INDEX = nodePath.join(DIST_DIR, 'index.js');

// ---- assertion 1 ----------------------------------------------------------
assert.ok(
  existsSync(DIST_INDEX),
  `dist-esm-smoke: ${DIST_INDEX} is missing — run \`npm run build\` from skill/plugin/ first`,
);
console.log(`ok 1 - dist/index.js exists at ${DIST_INDEX}`);

// ---- assertion 2 ----------------------------------------------------------
//
// We run this in a child process (a) to get a clean Node ESM context with
// no test-runner residue, (b) to mirror exactly how OpenClaw loads the
// plugin in production. `--input-type=module` forces ESM evaluation; the
// stdin path lets us pass the load script without writing a temp file.
//
// We import a file:// URL because Node's ESM loader on Windows does not
// accept bare relative paths from --eval/stdin scripts.
const distFileUrl = new URL(`file://${DIST_INDEX}`).href;
const child = execFileSync(
  process.execPath,
  ['--input-type=module', '-e', `await import(${JSON.stringify(distFileUrl)})`],
  { stdio: ['ignore', 'pipe', 'pipe'], encoding: 'utf-8', timeout: 60_000 },
);
// `child` is the captured stdout. We don't expect any output on success;
// we just need the process to exit 0. execFileSync throws on non-zero
// exit, so reaching this line means the import succeeded.
console.log(`ok 2 - dist/index.js imported in clean Node ESM (${child.length} bytes stdout, no throw)`);

// ---- assertion 3 ----------------------------------------------------------
//
// Re-import in this same process to actually inspect the default export.
// We can't introspect the child's exports, so this is a second load path.
// On a healthy build both loads are equivalent.
const mod = (await import(distFileUrl)) as { default?: { id?: string } };
assert.ok(
  mod.default && typeof mod.default === 'object',
  'dist-esm-smoke: dist/index.js default export must be an object',
);
assert.equal(
  mod.default.id,
  'totalreclaw',
  `dist-esm-smoke: plugin id must be "totalreclaw" (got ${JSON.stringify(mod.default.id)})`,
);
console.log(`ok 3 - dist default export has id="totalreclaw"`);

// ---- assertion 4 ----------------------------------------------------------
//
// Static-shape guard: scan every .js file in dist/ for bare `require(` calls
// outside of comments. The only acceptable shape post-rc.21 is via
// createRequire — call sites use a local binding (`requireWasm`,
// `__cjsRequire`, etc.) and NOT the bare global. Comments mentioning
// require are fine.
//
// Implementation: read each line, strip `//`-line comments, strip block
// comments crudely (nesting is rare in transpiled TS), then regex for
// the bare `require(` pattern. False-positive rate is acceptable — this
// is a pre-publish gate, not a production check.
function stripCommentsRough(src: string): string {
  // Remove block comments first (greedy, handles multi-line).
  let out = src.replace(/\/\*[\s\S]*?\*\//g, '');
  // Remove single-line comments.
  out = out
    .split('\n')
    .map((line) => {
      // Keep //-inside-string-literal alone — heuristic: only strip if //
      // is preceded by whitespace or start-of-line. Covers TS-emitted JS,
      // which never embeds // inside strings of meaningful spots.
      const idx = line.search(/(?:^|\s)\/\//);
      if (idx === -1) return line;
      return line.slice(0, idx);
    })
    .join('\n');
  return out;
}

function* walkJsFiles(dir: string): Generator<string> {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const full = nodePath.join(dir, entry.name);
    if (entry.isDirectory()) {
      yield* walkJsFiles(full);
    } else if (entry.isFile() && entry.name.endsWith('.js')) {
      yield full;
    }
  }
}

const violations: { file: string; line: number; text: string }[] = [];
for (const file of walkJsFiles(DIST_DIR)) {
  const src = readFileSync(file, 'utf-8');
  const stripped = stripCommentsRough(src);
  const lines = stripped.split('\n');
  for (let i = 0; i < lines.length; i++) {
    // Bare `require(` not preceded by `.` (so `requireWasm(` and
    // `createRequire(` are excluded), not preceded by a word char (so
    // `myrequire(` is excluded), and not followed by a `.` (cheap dedup).
    if (/(?:^|[^\w.])require\s*\(/.test(lines[i])) {
      violations.push({
        file: nodePath.relative(DIST_DIR, file),
        line: i + 1,
        text: lines[i].trim().slice(0, 160),
      });
    }
  }
}

if (violations.length > 0) {
  console.error('dist-esm-smoke: bare require() calls found in built dist:');
  for (const v of violations.slice(0, 10)) {
    console.error(`  ${v.file}:${v.line}  ${v.text}`);
  }
  if (violations.length > 10) {
    console.error(`  ... and ${violations.length - 10} more`);
  }
  console.error(
    '\nESM build (`"type":"module"`) — the bare `require` global is undefined ' +
      'at runtime. Use `createRequire(import.meta.url)` from `node:module` ' +
      'and call through that local binding (see crypto.ts / lsh.ts for the pattern). ' +
      'Issue #124 was rc.20 shipping with three of these.',
  );
  process.exit(1);
}
console.log(`ok 4 - no bare require() in dist/*.js (${violations.length} violations)`);

console.log('# fail: 0');
console.log('# 4/4 passed');
console.log('ALL TESTS PASSED');
