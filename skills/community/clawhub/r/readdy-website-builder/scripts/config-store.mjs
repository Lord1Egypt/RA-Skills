#!/usr/bin/env node

/**
 * Readdy API Key Config Store
 *
 * Standalone module for local API Key read/write.
 * Contains no network request logic.
 */

import path from 'path';
import fs from 'fs';
import os from 'os';

const CREDENTIALS_FILE = path.join(os.homedir(), '.openclaw', 'readdy.json');

export function loadApiKey() {
  try {
    return JSON.parse(fs.readFileSync(CREDENTIALS_FILE, 'utf8')).apiKey || '';
  } catch {
    return '';
  }
}

export function saveApiKey(key) {
  const dir = path.dirname(CREDENTIALS_FILE);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(CREDENTIALS_FILE, JSON.stringify({ apiKey: key }, null, 2) + '\n', { encoding: 'utf8', mode: 0o600 });
}

export function getCredentialsPath() {
  return CREDENTIALS_FILE;
}
