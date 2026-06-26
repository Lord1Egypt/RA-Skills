/**
 * Tests for pair-session-store (P1 of the v3.3.0 QR-pairing implementation).
 *
 * Coverage targets:
 *   1. clampTtlMs: default / min / max / negative / undefined.
 *   2. createPairSession: persists with correct fields, 0600 mode.
 *   3. createPairSession: two concurrent creates don't corrupt the file.
 *   4. loadPairSessionsFileSync: missing file → empty; bad JSON → empty;
 *      wrong version → empty; shape-invalid session → dropped.
 *   5. writePairSessionsFileSync: atomic (temp + rename), mode 0600.
 *   6. pruneStaleSessions: expired awaiting_scan flipped to expired;
 *      terminal past retention dropped; active sessions preserved.
 *   7. getPairSession: returns session; returns null for unknown sid;
 *      returns terminal sessions (for distinguishing 404 vs 409/410);
 *      null for sid past TTL that has been pruned-to-expired+retention.
 *   8. updatePairSession: mutates in place; returns updated copy;
 *      null mutator removes session.
 *   9. transitionPairSession: changes status + lastStatusChangeAtMs;
 *      idempotent for same status.
 *   10. registerFailedSecondaryCode: increments counter; at 5 attempts
 *       flips status to rejected.
 *   11. consumePairSession: flips awaiting_scan → consumed; returns
 *       pre-transition session; subsequent consume returns
 *       already_consumed; consume of expired returns expired.
 *   12. rejectPairSession: flips to rejected.
 *   13. listActivePairSessions: only returns awaiting_scan +
 *       device_connected (not terminal).
 *   14. redactPairSession: scrubs skGatewayB64 + secondaryCode.
 *   15. Concurrent updates don't race (lock enforcement).
 *
 * Run with: npx tsx pair-session-store.test.ts
 *
 * TAP-style, no jest dependency — matches onboarding-state.test.ts.
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import {
  clampTtlMs,
  createPairSession,
  loadPairSessionsFileSync,
  writePairSessionsFileSync,
  pruneStaleSessions,
  getPairSession,
  updatePairSession,
  transitionPairSession,
  registerFailedSecondaryCode,
  consumePairSession,
  rejectPairSession,
  listActivePairSessions,
  listAllPairSessions,
  redactPairSession,
  defaultPairSessionsPath,
  DEFAULT_PAIR_TTL_MS,
  MIN_PAIR_TTL_MS,
  MAX_PAIR_TTL_MS,
  TERMINAL_RETENTION_MS,
  MAX_SECONDARY_CODE_ATTEMPTS,
  PAIR_SESSION_FILE_VERSION,
  type PairSession,
  type PairSessionFile,
} from './pair-session-store.js';

let passed = 0;
let failed = 0;

function assert(condition: boolean, name: string): void {
  const n = passed + failed + 1;
  if (condition) {
    console.log(`ok ${n} - ${name}`);
    passed++;
  } else {
    console.log(`not ok ${n} - ${name}`);
    failed++;
  }
}

function mkTmp(): string {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'tr-pair-'));
}

/** Fixed-clock helper. */
function frozen(now: number): () => number {
  return () => now;
}

/** Minimal valid session factory for lightweight fixtures. */
function fixtureSession(overrides: Partial<PairSession> = {}): PairSession {
  return {
    sid: '00112233445566778899aabbccddeeff',
    skGatewayB64: 'A'.repeat(43), // 32-byte material base64url-encoded
    pkGatewayB64: 'B'.repeat(43),
    createdAtMs: 1_000_000,
    expiresAtMs: 1_000_000 + DEFAULT_PAIR_TTL_MS,
    secondaryCode: '123456',
    secondaryCodeAttempts: 0,
    operatorContext: { channel: 'cli' },
    mode: 'generate',
    status: 'awaiting_scan',
    lastStatusChangeAtMs: 1_000_000,
    ...overrides,
  };
}

async function main(): Promise<void> {
  // ---------------------------------------------------------------------
  // 1. clampTtlMs
  // ---------------------------------------------------------------------
  assert(clampTtlMs(undefined) === DEFAULT_PAIR_TTL_MS, 'clampTtlMs: undefined → default 15 min');
  assert(clampTtlMs(0) === DEFAULT_PAIR_TTL_MS, 'clampTtlMs: 0 → default (treated as invalid)');
  assert(clampTtlMs(-1) === DEFAULT_PAIR_TTL_MS, 'clampTtlMs: negative → default');
  assert(clampTtlMs(60_000) === MIN_PAIR_TTL_MS, 'clampTtlMs: 1 min → clamped to min 5 min');
  assert(clampTtlMs(10 * 60 * 1000) === 10 * 60 * 1000, 'clampTtlMs: 10 min → unchanged');
  assert(clampTtlMs(120 * 60 * 1000) === MAX_PAIR_TTL_MS, 'clampTtlMs: 2 hr → clamped to max 60 min');

  // ---------------------------------------------------------------------
  // 2. createPairSession: happy path
  // ---------------------------------------------------------------------
  {
    const tmp = mkTmp();
    const p = path.join(tmp, 'pair.json');
    const t = 2_000_000;
    const s = await createPairSession(p, {
      mode: 'generate',
      operatorContext: { channel: 'tui', senderId: 'alice' },
      rngSid: () => Buffer.from('a'.repeat(32), 'hex'), // 16 bytes of 0xaa
      rngPrivateKey: () => Buffer.alloc(32, 0x11),
      rngPublicKey: () => Buffer.alloc(32, 0x22),
      rngSecondaryCode: () => '987654',
      now: () => t,
    });

    assert(s.sid === 'a'.repeat(32), 'create: sid is 32 hex chars');
    assert(s.mode === 'generate', 'create: mode persisted');
    assert(s.secondaryCode === '987654', 'create: secondaryCode persisted');
    assert(s.status === 'awaiting_scan', 'create: initial status awaiting_scan');
    assert(s.createdAtMs === t, 'create: createdAtMs = now');
    assert(s.expiresAtMs === t + DEFAULT_PAIR_TTL_MS, 'create: expiresAtMs = now + default TTL');
    assert(s.operatorContext.senderId === 'alice', 'create: operatorContext persisted');
    assert(s.secondaryCodeAttempts === 0, 'create: attempts counter starts at 0');

    assert(fs.existsSync(p), 'create: sessions file on disk');
    const mode = fs.statSync(p).mode & 0o777;
    assert(mode === 0o600, `create: file mode is 0o600 (got ${mode.toString(8)})`);

    const onDisk = JSON.parse(fs.readFileSync(p, 'utf-8')) as PairSessionFile;
    assert(onDisk.version === PAIR_SESSION_FILE_VERSION, 'create: file version persisted');
    assert(onDisk.sessions.length === 1, 'create: one session persisted');
    assert(onDisk.sessions[0].sid === s.sid, 'create: sid round-trips');
    // Ensure no leftover tmp file
    const leftovers = fs.readdirSync(tmp).filter((f) => f.startsWith('pair.json.tmp-'));
    assert(leftovers.length === 0, 'create: no leftover temp files');
    // Ensure no leftover lock file
    assert(!fs.existsSync(`${p}.lock`), 'create: lock released');

    fs.rmSync(tmp, { recursive: true, force: true });
  }

  // ---------------------------------------------------------------------
  // 3. Two concurrent creates serialize
  // ---------------------------------------------------------------------
  {
    const tmp = mkTmp();
    const p = path.join(tmp, 'pair.json');

    const mkOpts = (label: string) => ({
      mode: 'generate' as const,
      operatorContext: { channel: 'cli', senderId: label },
      now: () => Date.now(),
    });

    const [a, b, c] = await Promise.all([
      createPairSession(p, mkOpts('a')),
      createPairSession(p, mkOpts('b')),
      createPairSession(p, mkOpts('c')),
    ]);
    assert(a.sid !== b.sid && b.sid !== c.sid, 'concurrent create: sids are distinct');

    const file = loadPairSessionsFileSync(p);
    assert(file.sessions.length === 3, 'concurrent create: all 3 persisted');
    assert(!fs.existsSync(`${p}.lock`), 'concurrent create: lock released');

    fs.rmSync(tmp, { recursive: true, force: true });
  }

  // ---------------------------------------------------------------------
  // 4. loadPairSessionsFileSync: missing / bad JSON / wrong shape
  // ---------------------------------------------------------------------
  {
    const tmp = mkTmp();

    const missing = loadPairSessionsFileSync(path.join(tmp, 'absent.json'));
    assert(missing.sessions.length === 0 && missing.version === PAIR_SESSION_FILE_VERSION, 'load: missing file → empty');

    const badJson = path.join(tmp, 'bad.json');
    fs.writeFileSync(badJson, 'not json');
    const parsed = loadPairSessionsFileSync(badJson);
    assert(parsed.sessions.length === 0, 'load: bad JSON → empty');

    const wrongVersion = path.join(tmp, 'v9.json');
    fs.writeFileSync(wrongVersion, JSON.stringify({ version: 9, sessions: [] }));
    assert(loadPairSessionsFileSync(wrongVersion).sessions.length === 0, 'load: wrong version → empty');

    const sessionsNotArray = path.join(tmp, 'notarr.json');
    fs.writeFileSync(sessionsNotArray, JSON.stringify({ version: 1, sessions: {} }));
    assert(loadPairSessionsFileSync(sessionsNotArray).sessions.length === 0, 'load: non-array sessions → empty');

    const mixedShape = path.join(tmp, 'mix.json');
    const good = fixtureSession();
    const bad = { sid: 'x', mode: 'bogus' };
    fs.writeFileSync(mixedShape, JSON.stringify({ version: 1, sessions: [good, bad] }));
    const mixed = loadPairSessionsFileSync(mixedShape);
    assert(mixed.sessions.length === 1 && mixed.sessions[0].sid === good.sid, 'load: drops shape-invalid entries');

    fs.rmSync(tmp, { recursive: true, force: true });
  }

  // ---------------------------------------------------------------------
  // 5. writePairSessionsFileSync: atomic, 0600
  // ---------------------------------------------------------------------
  {
    const tmp = mkTmp();
    const p = path.join(tmp, 'pair.json');
    const ok = writePairSessionsFileSync(p, {
      version: PAIR_SESSION_FILE_VERSION,
      sessions: [fixtureSession()],
    });
    assert(ok === true, 'write: returns true on success');
    assert(fs.existsSync(p), 'write: file exists');
    const mode = fs.statSync(p).mode & 0o777;
    assert(mode === 0o600, `write: mode 0o600 (got ${mode.toString(8)})`);
    const leftovers = fs.readdirSync(tmp).filter((f) => f.startsWith('pair.json.tmp-'));
    assert(leftovers.length === 0, 'write: no leftover temp files');
    fs.rmSync(tmp, { recursive: true, force: true });
  }

  // ---------------------------------------------------------------------
  // 6. pruneStaleSessions
  // ---------------------------------------------------------------------
  {
    const now = 10_000_000;
    const active = fixtureSession({ sid: 'active', expiresAtMs: now + 1000, status: 'awaiting_scan' });
    const expired = fixtureSession({ sid: 'expired', expiresAtMs: now - 1, status: 'awaiting_scan' });
    const terminalFresh = fixtureSession({
      sid: 'termFresh',
      status: 'completed',
      lastStatusChangeAtMs: now - 1000,
    });
    const terminalStale = fixtureSession({
      sid: 'termStale',
      status: 'completed',
      lastStatusChangeAtMs: now - TERMINAL_RETENTION_MS - 1,
    });

    const pruned = pruneStaleSessions(
      { version: PAIR_SESSION_FILE_VERSION, sessions: [active, expired, terminalFresh, terminalStale] },
      now,
    );
    const keptSids = pruned.file.sessions.map((s) => s.sid).sort();
    assert(
      keptSids.includes('active'),
      'prune: active session preserved',
    );
    const expiredRec = pruned.file.sessions.find((s) => s.sid === 'expired');
    assert(!!expiredRec && expiredRec.status === 'expired', 'prune: expired awaiting_scan flipped to expired');
    assert(
      pruned.file.sessions.some((s) => s.sid === 'termFresh'),
      'prune: recent terminal preserved',
    );
    assert(
      !pruned.file.sessions.some((s) => s.sid === 'termStale'),
      'prune: stale terminal dropped',
    );
    assert(pruned.prunedSids.includes('termStale'), 'prune: reports dropped sid');
  }

  // ---------------------------------------------------------------------
  // 7. getPairSession
  // ---------------------------------------------------------------------
  {
    const tmp = mkTmp();
    const p = path.join(tmp, 'pair.json');
    const baseT = 5_000_000;
    const s = await createPairSession(p, {
      mode: 'generate',
      operatorContext: { channel: 'cli' },
      now: () => baseT,
      rngSid: () => Buffer.from('11'.repeat(16), 'hex'),
      rngPrivateKey: () => Buffer.alloc(32, 0x33),
      rngPublicKey: () => Buffer.alloc(32, 0x44),
      rngSecondaryCode: () => '000001',
    });

    const found = await getPairSession(p, s.sid, frozen(baseT + 1000));
    assert(!!found && found.sid === s.sid, 'get: returns matching session');

    const absent = await getPairSession(p, 'notreal', frozen(baseT + 1000));
    assert(absent === null, 'get: null for unknown sid');

    // Advance beyond TTL + retention → pruning evicts entirely
    const farFuture = s.expiresAtMs + TERMINAL_RETENTION_MS + 1;
    const gone = await getPairSession(p, s.sid, frozen(farFuture));
    assert(gone === null, 'get: expired + past retention → evicted → null');

    fs.rmSync(tmp, { recursive: true, force: true });
  }

  // ---------------------------------------------------------------------
  // 8. updatePairSession
  // ---------------------------------------------------------------------
  {
    const tmp = mkTmp();
    const p = path.join(tmp, 'pair.json');
    const s = await createPairSession(p, {
      mode: 'generate',
      operatorContext: { channel: 'cli' },
    });

    const changed = await updatePairSession(p, s.sid, (cur) => ({ ...cur, mode: 'import' }));
    assert(!!changed && changed.mode === 'import', 'update: mutator applied');

    const removed = await updatePairSession(p, s.sid, () => null);
    assert(removed === null, 'update: null mutator drops session');

    const file = loadPairSessionsFileSync(p);
    assert(file.sessions.length === 0, 'update: null mutator persists removal');

    const missing = await updatePairSession(p, 'nope', (cur) => cur);
    assert(missing === null, 'update: unknown sid → null');

    fs.rmSync(tmp, { recursive: true, force: true });
  }

  // ---------------------------------------------------------------------
  // 9. transitionPairSession
  // ---------------------------------------------------------------------
  {
    const tmp = mkTmp();
    const p = path.join(tmp, 'pair.json');
    const baseT = 7_000_000;
    const s = await createPairSession(p, {
      mode: 'generate',
      operatorContext: { channel: 'cli' },
      now: () => baseT,
    });

    const step1 = await transitionPairSession(p, s.sid, 'device_connected', frozen(baseT + 1000));
    assert(step1?.status === 'device_connected', 'transition: status changed');
    assert(step1?.lastStatusChangeAtMs === baseT + 1000, 'transition: timestamp updated');

    // Idempotent: same-status transition doesn't bump timestamp
    const step2 = await transitionPairSession(p, s.sid, 'device_connected', frozen(baseT + 2000));
    assert(step2?.lastStatusChangeAtMs === baseT + 1000, 'transition: idempotent (no-op when unchanged)');

    const step3 = await transitionPairSession(p, 'nope', 'completed');
    assert(step3 === null, 'transition: unknown sid → null');

    fs.rmSync(tmp, { recursive: true, force: true });
  }

  // ---------------------------------------------------------------------
  // 10. registerFailedSecondaryCode
  // ---------------------------------------------------------------------
  {
    const tmp = mkTmp();
    const p = path.join(tmp, 'pair.json');
    const s = await createPairSession(p, {
      mode: 'generate',
      operatorContext: { channel: 'cli' },
    });

    let last = s;
    for (let i = 1; i < MAX_SECONDARY_CODE_ATTEMPTS; i++) {
      const r = await registerFailedSecondaryCode(p, s.sid);
      assert(r?.secondaryCodeAttempts === i, `attempts: counter = ${i}`);
      assert(r?.status === 'awaiting_scan', `attempts: still awaiting_scan at ${i}`);
      last = r!;
    }
    const final = await registerFailedSecondaryCode(p, s.sid);
    assert(final?.secondaryCodeAttempts === MAX_SECONDARY_CODE_ATTEMPTS, 'attempts: hits max');
    assert(final?.status === 'rejected', 'attempts: max → rejected');
    void last;

    fs.rmSync(tmp, { recursive: true, force: true });
  }

  // ---------------------------------------------------------------------
  // 11. consumePairSession
  // ---------------------------------------------------------------------
  {
    const tmp = mkTmp();
    const p = path.join(tmp, 'pair.json');
    const baseT = 8_000_000;
    const s = await createPairSession(p, {
      mode: 'generate',
      operatorContext: { channel: 'cli' },
      now: () => baseT,
    });

    const r1 = await consumePairSession(p, s.sid, frozen(baseT + 1000));
    assert(r1.ok === true, 'consume: first consume succeeds');
    if (r1.ok) {
      assert(r1.session.status === 'awaiting_scan', 'consume: returns PRE-transition status');
      assert(r1.session.skGatewayB64 === s.skGatewayB64, 'consume: returns skGatewayB64 for crypto');
    }

    // After the consume, on-disk status should be "consumed"
    const afterConsume = await getPairSession(p, s.sid, frozen(baseT + 1500));
    assert(afterConsume?.status === 'consumed', 'consume: terminal on-disk state is consumed');

    const r2 = await consumePairSession(p, s.sid, frozen(baseT + 2000));
    assert(r2.ok === false && !r2.ok && r2.error === 'already_consumed', 'consume: 2nd attempt → already_consumed');

    const r3 = await consumePairSession(p, 'nope', frozen(baseT + 3000));
    assert(r3.ok === false && !r3.ok && r3.error === 'not_found', 'consume: unknown sid → not_found');

    // Expiry path: create a new session, jump past TTL, consume
    const s2 = await createPairSession(p, {
      mode: 'generate',
      operatorContext: { channel: 'cli' },
      now: () => baseT,
    });
    const r4 = await consumePairSession(p, s2.sid, frozen(s2.expiresAtMs + 1));
    assert(r4.ok === false && !r4.ok && r4.error === 'expired', 'consume: past TTL → expired');

    fs.rmSync(tmp, { recursive: true, force: true });
  }

  // ---------------------------------------------------------------------
  // 12. rejectPairSession
  // ---------------------------------------------------------------------
  {
    const tmp = mkTmp();
    const p = path.join(tmp, 'pair.json');
    const s = await createPairSession(p, {
      mode: 'generate',
      operatorContext: { channel: 'cli' },
    });
    const r = await rejectPairSession(p, s.sid);
    assert(r?.status === 'rejected', 'reject: status flipped');
    fs.rmSync(tmp, { recursive: true, force: true });
  }

  // ---------------------------------------------------------------------
  // 13. listActivePairSessions vs listAllPairSessions
  // ---------------------------------------------------------------------
  {
    const tmp = mkTmp();
    const p = path.join(tmp, 'pair.json');
    const a = await createPairSession(p, { mode: 'generate', operatorContext: { channel: 'cli' } });
    const b = await createPairSession(p, { mode: 'generate', operatorContext: { channel: 'cli' } });
    await transitionPairSession(p, b.sid, 'completed');

    const active = await listActivePairSessions(p);
    assert(active.length === 1 && active[0].sid === a.sid, 'listActive: excludes terminal');

    const all = await listAllPairSessions(p);
    assert(all.length === 2, 'listAll: includes terminal');
    fs.rmSync(tmp, { recursive: true, force: true });
  }

  // ---------------------------------------------------------------------
  // 14. redactPairSession
  // ---------------------------------------------------------------------
  {
    const s = fixtureSession();
    const r = redactPairSession(s);
    assert(r.skGatewayB64 === '[redacted]', 'redact: sk replaced');
    assert(r.secondaryCode === '[redacted]', 'redact: code replaced');
    assert(r.pkGatewayB64 === s.pkGatewayB64, 'redact: pk left intact');
    assert(r.sid === s.sid, 'redact: sid left intact');
  }

  // ---------------------------------------------------------------------
  // 15. Concurrent mutations don't race
  // ---------------------------------------------------------------------
  {
    const tmp = mkTmp();
    const p = path.join(tmp, 'pair.json');
    const s = await createPairSession(p, {
      mode: 'generate',
      operatorContext: { channel: 'cli' },
    });

    const results = await Promise.all([
      registerFailedSecondaryCode(p, s.sid),
      registerFailedSecondaryCode(p, s.sid),
      registerFailedSecondaryCode(p, s.sid),
    ]);
    // All three mutations must be reflected — the final counter value
    // must be exactly 3. The intermediate counter values reported by
    // each individual call may be in any order.
    const final = await getPairSession(p, s.sid);
    assert(final?.secondaryCodeAttempts === 3, 'concurrent: all 3 increments landed');
    assert(
      results.every((r) => r && r.secondaryCodeAttempts >= 1 && r.secondaryCodeAttempts <= 3),
      'concurrent: each return value is in [1,3]',
    );

    fs.rmSync(tmp, { recursive: true, force: true });
  }

  // ---------------------------------------------------------------------
  // 16. defaultPairSessionsPath uses the .totalreclaw dir
  // ---------------------------------------------------------------------
  {
    const p = defaultPairSessionsPath('/custom/base');
    assert(p === '/custom/base/pair-sessions.json', 'defaultPath: base dir override');
  }

  // ---------------------------------------------------------------------
  // 17. Fresh-install regression — parent dir does NOT exist
  //
  // Regression for rc.3 (totalreclaw-internal#21, QA strace evidence):
  // acquireSessionsFileLock ran openSync(lockPath, 'wx') BEFORE ensuring
  // the parent dir existed. On a fresh user account with no
  // `~/.totalreclaw/`, every attempt returned ENOENT; the retry loop
  // spun for LOCK_WAIT_MS (10s) and threw "could not acquire lock".
  // The CLI surfaced that as a hung `openclaw totalreclaw pair generate`
  // with no QR / URL / code ever rendered.
  //
  // Expectation: createPairSession against a deep missing path succeeds
  // QUICKLY (well under the 10s deadline), creates all missing
  // intermediates, persists the session, and leaves no lock file.
  // ---------------------------------------------------------------------
  {
    const root = mkTmp();
    // Three levels deep to prove `{ recursive: true }` is honored.
    const missingDeep = path.join(root, 'a', 'b', 'c');
    const p = path.join(missingDeep, 'pair-sessions.json');

    assert(!fs.existsSync(missingDeep), 'fresh-install: parent dir absent pre-create');

    const started = Date.now();
    const s = await createPairSession(p, {
      mode: 'generate',
      operatorContext: { channel: 'cli' },
    });
    const elapsed = Date.now() - started;

    assert(elapsed < 2_000, `fresh-install: create completes promptly (got ${elapsed}ms, bug was 10_000ms+)`);
    assert(fs.existsSync(missingDeep), 'fresh-install: deep parent dir created');
    assert(fs.existsSync(p), 'fresh-install: sessions file created');
    assert(!fs.existsSync(`${p}.lock`), 'fresh-install: lock released');
    assert(typeof s.sid === 'string' && s.sid.length === 32, 'fresh-install: session has valid sid');

    // Bonus: the on-disk file has 0o600 even though we created a missing
    // parent dir — the mkdir mode doesn't leak into the file mode.
    const mode = fs.statSync(p).mode & 0o777;
    assert(mode === 0o600, `fresh-install: file mode still 0o600 (got ${mode.toString(8)})`);

    fs.rmSync(root, { recursive: true, force: true });
  }

  // ---------------------------------------------------------------------
  // 18. Fresh-install regression — read paths also tolerate missing dir
  //
  // Defensive: `getPairSession` is called by the HTTP handler before the
  // CLI has had a chance to create anything. If the operator pokes the
  // browser page before `pair start` writes any state, we should return
  // null cleanly rather than throwing. `listActivePairSessions` is used
  // by the CLI's "is a pairing already in flight?" guard on a fresh box.
  // ---------------------------------------------------------------------
  {
    const root = mkTmp();
    const missingDeep = path.join(root, 'never', 'made');
    const p = path.join(missingDeep, 'pair-sessions.json');

    const found = await getPairSession(p, 'deadbeef'.repeat(4));
    assert(found === null, 'fresh-install: getPairSession returns null, no throw');

    const active = await listActivePairSessions(p);
    assert(Array.isArray(active) && active.length === 0, 'fresh-install: listActive returns [], no throw');

    fs.rmSync(root, { recursive: true, force: true });
  }

  // ---------------------------------------------------------------------
  // Summary
  // ---------------------------------------------------------------------
  console.log(`# ${passed} passed, ${failed} failed`);
  if (failed > 0) process.exit(1);
}

main().catch((err) => {
  console.error('fatal:', err);
  process.exit(1);
});
