#!/usr/bin/env node
// memory-crystal/mirror-sync.ts — Node-side delta sync.
// Pulls encrypted delta chunks from relay Worker, decrypts, and imports
// pre-embedded chunks into local crystal.db. No re-embedding needed.
//
// Replaces the old full-DB mirror approach. Core pushes only new chunks
// since last sync (delta). Node inserts them with their pre-computed vectors.
//
// Usage:
//   node mirror-sync.js              Pull latest delta (if available)
//   node mirror-sync.js --status     Show mirror state
//   node mirror-sync.js --force      Pull even if current mirror is recent

import { Crystal, resolveConfig, type ExportedChunk } from './core.js';
import { loadRelayKey, decryptJSON, type EncryptedPayload } from './crypto.js';
import { ldmPaths, resolveStatePath, stateWritePath } from './ldm.js';
import { pullFileSync } from './file-sync.js';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const RELAY_URL = process.env.CRYSTAL_RELAY_URL || '';
const RELAY_TOKEN = process.env.CRYSTAL_RELAY_TOKEN || '';
const _ldmPaths = ldmPaths();
const MIRROR_STATE_PATH = resolveStatePath('mirror-sync-state.json');

interface DeltaPayload {
  version: number;
  sinceId: number;
  maxId: number;
  chunkCount: number;
  pushedAt: string;
  chunks: ExportedChunk[];
}

interface MirrorState {
  lastSync: string | null;
  lastHash: string | null;
  lastSize: number | null;
  /** Watermark: highest chunk ID received from Core */
  lastDeltaChunkId: number;
  /** Total chunks imported via delta sync */
  totalImported: number;
}

function loadState(): MirrorState {
  try {
    if (existsSync(MIRROR_STATE_PATH)) {
      const state = JSON.parse(readFileSync(MIRROR_STATE_PATH, 'utf-8'));
      // Migration: add new fields if missing
      return {
        lastSync: state.lastSync || null,
        lastHash: state.lastHash || null,
        lastSize: state.lastSize || null,
        lastDeltaChunkId: state.lastDeltaChunkId || 0,
        totalImported: state.totalImported || 0,
      };
    }
  } catch {}
  return { lastSync: null, lastHash: null, lastSize: null, lastDeltaChunkId: 0, totalImported: 0 };
}

function saveState(state: MirrorState): void {
  const writePath = stateWritePath('mirror-sync-state.json');
  writeFileSync(writePath, JSON.stringify(state, null, 2));
}

// ── Pull delta ──

async function pullDelta(force: boolean): Promise<boolean> {
  if (!RELAY_URL || !RELAY_TOKEN) {
    throw new Error('CRYSTAL_RELAY_URL and CRYSTAL_RELAY_TOKEN must be set');
  }

  const relayKey = loadRelayKey();

  // List available mirror blobs
  const listResp = await fetch(`${RELAY_URL}/pickup/mirror`, {
    headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
  });

  if (!listResp.ok) {
    throw new Error(`Relay list failed: ${listResp.status} ${await listResp.text()}`);
  }

  const listData = await listResp.json() as { count: number; blobs: Array<{ id: string; size: number; dropped_at: string }> };

  if (listData.count === 0) {
    process.stderr.write('[mirror-sync] no delta available\n');
    return false;
  }

  // Initialize crystal for import
  const config = resolveConfig();
  const crystal = new Crystal(config);
  await crystal.init();

  const state = loadState();
  let totalImported = 0;

  // Process all available delta blobs (oldest first)
  for (const blob of listData.blobs) {
    try {
      const blobResp = await fetch(`${RELAY_URL}/pickup/mirror/${blob.id}`, {
        headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
      });

      if (!blobResp.ok) {
        process.stderr.write(`[mirror-sync] failed to fetch blob ${blob.id}: ${blobResp.status}\n`);
        continue;
      }

      const encryptedText = await blobResp.text();
      const encrypted = JSON.parse(encryptedText) as EncryptedPayload;

      // Decrypt delta payload
      let delta: DeltaPayload;
      try {
        delta = decryptJSON<DeltaPayload>(encrypted, relayKey);
      } catch (err: any) {
        process.stderr.write(`[mirror-sync] blob ${blob.id} failed verification: ${err.message} — DISCARDED\n`);
        // Delete bad blob
        await fetch(`${RELAY_URL}/confirm/mirror/${blob.id}`, {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
        });
        continue;
      }

      // Skip if we already have these chunks (unless forced)
      if (!force && delta.maxId <= state.lastDeltaChunkId) {
        process.stderr.write(`[mirror-sync] blob ${blob.id} already applied (maxId ${delta.maxId} <= watermark ${state.lastDeltaChunkId})\n`);
        // Confirm receipt to clean up relay
        await fetch(`${RELAY_URL}/confirm/mirror/${blob.id}`, {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
        });
        continue;
      }

      // Import pre-embedded chunks (dedup by hash happens inside importChunks)
      const imported = crystal.importChunks(delta.chunks);
      totalImported += imported;

      // Update watermark
      if (delta.maxId > state.lastDeltaChunkId) {
        state.lastDeltaChunkId = delta.maxId;
      }

      process.stderr.write(
        `[mirror-sync] blob ${blob.id}: ${imported}/${delta.chunkCount} chunks imported ` +
        `(ID ${delta.sinceId + 1}..${delta.maxId}), pushed=${delta.pushedAt}\n`
      );

      // Confirm receipt
      await fetch(`${RELAY_URL}/confirm/mirror/${blob.id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${RELAY_TOKEN}` },
      });
    } catch (err: any) {
      process.stderr.write(`[mirror-sync] error processing blob ${blob.id}: ${err.message}\n`);
    }
  }

  // Update state
  state.lastSync = new Date().toISOString();
  state.totalImported += totalImported;
  saveState(state);

  if (totalImported > 0) {
    process.stderr.write(`[mirror-sync] done: ${totalImported} chunks imported, watermark=${state.lastDeltaChunkId}\n`);
  }

  return totalImported > 0;
}

// ── CLI ──

const args = process.argv.slice(2);

if (args.includes('--status')) {
  const state = loadState();
  const paths = ldmPaths();
  const hasDb = existsSync(paths.crystalDb);
  console.log('Mirror sync status:');
  console.log(`  Relay URL:       ${RELAY_URL || '(not set)'}`);
  console.log(`  Local crystal:   ${hasDb ? paths.crystalDb : '(none)'}`);
  console.log(`  Last sync:       ${state.lastSync || 'never'}`);
  console.log(`  Delta watermark: chunk ID ${state.lastDeltaChunkId}`);
  console.log(`  Total imported:  ${state.totalImported}`);
  process.exit(0);
}

const force = args.includes('--force');

pullDelta(force)
  .then(async (updated) => {
    // Also pull file tree sync
    try {
      const { imported, deleted } = await pullFileSync();
      if (imported > 0 || deleted > 0) {
        process.stderr.write(`[mirror-sync] file sync: ${imported} imported, ${deleted} deleted\n`);
      }
    } catch (err: any) {
      process.stderr.write(`[mirror-sync] file sync failed (non-fatal): ${err.message}\n`);
    }

    if (updated) {
      process.stderr.write('[mirror-sync] done\n');
    }
    process.exit(0);
  })
  .catch(err => {
    process.stderr.write(`[mirror-sync] error: ${err.message}\n`);
    process.exit(1);
  });
