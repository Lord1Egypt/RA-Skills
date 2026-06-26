/**
 * Plugin reranker public-API tests.
 *
 * As of rc.22 the plugin reranker is a thin wrapper around `@totalreclaw/core`.
 * Internal helpers (BM25, RRF, MMR, recency, importance) are no longer in the
 * client and are tested at the core level (`rust/totalreclaw-core/src/reranker.rs`
 * tests + benches). This file covers the wrapper's public surface only:
 *   - `cosineSimilarity` — delegates to core WASM
 *   - `getSourceWeight` — delegates to core's source-weight table
 *   - `detectQueryIntent` — kept as TS heuristic (callers pass the result
 *     into rerank purely for backwards compat)
 *   - `rerank` — routes candidates through core::rerank_with_config
 *
 * Run with: npx tsx reranker.test.ts
 */

import {
  cosineSimilarity,
  detectQueryIntent,
  getSourceWeight,
  rerank,
  type RerankerCandidate,
} from './reranker.js';

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

function assertClose(actual: number, expected: number, eps: number, message: string): void {
  assert(Math.abs(actual - expected) < eps, `${message} (expected ~${expected}, got ${actual})`);
}

// ---------------------------------------------------------------------------
// cosineSimilarity (WASM-backed)
// ---------------------------------------------------------------------------

console.log('# cosineSimilarity');

{
  // Identical vectors -> 1.0
  assertClose(cosineSimilarity([1, 0, 0], [1, 0, 0]), 1.0, 1e-6, 'cosine: identical = 1.0');
  // Orthogonal vectors -> 0
  assertClose(cosineSimilarity([1, 0, 0], [0, 1, 0]), 0.0, 1e-6, 'cosine: orthogonal = 0');
  // Opposite vectors -> -1.0
  assertClose(cosineSimilarity([1, 0, 0], [-1, 0, 0]), -1.0, 1e-6, 'cosine: opposite = -1.0');
  // Empty inputs -> 0 (TS guard, no WASM call)
  assert(cosineSimilarity([], [1, 0]) === 0, 'cosine: empty a -> 0');
  assert(cosineSimilarity([1, 0], []) === 0, 'cosine: empty b -> 0');
  // Mismatched lengths -> 0 (TS guard)
  assert(cosineSimilarity([1, 0], [1, 0, 0]) === 0, 'cosine: mismatched length -> 0');
}

// ---------------------------------------------------------------------------
// getSourceWeight (delegated to core)
// ---------------------------------------------------------------------------

console.log('# getSourceWeight');

{
  // v2-lenient (core 2.4.0+) — per docs/specs/totalreclaw/retrieval-v2.md §Tier 1.
  assert(getSourceWeight('user') === 1.0, 'sourceWeight: user = 1.0');
  assert(getSourceWeight('user-inferred') === 0.95, 'sourceWeight: user-inferred = 0.95');
  assert(getSourceWeight('derived') === 0.85, 'sourceWeight: derived = 0.85');
  assert(getSourceWeight('external') === 0.85, 'sourceWeight: external = 0.85');
  assert(getSourceWeight('assistant') === 0.85, 'sourceWeight: assistant = 0.85');
  assert(getSourceWeight(undefined) === 0.85, 'sourceWeight: undefined -> 0.85 (legacy fallback)');
}

// ---------------------------------------------------------------------------
// detectQueryIntent (TS heuristic)
// ---------------------------------------------------------------------------

console.log('# detectQueryIntent');

{
  assert(detectQueryIntent("What did we discuss yesterday?") === 'temporal', 'temporal: yesterday');
  assert(detectQueryIntent("What's Alex's email?") === 'factual', 'factual: short what-question');
  assert(detectQueryIntent("Tell me about the project architecture and design") === 'semantic', 'semantic: open-ended');
  // Long factual-pattern query falls through to semantic (>80 chars)
  const longQuery = "What are all the different design patterns and architectural decisions that were discussed in the project?";
  assert(detectQueryIntent(longQuery) === 'semantic', 'semantic: long factual-pattern -> semantic');
  // Temporal beats factual when both keywords present
  assert(detectQueryIntent("What happened last week?") === 'temporal', 'temporal: beats factual');
}

// ---------------------------------------------------------------------------
// rerank (routes through core)
// ---------------------------------------------------------------------------

console.log('# rerank (core delegation)');

{
  // BM25-only path (no embeddings) — exact-match doc ranks first.
  const candidates: RerankerCandidate[] = [
    { id: '1', text: 'Alex works at Nexus Labs as a senior engineer' },
    { id: '2', text: 'The weather today is sunny and warm' },
    { id: '3', text: 'Bob enjoys hiking in the mountains on weekends' },
  ];
  const results = rerank('Alex Nexus Labs', [], candidates, 2);
  assert(results.length === 2, 'rerank: returns topK=2');
  assert(results[0].id === '1', 'rerank: BM25-only ranks matching doc first');
}

{
  // Cosine-strong + BM25-strong candidates beat irrelevant ones.
  const queryEmb = [1, 0, 0, 0];
  const candidates: RerankerCandidate[] = [
    { id: '1', text: 'Alex works at Nexus Labs', embedding: [0, 1, 0, 0] },
    { id: '2', text: 'career position company staff', embedding: [0.99, 0.1, 0, 0] },
    { id: '3', text: 'sunny weather forecast today', embedding: [0, 0, 0, 1] },
  ];
  const results = rerank('Alex Nexus Labs', queryEmb, candidates, 3);
  assert(results.length === 3, 'rerank: returns all 3');
  assert(results[2].id === '3', 'rerank: irrelevant doc last');
}

{
  // Empty candidates -> empty result
  const results = rerank('test', [1, 0, 0], [], 5);
  assert(results.length === 0, 'rerank: empty candidates -> empty');
}

{
  // topK > candidate count
  const candidates: RerankerCandidate[] = [{ id: '1', text: 'only candidate' }];
  const results = rerank('only', [], candidates, 10);
  assert(results.length === 1, 'rerank: topK > count returns all');
}

{
  // applySourceWeights=true: user (1.0) beats assistant (0.85, v2-lenient) on tied content
  const embedding = new Array(8).fill(0).map((_, i) => (i % 3) * 0.1);
  const candidates: RerankerCandidate[] = [
    { id: 'asst', text: 'prefers PostgreSQL for analytics', embedding, source: 'assistant' },
    { id: 'user', text: 'prefers PostgreSQL for analytics', embedding, source: 'user' },
  ];
  const ranked = rerank('PostgreSQL analytics', embedding, candidates, 2, undefined, true);
  assert(ranked[0].id === 'user', 'rerank: user > assistant w/ source weights');
  assertClose(ranked[0].sourceWeight ?? 0, 1.0, 1e-6, 'rerank: user weight = 1.0');
  assertClose(ranked[1].sourceWeight ?? 0, 0.85, 1e-6, 'rerank: assistant weight = 0.85 (v2-lenient)');
}

{
  // applySourceWeights=false: sourceWeight is undefined (no weighting applied)
  const embedding = [0.1, 0.2, 0.3];
  const candidates: RerankerCandidate[] = [
    { id: 'a', text: 'fact one', embedding, source: 'user' },
    { id: 'b', text: 'fact two', embedding, source: 'assistant' },
  ];
  const ranked = rerank('fact', embedding, candidates, 2, undefined, false);
  assert(
    ranked.every((r) => r.sourceWeight === undefined),
    'rerank: applySourceWeights=false leaves sourceWeight undefined',
  );
}

{
  // Legacy candidates (no source) get 0.85 fallback
  const embedding = new Array(8).fill(0).map((_, i) => (i % 3) * 0.1);
  const candidates: RerankerCandidate[] = [
    { id: 'legacy', text: 'prefers PostgreSQL for analytics', embedding /* no source */ },
    { id: 'user', text: 'prefers PostgreSQL for analytics', embedding, source: 'user' },
  ];
  const ranked = rerank('PostgreSQL', embedding, candidates, 2, undefined, true);
  assert(ranked[0].id === 'user', 'rerank: user (1.0) beats legacy (0.85) on tied content');
  assertClose(ranked[1].sourceWeight ?? 0, 0.85, 1e-6, 'rerank: legacy fallback = 0.85');
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
