import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import { redactObject, redactString } from '../scripts/lib/redact.mjs';

describe('redactString', () => {
  it('redacts Figma tokens, client secrets, Authorization headers, and FIGMA env values', () => {
    const input = [
      'Authorization: Bearer figd_access_token_123456',
      'FIGMA_ACCESS_TOKEN=figd_access_token_123456',
      'FIGMA_REFRESH_TOKEN=refresh-token-secret',
      'FIGMA_CLIENT_SECRET=client-secret-value',
      'client_secret=client-secret-value',
      'access_token=figd_access_token_123456',
      'refresh_token=refresh-token-secret',
    ].join('\n');

    const redacted = redactString(input, {
      secrets: ['figd_access_token_123456', 'refresh-token-secret', 'client-secret-value'],
    });

    assert.equal(redacted.includes('figd_access_token_123456'), false);
    assert.equal(redacted.includes('refresh-token-secret'), false);
    assert.equal(redacted.includes('client-secret-value'), false);
    assert.match(redacted, /Authorization: Bearer \[REDACTED\]/);
    assert.match(redacted, /FIGMA_ACCESS_TOKEN=\[REDACTED\]/);
    assert.match(redacted, /FIGMA_REFRESH_TOKEN=\[REDACTED\]/);
    assert.match(redacted, /FIGMA_CLIENT_SECRET=\[REDACTED\]/);
  });
});

describe('redactObject', () => {
  it('redacts nested sensitive keys without mutating the input object', () => {
    const input = {
      accessToken: 'access-secret',
      nested: {
        headers: {
          Authorization: 'Bearer access-secret',
        },
        keep: 'visible',
      },
    };

    const redacted = redactObject(input);

    assert.deepEqual(redacted, {
      accessToken: '[REDACTED]',
      nested: {
        headers: {
          Authorization: '[REDACTED]',
        },
        keep: 'visible',
      },
    });
    assert.equal(input.accessToken, 'access-secret');
  });
});
