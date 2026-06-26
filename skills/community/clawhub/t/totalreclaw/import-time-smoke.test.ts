/**
 * import-time-smoke.test.ts — regression guard for issue #110 fix 2.
 *
 * Background
 *   rc.18 manual QA (issue #110): "Plugin init blocks CLI for ~2hr (likely
 *   ONNX 216MB synchronous download on module-load)". `embedding.ts` is
 *   already lazy (model loads on first generateEmbedding call), but this
 *   test asserts the GUARANTEE: importing the plugin's default-export
 *   completes in well under 5 seconds with no network access required.
 *
 * What this catches
 *   - Future regression that adds eager `await Auto*.from_pretrained(...)`
 *     to module-top-level (fetches ONNX, blocks for minutes on slow links).
 *   - Eager subgraph queries / api-staging round-trips at import.
 *   - Sync `fs.readFileSync` of large credentials on every import.
 *
 * Bound: 5000ms is generous (cold node + jiti + 6kLoC plugin); typical
 * macOS dev box is ~150ms. CI Linux runners are ~300-500ms. If this test
 * starts timing out without an obvious heavy-init culprit, look at new
 * top-level `await import('./...')` in index.ts.
 *
 * Runtime
 *   `npx tsx import-time-smoke.test.ts` (matches the rest of the suite).
 *
 * NOTE: this test imports the SOURCE `./index.ts` via tsx — it does NOT
 * exercise the built `dist/index.js` (the actual shipped artifact). The
 * publish workflow runs a separate `node --check dist/index.js` step in
 * `verify-tarball.mjs` that catches dist-side regressions.
 */

import assert from 'node:assert/strict';

const START = Date.now();
const mod = await import('./index.js');
const ELAPSED = Date.now() - START;

const BUDGET_MS = 5000;

assert.ok(
  typeof mod.default === 'object' && mod.default !== null,
  'plugin default export must be an object',
);
assert.equal(
  (mod.default as { id?: string }).id,
  'totalreclaw',
  'plugin id must be "totalreclaw"',
);
assert.ok(
  ELAPSED < BUDGET_MS,
  `plugin module import took ${ELAPSED}ms, budget is ${BUDGET_MS}ms — possible regression to eager ONNX load (issue #110 fix 2)`,
);

console.log(`ok 1 - plugin import took ${ELAPSED}ms (< ${BUDGET_MS}ms budget)`);
console.log('ok 2 - plugin default export is an object with id="totalreclaw"');
console.log('# fail: 0');
console.log('# 2/2 passed');
console.log('ALL TESTS PASSED');
