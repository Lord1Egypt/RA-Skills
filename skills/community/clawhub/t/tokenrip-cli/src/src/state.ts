import fs from 'node:fs';
import path from 'node:path';
import { CONFIG_DIR } from './config.js';

const STATE_FILE = path.join(CONFIG_DIR, 'state.json');

export interface TokenripState {
  lastInboxPoll?: string; // ISO 8601 timestamp
}

export function loadState(): TokenripState {
  try {
    const raw = fs.readFileSync(STATE_FILE, 'utf-8');
    return JSON.parse(raw) as TokenripState;
  } catch {
    return {};
  }
}

export function saveState(state: TokenripState): void {
  fs.mkdirSync(CONFIG_DIR, { recursive: true });
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2), 'utf-8');
}
