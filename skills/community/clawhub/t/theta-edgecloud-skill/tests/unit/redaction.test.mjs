import assert from 'node:assert/strict';
import test from 'node:test';

import { redact, redactObject } from '../../build/redaction.js';

test('redact masks short and long strings', () => {
  assert.equal(redact('abcd'), '[redacted]');
  assert.equal(redact('0123456789abcdef'), '[redacted]');
});

test('redactObject recursively redacts secret-like keys', () => {
  const input = {
    token: 'abcdefghijk',
    nested: {
      api_key: 'my-super-key',
      profile: { name: 'operator', password: 'hunter2-value' }
    },
    list: [{ secret: 'abc12345678' }, { safe: 'ok' }]
  };

  const redacted = redactObject(input);

  assert.equal(redacted.token, '[redacted]');
  assert.equal(redacted.nested.api_key, '[redacted]');
  assert.equal(redacted.nested.profile.password, '[redacted]');
  assert.equal(redacted.list[0].secret, '[redacted]');
  assert.equal(redacted.list[1].safe, 'ok');
});

test('redactObject survives circular objects', () => {
  const input = { token: 'abcdefghi' };
  input.self = input;

  const redacted = redactObject(input);
  assert.equal(redacted.token, '[redacted]');
  assert.equal(redacted.self, '[circular]');
});
