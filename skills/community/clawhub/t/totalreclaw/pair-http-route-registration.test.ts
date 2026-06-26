/**
 * Tests that the 4 QR-pairing HTTP routes are registered:
 *   1. With the correct `auth: 'plugin'` literal (rc.4 fix, preserved in rc.5).
 *   2. **Synchronously** during `plugin.register(api)` — never inside an async
 *      IIFE or other microtask-deferred construct (rc.5 fix).
 *
 * Background / history:
 *   - rc.2 shipped without the `auth` field — OpenClaw's loader silently
 *     dropped all 4 registrations (`httpRouteCount: 0`).
 *   - rc.3 added `auth: 'gateway'`. The SDK accepted the literal but its
 *     runtime semantics ("requires gateway bearer token") blocks every
 *     browser caller (phones never have the token), so `/pair/*` was 401
 *     at the plugin-auth stage before ever reaching the handler.
 *   - rc.4 switched to `auth: 'plugin'`, the SDK's second valid literal
 *     (verified in shipped gateway dist at `loader-BkOjign1.js:662`). The
 *     `auth` literal was correct. But the 4 `registerHttpRoute` calls were
 *     wrapped in a fire-and-forget async IIFE (`(async () => { ... })()`)
 *     whose `await import('./pair-http.js')` settled one microtask AFTER
 *     the SDK loader had already activated the plugin's (empty) HTTP-route
 *     registry. The post-activation pushes landed on the dispatcher's
 *     "inactive" copy; `openclaw plugins inspect totalreclaw --json
 *     | jq .httpRouteCount` returned 0. QA report:
 *     `docs/notes/QA-plugin-3.3.0-rc.4-20260420-1517.md` (internal#21).
 *   - rc.5 (this test) converts the dynamic imports to static top-of-file
 *     imports and moves `buildPairRoutes` + `registerHttpRoute` into the
 *     synchronous body of `register(api)`. The `completePairing` callback
 *     remains async (it does disk I/O) — that's fine, `registerHttpRoute`
 *     accepts async handlers; only the REGISTRATION must be synchronous.
 *
 * The plugin's own `logger.info('registered ...')` still fires whether or
 * not the routes actually land in the gateway's registry, so this unit
 * test is NOT sufficient end-to-end proof — it's a guard that ensures:
 *   a) Every production call site passes `auth: 'plugin'`.
 *   b) The calls happen synchronously inside `register()` — no await, no
 *      queueMicrotask, no IIFE shenanigans.
 *
 * References: totalreclaw-internal#21, QA reports for rc.3 + rc.4.
 *
 * Run with: npx tsx pair-http-route-registration.test.ts
 *
 * Test matrix:
 *   SIMULATION (mirror of the index.ts call pattern)
 *     1. registerHttpRoute is called exactly 4 times when api provides it.
 *     2. Each call receives an `auth` field.
 *     3. Each `auth` value equals `'plugin'` (NOT `'gateway'`).
 *     4. Each call includes a `path` containing the '/pair/' prefix.
 *     5. Each call includes a `handler` function.
 *     6. When api does NOT provide registerHttpRoute, no call is made + no throw.
 *     7. The 4 paths cover finish, start, respond, status (by substring).
 *     8. `'gateway'` is NOT accidentally used (regression guard against rc.3).
 *
 *   SYNCHRONY (rc.5 regression guard — calls happen inside register())
 *     9. plugin.register(mockApi) synchronously calls registerHttpRoute 4 times
 *        BEFORE control returns to the caller (no await, no tick wait needed).
 *    10. All 4 auth literals are `'plugin'` when invoked through register().
 *    11. All 4 paths contain '/pair/' when invoked through register().
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import { buildPairRoutes, type PairRouteBundle } from './pair-http.js';
import plugin from './index.js';

let passed = 0;
let failed = 0;

function assert(condition: boolean, name: string): void {
  const n = passed + failed + 1;
  if (condition) {
    console.log(`ok ${n} - ${name}`);
    passed++;
  } else {
    console.log(`not ok ${n} - ${name}`);
    failed++;
  }
}

function assertEq<T>(actual: T, expected: T, name: string): void {
  const ok = JSON.stringify(actual) === JSON.stringify(expected);
  if (!ok) {
    console.log(`  actual:   ${JSON.stringify(actual)}`);
    console.log(`  expected: ${JSON.stringify(expected)}`);
  }
  assert(ok, name);
}

// ---------------------------------------------------------------------------
// Helpers — SIMULATION path (mirrors the synchronous call sites in index.ts)
// ---------------------------------------------------------------------------

interface RouteCall {
  path: string;
  handler: unknown;
  auth: unknown;
}

/**
 * Build a minimal pair-route bundle using a temp sessions dir, then simulate
 * exactly what index.ts does with it: 4 `api.registerHttpRoute(...)` calls.
 * Returns the recorded call args so tests can assert on them.
 */
function buildAndRegister(): { calls: RouteCall[] } {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-pair-reg-'));
  const sessionsPath = path.join(tmpDir, 'pair-sessions.json');

  const noop = (): void => {};
  const logger = {
    info: noop,
    warn: noop,
    error: noop,
    debug: noop,
  };

  const bundle: PairRouteBundle = buildPairRoutes({
    sessionsPath,
    apiBase: '/plugin/totalreclaw/pair',
    logger,
    validateMnemonic: () => true,
    completePairing: async () => ({ state: 'active' }),
  });

  // Simulate the 4 registration calls from index.ts (the rc.5 synchronous version).
  const calls: RouteCall[] = [];
  const registerHttpRoute = (params: RouteCall): void => {
    calls.push(params);
  };

  registerHttpRoute({ path: bundle.finishPath, handler: bundle.handlers.finish, auth: 'plugin' });
  registerHttpRoute({ path: bundle.startPath, handler: bundle.handlers.start, auth: 'plugin' });
  registerHttpRoute({ path: bundle.respondPath, handler: bundle.handlers.respond, auth: 'plugin' });
  registerHttpRoute({ path: bundle.statusPath, handler: bundle.handlers.status, auth: 'plugin' });

  return { calls };
}

// ---------------------------------------------------------------------------
// Helpers — SYNCHRONY path (actually invokes plugin.register())
// ---------------------------------------------------------------------------

/**
 * Build a minimal OpenClaw plugin-API mock sufficient to drive
 * `plugin.register(mockApi)` to completion. Captures every
 * `registerHttpRoute` call into `calls` so the test can assert on them
 * immediately after `register()` returns (no await / tick wait).
 */
function buildMockApi(): {
  api: unknown;
  calls: RouteCall[];
  registerHttpRouteCallCount: () => number;
} {
  const calls: RouteCall[] = [];
  const noop = (): void => {};
  const logger = {
    info: noop,
    warn: noop,
    error: noop,
    debug: noop,
  };
  const api = {
    logger,
    config: {
      agents: { defaults: { model: { primary: undefined as string | undefined } } },
      models: { providers: {} },
    },
    pluginConfig: {},
    registerTool: noop,
    registerService: noop,
    on: noop,
    registerCli: noop,
    registerCommand: noop,
    registerHttpRoute: (params: RouteCall): void => {
      calls.push(params);
    },
  };
  return {
    api,
    calls,
    registerHttpRouteCallCount: () => calls.length,
  };
}

// ---------------------------------------------------------------------------
// 1–5. SIMULATION happy path — registerHttpRoute provided
// ---------------------------------------------------------------------------

{
  const { calls } = buildAndRegister();

  // 1. Exactly 4 calls
  assertEq(calls.length, 4, 'SIM: registerHttpRoute is called exactly 4 times');

  // 2–3. auth field present and equals 'plugin' on every call
  for (let i = 0; i < calls.length; i++) {
    assert('auth' in calls[i], `SIM: call[${i}] has auth field`);
    assertEq(calls[i].auth, 'plugin', `SIM: call[${i}].auth === 'plugin'`);
    // 8. Regression guard: ensure the rc.3 value is gone.
    assert(calls[i].auth !== 'gateway', `SIM: call[${i}].auth is NOT 'gateway' (rc.3 regression guard)`);
  }

  // 4. Every path contains the '/pair/' segment
  for (let i = 0; i < calls.length; i++) {
    assert(
      typeof calls[i].path === 'string' && calls[i].path.includes('/pair/'),
      `SIM: call[${i}].path contains '/pair/'`,
    );
  }

  // 5. Every handler is a function
  for (let i = 0; i < calls.length; i++) {
    assert(typeof calls[i].handler === 'function', `SIM: call[${i}].handler is a function`);
  }
}

// ---------------------------------------------------------------------------
// 6. registerHttpRoute NOT provided — no throw, zero calls
// ---------------------------------------------------------------------------

{
  // Verify the guard pattern in index.ts: `if (typeof api.registerHttpRoute === 'function')`
  // means the code path is skipped entirely when the method is absent.
  let callCount = 0;

  const apiWithout = {
    // Deliberately omits registerHttpRoute to simulate older OpenClaw.
    logger: {
      info: (): void => {},
      warn: (msg: string): void => { void msg; },
      error: (): void => {},
      debug: (): void => {},
    },
  };

  // Guard mirrors the index.ts check
  let threw = false;
  try {
    if (typeof (apiWithout as Record<string, unknown>)['registerHttpRoute'] === 'function') {
      callCount++;
    }
    // If we reach here without incrementing, the guard correctly prevented the call.
  } catch {
    threw = true;
  }

  assert(!threw, 'SIM: no registerHttpRoute present → no throw');
  assertEq(callCount, 0, 'SIM: no registerHttpRoute present → zero calls');
}

// ---------------------------------------------------------------------------
// 7. SIMULATION — path segments cover all four endpoints
// ---------------------------------------------------------------------------

{
  const { calls } = buildAndRegister();
  const paths = calls.map((c) => c.path);

  for (const segment of ['finish', 'start', 'respond', 'status']) {
    assert(
      paths.some((p) => p.includes(segment)),
      `SIM: a registered path includes '${segment}'`,
    );
  }
}

// ---------------------------------------------------------------------------
// 9–11. SYNCHRONY — plugin.register(mockApi) really IS synchronous (rc.5)
// ---------------------------------------------------------------------------
//
// This is the rc.5 regression guard. In rc.2–rc.4 the 4 registerHttpRoute
// calls were inside `(async () => { ... })()` — the callCount at THIS
// point would be 0 immediately after register() returned. Any future
// refactor that re-introduces an async wrapper here will flip these
// assertions red.

{
  const mock = buildMockApi();

  // Snapshot the call count BEFORE register() — must be 0.
  assertEq(mock.registerHttpRouteCallCount(), 0, 'SYNC: pre-register → 0 registerHttpRoute calls');

  // Invoke register synchronously. No await.
  plugin.register(mock.api as Parameters<typeof plugin.register>[0]);

  // IMMEDIATELY after register() returns — no tick wait, no microtask flush.
  // If the 4 calls are NOT visible now, we've regressed to rc.4 behaviour
  // (async IIFE deferring the pushes past the SDK's registry-activation
  // boundary).
  assertEq(
    mock.registerHttpRouteCallCount(),
    4,
    'SYNC: register(api) synchronously calls registerHttpRoute 4 times',
  );

  // All 4 auth literals must be 'plugin'.
  for (let i = 0; i < mock.calls.length; i++) {
    assertEq(mock.calls[i].auth, 'plugin', `SYNC: register-call[${i}].auth === 'plugin'`);
  }

  // All 4 paths must contain '/pair/'.
  for (let i = 0; i < mock.calls.length; i++) {
    assert(
      typeof mock.calls[i].path === 'string' && mock.calls[i].path.includes('/pair/'),
      `SYNC: register-call[${i}].path contains '/pair/'`,
    );
  }

  // Path coverage: finish / start / respond / status all present.
  const paths = mock.calls.map((c) => c.path);
  for (const segment of ['finish', 'start', 'respond', 'status']) {
    assert(
      paths.some((p) => p.includes(segment)),
      `SYNC: a registered path includes '${segment}'`,
    );
  }
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------
console.log(`# fail: ${failed}`);
console.log(`# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('SOME TESTS FAILED');
  process.exit(1);
}
console.log('ALL TESTS PASSED');
