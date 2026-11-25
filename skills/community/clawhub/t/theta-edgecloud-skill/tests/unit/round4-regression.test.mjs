// Regression tests for the internal round-4 pre-scan findings (F1 redaction cost on large error
// bodies, F2 library-list field allowlist and offset, F3 escaped JSON / multi-word secrets).
import test from 'node:test';
import assert from 'node:assert/strict';
import { executeThetaRuntimeCommand as run, theta } from '../../dist/index.js';
import { sanitizeHttpErrorMessage } from '../../build/errors.js';

const KEY = { THETA_CHARACTERS_API_KEY: 'test-game', THETA_HTTP_MAX_RETRIES: '0' };
const VIDEO = { THETA_VIDEO_SA_ID: 'srvacc_test', THETA_VIDEO_SA_SECRET: 'fixture-secret', THETA_HTTP_MAX_RETRIES: '0' };
const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });
async function capture(handler, fn) {
  const prior = globalThis.fetch; const calls = [];
  globalThis.fetch = async (url, init = {}) => { calls.push({ url: String(url), method: init.method ?? 'GET' }); return handler(String(url), init); };
  try { let error; let result; try { result = await fn(); } catch (e) { error = e; } return { calls, error, result }; } finally { globalThis.fetch = prior; }
}
const listResponse = (response) => (url) => {
  if (url.endsWith('/storyline/sl_1')) return json({ status: 'success', body: { storyline: { id: 'sl_1', grouping_ids: ['grp_0'] } } });
  if (/\/grouping\/grp_\d+\/message\/list$/.test(url)) return json(response);
  if (url.endsWith('/storyline/sl_1/generate_all')) return json({ status: 'success', body: { total_paths: 1, created: 1 } });
  return json({}, 404);
};
const generate = (handler) => capture(handler, () => run({ command: 'theta.characters.storyline.generateAll', storylineId: 'sl_1', maxPaths: 1, confirm: true }, { env: KEY }));

test('F1: sanitizing very large error bodies stays fast (bounded, linear)', () => {
  for (const body of ['a'.repeat(80_000), 'a'.repeat(1_000_000), 'ab '.repeat(300_000), 'x='.repeat(400_000), '"'.repeat(500_000), 'token: ' + '['.repeat(200_000)]) {
    const started = performance.now();
    const out = sanitizeHttpErrorMessage(body);
    const elapsed = performance.now() - started;
    assert.ok(elapsed < 500, `took ${elapsed.toFixed(0)} ms for ${body.slice(0, 6)}... (${body.length})`);
    assert.ok(out.length <= 280);
  }
});

test('M5-1: huge JSON error bodies are cut before parsing and stay fast and redacted', () => {
  const wide = JSON.stringify(Object.fromEntries(Array.from({ length: 400_000 }, (_, i) => [`k${i}`, i])));
  const deep = JSON.stringify({ api_key: 'SYN_JSON_KEY', pad: 'p'.repeat(9_000_000) });
  for (const body of [wide, deep]) {
    const started = performance.now();
    const out = sanitizeHttpErrorMessage(body);
    assert.ok(performance.now() - started < 500, `JSON body of ${body.length} chars too slow`);
    assert.equal(out.includes('SYN_JSON_KEY'), false, out);
  }
});

test('F1: runtime returns promptly for a 1 MB plaintext error body', async () => {
  const big = `Bad request ${'z'.repeat(1_000_000)} token=SYN_BIG`;
  const started = performance.now();
  const { error, result } = await capture(() => new Response(big, { status: 400 }), () => run({ command: 'theta.video.streamGet', streamId: 's' }, { env: VIDEO }));
  assert.ok(performance.now() - started < 2000);
  assert.equal(JSON.stringify({ e: error?.message ?? null, r: result ?? null }).includes('SYN_BIG'), false);
});

test('F2: any unrecognised list-response field, or a non-zero offset, refuses with zero writes', async () => {
  const cases = [
    { body: { messages: [{}], continuation_token: 'c' } },
    { body: { messages: [{}], is_truncated: true } },
    { body: { messages: [{}], truncated: true } },
    { body: { messages: [{}], partial: true } },
    { body: { messages: [{}], scroll_id: 's' } },
    { body: { messages: [{}], after: 'cursor' } },
    { body: { messages: [{}], hits: [{}, {}] } },
    { body: { messages: [{}], rows: [{}, {}] } },
    { body: { messages: [{}], edges: [{}, {}] } },
    { body: { messages: [{}], msgs: [{}, {}] } },
    { body: { messages: [{}], num_found: 500 } },
    { body: { messages: [{}], grouping: { messages: [{}, {}] } } },
    { body: { messages: [{}], pagination: { offset: 500 } } },
    { body: { messages: [{}], offset: 1 } },
    { body: { messages: [{}], pagination: { limit: '10' } } },
    { body: { messages: [{}], name: { total: 10 } } },
    { scroll_id: 'x', body: { messages: [{}] } },
    { success: false, body: { messages: [{}] } },
    { status: 'error', body: { messages: [{}] } },
    { success: false, messages: [{}] },
    { status: 'FAILED', messages: [{}] },
    { status: 'success', body: { success: false, messages: [{}] } },
    { body: { status: 'failure', messages: [{}] } },
    { success: false, body: [{}] },
    { success: 'false', body: { messages: [{}] } },
    { success: 0, body: { messages: [{}] } },
    { status: 'error ', body: { messages: [{}] } },
    { status: 'err', body: { messages: [{}] } },
    { status: 500, body: { messages: [{}] } },
    { status: '500', body: { messages: [{}] } },
    { error: 'quota', body: { messages: [{}] } },
    { error: true, body: { messages: [{}] } },
    { body: { messages: [{}], pagination: { per_page: 1 } } },
    { body: { messages: [{}, {}], number: 2 } }
  ];
  for (const response of cases) {
    const { calls, error } = await generate(listResponse(response));
    assert.ok(error, `expected refusal for ${JSON.stringify(response)}`);
    assert.match(String(error.message), /refusing/);
    assert.equal(calls.filter((c) => c.method !== 'GET').length, 0, `zero writes: ${JSON.stringify(response)}`);
  }
});

test('F2 control: allowlisted identity/info fields and offset 0 still send exactly one POST', async () => {
  for (const response of [
    { status: 'success', message: 'ok', request_id: 'r', body: { messages: [{}], id: 'x', grouping_id: 'grp_0', name: 'Act', title: 't', created_at: '2026-01-01', updatedAt: 1 } },
    { body: { messages: [{}], pagination: { offset: 0, limit: 100, total_count: 1, has_more: false } } },
    { body: { messages: [{}], pagination: { per_page: 1, has_more: false } } },
    { success: true, status: 200, error: null, body: { messages: [{}] } },
    { status: 'OK', error: '', body: { messages: [{}] } },
    { body: { messages: [{}], number: 1000 } }
  ]) {
    const { calls, error, result } = await generate(listResponse(response));
    assert.equal(error, undefined, JSON.stringify(response));
    assert.equal(result.pathCount, 1);
    assert.equal(calls.filter((c) => c.method !== 'GET').length, 1);
  }
});

// PEM markers are assembled at runtime so secret scanners do not flag these synthetic fixtures.
const D = '-'.repeat(5);
const F3_LEAKS = [
  ['{\\"api_key\\":\\"SYN_ESC1 more\\"}', ['SYN_ESC1', 'more\\"']],
  ['{\\"password\\":\\"p,SYN_ESC2\\"}', ['SYN_ESC2']],
  ['mnemonic: w1 w2 SYN_W3 SYN_W4', ['SYN_W3', 'SYN_W4']],
  ['seed phrase = alpha beta SYN_SEED_END', ['SYN_SEED_END']],
  ['passphrase: correct horse SYN_STAPLE', ['SYN_STAPLE']],
  [`private_key: ${D}BEGIN PRIVATE KEY${D} MIISYNBODY ${D}END PRIVATE KEY${D}`, ['MIISYNBODY']],
  [`error ${D}BEGIN RSA PRIVATE KEY${D} MIIBOGUSSYN`, ['MIIBOGUSSYN']],
  ['password=abc,SYN_AFTER_COMMA', ['SYN_AFTER_COMMA']],
  ['token=abc;SYN_AFTER_SEMI', ['SYN_AFTER_SEMI']],
  ['token\uff1aSYN_FULLWIDTH', ['SYN_FULLWIDTH']],
  ['secret phrase: w1 SYN_SP2 SYN_SP3', ['SYN_SP2', 'SYN_SP3']],
  ['recovery phrase: SYN_RP1 SYN_RP2', ['SYN_RP1', 'SYN_RP2']],
  ['seed words: SYN_SW1 SYN_SW2', ['SYN_SW1', 'SYN_SW2']],
  [`key ${D}begin private key${D} SYN_PEML ${D}end private key${D}`, ['SYN_PEML']],
  ['password=abc&SYN_AMP', ['SYN_AMP']]
];

test('F3: escaped JSON values, multi-word secrets, PEM blocks and comma/semicolon values are redacted', () => {
  for (const [input, secrets] of F3_LEAKS) {
    const out = sanitizeHttpErrorMessage(`Request failed: ${input}`);
    for (const secret of secrets) assert.equal(out.includes(secret), false, `${input} -> ${out}`);
    assert.match(out, /\[redacted\]/, input);
  }
});

test('F3: runtime and facade errors carry none of the F3 secrets', async () => {
  const restoreEnv = setEnv(VIDEO);
  try {
    for (const [input, secrets] of F3_LEAKS) {
      const handler = () => new Response(`Bad request: ${input}`, { status: 400, headers: { 'content-type': 'text/plain' } });
      for (const [label, r] of [
        ['runtime', await capture(handler, () => run({ command: 'theta.video.streamGet', streamId: 's' }, { env: VIDEO }))],
        ['facade', await capture(handler, () => theta().video.streamGet('s'))]
      ]) {
        const text = JSON.stringify({ e: r.error?.message ?? null, r: r.result ?? null, x: r.error ?? null });
        for (const secret of secrets) assert.equal(text.includes(secret), false, `${label}: ${input} -> ${text}`);
      }
    }
  } finally {
    restoreEnv();
  }
});

// Sets only the named variables and returns a function that restores exactly those names.
function setEnv(vars) {
  const saved = Object.entries(vars).map(([name]) => [name, process.env[name]]);
  for (const [name, value] of Object.entries(vars)) process.env[name] = value;
  return () => { for (const [name, value] of saved) { if (value === undefined) delete process.env[name]; else process.env[name] = value; } };
}
