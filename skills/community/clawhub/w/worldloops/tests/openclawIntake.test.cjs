'use strict';

const assert = require('node:assert');
const { spawnSync } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

console.log('\nopenclawIntake tests\n');

// ── helpers ───────────────────────────────────────────────────────────────────

const {
  adjudicateObservation,
  canonicalKeyForObservation,
  runIntake,
  loadObservations,
} = require('../dist/openclawIntake');

function makeTempDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-intake-test-'));
}

function makeObs(overrides) {
  return {
    id: 'test-obs',
    source: 'gmail',
    sourceId: 'gmail-test-001',
    observedBy: 'openclaw',
    title: 'Follow up on budget proposal',
    text: 'Please send me the updated specs by Friday.',
    timestamp: '2026-05-22T10:00:00Z',
    evidence: { subject: 'Budget proposal', snippet: 'Please send specs by Friday.' },
    confidence: 0.88,
    relatedContext: null,
    ...overrides,
  };
}

const emptyBatch = new Set();
const emptyMap = new Map();
const emptyLoops = [];

// ── unit: adjudication ────────────────────────────────────────────────────────

{
  const obs = makeObs();
  const result = adjudicateObservation(obs, emptyBatch, emptyBatch, emptyMap, emptyLoops);
  assert.strictEqual(result.verdict, 'accepted', 'real follow-up → accepted');
  console.log('  PASS  real follow-up → accepted');
}

{
  const obs = makeObs({
    title: 'Team update',
    text: 'No action required. This is for your information only.',
    evidence: { snippet: 'No action required.' },
  });
  const result = adjudicateObservation(obs, emptyBatch, emptyBatch, emptyMap, emptyLoops);
  assert.strictEqual(result.verdict, 'suppressed', 'no-action FYI → suppressed');
  assert.strictEqual(result.suppressionReason, 'negative_intent_no_action');
  console.log('  PASS  no-action signal → suppressed (negative_intent_no_action)');
}

{
  const obs = makeObs({
    title: 'Earn double miles this weekend',
    text: 'Limited time offer. Unsubscribe to opt out.',
    evidence: { snippet: 'Earn double miles. Unsubscribe.' },
  });
  const result = adjudicateObservation(obs, emptyBatch, emptyBatch, emptyMap, emptyLoops);
  assert.strictEqual(result.verdict, 'suppressed', 'promotional → suppressed');
  assert.strictEqual(result.suppressionReason, 'promotional_or_informational');
  console.log('  PASS  promotional signal → suppressed (promotional_or_informational)');
}

{
  const obs = makeObs({ source: 'slack', sourceId: 'slack-dup-001' });
  const key = canonicalKeyForObservation(obs);
  const result = adjudicateObservation(obs, new Set([key]), emptyBatch, emptyMap, emptyLoops);
  assert.strictEqual(result.verdict, 'suppressed', 'duplicate in batch → suppressed');
  assert.strictEqual(result.suppressionReason, 'duplicate_signal');
  console.log('  PASS  duplicate signal → suppressed (duplicate_signal)');
}

{
  const obs = makeObs({ confidence: 0.22, title: 'Unclear context', text: 'Maybe something here.' });
  const result = adjudicateObservation(obs, emptyBatch, emptyBatch, emptyMap, emptyLoops);
  assert.strictEqual(result.verdict, 'needs_review', 'weak evidence → needs_review');
  assert.strictEqual(result.suppressionReason, 'weak_evidence');
  console.log('  PASS  weak evidence → needs_review (weak_evidence)');
}

{
  const obs = makeObs({
    source: 'calendar',
    title: 'Flight SFO → ICN — Korean Air',
    text: 'Departing from San Francisco Airport.',
    evidence: { title: 'Flight SFO → ICN', location: 'SFO Terminal 2', description: 'Korean Air departure' },
    confidence: 0.90,
  });
  const result = adjudicateObservation(obs, emptyBatch, emptyBatch, emptyMap, emptyLoops);
  assert.strictEqual(result.verdict, 'attached_context', 'travel event → attached_context');
  assert.strictEqual(result.suppressionReason, 'context_only');
  console.log('  PASS  travel context → attached_context (context_only)');
}

{
  const obs = makeObs({
    title: 'Background doc forwarded',
    text: 'Supporting document shared by the partner team.',
    evidence: { snippet: 'Supporting doc.' },
    confidence: 0.70,
    relatedContext: { observationId: 'obs-001', type: 'supporting_document' },
  });
  const result = adjudicateObservation(obs, emptyBatch, emptyBatch, emptyMap, emptyLoops);
  assert.strictEqual(result.verdict, 'attached_context', 'relatedContext → attached_context');
  assert.strictEqual(result.suppressionReason, 'context_only');
  console.log('  PASS  relatedContext signal → attached_context (context_only)');
}

// ── unit: state_transition ────────────────────────────────────────────────────

{
  const targetKey = 'openclaw-gmail-gmail-mcp-001';
  const fakeLoop = {
    id: 'loop-uuid-001',
    canonicalKey: targetKey,
    title: 'Follow up with David Kim',
    status: 'todo',
    history: [],
  };
  const mapWithLoop = new Map([[targetKey, fakeLoop]]);
  const obs = makeObs({
    observationIntent: 'state_transition',
    title: 'David Kim confirmed specs received',
    text: 'David Kim confirmed receipt of the specs. Loop resolved.',
    relatedContext: { existingLoopKey: targetKey },
    confidence: 0.91,
  });

  // We can't actually call transitionOpenLoopState without a real WORLDLOOPS_DIR,
  // but we can verify the verdict is state_transition by using a temp dir
  const tempDir = makeTempDir();
  const prevDir = process.env.WORLDLOOPS_DIR;
  process.env.WORLDLOOPS_DIR = tempDir;

  // Pre-create the loop state file so transitionOpenLoopState can find it
  fs.mkdirSync(tempDir, { recursive: true });
  fs.writeFileSync(
    path.join(tempDir, 'open_loop_states.json'),
    JSON.stringify([{ ...fakeLoop, severity: 'medium', adjudication: { severity: 'medium', action: 'propose', approvalRequired: false, shouldEscalate: false, reason: '', safety: { externalWrite: false } }, owner: null, dueAt: null, lastObservedAt: new Date().toISOString(), updatedAt: new Date().toISOString(), sourceSignals: [], safety: { externalWrite: false } }], null, 2)
  );

  const result = adjudicateObservation(obs, emptyBatch, emptyBatch, mapWithLoop, []);
  assert.strictEqual(result.verdict, 'state_transition', 'state_transition obs → state_transition verdict');
  assert.ok(result.stateTransition, 'stateTransition info present');
  assert.strictEqual(result.stateTransition.fromStatus, 'todo');
  assert.strictEqual(result.stateTransition.toStatus, 'done');
  assert.strictEqual(result.stateTransition.transitionApplied, true);

  if (prevDir !== undefined) process.env.WORLDLOOPS_DIR = prevDir;
  else delete process.env.WORLDLOOPS_DIR;
  fs.rmSync(tempDir, { recursive: true });

  console.log('  PASS  state_transition observation → state_transition verdict, todo → done');
}

// ── integration: runIntake with fixture ──────────────────────────────────────

{
  const tempDir = makeTempDir();
  process.env.WORLDLOOPS_DIR = tempDir;

  const observations = loadObservations('scripts/fixtures/openclaw-signal-intake/mixed-observations.json');
  const summary = runIntake(observations);

  assert.strictEqual(summary.total, 14, `total should be 14, got ${summary.total}`);
  assert.strictEqual(summary.accepted, 3, `accepted should be 3, got ${summary.accepted}`);
  assert.strictEqual(summary.suppressed, 6, `suppressed should be 6, got ${summary.suppressed}`);
  assert.strictEqual(summary.attached_context, 2, `attached_context should be 2, got ${summary.attached_context}`);
  assert.strictEqual(summary.needs_review, 1, `needs_review should be 1, got ${summary.needs_review}`);
  assert.strictEqual(summary.state_transition, 2, `state_transition should be 2, got ${summary.state_transition}`);
  assert.strictEqual(summary.safety.externalWrite, false, 'externalWrite must be false');
  console.log('  PASS  runIntake returns correct adjudication counts (14 total, 3+2+6+2+1)');

  delete process.env.WORLDLOOPS_DIR;
  fs.rmSync(tempDir, { recursive: true });
}

{
  const tempDir = makeTempDir();
  process.env.WORLDLOOPS_DIR = tempDir;

  const observations = loadObservations('scripts/fixtures/openclaw-signal-intake/mixed-observations.json');
  runIntake(observations);

  const receiptsPath = path.join(tempDir, 'openclaw_suppression_receipts.json');
  assert.ok(fs.existsSync(receiptsPath), 'suppression receipts file should exist');
  const receipts = JSON.parse(fs.readFileSync(receiptsPath, 'utf8'));
  assert.ok(receipts.length >= 6, `at least 6 suppression receipts, got ${receipts.length}`);
  for (const r of receipts) {
    assert.strictEqual(r.safety.externalWrite, false, 'receipt externalWrite must be false');
    assert.ok(r.observationId, 'receipt must have observationId');
    assert.ok(r.adjudicatedAt, 'receipt must have adjudicatedAt');
  }
  console.log('  PASS  suppression receipts saved for suppressed / non-accepted decisions');

  delete process.env.WORLDLOOPS_DIR;
  fs.rmSync(tempDir, { recursive: true });
}

{
  const tempDir = makeTempDir();
  process.env.WORLDLOOPS_DIR = tempDir;

  const observations = loadObservations('scripts/fixtures/openclaw-signal-intake/mixed-observations.json');
  runIntake(observations);

  const loopsPath = path.join(tempDir, 'open_loop_states.json');
  assert.ok(fs.existsSync(loopsPath), 'open_loop_states.json should exist');
  const loops = JSON.parse(fs.readFileSync(loopsPath, 'utf8'));
  assert.strictEqual(loops.length, 3, `3 open loops should be created, got ${loops.length}`);
  for (const loop of loops) {
    assert.strictEqual(loop.safety.externalWrite, false, 'loop externalWrite must be false');
    assert.ok(loop.canonicalKey.startsWith('openclaw-'), 'canonicalKey must start with openclaw-');
  }
  // obs-001's loop should be transitioned to done by obs-013
  const mcp = loops.find(l => l.canonicalKey === 'openclaw-gmail-gmail-mcp-followup-001');
  assert.ok(mcp, 'MCP follow-up loop should exist');
  assert.strictEqual(mcp.status, 'done', `MCP loop should be done after state_transition, got ${mcp.status}`);

  // obs-003's loop should be escalated by obs-014
  const invoice = loops.find(l => l.canonicalKey === 'openclaw-gmail-gmail-invoice-ext-001');
  assert.ok(invoice, 'Invoice loop should exist');
  assert.strictEqual(invoice.status, 'escalated', `Invoice loop should be escalated, got ${invoice.status}`);

  // obs-002's loop should still be todo
  const lg = loops.find(l => l.canonicalKey === 'openclaw-slack-slack-msg-lgdeck-review-001');
  assert.ok(lg, 'LG deck loop should exist');
  assert.strictEqual(lg.status, 'todo', `LG deck loop should remain todo, got ${lg.status}`);

  console.log('  PASS  accepted signals become open loops; state transitions applied correctly');

  delete process.env.WORLDLOOPS_DIR;
  fs.rmSync(tempDir, { recursive: true });
}

{
  const tempDir = makeTempDir();
  process.env.WORLDLOOPS_DIR = tempDir;

  const observations = loadObservations('scripts/fixtures/openclaw-signal-intake/mixed-observations.json');
  const summary = runIntake(observations);

  assert.ok(summary.morningBriefLines.length > 0, 'morningBriefLines should not be empty');
  const briefText = summary.morningBriefLines.join('\n');
  assert.ok(briefText.includes('still open'), `morning brief should mention still open loops: ${briefText}`);
  assert.ok(briefText.includes('closed by new evidence'), `morning brief should mention closed loops: ${briefText}`);
  assert.ok(briefText.includes('escalated'), `morning brief should mention escalated loops: ${briefText}`);
  assert.ok(briefText.includes('suppressed as noise'), `morning brief should mention suppressed signals: ${briefText}`);
  console.log('  PASS  morning brief output includes loop lifecycle summary');

  delete process.env.WORLDLOOPS_DIR;
  fs.rmSync(tempDir, { recursive: true });
}

{
  const tempDir = makeTempDir();
  process.env.WORLDLOOPS_DIR = tempDir;

  // Run once to create obs-002's loop
  const observations = loadObservations('scripts/fixtures/openclaw-signal-intake/mixed-observations.json');
  runIntake(observations);

  const loopsBefore = JSON.parse(fs.readFileSync(path.join(tempDir, 'open_loop_states.json'), 'utf8'));
  assert.strictEqual(loopsBefore.length, 3, 'should have 3 loops after first run');

  // Run again — obs-002's loop already exists, so obs-002 would be suppressed as duplicate
  runIntake(observations);

  const loopsAfter = JSON.parse(fs.readFileSync(path.join(tempDir, 'open_loop_states.json'), 'utf8'));
  assert.strictEqual(loopsAfter.length, 3, `duplicate run should not create more open loops, got ${loopsAfter.length}`);
  console.log('  PASS  duplicate signal does not create duplicate open loop across runs');

  delete process.env.WORLDLOOPS_DIR;
  fs.rmSync(tempDir, { recursive: true });
}

// ── CLI integration ───────────────────────────────────────────────────────────

{
  const tempDir = makeTempDir();
  const result = spawnSync(
    'npm',
    ['run', '--silent', 'openclaw:intake', '--', '--input',
      'scripts/fixtures/openclaw-signal-intake/mixed-observations.json'],
    {
      encoding: 'utf8',
      env: { ...process.env, WORLDLOOPS_DIR: tempDir },
    }
  );
  fs.rmSync(tempDir, { recursive: true });

  assert.strictEqual(result.status, 0, `CLI should exit 0\nstdout: ${result.stdout}\nstderr: ${result.stderr}`);
  assert.ok(result.stdout.includes('OpenClaw observed'), 'output includes observed count');
  assert.ok(result.stdout.includes('WorldLoops adjudication'), 'output includes adjudication section');
  assert.ok(result.stdout.includes('accepted'), 'output includes accepted count');
  assert.ok(result.stdout.includes('Morning Brief'), 'output includes Morning Brief section');
  assert.ok(result.stdout.includes('externalWrite:false'), 'output includes externalWrite:false');
  assert.ok(!result.stdout.trim().startsWith('{'), 'output must not start with raw JSON');
  console.log('  PASS  CLI exits 0 with fixture input and correct output format');
}

{
  const result = spawnSync(
    'npm',
    ['run', '--silent', 'openclaw:intake'],
    { encoding: 'utf8', env: { ...process.env } }
  );
  assert.notStrictEqual(result.status, 0, 'CLI without --input should exit non-zero');
  console.log('  PASS  CLI exits non-zero when --input is missing');
}

console.log('\nAll openclawIntake tests passed.\n');
