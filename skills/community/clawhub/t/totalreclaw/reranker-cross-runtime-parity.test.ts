/**
 * Cross-runtime reranker parity check.
 *
 * Locks in the rc.22 hoist: plugin / Hermes / MCP all delegate ranking to
 * core::reranker, so the same fixture MUST produce identical top-K
 * orderings across runtimes (within floating-point tolerance).
 *
 * This file lives in the plugin tree (the runtime that historically drifted
 * most -- rc.18 cosine gate divergence). The Python side has a parity
 * companion at `python/tests/test_reranker_cross_runtime_parity.py` that
 * runs the SAME fixture against `totalreclaw_core.rerank_with_config` and
 * asserts identical ordering.
 *
 * Run with: npx tsx reranker-cross-runtime-parity.test.ts
 */

import { rerank, type RerankerCandidate } from './reranker.js';

let passed = 0;
let failed = 0;
let n = 0;

function ok(cond: boolean, msg: string): void {
  n++;
  if (cond) {
    passed++;
    console.log(`ok ${n} - ${msg}`);
  } else {
    failed++;
    console.log(`not ok ${n} - ${msg}`);
  }
}

// 30-candidate G-pipeline-shaped fixture (mixed sources, BM25-strong + cosine
// distractors). The numbers don't have to match a real corpus -- they just
// need to be deterministic so the test is reproducible across runtimes.
const FIXTURE: RerankerCandidate[] = [
  { id: 'g00', text: 'User set personal best 25:50 in charity 5K run', embedding: [0.9, 0.1, 0.05], source: 'user' },
  { id: 'g01', text: 'User completed half marathon in 1:55', embedding: [0.85, 0.15, 0.02], source: 'user' },
  { id: 'g02', text: 'Assistant suggested running shoes', embedding: [0.7, 0.3, 0.1], source: 'assistant' },
  { id: 'g03', text: 'User trains five days per week', embedding: [0.6, 0.2, 0.2], source: 'user' },
  { id: 'g04', text: 'Weather forecast says sunny tomorrow', embedding: [0.0, 0.1, 0.9], source: 'user' },
  { id: 'g05', text: 'User prefers PostgreSQL for analytics', embedding: [0.1, 0.9, 0.0], source: 'user' },
  { id: 'g06', text: 'Bob enjoys hiking on weekends', embedding: [0.3, 0.0, 0.6], source: 'user-inferred' },
  { id: 'g07', text: 'User had pizza for dinner', embedding: [0.0, 0.0, 1.0], source: 'user' },
  { id: 'g08', text: 'Marathon training tips and strategy', embedding: [0.5, 0.4, 0.1], source: 'external' },
  { id: 'g09', text: 'User runs in Central Park weekly', embedding: [0.7, 0.2, 0.1], source: 'user' },
  { id: 'g10', text: 'Charity 5K event raised funds for shelter', embedding: [0.5, 0.3, 0.2], source: 'derived' },
  { id: 'g11', text: 'User logged 25 minutes 50 seconds time', embedding: [0.95, 0.05, 0.0], source: 'user' },
  { id: 'g12', text: 'Project deadline next Friday', embedding: [0.0, 0.5, 0.5], source: 'user' },
  { id: 'g13', text: 'Coffee preference is dark roast', embedding: [0.0, 0.7, 0.3], source: 'user' },
  { id: 'g14', text: 'User won 5K race in 25 minutes 50', embedding: [0.92, 0.08, 0.0], source: 'user' },
  { id: 'g15', text: 'Assistant noted user enjoys running', embedding: [0.55, 0.4, 0.05], source: 'assistant' },
  { id: 'g16', text: 'Total kilometers run last month: 120', embedding: [0.6, 0.3, 0.1], source: 'derived' },
  { id: 'g17', text: 'Pace target is 5 minutes per kilometer', embedding: [0.65, 0.25, 0.1], source: 'user' },
  { id: 'g18', text: 'User dislikes interval training', embedding: [0.5, 0.4, 0.1], source: 'user' },
  { id: 'g19', text: 'Running playlist includes electronic music', embedding: [0.4, 0.3, 0.3], source: 'user' },
  { id: 'g20', text: 'Charity event was held on Saturday', embedding: [0.3, 0.5, 0.2], source: 'external' },
  { id: 'g21', text: 'User prefers morning runs over evening', embedding: [0.7, 0.2, 0.1], source: 'user-inferred' },
  { id: 'g22', text: 'Personal record was set in May', embedding: [0.85, 0.1, 0.05], source: 'user' },
  { id: 'g23', text: 'User uses Garmin watch for tracking', embedding: [0.5, 0.4, 0.1], source: 'user' },
  { id: 'g24', text: 'Distance was 5 kilometers exact', embedding: [0.7, 0.2, 0.1], source: 'user-inferred' },
  { id: 'g25', text: 'Random unrelated note about the weather', embedding: [0.05, 0.05, 0.9], source: 'user' },
  { id: 'g26', text: 'User trained six weeks for the race', embedding: [0.65, 0.25, 0.1], source: 'user' },
  { id: 'g27', text: 'Recovery routine includes stretching', embedding: [0.3, 0.4, 0.3], source: 'user' },
  { id: 'g28', text: 'Goal is sub-25-minute 5K next year', embedding: [0.8, 0.15, 0.05], source: 'user' },
  { id: 'g29', text: 'Assistant recommends hydration tips', embedding: [0.4, 0.3, 0.3], source: 'assistant' },
];

const QUERY = "What was my personal best time in the charity 5K run?";
const QUERY_EMBEDDING = [0.85, 0.1, 0.05];

// ---------------------------------------------------------------------------
// Determinism: re-running the same call must produce identical ordering.
// ---------------------------------------------------------------------------

console.log('# Determinism');

{
  const a = rerank(QUERY, QUERY_EMBEDDING, FIXTURE, 16, undefined, true);
  const b = rerank(QUERY, QUERY_EMBEDDING, FIXTURE, 16, undefined, true);
  ok(a.length === b.length, `determinism: same length (${a.length} === ${b.length})`);
  ok(
    a.every((r, i) => r.id === b[i].id),
    'determinism: same id ordering across two invocations',
  );
  ok(
    a.every((r, i) => Math.abs(r.rrfScore - b[i].rrfScore) < 1e-12),
    'determinism: identical rrfScore across two invocations',
  );
}

// ---------------------------------------------------------------------------
// Source-weight sensitivity: with weights ON, user-sourced facts surface
// above assistant-sourced ones for the same query.
// ---------------------------------------------------------------------------

console.log('# Source weighting');

{
  const withSW = rerank(QUERY, QUERY_EMBEDDING, FIXTURE, 16, undefined, true);
  const noSW = rerank(QUERY, QUERY_EMBEDDING, FIXTURE, 16, undefined, false);

  // Top-1 with source weighting MUST be a user / user-inferred / external /
  // derived candidate -- assistant-authored claims drop out of position 1
  // unless they completely dominate on text. The fixture's true positives
  // (g00, g11, g14) are user-sourced, so source weighting cannot hurt.
  const top1Source = withSW[0].source;
  ok(
    top1Source !== 'assistant',
    `source weighting: top-1 not assistant (got ${top1Source})`,
  );

  // The rrfScore distributions differ between SW=on and SW=off — they
  // should not be byte-identical.
  const swSum = withSW.reduce((s, r) => s + r.rrfScore, 0);
  const noSwSum = noSW.reduce((s, r) => s + r.rrfScore, 0);
  ok(swSum !== noSwSum, 'source weighting: SW on vs off produces different score sum');
}

// ---------------------------------------------------------------------------
// Top-K stability: top-K=8 must be a prefix of top-K=16's top-8.
// ---------------------------------------------------------------------------

console.log('# Top-K stability');

{
  const k8 = rerank(QUERY, QUERY_EMBEDDING, FIXTURE, 8, undefined, true);
  const k16 = rerank(QUERY, QUERY_EMBEDDING, FIXTURE, 16, undefined, true);
  ok(k8.length === 8, 'top-K=8 returns 8');
  ok(k16.length === 16, 'top-K=16 returns 16');
  ok(
    k8.every((r, i) => r.id === k16[i].id),
    'top-K=8 is the prefix of top-K=16',
  );
}

// ---------------------------------------------------------------------------
// Print the top-8 for cross-runtime comparison. The Python parity test
// runs the same fixture against `totalreclaw_core.rerank_with_config` and
// asserts the same id/score ordering.
// ---------------------------------------------------------------------------

console.log('# Top-8 trace (for cross-runtime comparison)');

{
  const top8 = rerank(QUERY, QUERY_EMBEDDING, FIXTURE, 8, undefined, true);
  for (const [i, r] of top8.entries()) {
    console.log(
      `# rank ${i + 1}: id=${r.id} src=${r.source ?? 'none'} ` +
      `score=${r.rrfScore.toFixed(8)} cosine=${(r.cosineSimilarity ?? 0).toFixed(4)} ` +
      `sourceWeight=${r.sourceWeight?.toFixed(2) ?? 'n/a'}`,
    );
  }
  ok(top8.length === 8, 'top-8 trace emitted');
}

console.log(`\n1..${n}`);
console.log(`# pass: ${passed}`);
console.log(`# fail: ${failed}`);

if (failed > 0) {
  console.log('\nFAILED');
  process.exit(1);
} else {
  console.log('\nALL TESTS PASSED');
  process.exit(0);
}
