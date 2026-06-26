import { generateKeyPairSync, sign as ed25519Sign, createPrivateKey } from 'node:crypto';
import { bech32 } from 'bech32';

const AGENT_HRP = 'rip';
const BECH32_LIMIT = 90;

// ASN.1 DER prefix for Ed25519 PKCS8 private key (prepend to 32-byte raw key)
const PKCS8_ED25519_PREFIX = Buffer.from('302e020100300506032b657004220420', 'hex');

export interface Keypair {
  publicKeyHex: string;
  secretKeyHex: string;
}

export function generateKeypair(): Keypair {
  const { publicKey, privateKey } = generateKeyPairSync('ed25519');
  const rawPub = (publicKey.export({ type: 'spki', format: 'der' }) as Buffer).subarray(12);
  const rawPriv = (privateKey.export({ type: 'pkcs8', format: 'der' }) as Buffer).subarray(16);
  return {
    publicKeyHex: rawPub.toString('hex'),
    secretKeyHex: rawPriv.toString('hex'),
  };
}

export function publicKeyToAgentId(publicKeyHex: string): string {
  const bytes = Buffer.from(publicKeyHex, 'hex');
  const words = bech32.toWords(bytes);
  return bech32.encode(AGENT_HRP, words, BECH32_LIMIT);
}

export interface CapabilityTokenOptions {
  sub: string;
  iss: string;
  perm: string[];
  exp?: number;
  aud?: string;
}

export function sign(data: Buffer, secretKeyHex: string): Buffer {
  const rawKey = Buffer.from(secretKeyHex, 'hex');
  const derKey = Buffer.concat([PKCS8_ED25519_PREFIX, rawKey]);
  const keyObj = createPrivateKey({ key: derKey, format: 'der', type: 'pkcs8' });
  return ed25519Sign(null, data, keyObj);
}

export function signPayload(payload: Record<string, unknown>, secretKeyHex: string): string {
  const payloadB64 = Buffer.from(JSON.stringify(payload)).toString('base64url');
  const signature = sign(Buffer.from(payloadB64), secretKeyHex);
  return `${payloadB64}.${signature.toString('base64url')}`;
}

export function createCapabilityToken(opts: CapabilityTokenOptions, secretKeyHex: string): string {
  const payload: Record<string, unknown> = { sub: opts.sub, iss: opts.iss, perm: opts.perm };
  if (opts.exp != null) payload.exp = opts.exp;
  if (opts.aud != null) payload.aud = opts.aud;
  return signPayload(payload, secretKeyHex);
}
