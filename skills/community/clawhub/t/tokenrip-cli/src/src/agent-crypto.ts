import { createCipheriv, createDecipheriv, randomBytes, hkdfSync } from 'node:crypto';
import { ed25519, x25519 } from '@noble/curves/ed25519.js';
import { agentIdToPublicKey } from './crypto.js';
import { CliError } from './errors.js';
import type { StoredIdentity } from './identities.js';

interface ExportBlob {
  version: number;
  fromAgentId: string;
  nonce: string;
  ciphertext: string;
  tag: string;
}

function deriveSharedKey(mySecretKeyHex: string, theirPublicKeyHex: string): Buffer {
  const myX25519 = ed25519.utils.toMontgomerySecret(Buffer.from(mySecretKeyHex, 'hex'));
  const theirX25519 = ed25519.utils.toMontgomery(Buffer.from(theirPublicKeyHex, 'hex'));
  const shared = x25519.getSharedSecret(myX25519, theirX25519);
  return Buffer.from(
    hkdfSync('sha256', Buffer.from(shared), '', 'tokenrip-agent-export-v1', 32),
  );
}

export function encryptIdentityForAgent(
  identity: StoredIdentity,
  recipientAgentId: string,
  senderSecretKeyHex: string,
): string {
  const recipientPubHex = agentIdToPublicKey(recipientAgentId);
  const key = deriveSharedKey(senderSecretKeyHex, recipientPubHex);
  const nonce = randomBytes(12);
  const cipher = createCipheriv('aes-256-gcm', key, nonce);
  const plaintext = JSON.stringify(identity);
  const encrypted = Buffer.concat([cipher.update(plaintext, 'utf-8'), cipher.final()]);
  const tag = cipher.getAuthTag();

  const blob: ExportBlob = {
    version: 1,
    fromAgentId: identity.agentId,
    nonce: nonce.toString('base64url'),
    ciphertext: encrypted.toString('base64url'),
    tag: tag.toString('base64url'),
  };

  return Buffer.from(JSON.stringify(blob)).toString('base64url');
}

export function decryptIdentityFromAgent(
  encodedBlob: string,
  recipientSecretKeyHex: string,
): StoredIdentity {
  let parsed: ExportBlob;
  try {
    parsed = JSON.parse(Buffer.from(encodedBlob, 'base64url').toString('utf-8'));
  } catch {
    throw new CliError('INVALID_EXPORT', 'Invalid export blob. Check the file contents.');
  }

  if (parsed.version !== 1) {
    throw new CliError(
      'UNSUPPORTED_VERSION',
      `Export blob version ${parsed.version} is not supported. Update your CLI.`,
    );
  }

  const senderPubHex = agentIdToPublicKey(parsed.fromAgentId);
  const key = deriveSharedKey(recipientSecretKeyHex, senderPubHex);
  const nonce = Buffer.from(parsed.nonce, 'base64url');
  const ciphertext = Buffer.from(parsed.ciphertext, 'base64url');
  const tag = Buffer.from(parsed.tag, 'base64url');

  try {
    const decipher = createDecipheriv('aes-256-gcm', key, nonce);
    decipher.setAuthTag(tag);
    const decrypted = Buffer.concat([decipher.update(ciphertext), decipher.final()]);
    return JSON.parse(decrypted.toString('utf-8')) as StoredIdentity;
  } catch {
    throw new CliError(
      'DECRYPT_FAILED',
      'Decryption failed. Wrong recipient agent or corrupted blob.',
    );
  }
}
