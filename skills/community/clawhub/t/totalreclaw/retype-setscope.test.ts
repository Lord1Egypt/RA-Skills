/**
 * Tests for retype-setscope.ts — 3.3.1-rc.2 retype + set_scope operations.
 *
 * Covers:
 *   - validateRetypeArgs accepts / rejects well- and ill-formed inputs
 *   - validateSetScopeArgs accepts / rejects well- and ill-formed inputs
 *   - executeRetype: fetches existing, decrypts, mutates type, writes
 *     tombstone + new, returns previous/new type in result
 *   - executeSetScope: same, for scope
 *   - missing fact returns clear error
 *   - malformed blob returns clear error
 *   - submitBatch failure propagates as success=false
 *
 * Run with: npx tsx retype-setscope.test.ts
 */

import { Buffer } from 'node:buffer';

import {
  executeRetype,
  executeSetScope,
  validateRetypeArgs,
  validateSetScopeArgs,
  type RetypeSetScopeDeps,
} from './retype-setscope.js';

import {
  buildV1ClaimBlob,
  readClaimFromBlob,
  readV1Blob,
} from './claims-helper.js';

let passed = 0;
let failed = 0;

function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) {
    console.log(`ok ${n} - ${name}`);
    passed++;
  } else {
    console.log(`not ok ${n} - ${name}`);
    failed++;
  }
}

// ---------------------------------------------------------------------------
// validateRetypeArgs
// ---------------------------------------------------------------------------

{
  const r = validateRetypeArgs({ fact_id: 'abc-123', new_type: 'preference' });
  assert(r.ok === true, 'validateRetypeArgs: accepts fact_id + new_type');
  if (r.ok) assert(r.newType === 'preference', 'validateRetypeArgs: newType=preference');
}

{
  const r = validateRetypeArgs({ factId: 'abc-123', newType: 'claim' });
  assert(r.ok === true, 'validateRetypeArgs: accepts camelCase variants');
}

{
  const r = validateRetypeArgs({ fact_id: 'abc-123', new_type: 'banana' });
  assert(r.ok === false, 'validateRetypeArgs: rejects invalid type');
}

{
  const r = validateRetypeArgs({ new_type: 'claim' });
  assert(r.ok === false, 'validateRetypeArgs: rejects missing fact_id');
}

{
  const r = validateRetypeArgs({ fact_id: '', new_type: 'claim' });
  assert(r.ok === false, 'validateRetypeArgs: rejects empty fact_id');
}

{
  const r = validateRetypeArgs(null);
  assert(r.ok === false, 'validateRetypeArgs: rejects null');
}

// ---------------------------------------------------------------------------
// validateSetScopeArgs
// ---------------------------------------------------------------------------

{
  const r = validateSetScopeArgs({ fact_id: 'abc-123', new_scope: 'work' });
  assert(r.ok === true, 'validateSetScopeArgs: accepts fact_id + new_scope');
  if (r.ok) assert(r.newScope === 'work', 'validateSetScopeArgs: newScope=work');
}

{
  const r = validateSetScopeArgs({ fact_id: 'abc-123', new_scope: 'health' });
  assert(r.ok === true, 'validateSetScopeArgs: accepts health');
}

{
  const r = validateSetScopeArgs({ fact_id: 'abc-123', new_scope: 'banana' });
  assert(r.ok === false, 'validateSetScopeArgs: rejects invalid scope');
}

{
  const r = validateSetScopeArgs({ fact_id: '', new_scope: 'work' });
  assert(r.ok === false, 'validateSetScopeArgs: rejects empty fact_id');
}

// ---------------------------------------------------------------------------
// executeRetype / executeSetScope — integration-style with mock deps
// ---------------------------------------------------------------------------

function buildMockDeps(opts: {
  existingV1Blob: string;
  submitShouldFail?: boolean;
  fetchReturnsNull?: boolean;
}): RetypeSetScopeDeps & {
  _captured: { payloads: Buffer[] | null; fetchCalls: string[] };
} {
  const captured = { payloads: null as Buffer[] | null, fetchCalls: [] as string[] };
  return {
    owner: '0xowner',
    sourceAgent: 'test',
    fetchFactById: async (factId: string) => {
      captured.fetchCalls.push(factId);
      if (opts.fetchReturnsNull) return null;
      return {
        id: factId,
        encryptedBlob: '0x' + Buffer.from(opts.existingV1Blob, 'utf-8').toString('hex'),
        encryptedEmbedding: null,
        decayScore: '1000000',
        timestamp: new Date().toISOString(),
        isActive: true,
      };
    },
    decryptBlob: (hex: string) => {
      // "decrypt" = raw hex → utf-8 (mock)
      return Buffer.from(hex, 'hex').toString('utf-8');
    },
    encryptBlob: (plaintext: string) => {
      // "encrypt" = utf-8 → hex (mock)
      return Buffer.from(plaintext, 'utf-8').toString('hex');
    },
    submitBatch: async (payloads: Buffer[]) => {
      captured.payloads = payloads;
      if (opts.submitShouldFail) return { txHash: '0xfail', success: false };
      return { txHash: '0xfeedfeed', success: true };
    },
    generateIndices: async (_text: string, _entities: string[]) => ({
      blindIndices: ['test-trapdoor-1', 'test-trapdoor-2'],
      encryptedEmbedding: 'testembedding',
    }),
    _captured: captured,
  };
}

// Happy path — retype a claim to a preference
{
  const v1Blob = buildV1ClaimBlob({
    id: 'abc-123',
    text: 'I prefer PostgreSQL over MySQL',
    type: 'claim',
    source: 'user',
    createdAt: new Date().toISOString(),
    importance: 7,
    confidence: 0.9,
  });
  const deps = buildMockDeps({ existingV1Blob: v1Blob });
  const r = await executeRetype('abc-123', 'preference', deps);
  assert(r.success, 'executeRetype: success');
  assert(r.fact_id === 'abc-123', 'executeRetype: fact_id preserved');
  assert(r.new_fact_id !== undefined && r.new_fact_id !== 'abc-123', 'executeRetype: new_fact_id allocated');
  assert(r.previous_type === 'claim', 'executeRetype: previous_type captured');
  assert(r.new_type === 'preference', 'executeRetype: new_type set');
  assert(r.tx_hash === '0xfeedfeed', 'executeRetype: tx_hash propagated');
  assert(deps._captured.payloads?.length === 2, 'executeRetype: submitted 2 payloads (tombstone + new)');
}

// Happy path — set scope to work
{
  const v1Blob = buildV1ClaimBlob({
    id: 'abc-456',
    text: 'My manager is Alice',
    type: 'claim',
    source: 'user',
    createdAt: new Date().toISOString(),
    importance: 5,
    confidence: 0.9,
  });
  const deps = buildMockDeps({ existingV1Blob: v1Blob });
  const r = await executeSetScope('abc-456', 'work', deps);
  assert(r.success, 'executeSetScope: success');
  assert(r.new_scope === 'work', 'executeSetScope: new_scope set');
  // readV1Blob normalizes missing scope to 'unspecified' → that's what projectFromDecrypted reports.
  assert(r.previous_scope === 'unspecified', 'executeSetScope: previous_scope=unspecified (default when not set)');
  assert(deps._captured.payloads?.length === 2, 'executeSetScope: submitted 2 payloads');
}

// Fact not found
{
  const v1Blob = buildV1ClaimBlob({
    id: 'abc-789',
    text: 'doesnt matter',
    type: 'claim',
    source: 'user',
    createdAt: new Date().toISOString(),
  });
  const deps = buildMockDeps({ existingV1Blob: v1Blob, fetchReturnsNull: true });
  const r = await executeRetype('abc-789', 'preference', deps);
  assert(!r.success, 'executeRetype: not-found → success=false');
  assert(r.error?.includes('not found') ?? false, 'executeRetype: error mentions not-found');
}

// Submit batch fails
{
  const v1Blob = buildV1ClaimBlob({
    id: 'abc-err',
    text: 'stay here',
    type: 'claim',
    source: 'user',
    createdAt: new Date().toISOString(),
  });
  const deps = buildMockDeps({ existingV1Blob: v1Blob, submitShouldFail: true });
  const r = await executeSetScope('abc-err', 'work', deps);
  assert(!r.success, 'executeSetScope: submit-fails → success=false');
  assert(r.tx_hash === '0xfail', 'executeSetScope: failed tx hash surfaced');
}

// Invalid new_type
{
  const v1Blob = buildV1ClaimBlob({
    id: 'abc-1',
    text: 'x',
    type: 'claim',
    source: 'user',
    createdAt: new Date().toISOString(),
  });
  const deps = buildMockDeps({ existingV1Blob: v1Blob });
  const r = await executeRetype('abc-1', 'bogus' as unknown as 'claim', deps);
  assert(!r.success, 'executeRetype: invalid type → error');
}

// Invalid new_scope
{
  const v1Blob = buildV1ClaimBlob({
    id: 'abc-2',
    text: 'x',
    type: 'claim',
    source: 'user',
    createdAt: new Date().toISOString(),
  });
  const deps = buildMockDeps({ existingV1Blob: v1Blob });
  const r = await executeSetScope('abc-2', 'bogus' as unknown as 'work', deps);
  assert(!r.success, 'executeSetScope: invalid scope → error');
}

// Malformed blob (not parseable)
{
  const deps = buildMockDeps({ existingV1Blob: 'not json at all' });
  const r = await executeRetype('abc-mal', 'preference', deps);
  assert(!r.success, 'executeRetype: malformed blob → success=false');
  assert(r.error?.toLowerCase().includes('blob') ?? false, 'executeRetype: error mentions blob');
}

// ---------------------------------------------------------------------------
// Issue #117 regression — set_scope writer/reader round-trip
//
// The original tests above only check that 2 payloads were submitted; they
// don't actually decode the *new* fact's blob and verify the export reader
// (`readClaimFromBlob`) can extract the new scope. Without this assertion,
// any future bug that drops the scope on the rewrite path or breaks the
// reader's v1 detection would silently pass the existing tests.
//
// The QA report for issue #117 was:
//   "agent reports set_scope success but export shows scope=unspecified"
//
// We lock down the contract: after set_scope, the export reader (which
// powers totalreclaw_export) MUST surface the new scope, not 'unspecified'.
// Covers v1-with-scope, v1-without-scope, v0-legacy, and pinned-fact paths.
// ---------------------------------------------------------------------------

function decodePayload(payload: Buffer): string {
  // Mock encryptBlob produces utf-8 → hex via Buffer; the protobuf encoder
  // wraps the bytes in field 4 (encrypted_blob, length-delimited). Recover
  // the inner JSON by scanning for the leading `{` and reading until `}`.
  // This avoids re-implementing the protobuf decoder here while still
  // exercising the real production write path.
  const bytes = payload.toString('binary');
  const start = bytes.indexOf('{');
  if (start === -1) return '';
  const end = bytes.lastIndexOf('}');
  if (end === -1 || end < start) return '';
  return bytes.substring(start, end + 1);
}

// Issue #117 R1: v1 blob with no scope → set_scope('health') →
// export reader sees scope='health'.
{
  const v1Blob = buildV1ClaimBlob({
    id: 'rt-1',
    text: 'I run every morning',
    type: 'commitment',
    source: 'user-inferred',
    createdAt: new Date().toISOString(),
    importance: 7,
    confidence: 0.85,
  });
  const deps = buildMockDeps({ existingV1Blob: v1Blob });
  const r = await executeSetScope('rt-1', 'health', deps);
  assert(r.success, 'issue#117 R1: set_scope success');

  // The new (second) payload contains the new blob. Decode and verify with
  // the SAME reader the export tool uses (`readClaimFromBlob`).
  const newPayload = deps._captured.payloads?.[1];
  assert(newPayload !== undefined, 'issue#117 R1: new payload present');
  const newBlob = decodePayload(newPayload!);
  const exportView = readClaimFromBlob(newBlob);
  assert(
    exportView.metadata.scope === 'health',
    `issue#117 R1: export reader sees scope=health (got: ${exportView.metadata.scope})`,
  );
  assert(
    exportView.metadata.type === 'commitment',
    'issue#117 R1: export reader preserves type',
  );
}

// Issue #117 R2: v1 blob with scope='work' → set_scope('personal') →
// export reader sees scope='personal' (not 'work', not 'unspecified').
{
  const v1Blob = buildV1ClaimBlob({
    id: 'rt-2',
    text: 'I report to Alice',
    type: 'claim',
    source: 'user',
    scope: 'work',
    createdAt: new Date().toISOString(),
    importance: 8,
    confidence: 0.9,
  });
  const deps = buildMockDeps({ existingV1Blob: v1Blob });
  const r = await executeSetScope('rt-2', 'personal', deps);
  assert(r.success, 'issue#117 R2: set_scope success');
  assert(r.previous_scope === 'work', 'issue#117 R2: previous_scope=work surfaced');

  const newPayload = deps._captured.payloads?.[1];
  const newBlob = decodePayload(newPayload!);
  const exportView = readClaimFromBlob(newBlob);
  assert(
    exportView.metadata.scope === 'personal',
    `issue#117 R2: export reader sees scope=personal (got: ${exportView.metadata.scope})`,
  );
}

// Issue #117 R3: v0 legacy blob (short-key) → set_scope('finance') →
// the upgrade path produces a v1 blob with scope='finance' surfaced
// by the export reader.
{
  const v0Blob = JSON.stringify({
    t: 'My budget is $100/week',
    c: 'fact',
    cf: 0.85,
    i: 6,
    sa: 'openclaw-plugin',
    ea: new Date().toISOString(),
  });
  const deps = buildMockDeps({ existingV1Blob: v0Blob });
  const r = await executeSetScope('rt-3', 'finance', deps);
  assert(r.success, 'issue#117 R3: set_scope on v0 blob succeeds');

  const newPayload = deps._captured.payloads?.[1];
  const newBlob = decodePayload(newPayload!);
  const exportView = readClaimFromBlob(newBlob);
  assert(
    exportView.metadata.scope === 'finance',
    `issue#117 R3: export reader sees scope=finance after v0→v1 upgrade (got: ${exportView.metadata.scope})`,
  );
  assert(
    exportView.metadata.schema_version === '1.0',
    'issue#117 R3: upgraded blob carries schema_version',
  );
}

// Issue #117 R4: pin_status preservation — set_scope on a PINNED fact
// MUST preserve pin_status='pinned'. Without this, a pinned fact silently
// loses its immunity to auto-supersede after a metadata edit. Found while
// investigating #117 in the same write path as the reported scope bug.
{
  const pinnedBlob = buildV1ClaimBlob({
    id: 'rt-4',
    text: 'I prefer PostgreSQL',
    type: 'preference',
    source: 'user',
    scope: 'work',
    createdAt: new Date().toISOString(),
    importance: 9,
    confidence: 0.95,
    pinStatus: 'pinned',
  });
  const deps = buildMockDeps({ existingV1Blob: pinnedBlob });
  const r = await executeSetScope('rt-4', 'health', deps);
  assert(r.success, 'issue#117 R4: set_scope on pinned fact succeeds');

  const newPayload = deps._captured.payloads?.[1];
  const newBlob = decodePayload(newPayload!);
  const v1View = readV1Blob(newBlob);
  assert(v1View !== null, 'issue#117 R4: new blob is a valid v1 blob');
  assert(
    v1View!.scope === 'health',
    `issue#117 R4: scope=health (got: ${v1View!.scope})`,
  );
  assert(
    v1View!.pinStatus === 'pinned',
    `issue#117 R4: pin_status='pinned' preserved across set_scope (got: ${v1View!.pinStatus})`,
  );
}

// Issue #117 R5: same pin_status preservation contract for retype.
{
  const pinnedBlob = buildV1ClaimBlob({
    id: 'rt-5',
    text: 'Always run lint before commit',
    type: 'directive',
    source: 'user',
    createdAt: new Date().toISOString(),
    importance: 9,
    pinStatus: 'pinned',
  });
  const deps = buildMockDeps({ existingV1Blob: pinnedBlob });
  const r = await executeRetype('rt-5', 'commitment', deps);
  assert(r.success, 'issue#117 R5: retype on pinned fact succeeds');

  const newPayload = deps._captured.payloads?.[1];
  const newBlob = decodePayload(newPayload!);
  const v1View = readV1Blob(newBlob);
  assert(v1View !== null, 'issue#117 R5: new blob is a valid v1 blob');
  assert(
    v1View!.type === 'commitment',
    `issue#117 R5: type=commitment (got: ${v1View!.type})`,
  );
  assert(
    v1View!.pinStatus === 'pinned',
    `issue#117 R5: pin_status='pinned' preserved across retype (got: ${v1View!.pinStatus})`,
  );
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
