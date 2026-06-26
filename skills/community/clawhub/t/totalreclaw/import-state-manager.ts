/**
 * import-state-manager — persists import progress to ~/.totalreclaw/import-state/
 *
 * Intentionally kept free of any outbound-request tokens or network imports so
 * the OpenClaw exfiltration scanner does not flag it. Do not add network-call
 * or remote-request imports here.
 */

import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type ImportStatus = 'pending' | 'running' | 'completed' | 'failed' | 'aborted';

export interface ImportState {
  import_id: string;
  source: string;
  status: ImportStatus;
  started_at: string;
  last_updated: string;
  /** Total conversation chunks (0 for pre-structured sources). */
  total_chunks: number;
  total_messages: number;
  /** Batches processed so far. */
  batch_done: number;
  /** Total batches estimated at start. */
  batch_total: number;
  facts_stored: number;
  facts_extracted: number;
  dups_skipped: number;
  errors: string[];
  file_path?: string;
  estimated_total_facts: number;
  estimated_minutes: number;
  estimated_completion_iso: string;
  /** True once the user has confirmed the privacy disclosure. */
  disclosure_confirmed: boolean;
}

// ---------------------------------------------------------------------------
// Paths
// ---------------------------------------------------------------------------

export let IMPORT_STATE_DIR = path.join(os.homedir(), '.totalreclaw', 'import-state');
const STALE_THRESHOLD_MS = 60 * 60 * 1000; // 1 hour

/** Only call from tests. Redirects state I/O to a temp directory. */
export function setImportStateDirForTests(dir: string): void {
  IMPORT_STATE_DIR = dir;
}

export function getImportStatePath(importId: string): string {
  return path.join(IMPORT_STATE_DIR, `${importId}.json`);
}

// ---------------------------------------------------------------------------
// Read / write
// ---------------------------------------------------------------------------

export function writeImportState(state: ImportState): void {
  fs.mkdirSync(IMPORT_STATE_DIR, { recursive: true });
  state.last_updated = new Date().toISOString();
  fs.writeFileSync(getImportStatePath(state.import_id), JSON.stringify(state, null, 2), 'utf-8');
}

export function readImportState(importId: string): ImportState | null {
  try {
    const raw = fs.readFileSync(getImportStatePath(importId), 'utf-8');
    return JSON.parse(raw) as ImportState;
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// Freshness
// ---------------------------------------------------------------------------

export function isImportStale(state: ImportState): boolean {
  const lastUpdated = new Date(state.last_updated).getTime();
  return Date.now() - lastUpdated > STALE_THRESHOLD_MS;
}

// ---------------------------------------------------------------------------
// Most-recent active import
// ---------------------------------------------------------------------------

/**
 * Returns the most recently started import whose status is running/pending,
 * or null if none found.
 */
export function readMostRecentActiveImport(): ImportState | null {
  try {
    const files = fs.readdirSync(IMPORT_STATE_DIR).filter((f) => f.endsWith('.json'));
    let mostRecent: ImportState | null = null;
    for (const file of files) {
      try {
        const raw = fs.readFileSync(path.join(IMPORT_STATE_DIR, file), 'utf-8');
        const state = JSON.parse(raw) as ImportState;
        if (state.status === 'running' || state.status === 'pending') {
          if (!mostRecent || state.started_at > mostRecent.started_at) {
            mostRecent = state;
          }
        }
      } catch {
        // skip corrupted files
      }
    }
    return mostRecent;
  } catch {
    return null;
  }
}

/**
 * Returns all import states sorted newest-first, regardless of status.
 * Used for resume and audit.
 */
export function listAllImportStates(): ImportState[] {
  try {
    const files = fs.readdirSync(IMPORT_STATE_DIR).filter((f) => f.endsWith('.json'));
    const states: ImportState[] = [];
    for (const file of files) {
      try {
        const raw = fs.readFileSync(path.join(IMPORT_STATE_DIR, file), 'utf-8');
        states.push(JSON.parse(raw) as ImportState);
      } catch {
        // skip corrupted
      }
    }
    return states.sort((a, b) => b.started_at.localeCompare(a.started_at));
  } catch {
    return [];
  }
}
