/**
 * Tests for Stage 3b: digest read path, staleness, and mode resolution.
 *
 * Covers pure helpers in claims-helper.ts (DIGEST_TRAPDOOR, resolveDigestMode,
 * buildDigestClaim, extractDigestFromClaim, isDigestStale, shouldRecompile,
 * hoursSince) plus the recompile-guard state machine.
 *
 * Run with: npx tsx digest-injection.test.ts
 */

import crypto from 'node:crypto';
import {
  DIGEST_TRAPDOOR,
  DIGEST_CATEGORY,
  DIGEST_SOURCE_AGENT,
  DIGEST_CLAIM_CAP,
  buildDigestClaim,
  extractDigestFromClaim,
  hoursSince,
  isDigestBlob,
  isDigestStale,
  resolveDigestMode,
  shouldRecompile,
} from './claims-helper.js';

import * as core from '@totalreclaw/core';

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
// DIGEST_TRAPDOOR — deterministic, matches plain SHA-256("type:digest")
// ---------------------------------------------------------------------------

{
  const expected = crypto.createHash('sha256').update('type:digest').digest('hex');
  assert(DIGEST_TRAPDOOR === expected, 'DIGEST_TRAPDOOR: equals sha256("type:digest")');
  assert(/^[0-9a-f]{64}$/.test(DIGEST_TRAPDOOR), 'DIGEST_TRAPDOOR: 64-hex-char SHA-256');
}

// ---------------------------------------------------------------------------
// resolveDigestMode — v1 always returns 'on' regardless of env var.
// TOTALRECLAW_DIGEST_MODE was removed; this test asserts the env var
// has zero effect.
// ---------------------------------------------------------------------------

{
  const original = process.env.TOTALRECLAW_DIGEST_MODE;
  try {
    delete process.env.TOTALRECLAW_DIGEST_MODE;
    assert(resolveDigestMode() === 'on', 'digestMode: unset → on');

    process.env.TOTALRECLAW_DIGEST_MODE = 'off';
    assert(resolveDigestMode() === 'on', 'digestMode: env var removed, "off" ignored');

    process.env.TOTALRECLAW_DIGEST_MODE = 'template';
    assert(resolveDigestMode() === 'on', 'digestMode: env var removed, "template" ignored');

    process.env.TOTALRECLAW_DIGEST_MODE = 'nonsense';
    assert(resolveDigestMode() === 'on', 'digestMode: env var removed, unknown ignored');
  } finally {
    if (original === undefined) delete process.env.TOTALRECLAW_DIGEST_MODE;
    else process.env.TOTALRECLAW_DIGEST_MODE = original;
  }
}

// ---------------------------------------------------------------------------
// buildDigestClaim — produces a canonical Claim wrapping the digest JSON
// ---------------------------------------------------------------------------

{
  // Build a reference digest via the template path from the WASM core so the
  // Digest JSON matches what recompileDigestAsync will actually produce.
  const digestJson = core.buildTemplateDigest('[]', 1776000000n);
  const compiledAt = '2026-04-12T00:00:00Z';

  const claimJson = buildDigestClaim({ digestJson, compiledAt });

  // The claim must be a canonical Claim JSON string. Parse via core to assert.
  const roundTripped = JSON.parse(core.parseClaimOrLegacy(claimJson));
  assert(roundTripped.c === 'dig', 'buildDigestClaim: category is dig');
  assert(roundTripped.cf === 1.0, 'buildDigestClaim: confidence 1.0');
  assert(roundTripped.i === 10, 'buildDigestClaim: importance 10');
  assert(roundTripped.sa === DIGEST_SOURCE_AGENT, 'buildDigestClaim: source agent marker');
  assert(roundTripped.ea === compiledAt, 'buildDigestClaim: extractedAt = compiledAt');
  assert(roundTripped.t === digestJson, 'buildDigestClaim: text field holds raw digest JSON');
  // Digest claims must NOT carry entity refs (otherwise they'd be findable by
  // entity trapdoors, polluting normal recall results).
  assert(
    roundTripped.e === undefined || roundTripped.e.length === 0,
    'buildDigestClaim: no entity refs',
  );
}

// Canonicalization determinism: same digest JSON + compiledAt → identical bytes.
{
  const digestJson = core.buildTemplateDigest('[]', 1776000000n);
  const compiledAt = '2026-04-12T00:00:00Z';
  const a = buildDigestClaim({ digestJson, compiledAt });
  const b = buildDigestClaim({ digestJson, compiledAt });
  assert(a === b, 'buildDigestClaim: byte-identical for same input');
}

// ---------------------------------------------------------------------------
// extractDigestFromClaim — inverse of buildDigestClaim
// ---------------------------------------------------------------------------

{
  const digestJson = core.buildTemplateDigest('[]', 1776000000n);
  const compiledAt = '2026-04-12T00:00:00Z';
  const claimJson = buildDigestClaim({ digestJson, compiledAt });

  // Reader workflow: decrypted blob → parseClaimOrLegacy → extractDigestFromClaim
  const parsed = core.parseClaimOrLegacy(claimJson);
  const digest = extractDigestFromClaim(parsed);
  assert(digest !== null, 'extractDigestFromClaim: returns a digest object');
  assert(digest!.prompt_text.includes('No memories'), 'extractDigestFromClaim: prompt_text preserved');
  assert(digest!.fact_count === 0, 'extractDigestFromClaim: numeric fields preserved');
}

// Non-digest claim → returns null.
{
  const nonDigest = JSON.stringify({
    t: 'just a regular fact',
    c: 'fact',
    cf: 0.9,
    i: 5,
    sa: 'openclaw-plugin',
  });
  const canonical = core.parseClaimOrLegacy(nonDigest);
  const digest = extractDigestFromClaim(canonical);
  assert(digest === null, 'extractDigestFromClaim: non-dig category → null');
}

// Malformed inner JSON → returns null (defensive).
{
  // Hand-build a dig claim whose t field is not valid Digest JSON.
  const broken = JSON.stringify({
    t: 'not a digest object',
    c: 'dig',
    cf: 1.0,
    i: 10,
    sa: DIGEST_SOURCE_AGENT,
  });
  const canonical = core.parseClaimOrLegacy(broken);
  const digest = extractDigestFromClaim(canonical);
  assert(digest === null, 'extractDigestFromClaim: malformed inner JSON → null');
}

// ---------------------------------------------------------------------------
// isDigestBlob — filter for recall result pipeline
// ---------------------------------------------------------------------------

{
  const digestJson = core.buildTemplateDigest('[]', 1776000000n);
  const claimJson = buildDigestClaim({ digestJson, compiledAt: '2026-04-12T00:00:00Z' });
  const canonical = core.parseClaimOrLegacy(claimJson);
  assert(isDigestBlob(canonical), 'isDigestBlob: dig claim → true');

  const factClaim = core.parseClaimOrLegacy(
    JSON.stringify({ t: 'hello', c: 'fact', cf: 0.9, i: 5, sa: 'oc' }),
  );
  assert(!isDigestBlob(factClaim), 'isDigestBlob: fact claim → false');

  const legacyDoc = JSON.stringify({ text: 'hi', metadata: { importance: 0.5 } });
  assert(!isDigestBlob(legacyDoc), 'isDigestBlob: legacy {text,metadata} → false');

  assert(!isDigestBlob('not json at all'), 'isDigestBlob: garbage → false');
}

// ---------------------------------------------------------------------------
// hoursSince — tolerant to invalid input
// ---------------------------------------------------------------------------

{
  const nowMs = Date.parse('2026-04-12T12:00:00Z');
  assert(hoursSince('2026-04-12T12:00:00Z', nowMs) === 0, 'hoursSince: zero when equal');
  assert(
    Math.abs(hoursSince('2026-04-12T06:00:00Z', nowMs) - 6) < 0.001,
    'hoursSince: six hours ago',
  );
  assert(
    Math.abs(hoursSince('2026-04-11T12:00:00Z', nowMs) - 24) < 0.001,
    'hoursSince: 24 hours ago',
  );
  assert(
    hoursSince('not a valid date', nowMs) === Infinity,
    'hoursSince: invalid ISO → Infinity (forces recompile)',
  );
  // Future dates (clock skew) → 0, never negative.
  assert(
    hoursSince('2027-01-01T00:00:00Z', nowMs) === 0,
    'hoursSince: future date clamped to 0',
  );
}

// ---------------------------------------------------------------------------
// isDigestStale — pure comparison
// ---------------------------------------------------------------------------

{
  // Digest captured all claims up to unix=1000. Newest on-chain is 1000 → not stale.
  assert(isDigestStale(1000, 1000) === false, 'isDigestStale: equal → not stale');
  // Newer fact exists → stale.
  assert(isDigestStale(1000, 1001) === true, 'isDigestStale: newer on-chain → stale');
  // currentMax < digestVersion (clock skew or empty vault) → not stale.
  assert(isDigestStale(1000, 500) === false, 'isDigestStale: currentMax below → not stale');
  // Empty vault (currentMax == 0). Digest version 0 → not stale.
  assert(isDigestStale(0, 0) === false, 'isDigestStale: both zero → not stale');
}

// ---------------------------------------------------------------------------
// shouldRecompile — guard conditions per plan §15.10
// ---------------------------------------------------------------------------

{
  // Exactly the boundary: 10 new claims → recompile.
  assert(
    shouldRecompile({ countNewClaims: 10, hoursSinceCompilation: 1 }) === true,
    'shouldRecompile: 10 new claims triggers recompile',
  );
  // 9 new claims, less than 24h → skip.
  assert(
    shouldRecompile({ countNewClaims: 9, hoursSinceCompilation: 1 }) === false,
    'shouldRecompile: 9 new claims, recent compile → skip',
  );
  // Exactly 24h since compile → recompile.
  assert(
    shouldRecompile({ countNewClaims: 0, hoursSinceCompilation: 24 }) === true,
    'shouldRecompile: 24h elapsed triggers recompile',
  );
  // 23h, 1 new claim → skip.
  assert(
    shouldRecompile({ countNewClaims: 1, hoursSinceCompilation: 23 }) === false,
    'shouldRecompile: 23h + 1 claim → skip',
  );
  // Both satisfied → recompile.
  assert(
    shouldRecompile({ countNewClaims: 100, hoursSinceCompilation: 48 }) === true,
    'shouldRecompile: both conditions → recompile',
  );
  // Neither satisfied.
  assert(
    shouldRecompile({ countNewClaims: 0, hoursSinceCompilation: 0 }) === false,
    'shouldRecompile: zero/zero → skip',
  );
  // Infinite hours (invalid compiledAt) → force recompile.
  assert(
    shouldRecompile({ countNewClaims: 0, hoursSinceCompilation: Infinity }) === true,
    'shouldRecompile: Infinity hours → recompile',
  );
}

// ---------------------------------------------------------------------------
// DIGEST_CLAIM_CAP — plan §9 recommendation
// ---------------------------------------------------------------------------

{
  assert(DIGEST_CLAIM_CAP === 200, 'DIGEST_CLAIM_CAP: 200 claims');
  assert(DIGEST_CATEGORY === 'dig', 'DIGEST_CATEGORY: dig');
}

// ---------------------------------------------------------------------------
// digest-sync — staleness + guard integration behavior (pure, no I/O)
// ---------------------------------------------------------------------------

// evaluateDigestState: a stale digest whose recompile guard is met → should
// recompile; stale but guard unmet → should not; fresh digest → should not.
{
  const { evaluateDigestState } = await import('./digest-sync.js');

  // Fresh digest, equal versions, 0 new claims, 0h since → neither stale nor recompile.
  {
    const state = evaluateDigestState({
      digestVersion: 1000,
      currentMaxCreatedAt: 1000,
      countNewClaims: 0,
      hoursSinceCompilation: 0,
    });
    assertEq(
      state,
      { stale: false, recompile: false },
      'evaluateDigestState: fresh digest → stale=false, recompile=false',
    );
  }

  // Stale but guard unmet: 2 new claims, 1h since → stale but no recompile.
  {
    const state = evaluateDigestState({
      digestVersion: 1000,
      currentMaxCreatedAt: 1002,
      countNewClaims: 2,
      hoursSinceCompilation: 1,
    });
    assertEq(
      state,
      { stale: true, recompile: false },
      'evaluateDigestState: stale but guard unmet → no recompile',
    );
  }

  // Stale and 10+ new claims → recompile.
  {
    const state = evaluateDigestState({
      digestVersion: 1000,
      currentMaxCreatedAt: 1010,
      countNewClaims: 10,
      hoursSinceCompilation: 1,
    });
    assertEq(
      state,
      { stale: true, recompile: true },
      'evaluateDigestState: stale + 10 new claims → recompile',
    );
  }

  // Stale and 24h elapsed → recompile.
  {
    const state = evaluateDigestState({
      digestVersion: 1000,
      currentMaxCreatedAt: 1001,
      countNewClaims: 1,
      hoursSinceCompilation: 24,
    });
    assertEq(
      state,
      { stale: true, recompile: true },
      'evaluateDigestState: stale + 24h → recompile',
    );
  }
}

// ---------------------------------------------------------------------------
// Recompile-in-progress guard (in-memory flag)
// ---------------------------------------------------------------------------

{
  const digestSync = await import('./digest-sync.js');

  // Reset state for deterministic test.
  digestSync.__resetDigestSyncState();

  assert(
    digestSync.isRecompileInProgress() === false,
    'recompile guard: clean state → not in progress',
  );

  // Try to acquire — should succeed.
  assert(
    digestSync.tryBeginRecompile() === true,
    'recompile guard: first acquire succeeds',
  );
  assert(
    digestSync.isRecompileInProgress() === true,
    'recompile guard: acquired → in progress',
  );

  // Second acquire while in progress — should fail.
  assert(
    digestSync.tryBeginRecompile() === false,
    'recompile guard: second concurrent acquire fails',
  );

  // Release.
  digestSync.endRecompile();
  assert(
    digestSync.isRecompileInProgress() === false,
    'recompile guard: after release → not in progress',
  );

  // Can acquire again after release.
  assert(
    digestSync.tryBeginRecompile() === true,
    'recompile guard: can re-acquire after release',
  );
  digestSync.endRecompile();
}

// ---------------------------------------------------------------------------
// Template-only compilation path (no LLM) — integration via compileDigestCore
// ---------------------------------------------------------------------------

{
  const { compileDigestCore } = await import('./digest-sync.js');

  // No claims → empty-vault template text.
  const emptyDigestJson = await compileDigestCore({
    claimsJson: '[]',
    nowUnixSeconds: 1776000000,
    mode: 'template',
    llmFn: null,
    logger: { info: () => {}, warn: () => {} },
  });
  const empty = JSON.parse(emptyDigestJson);
  assert(empty.fact_count === 0, 'compileDigestCore: empty claims → fact_count 0');
  assert(
    empty.prompt_text.includes('No memories'),
    'compileDigestCore: empty claims → empty-vault prompt',
  );

  // Two claims → template digest with top_claims populated.
  const twoClaims = JSON.stringify([
    {
      t: 'Pedro lives in Lisbon',
      c: 'fact',
      cf: 0.9,
      i: 8,
      sa: 'oc',
      ea: '2026-04-10T00:00:00Z',
    },
    {
      t: 'Pedro prefers PostgreSQL',
      c: 'pref',
      cf: 0.9,
      i: 9,
      sa: 'oc',
      ea: '2026-04-11T00:00:00Z',
    },
  ]);
  const digestJson = await compileDigestCore({
    claimsJson: twoClaims,
    nowUnixSeconds: 1776000000,
    mode: 'template',
    llmFn: null,
    logger: { info: () => {}, warn: () => {} },
  });
  const d = JSON.parse(digestJson);
  assert(d.fact_count === 2, 'compileDigestCore: two claims → fact_count 2');
  assert(
    d.top_claims.length === 2,
    'compileDigestCore: two claims → two top claims',
  );
  assert(
    d.prompt_text.includes('PostgreSQL'),
    'compileDigestCore: prompt_text mentions claim content',
  );
}

// LLM path success: llmFn returns valid JSON → assembled digest uses identity.
{
  const { compileDigestCore } = await import('./digest-sync.js');

  const twoClaims = JSON.stringify([
    {
      t: 'Pedro lives in Lisbon',
      c: 'fact',
      cf: 0.9,
      i: 8,
      sa: 'oc',
      ea: '2026-04-10T00:00:00Z',
    },
    {
      t: 'Pedro prefers PostgreSQL',
      c: 'pref',
      cf: 0.9,
      i: 9,
      sa: 'oc',
      ea: '2026-04-11T00:00:00Z',
    },
  ]);
  let promptSeen = '';
  const llmFn = async (prompt: string) => {
    promptSeen = prompt;
    return JSON.stringify({
      identity: 'You are a software engineer in Lisbon who prefers PostgreSQL.',
      top_claim_indices: [1, 2],
      recent_decision_indices: [],
      active_project_names: [],
    });
  };
  const digestJson = await compileDigestCore({
    claimsJson: twoClaims,
    nowUnixSeconds: 1776000000,
    mode: 'on',
    llmFn,
    logger: { info: () => {}, warn: () => {} },
  });
  const d = JSON.parse(digestJson);
  assert(
    d.identity.includes('Lisbon'),
    'compileDigestCore: LLM identity makes it into the digest',
  );
  assert(promptSeen.length > 0, 'compileDigestCore: LLM was invoked');
  assert(
    d.top_claims.length === 2,
    'compileDigestCore: LLM-selected top_claims populated',
  );
}

// LLM path failure: llmFn throws → falls back to template silently.
{
  const { compileDigestCore } = await import('./digest-sync.js');

  const twoClaims = JSON.stringify([
    {
      t: 'Pedro lives in Lisbon',
      c: 'fact',
      cf: 0.9,
      i: 8,
      sa: 'oc',
      ea: '2026-04-10T00:00:00Z',
    },
    {
      t: 'Pedro prefers PostgreSQL',
      c: 'pref',
      cf: 0.9,
      i: 9,
      sa: 'oc',
      ea: '2026-04-11T00:00:00Z',
    },
  ]);
  const llmFn = async () => {
    throw new Error('simulated LLM outage');
  };
  let warned = false;
  const digestJson = await compileDigestCore({
    claimsJson: twoClaims,
    nowUnixSeconds: 1776000000,
    mode: 'on',
    llmFn,
    logger: { info: () => {}, warn: () => { warned = true; } },
  });
  const d = JSON.parse(digestJson);
  assert(d.fact_count === 2, 'compileDigestCore: fallback digest still has facts');
  assert(d.identity === '', 'compileDigestCore: fallback has no LLM identity');
  assert(warned === true, 'compileDigestCore: LLM failure was logged as warning');
}

// LLM path bad JSON: llmFn returns garbage → falls back to template.
{
  const { compileDigestCore } = await import('./digest-sync.js');

  const oneClaim = JSON.stringify([
    {
      t: 'Pedro lives in Lisbon',
      c: 'fact',
      cf: 0.9,
      i: 8,
      sa: 'oc',
      ea: '2026-04-10T00:00:00Z',
    },
  ]);
  const llmFn = async () => 'not json at all {{{';
  const digestJson = await compileDigestCore({
    claimsJson: oneClaim,
    nowUnixSeconds: 1776000000,
    mode: 'on',
    llmFn,
    logger: { info: () => {}, warn: () => {} },
  });
  const d = JSON.parse(digestJson);
  assert(
    d.fact_count === 1 && d.identity === '',
    'compileDigestCore: garbage LLM → template fallback',
  );
}

// Template-mode flag: even with LLM available, template is used.
{
  const { compileDigestCore } = await import('./digest-sync.js');

  const oneClaim = JSON.stringify([
    {
      t: 'Pedro lives in Lisbon',
      c: 'fact',
      cf: 0.9,
      i: 8,
      sa: 'oc',
      ea: '2026-04-10T00:00:00Z',
    },
  ]);
  let llmCalled = false;
  const llmFn = async () => {
    llmCalled = true;
    return JSON.stringify({
      identity: 'You live in Lisbon.',
      top_claim_indices: [1],
      recent_decision_indices: [],
      active_project_names: [],
    });
  };
  const digestJson = await compileDigestCore({
    claimsJson: oneClaim,
    nowUnixSeconds: 1776000000,
    mode: 'template',
    llmFn,
    logger: { info: () => {}, warn: () => {} },
  });
  const d = JSON.parse(digestJson);
  assert(
    llmCalled === false,
    'compileDigestCore: mode=template bypasses LLM even when available',
  );
  assert(
    d.identity === '',
    'compileDigestCore: template mode → empty identity',
  );
}

// Claim-count cap: above DIGEST_CLAIM_CAP, template is forced.
{
  const { compileDigestCore } = await import('./digest-sync.js');

  // Build 201 trivial claims.
  const manyClaims = JSON.stringify(
    Array.from({ length: DIGEST_CLAIM_CAP + 1 }, (_, i) => ({
      t: `fact number ${i}`,
      c: 'fact',
      cf: 0.9,
      i: 5,
      sa: 'oc',
      ea: '2026-04-10T00:00:00Z',
    })),
  );
  let llmCalled = false;
  const llmFn = async () => {
    llmCalled = true;
    return '{"identity":"x","top_claim_indices":[1],"recent_decision_indices":[],"active_project_names":[]}';
  };
  const digestJson = await compileDigestCore({
    claimsJson: manyClaims,
    nowUnixSeconds: 1776000000,
    mode: 'on',
    llmFn,
    logger: { info: () => {}, warn: () => {} },
  });
  const d = JSON.parse(digestJson);
  assert(
    llmCalled === false,
    `compileDigestCore: >${DIGEST_CLAIM_CAP} claims → LLM skipped`,
  );
  assert(d.fact_count === DIGEST_CLAIM_CAP + 1, 'compileDigestCore: all claims still counted');
}

// ---------------------------------------------------------------------------
// maybeInjectDigest — full read path with mocked subgraph + crypto
// ---------------------------------------------------------------------------

// Helper: build a digest-claim blob as raw decrypted text, so the fake
// decryptFromHex can return it without real crypto.
function fakeDigestBlob(digestVersion: number, compiledAt: string): string {
  // Build the digest JSON with the required fields the reader cares about.
  const digest = {
    version: digestVersion,
    compiled_at: compiledAt,
    fact_count: 3,
    entity_count: 0,
    contradiction_count: 0,
    identity: 'You are a test user.',
    top_claims: [],
    recent_decisions: [],
    active_projects: [],
    active_contradictions: 0,
    prompt_text: 'You know three things.',
  };
  const digestJson = JSON.stringify(digest);
  // Wrap in a canonical Claim via the helper.
  return buildDigestClaim({ digestJson, compiledAt });
}

// mode='off' → never queries, always returns null.
{
  const { maybeInjectDigest, __resetDigestSyncState } = await import('./digest-sync.js');
  __resetDigestSyncState();

  let calls = 0;
  const result = await maybeInjectDigest({
    owner: '0xabc',
    authKeyHex: 'ff',
    encryptionKey: Buffer.from('0000000000000000000000000000000000000000000000000000000000000000', 'hex'),
    mode: 'off',
    nowMs: Date.now(),
    loadDeps: {
      searchSubgraph: async () => { calls++; return []; },
      decryptFromHex: () => 'unused',
    },
    probeDeps: {
      searchSubgraphBroadened: async () => { calls++; return []; },
    },
    recompileFn: () => {},
    logger: { info: () => {}, warn: () => {} },
  });
  assert(result.promptText === null, 'maybeInjectDigest: mode=off → promptText null');
  assert(result.state === 'off', 'maybeInjectDigest: mode=off → state off');
  assert(calls === 0, 'maybeInjectDigest: mode=off → no subgraph queries');
}

// No digest found → first-compile state, recompileFn invoked.
{
  const { maybeInjectDigest, __resetDigestSyncState } = await import('./digest-sync.js');
  __resetDigestSyncState();

  let recompileCalls: Array<string | null> = [];
  const result = await maybeInjectDigest({
    owner: '0xabc',
    authKeyHex: 'ff',
    encryptionKey: Buffer.alloc(32),
    mode: 'on',
    nowMs: Date.now(),
    loadDeps: {
      searchSubgraph: async () => [], // no digest
      decryptFromHex: () => 'unused',
    },
    probeDeps: {
      searchSubgraphBroadened: async () => [],
    },
    recompileFn: (prev) => { recompileCalls.push(prev); },
    logger: { info: () => {}, warn: () => {} },
  });
  assert(result.promptText === null, 'maybeInjectDigest: no digest → null');
  assert(result.state === 'first-compile', 'maybeInjectDigest: no digest → first-compile state');
  assert(recompileCalls.length === 1 && recompileCalls[0] === null, 'maybeInjectDigest: no digest → recompile triggered with null');
}

// Fresh digest → returns promptText, no recompile.
{
  const { maybeInjectDigest, __resetDigestSyncState } = await import('./digest-sync.js');
  __resetDigestSyncState();

  const compiledAt = new Date().toISOString();
  const digestVersion = 1776000000;
  const blob = fakeDigestBlob(digestVersion, compiledAt);

  let recompileCalls = 0;
  const result = await maybeInjectDigest({
    owner: '0xabc',
    authKeyHex: 'ff',
    encryptionKey: Buffer.alloc(32),
    mode: 'on',
    nowMs: Date.now(),
    loadDeps: {
      searchSubgraph: async () => [
        { id: '0xdeadbeef', encryptedBlob: 'dummy', createdAt: String(digestVersion) },
      ],
      decryptFromHex: () => blob,
    },
    probeDeps: {
      // Max createdAt equals digest version → not stale.
      searchSubgraphBroadened: async () => [
        { createdAt: String(digestVersion) },
      ],
    },
    recompileFn: () => { recompileCalls++; },
    logger: { info: () => {}, warn: () => {} },
  });
  assert(result.promptText === 'You know three things.', 'maybeInjectDigest: fresh → promptText injected');
  assert(result.state === 'fresh', 'maybeInjectDigest: fresh → state fresh');
  assert(recompileCalls === 0, 'maybeInjectDigest: fresh → no recompile');
}

// Stale digest with guard met → returns stale promptText + triggers recompile.
{
  const { maybeInjectDigest, __resetDigestSyncState } = await import('./digest-sync.js');
  __resetDigestSyncState();

  const compiledAt = '2026-04-10T00:00:00Z'; // old enough for 24h rule
  const nowMs = Date.parse('2026-04-12T00:00:00Z'); // 48h later
  const digestVersion = 1776000000;
  const newerMax = digestVersion + 1000; // stale
  const blob = fakeDigestBlob(digestVersion, compiledAt);

  let recompileCalls: Array<string | null> = [];
  const result = await maybeInjectDigest({
    owner: '0xabc',
    authKeyHex: 'ff',
    encryptionKey: Buffer.alloc(32),
    mode: 'on',
    nowMs,
    loadDeps: {
      searchSubgraph: async () => [
        { id: 'digest-claim-id', encryptedBlob: 'dummy', createdAt: String(digestVersion) },
      ],
      decryptFromHex: () => blob,
    },
    probeDeps: {
      searchSubgraphBroadened: async () => [
        { createdAt: String(newerMax) },
      ],
    },
    recompileFn: (prev) => { recompileCalls.push(prev); },
    logger: { info: () => {}, warn: () => {} },
  });
  assert(result.promptText === 'You know three things.', 'maybeInjectDigest: stale → stale promptText returned');
  assert(result.state === 'stale', 'maybeInjectDigest: stale → state stale');
  assert(
    recompileCalls.length === 1 && recompileCalls[0] === 'digest-claim-id',
    'maybeInjectDigest: stale → recompile triggered with previous claim id',
  );
}

// Stale but guard unmet → returns stale digest, NO recompile.
{
  const { maybeInjectDigest, __resetDigestSyncState } = await import('./digest-sync.js');
  __resetDigestSyncState();

  const compiledAt = new Date(Date.now() - 60 * 60 * 1000).toISOString(); // 1h ago
  const digestVersion = 1776000000;
  // Only 1 new fact → countNewerThan returns 1, under 10-claim threshold.
  const blob = fakeDigestBlob(digestVersion, compiledAt);

  let recompileCalls = 0;
  const result = await maybeInjectDigest({
    owner: '0xabc',
    authKeyHex: 'ff',
    encryptionKey: Buffer.alloc(32),
    mode: 'on',
    nowMs: Date.now(),
    loadDeps: {
      searchSubgraph: async () => [
        { id: 'id', encryptedBlob: 'dummy', createdAt: String(digestVersion) },
      ],
      decryptFromHex: () => blob,
    },
    probeDeps: {
      searchSubgraphBroadened: async () => [
        { createdAt: String(digestVersion + 1) },
      ],
    },
    recompileFn: () => { recompileCalls++; },
    logger: { info: () => {}, warn: () => {} },
  });
  assert(result.state === 'stale', 'maybeInjectDigest: stale-but-under-guard → still stale state');
  assert(recompileCalls === 0, 'maybeInjectDigest: stale-but-under-guard → no recompile');
}

// Recompile already in progress → returns digest but does NOT fire another.
{
  const digestSync = await import('./digest-sync.js');
  digestSync.__resetDigestSyncState();
  // Pretend a recompile is already running.
  digestSync.tryBeginRecompile();

  const compiledAt = '2026-04-10T00:00:00Z';
  const nowMs = Date.parse('2026-04-12T00:00:00Z');
  const digestVersion = 1776000000;
  const newerMax = digestVersion + 1000;
  const blob = fakeDigestBlob(digestVersion, compiledAt);

  let recompileCalls = 0;
  const result = await digestSync.maybeInjectDigest({
    owner: '0xabc',
    authKeyHex: 'ff',
    encryptionKey: Buffer.alloc(32),
    mode: 'on',
    nowMs,
    loadDeps: {
      searchSubgraph: async () => [
        { id: 'id', encryptedBlob: 'dummy', createdAt: String(digestVersion) },
      ],
      decryptFromHex: () => blob,
    },
    probeDeps: {
      searchSubgraphBroadened: async () => [{ createdAt: String(newerMax) }],
    },
    recompileFn: () => { recompileCalls++; },
    logger: { info: () => {}, warn: () => {} },
  });
  assert(result.state === 'stale', 'maybeInjectDigest: in-progress → still returns stale');
  assert(recompileCalls === 0, 'maybeInjectDigest: in-progress → no new recompile fired');
  digestSync.endRecompile();
}

// Subgraph query failure in loadLatestDigest → treated as "no digest" → first-compile.
{
  const { maybeInjectDigest, __resetDigestSyncState } = await import('./digest-sync.js');
  __resetDigestSyncState();

  let recompileCalls = 0;
  const result = await maybeInjectDigest({
    owner: '0xabc',
    authKeyHex: 'ff',
    encryptionKey: Buffer.alloc(32),
    mode: 'on',
    nowMs: Date.now(),
    loadDeps: {
      searchSubgraph: async () => { throw new Error('network down'); },
      decryptFromHex: () => 'unused',
    },
    probeDeps: {
      searchSubgraphBroadened: async () => [],
    },
    recompileFn: () => { recompileCalls++; },
    logger: { info: () => {}, warn: () => {} },
  });
  assert(result.promptText === null, 'maybeInjectDigest: subgraph error → null');
  assert(result.state === 'first-compile', 'maybeInjectDigest: subgraph error → first-compile');
  assert(recompileCalls === 1, 'maybeInjectDigest: subgraph error → schedule first compile');
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
