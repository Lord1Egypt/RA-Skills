'use strict';
// `no-node.js receive` is documented as "pocket every confirmed send". GET /v1/receivable answers at most the node's
// bound of hashes per call (100 on pursekeeper.dev) and, since api 2026-10-23, says so with `truncated: true` and a
// `next` line: "pocket these, then poll again for the rest". The script read one page, pocketed it and exited 0, so an
// account with more unpocketed sends than the bound was left with the rest unpocketed and no word that they exist.
// The stand below is the real CLI in its own process against a loopback mock whose bound is 3, with 5 sends pending.

const test = require('node:test');
const assert = require('node:assert/strict');
const { createServer } = require('node:http');
const { execFile } = require('node:child_process');
const { randomBytes } = require('node:crypto');
const { mkdtemp, writeFile, rm } = require('node:fs/promises');
const { tmpdir } = require('node:os');
const { join, resolve } = require('node:path');
const { promisify } = require('node:util');
const N = require('nanocurrency');

const exec = promisify(execFile);
const root = resolve(__dirname, '..');
const script = resolve(process.env.NO_NODE_SCRIPT || join(root, 'scripts/no-node.js'));
const RAW = 10n ** 30n;
const WORK = '0'.repeat(16);   // not real work: the mock does not check it
const BOUND = 3;               // the mock's receivable bound (pursekeeper.dev's is 100)

const localOnly = `
'use strict';
const allowed = new URL(process.env.API);
if (allowed.protocol !== 'http:' || allowed.hostname !== '127.0.0.1') throw new Error('test API must be loopback');
const originalFetch = globalThis.fetch;
globalThis.fetch = (input, init) => {
  const url = new URL(typeof input === 'string' ? input : input.url || input);
  if (url.origin !== allowed.origin || url.username || url.password) throw new Error('non-mock fetch blocked');
  return originalFetch(input, { ...init, redirect: 'error' });
};
`;

async function readJSON(req) { let t = ''; for await (const c of req) t += c; return JSON.parse(t); }

test('receive pockets every pending send when /v1/receivable answers truncated', { timeout: 20000 }, async t => {
  const seed = randomBytes(32).toString('hex');
  const pub = N.derivePublicKey(N.deriveSecretKey(seed, 0));
  const account = N.deriveAddress(pub, { useNanoPrefix: true });
  const peer = N.deriveAddress(N.derivePublicKey(randomBytes(32).toString('hex')), { useNanoPrefix: true });
  let frontier = 'A'.repeat(64), balance = 0n;
  // Five pending sends, listed in a stable order the way a node lists them.
  const pending = ['1', '2', '3', '4', '5'].map((d, i) => ({ hash: d.repeat(64), amount_raw: ((BigInt(i) + 1n) * RAW / 1000n).toString(), from: peer }));
  const received = [];
  const errors = [];
  const dir = await mkdtemp(join(tmpdir(), 'pursekeeper-trunc-'));
  const preload = join(dir, 'local-only.cjs');
  await writeFile(preload, localOnly);
  const server = createServer(async (req, res) => {
    const json = (b, s = 200) => { res.writeHead(s, { 'content-type': 'application/json' }); res.end(JSON.stringify(b)); };
    try {
      const url = new URL(req.url, 'http://127.0.0.1');
      if (req.method === 'GET' && url.pathname === '/v1/account_info')
        return json({ account, found: true, frontier, balance_raw: balance.toString(), representative: account });
      if (req.method === 'GET' && url.pathname === '/v1/receivable') {
        const blocks = pending.slice(0, BOUND);
        const truncated = blocks.length >= BOUND;
        return json({ account, count: blocks.length, blocks, confirmed_only: true, truncated,
          ...(truncated ? { next: 'the node answered its maximum of ' + BOUND + ' receivable hashes; pocket these, then poll again for the rest' } : {}) });
      }
      if (req.method === 'POST' && url.pathname === '/v1/work') { await readJSON(req); return json({ work: WORK }); }
      if (req.method === 'POST' && url.pathname === '/v1/process') {
        const { block } = await readJSON(req);
        if (block.previous !== frontier) return json({ ok: false, error: 'Fork' }, 400);
        const i = pending.findIndex(p => p.hash === block.link);
        if (i < 0) return json({ ok: false, error: 'Unreceivable' }, 400);
        assert.equal(block.balance, (balance + BigInt(pending[i].amount_raw)).toString());
        const hash = N.hashBlock(block);
        assert.ok(N.verifyBlock({ hash, signature: block.signature, publicKey: pub }));
        received.push(pending[i].hash); balance = BigInt(block.balance); frontier = hash; pending.splice(i, 1);
        return json({ ok: true, hash });
      }
      if (req.method === 'GET' && url.pathname === '/v1/verify') return json({ found: false });
      throw new Error('unexpected mock request: ' + req.method + ' ' + url.pathname);
    } catch (e) { errors.push(e); json({ error: 'mock assertion failed' }, 500); }
  });
  t.after(async () => { server.closeAllConnections(); server.close(); await rm(dir, { recursive: true, force: true }); });
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const API = 'http://127.0.0.1:' + server.address().port;
  const { stdout, stderr } = await exec(process.execPath, ['--require', preload, script, 'receive'], {
    cwd: root, env: { API, NANO_SEED: seed, NANO_INDEX: '0', NANO_REP: account, NODE_PATH: join(root, 'node_modules') },
    timeout: 15000, maxBuffer: 65536 });
  assert.deepEqual(errors, [], 'mock assertions must all pass');
  t.diagnostic('received ' + received.length + ' of 5; left pending ' + pending.length);
  assert.equal(pending.length, 0, 'every pending send is pocketed, not only the first page of ' + BOUND + '; stderr: ' + stderr.trim());
  assert.equal(received.length, 5);
  assert.equal(stdout.trim().split('\n').length, 5, 'one receipt line per pocketed send');
});
