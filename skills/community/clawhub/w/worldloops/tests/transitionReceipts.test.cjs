'use strict';

const os = require('os');
const fs = require('fs');
const path = require('path');

// Use a temp dir so tests never touch the real .worldloops/
const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-receipts-test-'));
process.env.WORLDLOOPS_DIR = tmpDir;

const {
  loadTransitionReceipts,
  saveTransitionReceipt,
  saveTransitionReceipts,
  buildTransitionReceipt,
  getTransitionReceiptsPath,
} = require('../dist/storage/transitionReceipts.js');

let passed = 0;
let failed = 0;

function assert(condition, label) {
  if (condition) {
    passed++;
    console.log(`  PASS  ${label}`);
  } else {
    failed++;
    console.error(`  FAIL  ${label}`);
  }
}

console.log('\ntransitionReceipts unit tests\n');

// --- loadTransitionReceipts: returns empty array when file missing ---

const receipts0 = loadTransitionReceipts();
assert(Array.isArray(receipts0), 'loadTransitionReceipts: returns array when file missing');
assert(receipts0.length === 0, 'loadTransitionReceipts: empty when file missing');

// --- buildTransitionReceipt: constructs correct shape ---

const mockCandidate = {
  idempotencyKey: 'loop-email-abc',
  entityType: 'email_thread',
  source: 'gmail',
  currentState: 'awaiting_reply',
  proposedState: 'acknowledged',
  reason: 'Follow-up email unanswered.',
  approvalRequired: true,
  actionHint: 'Reply to confirm receipt.',
};

const mockSignals = [
  { source: 'gmail', text: 'Just checking if you had a chance to review.', createdAt: '2026-05-18T09:00:00.000Z' },
  { source: 'calendar', text: 'Team sync tomorrow — no agenda set.', createdAt: '2026-05-18T08:00:00.000Z' },
];

const receipt = buildTransitionReceipt(mockCandidate, mockSignals, {
  adjudicationResult: 'proposed',
  decision: 'surfaced_for_review',
  boundaryCrossed: 'local_commit',
});

assert(typeof receipt.id === 'string' && receipt.id.length > 0, 'buildTransitionReceipt: id is non-empty string');
assert(receipt.id.startsWith('loop-email-abc-'), 'buildTransitionReceipt: id starts with proposalId');
assert(typeof receipt.createdAt === 'string', 'buildTransitionReceipt: createdAt is string');
assert(receipt.proposalId === 'loop-email-abc', 'buildTransitionReceipt: proposalId matches idempotencyKey');
assert(Array.isArray(receipt.sourceSignalsObserved), 'buildTransitionReceipt: sourceSignalsObserved is array');
assert(receipt.sourceSignalsObserved.length === 2, 'buildTransitionReceipt: captures all source signals');
assert(receipt.sourceSignalsObserved[0].includes('[gmail]'), 'buildTransitionReceipt: signal includes source tag');
assert(receipt.normalizedResponsibility === 'email_thread', 'buildTransitionReceipt: normalizedResponsibility = entityType');
assert(receipt.proposedTransition !== null, 'buildTransitionReceipt: proposedTransition is not null');
assert(receipt.proposedTransition.currentState === 'awaiting_reply', 'buildTransitionReceipt: currentState correct');
assert(receipt.proposedTransition.proposedState === 'acknowledged', 'buildTransitionReceipt: proposedState correct');
assert(receipt.reason === 'Follow-up email unanswered.', 'buildTransitionReceipt: reason is set');
assert(receipt.adjudicationResult === 'proposed', 'buildTransitionReceipt: adjudicationResult is set');
assert(receipt.boundaryCrossed === 'local_commit', 'buildTransitionReceipt: boundaryCrossed is local_commit');

// --- externalWrite is always false ---
assert(receipt.externalWrite === false, 'buildTransitionReceipt: externalWrite is false');

assert(receipt.actor === null, 'buildTransitionReceipt: actor is null');
assert(receipt.decision === 'surfaced_for_review', 'buildTransitionReceipt: decision is set');
assert(receipt.unresolvedState === null, 'buildTransitionReceipt: unresolvedState is null');
assert(typeof receipt.redactions === 'object', 'buildTransitionReceipt: redactions is object');
assert(receipt.redactions.applied === false, 'buildTransitionReceipt: redactions.applied is false');
assert(Array.isArray(receipt.redactions.fields), 'buildTransitionReceipt: redactions.fields is array');

// --- saveTransitionReceipt and loadTransitionReceipts roundtrip ---

saveTransitionReceipt(receipt);
assert(
  fs.existsSync(getTransitionReceiptsPath()),
  'saveTransitionReceipt: transition_receipts.json created'
);

const loaded = loadTransitionReceipts();
assert(loaded.length === 1, 'loadTransitionReceipts: reads 1 persisted receipt');
assert(loaded[0].proposalId === 'loop-email-abc', 'loadTransitionReceipts: proposalId roundtrips');
assert(loaded[0].externalWrite === false, 'loadTransitionReceipts: externalWrite is false after roundtrip');
assert(loaded[0].boundaryCrossed === 'local_commit', 'loadTransitionReceipts: boundaryCrossed roundtrips');

// --- upsert: saving same id overwrites ---

const updatedReceipt = { ...receipt, decision: 'updated_decision' };
saveTransitionReceipt(updatedReceipt);
const afterUpsert = loadTransitionReceipts();
assert(afterUpsert.length === 1, 'saveTransitionReceipt: upsert does not duplicate');
assert(afterUpsert[0].decision === 'updated_decision', 'saveTransitionReceipt: upsert updates existing');

// --- saveTransitionReceipts: batch write ---

const receipt2 = buildTransitionReceipt(
  { ...mockCandidate, idempotencyKey: 'loop-calendar-xyz' },
  mockSignals,
  { adjudicationResult: 'proposed', decision: 'surfaced_for_review', boundaryCrossed: 'read_only' }
);

saveTransitionReceipts([receipt, receipt2]);
const afterBatch = loadTransitionReceipts();
assert(afterBatch.length === 2, 'saveTransitionReceipts: batch write stores 2 receipts');
assert(
  afterBatch.every((r) => r.externalWrite === false),
  'saveTransitionReceipts: all receipts have externalWrite:false'
);
assert(
  afterBatch.some((r) => r.boundaryCrossed === 'read_only'),
  'saveTransitionReceipts: boundaryCrossed=read_only roundtrips'
);

// --- summary ---
console.log(`\n  ${passed} passed, ${failed} failed\n`);

if (failed > 0) {
  process.exit(1);
}
