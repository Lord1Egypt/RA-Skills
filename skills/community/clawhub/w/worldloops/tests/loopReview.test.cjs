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

const emptyDir = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-loop-review-empty-'));

const emptyResult = spawnSync(
  process.execPath,
  ['dist/scripts/loopReview.js'],
  { env: { ...process.env, WORLDLOOPS_DIR: emptyDir }, encoding: 'utf8' }
);

assert.strictEqual(emptyResult.status, 0, `expected exit 0, got: ${emptyResult.stderr}`);
assert.throws(() => JSON.parse(emptyResult.stdout), 'empty default output should not be JSON');
assert.ok(emptyResult.stdout.includes('Loop Lifecycle Review'), 'empty output should include header');
assert.ok(emptyResult.stdout.includes('Total loops: 0'), 'empty output should show 0 total');
assert.ok(emptyResult.stdout.includes('externalWrite: false'), 'empty output should show externalWrite');

// ── empty state --json ───────────────────────────────────────────────────────

const emptyJsonResult = execFileSync(
  process.execPath,
  ['dist/scripts/loopReview.js', '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: emptyDir }, encoding: 'utf8' }
);

const emptyJson = JSON.parse(emptyJsonResult);
assert.strictEqual(emptyJson.ok, true);
assert.strictEqual(emptyJson.review.total, 0);
assert.deepStrictEqual(emptyJson.review.highSeverityLoops, []);
assert.strictEqual(emptyJson.review.suggestedFocus, null);
assert.strictEqual(emptyJson.capabilityBoundary.externalWrite, false);
assert.strictEqual(emptyJson.safety.externalWrite, false);

// ── populated state ──────────────────────────────────────────────────────────

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-loop-review-'));
process.env.WORLDLOOPS_DIR = tmpDir;

const signals = [{ source: 'gmail', text: 'Test signal.', createdAt: '2026-05-18T00:00:00.000Z' }];

const candidates = [
  {
    idempotencyKey: 'review-test-high',
    entityType: 'work_signal',
    source: 'gmail',
    currentState: 'open',
    proposedState: 'needs_reply',
    reason: 'follow-up needed',
    approvalRequired: true,
    actionHint: 'Reply to customer A',
    severity: 'high',
  },
  {
    idempotencyKey: 'review-test-low',
    entityType: 'work_signal',
    source: 'slack',
    currentState: 'open',
    proposedState: 'needs_review',
    reason: 'review needed',
    approvalRequired: false,
    actionHint: 'Review PR',
    severity: 'low',
  },
  {
    idempotencyKey: 'review-test-critical',
    entityType: 'work_signal',
    source: 'slack',
    currentState: 'open',
    proposedState: 'needs_escalation',
    reason: 'critical issue',
    approvalRequired: true,
    actionHint: 'Escalate immediately',
    severity: 'critical',
  },
];

for (const c of candidates) {
  saveOpenLoopState(buildOpenLoopStateFromProposal(c, signals));
}

// ── human-readable output (default) ──────────────────────────────────────────

const humanResult = execFileSync(
  process.execPath,
  ['dist/scripts/loopReview.js'],
  { env: { ...process.env, WORLDLOOPS_DIR: tmpDir }, encoding: 'utf8' }
);

assert.throws(() => JSON.parse(humanResult), 'default output should not be JSON');
assert.ok(humanResult.includes('Loop Lifecycle Review'), 'output should include header');
assert.ok(humanResult.includes('Total loops: 3'), 'output should show correct total');
assert.ok(humanResult.includes('By status:'), 'output should show status section');
assert.ok(humanResult.includes('High severity loops:'), 'output should show high severity section');
assert.ok(humanResult.includes('externalWrite: false'), 'output should show externalWrite:false');
assert.ok(humanResult.includes('Suggested focus:'), 'output should show suggested focus');

// ── --json output ─────────────────────────────────────────────────────────────

const jsonResult = execFileSync(
  process.execPath,
  ['dist/scripts/loopReview.js', '--json'],
  { env: { ...process.env, WORLDLOOPS_DIR: tmpDir }, encoding: 'utf8' }
);

const json = JSON.parse(jsonResult);
assert.strictEqual(json.ok, true);
assert.strictEqual(json.source, 'worldloops.local');
assert.strictEqual(json.review.total, 3);
assert.ok(json.review.byStatus, 'should include byStatus');
// critical auto-escalates to 'escalated', high and low go to 'todo'
assert.strictEqual(json.review.byStatus.todo, 2, 'todo should be 2 (high + low)');
assert.strictEqual(json.review.byStatus.escalated, 1, 'escalated should be 1 (critical)');
assert.ok(Array.isArray(json.review.highSeverityLoops), 'should include highSeverityLoops array');
assert.ok(json.review.highSeverityLoops.length >= 1, 'should have at least 1 high severity loop');
assert.strictEqual(json.capabilityBoundary.externalWrite, false);
assert.strictEqual(json.capabilityBoundary.mode, 'safe_by_default');
assert.strictEqual(json.safety.externalWrite, false);

// high severity loops should not include low-severity loop
const titles = json.review.highSeverityLoops.map((l) => l.title);
assert.ok(!titles.includes('Review PR'), 'high severity list should not include low severity loop');

console.log('loopReview tests passed');
