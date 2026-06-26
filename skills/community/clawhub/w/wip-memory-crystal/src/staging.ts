// memory-crystal/staging.ts — Staging pipeline for bulk imports.
// When a Node relays historical data to Core, it goes through staging
// before being processed. This separates bulk imports (need Dream Weaver)
// from live turns (already have proper context).
//
// Flow:
//   1. Poller detects bulk data (new agent ID or bulk flag)
//   2. Writes raw files to ~/.ldm/staging/{agentId}/transcripts/
//   3. Creates READY trigger file
//   4. processStagedAgent() picks it up:
//      a. Runs crystal backfill on staged transcripts
//      b. Runs crystal dream-weave --mode full
//      c. Moves processed files to ~/.ldm/agents/{agentId}/memory/transcripts/
//      d. Removes READY file
//      e. Agent flips to live capture mode

import {
  existsSync, mkdirSync, readdirSync, renameSync, unlinkSync,
  writeFileSync, readFileSync,
} from 'node:fs';
import { join } from 'node:path';
import { ldmPaths, ensureLdm } from './ldm.js';
import { execSync } from 'node:child_process';

const HOME = process.env.HOME || '';
const STAGING_ROOT = join(HOME, '.ldm', 'staging');

// ── Staging directory management ──

export interface StagingPaths {
  root: string;           // ~/.ldm/staging/{agentId}/
  transcripts: string;    // ~/.ldm/staging/{agentId}/transcripts/
  readyFile: string;      // ~/.ldm/staging/{agentId}/READY
}

export function stagingPaths(agentId: string): StagingPaths {
  const root = join(STAGING_ROOT, agentId);
  return {
    root,
    transcripts: join(root, 'transcripts'),
    readyFile: join(root, 'READY'),
  };
}

/** Ensure staging directories exist for an agent. */
export function ensureStaging(agentId: string): StagingPaths {
  const paths = stagingPaths(agentId);
  mkdirSync(paths.transcripts, { recursive: true });
  return paths;
}

/** Mark an agent's staging as ready for processing. */
export function markReady(agentId: string): void {
  const paths = stagingPaths(agentId);
  writeFileSync(paths.readyFile, JSON.stringify({
    markedAt: new Date().toISOString(),
    agentId,
  }));
}

// ── Detection ──

/** Check if an agent ID is new (no existing LDM agent directory). */
export function isNewAgent(agentId: string): boolean {
  const paths = ldmPaths(agentId);
  return !existsSync(paths.agentRoot);
}

/** Check if an agent has staged data ready for processing. */
export function hasStagedData(agentId: string): boolean {
  const paths = stagingPaths(agentId);
  return existsSync(paths.readyFile);
}

/** List all agents with staged data ready for processing. */
export function listStagedAgents(): string[] {
  if (!existsSync(STAGING_ROOT)) return [];

  const agents: string[] = [];
  for (const entry of readdirSync(STAGING_ROOT, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    if (existsSync(join(STAGING_ROOT, entry.name, 'READY'))) {
      agents.push(entry.name);
    }
  }
  return agents;
}

// ── Processing ──

export interface StagingResult {
  agentId: string;
  transcriptsProcessed: number;
  backfillChunks: number;
  dreamWeaverRan: boolean;
  durationMs: number;
}

/** Process a staged agent: backfill + dream-weave + move to live. */
export async function processStagedAgent(agentId: string): Promise<StagingResult> {
  const startTime = Date.now();
  const staging = stagingPaths(agentId);

  if (!existsSync(staging.readyFile)) {
    throw new Error(`No READY file for agent ${agentId}`);
  }

  // Ensure the agent's LDM directory exists
  const agentPaths = ensureLdm(agentId);

  // Count staged transcripts
  const stagedFiles = existsSync(staging.transcripts)
    ? readdirSync(staging.transcripts).filter(f => f.endsWith('.jsonl'))
    : [];

  if (stagedFiles.length === 0) {
    // No files to process, clean up
    unlinkSync(staging.readyFile);
    return {
      agentId,
      transcriptsProcessed: 0,
      backfillChunks: 0,
      dreamWeaverRan: false,
      durationMs: Date.now() - startTime,
    };
  }

  // Move staged transcripts to agent's LDM transcripts dir first
  for (const file of stagedFiles) {
    const src = join(staging.transcripts, file);
    const dest = join(agentPaths.transcripts, file);
    // Use rename if same filesystem, otherwise would need copy+delete
    try {
      renameSync(src, dest);
    } catch {
      // Cross-filesystem: fall back to copy
      const { copyFileSync } = await import('node:fs');
      copyFileSync(src, dest);
      unlinkSync(src);
    }
  }

  let backfillChunks = 0;
  let dreamWeaverRan = false;

  // Run backfill (embed all transcripts)
  try {
    const output = execSync(
      `crystal backfill --agent ${agentId}`,
      { encoding: 'utf-8', timeout: 600_000 }
    );
    // Parse chunks from output
    const match = output.match(/(\d+) chunks embedded/);
    if (match) backfillChunks = parseInt(match[1], 10);
  } catch (err: any) {
    process.stderr.write(`[staging] backfill failed for ${agentId}: ${err.message}\n`);
  }

  // Run Dream Weaver (full mode for first-time import)
  try {
    execSync(
      `crystal dream-weave --agent ${agentId} --mode full`,
      { encoding: 'utf-8', timeout: 600_000 }
    );
    dreamWeaverRan = true;
  } catch (err: any) {
    process.stderr.write(`[staging] dream-weave failed for ${agentId}: ${err.message}\n`);
  }

  // Remove READY file (agent is now in live capture mode)
  try {
    unlinkSync(staging.readyFile);
  } catch {}

  return {
    agentId,
    transcriptsProcessed: stagedFiles.length,
    backfillChunks,
    dreamWeaverRan,
    durationMs: Date.now() - startTime,
  };
}

/** Process all staged agents. */
export async function processAllStaged(): Promise<StagingResult[]> {
  const agents = listStagedAgents();
  const results: StagingResult[] = [];

  for (const agentId of agents) {
    try {
      const result = await processStagedAgent(agentId);
      results.push(result);
    } catch (err: any) {
      process.stderr.write(`[staging] failed to process ${agentId}: ${err.message}\n`);
    }
  }

  return results;
}
