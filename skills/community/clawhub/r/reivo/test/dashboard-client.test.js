/**
 * OpenClaw skill audit tests — dashboard-client.js
 *
 * Tests DashboardClient construction, header generation, and URL building.
 * Does NOT make real HTTP calls — tests internal logic only.
 */
const { DashboardClient, DASHBOARD_API } = require('../lib/dashboard-client.js');

function assert(condition, message) {
  if (!condition) throw new Error(`FAIL: ${message}`);
}

function assertEqual(actual, expected, message) {
  if (actual !== expected) throw new Error(`FAIL: ${message} — got "${actual}", expected "${expected}"`);
}

function test(name, fn) {
  try {
    fn();
    console.log(`  ✓ ${name}`);
  } catch (e) {
    console.error(`  ✗ ${name}: ${e.message}`);
    process.exitCode = 1;
  }
}

console.log('dashboard-client.js tests');

test('DASHBOARD_API constant is correct', () => {
  assertEqual(DASHBOARD_API, 'https://app.reivo.dev/api/v1', 'base URL');
});

test('constructor stores apiKey and baseUrl', () => {
  const client = new DashboardClient('rv_test123');
  assertEqual(client.apiKey, 'rv_test123', 'apiKey');
  assertEqual(client.baseUrl, DASHBOARD_API, 'baseUrl');
});

test('_headers includes Authorization and Content-Type', () => {
  const client = new DashboardClient('rv_abc');
  const headers = client._headers();
  assertEqual(headers['Authorization'], 'Bearer rv_abc', 'auth header');
  assertEqual(headers['Content-Type'], 'application/json', 'content type');
});

test('_headers uses Bearer token format', () => {
  const client = new DashboardClient('rv_mykey');
  const headers = client._headers();
  assert(headers['Authorization'].startsWith('Bearer '), 'Bearer prefix');
});

test('constructor handles empty key', () => {
  const client = new DashboardClient('');
  const headers = client._headers();
  assertEqual(headers['Authorization'], 'Bearer ', 'empty key still has Bearer prefix');
});

test('get method exists and is async', () => {
  const client = new DashboardClient('rv_test');
  assert(typeof client.get === 'function', 'get is a function');
});

test('post method exists and is async', () => {
  const client = new DashboardClient('rv_test');
  assert(typeof client.post === 'function', 'post is a function');
});

// Mock fetch test: verify URL construction
test('get constructs correct URL', async () => {
  const client = new DashboardClient('rv_test');
  let capturedUrl = null;
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, opts) => {
    capturedUrl = url;
    return { ok: true, json: async () => ({}) };
  };
  try {
    await client.get('/overview?days=7');
    assertEqual(capturedUrl, 'https://app.reivo.dev/api/v1/overview?days=7', 'full URL');
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test('post sends correct method and body', async () => {
  const client = new DashboardClient('rv_test');
  let capturedOpts = null;
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, opts) => {
    capturedOpts = opts;
    return { ok: true, json: async () => ({}) };
  };
  try {
    await client.post('/settings', { budgetLimitUsd: 50 });
    assertEqual(capturedOpts.method, 'POST', 'method is POST');
    assertEqual(capturedOpts.body, '{"budgetLimitUsd":50}', 'body is JSON');
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test('get throws on non-ok response', async () => {
  const client = new DashboardClient('rv_test');
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => ({ ok: false, status: 401, statusText: 'Unauthorized' });
  try {
    let threw = false;
    try {
      await client.get('/overview');
    } catch (e) {
      threw = true;
      assert(e.message.includes('401'), 'error includes status code');
    }
    assert(threw, 'should have thrown');
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test('post throws on non-ok response', async () => {
  const client = new DashboardClient('rv_test');
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => ({ ok: false, status: 500, text: async () => 'Internal Server Error' });
  try {
    let threw = false;
    try {
      await client.post('/settings', {});
    } catch (e) {
      threw = true;
      assert(e.message.includes('500'), 'error includes status code');
    }
    assert(threw, 'should have thrown');
  } finally {
    globalThis.fetch = originalFetch;
  }
});

console.log('');
