/**
 * Tests for the Slice 2f weight-tuning loop — contradiction-sync.ts
 * `runWeightTuningLoop` + supporting feedback helpers.
 *
 * Runs against the real WASM core (no mocks) with an isolated state dir.
 *
 * Run with: npx tsx digest-tuning.test.ts
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {
  FEEDBACK_LOG_MAX_LINES,
  TUNING_LOOP_MIN_INTERVAL_SECONDS,
  appendFeedbackLog,
  feedbackLogPath,
  loadWeightsFile,
  runWeightTuningLoop,
  saveWeightsFile,
  type FeedbackEntry,
  type ScoreComponents,
  type WeightsFile,
} from './contradiction-sync.js';

let passed = 0;
let failed = 0;

function assert(condition: boolean, name: string): void {
  const n = passed + failed + 1;
  if (condition) {
    console.log(`ok ${n} - ${name}`);
    passed++;
  } else {
    console.log(`not ok ${n} - ${name}`);
    failed++;
  }
}

function assertEq<T>(actual: T, expected: T, name: string): void {
  const ok = JSON.stringify(actual) === JSON.stringify(expected);
  if (!ok) {
    console.log(`  actual:   ${JSON.stringify(actual)}`);
    console.log(`  expected: ${JSON.stringify(expected)}`);
  }
  assert(ok, name);
}

function setupTempStateDir(label: string): string {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), `tr-tuning-${label}-`));
  process.env.TOTALRECLAW_STATE_DIR = dir;
  return dir;
}

function cleanupTempStateDir(dir: string): void {
  try { fs.rmSync(dir, { recursive: true, force: true }); } catch { /* ignore */ }
  delete process.env.TOTALRECLAW_STATE_DIR;
}

const silentLogger = { info: (_: string) => {}, warn: (_: string) => {} };

function mkComponents(weighted: number, recency = 0.5): ScoreComponents {
  return {
    confidence: 0.85,
    corroboration: 1.0,
    recency,
    validation: 0.7,
    weighted_total: weighted,
  };
}

function mkEntry(ts: number, decision: FeedbackEntry['user_decision']): FeedbackEntry {
  return {
    ts,
    claim_a_id: '0xaaa',
    claim_b_id: '0xbbb',
    formula_winner: 'a',
    user_decision: decision,
    winner_components: mkComponents(0.83, 0.8),
    loser_components: mkComponents(0.73, 0.2),
  };
}

async function runAllTests(): Promise<void> {
  // Empty feedback.jsonl → no-op, no weights change
  {
    const tmp = setupTempStateDir('empty');
    try {
      const result = await runWeightTuningLoop(1_777_000_000, silentLogger);
      assertEq(result.processed, 0, 'empty: processed=0');
      assertEq(result.gradientSteps, 0, 'empty: gradientSteps=0');
      assertEq(result.skipped, 'no-new-entries', 'empty: skipped=no-new-entries');
    } finally {
      cleanupTempStateDir(tmp);
    }
  }

  // One counterexample → weights adjusted, last_tuning_ts set
  {
    const tmp = setupTempStateDir('one');
    try {
      const entry = mkEntry(1_776_500_000, 'pin_b'); // formula_winner=a, user pinned b → counterexample
      await appendFeedbackLog(entry);

      const before = await loadWeightsFile(1_777_000_000);
      const result = await runWeightTuningLoop(1_777_000_000, silentLogger);
      assertEq(result.processed, 1, 'one: processed=1');
      assertEq(result.gradientSteps, 1, 'one: one gradient step');
      assertEq(result.skipped, null, 'one: not skipped');
      assertEq(result.lastTuningTs, 1_776_500_000, 'one: last_tuning_ts advanced');

      const after = await loadWeightsFile(1_777_000_000);
      assert(after.last_tuning_ts === 1_776_500_000, 'one: weights file last_tuning_ts persisted');
      assert(
        JSON.stringify(after.weights) !== JSON.stringify(before.weights),
        'one: weights actually changed',
      );
      assertEq(after.feedback_count, 1, 'one: feedback_count incremented');
    } finally {
      cleanupTempStateDir(tmp);
    }
  }

  // User-agreed entry (pin_a with formula_winner=a) → no gradient step
  {
    const tmp = setupTempStateDir('agreed');
    try {
      const entry = mkEntry(1_776_500_000, 'pin_a'); // formula_winner=a, user pinned a → null counterexample
      await appendFeedbackLog(entry);

      const before = await loadWeightsFile(1_777_000_000);
      const result = await runWeightTuningLoop(1_777_000_000, silentLogger);
      assertEq(result.processed, 1, 'agreed: processed=1');
      assertEq(result.gradientSteps, 0, 'agreed: zero gradient steps');

      const after = await loadWeightsFile(1_777_000_000);
      assertEq(
        JSON.stringify(after.weights),
        JSON.stringify(before.weights),
        'agreed: weights unchanged when user agrees with formula',
      );
      assert(after.last_tuning_ts === 1_776_500_000, 'agreed: last_tuning_ts still advances');
    } finally {
      cleanupTempStateDir(tmp);
    }
  }

  // 10 counterexamples → accumulate gradient
  {
    const tmp = setupTempStateDir('ten');
    try {
      for (let i = 0; i < 10; i++) {
        await appendFeedbackLog(mkEntry(1_776_500_000 + i, 'pin_b'));
      }
      const result = await runWeightTuningLoop(1_777_000_000, silentLogger);
      assertEq(result.processed, 10, 'ten: processed=10');
      assertEq(result.gradientSteps, 10, 'ten: 10 gradient steps');
      const after = await loadWeightsFile(1_777_000_000);
      assertEq(after.feedback_count, 10, 'ten: feedback_count = 10');
      assert(after.last_tuning_ts === 1_776_500_009, 'ten: last_tuning_ts = max ts seen');
    } finally {
      cleanupTempStateDir(tmp);
    }
  }

  // Already-processed entries (ts <= last_tuning_ts) → skipped
  {
    const tmp = setupTempStateDir('processed');
    try {
      // Seed feedback + run once.
      await appendFeedbackLog(mkEntry(1_776_500_000, 'pin_b'));
      const first = await runWeightTuningLoop(1_777_000_000, silentLogger);
      assertEq(first.processed, 1, 'processed: first run processes entry');

      // Bump updated_at in the past so the rate limiter doesn't kick in.
      const stale = await loadWeightsFile(1_777_000_000);
      stale.updated_at = 1_776_000_000;
      await saveWeightsFile(stale);

      // Second run: same entry should be skipped via last_tuning_ts.
      const second = await runWeightTuningLoop(1_777_000_000, silentLogger);
      assertEq(second.processed, 0, 'processed: second run processes no entries');
      assertEq(second.skipped, 'no-new-entries', 'processed: skipped=no-new-entries');
    } finally {
      cleanupTempStateDir(tmp);
    }
  }

  // Idempotence: re-running the loop with the same feedback doesn't move weights.
  {
    const tmp = setupTempStateDir('idempotent');
    try {
      await appendFeedbackLog(mkEntry(1_776_500_000, 'pin_b'));
      await runWeightTuningLoop(1_777_000_000, silentLogger);
      const afterFirst = await loadWeightsFile(1_777_000_000);

      // Second pass — force past rate limit.
      afterFirst.updated_at = 1_776_000_000;
      await saveWeightsFile(afterFirst);
      await runWeightTuningLoop(1_777_000_000, silentLogger);
      const afterSecond = await loadWeightsFile(1_777_000_000);
      assertEq(
        JSON.stringify(afterSecond.weights),
        JSON.stringify(afterFirst.weights),
        'idempotent: weights unchanged across runs',
      );
      assertEq(
        afterSecond.feedback_count,
        afterFirst.feedback_count,
        'idempotent: feedback_count unchanged',
      );
    } finally {
      cleanupTempStateDir(tmp);
    }
  }

  // Weight clamping: 100 counterexamples → weights stay in [0.05, 0.60]
  {
    const tmp = setupTempStateDir('clamp');
    try {
      for (let i = 0; i < 100; i++) {
        await appendFeedbackLog(mkEntry(1_776_500_000 + i, 'pin_b'));
      }
      const result = await runWeightTuningLoop(1_777_000_000, silentLogger);
      assertEq(result.gradientSteps, 100, 'clamp: 100 gradient steps applied');
      const after = await loadWeightsFile(1_777_000_000);
      const ws = after.weights as Record<string, number>;
      for (const [k, v] of Object.entries(ws)) {
        assert(v >= 0.05 && v <= 0.60, `clamp: ${k} weight ${v.toFixed(3)} stays in [0.05, 0.60]`);
      }
      const total = Object.values(ws).reduce((a, b) => a + b, 0);
      assert(total >= 0.9 && total <= 1.1, `clamp: total sum ${total.toFixed(3)} stays in [0.9, 1.1]`);
    } finally {
      cleanupTempStateDir(tmp);
    }
  }

  // Mixed agreed + disagreed → only disagreed entries move weights
  {
    const tmp = setupTempStateDir('mixed');
    try {
      // 3 user-agreed + 2 user-disagreed entries.
      await appendFeedbackLog(mkEntry(1_776_500_000, 'pin_a'));
      await appendFeedbackLog(mkEntry(1_776_500_001, 'pin_a'));
      await appendFeedbackLog(mkEntry(1_776_500_002, 'pin_b'));
      await appendFeedbackLog(mkEntry(1_776_500_003, 'pin_a'));
      await appendFeedbackLog(mkEntry(1_776_500_004, 'pin_b'));

      const result = await runWeightTuningLoop(1_777_000_000, silentLogger);
      assertEq(result.processed, 5, 'mixed: all 5 processed');
      assertEq(result.gradientSteps, 2, 'mixed: only 2 gradient steps (pin_b when winner=a)');
    } finally {
      cleanupTempStateDir(tmp);
    }
  }

  // Rate limit: calling again within the window is skipped
  {
    const tmp = setupTempStateDir('rate');
    try {
      await appendFeedbackLog(mkEntry(1_776_500_000, 'pin_b'));
      const first = await runWeightTuningLoop(1_777_000_000, silentLogger);
      assertEq(first.skipped, null, 'rate: first run runs');

      // Add a new entry but call immediately — should be rate-limited.
      await appendFeedbackLog(mkEntry(1_777_000_100, 'pin_b'));
      const second = await runWeightTuningLoop(1_777_000_100, silentLogger);
      assertEq(second.skipped, 'rate-limited', 'rate: second run rate-limited');
      assertEq(second.gradientSteps, 0, 'rate: no gradient applied when rate-limited');

      // Move past the window → runs again.
      const third = await runWeightTuningLoop(
        1_777_000_000 + TUNING_LOOP_MIN_INTERVAL_SECONDS + 1,
        silentLogger,
      );
      assert(third.skipped !== 'rate-limited', 'rate: past window → runs');
      assertEq(third.gradientSteps, 1, 'rate: new entry processed after window');
    } finally {
      cleanupTempStateDir(tmp);
    }
  }

  // Feedback log format: appended lines are parseable by core.readFeedbackJsonl
  {
    const tmp = setupTempStateDir('format');
    try {
      await appendFeedbackLog(mkEntry(1_776_500_000, 'pin_b'));
      await appendFeedbackLog(mkEntry(1_776_500_001, 'pin_a'));
      const content = fs.readFileSync(feedbackLogPath(), 'utf-8');
      const lines = content.split('\n').filter((l) => l.length > 0);
      assertEq(lines.length, 2, 'format: two JSONL lines');
      for (const line of lines) {
        const parsed = JSON.parse(line);
        assert(typeof parsed.ts === 'number', 'format: ts is number');
        assert(
          typeof parsed.winner_components === 'object' && parsed.winner_components !== null,
          'format: winner_components object',
        );
      }
    } finally {
      cleanupTempStateDir(tmp);
    }
  }

  // Constants sanity
  {
    assert(FEEDBACK_LOG_MAX_LINES === 10_000, 'constants: FEEDBACK_LOG_MAX_LINES = 10000');
    assert(TUNING_LOOP_MIN_INTERVAL_SECONDS === 3600, 'constants: min interval = 1h');
  }

  // ── Summary ────────────────────────────────────────────────────────────────
  console.log(`\n# ${passed}/${passed + failed} passed`);
  if (failed > 0) {
    console.log('\nSOME TESTS FAILED');
    process.exit(1);
  } else {
    console.log('\nALL TESTS PASSED');
  }
}

runAllTests().catch((err) => {
  console.error('FATAL:', err);
  process.exit(1);
});

export {};
