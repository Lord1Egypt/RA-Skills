const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync, spawnSync } = require('node:child_process');

function mkTmp(label) {
  return fs.mkdtempSync(path.join(os.tmpdir(), `worldloops-plan-create-${label}-`));
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

function planCreate(dir, proposalId, extraArgs) {
  return spawnSync(
    process.execPath,
    ['dist/scripts/planCreate.js', proposalId, ...(extraArgs ?? [])],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
}

// ── creates plan from approved proposal ──────────────────────────────────────

const dirOk = mkTmp('ok');
const pOk = createProposal(dirOk, 'file-write');
approveProposal(dirOk, pOk.id);

const okResult = planCreate(dirOk, pOk.id, ['--json']);
assert.strictEqual(okResult.status, 0, 'plan:create should succeed for approved proposal');

const okJson = JSON.parse(okResult.stdout);
assert.strictEqual(okJson.ok, true);
assert.strictEqual(okJson.source, 'worldloops.local');
assert.strictEqual(okJson.safety.externalWrite, false);

const plan = okJson.plan;
assert.ok(plan.id, 'plan should have id');
assert.strictEqual(plan.proposalId, pOk.id);
assert.strictEqual(plan.templateId, 'file-write');
assert.strictEqual(plan.status, 'planned');
assert.strictEqual(plan.externalWrite, false);
assert.strictEqual(plan.source, 'worldloops.local');
assert.ok(plan.createdAt, 'plan should have createdAt');
assert.ok(plan.updatedAt, 'plan should have updatedAt');
assert.ok(Array.isArray(plan.steps), 'plan should have steps array');
assert.ok(plan.steps.length >= 4, 'plan should have at least 4 steps');

// ── all steps have externalWrite:false ────────────────────────────────────────

for (const step of plan.steps) {
  assert.strictEqual(step.externalWrite, false, `step "${step.title}" must have externalWrite:false`);
  assert.ok(step.id, `step "${step.title}" must have id`);
  assert.ok(step.type, `step "${step.title}" must have type`);
  assert.ok(step.description, `step "${step.title}" must have description`);
}

// ── persisted to .worldloops/execution_plans.json ────────────────────────────

const plansFile = path.join(dirOk, 'execution_plans.json');
assert.ok(fs.existsSync(plansFile), 'execution_plans.json should exist after create');

const stored = JSON.parse(fs.readFileSync(plansFile, 'utf8'));
assert.ok(Array.isArray(stored), 'execution_plans.json should be an array');
assert.strictEqual(stored.length, 1);
assert.strictEqual(stored[0].id, plan.id);
assert.strictEqual(stored[0].externalWrite, false);

// ── human-readable output ─────────────────────────────────────────────────────

const dirHuman = mkTmp('human');
const pHuman = createProposal(dirHuman, 'api-call');
approveProposal(dirHuman, pHuman.id);

const humanResult = planCreate(dirHuman, pHuman.id, []);
assert.strictEqual(humanResult.status, 0, 'human-readable plan:create should succeed');

assert.throws(
  () => JSON.parse(humanResult.stdout),
  'default output should not be valid JSON'
);

assert.ok(humanResult.stdout.includes('Execution plan created'), 'should include created message');
assert.ok(humanResult.stdout.includes('externalWrite'), 'should mention externalWrite');
assert.ok(humanResult.stdout.includes('false'), 'should show false');

// ── refuses proposed proposal with PROPOSAL_NOT_APPROVED ─────────────────────

const dirProposed = mkTmp('proposed');
const pProposed = createProposal(dirProposed, 'state-transition');

const proposedResult = planCreate(dirProposed, pProposed.id, ['--json']);
assert.strictEqual(proposedResult.status, 1, 'proposed proposal should fail');

const proposedJson = JSON.parse(proposedResult.stdout);
assert.strictEqual(proposedJson.ok, false);
assert.strictEqual(proposedJson.error.code, 'PROPOSAL_NOT_APPROVED');
assert.strictEqual(proposedJson.error.currentStatus, 'proposed');
assert.strictEqual(proposedJson.error.requiredStatus, 'approved');
assert.strictEqual(proposedJson.safety.externalWrite, false);

// ── refuses rejected proposal with PROPOSAL_NOT_APPROVED ─────────────────────

const dirRejected = mkTmp('rejected');
const pRejected = createProposal(dirRejected, 'human-review');
execFileSync(
  process.execPath,
  ['dist/scripts/proposalDecide.js', pRejected.id, 'reject', '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: dirRejected }, encoding: 'utf8' }
);

const rejectedResult = planCreate(dirRejected, pRejected.id, ['--json']);
assert.strictEqual(rejectedResult.status, 1, 'rejected proposal should fail');

const rejectedJson = JSON.parse(rejectedResult.stdout);
assert.strictEqual(rejectedJson.ok, false);
assert.strictEqual(rejectedJson.error.code, 'PROPOSAL_NOT_APPROVED');
assert.strictEqual(rejectedJson.error.currentStatus, 'rejected');
assert.strictEqual(rejectedJson.safety.externalWrite, false);

// ── missing proposal returns PROPOSAL_NOT_FOUND ───────────────────────────────

const dirMissing = mkTmp('missing');
const missingResult = planCreate(dirMissing, 'nonexistent-proposal-id', ['--json']);
assert.strictEqual(missingResult.status, 1, 'missing proposal should fail');

const missingJson = JSON.parse(missingResult.stdout);
assert.strictEqual(missingJson.ok, false);
assert.strictEqual(missingJson.error.code, 'PROPOSAL_NOT_FOUND');
assert.ok(Array.isArray(missingJson.error.availableProposalIds), 'should include availableProposalIds');
assert.strictEqual(missingJson.safety.externalWrite, false);

// ── high-risk proposal gets dry_run step ─────────────────────────────────────

const dirHighRisk = mkTmp('high-risk');
const pHighRisk = createProposal(dirHighRisk, 'api-call'); // api-call is high risk
approveProposal(dirHighRisk, pHighRisk.id);

const highRiskResult = planCreate(dirHighRisk, pHighRisk.id, ['--json']);
assert.strictEqual(highRiskResult.status, 0);
const highRiskJson = JSON.parse(highRiskResult.stdout);
const stepTypes = highRiskJson.plan.steps.map((s) => s.type);
assert.ok(stepTypes.includes('dry_run'), 'high-risk plan should include dry_run step');

// ── output safety.externalWrite:false ─────────────────────────────────────────

assert.strictEqual(okJson.safety.externalWrite, false);
assert.strictEqual(proposedJson.safety.externalWrite, false);
assert.strictEqual(rejectedJson.safety.externalWrite, false);
assert.strictEqual(missingJson.safety.externalWrite, false);
assert.strictEqual(highRiskJson.safety.externalWrite, false);

console.log('planCreate tests passed');
