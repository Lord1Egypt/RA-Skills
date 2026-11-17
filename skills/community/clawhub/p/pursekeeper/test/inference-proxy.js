'use strict';
// Offline tests for scripts/inference-proxy.js: a mock door that answers 402 in both Nano dialects, a mock node RPC
// that checks every block's signature and frontier, and the proxy as a child process with a throwaway seed.
// Nothing here reaches the network: UPSTREAM, NANO_RPC and WORK_URL all point at loopback servers in this file.

const test = require('node:test');
const assert = require('node:assert/strict');
const { createServer, request: httpRequest } = require('node:http');
const { spawn } = require('node:child_process');
const { randomBytes } = require('node:crypto');
const { mkdtemp, rm, readFile, writeFile } = require('node:fs/promises');
const { tmpdir } = require('node:os');
const { join, resolve } = require('node:path');
const N = require('nanocurrency');

const SCRIPT = resolve(__dirname, '../scripts/inference-proxy.js');
const RAW = 10n ** 30n;
const WORK = '0'.repeat(16);   // not real proof of work; the mock node does not check it
const listen = (srv) => new Promise(r => srv.listen(0, '127.0.0.1', () => r(`http://127.0.0.1:${srv.address().port}`)));
const readBody = req => new Promise((res, rej) => { let t = ''; req.on('data', c => { t += c; }); req.on('end', () => res(t)); req.on('error', rej); });

// ---- mock node: one account, balance and frontier tracked, blocks verified ----
function mockNode(account, publicKey, initial) {
  const st = { frontier: 'A'.repeat(64), height: 1, balance: initial, processed: [], receivable: {}, rejectNext: 0, lostReplyNext: 0, accountError: null, workCalls: 0 };
  const srv = createServer(async (req, res) => {
    const b = JSON.parse(await readBody(req) || '{}');
    const out = o => { res.writeHead(200, { 'content-type': 'application/json' }); res.end(JSON.stringify(o)); };
    if (b.action === 'account_info') return st.accountError ? out({ error: st.accountError }) : out({ frontier: st.frontier, balance: st.balance.toString(), representative: account, block_count: String(st.height), confirmation_height: String(st.height), confirmed_frontier: st.frontier });   // every accepted block counts as confirmed at once
    if (b.action === 'work_generate') { st.workCalls++; return out({ work: WORK }); }
    if (b.action === 'receivable') return out({ blocks: st.receivable });
    if (b.action === 'block_info') return st.processed.some(p => p.hash === b.hash) ? out({ contents: {} }) : out({ error: 'Block not found' });
    if (b.action === 'process') {
      const blk = b.block;
      const hash = N.hashBlock(blk);
      if (st.rejectNext > 0) { st.rejectNext--; return out({ error: 'Gap previous block' }); }
      if (blk.previous !== st.frontier) return out({ error: 'Fork' });
      if (blk.account !== account) return out({ error: 'Bad account' });
      if (!N.verifyBlock({ hash, signature: blk.signature, publicKey })) return out({ error: 'Bad signature' });
      const bal = BigInt(blk.balance);
      if (b.subtype === 'send') {
        if (bal > st.balance) return out({ error: 'Negative spend' });
        st.processed.push({ hash, subtype: 'send', amount: st.balance - bal, link: blk.link });
      } else if (b.subtype === 'change') {
        if (bal !== st.balance || blk.link !== '0'.repeat(64)) return out({ error: 'Not a change block' });
        st.processed.push({ hash, subtype: 'change', amount: 0n, link: blk.link });
      } else {
        const src = st.receivable[blk.link];
        if (!src || BigInt(src.amount) !== bal - st.balance) return out({ error: 'Unreceivable' });
        delete st.receivable[blk.link];
        st.processed.push({ hash, subtype: b.subtype, amount: bal - st.balance });
      }
      st.balance = bal; st.frontier = hash; st.height++;
      if (st.lostReplyNext > 0) { st.lostReplyNext--; return out({ error: 'timeout after accept' }); }
      return out({ hash });
    }
    out({ error: 'unknown action ' + b.action });
  });
  return { srv, st };
}

// ---- mock door: NanoGPT-shaped ("nano") or x402 v2 ("exact") 402s, then serves the paid call ----
function mockDoor(node, opts) {
  const st = { quotes: {}, completes: [], served: 0, lastHeaders: null, mode: opts.mode, amount: opts.amount, sse: !!opts.sse, host: null };
  const srv = createServer(async (req, res) => {
    const body = await readBody(req);
    st.lastHeaders = req.headers;
    const out = (code, h, s) => { res.writeHead(code, { 'content-type': 'application/json', ...h }); res.end(s); };
    const serve = () => {
      st.served++;
      let stream = false; try { stream = !!JSON.parse(body).stream; } catch { /* ignore */ }
      if (stream && st.sse) {
        res.writeHead(200, { 'content-type': 'text/event-stream' });
        res.write('data: {"id":"c1","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"OK"}}]}\n\n');
        return res.end('data: [DONE]\n\n');
      }
      out(200, { 'x-x402-reconciliation-amount': '0.000001' }, JSON.stringify(opts.completion || { id: 'c1', object: 'chat.completion', created: 1, model: 'm', choices: [{ index: 0, message: { role: 'assistant', content: 'OK' }, finish_reason: 'stop' }], usage: { total_tokens: 2 } }));
    };
    if (req.url.startsWith('/status/')) {
      if (opts.statusRedirect) return out(302, { location: opts.statusRedirect }, '');   // a door that sends the poll elsewhere
      const q = st.quotes[req.url.slice('/status/'.length)];
      const paid = q && node.st.processed.some(p => p.subtype === 'send' && p.link === N.derivePublicKey(q.payTo).toUpperCase() && p.amount === BigInt(q.amount));
      return out(200, {}, JSON.stringify(paid ? { status: 'paid', readyToComplete: true } : { status: 'pending', readyToComplete: false }));
    }
    if (req.url.startsWith('/complete/')) {
      const id = req.url.slice('/complete/'.length);
      const q = st.quotes[id];
      st.completes.push({ id, headers: req.headers, body });
      if (!q) return out(404, {}, '{"error":"unknown payment"}');
      const paid = node.st.processed.find(p => p.subtype === 'send' && p.link === N.derivePublicKey(q.payTo).toUpperCase() && p.amount === BigInt(q.amount));
      if (!paid) return out(402, {}, '{"error":"not paid"}');
      if (req.headers['x-x402-payment-id'] !== id || body !== q.body) return out(400, {}, '{"error":"body or id mismatch"}');
      if (opts.completeRedirect) return out(307, { location: opts.completeRedirect }, '');   // paid, then sent elsewhere
      return serve();
    }
    if (!req.url.startsWith('/v1/')) return out(404, {}, '{}');
    if (opts.free && req.url === opts.free) return serve(); // a path the door serves without a 402
    const host = req.headers.host;
    const payTo = opts.payTo || N.deriveAddress(N.derivePublicKey(randomBytes(32).toString('hex')), { useNanoPrefix: true });
    if (st.mode === 'exact') {
      const sig = req.headers['payment-signature'];
      const accepts = [{ scheme: 'exact', network: opts.network || 'nano:mainnet', amount: String(st.amount), payTo, resource: opts.resource || `http://${host}${req.url}` }];
      if (!sig) return out(402, { 'payment-required': Buffer.from(JSON.stringify({ x402Version: 2, resource: opts.resourceTop || `http://${host}${req.url}`, accepts })).toString('base64') }, '{"error":"payment required"}');
      const p = JSON.parse(Buffer.from(sig, 'base64').toString());
      const blk = p.payload.block;
      if (opts.keepUnbroadcast) { st.held = blk; return out(500, {}, '{"error":"served nothing, broadcast nothing"}'); }   // a seller that pockets the signed block and refuses
      // the seller broadcasts
      const r = await fetch(node.url, { method: 'POST', body: JSON.stringify({ action: 'process', subtype: 'send', block: blk }) }).then(x => x.json());
      if (!r.hash) return out(402, {}, JSON.stringify({ error: 'rejected: ' + r.error }));
      if (opts.refuseAfterBroadcast) return out(500, {}, '{"error":"served nothing"}');
      return serve();
    }
    // nano dialect
    const id = opts.fixedId || ('pay_' + randomBytes(6).toString('hex'));
    const base = opts.completeHost ? `http://${opts.completeHost}` : `${opts.completeProtocol || 'http:'}//${host}`;
    const a = { scheme: 'nano', protocolScheme: 'nano', network: opts.network || 'nano-mainnet', amount: String(st.amount), payTo, paymentId: id,
      expiresAt: opts.expired ? new Date(Date.now() - 1000).toISOString() : new Date(Date.now() + 900000).toISOString(), statusUrl: `${base}/status/${id}`, completeUrl: `${base}/complete/${id}` };
    if (opts.malformed === 'amount') a.amount = 'abc';
    if (opts.malformed === 'zero') a.amount = '0';
    if (opts.noExpiry) delete a.expiresAt;
    st.quotes[id] = { payTo, amount: a.amount, body };
    out(402, { 'x-payment-schemes': 'nano,nano-exact' }, JSON.stringify({ error: { message: 'Insufficient balance', code: 'insufficient_quota' }, payment: { version: 1, paymentId: id, accepted: [a, { scheme: 'nano-exact', network: 'nano:mainnet', amount: a.amount, payTo }] } }));
  });
  return { srv, st };
}

async function startProxy(env, dir) {
  const proc = spawn(process.execPath, [SCRIPT], { env: { PATH: process.env.PATH, HOME: dir, ...env }, stdio: ['ignore', 'pipe', 'pipe'] });
  let err = '';
  proc.stderr.on('data', c => { err += c; });
  const port = await new Promise((res, rej) => {
    const t = setTimeout(() => rej(new Error('proxy did not start: ' + err)), 8000);
    proc.stderr.on('data', () => { const m = /127\.0\.0\.1:(\d+)\/v1/.exec(err); if (m) { clearTimeout(t); res(Number(m[1])); } });
    proc.on('exit', code => { clearTimeout(t); rej(new Error('proxy exited ' + code + ': ' + err)); });
  });
  const stop = () => new Promise(r => { if (proc.exitCode !== null || proc.signalCode !== null) return r(); proc.once('exit', r); proc.kill(); });
  return { proc, port, log: () => err, stop };
}

async function stand(t, doorOpts, envExtra) {
  const seed = randomBytes(32).toString('hex');
  const pub = N.derivePublicKey(N.deriveSecretKey(seed, 0));
  const account = N.deriveAddress(pub, { useNanoPrefix: true });
  const node = mockNode(account, pub, 10n * RAW);
  node.url = await listen(node.srv);
  const door = mockDoor(node, doorOpts);
  const doorUrl = await listen(door.srv);
  const dir = await mkdtemp(join(tmpdir(), 'pk-proxy-'));
  const env = { NANO_SEED: seed, UPSTREAM: doorUrl, NANO_RPC: node.url, WORK_URL: node.url, NANO_CAP: '0.01', NANO_MAX_PER_CALL: '0.005', PORT: '0', STATE_FILE: join(dir, 'state.json'), PROXY_KEY: KEY, ...envExtra };
  const proxy = await startProxy(env, dir);
  const shut = srv => { srv.close(); srv.closeAllConnections(); };
  t.after(async () => { await proxy.stop(); shut(node.srv); shut(door.srv); await rm(dir, { recursive: true, force: true }); });
  const call = (body, headers, path) => fetch(`http://127.0.0.1:${proxy.port}${path || '/v1/chat/completions'}`, { method: 'POST', headers: { 'content-type': 'application/json', authorization: 'Bearer ' + KEY, ...headers }, body: JSON.stringify(body) });
  const stateOf = () => fetch(`http://127.0.0.1:${proxy.port}/_nano/state`, { headers: { authorization: 'Bearer ' + KEY } }).then(r => r.json());
  return { seed, account, pub, node, door, proxy, env, dir, call, stateOf, restart: async () => { await proxy.stop(); const p2 = await startProxy(env, dir); t.after(() => p2.stop()); return p2; } };
}

const KEY = 'test-proxy-key-0123456789abcdef';   // PROXY_KEY for every proxy started here; the runtime presents it
const MSG = { model: 'm', messages: [{ role: 'user', content: 'hi' }] };
const MILLI = RAW / 1000n;   // 0.001 XNO

test('nano dialect: pays exactly the quote, completes with the same body, counts the spend', async t => {
  const s = await stand(t, { mode: 'nano', amount: MILLI });
  const r = await s.call(MSG);
  const text = await r.text();
  assert.equal(r.status, 200, text);
  const j = JSON.parse(text);
  assert.equal(j.choices[0].message.content, 'OK');
  assert.equal(r.headers.get('x-payer-paid'), '0.001');
  assert.equal(s.node.st.processed.length, 1);
  assert.equal(s.node.st.processed[0].amount, MILLI);
  assert.equal(s.door.st.completes.length, 1);
  assert.equal(s.door.st.completes[0].body, JSON.stringify(MSG));
  assert.equal(s.door.st.completes[0].headers['x-x402'], 'nano');
  assert.equal(s.door.st.lastHeaders.authorization, undefined, 'the runtime key never reaches the door');
  const st = await s.stateOf();
  assert.equal(st.spent, '0.001'); assert.equal(st.paid, 1); assert.equal(st.payments[0].status, 'served');
  assert.equal(st.payments[0].reconciliation, '0.000001');
  const file = JSON.parse(await readFile(s.env.STATE_FILE, 'utf8'));
  assert.equal(file.spent_raw, MILLI.toString());
});

test('cap: a quote that would pass the cumulative cap is refused before anything is signed', async t => {
  const s = await stand(t, { mode: 'nano', amount: 6n * MILLI }, { NANO_CAP: '0.01', NANO_MAX_PER_CALL: '0.01' });
  assert.equal((await s.call(MSG)).status, 200);
  const r = await s.call(MSG);
  assert.equal(r.status, 402);
  const j = await r.json();
  assert.equal(j.payer.code, 'cap_exceeded');
  assert.equal(s.node.st.processed.length, 1, 'no second block');
  assert.equal(s.node.st.workCalls, 1, 'no work requested for the refused call');
  assert.equal((await s.stateOf()).spent, '0.006');
});

test('per-call limit, payTo allow-list, expired quote, malformed amounts: refused, nothing signed', async t => {
  for (const [opts, env, code] of [
    [{ mode: 'nano', amount: 6n * MILLI }, { NANO_MAX_PER_CALL: '0.005' }, 'over_per_call_limit'],
    [{ mode: 'nano', amount: MILLI }, { NANO_ALLOW_PAYTO: 'nano_3arg3asgtigae3xckabaaewkx3bzsh7nwz7jkmjos79ihyaxwphhm6qgjps4' }, 'payto_not_allowed'],
    [{ mode: 'nano', amount: MILLI, expired: true }, {}, 'quote_expired'],
    [{ mode: 'nano', amount: MILLI, malformed: 'amount' }, {}, 'malformed_quote'],
    [{ mode: 'nano', amount: MILLI, malformed: 'zero' }, {}, 'malformed_quote'],
  ]) {
    const s = await stand(t, opts, env);
    const r = await s.call(MSG);
    assert.equal(r.status, 402, code);
    assert.equal((await r.json()).payer.code, code);
    assert.equal(s.node.st.processed.length, 0, code + ': nothing broadcast');
    assert.equal(s.node.st.workCalls, 0, code + ': no work requested');
    assert.equal((await s.stateOf()).spent, '0');
  }
});

test('host binding: a completeUrl on another host is refused even when the amount is fine', async t => {
  const s = await stand(t, { mode: 'nano', amount: MILLI, completeHost: '127.0.0.1:1' });
  const r = await s.call(MSG);
  assert.equal(r.status, 402);
  assert.equal((await r.json()).payer.code, 'host_mismatch');
  assert.equal(s.node.st.processed.length, 0);
});

test('protocol binding: a completeUrl on the door\'s host but another protocol is refused before anything is signed', async t => {
  const s = await stand(t, { mode: 'nano', amount: MILLI, completeProtocol: 'https:' });
  const r = await s.call(MSG);
  assert.equal(r.status, 402);
  const j = await r.json();
  assert.equal(j.payer.code, 'protocol_mismatch');
  assert.equal(j.payer.detail.protocol, 'https:');
  assert.equal(s.node.st.processed.length, 0);
  assert.equal((await s.stateOf()).spent, '0');
});

test('restart: the spend survives in the state file and the cap still holds', async t => {
  const s = await stand(t, { mode: 'nano', amount: 4n * MILLI }, { NANO_CAP: '0.01', NANO_MAX_PER_CALL: '0.005' });
  assert.equal((await s.call(MSG)).status, 200);
  assert.equal((await s.call(MSG)).status, 200);
  const p2 = await s.restart();
  const call2 = () => fetch(`http://127.0.0.1:${p2.port}/v1/chat/completions`, { method: 'POST', headers: { 'content-type': 'application/json', authorization: 'Bearer ' + KEY }, body: JSON.stringify(MSG) });
  const r = await call2();
  assert.equal(r.status, 402);
  assert.equal((await r.json()).payer.code, 'cap_exceeded');
  const st = await fetch(`http://127.0.0.1:${p2.port}/_nano/state`, { headers: { authorization: 'Bearer ' + KEY } }).then(x => x.json());
  assert.equal(st.spent, '0.008'); assert.equal(st.paid, 2);
  assert.equal(s.node.st.processed.length, 2);
});

test('concurrency: parallel requests never pass the cap and never fork the account', async t => {
  const s = await stand(t, { mode: 'nano', amount: 3n * MILLI }, { NANO_CAP: '0.007', NANO_MAX_PER_CALL: '0.005' });
  const rs = await Promise.all(Array.from({ length: 6 }, () => s.call(MSG)));
  const codes = rs.map(r => r.status).sort();
  assert.deepEqual(codes, [200, 200, 402, 402, 402, 402]);
  assert.equal(s.node.st.processed.length, 2);
  assert.equal((await s.stateOf()).spent, '0.006');
  for (const r of rs) if (r.status === 402) assert.equal((await r.json()).payer.code, 'cap_exceeded');
});

test('stream:true: SSE from the door is passed through; a JSON answer is wrapped as one chunk', async t => {
  const s1 = await stand(t, { mode: 'nano', amount: MILLI, sse: true });
  const r1 = await s1.call({ ...MSG, stream: true });
  assert.equal(r1.status, 200);
  assert.equal(r1.headers.get('x-payer-stream'), 'passthrough');
  assert.match(r1.headers.get('content-type'), /text\/event-stream/);
  assert.match(await r1.text(), /"content":"OK"[\s\S]*\[DONE\]/);
  const s2 = await stand(t, { mode: 'nano', amount: MILLI, sse: false });
  const r2 = await s2.call({ ...MSG, stream: true });
  assert.equal(r2.status, 200);
  assert.equal(r2.headers.get('x-payer-stream'), 'buffered');
  const text = await r2.text();
  assert.match(text, /chat\.completion\.chunk/);
  assert.match(text, /"delta":\{"role":"assistant","content":"OK"\}/);
  assert.match(text, /data: \[DONE\]\n\n$/);
});

test('stream:true buffered wrap keeps tool_calls (with index), refusal and any other message field (pyfile-toolkit, api#89 slot 2)', async t => {
  const tool_calls = [{ id: 'call_1', type: 'function', function: { name: 'get_balance', arguments: '{"asset":"XNO"}' } }];
  const completion = { id: 'c2', object: 'chat.completion', created: 1, model: 'm', usage: { prompt_tokens: 2, completion_tokens: 3, total_tokens: 5 },
    choices: [{ index: 0, message: { role: 'assistant', content: null, tool_calls, refusal: null }, finish_reason: 'tool_calls' }] };
  const s = await stand(t, { mode: 'nano', amount: MILLI, sse: false, completion });
  const r = await s.call({ ...MSG, stream: true });
  assert.equal(r.status, 200);
  assert.equal(r.headers.get('x-payer-stream'), 'buffered');
  const text = await r.text();
  const frames = text.split('\n\n').filter(Boolean);
  assert.equal(frames.length, 2);
  assert.equal(frames[1], 'data: [DONE]');
  const first = JSON.parse(frames[0].replace(/^data: /, ''));
  assert.equal(first.object, 'chat.completion.chunk');
  assert.equal(first.choices[0].finish_reason, 'tool_calls');
  const d = first.choices[0].delta;
  assert.equal(d.role, 'assistant');
  assert.equal(d.content, '');
  assert.deepEqual(d.tool_calls, [{ index: 0, ...tool_calls[0] }]);
  assert.equal(d.refusal, null);
  assert.equal(s.node.st.processed.length, 1);
});

test('runtime credentials in any common header are dropped before the door sees them, on the paid path and the plain relay (pyfile-toolkit, api#89 slot 3)', async t => {
  const s = await stand(t, { mode: 'nano', amount: MILLI, free: '/v1/models' });
  const creds = { 'x-api-key': 'SYNTHETIC-X-API-KEY', 'api-key': 'SYNTHETIC-API-KEY', 'x-auth-token': 'SYNTHETIC-AUTH-TOKEN', 'x-goog-api-key': 'SYNTHETIC-GOOG', cookie: 'session=SYNTHETIC', 'proxy-authorization': 'Basic SYNTHETIC' };
  const dropped = ['authorization', ...Object.keys(creds)];
  // paid path: the quote request and the completion both go through doorHeaders
  const r = await s.call(MSG, { ...creds, 'x-runtime-note': 'kept' });
  assert.equal(r.status, 200, await r.text());
  assert.equal(s.door.st.completes.length, 1);
  for (const h of [s.door.st.lastHeaders, s.door.st.completes[0].headers]) {
    for (const k of dropped) assert.equal(h[k], undefined, `${k} never reaches the door`);
    assert.equal(h['x-runtime-note'], 'kept', 'a non-credential header is forwarded as is');
  }
  // plain relay: a door that answers 200 straight away (the pyfile-toolkit harness shape) sees no credential either
  const r2 = await s.call(MSG, creds, '/v1/models');
  assert.equal(r2.status, 200, await r2.text());
  assert.equal(s.door.st.completes.length, 1, 'a plain relay is not a paid completion');
  assert.equal(s.door.st.served, 2);
  for (const k of dropped) assert.equal(s.door.st.lastHeaders[k], undefined, `${k} never reaches the door on the plain relay`);
  assert.equal(s.node.st.processed.length, 1);
});

test('exact dialect: signed block in PAYMENT-SIGNATURE, seller broadcasts, spend counted', async t => {
  const s = await stand(t, { mode: 'exact', amount: MILLI });
  const r = await s.call(MSG);
  const text = await r.text();
  assert.equal(r.status, 200, text);
  assert.equal(r.headers.get('x-payer-paid'), '0.001');
  assert.equal(s.node.st.processed.length, 1);
  assert.equal(s.node.st.processed[0].amount, MILLI);
  const st = await s.stateOf();
  assert.equal(st.spent, '0.001'); assert.equal(st.payments[0].kind, 'exact'); assert.equal(st.payments[0].status, 'served');
  assert.equal(s.door.st.lastHeaders.authorization, undefined);
});

test('exact dialect: a call the seller broadcast but did not serve is reported, and stays counted', async t => {
  const s = await stand(t, { mode: 'exact', amount: MILLI, refuseAfterBroadcast: true });
  const r = await s.call(MSG);
  assert.equal(r.status, 502);
  const j = await r.json();
  assert.equal(j.payer.code, 'not_served_after_payment');
  assert.equal(j.payer.detail.broadcast, true);
  const st = await s.stateOf();
  assert.equal(st.spent, '0.001'); assert.equal(st.payments[0].status, 'broadcast_not_served');
});

test('nano dialect: a broadcast the node rejects is retired by a change block at the same height, then uncounted; the runtime told', async t => {
  const s = await stand(t, { mode: 'nano', amount: MILLI });
  s.node.st.rejectNext = 1;
  const r = await s.call(MSG);
  assert.equal(r.status, 402);
  const j = await r.json();
  assert.equal(j.payer.code, 'broadcast_failed');
  assert.equal(j.payer.detail.counted, false);
  assert.match(j.payer.detail.invalidated_by, /^[0-9A-F]{64}$/);
  const st = await s.stateOf();
  assert.equal(st.spent, '0'); assert.equal(st.payments[0].status, 'not_broadcast');
  assert.equal(st.payments[0].counted, false); assert.equal(st.payments[0].final, true);
  assert.equal(s.node.st.processed.map(p => p.subtype).join(','), 'change', 'the change block sits where the rejected send would have');
  assert.equal(s.node.st.processed[0].hash, j.payer.detail.invalidated_by);
  assert.equal(s.node.st.workCalls, 1, 'the work computed for the send is reused for the change block');
  assert.equal((await s.call(MSG)).status, 200, 'the next call pays normally');
  assert.equal((await s.stateOf()).spent, '0.001');
  assert.equal(s.node.st.processed.map(p => p.subtype).join(','), 'change,send');
});

test('exact dialect: a seller that keeps the signed block and refuses cannot broadcast it later: a change block takes its height, the spend is uncounted, no payload is kept', async t => {
  const s = await stand(t, { mode: 'exact', amount: MILLI, keepUnbroadcast: true });
  const r = await s.call(MSG);
  assert.equal(r.status, 502);
  const j = await r.json();
  assert.equal(j.payer.code, 'not_served_after_payment');
  assert.equal(j.payer.detail.broadcast, false);
  assert.equal(j.payer.detail.counted, false);
  assert.match(j.payer.detail.invalidated_by, /^[0-9A-F]{64}$/);
  const st = await s.stateOf();
  assert.equal(st.spent, '0');
  assert.equal(st.payments[0].status, 'not_broadcast_refused'); assert.equal(st.payments[0].counted, false); assert.equal(st.payments[0].final, true);
  assert.equal(st.payments[0].payload, undefined);
  const raw = JSON.parse(await readFile(join(s.dir, 'state.json'), 'utf8'));
  assert.equal(raw.payments[0].payload, undefined, 'the signed payload is not kept in the state file');
  assert.equal(s.node.st.processed.map(p => p.subtype).join(','), 'change');
  assert.equal(s.node.st.workCalls, 1, 'the send\'s work is reused');
  // the seller tries to cash the block it kept
  const held = s.door.st.held;
  assert.ok(held && held.signature, 'the seller holds the signed block');
  const late = await fetch(s.node.url, { method: 'POST', body: JSON.stringify({ action: 'process', subtype: 'send', block: held }) }).then(x => x.json());
  assert.equal(late.hash, undefined, 'the held block is dead: ' + JSON.stringify(late));
  assert.equal(s.node.st.balance, 10n * RAW, 'nothing moved');
  assert.equal((await s.call(MSG, {}, '/v1/chat/completions')).status, 502, 'the door still refuses, a fresh send each time');
  assert.equal((await s.stateOf()).spent, '0');
});

test('a retirement that cannot be published keeps the spend counted against the cap until it can', async t => {
  const s = await stand(t, { mode: 'nano', amount: MILLI }, { NANO_CAP: '0.0015' });
  s.node.st.rejectNext = 3;                                   // the send, the change block, and the change block again at the next call
  let r = await s.call(MSG);
  assert.equal(r.status, 402);
  let j = await r.json();
  assert.equal(j.payer.code, 'broadcast_failed');
  assert.equal(j.payer.detail.counted, true, 'no change block could be published: the signed block may still land, so it stays counted');
  assert.equal(j.payer.detail.invalidated_by, null);
  let st = await s.stateOf();
  assert.equal(st.spent, '0.001'); assert.equal(st.payments[0].status, 'not_broadcast'); assert.equal(st.payments[0].counted, true); assert.equal(st.payments[0].final, false);
  r = await s.call(MSG);
  assert.equal(r.status, 402);
  j = await r.json();
  assert.equal(j.payer.code, 'cap_exceeded', 'the held amount counts against the cap');
  assert.equal(s.node.st.processed.length, 0);
  r = await s.call(MSG);
  assert.equal(r.status, 200, 'the change block went through this time, the held amount was released, the call paid');
  st = await s.stateOf();
  assert.equal(st.spent, '0.001');
  assert.equal(st.payments[0].counted, false); assert.equal(st.payments[0].final, true); assert.match(st.payments[0].invalidated_by, /^[0-9A-F]{64}$/);
  assert.equal(s.node.st.processed.map(p => p.subtype).join(','), 'change,send');
});

test('a send signed by a run that died before broadcasting is settled at start-up: retired and uncounted', async t => {
  const s = await stand(t, { mode: 'nano', amount: MILLI });
  assert.equal((await s.call(MSG)).status, 200);
  await s.proxy.stop();
  const file = join(s.dir, 'state.json');
  const raw = JSON.parse(await readFile(file, 'utf8'));
  // a signed, counted, never-broadcast send at the current height, as a crash between persist() and broadcast() leaves it
  raw.payments.push({ t: new Date().toISOString(), kind: 'nano', amount_raw: MILLI.toString(), payTo: s.account, paymentId: 'pay_dead', hash: 'B'.repeat(64), previous: s.node.st.frontier, height: s.node.st.height + 1, work: WORK, status: 'signed', counted: true, path: '/v1/chat/completions' });
  raw.spent_raw = (BigInt(raw.spent_raw) + MILLI).toString();
  await writeFile(file, JSON.stringify(raw));
  const p2 = await s.restart();
  let st;
  for (let i = 0; i < 40; i++) { st = await fetch(`http://127.0.0.1:${p2.port}/_nano/state`, { headers: { authorization: 'Bearer ' + KEY } }).then(r => r.json()); if (st.payments[1].final) break; await new Promise(r => setTimeout(r, 100)); }
  assert.equal(st.spent, '0.001', 'the dead send is uncounted, the real one stays');
  assert.equal(st.payments[1].status, 'signed'); assert.equal(st.payments[1].counted, false); assert.equal(st.payments[1].final, true);
  assert.equal(s.node.st.processed.map(p => p.subtype).join(','), 'send,change');
});

test('refunds: a receivable is pocketed before the next paid call and counted as received', async t => {
  const s = await stand(t, { mode: 'nano', amount: MILLI });
  s.node.st.receivable['C'.repeat(64)] = { amount: (2n * MILLI).toString(), source: 'nano_3arg3asgtigae3xckabaaewkx3bzsh7nwz7jkmjos79ihyaxwphhm6qgjps4' };
  assert.equal((await s.call(MSG)).status, 200);
  const st = await s.stateOf();
  assert.equal(st.received, '0.002'); assert.equal(st.receipts.length, 1);
  assert.equal(s.node.st.processed.map(p => p.subtype).join(','), 'receive,send');
  assert.equal(s.node.st.balance, 10n * RAW + 2n * MILLI - MILLI);
});

test('a door that does not answer 402 is relayed as is; non-/v1 paths are not forwarded', async t => {
  const s = await stand(t, { mode: 'nano', amount: MILLI });
  const r = await s.call(MSG, {}, '/other');
  assert.equal(r.status, 404);
  assert.equal(s.node.st.processed.length, 0);
});

test('refuses to start without a cap, without an upstream, without a 16+ character PROXY_KEY, or with a state file of another account', async t => {
  const dir = await mkdtemp(join(tmpdir(), 'pk-proxy-'));
  t.after(() => rm(dir, { recursive: true, force: true }));
  const seed = randomBytes(32).toString('hex');
  for (const env of [
    { NANO_SEED: seed, UPSTREAM: 'https://example.invalid' },
    { NANO_SEED: seed, NANO_CAP: '0.1' },
    { NANO_SEED: seed, UPSTREAM: 'http://example.invalid', NANO_CAP: '0.1' },
    { NANO_SEED: seed, UPSTREAM: 'https://example.invalid', NANO_CAP: 'lots' },
    { NANO_SEED: seed, UPSTREAM: 'https://example.invalid', NANO_CAP: '0.1', PROXY_KEY: '' },
    { NANO_SEED: seed, UPSTREAM: 'https://example.invalid', NANO_CAP: '0.1', PROXY_KEY: 'short-key' },
  ]) {
    const code = await new Promise(r => spawn(process.execPath, [SCRIPT], { env: { PATH: process.env.PATH, HOME: dir, STATE_FILE: join(dir, 's.json'), PROXY_KEY: KEY, ...env }, stdio: 'ignore' }).on('exit', r));
    assert.equal(code, 2, JSON.stringify(env));
  }
});

test('raw-unit cap boundary: one raw pays exactly once and the next identical quote is refused', async t => {
  const oneRawXno = '0.' + '0'.repeat(29) + '1';
  const s = await stand(t, { mode: 'nano', amount: 1n }, { NANO_CAP: oneRawXno, NANO_MAX_PER_CALL: oneRawXno });
  assert.equal((await s.call(MSG)).status, 200);
  const second = await s.call(MSG);
  assert.equal(second.status, 402);
  assert.equal((await second.json()).payer.code, 'cap_exceeded');
  assert.equal(s.node.st.processed.length, 1);
  assert.equal(s.node.st.processed[0].amount, 1n);
  assert.equal((await s.stateOf()).spent, oneRawXno);
});

test('replayed NanoGPT paymentId: the second quote with the same id is refused before work or signing (Ops Control HQ, Review A case A11)', async t => {
  const s = await stand(t, { mode: 'nano', amount: MILLI, fixedId: 'pay_replayed' });
  assert.equal((await s.call(MSG)).status, 200);
  const work1 = s.node.st.workCalls;
  const second = await s.call(MSG);
  assert.equal(second.status, 402);
  const j = await second.json();
  assert.equal(j.payer.code, 'paymentid_replayed');
  assert.equal(j.payer.detail.paymentId, 'pay_replayed');
  assert.equal(s.node.st.processed.length, 1, 'exactly one send for one payment id');
  assert.equal(s.node.st.workCalls, work1, 'no work requested for the replay');
  assert.equal((await s.stateOf()).spent, '0.001');
});

test('exact quote whose accepts[].resource is on another origin is refused before work or signing (Ops Control HQ, Review A cases A06/A07)', async t => {
  const s = await stand(t, { mode: 'exact', amount: MILLI, resource: 'https://unapproved.example/v1/chat/completions' });
  const r = await s.call(MSG);
  assert.equal(r.status, 402);
  const j = await r.json();
  assert.equal(j.payer.code, 'resource_mismatch');
  assert.equal(j.payer.detail.field, 'accepts.resource');
  assert.equal(j.payer.detail.host, 'unapproved.example');
  assert.equal(s.node.st.processed.length, 0, 'nothing broadcast');
  assert.equal(s.node.st.workCalls, 0, 'no work requested');
  assert.equal((await s.stateOf()).spent, '0');
});

test('exact quote whose top-level resource {url} is on another origin is refused before work or signing', async t => {
  const s = await stand(t, { mode: 'exact', amount: MILLI, resourceTop: { url: 'https://unapproved.example/v1/chat/completions', description: 'x' } });
  const r = await s.call(MSG);
  assert.equal(r.status, 402);
  const j = await r.json();
  assert.equal(j.payer.code, 'resource_mismatch');
  assert.equal(j.payer.detail.field, 'resource');
  assert.equal(s.node.st.processed.length, 0);
  assert.equal(s.node.st.workCalls, 0);
  assert.equal((await s.stateOf()).spent, '0');
});

test('nano quote without expiresAt is refused as malformed before work or signing (pyfile-toolkit, 2026-10-10)', async t => {
  const s = await stand(t, { mode: 'nano', amount: MILLI, noExpiry: true });
  const r = await s.call(MSG);
  assert.equal(r.status, 402);
  const j = await r.json();
  assert.equal(j.payer.code, 'malformed_quote');
  assert.equal(j.payer.detail.field, 'expiresAt');
  assert.equal(s.node.st.processed.length, 0);
  assert.equal(s.node.st.workCalls, 0);
  assert.equal((await s.stateOf()).spent, '0');
});

test('wrong Nano network is refused before work, signing, or broadcast in both dialects', async t => {
  for (const mode of ['nano', 'exact']) {
    const s = await stand(t, { mode, amount: MILLI, network: 'nano:testnet' });
    const r = await s.call(MSG);
    assert.equal(r.status, 402);
    assert.equal((await r.json()).payer.code, 'no_nano_option');
    assert.equal(s.node.st.workCalls, 0);
    assert.equal(s.node.st.processed.length, 0);
    assert.equal((await s.stateOf()).spent, '0');
  }
});

test('RPC account error before submit refuses without work, signing, or broadcast', async t => {
  const s = await stand(t, { mode: 'nano', amount: MILLI });
  s.node.st.accountError = 'upstream timeout';
  const r = await s.call(MSG);
  assert.equal(r.status, 402);
  assert.equal((await r.json()).payer.code, 'account_unreadable');
  assert.equal(s.node.st.workCalls, 0);
  assert.equal(s.node.st.processed.length, 0);
  assert.equal((await s.stateOf()).spent, '0');
});

test('accepted broadcast with lost RPC reply is reconciled once and never paid twice', async t => {
  const s = await stand(t, { mode: 'nano', amount: MILLI });
  s.node.st.lostReplyNext = 1;
  const r = await s.call(MSG);
  assert.equal(r.status, 200);
  assert.equal(s.node.st.processed.length, 1);
  const st = await s.stateOf();
  assert.equal(st.spent, '0.001');
  assert.equal(st.payments.length, 1);
  assert.equal(st.payments[0].status, 'served');
});

test('PROXY_KEY: a /v1 request without the key, or with a wrong one, is refused 401 before the door is reached, counted or anything signed; x-api-key carries it too (ClawHub scanner note, 2026-10-11)', async t => {
  const s = await stand(t, { mode: 'nano', amount: MILLI });
  const bare = (headers, path) => fetch(`http://127.0.0.1:${s.proxy.port}${path || '/v1/chat/completions'}`, { method: 'POST', headers: { 'content-type': 'application/json', ...headers }, body: JSON.stringify(MSG) });
  for (const h of [{}, { authorization: 'Bearer ' + KEY.slice(0, -1) }, { authorization: KEY }, { 'x-api-key': 'not-the-key-at-all-0000' }, { 'x-api-key': KEY + 'x' }]) {
    const r = await bare(h);
    assert.equal(r.status, 401, JSON.stringify(h));
    assert.equal(r.headers.get('x-payer-refused'), 'proxy_key');
    const j = await r.json();
    assert.equal(j.error.code, 'proxy_key');
  }
  assert.equal(s.door.st.lastHeaders, null, 'nothing reached the door');
  assert.equal(s.door.st.completes.length, 0);
  assert.equal(s.node.st.processed.length, 0, 'nothing signed or broadcast');
  const st = await s.stateOf();
  assert.equal(st.calls, 0, 'an unauthenticated request is not a call');
  assert.equal(st.refused, 5);
  // the key in x-api-key (Anthropic-style runtimes) is accepted and, as before, never reaches the door
  const r = await bare({ 'x-api-key': KEY });
  assert.equal(r.status, 200, await r.text());
  assert.equal(s.door.st.lastHeaders['x-api-key'], undefined);
  assert.equal(s.door.st.completes.length, 1);
  assert.equal(s.node.st.processed.length, 1);
  // state is readable without the key (nothing secret in it), /v1 is not
  assert.equal((await s.stateOf()).paid, 1);
});

test('the state readout needs the key: 401 proxy_key without it, 200 as a bearer and as x-api-key, nothing counted', async t => {
  const s = await stand(t, { mode: 'nano', amount: MILLI });
  const url = `http://127.0.0.1:${s.proxy.port}/_nano/state`;
  const bare = await fetch(url);
  assert.equal(bare.status, 401);
  assert.equal(bare.headers.get('x-payer-refused'), 'proxy_key');
  const wrong = await fetch(url, { headers: { authorization: 'Bearer not-the-key-0123456789abcdef' } });
  assert.equal(wrong.status, 401);
  assert.equal((await bare.text()).includes('payments'), false, 'no state in the refusal');
  const bearer = await fetch(url, { headers: { authorization: 'Bearer ' + KEY } });
  assert.equal(bearer.status, 200);
  const viaApiKey = await fetch(url, { headers: { 'x-api-key': KEY } });
  assert.equal(viaApiKey.status, 200);
  const st = await viaApiKey.json();
  assert.equal(st.calls, 0, 'a state read is not a call');
  assert.equal(st.payments.length, 0);
  assert.equal(s.door.st.served, 0);
});

test('browser shapes are refused 403 before the key is even read: a non-loopback Host (DNS rebinding) and any Origin header (no-preflight POST), on /v1 and on /_nano/state', async t => {
  const s = await stand(t, { mode: 'nano', amount: MILLI });
  // raw http.request: Node's fetch silently replaces a caller-set Host header, and the Host is the point here
  const at = (path, headers) => new Promise((resolve, reject) => {
    const body = path === '/_nano/state' ? null : JSON.stringify(MSG);
    const req = httpRequest({ host: '127.0.0.1', port: s.proxy.port, path, method: body ? 'POST' : 'GET', headers: { 'content-type': 'application/json', authorization: 'Bearer ' + KEY, ...(body ? { 'content-length': Buffer.byteLength(body) } : {}), ...headers } }, res => {
      let t = ''; res.on('data', c => { t += c; }); res.on('end', () => resolve({ status: res.statusCode, headers: { get: k => res.headers[k] }, text: async () => t }));
    });
    req.on('error', reject); if (body) req.write(body); req.end();
  });
  for (const [path, headers, code] of [
    ['/v1/chat/completions', { host: 'rebound.example:3402' }, 'host_not_loopback'],
    ['/v1/chat/completions', { host: 'rebound.example' }, 'host_not_loopback'],
    ['/v1/chat/completions', { origin: 'https://evil.example' }, 'browser_origin'],
    ['/v1/chat/completions', { origin: 'null' }, 'browser_origin'],
    ['/_nano/state', { host: 'rebound.example:3402' }, 'host_not_loopback'],
    ['/_nano/state', { origin: 'https://evil.example' }, 'browser_origin'],
  ]) {
    const r = await at(path, headers);
    assert.equal(r.status, 403, path + ' ' + JSON.stringify(headers));
    assert.equal(r.headers.get('x-payer-refused'), code);
  }
  // a browser's actual no-preflight shape: text/plain body, no credential, an Origin: refused on the origin alone
  const r = await fetch(`http://127.0.0.1:${s.proxy.port}/v1/chat/completions`, { method: 'POST', headers: { 'content-type': 'text/plain', origin: 'https://evil.example' }, body: JSON.stringify(MSG) });
  assert.equal(r.status, 403);
  assert.equal(s.door.st.served, 0);
  assert.equal(s.node.st.processed.length, 0);
  // the loopback spellings a runtime uses all pass
  for (const host of ['127.0.0.1:' + s.proxy.port, 'localhost:' + s.proxy.port, 'localhost', '[::1]:' + s.proxy.port]) {
    const ok = await at('/_nano/state', { host });
    assert.equal(ok.status, 200, host);
  }
  const paid = await at('/v1/chat/completions', { host: 'localhost:' + s.proxy.port });
  assert.equal(paid.status, 200, await paid.text());
  assert.equal(s.node.st.processed.length, 1);
});

// ---- a door's redirects: never followed by the poll, never relayed after payment (ClawHub scanner on 0.3.10, 2026-10-22) ----
async function trap() {
  // a listener standing in for something on the operator's local network; records every hit
  const hits = [];
  const srv = createServer((req, res) => { hits.push(req.url); res.writeHead(200, { 'content-type': 'application/json' }); res.end('{"status":"paid","readyToComplete":true}'); });
  const url = await listen(srv);
  return { srv, url, hits };
}

test('status poll: a 302 from the door is not followed; nothing reaches the redirect target, the call completes on the complete step', async t => {
  const tr = await trap();
  t.after(() => { tr.srv.close(); tr.srv.closeAllConnections(); });
  const s = await stand(t, { mode: 'nano', amount: MILLI, statusRedirect: tr.url + '/internal' });
  const r = await s.call(MSG);
  assert.equal(r.status, 200, await r.text());
  assert.equal(tr.hits.length, 0, 'the redirect target was never contacted');
  assert.equal(s.node.st.processed.length, 1);
  assert.equal(s.door.st.completes.length, 1);
  assert.equal((await s.stateOf()).payments[0].status, 'served');
});

test('complete step: a 307 after payment is refused as door_redirect with the hash, never relayed, paid exactly once', async t => {
  // the door sends the paid runtime elsewhere (here: back at a proxy-shaped loopback origin); a relayed 307 would make a
  // following client pay again, a refusal cannot
  const s = await stand(t, { mode: 'nano', amount: MILLI, completeRedirect: 'http://127.0.0.1:3402/v1/chat/completions' });
  const r = await s.call(MSG);
  assert.equal(r.status, 502);
  const j = await r.json();
  assert.equal(j.payer.code, 'door_redirect');
  assert.equal(j.payer.detail.status, 307);
  assert.equal(j.payer.detail.location_origin, 'http://127.0.0.1:3402');
  assert.equal(typeof j.payer.detail.hash, 'string');
  assert.equal(s.node.st.processed.length, 1, 'paid exactly once');
  assert.equal(s.door.st.completes.length, 1);
  const st = await s.stateOf();
  assert.equal(st.payments[0].status, 'paid_not_served');
  assert.equal(st.payments[0].hash, j.payer.detail.hash);
});
