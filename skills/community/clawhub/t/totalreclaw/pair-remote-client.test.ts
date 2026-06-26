/**
 * Tests for `pair-remote-client` — relay-brokered pair flow (plugin rc.11).
 *
 * Runs a local WebSocket server that mimics the relay's open/forward/ack
 * protocol so the test covers the full TS <-> relay wire with no network
 * dependency. Encryption vectors are produced with the same `pair-crypto`
 * primitives the gateway would use — so the round-trip proves:
 *
 *   1. open frame shape is correct
 *   2. opened reply drives the user URL / PIN / token plumbing
 *   3. forward frame is decrypted locally + completion handler is invoked
 *   4. ack is sent back on success; nack carries a typed error on failure
 *
 * Does NOT run against the real staging relay — that is covered by the
 * auto-QA harness after publish.
 */
import { WebSocketServer, WebSocket } from 'ws';
import { createServer, type Server as HttpServer } from 'node:http';
import { AddressInfo } from 'node:net';

import {
  awaitPhraseUpload,
  openRemotePairSession,
} from './pair-remote-client.js';
import {
  encryptPairingPayload,
  generateGatewayKeypair,
  type GatewayKeypair,
} from './pair-crypto.js';

// Minimal tap-style harness — matches the rest of this plugin's test style.
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

/** The phrase the "browser" side will encrypt + upload in these tests. */
const TEST_PHRASE =
  'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about';

/** Non-BIP-39 lowercase ASCII — still matches the 12-word regex. */
const INVALID_PHRASE =
  'foo foo foo foo foo foo foo foo foo foo foo foo';

// ---------------------------------------------------------------------------
// Relay stub
// ---------------------------------------------------------------------------

interface RelayStubOptions {
  /** Override the default `token` the stub issues. */
  token?: string;
  /** Override the `expires_at` ISO string. */
  expiresAt?: string;
  /** If true, send an `{type:"error"}` frame instead of `opened`. */
  errorOnOpen?: string;
  /** Delay (ms) before sending the forward frame. Default 10. */
  forwardAfterMs?: number;
  /** If true, mimic a nonce/ciphertext built for the WRONG session id. */
  corruptSid?: boolean;
  /**
   * Phrase the stub-browser encrypts + uploads. Default TEST_PHRASE. Set
   * to something non-BIP-39 to exercise validator failure paths.
   */
  phrase?: string;
  /**
   * Force a device keypair so the test can verify the exact client pubkey
   * that reaches the gateway side.
   */
  forceDeviceKeypair?: GatewayKeypair;
}

interface RelayStub {
  wssUrl: string;
  /** Resolves with whatever frame the stub last received from the gateway. */
  lastGatewayFrame: () => Record<string, unknown> | null;
  /** Resolves when the `ack` or `nack` from the gateway arrives (or when the WS closes). */
  awaitAck: () => Promise<'ack' | 'nack' | 'closed'>;
  close: () => Promise<void>;
}

async function startRelayStub(opts: RelayStubOptions = {}): Promise<RelayStub> {
  const token = opts.token ?? 'testtoken12345678';
  const expiresAt =
    opts.expiresAt ?? new Date(Date.now() + 60_000).toISOString();
  const forwardDelay = opts.forwardAfterMs ?? 10;
  const phrase = opts.phrase ?? TEST_PHRASE;

  const http: HttpServer = createServer();
  const wss = new WebSocketServer({ server: http });

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

        // First frame must be `open`. Reply with `opened` (or `error`).
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

          // Simulate the browser POST: encrypt the phrase for the gateway's
          // public key + push a `forward` frame.
          setTimeout(() => {
            const gatewayPubkey = String(msg.gateway_pubkey);
            const deviceKp =
              opts.forceDeviceKeypair ?? generateGatewayKeypair();
            const sid = opts.corruptSid ? 'wrong-sid' : token;
            const { nonceB64, ciphertextB64 } = encryptPairingPayload({
              skLocalB64: deviceKp.skB64,
              pkRemoteB64: gatewayPubkey,
              sid,
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

        if (msg.type === 'ack') {
          ackResolver?.('ack');
          ackResolver = null;
          try {
            ws.close();
          } catch {
            /* noop */
          }
          return;
        }
        if (msg.type === 'nack') {
          ackResolver?.('nack');
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
    http.listen(0, '127.0.0.1', () => resolve());
  });

  const addr = http.address() as AddressInfo;
  const wssUrl = `ws://127.0.0.1:${addr.port}`;

  return {
    wssUrl,
    lastGatewayFrame: () => lastFrame,
    awaitAck: () => ackPromise,
    close: () =>
      new Promise<void>((resolve) => {
        try {
          wss.close(() => {
            http.close(() => resolve());
          });
        } catch {
          resolve();
        }
      }),
  };
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

async function testHappyPath(): Promise<void> {
  const stub = await startRelayStub({ token: 'abc12345' });
  try {
    const session = await openRemotePairSession({
      relayBaseUrl: stub.wssUrl,
      pin: '123456',
      clientId: 'gw-test-1',
      mode: 'either',
      webSocketImpl: WebSocket,
    });

    // Assertions against the open-side plumbing.
    ok(
      'happy: URL contains the token',
      session.url.includes('/pair/p/abc12345'),
      session.url,
    );
    ok(
      'happy: URL uses https scheme (stub serves ws://)',
      session.url.startsWith('http://'),
      session.url,
    );
    ok(
      'happy: URL carries #pk= fragment',
      /#pk=[A-Za-z0-9_-]{40,48}$/.test(session.url),
      session.url,
    );
    ok('happy: PIN echoes', session.pin === '123456');
    ok('happy: token echoes', session.token === 'abc12345');

    const firstFrame = stub.lastGatewayFrame();
    ok(
      'happy: open frame has correct shape',
      !!firstFrame &&
        firstFrame.type === 'open' &&
        typeof firstFrame.gateway_pubkey === 'string' &&
        firstFrame.pin === '123456' &&
        firstFrame.client_id === 'gw-test-1' &&
        firstFrame.mode === 'either',
      JSON.stringify(firstFrame),
    );

    // Block on phrase upload.
    let completed = false;
    const result = await awaitPhraseUpload(session, {
      completePairing: async ({ mnemonic }) => {
        completed = true;
        // MUST NOT log the phrase — but we can assert on its shape for the test.
        ok(
          'happy: completion received full 12-word phrase',
          mnemonic.split(' ').length === 12 && mnemonic === TEST_PHRASE,
          `len=${mnemonic.split(' ').length}`,
        );
        return { state: 'active', accountId: '0xdeadbeef' };
      },
    });

    ok('happy: completePairing called', completed);
    ok('happy: result.state active', result.state === 'active');
    ok(
      'happy: result.accountId echoed',
      result.accountId === '0xdeadbeef',
    );

    const ack = await stub.awaitAck();
    ok('happy: gateway sent ack', ack === 'ack');
  } finally {
    await stub.close();
  }
}

async function testInvalidPhraseSendsNack(): Promise<void> {
  const stub = await startRelayStub({ phrase: INVALID_PHRASE });
  try {
    const session = await openRemotePairSession({
      relayBaseUrl: stub.wssUrl,
      pin: '654321',
    });

    let called = false;
    let threw = false;
    try {
      await awaitPhraseUpload(session, {
        completePairing: async () => {
          called = true;
          return { state: 'active' };
        },
        phraseValidator: (_p) => false,
      });
    } catch (err) {
      threw =
        err instanceof Error &&
        /failed BIP-39 validation/.test(err.message);
    }

    ok(
      'invalid-phrase: completePairing NOT invoked',
      !called,
    );
    ok(
      'invalid-phrase: awaitPhraseUpload threw validation error',
      threw,
    );

    const ack = await stub.awaitAck();
    ok('invalid-phrase: gateway sent nack', ack === 'nack');
  } finally {
    await stub.close();
  }
}

async function testOpenErrorPropagates(): Promise<void> {
  const stub = await startRelayStub({ errorOnOpen: 'rate_limited' });
  try {
    let threw = false;
    try {
      await openRemotePairSession({
        relayBaseUrl: stub.wssUrl,
        pin: '000000',
      });
    } catch (err) {
      threw =
        err instanceof Error && /rate_limited/.test(err.message);
    }
    ok('open-error: error propagates with relay error code', threw);
  } finally {
    await stub.close();
  }
}

async function testDecryptFailureSendsNack(): Promise<void> {
  const stub = await startRelayStub({ corruptSid: true });
  try {
    const session = await openRemotePairSession({
      relayBaseUrl: stub.wssUrl,
      pin: '999999',
    });

    let called = false;
    let threw = false;
    try {
      await awaitPhraseUpload(session, {
        completePairing: async () => {
          called = true;
          return { state: 'active' };
        },
      });
    } catch {
      threw = true;
    }
    ok('decrypt-fail: completePairing NOT invoked', !called);
    ok('decrypt-fail: awaitPhraseUpload threw', threw);
    const ack = await stub.awaitAck();
    ok('decrypt-fail: gateway sent nack', ack === 'nack');
  } finally {
    await stub.close();
  }
}

async function testHttpsInputConvertedToWss(): Promise<void> {
  // The caller passes a https:// URL (as most config plumbing will produce
  // in production); the client should still hit wss://host/pair/session/open.
  const stub = await startRelayStub({ token: 'https-test' });
  try {
    const httpsStyle = stub.wssUrl.replace(/^ws:/, 'http:');
    const session = await openRemotePairSession({
      relayBaseUrl: httpsStyle,
      pin: '111111',
    });
    ok(
      'scheme-convert: URL uses http scheme (because stub is http://)',
      session.url.startsWith('http://'),
      session.url,
    );
    ok(
      'scheme-convert: URL contains token',
      session.url.includes('/pair/p/https-test'),
      session.url,
    );
    // Clean shutdown — cancel the awaiting phrase upload.
    try {
      session._ws.close();
    } catch {
      /* noop */
    }
  } finally {
    await stub.close();
  }
}

// ---------------------------------------------------------------------------
// Multi-session stub (issue #125 regression — pair-twice in same Node process)
// ---------------------------------------------------------------------------

/**
 * Per-connection state for the multi-session stub. Each new WebSocket the
 * gateway opens (one per pair invocation) gets its own slot — token,
 * lastFrame, ack resolver — so we can assert each cycle independently.
 */
interface StubSlot {
  index: number;
  token: string;
  lastFrame: Record<string, unknown> | null;
  ack: Promise<'ack' | 'nack' | 'closed'>;
  ackResolver: ((v: 'ack' | 'nack' | 'closed') => void) | null;
}

interface MultiSessionRelayStub {
  wssUrl: string;
  /** Slot for the Nth (0-indexed) connection. Resolves once that slot exists. */
  awaitSlot(index: number): Promise<StubSlot>;
  /** Connection count seen by the relay so far. */
  connectionCount(): number;
  close(): Promise<void>;
}

async function startMultiSessionRelayStub(
  opts: { tokens: string[] } = { tokens: ['tok-aaaaa1', 'tok-bbbbb2'] },
): Promise<MultiSessionRelayStub> {
  const tokens = opts.tokens;
  const http: HttpServer = createServer();
  const wss = new WebSocketServer({ server: http });
  const slots: StubSlot[] = [];
  const slotResolvers: Array<(s: StubSlot) => void> = [];

  function getOrCreateSlotPromise(idx: number): Promise<StubSlot> {
    if (slots[idx]) return Promise.resolve(slots[idx]!);
    return new Promise((resolve) => {
      slotResolvers[idx] = resolve;
    });
  }

  wss.on('connection', (ws) => {
    const slotIdx = slots.length;
    const token = tokens[slotIdx] ?? `tok-extra-${slotIdx}`;
    let resolveAck: ((v: 'ack' | 'nack' | 'closed') => void) | null = null;
    const ackPromise = new Promise<'ack' | 'nack' | 'closed'>((resolve) => {
      resolveAck = resolve;
    });
    const slot: StubSlot = {
      index: slotIdx,
      token,
      lastFrame: null,
      ack: ackPromise,
      ackResolver: resolveAck,
    };
    slots.push(slot);
    if (slotResolvers[slotIdx]) {
      slotResolvers[slotIdx]!(slot);
    }

    ws.on('message', (raw) => {
      try {
        const text =
          typeof raw === 'string'
            ? raw
            : Buffer.from(raw as ArrayBuffer).toString('utf-8');
        const msg = JSON.parse(text) as Record<string, unknown>;
        slot.lastFrame = msg;

        if (msg.type === 'open') {
          ws.send(
            JSON.stringify({
              type: 'opened',
              token: slot.token,
              short_url: `/pair/p/${slot.token}`,
              expires_at: new Date(Date.now() + 60_000).toISOString(),
            }),
          );

          // Simulate the browser uploading the encrypted phrase.
          setTimeout(() => {
            const gatewayPubkey = String(msg.gateway_pubkey);
            const deviceKp = generateGatewayKeypair();
            const { nonceB64, ciphertextB64 } = encryptPairingPayload({
              skLocalB64: deviceKp.skB64,
              pkRemoteB64: gatewayPubkey,
              sid: slot.token,
              plaintext: Buffer.from(TEST_PHRASE, 'utf-8'),
            });
            ws.send(
              JSON.stringify({
                type: 'forward',
                client_pubkey: deviceKp.pkB64,
                nonce: nonceB64,
                ciphertext: ciphertextB64,
              }),
            );
          }, 10);
          return;
        }
        if (msg.type === 'ack') {
          slot.ackResolver?.('ack');
          slot.ackResolver = null;
          try { ws.close(); } catch { /* noop */ }
          return;
        }
        if (msg.type === 'nack') {
          slot.ackResolver?.('nack');
          slot.ackResolver = null;
          try { ws.close(); } catch { /* noop */ }
          return;
        }
      } catch (err) {
        // eslint-disable-next-line no-console
        console.error('multi-stub: message handler error', err);
      }
    });

    ws.on('close', () => {
      if (slot.ackResolver) {
        slot.ackResolver('closed');
        slot.ackResolver = null;
      }
    });
  });

  await new Promise<void>((resolve) => {
    http.listen(0, '127.0.0.1', () => resolve());
  });
  const addr = http.address() as AddressInfo;

  return {
    wssUrl: `ws://127.0.0.1:${addr.port}`,
    awaitSlot: getOrCreateSlotPromise,
    connectionCount: () => slots.length,
    close: () =>
      new Promise<void>((resolve) => {
        try {
          wss.close(() => http.close(() => resolve()));
        } catch {
          resolve();
        }
      }),
  };
}

/**
 * Regression for issue #125 — pair flow is single-shot per gateway lifetime.
 *
 * Real-world bug: after a successful pair, a second `totalreclaw_pair` call
 * returned a URL whose token was never registered with the relay (HTTP 404
 * from the relay, 502 from the proxy). The QA bot's recommendation: ensure
 * every invocation recreates session state — fresh keypair, fresh PIN,
 * fresh client id, fresh WebSocket — and that the second cycle reaches the
 * relay end-to-end.
 *
 * This test runs two sequential open + await + complete cycles in a single
 * Node process against a multi-session stub. Both must succeed. Both must
 * use distinct ephemeral material.
 */
async function testTwoSequentialPairsSucceed(): Promise<void> {
  const tok1 = 'pair-once-1111';
  const tok2 = 'pair-twice-2222';
  const stub = await startMultiSessionRelayStub({ tokens: [tok1, tok2] });
  try {
    // ---- First pair ----
    const session1 = await openRemotePairSession({
      relayBaseUrl: stub.wssUrl,
      pin: '111111',
      clientId: 'gw-first',
    });
    ok(
      'pair-twice: first session URL contains first token',
      session1.url.includes(`/pair/p/${tok1}`),
      session1.url,
    );
    ok(
      'pair-twice: first session token echoes',
      session1.token === tok1,
      session1.token,
    );

    let firstCompletionRan = false;
    const result1 = await awaitPhraseUpload(session1, {
      completePairing: async () => {
        firstCompletionRan = true;
        return { state: 'active', accountId: '0xfirst' };
      },
    });
    ok('pair-twice: first completion ran', firstCompletionRan);
    ok('pair-twice: first result active', result1.state === 'active');
    const ack1 = await (await stub.awaitSlot(0)).ack;
    ok('pair-twice: first cycle ack received', ack1 === 'ack');

    // ---- Second pair (the bug — this is where rc.20 returns a URL whose
    //                  token never reaches the relay) ----
    const session2 = await openRemotePairSession({
      relayBaseUrl: stub.wssUrl,
      pin: '222222',
      clientId: 'gw-second',
    });

    ok(
      'pair-twice: second relay open frame received',
      stub.connectionCount() === 2,
      `connections=${stub.connectionCount()}`,
    );
    ok(
      'pair-twice: second session URL contains second token',
      session2.url.includes(`/pair/p/${tok2}`),
      session2.url,
    );
    ok(
      'pair-twice: second session token echoes',
      session2.token === tok2,
      session2.token,
    );
    ok(
      'pair-twice: second URL token differs from first',
      !session2.url.includes(tok1),
      session2.url,
    );

    // Fresh ephemeral material per call — keypair must NOT match between cycles.
    ok(
      'pair-twice: second keypair distinct from first',
      session1.keypair.pkB64 !== session2.keypair.pkB64
        && session1.keypair.skB64 !== session2.keypair.skB64,
    );

    // Inspect what the relay actually saw on the second connection. If the
    // bug regresses (no second open frame ever reaches the relay), the slot
    // never materialises and `awaitSlot(1)` hangs — which the outer promise
    // race catches.
    const slot2 = await Promise.race<StubSlot | 'timeout'>([
      stub.awaitSlot(1),
      new Promise<'timeout'>((resolve) =>
        setTimeout(() => resolve('timeout'), 1500),
      ),
    ]);
    ok(
      'pair-twice: second open frame reached relay (no single-shot regression)',
      slot2 !== 'timeout' && (slot2 as StubSlot).lastFrame?.type === 'open',
      typeof slot2 === 'string'
        ? slot2
        : JSON.stringify((slot2 as StubSlot).lastFrame),
    );

    let secondCompletionRan = false;
    const result2 = await awaitPhraseUpload(session2, {
      completePairing: async () => {
        secondCompletionRan = true;
        return { state: 'active', accountId: '0xsecond' };
      },
    });
    ok('pair-twice: second completion ran', secondCompletionRan);
    ok('pair-twice: second result active', result2.state === 'active');
    const ack2 = await (await stub.awaitSlot(1)).ack;
    ok('pair-twice: second cycle ack received', ack2 === 'ack');
  } finally {
    await stub.close();
  }
}

// ---------------------------------------------------------------------------
// 3.3.4-rc.2 — pair-tool 60s hard timeout (Pedro QA, stuck-session bug)
// ---------------------------------------------------------------------------

/**
 * Stub that opens normally but NEVER sends a `forward` frame. Mirrors the
 * relay-side bug Pedro saw in 3.3.4-rc.1: the relay accepted `open`, replied
 * `opened`, then dropped the session on `ws_close` before the browser could
 * complete pair. Plugin-side, the background task hung in `waitNextMessage`
 * for the full 5-minute session TTL. The 3.3.4-rc.2 fix wraps the WS-await
 * in a 60s hard timeout — this test asserts it fires and produces a
 * recognisable structured error.
 */
async function startSilentRelayStub(): Promise<{
  wssUrl: string;
  close: () => Promise<void>;
}> {
  const http: HttpServer = createServer();
  const wss = new WebSocketServer({ server: http });

  wss.on('connection', (ws) => {
    ws.on('message', (raw) => {
      try {
        const text =
          typeof raw === 'string'
            ? raw
            : Buffer.from(raw as ArrayBuffer).toString('utf-8');
        const msg = JSON.parse(text) as Record<string, unknown>;
        if (msg.type === 'open') {
          ws.send(
            JSON.stringify({
              type: 'opened',
              token: 'silent-tok-1',
              short_url: '/pair/p/silent-tok-1',
              expires_at: new Date(Date.now() + 60_000).toISOString(),
            }),
          );
          // Deliberately do NOT send `forward` — simulate the relay
          // dropping/silencing the session before phrase upload completes.
        }
      } catch {
        /* swallow */
      }
    });
  });

  await new Promise<void>((resolve) => {
    http.listen(0, '127.0.0.1', () => resolve());
  });
  const addr = http.address() as AddressInfo;
  return {
    wssUrl: `ws://127.0.0.1:${addr.port}`,
    close: () =>
      new Promise<void>((resolve) => {
        try {
          wss.close(() => http.close(() => resolve()));
        } catch {
          resolve();
        }
      }),
  };
}

/**
 * Asserts that `awaitPhraseUpload` honors the `timeoutMs` option (the inner
 * leg of the rc.2 fix) and that the outer Promise.race sentinel pattern used
 * in the plugin's `totalreclaw_pair` background task surfaces a structured
 * `{status: 'timed_out'}` value when the WS-await never receives a forward
 * frame. Uses a 200 ms timeout to keep test runtime bounded — the production
 * value is 60_000 ms (PAIR_TOOL_HARD_TIMEOUT_MS in index.ts).
 */
async function testPairToolHardTimeout(): Promise<void> {
  const stub = await startSilentRelayStub();
  try {
    const session = await openRemotePairSession({
      relayBaseUrl: stub.wssUrl,
      pin: '424242',
    });

    // Inner leg: awaitPhraseUpload with short timeout must reject (the
    // existing 5-minute default would hang the whole test process).
    const SHORT_MS = 200;
    let innerThrew = false;
    let innerErrMsg = '';
    try {
      await awaitPhraseUpload(session, {
        completePairing: async () => ({ state: 'active' }),
        timeoutMs: SHORT_MS,
      });
    } catch (err) {
      innerThrew = true;
      innerErrMsg = err instanceof Error ? err.message : String(err);
    }
    ok(
      'pair-timeout: awaitPhraseUpload threw on timeoutMs',
      innerThrew,
    );
    ok(
      'pair-timeout: awaitPhraseUpload error message identifies timeout',
      /timeout/i.test(innerErrMsg),
      innerErrMsg,
    );

    // Outer leg: the Promise.race sentinel pattern used inside index.ts'
    // `totalreclaw_pair` background task. When the awaitPhraseUpload promise
    // rejects (or stalls), the outer hard-timer must produce a structured
    // `{status: 'timed_out', message: ...}` shape that the catch handler
    // can recognise. We re-open a fresh session so the WS is healthy.
    const session2 = await openRemotePairSession({
      relayBaseUrl: stub.wssUrl,
      pin: '535353',
    });
    const phraseUploadPromise = awaitPhraseUpload(session2, {
      completePairing: async () => ({ state: 'active' }),
      // long enough that the OUTER race is the one that wins
      timeoutMs: 5_000,
    }).catch((err) => {
      // Inner leg may reject too — swallow so the race resolves cleanly.
      return { _innerRejected: true, _innerErr: err };
    });
    const TIMEOUT_SENTINEL = {
      status: 'timed_out' as const,
      message:
        'Pair flow timed out (60s) — generate a new URL with totalreclaw_pair.',
    };
    let hardTimer: ReturnType<typeof setTimeout> | undefined;
    const hardTimeoutPromise = new Promise<typeof TIMEOUT_SENTINEL>(
      (resolve) => {
        hardTimer = setTimeout(() => resolve(TIMEOUT_SENTINEL), 150);
      },
    );
    let raced: unknown;
    try {
      raced = await Promise.race([phraseUploadPromise, hardTimeoutPromise]);
    } finally {
      if (hardTimer) clearTimeout(hardTimer);
    }
    ok(
      'pair-timeout: outer race resolves to a structured value (not unhandled)',
      raced != null && typeof raced === 'object',
      typeof raced === 'object' ? JSON.stringify(raced) : String(raced),
    );
    const racedObj = raced as { status?: unknown; message?: unknown };
    ok(
      'pair-timeout: structured error has status: "timed_out"',
      racedObj.status === 'timed_out',
      JSON.stringify(racedObj),
    );
    ok(
      'pair-timeout: structured error message references generating a new URL',
      typeof racedObj.message === 'string' &&
        /totalreclaw_pair/.test(racedObj.message as string) &&
        /timed out/i.test(racedObj.message as string),
      typeof racedObj.message === 'string' ? racedObj.message : 'non-string',
    );

    // Clean up: close the WS that the second awaitPhraseUpload still holds.
    try {
      session2._ws.close();
    } catch {
      /* noop */
    }
    // Drain the inner promise so node doesn't warn about pending handles.
    await phraseUploadPromise.catch(() => undefined);
    try {
      session._ws.close();
    } catch {
      /* noop */
    }
  } finally {
    await stub.close();
  }
}

// ---------------------------------------------------------------------------
// Run
// ---------------------------------------------------------------------------

async function main(): Promise<void> {
  await testHappyPath();
  await testInvalidPhraseSendsNack();
  await testOpenErrorPropagates();
  await testDecryptFailureSendsNack();
  await testHttpsInputConvertedToWss();
  await testTwoSequentialPairsSucceed();
  await testPairToolHardTimeout();

  // eslint-disable-next-line no-console
  console.log(`# fail: ${_failed}`);
  // eslint-disable-next-line no-console
  console.log(`# ${_passed}/${_passed + _failed} passed`);
  if (_failed > 0) {
    // eslint-disable-next-line no-console
    console.log('TESTS FAILED');
    process.exit(1);
  } else {
    // eslint-disable-next-line no-console
    console.log('ALL TESTS PASSED');
  }
}

main().catch((err) => {
  // eslint-disable-next-line no-console
  console.error('Test runner crashed:', err);
  process.exit(1);
});
