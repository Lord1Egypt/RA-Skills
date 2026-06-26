const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync, spawnSync } = require('node:child_process');

function mkTmp(prefix) {
  return fs.mkdtempSync(path.join(os.tmpdir(), `worldloops-proposal-decide-${prefix}-`));
}

function createProposal(dir, templateId) {
  const result = execFileSync(
    process.execPath,
    ['dist/scripts/proposalCreate.js', templateId, '--json'],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
  return JSON.parse(result).proposal;
}

function decide(dir, proposalId, decisionArgs) {
  return spawnSync(
    process.execPath,
    ['dist/scripts/proposalDecide.js', proposalId, ...decisionArgs, '--json'],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
}

// ── approve a proposed proposal ───────────────────────────────────────────────

const dirApprove = mkTmp('approve');
const pApprove = createProposal(dirApprove, 'file-write');

const approveResult = decide(dirApprove, pApprove.id, ['approve']);
assert.strictEqual(approveResult.status, 0, 'approve should succeed');
const approveJson = JSON.parse(approveResult.stdout);
assert.strictEqual(approveJson.ok, true);
assert.strictEqual(approveJson.previousStatus, 'proposed');
assert.strictEqual(approveJson.newStatus, 'approved');
assert.strictEqual(approveJson.decision, 'approve');
assert.ok(approveJson.receiptId, 'should have receiptId');
assert.strictEqual(approveJson.safety.externalWrite, false);

// proposal status updated on disk
const approvedProposals = JSON.parse(fs.readFileSync(path.join(dirApprove, 'proposals.json'), 'utf8'));
assert.strictEqual(approvedProposals[0].status, 'approved');

// receipt file created
const approveReceipts = JSON.parse(fs.readFileSync(path.join(dirApprove, 'proposal_decision_receipts.json'), 'utf8'));
assert.strictEqual(approveReceipts.length, 1);
assert.strictEqual(approveReceipts[0].proposalId, pApprove.id);
assert.strictEqual(approveReceipts[0].decision, 'approve');
assert.strictEqual(approveReceipts[0].previousStatus, 'proposed');
assert.strictEqual(approveReceipts[0].newStatus, 'approved');
assert.strictEqual(approveReceipts[0].externalWrite, false);

// ── reject a proposed proposal ────────────────────────────────────────────────

const dirReject = mkTmp('reject');
const pReject = createProposal(dirReject, 'api-call');

const rejectResult = decide(dirReject, pReject.id, ['reject']);
assert.strictEqual(rejectResult.status, 0, 'reject should succeed');
const rejectJson = JSON.parse(rejectResult.stdout);
assert.strictEqual(rejectJson.ok, true);
assert.strictEqual(rejectJson.previousStatus, 'proposed');
assert.strictEqual(rejectJson.newStatus, 'rejected');
assert.strictEqual(rejectJson.safety.externalWrite, false);

const rejectedProposals = JSON.parse(fs.readFileSync(path.join(dirReject, 'proposals.json'), 'utf8'));
assert.strictEqual(rejectedProposals[0].status, 'rejected');

// ── snooze a proposed proposal ────────────────────────────────────────────────

const dirSnooze = mkTmp('snooze');
const pSnooze = createProposal(dirSnooze, 'state-transition');

const snoozeResult = decide(dirSnooze, pSnooze.id, ['snooze']);
assert.strictEqual(snoozeResult.status, 0, 'snooze should succeed');
const snoozeJson = JSON.parse(snoozeResult.stdout);
assert.strictEqual(snoozeJson.ok, true);
assert.strictEqual(snoozeJson.previousStatus, 'proposed');
assert.strictEqual(snoozeJson.newStatus, 'snoozed');
assert.strictEqual(snoozeJson.safety.externalWrite, false);

// ── escalate a proposed proposal ──────────────────────────────────────────────

const dirEscalate = mkTmp('escalate');
const pEscalate = createProposal(dirEscalate, 'escalation');

const escalateResult = decide(dirEscalate, pEscalate.id, ['escalate']);
assert.strictEqual(escalateResult.status, 0, 'escalate should succeed');
const escalateJson = JSON.parse(escalateResult.stdout);
assert.strictEqual(escalateJson.ok, true);
assert.strictEqual(escalateJson.previousStatus, 'proposed');
assert.strictEqual(escalateJson.newStatus, 'escalated');
assert.strictEqual(escalateJson.safety.externalWrite, false);

// ── snoozed → proposed (repropose) ───────────────────────────────────────────

const dirReproposeSnoozed = mkTmp('repropose-snoozed');
const pSnoozed = createProposal(dirReproposeSnoozed, 'human-review');
decide(dirReproposeSnoozed, pSnoozed.id, ['snooze']);

const reproposeFromSnoozeResult = decide(dirReproposeSnoozed, pSnoozed.id, ['repropose']);
assert.strictEqual(reproposeFromSnoozeResult.status, 0, 'repropose from snoozed should succeed');
const reproposeFromSnoozeJson = JSON.parse(reproposeFromSnoozeResult.stdout);
assert.strictEqual(reproposeFromSnoozeJson.ok, true);
assert.strictEqual(reproposeFromSnoozeJson.previousStatus, 'snoozed');
assert.strictEqual(reproposeFromSnoozeJson.newStatus, 'proposed');

// ── escalated → proposed (repropose) ─────────────────────────────────────────

const dirReproposeEscalated = mkTmp('repropose-escalated');
const pEscalated = createProposal(dirReproposeEscalated, 'notification-draft');
decide(dirReproposeEscalated, pEscalated.id, ['escalate']);

const reproposeFromEscalatedResult = decide(dirReproposeEscalated, pEscalated.id, ['repropose']);
assert.strictEqual(reproposeFromEscalatedResult.status, 0, 'repropose from escalated should succeed');
const reproposeFromEscalatedJson = JSON.parse(reproposeFromEscalatedResult.stdout);
assert.strictEqual(reproposeFromEscalatedJson.ok, true);
assert.strictEqual(reproposeFromEscalatedJson.previousStatus, 'escalated');
assert.strictEqual(reproposeFromEscalatedJson.newStatus, 'proposed');

// ── approved cannot be changed ────────────────────────────────────────────────

const dirTerminalApproved = mkTmp('terminal-approved');
const pTerminalApproved = createProposal(dirTerminalApproved, 'file-write');
decide(dirTerminalApproved, pTerminalApproved.id, ['approve']);

const approveApprovedResult = decide(dirTerminalApproved, pTerminalApproved.id, ['reject']);
assert.strictEqual(approveApprovedResult.status, 1, 'cannot decide on approved proposal');
const approveApprovedJson = JSON.parse(approveApprovedResult.stdout);
assert.strictEqual(approveApprovedJson.ok, false);
assert.strictEqual(approveApprovedJson.error.code, 'INVALID_PROPOSAL_DECISION');
assert.deepStrictEqual(approveApprovedJson.error.allowedDecisions, []);
assert.strictEqual(approveApprovedJson.safety.externalWrite, false);

// ── rejected cannot be changed ────────────────────────────────────────────────

const dirTerminalRejected = mkTmp('terminal-rejected');
const pTerminalRejected = createProposal(dirTerminalRejected, 'api-call');
decide(dirTerminalRejected, pTerminalRejected.id, ['reject']);

const rejectRejectedResult = decide(dirTerminalRejected, pTerminalRejected.id, ['approve']);
assert.strictEqual(rejectRejectedResult.status, 1, 'cannot decide on rejected proposal');
const rejectRejectedJson = JSON.parse(rejectRejectedResult.stdout);
assert.strictEqual(rejectRejectedJson.ok, false);
assert.strictEqual(rejectRejectedJson.error.code, 'INVALID_PROPOSAL_DECISION');
assert.deepStrictEqual(rejectRejectedJson.error.allowedDecisions, []);
assert.strictEqual(rejectRejectedJson.safety.externalWrite, false);

// ── missing proposal returns PROPOSAL_NOT_FOUND ───────────────────────────────

const dirMissingProposal = mkTmp('missing-proposal');
const missingProposalResult = decide(dirMissingProposal, 'nonexistent-uuid', ['approve']);
assert.strictEqual(missingProposalResult.status, 1, 'missing proposal should exit non-zero');
const missingProposalJson = JSON.parse(missingProposalResult.stdout);
assert.strictEqual(missingProposalJson.ok, false);
assert.strictEqual(missingProposalJson.error.code, 'PROPOSAL_NOT_FOUND');
assert.ok(Array.isArray(missingProposalJson.error.availableProposalIds), 'should include availableProposalIds');
assert.strictEqual(missingProposalJson.safety.externalWrite, false);

// ── missing decision returns MISSING_PROPOSAL_DECISION ────────────────────────

const dirMissingDecision = mkTmp('missing-decision');
const pMissingDecision = createProposal(dirMissingDecision, 'file-write');
const missingDecisionResult = spawnSync(
  process.execPath,
  ['dist/scripts/proposalDecide.js', pMissingDecision.id, '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: dirMissingDecision }, encoding: 'utf8' }
);
assert.strictEqual(missingDecisionResult.status, 1, 'missing decision should exit non-zero');
const missingDecisionJson = JSON.parse(missingDecisionResult.stdout);
assert.strictEqual(missingDecisionJson.ok, false);
assert.strictEqual(missingDecisionJson.error.code, 'MISSING_PROPOSAL_DECISION');
assert.ok(Array.isArray(missingDecisionJson.error.validDecisions), 'should include validDecisions');
assert.strictEqual(missingDecisionJson.safety.externalWrite, false);

// ── invalid decision returns INVALID_PROPOSAL_DECISION_VALUE ─────────────────

const dirInvalidDecision = mkTmp('invalid-decision');
const pInvalidDecision = createProposal(dirInvalidDecision, 'file-write');
const invalidDecisionResult = decide(dirInvalidDecision, pInvalidDecision.id, ['delete']);
assert.strictEqual(invalidDecisionResult.status, 1, 'invalid decision should exit non-zero');
const invalidDecisionJson = JSON.parse(invalidDecisionResult.stdout);
assert.strictEqual(invalidDecisionJson.ok, false);
assert.strictEqual(invalidDecisionJson.error.code, 'INVALID_PROPOSAL_DECISION_VALUE');
assert.ok(Array.isArray(invalidDecisionJson.error.validDecisions), 'should include validDecisions');
assert.strictEqual(invalidDecisionJson.safety.externalWrite, false);

// ── decision receipt is created ───────────────────────────────────────────────

const dirReceiptCheck = mkTmp('receipt-check');
const pReceiptCheck = createProposal(dirReceiptCheck, 'human-review');
decide(dirReceiptCheck, pReceiptCheck.id, ['approve']);

const receiptsFile = path.join(dirReceiptCheck, 'proposal_decision_receipts.json');
assert.ok(fs.existsSync(receiptsFile), 'proposal_decision_receipts.json should exist after decide');
const storedReceipts = JSON.parse(fs.readFileSync(receiptsFile, 'utf8'));
assert.strictEqual(storedReceipts.length, 1);
assert.strictEqual(storedReceipts[0].proposalId, pReceiptCheck.id);
assert.strictEqual(storedReceipts[0].externalWrite, false);
assert.strictEqual(storedReceipts[0].boundaryCrossed, 'local_commit');
assert.strictEqual(storedReceipts[0].source, 'worldloops.local');
assert.strictEqual(storedReceipts[0].actor, 'worldloops.local');

// ── proposal updatedAt changes ────────────────────────────────────────────────

const dirUpdatedAt = mkTmp('updated-at');
const pUpdatedAt = createProposal(dirUpdatedAt, 'api-call');
const originalUpdatedAt = pUpdatedAt.updatedAt;

decide(dirUpdatedAt, pUpdatedAt.id, ['snooze']);

const updatedProposals = JSON.parse(fs.readFileSync(path.join(dirUpdatedAt, 'proposals.json'), 'utf8'));
assert.ok(
  updatedProposals[0].updatedAt >= originalUpdatedAt,
  'updatedAt should be updated after decide'
);

// ── optional note field support ───────────────────────────────────────────────

const dirNote = mkTmp('note');
const pNote = createProposal(dirNote, 'human-review');
const noteResult = decide(dirNote, pNote.id, ['approve', 'Reviewed by human']);
assert.strictEqual(noteResult.status, 0, 'approve with note should succeed');
const noteJson = JSON.parse(noteResult.stdout);
assert.strictEqual(noteJson.note, 'Reviewed by human');

const noteReceipts = JSON.parse(fs.readFileSync(path.join(dirNote, 'proposal_decision_receipts.json'), 'utf8'));
assert.strictEqual(noteReceipts[0].note, 'Reviewed by human');

// ── --decision flag syntax ────────────────────────────────────────────────────

const dirFlagSyntax = mkTmp('flag-syntax');
const pFlagSyntax = createProposal(dirFlagSyntax, 'state-transition');
const flagResult = spawnSync(
  process.execPath,
  ['dist/scripts/proposalDecide.js', pFlagSyntax.id, '--decision', 'reject', '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: dirFlagSyntax }, encoding: 'utf8' }
);
assert.strictEqual(flagResult.status, 0, '--decision flag syntax should work');
const flagJson = JSON.parse(flagResult.stdout);
assert.strictEqual(flagJson.ok, true);
assert.strictEqual(flagJson.newStatus, 'rejected');

// ── human-readable output ─────────────────────────────────────────────────────

const dirHuman = mkTmp('human');
const pHuman = createProposal(dirHuman, 'file-write');
const humanResult = execFileSync(
  process.execPath,
  ['dist/scripts/proposalDecide.js', pHuman.id, 'approve'],
  { env: { ...process.env, WORLDLOOPS_DIR: dirHuman }, encoding: 'utf8' }
);
assert.throws(() => JSON.parse(humanResult), 'human output should not be valid JSON');
assert.ok(humanResult.includes('externalWrite'), 'human output should mention externalWrite');
assert.ok(humanResult.includes('false'), 'human output should mention false');

// ── externalWrite:false preserved across all error paths ──────────────────────

const dirExternalCheck = mkTmp('external-check');
// no proposal arg
const noIdResult = spawnSync(
  process.execPath,
  ['dist/scripts/proposalDecide.js', '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: dirExternalCheck }, encoding: 'utf8' }
);
const noIdJson = JSON.parse(noIdResult.stdout);
assert.strictEqual(noIdJson.safety.externalWrite, false);

console.log('proposalDecide tests passed');
