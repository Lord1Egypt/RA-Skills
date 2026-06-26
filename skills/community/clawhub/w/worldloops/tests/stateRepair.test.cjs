const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const { repairWorldState, loadRepairReceipts } = require('../dist/state/repairWorldState');

function mkTmp(label) {
  return fs.mkdtempSync(path.join(os.tmpdir(), `worldloops-repair-${label}-`));
}

function writeJson(dir, filename, data) {
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, filename), JSON.stringify(data, null, 2) + '\n', 'utf8');
}

function readJson(dir, filename) {
  return JSON.parse(fs.readFileSync(path.join(dir, filename), 'utf8'));
}

function fileContents(dir, filename) {
  return fs.readFileSync(path.join(dir, filename), 'utf8');
}

function runStateRepair(dir, extraArgs) {
  return spawnSync(
    process.execPath,
    ['dist/scripts/stateRepair.js', ...(extraArgs ?? [])],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
}

function runStateRepairList(dir, extraArgs) {
  return spawnSync(
    process.execPath,
    ['dist/scripts/stateRepairList.js', ...(extraArgs ?? [])],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
}

function runStateCheck(dir, extraArgs) {
  return spawnSync(
    process.execPath,
    ['dist/scripts/stateCheck.js', ...(extraArgs ?? [])],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
}

function runReceiptsVerify(dir, extraArgs) {
  return spawnSync(
    process.execPath,
    ['dist/scripts/receiptsVerify.js', ...(extraArgs ?? [])],
    { env: { ...process.env, WORLDLOOPS_DIR: dir }, encoding: 'utf8' }
  );
}

// ── dry-run does not modify files ─────────────────────────────────────────────

{
  const tmpDir = mkTmp('dry-no-modify');
  writeJson(tmpDir, 'proposals.json', []);
  writeJson(tmpDir, 'transition_receipts.json', [
    {
      id: 'tr-orphan-1',
      createdAt: new Date().toISOString(),
      proposalId: 'prop-missing',
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

  const beforeReceipts = fileContents(tmpDir, 'transition_receipts.json');
  const beforeProposals = fileContents(tmpDir, 'proposals.json');

  const result = repairWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.mode, 'dry_run', 'default mode should be dry_run');

  assert.strictEqual(
    fileContents(tmpDir, 'transition_receipts.json'),
    beforeReceipts,
    'dry-run must not modify transition_receipts.json'
  );
  assert.strictEqual(
    fileContents(tmpDir, 'proposals.json'),
    beforeProposals,
    'dry-run must not modify proposals.json'
  );
  assert.ok(
    !fs.existsSync(path.join(tmpDir, 'repair_receipts.json')),
    'dry-run must not create repair_receipts.json'
  );

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── apply creates repair receipt ──────────────────────────────────────────────

{
  const tmpDir = mkTmp('apply-creates-receipt');
  writeJson(tmpDir, 'proposals.json', []);
  writeJson(tmpDir, 'transition_receipts.json', [
    {
      id: 'tr-1',
      createdAt: new Date().toISOString(),
      proposalId: 'prop-gone',
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

  const result = repairWorldState({ worldloopsDir: tmpDir, apply: true });
  assert.strictEqual(result.mode, 'apply', 'mode should be apply');
  assert.ok(
    fs.existsSync(path.join(tmpDir, 'repair_receipts.json')),
    'apply must create repair_receipts.json'
  );

  const storedReceipts = readJson(tmpDir, 'repair_receipts.json');
  assert.ok(Array.isArray(storedReceipts), 'repair_receipts.json should be an array');
  assert.strictEqual(storedReceipts.length, 1, 'should have one repair receipt');
  assert.strictEqual(storedReceipts[0].id, result.receipt.id, 'stored receipt id must match result');
  assert.strictEqual(storedReceipts[0].externalWrite, false, 'receipt externalWrite must be false');
  assert.strictEqual(result.receipt.externalWrite, false, 'result receipt externalWrite must be false');
  assert.strictEqual(result.safety.externalWrite, false, 'safety.externalWrite must be false');

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── apply marks orphan receipts without deleting them ─────────────────────────

{
  const tmpDir = mkTmp('apply-orphan-receipt');
  writeJson(tmpDir, 'proposals.json', []);
  writeJson(tmpDir, 'transition_receipts.json', [
    {
      id: 'tr-orphan',
      createdAt: new Date().toISOString(),
      proposalId: 'prop-missing',
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

  repairWorldState({ worldloopsDir: tmpDir, apply: true });

  const receipts = readJson(tmpDir, 'transition_receipts.json');
  assert.strictEqual(receipts.length, 1, 'receipt must not be deleted');
  assert.strictEqual(receipts[0].id, 'tr-orphan', 'receipt id must be preserved');
  assert.strictEqual(receipts[0].proposalId, 'prop-missing', 'proposalId must be preserved');
  assert.strictEqual(receipts[0].externalWrite, false, 'externalWrite must remain false');
  assert.ok(
    typeof receipts[0]._worldloopsRepair === 'object' && receipts[0]._worldloopsRepair !== null,
    'repair metadata must be added'
  );
  assert.strictEqual(receipts[0]._worldloopsRepair.status, 'orphan', 'repair status must be orphan');
  assert.strictEqual(
    receipts[0]._worldloopsRepair.missingProposalId,
    'prop-missing',
    'missingProposalId must be recorded'
  );

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── apply marks unresolved plan references without deleting plan ───────────────

{
  const tmpDir = mkTmp('apply-plan-unresolved');
  writeJson(tmpDir, 'proposals.json', []);
  writeJson(tmpDir, 'execution_plans.json', [
    {
      id: 'plan-orphan',
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

  repairWorldState({ worldloopsDir: tmpDir, apply: true });

  const plans = readJson(tmpDir, 'execution_plans.json');
  assert.strictEqual(plans.length, 1, 'plan must not be deleted');
  assert.strictEqual(plans[0].id, 'plan-orphan', 'plan id must be preserved');
  assert.strictEqual(plans[0].proposalId, 'prop-missing', 'proposalId must be preserved');
  assert.strictEqual(plans[0].externalWrite, false, 'externalWrite must remain false');
  assert.ok(
    typeof plans[0]._worldloopsRepair === 'object' && plans[0]._worldloopsRepair !== null,
    'repair metadata must be added to plan'
  );
  assert.strictEqual(
    plans[0]._worldloopsRepair.status,
    'unresolved_proposal',
    'repair status must be unresolved_proposal'
  );

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── duplicate idempotencyKey is flagged, not deleted ──────────────────────────

{
  const tmpDir = mkTmp('dup-idem-flagged');
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
    idempotencyKey: 'dup-key',
  };
  writeJson(tmpDir, 'proposals.json', [
    { ...base, id: 'prop-dup-1' },
    { ...base, id: 'prop-dup-2' },
  ]);

  const result = repairWorldState({ worldloopsDir: tmpDir, apply: true });

  const proposals = readJson(tmpDir, 'proposals.json');
  assert.strictEqual(proposals.length, 2, 'both proposals must remain (not deleted)');
  assert.ok(
    result.repairs.some((r) => r.code === 'FLAG_DUPLICATE_IDEMPOTENCY_KEY'),
    'FLAG_DUPLICATE_IDEMPOTENCY_KEY must be in repairs'
  );
  assert.ok(
    result.repairs.some((r) => r.referenceId === 'dup-key'),
    'referenceId must be the duplicate key'
  );

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── malformed JSON is reported as non-repairable ──────────────────────────────

{
  const tmpDir = mkTmp('malformed-non-repairable');
  fs.mkdirSync(tmpDir, { recursive: true });
  fs.writeFileSync(path.join(tmpDir, 'proposals.json'), '{not valid json', 'utf8');

  const result = repairWorldState({ worldloopsDir: tmpDir });
  assert.ok(
    result.repairs.some((r) => r.code === 'MALFORMED_JSON' && r.status === 'non_repairable'),
    'MALFORMED_JSON must be non_repairable'
  );
  assert.strictEqual(result.summary.nonRepairableIssues > 0, true, 'must have non-repairable issues');
  assert.strictEqual(result.ok, false, 'ok must be false when non-repairable issues exist');

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── externalWrite:true is reported as non-repairable ─────────────────────────

{
  const tmpDir = mkTmp('ew-non-repairable');
  writeJson(tmpDir, 'proposals.json', [
    {
      id: 'prop-bad-ew',
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

  const result = repairWorldState({ worldloopsDir: tmpDir });
  assert.ok(
    result.repairs.some((r) => r.code === 'EXTERNAL_WRITE_VIOLATION' && r.status === 'non_repairable'),
    'EXTERNAL_WRITE_VIOLATION must be non_repairable'
  );
  assert.strictEqual(result.safety.externalWrite, false, 'safety.externalWrite must always be false');
  assert.strictEqual(result.ok, false, 'ok must be false when non-repairable issues exist');

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── repair:list shows repair receipts ─────────────────────────────────────────

{
  const tmpDir = mkTmp('repair-list');
  writeJson(tmpDir, 'proposals.json', []);
  writeJson(tmpDir, 'transition_receipts.json', [
    {
      id: 'tr-list-test',
      createdAt: new Date().toISOString(),
      proposalId: 'prop-gone',
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

  repairWorldState({ worldloopsDir: tmpDir, apply: true });

  const receipts = loadRepairReceipts({ worldloopsDir: tmpDir });
  assert.strictEqual(receipts.length, 1, 'loadRepairReceipts should return 1 receipt');

  const proc = runStateRepairList(tmpDir, []);
  assert.strictEqual(proc.status, 0, 'state:repair:list should exit 0');
  assert.ok(proc.stdout.includes('repair-'), 'output should include receipt id');

  const jsonProc = runStateRepairList(tmpDir, ['--json']);
  assert.strictEqual(jsonProc.status, 0, 'state:repair:list --json should exit 0');
  const parsed = JSON.parse(jsonProc.stdout);
  assert.ok(Array.isArray(parsed), '--json output should be an array');
  assert.strictEqual(parsed.length, 1, 'should have one receipt in json output');
  assert.strictEqual(parsed[0].externalWrite, false, 'receipt externalWrite must be false');

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── repair:list with no receipts ──────────────────────────────────────────────

{
  const tmpDir = mkTmp('repair-list-empty');
  const proc = runStateRepairList(tmpDir, []);
  assert.strictEqual(proc.status, 0, 'state:repair:list should exit 0 with no receipts');
  assert.ok(proc.stdout.includes('No repair receipts found'), 'should indicate no receipts');
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── --json output is valid ────────────────────────────────────────────────────

{
  const tmpDir = mkTmp('json-output');
  const proc = runStateRepair(tmpDir, ['--dry-run', '--json']);
  assert.strictEqual(proc.status, 0, '--json should exit 0');

  const parsed = JSON.parse(proc.stdout);
  assert.ok('ok' in parsed, 'output must have ok field');
  assert.ok('mode' in parsed, 'output must have mode field');
  assert.ok('summary' in parsed, 'output must have summary field');
  assert.ok('repairs' in parsed, 'output must have repairs field');
  assert.ok('receipt' in parsed, 'output must have receipt field');
  assert.ok('safety' in parsed, 'output must have safety field');
  assert.strictEqual(parsed.mode, 'dry_run', 'mode must be dry_run');
  assert.strictEqual(parsed.safety.externalWrite, false, 'safety.externalWrite must be false');
  assert.strictEqual(parsed.receipt.externalWrite, false, 'receipt.externalWrite must be false');
  assert.ok(Array.isArray(parsed.repairs), 'repairs must be an array');
  assert.ok('issuesObserved' in parsed.summary, 'summary must have issuesObserved');
  assert.ok('repairableIssues' in parsed.summary, 'summary must have repairableIssues');
  assert.ok('nonRepairableIssues' in parsed.summary, 'summary must have nonRepairableIssues');
  assert.ok('repairsPlanned' in parsed.summary, 'summary must have repairsPlanned');
  assert.ok('repairsApplied' in parsed.summary, 'summary must have repairsApplied');

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── apply --json output is valid ──────────────────────────────────────────────

{
  const tmpDir = mkTmp('apply-json-output');
  writeJson(tmpDir, 'proposals.json', []);

  const proc = runStateRepair(tmpDir, ['--apply', '--json']);
  assert.strictEqual(proc.status, 0, 'apply --json should exit 0');

  const parsed = JSON.parse(proc.stdout);
  assert.strictEqual(parsed.mode, 'apply', 'mode must be apply');
  assert.strictEqual(parsed.safety.externalWrite, false, 'safety.externalWrite must be false');

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── state:check still works after repair ──────────────────────────────────────

{
  const tmpDir = mkTmp('check-after-repair');
  const propId = 'prop-still-valid';
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
    },
  ]);
  writeJson(tmpDir, 'execution_plans.json', [
    {
      id: 'plan-1',
      proposalId: 'prop-gone-for-repair',
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

  repairWorldState({ worldloopsDir: tmpDir, apply: true });

  const checkProc = runStateCheck(tmpDir, ['--json']);
  const checkResult = JSON.parse(checkProc.stdout);
  assert.ok('ok' in checkResult, 'state:check should still produce valid output after repair');
  assert.strictEqual(checkResult.safety.externalWrite, false, 'state:check safety must still be false');

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── receipts:verify still works after repair ──────────────────────────────────

{
  const tmpDir = mkTmp('verify-after-repair');
  writeJson(tmpDir, 'proposals.json', []);
  writeJson(tmpDir, 'transition_receipts.json', [
    {
      id: 'tr-verify',
      createdAt: new Date().toISOString(),
      proposalId: 'prop-gone-verify',
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

  repairWorldState({ worldloopsDir: tmpDir, apply: true });

  const verifyProc = runReceiptsVerify(tmpDir, ['--json']);
  const verifyResult = JSON.parse(verifyProc.stdout);
  assert.ok('ok' in verifyResult, 'receipts:verify should still produce valid output after repair');
  assert.strictEqual(verifyResult.safety.externalWrite, false, 'receipts:verify safety must still be false');

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── default mode is dry-run ───────────────────────────────────────────────────

{
  const tmpDir = mkTmp('default-dry-run');
  writeJson(tmpDir, 'proposals.json', []);
  writeJson(tmpDir, 'transition_receipts.json', [
    {
      id: 'tr-default',
      createdAt: new Date().toISOString(),
      proposalId: 'prop-missing-default',
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

  const proc = runStateRepair(tmpDir, []);
  assert.strictEqual(proc.status, 0, 'default (no flags) should exit 0');
  assert.ok(proc.stdout.includes('dry-run'), 'default output should say dry-run');
  assert.ok(proc.stdout.includes('No files were modified'), 'should say no files were modified');
  assert.ok(
    !fs.existsSync(path.join(tmpDir, 'repair_receipts.json')),
    'default mode must not create repair_receipts.json'
  );

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── apply accumulates multiple repair receipts ────────────────────────────────

{
  const tmpDir = mkTmp('multiple-receipts');
  writeJson(tmpDir, 'proposals.json', []);
  writeJson(tmpDir, 'transition_receipts.json', [
    {
      id: 'tr-multi-1',
      createdAt: new Date().toISOString(),
      proposalId: 'prop-missing-multi',
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

  repairWorldState({ worldloopsDir: tmpDir, apply: true });
  repairWorldState({ worldloopsDir: tmpDir, apply: true });

  const receipts = readJson(tmpDir, 'repair_receipts.json');
  assert.strictEqual(receipts.length, 2, 'should accumulate two repair receipts');
  assert.notStrictEqual(receipts[0].id, receipts[1].id, 'receipt ids must be unique');

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── skipped when already marked ───────────────────────────────────────────────

{
  const tmpDir = mkTmp('already-marked');
  writeJson(tmpDir, 'proposals.json', []);
  writeJson(tmpDir, 'transition_receipts.json', [
    {
      id: 'tr-pre-marked',
      createdAt: new Date().toISOString(),
      proposalId: 'prop-missing-marked',
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
      _worldloopsRepair: { status: 'orphan', missingProposalId: 'prop-missing-marked', repairedAt: new Date().toISOString(), repairReceiptId: 'repair-prior' },
    },
  ]);

  const result = repairWorldState({ worldloopsDir: tmpDir, apply: true });
  assert.ok(
    result.repairs.some((r) => r.status === 'skipped'),
    'already-marked receipt should be skipped'
  );

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── clean state has no repairs ────────────────────────────────────────────────

{
  const tmpDir = mkTmp('clean-state');
  const propId = 'prop-clean';
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
    },
  ]);
  writeJson(tmpDir, 'transition_receipts.json', [
    {
      id: 'tr-clean',
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

  const result = repairWorldState({ worldloopsDir: tmpDir });
  assert.strictEqual(result.ok, true, 'clean state should be ok');
  assert.strictEqual(result.repairs.length, 0, 'clean state should have no repairs');
  assert.strictEqual(result.summary.issuesObserved, 0, 'clean state should have 0 issues observed');

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── state:check reclassifies repaired orphan transition receipts ──────────────

{
  const tmpDir = mkTmp('check-repaired-trans-receipt');
  writeJson(tmpDir, 'proposals.json', []);
  writeJson(tmpDir, 'transition_receipts.json', [
    {
      id: 'tr-check-orphan',
      createdAt: new Date().toISOString(),
      proposalId: 'prop-check-gone',
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

  repairWorldState({ worldloopsDir: tmpDir, apply: true });

  const checkProc = runStateCheck(tmpDir, ['--json']);
  assert.strictEqual(checkProc.status, 0, 'state:check should exit 0 after repair (no errors)');
  const checkResult = JSON.parse(checkProc.stdout);

  assert.ok(
    !checkResult.issues.some((i) => i.code === 'RECEIPT_MISSING_PROPOSAL'),
    'state:check must not report RECEIPT_MISSING_PROPOSAL for repaired orphan'
  );
  assert.ok(
    checkResult.issues.some((i) => i.code === 'REPAIRED_ORPHAN_RECEIPT'),
    'state:check must report REPAIRED_ORPHAN_RECEIPT for repaired orphan'
  );
  assert.ok(
    checkResult.issues.some((i) => i.severity === 'info'),
    'repaired orphan receipt must have info severity'
  );
  assert.strictEqual(checkResult.summary.repaired, 1, 'summary.repaired must be 1');
  assert.strictEqual(checkResult.summary.warnings, 0, 'repaired orphan must not count as warning');
  assert.strictEqual(checkResult.ok, true, 'state:check ok must be true after repair (no unrepaired errors)');

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── receipts:verify reclassifies repaired orphan transition receipts ──────────

{
  const tmpDir = mkTmp('verify-repaired-trans-receipt');
  writeJson(tmpDir, 'proposals.json', []);
  writeJson(tmpDir, 'transition_receipts.json', [
    {
      id: 'tr-verify-orphan',
      createdAt: new Date().toISOString(),
      proposalId: 'prop-verify-gone',
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

  repairWorldState({ worldloopsDir: tmpDir, apply: true });

  const verifyProc = runReceiptsVerify(tmpDir, ['--json']);
  assert.strictEqual(verifyProc.status, 0, 'receipts:verify should exit 0 after repair (no errors)');
  const verifyResult = JSON.parse(verifyProc.stdout);

  assert.ok(
    !verifyResult.issues.some((i) => i.code === 'RECEIPT_MISSING_PROPOSAL'),
    'receipts:verify must not report RECEIPT_MISSING_PROPOSAL for repaired orphan'
  );
  assert.ok(
    verifyResult.issues.some((i) => i.code === 'REPAIRED_ORPHAN_RECEIPT'),
    'receipts:verify must report REPAIRED_ORPHAN_RECEIPT for repaired orphan'
  );
  assert.strictEqual(verifyResult.summary.repaired, 1, 'summary.repaired must be 1');
  assert.strictEqual(verifyResult.summary.warnings, 0, 'repaired orphan must not count as warning');
  assert.strictEqual(verifyResult.ok, true, 'receipts:verify ok must be true after repair');

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── state:check reclassifies repaired orphan decision receipts ────────────────

{
  const tmpDir = mkTmp('check-repaired-dec-receipt');
  writeJson(tmpDir, 'proposals.json', []);
  writeJson(tmpDir, 'proposal_decision_receipts.json', [
    {
      id: 'dr-check-orphan',
      proposalId: 'prop-dec-gone',
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

  repairWorldState({ worldloopsDir: tmpDir, apply: true });

  const checkProc = runStateCheck(tmpDir, ['--json']);
  assert.strictEqual(checkProc.status, 0, 'state:check should exit 0 after decision receipt repair');
  const checkResult = JSON.parse(checkProc.stdout);

  assert.ok(
    !checkResult.issues.some((i) => i.code === 'RECEIPT_MISSING_PROPOSAL'),
    'state:check must not report RECEIPT_MISSING_PROPOSAL for repaired orphan decision receipt'
  );
  assert.ok(
    checkResult.issues.some((i) => i.code === 'REPAIRED_ORPHAN_RECEIPT'),
    'state:check must report REPAIRED_ORPHAN_RECEIPT for repaired orphan decision receipt'
  );
  assert.strictEqual(checkResult.summary.repaired, 1, 'summary.repaired must be 1 for repaired decision receipt');
  assert.strictEqual(checkResult.ok, true, 'state:check ok must be true after decision receipt repair');

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── unrepaired orphan receipt still reports RECEIPT_MISSING_PROPOSAL ──────────

{
  const tmpDir = mkTmp('unrepaired-still-warns');
  writeJson(tmpDir, 'proposals.json', []);
  writeJson(tmpDir, 'transition_receipts.json', [
    {
      id: 'tr-unrepaired',
      createdAt: new Date().toISOString(),
      proposalId: 'prop-unrepaired-gone',
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

  // No repair applied — check raw state:check and receipts:verify
  const checkProc = runStateCheck(tmpDir, ['--json']);
  const checkResult = JSON.parse(checkProc.stdout);
  assert.ok(
    checkResult.issues.some((i) => i.code === 'RECEIPT_MISSING_PROPOSAL'),
    'unrepaired orphan must still report RECEIPT_MISSING_PROPOSAL'
  );
  assert.ok(
    !checkResult.issues.some((i) => i.code === 'REPAIRED_ORPHAN_RECEIPT'),
    'unrepaired orphan must not report REPAIRED_ORPHAN_RECEIPT'
  );

  const verifyProc = runReceiptsVerify(tmpDir, ['--json']);
  const verifyResult = JSON.parse(verifyProc.stdout);
  assert.ok(
    verifyResult.issues.some((i) => i.code === 'RECEIPT_MISSING_PROPOSAL'),
    'unrepaired orphan must still report RECEIPT_MISSING_PROPOSAL in receipts:verify'
  );

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

console.log('stateRepair tests passed');
