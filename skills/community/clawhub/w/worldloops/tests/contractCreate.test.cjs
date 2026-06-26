const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync, spawnSync } = require('node:child_process');

function mkTmp(label) {
  return fs.mkdtempSync(path.join(os.tmpdir(), `worldloops-contract-create-${label}-`));
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

function contractCreate(dir, planId, extraArgs) {
  return spawnSync(
    process.execPath,
    ['dist/scripts/contractCreate.js', planId, ...(extraArgs ?? [])],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
}

// ── creates contract from planned execution plan with approved proposal + receipt ──

const dirOk = mkTmp('ok');
const pOk = createProposal(dirOk, 'file-write');
approveProposal(dirOk, pOk.id);
const planOk = createPlan(dirOk, pOk.id);

const okResult = contractCreate(dirOk, planOk.id, ['--json']);
assert.strictEqual(okResult.status, 0, 'contract:create should succeed for planned plan with approved proposal');

const okJson = JSON.parse(okResult.stdout);
assert.strictEqual(okJson.ok, true);
assert.strictEqual(okJson.source, 'worldloops.local');
assert.strictEqual(okJson.safety.externalWrite, false);

const contract = okJson.contract;
assert.ok(contract.id, 'contract should have id');
assert.strictEqual(contract.planId, planOk.id);
assert.strictEqual(contract.proposalId, pOk.id);
assert.strictEqual(contract.templateId, 'file-write');
assert.strictEqual(contract.status, 'draft');
assert.strictEqual(contract.externalWrite, false);
assert.strictEqual(contract.source, 'worldloops.local');
assert.ok(contract.createdAt, 'contract should have createdAt');
assert.ok(contract.updatedAt, 'contract should have updatedAt');

// ── executionBoundary.externalWrite is false ──────────────────────────────────

assert.strictEqual(contract.executionBoundary.externalWrite, false);
assert.strictEqual(contract.executionBoundary.allowedBoundary, 'local_commit');
assert.ok(Array.isArray(contract.executionBoundary.deniedCapabilities));
assert.ok(contract.executionBoundary.deniedCapabilities.includes('sendEmail'));
assert.ok(contract.executionBoundary.deniedCapabilities.includes('sendSlackMessage'));
assert.ok(contract.executionBoundary.deniedCapabilities.includes('createCalendarEvent'));
assert.ok(contract.executionBoundary.deniedCapabilities.includes('modifyGitHub'));
assert.ok(contract.executionBoundary.deniedCapabilities.includes('writeExternalSystem'));

// ── rollbackPlan.available is false ──────────────────────────────────────────

assert.strictEqual(contract.rollbackPlan.available, false);
assert.ok(contract.rollbackPlan.reason.includes('v1.0.0'));

// ── audit fields are correct ──────────────────────────────────────────────────

assert.strictEqual(contract.audit.proposalExists, true);
assert.strictEqual(contract.audit.proposalApproved, true);
assert.strictEqual(contract.audit.decisionReceiptExists, true);
assert.strictEqual(contract.audit.planExists, true);
assert.strictEqual(contract.audit.planStatus, 'planned');
assert.strictEqual(contract.audit.externalWrite, false);

// ── persisted to .worldloops/execution_contracts.json ────────────────────────

const contractsFile = path.join(dirOk, 'execution_contracts.json');
assert.ok(fs.existsSync(contractsFile), 'execution_contracts.json should exist after create');

const stored = JSON.parse(fs.readFileSync(contractsFile, 'utf8'));
assert.ok(Array.isArray(stored), 'execution_contracts.json should be an array');
assert.strictEqual(stored.length, 1);
assert.strictEqual(stored[0].id, contract.id);
assert.strictEqual(stored[0].externalWrite, false);

// ── human-readable output ─────────────────────────────────────────────────────

const dirHuman = mkTmp('human');
const pHuman = createProposal(dirHuman, 'api-call');
approveProposal(dirHuman, pHuman.id);
const planHuman = createPlan(dirHuman, pHuman.id);

const humanResult = contractCreate(dirHuman, planHuman.id, []);
assert.strictEqual(humanResult.status, 0, 'human-readable contract:create should succeed');

assert.throws(
  () => JSON.parse(humanResult.stdout),
  'default output should not be valid JSON'
);

assert.ok(humanResult.stdout.includes('Execution contract created'), 'should include created message');
assert.ok(humanResult.stdout.includes('externalWrite'), 'should mention externalWrite');
assert.ok(humanResult.stdout.includes('false'), 'should show false');

// ── refuses missing plan with EXECUTION_PLAN_NOT_FOUND ───────────────────────

const dirMissingPlan = mkTmp('missing-plan');
const missingPlanResult = contractCreate(dirMissingPlan, 'nonexistent-plan-id', ['--json']);
assert.strictEqual(missingPlanResult.status, 1, 'missing plan should fail');

const missingPlanJson = JSON.parse(missingPlanResult.stdout);
assert.strictEqual(missingPlanJson.ok, false);
assert.strictEqual(missingPlanJson.error.code, 'EXECUTION_PLAN_NOT_FOUND');
assert.ok(Array.isArray(missingPlanJson.error.availablePlanIds));
assert.strictEqual(missingPlanJson.safety.externalWrite, false);

// ── refuses missing proposal with PROPOSAL_NOT_FOUND ─────────────────────────
// Simulate: plan references a proposalId that has been removed from proposals.json

const dirMissingProposal = mkTmp('missing-proposal');
const pForPlan = createProposal(dirMissingProposal, 'state-transition');
approveProposal(dirMissingProposal, pForPlan.id);
const planForMissing = createPlan(dirMissingProposal, pForPlan.id);

// Remove proposals.json to simulate missing proposal
fs.unlinkSync(path.join(dirMissingProposal, 'proposals.json'));

const missingProposalResult = contractCreate(dirMissingProposal, planForMissing.id, ['--json']);
assert.strictEqual(missingProposalResult.status, 1, 'missing proposal should fail');

const missingProposalJson = JSON.parse(missingProposalResult.stdout);
assert.strictEqual(missingProposalJson.ok, false);
assert.strictEqual(missingProposalJson.error.code, 'PROPOSAL_NOT_FOUND');
assert.ok(Array.isArray(missingProposalJson.error.availableProposalIds));
assert.strictEqual(missingProposalJson.safety.externalWrite, false);

// ── refuses non-approved proposal with PROPOSAL_NOT_APPROVED ─────────────────

const dirNotApproved = mkTmp('not-approved');
const pNotApproved = createProposal(dirNotApproved, 'human-review');
// Do NOT approve — proposal stays in 'proposed' status
// Manually write a plan with this proposalId (bypass planCreate's approval check)
const fakePlanId = require('node:crypto').randomUUID();
const fakePlan = {
  id: fakePlanId,
  proposalId: pNotApproved.id,
  templateId: pNotApproved.templateId,
  title: 'Test plan',
  status: 'planned',
  riskLevel: pNotApproved.riskLevel,
  steps: [],
  externalWrite: false,
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  source: 'worldloops.local',
};
fs.writeFileSync(
  path.join(dirNotApproved, 'execution_plans.json'),
  JSON.stringify([fakePlan], null, 2) + '\n',
  'utf8'
);

const notApprovedResult = contractCreate(dirNotApproved, fakePlanId, ['--json']);
assert.strictEqual(notApprovedResult.status, 1, 'non-approved proposal should fail');

const notApprovedJson = JSON.parse(notApprovedResult.stdout);
assert.strictEqual(notApprovedJson.ok, false);
assert.strictEqual(notApprovedJson.error.code, 'PROPOSAL_NOT_APPROVED');
assert.strictEqual(notApprovedJson.error.currentStatus, 'proposed');
assert.strictEqual(notApprovedJson.error.requiredStatus, 'approved');
assert.strictEqual(notApprovedJson.safety.externalWrite, false);

// ── refuses missing approval receipt with DECISION_RECEIPT_NOT_FOUND ─────────

const dirNoReceipt = mkTmp('no-receipt');
const pNoReceipt = createProposal(dirNoReceipt, 'notification-draft');
approveProposal(dirNoReceipt, pNoReceipt.id);
const planNoReceipt = createPlan(dirNoReceipt, pNoReceipt.id);

// Remove decision receipts to simulate missing receipt
fs.unlinkSync(path.join(dirNoReceipt, 'proposal_decision_receipts.json'));

const noReceiptResult = contractCreate(dirNoReceipt, planNoReceipt.id, ['--json']);
assert.strictEqual(noReceiptResult.status, 1, 'missing decision receipt should fail');

const noReceiptJson = JSON.parse(noReceiptResult.stdout);
assert.strictEqual(noReceiptJson.ok, false);
assert.strictEqual(noReceiptJson.error.code, 'DECISION_RECEIPT_NOT_FOUND');
assert.strictEqual(noReceiptJson.error.proposalId, pNoReceipt.id);
assert.strictEqual(noReceiptJson.error.requiredDecision, 'approve');
assert.strictEqual(noReceiptJson.safety.externalWrite, false);

// ── output safety.externalWrite:false throughout ──────────────────────────────

assert.strictEqual(okJson.safety.externalWrite, false);
assert.strictEqual(missingPlanJson.safety.externalWrite, false);
assert.strictEqual(missingProposalJson.safety.externalWrite, false);
assert.strictEqual(notApprovedJson.safety.externalWrite, false);
assert.strictEqual(noReceiptJson.safety.externalWrite, false);

console.log('contractCreate tests passed');
