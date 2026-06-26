/**
 * Revision Manager Enhanced - Memory Version Lifecycle Management
 * Complete revision lifecycle with stages, conflict detection, and resolution
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
 * @property {string} [lifecycle_stage] // draft, review, approved, archived
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

// ============ Storage Helpers ============

async function loadRevisions() {
  try {
    const data = await fs.readFile(REVISIONS_FILE, 'utf-8');
    return JSON.parse(data);
  } catch {
    await saveRevisions({ revisions: [], conflicts: [], history: [] });
    return { revisions: [], conflicts: [], history: [] };
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
 * Record a new revision with lifecycle stage
 */
export async function recordRevision(memoryId, newContent, changeType, changedBy = 'unknown', commitHash = null, lifecycleStage = 'approved') {
  const store = await loadRevisions();
  
  const memoryRevisions = store.revisions.filter(r => r.memory_id === memoryId);
  const latestVersion = memoryRevisions.length > 0 
    ? Math.max(...memoryRevisions.map(r => r.version)) 
    : 0;
  
  const previousContent = memoryRevisions.length > 0 
    ? memoryRevisions[memoryRevisions.length - 1].content 
    : null;
  
  const revision = {
    memory_id: memoryId,
    version: latestVersion + 1,
    content: newContent,
    previous_content: previousContent,
    change_type: changeType,
    changed_at: new Date().toISOString(),
    changed_by: changedBy,
    commit_hash: commitHash,
    lifecycle_stage: lifecycleStage
  };
  
  store.revisions.push(revision);
  
  // Check for conflicts
  if (changeType === 'updated' && memoryRevisions.length > 0) {
    const latest = memoryRevisions[memoryRevisions.length - 1];
    if (latest.content !== newContent && latest.changed_by !== changedBy) {
      const conflict = {
        id: generateId(),
        memory_id: memoryId,
        local_version: { ...latest, changed_by: 'local' },
        remote_version: { ...revision, changed_by: changedBy },
        created_at: new Date().toISOString(),
        resolution: null
      };
      store.conflicts.push(conflict);
    }
  }
  
  // Log to history
  store.history.push({
    action: 'revision_created',
    memory_id: memoryId,
    version: revision.version,
    timestamp: revision.changed_at
  });
  
  await saveRevisions(store);
  return revision;
}

/**
 * Get all revisions for a memory
 */
export async function getRevisions(memoryId) {
  const store = await loadRevisions();
  return store.revisions
    .filter(r => r.memory_id === memoryId)
    .sort((a, b) => a.version - b.version);
}

/**
 * Get current content (latest revision)
 */
export async function getCurrentContent(memoryId) {
  const revisions = await getRevisions(memoryId);
  return revisions.length > 0 ? revisions[revisions.length - 1].content : null;
}

/**
 * Get revision history with metadata
 */
export async function getRevisionHistory(memoryId) {
  const revisions = await getRevisions(memoryId);
  
  return revisions.map((rev, index) => ({
    version: rev.version,
    change_type: rev.change_type,
    changed_at: rev.changed_at,
    changed_by: rev.changed_by,
    commit_hash: rev.commit_hash,
    lifecycle_stage: rev.lifecycle_stage,
    content_preview: rev.content.substring(0, 100) + (rev.content.length > 100 ? '...' : ''),
    has_previous: index > 0,
    previous_version: index > 0 ? revisions[index - 1].version : null
  }));
}

/**
 * Detect conflicts
 */
export function detectConflicts(localContent, remoteContent, localVersion, remoteVersion) {
  if (localContent === remoteContent) {
    return { has_conflict: false };
  }
  
  return {
    has_conflict: true,
    local_version: localVersion,
    remote_version: remoteVersion,
    local_content: localContent,
    remote_content: remoteContent
  };
}

/**
 * Auto-merge with last-write-wins
 */
export function autoMerge(localContent, remoteContent, localTimestamp, remoteTimestamp) {
  const localDate = new Date(localTimestamp);
  const remoteDate = new Date(remoteTimestamp);
  
  return remoteDate > localDate ? remoteContent : localContent;
}

/**
 * Resolve conflict manually
 */
export async function resolveConflict(conflictId, resolution, mergedContent = null) {
  const store = await loadRevisions();
  const conflict = store.conflicts.find(c => c.id === conflictId);
  
  if (!conflict) {
    return { success: false, error: 'Conflict not found' };
  }
  
  conflict.resolution = resolution;
  if (mergedContent) {
    conflict.merged_content = mergedContent;
  }
  
  store.conflicts = store.conflicts.filter(c => c.id !== conflictId);
  await saveRevisions(store);
  return { success: true, conflict };
}

/**
 * Get pending conflicts
 */
export async function getPendingConflicts() {
  const store = await loadRevisions();
  return store.conflicts.filter(c => !c.resolution);
}

/**
 * Get conflict history
 */
export async function getConflictHistory() {
  const store = await loadRevisions();
  return store.conflicts
    .filter(c => c.resolution)
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
}

/**
 * Auto-merge pending conflicts
 */
export async function autoMergePendingConflicts() {
  const store = await loadRevisions();
  const pending = store.conflicts.filter(c => !c.resolution);
  
  const merged = [];
  const failed = [];
  
  for (const conflict of pending) {
    try {
      const mergedContent = autoMerge(
        conflict.local_version.content,
        conflict.remote_version.content,
        conflict.local_version.changed_at,
        conflict.remote_version.changed_at
      );
      
      conflict.resolution = 'merged';
      conflict.merged_content = mergedContent;
      merged.push(conflict);
    } catch (err) {
      failed.push({ conflict, error: err.message });
    }
  }
  
  await saveRevisions(store);
  return { merged: merged.length, failed: failed.length };
}

/**
 * Get revision statistics
 */
export async function getRevisionStats() {
  const store = await loadRevisions();
  
  const totalRevisions = store.revisions.length;
  const uniqueMemories = new Set(store.revisions.map(r => r.memory_id)).size;
  const totalConflicts = store.conflicts.length;
  const resolvedConflicts = store.conflicts.filter(c => c.resolution).length;
  
  return {
    total_revisions,
    unique_memories,
    avg_revisions_per_memory: uniqueMemories > 0 ? totalRevisions / uniqueMemories : 0,
    total_conflicts,
    resolved_conflicts,
    pending_conflicts: totalConflicts - resolvedConflicts,
    conflict_resolution_rate: totalConflicts > 0 ? (resolvedConflicts / totalConflicts) * 100 : 0
  };
}

/**
 * Archive old revisions
 */
export async function archiveOldRevisions(memoryId, keepLast = 10) {
  const store = await loadRevisions();
  const memoryRevisions = store.revisions.filter(r => r.memory_id === memoryId);
  
  if (memoryRevisions.length <= keepLast) {
    return { archived: 0 };
  }
  
  memoryRevisions.sort((a, b) => a.version - b.version);
  const toArchive = memoryRevisions.slice(0, memoryRevisions.length - keepLast);
  const toKeep = memoryRevisions.slice(memoryRevisions.length - keepLast);
  
  store.revisions = store.revisions.filter(r => !toArchive.includes(r));
  await saveRevisions(store);
  return { archived: toArchive.length, kept: toKeep.length };
}

/**
 * Rollback to specific version
 */
export async function rollbackToVersion(memoryId, targetVersion) {
  const revisions = await getRevisions(memoryId);
  const targetRevision = revisions.find(r => r.version === targetVersion);
  
  if (!targetRevision) {
    return { success: false, error: 'Version not found' };
  }
  
  await recordRevision(
    memoryId,
    targetRevision.content,
    'updated',
    'rollback',
    `rollback_to_v${targetVersion}`
  );
  
  return {
    success: true,
    rolled_back_to: targetVersion,
    previous_version: revisions.length,
    new_version: revisions.length + 1
  };
}

/**
 * Get diff between two versions
 */
export function getDiff(version1, version2, content1, content2) {
  const lines1 = content1.split('\n');
  const lines2 = content2.split('\n');
  
  const diff = [];
  const maxLength = Math.max(lines1.length, lines2.length);
  
  for (let i = 0; i < maxLength; i++) {
    const line1 = lines1[i] || '';
    const line2 = lines2[i] || '';
    
    if (line1 !== line2) {
      diff.push({
        line: i + 1,
        old: line1,
        new: line2
      });
    }
  }
  
  return diff;
}

/**
 * Get revisions by lifecycle stage
 */
export async function getRevisionsByStage(lifecycleStage) {
  const store = await loadRevisions();
  return store.revisions.filter(r => r.lifecycle_stage === lifecycleStage);
}

/**
 * Update lifecycle stage
 */
export async function updateLifecycleStage(memoryId, version, newStage) {
  const store = await loadRevisions();
  const revision = store.revisions.find(
    r => r.memory_id === memoryId && r.version === version
  );
  
  if (!revision) {
    return { success: false, error: 'Revision not found' };
  }
  
  revision.lifecycle_stage = newStage;
  await saveRevisions(store);
  return { success: true, revision };
}

/**
 * Get lifecycle summary
 */
export async function getLifecycleSummary() {
  const store = await loadRevisions();
  const stages = {};
  
  store.revisions.forEach(r => {
    stages[r.lifecycle_stage] = (stages[r.lifecycle_stage] || 0) + 1;
  });
  
  return {
    total: store.revisions.length,
    by_stage: stages,
    pending_conflicts: store.conflicts.filter(c => !c.resolution).length
  };
}
