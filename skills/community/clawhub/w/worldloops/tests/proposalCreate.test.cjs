const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync, spawnSync } = require('node:child_process');

// ── create proposal from file-write template ──────────────────────────────────

const dir1 = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-proposal-create-'));

const createResult = execFileSync(
  process.execPath,
  ['dist/scripts/proposalCreate.js', 'file-write', '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: dir1 }, encoding: 'utf8' }
);

const createJson = JSON.parse(createResult);

assert.strictEqual(createJson.ok, true);
assert.strictEqual(createJson.source, 'worldloops.local');
assert.strictEqual(createJson.safety.externalWrite, false);

const proposal = createJson.proposal;
assert.ok(proposal.id, 'proposal should have id');
assert.strictEqual(proposal.templateId, 'file-write');
assert.strictEqual(proposal.status, 'proposed');
assert.strictEqual(proposal.externalWrite, false);
assert.strictEqual(proposal.requiredReview, true);
assert.strictEqual(proposal.source, 'worldloops.local');
assert.ok(Array.isArray(proposal.checks), 'proposal should have checks array');
assert.ok(proposal.checks.length > 0, 'proposal checks should be non-empty');
assert.ok(proposal.createdAt, 'proposal should have createdAt');
assert.ok(proposal.updatedAt, 'proposal should have updatedAt');

// ── proposal persisted to .worldloops/proposals.json ─────────────────────────

const proposalsFile = path.join(dir1, 'proposals.json');
assert.ok(fs.existsSync(proposalsFile), 'proposals.json should exist after create');

const stored = JSON.parse(fs.readFileSync(proposalsFile, 'utf8'));
assert.ok(Array.isArray(stored), 'proposals.json should be an array');
assert.strictEqual(stored.length, 1);
assert.strictEqual(stored[0].id, proposal.id);
assert.strictEqual(stored[0].externalWrite, false);

// ── human-readable output ─────────────────────────────────────────────────────

const dir2 = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-proposal-create-'));

const humanResult = execFileSync(
  process.execPath,
  ['dist/scripts/proposalCreate.js', 'api-call'],
  { env: { ...process.env, WORLDLOOPS_DIR: dir2 }, encoding: 'utf8' }
);

assert.throws(
  () => JSON.parse(humanResult),
  'default output should not be valid JSON'
);

assert.ok(humanResult.includes('Proposal created'), 'human output should include created message');
assert.ok(humanResult.includes('api-call'), 'human output should include template id');
assert.ok(humanResult.includes('externalWrite'), 'human output should mention externalWrite');
assert.ok(humanResult.includes('false'), 'human output should show externalWrite:false');

// ── create proposals from multiple templates ──────────────────────────────────

const dir3 = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-proposal-create-'));
const templates = ['state-transition', 'human-review', 'notification-draft', 'escalation'];

for (const tid of templates) {
  const r = execFileSync(
    process.execPath,
    ['dist/scripts/proposalCreate.js', tid, '--json'],
    { env: { ...process.env, WORLDLOOPS_DIR: dir3 }, encoding: 'utf8' }
  );
  const rJson = JSON.parse(r);
  assert.strictEqual(rJson.ok, true);
  assert.strictEqual(rJson.proposal.templateId, tid);
  assert.strictEqual(rJson.proposal.externalWrite, false);
}

const storedMulti = JSON.parse(fs.readFileSync(path.join(dir3, 'proposals.json'), 'utf8'));
assert.strictEqual(storedMulti.length, 4, 'should have 4 proposals');

// ── missing template returns PROPOSAL_TEMPLATE_NOT_FOUND ──────────────────────

const dir4 = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-proposal-create-'));

const notFoundResult = spawnSync(
  process.execPath,
  ['dist/scripts/proposalCreate.js', 'nonexistent-template', '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: dir4 }, encoding: 'utf8' }
);

assert.strictEqual(notFoundResult.status, 1, 'missing template should exit non-zero');
const notFoundJson = JSON.parse(notFoundResult.stdout);
assert.strictEqual(notFoundJson.ok, false);
assert.strictEqual(notFoundJson.error.code, 'PROPOSAL_TEMPLATE_NOT_FOUND');
assert.ok(Array.isArray(notFoundJson.error.availableTemplateIds), 'should include availableTemplateIds');
assert.strictEqual(notFoundJson.safety.externalWrite, false);

// ── missing template-id argument ──────────────────────────────────────────────

const noArgResult = spawnSync(
  process.execPath,
  ['dist/scripts/proposalCreate.js'],
  { env: { ...process.env, WORLDLOOPS_DIR: dir4 }, encoding: 'utf8' }
);

assert.strictEqual(noArgResult.status, 1, 'missing arg should exit non-zero');
const noArgJson = JSON.parse(noArgResult.stdout);
assert.strictEqual(noArgJson.ok, false);
assert.strictEqual(noArgJson.error.code, 'MISSING_TEMPLATE_ID');
assert.strictEqual(noArgJson.safety.externalWrite, false);

// ── no external writes (proposals.json stays local) ───────────────────────────

assert.ok(!fs.existsSync(path.join(dir4, 'proposals.json')), 'failed create should not produce proposals.json');

console.log('proposalCreate tests passed');
