const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync, spawnSync } = require('node:child_process');

function mkTmp(label) {
  return fs.mkdtempSync(path.join(os.tmpdir(), `worldloops-plan-list-${label}-`));
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
  return execFileSync(
    process.execPath,
    ['dist/scripts/planCreate.js', proposalId, '--json'],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
}

function planList(dir, extraArgs) {
  return spawnSync(
    process.execPath,
    ['dist/scripts/planList.js', ...(extraArgs ?? [])],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
}

// ── empty human-readable ──────────────────────────────────────────────────────

const dirEmpty = mkTmp('empty');
const emptyHumanResult = planList(dirEmpty, []);
assert.strictEqual(emptyHumanResult.status, 0);
assert.ok(emptyHumanResult.stdout.includes('No execution plans found'), 'empty human should say no plans found');
assert.ok(emptyHumanResult.stdout.includes('externalWrite'), 'empty human should mention externalWrite');
assert.ok(emptyHumanResult.stdout.includes('false'), 'empty human should show false');

// ── empty JSON ────────────────────────────────────────────────────────────────

const emptyJsonResult = planList(dirEmpty, ['--json']);
assert.strictEqual(emptyJsonResult.status, 0);
const emptyJson = JSON.parse(emptyJsonResult.stdout);
assert.strictEqual(emptyJson.ok, true);
assert.strictEqual(emptyJson.source, 'worldloops.local');
assert.strictEqual(emptyJson.count, 0);
assert.ok(Array.isArray(emptyJson.plans), 'plans should be an array');
assert.strictEqual(emptyJson.plans.length, 0);
assert.strictEqual(emptyJson.safety.externalWrite, false);

// ── populated human-readable ──────────────────────────────────────────────────

const dirPop = mkTmp('populated');
const p1 = createApprovedProposal(dirPop, 'file-write');
const p2 = createApprovedProposal(dirPop, 'api-call');
planCreate(dirPop, p1.id);
planCreate(dirPop, p2.id);

const popHumanResult = planList(dirPop, []);
assert.strictEqual(popHumanResult.status, 0);
assert.throws(() => JSON.parse(popHumanResult.stdout), 'human output should not be JSON');
assert.ok(popHumanResult.stdout.includes('planned'), 'should show status');
assert.ok(popHumanResult.stdout.includes('externalWrite'), 'should mention externalWrite');

// ── populated JSON ────────────────────────────────────────────────────────────

const popJsonResult = planList(dirPop, ['--json']);
assert.strictEqual(popJsonResult.status, 0);
const popJson = JSON.parse(popJsonResult.stdout);
assert.strictEqual(popJson.ok, true);
assert.strictEqual(popJson.count, 2);
assert.strictEqual(popJson.plans.length, 2);
assert.strictEqual(popJson.safety.externalWrite, false);

for (const plan of popJson.plans) {
  assert.ok(plan.id, 'plan should have id');
  assert.ok(plan.proposalId, 'plan should have proposalId');
  assert.strictEqual(plan.status, 'planned');
  assert.strictEqual(plan.externalWrite, false);
  assert.strictEqual(plan.source, 'worldloops.local');
}

// ── externalWrite:false in all outputs ───────────────────────────────────────

assert.strictEqual(emptyJson.safety.externalWrite, false);
assert.strictEqual(popJson.safety.externalWrite, false);

console.log('planList tests passed');
