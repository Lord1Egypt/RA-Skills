/**
 * embedding-model-id.test.ts — regression for the per-claim
 * `embedding_model_id` forward-compat tag (3.3.1-rc.22+).
 *
 * Failure mode this guards against:
 *   On the rc.21 baseline, `BuildClaimV1Input` has no `embeddingModelId`
 *   field — claims are written without any embedder identity tag, which
 *   means a future model distillation has no way to scope a re-embed
 *   pass per claim. `getEmbeddingModelId()` does not exist either; the
 *   import below fails. This test passes only on rc.22+.
 *
 * Coverage:
 *   1. `getEmbeddingModelId()` returns the locked v1 Harrier id
 *      (`harrier-oss-270m-q4`).
 *   2. `buildCanonicalClaimV1` re-attaches the field to the canonical
 *      JSON output when supplied.
 *   3. `buildV1ClaimBlob` re-attaches the field on the pin / retype path.
 *   4. Field is OMITTED when the input doesn't supply it (additive contract).
 *   5. `readV1Blob` round-trips the field back into the parsed result.
 *
 * Run with: `npx tsx embedding-model-id.test.ts`
 */

import { getEmbeddingModelId } from './embedding.js';
import {
  buildCanonicalClaimV1,
  buildV1ClaimBlob,
  readV1Blob,
} from './claims-helper.js';
import type { ExtractedFact } from './extractor.js';

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
// 1. getEmbeddingModelId returns the locked Harrier id
// ---------------------------------------------------------------------------
{
  console.log('# getEmbeddingModelId surface');
  const id = getEmbeddingModelId();
  assert(id === 'harrier-oss-270m-q4', `model id is harrier-oss-270m-q4 (got: ${id})`);
}

// ---------------------------------------------------------------------------
// 2. buildCanonicalClaimV1 stamps the field on output
// ---------------------------------------------------------------------------
{
  console.log('# buildCanonicalClaimV1 stamps embedding_model_id');
  const fact: ExtractedFact = {
    text: 'User prefers cold brew over espresso',
    type: 'preference',
    importance: 7,
    confidence: 0.9,
    source: 'user',
    entities: [],
  };
  const blob = buildCanonicalClaimV1({
    fact,
    importance: 7,
    embeddingModelId: 'harrier-oss-270m-q4',
  });
  const parsed = JSON.parse(blob) as Record<string, unknown>;
  assert(
    parsed.embedding_model_id === 'harrier-oss-270m-q4',
    'embedding_model_id appears at the top level',
  );
  assert(parsed.schema_version === '1.0', 'schema_version still emitted (no regression)');
  assert(typeof parsed.id === 'string', 'id field still emitted');
}

// ---------------------------------------------------------------------------
// 3. buildV1ClaimBlob (pin / retype path) stamps the field
// ---------------------------------------------------------------------------
{
  console.log('# buildV1ClaimBlob stamps embedding_model_id (pin / retype path)');
  const blob = buildV1ClaimBlob({
    text: 'User prefers cold brew over espresso',
    type: 'preference',
    source: 'user',
    importance: 7,
    confidence: 0.9,
    embeddingModelId: 'harrier-oss-270m-q4',
  });
  const parsed = JSON.parse(blob) as Record<string, unknown>;
  assert(
    parsed.embedding_model_id === 'harrier-oss-270m-q4',
    'embedding_model_id appears on the pin/retype output',
  );
}

// ---------------------------------------------------------------------------
// 4. Field is OMITTED when caller does not supply it (additive contract)
// ---------------------------------------------------------------------------
{
  console.log('# embedding_model_id is omitted when caller does not supply it');
  const blobA = buildV1ClaimBlob({
    text: 'User prefers cold brew over espresso',
    type: 'preference',
    source: 'user',
  });
  const parsedA = JSON.parse(blobA) as Record<string, unknown>;
  assert(
    !('embedding_model_id' in parsedA),
    'unsupplied embeddingModelId leaves the field absent (legacy parity)',
  );

  const fact: ExtractedFact = {
    text: 'User prefers cold brew over espresso',
    type: 'preference',
    importance: 7,
    confidence: 0.9,
    source: 'user',
    entities: [],
  };
  const blobB = buildCanonicalClaimV1({ fact, importance: 7 });
  const parsedB = JSON.parse(blobB) as Record<string, unknown>;
  assert(
    !('embedding_model_id' in parsedB),
    'buildCanonicalClaimV1 omits the field when input is undefined',
  );

  // Empty string is treated as absent (defensive).
  const blobC = buildV1ClaimBlob({
    text: 'User prefers cold brew over espresso',
    type: 'preference',
    source: 'user',
    embeddingModelId: '',
  });
  const parsedC = JSON.parse(blobC) as Record<string, unknown>;
  assert(
    !('embedding_model_id' in parsedC),
    'empty string is treated as absent',
  );
}

// ---------------------------------------------------------------------------
// 5. readV1Blob round-trips embedding_model_id
// ---------------------------------------------------------------------------
{
  console.log('# readV1Blob round-trips embedding_model_id');
  const blob = buildV1ClaimBlob({
    text: 'User prefers cold brew over espresso',
    type: 'preference',
    source: 'user',
    importance: 7,
    confidence: 0.9,
    embeddingModelId: 'harrier-oss-270m-q4',
  });
  const parsed = readV1Blob(blob);
  assert(parsed !== null, 'readV1Blob returns a parsed object');
  assert(parsed?.embeddingModelId === 'harrier-oss-270m-q4', 'embeddingModelId echoes through readV1Blob');

  // Legacy (rc.21-shape) blob: no embedding_model_id → readV1Blob returns
  // the parsed object with the field undefined.
  const legacy = buildV1ClaimBlob({
    text: 'old claim, no embedder tag',
    type: 'claim',
    source: 'user',
  });
  const legacyParsed = readV1Blob(legacy);
  assert(legacyParsed?.embeddingModelId === undefined, 'legacy blob → embeddingModelId is undefined');
}

console.log(`\n${passed}/${passed + failed} passed`);
if (failed > 0) process.exit(1);
