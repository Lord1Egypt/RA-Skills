// @ts-check

/**
 * Heartbeat log management for SPM v4 session tracking.
 *
 * Provides an append-only heartbeat log backed by a JSON-lines file.
 * Each heartbeat records session identity, active task, status, and a
 * free-form note so recovery components can reconstruct execution flow.
 *
 * @module session/heartbeat
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

/**
 * @typedef {Object} Heartbeat
 * @property {string}  timestamp   – ISO-8601 UTC string (e.g. "2026-07-04T17:30:00.000Z")
 * @property {string}  sessionId   – Unique session identifier
 * @property {string}  activeTask  – Name or ID of the currently active task
 * @property {string}  status      – Status label (e.g. "running", "paused", "completed", "failed")
 * @property {string}  [note]      – Optional free-text note
 */

const DEFAULT_PATH = '.spm/heartbeats.jsonl';

/**
 * Normalize the heartbeat file path, defaulting when not provided.
 * @param {string} [filePath] – Custom path to the dot-heartbeat file
 * @returns {string} Resolved absolute path
 */
function resolvePath(filePath) {
  return resolve(process.cwd(), filePath || DEFAULT_PATH);
}

/**
 * Ensure the parent directory of a file path exists.
 * @param {string} absPath – Absolute file path
 */
function ensureParentDir(absPath) {
  const dir = dirname(absPath);
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
}

/**
 * Append a heartbeat entry to the heartbeat log.
 *
 * Each entry is serialised as a single JSON line (JSON-lines format).
 * The file is created if it does not exist.
 *
 * @param {Heartbeat} heartbeat – The heartbeat record to persist
 * @param {string}    [filePath]– Custom path to the heartbeat file
 * @throws {Error} If heartbeat is missing required fields
 */
export function log(heartbeat, filePath) {
  if (!heartbeat.timestamp || !heartbeat.sessionId || !heartbeat.activeTask) {
    throw new Error(
      'Heartbeat requires at least "timestamp", "sessionId", and "activeTask".'
    );
  }
  const absPath = resolvePath(filePath);
  ensureParentDir(absPath);
  writeFileSync(absPath, JSON.stringify(heartbeat) + '\n', { flag: 'as' });
}

/**
 * Read all heartbeat entries from the log, in chronological order.
 *
 * Returns an empty array when the file does not exist or is empty.
 *
 * @param {string} [filePath] – Custom path to the heartbeat file
 * @returns {Heartbeat[]} All parsed heartbeats
 */
export function readAll(filePath) {
  const absPath = resolvePath(filePath);
  if (!existsSync(absPath)) {
    return [];
  }
  const raw = readFileSync(absPath, 'utf-8').trim();
  if (!raw) {
    return [];
  }
  return raw
    .split('\n')
    .filter(Boolean)
    .map((line) => /** @type {Heartbeat} */ (JSON.parse(line)));
}

/**
 * Return the most recent heartbeat entry.
 *
 * @param {string} [filePath] – Custom path to the heartbeat file
 * @returns {Heartbeat | null} The latest heartbeat, or null if the log is empty
 */
export function getLatest(filePath) {
  const all = readAll(filePath);
  return all.length > 0 ? all[all.length - 1] : null;
}

/**
 * Filter heartbeats belonging to a specific session.
 *
 * @param {string} sessionId – Session identifier to filter by
 * @param {string} [filePath]– Custom path to the heartbeat file
 * @returns {Heartbeat[]} Heartbeats matching the session, in chronological order
 */
export function getBySession(sessionId, filePath) {
  return readAll(filePath).filter((hb) => hb.sessionId === sessionId);
}