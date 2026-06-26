/**
 * pair-crypto — gateway-side cryptographic primitives for the v3.3.x
 * relay-brokered pair flow.
 *
 * Cipher suite (design doc 3a-3b, cipher swap ratified 2026-04-23 / rc.12):
 *   - ECDH on x25519 for key agreement.
 *   - HKDF-SHA256 for symmetric-key derivation from the shared secret.
 *   - AES-256-GCM AEAD for the ciphertext payload, with the sid bound as
 *     associated data (AD = sid UTF-8 bytes, 12-byte nonce, 16-byte tag).
 *
 * rc.4..rc.11 used ChaCha20-Poly1305, but the Web Crypto API does NOT
 * implement ChaCha20-Poly1305 in Chrome / Safari / Edge. The pair-page
 * submit path silently threw `Algorithm: Unrecognized name` before
 * reaching the network. rc.12 swaps the cipher suite to AES-256-GCM
 * (universally supported in WebCrypto) and bumps HKDF_INFO to v2 so
 * cross-version mis-pairs fail closed rather than garble.
 *
 * Every primitive is provided by the Node built-in `node:crypto` module
 * on Node 18.19+ and above. NO third-party crypto dependency is added
 * to the plugin for the gateway side. (The BROWSER side of the flow uses
 * WebCrypto's AES-GCM directly — no shim needed.)
 *
 * Scope and guarantees
 * --------------------
 *   - This module ONLY runs on the gateway host. The device side
 *     (browser) implements the mirror of these functions in a separate
 *     bundle served by pair-http.ts.
 *   - Round-trip correctness: deriveSessionKey on both sides with
 *     matching (sk_local, pk_remote) produces the same key.
 *   - AD (sid) binding: a ciphertext encrypted for session A CANNOT
 *     decrypt under session B's keys, even with identical plaintext
 *     and nonce. This is the AEAD contract; validated by tests.
 *   - No logging of key material. The only public thing this module
 *     emits is base64url-encoded raw public keys (32 bytes → 43 chars),
 *     which are safe for the QR payload.
 *   - No `fs.*` calls, no `process.env` reads, no network primitives.
 *     Keeps scanner surface isolated (see `check-scanner.mjs`).
 *
 * Interoperability with browser WebCrypto
 * ---------------------------------------
 *   The WebCrypto x25519 + HKDF + AES-GCM APIs are bit-for-bit compatible
 *   with Node's `crypto` as long as:
 *     - Raw 32-byte public/private keys are used (not DER/SPKI).
 *     - HKDF parameters are (hash=SHA-256, salt=sid bytes, info fixed
 *       ASCII string "totalreclaw-pair-v2", length=32 bytes).
 *     - AEAD uses a 12-byte random nonce + 16-byte tag, AD = sid bytes.
 *   See tests for fixed test vectors.
 */

import {
  createPrivateKey,
  createPublicKey,
  diffieHellman,
  generateKeyPairSync,
  hkdfSync,
  createCipheriv,
  createDecipheriv,
  randomBytes,
  timingSafeEqual,
} from 'node:crypto';

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

/**
 * HKDF "info" parameter — fixes the domain separation for this protocol.
 * MUST match the browser-side constant in the pair-page bundle + the
 * relay-served pair-html page.
 *
 * Versioned so we can roll to a new KDF or cipher suite without silently
 * producing garbage with old ciphertexts. rc.12: bumped from v1 to v2
 * after cipher-suite swap from ChaCha20-Poly1305 → AES-256-GCM (see
 * module header comment for context).
 */
export const HKDF_INFO = 'totalreclaw-pair-v2';

/** HKDF output length — 32 bytes = 256-bit AES-256-GCM key. */
export const AEAD_KEY_BYTES = 32;

/** AES-GCM nonce length — 12 bytes (SP 800-38D recommendation). */
export const AEAD_NONCE_BYTES = 12;

/** AES-GCM auth tag length — 16 bytes (128 bits, standard). */
export const AEAD_TAG_BYTES = 16;

/** Raw x25519 public/private key length — 32 bytes per RFC 7748. */
export const X25519_KEY_BYTES = 32;

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

/** Raw 32-byte x25519 public key, base64url-encoded. */
export type PublicKeyB64 = string;

/** Raw 32-byte x25519 private key, base64url-encoded. */
export type PrivateKeyB64 = string;

/** Raw 12-byte AEAD nonce, base64url-encoded. */
export type NonceB64 = string;

/** AEAD ciphertext + appended tag, base64url-encoded. */
export type CiphertextB64 = string;

/** An ephemeral gateway keypair, both halves base64url-encoded. */
export interface GatewayKeypair {
  skB64: PrivateKeyB64;
  pkB64: PublicKeyB64;
}

/** Fully-derived session keys — caller uses kEnc for AEAD ops. */
export interface SessionKeys {
  /** 32-byte AES-256-GCM key. */
  kEnc: Buffer;
}

/** Inputs to the gateway-side decryption happy path. */
export interface DecryptInputs {
  /** Gateway's base64url private key (from pair-session-store). */
  skGatewayB64: PrivateKeyB64;
  /** Device's ephemeral public key, base64url. */
  pkDeviceB64: PublicKeyB64;
  /** Session id, used as HKDF salt AND AEAD AD. */
  sid: string;
  /** Base64url nonce (12 bytes). */
  nonceB64: NonceB64;
  /** Base64url ciphertext (plaintext || 16-byte tag). */
  ciphertextB64: CiphertextB64;
}

/**
 * Inputs for the gateway-side encrypt helper. Only used by tests (the
 * actual encrypt side lives in the browser bundle) — exposed because
 * the test vectors need a round-trip, and because future "gateway
 * replies with an encrypted ACK" flows (4.x) could reuse it.
 */
export interface EncryptInputs {
  /** Gateway's private key (or ephemeral-side's private key). */
  skLocalB64: PrivateKeyB64;
  /** Peer's public key. */
  pkRemoteB64: PublicKeyB64;
  sid: string;
  plaintext: Buffer | Uint8Array;
  /** Override the 12-byte nonce. Used for tests that need deterministic output. */
  nonceB64?: NonceB64;
}

export interface EncryptOutput {
  nonceB64: NonceB64;
  ciphertextB64: CiphertextB64;
}

// ---------------------------------------------------------------------------
// Key generation / conversion
// ---------------------------------------------------------------------------

/**
 * Generate a fresh ephemeral x25519 keypair for a pairing session.
 *
 * Returns raw 32-byte values base64url-encoded. The caller persists the
 * private half in pair-session-store (under the session record's 0600
 * file) and embeds the public half in the QR URL fragment.
 *
 * The returned keys are raw x25519 — NOT DER/SPKI/PEM. The browser
 * side's WebCrypto needs raw bytes to import.
 */
export function generateGatewayKeypair(): GatewayKeypair {
  const { publicKey, privateKey } = generateKeyPairSync('x25519');
  return {
    skB64: extractRawPrivate(privateKey),
    pkB64: extractRawPublic(publicKey),
  };
}

/**
 * Re-constitute a Node `KeyObject` from raw base64url public-key bytes.
 * Uses the JWK OKP encoding because Node doesn't accept raw-format
 * inputs to `createPublicKey` directly.
 */
function publicKeyFromB64(pkB64: PublicKeyB64): ReturnType<typeof createPublicKey> {
  const raw = Buffer.from(pkB64, 'base64url');
  if (raw.length !== X25519_KEY_BYTES) {
    throw new Error(`pair-crypto: public key must be ${X25519_KEY_BYTES} bytes (got ${raw.length})`);
  }
  return createPublicKey({
    key: { kty: 'OKP', crv: 'X25519', x: raw.toString('base64url') },
    format: 'jwk',
  });
}

/**
 * Re-constitute a Node `KeyObject` from raw base64url private-key bytes.
 *
 * JWK OKP private keys require the `x` (public) field too; we derive it
 * by first constructing a temporary KeyObject from `d` alone, then
 * exporting its public half. This is cheap (one scalarmult) and keeps
 * the call sites clean.
 *
 * Mirror of the browser-side WebCrypto `importKey('raw', ...)` path.
 */
function privateKeyFromB64(skB64: PrivateKeyB64): ReturnType<typeof createPrivateKey> {
  const raw = Buffer.from(skB64, 'base64url');
  if (raw.length !== X25519_KEY_BYTES) {
    throw new Error(`pair-crypto: private key must be ${X25519_KEY_BYTES} bytes (got ${raw.length})`);
  }

  // The JWK OKP format requires `x` (public) alongside `d` (private).
  // Derive `x` by first constructing a public KeyObject from the scalar
  // via the OKP JWK path — Node accepts `d` alone and returns a usable
  // private KeyObject from which we can derive the public half.
  const tempPriv = createPrivateKey({
    key: { kty: 'OKP', crv: 'X25519', d: raw.toString('base64url'), x: '' },
    format: 'jwk',
  });
  // Derive the public half.
  const pubObj = createPublicKey(tempPriv);
  const pubJwk = pubObj.export({ format: 'jwk' }) as { x: string };

  // Re-construct with the full (x, d) pair. This is the canonical form
  // the rest of the code holds onto.
  return createPrivateKey({
    key: { kty: 'OKP', crv: 'X25519', d: raw.toString('base64url'), x: pubJwk.x },
    format: 'jwk',
  });
}

/** Extract the raw 32-byte public-key bytes from a Node KeyObject → base64url. */
function extractRawPublic(pk: ReturnType<typeof createPublicKey>): PublicKeyB64 {
  const jwk = pk.export({ format: 'jwk' }) as { x?: string };
  if (!jwk.x) throw new Error('pair-crypto: public key JWK is missing the x field');
  return jwk.x; // JWK `x` is already base64url-encoded raw bytes.
}

/** Extract the raw 32-byte private-key bytes from a Node KeyObject → base64url. */
function extractRawPrivate(sk: ReturnType<typeof createPrivateKey>): PrivateKeyB64 {
  const jwk = sk.export({ format: 'jwk' }) as { d?: string };
  if (!jwk.d) throw new Error('pair-crypto: private key JWK is missing the d field');
  return jwk.d;
}

/**
 * Derive the public key from a raw base64url private key. Exposed for
 * tests and for the session-store's self-consistency checks — the
 * default `createPairSession` doesn't call this (it generates both
 * halves at once via `generateGatewayKeypair`).
 */
export function derivePublicFromPrivate(skB64: PrivateKeyB64): PublicKeyB64 {
  const sk = privateKeyFromB64(skB64);
  const pk = createPublicKey(sk);
  return extractRawPublic(pk);
}

// ---------------------------------------------------------------------------
// ECDH + HKDF
// ---------------------------------------------------------------------------

/**
 * Perform x25519 ECDH between (local private key, remote public key),
 * producing a 32-byte shared secret.
 *
 * BOTH sides running this with swapped halves MUST produce the same
 * shared secret. This is the foundation of the pairing key agreement.
 *
 * Validation: throws if either key is the wrong byte length, or if
 * the underlying `diffieHellman` call fails (which Node will do for
 * invalid curve points).
 */
export function computeSharedSecret(opts: {
  skLocalB64: PrivateKeyB64;
  pkRemoteB64: PublicKeyB64;
}): Buffer {
  const sk = privateKeyFromB64(opts.skLocalB64);
  const pk = publicKeyFromB64(opts.pkRemoteB64);
  const shared = diffieHellman({ privateKey: sk, publicKey: pk });
  if (shared.length !== X25519_KEY_BYTES) {
    throw new Error(
      `pair-crypto: ECDH output wrong length (got ${shared.length}, expected ${X25519_KEY_BYTES})`,
    );
  }
  return shared;
}

/**
 * Derive the AEAD key from a shared secret via HKDF-SHA256. Uses the
 * session id as the salt and the fixed protocol tag as the info.
 *
 * Mathematical sketch (per RFC 5869):
 *   PRK = HMAC-SHA256(salt, shared)
 *   OKM = HMAC-SHA256(PRK, info || 0x01)[:L]
 *
 * Where L = 32 bytes = AEAD_KEY_BYTES.
 *
 * The sid binding means a ciphertext encrypted for session A is
 * DECRYPTABLE only under session A's derived key. Replaying ct from
 * session A into session B's decrypt path produces a different key →
 * AEAD tag fails → rejected.
 */
export function deriveSessionKeys(opts: {
  sharedSecret: Buffer;
  sid: string;
}): SessionKeys {
  if (opts.sharedSecret.length !== X25519_KEY_BYTES) {
    throw new Error('pair-crypto: shared secret must be 32 bytes');
  }
  if (typeof opts.sid !== 'string' || opts.sid.length === 0) {
    throw new Error('pair-crypto: sid is required for HKDF salt binding');
  }
  const salt = Buffer.from(opts.sid, 'utf-8');
  const info = Buffer.from(HKDF_INFO, 'utf-8');
  const okm = hkdfSync('sha256', opts.sharedSecret, salt, info, AEAD_KEY_BYTES);
  return { kEnc: Buffer.from(okm) };
}

/**
 * One-shot convenience: ECDH + HKDF in a single call. Used by both the
 * HTTP respond handler (decrypt side) and the tests.
 */
export function deriveAeadKeyFromEcdh(opts: {
  skLocalB64: PrivateKeyB64;
  pkRemoteB64: PublicKeyB64;
  sid: string;
}): SessionKeys {
  const shared = computeSharedSecret({
    skLocalB64: opts.skLocalB64,
    pkRemoteB64: opts.pkRemoteB64,
  });
  return deriveSessionKeys({ sharedSecret: shared, sid: opts.sid });
}

// ---------------------------------------------------------------------------
// AEAD
// ---------------------------------------------------------------------------

/**
 * Decrypt an AES-256-GCM AEAD ciphertext. Returns the plaintext on
 * success; throws if the tag is invalid (which includes both tampering
 * and wrong-key attempts).
 *
 * Ciphertext is expected in the combined form `plaintext || tag`, where
 * tag is the trailing 16 bytes. The caller MUST supply the same
 * (kEnc, nonce, sid-as-AD) used for encryption.
 */
export function aeadDecrypt(opts: {
  kEnc: Buffer;
  nonceB64: NonceB64;
  sid: string;
  ciphertextB64: CiphertextB64;
}): Buffer {
  const nonce = Buffer.from(opts.nonceB64, 'base64url');
  if (nonce.length !== AEAD_NONCE_BYTES) {
    throw new Error(`pair-crypto: nonce must be ${AEAD_NONCE_BYTES} bytes (got ${nonce.length})`);
  }
  if (opts.kEnc.length !== AEAD_KEY_BYTES) {
    throw new Error(`pair-crypto: AEAD key must be ${AEAD_KEY_BYTES} bytes`);
  }
  const combined = Buffer.from(opts.ciphertextB64, 'base64url');
  if (combined.length < AEAD_TAG_BYTES) {
    throw new Error('pair-crypto: ciphertext too short to contain tag');
  }
  const ct = combined.subarray(0, combined.length - AEAD_TAG_BYTES);
  const tag = combined.subarray(combined.length - AEAD_TAG_BYTES);

  const decipher = createDecipheriv('aes-256-gcm', opts.kEnc, nonce, {
    authTagLength: AEAD_TAG_BYTES,
  });
  decipher.setAAD(Buffer.from(opts.sid, 'utf-8'), { plaintextLength: ct.length });
  decipher.setAuthTag(tag);

  const pt1 = decipher.update(ct);
  const pt2 = decipher.final();
  return Buffer.concat([pt1, pt2]);
}

/**
 * One-shot decrypt: ECDH + HKDF + AEAD in one call. This is what the
 * HTTP respond handler calls. Returns the plaintext Buffer on success.
 *
 * Throws on ANY failure (wrong key length, invalid curve point, tag
 * mismatch). The caller catches and returns 400 to the device.
 */
export function decryptPairingPayload(inputs: DecryptInputs): Buffer {
  const { kEnc } = deriveAeadKeyFromEcdh({
    skLocalB64: inputs.skGatewayB64,
    pkRemoteB64: inputs.pkDeviceB64,
    sid: inputs.sid,
  });
  return aeadDecrypt({
    kEnc,
    nonceB64: inputs.nonceB64,
    sid: inputs.sid,
    ciphertextB64: inputs.ciphertextB64,
  });
}

/**
 * Encrypt a plaintext payload. Used by tests; also used by any future
 * gateway-to-device encrypted ACK path.
 *
 * Emits (nonce, ciphertext||tag) both base64url-encoded. If the caller
 * passes an explicit `nonceB64`, it is used verbatim; otherwise a
 * fresh 12-byte random nonce is generated.
 */
export function aeadEncryptWithSessionKey(opts: {
  kEnc: Buffer;
  sid: string;
  plaintext: Buffer | Uint8Array;
  nonceB64?: NonceB64;
}): EncryptOutput {
  if (opts.kEnc.length !== AEAD_KEY_BYTES) {
    throw new Error(`pair-crypto: AEAD key must be ${AEAD_KEY_BYTES} bytes`);
  }
  const nonceBuf =
    opts.nonceB64 !== undefined
      ? Buffer.from(opts.nonceB64, 'base64url')
      : randomBytes(AEAD_NONCE_BYTES);
  if (nonceBuf.length !== AEAD_NONCE_BYTES) {
    throw new Error(`pair-crypto: nonce must be ${AEAD_NONCE_BYTES} bytes`);
  }

  const pt = Buffer.isBuffer(opts.plaintext) ? opts.plaintext : Buffer.from(opts.plaintext);
  const cipher = createCipheriv('aes-256-gcm', opts.kEnc, nonceBuf, {
    authTagLength: AEAD_TAG_BYTES,
  });
  cipher.setAAD(Buffer.from(opts.sid, 'utf-8'), { plaintextLength: pt.length });
  const ct = Buffer.concat([cipher.update(pt), cipher.final()]);
  const tag = cipher.getAuthTag();
  return {
    nonceB64: nonceBuf.toString('base64url'),
    ciphertextB64: Buffer.concat([ct, tag]).toString('base64url'),
  };
}

/**
 * One-shot encrypt: ECDH + HKDF + AEAD (caller supplies both sides).
 * Used by the test vectors and future 4.x features. The real device
 * side does this in the browser, not here.
 */
export function encryptPairingPayload(inputs: EncryptInputs): EncryptOutput {
  const { kEnc } = deriveAeadKeyFromEcdh({
    skLocalB64: inputs.skLocalB64,
    pkRemoteB64: inputs.pkRemoteB64,
    sid: inputs.sid,
  });
  return aeadEncryptWithSessionKey({
    kEnc,
    sid: inputs.sid,
    plaintext: inputs.plaintext,
    nonceB64: inputs.nonceB64,
  });
}

// ---------------------------------------------------------------------------
// Constant-time secondary-code comparison
// ---------------------------------------------------------------------------

/**
 * Constant-time compare two 6-digit numeric strings. Used by the HTTP
 * start/respond handlers to check the user-supplied secondary code
 * against the session's expected code.
 *
 * Returns true on match, false otherwise. Length mismatch returns
 * false without short-circuit leak of which side was shorter.
 *
 * Uses Node `timingSafeEqual`, which requires equal-length inputs.
 * We pad the SHORTER input with NULs and always compare a fixed
 * 6-byte window — the length check happens BEFORE the actual compare
 * and uses boolean AND at the end so both branches run to completion.
 */
export function compareSecondaryCodesCT(a: string, b: string): boolean {
  const aBuf = Buffer.from(a, 'utf-8');
  const bBuf = Buffer.from(b, 'utf-8');
  const lenMatch = aBuf.length === bBuf.length;
  // Always compare a constant window so the total work is independent
  // of the actual input lengths. Pad the shorter to the longer with
  // zero bytes; if lengths diverge we force lenMatch=false below.
  const max = Math.max(aBuf.length, bBuf.length, 6);
  const aPad = Buffer.alloc(max);
  const bPad = Buffer.alloc(max);
  aBuf.copy(aPad);
  bBuf.copy(bPad);
  const byteMatch = timingSafeEqual(aPad, bPad);
  return lenMatch && byteMatch;
}
