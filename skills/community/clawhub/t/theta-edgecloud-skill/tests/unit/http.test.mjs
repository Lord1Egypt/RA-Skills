// Offline: every request is intercepted by a mocked fetch or dry-run; nothing is sent to the network.
import assert from 'node:assert/strict';
import test from 'node:test';

import { getJson } from '../../build/clients/http.js';

async function withMockFetch(mock, fn) {
  const original = globalThis.fetch;
  globalThis.fetch = mock;
  try {
    await fn();
  } finally {
    globalThis.fetch = original;
  }
}

test('getJson retries retryable HTTP statuses and eventually succeeds', async () => {
  let attempts = 0;

  await withMockFetch(async () => {
    attempts += 1;
    if (attempts < 3) {
      return new Response('busy', { status: 503 });
    }
    return new Response(JSON.stringify({ ok: true, attempts }), {
      status: 200,
      headers: { 'content-type': 'application/json' }
    });
  }, async () => {
    const result = await getJson('https://example.local/retry', {
      service: 'test-http',
      maxRetries: 3,
      retryBackoffMs: 25,
      timeoutMs: 5000
    });

    assert.equal(result.ok, true);
    assert.equal(result.attempts, 3);
    assert.equal(attempts, 3);
  });
});

test('getJson does not retry non-retryable HTTP status', async () => {
  let attempts = 0;

  await withMockFetch(async () => {
    attempts += 1;
    return new Response('bad request token=fixture-only', { status: 400 });
  }, async () => {
    await assert.rejects(
      () =>
        getJson('https://example.local/no-retry', {
          service: 'test-http',
          maxRetries: 3,
          retryBackoffMs: 25,
          timeoutMs: 5000
        }),
      (error) => {
        assert.equal(error.code, 'HTTP_400');
        assert.equal(error.retriable, false);
        assert.equal(error.message.includes('fixture-only'), false);
        return true;
      }
    );
  });

  assert.equal(attempts, 1);
});

test('getJson retries transport errors and surfaces NETWORK_ERROR when exhausted', async () => {
  let attempts = 0;

  await withMockFetch(async () => {
    attempts += 1;
    throw new TypeError('socket hang up');
  }, async () => {
    await assert.rejects(
      () =>
        getJson('https://example.local/network', {
          service: 'test-http',
          maxRetries: 2,
          retryBackoffMs: 25,
          timeoutMs: 5000
        }),
      (error) => {
        assert.equal(error.code, 'NETWORK_ERROR');
        assert.equal(error.retriable, true);
        return true;
      }
    );
  });

  assert.equal(attempts, 3);
});
