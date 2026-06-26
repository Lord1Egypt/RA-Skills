import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STATE_DIR = path.join(__dirname, '..', '..', 'data', 'state');

fs.mkdirSync(STATE_DIR, { recursive: true });

/**
 * Persist a value to local storage.
 *
 * @param {string} key - Storage key
 * @param {*} value - Any JSON-serializable value
 * @param {object} options
 * @param {number} options.ttl - Time to live in seconds (0 = forever)
 * @returns {object} { key, stored, expiresAt }
 */
export function persist(key, value, options = {}) {
  const { ttl = 0 } = options;

  const entry = {
    key,
    value,
    storedAt: new Date().toISOString(),
    expiresAt: ttl > 0 ? new Date(Date.now() + ttl * 1000).toISOString() : null,
  };

  const filepath = keyToPath(key);
  fs.writeFileSync(filepath, JSON.stringify(entry, null, 2));

  return {
    key,
    stored: true,
    expiresAt: entry.expiresAt,
  };
}

/**
 * Recall a stored value.
 *
 * @param {string} key - Storage key
 * @returns {*} The stored value, or null if not found/expired
 */
export function recall(key) {
  const filepath = keyToPath(key);

  if (!fs.existsSync(filepath)) {
    return null;
  }

  try {
    const entry = JSON.parse(fs.readFileSync(filepath, 'utf-8'));

    // Check TTL
    if (entry.expiresAt && new Date(entry.expiresAt) < new Date()) {
      // Expired — clean up
      fs.unlinkSync(filepath);
      return null;
    }

    return entry.value;
  } catch {
    return null;
  }
}

/**
 * Delete a stored value.
 *
 * @param {string} key - Storage key
 * @returns {boolean} true if deleted, false if not found
 */
export function forget(key) {
  const filepath = keyToPath(key);
  if (fs.existsSync(filepath)) {
    fs.unlinkSync(filepath);
    return true;
  }
  return false;
}

/**
 * List all stored keys.
 *
 * @returns {string[]} Array of stored keys
 */
export function listKeys() {
  const files = fs.readdirSync(STATE_DIR).filter(f => f.endsWith('.json'));
  return files.map(f => f.replace('.json', '').replace(/_/g, '/'));
}

function keyToPath(key) {
  // Sanitize key for filesystem
  const safe = key.replace(/[\/\\:*?"<>|]/g, '_');
  return path.join(STATE_DIR, `${safe}.json`);
}
