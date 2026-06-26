/**
 * Unit tests for memory consolidation & near-duplicate detection.
 *
 * Run with: npx tsx consolidation.test.ts
 *
 * Uses TAP-style output (no test framework dependency).
 */

import {
  findNearDuplicate,
  shouldSupersede,
  clusterFacts,
  getStoreDedupThreshold,
  getConsolidationThreshold,
  STORE_DEDUP_MAX_CANDIDATES,
} from './consolidation.js';
import type { DecryptedCandidate } from './consolidation.js';

let passed = 0;
let failed = 0;
let testNum = 0;

function assert(condition: boolean, message: string): void {
  testNum++;
  if (condition) {
    passed++;
    console.log(`ok ${testNum} - ${message}`);
  } else {
    failed++;
    console.log(`not ok ${testNum} - ${message}`);
  }
}

function assertClose(actual: number, expected: number, epsilon: number, message: string): void {
  const diff = Math.abs(actual - expected);
  assert(diff < epsilon, `${message} (expected ~${expected}, got ${actual}, diff=${diff})`);
}

// Helper: create a DecryptedCandidate
function makeCandidate(
  overrides: Partial<DecryptedCandidate> & { id: string },
): DecryptedCandidate {
  return {
    text: `fact ${overrides.id}`,
    embedding: null,
    importance: 5,
    decayScore: 1.0,
    createdAt: 1000,
    version: 1,
    ...overrides,
  };
}

// ---------------------------------------------------------------------------
// getStoreDedupThreshold tests
// ---------------------------------------------------------------------------

console.log('# getStoreDedupThreshold');

{
  // Default threshold should be 0.85 (no env var set)
  const orig = process.env.TOTALRECLAW_STORE_DEDUP_THRESHOLD;
  delete process.env.TOTALRECLAW_STORE_DEDUP_THRESHOLD;
  assertClose(getStoreDedupThreshold(), 0.85, 1e-10, 'default threshold is 0.85');
  if (orig !== undefined) process.env.TOTALRECLAW_STORE_DEDUP_THRESHOLD = orig;
}

{
  // Custom threshold via env var
  const orig = process.env.TOTALRECLAW_STORE_DEDUP_THRESHOLD;
  process.env.TOTALRECLAW_STORE_DEDUP_THRESHOLD = '0.75';
  assertClose(getStoreDedupThreshold(), 0.75, 1e-10, 'custom threshold 0.75 from env');
  if (orig !== undefined) {
    process.env.TOTALRECLAW_STORE_DEDUP_THRESHOLD = orig;
  } else {
    delete process.env.TOTALRECLAW_STORE_DEDUP_THRESHOLD;
  }
}

{
  // Invalid env var falls back to default
  const orig = process.env.TOTALRECLAW_STORE_DEDUP_THRESHOLD;
  process.env.TOTALRECLAW_STORE_DEDUP_THRESHOLD = 'not-a-number';
  assertClose(getStoreDedupThreshold(), 0.85, 1e-10, 'invalid env var falls back to 0.85');
  if (orig !== undefined) {
    process.env.TOTALRECLAW_STORE_DEDUP_THRESHOLD = orig;
  } else {
    delete process.env.TOTALRECLAW_STORE_DEDUP_THRESHOLD;
  }
}

// ---------------------------------------------------------------------------
// getConsolidationThreshold tests
// ---------------------------------------------------------------------------

console.log('# getConsolidationThreshold');

{
  // Default threshold should be 0.88 (no env var set)
  const orig = process.env.TOTALRECLAW_CONSOLIDATION_THRESHOLD;
  delete process.env.TOTALRECLAW_CONSOLIDATION_THRESHOLD;
  assertClose(getConsolidationThreshold(), 0.88, 1e-10, 'default threshold is 0.88');
  if (orig !== undefined) process.env.TOTALRECLAW_CONSOLIDATION_THRESHOLD = orig;
}

{
  // Custom threshold via env var
  const orig = process.env.TOTALRECLAW_CONSOLIDATION_THRESHOLD;
  process.env.TOTALRECLAW_CONSOLIDATION_THRESHOLD = '0.95';
  assertClose(getConsolidationThreshold(), 0.95, 1e-10, 'custom threshold 0.95 from env');
  if (orig !== undefined) {
    process.env.TOTALRECLAW_CONSOLIDATION_THRESHOLD = orig;
  } else {
    delete process.env.TOTALRECLAW_CONSOLIDATION_THRESHOLD;
  }
}

{
  // Invalid env var falls back to default
  const orig = process.env.TOTALRECLAW_CONSOLIDATION_THRESHOLD;
  process.env.TOTALRECLAW_CONSOLIDATION_THRESHOLD = 'garbage';
  assertClose(getConsolidationThreshold(), 0.88, 1e-10, 'invalid env var falls back to 0.88');
  if (orig !== undefined) {
    process.env.TOTALRECLAW_CONSOLIDATION_THRESHOLD = orig;
  } else {
    delete process.env.TOTALRECLAW_CONSOLIDATION_THRESHOLD;
  }
}

// ---------------------------------------------------------------------------
// STORE_DEDUP_MAX_CANDIDATES constant
// ---------------------------------------------------------------------------

console.log('# STORE_DEDUP_MAX_CANDIDATES');

assert(STORE_DEDUP_MAX_CANDIDATES === 200, 'STORE_DEDUP_MAX_CANDIDATES is 200');

// ---------------------------------------------------------------------------
// findNearDuplicate tests
// ---------------------------------------------------------------------------

console.log('# findNearDuplicate');

{
  // Empty candidates -> null
  const result = findNearDuplicate([1, 0, 0], [], 0.85);
  assert(result === null, 'empty candidates returns null');
}

{
  // No embeddings on candidates -> null
  const candidates = [
    makeCandidate({ id: 'a', embedding: null }),
    makeCandidate({ id: 'b', embedding: null }),
  ];
  const result = findNearDuplicate([1, 0, 0], candidates, 0.85);
  assert(result === null, 'candidates without embeddings returns null');
}

{
  // Below threshold -> null
  const candidates = [
    makeCandidate({ id: 'a', embedding: [0, 1, 0] }), // orthogonal, cosine = 0
  ];
  const result = findNearDuplicate([1, 0, 0], candidates, 0.85);
  assert(result === null, 'below threshold returns null');
}

{
  // Above threshold -> returns match
  const candidates = [
    makeCandidate({ id: 'a', embedding: [1, 0, 0] }), // cosine = 1.0
  ];
  const result = findNearDuplicate([1, 0, 0], candidates, 0.85);
  assert(result !== null, 'above threshold returns match');
  assert(result!.existingFact.id === 'a', 'match is the correct candidate');
  assertClose(result!.similarity, 1.0, 1e-6, 'similarity is ~1.0');
}

{
  // Multiple matches -> returns highest similarity
  const candidates = [
    makeCandidate({ id: 'low', embedding: [0.86, Math.sqrt(1 - 0.86 * 0.86), 0] }), // cosine ~ 0.86
    makeCandidate({ id: 'high', embedding: [0.99, Math.sqrt(1 - 0.99 * 0.99), 0] }), // cosine ~ 0.99
    makeCandidate({ id: 'mid', embedding: [0.90, Math.sqrt(1 - 0.90 * 0.90), 0] }),  // cosine ~ 0.90
  ];
  const result = findNearDuplicate([1, 0, 0], candidates, 0.85);
  assert(result !== null, 'multiple matches: returns a match');
  assert(result!.existingFact.id === 'high', 'multiple matches: returns highest similarity');
}

{
  // Parallel vectors (cosine = 1.0) -> match
  const candidates = [
    makeCandidate({ id: 'parallel', embedding: [3, 6, 9] }), // parallel to [1, 2, 3]
  ];
  const result = findNearDuplicate([1, 2, 3], candidates, 0.85);
  assert(result !== null, 'parallel vectors: returns match');
  assertClose(result!.similarity, 1.0, 1e-6, 'parallel vectors: cosine is ~1.0');
}

{
  // Orthogonal vectors (cosine = 0) -> null
  const candidates = [
    makeCandidate({ id: 'ortho', embedding: [0, 1, 0] }),
  ];
  const result = findNearDuplicate([1, 0, 0], candidates, 0.85);
  assert(result === null, 'orthogonal vectors: returns null');
}

// ---------------------------------------------------------------------------
// shouldSupersede tests
// ---------------------------------------------------------------------------

console.log('# shouldSupersede');

{
  // Higher new importance -> supersede
  const existing = makeCandidate({ id: 'old', importance: 5 });
  const result = shouldSupersede(8, existing);
  assert(result === 'supersede', 'higher new importance -> supersede');
}

{
  // Lower new importance -> skip
  const existing = makeCandidate({ id: 'old', importance: 8 });
  const result = shouldSupersede(3, existing);
  assert(result === 'skip', 'lower new importance -> skip');
}

{
  // Equal importance -> supersede (newer wins)
  const existing = makeCandidate({ id: 'old', importance: 5 });
  const result = shouldSupersede(5, existing);
  assert(result === 'supersede', 'equal importance -> supersede (newer wins)');
}

// ---------------------------------------------------------------------------
// clusterFacts tests
// ---------------------------------------------------------------------------

console.log('# clusterFacts');

{
  // Empty facts -> empty clusters
  const clusters = clusterFacts([], 0.88);
  assert(clusters.length === 0, 'empty facts -> no clusters');
}

{
  // Single fact -> no clusters (needs at least 2 to form a cluster)
  const facts = [
    makeCandidate({ id: 'a', embedding: [1, 0, 0] }),
  ];
  const clusters = clusterFacts(facts, 0.88);
  assert(clusters.length === 0, 'single fact -> no clusters');
}

{
  // Two identical embeddings -> one cluster
  const facts = [
    makeCandidate({ id: 'a', embedding: [1, 0, 0] }),
    makeCandidate({ id: 'b', embedding: [1, 0, 0] }),
  ];
  const clusters = clusterFacts(facts, 0.88);
  assert(clusters.length === 1, 'two identical -> one cluster');
  assert(clusters[0].duplicates.length === 1, 'two identical -> one duplicate');
}

{
  // Two dissimilar embeddings -> no clusters
  const facts = [
    makeCandidate({ id: 'a', embedding: [1, 0, 0] }),
    makeCandidate({ id: 'b', embedding: [0, 1, 0] }), // orthogonal
  ];
  const clusters = clusterFacts(facts, 0.88);
  assert(clusters.length === 0, 'two dissimilar -> no clusters');
}

{
  // Multiple clusters: two groups of duplicates + one unique
  const facts = [
    makeCandidate({ id: 'a1', embedding: [1, 0, 0] }),
    makeCandidate({ id: 'a2', embedding: [1, 0, 0] }),    // dup of a1
    makeCandidate({ id: 'b1', embedding: [0, 1, 0] }),
    makeCandidate({ id: 'b2', embedding: [0, 1, 0] }),    // dup of b1
    makeCandidate({ id: 'c1', embedding: [0, 0, 1] }),    // unique
  ];
  const clusters = clusterFacts(facts, 0.88);
  assert(clusters.length === 2, 'multiple clusters: two groups found');
}

{
  // Facts without embeddings are not clustered
  const facts = [
    makeCandidate({ id: 'a', embedding: [1, 0, 0] }),
    makeCandidate({ id: 'b', embedding: null }),           // no embedding
    makeCandidate({ id: 'c', embedding: [1, 0, 0] }),     // dup of a
  ];
  const clusters = clusterFacts(facts, 0.88);
  assert(clusters.length === 1, 'no-embedding facts skipped, one cluster of a+c');
  // b should not appear in any cluster
  const allIds = clusters.flatMap(c => [c.representative.id, ...c.duplicates.map(d => d.id)]);
  assert(!allIds.includes('b'), 'no-embedding fact not in any cluster');
}

{
  // Representative = highest importance (via decayScore tiebreak)
  const facts = [
    makeCandidate({ id: 'low', embedding: [1, 0, 0], decayScore: 0.5, importance: 3 }),
    makeCandidate({ id: 'high', embedding: [1, 0, 0], decayScore: 0.9, importance: 8 }),
    makeCandidate({ id: 'mid', embedding: [1, 0, 0], decayScore: 0.7, importance: 5 }),
  ];
  const clusters = clusterFacts(facts, 0.88);
  assert(clusters.length === 1, 'representative test: one cluster');
  assert(clusters[0].representative.id === 'high', 'representative = highest decayScore');
  assert(clusters[0].duplicates.length === 2, 'two duplicates');
}

{
  // Tiebreak: same decayScore -> most recent (highest createdAt)
  const facts = [
    makeCandidate({ id: 'old', embedding: [1, 0, 0], decayScore: 1.0, createdAt: 1000 }),
    makeCandidate({ id: 'new', embedding: [1, 0, 0], decayScore: 1.0, createdAt: 2000 }),
  ];
  const clusters = clusterFacts(facts, 0.88);
  assert(clusters.length === 1, 'tiebreak test: one cluster');
  assert(clusters[0].representative.id === 'new', 'tiebreak: most recent is representative');
}

{
  // Tiebreak: same decayScore + createdAt -> longest text
  const facts = [
    makeCandidate({ id: 'short', text: 'abc', embedding: [1, 0, 0], decayScore: 1.0, createdAt: 1000 }),
    makeCandidate({ id: 'long', text: 'abcdefghij', embedding: [1, 0, 0], decayScore: 1.0, createdAt: 1000 }),
  ];
  const clusters = clusterFacts(facts, 0.88);
  assert(clusters.length === 1, 'tiebreak longest text: one cluster');
  assert(clusters[0].representative.id === 'long', 'tiebreak: longest text is representative');
}

// ---------------------------------------------------------------------------
// Cross-impl parity: plugin wrappers delegate to the exact same WASM functions
// that MCP (`mcp/src/consolidation.ts`) delegates to. This block re-executes
// the same inputs against the raw WASM API and asserts the plugin wrapper
// returns the same result, so any future drift between plugin and core is
// caught at test time.
// ---------------------------------------------------------------------------

console.log('# cross-impl parity (raw WASM vs plugin wrapper)');

{
  // Use createRequire from node:module so this works under ESM (plugin's
  // runtime mode). Mirrors the pattern the module under test uses.
  const { createRequire } = await import('node:module');
  const requireWasm = createRequire(import.meta.url);
  const wasm = requireWasm('@totalreclaw/core') as typeof import('@totalreclaw/core');

  // findNearDuplicate parity
  const newEmb = [1, 0, 0, 0];
  const candidates = [
    makeCandidate({ id: 'low', embedding: [0.86, Math.sqrt(1 - 0.86 * 0.86), 0, 0] }),
    makeCandidate({ id: 'high', embedding: [0.99, Math.sqrt(1 - 0.99 * 0.99), 0, 0] }),
    makeCandidate({ id: 'mid', embedding: [0.90, Math.sqrt(1 - 0.90 * 0.90), 0, 0] }),
  ];

  const pluginMatch = findNearDuplicate(newEmb, candidates, 0.85);
  const rawExisting = candidates
    .filter((c) => c.embedding && c.embedding.length > 0)
    .map((c) => ({ id: c.id, embedding: c.embedding! }));
  const rawResultJs = (wasm as any).findBestNearDuplicate(
    JSON.stringify(newEmb),
    JSON.stringify(rawExisting),
    0.85,
  );
  const rawMatch: { fact_id: string; similarity: number } | null =
    rawResultJs == null
      ? null
      : typeof rawResultJs === 'string'
      ? JSON.parse(rawResultJs)
      : rawResultJs;

  assert(
    pluginMatch !== null && rawMatch !== null && pluginMatch.existingFact.id === rawMatch.fact_id,
    'parity: findNearDuplicate picks same fact_id as raw WASM findBestNearDuplicate',
  );
  assert(
    pluginMatch !== null && rawMatch !== null &&
      Math.abs(pluginMatch.similarity - rawMatch.similarity) < 1e-9,
    'parity: findNearDuplicate similarity equals raw WASM similarity',
  );
}

{
  // shouldSupersede parity — plugin wrapper is a thin pass-through. Test
  // that equal importance returns 'supersede' from BOTH plugin and raw WASM.
  const { createRequire } = await import('node:module');
  const requireWasm = createRequire(import.meta.url);
  const wasm = requireWasm('@totalreclaw/core') as typeof import('@totalreclaw/core');

  const existing = makeCandidate({ id: 'e', importance: 5 });
  for (const [newImp, label] of [[8, 'higher'], [3, 'lower'], [5, 'equal']] as const) {
    const pluginAns = shouldSupersede(newImp, existing);
    const rawAns = wasm.shouldSupersede(newImp, existing.importance) ? 'supersede' : 'skip';
    assert(pluginAns === rawAns, `parity: shouldSupersede agrees with raw WASM (${label} importance)`);
  }
}

{
  // clusterFacts parity — compare plugin-wrapper output (IDs only) against a
  // raw WASM call with the same JSON payload. The plugin filters singleton
  // clusters; apply the same filter to the raw output before comparing.
  const { createRequire } = await import('node:module');
  const requireWasm = createRequire(import.meta.url);
  const wasm = requireWasm('@totalreclaw/core') as typeof import('@totalreclaw/core');

  const facts = [
    makeCandidate({ id: 'a1', embedding: [1, 0, 0] }),
    makeCandidate({ id: 'a2', embedding: [1, 0, 0] }),
    makeCandidate({ id: 'b1', embedding: [0, 1, 0] }),
    makeCandidate({ id: 'b2', embedding: [0, 1, 0] }),
    makeCandidate({ id: 'c1', embedding: [0, 0, 1] }), // singleton
  ];

  const pluginClusters = clusterFacts(facts, 0.88).map((c) => ({
    representative: c.representative.id,
    duplicates: [...c.duplicates.map((d) => d.id)].sort(),
  }));

  const wasmCandidates = facts.map((f) => ({
    id: f.id,
    text: f.text,
    embedding: f.embedding!,
    importance: f.importance,
    decay_score: f.decayScore,
    created_at: f.createdAt,
    version: f.version,
  }));
  const rawJs = (wasm as any).clusterFacts(JSON.stringify(wasmCandidates), 0.88);
  const rawClusters: { representative: string; duplicates: string[] }[] =
    typeof rawJs === 'string' ? JSON.parse(rawJs) : rawJs;
  const rawFiltered = rawClusters
    .filter((c) => c.duplicates.length > 0)
    .map((c) => ({ representative: c.representative, duplicates: [...c.duplicates].sort() }));

  // Sort both by representative for stable comparison.
  const norm = (arr: { representative: string; duplicates: string[] }[]) =>
    [...arr].sort((x, y) => x.representative.localeCompare(y.representative));

  assert(
    JSON.stringify(norm(pluginClusters)) === JSON.stringify(norm(rawFiltered)),
    'parity: clusterFacts output (sans singletons) equals raw WASM clusterFacts output',
  );
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

console.log(`\n1..${testNum}`);
console.log(`# pass: ${passed}`);
console.log(`# fail: ${failed}`);

if (failed > 0) {
  console.log('\nFAILED');
  process.exit(1);
} else {
  console.log('\nALL TESTS PASSED');
  process.exit(0);
}
