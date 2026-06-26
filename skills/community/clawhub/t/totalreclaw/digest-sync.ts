/**
 * TotalReclaw Plugin — digest read path (Stage 3b).
 *
 * Loads the latest digest claim from the subgraph, checks staleness, and
 * returns the pre-compiled `promptText` for injection into before_agent_start.
 * Triggers background recompilation (non-blocking) when the digest is stale
 * and the guard conditions (>=10 new claims OR >=24h) are met.
 *
 * The digest is stored on-chain as a regular encrypted fact where the
 * decrypted content is a canonical Claim with category="dig" and a
 * distinctive blind-index marker `DIGEST_TRAPDOOR`.
 */

import { createRequire } from 'node:module';
import {
  DIGEST_CLAIM_CAP,
  DIGEST_TRAPDOOR,
  buildDigestClaim,
  extractDigestFromClaim,
  hoursSince,
  isDigestStale,
  shouldRecompile,
  type DigestMode,
} from './claims-helper.js';

const requireWasm = createRequire(import.meta.url);
let _wasm: typeof import('@totalreclaw/core') | null = null;
function getWasm() {
  if (!_wasm) _wasm = requireWasm('@totalreclaw/core');
  return _wasm!;
}

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface DigestLogger {
  info: (msg: string) => void;
  warn: (msg: string) => void;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type ParsedDigest = any;

export interface LoadedDigest {
  digest: ParsedDigest;
  claimId: string;
  createdAt: number;
}

export interface EvaluateDigestStateInput {
  digestVersion: number;
  currentMaxCreatedAt: number;
  countNewClaims: number;
  hoursSinceCompilation: number;
}

export interface DigestState {
  stale: boolean;
  recompile: boolean;
}

export interface CompileDigestCoreInput {
  claimsJson: string;
  nowUnixSeconds: number;
  mode: DigestMode;
  /**
   * Optional LLM invocation. Receives the compiled prompt and must return
   * the raw model output. Throw on HTTP error or timeout — compileDigestCore
   * catches and falls back to the template path.
   */
  llmFn: ((prompt: string) => Promise<string>) | null;
  logger: DigestLogger;
}

// ---------------------------------------------------------------------------
// Stub / tombstone blob detection
// ---------------------------------------------------------------------------

/**
 * Is this subgraph-stored blob a supersede tombstone or other non-content
 * stub? The 3.0.7-rc.1 QA found that 7 of 25 facts on the QA wallet had
 * `encryptedBlob == "0x00"` — a 1-byte stub written as a supersede
 * tombstone. The digest pipeline attempted to decrypt these unconditionally
 * and produced 5 `Digest: decrypt failed … Encrypted data too short`
 * warnings per QA window.
 *
 * We deliberately ONLY short-circuit shapes that cannot plausibly contain
 * a real XChaCha20-Poly1305 payload — a valid ciphertext must be at
 * least 40 bytes (24B nonce + 16B tag). We stay conservative about
 * "short-but-non-stub" blobs: if someone's wire format changes and we
 * see a 30-byte blob, that's a legitimate decrypt-failure case worth
 * logging as a WARN, not silently skipping. So the check is:
 *
 *   - Empty string                        → stub
 *   - Just the `0x` / `0X` prefix         → stub
 *   - All-zero hex (e.g. "0x00", "00")    → stub (explicit tombstone)
 *
 * Anything else falls through to the decrypt attempt.
 *
 * Called from both `loadLatestDigest` (digest read path) and
 * `fetchAllActiveClaims` (digest recompile path).
 */
export function isStubBlob(hex: string): boolean {
  if (typeof hex !== 'string') return true;
  const stripped = (hex.startsWith('0x') || hex.startsWith('0X')) ? hex.slice(2) : hex;
  if (stripped.length === 0) return true;
  // All-zero hex is the explicit tombstone shape the relay emits
  // when marking a fact superseded (seen as "0x00" on the QA wallet,
  // but any "00...00" of any length is semantically the same).
  return /^0+$/i.test(stripped);
}

// ---------------------------------------------------------------------------
// Recompile-in-progress guard (in-memory, per-process)
// ---------------------------------------------------------------------------

let _recompileInProgress = false;

/** Is a digest recompilation currently running for this process? */
export function isRecompileInProgress(): boolean {
  return _recompileInProgress;
}

/** Attempt to acquire the recompile lock. Returns true on success. */
export function tryBeginRecompile(): boolean {
  if (_recompileInProgress) return false;
  _recompileInProgress = true;
  return true;
}

/** Release the recompile lock — always call in a finally block. */
export function endRecompile(): void {
  _recompileInProgress = false;
}

/** Test-only helper to reset module state between cases. */
export function __resetDigestSyncState(): void {
  _recompileInProgress = false;
}

// ---------------------------------------------------------------------------
// Pure staleness + guard evaluation
// ---------------------------------------------------------------------------

/**
 * Combine staleness + guard checks into one decision.
 *
 * The caller still needs to consult `isRecompileInProgress()` before firing
 * the background task — this function is purely about the digest's age.
 */
export function evaluateDigestState(input: EvaluateDigestStateInput): DigestState {
  const stale = isDigestStale(input.digestVersion, input.currentMaxCreatedAt);
  if (!stale) return { stale: false, recompile: false };
  const recompile = shouldRecompile({
    countNewClaims: input.countNewClaims,
    hoursSinceCompilation: input.hoursSinceCompilation,
  });
  return { stale: true, recompile };
}

// ---------------------------------------------------------------------------
// Core compilation (pure, no I/O)
// ---------------------------------------------------------------------------

/**
 * Compile a Digest JSON from an array of Claim JSON.
 *
 * - `mode === 'template'` or `llmFn === null` → template path.
 * - `mode === 'on'` with a non-null `llmFn` → LLM path with template fallback.
 *   Any parsing/assembly/LLM failure logs a warning and falls back silently.
 * - Claim count above DIGEST_CLAIM_CAP forces the template path regardless
 *   of mode, to keep LLM token cost bounded.
 *
 * Returns the Digest JSON as produced by the WASM core.
 */
export async function compileDigestCore(input: CompileDigestCoreInput): Promise<string> {
  const { claimsJson, nowUnixSeconds, mode, llmFn, logger } = input;
  const core = getWasm();
  const nowBig = BigInt(Math.floor(nowUnixSeconds));

  // Check whether we should even attempt the LLM path.
  let useLlm = mode === 'on' && llmFn !== null;
  if (useLlm) {
    try {
      const parsedClaims = JSON.parse(claimsJson);
      if (!Array.isArray(parsedClaims) || parsedClaims.length === 0) {
        useLlm = false;
      } else if (parsedClaims.length > DIGEST_CLAIM_CAP) {
        logger.info(
          `Digest: ${parsedClaims.length} active claims > cap ${DIGEST_CLAIM_CAP}; using template path`,
        );
        useLlm = false;
      }
    } catch {
      useLlm = false;
    }
  }

  if (useLlm && llmFn) {
    try {
      const prompt = core.buildDigestPrompt(claimsJson);
      const raw = await llmFn(prompt);
      if (!raw || typeof raw !== 'string' || raw.trim().length === 0) {
        throw new Error('LLM returned empty response');
      }
      const parsedResponse = core.parseDigestResponse(raw);
      return core.assembleDigestFromLlm(parsedResponse, claimsJson, nowBig);
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      logger.warn(`Digest LLM compilation failed, falling back to template: ${msg}`);
      // fall through to template path
    }
  }

  return core.buildTemplateDigest(claimsJson, nowBig);
}

// ---------------------------------------------------------------------------
// I/O helpers — subgraph reads
// ---------------------------------------------------------------------------

/**
 * Find the latest digest claim on the subgraph for this owner, decrypt it,
 * and return the parsed Digest. Returns null when no digest exists, the
 * subgraph query fails, or the blob is not decryptable.
 *
 * The callback injection keeps this module easy to test — index.ts passes
 * in the real `searchSubgraph` + `decryptFromHex`, tests can pass fakes.
 */
export interface LoadLatestDigestDeps {
  searchSubgraph: (
    owner: string,
    trapdoors: string[],
    maxCandidates: number,
    authKeyHex: string,
  ) => Promise<Array<{ id: string; encryptedBlob: string; createdAt?: string; timestamp?: string }>>;
  decryptFromHex: (hex: string, key: Buffer) => string;
}

export async function loadLatestDigest(
  owner: string,
  authKeyHex: string,
  encryptionKey: Buffer,
  deps: LoadLatestDigestDeps,
  logger: DigestLogger,
): Promise<LoadedDigest | null> {
  let results: Awaited<ReturnType<typeof deps.searchSubgraph>>;
  try {
    results = await deps.searchSubgraph(owner, [DIGEST_TRAPDOOR], 10, authKeyHex);
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    logger.warn(`Digest: subgraph query failed: ${msg}`);
    return null;
  }
  if (!results || results.length === 0) return null;

  // Pick the highest createdAt (client-generated Unix seconds) among rows
  // with a real (non-stub) blob. Stub blobs are supersede tombstones —
  // see `isStubBlob` above; attempting to decrypt one produces a noisy
  // `Digest: decrypt failed … Encrypted data too short` WARN. We filter
  // them out pre-ranking so we prefer a slightly-older real digest over
  // a newer tombstone. If EVERY candidate is a stub, return null quietly.
  let best: { id: string; encryptedBlob: string; createdAt: number } | null = null;
  let stubCount = 0;
  for (const r of results) {
    if (isStubBlob(r.encryptedBlob)) {
      stubCount++;
      continue;
    }
    const createdAt = parseInt(r.createdAt ?? r.timestamp ?? '0', 10) || 0;
    if (!best || createdAt > best.createdAt) {
      best = { id: r.id, encryptedBlob: r.encryptedBlob, createdAt };
    }
  }
  if (!best) {
    if (stubCount > 0) {
      logger.info(`Digest: all ${stubCount} candidates were tombstone stubs — no digest available`);
    }
    return null;
  }

  try {
    const decrypted = deps.decryptFromHex(best.encryptedBlob, encryptionKey);
    const canonical = getWasm().parseClaimOrLegacy(decrypted);
    const digest = extractDigestFromClaim(canonical);
    if (!digest) {
      logger.warn(`Digest: blob ${best.id.slice(0, 10)}… did not parse as a digest claim`);
      return null;
    }
    return { digest, claimId: best.id, createdAt: best.createdAt };
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    logger.warn(`Digest: decrypt failed for ${best.id.slice(0, 10)}…: ${msg}`);
    return null;
  }
}

/**
 * Probe the subgraph for recency + new-claim signals in one query.
 *
 * Fetches the 10 most-recent active facts (sorted by timestamp DESC from the
 * broadened query), reads each row's `createdAt` (client-generated Unix
 * seconds), and returns:
 *
 *   - `maxCreatedAt`: the largest createdAt across the 10 rows (or 0 if none)
 *   - `countNewerThan(digestVersion)`: how many of the 10 have createdAt
 *     strictly greater than the digest's version; clamped at 10 by design
 *     (one query, one answer)
 *
 * That's enough to drive the §15.10 recompile guard: the 10-claim threshold
 * is exactly what the single query measures. Any user with more than 10 new
 * claims still trips the guard (we just saturate at 10 instead of knowing
 * the exact count, which doesn't matter — the guard fires either way).
 */
export interface DigestRecencyProbe {
  maxCreatedAt: number;
  countNewerThan(digestVersion: number): number;
}

export interface GetDigestRecencyProbeDeps {
  searchSubgraphBroadened: (
    owner: string,
    maxCandidates: number,
    authKeyHex: string,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  ) => Promise<Array<any>>;
}

/** How many recent facts we fetch to drive the recompile guard. */
export const DIGEST_RECENCY_PROBE_LIMIT = 10;

export async function getDigestRecencyProbe(
  owner: string,
  authKeyHex: string,
  deps: GetDigestRecencyProbeDeps,
): Promise<DigestRecencyProbe> {
  let results: Array<{ createdAt?: string; timestamp?: string }> = [];
  try {
    results = await deps.searchSubgraphBroadened(owner, DIGEST_RECENCY_PROBE_LIMIT, authKeyHex);
  } catch {
    return { maxCreatedAt: 0, countNewerThan: () => 0 };
  }
  if (!results || results.length === 0) {
    return { maxCreatedAt: 0, countNewerThan: () => 0 };
  }

  const createdAts: number[] = [];
  for (const r of results) {
    const ts = parseInt(r.createdAt ?? r.timestamp ?? '0', 10);
    if (!Number.isNaN(ts) && ts > 0) createdAts.push(ts);
  }
  const maxCreatedAt = createdAts.length > 0 ? Math.max(...createdAts) : 0;

  return {
    maxCreatedAt,
    countNewerThan(digestVersion: number): number {
      let n = 0;
      for (const ca of createdAts) if (ca > digestVersion) n++;
      return n;
    },
  };
}

/**
 * Fetch all active claims for this owner (up to limit), decrypt each,
 * parse as canonical Claim, and filter out infrastructure claims
 * (digest and entity categories) so only user-facing memories remain.
 *
 * Returns an array of canonical Claim JSON strings (not parsed objects),
 * suitable for passing directly to `buildDigestPrompt` / `buildTemplateDigest`
 * after JSON.stringify-ing the array. The helper wraps them in a JSON array.
 */
export interface FetchAllActiveClaimsDeps {
  searchSubgraphBroadened: (
    owner: string,
    maxCandidates: number,
    authKeyHex: string,
  ) => Promise<Array<{ id: string; encryptedBlob: string; isActive?: boolean }>>;
  decryptFromHex: (hex: string, key: Buffer) => string;
}

export async function fetchAllActiveClaims(
  owner: string,
  authKeyHex: string,
  encryptionKey: Buffer,
  limit: number,
  deps: FetchAllActiveClaimsDeps,
  logger: DigestLogger,
): Promise<string> {
  let rows: Awaited<ReturnType<typeof deps.searchSubgraphBroadened>>;
  try {
    rows = await deps.searchSubgraphBroadened(owner, limit, authKeyHex);
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    logger.warn(`Digest: fetchAllActiveClaims subgraph query failed: ${msg}`);
    return '[]';
  }
  if (!rows || rows.length === 0) return '[]';

  const claimsOut: unknown[] = [];
  for (const row of rows) {
    if (row.isActive === false) continue;
    // Stub / tombstone blobs (encryptedBlob == "0x00") will always fail
    // decrypt with `Encrypted data too short`. Skip pre-decrypt so we
    // don't spin up a WASM call path per stub — the QA wallet had 7 of
    // 25 facts as stubs, so this matters for recompile cost too.
    if (isStubBlob(row.encryptedBlob)) continue;
    try {
      const decrypted = deps.decryptFromHex(row.encryptedBlob, encryptionKey);
      const canonicalJson = getWasm().parseClaimOrLegacy(decrypted);
      const claim = JSON.parse(canonicalJson) as { c?: string };
      // Skip infrastructure claims — digest and entity records aren't user memories.
      if (claim.c === 'dig' || claim.c === 'ent') continue;
      claimsOut.push(claim);
    } catch {
      // Skip un-decryptable / un-parseable rows. Don't fail the whole compilation.
    }
  }
  return JSON.stringify(claimsOut);
}

// ---------------------------------------------------------------------------
// Build + inject logic (the full read path pipeline used by the hook)
// ---------------------------------------------------------------------------

export interface RecompileDigestDeps {
  /** Called with the canonical Claim JSON string of the new digest. */
  storeDigestClaim: (canonicalClaimJson: string, compiledAt: string) => Promise<void>;
  /** Tombstone the previous digest (best-effort; failures are non-fatal). */
  tombstoneDigest: (claimId: string) => Promise<void>;
  fetchAllActiveClaimsFn: () => Promise<string>;
  /** LLM invocation, or null when no LLM is configured. */
  llmFn: ((prompt: string) => Promise<string>) | null;
}

export interface RecompileDigestInput {
  mode: DigestMode;
  previousClaimId: string | null;
  nowUnixSeconds: number;
  deps: RecompileDigestDeps;
  logger: DigestLogger;
}

/**
 * Full recompile pipeline. Safe to fire-and-forget (never throws).
 *
 * Steps:
 *   1. Fetch all active claims (decrypted, filtered to user-facing categories)
 *   2. Compile via template or LLM (with template fallback)
 *   3. Wrap as a canonical Claim and encrypt + store on-chain
 *   4. Tombstone the previous digest (if any) so only one digest stays indexed
 *
 * The caller should call `tryBeginRecompile` before scheduling and
 * `endRecompile` in a finally. This function does not touch the guard itself.
 */
export async function recompileDigest(input: RecompileDigestInput): Promise<void> {
  const { mode, previousClaimId, nowUnixSeconds, deps, logger } = input;
  try {
    const claimsJson = await deps.fetchAllActiveClaimsFn();
    const digestJson = await compileDigestCore({
      claimsJson,
      nowUnixSeconds,
      mode,
      llmFn: deps.llmFn,
      logger,
    });
    const compiledAt = new Date(nowUnixSeconds * 1000).toISOString();
    const canonical = buildDigestClaim({ digestJson, compiledAt });
    await deps.storeDigestClaim(canonical, compiledAt);
    if (previousClaimId) {
      try {
        await deps.tombstoneDigest(previousClaimId);
      } catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        logger.warn(`Digest: tombstone of previous ${previousClaimId.slice(0, 10)}… failed: ${msg}`);
      }
    }
    logger.info(`Digest: recompiled and stored (compiledAt=${compiledAt})`);
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    logger.warn(`Digest: recompile failed: ${msg}`);
  }
}

// ---------------------------------------------------------------------------
// Top-level entry: maybeInjectDigest
// ---------------------------------------------------------------------------

export interface MaybeInjectDigestInput {
  owner: string;
  authKeyHex: string;
  encryptionKey: Buffer;
  mode: DigestMode;
  nowMs: number;
  loadDeps: LoadLatestDigestDeps;
  probeDeps: GetDigestRecencyProbeDeps;
  /** Fired (fire-and-forget) if the guard + state say so. */
  recompileFn: (previousClaimId: string | null) => void;
  logger: DigestLogger;
}

export interface MaybeInjectDigestResult {
  /** When non-null, the caller injects this string into `## Your Memory`. */
  promptText: string | null;
  /** For debugging / session debrief. */
  state: 'off' | 'fresh' | 'stale' | 'first-compile' | 'no-llm-yet';
}

/**
 * Top-level read path helper. Decides whether to return a promptText from
 * the latest digest, kicks off a background recompile when appropriate,
 * and never throws.
 *
 * If this returns `{ promptText: null }`, the caller must fall back to the
 * legacy individual-fact search path — digest injection is a fast path, not
 * a replacement.
 */
export async function maybeInjectDigest(
  input: MaybeInjectDigestInput,
): Promise<MaybeInjectDigestResult> {
  const {
    owner,
    authKeyHex,
    encryptionKey,
    mode,
    nowMs,
    loadDeps,
    probeDeps,
    recompileFn,
    logger,
  } = input;

  if (mode === 'off') {
    return { promptText: null, state: 'off' };
  }

  // Fetch the latest digest and the recency probe in parallel.
  const [loaded, probe] = await Promise.all([
    loadLatestDigest(owner, authKeyHex, encryptionKey, loadDeps, logger),
    getDigestRecencyProbe(owner, authKeyHex, probeDeps),
  ]);

  if (!loaded) {
    // No digest exists yet — schedule a first compile, fall back to legacy search.
    if (!isRecompileInProgress()) {
      recompileFn(null);
    }
    return { promptText: null, state: 'first-compile' };
  }

  const digestVersion = typeof loaded.digest.version === 'number'
    ? loaded.digest.version
    : parseInt(String(loaded.digest.version ?? 0), 10) || 0;
  const compiledAt = typeof loaded.digest.compiled_at === 'string' ? loaded.digest.compiled_at : '';

  const state = evaluateDigestState({
    digestVersion,
    currentMaxCreatedAt: probe.maxCreatedAt,
    countNewClaims: probe.countNewerThan(digestVersion),
    hoursSinceCompilation: hoursSince(compiledAt, nowMs),
  });

  if (state.stale && state.recompile && !isRecompileInProgress()) {
    recompileFn(loaded.claimId);
  }

  const promptText = typeof loaded.digest.prompt_text === 'string' ? loaded.digest.prompt_text : null;
  return {
    promptText,
    state: state.stale ? 'stale' : 'fresh',
  };
}
