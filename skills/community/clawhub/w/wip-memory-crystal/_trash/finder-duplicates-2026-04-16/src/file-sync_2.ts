// memory-crystal/file-sync.ts — Full LDM tree sync between Core and Nodes.
// Manifest-based delta file transfer. Core builds manifest (path + SHA-256 + size),
// pushes only changed files. Node compares, downloads, and applies changes.
//
// This complements delta chunk sync: chunks are the embeddings, files are the artifacts.
// Embeddings are pointers to files. If the file isn't on the node, the search result is an orphan.

import { loadRelayKey, encryptJSON, decryptJSON, encrypt, decrypt, type EncryptedPayload } from './crypto.js';
import { ldmPaths, resolveStatePath, stateWritePath } from './ldm.js';
import { createHash } from 'node:crypto';
import {
  existsSync, mkdirSync, readFileSync, writeFileSync, unlinkSync,
  readdirSync, statSync,
} from 'node:fs';
import { join, relative, dirname } from 'node:path';

const RELAY_URL = process.env.CRYSTAL_RELAY_URL || '';
const RELAY_TOKEN = process.env.CRYSTAL_RELAY_TOKEN || '';

// ── Types ──

export interface FileManifestEntry {
  /** Relative path from ~/.ldm/ (e.g. "agents/cc-mini/memory/daily/2026-03-05.md") */
  path: string;
  /** SHA-256 hex hash of file contents */
  sha256: string;
  /** File size in bytes */
  size: number;
}

export interface FileManifest {
  version: number;
  generatedAt: string;
  /** Total number of files */
  fileCount: number;
  entries: FileManifestEntry[];
}

export interface FileDelta {
  /** Files to create or update on the node */
  upsert: Array<{ path: string; sha256: string }>;
  /** Files to delete on the node */
  delete: string[];
}

export interface FileSyncState {
  lastSync: string | null;
  lastManifestHash: string | null;
  filesTransferred: number;
  filesDeleted: number;
}

// ── Exclusion rules ──

/** Paths to exclude from sync (relative to ~/.ldm/) */
const EXCLUDE_PATTERNS = [
  'memory/crystal.db',        // DB syncs via delta chunks, not file copy
  'memory/crystal.db-wal',
  'memory/crystal.db-shm',
  'memory/crystal.db.bak',
  'memory/crystal.db.tmp',
  'memory/lance/',            // LanceDB (deprecated, not synced)
  'state/',                   // Local state files (watermarks, etc.)
  'secrets/',                 // Encryption keys, tokens
  'staging/',                 // Staging pipeline (Core-only)
  'bin/',                     // Local scripts
  '.DS_Store',
];

function shouldExclude(relativePath: string): boolean {
  for (const pattern of EXCLUDE_PATTERNS) {
    if (relativePath === pattern || relativePath.startsWith(pattern)) return true;
  }
  // Skip hidden files/dirs (except agent dirs which start with letters)
  const parts = relativePath.split('/');
  for (const part of parts) {
    if (part.startsWith('.') && part !== '.ldm') return true;
  }
  return false;
}

// ── Manifest generation ──

/** Recursively scan a directory and build a file manifest. */
function scanDir(baseDir: string, currentDir: string, entries: FileManifestEntry[]): void {
  if (!existsSync(currentDir)) return;

  const items = readdirSync(currentDir);
  for (const item of items) {
    const fullPath = join(currentDir, item);
    const relPath = relative(baseDir, fullPath);

    if (shouldExclude(relPath)) continue;

    let stat;
    try {
      stat = statSync(fullPath);
    } catch {
      continue; // Skip broken symlinks, etc.
    }

    if (stat.isDirectory()) {
      scanDir(baseDir, fullPath, entries);
    } else if (stat.isFile()) {
      // Skip very large files (>50MB) for now
      if (stat.size > 50 * 1024 * 1024) continue;

      const content = readFileSync(fullPath);
      const sha256 = createHash('sha256').update(content).digest('hex');
      entries.push({ path: relPath, sha256, size: stat.size });
    }
  }
}

/** Generate a manifest of all files under ~/.ldm/. */
export function generateManifest(): FileManifest {
  const paths = ldmPaths();
  const entries: FileManifestEntry[] = [];
  scanDir(paths.root, paths.root, entries);

  return {
    version: 1,
    generatedAt: new Date().toISOString(),
    fileCount: entries.length,
    entries,
  };
}

/** Compare Core manifest against local files. Returns what needs to change. */
export function compareManifest(coreManifest: FileManifest): FileDelta {
  const paths = ldmPaths();
  const upsert: Array<{ path: string; sha256: string }> = [];
  const toDelete: string[] = [];

  // Build local manifest for comparison
  const localManifest = generateManifest();
  const localMap = new Map(localManifest.entries.map(e => [e.path, e]));
  const coreMap = new Map(coreManifest.entries.map(e => [e.path, e]));

  // Files in Core but not local (or different hash) = upsert
  for (const entry of coreManifest.entries) {
    const local = localMap.get(entry.path);
    if (!local || local.sha256 !== entry.sha256) {
      upsert.push({ path: entry.path, sha256: entry.sha256 });
    }
  }

  // Files in local but not Core = delete
  for (const entry of localManifest.entries) {
    if (!coreMap.has(entry.path)) {
      toDelete.push(entry.path);
    }
  }

  return { upsert, delete: toDelete };
}

// ── Core-side: push manifest and changed files ──

export function loadFileSyncState(): FileSyncState {
  const statePath = resolveStatePath('file-sync-state.json');
  try {
    if (existsSync(statePath)) {
      return JSON.parse(readFileSync(statePath, 'utf-8'));
    }
  } catch {}
  return { lastSync: null, lastManifestHash: null, filesTransferred: 0, filesDeleted: 0 };
}

export function saveFileSyncState(state: FileSyncState): void {
  const writePath = stateWritePath('file-sync-state.json');
  writeFileSync(writePath, JSON.stringify(state, null, 2));
}

/** Core pushes manifest + changed files to relay "files" channel. */
export async function pushFileSync(): Promise<{ manifest: number; files: number }> {
  if (!RELAY_URL || !RELAY_TOKEN) {
    throw new Error('CRYSTAL_RELAY_URL and CRYSTAL_RELAY_TOKEN must be set');
  }

  const relayKey = loadRelayKey();
  const paths = ldmPaths();
  const manifest = generateManifest();

  // Check if manifest changed since last push
  const manifestJson = JSON.stringify(manifest.entries.map(e => `${e.path}:${e.sha256}`));
  const manifestHash = createHash('sha256').update(manifestJson).digest('hex');
  const state = loadFileSyncState();

  if (state.lastManifestHash === manifestHash) {
    return { manifest: 0, files: 0 };
  }

  // Push manifest
  const encryptedManifest = encryptJSON(manifest, relayKey);
  const manifestResp = await fetch(`${RELAY_URL}/drop/files`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${RELAY_TOKEN}`,
      'Content-Type': 'application/octet-stream',
      'X-File-Type': 'manifest',
    },
    body: JSON.stringify(encryptedManifest),
  });

  if (!manifestResp.ok) {
    throw new Error(`Manifest push failed: ${manifestResp.status} ${await manifestResp.text()}`);
  }

  // Push each file that might have changed
  // (In practice, the Node compares and requests only what it needs.
  //  For now, we push all files. Optimization: Node requests specific files.)
  let filesPushed = 0;
  for (const entry of manifest.entries) {
    const fullPath = join(paths.root, entry.path);
    if (!existsSync(fullPath)) continue;

    const content = readFileSync(fullPath);
    const encrypted = encrypt(content, relayKey);

    const filePayload = JSON.stringify({
      path: entry.path,
      sha256: entry.sha256,
      size: entry.size,
      data: encrypted,
    });

    const fileResp = await fetch(`${RELAY_URL}/drop/files`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${RELAY_TOKEN}`,
        'Content-Type': 'application/octet-stream',
        'X-File-Type': 'file',
      },
      body: filePayload,
    });

    if (fileResp.ok) filesPushed++;
  }

  // Update state
  state.lastSync = new Date().toISOString();
  state.lastManifestHash = manifestHash;
  state.filesTransferred += filesPushed;
  saveFileSyncState(state);

  return { manifest: manifest.fileCount, files: filesPushed };
}

// ── Node-side: pull manifest and apply file changes ──

/** Node pulls files from relay and applies changes. */
export async function pullFileSync(): Promise<{ imported: number; deleted: number }> {
  if (!RELAY_URL || !RELAY_TOKEN) {
    throw new Error('CRYSTAL_RELAY_URL and CRYSTAL_RELAY_TOKEN must be set');
  }

  const relayKey = loadRelayKey();
  const paths = ldmPaths();

  // List available file blobs
  const listResp = await fetch(`${RELAY_URL}/pickup/files`, {
    headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
  });

  if (!listResp.ok) {
    throw new Error(`File sync list failed: ${listResp.status} ${await listResp.text()}`);
  }

  const listData = await listResp.json() as { count: number; blobs: Array<{ id: string; size: number; dropped_at: string }> };

  if (listData.count === 0) {
    return { imported: 0, deleted: 0 };
  }

  // Separate manifest blobs from file blobs
  // We process all blobs: first find the manifest, then apply files
  let coreManifest: FileManifest | null = null;
  const fileBlobs: Array<{ id: string; path: string; sha256: string; data: EncryptedPayload }> = [];

  for (const blob of listData.blobs) {
    try {
      const blobResp = await fetch(`${RELAY_URL}/pickup/files/${blob.id}`, {
        headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
      });

      if (!blobResp.ok) continue;

      const text = await blobResp.text();
      const parsed = JSON.parse(text);

      // Detect if this is a manifest or a file
      if (parsed.v !== undefined && parsed.nonce !== undefined) {
        // This is an encrypted manifest
        try {
          const manifest = decryptJSON<FileManifest>(parsed as EncryptedPayload, relayKey);
          if (manifest.version && manifest.entries) {
            coreManifest = manifest;
          }
        } catch {}
      } else if (parsed.path && parsed.data) {
        // This is a file payload
        fileBlobs.push({
          id: blob.id,
          path: parsed.path,
          sha256: parsed.sha256,
          data: parsed.data as EncryptedPayload,
        });
      }

      // Confirm receipt
      await fetch(`${RELAY_URL}/confirm/files/${blob.id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
      });
    } catch (err: any) {
      process.stderr.write(`[file-sync] error processing blob ${blob.id}: ${err.message}\n`);
    }
  }

  if (!coreManifest) {
    process.stderr.write('[file-sync] no manifest found in relay\n');
    return { imported: 0, deleted: 0 };
  }

  // Compare manifest to determine what we need
  const delta = compareManifest(coreManifest);

  // Build a lookup of available file blobs by path
  const fileBlobMap = new Map(fileBlobs.map(f => [f.path, f]));

  // Apply upserts
  let imported = 0;
  for (const entry of delta.upsert) {
    const fileBlob = fileBlobMap.get(entry.path);
    if (!fileBlob) {
      // File not in this batch (may arrive in next sync)
      continue;
    }

    try {
      const content = decrypt(fileBlob.data, relayKey);

      // Verify integrity
      const actualHash = createHash('sha256').update(content).digest('hex');
      if (actualHash !== entry.sha256) {
        process.stderr.write(`[file-sync] hash mismatch for ${entry.path}, skipping\n`);
        continue;
      }

      // Write file
      const destPath = join(paths.root, entry.path);
      mkdirSync(dirname(destPath), { recursive: true });
      writeFileSync(destPath, content);
      imported++;
    } catch (err: any) {
      process.stderr.write(`[file-sync] failed to write ${entry.path}: ${err.message}\n`);
    }
  }

  // Apply deletes
  let deleted = 0;
  for (const path of delta.delete) {
    const destPath = join(paths.root, path);
    if (existsSync(destPath)) {
      try {
        unlinkSync(destPath);
        deleted++;
      } catch (err: any) {
        process.stderr.write(`[file-sync] failed to delete ${path}: ${err.message}\n`);
      }
    }
  }

  // Update state
  const state = loadFileSyncState();
  state.lastSync = new Date().toISOString();
  state.filesTransferred += imported;
  state.filesDeleted += deleted;
  saveFileSyncState(state);

  return { imported, deleted };
}
