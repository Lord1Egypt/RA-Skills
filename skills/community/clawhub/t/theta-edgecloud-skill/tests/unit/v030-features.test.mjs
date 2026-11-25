// Offline: every request is intercepted by a mocked fetch or dry-run; nothing is sent to the network.
import test from 'node:test';
import assert from 'node:assert/strict';
import { executeThetaRuntimeCommand as run, listThetaRuntimeCommands, thetaRuntimeCommandSchemas, thetaCommandRequiresConfirm, theta } from '../../dist/index.js';
import { characterRoutes, characterRequest, storylineGenerateAll } from '../../build/commands/characters.js';
import { deployments } from '../../build/commands/deployments.js';
import { inference } from '../../build/commands/inference.js';
import { thetaVideoClient } from '../../build/clients/thetaVideo.js';
import { redactObject } from '../../build/redaction.js';

const KEY = { THETA_CHARACTERS_API_KEY: 'test-game', THETA_HTTP_MAX_RETRIES: '0' };
const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });
async function capture(handler, fn) {
  const prior = globalThis.fetch; const calls = [];
  globalThis.fetch = async (url, init = {}) => { calls.push({ url: String(url), method: init.method ?? 'GET', body: init.body, init }); return handler(String(url), init); };
  try { let error; let result; try { result = await fn(); } catch (e) { error = e; } return { calls, error, result }; } finally { globalThis.fetch = prior; }
}
const noNet = () => { throw new Error('unexpected network'); };

// ---------- Story line generate_all ----------
function storyFixture(counts, extra = {}) {
  return (url) => {
    if (url.endsWith('/storyline/sl_1')) return json({ status: 'success', body: { storyline: { id: 'sl_1', npc_id: 'c', grouping_ids: counts.map((_, i) => `grp_${i}`) } } });
    const m = url.match(/\/grouping\/grp_(\d+)\/message\/list$/);
    if (m) return json({ status: 'success', body: { messages: Array.from({ length: counts[Number(m[1])] }, (_, j) => ({ id: `m${j}` })), ...(extra.total ? { pagination: { total_count: extra.total } } : {}) } });
    if (url.endsWith('/storyline/sl_1/generate_all')) return json({ status: 'success', body: { total_paths: counts.reduce((a, b) => a * b, 1), created: 1, skipped: 0 } });
    return json({}, 404);
  };
}

test('generateAll: counts paths with reads, then POSTs {} once when within maxPaths and confirmed', async () => {
  const { calls, error, result } = await capture(storyFixture([3, 2]), () => run({ command: 'theta.characters.storyline.generateAll', storylineId: 'sl_1', maxPaths: 6, confirm: true }, { env: KEY }));
  assert.equal(error, undefined);
  assert.equal(result.pathCount, 6);
  const writes = calls.filter((c) => c.method !== 'GET');
  assert.equal(writes.length, 1);
  assert.equal(writes[0].url, 'https://ai-chars-api.thetaedgecloud.com/storyline/sl_1/generate_all');
  assert.deepEqual(JSON.parse(writes[0].body), {});
  assert.equal(new Headers(writes[0].init.headers).get('authorization'), 'Bearer test-game');
});

test('generateAll: refuses above maxPaths, above 5000, empty grouping, unreadable shapes \u2014 zero writes', async () => {
  const cases = [
    [storyFixture([3, 2]), { maxPaths: 5 }, /exceeds the approved maxPaths/],
    [storyFixture([100, 100]), { maxPaths: 5000 }, /exceeds Theta's 5000-path cap/],
    [storyFixture([3, 0]), { maxPaths: 10 }, /no library messages/],
    [storyFixture([2], { total: 400 }), { maxPaths: 10 }, /exceeds the approved maxPaths/],
    [() => json({ status: 'success', body: { storyline: { id: 'sl_1' } } }), { maxPaths: 10 }, /grouping_ids/],
    [(url) => url.includes('/storyline/') ? json({ body: { grouping_ids: ['g'] } }) : json({ body: { weird: true } }), { maxPaths: 10 }, /library message list/i]
  ];
  for (const [handler, extra, pattern] of cases) {
    const { calls, error } = await capture(handler, () => run({ command: 'theta.characters.storyline.generateAll', storylineId: 'sl_1', confirm: true, ...extra }, { env: KEY }));
    assert.match(String(error?.message), pattern);
    assert.equal(calls.filter((c) => c.method !== 'GET').length, 0);
  }
});

test('generateAll: ambiguous or malformed pagination metadata refuses with zero writes (Astra A1)', async () => {
  const badPagination = (pagination) => (url) => {
    if (url.endsWith('/storyline/sl_1')) return json({ status: 'success', body: { storyline: { id: 'sl_1', grouping_ids: ['grp_0'] } } });
    if (url.match(/\/grouping\/grp_0\/message\/list$/)) return json({ status: 'success', body: { messages: [{ id: 'm0' }], pagination } });
    return json({}, 404);
  };
  const outerTotal = (url) => url.endsWith('/storyline/sl_1') ? json({ body: { storyline: { grouping_ids: ['grp_0'] } } }) : json({ body: { messages: [{ id: 'm0' }], total_count: 1000, pagination: { page: 1 } } });
  const smallTotal = (url) => url.endsWith('/storyline/sl_1') ? json({ body: { storyline: { grouping_ids: ['grp_0'] } } }) : json({ body: { messages: [{ id: 'm0' }, { id: 'm1' }], pagination: { total_count: 1 } } });
  const cases = [
    [badPagination({ total_count: '1000' }), /malformed/],
    [badPagination({ total_count: 1000.5 }), /malformed/],
    [badPagination({ total_count: 1, total: 1000 }), /conflict/],
    [badPagination({ has_more: true }), /incomplete/],
    [badPagination({ total_count: null }), /malformed/],
    [outerTotal, /exceeds the approved maxPaths/],
    [smallTotal, /smaller than the returned page/]
  ];
  for (const [handler, pattern] of cases) {
    { const { calls, error } = await capture(handler, () => run({ command: 'theta.characters.storyline.generateAll', storylineId: 'sl_1', maxPaths: 1, confirm: true }, { env: KEY }));
      assert.match(String(error?.message), pattern);
      assert.equal(calls.filter((c) => c.method !== 'GET').length, 0); }
  }
});

test('generateAll: overflow and NaN path arithmetic refuses with zero writes (Astra A2)', async () => {
  const overflow = (counts) => (url) => {
    if (url.endsWith('/storyline/sl_1')) return json({ status: 'success', body: { storyline: { id: 'sl_1', grouping_ids: counts.map((_, i) => `grp_${i}`) } } });
    const m = url.match(/\/grouping\/grp_(\d+)\/message\/list$/);
    if (m) return json({ status: 'success', body: { messages: [{ id: 'm0' }], pagination: { total_count: counts[Number(m[1])] } } });
    return json({}, 404);
  };
  for (const counts of [[1e308, 1e308, 0], [1e308, 1e308, 1e308], [1e308, 1]]) {
    const { calls, error } = await capture(overflow(counts), () => run({ command: 'theta.characters.storyline.generateAll', storylineId: 'sl_1', maxPaths: 1, confirm: true }, { env: KEY }));
    assert.ok(error, `expected refusal for ${counts}`);
    assert.match(String(error?.message), /exceeds|final safety check|no library messages|malformed/);
    assert.equal(calls.filter((c) => c.method !== 'GET').length, 0, `zero writes expected for ${counts}`);
  }
});

test('generateAll: maxPaths is required and bounded; no confirm means zero requests of any kind', async () => {
  for (const maxPaths of [undefined, 0, 5001, 2.5, '10', null]) {
    const { calls, error } = await capture(noNet, () => run({ command: 'theta.characters.storyline.generateAll', storylineId: 'sl_1', maxPaths, confirm: true }, { env: KEY }));
    assert.ok(error); assert.equal(calls.length, 0);
  }
  const { calls, error } = await capture(noNet, () => run({ command: 'theta.characters.storyline.generateAll', storylineId: 'sl_1', maxPaths: 10 }, { env: KEY }));
  assert.match(String(error?.message), /confirm:true/); assert.equal(calls.length, 0);
  const direct = await capture(noNet, () => storylineGenerateAll({ dryRun: false, charactersApiKey: 'k', httpTimeoutMs: 1000, httpMaxRetries: 0, httpRetryBackoffMs: 25 }, { storylineId: 'sl_1', maxPaths: 10 }));
  assert.match(String(direct.error?.message), /confirm:true/); assert.equal(direct.calls.length, 0);
});

test('generateAll dry-run: reads only (to count) and never POSTs; without a key it makes no request', async () => {
  const withKey = await capture(storyFixture([2, 2]), () => run({ command: 'theta.characters.storyline.generateAll', storylineId: 'sl_1', maxPaths: 4 }, { env: { ...KEY, THETA_DRY_RUN: '1' } }));
  assert.equal(withKey.result.dryRun, true); assert.equal(withKey.result.pathCount, 4);
  assert.equal(withKey.calls.filter((c) => c.method !== 'GET').length, 0);
  const noKey = await capture(noNet, () => run({ command: 'theta.characters.storyline.generateAll', storylineId: 'sl_1', maxPaths: 4 }, { env: { THETA_DRY_RUN: '1' } }));
  assert.equal(noKey.result.requiresKeyForPathCount, true); assert.equal(noKey.calls.length, 0);
});

test('generateAll and billable Characters writes are never retried on 5xx', async () => {
  const handler = (url) => url.endsWith('/generate_all') ? new Response('busy', { status: 503 }) : storyFixture([1])(url);
  const r = await capture(handler, () => run({ command: 'theta.characters.storyline.generateAll', storylineId: 'sl_1', maxPaths: 1, confirm: true }, { env: { ...KEY, THETA_HTTP_MAX_RETRIES: '6' } }));
  assert.ok(r.error); assert.equal(r.calls.filter((c) => c.method === 'POST').length, 1);
  for (const command of ['theta.characters.dialog.create', 'theta.characters.dialog.recreate', 'theta.characters.session.message']) {
    const args = { command, gameId: 'g', dialogId: 'd', sessionId: 's', confirm: true,
      payload: command.endsWith('dialog.create') ? { npc_id: 'c', message_refs: [{ grouping_id: 'g', message_id: 'm' }] } : { type: 'event', content: 'x' } };
    const w = await capture(() => new Response('busy', { status: 503 }), () => run(args, { env: { ...KEY, THETA_HTTP_MAX_RETRIES: '6' } }));
    assert.ok(w.error); assert.equal(w.calls.length, 1, command);
  }
});

// ---------- Validation: refused before any request ----------
test('Characters payload validation refuses malformed input with zero requests', async () => {
  const bad = [
    ['session.message', { sessionId: 's', payload: { type: 'shout', content: 'x' } }],
    ['session.message', { sessionId: 's', payload: { type: 'chat', content: 'x' } }],
    ['session.message', { sessionId: 's', payload: { type: 'add_participant', participant_type: 'admin', participant_id: 'x' } }],
    ['create', { gameId: 'g', payload: { name: 'x', speaking_style: { formality: 'rude' } } }],
    ['storyline.create', { gameId: 'g', payload: { name: 'x', npc_id: 'c', grouping_ids: [] } }],
    ['storyline.create', { gameId: 'g', payload: { name: 'x', grouping_ids: ['a'] } }],
    ['storyline.update', { storylineId: 's', payload: { grouping_ids: Array.from({ length: 21 }, (_, i) => `g${i}`) } }],
    ['dialog.create', { gameId: 'g', payload: { npc_id: 'c', message_refs: [{ grouping_id: 'g' }] } }],
    ['grouping.create', { gameId: 'g', payload: { name: 'x', order_index: -1 } }],
    ['session.messages', { sessionId: 's', page: 0 }],
    ['session.messages', { sessionId: 's', number: 1000 }],
    ['grouping.get', { gameId: 'g', groupingId: '..' }]
  ];
  for (const [name, args] of bad) {
    const { calls, error } = await capture(noNet, () => run({ command: `theta.characters.${name}`, confirm: true, ...args }, { env: KEY }));
    assert.ok(error, name); assert.equal(calls.length, 0, name);
  }
});

test('session.messages sends bounded page/number as an encoded query', async () => {
  const { calls } = await capture(() => json({}), () => run({ command: 'theta.characters.session.messages', sessionId: 's', page: 2, number: 50 }, { env: KEY }));
  assert.equal(calls[0].url, 'https://ai-chars-api.thetaedgecloud.com/session/s/message/list?page=2&number=50');
});

test('Characters payload is snapshotted once: getters/Proxy cannot swap validated content', async () => {
  let reads = 0;
  const payload = { get type() { reads++; return reads === 1 ? 'event' : 'shout'; }, content: 'x' };
  const { calls } = await capture(() => json({}), () => characterRequest({ dryRun: false, charactersApiKey: 'k', httpTimeoutMs: 1000, httpMaxRetries: 0, httpRetryBackoffMs: 25 }, 'session.message', { sessionId: 's', payload, confirm: true }));
  assert.equal(reads, 1);
  assert.equal(JSON.parse(calls[0].body).type, 'event');
  const proxy = new Proxy({ type: 'event', content: 'x' }, { get: (t, k) => (k === 'toJSON' ? undefined : t[k]) });
  const p = await capture(() => json({}), () => characterRequest({ dryRun: false, charactersApiKey: 'k', httpTimeoutMs: 1000, httpMaxRetries: 0, httpRetryBackoffMs: 25 }, 'session.message', { sessionId: 's', payload: proxy, confirm: true }));
  assert.equal(p.calls.length, 1);
});

test('fixed-body action routes ignore caller payloads', async () => {
  const { calls } = await capture(() => json({}), () => run({ command: 'theta.characters.dialog.recreate', dialogId: 'd', payload: { count: 999 }, confirm: true }, { env: KEY }));
  assert.deepEqual(JSON.parse(calls[0].body), {});
});

test('every non-GET Characters command and generateAll require confirm in schema and router', () => {
  for (const [name, route] of Object.entries(characterRoutes)) {
    const cmd = `theta.characters.${name}`;
    assert.equal(thetaCommandRequiresConfirm(cmd), route.method !== 'GET', cmd);
    if (route.method !== 'GET') assert.match(thetaRuntimeCommandSchemas[cmd].description, /requires confirm:true/);
  }
  assert.equal(thetaCommandRequiresConfirm('theta.characters.storyline.generateAll'), true);
  assert.equal(thetaCommandRequiresConfirm('theta.characters.estimateCost'), false);
  assert.ok(listThetaRuntimeCommands().includes('theta.video.ingestorUnselect'));
  assert.equal(thetaCommandRequiresConfirm('theta.video.ingestorUnselect'), true);
});

test('theta() facade gains no mutation helpers', () => {
  const t = theta();
  assert.equal(t.characters, undefined);
  assert.equal(t.video.ingestorUnselect, undefined);
  assert.equal(t.video.ingestorSelect, undefined);
});

// ---------- Cost estimate ----------
test('estimateCost is offline arithmetic at published prices and validates inputs', async () => {
  const { calls, result } = await capture(noNet, () => run({ command: 'theta.characters.estimateCost', inputTokens: 1e6, outputTokens: 5e5, embeddingTokens: 2e6 }, { env: {} }));
  assert.equal(calls.length, 0);
  assert.equal(result.estimateUsd, 7.5 + 10 + 0.4);
  assert.equal(result.usage.outputTokens, 5e5);
  for (const bad of [-1, NaN, Infinity, '5', 1e13]) {
    await assert.rejects(run({ command: 'theta.characters.estimateCost', inputTokens: bad }, { env: {} }));
  }
});

// ---------- A2: probe enum (Astra D1) ----------
test('D1: malformed probe values are refused before any request on every entry point', async () => {
  const cfg = { dryRun: false, edgecloudApiKey: 'k', edgecloudProjectId: 'p', edgecloudOrgId: 'o', inferenceEndpoint: 'https://x.thetaedgecloud.com', httpTimeoutMs: 1000, httpMaxRetries: 0, httpRetryBackoffMs: 25 };
  for (const probe of ['OPENAI', 'foo', {}, '', null, 1]) {
    const env = { THETA_EC_API_KEY: 'k', THETA_EC_PROJECT_ID: 'p' };
    for (const fn of [
      () => run({ command: 'theta.deployments.validateDisposable', payload: { x: 1 }, probe, confirm: true }, { env }),
      () => run({ command: 'theta.inference.ready', probe }, { env: { THETA_INFERENCE_ENDPOINT: 'https://x.thetaedgecloud.com' } }),
      () => deployments.validateDisposable(cfg, { payload: {}, probe, confirm: true }),
      () => inference.ready(cfg, { probe })
    ]) {
      const { calls, error } = await capture(noNet, fn);
      assert.match(String(error?.message), /probe must be exactly/); assert.equal(calls.length, 0);
    }
  }
});

// ---------- A3: pricing labels ----------
test('billing.pricing exposes usage labels and USD while real secrets stay redacted', async () => {
  const sse = (result) => new Response(`event: message\ndata: ${JSON.stringify({ jsonrpc: '2.0', id: 1, result: { content: [{ type: 'text', text: JSON.stringify(result) }] } })}\n\n`, { headers: { 'content-type': 'text/event-stream' } });
  const { result } = await capture(() => sse({ chatbot: [{ token: 'prompt_tokens', unit: '1M', price: '750' }, { token: 'sk-live-should-hide', unit: '1M', price: '1' }], storage: { unit: 'GB / Month', price: '15' }, on_demand_inference: [] }),
    () => run({ command: 'theta.billing.pricing' }, { env: { THETA_EC_API_KEY: 'k', THETA_EC_PROJECT_ID: 'p' } }));
  assert.deepEqual(result.chatbot[0], { usage_type: 'prompt_tokens', unit: '1M', price: '750', price_usd: 7.5 });
  assert.equal(result.chatbot[1].token, '[redacted]');
  assert.equal(result.storage.price_usd, 0.15);
  assert.equal(redactObject({ token: 'prompt_tokens' }).token, '[redacted]');
  assert.equal(redactObject({ access_token: 'x', usage: { prompt_tokens: 3 } }).access_token, '[redacted]');
});

test('billing.pricing only declassifies the exact documented usage labels (Astra A4)', async () => {
  const sse = (result) => new Response(`event: message\ndata: ${JSON.stringify({ jsonrpc: '2.0', id: 1, result: { content: [{ type: 'text', text: JSON.stringify(result) }] } })}\n\n`, { headers: { 'content-type': 'text/event-stream' } });
  const { result } = await capture(() => sse({ chatbot: [
    { token: 'private_secret_tokens', unit: '1M', price: '750' },
    { token: 'completion_tokens', unit: '1M', price: '2000' },
    { token: 'embedding_tokens', unit: '1M', price: '20' }
  ] }), () => run({ command: 'theta.billing.pricing' }, { env: { THETA_EC_API_KEY: 'k', THETA_EC_PROJECT_ID: 'p' } }));
  assert.equal(result.chatbot[0].token, '[redacted]');
  assert.equal(result.chatbot[0].usage_type, undefined);
  assert.equal(result.chatbot[1].usage_type, 'completion_tokens');
  assert.equal(result.chatbot[2].usage_type, 'embedding_tokens');
});

// ---------- Video additions ----------
const VIDEO = { THETA_VIDEO_SA_ID: 'srvacc_test', THETA_VIDEO_SA_SECRET: 'fixture-secret', THETA_HTTP_MAX_RETRIES: '0' };
test('video.search builds an encoded query and cannot inject reserved or extra parameters', async () => {
  const { calls } = await capture(() => json({ status: 'success', body: { videos: [] } }), () => run({ command: 'theta.video.search', serviceAccountId: 'srvacc/x', filters: { 'obj.key': 'a&b=c', file_name: 'x y' }, operator: 'or', page: 2, number: 20 }, { env: VIDEO }));
  assert.equal(calls[0].url, 'https://api.thetavideoapi.com/video/srvacc%2Fx/search?obj.key=a%26b%3Dc&file_name=x+y&operator=or&page=2&number=20');
  assert.equal(new Headers(calls[0].init.headers).get('x-tva-sa-secret'), 'fixture-secret');
  for (const [filters, extra] of [[{ page: '9' }, {}], [{ Operator: 'or' }, {}], [{ 'a b': 'x' }, {}], [{}, {}], [{ a: 1 }, {}], [{ a: 'x' }, { operator: 'xor' }], [{ a: 'x' }, { number: 101 }],
    [Object.fromEntries(Array.from({ length: 11 }, (_, i) => [`k${i}`, 'v'])), {}]]) {
    const r = await capture(noNet, () => run({ command: 'theta.video.search', serviceAccountId: 's', filters, ...extra }, { env: VIDEO }));
    assert.ok(r.error); assert.equal(r.calls.length, 0);
  }
});

test('video.streamList validates status and redacts stream keys', async () => {
  const { calls, result } = await capture(() => json({ status: 'success', body: { total_count: 1, streams: [{ id: 's', stream_key: 'live-secret', stream_server: 'rtmp://x', status: 'on' }] } }),
    () => run({ command: 'theta.video.streamList', serviceAccountId: 'srvacc_test', status: 'on' }, { env: VIDEO }));
  assert.equal(calls[0].url, 'https://api.thetavideoapi.com/service_account/srvacc_test/streams?status=on');
  assert.equal(result.body.streams[0].stream_key, '[redacted]');
  assert.equal(result.body.streams[0].stream_server, 'rtmp://x');
  const bad = await capture(noNet, () => run({ command: 'theta.video.streamList', serviceAccountId: 's', status: 'all' }, { env: VIDEO }));
  assert.ok(bad.error); assert.equal(bad.calls.length, 0);
});

test('video.ingestorUnselect is confirm-gated, dry-run safe, body {} and never retried', async () => {
  const noConfirm = await capture(noNet, () => run({ command: 'theta.video.ingestorUnselect', ingestorId: 'ingestor_1' }, { env: VIDEO }));
  assert.match(String(noConfirm.error?.message), /confirm:true/); assert.equal(noConfirm.calls.length, 0);
  const direct = await capture(noNet, () => thetaVideoClient.unselectIngestor({ dryRun: false, videoSaId: 'a', videoSaSecret: 'b' }, 'i'));
  assert.match(String(direct.error?.message), /confirm:true/); assert.equal(direct.calls.length, 0);
  const dry = await capture(noNet, () => run({ command: 'theta.video.ingestorUnselect', ingestorId: '0xabc', confirm: true }, { env: { ...VIDEO, THETA_DRY_RUN: '1' } }));
  assert.equal(dry.result.dryRun, true); assert.equal(dry.calls.length, 0);
  const live = await capture(() => new Response('busy', { status: 503 }), () => run({ command: 'theta.video.ingestorUnselect', ingestorId: 'ingestor/1', confirm: true }, { env: { ...VIDEO, THETA_HTTP_MAX_RETRIES: '6' } }));
  assert.equal(live.calls.length, 1);
  assert.equal(live.calls[0].url, 'https://api.thetavideoapi.com/ingestor/ingestor%2F1/unselect');
  assert.equal(live.calls[0].method, 'PUT'); assert.deepEqual(JSON.parse(live.calls[0].body), {});
});

test('0.3.1: the Theta Video client itself redacts stream keys on every stream response', async () => {
  const cfg = { dryRun: false, videoSaId: 'srvacc_test', videoSaSecret: 'fixture-secret', httpTimeoutMs: 1000, httpMaxRetries: 0, httpRetryBackoffMs: 1 };
  const stream = { id: 's', stream_key: 'live-secret', streamKey: 'live-secret-2', stream_server: 'rtmp://x', status: 'on' };
  const reply = () => json({ status: 'success', body: { stream, streams: [stream] } });
  for (const call of [
    () => thetaVideoClient.getStream(cfg, 's'),
    () => thetaVideoClient.listStreams(cfg, 'srvacc_test'),
    () => thetaVideoClient.createStream(cfg, { name: 'n' }, true)
  ]) {
    const { error, result, calls } = await capture(reply, call);
    assert.equal(error, undefined, String(error));
    assert.equal(calls.length, 1);
    const text = JSON.stringify(result);
    assert.equal(text.includes('live-secret'), false, text);
    assert.equal(result.body.stream.stream_server, 'rtmp://x');
  }
});
