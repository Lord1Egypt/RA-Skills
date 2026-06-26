/**
 * Tests for auto-pair-on-load.ts.
 *
 * Covers the four primary branches:
 *   1. credentials.json present -> no-op (early return)
 *   2. no creds + no pending sentinel -> opens a new session + writes sentinel
 *   3. no creds + valid (non-expired) sentinel -> reuse (no-op)
 *   4. no creds + expired sentinel -> delete + re-create
 *
 * The relay is stubbed via `openSession` / `awaitPhrase` injection — no
 * WebSocket traffic. Disk I/O is sandboxed under `mkdtempSync` so the
 * real `~/.totalreclaw/` is never touched.
 *
 * Run with: npx tsx auto-pair-on-load.test.ts
 *
 * TAP-style output, no jest dependency.
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import {
  maybeStartAutoPair,
  type AutoPairDeps,
  type AutoPairLogger,
} from './auto-pair-on-load.js';
import {
  defaultPairPendingPath,
  loadPairPendingFile,
  writeCredentialsJson,
  writePairPendingFile,
  type PairPendingFile,
} from './fs-helpers.js';
import type {
  GatewayKeypair,
} from './pair-crypto.js';
import type { RemotePairSession } from './pair-remote-client.js';

let _passed = 0;
let _failed = 0;
let _seq = 0;
function ok(name: string, cond: boolean, detail?: string): void {
  const status = cond ? 'ok' : 'not ok';
  const tail = detail ? ` -- ${detail}` : '';
  _seq += 1;
  console.log(`${status} ${_seq} - ${name}${tail}`);
  if (cond) _passed += 1;
  else _failed += 1;
}

// ---------------------------------------------------------------------------
// Test fixtures
// ---------------------------------------------------------------------------

function makeLogger(): { logger: AutoPairLogger; lines: string[] } {
  const lines: string[] = [];
  return {
    lines,
    logger: {
      info: (msg: string) => lines.push(`INFO ${msg}`),
      warn: (msg: string) => lines.push(`WARN ${msg}`),
      error: (msg: string) => lines.push(`ERROR ${msg}`),
    },
  };
}

function makeMockSession(token: string, expiresAt: string): RemotePairSession {
  const fakeKeypair: GatewayKeypair = {
    skB64: 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=',
    pkB64: 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=',
  };
  // Minimal WS stub — only `close` is called in code paths exercised here.
  const fakeWs = { close: () => undefined } as unknown as WebSocket;
  return {
    url: `https://relay.example/pair/p/${token}#pk=AAAA`,
    pin: '123456',
    token,
    expiresAt,
    keypair: fakeKeypair,
    mode: 'generate',
    _ws: fakeWs,
  };
}

function makeDeps(
  tmp: string,
  overrides: Partial<AutoPairDeps> = {},
): { deps: AutoPairDeps; logLines: string[] } {
  const credentialsPath = path.join(tmp, 'credentials.json');
  const pendingPath = path.join(tmp, '.pair-pending.json');
  const onboardingStatePath = path.join(tmp, 'state.json');
  const { logger, lines } = makeLogger();

  return {
    logLines: lines,
    deps: {
      credentialsPath,
      pendingPath,
      onboardingStatePath,
      relayBaseUrl: 'wss://relay.example',
      pluginVersion: '3.3.13-test',
      logger,
      // Tests inject openSession + awaitPhrase to avoid real WS traffic.
      openSession: async () =>
        makeMockSession(
          'test-token-' + Math.random().toString(36).slice(2, 8),
          new Date(Date.now() + 60_000).toISOString(),
        ),
      awaitPhrase: async () => {
        // Default: never resolve in test scope (background task is never awaited).
        // Tests that need completion behavior inject their own awaitPhrase.
      },
      ...overrides,
    },
  };
}

// ---------------------------------------------------------------------------
// Test 1: credentials.json present -> no-op
// ---------------------------------------------------------------------------

async function test_creds_exist_no_op(): Promise<void> {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-auto-pair-creds-'));
  try {
    const { deps } = makeDeps(tmp);
    writeCredentialsJson(deps.credentialsPath, {
      mnemonic: 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about',
      userId: 'u1',
    });

    let opened = false;
    const result = await maybeStartAutoPair({
      ...deps,
      openSession: async () => {
        opened = true;
        return makeMockSession('should-not-happen', new Date().toISOString());
      },
    });

    ok(
      'creds-exist: status is creds_exist',
      result.status === 'creds_exist',
      `got ${result.status}`,
    );
    ok(
      'creds-exist: never opens a relay session',
      !opened,
      'openSession must NOT be called when credentials.json has a mnemonic',
    );
    ok(
      'creds-exist: no sentinel written',
      !fs.existsSync(deps.pendingPath ?? defaultPairPendingPath(deps.credentialsPath)),
      'sentinel file should not exist',
    );
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

// ---------------------------------------------------------------------------
// Test 2: no creds + no pending -> creates pending
// ---------------------------------------------------------------------------

async function test_no_creds_no_pending_creates(): Promise<void> {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-auto-pair-create-'));
  try {
    const { deps } = makeDeps(tmp);
    let openCalls = 0;
    const expiry = new Date(Date.now() + 120_000).toISOString();

    const result = await maybeStartAutoPair({
      ...deps,
      openSession: async () => {
        openCalls += 1;
        return makeMockSession('sid-fresh', expiry);
      },
    });

    ok(
      'no-creds/no-pending: status is started',
      result.status === 'started',
      `got ${result.status}`,
    );
    ok(
      'no-creds/no-pending: openSession called exactly once',
      openCalls === 1,
      `got ${openCalls}`,
    );
    const loaded = loadPairPendingFile(
      deps.pendingPath ?? defaultPairPendingPath(deps.credentialsPath),
    );
    ok(
      'no-creds/no-pending: sentinel written with v=1',
      !!loaded && loaded.v === 1,
      JSON.stringify(loaded),
    );
    ok(
      'no-creds/no-pending: sentinel url present',
      !!loaded && loaded.url.includes('/pair/p/sid-fresh'),
      loaded?.url,
    );
    ok(
      'no-creds/no-pending: sentinel pin = 123456',
      loaded?.pin === '123456',
      loaded?.pin,
    );
    ok(
      'no-creds/no-pending: sentinel sid = sid-fresh',
      loaded?.sid === 'sid-fresh',
      loaded?.sid,
    );
    ok(
      'no-creds/no-pending: expires_at_ms is the parsed relay expiry',
      !!loaded && loaded.expires_at_ms === Date.parse(expiry),
      String(loaded?.expires_at_ms),
    );
    ok(
      'no-creds/no-pending: NO mnemonic / phrase field in sentinel',
      !!loaded
        && !('mnemonic' in (loaded as Record<string, unknown>))
        && !('phrase' in (loaded as Record<string, unknown>))
        && !('recovery_phrase' in (loaded as Record<string, unknown>)),
      'phrase-safety: sentinel must NEVER hold phrase material',
    );
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

// ---------------------------------------------------------------------------
// Test 3: no creds + valid pending -> reuse (no-op)
// ---------------------------------------------------------------------------

async function test_valid_pending_reused(): Promise<void> {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-auto-pair-reuse-'));
  try {
    const { deps } = makeDeps(tmp);
    const pendingPath = deps.pendingPath ?? defaultPairPendingPath(deps.credentialsPath);
    const existing: PairPendingFile = {
      v: 1,
      url: 'https://relay.example/pair/p/sid-already',
      pin: '987654',
      sid: 'sid-already',
      expires_at_ms: Date.now() + 120_000,
      created_at_ms: Date.now(),
      mode: 'generate',
    };
    writePairPendingFile(pendingPath, existing);

    let openCalls = 0;
    const result = await maybeStartAutoPair({
      ...deps,
      openSession: async () => {
        openCalls += 1;
        return makeMockSession('should-not-happen', new Date().toISOString());
      },
    });

    ok(
      'valid-pending: status is pending_reused',
      result.status === 'pending_reused',
      `got ${result.status}`,
    );
    ok(
      'valid-pending: openSession NOT called',
      openCalls === 0,
      `got ${openCalls}`,
    );
    const reloaded = loadPairPendingFile(pendingPath);
    ok(
      'valid-pending: sentinel unchanged (still sid-already)',
      reloaded?.sid === 'sid-already',
      reloaded?.sid,
    );
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

// ---------------------------------------------------------------------------
// Test 4: no creds + expired pending -> re-create
// ---------------------------------------------------------------------------

async function test_expired_pending_recreated(): Promise<void> {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-auto-pair-expired-'));
  try {
    const { deps } = makeDeps(tmp);
    const pendingPath = deps.pendingPath ?? defaultPairPendingPath(deps.credentialsPath);
    const expired: PairPendingFile = {
      v: 1,
      url: 'https://relay.example/pair/p/sid-stale',
      pin: '000000',
      sid: 'sid-stale',
      expires_at_ms: Date.now() - 60_000, // 1 min ago
      created_at_ms: Date.now() - 600_000,
      mode: 'generate',
    };
    writePairPendingFile(pendingPath, expired);

    let openCalls = 0;
    const result = await maybeStartAutoPair({
      ...deps,
      openSession: async () => {
        openCalls += 1;
        return makeMockSession(
          'sid-fresh',
          new Date(Date.now() + 120_000).toISOString(),
        );
      },
    });

    ok(
      'expired-pending: status is started (fresh session opened)',
      result.status === 'started',
      `got ${result.status}`,
    );
    ok(
      'expired-pending: openSession called exactly once',
      openCalls === 1,
      `got ${openCalls}`,
    );
    const reloaded = loadPairPendingFile(pendingPath);
    ok(
      'expired-pending: sentinel replaced with fresh sid',
      reloaded?.sid === 'sid-fresh',
      reloaded?.sid,
    );
    ok(
      'expired-pending: stale URL no longer present',
      reloaded?.url !== 'https://relay.example/pair/p/sid-stale',
      reloaded?.url,
    );
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

// ---------------------------------------------------------------------------
// Test 5: openSession failure surfaces as { failed }
// ---------------------------------------------------------------------------

async function test_open_failure_returns_failed(): Promise<void> {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-auto-pair-fail-'));
  try {
    const { deps } = makeDeps(tmp);
    const result = await maybeStartAutoPair({
      ...deps,
      openSession: async () => {
        throw new Error('relay unreachable');
      },
    });
    ok(
      'open-failure: status is failed',
      result.status === 'failed',
      `got ${result.status}`,
    );
    if (result.status === 'failed') {
      ok(
        'open-failure: error contains reason',
        result.error.includes('relay unreachable'),
        result.error,
      );
    }
    ok(
      'open-failure: no sentinel written',
      !fs.existsSync(deps.pendingPath ?? defaultPairPendingPath(deps.credentialsPath)),
      'sentinel must not exist after a failed open',
    );
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

// ---------------------------------------------------------------------------
// Run
// ---------------------------------------------------------------------------

async function main(): Promise<void> {
  await test_creds_exist_no_op();
  await test_no_creds_no_pending_creates();
  await test_valid_pending_reused();
  await test_expired_pending_recreated();
  await test_open_failure_returns_failed();

  console.log(`\n# tests ${_passed + _failed}`);
  console.log(`# pass ${_passed}`);
  console.log(`# fail ${_failed}`);
  if (_failed > 0) {
    process.exit(1);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
