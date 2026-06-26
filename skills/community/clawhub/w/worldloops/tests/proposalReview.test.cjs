const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync, spawnSync } = require('node:child_process');

function mkTmp(prefix) {
  return fs.mkdtempSync(path.join(os.tmpdir(), `worldloops-proposal-review-${prefix}-`));
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
  ['dist/scripts/proposalReview.js'],
  { env: { ...process.env, WORLDLOOPS_DIR: dirEmpty }, encoding: 'utf8' }
);
assert.throws(() => JSON.parse(emptyHuman), 'human output should not be valid JSON');
assert.ok(emptyHuman.includes('Total proposals: 0'), 'should show 0 total');
assert.ok(emptyHuman.includes('proposed: 0'), 'should show 0 proposed');
assert.ok(emptyHuman.includes('externalWrite'), 'should mention externalWrite');
assert.ok(emptyHuman.includes('false'), 'should show false');

// ── empty state JSON ──────────────────────────────────────────────────────────

const emptyJson = execFileSync(
  process.execPath,
  ['dist/scripts/proposalReview.js', '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: dirEmpty }, encoding: 'utf8' }
);
const emptyJsonParsed = JSON.parse(emptyJson);
assert.strictEqual(emptyJsonParsed.ok, true);
assert.strictEqual(emptyJsonParsed.source, 'worldloops.local');
assert.strictEqual(emptyJsonParsed.review.total, 0);
assert.strictEqual(emptyJsonParsed.review.byStatus.proposed, 0);
assert.strictEqual(emptyJsonParsed.review.byStatus.approved, 0);
assert.strictEqual(emptyJsonParsed.review.byStatus.rejected, 0);
assert.strictEqual(emptyJsonParsed.review.byStatus.snoozed, 0);
assert.strictEqual(emptyJsonParsed.review.byStatus.escalated, 0);
assert.ok(Array.isArray(emptyJsonParsed.review.highRiskProposals), 'should have highRiskProposals array');
assert.strictEqual(emptyJsonParsed.review.highRiskProposals.length, 0);
assert.strictEqual(emptyJsonParsed.review.suggestedFocus, null);
assert.strictEqual(emptyJsonParsed.safety.externalWrite, false);

// ── populated counts by status ────────────────────────────────────────────────

const dirPopulated = mkTmp('populated');

// Create 5 proposals with different statuses
const p1 = createProposal(dirPopulated, 'file-write');       // will be approved
const p2 = createProposal(dirPopulated, 'api-call');         // will be rejected
const p3 = createProposal(dirPopulated, 'state-transition'); // will remain proposed
const p4 = createProposal(dirPopulated, 'human-review');     // will be snoozed
const p5 = createProposal(dirPopulated, 'escalation');       // will be escalated

decide(dirPopulated, p1.id, 'approve');
decide(dirPopulated, p2.id, 'reject');
decide(dirPopulated, p4.id, 'snooze');
decide(dirPopulated, p5.id, 'escalate');
// p3 remains proposed

const populatedJson = execFileSync(
  process.execPath,
  ['dist/scripts/proposalReview.js', '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: dirPopulated }, encoding: 'utf8' }
);
const populatedParsed = JSON.parse(populatedJson);

assert.strictEqual(populatedParsed.ok, true);
assert.strictEqual(populatedParsed.review.total, 5);
assert.strictEqual(populatedParsed.review.byStatus.proposed, 1);
assert.strictEqual(populatedParsed.review.byStatus.approved, 1);
assert.strictEqual(populatedParsed.review.byStatus.rejected, 1);
assert.strictEqual(populatedParsed.review.byStatus.snoozed, 1);
assert.strictEqual(populatedParsed.review.byStatus.escalated, 1);
assert.strictEqual(populatedParsed.safety.externalWrite, false);

// ── human-readable populated ──────────────────────────────────────────────────

const populatedHuman = execFileSync(
  process.execPath,
  ['dist/scripts/proposalReview.js'],
  { env: { ...process.env, WORLDLOOPS_DIR: dirPopulated }, encoding: 'utf8' }
);
assert.ok(populatedHuman.includes('Total proposals: 5'), 'should show 5 total');
assert.ok(populatedHuman.includes('proposed: 1'), 'should show 1 proposed');
assert.ok(populatedHuman.includes('approved: 1'), 'should show 1 approved');
assert.ok(populatedHuman.includes('rejected: 1'), 'should show 1 rejected');
assert.ok(populatedHuman.includes('snoozed: 1'), 'should show 1 snoozed');
assert.ok(populatedHuman.includes('escalated: 1'), 'should show 1 escalated');

// ── high-risk proposed proposals surfaced ─────────────────────────────────────

// api-call (high risk) is rejected so not in high-risk proposed
// escalation (high risk) is escalated so not in high-risk proposed
// state-transition (medium risk) is proposed but not high-risk
// So no high-risk proposed proposals in this dir

// Create a new dir with a high-risk proposed proposal
const dirHighRisk = mkTmp('high-risk');
const pHighRisk = createProposal(dirHighRisk, 'api-call');   // high risk, stays proposed
const pLowRisk = createProposal(dirHighRisk, 'human-review'); // low risk, stays proposed

const highRiskJson = execFileSync(
  process.execPath,
  ['dist/scripts/proposalReview.js', '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: dirHighRisk }, encoding: 'utf8' }
);
const highRiskParsed = JSON.parse(highRiskJson);

assert.strictEqual(highRiskParsed.review.highRiskProposals.length, 1, 'should surface 1 high-risk proposed proposal');
assert.strictEqual(highRiskParsed.review.highRiskProposals[0].id, pHighRisk.id);
assert.strictEqual(highRiskParsed.review.highRiskProposals[0].riskLevel, 'high');

// ── suggested focus present when proposed proposals exist ──────────────────────

assert.ok(populatedParsed.review.suggestedFocus, 'suggestedFocus should be set when proposed proposals exist');
assert.ok(
  typeof populatedParsed.review.suggestedFocus === 'string',
  'suggestedFocus should be a string'
);
assert.ok(
  populatedParsed.review.suggestedFocus.includes('1'),
  'suggestedFocus should mention the count'
);

// ── suggested focus present in human-readable output ──────────────────────────

assert.ok(populatedHuman.includes('Suggested focus'), 'human output should include Suggested focus section');

// ── no suggested focus when no proposed proposals ─────────────────────────────

const dirAllDone = mkTmp('all-done');
const pAllDone = createProposal(dirAllDone, 'file-write');
decide(dirAllDone, pAllDone.id, 'approve');

const allDoneJson = execFileSync(
  process.execPath,
  ['dist/scripts/proposalReview.js', '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: dirAllDone }, encoding: 'utf8' }
);
const allDoneParsed = JSON.parse(allDoneJson);
assert.strictEqual(allDoneParsed.review.suggestedFocus, null, 'no suggestedFocus when no proposed proposals');

// ── externalWrite:false preserved ─────────────────────────────────────────────

assert.strictEqual(populatedParsed.safety.externalWrite, false);
assert.strictEqual(emptyJsonParsed.safety.externalWrite, false);

console.log('proposalReview tests passed');
