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

const emptyDir = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-loop-summary-empty-'));

const emptyResult = spawnSync(
  process.execPath,
  ['dist/scripts/loopSummary.js'],
  {
    env: { ...process.env, WORLDLOOPS_DIR: emptyDir },
    encoding: 'utf8',
  }
);

assert.strictEqual(emptyResult.status, 0, `expected exit 0, got ${emptyResult.status}: ${emptyResult.stderr}`);
assert.ok(
  emptyResult.stdout.includes('Open loop summary'),
  `empty output should include header, got: ${JSON.stringify(emptyResult.stdout)}`
);
assert.ok(
  emptyResult.stdout.includes('total: 0'),
  `empty output should show total: 0, got: ${JSON.stringify(emptyResult.stdout)}`
);
assert.ok(
  emptyResult.stdout.includes('No open loops found.'),
  `empty output should show empty message, got: ${JSON.stringify(emptyResult.stdout)}`
);

// ── populated state ──────────────────────────────────────────────────────────

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-loop-summary-'));
process.env.WORLDLOOPS_DIR = tmpDir;

// high → todo, severity high
// medium → todo, severity medium
// low → todo, severity low
// critical → escalated, severity critical
const candidates = [
  {
    idempotencyKey: 'summary-test-high',
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
    idempotencyKey: 'summary-test-medium',
    entityType: 'work_signal',
    source: 'gmail',
    currentState: 'open',
    proposedState: 'needs_reply',
    reason: 'follow-up needed',
    approvalRequired: false,
    actionHint: 'Reply to customer B',
    severity: 'medium',
  },
  {
    idempotencyKey: 'summary-test-low',
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
    idempotencyKey: 'summary-test-critical',
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

const signals = [{ source: 'gmail', text: 'Test signal', createdAt: '2026-05-18T00:00:00.000Z' }];

for (const candidate of candidates) {
  const loop = buildOpenLoopStateFromProposal(candidate, signals);
  saveOpenLoopState(loop);
}

// ── human-readable output (default) ──────────────────────────────────────────

const humanResult = execFileSync(
  process.execPath,
  ['dist/scripts/loopSummary.js'],
  {
    env: { ...process.env, WORLDLOOPS_DIR: tmpDir },
    encoding: 'utf8',
  }
);

assert.throws(
  () => JSON.parse(humanResult),
  'default output should not be valid JSON'
);

assert.ok(humanResult.includes('Open loop summary'), 'output should include header');
assert.ok(humanResult.includes('total: 4'), 'output should show correct total');
assert.ok(humanResult.includes('by status:'), 'output should show status section');
assert.ok(humanResult.includes('by severity:'), 'output should show severity section');

// ── counts by status ──────────────────────────────────────────────────────────
// high/medium/low → todo (shouldEscalate: false), critical → escalated

assert.ok(humanResult.includes('todo: 3'), 'status count: todo should be 3');
assert.ok(humanResult.includes('doing: 0'), 'status count: doing should be 0');
assert.ok(humanResult.includes('done: 0'), 'status count: done should be 0');
assert.ok(humanResult.includes('snoozed: 0'), 'status count: snoozed should be 0');
assert.ok(humanResult.includes('escalated: 1'), 'status count: escalated should be 1');

// ── counts by severity ────────────────────────────────────────────────────────

assert.ok(humanResult.includes('low: 1'), 'severity count: low should be 1');
assert.ok(humanResult.includes('medium: 1'), 'severity count: medium should be 1');
assert.ok(humanResult.includes('high: 1'), 'severity count: high should be 1');
assert.ok(humanResult.includes('critical: 1'), 'severity count: critical should be 1');

// ── --json output ────────────────────────────────────────────────────────────

const jsonOutput = execFileSync(
  process.execPath,
  ['dist/scripts/loopSummary.js', '--json'],
  {
    env: { ...process.env, WORLDLOOPS_DIR: tmpDir },
    encoding: 'utf8',
  }
);

const parsed = JSON.parse(jsonOutput);

assert.strictEqual(parsed.ok, true);
assert.ok(parsed.summary, '--json output should include summary');
assert.strictEqual(parsed.summary.total, 4, 'JSON total should be 4');
assert.ok(parsed.summary.byStatus, '--json output should include byStatus');
assert.strictEqual(parsed.summary.byStatus.todo, 3, 'JSON byStatus.todo should be 3');
assert.strictEqual(parsed.summary.byStatus.escalated, 1, 'JSON byStatus.escalated should be 1');
assert.ok(parsed.summary.bySeverity, '--json output should include bySeverity');
assert.strictEqual(parsed.summary.bySeverity.high, 1, 'JSON bySeverity.high should be 1');
assert.strictEqual(parsed.summary.bySeverity.critical, 1, 'JSON bySeverity.critical should be 1');
assert.strictEqual(parsed.capabilityBoundary.externalWrite, false, 'externalWrite must be false in JSON output');
assert.strictEqual(parsed.capabilityBoundary.mode, 'safe_by_default', 'mode must be safe_by_default');

console.log('loopSummary tests passed');
