const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync } = require('node:child_process');

// ── empty state: human-readable ───────────────────────────────────────────────

const emptyDir = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-proposal-list-'));

const emptyHuman = execFileSync(
  process.execPath,
  ['dist/scripts/proposalList.js'],
  { env: { ...process.env, WORLDLOOPS_DIR: emptyDir }, encoding: 'utf8' }
);

assert.throws(
  () => JSON.parse(emptyHuman),
  'empty human output should not be valid JSON'
);

assert.ok(emptyHuman.includes('No proposals found'), 'empty human output should say no proposals found');
assert.ok(emptyHuman.includes('externalWrite'), 'empty human output should mention externalWrite');
assert.ok(emptyHuman.includes('false'), 'empty human output should show false');

// ── empty state: --json ───────────────────────────────────────────────────────

const emptyJson = execFileSync(
  process.execPath,
  ['dist/scripts/proposalList.js', '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: emptyDir }, encoding: 'utf8' }
);

const emptyJsonParsed = JSON.parse(emptyJson);
assert.strictEqual(emptyJsonParsed.ok, true);
assert.strictEqual(emptyJsonParsed.source, 'worldloops.local');
assert.strictEqual(emptyJsonParsed.count, 0);
assert.ok(Array.isArray(emptyJsonParsed.proposals), 'proposals should be an array');
assert.strictEqual(emptyJsonParsed.proposals.length, 0);
assert.strictEqual(emptyJsonParsed.safety.externalWrite, false);

// ── populated state: create proposals then list ───────────────────────────────

const popDir = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-proposal-list-'));

for (const tid of ['file-write', 'api-call', 'escalation']) {
  execFileSync(
    process.execPath,
    ['dist/scripts/proposalCreate.js', tid, '--json'],
    { env: { ...process.env, WORLDLOOPS_DIR: popDir }, encoding: 'utf8' }
  );
}

// populated human-readable

const popHuman = execFileSync(
  process.execPath,
  ['dist/scripts/proposalList.js'],
  { env: { ...process.env, WORLDLOOPS_DIR: popDir }, encoding: 'utf8' }
);

assert.throws(
  () => JSON.parse(popHuman),
  'populated human output should not be valid JSON'
);

assert.ok(popHuman.includes('file-write'), 'human output should include file-write');
assert.ok(popHuman.includes('api-call'), 'human output should include api-call');
assert.ok(popHuman.includes('escalation'), 'human output should include escalation');
assert.ok(popHuman.includes('externalWrite'), 'human output should mention externalWrite');

// populated --json

const popJson = execFileSync(
  process.execPath,
  ['dist/scripts/proposalList.js', '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: popDir }, encoding: 'utf8' }
);

const popJsonParsed = JSON.parse(popJson);
assert.strictEqual(popJsonParsed.ok, true);
assert.strictEqual(popJsonParsed.count, 3);
assert.strictEqual(popJsonParsed.proposals.length, 3);
assert.strictEqual(popJsonParsed.safety.externalWrite, false);

for (const p of popJsonParsed.proposals) {
  assert.strictEqual(p.externalWrite, false, `proposal ${p.id} externalWrite must be false`);
  assert.strictEqual(p.status, 'proposed', `proposal ${p.id} status must be proposed`);
}

console.log('proposalList tests passed');
