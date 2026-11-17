import { lock, unlock } from 'proper-lockfile';
import { writeFileSync, readFileSync, existsSync, mkdirSync, renameSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import crypto from 'node:crypto';

const MAX_RETRIES = 3;
const RETRY_DELAY_MS = 200;

/**
 * Generate a SHA-256 checksum for a JSON event string.
 */
function checksum(line) {
  return crypto.createHash('sha256').update(line).digest('hex').substring(0, 16);
}

/**
 * Append an event line to a JSONL file with file locking and atomic write.
 * Uses proper-lockfile for cross-process locking.
 * Writes to temp file, then renames atomically.
 */
export async function append(filePath, eventJson) {
  const absPath = resolve(filePath);
  const dir = dirname(absPath);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });

  let release;
  for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
    try {
      release = await lock(absPath, { retries: 3, stale: 5000 });
      break;
    } catch {
      if (attempt < MAX_RETRIES - 1) await new Promise(r => setTimeout(r, RETRY_DELAY_MS * (attempt + 1)));
      else throw new Error(`Could not acquire lock for ${filePath} after ${MAX_RETRIES} attempts`);
    }
  }

  try {
    // Add checksum to event
    const line = JSON.stringify({ ...eventJson, _cs: checksum(JSON.stringify(eventJson)) }) + '\n';
    // Write to temp file
    const tmpPath = absPath + '.tmp';
    const existing = existsSync(absPath) ? readFileSync(absPath, 'utf8') : '';
    writeFileSync(tmpPath, existing + line, 'utf8');
    // Atomic rename (crash-safe on most OS)
    renameSync(tmpPath, absPath);
  } finally {
    try { await unlock(absPath); } catch { /* best effort */ }
  }
}

/**
 * Read all valid event lines from a JSONL file.
 * Skips partial/corrupt lines for crash recovery.
 */
export function readAll(filePath) {
  const absPath = resolve(filePath);
  if (!existsSync(absPath)) return [];

  const content = readFileSync(absPath, 'utf8');
  const lines = content.split('\n').filter(l => l.trim());

  return lines
    .map((line, i) => {
      try {
        const parsed = JSON.parse(line);
        // Verify checksum if present
        if (parsed._cs) {
          const cs = parsed._cs;
          const { _cs, ...data } = parsed;
          if (checksum(JSON.stringify(data)) !== cs) {
            console.warn(`Line ${i + 1}: checksum mismatch, skipping corrupt event`);
            return null;
          }
        }
        return parsed;
      } catch {
        console.warn(`Line ${i + 1}: parse error, skipping corrupt event`);
        return null;
      }
    })
    .filter(Boolean);
}

/**
 * Repair a JSONL file: remove all corrupt lines and rewrite.
 */
export function repair(filePath) {
  const absPath = resolve(filePath);
  const validLines = readAll(absPath);
  writeFileSync(absPath, validLines.map(e => JSON.stringify(e) + '\n').join(''), 'utf8');
  return validLines.length;
}

/**
 * Read a range of events: from (0-indexed) to (exclusive).
 */
export function readRange(filePath, from = 0, to) {
  const events = readAll(filePath);
  return events.slice(from, to ?? events.length);
}

/**
 * Read the most recent N events.
 */
export function readRecent(filePath, n = 10) {
  const events = readAll(filePath);
  return events.slice(-n);
}

/**
 * Rotate an event file: archive it and start fresh.
 */
export function rotate(filePath, archivePath) {
  const absPath = resolve(filePath);
  if (existsSync(absPath)) {
    renameSync(absPath, resolve(archivePath));
  }
}

/**
 * Prune old event files from a directory, keeping only the most recent N files.
 */
export function prune(dir, keepCount = 10) {
  const fs = require('node:fs');
  const path = require('node:path');
  if (!existsSync(dir)) return;
  const files = fs.readdirSync(dir)
    .filter(f => f.endsWith('.jsonl'))
    .map(f => ({ name: f, time: fs.statSync(path.join(dir, f)).mtimeMs }))
    .sort((a, b) => b.time - a.time);
  files.slice(keepCount).forEach(f => fs.rmSync(path.join(dir, f.name)));
}