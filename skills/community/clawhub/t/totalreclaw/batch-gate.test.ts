/**
 * Tests for batch-gate.ts — boot-time chain-gate predicate (#281 §9 Phase 1,
 * item imp-16).
 *
 * Covers:
 *   - default (env unset): Pro chain 100 → batch; Free chain 84532 → no batch
 *   - env=true: Pro chain → batch; Free chain → no batch
 *   - env=false: kill-switch, both chains → no batch
 *   - env=FALSE / False (case-insensitive): kill-switch active
 *   - any other value falls back to "enabled" (only `false` flips off)
 *   - unknown chain (e.g. 137 Polygon) → no batch regardless of env
 *
 * Module-import wiring is also exercised by importing the live module and
 * checking that `shouldBatchOnChain` matches the gate computed from the
 * current process env. We re-mint the predicate via the `__testing` helper
 * for the rest of the cases so each scenario reads its own simulated env.
 *
 * Run with: npx tsx batch-gate.test.ts
 */

import { shouldBatchOnChain, __testing } from './batch-gate.js';

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

const PRO_CHAIN = 100;
const FREE_CHAIN = 84532;
const UNKNOWN_CHAIN = 137;

// --- env unset → defaults ---
{
  const env: NodeJS.ProcessEnv = {};
  assert(__testing.readGateForTests(env, PRO_CHAIN) === true, 'env unset + Gnosis(100) → batch');
  assert(__testing.readGateForTests(env, FREE_CHAIN) === false, 'env unset + Sepolia(84532) → no batch');
}

// --- env=true → same as default ---
{
  const env: NodeJS.ProcessEnv = { TOTALRECLAW_GNOSIS_BATCH_ENABLED: 'true' };
  assert(__testing.readGateForTests(env, PRO_CHAIN) === true, 'env=true + Gnosis(100) → batch');
  assert(__testing.readGateForTests(env, FREE_CHAIN) === false, 'env=true + Sepolia(84532) → no batch');
}

// --- env=false → kill switch, batching off everywhere ---
{
  const env: NodeJS.ProcessEnv = { TOTALRECLAW_GNOSIS_BATCH_ENABLED: 'false' };
  assert(__testing.readGateForTests(env, PRO_CHAIN) === false, 'env=false + Gnosis(100) → no batch (kill-switch)');
  assert(__testing.readGateForTests(env, FREE_CHAIN) === false, 'env=false + Sepolia(84532) → no batch');
}

// --- case-insensitive false ---
{
  const env: NodeJS.ProcessEnv = { TOTALRECLAW_GNOSIS_BATCH_ENABLED: 'FALSE' };
  assert(__testing.readGateForTests(env, PRO_CHAIN) === false, 'env=FALSE → kill-switch (case-insensitive)');
}
{
  const env: NodeJS.ProcessEnv = { TOTALRECLAW_GNOSIS_BATCH_ENABLED: 'False' };
  assert(__testing.readGateForTests(env, PRO_CHAIN) === false, 'env=False → kill-switch (mixed-case)');
}

// --- any non-"false" value keeps default behaviour ---
{
  const env: NodeJS.ProcessEnv = { TOTALRECLAW_GNOSIS_BATCH_ENABLED: '1' };
  assert(__testing.readGateForTests(env, PRO_CHAIN) === true, 'env=1 → enabled (only literal `false` flips off)');
}
{
  const env: NodeJS.ProcessEnv = { TOTALRECLAW_GNOSIS_BATCH_ENABLED: '0' };
  assert(__testing.readGateForTests(env, PRO_CHAIN) === true, 'env=0 → enabled (only literal `false` flips off)');
}
{
  const env: NodeJS.ProcessEnv = { TOTALRECLAW_GNOSIS_BATCH_ENABLED: '' };
  assert(__testing.readGateForTests(env, PRO_CHAIN) === true, 'env="" → enabled (empty treated as unset)');
}

// --- unknown chain id never batches regardless of env ---
{
  const env: NodeJS.ProcessEnv = { TOTALRECLAW_GNOSIS_BATCH_ENABLED: 'true' };
  assert(__testing.readGateForTests(env, UNKNOWN_CHAIN) === false, 'env=true + unknown chain → no batch');
}
{
  const env: NodeJS.ProcessEnv = { TOTALRECLAW_GNOSIS_BATCH_ENABLED: 'false' };
  assert(__testing.readGateForTests(env, UNKNOWN_CHAIN) === false, 'env=false + unknown chain → no batch');
}

// --- live module export matches the predicate computed from real process.env ---
{
  const expectedProDefault =
    (process.env.TOTALRECLAW_GNOSIS_BATCH_ENABLED ?? '').toLowerCase() !== 'false';
  assert(
    shouldBatchOnChain(PRO_CHAIN) === expectedProDefault,
    'live export: shouldBatchOnChain(100) matches boot-time env evaluation',
  );
  assert(
    shouldBatchOnChain(FREE_CHAIN) === false,
    'live export: shouldBatchOnChain(84532) is always false (Free tier never batches)',
  );
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
