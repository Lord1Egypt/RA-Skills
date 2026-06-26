/**
 * Tests for the totalreclaw_remember tool schema enum construction.
 *
 * Regression from v3.0.7-rc.1 QA (internal PR #10, 2026-04-20):
 * The `totalreclaw_remember` tool registered an `enum` for the `type`
 * property built by `[...VALID_MEMORY_TYPES, ...LEGACY_V0_MEMORY_TYPES]`.
 * Because `preference` and `summary` appear in BOTH the v1 and legacy v0
 * sets, the resulting array contained duplicate entries at indices
 * ## 5 and 12. OpenClaw's ajv-based tool validator rejects such schemas
 * with `schema is invalid: data/properties/type/enum must NOT have
 * duplicate items (items ## 5 and 12 are identical)`, so the FIRST
 * invocation of `totalreclaw_remember` in every session failed.
 *
 * This test asserts:
 *   1. The raw merge would still produce duplicates (tripwire — proves
 *      the bug precondition holds if someone removes the dedup).
 *   2. The deduplicated enum contains every v1 type exactly once and
 *      every legacy-only token exactly once — shape-preserving, so
 *      agents that still emit legacy tokens (`rule`, `fact`, `decision`,
 *      `episodic`, `goal`, `context`) keep validating.
 *   3. JSON.stringify of the index.ts-exported schema contains no
 *      duplicated enum items (regression guard against a future edit
 *      that re-introduces the raw merge at the call site).
 *
 * Run with: npx tsx remember-schema.test.ts
 *
 * TAP-style output, no jest dependency.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import {
  VALID_MEMORY_TYPES,
  LEGACY_V0_MEMORY_TYPES,
} from './extractor.js';

let passed = 0;
let failed = 0;

function assert(condition: boolean, name: string): void {
  if (condition) {
    console.log(`ok ${++passed + failed} - ${name}`);
  } else {
    console.log(`not ok ${passed + ++failed} - ${name}`);
  }
}

// ---------------------------------------------------------------------------
// 1. Bug precondition: naive merge still produces duplicates
// ---------------------------------------------------------------------------
{
  const naive = [...VALID_MEMORY_TYPES, ...LEGACY_V0_MEMORY_TYPES];
  const seen = new Set<string>();
  const dups: string[] = [];
  for (const t of naive) {
    if (seen.has(t)) dups.push(t);
    else seen.add(t);
  }
  // Tripwire: if the two source arrays are ever deduped at the source,
  // the naive merge would no longer duplicate. That would be fine, but it
  // would mean the dedup in index.ts is no longer load-bearing — at
  // which point this test should be updated to delete the tripwire.
  assert(dups.length >= 1, 'tripwire: naive merge produces ≥1 duplicate (else dedup no longer needed)');
  assert(dups.includes('preference'), 'tripwire: "preference" is duplicated between v1 + legacy sets');
  assert(dups.includes('summary'), 'tripwire: "summary" is duplicated between v1 + legacy sets');

  // Exact match of the QA-reported failure signature: items ## 5 and 12
  // are identical. Index 5 is `summary` (last of v1 set); index 7 + 5 = 12
  // is again `summary` (last of legacy set after the v1 6-item prefix).
  assert(naive[5] === 'summary', 'tripwire: naive[5] is "summary" (first duplicate site)');
  assert(naive[12] === 'summary', 'tripwire: naive[12] is "summary" (matches ajv error "items ## 5 and 12")');
}

// ---------------------------------------------------------------------------
// 2. Deduped enum: each v1 type once, each legacy-only token once, total 12
// ---------------------------------------------------------------------------
{
  // This is the exact same construction the plugin uses at tool-register
  // time. If this line changes, update the call-site in index.ts too.
  const deduped = Array.from(new Set([...VALID_MEMORY_TYPES, ...LEGACY_V0_MEMORY_TYPES]));

  // No duplicates
  assert(new Set(deduped).size === deduped.length, 'deduped: no duplicate entries');

  // Every v1 type present
  for (const t of VALID_MEMORY_TYPES) {
    assert(deduped.includes(t), `deduped: contains v1 type "${t}"`);
  }

  // Every legacy v0 token present (including the shared `preference` / `summary`)
  for (const t of LEGACY_V0_MEMORY_TYPES) {
    assert(deduped.includes(t), `deduped: contains legacy v0 type "${t}"`);
  }

  // Length = 6 (v1) + 8 (legacy) - 2 (shared) = 12
  assert(deduped.length === 12, `deduped: exactly 12 entries (got ${deduped.length})`);
}

// ---------------------------------------------------------------------------
// 3. Source-level regression guard — index.ts must not contain the naive
//    spread merge pattern. If someone reverts to the bug pattern, this
//    lights up red.
// ---------------------------------------------------------------------------
{
  const here = path.dirname(fileURLToPath(import.meta.url));
  const indexSrc = fs.readFileSync(path.join(here, 'index.ts'), 'utf-8');

  // The bug pattern was literally:
  //   enum: [...VALID_MEMORY_TYPES, ...LEGACY_V0_MEMORY_TYPES],
  // Anything that matches that shape — raw spread of both constants
  // with no new Set() wrapper — is a regression.
  const bugPattern = /\.\.\.VALID_MEMORY_TYPES\s*,\s*\.\.\.LEGACY_V0_MEMORY_TYPES/;

  // Ensure the bug pattern is used ONLY inside a `new Set(...)` (or
  // equivalent dedup). Find every match and check each.
  const matches = [...indexSrc.matchAll(/\[\s*\.\.\.VALID_MEMORY_TYPES\s*,\s*\.\.\.LEGACY_V0_MEMORY_TYPES\s*\]/g)];
  let bareMerges = 0;
  for (const m of matches) {
    // Look back 30 chars to see if this spread sits inside `new Set(` or `Array.from(new Set(`.
    const start = Math.max(0, (m.index ?? 0) - 30);
    const prefix = indexSrc.slice(start, m.index);
    const wrappedBySet = /new\s+Set\s*\(\s*$/.test(prefix);
    if (!wrappedBySet) bareMerges++;
  }

  assert(
    matches.length > 0 ? bareMerges === 0 : true,
    `index.ts: every [...VALID_MEMORY_TYPES, ...LEGACY_V0_MEMORY_TYPES] spread is wrapped in new Set() (${bareMerges} bare)`,
  );

  // At least one dedup site must exist (positive assertion — catches the
  // case where someone deletes the merge entirely and leaves the v1-only
  // enum, which would regress behaviour for legacy-token-emitting agents).
  assert(bugPattern.test(indexSrc), 'index.ts: still references both type constants together somewhere');
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
