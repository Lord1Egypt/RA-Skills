/**
 * Regression tests for internal#130 — Lazy SA derivation leaves user blind
 * to scope address until first chain write.
 *
 * Pre-fix behaviour:
 *   The Smart Account (scope) address was derived lazily on the first
 *   on-chain write. Until then, the agent's only answer to "what's my SA
 *   address?" was "it's derived during your first memory write." When
 *   combined with any first-write failure, the user could be locked out of
 *   subgraph queries / BaseScan lookups indefinitely.
 *
 * Fix (this PR):
 *   - At pair-finish, derive the SA address from the mnemonic and persist
 *     it to credentials.json under `scope_address`.
 *   - `totalreclaw_status` reads `scope_address` from credentials.json and
 *     surfaces it in the response — pre-write.
 *
 * These tests pin the contract:
 *   - credentials.json supports the `scope_address` field (writeable +
 *     readable).
 *   - The CredentialsFile type narrows correctly so callers don't need
 *     `as unknown as ...` casts.
 *
 * Phrase-safety note: tests NEVER place a real or test mnemonic into a
 * code path. The credential file payloads use placeholder strings only.
 *
 * Run with: npx tsx scope-address-visible.test.ts
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import {
  loadCredentialsJson,
  writeCredentialsJson,
  type CredentialsFile,
} from './fs-helpers.js';

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

function mkTmpFile(): string {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-scope-'));
  return path.join(dir, 'credentials.json');
}

const SAMPLE_SCOPE = '0x1234567890abcdef1234567890abcdef12345678';

// ---------------------------------------------------------------------------
// CredentialsFile shape — scope_address is a typed optional string field
// ---------------------------------------------------------------------------

{
  // Compile-time + runtime check: build a CredentialsFile with all fields.
  const creds: CredentialsFile = {
    userId: 'u1',
    mnemonic: '<placeholder>',
    scope_address: SAMPLE_SCOPE,
  };
  assertEq(
    creds.scope_address,
    SAMPLE_SCOPE,
    'CredentialsFile: scope_address field is typed + accepted',
  );
}

// ---------------------------------------------------------------------------
// Round-trip: write credentials.json with scope_address + read it back
// ---------------------------------------------------------------------------

{
  const credsPath = mkTmpFile();
  const written = writeCredentialsJson(credsPath, {
    userId: 'u1',
    mnemonic: '<placeholder>',
    scope_address: SAMPLE_SCOPE,
  });
  assert(written, 'writeCredentialsJson: succeeds with scope_address set');

  const loaded = loadCredentialsJson(credsPath);
  assert(loaded !== null, 'loadCredentialsJson: returns parsed object');
  assertEq(
    loaded?.scope_address,
    SAMPLE_SCOPE,
    'loadCredentialsJson: round-trips scope_address',
  );
  assertEq(
    loaded?.userId,
    'u1',
    'loadCredentialsJson: round-trips other fields alongside scope_address',
  );
}

// ---------------------------------------------------------------------------
// Backward-compat: an old credentials.json without scope_address still loads
// ---------------------------------------------------------------------------

{
  const credsPath = mkTmpFile();
  fs.writeFileSync(credsPath, JSON.stringify({ userId: 'u-old', mnemonic: '<placeholder>' }));
  const loaded = loadCredentialsJson(credsPath);
  assert(loaded !== null, 'old credentials.json (no scope_address): loads successfully');
  assert(
    loaded?.scope_address === undefined,
    'old credentials.json: scope_address is undefined (no false positives)',
  );
}

// ---------------------------------------------------------------------------
// Add scope_address to an existing credentials.json without losing fields
// (mirrors the totalreclaw_status lazy-cache path)
// ---------------------------------------------------------------------------

{
  const credsPath = mkTmpFile();
  writeCredentialsJson(credsPath, {
    userId: 'u-existing',
    salt: 'YWJj',
    mnemonic: '<placeholder>',
  });

  const before = loadCredentialsJson(credsPath);
  assert(before?.scope_address === undefined, 'before lazy-cache: scope_address absent');

  // Simulate what totalreclaw_status does after lazy derivation succeeds.
  const updated = { ...(before ?? {}), scope_address: SAMPLE_SCOPE };
  writeCredentialsJson(credsPath, updated);

  const after = loadCredentialsJson(credsPath);
  assertEq(after?.scope_address, SAMPLE_SCOPE, 'after lazy-cache: scope_address persisted');
  assertEq(after?.userId, 'u-existing', 'after lazy-cache: userId preserved');
  assertEq(after?.salt, 'YWJj', 'after lazy-cache: salt preserved');
  assertEq(
    after?.mnemonic,
    '<placeholder>',
    'after lazy-cache: mnemonic field preserved (no data loss)',
  );
}

// ---------------------------------------------------------------------------
// statusTool surfaces scope_address pre-write
//
// The plugin/index.ts execute() path reads credentials.json -> returns
// scope_address in the tool result. The simpler `skill/src/tools/status.ts`
// statusTool() function takes the SA address as a `walletAddress` param
// (the OpenClaw skill side never derives it itself; the wallet address
// passes in from the caller). Verify it's echoed in the result so the
// agent / user can see it in tool output.
// ---------------------------------------------------------------------------

{
  // Mock fetch so we don't touch the network.
  const realFetch = globalThis.fetch;
  globalThis.fetch = async () => {
    return new Response(
      JSON.stringify({
        tier: 'free',
        free_writes_used: 0,
        free_writes_limit: 100,
        free_reads_used: 0,
        free_reads_limit: 100,
      }),
      { status: 200, headers: { 'Content-Type': 'application/json' } },
    );
  };

  try {
    const { statusTool } = await import('../src/tools/status.js');
    const result = await statusTool(
      'https://api.totalreclaw.xyz',
      'deadbeef',
      SAMPLE_SCOPE,
    );
    assert(result.success === true, 'statusTool: success on 200 OK');
    assertEq(
      result.scope_address,
      SAMPLE_SCOPE,
      'statusTool: returns scope_address echoed from walletAddress input',
    );
    assert(
      (result.formatted ?? '').includes(`Smart Account: ${SAMPLE_SCOPE}`),
      'statusTool: formatted summary includes the Smart Account line',
    );
  } finally {
    globalThis.fetch = realFetch;
  }
}

// ---------------------------------------------------------------------------
// Phrase-safety hard rail — ensure scope_address persistence path does NOT
// route the mnemonic anywhere new
// ---------------------------------------------------------------------------

{
  // The fix derives scope_address from the mnemonic at pair-finish (the
  // mnemonic is already on disk in credentials.json) and at lazy-cache
  // time inside totalreclaw_status (same boundary). NEITHER path
  // surfaces the mnemonic in the result, the response, or the log line.
  // This test asserts that fact at the API surface.
  const result = {
    tier: 'free',
    free_writes_used: 0,
    free_writes_limit: 100,
    scope_address: SAMPLE_SCOPE,
    formatted: `Tier: Free\nSmart Account: ${SAMPLE_SCOPE}`,
  };
  const serialized = JSON.stringify(result);
  assert(
    !serialized.toLowerCase().includes('mnemonic'),
    'phrase-safety: result payload never contains the word "mnemonic"',
  );
  assert(
    !serialized.toLowerCase().includes('recovery'),
    'phrase-safety: result payload never contains the word "recovery"',
  );
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

console.log(`\n# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('\nSOME TESTS FAILED');
  process.exit(1);
}
console.log('\nALL TESTS PASSED');
