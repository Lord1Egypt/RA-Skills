const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const { checkWorldState } = require('../dist/state/checkWorldState');

function mkTmp(label) {
  return fs.mkdtempSync(path.join(os.tmpdir(), `worldloops-state-check-${label}-`));
}

function writeJson(dir, filename, data) {
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, filename), JSON.stringify(data, null, 2) + '\n', 'utf8');
}

function runStateCheck(dir, extraArgs) {
  return spawnSync(
    process.execPath,
    ['dist/scripts/stateCheck.js', ...(extraArgs ?? [])],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
}

// ── empty / missing .worldloops passes ────────────────────────────────────────

{
  const tmpDir = mkTmp('empty');
  const result = checkWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.ok, true, 'empty dir: should pass');
  assert.strictEqual(result.status, 'passed');
  assert.strictEqual(result.summary.filesChecked, 0);
  assert.strictEqual(result.summary.issues, 0);
  assert.strictEqual(result.safety.externalWrite, false);
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── existing dir with no state files passes ───────────────────────────────────

{
  const tmpDir = mkTmp('existing-empty');
  fs.mkdirSync(tmpDir, { recursive: true });
  const result = checkWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.ok, true, 'existing empty dir: should pass');
  assert.strictEqual(result.summary.filesChecked, 0);
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── valid empty-array state files pass ───────────────────────────────────────

{
  const tmpDir = mkTmp('empty-arrays');
  writeJson(tmpDir, 'open_loop_states.json', []);
  writeJson(tmpDir, 'proposals.json', []);
  writeJson(tmpDir, 'execution_plans.json', []);
  writeJson(tmpDir, 'execution_contracts.json', []);
  writeJson(tmpDir, 'transition_receipts.json', []);
  writeJson(tmpDir, 'proposal_decision_receipts.json', []);
  const result = checkWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.ok, true, 'empty arrays: should pass');
  assert.strictEqual(result.summary.filesChecked, 6);
  assert.strictEqual(result.summary.issues, 0);
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── malformed JSON fails ─────────────────────────────────────────────────────

{
  const tmpDir = mkTmp('malformed');
  fs.mkdirSync(tmpDir, { recursive: true });
  fs.writeFileSync(path.join(tmpDir, 'proposals.json'), '{not valid json', 'utf8');
  const result = checkWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.ok, false, 'malformed JSON: should fail');
  assert.ok(result.issues.some((i) => i.code === 'MALFORMED_JSON'), 'should report MALFORMED_JSON');
  assert.ok(result.issues.some((i) => i.severity === 'error'), 'should have error severity');
  assert.strictEqual(result.safety.externalWrite, false);
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── invalid file shape (object instead of array) fails ───────────────────────

{
  const tmpDir = mkTmp('wrong-shape');
  writeJson(tmpDir, 'proposals.json', { not: 'an array' });
  const result = checkWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.ok, false, 'wrong shape: should fail');
  assert.ok(result.issues.some((i) => i.code === 'INVALID_FILE_SHAPE'), 'should report INVALID_FILE_SHAPE');
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── duplicate loop ids fail ───────────────────────────────────────────────────

{
  const tmpDir = mkTmp('dup-loop');
  const loop = {
    id: 'loop-abc',
    canonicalKey: 'key1',
    title: 'Test',
    sourceSignals: [],
    status: 'todo',
    severity: 'medium',
    adjudication: {},
    owner: null,
    dueAt: null,
    lastObservedAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    history: [],
    safety: { externalWrite: false },
  };
  writeJson(tmpDir, 'open_loop_states.json', [loop, { ...loop }]);
  const result = checkWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.ok, false, 'duplicate loop id: should fail');
  assert.ok(result.issues.some((i) => i.code === 'DUPLICATE_LOOP_ID'), 'should report DUPLICATE_LOOP_ID');
  assert.ok(result.issues.some((i) => i.referenceId === 'loop-abc'), 'should include referenceId');
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── duplicate proposal ids fail ──────────────────────────────────────────────

{
  const tmpDir = mkTmp('dup-proposal');
  const proposal = {
    id: 'prop-abc',
    templateId: 'file-write',
    title: 'Test',
    intent: 'test',
    category: 'file_system',
    riskLevel: 'medium',
    requiredReview: true,
    externalWrite: false,
    checks: [],
    status: 'proposed',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    source: 'worldloops.local',
    idempotencyKey: 'key-1',
  };
  writeJson(tmpDir, 'proposals.json', [proposal, { ...proposal, idempotencyKey: 'key-2' }]);
  const result = checkWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.ok, false, 'duplicate proposal id: should fail');
  assert.ok(result.issues.some((i) => i.code === 'DUPLICATE_PROPOSAL_ID'), 'should report DUPLICATE_PROPOSAL_ID');
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── duplicate idempotencyKey in proposals fails ──────────────────────────────

{
  const tmpDir = mkTmp('dup-idem');
  const base = {
    templateId: 'file-write',
    title: 'Test',
    intent: 'test',
    category: 'file_system',
    riskLevel: 'medium',
    requiredReview: true,
    externalWrite: false,
    checks: [],
    status: 'proposed',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    source: 'worldloops.local',
    idempotencyKey: 'same-key',
  };
  writeJson(tmpDir, 'proposals.json', [
    { ...base, id: 'prop-1' },
    { ...base, id: 'prop-2' },
  ]);
  const result = checkWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.ok, false, 'duplicate idempotencyKey: should fail');
  assert.ok(
    result.issues.some((i) => i.code === 'DUPLICATE_PROPOSAL_IDEMPOTENCY_KEY'),
    'should report DUPLICATE_PROPOSAL_IDEMPOTENCY_KEY'
  );
  assert.ok(
    result.issues.some((i) => i.referenceId === 'same-key'),
    'should include referenceId = same-key'
  );
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── proposals with externalWrite:true fails ───────────────────────────────────

{
  const tmpDir = mkTmp('ew-proposal');
  writeJson(tmpDir, 'proposals.json', [
    {
      id: 'prop-bad',
      templateId: 'api-call',
      title: 'Bad',
      intent: 'bad',
      category: 'external_api',
      riskLevel: 'high',
      requiredReview: true,
      externalWrite: true,
      checks: [],
      status: 'proposed',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      source: 'worldloops.local',
    },
  ]);
  const result = checkWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.ok, false, 'externalWrite:true in proposal: should fail');
  assert.ok(result.issues.some((i) => i.code === 'EXTERNAL_WRITE_VIOLATION'), 'should report EXTERNAL_WRITE_VIOLATION');
  assert.ok(result.issues.some((i) => i.referenceId === 'prop-bad'), 'should include referenceId');
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── plan referencing missing proposal fails ───────────────────────────────────

{
  const tmpDir = mkTmp('plan-missing-prop');
  writeJson(tmpDir, 'proposals.json', []);
  writeJson(tmpDir, 'execution_plans.json', [
    {
      id: 'plan-1',
      proposalId: 'prop-missing',
      templateId: 'file-write',
      title: 'Orphan plan',
      status: 'planned',
      riskLevel: 'medium',
      steps: [],
      externalWrite: false,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      source: 'worldloops.local',
    },
  ]);
  const result = checkWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.ok, false, 'plan missing proposal: should fail');
  assert.ok(result.issues.some((i) => i.code === 'PLAN_MISSING_PROPOSAL'), 'should report PLAN_MISSING_PROPOSAL');
  assert.ok(result.issues.some((i) => i.referenceId === 'prop-missing'), 'should include referenceId');
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── contract referencing missing plan fails ───────────────────────────────────

{
  const tmpDir = mkTmp('contract-missing-plan');
  writeJson(tmpDir, 'execution_plans.json', []);
  writeJson(tmpDir, 'execution_contracts.json', [
    {
      id: 'contract-1',
      planId: 'plan-missing',
      proposalId: 'prop-1',
      templateId: 'file-write',
      title: 'Orphan contract',
      status: 'draft',
      riskLevel: 'medium',
      executionBoundary: { externalWrite: false, allowedBoundary: 'local_commit', deniedCapabilities: [], reason: '' },
      preconditions: [],
      requiredApprovals: [],
      rollbackPlan: { available: false, reason: '' },
      audit: { proposalExists: true, proposalApproved: true, decisionReceiptExists: true, planExists: false, planStatus: '', externalWrite: false },
      externalWrite: false,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      source: 'worldloops.local',
    },
  ]);
  const result = checkWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.ok, false, 'contract missing plan: should fail');
  assert.ok(result.issues.some((i) => i.code === 'CONTRACT_MISSING_PLAN'), 'should report CONTRACT_MISSING_PLAN');
  assert.ok(result.issues.some((i) => i.referenceId === 'plan-missing'), 'should include referenceId');
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── transition receipt externalWrite:true fails ───────────────────────────────

{
  const tmpDir = mkTmp('receipt-ew');
  writeJson(tmpDir, 'transition_receipts.json', [
    {
      id: 'receipt-bad',
      createdAt: new Date().toISOString(),
      proposalId: null,
      sourceSignalsObserved: [],
      normalizedResponsibility: null,
      proposedTransition: null,
      reason: null,
      adjudicationResult: null,
      boundaryCrossed: 'local_commit',
      externalWrite: true,
      actor: null,
      decision: null,
      unresolvedState: null,
      redactions: { applied: false, fields: [] },
    },
  ]);
  const result = checkWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.ok, false, 'receipt externalWrite:true: should fail');
  assert.ok(result.issues.some((i) => i.code === 'EXTERNAL_WRITE_VIOLATION'), 'should report EXTERNAL_WRITE_VIOLATION');
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── decision receipt referencing missing proposal fails ───────────────────────

{
  const tmpDir = mkTmp('dec-receipt-missing-prop');
  writeJson(tmpDir, 'proposals.json', []);
  writeJson(tmpDir, 'proposal_decision_receipts.json', [
    {
      id: 'dr-1',
      proposalId: 'prop-gone',
      templateId: 'file-write',
      decision: 'approved',
      previousStatus: 'proposed',
      newStatus: 'approved',
      actor: 'worldloops.local',
      note: null,
      boundaryCrossed: 'local_commit',
      externalWrite: false,
      createdAt: new Date().toISOString(),
      source: 'worldloops.local',
    },
  ]);
  const result = checkWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.ok, false, 'decision receipt missing proposal: should fail');
  assert.ok(result.issues.some((i) => i.code === 'RECEIPT_MISSING_PROPOSAL'), 'should report RECEIPT_MISSING_PROPOSAL');
  assert.ok(result.issues.some((i) => i.referenceId === 'prop-gone'), 'should include referenceId');
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── duplicate plan ids fail ───────────────────────────────────────────────────

{
  const tmpDir = mkTmp('dup-plan');
  const plan = {
    id: 'plan-same',
    proposalId: 'prop-1',
    templateId: 'file-write',
    title: 'Test plan',
    status: 'planned',
    riskLevel: 'medium',
    steps: [],
    externalWrite: false,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    source: 'worldloops.local',
  };
  writeJson(tmpDir, 'proposals.json', [{ id: 'prop-1', externalWrite: false }]);
  writeJson(tmpDir, 'execution_plans.json', [plan, { ...plan }]);
  const result = checkWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.ok, false, 'duplicate plan id: should fail');
  assert.ok(result.issues.some((i) => i.code === 'DUPLICATE_PLAN_ID'), 'should report DUPLICATE_PLAN_ID');
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── duplicate contract ids fail ───────────────────────────────────────────────

{
  const tmpDir = mkTmp('dup-contract');
  const contract = {
    id: 'contract-same',
    planId: 'plan-1',
    proposalId: 'prop-1',
    templateId: 'file-write',
    title: 'Test',
    status: 'draft',
    riskLevel: 'medium',
    executionBoundary: { externalWrite: false, allowedBoundary: 'local_commit', deniedCapabilities: [], reason: '' },
    preconditions: [],
    requiredApprovals: [],
    rollbackPlan: { available: false, reason: '' },
    audit: { proposalExists: true, proposalApproved: true, decisionReceiptExists: true, planExists: true, planStatus: 'planned', externalWrite: false },
    externalWrite: false,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    source: 'worldloops.local',
  };
  writeJson(tmpDir, 'execution_plans.json', [{ id: 'plan-1', externalWrite: false }]);
  writeJson(tmpDir, 'execution_contracts.json', [contract, { ...contract }]);
  const result = checkWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.ok, false, 'duplicate contract id: should fail');
  assert.ok(result.issues.some((i) => i.code === 'DUPLICATE_CONTRACT_ID'), 'should report DUPLICATE_CONTRACT_ID');
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── valid full state passes ───────────────────────────────────────────────────

{
  const tmpDir = mkTmp('valid-full');
  const propId = 'prop-valid-1';
  const planId = 'plan-valid-1';
  writeJson(tmpDir, 'open_loop_states.json', [
    {
      id: 'loop-1',
      canonicalKey: 'key1',
      title: 'Test loop',
      sourceSignals: [],
      status: 'todo',
      severity: 'medium',
      adjudication: { action: 'propose', externalWrite: false },
      owner: null,
      dueAt: null,
      lastObservedAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      history: [],
      safety: { externalWrite: false },
    },
  ]);
  writeJson(tmpDir, 'proposals.json', [
    {
      id: propId,
      templateId: 'file-write',
      title: 'Test',
      intent: 'test',
      category: 'file_system',
      riskLevel: 'medium',
      requiredReview: true,
      externalWrite: false,
      checks: [],
      status: 'approved',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      source: 'worldloops.local',
      idempotencyKey: 'idem-1',
    },
  ]);
  writeJson(tmpDir, 'execution_plans.json', [
    {
      id: planId,
      proposalId: propId,
      templateId: 'file-write',
      title: 'Test plan',
      status: 'planned',
      riskLevel: 'medium',
      steps: [],
      externalWrite: false,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      source: 'worldloops.local',
    },
  ]);
  writeJson(tmpDir, 'execution_contracts.json', [
    {
      id: 'contract-1',
      planId,
      proposalId: propId,
      templateId: 'file-write',
      title: 'Test contract',
      status: 'draft',
      riskLevel: 'medium',
      executionBoundary: { externalWrite: false, allowedBoundary: 'local_commit', deniedCapabilities: [], reason: '' },
      preconditions: [],
      requiredApprovals: [],
      rollbackPlan: { available: false, reason: '' },
      audit: { proposalExists: true, proposalApproved: true, decisionReceiptExists: true, planExists: true, planStatus: 'planned', externalWrite: false },
      externalWrite: false,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      source: 'worldloops.local',
    },
  ]);
  writeJson(tmpDir, 'transition_receipts.json', [
    {
      id: 'tr-1',
      createdAt: new Date().toISOString(),
      proposalId: propId,
      sourceSignalsObserved: [],
      normalizedResponsibility: null,
      proposedTransition: null,
      reason: null,
      adjudicationResult: null,
      boundaryCrossed: 'local_commit',
      externalWrite: false,
      actor: null,
      decision: null,
      unresolvedState: null,
      redactions: { applied: false, fields: [] },
    },
  ]);
  writeJson(tmpDir, 'proposal_decision_receipts.json', [
    {
      id: 'dr-valid-1',
      proposalId: propId,
      templateId: 'file-write',
      decision: 'approved',
      previousStatus: 'proposed',
      newStatus: 'approved',
      actor: 'worldloops.local',
      note: null,
      boundaryCrossed: 'local_commit',
      externalWrite: false,
      createdAt: new Date().toISOString(),
      source: 'worldloops.local',
    },
  ]);
  const result = checkWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.ok, true, 'valid full state: should pass');
  assert.strictEqual(result.summary.issues, 0);
  assert.strictEqual(result.summary.filesChecked, 6);
  assert.strictEqual(result.safety.externalWrite, false);
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── --json output is valid JSON ───────────────────────────────────────────────

{
  const tmpDir = mkTmp('json-output');
  const proc = runStateCheck(tmpDir, ['--json']);
  const parsed = JSON.parse(proc.stdout);
  assert.ok(typeof parsed === 'object', '--json: output should be an object');
  assert.ok('ok' in parsed, '--json: output should have ok field');
  assert.ok('status' in parsed, '--json: output should have status field');
  assert.ok('summary' in parsed, '--json: output should have summary field');
  assert.ok('issues' in parsed, '--json: output should have issues field');
  assert.ok('safety' in parsed, '--json: output should have safety field');
  assert.strictEqual(parsed.safety.externalWrite, false, '--json: safety.externalWrite must be false');
  assert.ok(Array.isArray(parsed.issues), '--json: issues should be an array');
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── CLI exits 0 on pass, 1 on fail ───────────────────────────────────────────

{
  const passDir = mkTmp('cli-pass');
  const passProc = runStateCheck(passDir, ['--json']);
  assert.strictEqual(passProc.status, 0, 'CLI should exit 0 when passing');
  fs.rmSync(passDir, { recursive: true, force: true });
}

{
  const failDir = mkTmp('cli-fail');
  fs.mkdirSync(failDir, { recursive: true });
  fs.writeFileSync(path.join(failDir, 'proposals.json'), 'bad json!!!', 'utf8');
  const failProc = runStateCheck(failDir, ['--json']);
  assert.strictEqual(failProc.status, 1, 'CLI should exit 1 when failing');
  fs.rmSync(failDir, { recursive: true, force: true });
}

// ── safety.externalWrite is always false ──────────────────────────────────────

{
  const tmpDir = mkTmp('safety');
  const result = checkWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.safety.externalWrite, false, 'safety.externalWrite must always be false');
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── notification_prefs.json malformed fails ───────────────────────────────────

{
  const tmpDir = mkTmp('prefs-malformed');
  fs.mkdirSync(tmpDir, { recursive: true });
  fs.writeFileSync(path.join(tmpDir, 'notification_prefs.json'), '{bad}', 'utf8');
  const result = checkWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.ok, false, 'malformed prefs: should fail');
  assert.ok(result.issues.some((i) => i.code === 'MALFORMED_JSON'), 'should report MALFORMED_JSON for prefs');
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

console.log('stateCheck tests passed');
