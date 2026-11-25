// Regression tests for the internal round-3 pre-scan findings (O1 paging outside `pagination`,
// O2 prefixed/suffixed plaintext credential labels, O3 conflicting grouping_ids).
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
const many = (n) => Array.from({ length: n }, (_, i) => ({ id: `m${i}` }));
const listResponse = (response, storyline = { status: 'success', body: { storyline: { id: 'sl_1', grouping_ids: ['grp_0'] } } }) => (url) => {
  if (url.endsWith('/storyline/sl_1')) return json(storyline);
  if (/\/grouping\/grp_\d+\/message\/list$/.test(url)) return json(response);
  if (url.endsWith('/storyline/sl_1/generate_all')) return json({ status: 'success', body: { total_paths: 1, created: 1 } });
  return json({}, 404);
};
const generate = (handler) => capture(handler, () => run({ command: 'theta.characters.storyline.generateAll', storylineId: 'sl_1', maxPaths: 1, confirm: true }, { env: KEY }));

test('O1: paging or list metadata outside `pagination` refuses with zero writes', async () => {
  const cases = [
    { body: { messages: [{}], meta: { total: 1000 } } },
    { body: { messages: [{}], total_items: 1000 } },
    { body: { messages: [{}], total_messages: 1000 } },
    { body: { messages: [{}], last_page: 1000 } },
    { body: { messages: [{}], next_page_url: 'https://x/2' } },
    { body: { messages: [{}], links: { next: '/2' } } },
    { body: { messages: [{}], page_info: { has_next_page: true } } },
    { body: { messages: [{}], paging: { total: 1000 } } },
    { body: { messages: [{}], is_last: false } },
    { body: { messages: [{}], HasMore: true } },
    { body: { body: { messages: many(1000) }, messages: [{}] } },
    { data: { messages: many(1000) }, body: { messages: [{}] } },
    { body: { data: many(1000), messages: [{}] } },
    { body: { messages: [{}], results: many(5) } },
    { body: { messages: [{}], message: { total: 9 } } },
    { meta: { total: 1000 }, body: { messages: [{}] } }
  ];
  for (const response of cases) {
    const { calls, error } = await generate(listResponse(response));
    assert.ok(error, `expected refusal for ${JSON.stringify(response).slice(0, 80)}`);
    assert.match(String(error.message), /refusing/);
    assert.equal(calls.filter((c) => c.method !== 'GET').length, 0, `zero writes: ${JSON.stringify(response).slice(0, 80)}`);
  }
});

test('O1 control: informational fields and recognised pagination still allow exactly one POST', async () => {
  for (const response of [
    { status: 'success', message: 'ok', body: { messages: [{}] } },
    { status: 'success', code: 0, request_id: 'r1', body: { messages: [{}], pagination: { total_count: 1, has_more: false } } },
    { status: 'success', body: { library_messages: [{}], grouping_id: 'grp_0', name: 'Act 1' } }
  ]) {
    const { calls, error, result } = await generate(listResponse(response));
    assert.equal(error, undefined, JSON.stringify(response));
    assert.equal(result.pathCount, 1);
    assert.equal(calls.filter((c) => c.method !== 'GET').length, 1);
  }
});

test('O3: conflicting grouping_ids copies refuse with zero writes', async () => {
  const story = { status: 'success', body: { storyline: { id: 'sl_1', grouping_ids: ['grp_0'] }, grouping_ids: ['grp_0', 'grp_1', 'grp_2'] } };
  const { calls, error } = await generate(listResponse({ body: { messages: [{}] } }, story));
  assert.match(String(error?.message), /conflicting grouping_ids/);
  assert.equal(calls.filter((c) => c.method !== 'GET').length, 0);
  // Agreeing copies are fine.
  const agree = { status: 'success', body: { storyline: { id: 'sl_1', grouping_ids: ['grp_0'] }, grouping_ids: ['grp_0'] } };
  const ok = await generate(listResponse({ body: { messages: [{}] } }, agree));
  assert.equal(ok.error, undefined);
  assert.equal(ok.calls.filter((c) => c.method !== 'GET').length, 1);
});

const O2_LEAKS = [
  ['sa_secret=SYN_B', 'SYN_B'],
  ['api_secret=SYN_C', 'SYN_C'],
  ['game_api_key=SYN_D', 'SYN_D'],
  ['user_password=SYN_E', 'SYN_E'],
  ['my_token=SYN_F', 'SYN_F'],
  ['service_account_secret: SYN_G', 'SYN_G'],
  ['secret_key=SYN_A', 'SYN_A'],
  ['token_value=SYN_N', 'SYN_N'],
  ['password_hash=SYN_O', 'SYN_O'],
  ['token := SYN_AD', 'SYN_AD'],
  ['token => SYN_AE', 'SYN_AE'],
  ['token=\u201cSYN Y\u201d', 'Y\u201d'],
  ['token=`SYN Z`', 'Z`'],
  ['stream key: SYN_Q', 'SYN_Q'],
  ['X-Tva-Sa-Secret: SYN_H', 'SYN_H'],
  ['cookie: sid=SYN_COOKIE', 'SYN_COOKIE'],
  ['error token=SYN_TWO_WORD', 'SYN_TWO_WORD'],
  ['access_key=SYN_ACCESS', 'SYN_ACCESS'],
  ['jwt=SYN_JWT', 'SYN_JWT']
];

test('O2: prefixed/suffixed credential labels and :=, =>, typographic quotes are redacted', () => {
  for (const [input, secret] of O2_LEAKS) {
    const out = sanitizeHttpErrorMessage(`Request rejected: ${input}; retry later`);
    assert.equal(out.includes(secret), false, `${input} -> ${out}`);
    assert.match(out, /\[redacted\]/, input);
  }
  // Scheme word is kept, numeric usage counts and ordinary labels are untouched.
  assert.equal(sanitizeHttpErrorMessage('Authorization: Bearer SYN_X'), 'Authorization: Bearer [redacted]');
  assert.equal(sanitizeHttpErrorMessage('prompt_tokens: 12, status=bad'), 'prompt_tokens: 12, status=bad');
  assert.equal(sanitizeHttpErrorMessage('see https://docs.example/x for name: demo'), 'see https://docs.example/x for name: demo');
});

test('O2: runtime and facade errors carry no prefixed credential values', async () => {
  const restoreEnv = setEnv(VIDEO);
  try {
    for (const [input, secret] of O2_LEAKS) {
      const handler = () => new Response(`Bad request: ${input}`, { status: 400, headers: { 'content-type': 'text/plain' } });
      const viaRuntime = await capture(handler, () => run({ command: 'theta.video.streamGet', streamId: 'stream_1' }, { env: VIDEO }));
      const viaFacade = await capture(handler, () => theta().video.streamGet('stream_1'));
      for (const [label, r] of [['runtime', viaRuntime], ['facade', viaFacade]]) {
        const text = JSON.stringify({ e: r.error?.message ?? null, r: r.result ?? null, x: r.error ?? null });
        assert.equal(text.includes(secret), false, `${label}: ${input} -> ${text}`);
        assert.equal(r.calls.length, 1, `${label}: one GET`);
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
