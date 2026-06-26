/**
 * lib/messages.mjs
 * File-based inter-session message bus.
 * Enables sessions to communicate without shared memory or network sockets.
 * Messages are JSON files in ~/.ldm/messages/. Processed messages move to _processed/.
 * Zero external dependencies.
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync, readdirSync, renameSync, unlinkSync, statSync } from 'node:fs';
import { join, basename } from 'node:path';
import { randomUUID } from 'node:crypto';

const HOME = process.env.HOME || '';
const LDM_ROOT = join(HOME, '.ldm');
const MESSAGES_DIR = join(LDM_ROOT, 'messages');
const PROCESSED_DIR = join(MESSAGES_DIR, '_processed');

// ── Helpers ──

function readJSON(path) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return null;
  }
}

function writeJSON(path, data) {
  mkdirSync(join(path, '..'), { recursive: true });
  writeFileSync(path, JSON.stringify(data, null, 2) + '\n');
}

// ── Message operations ──

/**
 * Send a message. Writes a JSON file to ~/.ldm/messages/{uuid}.json.
 * @param {Object} opts
 * @param {string} opts.from - Sender session name
 * @param {string} opts.to - Recipient session name (or "all" for broadcast)
 * @param {string} opts.body - Message content
 * @param {string} [opts.type] - Message type: "chat", "system", "update-available"
 * @returns {string|null} Message ID or null on failure
 */
export function sendMessage({ from, to, body, type = 'chat' }) {
  try {
    mkdirSync(MESSAGES_DIR, { recursive: true });
    const id = randomUUID();
    const messagePath = join(MESSAGES_DIR, `${id}.json`);
    const data = {
      id,
      from: from || 'unknown',
      to: to || 'all',
      body: body || '',
      type: type || 'chat',
      timestamp: new Date().toISOString(),
    };
    writeJSON(messagePath, data);
    return id;
  } catch {
    return null;
  }
}

/**
 * Read messages addressed to a session (or broadcast to "all").
 * @param {string} sessionName - Session name to read messages for
 * @param {Object} [opts]
 * @param {boolean} [opts.markRead] - Move messages to _processed/ after reading
 * @param {string} [opts.type] - Filter by message type
 * @returns {Array} Array of message objects
 */
export function readMessages(sessionName, { markRead = false, type } = {}) {
  try {
    if (!existsSync(MESSAGES_DIR)) return [];

    const files = readdirSync(MESSAGES_DIR).filter(f => f.endsWith('.json'));
    const messages = [];

    for (const file of files) {
      const messagePath = join(MESSAGES_DIR, file);
      const data = readJSON(messagePath);
      if (!data) continue;

      // Match: addressed to this session or broadcast to "all"
      if (data.to !== sessionName && data.to !== 'all') continue;

      // Filter by type if specified
      if (type && data.type !== type) continue;

      messages.push(data);

      // Move to processed if markRead
      if (markRead) {
        try {
          mkdirSync(PROCESSED_DIR, { recursive: true });
          renameSync(messagePath, join(PROCESSED_DIR, file));
        } catch {}
      }
    }

    // Sort by timestamp (oldest first)
    messages.sort((a, b) => (a.timestamp || '').localeCompare(b.timestamp || ''));
    return messages;
  } catch {
    return [];
  }
}

/**
 * Count unread messages for a session.
 * @param {string} sessionName - Session name
 * @returns {number}
 */
export function unreadCount(sessionName) {
  try {
    const messages = readMessages(sessionName, { markRead: false });
    return messages.length;
  } catch {
    return 0;
  }
}

/**
 * Acknowledge (mark as read) a single message by ID.
 * Moves the message file to _processed/.
 * @param {string} messageId - Message UUID
 * @returns {boolean}
 */
export function acknowledgeMessage(messageId) {
  try {
    const messagePath = join(MESSAGES_DIR, `${messageId}.json`);
    if (!existsSync(messagePath)) return false;

    mkdirSync(PROCESSED_DIR, { recursive: true });
    renameSync(messagePath, join(PROCESSED_DIR, `${messageId}.json`));
    return true;
  } catch {
    return false;
  }
}

/**
 * Clean up old messages.
 * Moves messages older than maxAgeDays to _processed/.
 * Deletes _processed/ files older than 30 days.
 * @param {Object} [opts]
 * @param {number} [opts.maxAgeDays] - Max age for unprocessed messages (default: 7)
 * @returns {{ moved: number, deleted: number }}
 */
export function cleanupMessages({ maxAgeDays = 7 } = {}) {
  let moved = 0;
  let deleted = 0;

  try {
    const now = Date.now();
    const maxAgeMs = maxAgeDays * 24 * 60 * 60 * 1000;
    const deleteAgeMs = 30 * 24 * 60 * 60 * 1000;

    // Move old unprocessed messages
    if (existsSync(MESSAGES_DIR)) {
      const files = readdirSync(MESSAGES_DIR).filter(f => f.endsWith('.json'));
      for (const file of files) {
        const messagePath = join(MESSAGES_DIR, file);
        try {
          const data = readJSON(messagePath);
          if (!data?.timestamp) continue;
          const age = now - new Date(data.timestamp).getTime();
          if (age > maxAgeMs) {
            mkdirSync(PROCESSED_DIR, { recursive: true });
            renameSync(messagePath, join(PROCESSED_DIR, file));
            moved++;
          }
        } catch {}
      }
    }

    // Delete old processed messages
    if (existsSync(PROCESSED_DIR)) {
      const files = readdirSync(PROCESSED_DIR).filter(f => f.endsWith('.json'));
      for (const file of files) {
        const filePath = join(PROCESSED_DIR, file);
        try {
          const stat = statSync(filePath);
          const age = now - stat.mtimeMs;
          if (age > deleteAgeMs) {
            unlinkSync(filePath);
            deleted++;
          }
        } catch {}
      }
    }
  } catch {}

  return { moved, deleted };
}
