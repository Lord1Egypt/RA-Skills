/**
 * Tests for the canonical Claim builder, entity trapdoors, and the
 * v1-default blob/read path.
 *
 * As of plugin v3.0.0:
 *   - `buildCanonicalClaim` unconditionally emits Memory Taxonomy v1 JSON
 *     (no more env gating). The v0 short-key format is gone from the write
 *     path; it only survives in `readClaimFromBlob` for legacy vault reads.
 *   - The `TOTALRECLAW_TAXONOMY_VERSION` + `TOTALRECLAW_CLAIM_FORMAT` env
 *     toggles are retired. No env-var gate tests remain.
 *
 * Run with: npx tsx claim-format.test.ts
 */

import crypto from 'node:crypto';
import {
  buildCanonicalClaim,
  computeEntityTrapdoor,
  computeEntityTrapdoors,
  mapTypeToCategory,
  readClaimFromBlob,
} from './claims-helper.js';
import type { ExtractedFact } from './extractor.js';

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
// mapTypeToCategory — accepts both v1 and legacy v0 tokens
// ---------------------------------------------------------------------------

// v1 type → short category
assert(mapTypeToCategory('claim') === 'claim', 'category: v1 claim → claim');
assert(mapTypeToCategory('preference') === 'pref', 'category: v1 preference → pref');
assert(mapTypeToCategory('directive') === 'rule', 'category: v1 directive → rule');
assert(mapTypeToCategory('commitment') === 'goal', 'category: v1 commitment → goal');
assert(mapTypeToCategory('episode') === 'epi', 'category: v1 episode → epi');
assert(mapTypeToCategory('summary') === 'sum', 'category: v1 summary → sum');

// Legacy v0 type → short category (read-side backward compat)
assert(mapTypeToCategory('fact') === 'fact', 'category: v0 fact → fact');
assert(mapTypeToCategory('decision') === 'dec', 'category: v0 decision → dec');
assert(mapTypeToCategory('episodic') === 'epi', 'category: v0 episodic → epi');
assert(mapTypeToCategory('goal') === 'goal', 'category: v0 goal → goal');
assert(mapTypeToCategory('context') === 'ctx', 'category: v0 context → ctx');
assert(mapTypeToCategory('rule') === 'rule', 'category: v0 rule → rule');

// ---------------------------------------------------------------------------
// buildCanonicalClaim — v1 output
// ---------------------------------------------------------------------------

{
  const fact: ExtractedFact = {
    text: 'Pedro chose PostgreSQL because it is relational and needs ACID.',
    type: 'claim',
    source: 'user',
    scope: 'work',
    reasoning: 'relational and needs ACID',
    importance: 8,
    confidence: 0.92,
    action: 'ADD',
    entities: [
      { name: 'Pedro', type: 'person', role: 'chooser' },
      { name: 'PostgreSQL', type: 'tool' },
    ],
  };
  const canonical = buildCanonicalClaim({
    fact,
    importance: 8,
    sourceAgent: 'openclaw-plugin',
    extractedAt: '2026-04-12T10:00:00Z',
  });

  // v1 emits long-form JSON with schema_version and long field names.
  const parsed = JSON.parse(canonical) as Record<string, unknown>;
  assertEq(parsed.text, fact.text, 'v1: text preserved');
  assertEq(parsed.type, 'claim', 'v1: type preserved');
  assertEq(parsed.source, 'user', 'v1: source preserved');
  assertEq(parsed.scope, 'work', 'v1: scope preserved');
  assertEq(parsed.reasoning, 'relational and needs ACID', 'v1: reasoning preserved');
  assertEq(parsed.importance, 8, 'v1: importance preserved');
  assertEq(parsed.confidence, 0.92, 'v1: confidence preserved');
  assertEq(parsed.created_at, '2026-04-12T10:00:00Z', 'v1: created_at preserved');
  assertEq(parsed.schema_version, '1.0', 'v1: schema_version = 1.0');
  assert(Array.isArray(parsed.entities), 'v1: entities is array');
  assert((parsed.entities as unknown[]).length === 2, 'v1: 2 entities preserved');
}

// Defensive: missing `fact.source` is auto-filled to 'user-inferred'.
{
  const fact: ExtractedFact = {
    text: 'The user lives in Lisbon.',
    type: 'claim',
    importance: 7,
    action: 'ADD',
  };
  const canonical = buildCanonicalClaim({
    fact,
    importance: 7,
    sourceAgent: 'auto-extraction',
    extractedAt: '2026-04-12T10:00:00Z',
  });
  const parsed = JSON.parse(canonical) as Record<string, unknown>;
  assertEq(parsed.source, 'user-inferred', 'v1: missing source defaults to user-inferred');
  assert(!('entities' in parsed), 'v1: entities field omitted when empty');
}

// Legacy v0 type tokens are accepted (normalized via V0_TO_V1_TYPE).
{
  const fact: ExtractedFact = {
    text: 'Chose DuckDB for analytics.',
    // This is a legacy v0 token; buildCanonicalClaim should coerce it.
    type: 'decision' as unknown as ExtractedFact['type'],
    source: 'user',
    importance: 8,
    action: 'ADD',
  };
  const canonical = buildCanonicalClaim({
    fact,
    importance: 8,
    sourceAgent: 'legacy-caller',
    extractedAt: '2026-04-12T10:00:00Z',
  });
  const parsed = JSON.parse(canonical) as Record<string, unknown>;
  assertEq(parsed.type, 'claim', 'v1: legacy "decision" coerced to "claim"');
}

// ---------------------------------------------------------------------------
// Entity trapdoors
// ---------------------------------------------------------------------------

// Deterministic: same input → same output.
{
  const a = computeEntityTrapdoor('PostgreSQL');
  const b = computeEntityTrapdoor('PostgreSQL');
  assert(a === b, 'trapdoor: deterministic for same input');
  assert(/^[0-9a-f]{64}$/.test(a), 'trapdoor: 64-hex-char SHA-256');
}

// Case / whitespace normalization: identical trapdoors.
{
  const a = computeEntityTrapdoor('PostgreSQL');
  const b = computeEntityTrapdoor('postgresql');
  const c = computeEntityTrapdoor('  POSTGRESQL  ');
  assert(a === b, 'trapdoor: case-insensitive (Postgres mixed == lower)');
  assert(a === c, 'trapdoor: whitespace trimmed');
}

// `entity:` prefix namespaces from word trapdoors.
{
  const entityTd = computeEntityTrapdoor('postgresql');
  const wordHash = crypto.createHash('sha256').update('postgresql').digest('hex');
  assert(entityTd !== wordHash, 'trapdoor: entity prefix distinct from raw word hash');

  // Independently derive: sha256('entity:postgresql')
  const expected = crypto.createHash('sha256').update('entity:postgresql').digest('hex');
  assert(entityTd === expected, 'trapdoor: equals sha256("entity:" + normalized)');
}

// Multi-entity dedup: two references to the same name → one trapdoor.
{
  const td = computeEntityTrapdoors([
    { name: 'Pedro', type: 'person' },
    { name: 'pedro', type: 'person' },
    { name: '  PEDRO ', type: 'person' },
  ]);
  assert(td.length === 1, 'trapdoors: three aliases dedup to one');
}

// Empty / undefined inputs → empty array.
{
  assert(computeEntityTrapdoors(undefined).length === 0, 'trapdoors: undefined → []');
  assert(computeEntityTrapdoors([]).length === 0, 'trapdoors: empty array → []');
}

// ---------------------------------------------------------------------------
// readClaimFromBlob — decrypted blob reader handles v1, v0 short-key,
// and plugin-legacy {text, metadata} formats transparently.
// ---------------------------------------------------------------------------

// v1 blob (long-form with schema_version).
{
  const v1Blob = JSON.stringify({
    id: '0191abcd-0000-7000-8000-000000000000',
    text: 'prefers PostgreSQL',
    type: 'preference',
    source: 'user',
    scope: 'work',
    volatility: 'stable',
    created_at: '2026-04-12T10:00:00Z',
    importance: 8,
    schema_version: '1.0',
  });
  const out = readClaimFromBlob(v1Blob);
  assertEq(out.text, 'prefers PostgreSQL', 'readClaim: v1 text');
  assertEq(out.importance, 8, 'readClaim: v1 importance');
  assertEq(out.category, 'pref', 'readClaim: v1 preference → pref category');
  assertEq(out.metadata.type, 'preference', 'readClaim: v1 metadata.type');
  assertEq(out.metadata.source, 'user', 'readClaim: v1 metadata.source');
  assertEq(out.metadata.scope, 'work', 'readClaim: v1 metadata.scope');
  assertEq(out.metadata.volatility, 'stable', 'readClaim: v1 metadata.volatility');
}

// Legacy v0 canonical Claim format — short keys.
{
  const outNew = readClaimFromBlob(
    JSON.stringify({ t: 'prefers PostgreSQL', c: 'pref', cf: 0.9, i: 8, sa: 'oc' }),
  );
  assertEq(outNew.text, 'prefers PostgreSQL', 'readClaim: v0 short-key text');
  assertEq(outNew.importance, 8, 'readClaim: v0 short-key importance');
  assertEq(outNew.category, 'pref', 'readClaim: v0 short-key category');

  // v0 with entities
  const outEntities = readClaimFromBlob(
    JSON.stringify({
      t: 'lives in Lisbon', c: 'fact', cf: 0.95, i: 9, sa: 'oc',
      e: [{ n: 'Lisbon', tp: 'place' }],
    }),
  );
  assertEq(outEntities.text, 'lives in Lisbon', 'readClaim: v0 short-key + entities text');
  assertEq(outEntities.importance, 9, 'readClaim: v0 short-key + entities importance');

  // Importance clamping (defensive — importance should be 1..10)
  const outHigh = readClaimFromBlob(JSON.stringify({ t: 'x', c: 'fact', cf: 0.9, i: 99, sa: 'oc' }));
  assertEq(outHigh.importance, 10, 'readClaim: clamps importance > 10');
  const outLow = readClaimFromBlob(JSON.stringify({ t: 'x', c: 'fact', cf: 0.9, i: 0, sa: 'oc' }));
  assertEq(outLow.importance, 1, 'readClaim: clamps importance < 1');
}

// Plugin-legacy {text, metadata} format.
{
  const outLegacy = readClaimFromBlob(
    JSON.stringify({
      text: 'legacy fact',
      metadata: { type: 'fact', importance: 0.7, source: 'auto-extraction' },
    }),
  );
  assertEq(outLegacy.text, 'legacy fact', 'readClaim: legacy text');
  assertEq(outLegacy.importance, 7, 'readClaim: legacy importance 0.7 → 7');
  assertEq(outLegacy.category, 'fact', 'readClaim: legacy category from metadata.type');

  // Legacy with 0.85 rounds to 9
  const outRound = readClaimFromBlob(
    JSON.stringify({ text: 'prefers dark mode', metadata: { type: 'preference', importance: 0.85 } }),
  );
  assertEq(outRound.importance, 9, 'readClaim: legacy 0.85 → 9 (rounded)');
  assertEq(outRound.category, 'preference', 'readClaim: legacy preference category');

  // Bare legacy — no metadata
  const outBare = readClaimFromBlob(JSON.stringify({ text: 'bare' }));
  assertEq(outBare.text, 'bare', 'readClaim: bare legacy text');
  assertEq(outBare.importance, 5, 'readClaim: bare legacy default importance');

  // Malformed JSON → fallback to raw string
  const outBad = readClaimFromBlob('not valid json');
  assertEq(outBad.text, 'not valid json', 'readClaim: malformed → raw text');
  assertEq(outBad.importance, 5, 'readClaim: malformed default importance');

  // Empty object
  const outEmpty = readClaimFromBlob('{}');
  assertEq(outEmpty.text, '{}', 'readClaim: empty object → raw fallback');

  // Digest blob (v0 canonical with c='dig')
  const outDigest = readClaimFromBlob(
    JSON.stringify({
      t: '{"prompt_text":"You are..."}',
      c: 'dig',
      cf: 1.0,
      i: 10,
      sa: 'openclaw-plugin-digest',
    }),
  );
  assertEq(outDigest.category, 'dig', 'readClaim: digest blob category');
  assertEq(outDigest.importance, 10, 'readClaim: digest blob importance');
}

// ---------------------------------------------------------------------------
// Env-var gate assertion
// ---------------------------------------------------------------------------
//
// Plugin v3.0.0 removed both TOTALRECLAW_TAXONOMY_VERSION and
// TOTALRECLAW_CLAIM_FORMAT. buildCanonicalClaim ALWAYS emits v1 regardless
// of these env vars. This test confirms the env vars have no effect on
// the write-path output.

{
  const original = {
    taxonomy: process.env.TOTALRECLAW_TAXONOMY_VERSION,
    claim: process.env.TOTALRECLAW_CLAIM_FORMAT,
  };
  try {
    const fact: ExtractedFact = {
      text: 'gate-bypass test',
      type: 'claim',
      source: 'user',
      importance: 7,
      action: 'ADD',
    };
    const input = {
      fact,
      importance: 7,
      sourceAgent: 'test',
      extractedAt: '2026-04-12T10:00:00Z',
    };

    // With "v1" gate: should emit v1.
    process.env.TOTALRECLAW_TAXONOMY_VERSION = 'v1';
    const withFlag = JSON.parse(buildCanonicalClaim(input));
    assertEq(withFlag.schema_version, '1.0', 'gate removed: TAXONOMY=v1 still yields v1');

    // Unset: default path should ALSO emit v1 (the whole point of v3.0.0).
    delete process.env.TOTALRECLAW_TAXONOMY_VERSION;
    const defaultPath = JSON.parse(buildCanonicalClaim(input));
    assertEq(defaultPath.schema_version, '1.0', 'gate removed: default path emits v1 (not v0)');

    // With "v0" (legacy): should STILL emit v1 — no toggle, no fallback.
    process.env.TOTALRECLAW_TAXONOMY_VERSION = 'v0';
    const v0Flag = JSON.parse(buildCanonicalClaim(input));
    assertEq(v0Flag.schema_version, '1.0', 'gate removed: TAXONOMY=v0 ignored, v1 emitted');

    // CLAIM_FORMAT=legacy: should ALSO be ignored; v1 still emitted.
    process.env.TOTALRECLAW_CLAIM_FORMAT = 'legacy';
    const legacyFlag = JSON.parse(buildCanonicalClaim(input));
    assertEq(legacyFlag.schema_version, '1.0', 'gate removed: CLAIM_FORMAT=legacy ignored, v1 emitted');
  } finally {
    if (original.taxonomy === undefined) delete process.env.TOTALRECLAW_TAXONOMY_VERSION;
    else process.env.TOTALRECLAW_TAXONOMY_VERSION = original.taxonomy;
    if (original.claim === undefined) delete process.env.TOTALRECLAW_CLAIM_FORMAT;
    else process.env.TOTALRECLAW_CLAIM_FORMAT = original.claim;
  }
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

console.log(`\n# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('\nSOME TESTS FAILED');
  process.exit(1);
} else {
  console.log('\nALL TESTS PASSED');
}

export {};
