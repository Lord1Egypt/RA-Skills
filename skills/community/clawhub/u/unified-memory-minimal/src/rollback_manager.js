/**
 * rollback_manager.js — Rollback Operations Manager
 * Part of Feature #11: Semantic Versioning
 * 
 * High-level rollback API: rollback to specific version, undo changes, rollback all.
 */
import { restoreVersion as restoreMemoryVersion, getVersions, getVersion, getVersionCount, getVersionStats } from './memory_diff.js';
import { deleteVersions } from './version_store.js';
import { getMemory, getAllMemories, updateMemory } from './storage.js';

/**
 * Rollback a single memory to a specific version
 */
export async function rollback(memoryId, versionId) {
  try {
    const currentMemory = getMemory(memoryId);
    if (!currentMemory) {
      throw new Error(`Memory ${memoryId} not found`);
    }
    
    const version = getVersion(memoryId, versionId);
    if (!version) {
      throw new Error(`Version ${versionId} not found`);
    }
    
    // Perform rollback
    const result = restoreMemoryVersion(memoryId, versionId);
    
    return {
      success: true,
      action: 'rollback',
      memoryId,
      ...result,
    };
  } catch (err) {
    return {
      success: false,
      error: err.message,
    };
  }
}

/**
 * Rollback all memories to a specific version (by timestamp)
 */
export async function rollbackAll(targetTimestamp) {
  const results = {
    success: [],
    failed: [],
    timestamp: targetTimestamp,
  };
  
  const allMemories = getAllMemories();
  const store = await import('./version_store.js');
  const versionStore = store.loadVersionStore();
  
  for (const memory of allMemories) {
    const versions = versionStore[memory.id]?.versions || [];
    
    // Find version at or before target timestamp
    const targetVersion = versions
      .filter(v => v.timestamp <= targetTimestamp)
      .sort((a, b) => b.timestamp - a.timestamp)[0];
    
    if (targetVersion) {
      try {
        await rollback(memory.id, targetVersion.versionId);
        results.success.push(memory.id);
      } catch (err) {
        results.failed.push({ memoryId: memory.id, error: err.message });
      }
    } else {
      results.failed.push({ memoryId: memory.id, error: 'No version at or before target timestamp' });
    }
  }
  
  return results;
}

/**
 * Undo last change to a memory (rollback to previous version)
 */
export async function undoLastChange(memoryId) {
  const versions = getVersions(memoryId);
  
  if (versions.length < 2) {
    return {
      success: false,
      error: 'No previous version to undo to',
    };
  }
  
  // Second to last version is the "current" one before last change
  const lastVersion = versions[versions.length - 1];
  const previousVersion = versions[versions.length - 2];
  
  return await rollback(memoryId, previousVersion.versionId);
}

/**
 * Get rollback candidates (memories with multiple versions)
 */
export function getRollbackCandidates() {
  const stats = getVersionStats();
  const candidates = [];
  
  for (const [memoryId, count] of Object.entries(stats.memoryCounts)) {
    if (count >= 2) {
      const memory = getMemory(memoryId);
      candidates.push({
        memoryId,
        currentText: memory?.text?.substring(0, 100) || '',
        versionCount: count,
      });
    }
  }
  
  return candidates;
}

/**
 * Batch rollback multiple memories
 */
export async function batchRollback(operations) {
  const results = {
    success: [],
    failed: [],
  };
  
  for (const op of operations) {
    const { memoryId, versionId } = op;
    const result = await rollback(memoryId, versionId);
    
    if (result.success) {
      results.success.push(memoryId);
    } else {
      results.failed.push({ memoryId, error: result.error });
    }
  }
  
  return results;
}

/**
 * Clear version history for a memory
 */
export function clearVersionHistory(memoryId) {
  try {
    deleteVersions(memoryId);
    return { success: true, memoryId };
  } catch (err) {
    return { success: false, error: err.message };
  }
}

/**
 * Get rollback preview (what would happen if rolled back)
 */
export function getRollbackPreview(memoryId, versionId) {
  const currentMemory = getMemory(memoryId);
  const version = getVersion(memoryId, versionId);
  
  if (!currentMemory || !version) {
    return null;
  }
  
  return {
    memoryId,
    current: {
      text: currentMemory.text?.substring(0, 200),
      updatedAt: currentMemory.updated_at,
    },
    restoreTo: {
      versionId: version.versionId,
      text: version.content?.text?.substring(0, 200),
      timestamp: version.timestamp,
    },
    willChange: currentMemory.text !== version.content?.text,
  };
}

export default {
  rollback,
  rollbackAll,
  undoLastChange,
  getRollbackCandidates,
  batchRollback,
  clearVersionHistory,
  getRollbackPreview,
};
