// memory-crystal/pair.ts — QR code pairing for relay key sharing.
// Transfers the encryption key between devices without touching a server.
// Physical proximity only. Same security model as AirDrop.

import { existsSync, writeFileSync, mkdirSync, chmodSync } from 'node:fs';
import { dirname } from 'node:path';
import {
  loadRelayKey,
  generateRelayKey,
  encodePairingString,
  decodePairingString,
  RELAY_KEY_PATH,
} from './crypto.js';

// qrcode-terminal has no types, import as default
import qrcode from 'qrcode-terminal';

function generateQR(text: string): Promise<string> {
  return new Promise((resolve) => {
    qrcode.generate(text, { small: true }, (code: string) => {
      resolve(code);
    });
  });
}

function saveKey(key: Buffer): void {
  const dir = dirname(RELAY_KEY_PATH);
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
  writeFileSync(RELAY_KEY_PATH, key.toString('base64') + '\n', { mode: 0o600 });
  // Ensure permissions even if file existed
  try { chmodSync(RELAY_KEY_PATH, 0o600); } catch {}
}

// ── crystal pair (show QR code) ──

export async function pairShow(): Promise<void> {
  let key: Buffer;

  try {
    key = loadRelayKey();
    console.log('Relay key found.\n');
  } catch {
    console.log('No relay key found. Generating one...');
    key = generateRelayKey();
    saveKey(key);
    console.log(`Key saved to ${RELAY_KEY_PATH}\n`);
  }

  const pairingString = encodePairingString(key);

  console.log('Scan this QR code from your other device:\n');
  const qr = await generateQR(pairingString);
  console.log(qr);

  console.log('Or copy this pairing code:\n');
  console.log(`  ${pairingString}\n`);
  console.log('On the other device, run:');
  console.log(`  crystal pair --code ${pairingString}\n`);
}

// ── crystal pair --code <string> (receive key) ──

export function pairReceive(code: string): void {
  const key = decodePairingString(code);

  if (existsSync(RELAY_KEY_PATH)) {
    try {
      const existing = loadRelayKey();
      if (existing.equals(key)) {
        console.log('This device already has the same key. Nothing to do.');
        return;
      }
      console.log('Replacing existing relay key with new key from pairing code.');
    } catch {
      // Existing key is corrupt. Overwrite.
    }
  }

  saveKey(key);
  console.log(`Key received and saved to ${RELAY_KEY_PATH}`);
  console.log('Relay encryption is now active on this device.');
}
