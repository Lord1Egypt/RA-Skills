const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const { runAdapterTest } = require('../dist/adapter/runAdapterTest');

const root = path.resolve(__dirname, '..');

function makeTmpDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-adapter-test-'));
}

// ── valid core adapter (slack-message.json) passes ───────────────────────────

{
  const tmpDir = makeTmpDir();
  const result = runAdapterTest(
    path.join(root, 'examples/adapters/slack-message.json'),
    { worldloopsDir: tmpDir }
  );

  assert.strictEqual(result.validate, 'passed', 'slack-message: validate should pass');
  assert.strictEqual(result.reconcile, 'passed', 'slack-message: reconcile should pass');
  assert.strictEqual(result.openLoopPersisted, true, 'slack-message: openLoopPersisted should be true');
  assert.strictEqual(result.proposalPersisted, true, 'slack-message: proposalPersisted should be true');
  assert.strictEqual(result.idempotency, 'passed', 'slack-message: idempotency should pass');
  assert.strictEqual(result.externalWrite, false, 'slack-message: externalWrite must be false');
  assert.strictEqual(result.file, path.join(root, 'examples/adapters/slack-message.json'));

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── valid community adapter (linear-issue.example.json) passes ───────────────

{
  const tmpDir = makeTmpDir();
  const result = runAdapterTest(
    path.join(root, 'examples/adapters/community/linear-issue.example.json'),
    { worldloopsDir: tmpDir }
  );

  assert.strictEqual(result.validate, 'passed', 'linear-issue: validate should pass');
  assert.strictEqual(result.reconcile, 'passed', 'linear-issue: reconcile should pass');
  assert.strictEqual(result.openLoopPersisted, true, 'linear-issue: openLoopPersisted should be true');
  assert.strictEqual(result.proposalPersisted, true, 'linear-issue: proposalPersisted should be true');
  assert.strictEqual(result.idempotency, 'passed', 'linear-issue: idempotency should pass');
  assert.strictEqual(result.externalWrite, false, 'linear-issue: externalWrite must be false');

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── invalid externalWrite adapter fails ──────────────────────────────────────

{
  const tmpDir = makeTmpDir();
  const result = runAdapterTest(
    path.join(root, 'examples/adapters/invalid-external-write.json'),
    { worldloopsDir: tmpDir }
  );

  assert.strictEqual(result.validate, 'failed', 'invalid-external-write: validate should fail');
  assert.ok(Array.isArray(result.validateErrors) && result.validateErrors.length > 0,
    'invalid-external-write: validateErrors should be non-empty');
  assert.ok(
    result.validateErrors.some((e) => e.includes('externalWrite')),
    'invalid-external-write: error should mention externalWrite'
  );
  assert.strictEqual(result.reconcile, 'failed', 'invalid-external-write: reconcile should not run');
  assert.strictEqual(result.openLoopPersisted, false, 'invalid-external-write: openLoopPersisted should be false');
  assert.strictEqual(result.proposalPersisted, false, 'invalid-external-write: proposalPersisted should be false');
  assert.strictEqual(result.externalWrite, false, 'invalid-external-write: externalWrite must still be false on result');

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── invalid date adapter fails ────────────────────────────────────────────────

{
  const tmpDir = makeTmpDir();
  const result = runAdapterTest(
    path.join(root, 'examples/adapters/invalid-date.json'),
    { worldloopsDir: tmpDir }
  );

  assert.strictEqual(result.validate, 'failed', 'invalid-date: validate should fail');
  assert.ok(Array.isArray(result.validateErrors) && result.validateErrors.length > 0,
    'invalid-date: validateErrors should be non-empty');
  assert.ok(
    result.validateErrors.some((e) => e.includes('observedAt')),
    'invalid-date: error should mention observedAt'
  );
  assert.strictEqual(result.reconcile, 'failed', 'invalid-date: reconcile should not run');
  assert.strictEqual(result.externalWrite, false);

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── --json mode returns structured output ────────────────────────────────────

{
  const tmpDir = makeTmpDir();
  const result = runAdapterTest(
    path.join(root, 'examples/adapters/slack-message.json'),
    { worldloopsDir: tmpDir }
  );

  const jsonOutput = {
    ok: result.validate === 'passed' &&
        result.reconcile === 'passed' &&
        result.openLoopPersisted === true &&
        result.proposalPersisted === true &&
        result.idempotency === 'passed' &&
        result.externalWrite === false,
    report: result,
    safety: { externalWrite: false },
  };

  assert.strictEqual(jsonOutput.ok, true, '--json: ok should be true for valid adapter');
  assert.ok(typeof jsonOutput.report === 'object', '--json: report should be an object');
  assert.strictEqual(jsonOutput.report.validate, 'passed', '--json: validate should be passed');
  assert.strictEqual(jsonOutput.report.idempotency, 'passed', '--json: idempotency should be passed');
  assert.strictEqual(jsonOutput.safety.externalWrite, false, '--json: safety.externalWrite must be false');

  const serialized = JSON.stringify(jsonOutput, null, 2);
  const parsed = JSON.parse(serialized);
  assert.strictEqual(parsed.ok, true, '--json: serialized output should round-trip correctly');
  assert.strictEqual(parsed.report.externalWrite, false, '--json: externalWrite preserved in serialized output');

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── idempotency check passes ──────────────────────────────────────────────────

{
  const tmpDir = makeTmpDir();

  const firstRun = runAdapterTest(
    path.join(root, 'examples/adapters/slack-message.json'),
    { worldloopsDir: tmpDir }
  );
  assert.strictEqual(firstRun.idempotency, 'passed', 'idempotency: first run should report idempotency passed');
  assert.strictEqual(firstRun.openLoopPersisted, true, 'idempotency: first run should persist open loop');
  assert.strictEqual(firstRun.proposalPersisted, true, 'idempotency: first run should persist proposal');

  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── externalWrite:false is preserved on all results ──────────────────────────

for (const fixture of [
  'examples/adapters/slack-message.json',
  'examples/adapters/invalid-external-write.json',
  'examples/adapters/invalid-date.json',
  'examples/adapters/community/linear-issue.example.json',
]) {
  const tmpDir = makeTmpDir();
  const result = runAdapterTest(path.join(root, fixture), { worldloopsDir: tmpDir });
  assert.strictEqual(result.externalWrite, false, `${fixture}: externalWrite must always be false`);
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── reconcileMode is always local_heuristic ───────────────────────────────────

{
  const tmpDir = makeTmpDir();
  const result = runAdapterTest(
    path.join(root, 'examples/adapters/slack-message.json'),
    { worldloopsDir: tmpDir }
  );
  assert.strictEqual(result.reconcileMode, 'local_heuristic',
    'adapter:test should always report reconcileMode:local_heuristic');
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── Gmail claim contact request fixture: validates and local reconcile passes ─

{
  const tmpDir = makeTmpDir();
  const result = runAdapterTest(
    path.join(root, 'examples/adapters/gmail-claim-contact-request.example.json'),
    { worldloopsDir: tmpDir }
  );
  assert.strictEqual(result.validate, 'passed', 'gmail-claim: validate should pass');
  assert.strictEqual(result.reconcile, 'passed', 'gmail-claim: local reconcile should pass');
  assert.strictEqual(result.openLoopPersisted, true, 'gmail-claim: openLoopPersisted (local heuristic)');
  assert.strictEqual(result.proposalPersisted, true, 'gmail-claim: proposalPersisted (local heuristic)');
  assert.strictEqual(result.idempotency, 'passed', 'gmail-claim: idempotency should pass');
  assert.strictEqual(result.externalWrite, false, 'gmail-claim: externalWrite must be false');
  assert.strictEqual(result.reconcileMode, 'local_heuristic');
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── Gmail claim: receipt aligns with proposal (no RECEIPT_MISSING_PROPOSAL) ──

{
  const os = require('node:os');
  const { checkReceipts } = require('../dist/state/checkWorldState');

  const tmpDir = makeTmpDir();
  runAdapterTest(
    path.join(root, 'examples/adapters/gmail-claim-contact-request.example.json'),
    { worldloopsDir: tmpDir }
  );
  const verifyResult = checkReceipts({ worldloopsDir: tmpDir });
  assert.ok(!verifyResult.issues.some((i) => i.code === 'RECEIPT_MISSING_PROPOSAL'),
    'gmail-claim: receipts:verify should produce no RECEIPT_MISSING_PROPOSAL');
  assert.strictEqual(verifyResult.safety.externalWrite, false);
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ── Gmail working-capital sales fixture: validates, externalWrite:false ───────

{
  const tmpDir = makeTmpDir();
  const result = runAdapterTest(
    path.join(root, 'examples/adapters/gmail-working-capital-sales.example.json'),
    { worldloopsDir: tmpDir }
  );
  assert.strictEqual(result.validate, 'passed', 'sales-outreach: validate should pass');
  assert.strictEqual(result.externalWrite, false, 'sales-outreach: externalWrite must be false');
  assert.strictEqual(result.reconcileMode, 'local_heuristic',
    'sales-outreach: mode is local_heuristic');
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

console.log('adapterTest tests passed');
