/**
 * E2E Crypto — Isomorphic AES-256-CTR encryption with PBKDF2 key derivation.
 *
 * Works in both Web Crypto API (browser / Cloudflare Workers) and Node.js.
 *
 * Design (compatible with BotChat's approach, adapted for WTT):
 *   - Salt = "wtt-e2e-shared" (fixed, so same password → same key for all parties)
 *   - PBKDF2-SHA256 with 310,000 iterations (OWASP 2023)
 *   - AES-256-CTR with nonce derived from contextId via HKDF-SHA256
 *   - Zero ciphertext overhead (no tag/MAC — CTR mode)
 *   - Each contextId MUST be globally unique and used ONLY ONCE per key
 */

const isNode =
  typeof globalThis.process !== "undefined" &&
  typeof globalThis.process.versions?.node === "string";

const PBKDF2_ITERATIONS = 310_000;
const KEY_LENGTH = 32; // 256 bits
const NONCE_LENGTH = 16; // AES-CTR counter block
const SALT_PREFIX = "wtt-e2e-shared";

function utf8Encode(str: string): Uint8Array {
  return new TextEncoder().encode(str);
}

function utf8Decode(buf: Uint8Array): string {
  return new TextDecoder().decode(buf);
}

// ---------------------------------------------------------------------------
// Web Crypto implementation (browser + Cloudflare Workers)
// ---------------------------------------------------------------------------

async function deriveKeyWeb(password: string, _agentId?: string): Promise<Uint8Array> {
  const enc = utf8Encode(password);
  const salt = utf8Encode(SALT_PREFIX);
  const baseKey = await crypto.subtle.importKey("raw", enc.buffer as ArrayBuffer, "PBKDF2", false, [
    "deriveBits",
  ]);
  const bits = await crypto.subtle.deriveBits(
    { name: "PBKDF2", salt: salt.buffer as ArrayBuffer, iterations: PBKDF2_ITERATIONS, hash: "SHA-256" },
    baseKey,
    KEY_LENGTH * 8,
  );
  return new Uint8Array(bits);
}

async function hkdfNonceWeb(key: Uint8Array, contextId: string): Promise<Uint8Array> {
  const hmacKey = await crypto.subtle.importKey(
    "raw",
    key.buffer as ArrayBuffer,
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const info = utf8Encode("nonce-" + contextId);
  const input = new Uint8Array(info.length + 1);
  input.set(info);
  input[info.length] = 0x01;
  const full = await crypto.subtle.sign("HMAC", hmacKey, input.buffer as ArrayBuffer);
  return new Uint8Array(full).slice(0, NONCE_LENGTH);
}

async function encryptWeb(key: Uint8Array, plaintext: Uint8Array, contextId: string): Promise<Uint8Array> {
  const counter = await hkdfNonceWeb(key, contextId);
  const aesKey = await crypto.subtle.importKey("raw", key.buffer as ArrayBuffer, { name: "AES-CTR" }, false, [
    "encrypt",
  ]);
  const ciphertext = await crypto.subtle.encrypt(
    { name: "AES-CTR", counter: counter.buffer as ArrayBuffer, length: 128 },
    aesKey,
    plaintext.buffer as ArrayBuffer,
  );
  return new Uint8Array(ciphertext);
}

async function decryptWeb(key: Uint8Array, ciphertext: Uint8Array, contextId: string): Promise<Uint8Array> {
  const counter = await hkdfNonceWeb(key, contextId);
  const aesKey = await crypto.subtle.importKey("raw", key.buffer as ArrayBuffer, { name: "AES-CTR" }, false, [
    "decrypt",
  ]);
  const plaintext = await crypto.subtle.decrypt(
    { name: "AES-CTR", counter: counter.buffer as ArrayBuffer, length: 128 },
    aesKey,
    ciphertext.buffer as ArrayBuffer,
  );
  return new Uint8Array(plaintext);
}

// ---------------------------------------------------------------------------
// Node.js implementation
// ---------------------------------------------------------------------------

let _nodeCrypto: typeof import("node:crypto") | null = null;
let _nodeUtil: typeof import("node:util") | null = null;

async function ensureNodeModules(): Promise<void> {
  if (_nodeCrypto && _nodeUtil) return;
  _nodeCrypto = await import("node:crypto");
  _nodeUtil = await import("node:util");
}

async function deriveKeyNode(password: string, _agentId?: string): Promise<Uint8Array> {
  await ensureNodeModules();
  const pbkdf2Async = _nodeUtil!.promisify(_nodeCrypto!.pbkdf2);
  const salt = SALT_PREFIX;
  const buf = await pbkdf2Async(password, salt, PBKDF2_ITERATIONS, KEY_LENGTH, "sha256");
  return new Uint8Array(buf);
}

async function hkdfNonceNode(key: Uint8Array, contextId: string): Promise<Uint8Array> {
  await ensureNodeModules();
  const info = utf8Encode("nonce-" + contextId);
  const input = new Uint8Array(info.length + 1);
  input.set(info);
  input[info.length] = 0x01;
  const hmac = _nodeCrypto!.createHmac("sha256", Buffer.from(key));
  hmac.update(Buffer.from(input));
  const full = hmac.digest();
  return new Uint8Array(full.buffer, full.byteOffset, NONCE_LENGTH);
}

async function encryptNode(key: Uint8Array, plaintext: Uint8Array, contextId: string): Promise<Uint8Array> {
  await ensureNodeModules();
  const iv = await hkdfNonceNode(key, contextId);
  const cipher = _nodeCrypto!.createCipheriv("aes-256-ctr", Buffer.from(key), Buffer.from(iv));
  const encrypted = Buffer.concat([cipher.update(Buffer.from(plaintext)), cipher.final()]);
  return new Uint8Array(encrypted);
}

async function decryptNode(key: Uint8Array, ciphertext: Uint8Array, contextId: string): Promise<Uint8Array> {
  await ensureNodeModules();
  const iv = await hkdfNonceNode(key, contextId);
  const decipher = _nodeCrypto!.createDecipheriv("aes-256-ctr", Buffer.from(key), Buffer.from(iv));
  const decrypted = Buffer.concat([decipher.update(Buffer.from(ciphertext)), decipher.final()]);
  return new Uint8Array(decrypted);
}

// ---------------------------------------------------------------------------
// Public API — auto-selects implementation based on runtime
// ---------------------------------------------------------------------------

/**
 * Derive a 256-bit master key from the user's E2E password.
 * Uses PBKDF2-SHA256 with 310,000 iterations; salt = "wtt-e2e-shared".
 * agentId parameter is accepted but ignored (kept for API compatibility).
 * Same password always produces same key, enabling cross-party P2P decryption.
 */
export async function deriveKey(password: string, _agentId?: string): Promise<Uint8Array> {
  return isNode ? deriveKeyNode(password) : deriveKeyWeb(password);
}

/**
 * Encrypt plaintext string. Returns raw ciphertext bytes (same length as UTF-8 input).
 * ⚠️ Each contextId MUST be globally unique and used ONLY ONCE per key.
 */
export async function encryptText(key: Uint8Array, plaintext: string, contextId: string): Promise<Uint8Array> {
  const data = utf8Encode(plaintext);
  return isNode ? encryptNode(key, data, contextId) : encryptWeb(key, data, contextId);
}

/**
 * Decrypt ciphertext bytes back to plaintext string.
 * AES-CTR has no authentication — caller must handle garbled output gracefully.
 */
export async function decryptText(key: Uint8Array, ciphertext: Uint8Array, contextId: string): Promise<string> {
  const data = isNode ? await decryptNode(key, ciphertext, contextId) : await decryptWeb(key, ciphertext, contextId);
  return utf8Decode(data);
}

/** Encrypt raw bytes. Returns ciphertext of same length. */
export async function encryptBytes(key: Uint8Array, plaintext: Uint8Array, contextId: string): Promise<Uint8Array> {
  return isNode ? encryptNode(key, plaintext, contextId) : encryptWeb(key, plaintext, contextId);
}

/** Decrypt raw ciphertext bytes. */
export async function decryptBytes(
  key: Uint8Array,
  ciphertext: Uint8Array,
  contextId: string,
): Promise<Uint8Array> {
  return isNode ? decryptNode(key, ciphertext, contextId) : decryptWeb(key, ciphertext, contextId);
}

// ---------------------------------------------------------------------------
// Utility: base64 encode/decode for JSON transport
// ---------------------------------------------------------------------------

export function toBase64(data: Uint8Array): string {
  if (typeof Buffer !== "undefined") {
    return Buffer.from(data).toString("base64");
  }
  let binary = "";
  for (let i = 0; i < data.length; i++) {
    binary += String.fromCharCode(data[i]);
  }
  return btoa(binary);
}

export function fromBase64(b64: string): Uint8Array {
  if (typeof Buffer !== "undefined") {
    const buf = Buffer.from(b64, "base64");
    return new Uint8Array(buf.buffer, buf.byteOffset, buf.byteLength);
  }
  const binary = atob(b64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes;
}
