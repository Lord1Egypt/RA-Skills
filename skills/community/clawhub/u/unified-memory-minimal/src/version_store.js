/**
 * version_store.js — Version Storage for Memory Snapshots (Feature #11)
 * Every memory update creates a new version in memory_versions.json
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WORKSPACE = process.env.OPENCLAW_WORKSPACE_DIR ?? join(process.env.HOME ?? '/root', '.openclaw', 'workspace');
const VERSIONS_FILE = join(WORKSPACE, 'memory', 'memory_versions.json');
const MAX_VERSIONS_PER_MEMORY = 50;
const MAX_TOTAL_VERSIONS = 10000;

/** Load version store from disk */
export function loadVersionStore() {
  if (!existsSync(VERSIONS_FILE)) {
    return {};
  }
  try {
    return JSON.parse(readFileSync(VERSIONS_FILE, 'utf8'));
  } catch (err) {
    console.error('[version_store] Load error:', err.message);
    return {};
  }
}

/** Persist version store to disk */
function persistVersionStore(store) {
  try {
    const dir = join(WORKSPACE, 'memory');
    if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
    writeFileSync(VERSIONS_FILE, JSON.stringify(store, null, 2), 'utf8');
  } catch (err) { console.error('[version_store] Persist error:', err.message); }
}

function generateVersionId() { return `v_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`; }

/** Create a new version for a memory */
export function createVersion(memoryId, newContent, oldContent = null, changeType = 'update') {
  const store = loadVersionStore();
  
  if (!store[memoryId]) {
    store[memoryId] = { versions: [] };
  }
  
  const versions = store[memoryId].versions;
  const latestVersion = versions[versions.length - 1];
  
  // Generate diff from previous version
  let diffFromPrev = null;
  if (oldContent && latestVersion) {
    diffFromPrev = computeSimpleDiff(latestVersion.content, newContent);
  } else if (!latestVersion && newContent) {
    diffFromPrev = computeSimpleDiff({}, newContent);
  }
  
  const version = {
    versionId: generateVersionId(),
    content: newContent,
    timestamp: Date.now(),
    changeType,
    diffFromPrev,
  };
  
  // Add version
  versions.push(version);
  
  // Trim if exceeds limit
  if (versions.length > MAX_VERSIONS_PER_MEMORY) {
    versions.splice(0, versions.length - MAX_VERSIONS_PER_MEMORY);
  }
  
  // Trim global store if too large
  const totalVersions = Object.values(store).reduce((sum, m) => sum + m.versions.length, 0);
  if (totalVersions > MAX_TOTAL_VERSIONS) {
    trimOldestVersions(store, totalVersions - MAX_TOTAL_VERSIONS);
  }
  
  persistVersionStore(store);
  return version;
}

/**
 * Simple line-by-line diff (no external deps)
 */
function computeSimpleDiff(oldObj, newObj) {
  const oldText = typeof oldObj === 'string' ? oldObj : JSON.stringify(oldObj, null, 2);
  const newText = typeof newObj === 'string' ? newObj : JSON.stringify(newObj, null, 2);
  
  const oldLines = oldText.split('\n');
  const newLines = newText.split('\n');
  
  const diff = {
    added: [],
    removed: [],
    unchanged: [],
  };
  
  // Simple diff: find lines that are new or removed
  const oldSet = new Set(oldLines);
  const newSet = new Set(newLines);
  
  for (const line of newLines) {
    if (!oldSet.has(line)) {
      diff.added.push(line);
    }
  }
  
  for (const line of oldLines) {
    if (!newSet.has(line)) {
      diff.removed.push(line);
    }
  }
  
  diff.addedCount = diff.added.length;
  diff.removedCount = diff.removed.length;
  
  return diff;
}

/**
 * Trim oldest versions when store is too large
 */
function trimOldestVersions(store, count) {
  const allVersions = [];
  
  for (const [memoryId, data] of Object.entries(store)) {
    for (const version of data.versions) {
      allVersions.push({ memoryId, version });
    }
  }
  
  // Sort by timestamp oldest first
  allVersions.sort((a, b) => a.version.timestamp - b.version.timestamp);
  
  // Remove oldest
  for (let i = 0; i < count && i < allVersions.length; i++) {
    const { memoryId, version } = allVersions[i];
    const idx = store[memoryId].versions.findIndex(v => v.versionId === version.versionId);
    if (idx !== -1) {
      store[memoryId].versions.splice(idx, 1);
    }
  }
  
  // Clean up empty entries
  for (const memoryId of Object.keys(store)) {
    if (store[memoryId].versions.length === 0) {
      delete store[memoryId];
    }
  }
}

/**
 * Get all versions for a memory
 */
export function getVersions(memoryId) {
  const store = loadVersionStore();
  const data = store[memoryId];
  if (!data) return [];
  return data.versions.map(v => ({
    versionId: v.versionId,
    timestamp: v.timestamp,
    changeType: v.changeType,
    diffFromPrev: v.diffFromPrev ? {
      addedCount: v.diffFromPrev.addedCount,
      removedCount: v.diffFromPrev.removedCount,
    } : null,
  }));
}

/**
 * Get a specific version
 */
export function getVersion(memoryId, versionId) {
  const store = loadVersionStore();
  const data = store[memoryId];
  if (!data) return null;
  return data.versions.find(v => v.versionId === versionId) || null;
}

/**
 * Get latest version of a memory
 */
export function getLatestVersion(memoryId) {
  const store = loadVersionStore();
  const data = store[memoryId];
  if (!data || data.versions.length === 0) return null;
  return data.versions[data.versions.length - 1];
}

/**
 * Get version count for a memory
 */
export function getVersionCount(memoryId) {
  const store = loadVersionStore();
  const data = store[memoryId];
  return data?.versions.length || 0;
}

/**
 * Delete all versions for a memory
 */
export function deleteVersions(memoryId) {
  const store = loadVersionStore();
  if (store[memoryId]) {
    delete store[memoryId];
    persistVersionStore(store);
  }
  return { success: true };
}

/**
 * Get global version stats
 */
export function getVersionStats() {
  const store = loadVersionStore();
  let totalVersions = 0;
  let totalMemories = Object.keys(store).length;
  
  const counts = {};
  for (const [memoryId, data] of Object.entries(store)) {
    const count = data.versions.length;
    totalVersions += count;
    counts[memoryId] = count;
  }
  
  return {
    totalVersions,
    totalMemories,
    maxPerMemory: MAX_VERSIONS_PER_MEMORY,
    memoryCounts: counts,
  };
}

export default {
  createVersion,
  getVersions,
  getVersion,
  getLatestVersion,
  getVersionCount,
  deleteVersions,
  getVersionStats,
  loadVersionStore,
};
