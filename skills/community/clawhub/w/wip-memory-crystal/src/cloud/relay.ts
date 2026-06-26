// memory-crystal/cloud/relay.ts — Encrypt + drop to relay from the cloud Worker.
// Uses Web Crypto API (not Node.js crypto) since this runs in a Cloudflare Worker.
// Mirrors the protocol in crypto.ts but uses browser-compatible APIs.

import type { Env, EncryptedPayload, RelayDrop, AttachmentData } from './types.js';

// ── Key Management ──

function base64ToBuffer(b64: string): ArrayBuffer {
  const binary = atob(b64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
  return bytes.buffer;
}

function bufferToBase64(buf: ArrayBuffer): string {
  const bytes = new Uint8Array(buf);
  let binary = '';
  for (const b of bytes) binary += String.fromCharCode(b);
  return btoa(binary);
}

function bufferToHex(buf: ArrayBuffer): string {
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
}

async function deriveSigningKey(masterKey: ArrayBuffer): Promise<CryptoKey> {
  // HKDF: derive signing key from master key
  const keyMaterial = await crypto.subtle.importKey('raw', masterKey, 'HKDF', false, ['deriveBits']);
  const derivedBits = await crypto.subtle.deriveBits(
    { name: 'HKDF', hash: 'SHA-256', salt: new Uint8Array(0), info: new TextEncoder().encode('crystal-relay-sign') },
    keyMaterial,
    256
  );
  return crypto.subtle.importKey('raw', derivedBits, { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
}

// ── AES-256-GCM Encryption (Web Crypto) ──

export async function encryptJSON(data: unknown, relayKeyBase64: string): Promise<EncryptedPayload> {
  const masterKey = base64ToBuffer(relayKeyBase64);
  const plaintext = new TextEncoder().encode(JSON.stringify(data));

  // Random 96-bit nonce
  const nonce = crypto.getRandomValues(new Uint8Array(12));

  // Import key for AES-GCM
  const aesKey = await crypto.subtle.importKey('raw', masterKey, 'AES-GCM', false, ['encrypt']);

  // Encrypt (GCM appends auth tag to ciphertext)
  const encrypted = await crypto.subtle.encrypt({ name: 'AES-GCM', iv: nonce }, aesKey, plaintext);

  // AES-GCM output: ciphertext + 16-byte tag appended
  const encryptedBytes = new Uint8Array(encrypted);
  const ciphertext = encryptedBytes.slice(0, encryptedBytes.length - 16);
  const tag = encryptedBytes.slice(encryptedBytes.length - 16);

  // HMAC over nonce + ciphertext + tag
  const signingKey = await deriveSigningKey(masterKey);
  const hmacData = new Uint8Array([...nonce, ...ciphertext, ...tag]);
  const hmacSig = await crypto.subtle.sign('HMAC', signingKey, hmacData);

  return {
    v: 1,
    nonce: bufferToBase64(nonce.buffer),
    ciphertext: bufferToBase64(ciphertext.buffer),
    tag: bufferToBase64(tag.buffer),
    hmac: bufferToHex(hmacSig),
  };
}

// ── Drop to Relay ──

export async function dropToRelay(env: Env, drop: RelayDrop): Promise<{ ok: boolean; id: string }> {
  const payload = await encryptJSON(drop, env.CRYSTAL_RELAY_KEY);
  const body = JSON.stringify(payload);

  const id = crypto.randomUUID();
  const channel = 'chatgpt';
  const key = `${channel}/${id}`;
  const now = new Date().toISOString();

  await env.RELAY.put(key, body, {
    customMetadata: {
      agent_id: drop.agent_id,
      dropped_at: now,
      size: String(body.length),
      type: drop.type,
    },
  });

  return { ok: true, id };
}

// ── Drop Binary Attachment to Relay ──
// Binary data gets its own R2 object (encrypted). The metadata drop references it by key.

export async function dropAttachment(
  env: Env,
  binary: ArrayBuffer,
  metadata: Omit<AttachmentData, 'r2_key'>,
  agentId: string,
  userId: string
): Promise<{ ok: boolean; id: string; r2_key: string }> {
  const id = crypto.randomUUID();
  const blobKey = `chatgpt-attachments/${id}`;

  // Encrypt the binary data
  const masterKey = base64ToBuffer(env.CRYSTAL_RELAY_KEY);
  const nonce = crypto.getRandomValues(new Uint8Array(12));
  const aesKey = await crypto.subtle.importKey('raw', masterKey, 'AES-GCM', false, ['encrypt']);
  const encrypted = await crypto.subtle.encrypt({ name: 'AES-GCM', iv: nonce }, aesKey, binary);

  // Store encrypted binary in R2
  const now = new Date().toISOString();
  const encryptedPayload = JSON.stringify({
    v: 1,
    nonce: bufferToBase64(nonce.buffer),
    data: bufferToBase64(encrypted),
  });

  await env.RELAY.put(blobKey, encryptedPayload, {
    customMetadata: {
      agent_id: agentId,
      dropped_at: now,
      size: String(binary.byteLength),
      type: 'attachment',
      mime_type: metadata.mime_type,
      filename: metadata.filename,
    },
  });

  // Now drop the metadata as a normal relay drop (references the blob key)
  const attachmentData: AttachmentData = {
    ...metadata,
    r2_key: blobKey,
  };

  const drop: RelayDrop = {
    type: 'attachment',
    agent_id: agentId,
    user_id: userId,
    timestamp: now,
    data: attachmentData,
  };

  const metaDrop = await dropToRelay(env, drop);
  return { ok: true, id: metaDrop.id, r2_key: blobKey };
}
