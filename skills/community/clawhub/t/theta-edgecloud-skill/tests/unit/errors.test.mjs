import assert from 'node:assert/strict';
import test from 'node:test';

import { fromHttpError, fromTransportError, isRetriableHttpError, sanitizeHttpErrorMessage } from '../../build/errors.js';

test('sanitizeHttpErrorMessage redacts bearer and key-value secrets', () => {
  const message = 'Authorization failed: Bearer fixture-bearer token=fixture-token x-api-key: fixture-key x-tva-sa-secret: fixture-video';
  const sanitized = sanitizeHttpErrorMessage(message);

  assert.equal(sanitized.includes('fixture-bearer'), false);
  assert.equal(sanitized.includes('fixture-token'), false);
  assert.equal(sanitized.includes('fixture-key'), false);
  assert.equal(sanitized.includes('fixture-video'), false);
  assert.match(sanitized, /Bearer/);
  assert.match(sanitized, /token=/);
  assert.match(sanitized, /x-api-key:/);
  assert.match(sanitized, /x-tva-sa-secret:/);
});

test('fromHttpError marks retryable statuses and sanitizes body', () => {
  const err = fromHttpError('theta-ondemand', '/infer', 503, 'temporary outage api-key=fixture-key');
  assert.equal(err.code, 'HTTP_503');
  assert.equal(err.retriable, true);
  assert.equal(err.message.includes('fixture-key'), false);
});

test('fromHttpError treats Theta on-demand capacity exhaustion as retriable', () => {
  const err = fromHttpError('theta-ondemand-api', '/infer_request/qwen3', 409, '{"message":"No instances available - try again later"}');

  assert.equal(err.code, 'THETA_ONDEMAND_CAPACITY_EXHAUSTED');
  assert.equal(err.retriable, true);
  assert.equal(err.status, 409);
  assert.equal(isRetriableHttpError(409, 'No instances available - try again later'), true);
});

test('fromTransportError normalizes abort timeout as HTTP_408', () => {
  const abortError = new DOMException('The operation was aborted.', 'AbortError');
  const err = fromTransportError('theta-video', '/stream', abortError);

  assert.equal(err.code, 'HTTP_408');
  assert.equal(err.retriable, true);
  assert.equal(err.status, 408);
});
