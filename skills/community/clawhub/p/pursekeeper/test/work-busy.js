'use strict';
// POST /v1/work answers 503 {"error": "work server busy; retry in a few seconds; nothing charged"} while four proofs are
// being generated (api server.js workGenerate: the four slots are shared by every caller, free and paid). The answer is
// transient by its own words, and no-node.js's work() already waits out the free-limit answer, but it threw on the 503,
// so `send` died before broadcasting and `receive` died part-way through a run of pending sends. The stand is the real
// CLI in its own process against a loopback mock whose /v1/work is busy on the first ask.

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
const WORK = '0'.repeat(16);

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

test('send waits out a 503 "work server busy" from /v1/work and broadcasts once', { timeout: 30000 }, async t => {
  const seed = randomBytes(32).toString('hex');
  const pub = N.derivePublicKey(N.deriveSecretKey(seed, 0));
  const account = N.deriveAddress(pub, { useNanoPrefix: true });
  const peer = N.deriveAddress(N.derivePublicKey(randomBytes(32).toString('hex')), { useNanoPrefix: true });
  let frontier = 'A'.repeat(64), balance = 5n * RAW, workAsks = 0;
  const accepted = [], errors = [];
  const dir = await mkdtemp(join(tmpdir(), 'pursekeeper-busy-'));
  const preload = join(dir, 'local-only.cjs');
  await writeFile(preload, localOnly);
  const server = createServer(async (req, res) => {
    const json = (b, s = 200) => { res.writeHead(s, { 'content-type': 'application/json' }); res.end(JSON.stringify(b)); };
    try {
      const url = new URL(req.url, 'http://127.0.0.1');
      if (req.method === 'GET' && url.pathname === '/v1/account_info')
        return json({ account, found: true, frontier, balance_raw: balance.toString(), representative: account });
      if (req.method === 'GET' && url.pathname === '/v1/receivable') return json({ account, count: 0, blocks: [], truncated: false });
      if (req.method === 'POST' && url.pathname === '/v1/work') {
        const { hash } = await readJSON(req); assert.equal(hash, frontier);
        // The server's exact 503 body (api server.js workGenerate) on the first ask, work after that.
        if (++workAsks === 1) return json({ error: 'work server busy; retry in a few seconds; nothing charged' }, 503);
        return json({ hash, work: WORK, source: 'gpu', tier: 'free' });
      }
      if (req.method === 'POST' && url.pathname === '/v1/process') {
        const { block } = await readJSON(req);
        if (block.previous !== frontier) return json({ ok: false, error: 'Fork' }, 400);
        const hash = N.hashBlock(block);
        assert.ok(N.verifyBlock({ hash, signature: block.signature, publicKey: pub }));
        accepted.push(hash); frontier = hash; balance = BigInt(block.balance);
        return json({ ok: true, hash });
      }
      throw new Error('unexpected mock request: ' + req.method + ' ' + url.pathname);
    } catch (e) { errors.push(e); json({ error: 'mock assertion failed' }, 500); }
  });
  t.after(async () => { server.closeAllConnections(); server.close(); await rm(dir, { recursive: true, force: true }); });
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const API = 'http://127.0.0.1:' + server.address().port;
  let out;
  try {
    out = await exec(process.execPath, ['--require', preload, script, 'send', peer, '1'], {
      cwd: root, env: { API, NANO_SEED: seed, NANO_INDEX: '0', NANO_REP: account, NODE_PATH: join(root, 'node_modules') },
      timeout: 25000, maxBuffer: 65536 });
  } catch (e) { out = { failed: true, code: e.code, stdout: e.stdout, stderr: e.stderr }; }
  assert.deepEqual(errors, [], 'mock assertions must all pass');
  assert.ok(!out.failed, 'send must not die on a transient 503 from /v1/work: exit ' + out.code + ', stderr: ' + String(out.stderr).trim());
  assert.equal(workAsks, 2, 'asked again after the busy answer');
  assert.equal(accepted.length, 1, 'one block broadcast');
  assert.equal(balance, 4n * RAW);
  assert.match(out.stdout, /^send 1 to /);
});
