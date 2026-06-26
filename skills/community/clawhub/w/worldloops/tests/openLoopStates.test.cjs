const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-open-loops-'));
process.env.WORLDLOOPS_DIR = tmpDir;

const {
  buildOpenLoopStateFromProposal,
  saveOpenLoopState,
  loadOpenLoopStates,
  transitionOpenLoopState,
  getOpenLoopStatesPath,
  selectRelevantSignalsForProposal,
} = require('../dist/storage/openLoopStates');

const candidate = {
  idempotencyKey: 'gmail-review-pr-123',
  entityType: 'review_request',
  source: 'gmail',
  currentState: 'needs_review',
  proposedState: 'resolved',
  reason: 'User was asked to review a PR.',
  approvalRequired: true,
  actionHint: 'Review PR #123',
  severity: 'high',
};

const signals = [
  {
    source: 'gmail',
    text: 'Can you review PR #123 today?',
    url: 'https://example.com/email/1',
    createdAt: '2026-05-18T00:00:00.000Z',
  },
  {
    source: 'calendar',
    text: 'Unrelated calendar prep item',
    url: 'https://example.com/calendar/1',
    createdAt: '2026-05-18T01:00:00.000Z',
  },
];

const loop = buildOpenLoopStateFromProposal(candidate, signals);

assert.strictEqual(loop.status, 'todo');
assert.strictEqual(loop.severity, 'high');
assert.strictEqual(loop.adjudication.action, 'require_approval');
assert.strictEqual(loop.adjudication.approvalRequired, true);
assert.strictEqual(loop.adjudication.safety.externalWrite, false);
assert.strictEqual(loop.safety.externalWrite, false);
assert.strictEqual(loop.history.length, 1);
assert.strictEqual(loop.sourceSignals.length, 1);
assert.strictEqual(loop.sourceSignals[0].source, 'gmail');
assert.strictEqual(loop.sourceSignals[0].text, 'Can you review PR #123 today?');

const relevantSignals = selectRelevantSignalsForProposal(candidate, signals);
assert.strictEqual(relevantSignals.length, 1);
assert.strictEqual(relevantSignals[0].source, 'gmail');

const fallbackSignals = selectRelevantSignalsForProposal(
  { ...candidate, source: 'github' },
  signals
);
assert.strictEqual(fallbackSignals.length, 1);
assert.strictEqual(fallbackSignals[0].source, 'gmail');

saveOpenLoopState(loop);

const loaded = loadOpenLoopStates();
assert.strictEqual(loaded.length, 1);
assert.strictEqual(loaded[0].canonicalKey, 'gmail-review-pr-123');

const transitioned = transitionOpenLoopState(loop.id, 'doing', {
  actor: 'test',
  note: 'Started locally',
});

assert.strictEqual(transitioned.status, 'doing');
assert.strictEqual(transitioned.history.length, 2);
assert.strictEqual(transitioned.history[1].from, 'todo');
assert.strictEqual(transitioned.history[1].to, 'doing');
assert.strictEqual(transitioned.safety.externalWrite, false);

assert.ok(fs.existsSync(getOpenLoopStatesPath()));

console.log('openLoopStates tests passed');
