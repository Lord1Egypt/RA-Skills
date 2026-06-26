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
// Paths
// ---------------------------------------------------------------------------
export let IMPORT_STATE_DIR = path.join(os.homedir(), '.totalreclaw', 'import-state');
const STALE_THRESHOLD_MS = 60 * 60 * 1000; // 1 hour
/** Only call from tests. Redirects state I/O to a temp directory. */
export function setImportStateDirForTests(dir) {
    IMPORT_STATE_DIR = dir;
}
export function getImportStatePath(importId) {
    return path.join(IMPORT_STATE_DIR, `${importId}.json`);
}
// ---------------------------------------------------------------------------
// Read / write
// ---------------------------------------------------------------------------
export function writeImportState(state) {
    fs.mkdirSync(IMPORT_STATE_DIR, { recursive: true });
    state.last_updated = new Date().toISOString();
    fs.writeFileSync(getImportStatePath(state.import_id), JSON.stringify(state, null, 2), 'utf-8');
}
export function readImportState(importId) {
    try {
        const raw = fs.readFileSync(getImportStatePath(importId), 'utf-8');
        return JSON.parse(raw);
    }
    catch {
        return null;
    }
}
// ---------------------------------------------------------------------------
// Freshness
// ---------------------------------------------------------------------------
export function isImportStale(state) {
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
export function readMostRecentActiveImport() {
    try {
        const files = fs.readdirSync(IMPORT_STATE_DIR).filter((f) => f.endsWith('.json'));
        let mostRecent = null;
        for (const file of files) {
            try {
                const raw = fs.readFileSync(path.join(IMPORT_STATE_DIR, file), 'utf-8');
                const state = JSON.parse(raw);
                if (state.status === 'running' || state.status === 'pending') {
                    if (!mostRecent || state.started_at > mostRecent.started_at) {
                        mostRecent = state;
                    }
                }
            }
            catch {
                // skip corrupted files
            }
        }
        return mostRecent;
    }
    catch {
        return null;
    }
}
/**
 * Returns all import states sorted newest-first, regardless of status.
 * Used for resume and audit.
 */
export function listAllImportStates() {
    try {
        const files = fs.readdirSync(IMPORT_STATE_DIR).filter((f) => f.endsWith('.json'));
        const states = [];
        for (const file of files) {
            try {
                const raw = fs.readFileSync(path.join(IMPORT_STATE_DIR, file), 'utf-8');
                states.push(JSON.parse(raw));
            }
            catch {
                // skip corrupted
            }
        }
        return states.sort((a, b) => b.started_at.localeCompare(a.started_at));
    }
    catch {
        return [];
    }
}
