const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync, spawnSync } = require('node:child_process');

function mkTmp(prefix) {
  return fs.mkdtempSync(path.join(os.tmpdir(), `worldloops-proposal-receipts-${prefix}-`));
}

function createProposal(dir, templateId) {
  const result = execFileSync(
    process.execPath,
    ['dist/scripts/proposalCreate.js', templateId, '--json'],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
  return JSON.parse(result).proposal;
}

function decide(dir, proposalId, decision) {
  return spawnSync(
    process.execPath,
    ['dist/scripts/proposalDecide.js', proposalId, decision, '--json'],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
}

// ── empty state human-readable ────────────────────────────────────────────────

const dirEmpty = mkTmp('empty');
const emptyHuman = execFileSync(
  process.execPath,
  ['dist/scripts/proposalReceipts.js'],
  { env: { ...process.env, WORLDLOOPS_DIR: dirEmpty }, encoding: 'utf8' }
);
assert.throws(() => JSON.parse(emptyHuman), 'human output should not be valid JSON');
assert.ok(emptyHuman.includes('No proposal decision receipts found'), 'should show empty message');
assert.ok(emptyHuman.includes('externalWrite'), 'should mention externalWrite');
assert.ok(emptyHuman.includes('false'), 'should show false');

// ── empty state JSON ──────────────────────────────────────────────────────────

const emptyJson = execFileSync(
  process.execPath,
  ['dist/scripts/proposalReceipts.js', '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: dirEmpty }, encoding: 'utf8' }
);
const emptyJsonParsed = JSON.parse(emptyJson);
assert.strictEqual(emptyJsonParsed.ok, true);
assert.strictEqual(emptyJsonParsed.source, 'worldloops.local');
assert.strictEqual(emptyJsonParsed.count, 0);
assert.ok(Array.isArray(emptyJsonParsed.receipts), 'receipts should be an array');
assert.strictEqual(emptyJsonParsed.receipts.length, 0);
assert.strictEqual(emptyJsonParsed.safety.externalWrite, false);

// ── populated human-readable ──────────────────────────────────────────────────

const dirPopulated = mkTmp('populated');
const p1 = createProposal(dirPopulated, 'file-write');
const p2 = createProposal(dirPopulated, 'api-call');
const p3 = createProposal(dirPopulated, 'human-review');

decide(dirPopulated, p1.id, 'approve');
decide(dirPopulated, p2.id, 'reject');
decide(dirPopulated, p3.id, 'snooze');

const populatedHuman = execFileSync(
  process.execPath,
  ['dist/scripts/proposalReceipts.js'],
  { env: { ...process.env, WORLDLOOPS_DIR: dirPopulated }, encoding: 'utf8' }
);
assert.throws(() => JSON.parse(populatedHuman), 'human output should not be valid JSON');
assert.ok(populatedHuman.includes('RECEIPT ID'), 'should include header');
assert.ok(populatedHuman.includes('DECISION'), 'should include decision column');
assert.ok(populatedHuman.includes('approve'), 'should include approve decision');
assert.ok(populatedHuman.includes('reject'), 'should include reject decision');
assert.ok(populatedHuman.includes('snooze'), 'should include snooze decision');
assert.ok(populatedHuman.includes('externalWrite'), 'should mention externalWrite');
assert.ok(populatedHuman.includes('false'), 'should show false');

// ── populated JSON ────────────────────────────────────────────────────────────

const populatedJson = execFileSync(
  process.execPath,
  ['dist/scripts/proposalReceipts.js', '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: dirPopulated }, encoding: 'utf8' }
);
const populatedParsed = JSON.parse(populatedJson);
assert.strictEqual(populatedParsed.ok, true);
assert.strictEqual(populatedParsed.source, 'worldloops.local');
assert.strictEqual(populatedParsed.count, 3);
assert.strictEqual(populatedParsed.receipts.length, 3);
assert.strictEqual(populatedParsed.safety.externalWrite, false);

// ── receipt contains required fields ─────────────────────────────────────────

const receipt = populatedParsed.receipts[0];
assert.ok(receipt.id, 'receipt should have id');
assert.ok(receipt.proposalId, 'receipt should have proposalId');
assert.ok(receipt.decision, 'receipt should have decision');
assert.ok(receipt.previousStatus, 'receipt should have previousStatus');
assert.ok(receipt.newStatus, 'receipt should have newStatus');
assert.ok(receipt.createdAt, 'receipt should have createdAt');
assert.strictEqual(receipt.externalWrite, false, 'receipt externalWrite should be false');
assert.strictEqual(receipt.boundaryCrossed, 'local_commit', 'receipt boundaryCrossed should be local_commit');
assert.strictEqual(receipt.source, 'worldloops.local', 'receipt source should be worldloops.local');
assert.strictEqual(receipt.actor, 'worldloops.local', 'receipt actor should be worldloops.local');

// ── receipt proposalId matches proposal ───────────────────────────────────────

const r1 = populatedParsed.receipts.find((r) => r.proposalId === p1.id);
assert.ok(r1, 'should find receipt for p1');
assert.strictEqual(r1.previousStatus, 'proposed');
assert.strictEqual(r1.newStatus, 'approved');
assert.strictEqual(r1.decision, 'approve');

const r2 = populatedParsed.receipts.find((r) => r.proposalId === p2.id);
assert.ok(r2, 'should find receipt for p2');
assert.strictEqual(r2.previousStatus, 'proposed');
assert.strictEqual(r2.newStatus, 'rejected');
assert.strictEqual(r2.decision, 'reject');

const r3 = populatedParsed.receipts.find((r) => r.proposalId === p3.id);
assert.ok(r3, 'should find receipt for p3');
assert.strictEqual(r3.previousStatus, 'proposed');
assert.strictEqual(r3.newStatus, 'snoozed');
assert.strictEqual(r3.decision, 'snooze');

// ── receipts stored in correct file ──────────────────────────────────────────

const receiptsFile = path.join(dirPopulated, 'proposal_decision_receipts.json');
assert.ok(fs.existsSync(receiptsFile), 'proposal_decision_receipts.json should exist');
const storedRaw = JSON.parse(fs.readFileSync(receiptsFile, 'utf8'));
assert.strictEqual(storedRaw.length, 3, 'should have 3 receipts on disk');

// ── externalWrite:false preserved ─────────────────────────────────────────────

assert.strictEqual(populatedParsed.safety.externalWrite, false);
assert.strictEqual(emptyJsonParsed.safety.externalWrite, false);

console.log('proposalReceipts tests passed');
