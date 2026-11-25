'use strict';
// The unresolved-payment record in scripts/client-x402.js: a retry after an unserved call must never put a second
// payment on the chain for the same call unless the caller says so. Offline: a fake seller and a fake node.

const test = require('node:test');
const assert = require('node:assert/strict');
const { createServer } = require('node:http');
const { randomBytes } = require('node:crypto');
const { execFile } = require('node:child_process');
const { promisify } = require('node:util');
const { resolve, join } = require('node:path');
const fs = require('node:fs');
const os = require('node:os');
const N = require('nanocurrency');

const exec = promisify(execFile);
const root = resolve(__dirname, '..');
const client = resolve(root, 'scripts/client-x402.js');
const PAY_TO = 'nano_1111111111111111111111111111111111111111111111111111hifc8npp';
const REP = 'nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3';
const hex64 = () => randomBytes(32).toString('hex').toUpperCase();

async function readBody(req) { const c = []; for await (const x of req) c.push(x); return Buffer.concat(c).toString('utf8'); }
async function listen(t, handler) {
  const server = createServer(handler);
  await new Promise((ok, no) => { server.once('error', no); server.listen(0, '127.0.0.1', ok); });
  t.after(async () => { server.closeAllConnections?.(); await new Promise(ok => server.close(() => ok())); });
  return 'http://127.0.0.1:' + server.address().port;
}

// One world per test: a seller that answers 402 and then does what `seller.mode` says with the paid request, and a node
// (reachable as a node RPC and as the no-node API on the seller's origin) whose chain the test moves by hand.
async function world(t) {
  const seed = randomBytes(32).toString('hex');
  const account = N.deriveAddress(N.derivePublicKey(N.deriveSecretKey(seed, 0)), { useNanoPrefix: true });
  const first = hex64();
  const node = { frontier: first, chain: new Map([[first, { confirmed: true, successor: null }]]), lookup: 'ok' };
  const seller = { mode: 'drop', paid: [], amount: '1000000000000000000000000000', onPaid: null };
  const dir = fs.mkdtempSync(join(os.tmpdir(), 'pk-pending-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const blockInfo = hash => {
    if (node.lookup === 'error') return { error: 'Too many requests' };
    if (node.lookup === 'account-not-found') return { error: 'Account not found' };
    const b = node.chain.get(String(hash).toUpperCase());
    return b ? { block_account: account, confirmed: b.confirmed ? 'true' : 'false', successor: b.successor || '0'.repeat(64) } : { error: 'Block not found' };
  };
  const rpc = await listen(t, async (req, res) => {
    const q = JSON.parse(await readBody(req));
    res.setHeader('content-type', 'application/json');
    if (q.action === 'account_info') return res.end(JSON.stringify({ frontier: node.frontier, representative: REP, balance: '5000000000000000000000000000000' }));
    res.end(JSON.stringify(q.action === 'block_info' ? blockInfo(q.hash) : { error: 'unknown action' }));
  });
  const origin = await listen(t, async (req, res) => {
    await readBody(req);
    const u = new URL(req.url, 'http://x');
    res.setHeader('content-type', 'application/json');
    if (u.pathname === '/v1/account_info') return res.end(JSON.stringify({ found: true, frontier: node.frontier, representative: REP, balance_raw: '5000000000000000000000000000000' }));
    if (u.pathname === '/v1/verify') {
      const b = blockInfo(u.searchParams.get('hash'));
      if (b.error === 'Block not found') { res.statusCode = 404; return res.end(JSON.stringify({ found: false })); }
      if (b.error) { res.statusCode = 502; return res.end(JSON.stringify({ error: b.error })); }
      return res.end(JSON.stringify({ found: true, confirmed: b.confirmed === 'true', successor: /^0+$/.test(b.successor) ? null : b.successor }));
    }
    if (u.pathname === '/alias') { res.writeHead(302, { location: '/thing' + u.search }); return res.end(); }   // a seller's canonical redirect
    const sig = req.headers['payment-signature'];
    if (!sig) {
      const pr = { x402Version: 2, resource: { url: 'http://x/' }, accepts: [{ scheme: 'exact', network: 'nano:mainnet', asset: 'XNO', amount: seller.amount, payTo: PAY_TO, maxTimeoutSeconds: 60, extra: { workOptional: true } }] };
      res.writeHead(402, { 'payment-required': Buffer.from(JSON.stringify(pr)).toString('base64') });
      return res.end('{}');
    }
    const block = JSON.parse(Buffer.from(sig, 'base64').toString('utf8')).payload.block;
    seller.paid.push({ hash: N.hashBlock(block), previous: block.previous.toUpperCase(), method: req.method });
    if (seller.onPaid) seller.onPaid(seller.paid[seller.paid.length - 1]);
    if (seller.mode === 'drop') return req.socket.destroy();
    if (seller.mode === 'refuse') { res.statusCode = 500; return res.end('{"error":"upstream"}'); }
    res.end('{"ok":true}');
  });
  const run = async (pathAndQuery = '/thing', env = {}, base = origin) => {
    try {
      const r = await exec(process.execPath, [client, base + pathAndQuery], {
        cwd: root, timeout: 10000, maxBuffer: 1024 * 1024,
        env: { PATH: process.env.PATH, NANO_SEED: seed, NANO_RPC: rpc, NANO_MAX_PAY: '1', NANO_LOCK_DIR: dir, NANO_PENDING_DIR: dir, ...env },
      });
      return { code: 0, stdout: r.stdout, stderr: r.stderr };
    } catch (e) { if (e.killed) throw e; return { code: e.code, stdout: e.stdout || '', stderr: e.stderr || '' }; }
  };
  const record = () => { try { return JSON.parse(fs.readFileSync(join(dir, 'pending-' + account + '.json'), 'utf8')); } catch (e) { if (e.code === 'ENOENT') return null; throw e; } };
  const unserved = () => { try { return fs.readFileSync(join(dir, 'unserved-' + account + '.jsonl'), 'utf8').trim().split('\n').map(l => JSON.parse(l)); } catch (e) { if (e.code === 'ENOENT') return []; throw e; } };
  // someone broadcasts a block the seller was given: it becomes the confirmed successor of its predecessor
  const land = b => { node.chain.get(b.previous).successor = b.hash; node.chain.set(b.hash, { confirmed: true, successor: null }); node.frontier = b.hash; };
  // another block lands on the current frontier (a receive, another wallet's send)
  const moveOn = (confirmed = true) => land({ hash: hex64(), previous: node.frontier }) || (node.chain.get(node.frontier).confirmed = confirmed);
  return { account, origin, node, seller, dir, run, record, unserved, land, moveOn };
}

test('a served call leaves no record', async t => {
  const w = await world(t); w.seller.mode = 'serve';
  const r = await w.run();
  assert.equal(r.code, 0, r.stderr);
  assert.equal(w.record(), null);
  assert.equal(w.seller.paid.length, 1);
  assert.doesNotMatch(r.stderr, /also on record/, 'its own entry is not another call');
});

test('the record is on disk when the signed request reaches the seller, and carries nothing spendable', async t => {
  const w = await world(t);
  let atArrival;
  w.seller.onPaid = () => { atArrival = w.record(); };
  const r = await w.run();
  assert.equal(r.code, 1, r.stderr);
  assert.equal(atArrival.length, 1, 'written before the request was sent');
  assert.equal(atArrival[0].hash, w.seller.paid[0].hash);
  const rec = w.record();
  assert.equal(rec[0].previous, w.seller.paid[0].previous);
  assert.deepEqual(Object.keys(rec[0]).sort(), ['amount_raw', 'body_sha256', 'hash', 'method', 'pay_to', 'previous', 'signed_at', 'signed_url', 'url']);
  assert.doesNotMatch(JSON.stringify(rec), /signature|"work"/);
  assert.equal(fs.statSync(join(w.dir, 'pending-' + w.account + '.json')).mode & 0o777, 0o600);
  assert.match(r.stderr, /unresolved payment [0-9A-F]{64} recorded in /);
});

test('lost reply, the block landed: the same call is refused with exit 7 and no second block is signed', async t => {
  const w = await world(t);
  await w.run();
  w.land(w.seller.paid[0]);
  const r = await w.run();
  assert.equal(r.code, 7, r.stderr);
  assert.match(r.stderr, /this call was already paid/);
  assert.match(r.stderr, new RegExp('NANO_PENDING_ACK=' + w.seller.paid[0].hash));
  assert.doesNotMatch(r.stderr, /signed block/);
  assert.equal(w.seller.paid.length, 1, 'no second payment reached the seller');
  assert.equal(w.record().length, 1, 'the entry stays');
});

test('the same call spelled another way is still the same call', async t => {
  const w = await world(t);
  await w.run('/thing', { METHOD: 'post', BODY: '{"n":1}' });
  w.land(w.seller.paid[0]);
  for (const [path, env, base] of [['/thing#frag', { METHOD: 'POST', BODY: '{"n":1}' }], ['/thing', { METHOD: 'Post', BODY: '{"n":1}' }, w.origin.replace('http://', 'HTTP://')]]) {
    const r = await w.run(path, env, base);
    assert.equal(r.code, 7, path + ' ' + r.stderr);
  }
  assert.equal(w.seller.paid.length, 1);
});

test('lost reply, the block landed behind a later block: still refused', async t => {
  const w = await world(t);
  await w.run();
  w.land(w.seller.paid[0]); w.moveOn();
  const r = await w.run();
  assert.equal(r.code, 7, r.stderr);
  assert.equal(w.seller.paid.length, 1);
});

test('NANO_PENDING_ACK with the block hash pays again on purpose and moves the entry to the unserved list', async t => {
  const w = await world(t);
  await w.run();
  const first = w.seller.paid[0].hash;
  w.land(w.seller.paid[0]); w.seller.mode = 'serve';
  const wrong = await w.run('/thing', { NANO_PENDING_ACK: hex64() });
  assert.equal(wrong.code, 7, 'another hash acknowledges nothing');
  const r = await w.run('/thing', { NANO_PENDING_ACK: hex64() + ', ' + first.toLowerCase() });
  assert.equal(r.code, 0, r.stderr);
  assert.equal(w.seller.paid.length, 2);
  assert.equal(w.seller.paid[1].previous, first, 'the second payment is built on the first');
  assert.equal(w.record(), null);
  const u = w.unserved();
  assert.equal(u.length, 1); assert.equal(u[0].hash, first); assert.equal(u[0].acknowledged, true); assert.equal(u[0].fate, 'landed');
});

test('a different call in between does not unlock the paid one', async t => {
  const w = await world(t);
  await w.run('/thing?q=1');
  w.land(w.seller.paid[0]); w.seller.mode = 'serve';
  const other = await w.run('/thing?q=2');
  assert.equal(other.code, 0, other.stderr);
  assert.match(other.stderr, /it stays on record/);
  assert.equal(w.record().length, 1, 'the landed entry is still there');
  const again = await w.run('/thing?q=1');
  assert.equal(again.code, 7, again.stderr);
  assert.equal(w.seller.paid.length, 2, 'q=1 was paid once, q=2 once');
});

test('after the hold a landed entry is history and the call can be bought again', async t => {
  const w = await world(t);
  await w.run();
  w.land(w.seller.paid[0]); w.seller.mode = 'serve';
  const r = await w.run('/thing', { NANO_PENDING_HOLD_H: '0.0000001' });
  assert.equal(r.code, 0, r.stderr);
  assert.equal(w.record(), null);
  assert.equal(w.unserved()[0].acknowledged, false);
});

test('the account moved on and the node cannot say: the same call is refused, another call goes ahead, nothing is dropped', async t => {
  for (const mode of ['error', 'account-not-found']) {
    const w = await world(t);
    await w.run('/thing?q=1');
    w.moveOn(); w.node.lookup = mode;
    const r = await w.run('/thing?q=1');
    assert.equal(r.code, 7, mode + ' ' + r.stderr);
    assert.match(r.stderr, /may already be paid/);
    assert.doesNotMatch(r.stderr, /signed block/);
    w.seller.mode = 'serve';
    const other = await w.run('/thing?q=2');
    assert.equal(other.code, 0, mode + ' ' + other.stderr);
    assert.equal(w.record().length, 1, 'the unknown entry stays');
    w.node.lookup = 'ok';   // now the node shows the predecessor's other, confirmed successor: proven dead
    const again = await w.run('/thing?q=1');
    assert.equal(again.code, 0, again.stderr);
    assert.match(again.stderr, /can never land/);
    assert.equal(w.record(), null);
  }
});

test('"Block not found" from a node that is behind is not proof of death', async t => {
  const w = await world(t);
  const start = w.node.frontier;
  w.moveOn(); await w.run();   // B1 signed on the second block
  const b1 = w.seller.paid[0];
  // the next answers come from a node that has only the first block: older frontier, B1 and its predecessor unknown
  const fresh = w.node.chain; w.node.chain = new Map([[start, { confirmed: true, successor: null }]]); w.node.frontier = start;
  const stale = await w.run();
  assert.equal(stale.code, 7, stale.stderr);
  assert.equal(w.record().length, 1, 'not dropped');
  w.node.chain = fresh; w.land(b1);   // the node catches up and B1 is on the chain
  const r = await w.run();
  assert.equal(r.code, 7, r.stderr);
  assert.match(r.stderr, /already paid/);
  assert.equal(w.seller.paid.length, 1);
});

test('an unconfirmed other successor is not proof of death either', async t => {
  const w = await world(t);
  await w.run();
  w.moveOn(false);
  const r = await w.run();
  assert.equal(r.code, 7, r.stderr);
  assert.match(r.stderr, /may already be paid/);
});

test('never broadcast: the next block names the same predecessor, so the two cannot both land', async t => {
  const w = await world(t);
  await w.run();
  const same = await w.run();   // same quote on the same frontier: the identical block, one entry
  assert.equal(same.code, 1, same.stderr);
  assert.match(same.stderr, /names the same predecessor/);
  assert.equal(w.seller.paid[1].hash, w.seller.paid[0].hash);
  assert.equal(w.record().length, 1, 'one entry per block');
  w.seller.amount = '2000000000000000000000000000';   // a new price: a different block on the same predecessor
  await w.run();
  assert.notEqual(w.seller.paid[2].hash, w.seller.paid[0].hash);
  assert.equal(w.seller.paid[2].previous, w.seller.paid[0].previous);
  assert.deepEqual(w.record().map(p => p.hash), [w.seller.paid[0].hash, w.seller.paid[2].hash], 'both blocks are on record');
});

// ClawHub's scan of 0.3.19 (2026-11-19, SDI-4) read "one block offered for two different calls stands against both"
// beside the code that clears every entry of a block once one call is served on it, and proposed keeping the other
// call's entry. This is that path, start to end. Two calls can share a block only while it has not been broadcast (same
// predecessor, same quote). When one of them is then served, the block has bought that call; the other call has not
// been paid for, and an entry kept for it would refuse its retry with "this call was already paid", which is false.
test('one block offered for two calls: serving one clears both, says so, and the other is then paid for by its own block', async t => {
  const w = await world(t); w.seller.mode = 'refuse';
  const a1 = await w.run('/thing?q=A');   // A: signed, refused by the seller, never broadcast
  assert.equal(a1.code, 1, a1.stderr);
  w.seller.amount = '2000000000000000000000000000';
  await w.run('/thing?q=C');              // C at another price: a different block on the same predecessor, also refused
  w.seller.amount = '1000000000000000000000000000';
  w.seller.mode = 'serve'; w.seller.onPaid = p => w.land(p);   // from here the seller broadcasts what it serves
  const b = await w.run('/thing?q=B');    // same frontier and quote as A: the identical block, now offered for B
  assert.equal(b.code, 0, b.stderr);
  assert.equal(w.seller.paid[2].hash, w.seller.paid[0].hash, 'one block, two calls');
  assert.match(b.stderr, new RegExp('block ' + w.seller.paid[0].hash + ' was also on record for GET [^\\n]*q=A[^\\n]*has not been paid for'));
  assert.deepEqual(w.record().map(p => [p.hash, p.url.slice(-3)]), [[w.seller.paid[1].hash, 'q=C']], 'only the other block is still on record');
  const a2 = await w.run('/thing?q=A');   // A again: not refused as already paid, because it was not
  assert.equal(a2.code, 0, a2.stderr);
  assert.doesNotMatch(a2.stderr, /already paid/);
  assert.match(a2.stderr, new RegExp(w.seller.paid[1].hash + '[^\\n]*can never land'));
  assert.equal(w.seller.paid[3].previous, w.seller.paid[0].hash, 'A is paid by the next block on the chain');
  assert.equal(w.node.chain.size, 3, 'two payments on the chain for two served calls');
  assert.equal(w.record(), null);
});

// Two edges a reviewing agent found beside that path (2026-11-19), both with one block on record for two calls, the block
// on the chain and the reply lost. Until 0.3.20 the acknowledgement and the hold removed entries by block hash.
test('an acknowledgement releases the call being made, not another call on record for the same block', async t => {
  const w = await world(t); w.seller.mode = 'refuse';
  await w.run('/thing?q=A');                                   // A: signed, refused, never broadcast
  w.seller.mode = 'drop'; w.seller.onPaid = p => w.land(p);
  await w.run('/thing?q=B');                                   // the identical block for B lands; B's reply is lost
  const H = w.seller.paid[0].hash;
  assert.equal(w.seller.paid[1].hash, H);
  w.seller.mode = 'serve';
  const a2 = await w.run('/thing?q=A');
  assert.equal(a2.code, 7, a2.stderr);
  assert.match(a2.stderr, /this call may already be paid[^\n]*also on record for GET [^\n]*q=B[^\n]*releases this call only/);
  assert.doesNotMatch(a2.stderr, /this call was already paid/);
  const other = await w.run('/thing?q=Z', { NANO_PENDING_ACK: H });   // an acknowledgement given on another call releases nothing
  assert.equal(other.code, 0, other.stderr);
  assert.match(other.stderr, /an acknowledgement covers the call being made/);
  assert.deepEqual(w.record().map(p => p.url.slice(-3)).sort(), ['q=A', 'q=B']);
  const a3 = await w.run('/thing?q=A', { NANO_PENDING_ACK: H });
  assert.equal(a3.code, 0, a3.stderr);
  assert.deepEqual(w.record().map(p => p.url.slice(-3)), ['q=B'], 'the entry of the call the block may have paid for stays');
  assert.deepEqual(w.unserved().map(u => [u.url.slice(-3), u.acknowledged]), [['q=A', true]]);
  const b2 = await w.run('/thing?q=B');                        // 0.3.19: exit 0 here and a second payment for B
  assert.equal(b2.code, 7, b2.stderr);
  // A's entry has left, and the client still does not know which of the two calls the block bought (the seller in
  // this test broadcast it with B's request; one that had kept A's copy and broadcast that would look the same from
  // here). The first draft of 0.3.20 said "this call was already paid" from this run on.
  assert.match(b2.stderr, /this call may already be paid[^\n]*also on record for GET [^\n]*q=A/);
  assert.doesNotMatch(b2.stderr, /this call was already paid/);
  assert.deepEqual(w.record().map(p => [p.url.slice(-3), p.also_for.map(x => x.slice(-3))]), [['q=B', ['q=A']]]);
  assert.equal(w.seller.paid.length, 4, 'A, B, Z and the acknowledged A; no block was signed for B again');
});

test('the hold runs out per entry: an older entry of the same block does not take a younger one with it', async t => {
  const w = await world(t); w.seller.mode = 'refuse';
  await w.run('/thing?q=A');
  await new Promise(s => setTimeout(s, 4000));
  w.seller.mode = 'drop'; w.seller.onPaid = p => w.land(p);
  await w.run('/thing?q=B');                                   // the identical block lands for B, reply lost
  assert.equal(w.seller.paid[1].hash, w.seller.paid[0].hash);
  w.seller.mode = 'serve';
  const b2 = await w.run('/thing?q=B', { NANO_PENDING_HOLD_H: String(2.5 / 3600) });   // A's entry is older than 2.5 s, B's is not
  assert.equal(b2.code, 7, b2.stderr);
  assert.match(b2.stderr, /q=A is on the chain; older than the hold, moved to /);
  assert.deepEqual(w.record().map(p => p.url.slice(-3)), ['q=B'], "B's own hold has not run out");
  assert.deepEqual(w.unserved().map(u => u.url.slice(-3)), ['q=A']);
  assert.match(b2.stderr, /this call may already be paid[^\n]*also on record for GET [^\n]*q=A/);
  const b3 = await w.run('/thing?q=B');                        // 0.3.19: exit 0 here and a second payment for B
  assert.equal(b3.code, 7, b3.stderr);
  assert.match(b3.stderr, /this call may already be paid[^\n]*also on record for GET [^\n]*q=A/, 'nothing was learned between the two runs, so the wording does not harden');
  assert.doesNotMatch(b3.stderr, /this call was already paid/);
  assert.equal(w.seller.paid.length, 2, 'no block was signed for B again');
});

// Four more from the second review of the draft (2026-11-19). The first is in 0.3.18 and 0.3.19 as released.
test('the hold is counted from the last sending of a block, not from its first signing', async t => {
  const w = await world(t); w.seller.mode = 'refuse';
  await w.run('/thing?q=A');                                   // signed, refused, never broadcast
  const t0 = w.record()[0].signed_at;
  await new Promise(s => setTimeout(s, 4000));
  w.seller.mode = 'drop'; w.seller.onPaid = p => w.land(p);
  await w.run('/thing?q=A');                                   // the identical block, sent again: it lands now, reply lost
  assert.equal(w.seller.paid[1].hash, w.seller.paid[0].hash);
  const rec = w.record();
  assert.equal(rec.length, 1, 'one entry per block and call');
  assert.ok(Date.parse(rec[0].signed_at) >= Date.parse(t0) + 3500, 'the entry carries the time of the second sending');
  w.seller.mode = 'serve';
  const r3 = await w.run('/thing?q=A', { NANO_PENDING_HOLD_H: String(3 / 3600) });   // 0.3.19: exit 0 here, a second payment under 3 s after the first landed
  assert.equal(r3.code, 7, r3.stderr);
  assert.match(r3.stderr, /this call was already paid/);
  assert.equal(w.seller.paid.length, 2, 'no third block reached the seller');
  assert.equal(w.node.chain.size, 2, 'one payment on the chain');
});

test('one call on record twice (as given, and behind a redirect) is one call, not two', async t => {
  const w = await world(t); w.seller.mode = 'refuse';
  await w.run('/alias?q=A');                                   // the quote redirects to /thing?q=A; refused, never broadcast
  w.seller.mode = 'drop'; w.seller.onPaid = p => w.land(p);
  await w.run('/thing?q=A');                                   // the identical block lands, reply lost
  assert.equal(w.seller.paid[1].hash, w.seller.paid[0].hash);
  assert.deepEqual(w.record().map(p => [new URL(p.url).pathname, new URL(p.signed_url).pathname]), [['/alias', '/thing'], ['/thing', '/thing']]);
  w.seller.mode = 'serve';
  for (const path of ['/thing?q=A', '/alias?q=A']) {
    const r = await w.run(path);
    assert.equal(r.code, 7, r.stderr);
    assert.match(r.stderr, /this call was already paid/, 'there is no other call the block could have bought');
    assert.doesNotMatch(r.stderr, /also on record|it bought the other call/);
  }
  const ack = await w.run('/thing?q=A', { NANO_PENDING_ACK: w.seller.paid[0].hash });
  assert.equal(ack.code, 0, ack.stderr);
  assert.equal(w.record(), null, 'the acknowledgement of a call releases both of its entries');
  const v = await world(t); v.seller.mode = 'refuse';
  await v.run('/alias?q=A');
  v.seller.mode = 'serve'; v.seller.onPaid = p => v.land(p);
  const s = await v.run('/thing?q=A');                         // the same call, served on the same block
  assert.equal(s.code, 0, s.stderr);
  assert.doesNotMatch(s.stderr, /also on record/, 'the call just served is that call');
  assert.equal(v.record(), null);
});

test('when the older of two entries for one call runs out its hold, the younger is not told about "another call"', async t => {
  const w = await world(t); w.seller.mode = 'refuse';
  await w.run('/alias?q=A');                                   // recorded behind the redirect; refused, never broadcast
  await new Promise(s => setTimeout(s, 4000));
  w.seller.mode = 'drop'; w.seller.onPaid = p => w.land(p);
  await w.run('/thing?q=A');                                   // the identical block lands, reply lost
  w.seller.mode = 'serve';
  const r1 = await w.run('/thing?q=A', { NANO_PENDING_HOLD_H: String(2.5 / 3600) });   // the /alias entry is older than 2.5 s
  assert.equal(r1.code, 7, r1.stderr);
  assert.match(r1.stderr, /older than the hold, moved to /);
  assert.deepEqual(w.record().map(p => [new URL(p.url).pathname, p.also_for]), [['/thing', undefined]]);
  const r2 = await w.run('/thing?q=A');
  assert.equal(r2.code, 7, r2.stderr);
  assert.match(r2.stderr, /this call was already paid/);
  assert.equal(w.seller.paid.length, 2);
});

test('the same URL with another body on the same block: an acknowledgement for one body keeps the other body\'s entry', async t => {
  const w = await world(t); w.seller.mode = 'refuse';
  await w.run('/thing', { METHOD: 'POST', BODY: '{"n":1}' });
  w.seller.mode = 'drop'; w.seller.onPaid = p => w.land(p);
  await w.run('/thing', { METHOD: 'POST', BODY: '{"n":2}' });  // the identical block lands for body 2, reply lost
  const H = w.seller.paid[0].hash;
  assert.equal(w.seller.paid[1].hash, H);
  assert.equal(w.record().length, 2);
  w.seller.mode = 'serve';
  const a = await w.run('/thing', { METHOD: 'POST', BODY: '{"n":1}', NANO_PENDING_ACK: H });
  assert.equal(a.code, 0, a.stderr);
  const b = await w.run('/thing', { METHOD: 'POST', BODY: '{"n":2}' });
  assert.equal(b.code, 7, b.stderr);
  assert.match(b.stderr, /this call may already be paid/);
  assert.equal(w.seller.paid.length, 3, 'body 1, body 2 and the acknowledged body 1; body 2 was not signed again');
});

test('a block that dies while on record for two calls drops both entries and claims nothing was bought', async t => {
  const w = await world(t); w.seller.mode = 'refuse';
  await w.run('/thing?q=A');                                   // A: signed, refused, never broadcast
  w.seller.onPaid = () => w.moveOn();                          // while the seller holds the same block for B, the account moves
  const b = await w.run('/thing?q=B');
  assert.equal(b.code, 1, b.stderr);
  assert.equal(w.seller.paid[1].hash, w.seller.paid[0].hash);
  assert.match(b.stderr, /can never land/);
  assert.doesNotMatch(b.stderr, /also on record|has now bought/);
  assert.equal(w.record(), null);
});

test('an older un-broadcast block that lands later still blocks the same call (the list is not one entry deep)', async t => {
  const w = await world(t);
  await w.run();
  w.seller.amount = '2000000000000000000000000000';
  await w.run();   // B1 and B2, different blocks on one predecessor, neither served
  assert.notEqual(w.seller.paid[0].hash, w.seller.paid[1].hash);
  w.land(w.seller.paid[0]);   // the seller broadcasts B1 late
  const r = await w.run();
  assert.equal(r.code, 7, r.stderr);
  assert.match(r.stderr, new RegExp('Block ' + w.seller.paid[0].hash));
  assert.match(r.stderr, new RegExp(w.seller.paid[1].hash + '[^\\n]*can never land'));
  assert.equal(w.seller.paid.length, 2, 'no third block');
  assert.deepEqual(w.record().map(p => p.hash), [w.seller.paid[0].hash], 'B2 is proven dead and dropped even though the run refused');
});

test('the same URL with another body or method is another call', async t => {
  const w = await world(t);
  await w.run('/thing', { METHOD: 'POST', BODY: '{"n":1}' });
  w.land(w.seller.paid[0]);
  const same = await w.run('/thing', { METHOD: 'POST', BODY: '{"n":1}' });
  assert.equal(same.code, 7, same.stderr);
  w.seller.mode = 'serve';
  const body = await w.run('/thing', { METHOD: 'POST', BODY: '{"n":2}' });
  assert.equal(body.code, 0, body.stderr);
  const method = await w.run('/thing', { METHOD: 'PUT', BODY: '{"n":1}' });
  assert.equal(method.code, 0, method.stderr);
});

test('a refusal while another block takes the predecessor drops the entry in the same run', async t => {
  const w = await world(t); w.seller.mode = 'refuse';
  w.seller.onPaid = () => w.moveOn();   // the account moves while the seller holds the block
  const r = await w.run();
  assert.equal(r.code, 1, r.stderr);
  assert.match(r.stderr, /can never land/);
  assert.equal(w.record(), null);
});

test('without NANO_RPC the same readings come from the API (/v1/account_info, /v1/verify with successor)', async t => {
  const w = await world(t);
  const env = { NANO_RPC: '', API: w.origin };
  await w.run('/thing', env);
  w.land(w.seller.paid[0]); w.moveOn();
  const paid = await w.run('/thing', env);
  assert.equal(paid.code, 7, paid.stderr);
  assert.match(paid.stderr, /already paid/);
  const v = await world(t);
  await v.run('/thing', { NANO_RPC: '', API: v.origin });
  v.moveOn(); v.seller.mode = 'serve';
  const dead = await v.run('/thing', { NANO_RPC: '', API: v.origin });
  assert.equal(dead.code, 0, dead.stderr);
  assert.match(dead.stderr, /can never land/);
});

test('two processes that do not share the wallet lock both end up on record', async t => {
  const w = await world(t);
  await Promise.all([w.run('/thing?q=1', { NANO_LOCK: '0' }), w.run('/thing?q=2', { NANO_LOCK: '0' }), w.run('/thing?q=3', { NANO_LOCK: '0' })]);
  w.seller.amount = '2000000000000000000000000000';
  await Promise.all([w.run('/thing?q=4', { NANO_LOCK: '0' }), w.run('/thing?q=5', { NANO_LOCK: '0' })]);
  assert.deepEqual(new Set(w.record().map(p => p.url.slice(-3))), new Set(['q=1', 'q=2', 'q=3', 'q=4', 'q=5']));
});

test('a record that cannot be written stops the payment before it is sent', async t => {
  const w = await world(t);
  const ro = join(w.dir, 'read-only'); fs.mkdirSync(ro, { mode: 0o500 });
  t.after(() => { try { fs.chmodSync(ro, 0o700); } catch { /* already removed with the test directory */ } });
  const r = await w.run('/thing', { NANO_PENDING_DIR: ro });
  assert.equal(r.code, 7, r.stderr);
  assert.match(r.stderr, /signed block/);
  assert.match(r.stderr, /cannot be written.*was not sent and is discarded/);
  assert.doesNotMatch(r.stderr, /Nothing signed/);
  assert.equal(w.seller.paid.length, 0, 'the signed request never left the process');
});

test('a record directory that cannot be read stops the payment before anything is signed', async t => {
  const w = await world(t);
  const file = join(w.dir, 'a-file'); fs.writeFileSync(file, 'x');
  const r = await w.run('/thing', { NANO_PENDING_DIR: join(file, 'sub') });
  assert.equal(r.code, 7, r.stderr);
  assert.match(r.stderr, /cannot be read/);
  assert.doesNotMatch(r.stderr, /signed block/);
  assert.equal(w.seller.paid.length, 0);
});

test('a record that cannot be parsed is not overwritten: exit 7', async t => {
  const w = await world(t);
  const file = join(w.dir, 'pending-' + w.account + '.json');
  fs.writeFileSync(file, '{"half":');
  const r = await w.run();
  assert.equal(r.code, 7, r.stderr);
  assert.equal(fs.readFileSync(file, 'utf8'), '{"half":');
  assert.equal(w.seller.paid.length, 0);
});

test('NANO_PENDING=0 turns the record off (the old behaviour)', async t => {
  const w = await world(t);
  await w.run('/thing', { NANO_PENDING: '0' });
  assert.equal(w.record(), null);
  w.land(w.seller.paid[0]);
  const r = await w.run('/thing', { NANO_PENDING: '0' });
  assert.equal(r.code, 1);
  assert.equal(w.seller.paid.length, 2, 'without the record the retry pays twice');
});
