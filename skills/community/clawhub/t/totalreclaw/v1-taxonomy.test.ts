/**
 * Tests for the Memory Taxonomy v1 integration in the OpenClaw plugin.
 *
 * Covers (deliverable G items):
 *   - v1 claim serialize → parse round-trip
 *   - Reranker with apply_source_weights: true (user > assistant on tied scores)
 *   - parseMergedResponseV1 (valid / malformed / empty)
 *   - applyProvenanceFilterLax (assistant-source capped at 7, not dropped)
 *
 * Run with: npx tsx v1-taxonomy.test.ts
 */

import {
  parseMergedResponseV1,
  applyProvenanceFilterLax,
  defaultVolatility,
  isValidMemoryTypeV1,
  V0_TO_V1_TYPE,
  type ExtractedFact,
  type MemoryTypeV1,
  type MemorySource,
} from './extractor.js';
import {
  buildCanonicalClaimV1,
  isV1Blob,
  readV1Blob,
  normalizeToV1Type,
  readClaimFromBlob,
  V1_SCHEMA_VERSION,
} from './claims-helper.js';
import { rerank, getSourceWeight, type RerankerCandidate } from './reranker.js';

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
// v1 type guards + mapping
// ---------------------------------------------------------------------------

assert(isValidMemoryTypeV1('claim'), 'v1 guard: claim is valid');
assert(isValidMemoryTypeV1('preference'), 'v1 guard: preference is valid');
assert(isValidMemoryTypeV1('directive'), 'v1 guard: directive is valid');
assert(isValidMemoryTypeV1('commitment'), 'v1 guard: commitment is valid');
assert(isValidMemoryTypeV1('episode'), 'v1 guard: episode is valid');
assert(isValidMemoryTypeV1('summary'), 'v1 guard: summary is valid');
assert(!isValidMemoryTypeV1('fact'), 'v1 guard: fact (v0) rejected');
assert(!isValidMemoryTypeV1('rule'), 'v1 guard: rule (v0) rejected');
assert(!isValidMemoryTypeV1('bogus'), 'v1 guard: unknown rejected');

assertEq(normalizeToV1Type('fact'), 'claim', 'normalize: fact → claim');
assertEq(normalizeToV1Type('decision'), 'claim', 'normalize: decision → claim');
assertEq(normalizeToV1Type('context'), 'claim', 'normalize: context → claim');
assertEq(normalizeToV1Type('rule'), 'directive', 'normalize: rule → directive');
assertEq(normalizeToV1Type('goal'), 'commitment', 'normalize: goal → commitment');
assertEq(normalizeToV1Type('episodic'), 'episode', 'normalize: episodic → episode');
assertEq(normalizeToV1Type('preference'), 'preference', 'normalize: preference → preference (passthrough)');
assertEq(normalizeToV1Type('claim'), 'claim', 'normalize: claim → claim (passthrough)');

// ---------------------------------------------------------------------------
// v0 → v1 mapping table completeness
// ---------------------------------------------------------------------------

const v0Types = ['fact', 'preference', 'decision', 'episodic', 'goal', 'context', 'summary', 'rule'] as const;
for (const t of v0Types) {
  assert(typeof V0_TO_V1_TYPE[t] === 'string', `V0_TO_V1_TYPE covers "${t}"`);
}

// ---------------------------------------------------------------------------
// buildCanonicalClaimV1 — round-trip through validateMemoryClaimV1
// ---------------------------------------------------------------------------

{
  const fact: ExtractedFact = {
    text: 'Uses PostgreSQL as the primary OLTP database',
    type: 'claim',
    source: 'user',
    scope: 'work',
    volatility: 'updatable',
    importance: 8,
    confidence: 0.95,
    action: 'ADD',
    entities: [{ name: 'PostgreSQL', type: 'tool', role: 'primary OLTP store' }],
  };
  const blob = buildCanonicalClaimV1({
    fact,
    importance: fact.importance,
    createdAt: '2026-04-17T10:00:00Z',
    id: 'claim-abc-123',
  });

  // Must parse as JSON and carry schema_version "1.0"
  const parsed = JSON.parse(blob) as Record<string, unknown>;
  assertEq(parsed.schema_version, V1_SCHEMA_VERSION, 'v1 build: schema_version is "1.0"');
  assertEq(parsed.text, fact.text, 'v1 build: text preserved');
  assertEq(parsed.type, 'claim', 'v1 build: type preserved');
  assertEq(parsed.source, 'user', 'v1 build: source preserved');
  assertEq(parsed.scope, 'work', 'v1 build: scope preserved');
  assertEq(parsed.volatility, 'updatable', 'v1 build: volatility preserved');
  assertEq(parsed.importance, 8, 'v1 build: importance preserved');
  assertEq(parsed.id, 'claim-abc-123', 'v1 build: id preserved');

  // isV1Blob should recognise it
  assert(isV1Blob(blob), 'isV1Blob: recognises new payload');

  // readV1Blob round-trip
  const read = readV1Blob(blob);
  assert(read !== null, 'readV1Blob: returns result object');
  if (read) {
    assertEq(read.text, fact.text, 'readV1Blob: text round-trip');
    assertEq(read.type, 'claim', 'readV1Blob: type round-trip');
    assertEq(read.source, 'user', 'readV1Blob: source round-trip');
    assertEq(read.scope, 'work', 'readV1Blob: scope round-trip');
    assertEq(read.volatility, 'updatable', 'readV1Blob: volatility round-trip');
    assertEq(read.importance, 8, 'readV1Blob: importance round-trip');
  }
}

// ---------------------------------------------------------------------------
// buildCanonicalClaimV1 rejects missing source (v1 mandate)
// ---------------------------------------------------------------------------

{
  let threw = false;
  try {
    buildCanonicalClaimV1({
      fact: {
        text: 'No source here',
        type: 'claim',
        importance: 7,
        action: 'ADD',
        // source deliberately missing
      } as ExtractedFact,
      importance: 7,
    });
  } catch {
    threw = true;
  }
  assert(threw, 'v1 build: throws when source is missing');
}

// ---------------------------------------------------------------------------
// buildCanonicalClaimV1 rejects invalid source
// ---------------------------------------------------------------------------

{
  let threw = false;
  try {
    buildCanonicalClaimV1({
      fact: {
        text: 'Bad source',
        type: 'claim',
        source: 'invalid-source' as MemorySource,
        importance: 7,
        action: 'ADD',
      },
      importance: 7,
    });
  } catch {
    threw = true;
  }
  assert(threw, 'v1 build: throws on invalid source');
}

// ---------------------------------------------------------------------------
// Build → serialize → parse JSON round-trip with v1 claim (simulating
// encrypt/decrypt where encryption is a no-op on the content bytes).
// Actual crypto round-trip is exercised by the E2E test suite — this file
// keeps deps minimal so `npx tsx` runs without WASM crypto init issues.
// ---------------------------------------------------------------------------

{
  const fact: ExtractedFact = {
    text: 'User wants to launch public beta by end of Q1',
    type: 'commitment',
    source: 'user',
    scope: 'work',
    volatility: 'ephemeral',
    importance: 9,
    confidence: 0.95,
    action: 'ADD',
  };
  const plaintext = buildCanonicalClaimV1({
    fact,
    importance: fact.importance,
  });
  // Simulate encrypt/decrypt: byte-identical ciphertext in a real run, so
  // plaintext-out === plaintext-in.
  const roundTripped = plaintext;
  const read = readV1Blob(roundTripped);
  assert(read !== null, 'v1 round-trip: parses back');
  if (read) {
    assertEq(read.type, 'commitment', 'v1 round-trip: type preserved');
    assertEq(read.source, 'user', 'v1 round-trip: source preserved');
    assertEq(read.volatility, 'ephemeral', 'v1 round-trip: volatility preserved');
  }
}

// ---------------------------------------------------------------------------
// readClaimFromBlob handles v1 payloads (backward-compat for callers)
// ---------------------------------------------------------------------------

{
  const blob = buildCanonicalClaimV1({
    fact: {
      text: 'Always check the systemd unit file before wiping state',
      type: 'directive',
      source: 'user',
      scope: 'work',
      volatility: 'stable',
      importance: 8,
      action: 'ADD',
    },
    importance: 8,
  });

  const result = readClaimFromBlob(blob);
  assertEq(result.text, 'Always check the systemd unit file before wiping state', 'readClaim: v1 text');
  assertEq(result.importance, 8, 'readClaim: v1 importance');
  assertEq(result.category, 'rule', 'readClaim: v1 directive → rule category');
  assertEq(result.metadata.type, 'directive', 'readClaim: v1 metadata type preserved');
  assertEq(result.metadata.source, 'user', 'readClaim: v1 metadata source preserved');
}

// ---------------------------------------------------------------------------
// readV1Blob returns null for legacy blobs
// ---------------------------------------------------------------------------

assertEq(readV1Blob(JSON.stringify({ text: 'legacy', metadata: {} })), null, 'readV1Blob: null on legacy');
assertEq(readV1Blob(JSON.stringify({ t: 'canonical', c: 'fact', i: 5 })), null, 'readV1Blob: null on v0 canonical');
assertEq(readV1Blob('not json'), null, 'readV1Blob: null on malformed');

// isV1Blob should reject legacy/v0 too
assert(!isV1Blob(JSON.stringify({ text: 'legacy', metadata: {} })), 'isV1Blob: rejects legacy');
assert(!isV1Blob(JSON.stringify({ t: 'canonical', c: 'fact', i: 5 })), 'isV1Blob: rejects v0');
assert(!isV1Blob('not json'), 'isV1Blob: rejects malformed');

// ---------------------------------------------------------------------------
// parseMergedResponseV1 — valid case
// ---------------------------------------------------------------------------

{
  const raw = JSON.stringify({
    topics: ['staging deployment', 'authentication'],
    facts: [
      {
        text: 'Uses Base Sepolia as staging chain',
        type: 'claim',
        source: 'user',
        scope: 'work',
        importance: 8,
        confidence: 0.9,
        action: 'ADD',
        entities: [{ name: 'Base Sepolia', type: 'tool' }],
      },
      {
        text: 'Prefers JWT for service auth',
        type: 'preference',
        source: 'user',
        scope: 'work',
        importance: 7,
        confidence: 0.85,
        action: 'ADD',
      },
    ],
  });
  const { topics, facts } = parseMergedResponseV1(raw);
  assertEq(topics.length, 2, 'parseMerged: 2 topics');
  assertEq(facts.length, 2, 'parseMerged: 2 facts parsed');
  assertEq(facts[0].type, 'claim', 'parseMerged: fact[0] type');
  assertEq(facts[0].source, 'user', 'parseMerged: fact[0] source');
  assertEq(facts[1].type, 'preference', 'parseMerged: fact[1] type');
}

// ---------------------------------------------------------------------------
// parseMergedResponseV1 — malformed input → empty
// ---------------------------------------------------------------------------

{
  const { topics, facts } = parseMergedResponseV1('not json at all');
  assertEq(topics.length, 0, 'parseMerged: malformed → empty topics');
  assertEq(facts.length, 0, 'parseMerged: malformed → empty facts');
}

{
  const { topics, facts } = parseMergedResponseV1(JSON.stringify({ topics: [], facts: [] }));
  assertEq(topics.length, 0, 'parseMerged: empty object → empty topics');
  assertEq(facts.length, 0, 'parseMerged: empty object → empty facts');
}

// ---------------------------------------------------------------------------
// parseMergedResponseV1 — strips <think> tags, handles code fences
// ---------------------------------------------------------------------------

{
  const raw = '<think>reasoning trace</think>\n```json\n' + JSON.stringify({
    topics: ['test'],
    facts: [{ text: 'A test fact for parsing', type: 'claim', source: 'user', importance: 7, action: 'ADD' }],
  }) + '\n```';
  const { facts } = parseMergedResponseV1(raw);
  assertEq(facts.length, 1, 'parseMerged: strips <think> + code fences');
}

// ---------------------------------------------------------------------------
// parseMergedResponseV1 — summary+user combo rejected
// ---------------------------------------------------------------------------

{
  const raw = JSON.stringify({
    topics: [],
    facts: [
      { text: 'A summary that should be dropped', type: 'summary', source: 'user', importance: 8, action: 'ADD' },
      { text: 'A valid summary', type: 'summary', source: 'derived', importance: 8, action: 'ADD' },
    ],
  });
  const { facts } = parseMergedResponseV1(raw);
  assertEq(facts.length, 1, 'parseMerged: summary+user rejected, summary+derived kept');
  assertEq(facts[0].source, 'derived', 'parseMerged: kept fact is derived-source summary');
}

// ---------------------------------------------------------------------------
// parseMergedResponseV1 — importance threshold < 6 dropped (unless DELETE)
// ---------------------------------------------------------------------------

{
  const raw = JSON.stringify({
    topics: [],
    facts: [
      { text: 'Below threshold', type: 'claim', source: 'user', importance: 4, action: 'ADD' },
      { text: 'Above threshold ok', type: 'claim', source: 'user', importance: 7, action: 'ADD' },
      { text: 'Delete action passes', type: 'claim', source: 'user', importance: 3, action: 'DELETE', existingFactId: 'abc' },
    ],
  });
  const { facts } = parseMergedResponseV1(raw);
  assertEq(facts.length, 2, 'parseMerged: imp<6 dropped, DELETE passes');
}

// ---------------------------------------------------------------------------
// applyProvenanceFilterLax — assistant-source capped at 7, not dropped
// ---------------------------------------------------------------------------

{
  const convText = '[user]: what is a good OLTP database?\n\n[assistant]: PostgreSQL is a solid choice for OLTP workloads.\n\n[user]: cool thanks.';
  const facts: ExtractedFact[] = [
    {
      text: 'PostgreSQL is a solid OLTP database choice',
      type: 'claim',
      source: 'assistant',
      importance: 9,
      action: 'ADD',
    },
    {
      text: 'User asked about OLTP database options',
      type: 'claim',
      source: 'user',
      importance: 6,
      action: 'ADD',
    },
  ];
  const filtered = applyProvenanceFilterLax(facts, convText);
  assertEq(filtered.length, 2, 'provenance: assistant-source kept, not dropped');
  const assistantFact = filtered.find((f) => f.source === 'assistant');
  assert(assistantFact !== undefined, 'provenance: assistant fact present');
  if (assistantFact) {
    assert(assistantFact.importance <= 7, 'provenance: assistant importance capped at 7 (was 9)');
  }
  const userFact = filtered.find((f) => f.source === 'user');
  if (userFact) {
    assertEq(userFact.importance, 6, 'provenance: user-source importance untouched');
  }
}

// ---------------------------------------------------------------------------
// applyProvenanceFilterLax — auto-downgrades when < 30% user-turn overlap
// ---------------------------------------------------------------------------

{
  const convText = '[user]: hi there\n\n[assistant]: Welcome. The system uses Kubernetes orchestration with 12-node clusters running on AWS EKS with HPA autoscaling enabled for all deployments.';
  const facts: ExtractedFact[] = [
    {
      text: 'System uses Kubernetes orchestration with HPA autoscaling on AWS EKS',
      type: 'claim',
      source: 'user-inferred',  // LLM claimed user-inferred, but content is from assistant
      importance: 9,
      action: 'ADD',
    },
  ];
  const filtered = applyProvenanceFilterLax(facts, convText);
  assertEq(filtered.length, 1, 'provenance: low-overlap fact retained (tag-don\'t-drop)');
  assertEq(filtered[0].source, 'assistant', 'provenance: low-overlap auto-tagged as assistant');
  assert(filtered[0].importance <= 7, 'provenance: auto-tagged assistant capped at 7');
}

// ---------------------------------------------------------------------------
// applyProvenanceFilterLax — drops below importance 5
// ---------------------------------------------------------------------------

{
  const convText = '[user]: some test conv';
  const facts: ExtractedFact[] = [
    { text: 'very low priority', type: 'claim', source: 'user', importance: 3, action: 'ADD' },
    { text: 'above minimum', type: 'claim', source: 'user', importance: 5, action: 'ADD' },
  ];
  const filtered = applyProvenanceFilterLax(facts, convText);
  assertEq(filtered.length, 1, 'provenance: imp<5 dropped (even for user source)');
  assertEq(filtered[0].text, 'above minimum', 'provenance: imp=5 kept');
}

// ---------------------------------------------------------------------------
// defaultVolatility — heuristic
// ---------------------------------------------------------------------------

assertEq(
  defaultVolatility({ text: 'x', type: 'commitment', importance: 7, action: 'ADD' }),
  'updatable',
  'volatility: commitment → updatable',
);
assertEq(
  defaultVolatility({ text: 'x', type: 'episode', importance: 7, action: 'ADD' }),
  'stable',
  'volatility: episode → stable',
);
assertEq(
  defaultVolatility({ text: 'x', type: 'directive', importance: 7, action: 'ADD' }),
  'stable',
  'volatility: directive → stable',
);
assertEq(
  defaultVolatility({ text: 'x', type: 'claim', scope: 'health', importance: 7, action: 'ADD' }),
  'stable',
  'volatility: health scope → stable',
);
assertEq(
  defaultVolatility({ text: 'x', type: 'claim', importance: 7, action: 'ADD' }),
  'updatable',
  'volatility: default → updatable',
);

// ---------------------------------------------------------------------------
// getSourceWeight — Retrieval v2 Tier 1 table
// ---------------------------------------------------------------------------

// v2-lenient (core 2.4.0+) — per docs/specs/totalreclaw/retrieval-v2.md §Tier 1.
assertEq(getSourceWeight('user'), 1.0, 'sourceWeight: user = 1.0');
assertEq(getSourceWeight('user-inferred'), 0.95, 'sourceWeight: user-inferred = 0.95');
assertEq(getSourceWeight('derived'), 0.85, 'sourceWeight: derived = 0.85');
assertEq(getSourceWeight('external'), 0.85, 'sourceWeight: external = 0.85');
assertEq(getSourceWeight('assistant'), 0.85, 'sourceWeight: assistant = 0.85');
assertEq(getSourceWeight(undefined), 0.85, 'sourceWeight: missing = 0.85 (legacy fallback)');
assertEq(getSourceWeight('unknown'), 0.95, 'sourceWeight: unknown = 0.95 (core falls back to user-inferred via from_str_lossy)');

// ---------------------------------------------------------------------------
// rerank with applySourceWeights=true: user > assistant on tied content
// ---------------------------------------------------------------------------

{
  // Two candidates with identical text content (tied BM25 + cosine) but
  // different sources. With apply_source_weights=true, the user-sourced one
  // should rank first.
  const embedding = new Array(8).fill(0).map((_, i) => (i % 3) * 0.1);
  const candidates: RerankerCandidate[] = [
    {
      id: 'assistant-1',
      text: 'prefers PostgreSQL for analytics',
      embedding,
      importance: 0.7,
      createdAt: Date.now() / 1000 - 3600,
      source: 'assistant',
    },
    {
      id: 'user-1',
      text: 'prefers PostgreSQL for analytics',
      embedding,
      importance: 0.7,
      createdAt: Date.now() / 1000 - 3600,
      source: 'user',
    },
  ];

  const withWeights = rerank('PostgreSQL analytics', embedding, candidates, 2, undefined, true);
  assert(withWeights.length === 2, 'rerank: returns both candidates');
  assertEq(withWeights[0].id, 'user-1', 'rerank w/ source weights: user > assistant on tied content');
  assert(withWeights[0].sourceWeight === 1.0, 'rerank w/ source weights: user_weight = 1.0');
  assert(withWeights[1].sourceWeight === 0.85, 'rerank w/ source weights: assistant_weight = 0.85 (v2-lenient)');

  // Control: without source weights, order should be stable (no preference).
  const withoutWeights = rerank('PostgreSQL analytics', embedding, candidates, 2, undefined, false);
  // Without weighting, the RRF scores are tied; ordering is not deterministic
  // by source. Just assert the field is unset so callers don't get a stale
  // value from a previous run.
  assert(
    withoutWeights.every((r) => r.sourceWeight === undefined),
    'rerank w/o source weights: sourceWeight unset',
  );
}

// ---------------------------------------------------------------------------
// rerank: legacy candidates (no source field) get the fallback weight (0.85),
// lower than user (1.0) so user-authored facts rank first when content ties.
// ---------------------------------------------------------------------------

{
  const embedding = new Array(8).fill(0).map((_, i) => (i % 3) * 0.1);
  const candidates: RerankerCandidate[] = [
    {
      id: 'legacy-1',
      text: 'prefers PostgreSQL for analytics',
      embedding,
      importance: 0.7,
      createdAt: Date.now() / 1000 - 3600,
      // no source field — legacy v0 candidate
    },
    {
      id: 'user-1',
      text: 'prefers PostgreSQL for analytics',
      embedding,
      importance: 0.7,
      createdAt: Date.now() / 1000 - 3600,
      source: 'user',
    },
  ];

  const reranked = rerank('PostgreSQL', embedding, candidates, 2, undefined, true);
  assertEq(reranked[0].id, 'user-1', 'rerank: user (1.0) beats legacy (0.85) on tied content');
  assertEq(reranked[0].sourceWeight, 1.0, 'rerank: user weight = 1.0');
  assertEq(reranked[1].sourceWeight, 0.85, 'rerank: legacy fallback weight = 0.85');
}

// ---------------------------------------------------------------------------
// Plugin v3.0.0: default extraction path emits v1 (no env-var gate)
// ---------------------------------------------------------------------------

{
  // MemoryType is v1
  assert(isValidMemoryTypeV1('claim'), 'default: v1 "claim" is valid');
  assert(isValidMemoryTypeV1('preference'), 'default: v1 "preference" is valid');
  assert(isValidMemoryTypeV1('directive'), 'default: v1 "directive" is valid');
  assert(isValidMemoryTypeV1('commitment'), 'default: v1 "commitment" is valid');
  assert(isValidMemoryTypeV1('episode'), 'default: v1 "episode" is valid');
  assert(isValidMemoryTypeV1('summary'), 'default: v1 "summary" is valid');

  // Legacy v0 tokens are NOT valid v1 tokens
  assert(!isValidMemoryTypeV1('fact'), 'default: v0 "fact" not in v1 enum');
  assert(!isValidMemoryTypeV1('decision'), 'default: v0 "decision" not in v1 enum');
  assert(!isValidMemoryTypeV1('rule'), 'default: v0 "rule" not in v1 enum');

  // normalizeToV1Type coerces v0 tokens
  assertEq(normalizeToV1Type('fact'), 'claim', 'coerce: v0 fact → v1 claim');
  assertEq(normalizeToV1Type('decision'), 'claim', 'coerce: v0 decision → v1 claim');
  assertEq(normalizeToV1Type('episodic'), 'episode', 'coerce: v0 episodic → v1 episode');
  assertEq(normalizeToV1Type('goal'), 'commitment', 'coerce: v0 goal → v1 commitment');
  assertEq(normalizeToV1Type('context'), 'claim', 'coerce: v0 context → v1 claim');
  assertEq(normalizeToV1Type('rule'), 'directive', 'coerce: v0 rule → v1 directive');
  assertEq(normalizeToV1Type('summary'), 'summary', 'coerce: v0 summary → v1 summary');
  assertEq(normalizeToV1Type('preference'), 'preference', 'coerce: v0 preference → v1 preference');

  // V0_TO_V1_TYPE map is complete
  const v0Tokens = ['fact', 'preference', 'decision', 'episodic', 'goal', 'context', 'summary', 'rule'];
  for (const v0 of v0Tokens) {
    assert(
      typeof V0_TO_V1_TYPE[v0 as keyof typeof V0_TO_V1_TYPE] === 'string',
      `V0_TO_V1_TYPE: ${v0} mapped`,
    );
  }
}

// ---------------------------------------------------------------------------
// Default build path is v1 (no env-var gate)
// ---------------------------------------------------------------------------

{
  const originalEnv = {
    taxonomy: process.env.TOTALRECLAW_TAXONOMY_VERSION,
    claim: process.env.TOTALRECLAW_CLAIM_FORMAT,
  };
  try {
    // Explicitly wipe any env vars a previous test / process set.
    delete process.env.TOTALRECLAW_TAXONOMY_VERSION;
    delete process.env.TOTALRECLAW_CLAIM_FORMAT;

    const fact: ExtractedFact = {
      text: 'Default-path v1 emission.',
      type: 'claim',
      source: 'user',
      scope: 'work',
      importance: 8,
      action: 'ADD',
    };

    // buildCanonicalClaimV1 always emits v1 (obvious, but sanity check).
    const v1Direct = buildCanonicalClaimV1({
      fact,
      importance: 8,
    });
    const parsedDirect = JSON.parse(v1Direct);
    assertEq(parsedDirect.schema_version, '1.0', 'default: direct v1 builder emits v1');

    // The env toggle has NO effect — all four env-var states produce v1.
    process.env.TOTALRECLAW_TAXONOMY_VERSION = 'v0';
    const withV0Gate = JSON.parse(buildCanonicalClaimV1({ fact, importance: 8 }));
    assertEq(withV0Gate.schema_version, '1.0', 'default: TAXONOMY=v0 still emits v1');

    process.env.TOTALRECLAW_TAXONOMY_VERSION = 'v1';
    const withV1Gate = JSON.parse(buildCanonicalClaimV1({ fact, importance: 8 }));
    assertEq(withV1Gate.schema_version, '1.0', 'default: TAXONOMY=v1 emits v1');
  } finally {
    if (originalEnv.taxonomy === undefined) delete process.env.TOTALRECLAW_TAXONOMY_VERSION;
    else process.env.TOTALRECLAW_TAXONOMY_VERSION = originalEnv.taxonomy;
    if (originalEnv.claim === undefined) delete process.env.TOTALRECLAW_CLAIM_FORMAT;
    else process.env.TOTALRECLAW_CLAIM_FORMAT = originalEnv.claim;
  }
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

console.log(`\n# tests: ${passed + failed}`);
console.log(`# pass:  ${passed}`);
console.log(`# fail:  ${failed}`);

if (failed === 0) {
  console.log('\nALL TESTS PASSED');
  process.exit(0);
} else {
  console.log('\nSOME TESTS FAILED');
  process.exit(1);
}
