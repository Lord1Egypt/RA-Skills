#!/usr/bin/env node
import { spawn, spawnSync } from 'node:child_process';
import assert from 'node:assert/strict';
import path from 'node:path';
import { readFileSync } from 'node:fs';
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
  const skillMd = readFileSync(path.join(__dirname, 'SKILL.md'), 'utf8');
  const frontmatterName = skillMd.match(/^name:\s*([^\r\n]+)/m)?.[1];
  const frontmatterDescription = skillMd.match(/^description:\s*([^\r\n]+)/m)?.[1];
  const frontmatterVersion = skillMd.match(/^version:\s*([^\r\n]+)/m)?.[1];
  const frontmatterRiskClass = skillMd.match(/^risk_class:\s*([^\r\n]+)/m)?.[1];
  const bodyVersion = skillMd.match(/^Version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*\//m)?.[1];
  assert.equal(frontmatterName, 'tavily-search-native-node', 'frontmatter name must match the skill slug');
  assert.equal(
    frontmatterDescription,
    "Minimal Tavily web search for OpenClaw - native Node.js, zero dependencies, small audit surface. Use when the user asks to search the web, look up current information, find news, research a topic, check recent events, compare options, or get current or recent web information. Returns Tavily's synthesized answer plus source URLs/snippets for verification. Requires TAVILY_API_KEY in the process environment. NOT for scraping individual URLs; use the platform URL-fetch/read tool when available. For caching, raw content, extract endpoint, and usage stats, use a separately reviewed Pro Tavily skill/package when available.",
    'frontmatter description must retain the reviewed public trigger/scope/env boundary'
  );
  assert.equal(frontmatterRiskClass, 'external-research-api-credit-usage-query-privacy-and-shell-invocation-boundary', 'frontmatter risk_class must retain the reviewed external-send/privacy/invocation boundary');
  assert.equal(bodyVersion, frontmatterVersion, 'visible body version must match frontmatter version');
}

{
  const r = run(['--help']);
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stdout, /Usage: search\.mjs/);
  assert.match(r.stdout, /--json\s+redacted JSON output/);
  assert.match(r.stdout, /TAVILY_TEST_ENDPOINT is local-test-only/);
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

{
  const sentinel = 'tvly-real-looking-key-DO-NOT-SEND';
  const r = run(['query'], { TAVILY_API_KEY: sentinel, TAVILY_TEST_ENDPOINT: 'http://127.0.0.1:9/search' });
  assert.notEqual(r.status, 0);
  assert.equal(r.stdout, '');
  assert.match(r.stderr, /requires a clearly dummy\/local\/test TAVILY_API_KEY/);
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

let redirectedHit = false;
let redirectedBody = '';
await withServer((redirectedReq, redirectedRes) => {
  redirectedHit = true;
  redirectedReq.on('data', (chunk) => { redirectedBody += chunk; });
  redirectedReq.on('end', () => {
    redirectedRes.writeHead(500, { 'content-type': 'text/plain' });
    redirectedRes.end('redirect target should not receive request');
  });
}, async (redirectTargetOrigin) => {
  let initialReceivedBody = '';
  await withServer((req, res) => {
    req.on('data', (chunk) => { initialReceivedBody += chunk; });
    req.on('end', () => {
      res.writeHead(307, { location: `${redirectTargetOrigin}/leak-target` });
      res.end('redirecting');
    });
  }, async (origin) => {
    const r = await runAsync(['--include', 'sensitive.example', 'redirect containment query'], { TAVILY_API_KEY: 'test-key', TAVILY_TEST_ENDPOINT: `${origin}/search` });
    assert.notEqual(r.status, 0);
    assert.match(r.stderr, /HTTP 307: redirect refused/);
    assert.match(initialReceivedBody, /redirect containment query/);
    assert.equal(redirectedHit, false, 'redirect target must not receive any redirected request');
    assert.equal(redirectedBody, '', 'redirect target must not receive forwarded POST body');
    assert.doesNotMatch(r.stdout + r.stderr, /redirect containment query|sensitive\.example/);
  });
});

await withServer((req, res) => {
  let body = '';
  req.on('data', (chunk) => { body += chunk; });
  req.on('end', () => {
    const payload = JSON.parse(body);
    assert.equal(payload.query, 'literal ; & | < > $HOME $(Get-Content secret) `whoami` %USERNAME% !VAR!');
    assert.equal(payload.max_results, 1);
    assert.doesNotMatch(body, /secret file contents|whoami-output/i);
    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ answer: 'metacharacters stayed argv data', results: [] }));
  });
}, async (origin) => {
  const metacharQuery = 'literal ; & | < > $HOME $(Get-Content secret) `whoami` %USERNAME% !VAR!';
  const r = await runAsync(['--max', '1', metacharQuery], { TAVILY_API_KEY: 'test-key', TAVILY_TEST_ENDPOINT: `${origin}/search` });
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stdout, /metacharacters stayed argv data/);
  assert.ok(r.stdout.includes(`Query: ${metacharQuery}`), 'stdout should echo the exact metacharacter query as literal argv data');
});

await withServer((_req, res) => {
  res.writeHead(200, { 'content-type': 'application/json' });
  res.end(JSON.stringify({
    answer: 'success echoed dummy-secret-success-human',
    response_time: 'dummy-secret-success-human',
    results: [{ title: 'dummy-secret-success-human title', url: 'https://example.com/dummy-secret-success-human', content: 'content dummy-secret-success-human' }],
  }));
}, async (origin) => {
  const sentinel = 'dummy-secret-success-human';
  const r = await runAsync(['query'], { TAVILY_API_KEY: sentinel, TAVILY_TEST_ENDPOINT: `${origin}/search` });
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stdout, /\[redacted\]/);
  assert.match(r.stdout, /api \[redacted\]s/);
  assert.doesNotMatch(r.stdout + r.stderr, new RegExp(sentinel));
});

await withServer((_req, res) => {
  res.writeHead(200, { 'content-type': 'application/json' });
  res.end(JSON.stringify({ answer: 'JSON echoed dummy-secret-success-json', results: [{ content: 'dummy-secret-success-json' }], 'dummy-secret-success-json-key': 'value' }));
}, async (origin) => {
  const sentinel = 'dummy-secret-success-json';
  const r = await runAsync(['--json', 'query'], { TAVILY_API_KEY: sentinel, TAVILY_TEST_ENDPOINT: `${origin}/search` });
  assert.equal(r.status, 0, r.stderr);
  const parsed = JSON.parse(r.stdout);
  assert.equal(parsed.answer, 'JSON echoed [redacted]');
  assert.equal(parsed.results[0].content, '[redacted]');
  assert.equal(parsed['[redacted]-key'], 'value');
  assert.doesNotMatch(r.stdout + r.stderr, new RegExp(sentinel));
});

await withServer((_req, res) => {
  res.writeHead(429, { 'content-type': 'application/json', 'retry-after': '12' });
  res.end(JSON.stringify({ detail: 'rate limited' }));
}, async (origin) => {
  const r = await runAsync(['query'], { TAVILY_API_KEY: 'test-key', TAVILY_TEST_ENDPOINT: `${origin}/search` });
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /HTTP 429 \(retry-after: 12\): rate limited/);
});

await withServer((_req, res) => {
  const sentinel = 'dummy-secret-retry-after-header';
  res.writeHead(429, { 'content-type': 'application/json', 'retry-after': sentinel });
  res.end(JSON.stringify({ detail: 'rate limited with credential echo header' }));
}, async (origin) => {
  const sentinel = 'dummy-secret-retry-after-header';
  const r = await runAsync(['query'], { TAVILY_API_KEY: sentinel, TAVILY_TEST_ENDPOINT: `${origin}/search` });
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /HTTP 429 \(retry-after: \[redacted\]\): rate limited with credential echo header/);
  assert.doesNotMatch(r.stdout + r.stderr, new RegExp(sentinel));
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
    const sentinel = `dummy-secret-status-${status}`;
    const r = await runAsync(['query'], { TAVILY_API_KEY: sentinel, TAVILY_TEST_ENDPOINT: `${origin}/search` });
    assert.notEqual(r.status, 0);
    assert.match(r.stderr, new RegExp(`HTTP ${status}: status ${status}`));
    assert.doesNotMatch(r.stdout + r.stderr, new RegExp(sentinel));
  });
}

await withServer((_req, res) => {
  res.writeHead(500, { 'content-type': 'application/json' });
  res.end(JSON.stringify({ detail: 'upstream echoed tavily_secret_ECHO_DO_NOT_PRINT in diagnostic text' }));
}, async (origin) => {
  const sentinel = 'tavily_secret_ECHO_DO_NOT_PRINT';
  const r = await runAsync(['query'], { TAVILY_API_KEY: sentinel, TAVILY_TEST_ENDPOINT: `${origin}/search` });
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /HTTP 500: upstream echoed \[redacted\] in diagnostic text/);
  assert.doesNotMatch(r.stdout + r.stderr, new RegExp(sentinel));
});

await withServer((_req, res) => {
  res.writeHead(200, { 'content-type': 'text/plain' });
  res.end('invalid response echoed tavily_secret_JSON_DO_NOT_PRINT');
}, async (origin) => {
  const sentinel = 'tavily_secret_JSON_DO_NOT_PRINT';
  const r = await runAsync(['query'], { TAVILY_API_KEY: sentinel, TAVILY_TEST_ENDPOINT: `${origin}/search` });
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /invalid JSON response: invalid response echoed \[redacted\]/);
  assert.doesNotMatch(r.stdout + r.stderr, new RegExp(sentinel));
});

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

await withServer((_req, res) => {
  res.writeHead(200, { 'content-type': 'application/json' });
  res.flushHeaders();
  setTimeout(() => {
    res.end(JSON.stringify({ answer: 'body too late', results: [] }));
  }, 1500);
}, async (origin) => {
  const r = await runAsync(['query'], { TAVILY_API_KEY: 'test-key', TAVILY_TIMEOUT_MS: '1000', TAVILY_TEST_ENDPOINT: `${origin}/search` });
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /network timeout after 1000ms/);
});

console.log('tavily-search-native-node tests passed');
