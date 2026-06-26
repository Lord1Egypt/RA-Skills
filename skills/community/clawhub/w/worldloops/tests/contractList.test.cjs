const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync, spawnSync } = require('node:child_process');

function mkTmp(label) {
  return fs.mkdtempSync(path.join(os.tmpdir(), `worldloops-contract-list-${label}-`));
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

function contractList(dir, extraArgs) {
  return spawnSync(
    process.execPath,
    ['dist/scripts/contractList.js', ...(extraArgs ?? [])],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
}

// ── empty human-readable ──────────────────────────────────────────────────────

const dirEmpty = mkTmp('empty');
const emptyHuman = contractList(dirEmpty, []);
assert.strictEqual(emptyHuman.status, 0);
assert.ok(emptyHuman.stdout.includes('No execution contracts found'));
assert.ok(emptyHuman.stdout.includes('externalWrite'));
assert.ok(emptyHuman.stdout.includes('false'));

// ── empty JSON ────────────────────────────────────────────────────────────────

const emptyJson = contractList(dirEmpty, ['--json']);
assert.strictEqual(emptyJson.status, 0);
const emptyParsed = JSON.parse(emptyJson.stdout);
assert.strictEqual(emptyParsed.ok, true);
assert.ok(Array.isArray(emptyParsed.contracts));
assert.strictEqual(emptyParsed.contracts.length, 0);
assert.strictEqual(emptyParsed.count, 0);
assert.strictEqual(emptyParsed.safety.externalWrite, false);

// ── populated human-readable ──────────────────────────────────────────────────

const dirPop = mkTmp('populated');
const p1 = createProposal(dirPop, 'file-write');
approveProposal(dirPop, p1.id);
const plan1 = createPlan(dirPop, p1.id);
const c1 = createContract(dirPop, plan1.id);

const p2 = createProposal(dirPop, 'api-call');
approveProposal(dirPop, p2.id);
const plan2 = createPlan(dirPop, p2.id);
const c2 = createContract(dirPop, plan2.id);

const popHuman = contractList(dirPop, []);
assert.strictEqual(popHuman.status, 0);
assert.ok(popHuman.stdout.includes(c1.id));
assert.ok(popHuman.stdout.includes(c2.id));
assert.ok(popHuman.stdout.includes('externalWrite'));
assert.ok(popHuman.stdout.includes('false'));

// ── populated JSON ────────────────────────────────────────────────────────────

const popJson = contractList(dirPop, ['--json']);
assert.strictEqual(popJson.status, 0);
const popParsed = JSON.parse(popJson.stdout);
assert.strictEqual(popParsed.ok, true);
assert.strictEqual(popParsed.count, 2);
assert.ok(Array.isArray(popParsed.contracts));
assert.strictEqual(popParsed.contracts.length, 2);
assert.strictEqual(popParsed.source, 'worldloops.local');
assert.strictEqual(popParsed.safety.externalWrite, false);

const ids = popParsed.contracts.map((c) => c.id);
assert.ok(ids.includes(c1.id));
assert.ok(ids.includes(c2.id));

console.log('contractList tests passed');
