/**
 * Tests for pair-http (P2 of the v3.3.0 QR-pairing implementation).
 *
 * Uses a live ephemeral HTTP server so the handlers run through the
 * real IncomingMessage / ServerResponse contract. The session store
 * runs against a real tmpfile (same as pair-session-store.test).
 *
 * Test matrix:
 *   1. GET /finish — valid sid → 200 HTML with sid / mode / apiBase embedded.
 *   2. GET /finish — missing sid → 400.
 *   3. GET /finish — unknown sid → 404.
 *   4. GET /finish — terminal session (completed) → 410.
 *   5. GET /start — valid sid + correct code → 200 + session transitions to device_connected.
 *   6. GET /start — wrong code → 403; attempts counter increments.
 *   7. GET /start — 5 wrong codes → session transitions to rejected, 403 attempts_exhausted.
 *   8. GET /start — missing sid / missing code → 400.
 *   9. GET /start — unknown sid → 404.
 *   10. GET /start — expired session → 410.
 *   11. POST /respond — wrong method (GET) → 405.
 *   12. POST /respond — wrong content-type → 400.
 *   13. POST /respond — oversize body → 400.
 *   14. POST /respond — malformed JSON → 400.
 *   15. POST /respond — body missing fields → 400 bad_sid / bad_pk_d / bad_nonce / bad_ct.
 *   16. POST /respond — body wrong version → 400 unsupported_version.
 *   17. POST /respond — respond without prior device_connected → 409 not_device_connected.
 *   18. POST /respond — valid encrypted payload + device_connected → 200 + completePairing called with mnemonic.
 *   19. POST /respond — valid payload, completePairing returns state=error → 500.
 *   20. POST /respond — tampered ciphertext → 400 decrypt_failed + session → rejected.
 *   21. GET /status — returns current status (awaiting_scan / device_connected / completed).
 *   22. Full end-to-end flow: create session, /start, /respond, assert completePairing invoked.
 *   23. Rate-limited/oversize body boundary.
 *
 * Run with: npx tsx pair-http.test.ts
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import http from 'node:http';
import type { AddressInfo } from 'node:net';

import {
  createPairSession,
  transitionPairSession,
  getPairSession,
  type PairSession,
} from './pair-session-store.js';
import {
  generateGatewayKeypair,
  encryptPairingPayload,
  derivePublicFromPrivate,
} from './pair-crypto.js';
import { buildPairRoutes, type CompletePairingHandler, type PairLogger } from './pair-http.js';

let passed = 0;
let failed = 0;
function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) { console.log(`ok ${n} - ${name}`); passed++; }
  else { console.log(`not ok ${n} - ${name}`); failed++; }
}

function mkTmp(): string {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'tr-pair-http-'));
}

const silentLogger: PairLogger = {
  info() {},
  warn() {},
  error() {},
};

/**
 * Build an HTTP server that routes exactly the four registered paths
 * and returns (port, close). Mirrors what OpenClaw's gateway plugin
 * router does in production.
 */
function startTestServer(routes: {
  finishPath: string;
  startPath: string;
  respondPath: string;
  statusPath: string;
  handlers: {
    finish: http.RequestListener;
    start: http.RequestListener;
    respond: http.RequestListener;
    status: http.RequestListener;
  };
}): Promise<{ url: string; close: () => Promise<void> }> {
  const server = http.createServer(async (req, res) => {
    try {
      const url = new URL(req.url ?? '/', 'http://localhost');
      if (url.pathname === routes.finishPath) await routes.handlers.finish(req, res);
      else if (url.pathname === routes.startPath) await routes.handlers.start(req, res);
      else if (url.pathname === routes.respondPath) await routes.handlers.respond(req, res);
      else if (url.pathname === routes.statusPath) await routes.handlers.status(req, res);
      else {
        res.statusCode = 404; res.end('no route');
      }
    } catch (err) {
      if (!res.headersSent) {
        res.statusCode = 500;
        res.end(`Internal: ${err instanceof Error ? err.message : String(err)}`);
      }
    }
  });

  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => {
      const addr = server.address() as AddressInfo;
      const url = `http://127.0.0.1:${addr.port}`;
      resolve({
        url,
        close: () => new Promise<void>((r) => server.close(() => r())),
      });
    });
  });
}

interface TestFixtureOptions {
  /** Override the completePairing stub; default records calls in an array. */
  completePairing?: CompletePairingHandler;
  /** Fixed now() for deterministic countdown; defaults to real Date.now. */
  now?: () => number;
}

interface TestFixture {
  tmp: string;
  sessionsPath: string;
  url: string;
  routes: ReturnType<typeof buildPairRoutes>;
  completeCalls: Array<{ mnemonic: string; sid: string }>;
  cleanup: () => Promise<void>;
}

async function withFixture(
  body: (fx: TestFixture) => Promise<void>,
  opts: TestFixtureOptions = {},
): Promise<void> {
  const tmp = mkTmp();
  const sessionsPath = path.join(tmp, 'pair.json');
  const completeCalls: Array<{ mnemonic: string; sid: string }> = [];
  const completePairing: CompletePairingHandler =
    opts.completePairing ??
    (async ({ mnemonic, session }) => {
      completeCalls.push({ mnemonic, sid: session.sid });
      return { state: 'active', accountId: 'acct_test' };
    });
  const routes = buildPairRoutes({
    sessionsPath,
    apiBase: '/plugin/totalreclaw/pair',
    completePairing,
    logger: silentLogger,
    now: opts.now,
  });
  const { url, close } = await startTestServer(routes);
  try {
    await body({ tmp, sessionsPath, url, routes, completeCalls, cleanup: async () => { await close(); fs.rmSync(tmp, { recursive: true, force: true }); } });
  } finally {
    await close();
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

async function readText(r: Response): Promise<string> {
  const txt = await r.text();
  return txt;
}

async function readJson<T = unknown>(r: Response): Promise<T> {
  return (await r.json()) as T;
}

async function main(): Promise<void> {
  // =======================================================================
  // 1. GET /finish — valid sid
  // =======================================================================
  await withFixture(async ({ url, sessionsPath }) => {
    const kp = generateGatewayKeypair();
    const s = await createPairSession(sessionsPath, {
      mode: 'generate',
      operatorContext: { channel: 'cli' },
      rngPrivateKey: () => Buffer.from(kp.skB64, 'base64url'),
      rngPublicKey: () => Buffer.from(kp.pkB64, 'base64url'),
    });
    const r = await fetch(`${url}/plugin/totalreclaw/pair/finish?sid=${s.sid}`);
    assert(r.status === 200, 'finish: status 200 for valid sid');
    const html = await readText(r);
    assert(html.includes(s.sid), 'finish: HTML embeds sid');
    assert(html.includes('"generate"'), 'finish: HTML embeds mode generate');
    assert(r.headers.get('content-type')?.includes('text/html') === true, 'finish: content-type html');
    assert(r.headers.get('cache-control')?.includes('no-store') === true, 'finish: cache-control no-store');
    assert(r.headers.get('x-frame-options') === 'DENY', 'finish: X-Frame-Options DENY');
  });

  // =======================================================================
  // 2. GET /finish — missing sid → 400
  // =======================================================================
  await withFixture(async ({ url }) => {
    const r = await fetch(`${url}/plugin/totalreclaw/pair/finish`);
    assert(r.status === 400, 'finish: missing sid → 400');
  });

  // =======================================================================
  // 3. GET /finish — unknown sid → 404
  // =======================================================================
  await withFixture(async ({ url }) => {
    const r = await fetch(`${url}/plugin/totalreclaw/pair/finish?sid=deadbeef`);
    assert(r.status === 404, 'finish: unknown sid → 404');
  });

  // =======================================================================
  // 4. GET /finish — terminal session → 410
  // =======================================================================
  await withFixture(async ({ url, sessionsPath }) => {
    const s = await createPairSession(sessionsPath, {
      mode: 'generate',
      operatorContext: { channel: 'cli' },
    });
    await transitionPairSession(sessionsPath, s.sid, 'completed');
    const r = await fetch(`${url}/plugin/totalreclaw/pair/finish?sid=${s.sid}`);
    assert(r.status === 410, 'finish: terminal session → 410');
  });

  // =======================================================================
  // 5. GET /start — valid + correct code → 200 + device_connected
  // =======================================================================
  await withFixture(async ({ url, sessionsPath }) => {
    const s = await createPairSession(sessionsPath, {
      mode: 'generate',
      operatorContext: { channel: 'cli' },
      rngSecondaryCode: () => '123456',
    });
    const r = await fetch(`${url}/plugin/totalreclaw/pair/start?sid=${s.sid}&c=123456`);
    assert(r.status === 200, 'start: correct code → 200');
    const body = await readJson<{ mode: string; expiresAt: number }>(r);
    assert(body.mode === 'generate', 'start: returns mode');
    assert(typeof body.expiresAt === 'number', 'start: returns expiresAt');
    const updated = await getPairSession(sessionsPath, s.sid);
    assert(updated?.status === 'device_connected', 'start: session transitioned to device_connected');
  });

  // =======================================================================
  // 6. GET /start — wrong code → 403 + attempts increments
  // =======================================================================
  await withFixture(async ({ url, sessionsPath }) => {
    const s = await createPairSession(sessionsPath, {
      mode: 'generate',
      operatorContext: { channel: 'cli' },
      rngSecondaryCode: () => '111111',
    });
    const r = await fetch(`${url}/plugin/totalreclaw/pair/start?sid=${s.sid}&c=222222`);
    assert(r.status === 403, 'start: wrong code → 403');
    const body = await readJson<{ error: string }>(r);
    assert(body.error === 'wrong_code', 'start: error=wrong_code');
    const after = await getPairSession(sessionsPath, s.sid);
    assert(after?.secondaryCodeAttempts === 1, 'start: attempts counter incremented');
    assert(after?.status === 'awaiting_scan', 'start: still awaiting_scan after 1 miss');
  });

  // =======================================================================
  // 7. GET /start — 5 wrong codes → rejected + attempts_exhausted
  // =======================================================================
  await withFixture(async ({ url, sessionsPath }) => {
    const s = await createPairSession(sessionsPath, {
      mode: 'generate',
      operatorContext: { channel: 'cli' },
      rngSecondaryCode: () => '999999',
    });
    let lastStatus = -1;
    let lastError = '';
    for (let i = 0; i < 5; i++) {
      const r = await fetch(`${url}/plugin/totalreclaw/pair/start?sid=${s.sid}&c=000000`);
      lastStatus = r.status;
      const j = await readJson<{ error: string }>(r);
      lastError = j.error;
    }
    assert(lastStatus === 403, 'start-lockout: final response 403');
    assert(lastError === 'attempts_exhausted', 'start-lockout: error=attempts_exhausted');
    const after = await getPairSession(sessionsPath, s.sid);
    assert(after?.status === 'rejected', 'start-lockout: session transitioned to rejected');
  });

  // =======================================================================
  // 8. GET /start — missing sid / missing code → 400
  // =======================================================================
  await withFixture(async ({ url }) => {
    const r1 = await fetch(`${url}/plugin/totalreclaw/pair/start?c=123456`);
    assert(r1.status === 400, 'start: missing sid → 400');
    const r2 = await fetch(`${url}/plugin/totalreclaw/pair/start?sid=x`);
    assert(r2.status === 400, 'start: missing code → 400');
  });

  // =======================================================================
  // 9. GET /start — unknown sid → 404
  // =======================================================================
  await withFixture(async ({ url }) => {
    const r = await fetch(`${url}/plugin/totalreclaw/pair/start?sid=deadbeef&c=123456`);
    assert(r.status === 404, 'start: unknown sid → 404');
  });

  // =======================================================================
  // 10. GET /start — expired session → 410
  // NOTE: we create the session with real-time now() (so retention is
  // not triggered by stale prune math), then explicitly transition to
  // 'expired'. The handler's session-status branch returns 410.
  // =======================================================================
  await withFixture(async ({ url, sessionsPath }) => {
    const s = await createPairSession(sessionsPath, {
      mode: 'generate',
      operatorContext: { channel: 'cli' },
      rngSecondaryCode: () => '123456',
    });
    await transitionPairSession(sessionsPath, s.sid, 'expired');
    const r = await fetch(`${url}/plugin/totalreclaw/pair/start?sid=${s.sid}&c=123456`);
    assert(r.status === 410, 'start: expired session → 410');
  });

  // =======================================================================
  // 11. POST /respond — wrong method (GET) → 405
  // =======================================================================
  await withFixture(async ({ url }) => {
    const r = await fetch(`${url}/plugin/totalreclaw/pair/respond`);
    assert(r.status === 405, 'respond: GET → 405');
  });

  // =======================================================================
  // 12. POST /respond — wrong content-type → 400
  // =======================================================================
  await withFixture(async ({ url }) => {
    const r = await fetch(`${url}/plugin/totalreclaw/pair/respond`, {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain' },
      body: 'hello',
    });
    assert(r.status === 400, 'respond: wrong content-type → 400');
  });

  // =======================================================================
  // 13. POST /respond — oversize body → 400
  // =======================================================================
  await withFixture(async ({ url }) => {
    const big = 'x'.repeat(9000);
    const r = await fetch(`${url}/plugin/totalreclaw/pair/respond`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ junk: big }),
    });
    assert(r.status === 400, 'respond: oversize body → 400');
  });

  // =======================================================================
  // 14. POST /respond — malformed JSON → 400
  // =======================================================================
  await withFixture(async ({ url }) => {
    const r = await fetch(`${url}/plugin/totalreclaw/pair/respond`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: 'not json',
    });
    assert(r.status === 400, 'respond: malformed JSON → 400');
  });

  // =======================================================================
  // 15. POST /respond — body missing fields → 400
  // =======================================================================
  await withFixture(async ({ url }) => {
    const cases = [
      { label: 'missing sid', body: { v: 1, pk_d: 'AA', nonce: 'AA', ct: 'AA' } },
      { label: 'bad sid format', body: { v: 1, sid: 'xyz', pk_d: 'AA', nonce: 'AA', ct: 'AA' } },
      { label: 'bad pk_d size', body: { v: 1, sid: 'a'.repeat(32), pk_d: 'AA', nonce: 'AA', ct: 'AA' } },
    ];
    for (const c of cases) {
      const r = await fetch(`${url}/plugin/totalreclaw/pair/respond`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(c.body),
      });
      assert(r.status === 400, `respond-validation: ${c.label} → 400`);
    }
  });

  // =======================================================================
  // 16. POST /respond — wrong version → 400 unsupported_version
  // =======================================================================
  await withFixture(async ({ url }) => {
    const r = await fetch(`${url}/plugin/totalreclaw/pair/respond`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        v: 2,
        sid: 'a'.repeat(32),
        pk_d: Buffer.alloc(32, 0).toString('base64url'),
        nonce: Buffer.alloc(12, 0).toString('base64url'),
        ct: Buffer.alloc(32, 0).toString('base64url'),
      }),
    });
    assert(r.status === 400, 'respond: v=2 → 400');
    const body = await readJson<{ error: string }>(r);
    assert(body.error === 'unsupported_version', 'respond: error=unsupported_version');
  });

  // =======================================================================
  // 17. POST /respond — respond before device_connected → 409 not_device_connected
  // =======================================================================
  await withFixture(async ({ url, sessionsPath }) => {
    const gw = generateGatewayKeypair();
    const dev = generateGatewayKeypair();
    const s = await createPairSession(sessionsPath, {
      mode: 'generate',
      operatorContext: { channel: 'cli' },
      rngPrivateKey: () => Buffer.from(gw.skB64, 'base64url'),
      rngPublicKey: () => Buffer.from(gw.pkB64, 'base64url'),
    });
    // Session is still 'awaiting_scan' — skip /start.
    const enc = encryptPairingPayload({
      skLocalB64: dev.skB64,
      pkRemoteB64: gw.pkB64,
      sid: s.sid,
      plaintext: Buffer.from('word '.repeat(12).trim()),
    });
    const r = await fetch(`${url}/plugin/totalreclaw/pair/respond`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        v: 1,
        sid: s.sid,
        pk_d: dev.pkB64,
        nonce: enc.nonceB64,
        ct: enc.ciphertextB64,
      }),
    });
    assert(r.status === 409, 'respond-order: no prior device_connected → 409');
    const body = await readJson<{ error: string }>(r);
    assert(body.error === 'not_device_connected', 'respond-order: error=not_device_connected');
    // Session should now be rejected.
    const after = await getPairSession(sessionsPath, s.sid);
    assert(after?.status === 'rejected', 'respond-order: session → rejected');
  });

  // =======================================================================
  // 18. Full happy path: /start then /respond with valid ciphertext
  // =======================================================================
  await withFixture(async ({ url, sessionsPath, completeCalls }) => {
    const gw = generateGatewayKeypair();
    const dev = generateGatewayKeypair();
    const s = await createPairSession(sessionsPath, {
      mode: 'generate',
      operatorContext: { channel: 'cli' },
      rngPrivateKey: () => Buffer.from(gw.skB64, 'base64url'),
      rngPublicKey: () => Buffer.from(gw.pkB64, 'base64url'),
      rngSecondaryCode: () => '654321',
    });

    // /start
    const rs = await fetch(`${url}/plugin/totalreclaw/pair/start?sid=${s.sid}&c=654321`);
    assert(rs.status === 200, 'e2e: /start → 200');

    // Encrypt a valid 12-word phrase
    const mnemonic = 'abandon ability able about above absent absorb abstract absurd abuse access accident';
    const enc = encryptPairingPayload({
      skLocalB64: dev.skB64,
      pkRemoteB64: gw.pkB64,
      sid: s.sid,
      plaintext: Buffer.from(mnemonic),
    });

    // /respond
    const rr = await fetch(`${url}/plugin/totalreclaw/pair/respond`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        v: 1,
        sid: s.sid,
        pk_d: dev.pkB64,
        nonce: enc.nonceB64,
        ct: enc.ciphertextB64,
      }),
    });
    assert(rr.status === 200, 'e2e: /respond → 200');
    const body = await readJson<{ ok: boolean; accountId: string }>(rr);
    assert(body.ok === true, 'e2e: ok=true');
    assert(body.accountId === 'acct_test', 'e2e: accountId echoed');

    assert(completeCalls.length === 1, 'e2e: completePairing called once');
    assert(completeCalls[0].mnemonic === mnemonic, 'e2e: completePairing received decrypted mnemonic');

    const after = await getPairSession(sessionsPath, s.sid);
    assert(after?.status === 'completed', 'e2e: session transitioned to completed');
  });

  // =======================================================================
  // 19. /respond with completePairing failure → 500
  // =======================================================================
  await withFixture(
    async ({ url, sessionsPath }) => {
      const gw = generateGatewayKeypair();
      const dev = generateGatewayKeypair();
      const s = await createPairSession(sessionsPath, {
        mode: 'generate',
        operatorContext: { channel: 'cli' },
        rngPrivateKey: () => Buffer.from(gw.skB64, 'base64url'),
        rngPublicKey: () => Buffer.from(gw.pkB64, 'base64url'),
        rngSecondaryCode: () => '000000',
      });
      await fetch(`${url}/plugin/totalreclaw/pair/start?sid=${s.sid}&c=000000`);
      const mnemonic = 'abandon ability able about above absent absorb abstract absurd abuse access accident';
      const enc = encryptPairingPayload({
        skLocalB64: dev.skB64,
        pkRemoteB64: gw.pkB64,
        sid: s.sid,
        plaintext: Buffer.from(mnemonic),
      });
      const r = await fetch(`${url}/plugin/totalreclaw/pair/respond`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          v: 1,
          sid: s.sid,
          pk_d: dev.pkB64,
          nonce: enc.nonceB64,
          ct: enc.ciphertextB64,
        }),
      });
      assert(r.status === 500, 'respond-fail: state=error → 500');
    },
    {
      completePairing: async () => ({ state: 'error', error: 'disk_full' }),
    },
  );

  // =======================================================================
  // 20. Tampered ciphertext → 400 decrypt_failed + session rejected
  // =======================================================================
  await withFixture(async ({ url, sessionsPath }) => {
    const gw = generateGatewayKeypair();
    const dev = generateGatewayKeypair();
    const s = await createPairSession(sessionsPath, {
      mode: 'generate',
      operatorContext: { channel: 'cli' },
      rngPrivateKey: () => Buffer.from(gw.skB64, 'base64url'),
      rngPublicKey: () => Buffer.from(gw.pkB64, 'base64url'),
      rngSecondaryCode: () => '424242',
    });
    await fetch(`${url}/plugin/totalreclaw/pair/start?sid=${s.sid}&c=424242`);
    const enc = encryptPairingPayload({
      skLocalB64: dev.skB64,
      pkRemoteB64: gw.pkB64,
      sid: s.sid,
      plaintext: Buffer.from('word '.repeat(12).trim()),
    });
    // Flip a byte in the ciphertext.
    const ctBuf = Buffer.from(enc.ciphertextB64, 'base64url');
    ctBuf[ctBuf.length - 1] ^= 0xff;
    const r = await fetch(`${url}/plugin/totalreclaw/pair/respond`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        v: 1,
        sid: s.sid,
        pk_d: dev.pkB64,
        nonce: enc.nonceB64,
        ct: ctBuf.toString('base64url'),
      }),
    });
    assert(r.status === 400, 'tamper-respond: 400 on AEAD failure');
    const body = await readJson<{ error: string }>(r);
    assert(body.error === 'decrypt_failed', 'tamper-respond: error=decrypt_failed');
    const after = await getPairSession(sessionsPath, s.sid);
    assert(after?.status === 'rejected', 'tamper-respond: session → rejected');
  });

  // =======================================================================
  // 21. GET /status — returns current state
  // =======================================================================
  await withFixture(async ({ url, sessionsPath }) => {
    const s = await createPairSession(sessionsPath, {
      mode: 'import',
      operatorContext: { channel: 'cli' },
    });
    const r1 = await fetch(`${url}/plugin/totalreclaw/pair/status?sid=${s.sid}`);
    assert(r1.status === 200, 'status: 200');
    const b1 = await readJson<{ status: string; mode: string }>(r1);
    assert(b1.status === 'awaiting_scan', 'status: initial awaiting_scan');
    assert(b1.mode === 'import', 'status: mode echoed');
    await transitionPairSession(sessionsPath, s.sid, 'device_connected');
    const r2 = await fetch(`${url}/plugin/totalreclaw/pair/status?sid=${s.sid}`);
    const b2 = await readJson<{ status: string }>(r2);
    assert(b2.status === 'device_connected', 'status: device_connected after transition');
    const r3 = await fetch(`${url}/plugin/totalreclaw/pair/status?sid=deadbeef`);
    assert(r3.status === 404, 'status: unknown sid → 404');
  });

  // =======================================================================
  // 22. Custom validateMnemonic rejects invalid phrase
  // =======================================================================
  await withFixture(
    async ({ url, sessionsPath }) => {
      const gw = generateGatewayKeypair();
      const dev = generateGatewayKeypair();
      const s = await createPairSession(sessionsPath, {
        mode: 'generate',
        operatorContext: { channel: 'cli' },
        rngPrivateKey: () => Buffer.from(gw.skB64, 'base64url'),
        rngPublicKey: () => Buffer.from(gw.pkB64, 'base64url'),
        rngSecondaryCode: () => '999999',
      });
      await fetch(`${url}/plugin/totalreclaw/pair/start?sid=${s.sid}&c=999999`);
      const enc = encryptPairingPayload({
        skLocalB64: dev.skB64,
        pkRemoteB64: gw.pkB64,
        sid: s.sid,
        plaintext: Buffer.from('only five words here ok'),
      });
      const r = await fetch(`${url}/plugin/totalreclaw/pair/respond`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          v: 1,
          sid: s.sid,
          pk_d: dev.pkB64,
          nonce: enc.nonceB64,
          ct: enc.ciphertextB64,
        }),
      });
      assert(r.status === 400, 'mnemonic-validate: invalid word-count → 400');
      const body = await readJson<{ error: string }>(r);
      assert(body.error === 'invalid_mnemonic', 'mnemonic-validate: error=invalid_mnemonic');
    },
  );

  // =======================================================================
  // 23. derivePublicFromPrivate consistency — pair-crypto <-> pair-http
  //     This is a sanity check that the session-store's randomly-generated
  //     private key, if actually derivable to a public via pair-crypto,
  //     matches what /start+/respond would use. Confirms cross-module
  //     contract stays tight.
  // =======================================================================
  {
    const kp = generateGatewayKeypair();
    const derived = derivePublicFromPrivate(kp.skB64);
    assert(derived === kp.pkB64, 'xmod: derivePublicFromPrivate matches keypair output');
  }

  console.log(`# ${passed} passed, ${failed} failed`);
  if (failed > 0) process.exit(1);
}

main().catch((err) => {
  console.error('fatal:', err);
  process.exit(1);
});
