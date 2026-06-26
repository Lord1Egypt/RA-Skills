/**
 * trajectory-poller.test.ts — regression tests for the auto-extraction
 * polling layer (3.3.11-rc.1).
 *
 * Covers:
 *   1. findTrajectoryFiles — scan ~/.openclaw/agents/<agent>/sessions/
 *   2. parseNewMessages — extract prompt.submitted + model.completed
 *      events into the {role, content}[] shape extractFacts expects
 *      from a `.trajectory.jsonl` byte slice; handle partial last line.
 *   3. countTurns — pair adjacent user+assistant entries
 *   4. loadState / saveState — round-trip per-file offset state
 *   5. startTrajectoryPoller — fires runExtraction + persistFacts when
 *      enough turns accumulate; defers below the threshold; honors
 *      isPairingPending / isImportActive gates; tracks offset across
 *      polls so messages aren't re-extracted.
 *
 * Run with: `npx tsx trajectory-poller.test.ts`
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {
  findTrajectoryFiles,
  parseNewMessages,
  countTurns,
  loadState,
  saveState,
  startTrajectoryPoller,
  type TrajectoryPollerDeps,
  type ExtractedFactLike,
  type PollerState,
} from './trajectory-poller.js';

let passed = 0;
let failed = 0;

function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) {
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

const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-poller-'));
const silentLogger: TrajectoryPollerDeps['logger'] = {
  info: () => {},
  warn: () => {},
  error: () => {},
};

// ---------------------------------------------------------------------------
// 1. findTrajectoryFiles
// ---------------------------------------------------------------------------

{
  // Empty home — returns [] without throwing.
  const empty = path.join(TMP, 'empty-home');
  fs.mkdirSync(empty, { recursive: true });
  const files = findTrajectoryFiles(empty);
  assertEq(files, [], 'findTrajectoryFiles: empty home returns []');
}

{
  // Mock ~/.openclaw/agents/main/sessions/<sid>.trajectory.jsonl
  const home = path.join(TMP, 'home-with-sessions');
  const sessionsDir = path.join(home, '.openclaw', 'agents', 'main', 'sessions');
  fs.mkdirSync(sessionsDir, { recursive: true });
  fs.writeFileSync(path.join(sessionsDir, 'aaa.trajectory.jsonl'), '');
  fs.writeFileSync(path.join(sessionsDir, 'bbb.trajectory.jsonl'), '');
  fs.writeFileSync(path.join(sessionsDir, 'ccc.trajectory-path.json'), '{}'); // pointer, NOT a trajectory
  fs.writeFileSync(path.join(sessionsDir, 'sessions.json'), '{}'); // index, NOT a trajectory

  const files = findTrajectoryFiles(home);
  assertEq(files.length, 2, 'findTrajectoryFiles: picks .trajectory.jsonl, skips .trajectory-path.json + sessions.json');
  assert(
    files.every((f) => f.endsWith('.trajectory.jsonl')),
    'findTrajectoryFiles: every result ends with .trajectory.jsonl',
  );
}

{
  // Multi-agent layout — agents/<agent_a>/sessions + agents/<agent_b>/sessions both walked.
  const home = path.join(TMP, 'home-multi-agent');
  fs.mkdirSync(path.join(home, '.openclaw', 'agents', 'main', 'sessions'), { recursive: true });
  fs.mkdirSync(path.join(home, '.openclaw', 'agents', 'helper', 'sessions'), { recursive: true });
  fs.writeFileSync(path.join(home, '.openclaw', 'agents', 'main', 'sessions', 'm1.trajectory.jsonl'), '');
  fs.writeFileSync(path.join(home, '.openclaw', 'agents', 'helper', 'sessions', 'h1.trajectory.jsonl'), '');
  const files = findTrajectoryFiles(home);
  assertEq(files.length, 2, 'findTrajectoryFiles: walks every agent under agents/');
}

// ---------------------------------------------------------------------------
// 2. parseNewMessages
// ---------------------------------------------------------------------------

{
  // Schema sample (matches pop-os 2026-05-06 trajectory):
  // - prompt.submitted with data.prompt
  // - model.completed with data.assistantTexts (string[])
  const file = path.join(TMP, 'sample.trajectory.jsonl');
  const lines = [
    JSON.stringify({ type: 'session.started', ts: '2026-05-06T00:27:30Z' }),
    JSON.stringify({ type: 'trace.metadata', ts: '2026-05-06T00:27:30Z' }),
    JSON.stringify({
      type: 'prompt.submitted',
      data: { prompt: 'I prefer Python over Go.' },
    }),
    JSON.stringify({
      type: 'model.completed',
      data: { assistantTexts: ['Got it. Logged your Python preference.'] },
    }),
    JSON.stringify({
      type: 'prompt.submitted',
      data: { prompt: 'I work at Graph Foundation.' },
    }),
    JSON.stringify({
      type: 'model.completed',
      data: { assistantTexts: ['Noted that you work at Graph Foundation.', 'Anything else?'] },
    }),
    JSON.stringify({ type: 'session.ended', ts: '2026-05-06T00:30:00Z' }),
  ];
  fs.writeFileSync(file, lines.join('\n') + '\n');

  const { messages, newOffset } = parseNewMessages(file, 0);

  assertEq(messages.length, 4, 'parseNewMessages: pulls 4 messages (2 user + 2 assistant)');
  assertEq(messages[0], { role: 'user', content: 'I prefer Python over Go.' }, 'parseNewMessages: first user message');
  assertEq(messages[1].role, 'assistant', 'parseNewMessages: second message is assistant');
  assert(messages[1].content.startsWith('Got it.'), 'parseNewMessages: assistant text matches first reply');
  assertEq(messages[2], { role: 'user', content: 'I work at Graph Foundation.' }, 'parseNewMessages: third user message');
  assert(
    messages[3].content.includes('Graph Foundation') && messages[3].content.includes('Anything else?'),
    'parseNewMessages: multi-string assistantTexts joined',
  );
  assertEq(newOffset, fs.statSync(file).size, 'parseNewMessages: full read advances offset to file size');
}

{
  // Incomplete trailing line (mid-flush) — newOffset must NOT advance past
  // the last full newline so we re-read the partial line next tick.
  const file = path.join(TMP, 'partial.trajectory.jsonl');
  const completeLine = JSON.stringify({
    type: 'prompt.submitted',
    data: { prompt: 'complete user msg' },
  });
  const partialLine = '{"type":"model.completed","data":{"assista'; // truncated mid-flush
  fs.writeFileSync(file, completeLine + '\n' + partialLine);

  const { messages, newOffset } = parseNewMessages(file, 0);
  assertEq(messages.length, 1, 'parseNewMessages: only complete lines parsed');
  assertEq(messages[0].content, 'complete user msg', 'parseNewMessages: complete line content');
  assertEq(
    newOffset,
    Buffer.byteLength(completeLine + '\n', 'utf-8'),
    'parseNewMessages: newOffset stops at last full newline (partial line will be re-read)',
  );
}

{
  // Offset > file size: empty result, newOffset clamped to file size.
  const file = path.join(TMP, 'noop.trajectory.jsonl');
  fs.writeFileSync(file, JSON.stringify({ type: 'session.started' }) + '\n');
  const size = fs.statSync(file).size;
  const { messages, newOffset } = parseNewMessages(file, size + 1000);
  assertEq(messages, [], 'parseNewMessages: offset past EOF returns []');
  assertEq(newOffset, size, 'parseNewMessages: offset past EOF clamps to file size');
}

{
  // Malformed JSON line — skipped silently; valid lines still parsed.
  const file = path.join(TMP, 'malformed.trajectory.jsonl');
  fs.writeFileSync(
    file,
    [
      'this is not json',
      JSON.stringify({ type: 'prompt.submitted', data: { prompt: 'after the bad line' } }),
      '{ broken json',
      JSON.stringify({ type: 'model.completed', data: { assistantTexts: ['ok'] } }),
    ].join('\n') + '\n',
  );
  const { messages } = parseNewMessages(file, 0);
  assertEq(messages.length, 2, 'parseNewMessages: malformed lines skipped, valid lines extracted');
  assertEq(messages[0].content, 'after the bad line', 'parseNewMessages: valid line after malformed line still parsed');
}

// ---------------------------------------------------------------------------
// 3. countTurns
// ---------------------------------------------------------------------------

{
  assertEq(
    countTurns([
      { role: 'user', content: 'a' },
      { role: 'assistant', content: 'b' },
      { role: 'user', content: 'c' },
      { role: 'assistant', content: 'd' },
    ]),
    2,
    'countTurns: 2 user+assistant pairs = 2 turns',
  );

  assertEq(
    countTurns([
      { role: 'user', content: 'a' },
      { role: 'user', content: 'b' }, // no assistant in between
      { role: 'assistant', content: 'c' },
    ]),
    1,
    'countTurns: only the matched user+assistant pair counts',
  );

  assertEq(
    countTurns([
      { role: 'assistant', content: 'a' }, // assistant first - not a turn
      { role: 'user', content: 'b' },
      { role: 'assistant', content: 'c' },
    ]),
    1,
    'countTurns: leading assistant ignored, then one full turn',
  );

  assertEq(
    countTurns([
      { role: 'user', content: 'a' }, // unmatched trailing user
    ]),
    0,
    'countTurns: unmatched user with no assistant reply = 0 turns',
  );
}

// ---------------------------------------------------------------------------
// 4. loadState / saveState
// ---------------------------------------------------------------------------

{
  const stateFile = path.join(TMP, 'state-rt.json');
  const state: PollerState = {
    '/path/to/a.trajectory.jsonl': { offset: 1234, turnsAccum: 2 },
    '/path/to/b.trajectory.jsonl': { offset: 0, turnsAccum: 0 },
  };
  saveState(stateFile, state, silentLogger);
  const loaded = loadState(stateFile, silentLogger);
  assertEq(loaded, state, 'loadState/saveState: round-trip preserves all entries');
}

{
  // Missing state file → empty state (fresh install).
  const stateFile = path.join(TMP, 'nonexistent-state.json');
  const loaded = loadState(stateFile, silentLogger);
  assertEq(loaded, {}, 'loadState: missing file returns empty state');
}

{
  // Corrupt state file → empty state + warn (silent in test logger).
  const stateFile = path.join(TMP, 'corrupt-state.json');
  fs.writeFileSync(stateFile, 'this is not json');
  const loaded = loadState(stateFile, silentLogger);
  assertEq(loaded, {}, 'loadState: corrupt file returns empty state (warns + recovers)');
}

// ---------------------------------------------------------------------------
// 5. startTrajectoryPoller — full pollOnce flow with mocked deps
// ---------------------------------------------------------------------------

async function withPoller(
  homeDir: string,
  overrides: Partial<TrajectoryPollerDeps>,
  fn: (handle: ReturnType<typeof startTrajectoryPoller>, calls: CallRecord) => Promise<void>,
): Promise<void> {
  const calls: CallRecord = {
    extraction: 0,
    persisted: 0,
    importanceFilterCalled: 0,
    dedupCalled: 0,
    persistedFacts: [],
  };
  const stateFile = path.join(homeDir, '.totalreclaw', 'extract-state.json');
  // Override HOME so findTrajectoryFiles walks the mock dir.
  const origHome = process.env.HOME;
  process.env.HOME = homeDir;
  try {
    const deps: TrajectoryPollerDeps = {
      logger: silentLogger,
      ensureInitialized: async () => {},
      isPairingPending: () => false,
      isImportActive: () => false,
      getExtractInterval: () => 2,
      getMaxFactsPerExtraction: () => 10,
      isDedupEnabled: () => true,
      getDedupCandidates: async () => {
        calls.dedupCalled++;
        return [];
      },
      runExtraction: async (messages) => {
        calls.extraction++;
        // Return one fake fact per assistant message, importance 0.8
        return messages
          .filter((m) => m.role === 'assistant')
          .map((m) => ({ text: `extracted: ${m.content.slice(0, 30)}`, importance: 0.8 } as ExtractedFactLike));
      },
      filterByImportance: (facts) => {
        calls.importanceFilterCalled++;
        return { kept: facts, dropped: 0 };
      },
      persistFacts: async (facts) => {
        calls.persistedFacts.push(...facts);
        calls.persisted += facts.length;
        return facts.length;
      },
      ...overrides,
    };
    const handle = startTrajectoryPoller(deps, { pollIntervalMs: 60_000, stateFile });
    try {
      await fn(handle, calls);
    } finally {
      handle.stop();
    }
  } finally {
    if (origHome === undefined) delete process.env.HOME;
    else process.env.HOME = origHome;
  }
}

interface CallRecord {
  extraction: number;
  persisted: number;
  importanceFilterCalled: number;
  dedupCalled: number;
  persistedFacts: ExtractedFactLike[];
}

function writeTrajectoryFile(home: string, sid: string, turns: Array<[string, string]>): string {
  const sessionsDir = path.join(home, '.openclaw', 'agents', 'main', 'sessions');
  fs.mkdirSync(sessionsDir, { recursive: true });
  const file = path.join(sessionsDir, `${sid}.trajectory.jsonl`);
  const lines: string[] = [];
  lines.push(JSON.stringify({ type: 'session.started' }));
  for (const [user, assistant] of turns) {
    lines.push(JSON.stringify({ type: 'prompt.submitted', data: { prompt: user } }));
    lines.push(JSON.stringify({ type: 'model.completed', data: { assistantTexts: [assistant] } }));
  }
  lines.push(JSON.stringify({ type: 'session.ended' }));
  fs.writeFileSync(file, lines.join('\n') + '\n');
  return file;
}

async function runTests(): Promise<void> {
  // 5a. Below threshold (1 turn, interval=2) → defer, no extraction.
  {
    const home = path.join(TMP, 'home-defer');
    writeTrajectoryFile(home, 'sess-defer', [['user 1', 'assistant 1']]);
    await withPoller(home, {}, async (h, calls) => {
      await h.pollOnce();
      assertEq(calls.extraction, 0, 'pollOnce defer: extraction NOT called below threshold');
      assertEq(calls.persisted, 0, 'pollOnce defer: persistFacts NOT called below threshold');
    });
  }

  // 5b. Threshold met (2 turns, interval=2) → extraction + persist fire.
  {
    const home = path.join(TMP, 'home-fire');
    writeTrajectoryFile(home, 'sess-fire', [
      ['I prefer Python over Go.', 'Got it. Logged your Python preference.'],
      ['I work at Graph Foundation.', 'Noted.'],
    ]);
    await withPoller(home, {}, async (h, calls) => {
      await h.pollOnce();
      assertEq(calls.extraction, 1, 'pollOnce fire: extraction called once');
      assert(calls.persisted >= 1, `pollOnce fire: persistFacts received >=1 fact (got ${calls.persisted})`);
      assertEq(calls.dedupCalled, 1, 'pollOnce fire: dedup-candidate lookup called once');
      assertEq(calls.importanceFilterCalled, 1, 'pollOnce fire: importance filter called once');
    });
  }

  // 5c. isPairingPending=true → no extraction even with messages present.
  {
    const home = path.join(TMP, 'home-pairing');
    writeTrajectoryFile(home, 'sess-pairing', [
      ['user', 'assistant'],
      ['user', 'assistant'],
    ]);
    await withPoller(home, { isPairingPending: () => true }, async (h, calls) => {
      await h.pollOnce();
      assertEq(calls.extraction, 0, 'pollOnce pairing-pending: extraction skipped');
      assertEq(calls.persisted, 0, 'pollOnce pairing-pending: nothing persisted');
    });
  }

  // 5d. isImportActive=true → no extraction.
  {
    const home = path.join(TMP, 'home-import');
    writeTrajectoryFile(home, 'sess-import', [
      ['user', 'assistant'],
      ['user', 'assistant'],
    ]);
    await withPoller(home, { isImportActive: () => true }, async (h, calls) => {
      await h.pollOnce();
      assertEq(calls.extraction, 0, 'pollOnce import-active: extraction skipped');
    });
  }

  // 5e. Offset persists across polls — no re-extraction of already-seen messages.
  {
    const home = path.join(TMP, 'home-offset');
    const file = writeTrajectoryFile(home, 'sess-offset', [
      ['turn 1 user', 'turn 1 assistant'],
      ['turn 2 user', 'turn 2 assistant'],
    ]);
    await withPoller(home, {}, async (h, calls) => {
      await h.pollOnce(); // first poll: extracts both turns
      assertEq(calls.extraction, 1, 'pollOnce offset: first poll runs extraction');
      const persistedAfter1 = calls.persisted;

      // Second poll on same file with no new lines — must NOT re-extract.
      await h.pollOnce();
      assertEq(calls.extraction, 1, 'pollOnce offset: second poll on unchanged file does NOT re-extract');
      assertEq(calls.persisted, persistedAfter1, 'pollOnce offset: nothing additional persisted on no-op poll');

      // Append a new turn to the file, poll again — but interval=2, only 1 new turn → defer.
      fs.appendFileSync(
        file,
        JSON.stringify({ type: 'prompt.submitted', data: { prompt: 'turn 3 user' } }) +
          '\n' +
          JSON.stringify({ type: 'model.completed', data: { assistantTexts: ['turn 3 assistant'] } }) +
          '\n',
      );
      await h.pollOnce();
      assertEq(calls.extraction, 1, 'pollOnce offset: 1 new turn after extraction reset accumulates, defers');

      // Append a 4th turn — total 2 new turns since last extraction → fires again.
      fs.appendFileSync(
        file,
        JSON.stringify({ type: 'prompt.submitted', data: { prompt: 'turn 4 user' } }) +
          '\n' +
          JSON.stringify({ type: 'model.completed', data: { assistantTexts: ['turn 4 assistant'] } }) +
          '\n',
      );
      await h.pollOnce();
      assertEq(calls.extraction, 2, 'pollOnce offset: cumulative 2 turns since last fires extraction');
    });
  }

  // 5f. Two independent session files — both crossing threshold in same poll.
  // 3.3.11-rc.5 cap=1: only ONE extraction per poll iteration to avoid
  // burst-firing the LLM rate-limiter. The deferred file's offset is
  // preserved so the next poll picks it up.
  {
    const home = path.join(TMP, 'home-multi-session');
    writeTrajectoryFile(home, 'sess-a', [
      ['a user 1', 'a assistant 1'],
      ['a user 2', 'a assistant 2'],
    ]);
    writeTrajectoryFile(home, 'sess-b', [
      ['b user 1', 'b assistant 1'],
      ['b user 2', 'b assistant 2'],
    ]);
    await withPoller(home, {}, async (h, calls) => {
      await h.pollOnce();
      assertEq(
        calls.extraction,
        1,
        'pollOnce multi-session cap=1: only ONE extraction per poll, deferred file picks up next poll',
      );
      // Second poll: no new content on either file. Deferred file from poll-1
      // already advanced its offset (cap-deferred files DO still record
      // newOffset to avoid re-parsing the same lines).
      await h.pollOnce();
      // Cap-deferred files are at offset = newOffset, turnsAccum = N (preserved).
      // Their content was already consumed; they don't re-extract until net-new
      // messages arrive. So second poll is no-op extraction-wise.
      assertEq(
        calls.extraction,
        1,
        'pollOnce multi-session cap=1: second poll on unchanged files no-ops',
      );
    });
  }

  // 5g. Stale-file skip — trajectory file with mtime > 7 days old gets
  // baseline offset captured but extraction skipped, preventing retroactive
  // backlog burst on hosts with months of session-log history.
  {
    const home = path.join(TMP, 'home-stale-skip');
    const file = writeTrajectoryFile(home, 'old-session', [
      ['old user 1', 'old assistant 1'],
      ['old user 2', 'old assistant 2'],
    ]);
    // Backdate mtime to 30 days ago.
    const past = Date.now() - 30 * 24 * 60 * 60 * 1000;
    fs.utimesSync(file, past / 1000, past / 1000);
    await withPoller(home, {}, async (h, calls) => {
      await h.pollOnce();
      assertEq(calls.extraction, 0, 'pollOnce stale-skip: extraction NOT called for >7-day-old trajectory');
      assertEq(calls.persisted, 0, 'pollOnce stale-skip: nothing persisted');
    });
  }

  // 5h. Recent file (within 7 days) is NOT skipped — sanity check that
  // stale-skip only catches truly old files.
  {
    const home = path.join(TMP, 'home-recent-not-skipped');
    const file = writeTrajectoryFile(home, 'recent-session', [
      ['recent user 1', 'recent assistant 1'],
      ['recent user 2', 'recent assistant 2'],
    ]);
    // Backdate to 3 days ago (within 7-day window).
    const recent = Date.now() - 3 * 24 * 60 * 60 * 1000;
    fs.utimesSync(file, recent / 1000, recent / 1000);
    await withPoller(home, {}, async (h, calls) => {
      await h.pollOnce();
      assertEq(calls.extraction, 1, 'pollOnce recent-not-skipped: extraction fires for <7-day-old trajectory');
    });
  }
}

// ---------------------------------------------------------------------------

await runTests();

console.log(`\n# ${passed} passed, ${failed} failed`);
process.exit(failed === 0 ? 0 : 1);
