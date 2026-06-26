/**
 * memory_diff.js — Memory Diff Operations
 * Part of Feature #11: Semantic Versioning
 * 
 * Handles diff generation, version restoration, and version history queries.
 */
import { loadVersionStore, getVersions, getVersion, getLatestVersion, createVersion, getVersionCount } from './version_store.js';
import { getMemory, updateMemory, getAllMemories } from './storage.js';

/**
 * Create a diff between two versions
 */
export function createVersionDiff(memoryId, versionId1, versionId2) {
  const v1 = getVersion(memoryId, versionId1);
  const v2 = getVersion(memoryId, versionId2);
  
  if (!v1 || !v2) {
    throw new Error('One or both versions not found');
  }
  
  const diff = computeDetailedDiff(v1.content, v2.content);
  
  return {
    memoryId,
    fromVersion: { versionId: v1.versionId, timestamp: v1.timestamp },
    toVersion: { versionId: v2.versionId, timestamp: v2.timestamp },
    diff,
  };
}

/**
 * Detailed diff between two content objects
 */
function computeDetailedDiff(content1, content2) {
  const text1 = typeof content1 === 'string' ? content1 : JSON.stringify(content1, null, 2);
  const text2 = typeof content2 === 'string' ? content2 : JSON.stringify(content2, null, 2);
  
  const lines1 = text1.split('\n');
  const lines2 = text2.split('\n');
  
  // Find LCS (Longest Common Subsequence) for alignment
  const lcs = computeLCS(lines1, lines2);
  
  const result = {
    lines: [],
    stats: { added: 0, removed: 0, unchanged: 0 },
  };
  
  let i1 = 0, i2 = 0, li = 0;
  
  while (i1 < lines1.length || i2 < lines2.length) {
    if (li < lcs.length && i1 < lines1.length && lines1[i1] === lcs[li] && i2 < lines2.length && lines2[i2] === lcs[li]) {
      result.lines.push({ type: 'unchanged', content: lines1[i1] });
      result.stats.unchanged++;
      i1++; i2++; li++;
    } else if (i2 < lines2.length && (li >= lcs.length || lines2[i2] !== lcs[li])) {
      result.lines.push({ type: 'added', content: lines2[i2] });
      result.stats.added++;
      i2++;
    } else if (i1 < lines1.length && (li >= lcs.length || lines1[i1] !== lcs[li])) {
      result.lines.push({ type: 'removed', content: lines1[i1] });
      result.stats.removed++;
      i1++;
    }
  }
  
  return result;
}

/**
 * Compute LCS (Longest Common Subsequence)
 */
function computeLCS(arr1, arr2) {
  const m = arr1.length;
  const n = arr2.length;
  const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));
  
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (arr1[i - 1] === arr2[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }
  
  // Backtrack to find LCS
  const lcs = [];
  let i = m, j = n;
  while (i > 0 && j > 0) {
    if (arr1[i - 1] === arr2[j - 1]) {
      lcs.unshift(arr1[i - 1]);
      i--; j--;
    } else if (dp[i - 1][j] > dp[i][j - 1]) {
      i--;
    } else {
      j--;
    }
  }
  
  return lcs;
}

/**
 * Restore a memory to a specific version
 */
export function restoreVersion(memoryId, versionId) {
  const version = getVersion(memoryId, versionId);
  
  if (!version) {
    throw new Error(`Version ${versionId} not found for memory ${memoryId}`);
  }
  
  // Get current memory
  const currentMemory = getMemory(memoryId);
  
  // Create a new version with the old content (for rollback tracking)
  createVersion(memoryId, currentMemory, version.content, 'rollback');
  
  // Update memory with restored content
  if (currentMemory) {
    const restored = {
      ...currentMemory,
      ...version.content,
      updated_at: Date.now(),
    };
    updateMemory(restored);
  }
  
  return {
    success: true,
    memoryId,
    restoredTo: { versionId: version.versionId, timestamp: version.timestamp },
    changeType: version.changeType,
  };
}

/**
 * List all versions for a memory with optional filters
 */
export function listVersions(memoryId, options = {}) {
  const { limit = 10, offset = 0, changeType } = options;
  
  let versions = getVersions(memoryId);
  
  if (changeType) {
    versions = versions.filter(v => v.changeType === changeType);
  }
  
  versions = versions.slice(offset, offset + limit);
  
  return {
    memoryId,
    total: getVersionCount(memoryId),
    offset,
    limit,
    versions,
  };
}

/**
 * Compare two adjacent versions (current vs previous)
 */
export function compareAdjacentVersions(memoryId, versionId) {
  const versions = getVersions(memoryId);
  const idx = versions.findIndex(v => v.versionId === versionId);
  
  if (idx === -1) {
    throw new Error(`Version ${versionId} not found`);
  }
  
  const current = versions[idx];
  const previous = idx > 0 ? versions[idx - 1] : null;
  
  const diff = previous 
    ? computeDetailedDiff(previous.content, current.content)
    : { lines: [{ type: 'added', content: JSON.stringify(current.content) }], stats: { added: 1, removed: 0, unchanged: 0 } };
  
  return {
    current: { versionId: current.versionId, timestamp: current.timestamp },
    previous: previous ? { versionId: previous.versionId, timestamp: previous.timestamp } : null,
    diff,
  };
}

/**
 * Get version timeline for a memory
 */
export function getVersionTimeline(memoryId) {
  const versions = getVersions(memoryId);
  
  return versions.map((v, idx) => ({
    position: idx + 1,
    versionId: v.versionId,
    timestamp: v.timestamp,
    changeType: v.changeType,
    diff: v.diffFromPrev ? {
      added: v.diffFromPrev.addedCount,
      removed: v.diffFromPrev.removedCount,
    } : null,
  }));
}

// Re-export version store functions for backwards compatibility
export { getVersion, getVersions, getLatestVersion, createVersion, getVersionCount, getVersionStats, deleteVersions } from './version_store.js';

export default {
  createVersionDiff,
  restoreVersion,
  listVersions,
  compareAdjacentVersions,
  getVersionTimeline,
  computeDetailedDiff,
};
