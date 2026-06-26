/**
 * Cross-impl parity test for the pin/unpin atomic batch calldata (plugin 3.2.2).
 *
 * The Python 2.2.3 refactor and the plugin 3.2.x pin path both emit pin
 * as a SINGLE ``SimpleAccount.executeBatch(tombstone_call, new_fact_call)``
 * UserOp via the shared Rust core:
 *
 *     plugin (TS) → ``@totalreclaw/core`` WASM ``encodeBatchCall``
 *                                  │
 *                                  ▼
 *                      ``totalreclaw_core::userop::encode_batch_call``
 *                                  ▲
 *                                  │
 *     python       → ``totalreclaw_core.encode_batch_call`` (PyO3)
 *
 * Because the ABI-encoding step is shared-Rust, the Python and TS paths
 * produce byte-identical calldata for byte-identical input payloads.
 * This test locks in the byte-identity by running the SAME fixed
 * pin-scenario inputs through the TS/WASM path and comparing against
 * the golden string baked into
 * ``python/tests/test_pin_batch_cross_impl_parity.py``.
 *
 * If this test fails while the Python sibling passes:
 *   - The plugin's TS protobuf helpers have drifted from Python / Rust.
 *
 * If both fail in lockstep:
 *   - The Rust core's ``encode_batch_call`` ABI output shape changed.
 *     Legitimate breaking change — bump both goldens in lockstep.
 *
 * Run with: npx tsx pin-batch-cross-impl-parity.test.ts
 */

import { createRequire } from 'node:module';

// Lazy-load WASM via createRequire so this test file runs under bare ESM
// tsx (subgraph-store.ts uses plain ``require()`` which breaks here —
// see pin.ts line 39 for the same pattern).
const requireWasm = createRequire(import.meta.url);
let _wasm: typeof import('@totalreclaw/core') | null = null;
function getWasm(): typeof import('@totalreclaw/core') {
  if (!_wasm) _wasm = requireWasm('@totalreclaw/core');
  return _wasm!;
}

const PROTOBUF_VERSION_V4 = 4;

/** Inline FactPayload shape (mirrors subgraph-store.ts). */
interface FactPayload {
  id: string;
  timestamp: string;
  owner: string;
  encryptedBlob: string;
  blindIndices: string[];
  decayScore: number;
  source: string;
  contentFp: string;
  agentId: string;
  encryptedEmbedding?: string;
  version?: number;
}

/** Mirror of ``subgraph-store.ts::encodeFactProtobuf`` — delegates to WASM
 *  core. Duplicated here so the test doesn't import subgraph-store (which
 *  uses plain ``require()`` and breaks under bare ESM tsx). Rust core
 *  output is byte-identical either way. */
function encodeFactProtobuf(fact: FactPayload): Buffer {
  const PROTOBUF_VERSION_LEGACY = 3;
  const json = JSON.stringify({
    id: fact.id,
    timestamp: fact.timestamp,
    owner: fact.owner,
    encrypted_blob_hex: fact.encryptedBlob,
    blind_indices: fact.blindIndices,
    decay_score: fact.decayScore,
    source: fact.source,
    content_fp: fact.contentFp,
    agent_id: fact.agentId,
    encrypted_embedding: fact.encryptedEmbedding || null,
    version: fact.version ?? PROTOBUF_VERSION_LEGACY,
  });
  return Buffer.from(getWasm().encodeFactProtobuf(json));
}

// ─── Mini test runner ─────────────────────────────────────────────────────────

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

function assertEqHex(actual: string, expected: string, name: string): void {
  const ok = actual.toLowerCase() === expected.toLowerCase();
  if (!ok) {
    console.log(`  actual[0..60]:   ${actual.slice(0, 60)}…`);
    console.log(`  expected[0..60]: ${expected.slice(0, 60)}…`);
    if (actual.length !== expected.length) {
      console.log(`  length mismatch: actual ${actual.length}, expected ${expected.length}`);
    }
  }
  assert(ok, name);
}

// ─── Fixed inputs — MUST match python/tests/test_pin_batch_cross_impl_parity.py ─

const OLD_FACT_ID = '01900000-0000-7000-8000-000000000001';
const NEW_FACT_ID = '01900000-0000-7000-8000-000000000002';
const OWNER = '0x0000000000000000000000000000000000001234';
const CANONICAL_TS = '2026-04-19T10:00:00.000Z';
const FIXED_ENCRYPTED_BLOB_HEX = 'c0ffee' + 'ab'.repeat(32); // 67 bytes
const FIXED_BLIND_INDICES = [
  'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', // sha256("")
  '5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9', // sha256("1")
];
const FIXED_ENCRYPTED_EMBEDDING = 'deadbeefcafe';

// Golden — must be byte-identical to Python's
// ``EXPECTED_PIN_BATCH_CALLDATA_HEX`` for the same inputs.
const EXPECTED_PIN_BATCH_CALLDATA_HEX = '47e1da2a000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000001200000000000000000000000000000000000000000000000000000000000000002000000000000000000000000c445af1d4eb9fce4e1e61fe96ea7b8febf03c5ca000000000000000000000000c445af1d4eb9fce4e1e61fe96ea7b8febf03c5ca00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000840a2430313930303030302d303030302d373030302d383030302d3030303030303030303030311218323032362d30342d31395431303a30303a30302e3030305a1a2a3078303030303030303030303030303030303030303030303030303030303030303030303030313233342209746f6d6273746f6e65310000000000000000380140030000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001300a2430313930303030302d303030302d373030302d383030302d3030303030303030303030321218323032362d30342d31395431303a30303a30302e3030305a1a2a3078303030303030303030303030303030303030303030303030303030303030303030303030313233342223c0ffeeabababababababababababababababababababababababababababababababab2a40653362306334343239386663316331343961666266346338393936666239323432376165343165343634396239333463613439353939316237383532623835352a403566656365623636666663383666333864393532373836633664363936633739633264626332333964643465393162343637323964373361323766623537653931000000000000f03f380140046a0c64656164626565666361666500000000000000000000000000000000';

// ─── Build the pin batch payloads ────────────────────────────────────────────

function buildPinBatchPayloads(): Buffer[] {
  // Tombstone at legacy protobuf v=3. Mirrors
  // ``pin.ts::executePinOperation`` line 640 and
  // ``_change_claim_status`` step 6 in the Python client.
  const tombstone: FactPayload = {
    id: OLD_FACT_ID,
    timestamp: CANONICAL_TS,
    owner: OWNER,
    encryptedBlob: Buffer.from('tombstone', 'utf8').toString('hex'),
    blindIndices: [],
    decayScore: 0,
    source: 'python_forget', // matches Python fixture
    contentFp: '',
    agentId: 'python-client',
    version: 3,
  };

  // New pinned fact at protobuf v=4 (v1 taxonomy).
  const newFact: FactPayload = {
    id: NEW_FACT_ID,
    timestamp: CANONICAL_TS,
    owner: OWNER,
    encryptedBlob: FIXED_ENCRYPTED_BLOB_HEX,
    blindIndices: FIXED_BLIND_INDICES,
    decayScore: 1.0,
    source: 'python_pin', // matches Python fixture
    contentFp: '',
    agentId: 'python-client',
    encryptedEmbedding: FIXED_ENCRYPTED_EMBEDDING,
    version: PROTOBUF_VERSION_V4,
  };

  return [encodeFactProtobuf(tombstone), encodeFactProtobuf(newFact)];
}

// ─── Tests ────────────────────────────────────────────────────────────────────

function runTests(): void {
  // 1. Batch has tombstone + new-fact in order
  const payloads = buildPinBatchPayloads();
  assert(payloads.length === 2, 'pin batch carries exactly 2 payloads');

  // 2. encodeBatchCall via WASM produces the same calldata as Python's
  //    ``encode_execute_batch_calldata_for_data_edge`` for identical inputs.
  //    This is THE cross-impl parity claim.
  const payloadsHex = payloads.map((p) => p.toString('hex'));
  const calldataBytes = getWasm().encodeBatchCall(JSON.stringify(payloadsHex));
  const calldataHex = Buffer.from(calldataBytes).toString('hex');

  // Selector check — 0x47e1da2a = executeBatch(address[],uint256[],bytes[])
  assert(
    calldataHex.slice(0, 8) === '47e1da2a',
    'pin batch calldata routes through SimpleAccount.executeBatch (selector 0x47e1da2a), not execute (0xb61d27f6)',
  );

  // Byte-match to Python golden.
  assertEqHex(
    calldataHex,
    EXPECTED_PIN_BATCH_CALLDATA_HEX,
    'pin batch calldata byte-identical to python/tests/test_pin_batch_cross_impl_parity.py::EXPECTED_PIN_BATCH_CALLDATA_HEX',
  );

  // ─── Summary ────────────────────────────────────────────────────────────────
  console.log(`\n# ${passed}/${passed + failed} passed`);
  if (failed > 0) {
    console.log('\nSOME TESTS FAILED');
    process.exit(1);
  } else {
    console.log('\nALL TESTS PASSED');
  }
}

runTests();
