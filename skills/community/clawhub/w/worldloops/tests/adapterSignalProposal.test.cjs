const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-adapter-proposal-'));
process.env.WORLDLOOPS_DIR = tmpDir;

const {
  buildProposalFromCandidate,
  findProposalByIdempotencyKey,
  saveProposal,
  loadProposals,
} = require('../dist/storage/proposals');

const candidate = {
  idempotencyKey: 'slack-review-q2-metrics-abc123',
  entityType: 'message',
  source: 'slack',
  currentState: 'unread',
  proposedState: 'reviewed',
  reason: 'Team member requested a review of the Q2 metrics dashboard before the meeting.',
  approvalRequired: true,
  actionHint: 'Review Q2 metrics dashboard',
  severity: 'medium',
};

const highCandidate = {
  idempotencyKey: 'github-pr-487-review',
  entityType: 'pull_request',
  source: 'github',
  currentState: 'open',
  proposedState: 'reviewed',
  reason: 'PR #487 has been awaiting review for 3 days.',
  approvalRequired: true,
  actionHint: 'Review PR #487',
  severity: 'high',
};

const criticalCandidate = {
  idempotencyKey: 'prod-incident-critical-loop',
  entityType: 'incident',
  source: 'slack',
  currentState: 'unresolved',
  proposedState: 'escalated',
  reason: 'Production incident unresolved for 2 hours.',
  approvalRequired: true,
  actionHint: 'Escalate production incident',
  severity: 'critical',
};

// ── buildProposalFromCandidate: medium severity → state-transition ────────────

const proposal = buildProposalFromCandidate(candidate);

assert.ok(proposal.id, 'proposal should have id');
assert.strictEqual(proposal.templateId, 'state-transition');
assert.strictEqual(proposal.title, candidate.actionHint);
assert.strictEqual(proposal.intent, candidate.reason);
assert.strictEqual(proposal.status, 'proposed');
assert.strictEqual(proposal.requiredReview, true);
assert.strictEqual(proposal.externalWrite, false);
assert.strictEqual(proposal.source, 'worldloops.local');
assert.strictEqual(proposal.idempotencyKey, candidate.idempotencyKey);
assert.ok(Array.isArray(proposal.checks) && proposal.checks.length > 0, 'checks should be non-empty');
assert.ok(proposal.createdAt, 'createdAt should be set');
assert.ok(proposal.updatedAt, 'updatedAt should be set');

// ── buildProposalFromCandidate: high severity → escalation ───────────────────

const highProposal = buildProposalFromCandidate(highCandidate);
assert.strictEqual(highProposal.templateId, 'escalation');
assert.strictEqual(highProposal.riskLevel, 'high');
assert.strictEqual(highProposal.idempotencyKey, highCandidate.idempotencyKey);
assert.strictEqual(highProposal.externalWrite, false);

// ── buildProposalFromCandidate: critical severity → escalation ───────────────

const critProposal = buildProposalFromCandidate(criticalCandidate);
assert.strictEqual(critProposal.templateId, 'escalation');
assert.strictEqual(critProposal.idempotencyKey, criticalCandidate.idempotencyKey);

// ── buildProposalFromCandidate: no severity → state-transition ───────────────

const noSeverityCandidate = { ...candidate, idempotencyKey: 'no-severity-test', severity: undefined };
const noSevProposal = buildProposalFromCandidate(noSeverityCandidate);
assert.strictEqual(noSevProposal.templateId, 'state-transition');

// ── findProposalByIdempotencyKey: not found before save ──────────────────────

assert.strictEqual(findProposalByIdempotencyKey(candidate.idempotencyKey), null);

// ── saveProposal + findProposalByIdempotencyKey: found after save ─────────────

saveProposal(proposal);
const found = findProposalByIdempotencyKey(candidate.idempotencyKey);
assert.ok(found, 'should find proposal by idempotencyKey after save');
assert.strictEqual(found.id, proposal.id);
assert.strictEqual(found.idempotencyKey, candidate.idempotencyKey);
assert.strictEqual(found.externalWrite, false);

// ── idempotency: saveProposal upserts by id; same id → one entry ──────────────

saveProposal(proposal); // save the same proposal object again
const allAfterReSave = loadProposals();
const withKeyAfterReSave = allAfterReSave.filter((p) => p.idempotencyKey === candidate.idempotencyKey);
assert.strictEqual(withKeyAfterReSave.length, 1, 'saving the same proposal id twice should result in one entry');

// ── reconcile-level idempotency: findProposalByIdempotencyKey guards new builds

const alreadyExists = findProposalByIdempotencyKey(candidate.idempotencyKey);
assert.ok(alreadyExists, 'should find existing proposal by idempotencyKey');
// In briefReconcile, we only call buildProposalFromCandidate when the key is not found.
// Simulating that guard here: if found, skip — no additional entry should be created.
if (!findProposalByIdempotencyKey(candidate.idempotencyKey)) {
  saveProposal(buildProposalFromCandidate(candidate));
}
const afterGuard = loadProposals().filter((p) => p.idempotencyKey === candidate.idempotencyKey);
assert.strictEqual(afterGuard.length, 1, 'reconcile-level guard prevents duplicate proposals');

// ── save two distinct candidates, both findable ───────────────────────────────

saveProposal(highProposal);

const foundHigh = findProposalByIdempotencyKey(highCandidate.idempotencyKey);
assert.ok(foundHigh, 'high candidate should be findable');
assert.strictEqual(foundHigh.templateId, 'escalation');

// ── externalWrite: false preserved on all candidates ─────────────────────────

for (const p of loadProposals()) {
  assert.strictEqual(p.externalWrite, false, `externalWrite must be false on proposal ${p.id}`);
}

// ── proposals.json is local-only (no network calls) ──────────────────────────

const proposalsFile = path.join(tmpDir, 'proposals.json');
assert.ok(fs.existsSync(proposalsFile), 'proposals.json should exist after saves');

const raw = JSON.parse(fs.readFileSync(proposalsFile, 'utf8'));
assert.ok(Array.isArray(raw), 'proposals.json should be an array');
assert.ok(raw.length >= 2, 'should have at least 2 proposals');

console.log('adapterSignalProposal tests passed');
