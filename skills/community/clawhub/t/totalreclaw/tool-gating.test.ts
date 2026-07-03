/**
 * Tests for the before_tool_call gating predicate (Phase 3.3 — native gate).
 *
 * Context: Task 3.2 retired the 19 `totalreclaw_*` agent tools. The agent
 * now reads memories via the bundled NATIVE `memory_search` / `memory_get`
 * tools (MemoryPluginCapability registered in index.ts). This gate now
 * targets those natives so an unpaired agent gets an actionable pointer
 * to `tr pair --url-pin` instead of silently seeing "no memories" from
 * the adapter's fail-soft path.
 *
 * Asserted properties:
 *   1. The native memory tools (memory_search, memory_get) ARE gated.
 *   2. Retired totalreclaw_* tool names are NOT in the gate (no phantom gating
 *      of tools that cannot be called — was the Task 3.3 dead-ref bug).
 *   3. state=active never blocks gated tools.
 *   4. state=fresh blocks gated tools with a non-secret pointer that references
 *      `tr pair --url-pin` (the CLI pair surface, since totalreclaw_pair is gone).
 *   5. state=null (resolution failure) blocks gated tools (safer default).
 *   6. Unknown tool names pass through unblocked.
 *   7. GATED_TOOL_NAMES is a frozen iterable array.
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
// 1. Expected gated tools — the NATIVE memory tools only
// ---------------------------------------------------------------------------
const EXPECTED_GATED = [
  'memory_search',
  'memory_get',
];
for (const t of EXPECTED_GATED) {
  assert(isGatedToolName(t), `gated list contains "${t}"`);
}

// ---------------------------------------------------------------------------
// 2. Tools that must NOT be gated
//    - The retired totalreclaw_* agent tools (Task 3.2). They can no longer
//      be called, so gating them is dead code — this guards the regression
//      the Task 3.3 report flagged.
//    - The native pair surface is intentionally NOT gated (users must be
//      able to start onboarding before the vault is active).
// ---------------------------------------------------------------------------
const EXPECTED_NOT_GATED = [
  // Retired in Task 3.2 — phantom-gating these was the dead-ref bug.
  'totalreclaw_remember',
  'totalreclaw_recall',
  'totalreclaw_forget',
  'totalreclaw_export',
  'totalreclaw_status',
  'totalreclaw_pin',
  'totalreclaw_unpin',
  'totalreclaw_pair',
  'totalreclaw_import_status',
  // An unrelated bundled tool must always pass through.
  'read_file',
  'write_file',
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
  assert(d.blockReason!.includes('tr pair --url-pin'), `fresh + ${t} → blockReason references the CLI pair surface (tr pair --url-pin)`);
  // Defensive: the blockReason must NEVER leak a mnemonic (there's no mnemonic
  // to leak in this predicate, but guard against future regressions).
  assert(!d.blockReason!.match(/[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+/),
    `fresh + ${t} → blockReason does NOT look like a 12-word sequence`);
}

// ---------------------------------------------------------------------------
// 5. state=null (resolution failure) → blocks gated tools
// ---------------------------------------------------------------------------
{
  const d = decideToolGate('memory_search', null);
  assert(d.block === true, 'null state + gated tool → blocked (safer default)');
  const d2 = decideToolGate('memory_search', undefined);
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
    (GATED_TOOL_NAMES as unknown as string[]).push('memory_hack');
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
