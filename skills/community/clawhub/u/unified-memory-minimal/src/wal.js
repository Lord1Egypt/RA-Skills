/**
 * wal.js - Write-Ahead Log (WAL) Protocol
 * 
 * Ensures data durability by writing to WAL before actual storage.
 * Provides crash recovery by replaying WAL on startup.
 * 
 * Inspired by Elite Longterm Memory WAL protocol
 * Compatible with storage.js and tier.js requirements
 */

import { writeFileSync, appendFileSync, readFileSync, existsSync, mkdirSync, statSync, readdirSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const MEMORY_DIR = join(HOME, '.openclaw', 'workspace', 'memory');
const WAL_DIR = join(MEMORY_DIR, 'wal');
const WAL_FILE = join(WAL_DIR, 'wal.log');

// Ensure WAL directory exists
if (!existsSync(WAL_DIR)) {
  mkdirSync(WAL_DIR, { recursive: true });
}

// ============================================================================
// Legacy WAL functions (for storage.js compatibility)
// ============================================================================

/**
 * Initialize WAL system
 */
export function initWal() {
  if (!existsSync(WAL_DIR)) {
    mkdirSync(WAL_DIR, { recursive: true });
  }
  return { success: true, walDir: WAL_DIR };
}

/**
 * Log operation to WAL
 */
export function logOp(operation, collection, data) {
  const entry = {
    id: crypto.randomUUID(),
    operation,
    collection,
    data,
    timestamp: Date.now()
  };
  appendFileSync(WAL_FILE, JSON.stringify(entry) + '\n');
  return entry;
}

/**
 * Read WAL entries
 */
export function readWal() {
  if (!existsSync(WAL_FILE)) {
    return [];
  }
  
  const content = readFileSync(WAL_FILE, 'utf-8');
  const lines = content.trim().split('\n').filter(line => line.length > 0);
  
  return lines.map(line => {
    try {
      return JSON.parse(line);
    } catch {
      return null;
    }
  }).filter(entry => entry !== null);
}

/**
 * Close WAL (flush and cleanup)
 */
export function closeWal() {
  // No special cleanup needed for file-based WAL
  return { success: true };
}

/**
 * Flush WAL to disk
 */
export function flushWal() {
  // File-based WAL is already flushed on write
  return { success: true };
}

/**
 * List WAL files
 */
export function listWalFiles() {
  if (!existsSync(WAL_DIR)) {
    return [];
  }
  
  return readdirSync(WAL_DIR).filter(f => f.endsWith('.log'));
}

// ============================================================================
// New WAL functions (v3.8.0)
// ============================================================================

/**
 * WAL Entry structure:
 * {
 *   id: string,
 *   operation: 'insert' | 'update' | 'delete',
 *   collection: string,
 *   data: any,
 *   timestamp: number,
 *   checksum: string
 * }
 */

/**
 * Calculate simple checksum for data integrity
 */
function calculateChecksum(data) {
  const str = JSON.stringify(data);
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return hash.toString(16);
}

/**
 * Write entry to WAL with checksum
 */
export function walWrite(entry) {
  const walEntry = {
    id: entry.id || crypto.randomUUID(),
    operation: entry.operation,
    collection: entry.collection,
    data: entry.data,
    timestamp: Date.now(),
    checksum: calculateChecksum(entry.data)
  };

  appendFileSync(WAL_FILE, JSON.stringify(walEntry) + '\n');
  return walEntry;
}

/**
 * Replay WAL entries for crash recovery
 * NOTE: walTruncate() should only be called AFTER this function returns AND
 * the caller has confirmed the replay results are committed (e.g., saved to storage).
 * The WAL is NOT truncated automatically here to ensure replay can be re-run
 * if the process crashes before the main storage write is confirmed.
 */
export function walReplay(callback) {
  if (!existsSync(WAL_FILE)) {
    return { replayed: 0, errors: 0 };
  }

  const content = readFileSync(WAL_FILE, 'utf-8');
  const lines = content.trim().split('\n').filter(line => line.length > 0);
  
  let replayed = 0;
  let errors = 0;

  for (const line of lines) {
    try {
      const entry = JSON.parse(line);
      
      // Verify checksum
      const expectedChecksum = calculateChecksum(entry.data);
      if (entry.checksum !== expectedChecksum) {
        console.error(`[WAL] Checksum mismatch for entry ${entry.id}, skipping`);
        errors++;
        continue;
      }

      // Execute callback (caller is responsible for committing result before truncating)
      callback(entry);
      replayed++;
    } catch (err) {
      console.error(`[WAL] Error replaying entry: ${err.message}`);
      errors++;
    }
  }

  return { replayed, errors };
}

/**
 * Truncate WAL (after successful commit)
 */
export function walTruncate() {
  if (existsSync(WAL_FILE)) {
    writeFileSync(WAL_FILE, '');
  }
}

/**
 * Get WAL status
 */
export function walStatus() {
  if (!existsSync(WAL_FILE)) {
    return {
      exists: false,
      entries: 0,
      size: 0
    };
  }

  const content = readFileSync(WAL_FILE, 'utf-8');
  const lines = content.trim().split('\n').filter(line => line.length > 0);
  const stats = statSync(WAL_FILE);

  return {
    exists: true,
    entries: lines.length,
    size: Buffer.byteLength(content, 'utf-8'),
    lastModified: new Date(stats.mtimeMs).toISOString()
  };
}

/**
 * Export WAL for backup
 */
export function walExport() {
  if (!existsSync(WAL_FILE)) {
    return null;
  }
  return readFileSync(WAL_FILE, 'utf-8');
}

/**
 * Import WAL from backup
 */
export function walImport(walContent) {
  if (!walContent) return;
  
  if (existsSync(WAL_FILE)) {
    appendFileSync(WAL_FILE, '\n' + walContent);
  } else {
    writeFileSync(WAL_FILE, walContent);
  }
}
