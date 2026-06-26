/**
 * pair-cli-relay — relay-mode runner for the `openclaw totalreclaw pair`
 * CLI subcommand (3.3.4-rc.1).
 *
 * Background
 * ----------
 * The CLI default through 3.3.3-rc.1 was the loopback / LAN URL flow
 * (`pair-cli.ts` `runPairCli` + `pair-session-store`). On Docker
 * deployments — i.e. the rc.6+ default — that emits `http://localhost:18789/…`
 * which is unreachable from the user's browser. QA on 3.3.3-rc.1 (Pedro
 * 2026-04-30) confirmed this is the *primary* CLI-fallback failure mode:
 * agent loses the `totalreclaw_pair` tool binding, falls back to
 * `openclaw totalreclaw pair generate --url-pin-only`, gets a localhost
 * URL, user can't open it.
 *
 * 3.3.4-rc.1 flips the CLI default to relay-mode. This file implements
 * the runner. It mirrors the relay flow already used by the agent tool
 * (`index.ts` `totalreclaw_pair` handler) so the CLI and the tool emit
 * URLs from the same relay (`api-staging.totalreclaw.xyz` / `api.…`).
 *
 * Output formats
 * --------------
 * Same `PairCliOutputMode` surface as the local flow:
 *   - `human` — multi-line banner + QR ASCII + URL + PIN (default)
 *   - `json` — single-line `{v:1,sid,url,pin,mode,expires_at_ms,qr_ascii}`
 *   - `url-pin` — single-line `{v:1,url,pin,expires_at_ms}` (no QR)
 *   - `pair-only` — single-line `{v:1,pair_url,pin,expires_at_ms}` (no QR)
 *
 * The `sid` field in JSON mode carries the relay token (relay-issued
 * opaque session id) so the agent can correlate emit + completion.
 *
 * Phrase safety
 * -------------
 * The same invariant the agent-tool path enforces: relay sees only
 * ciphertext, gateway decrypts locally via x25519 ECDH + AES-GCM, the
 * mnemonic is written to credentials.json by `completePairing` and never
 * crosses any logger / stdout. PIN is on stdout (required) but never
 * logged.
 *
 * Scanner / scope
 * ---------------
 * Touches `fs` indirectly via the credential-write completion handler
 * passed in. No env-var reads here — caller resolves URL / paths from
 * `CONFIG`. See `index.ts` wire-up.
 */
import { validateMnemonic } from '@scure/bip39';
import { wordlist } from '@scure/bip39/wordlists/english.js';
import { defaultPairPendingPath, deletePairPendingFile, loadCredentialsJson, writeCredentialsJson, writeOnboardingState, } from './fs-helpers.js';
import { awaitPhraseUpload, openRemotePairSession, } from './pair-remote-client.js';
import { setRecoveryPhraseOverride } from './config.js';
import { encodePng, encodeUnicode } from './pair-qr.js';
import { deriveKeys, computeAuthKeyHash } from './crypto.js';
import { createApiClient } from './api-client.js';
/**
 * Run the relay-mode pair CLI. Mirrors `runPairCli`'s exit-code semantics:
 *   - `completed` (status 0)
 *   - `canceled` (Ctrl+C — status 130)
 *   - `expired` / `rejected` / `error` (status 1)
 *
 * Resolves with the outcome; the caller (`registerPairCli` action) maps
 * the outcome to `process.exit(...)`.
 */
export async function runRelayPairCli(mode, opts) {
    const outputMode = opts.outputMode ?? 'human';
    const stdout = opts.io.stdout;
    // 1. Open the relay session. The relay returns the user-facing URL +
    //    PIN + token + expiresAt. The keypair stays in-process.
    let session;
    try {
        session = await openRemotePairSession({
            relayBaseUrl: opts.relayBaseUrl,
            mode: mode === 'generate' ? 'generate' : 'import',
        });
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        opts.io.stderr.write(`\nFailed to open relay pairing session: ${msg}\n` +
            `If the relay is unreachable from this gateway, retry with --local for the loopback URL flow.\n`);
        return { status: 'error', error: msg };
    }
    // ISO-8601 → ms for tool-payload parity with the agent tool.
    const parsedExpiresMs = Date.parse(session.expiresAt);
    const expiresAtMs = Number.isFinite(parsedExpiresMs)
        ? parsedExpiresMs
        : Date.now() + 5 * 60_000;
    // 2. Render the QR ASCII (skipped in url-pin / pair-only modes — the
    //    same as `runPairCli`). 10s timeout guard against a renderer that
    //    never fires its callback.
    const skipsQr = outputMode === 'url-pin' || outputMode === 'pair-only';
    const qrAscii = skipsQr
        ? ''
        : await new Promise((resolve) => {
            let settled = false;
            const t = setTimeout(() => {
                if (!settled) {
                    settled = true;
                    resolve('');
                }
            }, 10_000);
            try {
                opts.renderQr(session.url, (ascii) => {
                    if (settled)
                        return;
                    settled = true;
                    clearTimeout(t);
                    resolve(ascii);
                });
            }
            catch (err) {
                if (settled)
                    return;
                settled = true;
                clearTimeout(t);
                resolve(`(QR renderer crashed: ${err instanceof Error ? err.message : String(err)})`);
            }
        });
    // 3. Emit the visible surface — single JSON line for non-human modes,
    //    multi-line banner + QR for human mode. Identical layout to the
    //    local-mode runner so callers can swap transparently.
    if (outputMode === 'url-pin') {
        const payload = {
            v: 1,
            url: session.url,
            pin: session.pin,
            expires_at_ms: expiresAtMs,
        };
        stdout.write(JSON.stringify(payload) + '\n');
    }
    else if (outputMode === 'pair-only') {
        const payload = {
            v: 1,
            pair_url: session.url,
            pin: session.pin,
            expires_at_ms: expiresAtMs,
        };
        stdout.write(JSON.stringify(payload) + '\n');
    }
    else if (outputMode === 'json') {
        const payload = {
            v: 1,
            sid: session.token,
            url: session.url,
            pin: session.pin,
            mode,
            expires_at_ms: expiresAtMs,
            qr_ascii: qrAscii,
        };
        stdout.write(JSON.stringify(payload) + '\n');
    }
    else {
        // Human-mode banner. Mirror `pair-cli.ts` COPY surface, but tweak the
        // header so operators see "Relay" not "Local" (so it's obvious the
        // URL is universal-reachable, not gateway-loopback).
        stdout.write('\nTotalReclaw — Relay pairing\n\n' +
            'Your TotalReclaw recovery phrase will be created (or imported) in your\n' +
            'BROWSER and delivered to this gateway encrypted end-to-end via the\n' +
            'relay (the relay only sees ciphertext). The phrase never touches the\n' +
            'LLM, the session transcript, or the relay server in plaintext.\n\n' +
            'Scan the QR code below with your phone, or open the URL on any device\n' +
            '(no LAN / Tailscale / port-forward required). Then type the 6-digit\n' +
            'code shown here into the browser.\n');
        stdout.write(mode === 'generate'
            ? '\nMode: GENERATE — your browser will create a NEW 12-word recovery phrase.\n' +
                'You will be asked to write it down and retype 3 words before the\n' +
                'gateway accepts it.\n'
            : '\nMode: IMPORT — your browser will accept an existing TotalReclaw\n' +
                'recovery phrase that you already have. Paste it in the browser; it\n' +
                'will be validated locally and encrypted before upload.\n');
        if (qrAscii) {
            stdout.write('\n' + qrAscii + '\n');
        }
        else {
            stdout.write('\n(QR not rendered — use the URL below)\n');
        }
        stdout.write('\nSecondary code (type this into the browser):\n\n    ' +
            session.pin.split('').join(' ') +
            '\n\nURL (QR encodes this plus a one-time public key):\n\n    ' +
            session.url +
            '\n\nSecurity:\n' +
            '  * Do NOT share your screen during pairing.\n' +
            '  * Do NOT screenshot this terminal.\n' +
            '  * The browser page will warn you never to reuse this recovery\n' +
            '    phrase for wallets, banking, email, or any other service.\n' +
            '\nWaiting for browser to connect… (press Ctrl+C to cancel)\n');
    }
    // 4. Optional PNG / Unicode QR for richer transports — same as the
    //    agent tool. Best-effort; non-fatal on encode failure.
    if (!skipsQr && outputMode !== 'human') {
        // JSON consumers already have qr_ascii; PNG/Unicode would belong in
        // a separate response shape. Keeping the runner surface in-band with
        // the local runner means we don't add fields here. Skip silently.
        void encodePng;
        void encodeUnicode;
    }
    // 5. Set up Ctrl+C cancellation. The relay session can't be
    //    server-side rejected from the client (no rejectPairSession-equivalent
    //    over the WS), but closing the WebSocket terminates the session.
    let canceled = false;
    const releaseInterrupt = opts.io.onInterrupt(() => {
        canceled = true;
        try {
            session._ws.close();
        }
        catch {
            /* ignore */
        }
    });
    // 6. Block on the relay until the browser uploads the encrypted
    //    phrase, then write credentials + flip onboarding-state. Mirrors
    //    the agent-tool's `awaitPhraseUpload` callback inline so we have a
    //    single source of truth for credential persistence.
    const emitStatus = (text) => {
        if (outputMode === 'human')
            stdout.write(text);
    };
    try {
        const result = await awaitPhraseUpload(session, {
            phraseValidator: (p) => validateMnemonic(p, wordlist),
            completePairing: async ({ mnemonic }) => {
                try {
                    // 3.3.11-rc.3: derive auth key + salt from mnemonic and pre-register
                    // with the relay HERE (not deferred to the plugin's next register()
                    // load). Pedro's 2026-05-06 QA found that pop-os was leaving
                    // credentials.json with only `{mnemonic}` because the plugin's
                    // post-pair register() either didn't run (post-SIGUSR1 plugin-skip
                    // bug) or partially failed before writing userId/salt back to disk.
                    // Doing it inline here means a successful pair is self-contained:
                    // browser uploads phrase → completePairing derives keys → register
                    // → write {userId, salt, mnemonic, scope_address}. Plugin's
                    // register() on next boot just authenticates with the existing
                    // credentials.
                    const keys = deriveKeys(mnemonic);
                    const authKeyHash = computeAuthKeyHash(keys.authKey);
                    const saltHex = keys.salt.toString('hex');
                    const saltB64 = keys.salt.toString('base64');
                    let registeredUserId;
                    try {
                        // wss://… → https://… for the REST register call. The relay
                        // serves both protocols on the same host.
                        const httpsBase = opts.relayBaseUrl.replace(/^ws/, 'http').replace(/\/+$/, '');
                        const apiClient = createApiClient(httpsBase);
                        const result = await apiClient.register(authKeyHash, saltHex);
                        registeredUserId = result.user_id;
                        opts.logger.info(`pair-cli (relay): registered user_id=${registeredUserId} (salt + auth-key persisted)`);
                    }
                    catch (regErr) {
                        const msg = regErr instanceof Error ? regErr.message : String(regErr);
                        // USER_EXISTS in subgraph mode → derive userId deterministically
                        // from auth-key hash so the credentials are still complete.
                        // Other errors → continue with mnemonic-only creds; the plugin's
                        // register() will retry on next load.
                        if (msg.includes('USER_EXISTS')) {
                            registeredUserId = authKeyHash.slice(0, 32);
                            opts.logger.info(`pair-cli (relay): USER_EXISTS — using derived userId=${registeredUserId}`);
                        }
                        else {
                            opts.logger.warn(`pair-cli (relay): /v1/register failed (best-effort, will retry on plugin load): ${msg}`);
                        }
                    }
                    let scopeAddress;
                    try {
                        scopeAddress = await opts.deriveScopeAddress(mnemonic);
                    }
                    catch (deriveErr) {
                        opts.logger.warn(`pair-cli (relay): scope_address derivation failed (will retry lazily): ${deriveErr instanceof Error ? deriveErr.message : String(deriveErr)}`);
                    }
                    const creds = loadCredentialsJson(opts.credentialsPath) ?? {};
                    const next = { ...creds, mnemonic, salt: saltB64 };
                    if (registeredUserId)
                        next.userId = registeredUserId;
                    if (scopeAddress)
                        next.scope_address = scopeAddress;
                    if (!writeCredentialsJson(opts.credentialsPath, next)) {
                        return { state: 'error', error: 'credentials_write_failed' };
                    }
                    setRecoveryPhraseOverride(mnemonic);
                    writeOnboardingState(opts.onboardingStatePath, {
                        onboardingState: 'active',
                        createdBy: mode === 'generate' ? 'generate' : 'import',
                        credentialsCreatedAt: new Date().toISOString(),
                        version: opts.pluginVersion,
                    });
                    // 3.3.13 — sentinel cleanup. The CLI flow shares the
                    // .pair-pending.json sentinel with the auto-pair-on-load flow
                    // (a user who runs `tr pair --json` after the plugin already
                    // auto-opened a session ends up with both surfaces pointing at
                    // the same credentials.json target). Delete the sentinel here
                    // so subsequent agent turns don't keep surfacing a stale URL.
                    deletePairPendingFile(defaultPairPendingPath(opts.credentialsPath));
                    opts.logger.info(`pair-cli (relay): session ${session.token.slice(0, 8)}… completed; credentials written` +
                        (registeredUserId ? ` (userId=${registeredUserId.slice(0, 8)}…)` : '') +
                        (scopeAddress ? ` (scope_address=${scopeAddress})` : ''));
                    return { state: 'active' };
                }
                catch (err) {
                    const msg = err instanceof Error ? err.message : String(err);
                    opts.logger.error(`pair-cli (relay): completePairing failed: ${msg}`);
                    return { state: 'error', error: msg };
                }
            },
        });
        if (canceled) {
            emitStatus('\nCanceled. Pairing session invalidated.\n');
            return { status: 'canceled', sid: session.token };
        }
        if (result.state === 'active') {
            emitStatus('\nPairing complete. Account is active.\n');
            return { status: 'completed', sid: session.token };
        }
        emitStatus(`\nPairing failed: ${result.error ?? 'unknown_error'}\n`);
        return { status: 'error', sid: session.token, error: result.error ?? 'unknown_error' };
    }
    catch (err) {
        if (canceled) {
            emitStatus('\nCanceled. Pairing session invalidated.\n');
            return { status: 'canceled', sid: session.token };
        }
        const msg = err instanceof Error ? err.message : String(err);
        if (msg.includes('timeout')) {
            emitStatus('\nSession expired. Run the command again to restart.\n');
            return { status: 'expired', sid: session.token };
        }
        emitStatus(`\nPairing error: ${msg}\n`);
        return { status: 'error', sid: session.token, error: msg };
    }
    finally {
        releaseInterrupt();
    }
}
