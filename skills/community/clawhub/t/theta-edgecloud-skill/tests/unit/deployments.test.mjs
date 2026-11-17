// Offline: every request is intercepted by a mocked fetch or dry-run; nothing is sent to the network.
import assert from 'node:assert/strict';
import test from 'node:test';

import { deployments } from '../../build/commands/deployments.js';

const cfg = {
  dryRun: false,
  edgecloudApiKey: 'test-key',
  edgecloudProjectId: 'prj_test',
  edgecloudOrgId: 'org_test',
  httpTimeoutMs: 5000,
  httpMaxRetries: 0,
  httpRetryBackoffMs: 25
};

async function withMockFetch(mock, fn) {
  const original = globalThis.fetch;
  globalThis.fetch = mock;
  try {
    await fn();
  } finally {
    globalThis.fetch = original;
  }
}

test('deployment list falls back from singular to plural route', async () => {
  const urls = [];

  await withMockFetch(async (url) => {
    urls.push(String(url));
    if (String(url).includes('/deployment/list')) {
      return new Response(JSON.stringify({ status: 'error', message: 'not found' }), {
        status: 404,
        headers: { 'content-type': 'application/json' }
      });
    }
    return new Response(JSON.stringify({ body: { deployments: [] } }), {
      status: 200,
      headers: { 'content-type': 'application/json' }
    });
  }, async () => {
    const result = await deployments.list(cfg, 'prj_test');
    assert.deepEqual(result, { body: { deployments: [] } });
  });

  assert.equal(urls[0], 'https://controller.thetaedgecloud.com/deployment/list?project_id=prj_test');
  assert.equal(urls[1], 'https://controller.thetaedgecloud.com/deployments/list?project_id=prj_test');
});

test('route probe reports selected deployment route', async () => {
  await withMockFetch(async (url) => {
    return new Response(JSON.stringify({ route: String(url) }), {
      status: 200,
      headers: { 'content-type': 'application/json' }
    });
  }, async () => {
    const result = await deployments.routeProbe(cfg, 'prj_test');
    assert.equal(result.ok, true);
    assert.equal(result.selectedRoute, 'https://controller.thetaedgecloud.com/deployment/list?project_id=prj_test');
    assert.equal(result.attempts[0].ok, true);
  });
});

test('balance snapshot extracts numeric value', async () => {
  await withMockFetch(async () => {
    return new Response(JSON.stringify({ body: { balances: [{ org_id: 'org_test', balance: 42.5 }] } }), {
      status: 200,
      headers: { 'content-type': 'application/json' }
    });
  }, async () => {
    const result = await deployments.balanceSnapshot(cfg);
    assert.equal(result.skipped, false);
    assert.equal(result.orgId, 'org_test');
    assert.equal(result.value, 42.5);
  });
});

test('validateDisposable dry-run redacts generated auth payload', async () => {
  const result = await deployments.validateDisposable(
    { ...cfg, dryRun: true },
    {
      payload: {
        project_id: 'prj_test',
        deployment_template_id: 'img_test',
        auth_password: 'supersecret-password'
      },
      probe: 'openai',
      readyTimeoutMs: 1000
    }
  );

  assert.equal(result.dryRun, true);
  assert.equal(result.payload.auth_password.includes('supersecret-password'), false);
  assert.equal(result.probe, 'openai');
});

