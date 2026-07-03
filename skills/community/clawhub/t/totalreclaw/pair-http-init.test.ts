/**
 * Tests for the in-process `/pair/init` HTTP route (3.3.14 — the
 * 30s-subprocess-kill 502 fix).
 *
 * Background
 * ----------
 * Through 3.3.13 the relay pair WebSocket was held by the `tr pair`
 * CLI subprocess. OpenClaw's shell tool kills subprocesses after 30s,
 * which tore down the WS mid-pair → the relay returned 502 on
 * /pair/respond when the user's browser tried to complete pairing
 * (every pair WS disconnected at exactly 30s in production relay logs).
 *
 * 3.3.14 moves the WS open + awaitPhraseUpload into the plugin's
 * in-process HTTP route handler (`GET /plugin/totalreclaw/pair/init`).
 * The WS now lives in the gateway process itself, immune to shell-tool
 * timeouts, retries, and SIGUSR1 reloads.
 *
 * What this test proves
 * ---------------------
 *   1. The bundle exposes `initPath` + `handlers.init` ONLY when
 *      `relayBaseUrl` is wired (back-compat for older callers).
 *   2. `handleInit` opens the relay WS in-process via the REAL
 *      `openRemotePairSession` (driven against a local WS stub that
 *      mirrors the relay's open/forward/ack protocol).
 *   3. The HTTP response returns immediately with `{v, sid, url, pin,
 *      mode, expires_at_ms}` — the agent reads these and surfaces
 *      URL+PIN to the user. The response is NOT blocked on the browser
 *      uploading the phrase.
 *   4. The background `awaitPhraseUpload` runs in-process: when the
 *      stub-relay pushes the encrypted forward frame, the gateway
 *      decrypts locally and invokes the injected `completePairing`
 *      callback with the mnemonic.
 *   5. Full end-to-end flow: init → WS opens → phrase arrives →
 *      completePairing called → ack sent.
 *   6. Error path: when the relay refuses the open frame, the route
 *      returns 502 relay_open_failed (no background task started).
 *
 * The relay stub here is a faithful re-implementation of the relay's
 * open/forward/ack protocol — the same one pair-remote-client.test.ts
 * uses. We re-implement it inline (rather than import) so this test
 * file stays self-contained and the failure modes are obvious.
 *
 * Run with: npx tsx pair-http-init.test.ts
 */

import { createServer, type Server as HttpServer } from 'node:http';
import { AddressInfo } from 'node:net';
import http from 'node:http';

import { WebSocketServer, WebSocket } from 'ws';

import { buildPairRoutes, type PairLogger } from './pair-http.js';
import {
  encryptPairingPayload,
  generateGatewayKeypair,
} from './pair-crypto.js';

// ---------------------------------------------------------------------------
// Tap-style harness (matches the rest of this plugin's test style)
// ---------------------------------------------------------------------------

let _passed = 0;
let _failed = 0;
let _seq = 0;
function ok(name: string, cond: boolean, detail?: string): void {
  const status = cond ? 'ok' : 'fail';
  const tail = detail ? ` -- ${detail}` : '';
  _seq += 1;
  // eslint-disable-next-line no-console
  console.log(`${status} ${_seq} - ${name}${tail}`);
  if (cond) _passed += 1;
  else _failed += 1;
}

const TEST_PHRASE =
  'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about';

const silentLogger: PairLogger = {
  info() {},
  warn() {},
  error() {},
};

// ---------------------------------------------------------------------------
// Relay stub — mirrors the relay's open/forward/ack WebSocket protocol
// ---------------------------------------------------------------------------

interface RelayStub {
  wssUrl: string;
  /** Last frame received from the gateway (the `open` frame). */
  lastGatewayFrame: () => Record<string, unknown> | null;
  /** Resolves 'ack' / 'nack' / 'closed' when the gateway replies. */
  awaitAck: () => Promise<'ack' | 'nack' | 'closed'>;
  close: () => Promise<void>;
}

async function startRelayStub(opts: {
  token?: string;
  phrase?: string;
  errorOnOpen?: string;
  forwardAfterMs?: number;
} = {}): Promise<RelayStub> {
  const token = opts.token ?? 'inittoken123456';
  const expiresAt = new Date(Date.now() + 5 * 60_000).toISOString();
  const phrase = opts.phrase ?? TEST_PHRASE;
  const forwardDelay = opts.forwardAfterMs ?? 10;

  const httpServer: HttpServer = createServer();
  const wss = new WebSocketServer({ server: httpServer });

  let lastFrame: Record<string, unknown> | null = null;
  let ackResolver: ((v: 'ack' | 'nack' | 'closed') => void) | null = null;
  const ackPromise: Promise<'ack' | 'nack' | 'closed'> = new Promise(
    (resolve) => {
      ackResolver = resolve;
    },
  );

  wss.on('connection', (ws) => {
    ws.on('message', async (raw) => {
      try {
        const text =
          typeof raw === 'string'
            ? raw
            : Buffer.from(raw as ArrayBuffer).toString('utf-8');
        const msg = JSON.parse(text) as Record<string, unknown>;
        lastFrame = msg;

        if (msg.type === 'open') {
          if (opts.errorOnOpen) {
            ws.send(JSON.stringify({ type: 'error', error: opts.errorOnOpen }));
            return;
          }
          ws.send(
            JSON.stringify({
              type: 'opened',
              token,
              short_url: `/pair/p/${token}`,
              expires_at: expiresAt,
            }),
          );
          // Simulate the browser uploading the encrypted phrase.
          setTimeout(() => {
            const gatewayPubkey = String(msg.gateway_pubkey);
            const deviceKp = generateGatewayKeypair();
            const { nonceB64, ciphertextB64 } = encryptPairingPayload({
              skLocalB64: deviceKp.skB64,
              pkRemoteB64: gatewayPubkey,
              sid: token,
              plaintext: Buffer.from(phrase, 'utf-8'),
            });
            ws.send(
              JSON.stringify({
                type: 'forward',
                client_pubkey: deviceKp.pkB64,
                nonce: nonceB64,
                ciphertext: ciphertextB64,
              }),
            );
          }, forwardDelay);
          return;
        }
        if (msg.type === 'ack' || msg.type === 'nack') {
          ackResolver?.(msg.type as 'ack' | 'nack');
          ackResolver = null;
          try {
            ws.close();
          } catch {
            /* noop */
          }
          return;
        }
      } catch (err) {
        // eslint-disable-next-line no-console
        console.error('relay-stub: message handler error', err);
      }
    });
    ws.on('close', () => {
      if (ackResolver) {
        ackResolver('closed');
        ackResolver = null;
      }
    });
  });

  await new Promise<void>((resolve) => {
    httpServer.listen(0, '127.0.0.1', () => resolve());
  });
  const addr = httpServer.address() as AddressInfo;
  return {
    wssUrl: `ws://127.0.0.1:${addr.port}`,
    lastGatewayFrame: () => lastFrame,
    awaitAck: () => ackPromise,
    close: () =>
      new Promise<void>((resolve) => {
        try {
          wss.close(() => {
            httpServer.close(() => resolve());
          });
        } catch {
          resolve();
        }
      }),
  };
}

// ---------------------------------------------------------------------------
// HTTP test client — drives the registered route handler via a real
// http.Server so the handler runs through the real IncomingMessage /
// ServerResponse contract (same harness pair-http.test.ts uses).
// ---------------------------------------------------------------------------

function startRouteServer(
  handler: http.RequestListener,
): Promise<{ url: string; close: () => Promise<void> }> {
  const server = http.createServer(async (req, res) => {
    try {
      await handler(req, res);
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
      resolve({
        url: `http://127.0.0.1:${addr.port}`,
        close: () =>
          new Promise<void>((r) => server.close(() => r())),
      });
    });
  });
}

async function httpGet(url: string): Promise<{ status: number; body: unknown }> {
  return new Promise((resolve, reject) => {
    http
      .get(url, (res) => {
        const chunks: Buffer[] = [];
        res.on('data', (c) => chunks.push(c));
        res.on('end', () => {
          const raw = Buffer.concat(chunks).toString('utf-8');
          try {
            resolve({ status: res.statusCode ?? 0, body: JSON.parse(raw) });
          } catch {
            resolve({ status: res.statusCode ?? 0, body: raw });
          }
        });
      })
      .on('error', reject);
  });
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

async function testInitPathAbsentWithoutRelayUrl(): Promise<void> {
  const bundle = buildPairRoutes({
    sessionsPath: '/dev/null',
    apiBase: '/plugin/totalreclaw/pair',
    logger: silentLogger,
    validateMnemonic: () => true,
    completePairing: async () => ({ state: 'active' }),
    // No relayBaseUrl → init route MUST be absent (back-compat).
  });
  ok(
    'no-relay: initPath is undefined when relayBaseUrl omitted',
    bundle.initPath === undefined,
  );
  ok(
    'no-relay: handlers.init is undefined when relayBaseUrl omitted',
    bundle.handlers.init === undefined,
  );
  // The original 4 routes are still present.
  ok(
    'no-relay: finish/start/respond/status still present',
    !!bundle.finishPath &&
      !!bundle.startPath &&
      !!bundle.respondPath &&
      !!bundle.statusPath,
  );
}

async function testInitHappyPath(): Promise<void> {
  const stub = await startRelayStub({ token: 'happytoken1234' });
  const server = await startRouteServer(
    // The handler is async; the route server awaits it.
    // eslint-disable-next-line @typescript-eslint/no-misused-promises
    (async (req, res) => {
      // buildPairRoutes returns a bundle; we invoke handlers.init directly.
      const bundle = buildPairRoutes({
        sessionsPath: '/dev/null',
        apiBase: '/plugin/totalreclaw/pair',
        logger: silentLogger,
        relayBaseUrl: stub.wssUrl,
        initPairMode: 'either',
        initWebSocketImpl: WebSocket,
        validateMnemonic: () => true,
        completePairing: async ({ mnemonic }) => {
          ok(
            'happy: completePairing received 12-word phrase',
            mnemonic.split(' ').length === 12 && mnemonic === TEST_PHRASE,
            `len=${mnemonic.split(' ').length}`,
          );
          return { state: 'active', accountId: '0xinitface' };
        },
      });
      const init = bundle.handlers.init;
      if (!init) throw new Error('init handler missing');
      await init(req, res);
    }) as unknown as http.RequestListener,
  );

  try {
    // 1. Hit the /init route. The handler opens the relay WS in-process
    //    and returns the URL+PIN immediately.
    const { status, body } = await httpGet(`${server.url}/plugin/totalreclaw/pair/init`);

    ok('happy: HTTP 200', status === 200, `status=${status}`);

    const payload = body as Record<string, unknown>;
    ok('happy: v=1', payload.v === 1);
    ok(
      'happy: sid is the relay token',
      payload.sid === 'happytoken1234',
      `sid=${payload.sid}`,
    );
    ok(
      'happy: url contains the token',
      typeof payload.url === 'string' && payload.url.includes('/pair/p/happytoken1234'),
      `url=${payload.url}`,
    );
    ok(
      'happy: url carries #pk= fragment',
      typeof payload.url === 'string' && /#pk=[A-Za-z0-9_-]{40,48}$/.test(payload.url),
      `url=${payload.url}`,
    );
    ok(
      'happy: pin is a 6-digit string',
      typeof payload.pin === 'string' && /^\d{6}$/.test(payload.pin),
      `pin=${payload.pin}`,
    );
    ok('happy: mode is either', payload.mode === 'either');
    ok(
      'happy: expires_at_ms is a finite number in the future',
      typeof payload.expires_at_ms === 'number' &&
        Number.isFinite(payload.expires_at_ms) &&
        payload.expires_at_ms > Date.now(),
      `expires_at_ms=${payload.expires_at_ms}`,
    );

    // 2. The open frame reached the stub-relay with the right shape.
    const openFrame = stub.lastGatewayFrame();
    ok(
      'happy: open frame has correct shape',
      !!openFrame &&
        openFrame.type === 'open' &&
        typeof openFrame.gateway_pubkey === 'string' &&
        typeof openFrame.pin === 'string' &&
        openFrame.mode === 'either',
      JSON.stringify(openFrame),
    );

    // 3. The background awaitPhraseUpload resolved: the gateway decrypted
    //    the forward frame and called completePairing (assertions inside
    //    the callback fire during the wait). Wait for the ack to land at
    //    the stub to confirm the full round-trip completed.
    const ack = await stub.awaitAck();
    ok('happy: gateway sent ack to relay', ack === 'ack', `ack=${ack}`);
  } finally {
    await server.close();
    await stub.close();
  }
}

async function testInitRelayOpenFailure(): Promise<void> {
  const stub = await startRelayStub({ errorOnOpen: 'relay_full' });
  const server = await startRouteServer(
    // eslint-disable-next-line @typescript-eslint/no-misused-promises
    (async (req, res) => {
      const bundle = buildPairRoutes({
        sessionsPath: '/dev/null',
        apiBase: '/plugin/totalreclaw/pair',
        logger: silentLogger,
        relayBaseUrl: stub.wssUrl,
        initWebSocketImpl: WebSocket,
        validateMnemonic: () => true,
        completePairing: async () => {
          ok('relay-fail: completePairing SHOULD NOT be called', false);
          return { state: 'error', error: 'should_not_reach' };
        },
      });
      const init = bundle.handlers.init;
      if (!init) throw new Error('init handler missing');
      await init(req, res);
    }) as unknown as http.RequestListener,
  );

  try {
    const { status, body } = await httpGet(`${server.url}/plugin/totalreclaw/pair/init`);
    ok(
      'relay-fail: HTTP 502 on relay_open_failed',
      status === 502,
      `status=${status}`,
    );
    const payload = body as Record<string, unknown>;
    ok(
      'relay-fail: error=relay_open_failed',
      payload.error === 'relay_open_failed',
      `error=${payload.error}`,
    );
    // Give the background task a moment in case it was incorrectly started;
    // the completePairing assertion above will fire if it runs.
    await new Promise((r) => setTimeout(r, 50));
  } finally {
    await server.close();
    await stub.close();
  }
}

async function testInitMethodNotAllowed(): Promise<void> {
  const bundle = buildPairRoutes({
    sessionsPath: '/dev/null',
    apiBase: '/plugin/totalreclaw/pair',
    logger: silentLogger,
    relayBaseUrl: 'ws://127.0.0.1:1', // never reached
    validateMnemonic: () => true,
    completePairing: async () => ({ state: 'active' }),
  });
  const init = bundle.handlers.init!;
  // Synthesize a POST request.
  const req = { method: 'POST', url: '/plugin/totalreclaw/pair/init' } as unknown as http.IncomingMessage;
  let ended = false;
  const res = {
    statusCode: 0,
    headersSent: false,
    setHeader() {},
    end(body: unknown) {
      ended = true;
      // Capture the body for assertion.
      (res as { _body?: unknown })._body = body;
    },
  } as unknown as http.ServerResponse;
  await init(req, res);
  ok('method: POST → 405', (res as { statusCode: number }).statusCode === 405);
  ok('method: response ended', ended);
  const body = (res as { _body?: string })._body as string;
  ok('method: error=method_not_allowed', body.includes('method_not_allowed'), body);
}

// ---------------------------------------------------------------------------
// Run
// ---------------------------------------------------------------------------

async function main(): Promise<void> {
  await testInitPathAbsentWithoutRelayUrl();
  await testInitHappyPath();
  await testInitRelayOpenFailure();
  await testInitMethodNotAllowed();

  // eslint-disable-next-line no-console
  console.log(`# fail: ${_failed}`);
  // eslint-disable-next-line no-console
  console.log(`# ${_passed}/${_passed + _failed} passed`);
  if (_failed > 0) {
    // eslint-disable-next-line no-console
    console.log('SOME TESTS FAILED');
    process.exit(1);
  }
  // eslint-disable-next-line no-console
  console.log('ALL TESTS PASSED');
}

main().catch((err) => {
  // eslint-disable-next-line no-console
  console.error('test harness crashed:', err);
  process.exit(1);
});
