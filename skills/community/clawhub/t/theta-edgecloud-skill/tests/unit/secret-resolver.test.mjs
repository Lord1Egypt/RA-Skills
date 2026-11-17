import assert from 'node:assert/strict';
import test from 'node:test';

import { resolveThetaOnDemandToken } from '../../build/runtime/secretResolver.js';

test('resolver prioritizes runtime secret provider over env/base fallbacks', async () => {
  const token = await resolveThetaOnDemandToken(
    {
      env: {
        THETA_ONDEMAND_API_TOKEN: 'env-token'
      },
      getSecret: async () => 'provider-token'
    },
    'base-token'
  );

  assert.equal(token, 'provider-token');
});

test('resolver falls back to env token when provider token is unavailable', async () => {
  const token = await resolveThetaOnDemandToken(
    {
      env: {
        THETA_ONDEMAND_API_TOKEN: 'env-token'
      },
      getSecret: async () => undefined
    },
    'base-token'
  );

  assert.equal(token, 'env-token');
});

test('resolver accepts on-demand API key aliases', async () => {
  const token = await resolveThetaOnDemandToken(
    {
      env: {
        THETA_ONDEMAND_API_KEY: 'alias-token'
      },
      getSecret: async () => undefined
    },
    'base-token'
  );

  assert.equal(token, 'alias-token');
});

test('resolver falls back to base token when no other source exists', async () => {
  const token = await resolveThetaOnDemandToken(
    {
      env: {},
      getSecret: async () => undefined
    },
    'base-token'
  );

  assert.equal(token, 'base-token');
});

test('resolver returns undefined when all token sources are empty', async () => {
  const token = await resolveThetaOnDemandToken(
    {
      env: {},
      getSecret: async () => undefined
    },
    undefined
  );

  assert.equal(token, undefined);
});
