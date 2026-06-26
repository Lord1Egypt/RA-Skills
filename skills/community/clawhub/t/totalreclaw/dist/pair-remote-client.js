/**
 * pair-remote-client — gateway-side WebSocket client for the relay-brokered
 * pair flow (plugin rc.11).
 *
 * TypeScript mirror of ``python/src/totalreclaw/pair/remote_client.py``. Wire
 * formats (WebSocket frame shapes, URL layout, base64url encoding) match the
 * Python implementation byte-for-byte so either side can open a session that
 * the relay (`totalreclaw-relay`) + browser page (`pair-html.ts`) already
 * understand. Crypto primitives come from the shared ``pair-crypto.ts``
 * module — the same ECDH + HKDF + AES-256-GCM stack the loopback HTTP
 * server uses.
 *
 * Flow (this file implements the gateway half):
 *
 *   1. Generate an ephemeral x25519 keypair (`generateGatewayKeypair`).
 *   2. Open a short-lived WebSocket to `wss://<relay>/pair/session/open`.
 *   3. Send `{type: "open", gateway_pubkey, pin, client_id, mode?}`.
 *   4. Receive `{type: "opened", token, short_url, expires_at}` — use these
 *      to build the user-facing pair URL (token + `#pk=<gateway_pubkey>`).
 *   5. Block on the WebSocket until the relay pushes
 *      `{type: "forward", client_pubkey, nonce, ciphertext}`.
 *   6. Decrypt locally via `decryptPairingPayload` using the gateway private
 *      key. If decrypt succeeds and phrase is valid, call the caller's
 *      `completePairing` handler (writes credentials.json).
 *   7. Send `{type: "ack"}` back; close the WebSocket.
 *
 * Phrase-safety invariants preserved:
 *   - Relay sees only ciphertext; it cannot derive the symmetric key without
 *     the gateway's private key.
 *   - The gateway pubkey transits the relay as a label in the open frame so
 *     the relay can display the session, but is ALSO bound into the URL
 *     fragment the user opens — the fragment never hits the relay.
 *   - Phrase NEVER enters any logs. PIN is never logged.
 *   - No relay credentials are required — auth is the single-use PIN +
 *     5-minute TTL + gateway ECDH private key.
 *
 * Scope / scanner surface:
 *   - NO `fs.*` primitives (delegates credentials writes to the caller via
 *     `completePairing`). Safe for the check-scanner cross-rule guard.
 *   - NO env-var reads. Caller passes `relayBaseUrl` explicitly; the plugin
 *     sources it from the `TOTALRECLAW_PAIR_RELAY_URL` env (via `config.ts`)
 *     or falls back to the staging default.
 */
import { randomBytes, randomInt } from 'node:crypto';
import WebSocket from 'ws';
import { decryptPairingPayload, generateGatewayKeypair, } from './pair-crypto.js';
// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------
/** Default relay endpoint. Caller passes `TOTALRECLAW_PAIR_RELAY_URL` via config. */
export const DEFAULT_RELAY_URL = 'wss://api.totalreclaw.xyz';
/** WebSocket connect + handshake timeout (ms). */
const OPEN_TIMEOUT_MS = 10_000;
/** Default blocking-await-for-forward timeout (5 minutes — matches relay TTL). */
const DEFAULT_AWAIT_TIMEOUT_MS = 5 * 60_000;
/** Default validator — 12 or 24 lowercase ASCII words. Matches pair-http default. */
function defaultBip39CountValidator(phrase) {
    const words = phrase.split(' ');
    if (words.length !== 12 && words.length !== 24)
        return false;
    return words.every((w) => /^[a-z]+$/.test(w));
}
/** 6-digit uniform PIN. Uses `node:crypto.randomInt` (cryptographically random). */
function defaultPin() {
    const n = randomInt(0, 1_000_000);
    return n.toString(10).padStart(6, '0');
}
/** Random hex client id. Opaque to the relay. */
function defaultClientId() {
    return 'gw-' + randomBytes(8).toString('hex');
}
/**
 * Assemble the user-facing pair URL. Converts `wss://` → `https://` and
 * `ws://` → `http://` for the URL the user opens in a browser. The gateway
 * pubkey lives in the URL fragment so it never hits relay logs.
 */
function buildUserUrl(relayBase, token, pkB64) {
    let httpBase = relayBase;
    if (httpBase.startsWith('wss://')) {
        httpBase = 'https://' + httpBase.slice('wss://'.length);
    }
    else if (httpBase.startsWith('ws://')) {
        httpBase = 'http://' + httpBase.slice('ws://'.length);
    }
    return `${httpBase}/pair/p/${token}#pk=${pkB64}`;
}
/**
 * Normalise the relay base URL for the WebSocket connect. We always hit
 * `wss://` for the open-frame WS even if the caller passed an `https://`
 * browser-facing URL in the config (most self-hosters will pass one URL for
 * both). Strips trailing slashes.
 */
function wsConnectBase(relayBase) {
    let base = relayBase.replace(/\/+$/, '');
    if (base.startsWith('https://')) {
        base = 'wss://' + base.slice('https://'.length);
    }
    else if (base.startsWith('http://')) {
        base = 'ws://' + base.slice('http://'.length);
    }
    return base;
}
// ---------------------------------------------------------------------------
// Open
// ---------------------------------------------------------------------------
/**
 * Open a pair session on the relay. Returns a handle with the user-facing
 * URL, 6-digit PIN, expiry, keypair, and a live WebSocket the caller holds
 * until `awaitPhraseUpload` resolves.
 *
 * Throws if the relay responds with `{type: "error"}` or an unexpected frame.
 */
export async function openRemotePairSession(opts = {}) {
    const relayBase = (opts.relayBaseUrl ?? DEFAULT_RELAY_URL).replace(/\/+$/, '');
    const wsBase = wsConnectBase(relayBase);
    const wsUrl = `${wsBase}/pair/session/open`;
    const WebSocketImpl = opts.webSocketImpl ?? WebSocket;
    const keypair = opts.keypair ?? generateGatewayKeypair();
    const pin = opts.pin ?? defaultPin();
    const clientId = opts.clientId ?? defaultClientId();
    const mode = opts.mode ?? 'either';
    const ws = new WebSocketImpl(wsUrl, {
        handshakeTimeout: OPEN_TIMEOUT_MS,
    });
    // Wait for the WS to open (so `send` doesn't race the handshake).
    try {
        await waitOpen(ws, OPEN_TIMEOUT_MS);
    }
    catch (err) {
        safeClose(ws);
        throw err;
    }
    // Send the open frame.
    try {
        ws.send(JSON.stringify({
            type: 'open',
            gateway_pubkey: keypair.pkB64,
            pin,
            client_id: clientId,
            mode,
        }));
    }
    catch (err) {
        safeClose(ws);
        throw err instanceof Error ? err : new Error(String(err));
    }
    // Wait for the opened frame.
    let raw;
    try {
        raw = await waitNextMessage(ws, OPEN_TIMEOUT_MS);
    }
    catch (err) {
        safeClose(ws);
        throw err;
    }
    let msg;
    try {
        const text = typeof raw === 'string' ? raw : Buffer.from(raw).toString('utf-8');
        msg = JSON.parse(text);
    }
    catch {
        safeClose(ws);
        throw new Error('pair-remote-client: opened frame not valid JSON');
    }
    if (msg.type === 'error') {
        const errStr = typeof msg.error === 'string' ? msg.error : 'relay_error';
        safeClose(ws);
        throw new Error(`pair-remote-client: session/open failed: ${errStr}`);
    }
    if (msg.type !== 'opened') {
        safeClose(ws);
        throw new Error(`pair-remote-client: unexpected response type '${String(msg.type)}'`);
    }
    const token = typeof msg.token === 'string' ? msg.token : '';
    const expiresAt = typeof msg.expires_at === 'string' ? msg.expires_at : '';
    if (!token || !expiresAt) {
        safeClose(ws);
        throw new Error('pair-remote-client: opened frame missing token or expires_at');
    }
    const url = buildUserUrl(relayBase, token, keypair.pkB64);
    return {
        url,
        pin,
        token,
        expiresAt,
        keypair,
        mode,
        _ws: ws,
    };
}
// ---------------------------------------------------------------------------
// Await + decrypt + ack
// ---------------------------------------------------------------------------
/**
 * Block on the WebSocket until the relay pushes the encrypted phrase, then
 * decrypt and invoke `completePairing`. Sends `{type: "ack"}` on success or
 * `{type: "nack", error: "..."}` on failure, then closes the WebSocket.
 *
 * Returns the `RelayCompletionResult` produced by the caller's handler.
 *
 * Caller semantics: most plugin callers schedule this as a background task so
 * the `totalreclaw_pair` tool handler can return the URL + PIN to the agent
 * immediately, and the phrase-upload wait happens asynchronously while the
 * agent chats with the user.
 */
export async function awaitPhraseUpload(session, opts) {
    const validate = opts.phraseValidator ?? defaultBip39CountValidator;
    const timeoutMs = opts.timeoutMs ?? DEFAULT_AWAIT_TIMEOUT_MS;
    const ws = session._ws;
    let raw;
    try {
        raw = await waitNextMessage(ws, timeoutMs);
    }
    catch (err) {
        safeClose(ws);
        throw err;
    }
    let msg;
    try {
        const text = typeof raw === 'string' ? raw : Buffer.from(raw).toString('utf-8');
        msg = JSON.parse(text);
    }
    catch {
        safeSend(ws, { type: 'nack', error: 'bad_json' });
        safeClose(ws);
        throw new Error('pair-remote-client: forward frame not valid JSON');
    }
    if (msg.type !== 'forward') {
        safeSend(ws, { type: 'nack', error: 'expected_forward' });
        safeClose(ws);
        throw new Error(`pair-remote-client: unexpected frame '${String(msg.type)}'`);
    }
    const clientPubkey = typeof msg.client_pubkey === 'string' ? msg.client_pubkey : '';
    const nonce = typeof msg.nonce === 'string' ? msg.nonce : '';
    const ciphertext = typeof msg.ciphertext === 'string' ? msg.ciphertext : '';
    if (!clientPubkey || !nonce || !ciphertext) {
        safeSend(ws, { type: 'nack', error: 'bad_forward_body' });
        safeClose(ws);
        throw new Error('pair-remote-client: forward frame missing required fields');
    }
    // Decrypt locally (ciphertext + shared-secret derivation never leave this host).
    let plaintext;
    try {
        plaintext = decryptPairingPayload({
            skGatewayB64: session.keypair.skB64,
            pkDeviceB64: clientPubkey,
            sid: session.token,
            nonceB64: nonce,
            ciphertextB64: ciphertext,
        });
    }
    catch (err) {
        safeSend(ws, { type: 'nack', error: 'decrypt_failed' });
        safeClose(ws);
        throw err instanceof Error ? err : new Error(String(err));
    }
    // Decode + normalize. Match pair-http's BIP-39 norm: NFKC → lowercase → trim → single-space.
    let mnemonic;
    try {
        mnemonic = plaintext
            .toString('utf-8')
            .normalize('NFKC')
            .toLowerCase()
            .trim()
            .split(/\s+/)
            .join(' ');
    }
    catch (err) {
        safeSend(ws, { type: 'nack', error: 'bad_utf8' });
        safeClose(ws);
        throw err instanceof Error ? err : new Error(String(err));
    }
    finally {
        // Best-effort: scrub the raw plaintext buffer.
        plaintext.fill(0);
    }
    if (!validate(mnemonic)) {
        safeSend(ws, { type: 'nack', error: 'invalid_mnemonic' });
        safeClose(ws);
        throw new Error('pair-remote-client: phrase failed BIP-39 validation');
    }
    // Hand off to the caller-supplied completion handler. Wrapped in try/finally
    // so we always drop our own reference to the mnemonic.
    let result;
    try {
        result = await opts.completePairing({ mnemonic, session });
    }
    catch (err) {
        safeSend(ws, { type: 'nack', error: 'completion_failed' });
        safeClose(ws);
        throw err instanceof Error ? err : new Error(String(err));
    }
    finally {
        // Drop our reference. JS strings are immutable so we can't zero them;
        // rebinding at least drops the reference from this closure.
        mnemonic = '';
    }
    if (result.state !== 'active') {
        safeSend(ws, { type: 'nack', error: result.error ?? 'completion_failed' });
        safeClose(ws);
        return result;
    }
    safeSend(ws, { type: 'ack' });
    safeClose(ws);
    return result;
}
/**
 * One-shot convenience: open session + await phrase upload + run completion.
 * Tool handlers normally split this into two calls so the agent can tell the
 * user the URL + PIN before blocking. This helper exists for tests and for
 * simpler callers.
 */
export async function pairViaRelay(opts) {
    const session = await openRemotePairSession({
        relayBaseUrl: opts.relayBaseUrl,
        pin: opts.pin,
        mode: opts.mode,
    });
    return awaitPhraseUpload(session, {
        completePairing: opts.completePairing,
        phraseValidator: opts.phraseValidator,
        timeoutMs: opts.timeoutMs,
    });
}
// ---------------------------------------------------------------------------
// WS helpers
// ---------------------------------------------------------------------------
function waitOpen(ws, timeoutMs) {
    return new Promise((resolve, reject) => {
        if (ws.readyState === WebSocket.OPEN) {
            resolve();
            return;
        }
        const onOpen = () => {
            cleanup();
            resolve();
        };
        const onError = (err) => {
            cleanup();
            reject(err instanceof Error ? err : new Error(String(err)));
        };
        const onClose = (code) => {
            cleanup();
            reject(new Error(`pair-remote-client: ws closed before open (${code})`));
        };
        const timer = setTimeout(() => {
            cleanup();
            reject(new Error('pair-remote-client: ws open timeout'));
        }, timeoutMs);
        const cleanup = () => {
            clearTimeout(timer);
            ws.off('open', onOpen);
            ws.off('error', onError);
            ws.off('close', onClose);
        };
        ws.on('open', onOpen);
        ws.on('error', onError);
        ws.on('close', onClose);
    });
}
function waitNextMessage(ws, timeoutMs) {
    return new Promise((resolve, reject) => {
        const onMessage = (data) => {
            cleanup();
            resolve(data);
        };
        const onError = (err) => {
            cleanup();
            reject(err instanceof Error ? err : new Error(String(err)));
        };
        const onClose = (code) => {
            cleanup();
            reject(new Error(`pair-remote-client: ws closed before message (${code})`));
        };
        const timer = setTimeout(() => {
            cleanup();
            reject(new Error('pair-remote-client: ws message timeout'));
        }, timeoutMs);
        const cleanup = () => {
            clearTimeout(timer);
            ws.off('message', onMessage);
            ws.off('error', onError);
            ws.off('close', onClose);
        };
        ws.on('message', onMessage);
        ws.on('error', onError);
        ws.on('close', onClose);
    });
}
function safeSend(ws, msg) {
    try {
        if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify(msg));
        }
    }
    catch {
        /* swallow */
    }
}
function safeClose(ws) {
    try {
        if (ws.readyState === WebSocket.OPEN ||
            ws.readyState === WebSocket.CONNECTING) {
            ws.close();
        }
    }
    catch {
        /* swallow */
    }
}
