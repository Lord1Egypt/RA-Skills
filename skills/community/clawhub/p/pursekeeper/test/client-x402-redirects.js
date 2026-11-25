'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { createServer } = require('node:http');
const { randomBytes } = require('node:crypto');
const { execFile } = require('node:child_process');
const { promisify } = require('node:util');
const { resolve } = require('node:path');

const exec = promisify(execFile);
const root = resolve(__dirname, '..');
const client = resolve(root, 'scripts/client-x402.js');
const redirectStatuses = [301, 302, 307, 308];

async function readBody(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  return Buffer.concat(chunks).toString('utf8');
}

async function listen(t, handler) {
  const server = createServer(handler);
  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', resolve);
  });
  t.after(async () => {
    if (!server.listening) return;
    server.closeAllConnections?.();
    await new Promise((resolve, reject) => server.close(error => error ? reject(error) : resolve()));
  });
  const address = server.address();
  return { server, origin: `http://127.0.0.1:${address.port}` };
}

async function runClient(url, { method = 'GET', body, headers } = {}) {
  const env = {
    NANO_SEED: randomBytes(32).toString('hex'),
    NANO_INDEX: '0',
    NANO_LOCK: '0',
    API: new URL(url).origin,
    METHOD: method,
  };
  if (body !== undefined) env.BODY = body;
  if (headers !== undefined) env.HEADERS = JSON.stringify(headers);

  try {
    const result = await exec(process.execPath, [client, url], {
      cwd: root,
      env,
      timeout: 5000,
      maxBuffer: 1024 * 1024,
    });
    return { code: 0, stdout: result.stdout, stderr: result.stderr };
  } catch (error) {
    if (error.code === 'ETIMEDOUT') throw error;
    return {
      code: error.code,
      stdout: error.stdout || '',
      stderr: error.stderr || '',
    };
  }
}

const crossOriginCases = [
  { method: 'GET', label: 'GET without BODY or HEADERS' },
  { method: 'GET', headers: { 'x-redirect-test': 'present' }, label: 'GET without BODY, with HEADERS' },
  { method: 'POST', body: '{"probe":"body-sentinel"}', label: 'POST with BODY, without HEADERS' },
  { method: 'POST', body: '{"probe":"body-sentinel"}', headers: { 'x-redirect-test': 'present' }, label: 'POST with BODY and HEADERS' },
  { method: 'POST', label: 'POST without BODY or HEADERS' },
  { method: 'PUT', headers: { 'x-redirect-test': 'present' }, label: 'PUT without BODY, with HEADERS' },
  { method: 'DELETE', label: 'DELETE without BODY or HEADERS' },
];

for (const status of redirectStatuses) {
  for (const config of crossOriginCases) {
    test(`unsigned quote refuses cross-origin ${status}: ${config.label}`, async t => {
      const targetHits = [];
      const target = await listen(t, async (req, res) => {
        targetHits.push({ method: req.method, body: await readBody(req) });
        res.writeHead(200, { 'content-type': 'text/plain' });
        res.end('target reached');
      });

      const sourceHits = [];
      const source = await listen(t, async (req, res) => {
        sourceHits.push({ method: req.method, body: await readBody(req), testHeader: req.headers['x-redirect-test'] });
        res.writeHead(status, { location: target.origin + '/sink' });
        res.end();
      });

      const result = await runClient(source.origin + '/quote', config);
      assert.equal(result.code, 6, result.stderr);
      assert.match(result.stderr, /Cross-origin redirects are refused even when HEADERS are absent/);
      assert.equal(sourceHits.length, 1, 'the original quote endpoint receives exactly one request');
      assert.equal(sourceHits[0].method, config.method);
      assert.equal(sourceHits[0].body, config.body || '');
      assert.equal(sourceHits[0].testHeader, config.headers?.['x-redirect-test']);
      assert.deepEqual(targetHits, [], 'no request reaches the cross-origin redirect target');
    });
  }
}

for (const config of [
  { method: 'GET', status: 302, label: 'GET without HEADERS' },
  { method: 'POST', status: 301, body: '{"sameOrigin":"post"}', label: 'POST with BODY, no HEADERS' },
  { method: 'POST', status: 308, body: '{"sameOrigin":"post"}', headers: { 'x-redirect-test': 'post' }, label: 'POST with BODY and HEADERS' },
  { method: 'PUT', status: 307, headers: { 'x-redirect-test': 'put' }, label: 'PUT without BODY' },
]) {
  test(`unsigned quote still follows same-origin ${config.status} for ${config.label}`, async t => {
    let origin;
    const hits = [];
    const { origin: startedOrigin } = await listen(t, async (req, res) => {
      const body = await readBody(req);
      hits.push({ path: new URL(req.url, origin).pathname, method: req.method, body, testHeader: req.headers['x-redirect-test'] });
      if (req.url === '/quote') {
        res.writeHead(config.status, { location: origin + '/final' });
        res.end();
        return;
      }
      res.writeHead(200, { 'content-type': 'text/plain' });
      res.end('same-origin response');
    });
    origin = startedOrigin;

    const result = await runClient(origin + '/quote', config);
    assert.equal(result.code, 0, result.stderr);
    assert.match(result.stdout, /^200 same-origin response/);
    assert.deepEqual(hits, [
      { path: '/quote', method: config.method, body: config.body || '', testHeader: config.headers?.['x-redirect-test'] },
      { path: '/final', method: config.method, body: config.body || '', testHeader: config.headers?.['x-redirect-test'] },
    ]);
  });
}

for (const bad of [
  { label: 'zero amount ("0")', patch: { amount: '0' }, match: /accepted\.amount "0" must be a positive integer string in raw/ },
  { label: 'empty amount ("")', patch: { amount: '' }, match: /accepted\.amount "" must be a positive integer string in raw/ },
  { label: 'negative amount ("-1000")', patch: { amount: '-1000' }, match: /accepted\.amount "-1000" must be a positive integer string in raw/ },
  { label: 'above supply ceiling', patch: { amount: '133248297920938463463374607431768211456' }, match: /exceeds the Nano supply ceiling/ },
  { label: 'invalid payTo address', patch: { payTo: 'nano_1badaddress' }, match: /accepted\.payTo .* is not a valid Nano address/ },
  { label: 'wrong asset', patch: { asset: 'USDC' }, match: /accepted\.asset is "USDC", expected "XNO"/ },
]) {
  test(`client-x402 refuses malformed 402 quote before account_info or signing: ${bad.label}`, async t => {
    let accountInfoHits = 0;
    const { origin } = await listen(t, async (req, res) => {
      if (req.url.startsWith('/v1/account_info')) {
        accountInfoHits++;
        res.writeHead(200, { 'content-type': 'application/json' });
        res.end(JSON.stringify({ found: true }));
        return;
      }
      const pr = {
        x402Version: 2,
        resource: { url: 'https://seller.example/paid' },
        accepts: [{
          scheme: 'exact',
          network: 'nano:mainnet',
          asset: 'XNO',
          amount: '1000000000000000000000000000',
          payTo: 'nano_1xug1q5t7nxoj3ywwzokiea9jz8fq8qfgzp8pbyfr3co3e5xgj755uofu8ue',
          maxTimeoutSeconds: 60,
          extra: { workOptional: true },
          ...bad.patch,
        }],
      };
      res.writeHead(402, {
        'content-type': 'application/json',
        'payment-required': Buffer.from(JSON.stringify(pr)).toString('base64'),
      });
      res.end(JSON.stringify({ x402: pr }));
    });

    const result = await runClient(origin + '/paid');
    assert.equal(result.code, 4, result.stderr);
    assert.match(result.stderr, bad.match);
    assert.equal(accountInfoHits, 0, 'must refuse before reading account_info or acquiring wallet lock');
  });
}
