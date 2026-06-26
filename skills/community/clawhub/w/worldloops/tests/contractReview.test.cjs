const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync, spawnSync } = require('node:child_process');

function mkTmp(label) {
  return fs.mkdtempSync(path.join(os.tmpdir(), `worldloops-contract-review-${label}-`));
}

function createProposal(dir, templateId) {
  const result = execFileSync(
    process.execPath,
    ['dist/scripts/proposalCreate.js', templateId, '--json'],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
  return JSON.parse(result).proposal;
}

function approveProposal(dir, proposalId) {
  execFileSync(
    process.execPath,
    ['dist/scripts/proposalDecide.js', proposalId, 'approve', '--json'],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
}

function createPlan(dir, proposalId) {
  const result = execFileSync(
    process.execPath,
    ['dist/scripts/planCreate.js', proposalId, '--json'],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
  return JSON.parse(result).plan;
}

function createContract(dir, planId) {
  const result = execFileSync(
    process.execPath,
    ['dist/scripts/contractCreate.js', planId, '--json'],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
  return JSON.parse(result).contract;
}

function contractReview(dir, extraArgs) {
  return spawnSync(
    process.execPath,
    ['dist/scripts/contractReview.js', ...(extraArgs ?? [])],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
}

// ── empty human-readable ──────────────────────────────────────────────────────

const dirEmpty = mkTmp('empty');
const emptyHuman = contractReview(dirEmpty, []);
assert.strictEqual(emptyHuman.status, 0);
assert.ok(emptyHuman.stdout.includes('Execution Contract Review'));
assert.ok(emptyHuman.stdout.includes('Total contracts: 0'));
assert.ok(emptyHuman.stdout.includes('draft: 0'));
assert.ok(emptyHuman.stdout.includes('externalWrite'));
assert.ok(emptyHuman.stdout.includes('false'));

// ── empty JSON ────────────────────────────────────────────────────────────────

const emptyJson = contractReview(dirEmpty, ['--json']);
assert.strictEqual(emptyJson.status, 0);
const emptyParsed = JSON.parse(emptyJson.stdout);
assert.strictEqual(emptyParsed.ok, true);
assert.strictEqual(emptyParsed.source, 'worldloops.local');
assert.strictEqual(emptyParsed.review.total, 0);
assert.strictEqual(emptyParsed.review.byStatus.draft, 0);
assert.ok(Array.isArray(emptyParsed.review.highRiskContracts));
assert.strictEqual(emptyParsed.review.highRiskContracts.length, 0);
assert.strictEqual(emptyParsed.review.suggestedFocus, null);
assert.strictEqual(emptyParsed.safety.externalWrite, false);

// ── populated counts ──────────────────────────────────────────────────────────

const dirPop = mkTmp('populated');
const p1 = createProposal(dirPop, 'file-write');
approveProposal(dirPop, p1.id);
const plan1 = createPlan(dirPop, p1.id);
createContract(dirPop, plan1.id);

const p2 = createProposal(dirPop, 'human-review');
approveProposal(dirPop, p2.id);
const plan2 = createPlan(dirPop, p2.id);
createContract(dirPop, plan2.id);

const popJson = contractReview(dirPop, ['--json']);
assert.strictEqual(popJson.status, 0);
const popParsed = JSON.parse(popJson.stdout);
assert.strictEqual(popParsed.review.total, 2);
assert.strictEqual(popParsed.review.byStatus.draft, 2);
assert.ok(popParsed.review.suggestedFocus !== null);
assert.strictEqual(popParsed.safety.externalWrite, false);

// ── high-risk contracts surfaced ──────────────────────────────────────────────

const dirHigh = mkTmp('high-risk');
// api-call is high risk
const pHigh = createProposal(dirHigh, 'api-call');
approveProposal(dirHigh, pHigh.id);
const planHigh = createPlan(dirHigh, pHigh.id);
const cHigh = createContract(dirHigh, planHigh.id);

const highJson = contractReview(dirHigh, ['--json']);
assert.strictEqual(highJson.status, 0);
const highParsed = JSON.parse(highJson.stdout);
assert.strictEqual(highParsed.review.highRiskContracts.length, 1);
assert.strictEqual(highParsed.review.highRiskContracts[0].id, cHigh.id);
assert.ok(highParsed.review.suggestedFocus.includes('high-risk'));

// ── high-risk in human-readable ───────────────────────────────────────────────

const highHuman = contractReview(dirHigh, []);
assert.strictEqual(highHuman.status, 0);
assert.ok(highHuman.stdout.includes('High-risk contracts'));
assert.ok(highHuman.stdout.includes(cHigh.id));
assert.ok(highHuman.stdout.includes('Suggested focus'));

// ── suggested focus is set for non-high-risk when contracts exist ─────────────

const popHuman = contractReview(dirPop, []);
assert.ok(popHuman.stdout.includes('Suggested focus'));

console.log('contractReview tests passed');
