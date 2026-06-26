/**
 * Tests for Phase 2 Slice 2d: contradiction detection + auto-resolution in the
 * OpenClaw plugin write path.
 *
 * Exercises both the pure resolver (`resolveWithCore`) and the full write-path
 * entry point (`detectAndResolveContradictions`) with a mocked subgraph + a
 * real in-memory decryptFromHex. The WASM core is NOT mocked — tests run
 * against the live @totalreclaw/core bindings.
 *
 * Run with: npx tsx contradiction-sync.test.ts
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {
  appendDecisionLog,
  collectCandidatesForEntities,
  CONTRADICTION_CANDIDATE_CAP,
  decisionsLogPath,
  detectAndResolveContradictions,
  DecisionLogEntry,
  findLoserClaimInDecisionLog,
  getTuningLoopMinIntervalSeconds,
  isPinnedClaim,
  loadWeightsFile,
  parseCandidateClaim,
  resolveWithCore,
  TIE_ZONE_SCORE_TOLERANCE,
  TUNING_LOOP_MIN_INTERVAL_SECONDS,
  weightsFilePath,
  type CandidateClaim,
  type CanonicalClaim,
  type ResolutionDecision,
} from './contradiction-sync.js';
import { computeEntityTrapdoor } from './claims-helper.js';

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
// Shared helpers
// ---------------------------------------------------------------------------

function setupTempStateDir(label: string): string {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), `tr-contradiction-${label}-`));
  process.env.TOTALRECLAW_STATE_DIR = dir;
  return dir;
}

function cleanupTempStateDir(dir: string): void {
  try {
    fs.rmSync(dir, { recursive: true, force: true });
  } catch {
    /* ignore */
  }
  delete process.env.TOTALRECLAW_STATE_DIR;
}

const silentLogger = {
  info: () => undefined,
  warn: () => undefined,
};

function makeCaptureLogger() {
  const warnings: string[] = [];
  const infos: string[] = [];
  return {
    logger: {
      info: (m: string) => {
        infos.push(m);
      },
      warn: (m: string) => {
        warnings.push(m);
      },
    },
    warnings,
    infos,
  };
}

function makeClaim(fields: Partial<CanonicalClaim> & { t: string; c?: string }): CanonicalClaim {
  return {
    t: fields.t,
    c: fields.c ?? 'pref',
    cf: 0.9,
    i: 7,
    sa: 'auto-extraction',
    ea: '2026-04-01T00:00:00Z',
    e: [{ n: 'editor', tp: 'concept' }],
    ...fields,
  };
}

// Build a unit-ish embedding of arbitrary dimension for cosine work.
function embed(values: number[], dims = 8): number[] {
  const out = new Array<number>(dims).fill(0);
  for (let i = 0; i < values.length && i < dims; i++) out[i] = values[i];
  return out;
}

// Fake decrypt: our "encryptedBlob" is just the raw canonical claim JSON hex.
function fakeEncrypt(jsonString: string): string {
  return Buffer.from(jsonString, 'utf-8').toString('hex');
}

function fakeDecrypt(hex: string, _key: Buffer): string {
  const clean = hex.startsWith('0x') ? hex.slice(2) : hex;
  return Buffer.from(clean, 'hex').toString('utf-8');
}

// Build a mock subgraph search function that returns the given rows only
// when queried with the matching trapdoor. Any other trapdoor returns [].
type FakeRow = {
  id: string;
  encryptedBlob: string;
  encryptedEmbedding?: string | null;
  isActive?: boolean;
};

function fakeSubgraph(byTrapdoor: Record<string, FakeRow[]>) {
  return async (
    _owner: string,
    trapdoors: string[],
    maxCandidates: number,
    _authKeyHex?: string,
  ): Promise<FakeRow[]> => {
    const seen = new Set<string>();
    const out: FakeRow[] = [];
    for (const t of trapdoors) {
      const rows = byTrapdoor[t] ?? [];
      for (const r of rows) {
        if (seen.has(r.id)) continue;
        seen.add(r.id);
        out.push(r);
        if (out.length >= maxCandidates) return out;
      }
    }
    return out;
  };
}

// ---------------------------------------------------------------------------
// resolveAutoResolveMode (env var)
// ---------------------------------------------------------------------------

{
  const original = process.env.TOTALRECLAW_AUTO_RESOLVE_MODE;
  try {
    const { resolveAutoResolveMode } = await import('./claims-helper.js');

    delete process.env.TOTALRECLAW_AUTO_RESOLVE_MODE;
    assert(resolveAutoResolveMode() === 'active', 'autoResolveMode: unset → active');

    process.env.TOTALRECLAW_AUTO_RESOLVE_MODE = 'active';
    assert(resolveAutoResolveMode() === 'active', 'autoResolveMode: explicit active');

    process.env.TOTALRECLAW_AUTO_RESOLVE_MODE = 'OFF';
    assert(resolveAutoResolveMode() === 'off', 'autoResolveMode: case-insensitive OFF');

    process.env.TOTALRECLAW_AUTO_RESOLVE_MODE = 'shadow';
    assert(resolveAutoResolveMode() === 'shadow', 'autoResolveMode: shadow');

    process.env.TOTALRECLAW_AUTO_RESOLVE_MODE = 'nonsense';
    assert(resolveAutoResolveMode() === 'active', 'autoResolveMode: unknown → active');

    process.env.TOTALRECLAW_AUTO_RESOLVE_MODE = '';
    assert(resolveAutoResolveMode() === 'active', 'autoResolveMode: empty → active');
  } finally {
    if (original === undefined) delete process.env.TOTALRECLAW_AUTO_RESOLVE_MODE;
    else process.env.TOTALRECLAW_AUTO_RESOLVE_MODE = original;
  }
}

// ---------------------------------------------------------------------------
// parseCandidateClaim — accepts canonical, rejects infra + bad blobs
// ---------------------------------------------------------------------------

{
  const claimJson = JSON.stringify({
    t: 'I prefer Neovim',
    c: 'pref',
    cf: 0.9,
    i: 7,
    sa: 'auto-extraction',
    ea: '2026-04-01T00:00:00Z',
  });
  const parsed = parseCandidateClaim(claimJson);
  assert(parsed !== null && parsed!.t === 'I prefer Neovim', 'parseCandidateClaim: canonical claim passes');
}
{
  const digestJson = JSON.stringify({ t: 'x', c: 'dig', cf: 1, i: 10, sa: 'digest', ea: 'now' });
  assert(parseCandidateClaim(digestJson) === null, 'parseCandidateClaim: digest blob rejected');
}
{
  const entityJson = JSON.stringify({ t: 'x', c: 'ent', cf: 1, i: 10, sa: 'plugin', ea: 'now' });
  assert(parseCandidateClaim(entityJson) === null, 'parseCandidateClaim: entity blob rejected');
}
{
  const legacyJson = JSON.stringify({ text: 'old-style', metadata: { importance: 0.5 } });
  assert(parseCandidateClaim(legacyJson) === null, 'parseCandidateClaim: legacy doc rejected');
}
{
  assert(parseCandidateClaim('not json at all {{{') === null, 'parseCandidateClaim: malformed JSON rejected');
}

// ---------------------------------------------------------------------------
// isPinnedClaim
// ---------------------------------------------------------------------------

{
  assert(isPinnedClaim({ t: 'x', c: 'fact', st: 'p' }) === true, 'isPinnedClaim: st=p → true');
  assert(isPinnedClaim({ t: 'x', c: 'fact' }) === false, 'isPinnedClaim: missing st → false (default active)');
  assert(isPinnedClaim({ t: 'x', c: 'fact', st: 'a' }) === false, 'isPinnedClaim: st=a → false');
  assert(isPinnedClaim({ t: 'x', c: 'fact', st: 's' }) === false, 'isPinnedClaim: st=s (superseded) → false');
}

// ---------------------------------------------------------------------------
// resolveWithCore — pure logic against real WASM
// ---------------------------------------------------------------------------

async function getDefaultWeightsJson(): Promise<string> {
  const tmp = setupTempStateDir('weights');
  try {
    const file = await loadWeightsFile(1_776_384_000);
    return JSON.stringify(file.weights);
  } finally {
    cleanupTempStateDir(tmp);
  }
}

const WEIGHTS_JSON = await getDefaultWeightsJson();

// Vim-vs-VS-Code: new claim "I use VS Code" vs existing "I use Vim" (~0.5 cosine).
function makeVimVsVsCodeCandidate(): CandidateClaim {
  return {
    id: 'existing-vim',
    claim: makeClaim({
      t: 'I use Vim as my primary editor',
      c: 'pref',
      ea: '2025-06-01T00:00:00Z', // old
      sa: 'auto-extraction',
    }),
    embedding: embed([0.7, 0.7, 0.0, 0.0], 8),
  };
}

// Empty existing list → no decisions.
{
  const decisions = resolveWithCore({
    newClaim: makeClaim({ t: 'I use VS Code now' }),
    newClaimId: 'new-1',
    newEmbedding: embed([0.7, 0.7, 0.0, 0.0], 8),
    candidates: [],
    weightsJson: WEIGHTS_JSON,
    thresholdLower: 0.3,
    thresholdUpper: 0.85,
    nowUnixSeconds: 1_777_000_000,
    mode: 'active',
    logger: silentLogger,
  });
  assertEq(decisions, [], 'resolveWithCore: no candidates → empty decisions');
}

// Mode=off → empty regardless of candidates.
{
  const decisions = resolveWithCore({
    newClaim: makeClaim({ t: 'I use VS Code now' }),
    newClaimId: 'new-1',
    newEmbedding: embed([0.7, 0.7, 0.0, 0.0], 8),
    candidates: [makeVimVsVsCodeCandidate()],
    weightsJson: WEIGHTS_JSON,
    thresholdLower: 0.3,
    thresholdUpper: 0.85,
    nowUnixSeconds: 1_777_000_000,
    mode: 'off',
    logger: silentLogger,
  });
  assertEq(decisions, [], 'resolveWithCore: mode=off → empty decisions');
}

// New claim has no entities → empty (matches Rust contract).
{
  const decisions = resolveWithCore({
    newClaim: { t: 'orphan fact', c: 'fact', cf: 0.9, i: 5, sa: 'auto-extraction', ea: 'x' },
    newClaimId: 'new-1',
    newEmbedding: embed([0.7, 0.7, 0.0, 0.0], 8),
    candidates: [makeVimVsVsCodeCandidate()],
    weightsJson: WEIGHTS_JSON,
    thresholdLower: 0.3,
    thresholdUpper: 0.85,
    nowUnixSeconds: 1_777_000_000,
    mode: 'active',
    logger: silentLogger,
  });
  assertEq(decisions, [], 'resolveWithCore: no entities on new claim → empty');
}

// Empty new embedding → no decisions + warn.
{
  const cap = makeCaptureLogger();
  const decisions = resolveWithCore({
    newClaim: makeClaim({ t: 'I use VS Code now' }),
    newClaimId: 'new-1',
    newEmbedding: [],
    candidates: [makeVimVsVsCodeCandidate()],
    weightsJson: WEIGHTS_JSON,
    thresholdLower: 0.3,
    thresholdUpper: 0.85,
    nowUnixSeconds: 1_777_000_000,
    mode: 'active',
    logger: cap.logger,
  });
  assertEq(decisions, [], 'resolveWithCore: empty new embedding → empty');
  assert(cap.warnings.length > 0, 'resolveWithCore: empty new embedding → warning logged');
}

// Vim vs VS Code with new claim FRESH (now) and old claim STALE → new wins.
{
  const existing = makeVimVsVsCodeCandidate();
  const newEmbedding = embed([0.75, 0.65, 0.0, 0.0], 8); // sim ~0.99? no — far from 1 b/c normalized?
  // The point: we want sim in [0.3, 0.85). Let's use orthogonal-ish vectors.
  const newClaim = makeClaim({
    t: 'I have switched to VS Code full-time',
    c: 'pref',
    ea: '2026-04-10T00:00:00Z', // very fresh
    sa: 'totalreclaw_remember', // explicit validation boost
  });
  // Use vectors with a known cosine: a=[1,0,0,...], b=[cos45, sin45, 0,...] → cos = 0.707
  const newEmb = embed([1.0, 0.0, 0.0, 0.0], 8);
  existing.embedding = embed([Math.cos(Math.PI / 4), Math.sin(Math.PI / 4), 0, 0], 8);
  const decisions = resolveWithCore({
    newClaim,
    newClaimId: 'new-vscode',
    newEmbedding: newEmb,
    candidates: [existing],
    weightsJson: WEIGHTS_JSON,
    thresholdLower: 0.3,
    thresholdUpper: 0.85,
    nowUnixSeconds: 1_777_000_000,
    mode: 'active',
    logger: silentLogger,
  });
  assert(decisions.length === 1, 'resolveWithCore: vim-vs-vscode → exactly one decision');
  const d = decisions[0];
  assert(d.action === 'supersede_existing', 'resolveWithCore: vim-vs-vscode → new fresh+validated wins');
  if (d.action === 'supersede_existing') {
    assert(d.existingFactId === 'existing-vim', 'resolveWithCore: decision names the existing claim id');
    assert(d.similarity >= 0.3 && d.similarity < 0.85, 'resolveWithCore: similarity in band');
    assert(typeof d.winnerScore === 'number', 'resolveWithCore: decision carries winner score');
    // Slice 2f: full per-component breakdowns must thread through.
    assert(typeof d.winnerComponents === 'object', 'resolveWithCore: decision carries winnerComponents');
    assert(typeof d.loserComponents === 'object', 'resolveWithCore: decision carries loserComponents');
    assert(
      typeof d.winnerComponents.confidence === 'number' &&
        typeof d.winnerComponents.corroboration === 'number' &&
        typeof d.winnerComponents.recency === 'number' &&
        typeof d.winnerComponents.validation === 'number' &&
        typeof d.winnerComponents.weighted_total === 'number',
      'resolveWithCore: winnerComponents has all 5 fields',
    );
    assert(
      d.winnerComponents.weighted_total === d.winnerScore,
      'resolveWithCore: winnerComponents.weighted_total matches winnerScore',
    );
    assert(
      d.loserComponents.weighted_total === d.loserScore,
      'resolveWithCore: loserComponents.weighted_total matches loserScore',
    );
  }
}

// Existing is pinned → skip_new with reason=existing_pinned, formula not consulted.
{
  const existing: CandidateClaim = {
    id: 'pinned-vim',
    claim: {
      ...makeClaim({ t: 'I use Vim as my primary editor', c: 'pref' }),
      st: 'p',
    },
    embedding: embed([Math.cos(Math.PI / 4), Math.sin(Math.PI / 4), 0, 0], 8),
  };
  const newEmb = embed([1.0, 0.0, 0.0, 0.0], 8);
  const decisions = resolveWithCore({
    newClaim: makeClaim({ t: 'I use VS Code now', ea: '2026-04-10T00:00:00Z' }),
    newClaimId: 'new-vscode',
    newEmbedding: newEmb,
    candidates: [existing],
    weightsJson: WEIGHTS_JSON,
    thresholdLower: 0.3,
    thresholdUpper: 0.85,
    nowUnixSeconds: 1_777_000_000,
    mode: 'active',
    logger: silentLogger,
  });
  assert(decisions.length === 1, 'resolveWithCore: pinned existing → exactly one decision');
  const d = decisions[0];
  assert(d.action === 'skip_new', 'resolveWithCore: pinned existing → skip_new');
  if (d.action === 'skip_new') {
    assertEq(d.reason, 'existing_pinned', 'resolveWithCore: reason=existing_pinned');
    assertEq(d.existingFactId, 'pinned-vim', 'resolveWithCore: pinned decision names the pinned id');
    assert(d.winnerScore === undefined, 'resolveWithCore: pinned skip does not carry scores');
  }
}

// Existing wins (fresher + validated) → skip_new with reason=existing_wins.
{
  const existing: CandidateClaim = {
    id: 'fresh-existing',
    claim: makeClaim({
      t: 'I prefer Neovim',
      ea: '2026-04-10T00:00:00Z',
      sa: 'totalreclaw_remember', // explicit, validation=1.0
    }),
    embedding: embed([Math.cos(Math.PI / 4), Math.sin(Math.PI / 4), 0, 0], 8),
  };
  const newClaim = makeClaim({
    t: 'I use Vim a little',
    ea: '2024-01-01T00:00:00Z', // very old
    sa: 'auto-extraction', // validation=0.7
  });
  const newEmb = embed([1.0, 0.0, 0.0, 0.0], 8);
  const decisions = resolveWithCore({
    newClaim,
    newClaimId: 'new-stale',
    newEmbedding: newEmb,
    candidates: [existing],
    weightsJson: WEIGHTS_JSON,
    thresholdLower: 0.3,
    thresholdUpper: 0.85,
    nowUnixSeconds: 1_777_000_000,
    mode: 'active',
    logger: silentLogger,
  });
  assert(decisions.length === 1, 'resolveWithCore: stale new + fresh existing → one decision');
  const d = decisions[0];
  assert(d.action === 'skip_new', 'resolveWithCore: existing wins → skip_new');
  if (d.action === 'skip_new') {
    assertEq(d.reason, 'existing_wins', 'resolveWithCore: reason=existing_wins');
  }
}

// Similarity out of band (too similar, ~0.99) → no contradiction.
{
  const existing: CandidateClaim = {
    id: 'almost-same',
    claim: makeClaim({ t: 'I like TypeScript a lot' }),
    embedding: embed([1.0, 0.01, 0.0, 0.0], 8),
  };
  const newEmb = embed([1.0, 0.0, 0.0, 0.0], 8);
  const decisions = resolveWithCore({
    newClaim: makeClaim({ t: 'I really like TypeScript' }),
    newClaimId: 'new-ts',
    newEmbedding: newEmb,
    candidates: [existing],
    weightsJson: WEIGHTS_JSON,
    thresholdLower: 0.3,
    thresholdUpper: 0.85,
    nowUnixSeconds: 1_777_000_000,
    mode: 'active',
    logger: silentLogger,
  });
  assertEq(decisions, [], 'resolveWithCore: sim ≥ 0.85 (duplicate) → not a contradiction');
}

// Similarity below band (orthogonal) → no contradiction.
{
  const existing: CandidateClaim = {
    id: 'orthogonal',
    claim: makeClaim({ t: 'Something unrelated' }),
    embedding: embed([0.0, 0.0, 1.0, 0.0], 8),
  };
  const newEmb = embed([1.0, 0.0, 0.0, 0.0], 8);
  const decisions = resolveWithCore({
    newClaim: makeClaim({ t: 'Something entirely different' }),
    newClaimId: 'new-orth',
    newEmbedding: newEmb,
    candidates: [existing],
    weightsJson: WEIGHTS_JSON,
    thresholdLower: 0.3,
    thresholdUpper: 0.85,
    nowUnixSeconds: 1_777_000_000,
    mode: 'active',
    logger: silentLogger,
  });
  assertEq(decisions, [], 'resolveWithCore: sim < 0.3 (orthogonal) → not a contradiction');
}

// Candidate with empty embedding → skipped.
{
  const existing: CandidateClaim = {
    id: 'no-embed',
    claim: makeClaim({ t: 'something' }),
    embedding: [],
  };
  const decisions = resolveWithCore({
    newClaim: makeClaim({ t: 'I use VS Code' }),
    newClaimId: 'new-1',
    newEmbedding: embed([1, 0, 0, 0], 8),
    candidates: [existing],
    weightsJson: WEIGHTS_JSON,
    thresholdLower: 0.3,
    thresholdUpper: 0.85,
    nowUnixSeconds: 1_777_000_000,
    mode: 'active',
    logger: silentLogger,
  });
  assertEq(decisions, [], 'resolveWithCore: empty candidate embedding → skipped');
}

// ---------------------------------------------------------------------------
// appendDecisionLog + decisionsLogPath
// ---------------------------------------------------------------------------

{
  const tmp = setupTempStateDir('decisionlog');
  try {
    const entry: DecisionLogEntry = {
      ts: 1_777_000_000,
      entity_id: 'deadbeef12345678',
      new_claim_id: '0xnew',
      existing_claim_id: '0xold',
      similarity: 0.623,
      action: 'supersede_existing',
      reason: 'new_wins',
      winner_score: 0.812,
      loser_score: 0.45,
      mode: 'active',
    };
    await appendDecisionLog(entry);
    const content = fs.readFileSync(decisionsLogPath(), 'utf-8');
    const lines = content.trim().split('\n');
    assert(lines.length === 1, 'appendDecisionLog: writes exactly one JSONL line');
    const parsed = JSON.parse(lines[0]);
    assertEq(parsed.entity_id, 'deadbeef12345678', 'appendDecisionLog: round-trips entity_id');
    assertEq(parsed.action, 'supersede_existing', 'appendDecisionLog: round-trips action');
    assertEq(parsed.reason, 'new_wins', 'appendDecisionLog: round-trips reason');
    assertEq(parsed.mode, 'active', 'appendDecisionLog: round-trips mode');

    await appendDecisionLog({ ...entry, existing_claim_id: '0xold2' });
    const content2 = fs.readFileSync(decisionsLogPath(), 'utf-8');
    assert(
      content2.trim().split('\n').length === 2,
      'appendDecisionLog: second call appends second line',
    );

    // Slice 2f: components must round-trip when present.
    const entryWithComponents: DecisionLogEntry = {
      ...entry,
      winner_components: {
        confidence: 0.85,
        corroboration: 1.0,
        recency: 0.812,
        validation: 0.7,
        weighted_total: 0.823,
      },
      loser_components: {
        confidence: 0.6,
        corroboration: 1.73,
        recency: 0.333,
        validation: 0.7,
        weighted_total: 0.734,
      },
    };
    await appendDecisionLog(entryWithComponents);
    const content3 = fs.readFileSync(decisionsLogPath(), 'utf-8');
    const lastLine = content3.trim().split('\n').slice(-1)[0];
    const parsedWithComps = JSON.parse(lastLine);
    assert(
      typeof parsedWithComps.winner_components === 'object',
      'appendDecisionLog: winner_components round-trips',
    );
    assertEq(
      parsedWithComps.winner_components.weighted_total,
      0.823,
      'appendDecisionLog: winner weighted_total preserved',
    );
    assertEq(
      parsedWithComps.loser_components.weighted_total,
      0.734,
      'appendDecisionLog: loser weighted_total preserved',
    );
  } finally {
    cleanupTempStateDir(tmp);
  }
}

// ---------------------------------------------------------------------------
// loadWeightsFile / weightsFilePath — defaults when missing
// ---------------------------------------------------------------------------

{
  const tmp = setupTempStateDir('weightsdefault');
  try {
    const file = await loadWeightsFile(1_777_000_000);
    assert(typeof file.weights === 'object', 'loadWeightsFile: default has weights object');
    assert(file.threshold_lower === 0.3, 'loadWeightsFile: default lower threshold 0.3');
    assert(file.threshold_upper === 0.85, 'loadWeightsFile: default upper threshold 0.85');
    assert(
      typeof file.weights.confidence === 'number' && file.weights.confidence === 0.25,
      'loadWeightsFile: default confidence weight 0.25',
    );
    assert(file.weights.recency === 0.4, 'loadWeightsFile: default recency weight 0.40');
  } finally {
    cleanupTempStateDir(tmp);
  }
}

// loadWeightsFile with malformed file → falls back to defaults.
{
  const tmp = setupTempStateDir('weightsmalformed');
  try {
    fs.writeFileSync(weightsFilePath(), 'not valid json at all', 'utf-8');
    const file = await loadWeightsFile(1_777_000_000);
    assert(file.threshold_lower === 0.3, 'loadWeightsFile: malformed → falls back to defaults');
  } finally {
    cleanupTempStateDir(tmp);
  }
}

// ---------------------------------------------------------------------------
// collectCandidatesForEntities — subgraph + decrypt wiring
// ---------------------------------------------------------------------------

{
  const existingClaim = makeClaim({
    t: 'I prefer Neovim',
    c: 'pref',
  });
  const existingClaimJson = JSON.stringify(existingClaim);
  const trapdoor = computeEntityTrapdoor('editor');
  const search = fakeSubgraph({
    [trapdoor]: [
      {
        id: 'fact-abc',
        encryptedBlob: fakeEncrypt(existingClaimJson),
        encryptedEmbedding: fakeEncrypt(JSON.stringify([1.0, 0.0, 0.0])),
        isActive: true,
      },
    ],
  });
  const newClaim = makeClaim({ t: 'I use VS Code now' });
  const candidates = await collectCandidatesForEntities(
    newClaim,
    'new-id',
    '0xowner',
    'authKey',
    Buffer.alloc(32),
    { searchSubgraph: search, decryptFromHex: fakeDecrypt },
    silentLogger,
  );
  assert(candidates.length === 1, 'collectCandidates: fetches one candidate for single entity');
  assertEq(candidates[0].id, 'fact-abc', 'collectCandidates: returns subgraph id');
  assertEq(candidates[0].claim.t, 'I prefer Neovim', 'collectCandidates: decrypts claim text');
  assertEq(candidates[0].embedding.length, 3, 'collectCandidates: recovers stored embedding');
}

// Skips rows that are the same id as the new claim.
{
  const existingClaimJson = JSON.stringify(makeClaim({ t: 'I use VS Code' }));
  const trapdoor = computeEntityTrapdoor('editor');
  const search = fakeSubgraph({
    [trapdoor]: [
      { id: 'same-id', encryptedBlob: fakeEncrypt(existingClaimJson), encryptedEmbedding: null, isActive: true },
    ],
  });
  const candidates = await collectCandidatesForEntities(
    makeClaim({ t: 'I use VS Code' }),
    'same-id',
    '0xowner',
    'authKey',
    Buffer.alloc(32),
    { searchSubgraph: search, decryptFromHex: fakeDecrypt },
    silentLogger,
  );
  assertEq(candidates, [], 'collectCandidates: drops row that matches new-claim id');
}

// Skips digest / entity infra blobs and isActive=false.
{
  const digestJson = JSON.stringify({ t: 'd', c: 'dig', cf: 1, i: 10, sa: 's', ea: 'e' });
  const entityJson = JSON.stringify({ t: 'e', c: 'ent', cf: 1, i: 10, sa: 's', ea: 'e' });
  const activeJson = JSON.stringify(makeClaim({ t: 'keep me' }));
  const trapdoor = computeEntityTrapdoor('editor');
  const search = fakeSubgraph({
    [trapdoor]: [
      { id: 'digest-row', encryptedBlob: fakeEncrypt(digestJson), isActive: true },
      { id: 'entity-row', encryptedBlob: fakeEncrypt(entityJson), isActive: true },
      { id: 'tombstoned', encryptedBlob: fakeEncrypt(activeJson), isActive: false },
      { id: 'keeper', encryptedBlob: fakeEncrypt(activeJson), isActive: true },
    ],
  });
  const candidates = await collectCandidatesForEntities(
    makeClaim({ t: 'something' }),
    'new-id',
    '0xowner',
    'authKey',
    Buffer.alloc(32),
    { searchSubgraph: search, decryptFromHex: fakeDecrypt },
    silentLogger,
  );
  assert(candidates.length === 1, 'collectCandidates: filters out digest/entity/tombstoned rows');
  assertEq(candidates[0].id, 'keeper', 'collectCandidates: only the active user-facing row survives');
}

// Multi-entity dedup by id across entities.
{
  const claimJson = JSON.stringify(
    makeClaim({ t: 'shared fact', e: [{ n: 'alpha', tp: 'concept' }, { n: 'beta', tp: 'concept' }] }),
  );
  const tdAlpha = computeEntityTrapdoor('alpha');
  const tdBeta = computeEntityTrapdoor('beta');
  const search = fakeSubgraph({
    [tdAlpha]: [{ id: 'shared', encryptedBlob: fakeEncrypt(claimJson), isActive: true }],
    [tdBeta]: [{ id: 'shared', encryptedBlob: fakeEncrypt(claimJson), isActive: true }],
  });
  const newClaim = makeClaim({
    t: 'probe',
    e: [{ n: 'alpha', tp: 'concept' }, { n: 'beta', tp: 'concept' }],
  });
  const candidates = await collectCandidatesForEntities(
    newClaim,
    'new-id',
    '0xowner',
    'authKey',
    Buffer.alloc(32),
    { searchSubgraph: search, decryptFromHex: fakeDecrypt },
    silentLogger,
  );
  assert(candidates.length === 1, 'collectCandidates: dedups same id across entities');
}

// Subgraph throws → logs warn, returns [] for that entity.
{
  const cap = makeCaptureLogger();
  const failingSearch = async () => {
    throw new Error('boom');
  };
  const candidates = await collectCandidatesForEntities(
    makeClaim({ t: 'x' }),
    'new-id',
    '0xowner',
    'authKey',
    Buffer.alloc(32),
    { searchSubgraph: failingSearch, decryptFromHex: fakeDecrypt },
    cap.logger,
  );
  assertEq(candidates, [], 'collectCandidates: subgraph throw → empty list');
  assert(cap.warnings.some((w) => w.includes('boom')), 'collectCandidates: subgraph throw → warning logged');
}

// ---------------------------------------------------------------------------
// detectAndResolveContradictions — end-to-end (full pipeline, real WASM)
// ---------------------------------------------------------------------------

// Happy path: new fresh + validated claim supersedes a stale existing one.
{
  const tmp = setupTempStateDir('e2e-happy');
  const originalEnv = process.env.TOTALRECLAW_AUTO_RESOLVE_MODE;
  delete process.env.TOTALRECLAW_AUTO_RESOLVE_MODE;
  try {
    const existingClaim = makeClaim({
      t: 'I use Vim as my primary editor',
      c: 'pref',
      ea: '2025-06-01T00:00:00Z',
      sa: 'auto-extraction',
    });
    const existingEmb = embed([Math.cos(Math.PI / 4), Math.sin(Math.PI / 4), 0, 0], 8);
    const trapdoor = computeEntityTrapdoor('editor');
    const search = fakeSubgraph({
      [trapdoor]: [
        {
          id: 'existing-vim',
          encryptedBlob: fakeEncrypt(JSON.stringify(existingClaim)),
          encryptedEmbedding: fakeEncrypt(JSON.stringify(existingEmb)),
          isActive: true,
        },
      ],
    });
    const newClaim = makeClaim({
      t: 'I have switched to VS Code full-time',
      c: 'pref',
      ea: '2026-04-10T00:00:00Z',
      sa: 'totalreclaw_remember',
    });
    const newEmb = embed([1.0, 0.0, 0.0, 0.0], 8);

    const decisions = await detectAndResolveContradictions({
      newClaim,
      newClaimId: 'new-vscode',
      newEmbedding: newEmb,
      subgraphOwner: '0xowner',
      authKeyHex: 'authKey',
      encryptionKey: Buffer.alloc(32),
      deps: {
        searchSubgraph: search,
        decryptFromHex: fakeDecrypt,
        nowUnixSeconds: 1_777_000_000,
      },
      logger: silentLogger,
    });
    assert(decisions.length === 1, 'detectAndResolve: happy path → one decision');
    assert(decisions[0].action === 'supersede_existing', 'detectAndResolve: new wins → supersede_existing');
    // Decision log written.
    const log = fs.readFileSync(decisionsLogPath(), 'utf-8');
    assert(log.includes('supersede_existing'), 'detectAndResolve: writes decision log row');
    assert(log.includes('new_wins'), 'detectAndResolve: log row carries reason=new_wins');
  } finally {
    if (originalEnv !== undefined) process.env.TOTALRECLAW_AUTO_RESOLVE_MODE = originalEnv;
    cleanupTempStateDir(tmp);
  }
}

// Pinned existing → skip_new + log row with reason=existing_pinned.
{
  const tmp = setupTempStateDir('e2e-pinned');
  try {
    const pinnedClaim = { ...makeClaim({ t: 'I use Vim' }), st: 'p' };
    const existingEmb = embed([Math.cos(Math.PI / 4), Math.sin(Math.PI / 4), 0, 0], 8);
    const trapdoor = computeEntityTrapdoor('editor');
    const search = fakeSubgraph({
      [trapdoor]: [
        {
          id: 'pinned-vim',
          encryptedBlob: fakeEncrypt(JSON.stringify(pinnedClaim)),
          encryptedEmbedding: fakeEncrypt(JSON.stringify(existingEmb)),
          isActive: true,
        },
      ],
    });
    const newEmb = embed([1.0, 0.0, 0.0, 0.0], 8);
    const decisions = await detectAndResolveContradictions({
      newClaim: makeClaim({ t: 'I use VS Code now', ea: '2026-04-10T00:00:00Z' }),
      newClaimId: 'new-vscode',
      newEmbedding: newEmb,
      subgraphOwner: '0xowner',
      authKeyHex: 'authKey',
      encryptionKey: Buffer.alloc(32),
      deps: {
        searchSubgraph: search,
        decryptFromHex: fakeDecrypt,
        nowUnixSeconds: 1_777_000_000,
      },
      logger: silentLogger,
    });
    assert(decisions.length === 1, 'detectAndResolve: pinned → one decision');
    const d = decisions[0];
    assert(d.action === 'skip_new', 'detectAndResolve: pinned → skip_new');
    if (d.action === 'skip_new') {
      assertEq(d.reason, 'existing_pinned', 'detectAndResolve: pinned reason=existing_pinned');
    }
    const log = fs.readFileSync(decisionsLogPath(), 'utf-8');
    assert(log.includes('existing_pinned'), 'detectAndResolve: log row carries existing_pinned');
  } finally {
    cleanupTempStateDir(tmp);
  }
}

// mode=off → short-circuits, no subgraph query, empty decisions, no log file.
{
  const tmp = setupTempStateDir('e2e-off');
  const originalEnv = process.env.TOTALRECLAW_AUTO_RESOLVE_MODE;
  process.env.TOTALRECLAW_AUTO_RESOLVE_MODE = 'off';
  try {
    let searchCalls = 0;
    const search = (async () => {
      searchCalls++;
      return [];
    }) as unknown as Parameters<typeof detectAndResolveContradictions>[0]['deps']['searchSubgraph'];
    const decisions = await detectAndResolveContradictions({
      newClaim: makeClaim({ t: 'I use VS Code now' }),
      newClaimId: 'new-1',
      newEmbedding: embed([1, 0, 0, 0], 8),
      subgraphOwner: '0xowner',
      authKeyHex: 'authKey',
      encryptionKey: Buffer.alloc(32),
      deps: { searchSubgraph: search, decryptFromHex: fakeDecrypt, nowUnixSeconds: 1_777_000_000 },
      logger: silentLogger,
    });
    assertEq(decisions, [], 'detectAndResolve: mode=off → empty decisions');
    assert(searchCalls === 0, 'detectAndResolve: mode=off → subgraph not queried');
    assert(!fs.existsSync(decisionsLogPath()), 'detectAndResolve: mode=off → no decision log written');
  } finally {
    if (originalEnv !== undefined) process.env.TOTALRECLAW_AUTO_RESOLVE_MODE = originalEnv;
    else delete process.env.TOTALRECLAW_AUTO_RESOLVE_MODE;
    cleanupTempStateDir(tmp);
  }
}

// mode=shadow → detects + logs but returns empty (no write-path application).
{
  const tmp = setupTempStateDir('e2e-shadow');
  const originalEnv = process.env.TOTALRECLAW_AUTO_RESOLVE_MODE;
  process.env.TOTALRECLAW_AUTO_RESOLVE_MODE = 'shadow';
  try {
    const existingClaim = makeClaim({
      t: 'I use Vim as my primary editor',
      c: 'pref',
      ea: '2025-06-01T00:00:00Z',
    });
    const existingEmb = embed([Math.cos(Math.PI / 4), Math.sin(Math.PI / 4), 0, 0], 8);
    const trapdoor = computeEntityTrapdoor('editor');
    const search = fakeSubgraph({
      [trapdoor]: [
        {
          id: 'existing-vim',
          encryptedBlob: fakeEncrypt(JSON.stringify(existingClaim)),
          encryptedEmbedding: fakeEncrypt(JSON.stringify(existingEmb)),
          isActive: true,
        },
      ],
    });
    const decisions = await detectAndResolveContradictions({
      newClaim: makeClaim({
        t: 'I have switched to VS Code full-time',
        c: 'pref',
        ea: '2026-04-10T00:00:00Z',
        sa: 'totalreclaw_remember',
      }),
      newClaimId: 'new-vscode',
      newEmbedding: embed([1, 0, 0, 0], 8),
      subgraphOwner: '0xowner',
      authKeyHex: 'authKey',
      encryptionKey: Buffer.alloc(32),
      deps: { searchSubgraph: search, decryptFromHex: fakeDecrypt, nowUnixSeconds: 1_777_000_000 },
      logger: silentLogger,
    });
    assertEq(decisions, [], 'detectAndResolve: mode=shadow → empty decisions returned');
    const log = fs.readFileSync(decisionsLogPath(), 'utf-8');
    assert(log.includes('"action":"shadow"'), 'detectAndResolve: mode=shadow → log row action=shadow');
  } finally {
    if (originalEnv !== undefined) process.env.TOTALRECLAW_AUTO_RESOLVE_MODE = originalEnv;
    else delete process.env.TOTALRECLAW_AUTO_RESOLVE_MODE;
    cleanupTempStateDir(tmp);
  }
}

// Mixed: two entities, one contradiction per entity → two decisions.
{
  const tmp = setupTempStateDir('e2e-mixed');
  try {
    // One fresh existing claim on entity 'alpha' that will WIN — it's
    // stronger than the new claim on every axis (higher confidence, higher
    // corroboration, fresher, explicit validation).
    const freshExistingClaim: CanonicalClaim = {
      t: 'I prefer Neovim',
      c: 'pref',
      cf: 0.99,
      i: 10,
      cc: 5,
      sa: 'totalreclaw_remember',
      ea: '2026-04-11T00:00:00Z',
      e: [{ n: 'alpha', tp: 'concept' }],
    };
    // One stale existing claim on entity 'beta' that will LOSE.
    const staleExistingClaim = makeClaim({
      t: 'I use Emacs sometimes',
      ea: '2024-01-01T00:00:00Z',
      sa: 'auto-extraction',
      e: [{ n: 'beta', tp: 'concept' }],
    });
    const sameEmb = embed([Math.cos(Math.PI / 4), Math.sin(Math.PI / 4), 0, 0], 8);
    const tdAlpha = computeEntityTrapdoor('alpha');
    const tdBeta = computeEntityTrapdoor('beta');
    const search = fakeSubgraph({
      [tdAlpha]: [
        {
          id: 'alpha-fresh',
          encryptedBlob: fakeEncrypt(JSON.stringify(freshExistingClaim)),
          encryptedEmbedding: fakeEncrypt(JSON.stringify(sameEmb)),
          isActive: true,
        },
      ],
      [tdBeta]: [
        {
          id: 'beta-stale',
          encryptedBlob: fakeEncrypt(JSON.stringify(staleExistingClaim)),
          encryptedEmbedding: fakeEncrypt(JSON.stringify(sameEmb)),
          isActive: true,
        },
      ],
    });
    // New claim: fresh enough to beat the STALE 'beta' candidate but
    // weaker than the FRESH+corroborated 'alpha' candidate.
    const newClaim = makeClaim({
      t: 'I have switched to VS Code full-time',
      cf: 0.85,
      i: 7,
      ea: '2026-04-09T00:00:00Z',
      sa: 'auto-extraction',
      e: [
        { n: 'alpha', tp: 'concept' },
        { n: 'beta', tp: 'concept' },
      ],
    });
    const decisions = await detectAndResolveContradictions({
      newClaim,
      newClaimId: 'new-vscode',
      newEmbedding: embed([1, 0, 0, 0], 8),
      subgraphOwner: '0xowner',
      authKeyHex: 'authKey',
      encryptionKey: Buffer.alloc(32),
      deps: { searchSubgraph: search, decryptFromHex: fakeDecrypt, nowUnixSeconds: 1_777_000_000 },
      logger: silentLogger,
    });
    assert(decisions.length === 2, 'detectAndResolve: mixed → two decisions');
    const bySupersede = decisions.find((d) => d.action === 'supersede_existing');
    const bySkip = decisions.find((d) => d.action === 'skip_new');
    assert(
      bySupersede !== undefined && bySkip !== undefined,
      'detectAndResolve: mixed → one supersede + one skip',
    );
  } finally {
    cleanupTempStateDir(tmp);
  }
}

// ---------------------------------------------------------------------------
// Sanity: CONTRADICTION_CANDIDATE_CAP is a small, documented number
// ---------------------------------------------------------------------------

{
  assert(CONTRADICTION_CANDIDATE_CAP === 20, 'CONTRADICTION_CANDIDATE_CAP: documented value 20');
}

// ---------------------------------------------------------------------------
// Tie-zone guard: near-identical scoring claims are left active.
//
// Reproduces the 2026-04-14 Postgres/DuckDB false positive (discovered during
// KG QA on the VPS): two explicitly-stored, equally-recent, equally-confident
// claims about complementary tech that share an entity. The formula produces
// a supersede_existing decision with winner/loser scores differing by parts
// per million — rounding noise. The guard converts this into tie_leave_both.
// ---------------------------------------------------------------------------

{
  const tmp = setupTempStateDir('e2e-tie-zone');
  const originalEnv = process.env.TOTALRECLAW_AUTO_RESOLVE_MODE;
  delete process.env.TOTALRECLAW_AUTO_RESOLVE_MODE;
  try {
    // Existing and new: same confidence, same corroboration, same entity,
    // ea 10 seconds apart — recency decay at days-scale makes the gap tiny.
    const existingClaim = makeClaim({
      t: 'Uses PostgreSQL for the primary OLTP database',
      c: 'pref',
      cf: 1.0,
      i: 8,
      ea: '2026-04-14T17:20:00Z',
      sa: 'openclaw-plugin',
      e: [{ n: 'database', tp: 'concept' }],
    });
    const existingEmb = embed([Math.cos(Math.PI / 4), Math.sin(Math.PI / 4), 0, 0], 8);

    const trapdoor = computeEntityTrapdoor('database');
    const search = fakeSubgraph({
      [trapdoor]: [
        {
          id: 'existing-postgres',
          encryptedBlob: fakeEncrypt(JSON.stringify(existingClaim)),
          encryptedEmbedding: fakeEncrypt(JSON.stringify(existingEmb)),
          isActive: true,
        },
      ],
    });

    const newClaim = makeClaim({
      t: 'Uses DuckDB for analytics and reporting workloads',
      c: 'pref',
      cf: 1.0,
      i: 8,
      ea: '2026-04-14T17:20:10Z',
      sa: 'openclaw-plugin',
      e: [{ n: 'database', tp: 'concept' }],
    });
    const newEmb = embed([1.0, 0.0, 0.0, 0.0], 8); // cosine sim vs existing = 0.707

    const cap = makeCaptureLogger();
    const decisions = await detectAndResolveContradictions({
      newClaim,
      newClaimId: 'new-duckdb',
      newEmbedding: newEmb,
      subgraphOwner: '0xowner',
      authKeyHex: 'authKey',
      encryptionKey: Buffer.alloc(32),
      deps: {
        searchSubgraph: search,
        decryptFromHex: fakeDecrypt,
        nowUnixSeconds: Math.floor(new Date('2026-04-14T17:20:15Z').getTime() / 1000),
      },
      logger: cap.logger,
    });

    // The caller receives an EMPTY array — ties are filtered so the write path
    // does not tombstone either claim.
    assertEq(decisions, [], 'tie-zone: filtered decision list is empty (no supersede applied)');

    // The decision log still has an audit row, but with action=tie_leave_both.
    const log = fs.readFileSync(decisionsLogPath(), 'utf-8');
    assert(log.includes('"action":"tie_leave_both"'), 'tie-zone: log row action=tie_leave_both');
    assert(log.includes('"reason":"tie_below_tolerance"'), 'tie-zone: log row reason=tie_below_tolerance');
    assert(
      !log.includes('"action":"supersede_existing"'),
      'tie-zone: no supersede_existing row written',
    );

    // A human-readable info line lets operators see the tie.
    assert(
      cap.infos.some((m) => m.startsWith('Contradiction: tie') && m.includes('leaving both active')),
      'tie-zone: logger.info explains the tie',
    );

    // Sanity: the components should be carried through so the feedback loop
    // can reconstruct the scores later.
    const logRow = JSON.parse(log.trim().split('\n').pop() as string);
    assert(typeof logRow.winner_score === 'number', 'tie-zone: winner_score preserved');
    assert(typeof logRow.loser_score === 'number', 'tie-zone: loser_score preserved');
    assert(
      Math.abs(logRow.winner_score - logRow.loser_score) < TIE_ZONE_SCORE_TOLERANCE,
      'tie-zone: gap is within tolerance',
    );
    assert(
      typeof logRow.winner_components?.weighted_total === 'number',
      'tie-zone: winner_components preserved',
    );
    assert(
      typeof logRow.loser_components?.weighted_total === 'number',
      'tie-zone: loser_components preserved',
    );
  } finally {
    if (originalEnv !== undefined) process.env.TOTALRECLAW_AUTO_RESOLVE_MODE = originalEnv;
    cleanupTempStateDir(tmp);
  }
}

// Tie-zone: a LEGITIMATE wide-margin supersede still fires (regression guard).
{
  const tmp = setupTempStateDir('e2e-tie-zone-wide-margin');
  const originalEnv = process.env.TOTALRECLAW_AUTO_RESOLVE_MODE;
  delete process.env.TOTALRECLAW_AUTO_RESOLVE_MODE;
  try {
    // Stale, low-confidence existing vs fresh, high-confidence new. Wide gap.
    const existingClaim = makeClaim({
      t: 'I use Vim as my primary editor',
      c: 'pref',
      cf: 0.7,
      i: 6,
      ea: '2025-06-01T00:00:00Z', // ~10 months old
      sa: 'auto-extraction',
      e: [{ n: 'editor', tp: 'concept' }],
    });
    const existingEmb = embed([Math.cos(Math.PI / 4), Math.sin(Math.PI / 4), 0, 0], 8);
    const trapdoor = computeEntityTrapdoor('editor');
    const search = fakeSubgraph({
      [trapdoor]: [
        {
          id: 'existing-vim-old',
          encryptedBlob: fakeEncrypt(JSON.stringify(existingClaim)),
          encryptedEmbedding: fakeEncrypt(JSON.stringify(existingEmb)),
          isActive: true,
        },
      ],
    });
    const newClaim = makeClaim({
      t: 'I have switched to VS Code full-time',
      c: 'pref',
      cf: 1.0,
      i: 9,
      ea: '2026-04-14T00:00:00Z',
      sa: 'totalreclaw_remember',
      e: [{ n: 'editor', tp: 'concept' }],
    });
    const decisions = await detectAndResolveContradictions({
      newClaim,
      newClaimId: 'new-vscode',
      newEmbedding: embed([1, 0, 0, 0], 8),
      subgraphOwner: '0xowner',
      authKeyHex: 'authKey',
      encryptionKey: Buffer.alloc(32),
      deps: {
        searchSubgraph: search,
        decryptFromHex: fakeDecrypt,
        nowUnixSeconds: Math.floor(new Date('2026-04-14T00:00:05Z').getTime() / 1000),
      },
      logger: silentLogger,
    });
    assert(decisions.length === 1, 'tie-zone: wide-margin case still returns one decision');
    assert(
      decisions[0].action === 'supersede_existing',
      'tie-zone: wide-margin supersede NOT blocked by tie guard',
    );
    const log = fs.readFileSync(decisionsLogPath(), 'utf-8');
    assert(
      log.includes('"action":"supersede_existing"'),
      'tie-zone: wide-margin supersede row written',
    );
    assert(
      !log.includes('"action":"tie_leave_both"'),
      'tie-zone: wide-margin case does not write tie row',
    );
  } finally {
    if (originalEnv !== undefined) process.env.TOTALRECLAW_AUTO_RESOLVE_MODE = originalEnv;
    cleanupTempStateDir(tmp);
  }
}

// Tie-zone: TIE_ZONE_SCORE_TOLERANCE is documented at 1% (0.01).
{
  assert(TIE_ZONE_SCORE_TOLERANCE === 0.01, 'tie-zone: TIE_ZONE_SCORE_TOLERANCE documented at 0.01');
}

// ---------------------------------------------------------------------------
// Phase 2.1: loser_claim_json on supersede rows + findLoserClaimInDecisionLog
// ---------------------------------------------------------------------------

// supersede_existing rows now carry loser_claim_json with the original loser
// canonical Claim JSON, so the pin tool can recover from a tombstoned blob.
{
  const tmp = setupTempStateDir('e2e-loser-json');
  const originalEnv = process.env.TOTALRECLAW_AUTO_RESOLVE_MODE;
  delete process.env.TOTALRECLAW_AUTO_RESOLVE_MODE;
  try {
    const existingClaim = makeClaim({
      t: 'I use Vim as my primary editor for everything',
      c: 'pref',
      ea: '2025-06-01T00:00:00Z',
      sa: 'auto-extraction',
      e: [
        { n: 'editor', tp: 'concept' },
        { n: 'Vim', tp: 'tool' },
      ],
    });
    const existingEmb = embed([Math.cos(Math.PI / 4), Math.sin(Math.PI / 4), 0, 0], 8);
    const trapdoor = computeEntityTrapdoor('editor');
    const search = fakeSubgraph({
      [trapdoor]: [
        {
          id: 'existing-vim-loser',
          encryptedBlob: fakeEncrypt(JSON.stringify(existingClaim)),
          encryptedEmbedding: fakeEncrypt(JSON.stringify(existingEmb)),
          isActive: true,
        },
      ],
    });
    const newClaim = makeClaim({
      t: 'I have switched to VS Code full-time',
      c: 'pref',
      ea: '2026-04-10T00:00:00Z',
      sa: 'totalreclaw_remember',
    });

    const decisions = await detectAndResolveContradictions({
      newClaim,
      newClaimId: 'new-vscode',
      newEmbedding: embed([1, 0, 0, 0], 8),
      subgraphOwner: '0xowner',
      authKeyHex: 'authKey',
      encryptionKey: Buffer.alloc(32),
      deps: {
        searchSubgraph: search,
        decryptFromHex: fakeDecrypt,
        nowUnixSeconds: 1_777_000_000,
      },
      logger: silentLogger,
    });
    assert(decisions.length === 1, 'loser-json: produced one decision');
    assert(
      decisions[0].action === 'supersede_existing',
      'loser-json: action is supersede_existing',
    );

    const log = fs.readFileSync(decisionsLogPath(), 'utf-8');
    const lastLine = log.trim().split('\n').pop() as string;
    const row = JSON.parse(lastLine) as DecisionLogEntry;
    assert(row.action === 'supersede_existing', 'loser-json: log row is supersede');
    assert(
      typeof row.loser_claim_json === 'string' && row.loser_claim_json.length > 0,
      'loser-json: loser_claim_json field is present + non-empty',
    );

    const recoveredClaim = JSON.parse(row.loser_claim_json!) as CanonicalClaim;
    assertEq(
      recoveredClaim.t,
      'I use Vim as my primary editor for everything',
      'loser-json: recovered text matches the original loser',
    );
    assertEq(
      recoveredClaim.c,
      'pref',
      'loser-json: recovered category matches the original loser',
    );
    assert(
      Array.isArray(recoveredClaim.e) && recoveredClaim.e.length === 2,
      'loser-json: recovered entities preserved (2 entries)',
    );
    assertEq(
      recoveredClaim.e[0].n,
      'editor',
      'loser-json: first entity name preserved',
    );
    assertEq(
      recoveredClaim.e[1].n,
      'Vim',
      'loser-json: second entity name preserved',
    );
  } finally {
    if (originalEnv !== undefined) process.env.TOTALRECLAW_AUTO_RESOLVE_MODE = originalEnv;
    cleanupTempStateDir(tmp);
  }
}

// tie_leave_both rows do NOT carry loser_claim_json (no recovery needed —
// nothing got tombstoned in the first place).
{
  const tmp = setupTempStateDir('e2e-tie-no-loser-json');
  const originalEnv = process.env.TOTALRECLAW_AUTO_RESOLVE_MODE;
  delete process.env.TOTALRECLAW_AUTO_RESOLVE_MODE;
  try {
    // Reproduce the Postgres/DuckDB tie scenario from the existing tie-zone test.
    const existingClaim = makeClaim({
      t: 'Uses PostgreSQL for the primary OLTP database',
      c: 'pref',
      cf: 1.0,
      i: 8,
      ea: '2026-04-14T17:20:00Z',
      sa: 'openclaw-plugin',
      e: [{ n: 'database', tp: 'concept' }],
    });
    const existingEmb = embed([Math.cos(Math.PI / 4), Math.sin(Math.PI / 4), 0, 0], 8);
    const trapdoor = computeEntityTrapdoor('database');
    const search = fakeSubgraph({
      [trapdoor]: [
        {
          id: 'existing-postgres',
          encryptedBlob: fakeEncrypt(JSON.stringify(existingClaim)),
          encryptedEmbedding: fakeEncrypt(JSON.stringify(existingEmb)),
          isActive: true,
        },
      ],
    });
    const newClaim = makeClaim({
      t: 'Uses DuckDB for analytics workloads',
      c: 'pref',
      cf: 1.0,
      i: 8,
      ea: '2026-04-14T17:20:10Z',
      sa: 'openclaw-plugin',
      e: [{ n: 'database', tp: 'concept' }],
    });
    await detectAndResolveContradictions({
      newClaim,
      newClaimId: 'new-duckdb',
      newEmbedding: embed([1, 0, 0, 0], 8),
      subgraphOwner: '0xowner',
      authKeyHex: 'authKey',
      encryptionKey: Buffer.alloc(32),
      deps: {
        searchSubgraph: search,
        decryptFromHex: fakeDecrypt,
        nowUnixSeconds: Math.floor(new Date('2026-04-14T17:20:15Z').getTime() / 1000),
      },
      logger: silentLogger,
    });
    const log = fs.readFileSync(decisionsLogPath(), 'utf-8');
    const lastLine = log.trim().split('\n').pop() as string;
    const row = JSON.parse(lastLine) as DecisionLogEntry;
    assert(row.action === 'tie_leave_both', 'loser-json (tie): row is tie_leave_both');
    assert(
      row.loser_claim_json === undefined,
      'loser-json (tie): tie rows do NOT carry loser_claim_json',
    );
  } finally {
    if (originalEnv !== undefined) process.env.TOTALRECLAW_AUTO_RESOLVE_MODE = originalEnv;
    cleanupTempStateDir(tmp);
  }
}

// findLoserClaimInDecisionLog: returns the loser claim when a matching
// supersede row exists in decisions.jsonl.
{
  const tmp = setupTempStateDir('find-loser-happy');
  try {
    const loserText = 'I use Neovim daily';
    await appendDecisionLog({
      ts: 1_777_000_000,
      entity_id: 'editor',
      new_claim_id: 'new-vscode-id',
      existing_claim_id: 'tombstoned-neovim',
      similarity: 0.55,
      action: 'supersede_existing',
      reason: 'new_wins',
      winner_score: 0.91,
      loser_score: 0.74,
      loser_claim_json: JSON.stringify({
        t: loserText,
        c: 'pref',
        cf: 0.95,
        i: 8,
        sa: 'auto-extraction',
        ea: '2025-12-01T00:00:00Z',
        e: [{ n: 'Neovim', tp: 'tool' }],
      }),
      mode: 'active',
    });
    const recovered = findLoserClaimInDecisionLog('tombstoned-neovim');
    assert(recovered !== null, 'find-loser-happy: returns the loser_claim_json string');
    if (recovered !== null) {
      const claim = JSON.parse(recovered) as CanonicalClaim;
      assertEq(claim.t, loserText, 'find-loser-happy: recovered text matches');
      assertEq(claim.c, 'pref', 'find-loser-happy: recovered category matches');
      assert(
        Array.isArray(claim.e) && claim.e[0].n === 'Neovim',
        'find-loser-happy: recovered entities matches',
      );
    }
  } finally {
    cleanupTempStateDir(tmp);
  }
}

// findLoserClaimInDecisionLog: returns null when no matching row exists.
{
  const tmp = setupTempStateDir('find-loser-none');
  try {
    await appendDecisionLog({
      ts: 1_777_000_000,
      entity_id: 'editor',
      new_claim_id: 'new-vscode-id',
      existing_claim_id: 'different-id',
      similarity: 0.55,
      action: 'supersede_existing',
      reason: 'new_wins',
      loser_claim_json: '{"t":"other claim","c":"pref","cf":0.9,"i":7,"sa":"x","ea":"y"}',
      mode: 'active',
    });
    const recovered = findLoserClaimInDecisionLog('does-not-exist');
    assert(recovered === null, 'find-loser-none: returns null when no row matches');
  } finally {
    cleanupTempStateDir(tmp);
  }
}

// findLoserClaimInDecisionLog: returns null for tie rows, even if existing_claim_id
// matches (ties don't tombstone, so there's nothing to recover).
{
  const tmp = setupTempStateDir('find-loser-skip-tie');
  try {
    await appendDecisionLog({
      ts: 1_777_000_000,
      entity_id: 'database',
      new_claim_id: 'new-duckdb',
      existing_claim_id: 'tied-postgres',
      similarity: 0.74,
      action: 'tie_leave_both',
      reason: 'tie_below_tolerance',
      mode: 'active',
    });
    const recovered = findLoserClaimInDecisionLog('tied-postgres');
    assert(
      recovered === null,
      'find-loser-skip-tie: tie rows are not considered recoverable',
    );
  } finally {
    cleanupTempStateDir(tmp);
  }
}

// findLoserClaimInDecisionLog: returns null for pre-Phase-2.1 rows that have
// no loser_claim_json field (backwards-compat with old logs).
{
  const tmp = setupTempStateDir('find-loser-pre-2-1');
  try {
    await appendDecisionLog({
      ts: 1_777_000_000,
      entity_id: 'editor',
      new_claim_id: 'new-id',
      existing_claim_id: 'old-loser-no-json',
      similarity: 0.55,
      action: 'supersede_existing',
      reason: 'new_wins',
      // intentionally no loser_claim_json — pre-Phase-2.1 row
      mode: 'active',
    });
    const recovered = findLoserClaimInDecisionLog('old-loser-no-json');
    assert(
      recovered === null,
      'find-loser-pre-2-1: pre-Phase-2.1 rows return null (no field to recover)',
    );
  } finally {
    cleanupTempStateDir(tmp);
  }
}

// findLoserClaimInDecisionLog: when the log has multiple matching supersede
// rows for the same factId, return the MOST RECENT one (last in the file).
{
  const tmp = setupTempStateDir('find-loser-most-recent');
  try {
    await appendDecisionLog({
      ts: 1_776_000_000,
      entity_id: 'editor',
      new_claim_id: 'first-new',
      existing_claim_id: 'multi-loser',
      similarity: 0.55,
      action: 'supersede_existing',
      reason: 'new_wins',
      loser_claim_json: '{"t":"first version","c":"pref","cf":0.9,"i":7,"sa":"a","ea":"b"}',
      mode: 'active',
    });
    await appendDecisionLog({
      ts: 1_777_000_000,
      entity_id: 'editor',
      new_claim_id: 'second-new',
      existing_claim_id: 'multi-loser',
      similarity: 0.55,
      action: 'supersede_existing',
      reason: 'new_wins',
      loser_claim_json: '{"t":"second version","c":"pref","cf":0.9,"i":7,"sa":"a","ea":"b"}',
      mode: 'active',
    });
    const recovered = findLoserClaimInDecisionLog('multi-loser');
    assert(recovered !== null, 'find-loser-most-recent: returns a row');
    if (recovered !== null) {
      const claim = JSON.parse(recovered) as CanonicalClaim;
      assertEq(
        claim.t,
        'second version',
        'find-loser-most-recent: returns the most recent (last) matching row',
      );
    }
  } finally {
    cleanupTempStateDir(tmp);
  }
}

// findLoserClaimInDecisionLog: returns null when decisions.jsonl is missing.
{
  const tmp = setupTempStateDir('find-loser-no-file');
  try {
    // Don't create decisions.jsonl at all.
    const recovered = findLoserClaimInDecisionLog('any-id');
    assert(
      recovered === null,
      'find-loser-no-file: returns null when log file does not exist',
    );
  } finally {
    cleanupTempStateDir(tmp);
  }
}

// ---------------------------------------------------------------------------
// Phase 2.1: TUNING_LOOP_MIN_INTERVAL_OVERRIDE_SECONDS env var
// ---------------------------------------------------------------------------

// Default: env unset → returns the production constant (3600).
{
  const original = process.env.TOTALRECLAW_TUNING_MIN_INTERVAL_OVERRIDE_SECONDS;
  delete process.env.TOTALRECLAW_TUNING_MIN_INTERVAL_OVERRIDE_SECONDS;
  try {
    assertEq(
      getTuningLoopMinIntervalSeconds(),
      TUNING_LOOP_MIN_INTERVAL_SECONDS,
      'tuning-override: unset env returns default 3600',
    );
    assertEq(
      TUNING_LOOP_MIN_INTERVAL_SECONDS,
      3600,
      'tuning-override: default is documented at 3600',
    );
  } finally {
    if (original !== undefined) {
      process.env.TOTALRECLAW_TUNING_MIN_INTERVAL_OVERRIDE_SECONDS = original;
    }
  }
}

// Override: env set to a small number → QA short interval.
{
  const original = process.env.TOTALRECLAW_TUNING_MIN_INTERVAL_OVERRIDE_SECONDS;
  process.env.TOTALRECLAW_TUNING_MIN_INTERVAL_OVERRIDE_SECONDS = '10';
  try {
    assertEq(
      getTuningLoopMinIntervalSeconds(),
      10,
      'tuning-override: env=10 returns 10',
    );
  } finally {
    if (original !== undefined) {
      process.env.TOTALRECLAW_TUNING_MIN_INTERVAL_OVERRIDE_SECONDS = original;
    } else {
      delete process.env.TOTALRECLAW_TUNING_MIN_INTERVAL_OVERRIDE_SECONDS;
    }
  }
}

// Invalid override (NaN) → falls back to default.
{
  const original = process.env.TOTALRECLAW_TUNING_MIN_INTERVAL_OVERRIDE_SECONDS;
  process.env.TOTALRECLAW_TUNING_MIN_INTERVAL_OVERRIDE_SECONDS = 'not-a-number';
  try {
    assertEq(
      getTuningLoopMinIntervalSeconds(),
      TUNING_LOOP_MIN_INTERVAL_SECONDS,
      'tuning-override: NaN env falls back to default',
    );
  } finally {
    if (original !== undefined) {
      process.env.TOTALRECLAW_TUNING_MIN_INTERVAL_OVERRIDE_SECONDS = original;
    } else {
      delete process.env.TOTALRECLAW_TUNING_MIN_INTERVAL_OVERRIDE_SECONDS;
    }
  }
}

// Negative override → falls back to default (negative intervals would be a bug).
{
  const original = process.env.TOTALRECLAW_TUNING_MIN_INTERVAL_OVERRIDE_SECONDS;
  process.env.TOTALRECLAW_TUNING_MIN_INTERVAL_OVERRIDE_SECONDS = '-5';
  try {
    assertEq(
      getTuningLoopMinIntervalSeconds(),
      TUNING_LOOP_MIN_INTERVAL_SECONDS,
      'tuning-override: negative env falls back to default',
    );
  } finally {
    if (original !== undefined) {
      process.env.TOTALRECLAW_TUNING_MIN_INTERVAL_OVERRIDE_SECONDS = original;
    } else {
      delete process.env.TOTALRECLAW_TUNING_MIN_INTERVAL_OVERRIDE_SECONDS;
    }
  }
}

// Zero override is allowed — useful for tests that want immediate tuning.
{
  const original = process.env.TOTALRECLAW_TUNING_MIN_INTERVAL_OVERRIDE_SECONDS;
  process.env.TOTALRECLAW_TUNING_MIN_INTERVAL_OVERRIDE_SECONDS = '0';
  try {
    assertEq(
      getTuningLoopMinIntervalSeconds(),
      0,
      'tuning-override: zero env returns 0 (allowed)',
    );
  } finally {
    if (original !== undefined) {
      process.env.TOTALRECLAW_TUNING_MIN_INTERVAL_OVERRIDE_SECONDS = original;
    } else {
      delete process.env.TOTALRECLAW_TUNING_MIN_INTERVAL_OVERRIDE_SECONDS;
    }
  }
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

const total = passed + failed;
console.log(`\n# ${passed}/${total} passed`);
if (failed === 0) {
  console.log('\nALL TESTS PASSED');
  process.exit(0);
} else {
  console.log(`\n${failed} FAILURES`);
  process.exit(1);
}
