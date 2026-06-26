/**
 * Tests for digest-pipeline stub-blob skipping (bug #3 from 3.0.7-rc.1 QA).
 *
 * Regression: on-chain facts can carry `encryptedBlob == "0x00"` — a 2-byte
 * zero stub used as a supersede tombstone (cheaper than writing a full
 * fact). These rows come back from subgraph searches with
 * `isActive: true`, so the digest read path saw them and tried to
 * `decryptFromHex` them unconditionally. Every stub produced a
 * `Digest: decrypt failed for <id>…: crypto error: Encrypted data too
 * short` WARN. QA saw 5 of these over ~5 minutes of normal operation
 * (7 of 25 facts on that wallet were stubs).
 *
 * Fix: centralize stub detection in `isStubBlob(hex)` and short-circuit
 * decryption at every digest decrypt site (`loadLatestDigest` picks a
 * non-stub best candidate; `fetchAllActiveClaims` skips stubs pre-decrypt).
 *
 * This test asserts:
 *   1. `isStubBlob` returns true for all known tombstone shapes and false
 *      for a plausibly-encrypted blob.
 *   2. `loadLatestDigest` with a result set of [stub_newer, real_older]
 *      returns the real_older digest (does NOT fail) and emits zero
 *      "decrypt failed" WARNs.
 *   3. `loadLatestDigest` with an all-stubs result set returns null
 *      quietly — one "no non-stub digest candidates" info log, zero
 *      "decrypt failed" WARNs.
 *   4. `fetchAllActiveClaims` with a mix of real + stub rows returns
 *      only the real rows, zero WARNs from stub decrypt attempts.
 *
 * Run with: npx tsx digest-stub-skip.test.ts
 *
 * TAP-style output, no jest dependency.
 */

import {
  fetchAllActiveClaims,
  isStubBlob,
  loadLatestDigest,
  type DigestLogger,
  type FetchAllActiveClaimsDeps,
  type LoadLatestDigestDeps,
} from './digest-sync.js';

import { buildDigestClaim } from './claims-helper.js';

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

function makeLogger(): {
  logger: DigestLogger;
  infos: string[];
  warns: string[];
} {
  const infos: string[] = [];
  const warns: string[] = [];
  return {
    infos,
    warns,
    logger: {
      info: (m) => infos.push(m),
      warn: (m) => warns.push(m),
    },
  };
}

// ---------------------------------------------------------------------------
// 1. isStubBlob — classifies tombstone shapes
// ---------------------------------------------------------------------------
{
  // Known tombstone shapes from 3.0.7-rc.1 QA
  assert(isStubBlob('0x00') === true, 'isStubBlob: "0x00" (QA-observed tombstone) → true');
  assert(isStubBlob('0x') === true, 'isStubBlob: "0x" (empty with prefix) → true');
  assert(isStubBlob('') === true, 'isStubBlob: "" (empty) → true');
  assert(isStubBlob('00') === true, 'isStubBlob: "00" (no prefix) → true');

  // Any all-zero-hex length is a tombstone shape.
  assert(isStubBlob('0x0000000000') === true, 'isStubBlob: "0x00"*5 (multi-byte zero stub) → true');

  // Plausible blobs — let decrypt attempt them. We deliberately do NOT
  // treat "short but non-zero" as a stub — that could hide genuine
  // decrypt-failure bugs in the wire format.
  assert(isStubBlob('0x01') === false, 'isStubBlob: "0x01" (1-byte non-zero) → false (not a stub; decrypt will fail loudly)');
  assert(isStubBlob('0x' + 'de'.repeat(40)) === false, 'isStubBlob: 40-byte blob → false');
  assert(isStubBlob('0x' + 'de'.repeat(120)) === false, 'isStubBlob: 120-byte plausible blob → false');

  // Uppercase / mixed case 0x prefix
  assert(isStubBlob('0X00') === true, 'isStubBlob: uppercase "0X00" → true');
}

// ---------------------------------------------------------------------------
// 2. loadLatestDigest — prefers non-stub over newer stub
// ---------------------------------------------------------------------------
{
  // Construct a real canonical digest claim via buildDigestClaim so
  // parseClaimOrLegacy + extractDigestFromClaim round-trip it. The
  // signing `sa: openclaw-plugin-digest` field is what the WASM parser
  // uses to preserve `c: 'dig'`, so we must build the claim the same
  // way the production code does instead of hand-rolling the JSON.
  const realDigestJson = JSON.stringify({
    version: 12345,
    compiled_at: '2026-04-19T18:00:00Z',
    prompt_text: 'compiled-digest-prompt',
  });
  const realCanonicalClaim = buildDigestClaim({
    digestJson: realDigestJson,
    compiledAt: '2026-04-19T18:00:00Z',
  });
  const REAL_BLOB = '0x' + 'ab'.repeat(80);
  let stubDecryptAttempts = 0;

  const deps: LoadLatestDigestDeps = {
    searchSubgraph: async () => [
      { id: 'stub000newer', encryptedBlob: '0x00', createdAt: '2000' },
      { id: 'realblob000', encryptedBlob: REAL_BLOB, createdAt: '1000' },
    ],
    decryptFromHex: (hex) => {
      if (isStubBlob(hex)) {
        stubDecryptAttempts++;
        throw new Error('Encrypted data too short');
      }
      return realCanonicalClaim;
    },
  };
  const { logger, warns } = makeLogger();

  const result = await loadLatestDigest('0xowner', 'deadbeef', Buffer.alloc(32), deps, logger);
  assert(result !== null, 'loadLatestDigest: returns a result when a real blob exists alongside a newer stub');
  assert(stubDecryptAttempts === 0, `loadLatestDigest: never calls decrypt on stub (attempts=${stubDecryptAttempts})`);
  assert(
    warns.filter((w) => w.includes('decrypt failed')).length === 0,
    `loadLatestDigest: zero "decrypt failed" warnings (got ${warns.filter((w) => w.includes('decrypt failed')).length})`,
  );
  if (result) {
    assert(result.claimId === 'realblob000', 'loadLatestDigest: picks the real blob id, not the stub id');
  }
}

// ---------------------------------------------------------------------------
// 3. loadLatestDigest — all stubs → null, zero warns
// ---------------------------------------------------------------------------
{
  let stubDecryptAttempts = 0;
  const deps: LoadLatestDigestDeps = {
    searchSubgraph: async () => [
      { id: 'stub1', encryptedBlob: '0x00', createdAt: '3000' },
      { id: 'stub2', encryptedBlob: '0x', createdAt: '2000' },
      { id: 'stub3', encryptedBlob: '', createdAt: '1000' },
    ],
    decryptFromHex: () => {
      stubDecryptAttempts++;
      throw new Error('Encrypted data too short');
    },
  };
  const { logger, warns } = makeLogger();

  const result = await loadLatestDigest('0xowner', 'deadbeef', Buffer.alloc(32), deps, logger);
  assert(result === null, 'loadLatestDigest: all-stubs result → null');
  assert(stubDecryptAttempts === 0, `loadLatestDigest: all-stubs → zero decrypt attempts (got ${stubDecryptAttempts})`);
  assert(
    warns.filter((w) => w.includes('decrypt failed')).length === 0,
    `loadLatestDigest: all-stubs → zero "decrypt failed" warnings`,
  );
}

// ---------------------------------------------------------------------------
// 4. fetchAllActiveClaims — skips stubs pre-decrypt, returns only real claims
// ---------------------------------------------------------------------------
{
  let stubDecryptAttempts = 0;
  const deps: FetchAllActiveClaimsDeps = {
    searchSubgraphBroadened: async () => [
      { id: 'real1', encryptedBlob: '0x' + 'aa'.repeat(80), isActive: true },
      { id: 'stub1', encryptedBlob: '0x00', isActive: true },
      { id: 'real2', encryptedBlob: '0x' + 'bb'.repeat(80), isActive: true },
      { id: 'stub2', encryptedBlob: '0x', isActive: true },
      { id: 'inactive1', encryptedBlob: '0x' + 'cc'.repeat(80), isActive: false },
    ],
    decryptFromHex: (hex) => {
      if (isStubBlob(hex)) {
        stubDecryptAttempts++;
        throw new Error('Encrypted data too short');
      }
      // Return a plausible canonical Claim with category 'pref' (a user-
      // facing category; `dig` and `ent` are filtered out).
      return JSON.stringify({
        c: 'pref',
        e: 'sample-fact-text-for-' + hex.slice(2, 10),
        vt: 's',
        sv: 'full',
        tv: 1,
      });
    },
  };
  const { logger, warns } = makeLogger();

  const claimsJsonStr = await fetchAllActiveClaims(
    '0xowner',
    'deadbeef',
    Buffer.alloc(32),
    100,
    deps,
    logger,
  );
  const claims = JSON.parse(claimsJsonStr) as Array<{ c: string; e: string }>;
  assert(claims.length === 2, `fetchAllActiveClaims: returns 2 real claims (got ${claims.length})`);
  assert(stubDecryptAttempts === 0, `fetchAllActiveClaims: never decrypts stubs (attempts=${stubDecryptAttempts})`);
  assert(
    warns.filter((w) => w.includes('decrypt failed')).length === 0,
    `fetchAllActiveClaims: zero "decrypt failed" warnings`,
  );
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------
console.log(`# fail: ${failed}`);
if (failed === 0) {
  console.log(`# ${passed}/${passed} passed`);
  console.log(`\nALL TESTS PASSED`);
  process.exit(0);
} else {
  console.log(`# ${passed}/${passed + failed} passed, ${failed} failed`);
  process.exit(1);
}
