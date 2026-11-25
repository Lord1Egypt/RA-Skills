// Regression tests for the internal round-2 pre-scan findings (R1 pagination, R2 plaintext redaction).
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

// One grouping whose library list returns `listBody` as its body.
const oneGrouping = (listBody, envelopeExtra = {}) => (url) => {
  if (url.endsWith('/storyline/sl_1')) return json({ status: 'success', body: { storyline: { id: 'sl_1', grouping_ids: ['grp_0'] } } });
  if (/\/grouping\/grp_0\/message\/list$/.test(url)) return json({ status: 'success', ...envelopeExtra, body: listBody });
  if (url.endsWith('/storyline/sl_1/generate_all')) return json({ status: 'success', body: { total_paths: 1, created: 1 } });
  return json({}, 404);
};
const generate = (handler) => capture(handler, () => run({ command: 'theta.characters.storyline.generateAll', storylineId: 'sl_1', maxPaths: 1, confirm: true }, { env: KEY }));

test('R1: malformed pagination containers, non-boolean completeness flags and unknown fields refuse with zero writes', async () => {
  const cases = [
    ['pagination string', { messages: [{}], pagination: '1000' }],
    ['pagination array', { messages: [{}], pagination: [{ total_count: 1000 }] }],
    ['pagination null', { messages: [{}], pagination: null }],
    ['pagination number', { messages: [{}], pagination: 7 }],
    ['has_more string', { messages: [{}], pagination: { has_more: 'true' } }],
    ['has_more number', { messages: [{}], pagination: { has_more: 1 } }],
    ['hasMore null', { messages: [{}], pagination: { hasMore: null } }],
    ['total_pages 1000', { messages: [{}], pagination: { page: 1, total_pages: 1000 } }],
    ['page 2', { messages: [{}], pagination: { page: 2 } }],
    ['next cursor', { messages: [{}], pagination: { next_cursor: 'abc' } }],
    ['unknown pagination field', { messages: [{}], pagination: { remaining: 999 } }],
    ['conflicting list aliases', { messages: [{}], library_messages: [{}, {}] }],
    ['list missing', { weird: [{}] }],
    ['list not array', { messages: { a: 1 } }],
    ['outer has_more string', { messages: [{}], has_more: 'yes' }],
    ['outer total larger', { messages: [{}], total_count: 1000 }]
  ];
  for (const [name, body] of cases) {
    const { calls, error } = await generate(oneGrouping(body));
    assert.ok(error, `${name}: expected refusal`);
    assert.match(String(error.message), /refusing|exceeds the approved maxPaths/, name);
    assert.equal(calls.filter((c) => c.method !== 'GET').length, 0, `${name}: zero writes`);
  }
  // Envelope-level metadata is checked too.
  for (const [name, extra] of [['envelope has_more', { has_more: true }], ['envelope pagination string', { pagination: 'x' }], ['envelope total', { total_count: 50 }]]) {
    const { calls, error } = await generate(oneGrouping({ messages: [{}] }, extra));
    assert.ok(error, `${name}: expected refusal`);
    assert.equal(calls.filter((c) => c.method !== 'GET').length, 0, `${name}: zero writes`);
  }
  // Non-object body and non-object response refuse.
  for (const handler of [oneGrouping('x'), oneGrouping(null), () => json('x')]) {
    const { calls, error } = await generate((url) => url.endsWith('/storyline/sl_1') ? json({ body: { storyline: { grouping_ids: ['grp_0'] } } }) : handler(url));
    assert.ok(error);
    assert.equal(calls.filter((c) => c.method !== 'GET').length, 0);
  }
});

test('R1 control: well-formed complete pages still send exactly one POST {}', async () => {
  for (const body of [
    { messages: [{}] },
    { messages: [{}], pagination: { total_count: 1, has_more: false } },
    { library_messages: [{}], pagination: { page: 1, total_pages: 1, next: null } }
  ]) {
    const { calls, error, result } = await generate(oneGrouping(body));
    assert.equal(error, undefined, JSON.stringify(body));
    assert.equal(result.pathCount, 1);
    assert.equal(calls.filter((c) => c.method === 'GET').length, 2);
    assert.equal(calls.filter((c) => c.method !== 'GET').length, 1);
  }
});

const R2_LEAKS = [
  ['stream_key = SYN_STREAM', 'SYN_STREAM'],
  ['credential=SYN_CREDENTIAL', 'SYN_CREDENTIAL'],
  ['private_key: SYN_PRIVATE', 'SYN_PRIVATE'],
  ['mnemonic: SYN_MNEMONIC', 'SYN_MNEMONIC'],
  ['authorization=SYN_AUTH', 'SYN_AUTH'],
  ['access_tokens: ["SYN_ONE", "SYN_TWO"]', 'SYN_TWO'],
  ['access_tokens: ["SYN_ONE", "SYN_TWO"]', 'SYN_ONE'],
  ['stream_key: "SYN STREAM"', 'STREAM"'],
  ["client_secret='SYN QUOTED'", 'QUOTED'],
  ['"api_key": "SYN_JSONISH"', 'SYN_JSONISH'],
  ['refresh_token = {"a":"SYN_OBJ1","b":"SYN_OBJ2"}', 'SYN_OBJ2'],
  ['seed_phrase: "w1 w2 SYN_SEED"', 'SYN_SEED'],
  ['Authorization: Bearer SYN_BEARER', 'SYN_BEARER'],
  ['password = "unterminated SYN_TAIL', 'SYN_TAIL']
];

test('R2: labelled plaintext credentials are fully redacted (spaced, quoted, list, object, unterminated)', () => {
  for (const [input, secret] of R2_LEAKS) {
    const out = sanitizeHttpErrorMessage(`Bad request: ${input} (see docs)`);
    assert.equal(out.includes(secret), false, `${input} -> ${out}`);
    assert.match(out, /\[redacted\]/, input);
  }
  // Non-credential text is preserved.
  assert.equal(sanitizeHttpErrorMessage('status=invalid name: demo'), 'status=invalid name: demo');
});

test('R2: runtime and facade HTTP errors carry no labelled credential values', async () => {
  const restoreEnv = setEnv(VIDEO);
  try {
    for (const [input, secret] of R2_LEAKS) {
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
