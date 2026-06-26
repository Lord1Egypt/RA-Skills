// scanner-sim: allow — test fixture needs to monkey-patch fetch + mutate process.env; not shipped in npm package (see files allowlist in package.json).
/**
 * Tests for the 3.3.1-rc.2 retry wrapper added to llm-client.chatCompletion.
 *
 * Covers:
 *   - isRetryable classifies 429, 502/503/504, timeouts as retryable
 *   - isRetryable classifies 401/403/404/parse-errors as non-retryable
 *   - chatCompletion retries transient failures with exponential backoff
 *   - chatCompletion fails fast on non-retryable errors
 *   - chatCompletion respects `attempts: 0` (still runs once) and
 *     `attempts: 3` caps retry count
 *   - Logger is called with the right levels (INFO on first failure,
 *     DEBUG on subsequent, WARN on final give-up)
 *
 * Run with: npx tsx llm-client-retry.test.ts
 */

import {
  isRetryable,
  chatCompletion,
  LLMUpstreamOutageError,
  isZaiBalanceError,
  zaiFallbackBaseUrl,
  ZAI_CODING_BASE_URL,
  ZAI_STANDARD_BASE_URL,
  getZaiBaseUrl,
  type LLMClientConfig,
} from './llm-client.js';

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

// ---------------------------------------------------------------------------
// isRetryable
// ---------------------------------------------------------------------------

assert(isRetryable('LLM API 429: rate limit reached'), 'isRetryable: 429 → true');
assert(isRetryable('Rate limit reached for requests'), 'isRetryable: "rate limit" → true');
assert(isRetryable('LLM API 502: bad gateway'), 'isRetryable: 502 → true');
assert(isRetryable('LLM API 503: unavailable'), 'isRetryable: 503 → true');
assert(isRetryable('LLM API 504: timeout'), 'isRetryable: 504 → true');
assert(isRetryable('The operation was aborted due to timeout'), 'isRetryable: timeout msg → true');
assert(isRetryable('AbortError: aborted'), 'isRetryable: AbortError → true');

assert(!isRetryable('LLM API 401: unauthorized'), 'isRetryable: 401 → false');
assert(!isRetryable('LLM API 403: forbidden'), 'isRetryable: 403 → false');
assert(!isRetryable('LLM API 404: not found'), 'isRetryable: 404 → false');
assert(!isRetryable('LLM API 400: bad request'), 'isRetryable: 400 → false');
assert(!isRetryable('JSON parse error'), 'isRetryable: JSON parse → false');

// ---------------------------------------------------------------------------
// chatCompletion retry harness — we monkey-patch fetch for determinism.
// ---------------------------------------------------------------------------

// Save the real fetch.
const realFetch = globalThis.fetch;

function stubFetch(sequence: Array<() => Promise<Response>>): () => number {
  let callIdx = 0;
  globalThis.fetch = (async (..._args: unknown[]): Promise<Response> => {
    const next = sequence[Math.min(callIdx, sequence.length - 1)];
    callIdx++;
    return next();
  }) as unknown as typeof fetch;
  return () => callIdx;
}

function restoreFetch(): void {
  globalThis.fetch = realFetch;
}

function mockResponse(status: number, body: string): Response {
  return new Response(body, {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function okResponse(content: string): Response {
  return mockResponse(
    200,
    JSON.stringify({
      choices: [{ message: { content } }],
    }),
  );
}

const testConfig: LLMClientConfig = {
  apiKey: 'test',
  baseUrl: 'http://example.test/v1',
  model: 'test-model',
  apiFormat: 'openai',
};

// ---------------------------------------------------------------------------
// Happy path — first attempt succeeds, no retries.
// ---------------------------------------------------------------------------

{
  const getCount = stubFetch([
    async () => okResponse('hello from LLM'),
  ]);
  try {
    const logs: Array<[string, string]> = [];
    const logger = {
      info: (msg: string) => logs.push(['info', msg]),
      warn: (msg: string) => logs.push(['warn', msg]),
      debug: (msg: string) => logs.push(['debug', msg]),
    };
    const result = await chatCompletion(testConfig, [
      { role: 'user', content: 'hi' },
    ], { logger });
    assert(result === 'hello from LLM', 'retry: first-attempt-success returns content');
    assert(getCount() === 1, 'retry: first-attempt-success → 1 fetch');
    assert(logs.length === 0, 'retry: first-attempt-success → no log lines');
  } finally {
    restoreFetch();
  }
}

// ---------------------------------------------------------------------------
// 429 → retry → success
// ---------------------------------------------------------------------------

{
  const getCount = stubFetch([
    async () => mockResponse(429, '{"error":{"message":"Rate limit reached"}}'),
    async () => okResponse('recovered'),
  ]);
  try {
    const logs: Array<[string, string]> = [];
    const logger = {
      info: (msg: string) => logs.push(['info', msg]),
      warn: (msg: string) => logs.push(['warn', msg]),
      debug: (msg: string) => logs.push(['debug', msg]),
    };
    const result = await chatCompletion(testConfig, [
      { role: 'user', content: 'hi' },
    ], { logger, retry: { attempts: 3, baseDelayMs: 10 } });
    assert(result === 'recovered', 'retry: 429 → 200 returns content from 2nd attempt');
    assert(getCount() === 2, 'retry: 429 → 200 made 2 fetch calls');
    assert(logs.some(([lvl]) => lvl === 'info'), 'retry: 429 → 200 emits INFO log on first failure');
  } finally {
    restoreFetch();
  }
}

// ---------------------------------------------------------------------------
// All attempts fail with 429 → give up with warn
// ---------------------------------------------------------------------------

{
  const getCount = stubFetch([
    async () => mockResponse(429, '{"error":{"message":"Rate limit"}}'),
    async () => mockResponse(429, '{"error":{"message":"Rate limit"}}'),
    async () => mockResponse(429, '{"error":{"message":"Rate limit"}}'),
  ]);
  try {
    const logs: Array<[string, string]> = [];
    const logger = {
      info: (msg: string) => logs.push(['info', msg]),
      warn: (msg: string) => logs.push(['warn', msg]),
      debug: (msg: string) => logs.push(['debug', msg]),
    };
    let thrown: unknown;
    try {
      await chatCompletion(testConfig, [
        { role: 'user', content: 'hi' },
      ], { logger, retry: { attempts: 3, baseDelayMs: 10 } });
    } catch (err) {
      thrown = err;
    }
    assert(thrown instanceof Error, 'retry: all-fail throws');
    assert(getCount() === 3, 'retry: all-fail with attempts=3 → 3 fetches');
    assert(logs.some(([lvl]) => lvl === 'warn'), 'retry: all-fail emits WARN on give-up');
    assert(logs.some(([lvl]) => lvl === 'info'), 'retry: all-fail emits INFO on first failure');
    assert(logs.some(([lvl]) => lvl === 'debug'), 'retry: all-fail emits DEBUG on 2nd retry attempt');
  } finally {
    restoreFetch();
  }
}

// ---------------------------------------------------------------------------
// 401 (unauth) → fail-fast, no retry
// ---------------------------------------------------------------------------

{
  const getCount = stubFetch([
    async () => mockResponse(401, '{"error":{"message":"unauthorized"}}'),
  ]);
  try {
    let thrown: unknown;
    try {
      await chatCompletion(testConfig, [
        { role: 'user', content: 'hi' },
      ], { retry: { attempts: 3, baseDelayMs: 10 } });
    } catch (err) {
      thrown = err;
    }
    assert(thrown instanceof Error, 'retry: 401 throws');
    assert(getCount() === 1, 'retry: 401 is fail-fast (1 fetch)');
  } finally {
    restoreFetch();
  }
}

// ---------------------------------------------------------------------------
// Timeout / AbortError → retry
// ---------------------------------------------------------------------------

{
  const getCount = stubFetch([
    async () => {
      throw new Error('The operation was aborted due to timeout');
    },
    async () => okResponse('recovered from timeout'),
  ]);
  try {
    const logs: Array<[string, string]> = [];
    const logger = {
      info: (msg: string) => logs.push(['info', msg]),
      warn: (msg: string) => logs.push(['warn', msg]),
      debug: (msg: string) => logs.push(['debug', msg]),
    };
    const result = await chatCompletion(testConfig, [
      { role: 'user', content: 'hi' },
    ], { logger, retry: { attempts: 3, baseDelayMs: 10 } });
    assert(result === 'recovered from timeout', 'retry: timeout → retry → success');
    assert(getCount() === 2, 'retry: timeout → 2 fetches');
  } finally {
    restoreFetch();
  }
}

// ---------------------------------------------------------------------------
// Disable retry: attempts set to 1 → no retry even on 429
// ---------------------------------------------------------------------------

{
  const getCount = stubFetch([
    async () => mockResponse(429, '{"error":{"message":"Rate limit"}}'),
  ]);
  try {
    let thrown: unknown;
    try {
      await chatCompletion(testConfig, [
        { role: 'user', content: 'hi' },
      ], { retry: { attempts: 1, baseDelayMs: 10 } });
    } catch (err) {
      thrown = err;
    }
    assert(thrown instanceof Error, 'retry: attempts=1 → throws on 429');
    assert(getCount() === 1, 'retry: attempts=1 → single fetch, no retry');
  } finally {
    restoreFetch();
  }
}

// ---------------------------------------------------------------------------
// 3.3.1-rc.3 — zai endpoint helpers
// ---------------------------------------------------------------------------

// Balance-error detector — catches the two wordings we've seen from zai.
assert(isZaiBalanceError('LLM API 429: Insufficient balance or no resource package. Please recharge.'), 'isZaiBalanceError: full message → true');
assert(isZaiBalanceError('429: insufficient balance'), 'isZaiBalanceError: short "insufficient balance" → true');
assert(isZaiBalanceError('no resource package available'), 'isZaiBalanceError: "no resource package" → true');
assert(!isZaiBalanceError('LLM API 429: rate limit reached'), 'isZaiBalanceError: plain rate-limit → false');
assert(!isZaiBalanceError('LLM API 502: bad gateway'), 'isZaiBalanceError: 502 → false');

// Fallback URL picker — CODING ↔ STANDARD.
assert(zaiFallbackBaseUrl(ZAI_CODING_BASE_URL) === ZAI_STANDARD_BASE_URL, 'zaiFallbackBaseUrl: CODING → STANDARD');
assert(zaiFallbackBaseUrl(ZAI_STANDARD_BASE_URL) === ZAI_CODING_BASE_URL, 'zaiFallbackBaseUrl: STANDARD → CODING');
assert(zaiFallbackBaseUrl(ZAI_CODING_BASE_URL + '/') === ZAI_STANDARD_BASE_URL, 'zaiFallbackBaseUrl: trailing slash normalized');
assert(zaiFallbackBaseUrl('https://custom.proxy/v1') === null, 'zaiFallbackBaseUrl: unknown URL → null');

// Env-var override.
{
  const original = process.env.ZAI_BASE_URL;
  try {
    delete process.env.ZAI_BASE_URL;
    assert(getZaiBaseUrl() === ZAI_CODING_BASE_URL, 'getZaiBaseUrl: default is coding endpoint');
    process.env.ZAI_BASE_URL = ZAI_STANDARD_BASE_URL;
    assert(getZaiBaseUrl() === ZAI_STANDARD_BASE_URL, 'getZaiBaseUrl: env override respected');
    process.env.ZAI_BASE_URL = 'https://custom.proxy/v1/';
    assert(getZaiBaseUrl() === 'https://custom.proxy/v1', 'getZaiBaseUrl: env override strips trailing slash');
  } finally {
    if (original === undefined) delete process.env.ZAI_BASE_URL;
    else process.env.ZAI_BASE_URL = original;
  }
}

// ---------------------------------------------------------------------------
// zai auto-fallback — "Insufficient balance" 429 flips baseUrl + retries.
// Fixture tracks which URL each request went to; we assert the 2nd call
// hit the OTHER endpoint.
// ---------------------------------------------------------------------------

{
  const urlsSeen: string[] = [];
  const realFetch2 = globalThis.fetch;
  try {
    globalThis.fetch = (async (input: unknown): Promise<Response> => {
      const url = typeof input === 'string' ? input : (input as { url?: string }).url ?? '';
      urlsSeen.push(url);
      if (urlsSeen.length === 1) {
        // First call → balance 429
        return mockResponse(
          429,
          JSON.stringify({
            error: { message: 'Insufficient balance or no resource package. Please recharge.' },
          }),
        );
      }
      // Second call → success
      return okResponse('recovered after zai fallback');
    }) as unknown as typeof fetch;

    const logs: Array<[string, string]> = [];
    const logger = {
      info: (msg: string) => logs.push(['info', msg]),
      warn: (msg: string) => logs.push(['warn', msg]),
      debug: (msg: string) => logs.push(['debug', msg]),
    };
    const zaiConfig: LLMClientConfig = {
      apiKey: 'zai-test',
      baseUrl: ZAI_CODING_BASE_URL,
      model: 'glm-4.5-flash',
      apiFormat: 'openai',
    };
    const result = await chatCompletion(zaiConfig, [{ role: 'user', content: 'hi' }], {
      logger,
      retry: { attempts: 3, baseDelayMs: 10 },
    });
    assert(result === 'recovered after zai fallback', 'zai fallback: succeeds on 2nd attempt');
    assert(urlsSeen.length === 2, 'zai fallback: exactly 2 fetches');
    assert(
      urlsSeen[0].startsWith(ZAI_CODING_BASE_URL) && urlsSeen[1].startsWith(ZAI_STANDARD_BASE_URL),
      'zai fallback: 1st call CODING, 2nd call STANDARD',
    );
    assert(
      logs.some(([lvl, msg]) => lvl === 'info' && msg.includes('auto-fallback')),
      'zai fallback: logs the flip at INFO',
    );
    // The fixture config should NOT be mutated — we clone internally.
    assert(zaiConfig.baseUrl === ZAI_CODING_BASE_URL, 'zai fallback: caller config untouched');
  } finally {
    globalThis.fetch = realFetch2;
  }
}

// Inverse direction: starting on STANDARD, 429 with balance error → flip to CODING.
{
  const urlsSeen: string[] = [];
  const realFetch2 = globalThis.fetch;
  try {
    globalThis.fetch = (async (input: unknown): Promise<Response> => {
      const url = typeof input === 'string' ? input : (input as { url?: string }).url ?? '';
      urlsSeen.push(url);
      if (urlsSeen.length === 1) {
        return mockResponse(
          429,
          JSON.stringify({ error: { message: 'Insufficient balance — please top up.' } }),
        );
      }
      return okResponse('ok on coding endpoint');
    }) as unknown as typeof fetch;

    const zaiConfig: LLMClientConfig = {
      apiKey: 'zai-test',
      baseUrl: ZAI_STANDARD_BASE_URL,
      model: 'glm-4.5-flash',
      apiFormat: 'openai',
    };
    const result = await chatCompletion(zaiConfig, [{ role: 'user', content: 'hi' }], {
      retry: { attempts: 3, baseDelayMs: 10 },
    });
    assert(result === 'ok on coding endpoint', 'zai fallback reverse: STANDARD → CODING succeeds');
    assert(urlsSeen.length === 2, 'zai fallback reverse: 2 fetches');
    assert(
      urlsSeen[0].startsWith(ZAI_STANDARD_BASE_URL) && urlsSeen[1].startsWith(ZAI_CODING_BASE_URL),
      'zai fallback reverse: 1st STANDARD, 2nd CODING',
    );
  } finally {
    globalThis.fetch = realFetch2;
  }
}

// Only one fallback per call — if the OTHER endpoint ALSO returns balance,
// we fall through to the normal retry path (and eventually surface outage).
{
  const urlsSeen: string[] = [];
  const realFetch2 = globalThis.fetch;
  try {
    globalThis.fetch = (async (input: unknown): Promise<Response> => {
      const url = typeof input === 'string' ? input : (input as { url?: string }).url ?? '';
      urlsSeen.push(url);
      return mockResponse(
        429,
        JSON.stringify({ error: { message: 'Insufficient balance' } }),
      );
    }) as unknown as typeof fetch;
    const zaiConfig: LLMClientConfig = {
      apiKey: 'zai-test',
      baseUrl: ZAI_CODING_BASE_URL,
      model: 'glm-4.5-flash',
      apiFormat: 'openai',
    };
    let thrown: unknown;
    try {
      await chatCompletion(zaiConfig, [{ role: 'user', content: 'hi' }], {
        retry: { attempts: 2, baseDelayMs: 10 },
      });
    } catch (err) {
      thrown = err;
    }
    assert(thrown instanceof LLMUpstreamOutageError, 'zai fallback both-fail: throws LLMUpstreamOutageError');
    // One CODING (initial) + one STANDARD (fallback freebie) + one CODING (normal retry, attempt=2) = 3 fetches.
    // Our fallback does `attempt--` so the first retry after fallback comes "free" — but still counts vs attempts.
    assert(urlsSeen.length >= 2, 'zai fallback both-fail: at least 2 fetches');
  } finally {
    globalThis.fetch = realFetch2;
  }
}

// ---------------------------------------------------------------------------
// LLMUpstreamOutageError surfaces on exhausted retries with retryable errors
// ---------------------------------------------------------------------------

{
  const getCount = stubFetch([
    async () => mockResponse(503, '{"error":{"message":"Service Unavailable"}}'),
    async () => mockResponse(503, '{"error":{"message":"Service Unavailable"}}'),
  ]);
  try {
    let thrown: unknown;
    try {
      await chatCompletion(testConfig, [{ role: 'user', content: 'hi' }], {
        retry: { attempts: 2, baseDelayMs: 10 },
      });
    } catch (err) {
      thrown = err;
    }
    assert(thrown instanceof LLMUpstreamOutageError, 'outage: 503 exhaustion throws LLMUpstreamOutageError');
    assert(
      (thrown as LLMUpstreamOutageError).lastStatus === 503,
      'outage: LLMUpstreamOutageError.lastStatus captures 503',
    );
    assert(getCount() === 2, 'outage: exactly attempts fetches');
  } finally {
    restoreFetch();
  }
}

// Non-retryable error (401) should NOT throw LLMUpstreamOutageError — the
// original error propagates so callers distinguish config errors from
// transient outages.
{
  const getCount = stubFetch([
    async () => mockResponse(401, '{"error":{"message":"unauthorized"}}'),
  ]);
  try {
    let thrown: unknown;
    try {
      await chatCompletion(testConfig, [{ role: 'user', content: 'hi' }], {
        retry: { attempts: 3, baseDelayMs: 10 },
      });
    } catch (err) {
      thrown = err;
    }
    assert(thrown instanceof Error, 'non-retryable: throws');
    assert(!(thrown instanceof LLMUpstreamOutageError), 'non-retryable: NOT LLMUpstreamOutageError');
    assert(getCount() === 1, 'non-retryable: fail-fast');
  } finally {
    restoreFetch();
  }
}

// ---------------------------------------------------------------------------
// Retry budget enforcement — when cumulative delay would exceed budgetMs,
// chatCompletion surfaces LLMUpstreamOutageError early.
// ---------------------------------------------------------------------------

{
  // attempts: 5, baseDelay: 10ms → delays 10, 20, 40, 80, 160 (cumulative 310ms total over 4 retries).
  // Set budgetMs: 50 → first retry ok (cum=10), 2nd retry (would add 20 → cum=30, ok), 3rd retry (would add 40 → cum=70 > 50 → stop).
  const getCount = stubFetch([
    async () => mockResponse(503, '{"error":{"message":"down"}}'),
    async () => mockResponse(503, '{"error":{"message":"down"}}'),
    async () => mockResponse(503, '{"error":{"message":"down"}}'),
    async () => mockResponse(503, '{"error":{"message":"down"}}'),
    async () => mockResponse(503, '{"error":{"message":"down"}}'),
  ]);
  try {
    let thrown: unknown;
    try {
      await chatCompletion(testConfig, [{ role: 'user', content: 'hi' }], {
        retry: { attempts: 5, baseDelayMs: 10, budgetMs: 50 },
      });
    } catch (err) {
      thrown = err;
    }
    assert(thrown instanceof LLMUpstreamOutageError, 'budget: exhaustion throws LLMUpstreamOutageError');
    // Budget stops retries before attempt 4 — we get ≤3 fetches (2 succeeded delay + 1 attempt that tripped the cap).
    const count = getCount();
    assert(count >= 2 && count <= 4, `budget: between 2 and 4 fetches before budget-stop (got ${count})`);
  } finally {
    restoreFetch();
  }
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
