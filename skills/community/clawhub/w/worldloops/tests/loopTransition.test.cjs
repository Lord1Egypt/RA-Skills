const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync, spawnSync } = require('node:child_process');

const {
  buildOpenLoopStateFromProposal,
  saveOpenLoopState,
  findOpenLoopStateById,
} = require('../dist/storage/openLoopStates');

function makeLoop(tmpDir, idempotencyKey, severity = 'high') {
  process.env.WORLDLOOPS_DIR = tmpDir;
  const candidate = {
    idempotencyKey,
    entityType: 'work_signal',
    source: 'gmail',
    currentState: 'open',
    proposedState: 'needs_reply',
    reason: 'follow-up needed',
    approvalRequired: true,
    actionHint: 'Draft a reply',
    severity,
  };
  const signals = [{ source: 'gmail', text: 'Test signal.', createdAt: '2026-05-18T00:00:00.000Z' }];
  const loop = buildOpenLoopStateFromProposal(candidate, signals);
  saveOpenLoopState(loop);
  return loop;
}

// ── valid positional transition (todo -> doing) ───────────────────────────────

const dir1 = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-loop-transition-'));
const loop1 = makeLoop(dir1, 'transition-test-positional');

const positionalResult = execFileSync(
  process.execPath,
  ['dist/scripts/loopTransition.js', loop1.id, 'doing'],
  { env: { ...process.env, WORLDLOOPS_DIR: dir1 }, encoding: 'utf8' }
);

const positionalJson = JSON.parse(positionalResult);
assert.strictEqual(positionalJson.ok, true);
assert.strictEqual(positionalJson.loop.status, 'doing');
assert.strictEqual(positionalJson.safety.externalWrite, false);

// ── valid --to flag transition (todo -> doing) ────────────────────────────────

const dir2 = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-loop-transition-'));
const loop2 = makeLoop(dir2, 'transition-test-to-flag');

const toFlagResult = execFileSync(
  process.execPath,
  ['dist/scripts/loopTransition.js', loop2.id, '--to', 'doing'],
  { env: { ...process.env, WORLDLOOPS_DIR: dir2 }, encoding: 'utf8' }
);

const toFlagJson = JSON.parse(toFlagResult);
assert.strictEqual(toFlagJson.ok, true);
assert.strictEqual(toFlagJson.loop.status, 'doing');
assert.strictEqual(toFlagJson.safety.externalWrite, false);

// ── invalid governed transition (todo -> done is not allowed) ─────────────────

const dir3 = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-loop-transition-'));
const loop3 = makeLoop(dir3, 'transition-test-invalid');

const invalidResult = spawnSync(
  process.execPath,
  ['dist/scripts/loopTransition.js', loop3.id, 'done'],
  { env: { ...process.env, WORLDLOOPS_DIR: dir3 }, encoding: 'utf8' }
);

assert.notStrictEqual(invalidResult.status, 0, 'invalid transition should exit non-zero');
const invalidJson = JSON.parse(invalidResult.stdout);
assert.strictEqual(invalidJson.ok, false);
assert.strictEqual(invalidJson.error.code, 'INVALID_LOOP_TRANSITION');
assert.ok(invalidJson.error.message.includes('todo'), 'error should mention from status');
assert.ok(invalidJson.error.message.includes('done'), 'error should mention to status');
assert.ok(Array.isArray(invalidJson.error.allowedTransitions), 'should include allowedTransitions');
assert.ok(invalidJson.error.allowedTransitions.includes('doing'), 'allowedTransitions should include doing');
assert.strictEqual(invalidJson.safety.externalWrite, false);

// ── invalid governed transition with --to flag ────────────────────────────────

const invalidToFlagResult = spawnSync(
  process.execPath,
  ['dist/scripts/loopTransition.js', loop3.id, '--to', 'snoozed'],
  { env: { ...process.env, WORLDLOOPS_DIR: dir3 }, encoding: 'utf8' }
);

assert.notStrictEqual(invalidToFlagResult.status, 0, 'invalid --to transition should exit non-zero');
const invalidToFlagJson = JSON.parse(invalidToFlagResult.stdout);
assert.strictEqual(invalidToFlagJson.ok, false);
assert.strictEqual(invalidToFlagJson.error.code, 'INVALID_LOOP_TRANSITION');

// ── dry-run: valid transition (todo -> doing) does not commit ─────────────────

const dir4 = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-loop-transition-'));
const loop4 = makeLoop(dir4, 'transition-test-dry-run');

const dryRunResult = execFileSync(
  process.execPath,
  ['dist/scripts/loopTransition.js', loop4.id, '--to', 'doing', '--dry-run'],
  { env: { ...process.env, WORLDLOOPS_DIR: dir4 }, encoding: 'utf8' }
);

const dryRunJson = JSON.parse(dryRunResult);
assert.strictEqual(dryRunJson.ok, true);
assert.strictEqual(dryRunJson.dryRun, true);
assert.strictEqual(dryRunJson.preview.from, 'todo');
assert.strictEqual(dryRunJson.preview.to, 'doing');
assert.strictEqual(dryRunJson.safety.externalWrite, false);

// verify state was NOT actually changed
process.env.WORLDLOOPS_DIR = dir4;
const afterDryRun = findOpenLoopStateById(loop4.id);
assert.strictEqual(afterDryRun.status, 'todo', 'dry-run must not commit state');

// ── dry-run: invalid transition returns error (not committed) ─────────────────

const dryRunInvalidResult = spawnSync(
  process.execPath,
  ['dist/scripts/loopTransition.js', loop4.id, 'done', '--dry-run'],
  { env: { ...process.env, WORLDLOOPS_DIR: dir4 }, encoding: 'utf8' }
);

assert.notStrictEqual(dryRunInvalidResult.status, 0, 'dry-run on invalid transition should exit non-zero');
const dryRunInvalidJson = JSON.parse(dryRunInvalidResult.stdout);
assert.strictEqual(dryRunInvalidJson.ok, false);
assert.strictEqual(dryRunInvalidJson.error.code, 'INVALID_LOOP_TRANSITION');

// ── loop not found ───────────────────────────────────────────────────────────

const dir5 = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-loop-transition-'));

const notFoundResult = spawnSync(
  process.execPath,
  ['dist/scripts/loopTransition.js', 'missing-id', 'doing'],
  { env: { ...process.env, WORLDLOOPS_DIR: dir5 }, encoding: 'utf8' }
);

assert.notStrictEqual(notFoundResult.status, 0, 'missing loop should exit non-zero');
const notFoundJson = JSON.parse(notFoundResult.stdout);
assert.strictEqual(notFoundJson.ok, false);
assert.strictEqual(notFoundJson.error.code, 'LOOP_NOT_FOUND');

// ── full lifecycle: todo -> doing -> done ─────────────────────────────────────

const dir6 = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-loop-transition-'));
const loop6 = makeLoop(dir6, 'transition-test-lifecycle');

execFileSync(process.execPath, ['dist/scripts/loopTransition.js', loop6.id, 'doing'],
  { env: { ...process.env, WORLDLOOPS_DIR: dir6 }, encoding: 'utf8' });

const doneResult = execFileSync(
  process.execPath,
  ['dist/scripts/loopTransition.js', loop6.id, '--to', 'done'],
  { env: { ...process.env, WORLDLOOPS_DIR: dir6 }, encoding: 'utf8' }
);

const doneJson = JSON.parse(doneResult);
assert.strictEqual(doneJson.ok, true);
assert.strictEqual(doneJson.loop.status, 'done');
assert.strictEqual(doneJson.loop.history.length, 3, 'history should have 3 entries (create + doing + done)');

console.log('loopTransition tests passed');
