/**
 * Tests for the pure pin/unpin operation (Slice 2e-plugin).
 *
 * Mirrors MCP's tools/pin.test.ts coverage: idempotency, supersession,
 * trapdoor regeneration, legacy-blob lift, and input validation.
 *
 * Run with: npx tsx pin-unpin.test.ts
 */

import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {
  executePinOperation,
  parseBlobForPin,
  validatePinArgs,
  type PinOpDeps,
} from './pin.js';
import { buildCanonicalClaim, computeEntityTrapdoor } from './claims-helper.js';
import {
  appendDecisionLog,
  decisionsLogPath,
  feedbackLogPath,
  type DecisionLogEntry,
  type FeedbackEntry,
} from './contradiction-sync.js';
import type { SubgraphSearchFact } from './subgraph-search.js';
import type { ExtractedFact } from './extractor.js';

// Isolate the state dir so tests never touch the real ~/.totalreclaw/.
const TEST_STATE_DIR = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-pin-test-'));
process.env.TOTALRECLAW_STATE_DIR = TEST_STATE_DIR;

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
// Mock-deps builder
// ---------------------------------------------------------------------------

interface MockState {
  facts: Map<string, { blobPlain: string; hexBlob: string; fact: SubgraphSearchFact }>;
  submittedBatches: Buffer[][];
  shouldFailSubmit?: boolean;
  submitThrow?: boolean;
}

/**
 * Make a mock `PinOpDeps` over an in-memory Map.
 *
 * The fake "decrypt" is identity: `hexBlob` is the hex of the UTF-8 plaintext,
 * and `encryptBlob(plaintext)` returns hex(plaintext). This lets us assert on
 * the encrypted blob's contents without a real cipher.
 */
function makeDeps(state: MockState, overrides: Partial<PinOpDeps> = {}): PinOpDeps {
  const deps: PinOpDeps = {
    owner: '0xowner',
    sourceAgent: 'openclaw-plugin',
    fetchFactById: async (id: string) => {
      const entry = state.facts.get(id);
      return entry ? entry.fact : null;
    },
    decryptBlob: (hex: string) => {
      // Identity: hex → UTF-8. Used with plaintexts we stored as hex above.
      return Buffer.from(hex.startsWith('0x') ? hex.slice(2) : hex, 'hex').toString('utf8');
    },
    encryptBlob: (plaintext: string) => {
      return Buffer.from(plaintext, 'utf8').toString('hex');
    },
    submitBatch: async (payloads: Buffer[]) => {
      if (state.submitThrow) throw new Error('submit boom');
      state.submittedBatches.push(payloads);
      return {
        txHash: '0x' + 'a'.repeat(64),
        success: !state.shouldFailSubmit,
      };
    },
    generateIndices: async (text: string, entityNames: string[]) => {
      // Deterministic: word-like trapdoors + entity trapdoors so tests can grep.
      const wordTrapdoors = text
        .split(/\s+/)
        .filter((w) => w.length > 0)
        .map((w) => crypto.createHash('sha256').update(w.toLowerCase()).digest('hex'));
      const entityTrapdoors = entityNames.map((n) => computeEntityTrapdoor(n));
      return {
        blindIndices: [...wordTrapdoors, ...entityTrapdoors],
        encryptedEmbedding: 'deadbeef',
      };
    },
    ...overrides,
  };
  return deps;
}

/** Seed a fact in the mock state, wrapping the plaintext blob. */
function seedFact(
  state: MockState,
  id: string,
  plaintext: string,
): SubgraphSearchFact {
  const hex = Buffer.from(plaintext, 'utf8').toString('hex');
  const fact: SubgraphSearchFact = {
    id,
    encryptedBlob: hex,
    encryptedEmbedding: null,
    decayScore: '0.8',
    timestamp: '1700000000',
    isActive: true,
  };
  state.facts.set(id, { blobPlain: plaintext, hexBlob: hex, fact });
  return fact;
}

// ---------------------------------------------------------------------------
// parseBlobForPin — unit tests
// ---------------------------------------------------------------------------

{
  const canonical = JSON.stringify({
    t: 'Pedro uses Vim',
    c: 'pref',
    cf: 0.9,
    i: 8,
    sa: 'openclaw-plugin',
    ea: '2026-04-12T10:00:00.000Z',
  });
  const parsed = parseBlobForPin(canonical);
  assertEq(parsed.currentStatus, 'active', 'parse: canonical w/o st → active');
  assertEq(parsed.isLegacy, false, 'parse: canonical is not legacy');
  assertEq((parsed.claim as { t: string }).t, 'Pedro uses Vim', 'parse: text round-trip');
}

{
  const pinned = JSON.stringify({
    t: 'x', c: 'fact', cf: 0.9, i: 5, sa: 'a', ea: 'b', st: 'p',
  });
  const parsed = parseBlobForPin(pinned);
  assertEq(parsed.currentStatus, 'pinned', 'parse: canonical st=p → pinned');
}

{
  const legacy = JSON.stringify({
    text: 'legacy fact',
    metadata: { type: 'preference', importance: 0.8, source: 'auto-extraction' },
  });
  const parsed = parseBlobForPin(legacy);
  assertEq(parsed.currentStatus, 'active', 'parse: legacy blob → active default');
  assertEq(parsed.isLegacy, true, 'parse: legacy blob flagged');
  assertEq((parsed.claim as { t: string }).t, 'legacy fact', 'parse: legacy text lifted');
  assertEq((parsed.claim as { c: string }).c, 'pref', 'parse: legacy type mapped to pref');
  assertEq((parsed.claim as { i: number }).i, 8, 'parse: legacy importance 0.8 → 8');
}

{
  const parsed = parseBlobForPin('not valid json');
  assertEq(parsed.currentStatus, 'active', 'parse: raw text → active');
  assertEq(parsed.isLegacy, true, 'parse: raw text flagged legacy');
  assertEq((parsed.claim as { t: string }).t, 'not valid json', 'parse: raw text lifted into t');
}

// ---------------------------------------------------------------------------
// validatePinArgs — unit tests
// ---------------------------------------------------------------------------

{
  const v = validatePinArgs({ fact_id: 'abc-123' });
  assertEq(v.ok, true, 'validate: happy path ok');
  assertEq(v.factId, 'abc-123', 'validate: happy path factId');
}

{
  const v = validatePinArgs({ fact_id: '  trim-me  ', reason: 'because' });
  assertEq(v.ok, true, 'validate: trim ok');
  assertEq(v.factId, 'trim-me', 'validate: trims whitespace');
  assertEq(v.reason, 'because', 'validate: reason passed through');
}

{
  const v = validatePinArgs({});
  assertEq(v.ok, false, 'validate: missing fact_id → fail');
  assert(v.error.includes('fact_id'), 'validate: missing fact_id error message');
}

{
  const v = validatePinArgs({ fact_id: 42 });
  assertEq(v.ok, false, 'validate: non-string fact_id → fail');
  assert(v.error.includes('non-empty string'), 'validate: non-string error message');
}

{
  const v = validatePinArgs({ fact_id: '' });
  assertEq(v.ok, false, 'validate: empty fact_id → fail');
}

{
  const v = validatePinArgs(null);
  assertEq(v.ok, false, 'validate: null args → fail');
}

{
  const v = validatePinArgs('not an object');
  assertEq(v.ok, false, 'validate: string args → fail');
}

// ---------------------------------------------------------------------------
// executePinOperation — pin a canonical claim
// ---------------------------------------------------------------------------

async function runTests(): Promise<void> {
  // Pin a canonical active claim → success + supersession
  {
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const fact: ExtractedFact = {
      text: 'Pedro uses Vim daily',
      type: 'preference',
      importance: 8,
      action: 'ADD',
      confidence: 0.92,
      entities: [{ name: 'Pedro', type: 'person' }, { name: 'Vim', type: 'tool' }],
    };
    const canonical = buildCanonicalClaim({
      fact,
      importance: 8,
      sourceAgent: 'openclaw-plugin',
      extractedAt: '2026-04-12T10:00:00.000Z',
    });
    seedFact(state, 'old-id-1', canonical);

    const deps = makeDeps(state);
    const result = await executePinOperation('old-id-1', 'pinned', deps, 'user confirmed');

    assertEq(result.success, true, 'pin canonical: success');
    assertEq(result.fact_id, 'old-id-1', 'pin canonical: returns original id');
    assert(typeof result.new_fact_id === 'string' && result.new_fact_id.length > 0, 'pin canonical: new_fact_id set');
    assertEq(result.previous_status, 'active', 'pin canonical: previous_status active');
    assertEq(result.new_status, 'pinned', 'pin canonical: new_status pinned');
    assertEq(result.idempotent, undefined, 'pin canonical: not idempotent');
    assertEq(result.reason, 'user confirmed', 'pin canonical: reason passed through');
    assertEq(state.submittedBatches.length, 1, 'pin canonical: exactly 1 batch submitted');
    assertEq(state.submittedBatches[0].length, 2, 'pin canonical: batch has 2 payloads (tombstone + new)');
  }

  // Idempotency: pin an already-pinned claim → no on-chain write
  {
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const pinnedJson = JSON.stringify({
      t: 'Pedro uses Vim',
      c: 'pref',
      cf: 0.9,
      i: 8,
      sa: 'openclaw-plugin',
      ea: '2026-04-12T10:00:00.000Z',
      st: 'p',
    });
    seedFact(state, 'pinned-1', pinnedJson);

    const deps = makeDeps(state);
    const result = await executePinOperation('pinned-1', 'pinned', deps);

    assertEq(result.success, true, 'pin idempotent: success');
    assertEq(result.idempotent, true, 'pin idempotent: idempotent flag set');
    assertEq(result.fact_id, 'pinned-1', 'pin idempotent: fact_id unchanged');
    assertEq(result.new_fact_id, undefined, 'pin idempotent: no new_fact_id');
    assertEq(result.previous_status, 'pinned', 'pin idempotent: previous_status pinned');
    assertEq(result.new_status, 'pinned', 'pin idempotent: new_status pinned');
    assertEq(state.submittedBatches.length, 0, 'pin idempotent: zero on-chain writes');
  }

  // Unpin a pinned claim → status flipped to active, `st` omitted
  {
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const pinnedJson = JSON.stringify({
      t: 'Pedro uses Vim',
      c: 'pref',
      cf: 0.9,
      i: 8,
      sa: 'openclaw-plugin',
      ea: '2026-04-12T10:00:00.000Z',
      st: 'p',
    });
    seedFact(state, 'pinned-2', pinnedJson);

    let capturedEncryptedHex: string | null = null;
    const deps = makeDeps(state, {
      encryptBlob: (plaintext: string) => {
        capturedEncryptedHex = Buffer.from(plaintext, 'utf8').toString('hex');
        return capturedEncryptedHex;
      },
    });
    const result = await executePinOperation('pinned-2', 'active', deps);

    assertEq(result.success, true, 'unpin pinned: success');
    assertEq(result.previous_status, 'pinned', 'unpin pinned: previous_status pinned');
    assertEq(result.new_status, 'active', 'unpin pinned: new_status active');
    assertEq(result.idempotent, undefined, 'unpin pinned: not idempotent');
    assert(typeof result.new_fact_id === 'string', 'unpin pinned: new_fact_id set');
    assertEq(state.submittedBatches.length, 1, 'unpin pinned: one batch submitted');

    // v1.1 unpin: the new canonical blob is a v1 payload with
    // pin_status=unpinned and superseded_by pointing to the old fact id.
    assert(capturedEncryptedHex !== null, 'unpin pinned: encrypted blob captured');
    const canonicalPlaintext = Buffer.from(capturedEncryptedHex!, 'hex').toString('utf8');
    assert(canonicalPlaintext.includes('"schema_version":"1.0"'), 'unpin pinned: blob is v1 (schema_version 1.0)');
    assert(canonicalPlaintext.includes('"pin_status":"unpinned"'), 'unpin pinned: v1 pin_status=unpinned');
    assert(canonicalPlaintext.includes('"superseded_by":"pinned-2"'), 'unpin pinned: v1 superseded_by points to old id');
    // v0 short-key fields MUST NOT leak into a v1 blob.
    assert(!canonicalPlaintext.includes('"st":'), 'unpin pinned: no v0 st field on v1 blob');
    assert(!canonicalPlaintext.includes('"sup":"'), 'unpin pinned: no v0 sup field on v1 blob');
  }

  // Unpin a non-pinned claim → idempotent no-op
  {
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const activeJson = JSON.stringify({
      t: 'x', c: 'fact', cf: 0.9, i: 5, sa: 'a', ea: 'b',
    });
    seedFact(state, 'active-1', activeJson);

    const deps = makeDeps(state);
    const result = await executePinOperation('active-1', 'active', deps);

    assertEq(result.success, true, 'unpin active: success');
    assertEq(result.idempotent, true, 'unpin active: idempotent');
    assertEq(state.submittedBatches.length, 0, 'unpin active: zero writes');
  }

  // Pin a legacy {text, metadata} blob → successfully lifts into canonical
  {
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const legacyJson = JSON.stringify({
      text: 'Pedro lives in Lisbon',
      metadata: { type: 'fact', importance: 0.9, source: 'auto-extraction' },
    });
    seedFact(state, 'legacy-1', legacyJson);

    let capturedNewBlob: string | null = null;
    const deps = makeDeps(state, {
      encryptBlob: (plaintext: string) => {
        capturedNewBlob = plaintext;
        return Buffer.from(plaintext, 'utf8').toString('hex');
      },
    });
    const result = await executePinOperation('legacy-1', 'pinned', deps);

    assertEq(result.success, true, 'pin legacy: success');
    assertEq(result.previous_status, 'active', 'pin legacy: previous_status active (legacy default)');
    assertEq(result.new_status, 'pinned', 'pin legacy: new_status pinned');
    assert(capturedNewBlob !== null, 'pin legacy: new blob captured');
    // v1.1: legacy blob is UPGRADED to a v1 payload on the pin path.
    assert(capturedNewBlob!.includes('"text":"Pedro lives in Lisbon"'), 'pin legacy: text lifted into v1 text field');
    assert(capturedNewBlob!.includes('"schema_version":"1.0"'), 'pin legacy: output is v1 (schema_version 1.0)');
    assert(capturedNewBlob!.includes('"pin_status":"pinned"'), 'pin legacy: v1 pin_status=pinned');
    assert(capturedNewBlob!.includes('"superseded_by":"legacy-1"'), 'pin legacy: v1 superseded_by points to old id');
    // legacy v0 type "fact" upgrades to v1 type "claim" per the spec map.
    assert(capturedNewBlob!.includes('"type":"claim"'), 'pin legacy: v0 fact → v1 claim type');
  }

  // Fact not found → error
  {
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const deps = makeDeps(state);
    const result = await executePinOperation('does-not-exist', 'pinned', deps);
    assertEq(result.success, false, 'pin missing: success=false');
    assert(typeof result.error === 'string' && result.error.includes('not found'), 'pin missing: clear error message');
    assertEq(state.submittedBatches.length, 0, 'pin missing: zero writes');
  }

  // On-chain submit failure → error with previous_status preserved
  {
    const state: MockState = { facts: new Map(), submittedBatches: [], shouldFailSubmit: true };
    const canonical = JSON.stringify({
      t: 'hello', c: 'fact', cf: 0.9, i: 5, sa: 'a', ea: 'b',
    });
    seedFact(state, 'will-fail', canonical);

    const deps = makeDeps(state);
    const result = await executePinOperation('will-fail', 'pinned', deps);
    assertEq(result.success, false, 'pin submit-fail: success=false');
    assertEq(result.previous_status, 'active', 'pin submit-fail: previous_status preserved');
    assert(typeof result.error === 'string' && result.error.length > 0, 'pin submit-fail: error message set');
  }

  // Submit throws → caught and surfaced
  {
    const state: MockState = { facts: new Map(), submittedBatches: [], submitThrow: true };
    const canonical = JSON.stringify({
      t: 'hello', c: 'fact', cf: 0.9, i: 5, sa: 'a', ea: 'b',
    });
    seedFact(state, 'will-throw', canonical);

    const deps = makeDeps(state);
    const result = await executePinOperation('will-throw', 'pinned', deps);
    assertEq(result.success, false, 'pin submit-throw: success=false');
    assert(typeof result.error === 'string' && result.error.includes('submit'), 'pin submit-throw: error mentions submit');
  }

  // ── Trapdoor regeneration tests ────────────────────────────────────────────
  //
  // The new fact MUST carry blind indices so trapdoor search still surfaces it
  // after the old fact is tombstoned. Mirrors the MCP + Python regen fix.

  // Trapdoors on the new fact include SHA-256 of every word in the claim text
  {
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const fact: ExtractedFact = {
      text: 'Pedro uses Vim',
      type: 'preference',
      importance: 8,
      action: 'ADD',
      confidence: 0.92,
    };
    const canonical = buildCanonicalClaim({
      fact,
      importance: 8,
      sourceAgent: 'openclaw-plugin',
      extractedAt: '2026-04-12T10:00:00.000Z',
    });
    seedFact(state, 'trap-1', canonical);

    // Capture the raw protobuf payload bytes for the new fact.
    let capturedSecondPayload: Buffer | null = null;
    const deps = makeDeps(state, {
      submitBatch: async (payloads: Buffer[]) => {
        state.submittedBatches.push(payloads);
        capturedSecondPayload = payloads[1];
        return { txHash: '0xfeed', success: true };
      },
    });

    const result = await executePinOperation('trap-1', 'pinned', deps);
    assertEq(result.success, true, 'trapdoor: pin succeeded');
    assert(capturedSecondPayload !== null, 'trapdoor: captured new fact payload');

    // Known word trapdoor: sha256("vim") — should appear in the protobuf bytes.
    // We look for the raw 32-byte hash as a hex string inside the payload. The
    // payload encodes the indices via plugin's protobuf encoder, which stores
    // them as hex strings.
    const vimTrapdoor = crypto.createHash('sha256').update('vim').digest('hex');
    const pedroTrapdoor = crypto.createHash('sha256').update('pedro').digest('hex');
    const payloadStr = capturedSecondPayload!.toString('binary');
    assert(payloadStr.includes(vimTrapdoor), 'trapdoor: vim word trapdoor embedded in new fact');
    assert(payloadStr.includes(pedroTrapdoor), 'trapdoor: pedro word trapdoor embedded in new fact');
  }

  // Entity trapdoors are included when the claim carries entities
  {
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const fact: ExtractedFact = {
      text: 'I prefer PostgreSQL',
      type: 'preference',
      importance: 8,
      action: 'ADD',
      confidence: 0.9,
      entities: [{ name: 'PostgreSQL', type: 'tool' }],
    };
    const canonical = buildCanonicalClaim({
      fact,
      importance: 8,
      sourceAgent: 'openclaw-plugin',
      extractedAt: '2026-04-12T10:00:00.000Z',
    });
    seedFact(state, 'trap-entity-1', canonical);

    let capturedSecondPayload: Buffer | null = null;
    const deps = makeDeps(state, {
      submitBatch: async (payloads: Buffer[]) => {
        state.submittedBatches.push(payloads);
        capturedSecondPayload = payloads[1];
        return { txHash: '0xfeed', success: true };
      },
    });

    const result = await executePinOperation('trap-entity-1', 'pinned', deps);
    assertEq(result.success, true, 'entity trapdoor: pin succeeded');

    const postgresEntityTrapdoor = computeEntityTrapdoor('PostgreSQL');
    const payloadStr = capturedSecondPayload!.toString('binary');
    assert(payloadStr.includes(postgresEntityTrapdoor), 'entity trapdoor: PostgreSQL entity trapdoor embedded');
  }

  // Non-empty blind indices guard: even without entities, new fact gets word trapdoors
  {
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const canonical = JSON.stringify({
      t: 'foo bar baz',
      c: 'fact',
      cf: 0.9,
      i: 5,
      sa: 'openclaw-plugin',
      ea: '2026-04-12T10:00:00.000Z',
    });
    seedFact(state, 'trap-guard', canonical);

    let indicesCaptured: string[] | null = null;
    const deps = makeDeps(state, {
      generateIndices: async (text, entityNames) => {
        const words = text.split(/\s+/).filter((w) => w.length > 0);
        const out = words.map((w) => crypto.createHash('sha256').update(w).digest('hex'));
        indicesCaptured = out;
        return { blindIndices: out, encryptedEmbedding: 'cafe' };
      },
    });
    const result = await executePinOperation('trap-guard', 'pinned', deps);
    assertEq(result.success, true, 'trap-guard: pin succeeded');
    assert(indicesCaptured !== null && indicesCaptured!.length === 3, 'trap-guard: three word trapdoors generated');
  }

  // Defensive: if generateIndices throws, the op still succeeds with empty indices
  {
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const canonical = JSON.stringify({
      t: 'hello', c: 'fact', cf: 0.9, i: 5, sa: 'a', ea: 'b',
    });
    seedFact(state, 'trap-throws', canonical);

    const deps = makeDeps(state, {
      generateIndices: async () => {
        throw new Error('embedding offline');
      },
    });
    const result = await executePinOperation('trap-throws', 'pinned', deps);
    assertEq(result.success, true, 'trap-throws: pin still succeeded');
    assertEq(state.submittedBatches.length, 1, 'trap-throws: batch still submitted');
  }

  // Supersession link: the new canonical claim has `sup` equal to the old id
  {
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const canonical = JSON.stringify({
      t: 'hello world', c: 'fact', cf: 0.9, i: 5, sa: 'openclaw-plugin', ea: '2026-04-12T10:00:00.000Z',
    });
    seedFact(state, 'sup-link-1', canonical);

    let capturedPlaintext: string | null = null;
    const deps = makeDeps(state, {
      encryptBlob: (plaintext: string) => {
        capturedPlaintext = plaintext;
        return Buffer.from(plaintext, 'utf8').toString('hex');
      },
    });
    const result = await executePinOperation('sup-link-1', 'pinned', deps);
    assertEq(result.success, true, 'sup-link: success');
    assert(capturedPlaintext !== null, 'sup-link: plaintext captured');
    // v1.1: `sup` → `superseded_by`, `st` → `pin_status`, `ea` → `created_at`.
    assert(capturedPlaintext!.includes('"superseded_by":"sup-link-1"'), 'sup-link: v1 superseded_by set to old id');
    assert(capturedPlaintext!.includes('"pin_status":"pinned"'), 'sup-link: v1 pin_status=pinned');
    assert(capturedPlaintext!.includes('"schema_version":"1.0"'), 'sup-link: output is v1');
    // created_at must be refreshed (non-empty, different from source ea)
    const match = capturedPlaintext!.match(/"created_at":"([^"]+)"/);
    assert(match !== null && match![1] !== '2026-04-12T10:00:00.000Z', 'sup-link: created_at refreshed to a new timestamp');
  }

  // ── Slice 2f: pin → feedback.jsonl wiring ────────────────────────────────

  function sampleComponents(weighted: number) {
    return {
      confidence: 0.85,
      corroboration: 1.0,
      recency: 0.5,
      validation: 0.7,
      weighted_total: weighted,
    };
  }

  /** Reset the on-disk decisions + feedback logs between tests. */
  function clearLogs() {
    try { fs.rmSync(decisionsLogPath(), { force: true }); } catch {}
    try { fs.rmSync(feedbackLogPath(), { force: true }); } catch {}
  }

  // Pinning a loser of a prior auto-resolution → feedback row is written
  {
    clearLogs();
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const canonical = JSON.stringify({
      t: 'Pedro uses Vim',
      c: 'pref',
      cf: 0.9,
      i: 8,
      sa: 'openclaw-plugin',
      ea: '2026-04-12T10:00:00.000Z',
    });
    seedFact(state, 'vim-loser-id', canonical);

    // Seed a matching decisions.jsonl entry where vim-loser-id was tombstoned.
    const decision: DecisionLogEntry = {
      ts: 1_776_000_000,
      entity_id: 'editor',
      new_claim_id: 'vscode-winner-id',
      existing_claim_id: 'vim-loser-id',
      similarity: 0.5,
      action: 'supersede_existing',
      reason: 'new_wins',
      winner_score: 0.83,
      loser_score: 0.73,
      winner_components: sampleComponents(0.83),
      loser_components: sampleComponents(0.73),
      mode: 'active',
    };
    await appendDecisionLog(decision);

    const deps = makeDeps(state);
    const result = await executePinOperation('vim-loser-id', 'pinned', deps);
    assertEq(result.success, true, 'feedback-pin-loser: pin succeeded');

    const fbContent = fs.readFileSync(feedbackLogPath(), 'utf-8');
    const lines = fbContent.split('\n').filter((l) => l.length > 0);
    assertEq(lines.length, 1, 'feedback-pin-loser: exactly one feedback line written');
    const fb = JSON.parse(lines[0]) as FeedbackEntry;
    assertEq(fb.claim_a_id, 'vim-loser-id', 'feedback-pin-loser: claim_a = loser (now pinned)');
    assertEq(fb.claim_b_id, 'vscode-winner-id', 'feedback-pin-loser: claim_b = formula winner');
    assertEq(fb.formula_winner, 'b', 'feedback-pin-loser: formula_winner=b (the loser is a)');
    assertEq(fb.user_decision, 'pin_a', 'feedback-pin-loser: user_decision=pin_a');
    assertEq(fb.winner_components.weighted_total, 0.83, 'feedback-pin-loser: winner components preserved');
    assertEq(fb.loser_components.weighted_total, 0.73, 'feedback-pin-loser: loser components preserved');
  }

  // Voluntary pin (no matching decision row) → no feedback row written
  {
    clearLogs();
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const canonical = JSON.stringify({
      t: 'My favorite color is teal',
      c: 'pref',
      cf: 0.9,
      i: 8,
      sa: 'openclaw-plugin',
      ea: '2026-04-12T10:00:00.000Z',
    });
    seedFact(state, 'teal-id', canonical);

    // Seed a decisions.jsonl that does NOT mention teal-id.
    const decision: DecisionLogEntry = {
      ts: 1_776_000_000,
      entity_id: 'editor',
      new_claim_id: 'vscode-id',
      existing_claim_id: 'vim-id',
      similarity: 0.5,
      action: 'supersede_existing',
      reason: 'new_wins',
      winner_score: 0.83,
      loser_score: 0.73,
      winner_components: sampleComponents(0.83),
      loser_components: sampleComponents(0.73),
      mode: 'active',
    };
    await appendDecisionLog(decision);

    const deps = makeDeps(state);
    const result = await executePinOperation('teal-id', 'pinned', deps);
    assertEq(result.success, true, 'feedback-voluntary-pin: pin succeeded');
    assert(
      !fs.existsSync(feedbackLogPath()) || fs.readFileSync(feedbackLogPath(), 'utf-8').trim() === '',
      'feedback-voluntary-pin: feedback.jsonl stays empty',
    );
  }

  // Unpin a formula winner → feedback row with user_decision=pin_b
  {
    clearLogs();
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const pinnedJson = JSON.stringify({
      t: 'Pedro prefers VS Code',
      c: 'pref',
      cf: 0.9,
      i: 8,
      sa: 'openclaw-plugin',
      ea: '2026-04-12T10:00:00.000Z',
      st: 'p',
    });
    seedFact(state, 'vscode-winner-id-2', pinnedJson);

    const decision: DecisionLogEntry = {
      ts: 1_776_100_000,
      entity_id: 'editor',
      new_claim_id: 'vscode-winner-id-2',
      existing_claim_id: 'vim-tombstoned-id',
      similarity: 0.5,
      action: 'supersede_existing',
      reason: 'new_wins',
      winner_score: 0.83,
      loser_score: 0.73,
      winner_components: sampleComponents(0.83),
      loser_components: sampleComponents(0.73),
      mode: 'active',
    };
    await appendDecisionLog(decision);

    const deps = makeDeps(state);
    const result = await executePinOperation('vscode-winner-id-2', 'active', deps);
    assertEq(result.success, true, 'feedback-unpin-winner: unpin succeeded');

    const fb = JSON.parse(
      fs.readFileSync(feedbackLogPath(), 'utf-8').split('\n').filter((l) => l.length > 0)[0],
    ) as FeedbackEntry;
    assertEq(fb.user_decision, 'pin_b', 'feedback-unpin-winner: user_decision=pin_b');
    assertEq(fb.claim_b_id, 'vscode-winner-id-2', 'feedback-unpin-winner: claim_b = formula winner');
  }

  // Pre-Slice-2f decision row (no components) → no feedback row written
  {
    clearLogs();
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const canonical = JSON.stringify({
      t: 'Pedro uses Vim',
      c: 'pref',
      cf: 0.9,
      i: 8,
      sa: 'openclaw-plugin',
      ea: '2026-04-12T10:00:00.000Z',
    });
    seedFact(state, 'old-loser-id', canonical);

    // Legacy decision log row — predates winner_components/loser_components.
    const legacy: DecisionLogEntry = {
      ts: 1_776_000_000,
      entity_id: 'editor',
      new_claim_id: 'vscode-winner-id',
      existing_claim_id: 'old-loser-id',
      similarity: 0.5,
      action: 'supersede_existing',
      reason: 'new_wins',
      winner_score: 0.83,
      loser_score: 0.73,
      mode: 'active',
    };
    await appendDecisionLog(legacy);

    const deps = makeDeps(state);
    const result = await executePinOperation('old-loser-id', 'pinned', deps);
    assertEq(result.success, true, 'feedback-legacy-row: pin succeeded');
    assert(
      !fs.existsSync(feedbackLogPath()) || fs.readFileSync(feedbackLogPath(), 'utf-8').trim() === '',
      'feedback-legacy-row: legacy rows without components produce no feedback',
    );
  }

  // Idempotent pin (already pinned) → no feedback write
  {
    clearLogs();
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const pinnedJson = JSON.stringify({
      t: 'x', c: 'fact', cf: 0.9, i: 5, sa: 'a', ea: 'b', st: 'p',
    });
    seedFact(state, 'already-pinned', pinnedJson);

    // Even if there's a matching decision row, the idempotent early-exit
    // path must not write feedback — no user override actually happened.
    const decision: DecisionLogEntry = {
      ts: 1_776_000_000,
      entity_id: 'foo',
      new_claim_id: 'bar',
      existing_claim_id: 'already-pinned',
      similarity: 0.5,
      action: 'supersede_existing',
      reason: 'new_wins',
      winner_score: 0.83,
      loser_score: 0.73,
      winner_components: sampleComponents(0.83),
      loser_components: sampleComponents(0.73),
      mode: 'active',
    };
    await appendDecisionLog(decision);

    const deps = makeDeps(state);
    const result = await executePinOperation('already-pinned', 'pinned', deps);
    assertEq(result.idempotent, true, 'feedback-idempotent: idempotent flag set');
    assert(
      !fs.existsSync(feedbackLogPath()) || fs.readFileSync(feedbackLogPath(), 'utf-8').trim() === '',
      'feedback-idempotent: no feedback row on idempotent pin',
    );
  }

  // ── Phase 2.1: pin-on-tombstone recovery via decisions.jsonl ──────────────

  // Pin a tombstoned fact id: decryptBlob throws "Encrypted data too short",
  // recovery from decisions.jsonl succeeds, the pin completes normally.
  {
    clearLogs();
    const state: MockState = { facts: new Map(), submittedBatches: [] };

    // Seed the on-chain "fact" with a 1-byte tombstone blob.
    const tombstonedFact: SubgraphSearchFact = {
      id: 'tombstoned-vim',
      encryptedBlob: '00',
      encryptedEmbedding: null,
      decayScore: '0',
      timestamp: '1700000000',
      isActive: true, // subgraph still returns it by id
    };
    state.facts.set('tombstoned-vim', {
      blobPlain: '',
      hexBlob: '00',
      fact: tombstonedFact,
    });

    // Seed a matching supersede row in decisions.jsonl carrying the loser
    // canonical Claim JSON. This is what the auto-resolver writes at decision
    // time per Phase 2.1.
    const loserClaim = {
      t: 'I use Neovim as my primary editor for everything',
      c: 'pref',
      cf: 0.95,
      i: 8,
      sa: 'auto-extraction',
      ea: '2025-12-01T00:00:00Z',
      e: [
        { n: 'editor', tp: 'concept' },
        { n: 'Neovim', tp: 'tool' },
      ],
    };
    const decision: DecisionLogEntry = {
      ts: 1_777_000_000,
      entity_id: 'editor',
      new_claim_id: 'new-vscode-id',
      existing_claim_id: 'tombstoned-vim',
      similarity: 0.55,
      action: 'supersede_existing',
      reason: 'new_wins',
      winner_score: 0.91,
      loser_score: 0.74,
      winner_components: sampleComponents(0.91),
      loser_components: sampleComponents(0.74),
      loser_claim_json: JSON.stringify(loserClaim),
      mode: 'active',
    };
    await appendDecisionLog(decision);

    // Stub decryptBlob: throw on '00' (real cipher fails the same way), pass
    // through valid hex blobs.
    const recoveryInfos: string[] = [];
    const deps = makeDeps(state, {
      decryptBlob: (hex: string) => {
        if (hex === '00' || hex === '') {
          throw new Error('Encrypted data too short');
        }
        return Buffer.from(hex.startsWith('0x') ? hex.slice(2) : hex, 'hex').toString('utf8');
      },
      logger: {
        info: (m: string) => recoveryInfos.push(m),
        warn: () => undefined,
      },
    });

    const result = await executePinOperation('tombstoned-vim', 'pinned', deps, 'user override');
    assertEq(result.success, true, 'pin-tombstone: recovery path succeeds');
    assertEq(result.fact_id, 'tombstoned-vim', 'pin-tombstone: returns original tombstoned id');
    assertEq(result.previous_status, 'active', 'pin-tombstone: previous_status forced to active after recovery');
    assertEq(result.new_status, 'pinned', 'pin-tombstone: new_status is pinned');
    assert(
      typeof result.new_fact_id === 'string' && result.new_fact_id!.length > 0,
      'pin-tombstone: a fresh new_fact_id was minted',
    );
    assertEq(state.submittedBatches.length, 1, 'pin-tombstone: exactly 1 batch submitted');
    assertEq(state.submittedBatches[0].length, 2, 'pin-tombstone: batch has tombstone + new payloads');

    // Verify the recovery info log line fired so operators can audit the path.
    assert(
      recoveryInfos.some((m) => m.startsWith('pin: recovered loser claim')),
      'pin-tombstone: info log line announces recovery',
    );

    // Verify a feedback row was written — this is the whole point of Phase 2.1
    // (unblocking feedback.jsonl + the weight-tuning loop).
    const fb = fs.readFileSync(feedbackLogPath(), 'utf-8').trim();
    assert(fb.length > 0, 'pin-tombstone: feedback.jsonl is non-empty (tuning signal recorded)');
    const fbRow = JSON.parse(fb.split('\n').filter((l) => l.length > 0)[0]) as FeedbackEntry;
    assertEq(
      fbRow.claim_a_id,
      'tombstoned-vim',
      'pin-tombstone: feedback row claim_a = recovered loser id',
    );
    assertEq(
      fbRow.user_decision,
      'pin_a',
      'pin-tombstone: feedback row user_decision=pin_a',
    );
  }

  // Pin a tombstoned fact id with NO matching decisions.jsonl row → returns
  // a clear error message, does NOT silently succeed.
  {
    clearLogs();
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const tombstonedFact: SubgraphSearchFact = {
      id: 'orphan-tombstone',
      encryptedBlob: '00',
      encryptedEmbedding: null,
      decayScore: '0',
      timestamp: '1700000000',
      isActive: true,
    };
    state.facts.set('orphan-tombstone', {
      blobPlain: '',
      hexBlob: '00',
      fact: tombstonedFact,
    });

    // No appendDecisionLog call → empty log file.
    const deps = makeDeps(state, {
      decryptBlob: () => {
        throw new Error('Encrypted data too short');
      },
    });

    const result = await executePinOperation('orphan-tombstone', 'pinned', deps);
    assertEq(result.success, false, 'pin-tombstone-orphan: no recovery → success=false');
    assert(
      typeof result.error === 'string' && result.error!.includes('decisions.jsonl'),
      'pin-tombstone-orphan: error mentions decisions.jsonl recovery path',
    );
    assertEq(
      state.submittedBatches.length,
      0,
      'pin-tombstone-orphan: no on-chain submission attempted',
    );
  }

  // Non-tombstone decrypt failure (real corruption) → does NOT trigger recovery,
  // surfaces the original error.
  {
    clearLogs();
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const corruptedFact: SubgraphSearchFact = {
      id: 'corrupted-fact',
      encryptedBlob: 'cafebabedeadbeef0123456789abcdef',
      encryptedEmbedding: null,
      decayScore: '0.8',
      timestamp: '1700000000',
      isActive: true,
    };
    state.facts.set('corrupted-fact', {
      blobPlain: '',
      hexBlob: 'cafebabedeadbeef0123456789abcdef',
      fact: corruptedFact,
    });

    // Even if we seed a matching decision row, a non-tombstone-shaped decrypt
    // failure must NOT take the recovery path — that path is reserved for
    // tombstoned blobs. Real corruption is a genuine error.
    await appendDecisionLog({
      ts: 1_777_000_000,
      entity_id: 'x',
      new_claim_id: 'y',
      existing_claim_id: 'corrupted-fact',
      similarity: 0.5,
      action: 'supersede_existing',
      reason: 'new_wins',
      loser_claim_json: '{"t":"recovered","c":"pref","cf":0.9,"i":7,"sa":"a","ea":"b"}',
      mode: 'active',
    });

    const deps = makeDeps(state, {
      decryptBlob: () => {
        throw new Error('AEAD authentication failed');
      },
    });

    const result = await executePinOperation('corrupted-fact', 'pinned', deps);
    assertEq(result.success, false, 'pin-tombstone-real-corruption: success=false');
    assert(
      typeof result.error === 'string' && result.error!.includes('AEAD authentication failed'),
      'pin-tombstone-real-corruption: original decrypt error surfaced',
    );
    assert(
      typeof result.error === 'string' && !result.error!.includes('decisions.jsonl'),
      'pin-tombstone-real-corruption: error does NOT mention recovery (path not taken)',
    );
  }

  // ── v1.1 pin_status end-to-end ────────────────────────────────────────────

  // A pin on a v1.1 source blob preserves all v1 fields + flips pin_status=pinned.
  {
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const v1Claim = JSON.stringify({
      id: '01900000-0000-7000-8000-000000000099',
      text: 'prefers PostgreSQL over MongoDB for transactional workloads',
      type: 'preference',
      source: 'user',
      created_at: '2026-04-19T10:00:00.000Z',
      schema_version: '1.0',
      scope: 'work',
      volatility: 'stable',
      reasoning: 'ACID guarantees matter for OrbitLedger',
      importance: 9,
      confidence: 0.95,
    });
    seedFact(state, 'v1-source-1', v1Claim);

    let capturedBlob: string | null = null;
    const deps = makeDeps(state, {
      encryptBlob: (plaintext: string) => {
        capturedBlob = plaintext;
        return Buffer.from(plaintext, 'utf8').toString('hex');
      },
    });
    const result = await executePinOperation('v1-source-1', 'pinned', deps);

    assertEq(result.success, true, 'v1-pin: success');
    assert(capturedBlob !== null, 'v1-pin: plaintext captured');
    assert(capturedBlob!.includes('"schema_version":"1.0"'), 'v1-pin: output schema_version 1.0');
    assert(capturedBlob!.includes('"pin_status":"pinned"'), 'v1-pin: pin_status=pinned');
    assert(capturedBlob!.includes('"type":"preference"'), 'v1-pin: preserves v1 type');
    assert(capturedBlob!.includes('"source":"user"'), 'v1-pin: preserves v1 source');
    assert(capturedBlob!.includes('"scope":"work"'), 'v1-pin: preserves scope');
    assert(capturedBlob!.includes('"volatility":"stable"'), 'v1-pin: preserves volatility');
    assert(capturedBlob!.includes('"reasoning":"ACID guarantees'), 'v1-pin: preserves reasoning');
    assert(capturedBlob!.includes('"importance":9'), 'v1-pin: preserves importance');
    assert(capturedBlob!.includes('"superseded_by":"v1-source-1"'), 'v1-pin: superseded_by points to source fact');
  }

  // An unpin on a v1.1 pinned blob flips pin_status=unpinned and preserves fields.
  {
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const v1PinnedClaim = JSON.stringify({
      id: '01900000-0000-7000-8000-0000000000a0',
      text: 'always use snake_case for database column names',
      type: 'directive',
      source: 'user',
      created_at: '2026-04-19T10:00:00.000Z',
      schema_version: '1.0',
      scope: 'work',
      pin_status: 'pinned',
    });
    seedFact(state, 'v1-pinned-1', v1PinnedClaim);

    let capturedBlob: string | null = null;
    const deps = makeDeps(state, {
      encryptBlob: (plaintext: string) => {
        capturedBlob = plaintext;
        return Buffer.from(plaintext, 'utf8').toString('hex');
      },
    });
    const result = await executePinOperation('v1-pinned-1', 'active', deps);

    assertEq(result.success, true, 'v1-unpin: success');
    assertEq(result.previous_status, 'pinned', 'v1-unpin: previous_status=pinned detected via pin_status');
    assertEq(result.new_status, 'active', 'v1-unpin: new_status=active');
    assert(capturedBlob !== null, 'v1-unpin: plaintext captured');
    assert(capturedBlob!.includes('"pin_status":"unpinned"'), 'v1-unpin: pin_status=unpinned');
    assert(capturedBlob!.includes('"type":"directive"'), 'v1-unpin: preserves directive type');
    assert(capturedBlob!.includes('"superseded_by":"v1-pinned-1"'), 'v1-unpin: supersedes pinned fact');
  }

  // Idempotent pin: a v1.1 blob already pinned via pin_status is a no-op.
  {
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const v1PinnedClaim = JSON.stringify({
      id: '01900000-0000-7000-8000-0000000000a1',
      text: 'already pinned',
      type: 'claim',
      source: 'user',
      created_at: '2026-04-19T10:00:00.000Z',
      schema_version: '1.0',
      pin_status: 'pinned',
    });
    seedFact(state, 'v1-already-pinned', v1PinnedClaim);

    const deps = makeDeps(state);
    const result = await executePinOperation('v1-already-pinned', 'pinned', deps);

    assertEq(result.success, true, 'v1-idempotent: success');
    assertEq(result.idempotent, true, 'v1-idempotent: idempotent flag set');
    assertEq(state.submittedBatches.length, 0, 'v1-idempotent: zero on-chain writes');
  }

  // Cross-impl parity: plugin output v1 JSON has the SAME canonical field
  // ordering as core's validateMemoryClaimV1 produces. This is what makes the
  // cross-client pin-in-plugin / unpin-in-mcp round-trip byte-stable.
  {
    const state: MockState = { facts: new Map(), submittedBatches: [] };
    const v1Source = JSON.stringify({
      id: '01900000-0000-7000-8000-0000000000b0',
      text: 'cross-client parity test',
      type: 'claim',
      source: 'user',
      created_at: '2026-04-19T10:00:00.000Z',
      schema_version: '1.0',
    });
    seedFact(state, 'parity-src', v1Source);

    let capturedBlob: string | null = null;
    const deps = makeDeps(state, {
      encryptBlob: (plaintext: string) => {
        capturedBlob = plaintext;
        return Buffer.from(plaintext, 'utf8').toString('hex');
      },
    });
    const result = await executePinOperation('parity-src', 'pinned', deps);
    assertEq(result.success, true, 'parity: success');
    assert(capturedBlob !== null, 'parity: plaintext captured');
    const parsed = JSON.parse(capturedBlob!);
    // Required fields present.
    assert(typeof parsed.id === 'string', 'parity: id present');
    assert(typeof parsed.text === 'string', 'parity: text present');
    assert(typeof parsed.type === 'string', 'parity: type present');
    assert(typeof parsed.source === 'string', 'parity: source present');
    assert(typeof parsed.created_at === 'string', 'parity: created_at present');
    assertEq(parsed.schema_version, '1.0', 'parity: schema_version=1.0');
    assertEq(parsed.pin_status, 'pinned', 'parity: pin_status=pinned');
    assertEq(parsed.superseded_by, 'parity-src', 'parity: superseded_by points to src');
    // Ensure no v0 leak.
    assert(!Object.prototype.hasOwnProperty.call(parsed, 't'), 'parity: no v0 t field');
    assert(!Object.prototype.hasOwnProperty.call(parsed, 'c'), 'parity: no v0 c field');
    assert(!Object.prototype.hasOwnProperty.call(parsed, 'st'), 'parity: no v0 st field');
    assert(!Object.prototype.hasOwnProperty.call(parsed, 'sup'), 'parity: no v0 sup field');
  }

  // Cleanup: remove the temp state dir.
  try { fs.rmSync(TEST_STATE_DIR, { recursive: true, force: true }); } catch {}

  // ── Summary ────────────────────────────────────────────────────────────────
  console.log(`\n# ${passed}/${passed + failed} passed`);
  if (failed > 0) {
    console.log('\nSOME TESTS FAILED');
    process.exit(1);
  } else {
    console.log('\nALL TESTS PASSED');
  }
}

runTests().catch((err) => {
  console.error('FATAL:', err);
  process.exit(1);
});

export {};
