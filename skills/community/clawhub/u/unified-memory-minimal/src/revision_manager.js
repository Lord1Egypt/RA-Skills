/**
 * Revision Manager - Memory Version Conflict Detection & Resolution
 * Tracks memory changes over time, detects conflicts, and resolves them.
 * 
 * Storage: ~/.openclaw/workspace/memory/revisions.json
 */

import fs from 'fs/promises';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';
import { z } from 'zod';
import { config } from './config.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Storage path
const REVISIONS_FILE = path.join(config.memoryDir, 'revisions.json');

// ============ Types ============

/**
 * @typedef {Object} MemoryRevision
 * @property {string} memory_id
 * @property {number} version
 * @property {string} content
 * @property {string} previous_content
 * @property {'created'|'updated'|'deleted'} change_type
 * @property {string} changed_at
 * @property {string} changed_by
 * @property {string} [commit_hash]
 */

/**
 * @typedef {Object} ConflictReport
 * @property {boolean} has_conflict
 * @property {string} memory_id
 * @property {MemoryRevision} local_version
 * @property {MemoryRevision} remote_version
 * @property {'local'|'remote'|'merged'|'manual'} [resolution]
 * @property {string} [merged_content]
 */

/**
 * @typedef {'last-write-wins'|'local-wins'|'remote-wins'|'manual'} UpdatePolicy
 */

// ============ Storage Helpers ============

async function loadRevisions() {
  try {
    const data = await fs.readFile(REVISIONS_FILE, 'utf-8');
    return JSON.parse(data);
  } catch {
    // Auto-create if not exists
    await saveRevisions({ revisions: [], conflicts: [], pending_merges: [] });
    return { revisions: [], conflicts: [], pending_merges: [] };
  }
}

async function saveRevisions(data) {
  await fs.mkdir(path.dirname(REVISIONS_FILE), { recursive: true });
  await fs.writeFile(REVISIONS_FILE, JSON.stringify(data, null, 2), 'utf-8');
}

function generateId() {
  return crypto.randomBytes(8).toString('hex');
}

// ============ Core Functions ============

/**
 * Record a new revision for a memory change.
 * Every memory change creates a new revision entry.
 */
export async function recordRevision(memoryId, newContent, changeType, changedBy = 'unknown', commitHash = null) {
  const store = await loadRevisions();
  
  // Get existing revisions for this memory
  const existing = store.revisions.filter(r => r.memory_id === memoryId);
  const latestVersion = existing.length > 0 ? Math.max(...existing.map(r => r.version)) : 0;
  const previousContent = existing.length > 0 
    ? (existing.find(r => r.version === latestVersion)?.content || '')
    : '';
  
  const revision = {
    memory_id: memoryId,
    version: latestVersion + 1,
    content: newContent,
    previous_content: previousContent,
    change_type: changeType,
    changed_at: new Date().toISOString(),
    changed_by: changedBy,
    commit_hash: commitHash || null,
    revision_id: generateId(),
  };
  
  store.revisions.push(revision);
  await saveRevisions(store);
  
  return revision;
}

/**
 * Get revision history for a specific memory.
 * Returns revisions sorted by version descending (newest first).
 */
export async function getRevisions(memoryId, limit = 50) {
  const store = await loadRevisions();
  const revisions = store.revisions
    .filter(r => r.memory_id === memoryId)
    .sort((a, b) => b.version - a.version)
    .slice(0, limit);
  
  return revisions;
}

/**
 * Detect conflicts between local and remote versions.
 * Compares content and version numbers to identify divergent changes.
 */
export async function detectConflict(memoryId, localContent, remoteVersion) {
  const store = await loadRevisions();
  const existing = store.revisions
    .filter(r => r.memory_id === memoryId)
    .sort((a, b) => b.version - a.version);
  
  const localLatest = existing[0];
  
  // No local history = no conflict possible
  if (!localLatest) {
    return {
      has_conflict: false,
      memory_id: memoryId,
      local_version: null,
      remote_version: remoteVersion,
      resolution: 'remote',
    };
  }
  
  // Check if local and remote have diverged
  const hasConflict = localLatest.content !== remoteVersion.content && 
                     localLatest.version !== remoteVersion.version;
  
  if (hasConflict) {
    const conflict = {
      memory_id: memoryId,
      has_conflict: true,
      local_version: localLatest,
      remote_version: remoteVersion,
      detected_at: new Date().toISOString(),
    };
    
    // Store pending conflict
    const existingConflict = store.conflicts.findIndex(c => c.memory_id === memoryId && !c.resolution);
    if (existingConflict >= 0) {
      store.conflicts[existingConflict] = conflict;
    } else {
      store.conflicts.push(conflict);
    }
    await saveRevisions(store);
    
    return conflict;
  }
  
  return {
    has_conflict: false,
    memory_id: memoryId,
    local_version: localLatest,
    remote_version: remoteVersion,
  };
}

/**
 * Resolve a detected conflict with a chosen strategy.
 */
export async function resolveConflict(memoryId, resolution, mergedContent = null) {
  const store = await loadRevisions();
  const conflictIdx = store.conflicts.findIndex(c => c.memory_id === memoryId);
  
  if (conflictIdx < 0) {
    throw new Error(`No pending conflict found for memory ${memoryId}`);
  }
  
  const conflict = store.conflicts[conflictIdx];
  
  // Determine final content based on resolution
  let finalContent;
  switch (resolution) {
    case 'local':
      finalContent = conflict.local_version.content;
      break;
    case 'remote':
      finalContent = conflict.remote_version.content;
      break;
    case 'merged':
      if (!mergedContent) throw new Error('Merged content required for merged resolution');
      finalContent = mergedContent;
      break;
    case 'manual':
      // Mark for manual resolution (keep conflict pending)
      conflict.resolution = 'manual';
      store.conflicts[conflictIdx] = conflict;
      await saveRevisions(store);
      return;
    default:
      throw new Error(`Unknown resolution: ${resolution}`);
  }
  
  // Record resolution
  conflict.resolution = resolution;
  conflict.merged_content = finalContent;
  conflict.resolved_at = new Date().toISOString();
  store.conflicts[conflictIdx] = conflict;
  
  // Create a new revision with resolved content
  await recordRevision(
    memoryId,
    finalContent,
    'updated',
    'conflict-resolver',
    null
  );
  
  await saveRevisions(store);
}

/**
 * Generate a diff between two versions of a memory.
 * Returns a simple unified diff format.
 */
export async function diffRevisions(memoryId, v1, v2) {
  const store = await loadRevisions();
  const rev1 = store.revisions.find(r => r.memory_id === memoryId && r.version === v1);
  const rev2 = store.revisions.find(r => r.memory_id === memoryId && r.version === v2);
  
  if (!rev1 || !rev2) {
    throw new Error(`Revision not found: v1=${v1}, v2=${v2}`);
  }
  
  const oldLines = rev1.content.split('\n');
  const newLines = rev2.content.split('\n');
  
  // Simple line-by-line diff
  const diff = [];
  diff.push(`--- Version ${v1} (${rev1.changed_at})`);
  diff.push(`+++ Version ${v2} (${rev2.changed_at})`);
  
  const maxLines = Math.max(oldLines.length, newLines.length);
  for (let i = 0; i < maxLines; i++) {
    const oldLine = oldLines[i] ?? '';
    const newLine = newLines[i] ?? '';
    
    if (oldLine === newLine) {
      diff.push(`  ${oldLine}`);
    } else {
      if (oldLines[i] !== undefined) diff.push(`- ${oldLine}`);
      if (newLines[i] !== undefined) diff.push(`+ ${newLine}`);
    }
  }
  
  return diff.join('\n');
}

/**
 * Auto-merge two sets of revisions.
 * Uses update policy to resolve conflicts automatically when possible.
 */
export async function autoMerge(localRevisions, remoteRevisions, policy = 'last-write-wins') {
  if (!localRevisions || localRevisions.length === 0) {
    return {
      success: true,
      merged: remoteRevisions,
      conflicts: [],
      policy,
    };
  }
  
  if (!remoteRevisions || remoteRevisions.length === 0) {
    return {
      success: true,
      merged: localRevisions,
      conflicts: [],
      policy,
    };
  }
  
  const merged = [];
  const conflicts = [];
  
  // Group by memory_id
  const localByMemory = {};
  const remoteByMemory = {};
  
  for (const rev of localRevisions) {
    if (!localByMemory[rev.memory_id]) localByMemory[rev.memory_id] = [];
    localByMemory[rev.memory_id].push(rev);
  }
  
  for (const rev of remoteRevisions) {
    if (!remoteByMemory[rev.memory_id]) remoteByMemory[rev.memory_id] = [];
    remoteByMemory[rev.memory_id].push(rev);
  }
  
  // Get all memory IDs
  const allMemoryIds = new Set([...Object.keys(localByMemory), ...Object.keys(remoteByMemory)]);
  
  for (const memoryId of allMemoryIds) {
    const local = localByMemory[memoryId] || [];
    const remote = remoteByMemory[memoryId] || [];
    
    const localLatest = local.sort((a, b) => b.version - a.version)[0];
    const remoteLatest = remote.sort((a, b) => b.version - a.version)[0];
    
    if (!localLatest) {
      // Only remote exists
      merged.push(...remote);
    } else if (!remoteLatest) {
      // Only local exists
      merged.push(...local);
    } else {
      // Both exist - check for conflict
      const hasConflict = localLatest.content !== remoteLatest.content;
      
      if (!hasConflict) {
        // No conflict - take the latest
        merged.push(localLatest.version >= remoteLatest.version ? localLatest : remoteLatest);
      } else {
        // Conflict detected - apply policy
        let winner;
        
        switch (policy) {
          case 'last-write-wins':
            winner = new Date(localLatest.changed_at) > new Date(remoteLatest.changed_at) 
              ? localLatest 
              : remoteLatest;
            break;
          case 'local-wins':
            winner = localLatest;
            break;
          case 'remote-wins':
            winner = remoteLatest;
            break;
          case 'manual':
            // Mark for manual resolution
            conflicts.push({
              memory_id: memoryId,
              local_version: localLatest,
              remote_version: remoteLatest,
              resolution: 'manual',
            });
            // Store conflict
            const store = await loadRevisions();
            store.conflicts.push({
              memory_id: memoryId,
              has_conflict: true,
              local_version: localLatest,
              remote_version: remoteLatest,
              detected_at: new Date().toISOString(),
              resolution: 'manual',
            });
            await saveRevisions(store);
            continue;
          default:
            throw new Error(`Unknown policy: ${policy}`);
        }
        
        merged.push(winner);
      }
    }
  }
  
  return {
    success: conflicts.length === 0,
    merged,
    conflicts,
    policy,
  };
}

/**
 * Get all pending conflicts.
 */
export async function getPendingConflicts() {
  const store = await loadRevisions();
  return store.conflicts.filter(c => !c.resolution || c.resolution === 'manual');
}

/**
 * Get a specific revision by memory ID and version.
 */
export async function getRevision(memoryId, version) {
  const store = await loadRevisions();
  return store.revisions.find(r => r.memory_id === memoryId && r.version === version) || null;
}

// ============ MCP Tool Handlers ============

export const memoryRevisionHandlers = {
  /**
   * record - Record a new memory revision
   */
  record: async ({ memory_id, content, change_type, changed_by, commit_hash }) => {
    try {
      const revision = await recordRevision(memory_id, content, change_type, changed_by, commit_hash);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            success: true,
            revision,
          }, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  },

  /**
   * history - Get revision history for a memory
   */
  history: async ({ memory_id, limit }) => {
    try {
      const revisions = await getRevisions(memory_id, limit);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            memory_id,
            count: revisions.length,
            revisions,
          }, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  },

  /**
   * diff - Get diff between two versions
   */
  diff: async ({ memory_id, v1, v2 }) => {
    try {
      const diffResult = await diffRevisions(memory_id, v1, v2);
      return {
        content: [{
          type: 'text',
          text: diffResult,
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  },

  /**
   * detect_conflict - Detect conflicts between local and remote
   */
  detect_conflict: async ({ memory_id, local_content, remote_version }) => {
    try {
      const report = await detectConflict(memory_id, local_content, remote_version);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(report, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  },

  /**
   * resolve - Resolve a detected conflict
   */
  resolve: async ({ memory_id, resolution, merged_content }) => {
    try {
      await resolveConflict(memory_id, resolution, merged_content);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            success: true,
            memory_id,
            resolution,
          }),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  },

  /**
   * auto_merge - Auto-merge local and remote revisions
   */
  auto_merge: async ({ local_revisions, remote_revisions, policy }) => {
    try {
      const result = await autoMerge(local_revisions, remote_revisions, policy);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(result, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  },

  /**
   * pending_conflicts - List all pending conflicts
   */
  pending_conflicts: async () => {
    try {
      const conflicts = await getPendingConflicts();
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            count: conflicts.length,
            conflicts,
          }, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  },
};

// ============ Tool Registration ============

export function registerRevisionTools(server) {
  server.registerTool('memory_revision', {
    description: 'Memory revision management - record changes, detect conflicts, resolve merges, and view version history.',
    inputSchema: z.object({
      action: z.enum(['record', 'history', 'diff', 'detect_conflict', 'resolve', 'auto_merge', 'pending_conflicts']),
      memory_id: z.string().optional(),
      content: z.string().optional(),
      change_type: z.enum(['created', 'updated', 'deleted']).optional(),
      changed_by: z.string().optional().default('unknown'),
      commit_hash: z.string().optional(),
      limit: z.number().optional().default(50),
      v1: z.number().optional(),
      v2: z.number().optional(),
      local_content: z.string().optional(),
      remote_version: z.any().optional(),
      resolution: z.enum(['local', 'remote', 'merged', 'manual']).optional(),
      merged_content: z.string().optional(),
      local_revisions: z.array(z.any()).optional(),
      remote_revisions: z.array(z.any()).optional(),
      policy: z.enum(['last-write-wins', 'local-wins', 'remote-wins', 'manual']).optional().default('last-write-wins'),
    }),
  }, async (args) => {
    const handler = memoryRevisionHandlers[args.action];
    if (!handler) {
      return { content: [{ type: 'text', text: `Unknown action: ${args.action}` }], isError: true };
    }
    return handler(args);
  });
}
