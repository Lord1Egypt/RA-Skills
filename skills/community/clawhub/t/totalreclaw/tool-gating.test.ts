/**
 * Tests for the 3.2.0 before_tool_call gating predicate.
 *
 * Asserted properties:
 *   1. Every expected memory tool is in GATED_TOOL_NAMES.
 *   2. Non-memory tools (upgrade, migrate, setup, onboarding_start) are NOT gated.
 *   3. state=active never blocks gated tools.
 *   4. state=fresh blocks gated tools with a non-secret pointer.
 *   5. state=null (resolution failure) blocks gated tools (safer default).
 *   6. Unknown tool names pass through unblocked.
 *   7. The blockReason is non-secret and references the CLI wizard path.
 *   8. GATED_TOOL_NAMES is an array that can be iterated.
 *
 * Run with: npx tsx tool-gating.test.ts
 */

import {
  decideToolGate,
  isGatedToolName,
  GATED_TOOL_NAMES,
} from './tool-gating.js';
import type { OnboardingState } from './fs-helpers.js';

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

const ACTIVE: OnboardingState = { onboardingState: 'active', createdBy: 'generate', version: '3.2.0' };
const FRESH: OnboardingState = { onboardingState: 'fresh', version: '3.2.0' };

// ---------------------------------------------------------------------------
// 1. Expected gated tools
// ---------------------------------------------------------------------------
const EXPECTED_GATED = [
  'totalreclaw_remember',
  'totalreclaw_recall',
  'totalreclaw_forget',
  'totalreclaw_export',
  'totalreclaw_status',
  'totalreclaw_consolidate',
  'totalreclaw_pin',
  'totalreclaw_unpin',
  // 3.3.1-rc.2: retype + set_scope are gated (require onboarding state=active).
  'totalreclaw_retype',
  'totalreclaw_set_scope',
  'totalreclaw_import_from',
  'totalreclaw_import_batch',
];
for (const t of EXPECTED_GATED) {
  assert(isGatedToolName(t), `gated list contains "${t}"`);
}

// ---------------------------------------------------------------------------
// 2. Tools that must NOT be gated
// ---------------------------------------------------------------------------
const EXPECTED_NOT_GATED = [
  'totalreclaw_upgrade',
  'totalreclaw_migrate',
  'totalreclaw_setup',
  'totalreclaw_onboarding_start',
];
for (const t of EXPECTED_NOT_GATED) {
  assert(!isGatedToolName(t), `NOT gated: "${t}"`);
}

// ---------------------------------------------------------------------------
// 3. state=active unblocks gated tools
// ---------------------------------------------------------------------------
for (const t of EXPECTED_GATED) {
  const d = decideToolGate(t, ACTIVE);
  assert(d.block === false, `active + ${t} → NOT blocked`);
  assert(d.blockReason === undefined, `active + ${t} → no blockReason`);
}

// ---------------------------------------------------------------------------
// 4. state=fresh blocks gated tools with a non-secret pointer
// ---------------------------------------------------------------------------
for (const t of EXPECTED_GATED) {
  const d = decideToolGate(t, FRESH);
  assert(d.block === true, `fresh + ${t} → blocked`);
  assert(typeof d.blockReason === 'string' && d.blockReason.length > 0, `fresh + ${t} → blockReason present`);
  assert(d.blockReason!.includes('openclaw totalreclaw onboard'), `fresh + ${t} → blockReason references CLI`);
  // Defensive: the blockReason must NEVER leak a mnemonic (there's no mnemonic
  // to leak in this predicate, but guard against future regressions).
  assert(!d.blockReason!.match(/[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+/),
    `fresh + ${t} → blockReason does NOT look like a 12-word sequence`);
}

// ---------------------------------------------------------------------------
// 5. state=null (resolution failure) → blocks gated tools
// ---------------------------------------------------------------------------
{
  const d = decideToolGate('totalreclaw_remember', null);
  assert(d.block === true, 'null state + gated tool → blocked (safer default)');
  const d2 = decideToolGate('totalreclaw_remember', undefined);
  assert(d2.block === true, 'undefined state + gated tool → blocked (safer default)');
}

// ---------------------------------------------------------------------------
// 6. Unknown tool names pass through
// ---------------------------------------------------------------------------
{
  for (const [state, label] of [[ACTIVE, 'active'], [FRESH, 'fresh'], [null, 'null'], [undefined, 'undefined']] as const) {
    const d = decideToolGate('random_unrelated_tool', state ?? null);
    assert(d.block === false, `${label} + unknown tool → NOT blocked`);
  }
  const d = decideToolGate(undefined, FRESH);
  assert(d.block === false, 'undefined toolName → NOT blocked');
  const d2 = decideToolGate('', FRESH);
  assert(d2.block === false, 'empty toolName → NOT blocked');
}

// ---------------------------------------------------------------------------
// 7. GATED_TOOL_NAMES is immutable & iterable
// ---------------------------------------------------------------------------
{
  assert(Array.isArray(GATED_TOOL_NAMES), 'GATED_TOOL_NAMES is an array');
  assert(GATED_TOOL_NAMES.length === EXPECTED_GATED.length, `GATED_TOOL_NAMES length matches (${GATED_TOOL_NAMES.length})`);
  // Frozen — push should throw (or silently no-op in non-strict; we just
  // verify length stays the same after a mutation attempt).
  const before = GATED_TOOL_NAMES.length;
  try {
    (GATED_TOOL_NAMES as unknown as string[]).push('totalreclaw_hack');
  } catch {
    // expected in strict mode
  }
  assert(GATED_TOOL_NAMES.length === before, 'GATED_TOOL_NAMES is frozen (length unchanged after push attempt)');
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
