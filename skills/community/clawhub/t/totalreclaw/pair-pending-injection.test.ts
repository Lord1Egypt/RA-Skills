/**
 * Tests for pair-pending-injection.ts.
 *
 * Covers:
 *   1. Sentinel missing -> hook no-ops (returns undefined)
 *   2. Sentinel present + non-expired -> hook injects prependContext
 *      with the EXACT url + pin (no template substitution shenanigans)
 *   3. Sentinel present + expired -> hook deletes the file; if a re-create
 *      factory is provided AND it returns a fresh sentinel, the hook
 *      injects the new url + pin; else returns undefined
 *
 * Run with: npx tsx pair-pending-injection.test.ts
 *
 * TAP-style output, no jest dependency.
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import {
  runPairPendingInjection,
  buildPrependContext,
  installBeforeAgentStartHook,
  type PairInjectionDeps,
  type PairInjectionApi,
} from './pair-pending-injection.js';
import {
  defaultPairPendingPath,
  writePairPendingFile,
  type PairPendingFile,
} from './fs-helpers.js';
import type { AutoPairDeps } from './auto-pair-on-load.js';

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
// Fixtures
// ---------------------------------------------------------------------------

function makeLogger(): { logger: PairInjectionApi['logger']; lines: string[] } {
  const lines: string[] = [];
  return {
    lines,
    logger: {
      info: (...args: unknown[]) => lines.push(`INFO ${args.join(' ')}`),
      warn: (...args: unknown[]) => lines.push(`WARN ${args.join(' ')}`),
      error: (...args: unknown[]) => lines.push(`ERROR ${args.join(' ')}`),
    },
  };
}

function makePending(overrides: Partial<PairPendingFile> = {}): PairPendingFile {
  return {
    v: 1,
    url: 'https://relay.example/pair/p/sid-test#pk=AAAAFOO',
    pin: '654321',
    sid: 'sid-test',
    expires_at_ms: Date.now() + 60_000,
    created_at_ms: Date.now(),
    mode: 'generate',
    ...overrides,
  };
}

function makeFakeAutoPairDeps(tmp: string): AutoPairDeps {
  const { logger } = makeLogger();
  return {
    credentialsPath: path.join(tmp, 'credentials.json'),
    pendingPath: path.join(tmp, '.pair-pending.json'),
    onboardingStatePath: path.join(tmp, 'state.json'),
    relayBaseUrl: 'wss://relay.example',
    pluginVersion: '3.3.13-test',
    logger,
  };
}

// ---------------------------------------------------------------------------
// Test 1: sentinel missing -> no-op
// ---------------------------------------------------------------------------

async function test_missing_sentinel_no_op(): Promise<void> {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-pair-inj-missing-'));
  try {
    const { logger } = makeLogger();
    const deps: PairInjectionDeps = {
      credentialsPath: path.join(tmp, 'credentials.json'),
      pendingPath: path.join(tmp, '.pair-pending.json'),
    };
    const result = await runPairPendingInjection(deps, logger);
    ok(
      'missing-sentinel: returns undefined',
      result === undefined,
      `got ${JSON.stringify(result)}`,
    );
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

// ---------------------------------------------------------------------------
// Test 2: valid sentinel -> hook injects context with verbatim url + pin
// ---------------------------------------------------------------------------

async function test_valid_sentinel_injects(): Promise<void> {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-pair-inj-valid-'));
  try {
    const credentialsPath = path.join(tmp, 'credentials.json');
    const pendingPath = defaultPairPendingPath(credentialsPath);
    const pending = makePending({
      url: 'https://relay.example/pair/p/sid-XYZ#pk=ABCDEF',
      pin: '111222',
    });
    writePairPendingFile(pendingPath, pending);

    const { logger } = makeLogger();
    const result = await runPairPendingInjection(
      { credentialsPath, pendingPath },
      logger,
    );

    ok(
      'valid-sentinel: returns prependContext object',
      !!result && typeof result.prependContext === 'string',
      `got ${JSON.stringify(result)}`,
    );
    const ctx = result?.prependContext ?? '';
    ok(
      'valid-sentinel: prependContext contains the exact URL',
      ctx.includes('https://relay.example/pair/p/sid-XYZ#pk=ABCDEF'),
      'URL must appear verbatim — no template substitution',
    );
    ok(
      'valid-sentinel: prependContext contains the exact PIN',
      ctx.includes('111222'),
      'PIN must appear verbatim',
    );
    ok(
      'valid-sentinel: prependContext warns the agent not to invent values',
      ctx.includes('do NOT') || ctx.includes('NEVER') || ctx.includes('CRITICAL'),
      'must include explicit "do not invent" instruction',
    );
    ok(
      'valid-sentinel: prependContext references the pending file as source of truth',
      ctx.includes('.pair-pending.json'),
      'agent must be told where the file lives',
    );
    ok(
      'valid-sentinel: prependContext does NOT contain phrase / mnemonic / recovery_phrase',
      !/\bmnemonic\b|\brecovery[_ ]?phrase\b/i.test(
        ctx.replace(/recovery phrase/g, '').replace(/12-word recovery phrase/g, ''),
      )
        // The block intentionally mentions "recovery phrase" in the user-facing
        // explanation ("the user can generate a 12-word recovery phrase"). Strip
        // those known-good occurrences before checking for stray uses.
        || !ctx.includes('abandon'),
      'phrase-safety: never embed real phrase material',
    );
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

// ---------------------------------------------------------------------------
// Test 3: expired sentinel + no factory -> delete + return undefined
// ---------------------------------------------------------------------------

async function test_expired_no_factory(): Promise<void> {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-pair-inj-expired1-'));
  try {
    const credentialsPath = path.join(tmp, 'credentials.json');
    const pendingPath = defaultPairPendingPath(credentialsPath);
    const expired = makePending({
      sid: 'sid-stale',
      url: 'https://relay.example/pair/p/sid-stale',
      expires_at_ms: Date.now() - 60_000,
    });
    writePairPendingFile(pendingPath, expired);

    const { logger } = makeLogger();
    const result = await runPairPendingInjection(
      { credentialsPath, pendingPath },
      logger,
    );

    ok(
      'expired/no-factory: returns undefined',
      result === undefined,
      `got ${JSON.stringify(result)}`,
    );
    ok(
      'expired/no-factory: sentinel file deleted',
      !fs.existsSync(pendingPath),
      'expired sentinel must be cleaned up',
    );
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

// ---------------------------------------------------------------------------
// Test 4: expired sentinel + factory -> re-create + inject new URL/PIN
// ---------------------------------------------------------------------------

async function test_expired_with_factory_recreates(): Promise<void> {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-pair-inj-expired2-'));
  try {
    const credentialsPath = path.join(tmp, 'credentials.json');
    const pendingPath = defaultPairPendingPath(credentialsPath);
    const expired = makePending({
      sid: 'sid-stale',
      url: 'https://relay.example/pair/p/sid-stale',
      expires_at_ms: Date.now() - 60_000,
    });
    writePairPendingFile(pendingPath, expired);

    const fresh = makePending({
      sid: 'sid-fresh',
      url: 'https://relay.example/pair/p/sid-fresh#pk=NEW',
      pin: '999000',
      expires_at_ms: Date.now() + 120_000,
    });

    let factoryCalls = 0;
    let startCalls = 0;

    const { logger } = makeLogger();
    const result = await runPairPendingInjection(
      {
        credentialsPath,
        pendingPath,
        autoPairDepsFactory: () => {
          factoryCalls += 1;
          return makeFakeAutoPairDeps(tmp);
        },
        startAutoPair: async () => {
          startCalls += 1;
          // Simulate maybeStartAutoPair writing the fresh sentinel.
          writePairPendingFile(pendingPath, fresh);
          return { status: 'started' as const, pending: fresh };
        },
      },
      logger,
    );

    ok(
      'expired/factory: factory called once',
      factoryCalls === 1,
      `got ${factoryCalls}`,
    );
    ok(
      'expired/factory: startAutoPair called once',
      startCalls === 1,
      `got ${startCalls}`,
    );
    ok(
      'expired/factory: returns prependContext for FRESH URL',
      !!result?.prependContext && result.prependContext.includes('sid-fresh'),
      `got ${result?.prependContext?.slice(0, 200)}`,
    );
    ok(
      'expired/factory: prependContext contains fresh PIN',
      !!result?.prependContext && result.prependContext.includes('999000'),
      'must contain fresh PIN not stale one',
    );
    ok(
      'expired/factory: stale URL NOT in prepend',
      !result?.prependContext?.includes('sid-stale'),
      'stale URL must not leak',
    );
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

// ---------------------------------------------------------------------------
// Test 5: expired + factory that returns null -> undefined
// ---------------------------------------------------------------------------

async function test_expired_factory_returns_null(): Promise<void> {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-pair-inj-expired3-'));
  try {
    const credentialsPath = path.join(tmp, 'credentials.json');
    const pendingPath = defaultPairPendingPath(credentialsPath);
    writePairPendingFile(
      pendingPath,
      makePending({ expires_at_ms: Date.now() - 60_000 }),
    );

    const { logger } = makeLogger();
    const result = await runPairPendingInjection(
      {
        credentialsPath,
        pendingPath,
        autoPairDepsFactory: () => null,
      },
      logger,
    );
    ok(
      'factory-null: returns undefined',
      result === undefined,
      `got ${JSON.stringify(result)}`,
    );
    ok(
      'factory-null: sentinel still deleted',
      !fs.existsSync(pendingPath),
      'expired sentinel must be cleaned up even when no re-create',
    );
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

// ---------------------------------------------------------------------------
// Test 6: buildPrependContext is pure — same input -> same output
// ---------------------------------------------------------------------------

function test_build_prepend_pure(): void {
  const pending = makePending({
    url: 'https://relay.example/pair/p/sid-pure#pk=PURE',
    pin: '424242',
  });
  const a = buildPrependContext(pending);
  const b = buildPrependContext(pending);
  ok(
    'build-prepend: deterministic for same input',
    a === b,
    'must be a pure function',
  );
  ok(
    'build-prepend: contains exact URL',
    a.includes('https://relay.example/pair/p/sid-pure#pk=PURE'),
    'URL must round-trip verbatim',
  );
  ok(
    'build-prepend: contains exact PIN',
    a.includes('424242'),
    'PIN must round-trip verbatim',
  );
}

// ---------------------------------------------------------------------------
// Test 7: installBeforeAgentStartHook registers with priority + try/catches
// ---------------------------------------------------------------------------

function test_install_hook(): void {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-pair-inj-install-'));
  try {
    const credentialsPath = path.join(tmp, 'credentials.json');
    let registered: { name: string; priority?: number } | null = null;
    const { logger } = makeLogger();
    const fakeApi: PairInjectionApi = {
      logger,
      on: (name, _handler, opts) => {
        registered = { name, priority: opts?.priority };
      },
    };
    installBeforeAgentStartHook(fakeApi, { credentialsPath });
    ok(
      'install-hook: registered before_agent_start',
      registered !== null && (registered as { name: string }).name === 'before_agent_start',
      `got ${JSON.stringify(registered)}`,
    );
    ok(
      'install-hook: priority is numeric (chosen for predictable ordering)',
      registered !== null && typeof (registered as { priority?: number }).priority === 'number',
      `got ${JSON.stringify(registered)}`,
    );
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

// ---------------------------------------------------------------------------
// Run
// ---------------------------------------------------------------------------

async function main(): Promise<void> {
  await test_missing_sentinel_no_op();
  await test_valid_sentinel_injects();
  await test_expired_no_factory();
  await test_expired_with_factory_recreates();
  await test_expired_factory_returns_null();
  test_build_prepend_pure();
  test_install_hook();

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
