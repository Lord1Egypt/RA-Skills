/**
 * test_issue_92_onnx_download_ux.test.ts — Regression for #92.
 *
 * The ONNX runtime / embedding-model download is wrapped with a per-attempt
 * timeout, a periodic keep-alive, and 3-attempt exponential-backoff retry
 * with a final fail-loud actionable error. This test exercises that wrapper
 * (`downloadWithUX`) without touching the network or the real model.
 *
 * Run with: npx tsx test_issue_92_onnx_download_ux.test.ts
 */

import { downloadWithUX } from './download-ux.ts';

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

const captured: string[] = [];
const captureLog = (msg: string) => captured.push(msg);
const fastSleep = async (_ms: number) => { /* no-op for tests */ };

// ---------------------------------------------------------------------------
// 1. Happy path: download resolves on first attempt → no retry, returns value.
// ---------------------------------------------------------------------------
{
  captured.length = 0;
  let calls = 0;
  const result = await downloadWithUX(
    'happy',
    async () => { calls++; return 'ok'; },
    { timeoutMs: 5_000, keepaliveMs: 60_000, log: captureLog, sleep: fastSleep },
  );
  assert(result === 'ok', 'happy path: returns the resolved value');
  assert(calls === 1, 'happy path: download is called exactly once');
  assert(captured.length === 0, 'happy path: no keep-alive logs when download is fast');
}

// ---------------------------------------------------------------------------
// 2. Transient failure → retries → succeeds on attempt 2.
// ---------------------------------------------------------------------------
{
  captured.length = 0;
  let calls = 0;
  const result = await downloadWithUX(
    'transient',
    async () => {
      calls++;
      if (calls === 1) throw new Error('ECONNRESET');
      return 'recovered';
    },
    { timeoutMs: 5_000, keepaliveMs: 60_000, maxAttempts: 3, log: captureLog, sleep: fastSleep },
  );
  assert(result === 'recovered', 'transient failure: returns value from attempt 2');
  assert(calls === 2, 'transient failure: download is called twice');
  const retryMsgFound = captured.some(m => m.includes('attempt 1 failed') && m.includes('Retrying'));
  assert(retryMsgFound, 'transient failure: emits a Retrying log between attempts');
}

// ---------------------------------------------------------------------------
// 3. All attempts fail → throws actionable error mentioning env var + cmd.
// ---------------------------------------------------------------------------
{
  captured.length = 0;
  let calls = 0;
  let caught: Error | null = null;
  try {
    await downloadWithUX(
      'always-fails',
      async () => { calls++; throw new Error('network down'); },
      { timeoutMs: 5_000, keepaliveMs: 60_000, maxAttempts: 3, log: captureLog, sleep: fastSleep },
    );
  } catch (err) {
    caught = err as Error;
  }
  assert(caught !== null, 'fail-loud: throws after all attempts exhausted');
  assert(calls === 3, 'fail-loud: tried exactly maxAttempts (3) times');
  assert(
    caught !== null && /TOTALRECLAW_ONNX_INSTALL_TIMEOUT/.test(caught.message),
    'fail-loud: error message names the timeout env var',
  );
  assert(
    caught !== null && /openclaw plugins install/.test(caught.message),
    'fail-loud: error message includes the retry command',
  );
  assert(
    caught !== null && /failed after 3 attempts/.test(caught.message),
    'fail-loud: error message mentions attempt count',
  );
}

// ---------------------------------------------------------------------------
// 4. Per-attempt timeout fires → counts as a failure → triggers retry.
// ---------------------------------------------------------------------------
{
  captured.length = 0;
  let calls = 0;
  let caught: Error | null = null;
  try {
    await downloadWithUX(
      'timeout',
      async () => {
        calls++;
        // Hang past the per-attempt timeout.
        await new Promise(r => setTimeout(r, 500));
      },
      { timeoutMs: 50, keepaliveMs: 60_000, maxAttempts: 2, log: captureLog, sleep: fastSleep },
    );
  } catch (err) {
    caught = err as Error;
  }
  assert(caught !== null, 'timeout: throws after both attempts time out');
  assert(calls === 2, 'timeout: ran 2 attempts before giving up');
  const tookTimeoutPath = captured.some(m => /timeout after/i.test(m));
  assert(tookTimeoutPath, 'timeout: at least one log message references the timeout');
}

// ---------------------------------------------------------------------------
// 5. Keep-alive cadence: long-running attempt emits "still downloading" pings.
// ---------------------------------------------------------------------------
{
  captured.length = 0;
  const result = await downloadWithUX(
    'keepalive',
    async () => {
      // Run longer than 2 keep-alive intervals to guarantee at least 2 logs.
      await new Promise(r => setTimeout(r, 250));
      return 'done';
    },
    { timeoutMs: 5_000, keepaliveMs: 80, maxAttempts: 1, log: captureLog, sleep: fastSleep },
  );
  assert(result === 'done', 'keepalive: long-running attempt eventually returns');
  const pings = captured.filter(m => /still downloading/.test(m)).length;
  assert(pings >= 2, `keepalive: emitted ${pings} pings (>=2 expected)`);
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

console.log(`# fail: ${failed}`);
console.log(`# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('SOME TESTS FAILED');
  process.exit(1);
}
console.log('ALL TESTS PASSED');
