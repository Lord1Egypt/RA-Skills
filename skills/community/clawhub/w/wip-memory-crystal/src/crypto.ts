// memory-crystal/crypto.ts — Client-side encryption for ephemeral relay.
// AES-256-GCM encryption, HMAC-SHA256 signing, HKDF key derivation.
// Key never leaves trusted machines. Worker sees only ciphertext.

import { readFileSync, existsSync } from 'node:fs';
import { createCipheriv, createDecipheriv, createHmac, randomBytes, hkdfSync } from 'node:crypto';
import { resolveSecretPath } from './ldm.js';

const KEY_PATH = process.env.CRYSTAL_RELAY_KEY_PATH || resolveSecretPath('crystal-relay-key');

// ── Key Management ──

export function loadRelayKey(): Buffer {
  if (!existsSync(KEY_PATH)) {
    throw new Error(
      `Relay key not found at ${KEY_PATH}\n` +
      `Generate one: mkdir -p ~/.ldm/secrets && openssl rand -base64 32 > ~/.ldm/secrets/crystal-relay-key && chmod 600 ~/.ldm/secrets/crystal-relay-key\n` +
      `Or run: crystal pair`
    );
  }
  const raw = readFileSync(KEY_PATH, 'utf-8').trim();
  const key = Buffer.from(raw, 'base64');
  if (key.length !== 32) {
    throw new Error(`Relay key must be 32 bytes (256 bits). Got ${key.length} bytes. Regenerate with: openssl rand -base64 32`);
  }
  return key;
}

function deriveSigningKey(masterKey: Buffer): Buffer {
  return Buffer.from(hkdfSync('sha256', masterKey, '', 'crystal-relay-sign', 32));
}

// ── AES-256-GCM Encryption ──

export interface EncryptedPayload {
  v: 1;                // version
  nonce: string;       // 12 bytes, base64
  ciphertext: string;  // base64
  tag: string;         // 16 bytes, base64 (GCM auth tag)
  hmac: string;        // 32 bytes, hex (HMAC-SHA256 over nonce+ciphertext+tag)
}

export function encrypt(plaintext: Buffer, masterKey: Buffer): EncryptedPayload {
  // Random 96-bit nonce — never reuse with same key
  const nonce = randomBytes(12);

  const cipher = createCipheriv('aes-256-gcm', masterKey, nonce);
  const ciphertext = Buffer.concat([cipher.update(plaintext), cipher.final()]);
  const tag = cipher.getAuthTag();

  // HMAC over ciphertext proves origin (sender had the signing key)
  const signingKey = deriveSigningKey(masterKey);
  const hmacData = Buffer.concat([nonce, ciphertext, tag]);
  const hmac = createHmac('sha256', signingKey).update(hmacData).digest('hex');

  return {
    v: 1,
    nonce: nonce.toString('base64'),
    ciphertext: ciphertext.toString('base64'),
    tag: tag.toString('base64'),
    hmac,
  };
}

export function decrypt(payload: EncryptedPayload, masterKey: Buffer): Buffer {
  if (payload.v !== 1) {
    throw new Error(`Unknown payload version: ${payload.v}`);
  }

  const nonce = Buffer.from(payload.nonce, 'base64');
  const ciphertext = Buffer.from(payload.ciphertext, 'base64');
  const tag = Buffer.from(payload.tag, 'base64');

  // Verify HMAC first — confirms origin before decrypting
  const signingKey = deriveSigningKey(masterKey);
  const hmacData = Buffer.concat([nonce, ciphertext, tag]);
  const expectedHmac = createHmac('sha256', signingKey).update(hmacData).digest('hex');

  if (payload.hmac !== expectedHmac) {
    throw new Error('HMAC verification failed — blob rejected (tampered or wrong key)');
  }

  // Decrypt
  const decipher = createDecipheriv('aes-256-gcm', masterKey, nonce);
  decipher.setAuthTag(tag);
  return Buffer.concat([decipher.update(ciphertext), decipher.final()]);
}

// ── Convenience wrappers ──

export function encryptJSON(data: unknown, masterKey: Buffer): EncryptedPayload {
  const plaintext = Buffer.from(JSON.stringify(data), 'utf-8');
  return encrypt(plaintext, masterKey);
}

export function decryptJSON<T = unknown>(payload: EncryptedPayload, masterKey: Buffer): T {
  const plaintext = decrypt(payload, masterKey);
  return JSON.parse(plaintext.toString('utf-8')) as T;
}

export function encryptFile(filePath: string, masterKey: Buffer): EncryptedPayload {
  const plaintext = readFileSync(filePath);
  return encrypt(plaintext, masterKey);
}

// ── Pairing ──

export const RELAY_KEY_PATH = KEY_PATH;

export function generateRelayKey(): Buffer {
  return randomBytes(32);
}

export function encodePairingString(key: Buffer): string {
  if (key.length !== 32) throw new Error('Key must be 32 bytes');
  return `mc1:${key.toString('base64')}`;
}

export function decodePairingString(str: string): Buffer {
  const trimmed = str.trim();
  if (!trimmed.startsWith('mc1:')) {
    throw new Error('Invalid pairing string (expected mc1: prefix)');
  }
  const key = Buffer.from(trimmed.slice(4), 'base64');
  if (key.length !== 32) {
    throw new Error(`Invalid key length: expected 32 bytes, got ${key.length}`);
  }
  return key;
}

// ── Integrity hash for mirror snapshots ──

import { createHash } from 'node:crypto';

export function hashBuffer(data: Buffer): string {
  return createHash('sha256').update(data).digest('hex');
}
