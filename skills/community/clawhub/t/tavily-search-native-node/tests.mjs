#!/usr/bin/env node
import { spawn, spawnSync } from 'node:child_process';
import assert from 'node:assert/strict';
import path from 'node:path';
import { createServer } from 'node:http';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const script = path.join(__dirname, 'scripts', 'search.mjs');

function run(args, env = {}) {
  return spawnSync(process.execPath, [script, ...args], {
    cwd: __dirname,
    encoding: 'utf8',
    env: { ...process.env, TAVILY_API_KEY: '', ...env },
    timeout: 20000,
  });
}

function runAsync(args, env = {}) {
  return new Promise((resolve) => {
    const child = spawn(process.execPath, [script, ...args], {
      cwd: __dirname,
      env: { ...process.env, TAVILY_API_KEY: '', ...env },
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    let stdout = '';
    let stderr = '';
    const timer = setTimeout(() => child.kill(), 20000);
    child.stdout.on('data', (chunk) => { stdout += chunk; });
    child.stderr.on('data', (chunk) => { stderr += chunk; });
    child.on('close', (status) => {
      clearTimeout(timer);
      resolve({ status, stdout, stderr });
    });
  });
}

{
  const r = spawnSync(process.execPath, ['--check', script], { encoding: 'utf8' });
  assert.equal(r.status, 0, r.stderr);
}

{
  const r = run(['--help']);
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stdout, /Usage: search\.mjs/);
  assert.equal(r.stderr, '');
}

{
  const r = run(['latest ai news']);
  assert.notEqual(r.status, 0);
  assert.equal(r.stdout, '');
  assert.match(r.stderr, /TAVILY_API_KEY not set/);
  assert.doesNotMatch(r.stderr, /SECRET|tvly[-_]|tavily_secret/i);
}

for (const args of [
  ['--bogus', 'query'],
  ['--max', '0', 'query'],
  ['--max', '21', 'query'],
  ['--max', 'abc', 'query'],
  ['--days', '0', 'query'],
  ['--days', '366', 'query'],
  ['--topic', 'bad', 'query'],
  ['--depth', 'deep', 'query'],
  ['--include'],
]) {
  const r = run(args);
  assert.notEqual(r.status, 0, args.join(' '));
  assert.equal(r.stdout, '');
  assert.match(r.stderr, /error:/);
}

{
  const r = run(['query'], { TAVILY_API_KEY: 'test-key-not-real', TAVILY_TIMEOUT_MS: '999' });
  assert.notEqual(r.status, 0);
  assert.equal(r.stdout, '');
  assert.match(r.stderr, /TAVILY_TIMEOUT_MS must be an integer from 1000 to 120000/);
}

{
  const sentinel = 'tavily_secret_DO_NOT_PRINT_12345';
  const r = run(['query'], { TAVILY_API_KEY: sentinel, TAVILY_TIMEOUT_MS: '5000', TAVILY_TEST_ENDPOINT: 'http://127.0.0.1:9/search' });
  assert.notEqual(r.status, 0);
  assert.equal(r.stdout, '');
  assert.match(r.stderr, /error: network/);
  assert.doesNotMatch(r.stderr, new RegExp(sentinel));
}

{
  const sentinel = 'tavily_secret_DO_NOT_PRINT_67890';
  const r = run(['query'], { TAVILY_API_KEY: sentinel, TAVILY_TEST_ENDPOINT: 'http://127.0.0.1:9@example.com/search' });
  assert.notEqual(r.status, 0);
  assert.equal(r.stdout, '');
  assert.match(r.stderr, /TAVILY_TEST_ENDPOINT is only allowed/);
  assert.doesNotMatch(r.stderr, new RegExp(sentinel));
}

async function withServer(handler, fn) {
  const server = createServer(handler);
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  try {
    await fn(origin);
  } finally {
    await new Promise((resolve) => server.close(resolve));
  }
}

await withServer((req, res) => {
  let body = '';
  req.on('data', (chunk) => { body += chunk; });
  req.on('end', () => {
    const payload = JSON.parse(body);
    assert.equal(payload.query, 'query');
    assert.equal(payload.max_results, 1);
    assert.equal(payload.search_depth, 'basic');
    assert.doesNotMatch(body, /tavily_secret/);
    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify({
      answer: 'Short answer',
      response_time: 0.01,
      results: [{ title: 'Example \u201cSmart\u201d Result', url: 'https://example.com', published_date: '2026-05-31', content: 'Smart quotes \u2192 arrows' }],
    }));
  });
}, async (origin) => {
  const sentinel = 'tavily_secret_SUCCESS_DO_NOT_PRINT';
  const r = await runAsync(['--max', '1', 'query'], { TAVILY_API_KEY: sentinel, TAVILY_TEST_ENDPOINT: `${origin}/search` });
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stdout, /Query: query/);
  assert.match(r.stdout, /Example "Smart" Result/);
  assert.match(r.stdout, /Smart quotes -> arrows/);
  assert.doesNotMatch(r.stdout + r.stderr, new RegExp(sentinel));
});

await withServer((_req, res) => {
  res.writeHead(200, { 'content-type': 'application/json' });
  res.end(JSON.stringify({ answer: 'JSON answer', results: [] }));
}, async (origin) => {
  const r = await runAsync(['--json', 'query'], { TAVILY_API_KEY: 'test-key', TAVILY_TEST_ENDPOINT: `${origin}/search` });
  assert.equal(r.status, 0, r.stderr);
  assert.equal(JSON.parse(r.stdout).answer, 'JSON answer');
});

await withServer((_req, res) => {
  res.writeHead(429, { 'content-type': 'application/json', 'retry-after': '12' });
  res.end(JSON.stringify({ detail: 'rate limited' }));
}, async (origin) => {
  const r = await runAsync(['query'], { TAVILY_API_KEY: 'test-key', TAVILY_TEST_ENDPOINT: `${origin}/search` });
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /HTTP 429 \(retry-after: 12s\): rate limited/);
});

await withServer((_req, res) => {
  res.writeHead(429, { 'content-type': 'application/json' });
  res.end(JSON.stringify({ detail: 'rate limited no header' }));
}, async (origin) => {
  const r = await runAsync(['query'], { TAVILY_API_KEY: 'test-key', TAVILY_TEST_ENDPOINT: `${origin}/search` });
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /HTTP 429: rate limited no header/);
});

for (const status of [401, 403, 500, 502, 503]) {
  await withServer((_req, res) => {
    res.writeHead(status, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ detail: `status ${status}` }));
  }, async (origin) => {
    const sentinel = `tavily_secret_STATUS_${status}`;
    const r = await runAsync(['query'], { TAVILY_API_KEY: sentinel, TAVILY_TEST_ENDPOINT: `${origin}/search` });
    assert.notEqual(r.status, 0);
    assert.match(r.stderr, new RegExp(`HTTP ${status}: status ${status}`));
    assert.doesNotMatch(r.stdout + r.stderr, new RegExp(sentinel));
  });
}

await withServer((req, res) => {
  let body = '';
  req.on('data', (chunk) => { body += chunk; });
  req.on('end', () => {
    const payload = JSON.parse(body);
    assert.equal(payload.query, 'latest news');
    assert.equal(payload.topic, 'news');
    assert.equal(payload.search_depth, 'advanced');
    assert.equal(payload.max_results, 5);
    assert.equal(payload.days, 7);
    assert.deepEqual(payload.include_domains, ['example.com']);
    assert.deepEqual(payload.exclude_domains, ['bad.example']);
    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ answer: 'ok', results: [] }));
  });
}, async (origin) => {
  const r = await runAsync(['--topic', 'news', '--depth', 'advanced', '--max', '5', '--days', '7', '--include', 'example.com', '--exclude', 'bad.example', 'latest news'], { TAVILY_API_KEY: 'test-key', TAVILY_TEST_ENDPOINT: `${origin}/search` });
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stdout, /Query: latest news/);
});

await withServer((_req, res) => {
  res.writeHead(200, { 'content-type': 'application/json' });
  res.end('not json');
}, async (origin) => {
  const r = await runAsync(['query'], { TAVILY_API_KEY: 'test-key', TAVILY_TEST_ENDPOINT: `${origin}/search` });
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /invalid JSON response/);
});

await withServer((_req, res) => {
  setTimeout(() => {
    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ answer: 'too late', results: [] }));
  }, 1500);
}, async (origin) => {
  const r = await runAsync(['query'], { TAVILY_API_KEY: 'test-key', TAVILY_TIMEOUT_MS: '1000', TAVILY_TEST_ENDPOINT: `${origin}/search` });
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /network timeout after 1000ms/);
});

console.log('tavily-search-native-node tests passed');
