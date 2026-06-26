/**
 * auto-pair-on-load — autonomously open a relay pair session when the
 * plugin loads without credentials, so the chat agent never has to guess
 * (or hallucinate) a pair URL.
 *
 * Background
 * ----------
 * Through 3.3.12 the plugin's only fallback on a fresh install was a log
 * line telling the user to run `openclaw totalreclaw onboard`. The chat
 * agent then guessed URLs / sessions from training data and shipped users
 * to dead links — Pop-OS QA (2026-05-10) saw an invented session ID,
 * 404/502 in the browser, and no recovery phrase generated.
 *
 * 3.3.13 flips the default: when register() finds no credentials, the
 * plugin opens its OWN relay session (the same one `tr pair --json` opens)
 * and writes URL + PIN + sid + expiry to
 * `~/.totalreclaw/.pair-pending.json`. A separate before_agent_start hook
 * (see `pair-pending-injection.ts`) reads that file and instructs the
 * agent to copy the values verbatim. There is no LLM-side string
 * generation in the path.
 *
 * Phrase safety
 * -------------
 * The recovery phrase is NEVER written to the sentinel. The background
 * WS listener (awaitPhraseUpload) writes the decrypted mnemonic directly
 * to credentials.json — the same code path the `totalreclaw_pair` tool
 * and the `tr pair --json` CLI already use. The sentinel only holds URL,
 * PIN, sid, and expiry — all values the user already needs to see in
 * chat to complete the flow.
 *
 * Idempotency / TTL
 * -----------------
 * - credentials.json present → no-op
 * - valid non-expired sentinel → no-op (reuse existing session)
 * - expired sentinel → delete + open fresh session
 * - no sentinel → open fresh session
 *
 * Scanner scope
 * -------------
 * This file MUST NOT import `node:fs` directly. All disk I/O is delegated
 * to `fs-helpers.ts`. We DO import `pair-remote-client.js`, which opens a
 * WebSocket — but that file already passes the scanner (no readFile*).
 */
import { validateMnemonic } from '@scure/bip39';
import { wordlist } from '@scure/bip39/wordlists/english.js';
import { deletePairPendingFile, defaultPairPendingPath, loadCredentialsJson, loadPairPendingFile, writeCredentialsJson, writePairPendingFile, writeOnboardingState, } from './fs-helpers.js';
import { awaitPhraseUpload, openRemotePairSession, } from './pair-remote-client.js';
import { setRecoveryPhraseOverride } from './config.js';
// ---------------------------------------------------------------------------
// Public entrypoint
// ---------------------------------------------------------------------------
/**
 * Check the credentials + pending-sentinel state and, if needed, open a
 * fresh relay pair session. Idempotent under concurrent calls in the same
 * gateway process — repeated calls within the TTL reuse the existing
 * sentinel (no second session is opened).
 *
 * Returns immediately after writing the sentinel. The background WS
 * listener that drains the encrypted phrase + writes credentials.json is
 * kicked off via `void (async () => ...)()` so register() can finish
 * synchronously.
 */
export async function maybeStartAutoPair(deps) {
    const now = deps.now ?? Date.now;
    const pendingPath = deps.pendingPath ?? defaultPairPendingPath(deps.credentialsPath);
    const logger = deps.logger;
    // 1. credentials.json present → setup already complete; clean up any
    //    stale sentinel and return early.
    const creds = loadCredentialsJson(deps.credentialsPath);
    if (creds && (typeof creds.mnemonic === 'string' || typeof creds.recovery_phrase === 'string')) {
        if (deletePairPendingFile(pendingPath)) {
            logger.info('auto-pair-on-load: credentials present, cleared stale pending sentinel');
        }
        return { status: 'creds_exist' };
    }
    // 2. Valid non-expired sentinel → reuse it. The background WS listener
    //    from the original call is presumed alive; if the gateway restarted
    //    we cannot resurrect that listener but we leave the sentinel alone
    //    so the existing PIN keeps working until the user navigates to the
    //    URL. (If the listener died, the relay will time out the session;
    //    on next plugin reload after expiry we open a fresh one.)
    const existing = loadPairPendingFile(pendingPath);
    if (existing && existing.expires_at_ms > now()) {
        logger.info(`auto-pair-on-load: reusing pending pair sentinel (sid=${existing.sid.slice(0, 8)}…, expires in ${Math.round((existing.expires_at_ms - now()) / 1000)}s)`);
        return { status: 'pending_reused', pending: existing };
    }
    // 3. Expired sentinel → drop it before opening a new session so we never
    //    leave two competing files on disk.
    if (existing) {
        deletePairPendingFile(pendingPath);
        logger.info('auto-pair-on-load: pending sentinel expired, opening fresh session');
    }
    // 4. Open a new relay session. This is the same call path as
    //    `tr pair --json` and the `totalreclaw_pair` tool handler.
    const mode = deps.mode ?? 'generate';
    let session;
    try {
        const opener = deps.openSession ?? openRemotePairSession;
        session = await opener({ relayBaseUrl: deps.relayBaseUrl, mode });
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        logger.warn(`auto-pair-on-load: failed to open relay session: ${msg}`);
        return { status: 'failed', error: msg };
    }
    // ISO-8601 -> ms.  If the relay omits the field we fall back to 5 min.
    const parsedExpiresMs = Date.parse(session.expiresAt);
    const expiresAtMs = Number.isFinite(parsedExpiresMs)
        ? parsedExpiresMs
        : now() + 5 * 60_000;
    const payload = {
        v: 1,
        url: session.url,
        pin: session.pin,
        sid: session.token,
        expires_at_ms: expiresAtMs,
        created_at_ms: now(),
        mode,
    };
    if (!writePairPendingFile(pendingPath, payload)) {
        logger.warn('auto-pair-on-load: failed to write .pair-pending.json sentinel');
        // Best-effort: try to close the WS so we don't leak it.
        try {
            session._ws.close();
        }
        catch {
            /* ignore */
        }
        return { status: 'failed', error: 'pending_write_failed' };
    }
    logger.info(`auto-pair-on-load: opened pair session (sid=${session.token.slice(0, 8)}…, expires in ${Math.round((expiresAtMs - now()) / 1000)}s); sentinel written`);
    // 5. Kick off the background WS listener. On success it writes
    //    credentials.json + deletes the sentinel. `void` so register()
    //    returns immediately.
    void runBackgroundAwait({
        session,
        deps,
        pendingPath,
        mode,
    });
    return { status: 'started', pending: payload };
}
async function runBackgroundAwait(opts) {
    const { session, deps, pendingPath, mode } = opts;
    const timeoutMs = deps.awaitTimeoutMs ?? 5 * 60_000;
    const logger = deps.logger;
    const onComplete = async (mnemonic) => {
        const existingCreds = loadCredentialsJson(deps.credentialsPath) ?? {};
        const next = { ...existingCreds, mnemonic };
        if (!writeCredentialsJson(deps.credentialsPath, next)) {
            throw new Error('credentials_write_failed');
        }
        setRecoveryPhraseOverride(mnemonic);
        writeOnboardingState(deps.onboardingStatePath, {
            onboardingState: 'active',
            createdBy: mode === 'generate' ? 'generate' : 'import',
            credentialsCreatedAt: new Date().toISOString(),
            version: deps.pluginVersion,
        });
        // Sentinel is consumed — drop it so the before_agent_start hook
        // stops surfacing the URL on the next turn.
        deletePairPendingFile(pendingPath);
        logger.info(`auto-pair-on-load: pair completed (sid=${session.token.slice(0, 8)}…); credentials written, sentinel cleared`);
    };
    if (deps.awaitPhrase) {
        try {
            await deps.awaitPhrase(session, onComplete);
        }
        catch (err) {
            const msg = err instanceof Error ? err.message : String(err);
            logger.warn(`auto-pair-on-load: background await failed: ${msg}`);
        }
        return;
    }
    try {
        await awaitPhraseUpload(session, {
            phraseValidator: (p) => validateMnemonic(p, wordlist),
            completePairing: async ({ mnemonic }) => {
                try {
                    await onComplete(mnemonic);
                    return { state: 'active' };
                }
                catch (err) {
                    const msg = err instanceof Error ? err.message : String(err);
                    logger.error(`auto-pair-on-load: completePairing failed: ${msg}`);
                    return { state: 'error', error: msg };
                }
            },
            timeoutMs,
        });
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        // Expected on TTL expiry or user abandon — warn not error.
        logger.warn(`auto-pair-on-load: background task ended (sid=${session.token.slice(0, 8)}…): ${msg}`);
    }
}
