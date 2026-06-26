import fs from 'node:fs';
import path from 'node:path';
import { CONFIG_DIR } from './config.js';

const IDENTITY_FILE = path.join(CONFIG_DIR, 'identity.json');

export interface Identity {
  agentId: string;
  publicKey: string;
  secretKey: string;
}

export function loadIdentity(): Identity | null {
  try {
    const raw = fs.readFileSync(IDENTITY_FILE, 'utf-8');
    return JSON.parse(raw) as Identity;
  } catch {
    return null;
  }
}

export function saveIdentity(identity: Identity): void {
  fs.mkdirSync(CONFIG_DIR, { recursive: true });
  // Back up existing identity before overwriting — the secret key is unrecoverable
  if (fs.existsSync(IDENTITY_FILE)) {
    fs.copyFileSync(IDENTITY_FILE, `${IDENTITY_FILE}.bak`);
  }
  fs.writeFileSync(IDENTITY_FILE, JSON.stringify(identity, null, 2), { encoding: 'utf-8', mode: 0o600 });
}
