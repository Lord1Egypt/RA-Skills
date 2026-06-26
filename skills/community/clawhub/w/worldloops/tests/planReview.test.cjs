const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync, spawnSync } = require('node:child_process');

function mkTmp(label) {
  return fs.mkdtempSync(path.join(os.tmpdir(), `worldloops-plan-review-${label}-`));
}

function createApprovedProposal(dir, templateId) {
  const r = execFileSync(
    process.execPath,
    ['dist/scripts/proposalCreate.js', templateId, '--json'],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
  const proposal = JSON.parse(r).proposal;
  execFileSync(
    process.execPath,
    ['dist/scripts/proposalDecide.js', proposal.id, 'approve', '--json'],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
  return proposal;
}

function planCreate(dir, proposalId) {
  execFileSync(
    process.execPath,
    ['dist/scripts/planCreate.js', proposalId, '--json'],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
}

function planReview(dir, extraArgs) {
  return spawnSync(
    process.execPath,
    ['dist/scripts/planReview.js', ...(extraArgs ?? [])],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
}

// ── empty human-readable ──────────────────────────────────────────────────────

const dirEmpty = mkTmp('empty');
const emptyHuman = planReview(dirEmpty, []);
assert.strictEqual(emptyHuman.status, 0);
assert.ok(emptyHuman.stdout.includes('Execution Plan Review'), 'should include review header');
assert.ok(emptyHuman.stdout.includes('Total plans: 0'), 'should show 0 total');
assert.ok(emptyHuman.stdout.includes('externalWrite'), 'should mention externalWrite');
assert.ok(emptyHuman.stdout.includes('false'), 'should show false');

// ── empty JSON ────────────────────────────────────────────────────────────────

const emptyJsonResult = planReview(dirEmpty, ['--json']);
assert.strictEqual(emptyJsonResult.status, 0);
const emptyJson = JSON.parse(emptyJsonResult.stdout);
assert.strictEqual(emptyJson.ok, true);
assert.strictEqual(emptyJson.source, 'worldloops.local');
assert.strictEqual(emptyJson.review.total, 0);
assert.ok('planned' in emptyJson.review.byStatus, 'byStatus should include planned');
assert.strictEqual(emptyJson.review.byStatus.planned, 0);
assert.ok(Array.isArray(emptyJson.review.highRiskPlans), 'highRiskPlans should be array');
assert.strictEqual(emptyJson.review.highRiskPlans.length, 0);
assert.strictEqual(emptyJson.review.suggestedFocus, null);
assert.strictEqual(emptyJson.safety.externalWrite, false);

// ── populated counts ──────────────────────────────────────────────────────────

const dirPop = mkTmp('populated');
const pLow = createApprovedProposal(dirPop, 'human-review');    // risk: low
const pMed = createApprovedProposal(dirPop, 'file-write');      // risk: medium
const pHigh = createApprovedProposal(dirPop, 'api-call');       // risk: high
planCreate(dirPop, pLow.id);
planCreate(dirPop, pMed.id);
planCreate(dirPop, pHigh.id);

const popJsonResult = planReview(dirPop, ['--json']);
assert.strictEqual(popJsonResult.status, 0);
const popJson = JSON.parse(popJsonResult.stdout);
assert.strictEqual(popJson.ok, true);
assert.strictEqual(popJson.review.total, 3);
assert.strictEqual(popJson.review.byStatus.planned, 3);
assert.strictEqual(popJson.safety.externalWrite, false);

// ── high-risk plans surfaced ──────────────────────────────────────────────────

assert.ok(popJson.review.highRiskPlans.length >= 1, 'should surface high-risk plans');
const highRiskIds = popJson.review.highRiskPlans.map((p) => p.id);
const highRiskLevels = popJson.review.highRiskPlans.map((p) => p.riskLevel);
for (const level of highRiskLevels) {
  assert.ok(level === 'high' || level === 'critical', `high-risk plan must have high or critical risk level, got: ${level}`);
}

// all high-risk plans have required fields
for (const p of popJson.review.highRiskPlans) {
  assert.ok(p.id, 'highRiskPlan should have id');
  assert.ok(p.proposalId, 'highRiskPlan should have proposalId');
  assert.ok(p.templateId, 'highRiskPlan should have templateId');
  assert.ok(p.riskLevel, 'highRiskPlan should have riskLevel');
  assert.ok(p.title, 'highRiskPlan should have title');
  assert.ok(p.status, 'highRiskPlan should have status');
}

// ── suggested focus ───────────────────────────────────────────────────────────

assert.ok(popJson.review.suggestedFocus !== null, 'populated review should have suggestedFocus');
assert.strictEqual(typeof popJson.review.suggestedFocus, 'string');

// ── human-readable populated ──────────────────────────────────────────────────

const popHuman = planReview(dirPop, []);
assert.strictEqual(popHuman.status, 0);
assert.ok(popHuman.stdout.includes('Total plans: 3'), 'should show 3 total');
assert.ok(popHuman.stdout.includes('planned: 3'), 'should show planned count');
assert.ok(popHuman.stdout.includes('High-risk'), 'should include high-risk section');
assert.ok(popHuman.stdout.includes('Suggested focus'), 'should include suggested focus');
assert.ok(popHuman.stdout.includes('externalWrite'), 'should mention externalWrite');

// ── externalWrite:false in all outputs ───────────────────────────────────────

assert.strictEqual(emptyJson.safety.externalWrite, false);
assert.strictEqual(popJson.safety.externalWrite, false);

console.log('planReview tests passed');
