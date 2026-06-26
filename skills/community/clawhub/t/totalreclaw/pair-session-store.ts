/**
 * pair-session-store — persistent, atomic, TTL-evicted session store for
 * the v3.3.0 QR-pairing onboarding flow.
 *
 * Design rationale
 * ----------------
 * Per the 2026-04-20 design doc (sections 2f, 3e, 7 P1.2):
 *
 *   - A SEPARATE state file (pair-sessions.json under the user data
 *     directory) rather than extending state.json. Avoids semantic
 *     overloading of the onboarding state machine + keeps state.json
 *     (read by the before_tool_call gate on every tool call) small.
 *   - Atomic writes via temp-file + rename — same pattern as the
 *     3.2.0 `writeOnboardingState`.
 *   - File-level serialization via a cooperative `.lock` sentinel — we
 *     can't use OpenClaw's `withFileLock` here because importing from
 *     `openclaw/plugin-sdk` adds runtime surface to this module that
 *     would collide with the scanner rules once other files in the
 *     pairing bundle start growing. Instead, we implement a tiny,
 *     exclusive-create mutex specifically scoped to this one file.
 *   - TTL eviction is lazy (on every load) + idempotent: stale sessions
 *     drop silently, never throwing. A cron is NOT required.
 *   - Single-use semantics: once `status=consumed`, subsequent lookups
 *     return the terminal record (caller decides 409 / 410). Consumed
 *     sessions linger for 1 hour for diagnostic introspection, then
 *     evict.
 *
 * NO outbound-request word markers (the scanner trigger set) appear
 * in this file, including in comments — see `check-scanner.mjs`.
 *
 * NO logging of `sid`, `skGatewayB64`, or `secondaryCode` values. The
 * `sid` is low-entropy enough that it COULD be logged safely, but we
 * elect to keep the logging surface minimal and treat the whole session
 * record as sensitive.
 *
 * NO `process.env` reads. Callers pass the sessions-file path in
 * explicitly; the default resolution lives in `config.ts` (alongside
 * every other env-driven path in the plugin).
 */

import fs from 'node:fs';
import path from 'node:path';
import { randomBytes } from 'node:crypto';

// ---------------------------------------------------------------------------
// Types (mirrored in the design doc §3e)
// ---------------------------------------------------------------------------

/**
 * Mode the operator chose when starting the session. Drives the browser
 * page's UI branch in P2 (generate → bip39.generateMnemonic; import →
 * paste textarea).
 */
export type PairSessionMode = 'generate' | 'import';

/**
 * Lifecycle state. Transitions:
 *
 *   awaiting_scan    (created)
 *     → device_connected  (browser fetched /pair/start + verified code)
 *     → completed         (successful /pair/respond decrypt + creds write)
 *     → consumed          (alias for completed; single-use lockout)
 *     → expired           (TTL elapsed without a successful respond)
 *     → rejected          (secondary-code strikeout or explicit cancel)
 *
 * The CLI TUI polls for the transition from `awaiting_scan` to
 * `device_connected` so the "Phone connected..." message fires at the
 * right time.
 */
export type PairSessionStatus =
  | 'awaiting_scan'
  | 'device_connected'
  | 'completed'
  | 'consumed'
  | 'expired'
  | 'rejected';

/**
 * Operator context — who triggered the pairing session. Used for
 * confirmation delivery back to the triggering channel after a
 * successful pairing + for diagnostic logging. Contains NO secret
 * material.
 *
 * `channel` examples: "cli", "tui", "telegram", "webchat", "unknown".
 */
export interface PairOperatorContext {
  channel: string;
  senderId?: string;
  accountId?: string;
}

/**
 * Persistent record written to `~/.totalreclaw/pair-sessions.json`.
 *
 * All fields are stored as base64url ASCII where the source is binary.
 * Timestamps are milliseconds since epoch (ms) for trivial comparison.
 *
 * `skGatewayB64` is the gateway's ephemeral x25519 PRIVATE key. It is
 * stored in cleartext on disk under the session file's 0600 mode — the
 * attacker model here is "anyone who can read 0600 files owned by the
 * gateway user has root-equivalent anyway; they can also read
 * credentials.json". A rooted gateway host is explicitly out-of-scope
 * per design doc §5d.
 */
export interface PairSession {
  sid: string;
  skGatewayB64: string;
  pkGatewayB64: string;
  createdAtMs: number;
  expiresAtMs: number;
  /**
   * 6-digit numeric string shown to the operator in the triggering channel
   * and verified by the browser before the mnemonic phase. 5-strike
   * lockout handled by `registerFailedAttempt`.
   */
  secondaryCode: string;
  /** Count of wrong secondary-code submissions this session has seen. */
  secondaryCodeAttempts: number;
  operatorContext: PairOperatorContext;
  mode: PairSessionMode;
  status: PairSessionStatus;
  /** ISO timestamp of the last status transition. For debugging only. */
  lastStatusChangeAtMs: number;
}

/** On-disk blob: a plain array of sessions + a schema version. */
export interface PairSessionFile {
  version: number;
  sessions: PairSession[];
}

/** Options passed to `createSession`. */
export interface CreateSessionOptions {
  mode: PairSessionMode;
  operatorContext: PairOperatorContext;
  /**
   * Session TTL in ms. Default 15 minutes (900_000). Clamped to
   * [5 min, 60 min] per user ratification 2026-04-20 Q1.
   */
  ttlMs?: number;
  /** Override for tests. Returns 32 bytes of randomness. */
  rngPrivateKey?: () => Buffer;
  /** Override for tests. Returns 32 bytes of randomness. */
  rngPublicKey?: () => Buffer;
  /** Override for tests. Returns a 16-byte sid. */
  rngSid?: () => Buffer;
  /** Override for tests. Returns a numeric string in [100000, 999999]. */
  rngSecondaryCode?: () => string;
  /** Override for tests. Returns now() in ms. */
  now?: () => number;
}

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

/** Schema version of the pair-sessions.json file. Bump on shape change. */
export const PAIR_SESSION_FILE_VERSION = 1;

/** Default TTL: 15 minutes (per user ratification 2026-04-20 Q1). */
export const DEFAULT_PAIR_TTL_MS = 15 * 60 * 1000;

/** Minimum configurable TTL: 5 minutes. */
export const MIN_PAIR_TTL_MS = 5 * 60 * 1000;

/** Maximum configurable TTL: 60 minutes. */
export const MAX_PAIR_TTL_MS = 60 * 60 * 1000;

/** How long to keep completed/consumed/rejected sessions before evicting. */
export const TERMINAL_RETENTION_MS = 60 * 60 * 1000; // 1 hour

/** Maximum number of wrong secondary-code submissions before lockout. */
export const MAX_SECONDARY_CODE_ATTEMPTS = 5;

// ---------------------------------------------------------------------------
// Path helpers
// ---------------------------------------------------------------------------

/**
 * Build a pair-sessions path rooted at `baseDir`. Callers normally
 * resolve `baseDir` via `CONFIG.pairSessionsPath`'s parent directory
 * (see `config.ts`); tests pass a hermetic tmpdir.
 *
 * This helper intentionally does NOT read `process.env` — every env
 * var read in the plugin lives in `config.ts` so the scanner rules stay
 * satisfiable here (see module docstring).
 */
export function defaultPairSessionsPath(baseDir: string): string {
  return path.join(baseDir, 'pair-sessions.json');
}

// ---------------------------------------------------------------------------
// Default randomness helpers
// ---------------------------------------------------------------------------

/**
 * 16-byte session id → 32-hex-char string. Uniformly random; enough
 * entropy that collisions are cryptographically negligible, short enough
 * to fit comfortably in a QR URL (32 chars plus the pk fragment).
 */
function defaultRngSid(): Buffer {
  return randomBytes(16);
}

/**
 * Reject-sample a uniformly random 6-digit numeric code, left-padded.
 * Using `randomBytes` + modulo has a tiny bias for ranges that don't
 * divide 2**k evenly; we reject-sample to stay uniform. The bias is
 * irrelevant for the attacker model here (5-strike lockout) but uniform
 * is cheap and principled.
 */
function defaultRngSecondaryCode(): string {
  while (true) {
    const b = randomBytes(4);
    const n = b.readUInt32BE(0);
    if (n >= 4_294_967_000) continue; // trim the last partial bucket
    const code = n % 1_000_000;
    return String(code).padStart(6, '0');
  }
}

/** 32-byte RNG. Used for ephemeral x25519 keypair material in P3. */
function defaultRng32(): Buffer {
  return randomBytes(32);
}

// ---------------------------------------------------------------------------
// Lock primitive (cooperative exclusive-create sentinel)
// ---------------------------------------------------------------------------

/** Default stale-lock threshold. If a .lock file is older than this, we
 * force-break it on next acquire. 30s is generous for a pairing flow. */
export const LOCK_STALE_MS = 30_000;

/** Max time to wait for a lock, in ms. 10s — pairing is not latency-critical. */
export const LOCK_WAIT_MS = 10_000;

/** Between-retry sleep. Short enough to feel responsive, long enough not to spin. */
export const LOCK_RETRY_MS = 50;

/**
 * Ensure the parent directory of `sessionsPath` exists, creating it
 * (and any missing intermediates) with 0700 mode. This is called from
 * BOTH the lock-acquisition and the write paths — if we only create
 * the dir on write, a fresh install hits ENOENT on the lock's
 * `openSync(path, 'wx')` and spins the retry loop until deadline (rc.3
 * regression: QA-plugin-3.3.0-rc.3 report).
 *
 * Best-effort: a mkdir failure is re-thrown to the caller, which will
 * surface it via the lock-acquisition error path (for lock) or the
 * try/catch in `writePairSessionsFileSync` (for write). 0700 mode
 * matches the privacy posture of the sessions file (0600) — if the
 * user can read the directory they can already read the file.
 */
function ensureSessionsFileDir(sessionsPath: string): void {
  const dir = path.dirname(sessionsPath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
}

/**
 * Acquire an exclusive lock on the given sessions-file path by
 * atomically creating `<path>.lock` with `wx` mode. Retries up to
 * `LOCK_WAIT_MS`; breaks a lock older than `LOCK_STALE_MS`; returns
 * a release function.
 *
 * This is scope-limited to this module — we deliberately avoid
 * importing `withFileLock` from the plugin-sdk because that would pull
 * the OpenClaw runtime surface into the session-store file, and the
 * scanner rules treat that as a network-capable file. Keeping it tiny
 * and self-contained is safer than fighting the scanner.
 */
async function acquireSessionsFileLock(sessionsPath: string): Promise<() => void> {
  // Guarantee the parent directory exists BEFORE the first openSync(wx).
  // Without this, a fresh install where `~/.totalreclaw/` doesn't yet
  // exist gets ENOENT on every attempt, tight-loops until deadline, and
  // throws "could not acquire lock" — which the CLI surfaces as a hung
  // pair command with no QR / code / URL ever rendered (rc.3 blocker;
  // QA-plugin-3.3.0-rc.3 strace evidence in totalreclaw-internal#21).
  // `writePairSessionsFileSync` already creates the dir, but that path
  // is never reached because the lock never acquires.
  ensureSessionsFileDir(sessionsPath);

  const lockPath = `${sessionsPath}.lock`;
  const deadline = Date.now() + LOCK_WAIT_MS;

  while (true) {
    try {
      const fd = fs.openSync(lockPath, 'wx');
      fs.writeSync(fd, `${process.pid}\n`);
      fs.closeSync(fd);
      return () => {
        try {
          fs.unlinkSync(lockPath);
        } catch {
          // Lock already gone — fine.
        }
      };
    } catch (err: unknown) {
      // Lock exists. Check if it's stale.
      try {
        const st = fs.statSync(lockPath);
        if (Date.now() - st.mtimeMs > LOCK_STALE_MS) {
          // Break it.
          try {
            fs.unlinkSync(lockPath);
          } catch {
            // Race — someone else broke it first. Retry.
          }
          continue;
        }
      } catch {
        // Lock vanished between our open and stat — retry immediately.
        continue;
      }

      if (Date.now() >= deadline) {
        throw new Error(
          `pair-session-store: could not acquire lock at ${lockPath} within ${LOCK_WAIT_MS}ms`,
        );
      }
      await new Promise((r) => setTimeout(r, LOCK_RETRY_MS));
    }
  }
}

// ---------------------------------------------------------------------------
// Load / save (no lock — callers wrap via `withSessionsLock`)
// ---------------------------------------------------------------------------

function emptyFile(): PairSessionFile {
  return { version: PAIR_SESSION_FILE_VERSION, sessions: [] };
}

/**
 * Load the sessions file. Returns an empty file on any read/parse error
 * — the caller treats that as "no prior sessions exist" and starts
 * fresh. Any malformed shape is discarded without raising.
 *
 * This helper intentionally uses `readFileSync` — see module docstring
 * for why this file is safe to pair with that token (no outbound
 * request words anywhere in the file).
 */
export function loadPairSessionsFileSync(sessionsPath: string): PairSessionFile {
  try {
    if (!fs.existsSync(sessionsPath)) return emptyFile();
    const raw = fs.readFileSync(sessionsPath, 'utf-8');
    const parsed = JSON.parse(raw) as Partial<PairSessionFile>;
    if (
      typeof parsed !== 'object' ||
      parsed === null ||
      parsed.version !== PAIR_SESSION_FILE_VERSION ||
      !Array.isArray(parsed.sessions)
    ) {
      return emptyFile();
    }
    // Shape-validate each entry; drop malformed ones silently. The
    // caller's next prune pass would evict them anyway.
    const clean: PairSession[] = [];
    for (const s of parsed.sessions) {
      if (isValidSession(s)) clean.push(s as PairSession);
    }
    return { version: PAIR_SESSION_FILE_VERSION, sessions: clean };
  } catch {
    return emptyFile();
  }
}

/**
 * Atomic write: temp file + rename. Mode 0600 to match credentials.json
 * and state.json. Returns true on success, false on any I/O error.
 *
 * Best-effort: the caller treats false as "retry later" or "session
 * state may be lost; user will need to restart pairing" — failure is
 * never fatal because pairing sessions are ephemeral by design.
 */
export function writePairSessionsFileSync(
  sessionsPath: string,
  file: PairSessionFile,
): boolean {
  try {
    // Same ensureSessionsFileDir used by acquireSessionsFileLock so the
    // two paths can't drift.
    ensureSessionsFileDir(sessionsPath);
    const tmp = `${sessionsPath}.tmp-${process.pid}-${Date.now()}`;
    fs.writeFileSync(tmp, JSON.stringify(file), { mode: 0o600 });
    fs.renameSync(tmp, sessionsPath);
    return true;
  } catch {
    return false;
  }
}

function isValidSession(s: unknown): boolean {
  if (typeof s !== 'object' || s === null) return false;
  const r = s as Record<string, unknown>;
  return (
    typeof r.sid === 'string' &&
    r.sid.length > 0 &&
    typeof r.skGatewayB64 === 'string' &&
    typeof r.pkGatewayB64 === 'string' &&
    typeof r.createdAtMs === 'number' &&
    typeof r.expiresAtMs === 'number' &&
    typeof r.secondaryCode === 'string' &&
    /^\d{6}$/.test(r.secondaryCode) &&
    typeof r.secondaryCodeAttempts === 'number' &&
    typeof r.operatorContext === 'object' &&
    r.operatorContext !== null &&
    (r.mode === 'generate' || r.mode === 'import') &&
    typeof r.status === 'string' &&
    typeof r.lastStatusChangeAtMs === 'number'
  );
}

// ---------------------------------------------------------------------------
// Pruning — lazy, idempotent, called on every read path
// ---------------------------------------------------------------------------

/**
 * Drop expired sessions and terminal sessions older than the retention
 * window. Returns the pruned file plus the list of pruned sids (useful
 * for logging counts at the caller).
 *
 * Rules:
 *   - status=awaiting_scan or device_connected and now > expiresAtMs
 *     → flip to `expired` and keep for TERMINAL_RETENTION_MS.
 *   - any terminal status (completed / consumed / expired / rejected)
 *     and (now - lastStatusChangeAtMs) > TERMINAL_RETENTION_MS → drop.
 */
export function pruneStaleSessions(
  file: PairSessionFile,
  nowMs: number,
): { file: PairSessionFile; prunedSids: string[] } {
  const keepers: PairSession[] = [];
  const pruned: string[] = [];

  for (const s of file.sessions) {
    const isTerminal =
      s.status === 'completed' ||
      s.status === 'consumed' ||
      s.status === 'expired' ||
      s.status === 'rejected';

    // First, promote any active-but-expired sessions to expired. We
    // anchor `lastStatusChangeAtMs` to `expiresAtMs` (the actual moment
    // the session became expired, not the moment we happened to observe
    // it) so that a session observed long after expiry is dropped by
    // the retention check below rather than getting its retention clock
    // reset to "now".
    let next = s;
    if (!isTerminal && nowMs > s.expiresAtMs) {
      next = {
        ...s,
        status: 'expired',
        lastStatusChangeAtMs: s.expiresAtMs,
      };
    }

    const nowTerminal =
      next.status === 'completed' ||
      next.status === 'consumed' ||
      next.status === 'expired' ||
      next.status === 'rejected';

    if (nowTerminal && nowMs - next.lastStatusChangeAtMs > TERMINAL_RETENTION_MS) {
      pruned.push(next.sid);
      continue;
    }
    keepers.push(next);
  }

  return {
    file: { version: file.version, sessions: keepers },
    prunedSids: pruned,
  };
}

// ---------------------------------------------------------------------------
// Public API — all operations go through the lock
// ---------------------------------------------------------------------------

/** Clamp a caller-supplied TTL to the ratified bounds. */
export function clampTtlMs(ttlMs: number | undefined): number {
  const raw = typeof ttlMs === 'number' && ttlMs > 0 ? ttlMs : DEFAULT_PAIR_TTL_MS;
  return Math.max(MIN_PAIR_TTL_MS, Math.min(MAX_PAIR_TTL_MS, raw));
}

/**
 * Create a new session, persist it, return the in-memory record.
 *
 * Caller is responsible for:
 *   - Deriving `pk_G` from `sk_G` (done in P3 via `pair-crypto.ts`).
 *     In P1 this accepts pre-generated keypair material via the
 *     `rngPrivateKey` / `rngPublicKey` hooks OR returns a stub where
 *     the pubkey is a derived placeholder. The P3 module will replace
 *     the default generators with a real x25519-aware pair.
 *   - Ensuring the gateway has quiesced any prior in-flight sessions
 *     this user started (the session store itself does NOT enforce a
 *     single-active-session policy; that's P4's concern).
 */
export async function createPairSession(
  sessionsPath: string,
  opts: CreateSessionOptions,
): Promise<PairSession> {
  const now = (opts.now ?? Date.now)();
  const ttl = clampTtlMs(opts.ttlMs);
  const sidBuf = (opts.rngSid ?? defaultRngSid)();
  const skBuf = (opts.rngPrivateKey ?? defaultRng32)();
  const pkBuf = (opts.rngPublicKey ?? defaultRng32)();
  const secondaryCode = (opts.rngSecondaryCode ?? defaultRngSecondaryCode)();

  const session: PairSession = {
    sid: sidBuf.toString('hex'),
    skGatewayB64: skBuf.toString('base64url'),
    pkGatewayB64: pkBuf.toString('base64url'),
    createdAtMs: now,
    expiresAtMs: now + ttl,
    secondaryCode,
    secondaryCodeAttempts: 0,
    operatorContext: opts.operatorContext,
    mode: opts.mode,
    status: 'awaiting_scan',
    lastStatusChangeAtMs: now,
  };

  const release = await acquireSessionsFileLock(sessionsPath);
  try {
    const current = loadPairSessionsFileSync(sessionsPath);
    const pruned = pruneStaleSessions(current, now);
    pruned.file.sessions.push(session);
    writePairSessionsFileSync(sessionsPath, pruned.file);
  } finally {
    release();
  }

  return session;
}

/**
 * Look up a session by sid. Returns null on not-found, expired, or any
 * error. DOES return completed/consumed/rejected sessions so the HTTP
 * handler can distinguish 404 (genuinely absent) from 409/410 (terminal).
 *
 * Prunes stale entries as a side effect; this is cheap and keeps the
 * file from growing unbounded.
 */
export async function getPairSession(
  sessionsPath: string,
  sid: string,
  now: () => number = Date.now,
): Promise<PairSession | null> {
  const release = await acquireSessionsFileLock(sessionsPath);
  try {
    const file = loadPairSessionsFileSync(sessionsPath);
    const pruned = pruneStaleSessions(file, now());
    // Persist the prune if anything changed, but don't block on failure.
    if (pruned.prunedSids.length > 0) {
      writePairSessionsFileSync(sessionsPath, pruned.file);
    }
    return pruned.file.sessions.find((s) => s.sid === sid) ?? null;
  } finally {
    release();
  }
}

/**
 * Apply a mutation to a session. Re-reads under the lock, finds the
 * session by sid, calls the mutator, writes back. The mutator returns
 * the new session state (or null to drop the session entirely).
 *
 * Returns the resulting session (after the mutation) or null if the
 * mutator chose to drop it / the session wasn't found.
 *
 * Stale prune runs on the same lock acquisition, so callers never see
 * a session that should already be expired.
 */
export async function updatePairSession(
  sessionsPath: string,
  sid: string,
  mutate: (s: PairSession) => PairSession | null,
  now: () => number = Date.now,
): Promise<PairSession | null> {
  const release = await acquireSessionsFileLock(sessionsPath);
  try {
    const file = loadPairSessionsFileSync(sessionsPath);
    const pruned = pruneStaleSessions(file, now());
    const idx = pruned.file.sessions.findIndex((s) => s.sid === sid);
    if (idx < 0) {
      if (pruned.prunedSids.length > 0) {
        writePairSessionsFileSync(sessionsPath, pruned.file);
      }
      return null;
    }
    const current = pruned.file.sessions[idx];
    const next = mutate(current);
    let result: PairSession | null;
    if (next === null) {
      pruned.file.sessions.splice(idx, 1);
      result = null;
    } else {
      pruned.file.sessions[idx] = next;
      result = next;
    }
    writePairSessionsFileSync(sessionsPath, pruned.file);
    return result;
  } finally {
    release();
  }
}

/**
 * Transition a session's status. Convenience wrapper around
 * `updatePairSession`. Returns the new session or null if not found.
 */
export async function transitionPairSession(
  sessionsPath: string,
  sid: string,
  nextStatus: PairSessionStatus,
  now: () => number = Date.now,
): Promise<PairSession | null> {
  return updatePairSession(
    sessionsPath,
    sid,
    (s) => {
      if (s.status === nextStatus) return s;
      return {
        ...s,
        status: nextStatus,
        lastStatusChangeAtMs: now(),
      };
    },
    now,
  );
}

/**
 * Register a failed secondary-code attempt. Increments the counter.
 * Returns the updated session, or null if the session is gone. If the
 * attempt count reaches MAX_SECONDARY_CODE_ATTEMPTS, the session is
 * transitioned to `rejected` and the HTTP handler should return 403
 * + "too many attempts".
 *
 * The returned session's status reflects the incremented state —
 * callers can check `session.status === 'rejected'` after this returns
 * to know whether to lock the session out.
 */
export async function registerFailedSecondaryCode(
  sessionsPath: string,
  sid: string,
  now: () => number = Date.now,
): Promise<PairSession | null> {
  return updatePairSession(
    sessionsPath,
    sid,
    (s) => {
      const nextAttempts = s.secondaryCodeAttempts + 1;
      const shouldReject = nextAttempts >= MAX_SECONDARY_CODE_ATTEMPTS;
      return {
        ...s,
        secondaryCodeAttempts: nextAttempts,
        status: shouldReject ? 'rejected' : s.status,
        lastStatusChangeAtMs: shouldReject ? now() : s.lastStatusChangeAtMs,
      };
    },
    now,
  );
}

/**
 * Consume a session atomically: verify it is in a consumable state
 * (device_connected or awaiting_scan, not expired), flip to `consumed`,
 * and return the pre-transition session so the caller can use the
 * `skGatewayB64` one last time before it's retired.
 *
 * Returns:
 *   - the session (pre-transition) on success
 *   - `{ error: 'not_found' }` if sid absent
 *   - `{ error: 'expired' }` if TTL elapsed
 *   - `{ error: 'already_consumed' }` if status is completed/consumed
 *   - `{ error: 'rejected' }` if status is rejected (too many code
 *     failures or explicit cancel)
 *
 * The "consumed" flip happens BEFORE the caller does crypto work, so a
 * retrying duplicate request sees `already_consumed` and the
 * credentials-write logic doesn't race.
 */
export type ConsumeResult =
  | { ok: true; session: PairSession }
  | { ok: false; error: 'not_found' | 'expired' | 'already_consumed' | 'rejected' };

export async function consumePairSession(
  sessionsPath: string,
  sid: string,
  now: () => number = Date.now,
): Promise<ConsumeResult> {
  let outcome: ConsumeResult = { ok: false, error: 'not_found' };

  await updatePairSession(
    sessionsPath,
    sid,
    (s) => {
      const t = now();
      if (t > s.expiresAtMs) {
        outcome = { ok: false, error: 'expired' };
        return { ...s, status: 'expired', lastStatusChangeAtMs: t };
      }
      if (s.status === 'completed' || s.status === 'consumed') {
        outcome = { ok: false, error: 'already_consumed' };
        return s;
      }
      if (s.status === 'rejected' || s.status === 'expired') {
        outcome = { ok: false, error: s.status };
        return s;
      }
      // Success — flip to consumed and hand the PRE-transition session
      // back so the caller can derive the shared key one last time.
      outcome = { ok: true, session: s };
      return { ...s, status: 'consumed', lastStatusChangeAtMs: t };
    },
    now,
  );

  return outcome;
}

/**
 * Force a terminal status on a session (caller decides why). Used by
 * the CLI on Ctrl+C ("user canceled") and by P4's "already active →
 * refuse new pairing" guard. Returns the updated session or null.
 */
export async function rejectPairSession(
  sessionsPath: string,
  sid: string,
  now: () => number = Date.now,
): Promise<PairSession | null> {
  return transitionPairSession(sessionsPath, sid, 'rejected', now);
}

/**
 * List all non-terminal sessions. Primarily for the CLI "are any
 * pairings in flight?" check. Returns a defensive copy.
 */
export async function listActivePairSessions(
  sessionsPath: string,
  now: () => number = Date.now,
): Promise<PairSession[]> {
  const release = await acquireSessionsFileLock(sessionsPath);
  try {
    const file = loadPairSessionsFileSync(sessionsPath);
    const pruned = pruneStaleSessions(file, now());
    if (pruned.prunedSids.length > 0) {
      writePairSessionsFileSync(sessionsPath, pruned.file);
    }
    return pruned.file.sessions
      .filter((s) => s.status === 'awaiting_scan' || s.status === 'device_connected')
      .map((s) => ({ ...s }));
  } finally {
    release();
  }
}

/**
 * Debug utility — list ALL sessions (including terminal) for the
 * status CLI. Never logs or exposes the sk/pk material.
 */
export async function listAllPairSessions(
  sessionsPath: string,
  now: () => number = Date.now,
): Promise<PairSession[]> {
  const release = await acquireSessionsFileLock(sessionsPath);
  try {
    const file = loadPairSessionsFileSync(sessionsPath);
    const pruned = pruneStaleSessions(file, now());
    if (pruned.prunedSids.length > 0) {
      writePairSessionsFileSync(sessionsPath, pruned.file);
    }
    return pruned.file.sessions.map((s) => ({ ...s }));
  } finally {
    release();
  }
}

/**
 * Scrub sensitive fields from a session for safe logging / status
 * display. Returns a shallow clone with `skGatewayB64` and
 * `secondaryCode` replaced by "[redacted]". The pk, sid, status,
 * timestamps, mode, and operator-context are fine to log.
 */
export function redactPairSession(s: PairSession): PairSession {
  return {
    ...s,
    skGatewayB64: '[redacted]',
    secondaryCode: '[redacted]',
  };
}
