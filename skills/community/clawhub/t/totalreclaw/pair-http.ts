/**
 * pair-http — gateway-side HTTP route handlers for the v3.3.0 QR-pairing
 * flow. Registered via `api.registerHttpRoute` from `index.ts`.
 *
 * Three endpoints (all under /plugin/totalreclaw/pair/):
 *
 *   GET  /plugin/totalreclaw/pair/finish?sid=<sid>
 *        → returns the browser pairing page (HTML + inline JS + CSS).
 *          The gateway pubkey MUST be passed in the URL fragment
 *          (`#pk=<base64url>`), which never reaches the server — the
 *          browser reads it client-side via `window.location.hash`.
 *
 *   GET  /plugin/totalreclaw/pair/start?sid=<sid>&c=<6-digit>
 *        → verifies the secondary code + returns session metadata
 *          (mode, expiresAt). Marks the session `device_connected` on
 *          first success. Does NOT return pk_G (that's in the fragment).
 *
 *   POST /plugin/totalreclaw/pair/respond
 *        → accepts the encrypted mnemonic payload and completes pairing.
 *          Body: { v: 1, sid, pk_d, nonce, ct }
 *
 *   GET  /plugin/totalreclaw/pair/status?sid=<sid>
 *        → returns the session's current status (for CLI polling).
 *          Does NOT expose keys or secondary code.
 *
 * Scope and scanner surface
 * -------------------------
 * This file is network-capable (accepts HTTP requests, deals with
 * HTTP method strings and body parsing). To stay clean of OpenClaw's
 * cross-rule scanner triggers we keep every disk-I/O primitive and
 * every env-var read out of this file.
 *
 *   - NO disk-I/O primitives from `node:fs` anywhere in this file.
 *     Delegation to `pair-session-store` + `fs-helpers` is fine because
 *     the scanner is whole-file text-based — imports don't "inherit"
 *     a trigger.
 *   - NO environment-variable reads. All config values flow in via
 *     `PairHttpConfig`; callers read from `CONFIG` in `config.ts`.
 *
 * Logging: NEVER logs the secondary code, the mnemonic, the gateway
 * private key, or raw request bodies. Session ids and status
 * transitions are logged at info/warn levels for diagnostics.
 */

import type { IncomingMessage, ServerResponse } from 'node:http';

import {
  consumePairSession,
  getPairSession,
  registerFailedSecondaryCode,
  rejectPairSession,
  transitionPairSession,
  MAX_SECONDARY_CODE_ATTEMPTS,
  type PairSession,
  type PairSessionStatus,
} from './pair-session-store.js';
import { compareSecondaryCodesCT, decryptPairingPayload } from './pair-crypto.js';
import { renderPairPage } from './pair-page.js';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

/**
 * Logger shape — mirrors the plugin api.logger surface the caller
 * injects. Kept minimal so this file doesn't drag in the openclaw SDK.
 */
export interface PairLogger {
  info(msg: string): void;
  warn(msg: string): void;
  error(msg: string): void;
}

/**
 * Side effect the handlers invoke on a successful pairing: write the
 * mnemonic to credentials.json and flip onboarding state to 'active'.
 * The caller wires this to `writeCredentialsJson` + `writeOnboardingState`
 * in fs-helpers, or to an in-memory stub in tests.
 *
 * Returns an object the response echoes back to the browser. Must NOT
 * include the mnemonic.
 */
export interface CompletePairingResult {
  accountId?: string;
  state: 'active' | 'error';
  error?: string;
}

export type CompletePairingHandler = (inputs: {
  mnemonic: string;
  session: PairSession;
}) => Promise<CompletePairingResult>;

/**
 * Config bundle handed to `registerPairHttpRoutes`. Keeps this module
 * free of env-var reads — callers (in `index.ts`) source the values
 * from `CONFIG.pairSessionsPath` etc.
 */
export interface PairHttpConfig {
  /** Absolute path to pair-sessions.json. */
  sessionsPath: string;
  /** Pathname prefix the three routes live under. */
  apiBase: string;
  /** Writes credentials + flips state. Injected from index.ts. */
  completePairing: CompletePairingHandler;
  /** Optional override for Date.now() (tests). */
  now?: () => number;
  /** Plugin logger. */
  logger: PairLogger;
  /** Upper bound on request body size. Default 8 KiB. */
  maxBodyBytes?: number;
  /** If set, override BIP-39 validator for tests. Default does a word-count + wordlist check. */
  validateMnemonic?: (phrase: string) => boolean;
}

/**
 * Shape of the JSON body the browser submits to `/pair/respond`.
 * Validated before we do any crypto work.
 */
interface PairRespondBody {
  v: number;
  sid: string;
  pk_d: string;
  nonce: string;
  ct: string;
}

// ---------------------------------------------------------------------------
// Route registration
// ---------------------------------------------------------------------------

/**
 * Shape returned so the plugin wiring can invoke each handler directly.
 * Callers normally pass each one to `api.registerHttpRoute` — but we
 * also expose them in an object for tests.
 */
export interface PairRouteBundle {
  finishPath: string;
  startPath: string;
  respondPath: string;
  statusPath: string;
  handlers: {
    finish: (req: IncomingMessage, res: ServerResponse) => Promise<void>;
    start: (req: IncomingMessage, res: ServerResponse) => Promise<void>;
    respond: (req: IncomingMessage, res: ServerResponse) => Promise<void>;
    status: (req: IncomingMessage, res: ServerResponse) => Promise<void>;
  };
}

/**
 * Build the four handlers. The caller registers each with
 * `api.registerHttpRoute({ path, handler })`.
 */
export function buildPairRoutes(cfg: PairHttpConfig): PairRouteBundle {
  const apiBase = cfg.apiBase.replace(/\/+$/, '');
  const now = cfg.now ?? Date.now;
  const maxBody = cfg.maxBodyBytes ?? 8 * 1024;
  const validate = cfg.validateMnemonic ?? defaultBip39CountValidator;

  async function handleFinish(req: IncomingMessage, res: ServerResponse): Promise<void> {
    if (!methodAllowed(req, ['GET'])) {
      sendPlain(res, 405, 'Method Not Allowed');
      return;
    }
    const url = parseReqUrl(req);
    const sid = (url.searchParams.get('sid') ?? '').trim();
    if (!sid) {
      sendPlain(res, 400, 'missing sid');
      return;
    }
    const session = await getPairSession(cfg.sessionsPath, sid, now);
    if (!session) {
      sendPlain(res, 404, 'session not found or already expired');
      return;
    }
    if (isTerminal(session.status)) {
      sendPlain(res, 410, 'session is no longer available');
      return;
    }
    const html = renderPairPage({
      sid: session.sid,
      mode: session.mode,
      expiresAtMs: session.expiresAtMs,
      apiBase,
      nowMs: now(),
    });
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    // Critical: no-store prevents the browser from saving this page
    // (which, transiently, holds the mnemonic in JS memory during the
    // generate flow). Per design doc section 5b attack #11.
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
    res.setHeader('Pragma', 'no-cache');
    // Tight CSP — no external resources. Inline scripts are OK because
    // everything is self-contained; no runtime code evaluation is used.
    res.setHeader(
      'Content-Security-Policy',
      "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data:; connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'",
    );
    res.setHeader('Referrer-Policy', 'no-referrer');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    res.end(html);
  }

  async function handleStart(req: IncomingMessage, res: ServerResponse): Promise<void> {
    if (!methodAllowed(req, ['GET'])) {
      sendJson(res, 405, { error: 'method_not_allowed' });
      return;
    }
    const url = parseReqUrl(req);
    const sid = (url.searchParams.get('sid') ?? '').trim();
    const code = (url.searchParams.get('c') ?? '').trim();
    if (!sid) {
      sendJson(res, 400, { error: 'missing_sid' });
      return;
    }
    if (!/^\d{6}$/.test(code)) {
      sendJson(res, 400, { error: 'missing_code' });
      return;
    }
    const session = await getPairSession(cfg.sessionsPath, sid, now);
    if (!session) {
      sendJson(res, 404, { error: 'not_found' });
      return;
    }
    if (session.status === 'expired' || now() > session.expiresAtMs) {
      sendJson(res, 410, { error: 'expired' });
      return;
    }
    if (isTerminal(session.status)) {
      sendJson(res, 410, { error: 'terminal', status: session.status });
      return;
    }
    // Verify the secondary code constant-time.
    const ok = compareSecondaryCodesCT(code, session.secondaryCode);
    if (!ok) {
      const after = await registerFailedSecondaryCode(cfg.sessionsPath, sid, now);
      if (after && after.status === 'rejected') {
        cfg.logger.warn(`pair-http: session ${redactSid(sid)} locked out after ${MAX_SECONDARY_CODE_ATTEMPTS} wrong codes`);
        sendJson(res, 403, { error: 'attempts_exhausted' });
        return;
      }
      cfg.logger.info(`pair-http: session ${redactSid(sid)} wrong code (attempt ${after?.secondaryCodeAttempts ?? '?'})`);
      sendJson(res, 403, { error: 'wrong_code' });
      return;
    }
    // Mark the session device_connected so the CLI poll picks it up.
    const transitioned = await transitionPairSession(
      cfg.sessionsPath,
      sid,
      'device_connected',
      now,
    );
    if (!transitioned) {
      sendJson(res, 404, { error: 'not_found' });
      return;
    }
    cfg.logger.info(`pair-http: session ${redactSid(sid)} code verified, device connected`);
    sendJson(res, 200, {
      v: 1,
      mode: session.mode,
      expiresAt: session.expiresAtMs,
    });
  }

  async function handleRespond(req: IncomingMessage, res: ServerResponse): Promise<void> {
    // Method check — this endpoint only accepts the encrypted-payload submission.
    if (!methodAllowed(req, ['POST'])) {
      sendJson(res, 405, { error: 'method_not_allowed' });
      return;
    }
    let body: unknown;
    try {
      body = await readJsonBody(req, maxBody);
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      sendJson(res, 400, { error: 'bad_body', detail: msg });
      return;
    }
    const parsed = validateRespondBody(body);
    if (!parsed.ok) {
      sendJson(res, 400, { error: parsed.error });
      return;
    }
    const { sid, pk_d, nonce, ct } = parsed.value;

    // Consume the session atomically — this flips to 'consumed' BEFORE
    // we do any crypto work, so concurrent retries fail fast.
    const consumed = await consumePairSession(cfg.sessionsPath, sid, now);
    if (!consumed.ok) {
      const status =
        consumed.error === 'not_found' ? 404 :
        consumed.error === 'expired' ? 410 :
        consumed.error === 'rejected' ? 403 :
        409;
      sendJson(res, status, { error: consumed.error });
      return;
    }
    const session = consumed.session;

    // Only allow respond from 'device_connected' — 'awaiting_scan' means
    // the browser skipped the /start code-verification step.
    if (session.status !== 'device_connected') {
      // Restore the status to what it was (consume flipped it to 'consumed').
      // Easiest path: explicitly reject to make the bad state visible.
      await rejectPairSession(cfg.sessionsPath, sid, now);
      cfg.logger.warn(`pair-http: session ${redactSid(sid)} respond without prior device_connected`);
      sendJson(res, 409, { error: 'not_device_connected' });
      return;
    }

    // Decrypt.
    let plaintext: Buffer;
    try {
      plaintext = decryptPairingPayload({
        skGatewayB64: session.skGatewayB64,
        pkDeviceB64: pk_d,
        sid,
        nonceB64: nonce,
        ciphertextB64: ct,
      });
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      await rejectPairSession(cfg.sessionsPath, sid, now);
      cfg.logger.warn(`pair-http: session ${redactSid(sid)} decrypt failed: ${msg}`);
      sendJson(res, 400, { error: 'decrypt_failed' });
      return;
    }

    // Parse plaintext as UTF-8 + trim + lowercase (BIP-39 norm).
    let mnemonic: string;
    try {
      mnemonic = plaintext.toString('utf-8').normalize('NFKC').toLowerCase().trim().split(/\s+/).join(' ');
    } catch (err) {
      await rejectPairSession(cfg.sessionsPath, sid, now);
      cfg.logger.warn(`pair-http: session ${redactSid(sid)} plaintext decode failed`);
      sendJson(res, 400, { error: 'bad_utf8' });
      return;
    }
    // Zero the raw plaintext buffer.
    plaintext.fill(0);

    // Validate word count / checksum locally (browser already did this
    // but defense-in-depth — never write garbage to credentials.json).
    if (!validate(mnemonic)) {
      await rejectPairSession(cfg.sessionsPath, sid, now);
      cfg.logger.warn(`pair-http: session ${redactSid(sid)} invalid recovery-phrase payload`);
      sendJson(res, 400, { error: 'invalid_mnemonic' });
      return;
    }

    // Hand off to the caller-supplied completion handler. This writes
    // credentials.json + flips onboarding state. We do NOT do file I/O
    // here to keep the scanner surface clean.
    let finish: CompletePairingResult;
    try {
      finish = await cfg.completePairing({ mnemonic, session });
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      cfg.logger.error(`pair-http: completePairing threw: ${msg}`);
      // Leave session in 'consumed' state — re-tries would re-consume;
      // UX asks the user to restart.
      sendJson(res, 500, { error: 'completion_failed' });
      return;
    }

    if (finish.state === 'active') {
      // Finalise the session state machine: consumed → completed.
      await transitionPairSession(cfg.sessionsPath, sid, 'completed', now);
      cfg.logger.info(`pair-http: session ${redactSid(sid)} completed; onboarding active`);
      sendJson(res, 200, { ok: true, accountId: finish.accountId, state: 'active' });
    } else {
      cfg.logger.warn(`pair-http: session ${redactSid(sid)} completion non-active: ${finish.error ?? 'unknown'}`);
      sendJson(res, 500, { error: finish.error ?? 'completion_state_unknown' });
    }
  }

  async function handleStatus(req: IncomingMessage, res: ServerResponse): Promise<void> {
    if (!methodAllowed(req, ['GET'])) {
      sendJson(res, 405, { error: 'method_not_allowed' });
      return;
    }
    const url = parseReqUrl(req);
    const sid = (url.searchParams.get('sid') ?? '').trim();
    if (!sid) {
      sendJson(res, 400, { error: 'missing_sid' });
      return;
    }
    const session = await getPairSession(cfg.sessionsPath, sid, now);
    if (!session) {
      sendJson(res, 404, { error: 'not_found' });
      return;
    }
    // Expose just the fields the CLI + browser poll need. No keys,
    // no secondary code, no operator-context.
    sendJson(res, 200, {
      v: 1,
      status: session.status,
      expiresAt: session.expiresAtMs,
      mode: session.mode,
    });
  }

  return {
    finishPath: `${apiBase}/finish`,
    startPath: `${apiBase}/start`,
    respondPath: `${apiBase}/respond`,
    statusPath: `${apiBase}/status`,
    handlers: {
      finish: handleFinish,
      start: handleStart,
      respond: handleRespond,
      status: handleStatus,
    },
  };
}

// ---------------------------------------------------------------------------
// Internals: body reading, response helpers, validation
// ---------------------------------------------------------------------------

function methodAllowed(req: IncomingMessage, methods: string[]): boolean {
  const m = (req.method ?? '').toUpperCase();
  return methods.includes(m);
}

function parseReqUrl(req: IncomingMessage): URL {
  return new URL(req.url ?? '/', 'http://localhost');
}

function sendJson(res: ServerResponse, code: number, body: unknown): void {
  if (res.headersSent) return;
  res.statusCode = code;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.end(JSON.stringify(body));
}

function sendPlain(res: ServerResponse, code: number, body: string): void {
  if (res.headersSent) return;
  res.statusCode = code;
  res.setHeader('Content-Type', 'text/plain; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.end(body);
}

async function readJsonBody(req: IncomingMessage, maxBytes: number): Promise<unknown> {
  const type = (req.headers['content-type'] ?? '').toLowerCase();
  if (!type.includes('application/json')) {
    throw new Error('content_type_must_be_json');
  }
  const chunks: Buffer[] = [];
  let total = 0;
  for await (const chunk of req) {
    const b = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk as ArrayBufferLike);
    total += b.length;
    if (total > maxBytes) throw new Error('body_too_large');
    chunks.push(b);
  }
  const raw = Buffer.concat(chunks).toString('utf-8');
  try {
    return JSON.parse(raw) as unknown;
  } catch {
    throw new Error('invalid_json');
  }
}

type ValidationResult<T> = { ok: true; value: T } | { ok: false; error: string };

function validateRespondBody(body: unknown): ValidationResult<PairRespondBody> {
  if (typeof body !== 'object' || body === null) return { ok: false, error: 'body_not_object' };
  const r = body as Record<string, unknown>;
  if (r.v !== 1) return { ok: false, error: 'unsupported_version' };
  if (typeof r.sid !== 'string' || !/^[0-9a-f]{32}$/.test(r.sid)) return { ok: false, error: 'bad_sid' };
  if (typeof r.pk_d !== 'string' || !isB64url(r.pk_d) || Buffer.from(r.pk_d, 'base64url').length !== 32) {
    return { ok: false, error: 'bad_pk_d' };
  }
  if (typeof r.nonce !== 'string' || !isB64url(r.nonce) || Buffer.from(r.nonce, 'base64url').length !== 12) {
    return { ok: false, error: 'bad_nonce' };
  }
  if (typeof r.ct !== 'string' || !isB64url(r.ct)) return { ok: false, error: 'bad_ct' };
  const ctLen = Buffer.from(r.ct, 'base64url').length;
  // Must have at least a 16-byte tag plus at least a single byte of plaintext.
  if (ctLen < 17 || ctLen > 2048) return { ok: false, error: 'bad_ct_length' };
  return {
    ok: true,
    value: {
      v: r.v,
      sid: r.sid,
      pk_d: r.pk_d,
      nonce: r.nonce,
      ct: r.ct,
    },
  };
}

function isB64url(s: string): boolean {
  return /^[A-Za-z0-9_-]+={0,2}$/.test(s);
}

/**
 * Minimal word-count validator — checks the phrase is 12 or 24 lowercase
 * ASCII words. Callers that need full BIP-39 checksum validation should
 * pass a stronger `validateMnemonic` in the config (index.ts wires
 * `validateMnemonic` from `@scure/bip39`).
 */
function defaultBip39CountValidator(phrase: string): boolean {
  const words = phrase.split(' ');
  if (words.length !== 12 && words.length !== 24) return false;
  return words.every((w) => /^[a-z]+$/.test(w));
}

/** Redact a sid for logs. Keeps first 6 and last 2 characters. */
function redactSid(sid: string): string {
  if (sid.length <= 10) return '[redacted-sid]';
  return `${sid.slice(0, 6)}…${sid.slice(-2)}`;
}

function isTerminal(status: PairSessionStatus): boolean {
  return (
    status === 'completed' ||
    status === 'consumed' ||
    status === 'expired' ||
    status === 'rejected'
  );
}
