/**
 * pair-qr — QR encoders for the rc.5 pair-tool payload.
 *
 * Two helpers that render the pair URL as either a PNG (for
 * image-capable chat transports like Telegram) or a Unicode block
 * string (for terminal-only transports like the OpenClaw native CLI).
 *
 * Phrase-safety invariant (see
 * `project_phrase_safety_rule.md` in the internal repo):
 *   The QR payload is ONLY the pair URL. The 6-digit PIN is a separate
 *   out-of-band confirmation — it is NEVER baked into the QR. The URL
 *   itself carries only the session token + gateway ephemeral pubkey
 *   (fragment-encoded).
 *
 * Size profile for a typical ~110-char pair URL:
 *   - `encodePng` defaults (scale=10, margin=4): ~4 KiB PNG, ~5.5 KiB
 *     base64. Fits comfortably in a tool-call response.
 *   - `encodeUnicode` (margin=2): ~1.1 KiB, 23 lines.
 *
 * We wrap the `qrcode` npm package (~50 KiB, pure TS, no native
 * bindings) so neither tsx dev runs nor the published plugin depend on
 * the bundler understanding CJS vs ESM subpath imports. All we use is
 * the high-level `toBuffer` / `toString` surface.
 */
/**
 * Error class raised by the rc.5 QR encoders.
 *
 * Extends the built-in `Error` so `instanceof Error` checks in callers
 * keep working.
 */
export class QREncodeError extends Error {
    constructor(message) {
        super(message);
        this.name = 'QREncodeError';
    }
}
// QR v40 maxes out at ~2953 alphanumeric bytes at ECC-L. We reject
// payloads over 2 KiB — the pair URL should never approach this. This
// is defence-in-depth against a caller accidentally feeding a
// phrase-length blob.
const MAX_PAYLOAD_BYTES = 2048;
function validatePayload(url) {
    if (typeof url !== 'string') {
        throw new QREncodeError(`url must be a string, got ${typeof url}`);
    }
    if (url.length === 0) {
        throw new QREncodeError('url must not be empty');
    }
    const bytes = Buffer.byteLength(url, 'utf-8');
    if (bytes > MAX_PAYLOAD_BYTES) {
        throw new QREncodeError(`url too large for QR encoding: ${bytes} bytes (max ${MAX_PAYLOAD_BYTES}). ` +
            'This limit prevents accidentally encoding phrase-length blobs; a pair ' +
            'URL should be ~80-150 bytes.');
    }
}
async function loadQrCodeModule() {
    const raw = (await import('qrcode'));
    // qrcode ships CJS; the `default` export contains the surface under
    // both Node's ESM interop and tsx's loader.
    const mod = raw.default ?? raw;
    return mod;
}
/**
 * Render `url` as a PNG QR code.
 *
 * @throws {QREncodeError} if the URL is empty, non-string, or exceeds
 *   the 2 KiB safety cap.
 */
export async function encodePng(url, options = {}) {
    validatePayload(url);
    const qr = await loadQrCodeModule();
    try {
        return await qr.toBuffer(url, {
            errorCorrectionLevel: options.ecc ?? 'M',
            scale: Math.max(1, options.boxSize ?? 10),
            margin: Math.max(0, options.border ?? 4),
        });
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        throw new QREncodeError(`QR encoding failed: ${msg}`);
    }
}
/**
 * Render `url` as a Unicode block QR string (for terminal output).
 *
 * Uses half-block glyphs so each character represents two vertical
 * pixels — the resulting string renders square-ish in terminals with
 * ~2:1 line-height. Emitted as a single newline-delimited string.
 *
 * @throws {QREncodeError} on invalid input.
 */
export async function encodeUnicode(url, options = {}) {
    validatePayload(url);
    const qr = await loadQrCodeModule();
    try {
        return await qr.toString(url, {
            type: 'utf8',
            errorCorrectionLevel: options.ecc ?? 'M',
            margin: Math.max(0, options.border ?? 2),
        });
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        throw new QREncodeError(`QR encoding failed: ${msg}`);
    }
}
