/**
 * Regression tests for the TOTALRECLAW_SESSION_ID env var → outbound header
 * propagation (internal#127).
 *
 * Scenario:
 *   - The v1 cleanup accidentally placed TOTALRECLAW_SESSION_ID in the
 *     REMOVED_ENV_VARS list. Setting the var emitted a "ignoring removed env
 *     var(s)" warning and the value was dropped. QA harnesses that rely on
 *     the X-TotalReclaw-Session header for Axiom log filtering had no way to
 *     tag relay calls with their run id.
 *   - Fix (this PR): TOTALRECLAW_SESSION_ID is read by `getSessionId()` and
 *     forwarded via `buildRelayHeaders()` on every outbound relay call.
 *
 * These tests pin the contract: env var set → header present; var unset
 * (or empty / whitespace) → header absent.
 *
 * Run with:
 *   npx tsx relay-headers.test.ts
 */

import { buildRelayHeaders, DEFAULT_CLIENT_ID } from './relay-headers.js';
import { getSessionId, CONFIG } from './config.js';

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

// Save / restore guard so we don't leak state into other suites.
const _origSessionId = process.env.TOTALRECLAW_SESSION_ID;

// ---------------------------------------------------------------------------
// getSessionId() resolution
// ---------------------------------------------------------------------------

{
  delete process.env.TOTALRECLAW_SESSION_ID;
  assertEq(getSessionId(), null, 'getSessionId(): null when unset');

  process.env.TOTALRECLAW_SESSION_ID = '';
  assertEq(getSessionId(), null, 'getSessionId(): null when empty string');

  process.env.TOTALRECLAW_SESSION_ID = '   ';
  assertEq(getSessionId(), null, 'getSessionId(): null when whitespace only');

  process.env.TOTALRECLAW_SESSION_ID = 'qa-test-12345';
  assertEq(getSessionId(), 'qa-test-12345', 'getSessionId(): returns trimmed value when set');

  // CONFIG.sessionId is the getter form — should mirror getSessionId().
  assertEq(CONFIG.sessionId, 'qa-test-12345', 'CONFIG.sessionId: getter mirrors getSessionId()');

  // Trim whitespace.
  process.env.TOTALRECLAW_SESSION_ID = '  qa-rc20-run-7  ';
  assertEq(getSessionId(), 'qa-rc20-run-7', 'getSessionId(): trims surrounding whitespace');
}

// ---------------------------------------------------------------------------
// buildRelayHeaders() — session header propagation
// ---------------------------------------------------------------------------

{
  // Var unset → no X-TotalReclaw-Session header.
  delete process.env.TOTALRECLAW_SESSION_ID;
  const noSid = buildRelayHeaders();
  assert(
    !('X-TotalReclaw-Session' in noSid),
    'buildRelayHeaders: omits X-TotalReclaw-Session when env unset',
  );
  assertEq(
    noSid['X-TotalReclaw-Client'],
    DEFAULT_CLIENT_ID,
    'buildRelayHeaders: always sets X-TotalReclaw-Client',
  );

  // Var set → header forwarded with the env value.
  process.env.TOTALRECLAW_SESSION_ID = 'qa-test-12345';
  const withSid = buildRelayHeaders();
  assertEq(
    withSid['X-TotalReclaw-Session'],
    'qa-test-12345',
    'buildRelayHeaders: sets X-TotalReclaw-Session=qa-test-12345 when env set',
  );

  // Authorization + Content-Type overrides merge in.
  const merged = buildRelayHeaders({
    Authorization: 'Bearer deadbeef',
    'Content-Type': 'application/json',
  });
  assertEq(
    merged['X-TotalReclaw-Session'],
    'qa-test-12345',
    'buildRelayHeaders: keeps session header when overrides merged in',
  );
  assertEq(
    merged.Authorization,
    'Bearer deadbeef',
    'buildRelayHeaders: passes through Authorization override',
  );
  assertEq(
    merged['Content-Type'],
    'application/json',
    'buildRelayHeaders: passes through Content-Type override',
  );

  // Empty / whitespace value → header absent.
  process.env.TOTALRECLAW_SESSION_ID = '';
  const empty = buildRelayHeaders();
  assert(
    !('X-TotalReclaw-Session' in empty),
    'buildRelayHeaders: omits X-TotalReclaw-Session when env is empty string',
  );

  process.env.TOTALRECLAW_SESSION_ID = '   ';
  const ws = buildRelayHeaders();
  assert(
    !('X-TotalReclaw-Session' in ws),
    'buildRelayHeaders: omits X-TotalReclaw-Session when env is whitespace',
  );

  // Custom client id override.
  process.env.TOTALRECLAW_SESSION_ID = 'qa-rc20-run-7';
  const customClient = buildRelayHeaders({}, 'mcp-server:test');
  assertEq(
    customClient['X-TotalReclaw-Client'],
    'mcp-server:test',
    'buildRelayHeaders: respects custom client id',
  );
  assertEq(
    customClient['X-TotalReclaw-Session'],
    'qa-rc20-run-7',
    'buildRelayHeaders: still forwards session header with custom client id',
  );
}

// ---------------------------------------------------------------------------
// Restore + summary
// ---------------------------------------------------------------------------

if (_origSessionId === undefined) {
  delete process.env.TOTALRECLAW_SESSION_ID;
} else {
  process.env.TOTALRECLAW_SESSION_ID = _origSessionId;
}

console.log(`\n# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('\nSOME TESTS FAILED');
  process.exit(1);
}
console.log('\nALL TESTS PASSED');
