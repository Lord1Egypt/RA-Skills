const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync, spawnSync } = require('node:child_process');

function mkTmp(label) {
  return fs.mkdtempSync(path.join(os.tmpdir(), `worldloops-contract-show-${label}-`));
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

function contractShow(dir, contractId, extraArgs) {
  return spawnSync(
    process.execPath,
    ['dist/scripts/contractShow.js', contractId, ...(extraArgs ?? [])],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
}

// ── setup: create contract ────────────────────────────────────────────────────

const dirOk = mkTmp('ok');
const p = createProposal(dirOk, 'state-transition');
approveProposal(dirOk, p.id);
const plan = createPlan(dirOk, p.id);
const contract = createContract(dirOk, plan.id);

// ── human-readable detail ─────────────────────────────────────────────────────

const humanResult = contractShow(dirOk, contract.id, []);
assert.strictEqual(humanResult.status, 0, 'contract:show should succeed for known contract');

assert.throws(
  () => JSON.parse(humanResult.stdout),
  'default output should not be valid JSON'
);

assert.ok(humanResult.stdout.includes(contract.id), 'should show contract id');
assert.ok(humanResult.stdout.includes(plan.id), 'should show plan id');
assert.ok(humanResult.stdout.includes(p.id), 'should show proposal id');
assert.ok(humanResult.stdout.includes('draft'), 'should show status');
assert.ok(humanResult.stdout.includes('local_commit'), 'should show allowed boundary');
assert.ok(humanResult.stdout.includes('Rollback'), 'should include rollback section');
assert.ok(humanResult.stdout.includes('Audit'), 'should include audit section');
assert.ok(humanResult.stdout.includes('externalWrite'), 'should mention externalWrite');
assert.ok(humanResult.stdout.includes('false'), 'should show false');

// ── JSON detail ───────────────────────────────────────────────────────────────

const jsonResult = contractShow(dirOk, contract.id, ['--json']);
assert.strictEqual(jsonResult.status, 0, 'contract:show --json should succeed');

const jsonParsed = JSON.parse(jsonResult.stdout);
assert.strictEqual(jsonParsed.ok, true);
assert.strictEqual(jsonParsed.source, 'worldloops.local');
assert.strictEqual(jsonParsed.safety.externalWrite, false);

const shown = jsonParsed.contract;
assert.strictEqual(shown.id, contract.id);
assert.strictEqual(shown.planId, plan.id);
assert.strictEqual(shown.proposalId, p.id);
assert.strictEqual(shown.status, 'draft');
assert.strictEqual(shown.externalWrite, false);
assert.strictEqual(shown.executionBoundary.externalWrite, false);
assert.strictEqual(shown.rollbackPlan.available, false);
assert.strictEqual(shown.audit.externalWrite, false);
assert.strictEqual(shown.audit.proposalApproved, true);
assert.strictEqual(shown.audit.decisionReceiptExists, true);

// ── missing contract returns EXECUTION_CONTRACT_NOT_FOUND ─────────────────────

const missingResult = contractShow(dirOk, 'nonexistent-contract-id', ['--json']);
assert.strictEqual(missingResult.status, 1, 'missing contract should fail');

const missingParsed = JSON.parse(missingResult.stdout);
assert.strictEqual(missingParsed.ok, false);
assert.strictEqual(missingParsed.error.code, 'EXECUTION_CONTRACT_NOT_FOUND');
assert.ok(Array.isArray(missingParsed.error.availableContractIds));
assert.strictEqual(missingParsed.safety.externalWrite, false);

console.log('contractShow tests passed');
