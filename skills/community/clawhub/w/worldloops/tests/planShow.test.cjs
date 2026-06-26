const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync, spawnSync } = require('node:child_process');

function mkTmp(label) {
  return fs.mkdtempSync(path.join(os.tmpdir(), `worldloops-plan-show-${label}-`));
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
  const r = execFileSync(
    process.execPath,
    ['dist/scripts/planCreate.js', proposalId, '--json'],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
  return JSON.parse(r).plan;
}

function planShow(dir, planId, extraArgs) {
  return spawnSync(
    process.execPath,
    ['dist/scripts/planShow.js', planId, ...(extraArgs ?? [])],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
}

// ── JSON detail ───────────────────────────────────────────────────────────────

const dirJson = mkTmp('json');
const pJson = createApprovedProposal(dirJson, 'state-transition');
const planJson = planCreate(dirJson, pJson.id);

const jsonResult = planShow(dirJson, planJson.id, ['--json']);
assert.strictEqual(jsonResult.status, 0, 'plan:show should succeed');

const jsonOut = JSON.parse(jsonResult.stdout);
assert.strictEqual(jsonOut.ok, true);
assert.strictEqual(jsonOut.source, 'worldloops.local');
assert.strictEqual(jsonOut.safety.externalWrite, false);

const shownPlan = jsonOut.plan;
assert.strictEqual(shownPlan.id, planJson.id);
assert.strictEqual(shownPlan.proposalId, pJson.id);
assert.strictEqual(shownPlan.templateId, 'state-transition');
assert.strictEqual(shownPlan.status, 'planned');
assert.strictEqual(shownPlan.externalWrite, false);
assert.strictEqual(shownPlan.source, 'worldloops.local');
assert.ok(Array.isArray(shownPlan.steps), 'shown plan should have steps');
assert.ok(shownPlan.steps.length >= 4, 'shown plan should have at least 4 steps');

for (const step of shownPlan.steps) {
  assert.strictEqual(step.externalWrite, false, `step "${step.title}" externalWrite must be false`);
}

// ── human-readable detail ─────────────────────────────────────────────────────

const dirHuman = mkTmp('human');
const pHuman = createApprovedProposal(dirHuman, 'human-review');
const planHuman = planCreate(dirHuman, pHuman.id);

const humanResult = planShow(dirHuman, planHuman.id, []);
assert.strictEqual(humanResult.status, 0);
assert.throws(() => JSON.parse(humanResult.stdout), 'human output should not be JSON');
assert.ok(humanResult.stdout.includes('Execution Plan'), 'should include plan header');
assert.ok(humanResult.stdout.includes(planHuman.id), 'should include plan id');
assert.ok(humanResult.stdout.includes('planned'), 'should include status');
assert.ok(humanResult.stdout.includes('Steps'), 'should include steps section');
assert.ok(humanResult.stdout.includes('externalWrite'), 'should mention externalWrite');
assert.ok(humanResult.stdout.includes('false'), 'should show false');

// ── missing plan returns EXECUTION_PLAN_NOT_FOUND ─────────────────────────────

const dirMissing = mkTmp('missing');
const missingResult = planShow(dirMissing, 'nonexistent-plan-id', ['--json']);
assert.strictEqual(missingResult.status, 1, 'missing plan should fail');

const missingJson = JSON.parse(missingResult.stdout);
assert.strictEqual(missingJson.ok, false);
assert.strictEqual(missingJson.error.code, 'EXECUTION_PLAN_NOT_FOUND');
assert.ok(Array.isArray(missingJson.error.availablePlanIds), 'should include availablePlanIds');
assert.strictEqual(missingJson.safety.externalWrite, false);

// ── externalWrite:false in all outputs ───────────────────────────────────────

assert.strictEqual(jsonOut.safety.externalWrite, false);
assert.strictEqual(missingJson.safety.externalWrite, false);

console.log('planShow tests passed');
