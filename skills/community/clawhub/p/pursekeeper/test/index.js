'use strict';

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
// Optional local snapshot for the documented 0.1.3 RED / 0.1.4 GREEN check.
const script = resolve(process.env.NO_NODE_SCRIPT || join(root, 'scripts/no-node.js'));
const RAW = 10n ** 30n;
const INITIAL_BALANCE = 5n * RAW;
const AMOUNT = RAW;
const INITIAL_FRONTIER = 'A'.repeat(64);
const SOURCE_HASH = 'B'.repeat(64);
// Deliberately not real proof of work: these blocks are only for the local stand.
const WORK = '0'.repeat(16);

// The real CLI uses fetch. Restrict it to this test's loopback origin, including
// redirects, rather than inheriting a user's API, seed, proxy or NODE_OPTIONS.
const localOnly = `
'use strict';
const allowed = new URL(process.env.API);
if (allowed.protocol !== 'http:' || allowed.hostname !== '127.0.0.1') {
  throw new Error('test API must be loopback');
}
const originalFetch = globalThis.fetch;
globalThis.fetch = (input, init) => {
  const url = new URL(typeof input === 'string' ? input : input.url || input);
  if (url.origin !== allowed.origin || url.username || url.password) {
    throw new Error('non-mock fetch blocked');
  }
  return originalFetch(input, { ...init, redirect: 'error' });
};
`;

function identity(seed) {
  const publicKey = N.derivePublicKey(N.deriveSecretKey(seed, 0));
  return { publicKey, account: N.deriveAddress(publicKey, { useNanoPrefix: true }) };
}

async function readJSON(req) {
  let text = '';
  for await (const chunk of req) {
    text += chunk;
    assert.ok(text.length < 32768, 'bounded mock request');
  }
  return JSON.parse(text);
}

async function lostReply(t, command) {
  const seed = randomBytes(32).toString('hex');
  const owner = identity(seed);
  const peer = identity(randomBytes(32).toString('hex'));
  let frontier = INITIAL_FRONTIER;
  let balance = INITIAL_BALANCE;
  let pending = command === 'receive';
  let processCalls = 0;
  let infoCalls = 0;
  let workCalls = 0;
  let lostReplies = 0;
  const accepted = [];
  const errors = [];
  const requests = [];
  const dir = await mkdtemp(join(tmpdir(), 'pursekeeper-retry-'));
  const preload = join(dir, 'local-only.cjs');
  let server;
  t.after(async () => {
    if (server?.listening) {
      await new Promise((done, reject) => {
        server.close(error => error ? reject(error) : done());
        server.closeAllConnections();
      });
    }
    await rm(dir, { recursive: true, force: true });
  });
  await writeFile(preload, localOnly);

  server = createServer(async (req, res) => {
    const json = (body, status = 200) => {
      res.writeHead(status, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(body));
    };
    try {
      const url = new URL(req.url, 'http://127.0.0.1');
      requests.push(`${req.method} ${url.pathname}`);
      if (req.method === 'GET' && url.pathname === '/v1/account_info') {
        assert.equal(url.searchParams.get('account'), owner.account);
        infoCalls++;
        return json({ found: true, frontier, balance_raw: balance.toString(), representative: owner.account });
      }
      if (req.method === 'GET' && url.pathname === '/v1/receivable') {
        assert.equal(url.searchParams.get('account'), owner.account);
        return json({ blocks: pending ? [{ hash: SOURCE_HASH, amount_raw: AMOUNT.toString(), from: peer.account }] : [] });
      }
      if (req.method === 'POST' && url.pathname === '/v1/work') {
        const body = await readJSON(req);
        assert.equal(body.hash, frontier);
        workCalls++;
        return json({ work: WORK });
      }
      if (req.method === 'POST' && url.pathname === '/v1/process') {
        processCalls++;
        const { block, subtype } = await readJSON(req);
        assert.equal(block.type, 'state');
        assert.equal(block.account, owner.account);
        assert.equal(block.representative, owner.account);
        assert.equal(block.work, WORK);
        assert.equal(subtype, command);
        // Model the node's ordering: previous must be the actual current frontier.
        if (block.previous !== frontier) return json({ ok: false, error: 'Fork' });
        if (command === 'receive' && !pending) return json({ ok: false, error: 'Unreceivable' });
        assert.equal(block.link, command === 'send' ? peer.publicKey : SOURCE_HASH);
        const nextBalance = balance + (command === 'send' ? -AMOUNT : AMOUNT);
        assert.equal(block.balance, nextBalance.toString());
        const hash = N.hashBlock(block);
        assert.ok(N.verifyBlock({ hash, signature: block.signature, publicKey: owner.publicKey }));
        accepted.push({ hash, block, subtype });
        // Crucial: use the accepted block's real hash, never an arbitrary frontier.
        frontier = hash;
        balance = nextBalance;
        if (command === 'receive') pending = false;
        if (accepted.length === 1) {
          lostReplies++;
          // The block landed, but its success reply was lost. "Fork" enters the
          // stale-frontier path in both 0.1.3 and 0.1.4 (issue #3's node-like stand).
          return json({ ok: false, error: 'Fork' }, 502);
        }
        // Accept a valid second send rather than faking a pass by rejecting it.
        return json({ ok: true, hash });
      }
      if (req.method === 'GET' && url.pathname === '/v1/verify') {
        const hash = url.searchParams.get('hash');
        assert.match(hash || '', /^[0-9A-F]{64}$/);
        return json({ found: accepted.some(block => block.hash === hash), hash });
      }
      throw new Error(`unexpected mock request: ${req.method} ${url.pathname}`);
    } catch (error) {
      errors.push(error);
      json({ error: 'mock assertion failed' }, 500);
    }
  });
  await new Promise((done, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', done);
  });
  const API = `http://127.0.0.1:${server.address().port}`;
  const args = command === 'send' ? ['send', peer.account, '1'] : ['receive'];
  const { stdout, stderr } = await exec(process.execPath, ['--require', preload, script, ...args], {
    cwd: root,
    env: { API, NANO_SEED: seed, NANO_INDEX: '0', NANO_REP: owner.account, NODE_PATH: join(root, 'node_modules') },
    timeout: 10000,
    maxBuffer: 65536,
  });
  assert.deepEqual(errors, [], 'mock assertions must all pass');
  t.diagnostic(`${command}: process=${processCalls}, accepted=${accepted.length}, work=${workCalls}, raw delta=${balance - INITIAL_BALANCE}`);
  assert.equal(lostReplies, 1, 'the accepted first block got an error, not a success response');
  assert.equal(processCalls, 1, `do not broadcast a second ${command}: ${stderr}`);
  assert.equal(accepted.length, 1, 'exactly one block was accepted');
  assert.equal(workCalls, 1, 'no second block should be built');
  assert.equal(infoCalls, 2, 'refresh after the lost reply');
  assert.ok(requests.includes('GET /v1/receivable'));
  assert.equal(balance, INITIAL_BALANCE + (command === 'send' ? -AMOUNT : AMOUNT));
  assert.equal(frontier, accepted[0].hash);
  assert.equal(pending, false);
  assert.ok(stdout.startsWith(`${command} 1 `), 'successful CLI receipt, not just a skip');
  assert.ok(stdout.includes(accepted[0].hash), 'return the original accepted hash');
  assert.equal(stdout.trim().split('\n').length, 1, 'one CLI receipt');
}

// Exercise the real CLI in separate processes; only the remote node is mocked.
test('send with a lost reply publishes and accepts exactly one block', { timeout: 15000 }, async t => {
  await lostReply(t, 'send');
});

test('receive with a lost reply returns the original accepted block', { timeout: 15000 }, async t => {
  await lostReply(t, 'receive');
});
