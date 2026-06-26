/**
 * Tests for billing-cache.ts (3.0.7 extraction).
 *
 * Covers round-trip read/write, TTL expiry, corrupt-cache fallback, and
 * missing-file fallback. Also verifies the chain-id sync side-effect on both
 * read and write paths.
 *
 * Run with: npx tsx billing-cache.test.ts
 *
 * TAP-style output, no jest dependency.
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

// Isolate the on-disk cache location to a temp dir BEFORE importing the
// modules under test. `CONFIG.billingCachePath` is derived from HOME at
// module-load time, so overriding HOME now redirects the cache away from
// the real `~/.totalreclaw/`.
const TEST_HOME = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-billing-cache-test-'));
process.env.HOME = TEST_HOME;

// Dynamic imports AFTER HOME override so CONFIG.billingCachePath picks up
// the test location. Node ESM caches by URL; these are the first imports.
const { readBillingCache, writeBillingCache, BILLING_CACHE_PATH, BILLING_CACHE_TTL } =
  await import('./billing-cache.js');
const { CONFIG, __resetChainIdOverrideForTests } = await import('./config.js');
import type { BillingCache } from './billing-cache.js';

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

// Safety: the redirected path must actually live under the tmp dir. If HOME
// override was defeated by caching, we'd clobber the real cache.
assert(
  BILLING_CACHE_PATH.startsWith(TEST_HOME),
  `BILLING_CACHE_PATH redirects under TEST_HOME (got: ${BILLING_CACHE_PATH})`,
);

function resetCache(): void {
  try { fs.unlinkSync(BILLING_CACHE_PATH); } catch { /* ignore */ }
}

// ---------------------------------------------------------------------------
// Sanity — constants
// ---------------------------------------------------------------------------

{
  assertEq(BILLING_CACHE_TTL, 2 * 60 * 60 * 1000, 'BILLING_CACHE_TTL is 2 hours in ms');
  assertEq(
    BILLING_CACHE_PATH,
    CONFIG.billingCachePath,
    'BILLING_CACHE_PATH tracks CONFIG.billingCachePath',
  );
}

// ---------------------------------------------------------------------------
// Missing file → null
// ---------------------------------------------------------------------------

{
  resetCache();
  assertEq(readBillingCache(), null, 'readBillingCache: returns null when file missing');
}

// ---------------------------------------------------------------------------
// Round-trip write + read
// ---------------------------------------------------------------------------

{
  resetCache();
  __resetChainIdOverrideForTests();
  const now = Date.now();
  const cache: BillingCache = {
    tier: 'free',
    free_writes_used: 3,
    free_writes_limit: 10,
    features: { llm_dedup: true, extraction_interval: 5 },
    checked_at: now,
  };
  writeBillingCache(cache);

  const read = readBillingCache();
  assert(read !== null, 'readBillingCache: round-trip read returns non-null');
  assertEq(read?.tier, 'free', 'readBillingCache: tier round-trips');
  assertEq(read?.free_writes_used, 3, 'readBillingCache: free_writes_used round-trips');
  assertEq(read?.free_writes_limit, 10, 'readBillingCache: free_writes_limit round-trips');
  assertEq(read?.features?.llm_dedup, true, 'readBillingCache: features.llm_dedup round-trips');
  assertEq(
    read?.features?.extraction_interval,
    5,
    'readBillingCache: features.extraction_interval round-trips',
  );
  assertEq(read?.checked_at, now, 'readBillingCache: checked_at round-trips');

  // Side-effect: Free tier should set chain to 84532.
  assertEq(CONFIG.chainId, 84532, 'writeBillingCache: Free tier syncs chain to 84532');
}

// ---------------------------------------------------------------------------
// Pro tier → chain 100
// ---------------------------------------------------------------------------

{
  resetCache();
  __resetChainIdOverrideForTests();
  const cache: BillingCache = {
    tier: 'pro',
    free_writes_used: 0,
    free_writes_limit: 0,
    checked_at: Date.now(),
  };
  writeBillingCache(cache);
  assertEq(CONFIG.chainId, 100, 'writeBillingCache: Pro tier syncs chain to 100 (Gnosis)');

  // readBillingCache should also sync chain when loading persisted Pro tier
  // in a cold process (simulate by resetting override then reading).
  __resetChainIdOverrideForTests();
  assertEq(CONFIG.chainId, 84532, 'pre-read: chain override reset to 84532 default');
  const read = readBillingCache();
  assertEq(read?.tier, 'pro', 'readBillingCache: reads persisted Pro tier');
  assertEq(CONFIG.chainId, 100, 'readBillingCache: Pro tier syncs chain to 100 on load');
}

// ---------------------------------------------------------------------------
// TTL expiry → null (stale entries rejected)
// ---------------------------------------------------------------------------

{
  resetCache();
  __resetChainIdOverrideForTests();
  const stale: BillingCache = {
    tier: 'pro',
    free_writes_used: 0,
    free_writes_limit: 0,
    checked_at: Date.now() - (BILLING_CACHE_TTL + 60_000), // 1 min past TTL
  };
  // Bypass writeBillingCache's chain sync — write directly so we test read
  // behaviour on a stale entry only.
  fs.writeFileSync(BILLING_CACHE_PATH, JSON.stringify(stale));
  __resetChainIdOverrideForTests();

  const read = readBillingCache();
  assertEq(read, null, 'readBillingCache: returns null when checked_at > TTL');
  // Should NOT have synced to Pro — the stale entry must not leak its tier.
  assertEq(
    CONFIG.chainId,
    84532,
    'readBillingCache: stale entry does not sync chain override',
  );
}

// ---------------------------------------------------------------------------
// checked_at missing → null (defensive — rejects malformed entries)
// ---------------------------------------------------------------------------

{
  resetCache();
  fs.writeFileSync(
    BILLING_CACHE_PATH,
    JSON.stringify({ tier: 'pro', free_writes_used: 0, free_writes_limit: 0 }),
  );
  assertEq(
    readBillingCache(),
    null,
    'readBillingCache: returns null when checked_at missing',
  );
}

// ---------------------------------------------------------------------------
// Corrupt JSON → null (no throw)
// ---------------------------------------------------------------------------

{
  resetCache();
  fs.writeFileSync(BILLING_CACHE_PATH, '{not valid json');
  assertEq(
    readBillingCache(),
    null,
    'readBillingCache: returns null on corrupt JSON (no throw)',
  );
}

// ---------------------------------------------------------------------------
// writeBillingCache creates parent dir if missing
// ---------------------------------------------------------------------------

{
  resetCache();
  // Remove the entire .totalreclaw dir so write must recreate it.
  const parentDir = path.dirname(BILLING_CACHE_PATH);
  try { fs.rmSync(parentDir, { recursive: true, force: true }); } catch { /* ignore */ }
  assert(!fs.existsSync(parentDir), 'precondition: parent dir removed');

  writeBillingCache({
    tier: 'free',
    free_writes_used: 1,
    free_writes_limit: 10,
    checked_at: Date.now(),
  });
  assert(fs.existsSync(BILLING_CACHE_PATH), 'writeBillingCache: creates parent dir + file');
}

// ---------------------------------------------------------------------------
// Cleanup + summary
// ---------------------------------------------------------------------------

resetCache();
try { fs.rmSync(TEST_HOME, { recursive: true, force: true }); } catch { /* ignore */ }

console.log(`\n# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('\nSOME TESTS FAILED');
  process.exit(1);
}
console.log('\nALL TESTS PASSED');
