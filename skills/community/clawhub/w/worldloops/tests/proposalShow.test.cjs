const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync, spawnSync } = require('node:child_process');

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-proposal-show-'));

// create a proposal to show

const createResult = execFileSync(
  process.execPath,
  ['dist/scripts/proposalCreate.js', 'human-review', '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: tmpDir }, encoding: 'utf8' }
);

const { proposal } = JSON.parse(createResult);

// ── human-readable output ─────────────────────────────────────────────────────

const humanOutput = execFileSync(
  process.execPath,
  ['dist/scripts/proposalShow.js', proposal.id],
  { env: { ...process.env, WORLDLOOPS_DIR: tmpDir }, encoding: 'utf8' }
);

assert.throws(
  () => JSON.parse(humanOutput),
  'default output should not be valid JSON'
);

assert.ok(humanOutput.includes(proposal.id), 'human output should include proposal id');
assert.ok(humanOutput.includes('human-review'), 'human output should include template id');
assert.ok(humanOutput.includes('proposed'), 'human output should include status');
assert.ok(humanOutput.includes('externalWrite'), 'human output should mention externalWrite');
assert.ok(humanOutput.includes('false'), 'human output should show false');
assert.ok(humanOutput.includes('worldloops.local'), 'human output should include source');

// ── --json output ─────────────────────────────────────────────────────────────

const jsonOutput = execFileSync(
  process.execPath,
  ['dist/scripts/proposalShow.js', proposal.id, '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: tmpDir }, encoding: 'utf8' }
);

const json = JSON.parse(jsonOutput);

assert.strictEqual(json.ok, true);
assert.strictEqual(json.source, 'worldloops.local');
assert.strictEqual(json.safety.externalWrite, false);
assert.strictEqual(json.proposal.id, proposal.id);
assert.strictEqual(json.proposal.templateId, 'human-review');
assert.strictEqual(json.proposal.status, 'proposed');
assert.strictEqual(json.proposal.externalWrite, false);
assert.strictEqual(json.proposal.requiredReview, true);
assert.strictEqual(json.proposal.source, 'worldloops.local');
assert.ok(Array.isArray(json.proposal.checks), 'proposal should have checks');
assert.ok(json.proposal.checks.length > 0, 'checks should be non-empty');

// ── missing proposal returns PROPOSAL_NOT_FOUND ───────────────────────────────

const missingResult = spawnSync(
  process.execPath,
  ['dist/scripts/proposalShow.js', 'nonexistent-proposal-id'],
  { env: { ...process.env, WORLDLOOPS_DIR: tmpDir }, encoding: 'utf8' }
);

assert.strictEqual(missingResult.status, 1, 'missing proposal should exit non-zero');

const missingJson = JSON.parse(missingResult.stdout);
assert.strictEqual(missingJson.ok, false);
assert.strictEqual(missingJson.error.code, 'PROPOSAL_NOT_FOUND');
assert.ok(Array.isArray(missingJson.error.availableProposalIds), 'should include availableProposalIds');
assert.strictEqual(missingJson.error.availableProposalIds.length, 1);
assert.strictEqual(missingJson.safety.externalWrite, false);

// ── missing proposal-id argument ──────────────────────────────────────────────

const noArgResult = spawnSync(
  process.execPath,
  ['dist/scripts/proposalShow.js'],
  { env: { ...process.env, WORLDLOOPS_DIR: tmpDir }, encoding: 'utf8' }
);

assert.strictEqual(noArgResult.status, 1, 'missing arg should exit non-zero');
const noArgJson = JSON.parse(noArgResult.stdout);
assert.strictEqual(noArgJson.ok, false);
assert.strictEqual(noArgJson.error.code, 'MISSING_PROPOSAL_ID');
assert.strictEqual(noArgJson.safety.externalWrite, false);

console.log('proposalShow tests passed');
