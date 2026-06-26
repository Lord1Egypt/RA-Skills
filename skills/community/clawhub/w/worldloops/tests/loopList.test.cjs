const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync, spawnSync } = require('node:child_process');

const {
  buildOpenLoopStateFromProposal,
  saveOpenLoopState,
} = require('../dist/storage/openLoopStates');

// ── empty state ──────────────────────────────────────────────────────────────

const emptyDir = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-loop-list-empty-'));

const emptyResult = spawnSync(
  process.execPath,
  ['dist/scripts/loopList.js'],
  {
    env: { ...process.env, WORLDLOOPS_DIR: emptyDir },
    encoding: 'utf8',
  }
);

assert.strictEqual(emptyResult.status, 0, `expected exit 0, got ${emptyResult.status}: ${emptyResult.stderr}`);
assert.ok(
  emptyResult.stdout.trim() === 'No open loops found.',
  `expected empty-state message, got: ${JSON.stringify(emptyResult.stdout)}`
);

// ── populated state ──────────────────────────────────────────────────────────

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-loop-list-'));
process.env.WORLDLOOPS_DIR = tmpDir;

const candidate = {
  idempotencyKey: 'gmail-loop-list-test',
  entityType: 'work_signal',
  source: 'gmail',
  currentState: 'open',
  proposedState: 'needs_reply',
  reason: 'follow-up needed',
  approvalRequired: true,
  actionHint: 'Draft a reply to the customer',
  severity: 'high',
};

const signals = [
  {
    source: 'gmail',
    text: 'Please reply to this customer.',
    createdAt: '2026-05-18T00:00:00.000Z',
  },
];

const loop = buildOpenLoopStateFromProposal(candidate, signals);
saveOpenLoopState(loop);

// ── compact table (default) ──────────────────────────────────────────────────

const tableResult = execFileSync(
  process.execPath,
  ['dist/scripts/loopList.js'],
  {
    env: { ...process.env, WORLDLOOPS_DIR: tmpDir },
    encoding: 'utf8',
  }
);

// must NOT be JSON
assert.throws(
  () => JSON.parse(tableResult),
  'default output should not be valid JSON'
);

// must contain key columns
assert.ok(tableResult.includes(loop.id), 'table should include loop id');
assert.ok(tableResult.includes(loop.status), 'table should include status');
assert.ok(tableResult.includes(loop.severity), 'table should include severity');
assert.ok(tableResult.includes('Draft a reply'), 'table should include truncated title');
assert.ok(tableResult.includes('UPDATED AT'), 'table should include header');

// ── --json flag ──────────────────────────────────────────────────────────────

const jsonOutput = execFileSync(
  process.execPath,
  ['dist/scripts/loopList.js', '--json'],
  {
    env: { ...process.env, WORLDLOOPS_DIR: tmpDir },
    encoding: 'utf8',
  }
);

const parsed = JSON.parse(jsonOutput);

assert.strictEqual(parsed.ok, true);
assert.strictEqual(parsed.source, 'worldloops.local');
assert.strictEqual(parsed.count, 1);
assert.strictEqual(parsed.loops.length, 1);
assert.strictEqual(parsed.loops[0].id, loop.id);
assert.strictEqual(parsed.loops[0].status, loop.status);
assert.strictEqual(parsed.loops[0].severity, loop.severity);
assert.strictEqual(parsed.safety.externalWrite, false);
assert.ok(parsed.capabilityBoundary, '--json output should include capabilityBoundary');
assert.ok(parsed.path, '--json output should include path');

// ── filter tests ─────────────────────────────────────────────────────────────

const filterDir = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-loop-list-filter-'));

const filterSignals = [
  { source: 'gmail', text: 'Test signal.', createdAt: '2026-05-18T00:00:00.000Z' },
];

const highCandidate = {
  idempotencyKey: 'filter-test-high',
  entityType: 'work_signal',
  source: 'gmail',
  currentState: 'open',
  proposedState: 'needs_reply',
  reason: 'high severity loop',
  approvalRequired: true,
  actionHint: 'High severity task to action',
  severity: 'high',
};

const lowCandidate = {
  idempotencyKey: 'filter-test-low',
  entityType: 'work_signal',
  source: 'slack',
  currentState: 'open',
  proposedState: 'needs_review',
  reason: 'low severity loop',
  approvalRequired: false,
  actionHint: 'Low severity task to track',
  severity: 'low',
};

process.env.WORLDLOOPS_DIR = filterDir;
const highLoop = buildOpenLoopStateFromProposal(highCandidate, filterSignals);
const lowLoop = buildOpenLoopStateFromProposal(lowCandidate, filterSignals);
saveOpenLoopState(highLoop);
saveOpenLoopState(lowLoop);

// ── severity filter (table) ───────────────────────────────────────────────────

const severityFilterResult = execFileSync(
  process.execPath,
  ['dist/scripts/loopList.js', '--severity', 'high'],
  { env: { ...process.env, WORLDLOOPS_DIR: filterDir }, encoding: 'utf8' }
);

assert.ok(severityFilterResult.includes(highLoop.id), 'severity filter should include high loop');
assert.ok(!severityFilterResult.includes(lowLoop.id), 'severity filter should exclude low loop');

// ── severity filter (--json) ──────────────────────────────────────────────────

const severityJsonOutput = execFileSync(
  process.execPath,
  ['dist/scripts/loopList.js', '--severity', 'high', '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: filterDir }, encoding: 'utf8' }
);

const severityParsed = JSON.parse(severityJsonOutput);
assert.strictEqual(severityParsed.ok, true);
assert.strictEqual(severityParsed.count, 1);
assert.strictEqual(severityParsed.loops.length, 1);
assert.strictEqual(severityParsed.filters.severity, 'high');
assert.strictEqual(severityParsed.safety.externalWrite, false);
assert.ok(severityParsed.capabilityBoundary, 'filtered --json should include capabilityBoundary');

// ── status filter (table) ────────────────────────────────────────────────────

const statusFilterResult = execFileSync(
  process.execPath,
  ['dist/scripts/loopList.js', '--status', 'todo'],
  { env: { ...process.env, WORLDLOOPS_DIR: filterDir }, encoding: 'utf8' }
);

assert.ok(statusFilterResult.includes(highLoop.id), 'status filter todo should include high loop');
assert.ok(statusFilterResult.includes(lowLoop.id), 'status filter todo should include low loop');

// ── combined status + severity filter (table) ────────────────────────────────

const combinedResult = execFileSync(
  process.execPath,
  ['dist/scripts/loopList.js', '--status', 'todo', '--severity', 'high'],
  { env: { ...process.env, WORLDLOOPS_DIR: filterDir }, encoding: 'utf8' }
);

assert.ok(combinedResult.includes(highLoop.id), 'combined filter should include high loop');
assert.ok(!combinedResult.includes(lowLoop.id), 'combined filter should exclude low loop');

// ── combined status + severity filter (--json) ───────────────────────────────

const combinedJsonOutput = execFileSync(
  process.execPath,
  ['dist/scripts/loopList.js', '--status', 'todo', '--severity', 'high', '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: filterDir }, encoding: 'utf8' }
);

const combinedParsed = JSON.parse(combinedJsonOutput);
assert.strictEqual(combinedParsed.ok, true);
assert.strictEqual(combinedParsed.filters.status, 'todo');
assert.strictEqual(combinedParsed.filters.severity, 'high');
assert.strictEqual(combinedParsed.safety.externalWrite, false);

// ── no matching filtered loops ────────────────────────────────────────────────

const noMatchResult = spawnSync(
  process.execPath,
  ['dist/scripts/loopList.js', '--status', 'done'],
  { env: { ...process.env, WORLDLOOPS_DIR: filterDir }, encoding: 'utf8' }
);

assert.strictEqual(noMatchResult.status, 0, `expected exit 0, got ${noMatchResult.status}`);
assert.ok(
  noMatchResult.stdout.trim() === 'No open loops matched the selected filters.',
  `expected filter empty-state message, got: ${JSON.stringify(noMatchResult.stdout)}`
);

// ── no matching filtered loops (--json) ──────────────────────────────────────

const noMatchJsonOutput = execFileSync(
  process.execPath,
  ['dist/scripts/loopList.js', '--status', 'done', '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: filterDir }, encoding: 'utf8' }
);

const noMatchParsed = JSON.parse(noMatchJsonOutput);
assert.strictEqual(noMatchParsed.ok, true);
assert.strictEqual(noMatchParsed.count, 0);
assert.deepStrictEqual(noMatchParsed.loops, []);
assert.strictEqual(noMatchParsed.filters.status, 'done');
assert.strictEqual(noMatchParsed.safety.externalWrite, false);

// ── invalid status filter ─────────────────────────────────────────────────────

const invalidStatusResult = spawnSync(
  process.execPath,
  ['dist/scripts/loopList.js', '--status', 'invalid'],
  { env: { ...process.env, WORLDLOOPS_DIR: filterDir }, encoding: 'utf8' }
);

assert.notStrictEqual(invalidStatusResult.status, 0, 'invalid status should exit non-zero');
const invalidStatusParsed = JSON.parse(invalidStatusResult.stdout);
assert.strictEqual(invalidStatusParsed.ok, false);
assert.strictEqual(invalidStatusParsed.error.code, 'INVALID_STATUS_FILTER');
assert.ok(
  invalidStatusParsed.error.message.includes('invalid'),
  'error message should include the bad value'
);
assert.ok(Array.isArray(invalidStatusParsed.allowed), 'should include allowed values array');
assert.ok(invalidStatusParsed.allowed.includes('todo'), 'allowed should include todo');
assert.strictEqual(invalidStatusParsed.capabilityBoundary.externalWrite, false);

// ── invalid severity filter ───────────────────────────────────────────────────

const invalidSeverityResult = spawnSync(
  process.execPath,
  ['dist/scripts/loopList.js', '--severity', 'extreme'],
  { env: { ...process.env, WORLDLOOPS_DIR: filterDir }, encoding: 'utf8' }
);

assert.notStrictEqual(invalidSeverityResult.status, 0, 'invalid severity should exit non-zero');
const invalidSeverityParsed = JSON.parse(invalidSeverityResult.stdout);
assert.strictEqual(invalidSeverityParsed.ok, false);
assert.strictEqual(invalidSeverityParsed.error.code, 'INVALID_SEVERITY_FILTER');
assert.ok(
  invalidSeverityParsed.error.message.includes('extreme'),
  'error message should include the bad value'
);
assert.ok(Array.isArray(invalidSeverityParsed.allowed), 'should include allowed values array');
assert.ok(invalidSeverityParsed.allowed.includes('high'), 'allowed should include high');
assert.strictEqual(invalidSeverityParsed.capabilityBoundary.externalWrite, false);

console.log('loopList tests passed');
