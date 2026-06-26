/**
 * working_memory_manager.js - Working Memory Manager
 * 
 * Manages working memory lifecycle: create, hold, resume, clear, extend, list.
 * Enforces max limit (oldest archived when limit hit) and auto-expiration.
 */

import {
  createWorkingMemory,
  loadWorkingMemories,
  saveWorkingMemories,
  persistWorkingMemories,
  WorkingMemoryStatus,
  DEFAULT_WORKING_MEMORY_TTL,
  MAX_ACTIVE_WORKING_MEMORIES,
  categorizeWorkingMemories,
  findWorkingMemoryById,
  formatWorkingMemory,
  pruneWorkingMemories,
  isActive,
  isExpired,
  isHeld,
} from './working_memory.js';
import { config } from './config.js';

// Use config values if available, fall back to constants
const MAX_ACTIVE = config.maxWorkingMemories || MAX_ACTIVE_WORKING_MEMORIES;
const DEFAULT_TTL = config.workingMemoryTTL || DEFAULT_WORKING_MEMORY_TTL;

// ============================================================================
// Manager State
// ============================================================================

/** In-memory cache to avoid repeated disk reads */
let _cache = null;
let _cacheDirty = false;

/**
 * Get working memories with caching
 * @returns {import('./working_memory.js').WorkingMemory[]}
 */
function getStore() {
  if (_cache === null) {
    _cache = loadWorkingMemories();
  }
  return _cache;
}

/**
 * Mark cache as dirty and persist
 */
function markDirty() {
  _cacheDirty = true;
  persistWorkingMemories(getStore());
}

/**
 * Invalidate cache (force reload from disk)
 */
function invalidateCache() {
  _cache = null;
  _cacheDirty = false;
}

// ============================================================================
// Core Operations
// ============================================================================

/**
 * Create a new working memory
 * 
 * @param {string} taskDescription - Description of the task
 * @param {object} options
 * @param {string} [options.taskId] - Custom task ID
 * @param {string} [options.contextWindow] - Initial context/details
 * @param {number} [options.ttlMs] - Custom TTL in ms
 * @param {string} [options.episodeId] - Link to episodic memory
 * @param {string} [options.parentTaskId] - Parent task ID for hierarchy
 * @returns {{success: boolean, workingMemory: object|null, archived: object|null, error: string|null}}
 */
export function create({ taskDescription, taskId = null, contextWindow = '', ttlMs = null, episodeId = null, parentTaskId = null }) {
  try {
    pruneWorkingMemories(); // Clean up first
    const store = getStore();
    const ttl = ttlMs || DEFAULT_TTL;

    // Enforce max active limit - archive oldest if needed
    let archived = null;
    const { active } = categorizeWorkingMemories(store);
    
    if (active.length >= MAX_ACTIVE) {
      // Sort by createdAt, oldest first
      const sorted = [...active].sort((a, b) => a.createdAt - b.createdAt);
      const oldest = sorted[0];
      oldest.status = WorkingMemoryStatus.CLEARED;
      oldest.clearedReason = 'max_limit_exceeded';
      oldest.clearedAt = Date.now();
      archived = formatWorkingMemory(oldest);
      markDirty();
    }

    // Create new working memory
    const wm = createWorkingMemory({
      taskId,
      description: taskDescription,
      contextWindow,
      ttlMs: ttl,
      episodeId,
      parentTaskId,
    });

    // Link to parent if provided
    if (parentTaskId) {
      const parent = store.find(w => w.taskId === parentTaskId && w.status !== WorkingMemoryStatus.CLEARED);
      if (parent) {
        if (!parent.subtaskIds) parent.subtaskIds = [];
        if (!parent.subtaskIds.includes(wm.id)) {
          parent.subtaskIds.push(wm.id);
        }
        markDirty();
      }
    }

    store.push(wm);
    markDirty();

    return {
      success: true,
      workingMemory: formatWorkingMemory(wm),
      archived,
      error: null,
    };
  } catch (err) {
    return { success: false, workingMemory: null, archived: null, error: err.message };
  }
}

/**
 * Hold (pause) a working memory without clearing it
 * 
 * @param {string} workingMemoryId - Working memory ID to hold
 * @returns {{success: boolean, workingMemory: object|null, error: string|null}}
 */
export function hold(workingMemoryId) {
  try {
    const store = getStore();
    const wm = store.find(w => w.id === workingMemoryId);

    if (!wm) {
      return { success: false, workingMemory: null, error: 'Working memory not found' };
    }
    if (wm.status === WorkingMemoryStatus.CLEARED) {
      return { success: false, workingMemory: null, error: 'Working memory already cleared' };
    }
    if (wm.status === WorkingMemoryStatus.HELD) {
      return { success: false, workingMemory: null, error: 'Working memory already held' };
    }

    wm.status = WorkingMemoryStatus.HELD;
    wm.heldAt = Date.now();
    wm.updatedAt = Date.now();
    markDirty();

    return { success: true, workingMemory: formatWorkingMemory(wm), error: null };
  } catch (err) {
    return { success: false, workingMemory: null, error: err.message };
  }
}

/**
 * Resume a held working memory back to active
 * 
 * @param {string} workingMemoryId - Working memory ID to resume
 * @param {number} [extendMs] - Optional TTL extension in ms
 * @returns {{success: boolean, workingMemory: object|null, error: string|null}}
 */
export function resume(workingMemoryId, extendMs = null) {
  try {
    const store = getStore();
    const wm = store.find(w => w.id === workingMemoryId);

    if (!wm) {
      return { success: false, workingMemory: null, error: 'Working memory not found' };
    }
    if (wm.status === WorkingMemoryStatus.CLEARED) {
      return { success: false, workingMemory: null, error: 'Cannot resume cleared working memory' };
    }
    if (wm.status === WorkingMemoryStatus.ACTIVE) {
      return { success: false, workingMemory: null, error: 'Working memory is already active' };
    }

    // Check if expired while held
    if (isExpired(wm)) {
      wm.status = WorkingMemoryStatus.CLEARED;
      wm.clearedReason = 'ttl_expired_while_held';
      wm.clearedAt = Date.now();
      markDirty();
      return { success: false, workingMemory: null, error: 'Working memory expired while held' };
    }

    wm.status = WorkingMemoryStatus.ACTIVE;
    wm.heldAt = null;
    wm.updatedAt = Date.now();

    // Extend TTL if requested
    if (extendMs) {
      wm.expiresAt = Date.now() + extendMs;
    }

    markDirty();
    return { success: true, workingMemory: formatWorkingMemory(wm), error: null };
  } catch (err) {
    return { success: false, workingMemory: null, error: err.message };
  }
}

/**
 * Explicitly clear a working memory
 * 
 * @param {string} workingMemoryId - Working memory ID to clear
 * @param {string} [reason] - Reason for clearing
 * @returns {{success: boolean, workingMemory: object|null, error: string|null}}
 */
export function clear(workingMemoryId, reason = 'explicit_clear') {
  try {
    const store = getStore();
    const wm = store.find(w => w.id === workingMemoryId);

    if (!wm) {
      return { success: false, workingMemory: null, error: 'Working memory not found' };
    }
    if (wm.status === WorkingMemoryStatus.CLEARED) {
      return { success: false, workingMemory: null, error: 'Working memory already cleared' };
    }

    wm.status = WorkingMemoryStatus.CLEARED;
    wm.clearedReason = reason;
    wm.clearedAt = Date.now();
    wm.updatedAt = Date.now();

    // Auto-hold subtasks when parent is cleared
    if (wm.subtaskIds && wm.subtaskIds.length > 0) {
      for (const subtaskId of wm.subtaskIds) {
        const subtask = store.find(w => w.id === subtaskId);
        if (subtask && subtask.status === WorkingMemoryStatus.ACTIVE) {
          subtask.status = WorkingMemoryStatus.HELD;
          subtask.heldAt = Date.now();
          subtask.heldReason = 'parent_cleared';
          subtask.updatedAt = Date.now();
        }
      }
    }

    markDirty();
    return { success: true, workingMemory: formatWorkingMemory(wm), error: null };
  } catch (err) {
    return { success: false, workingMemory: null, error: err.message };
  }
}

/**
 * Extend the TTL of a working memory
 * 
 * @param {string} workingMemoryId - Working memory ID
 * @param {number} durationMs - Duration to extend in ms
 * @returns {{success: boolean, workingMemory: object|null, error: string|null}}
 */
export function extend(workingMemoryId, durationMs) {
  try {
    const store = getStore();
    const wm = store.find(w => w.id === workingMemoryId);

    if (!wm) {
      return { success: false, workingMemory: null, error: 'Working memory not found' };
    }
    if (wm.status === WorkingMemoryStatus.CLEARED) {
      return { success: false, workingMemory: null, error: 'Cannot extend cleared working memory' };
    }

    wm.expiresAt = Date.now() + durationMs;
    wm.updatedAt = Date.now();
    markDirty();

    return { success: true, workingMemory: formatWorkingMemory(wm), error: null };
  } catch (err) {
    return { success: false, workingMemory: null, error: err.message };
  }
}

/**
 * Get all active working memories (non-cleared, non-expired)
 * 
 * @returns {object[]}
 */
export function getActive() {
  pruneWorkingMemories();
  const store = getStore();
  const { active, held } = categorizeWorkingMemories(store);

  return {
    active: active.map(formatWorkingMemory).sort((a, b) => a.createdAt.localeCompare(b.createdAt)),
    held: held.map(formatWorkingMemory).sort((a, b) => a.heldAt?.localeCompare(b.heldAt)),
    counts: {
      active: active.length,
      held: held.length,
      maxActive: MAX_ACTIVE,
    },
  };
}

/**
 * Get a specific working memory by ID
 * @param {string} workingMemoryId
 * @returns {object|null}
 */
export function get(workingMemoryId) {
  const store = getStore();
  const wm = store.find(w => w.id === workingMemoryId);
  if (!wm) return null;
  
  // Auto-clear if expired
  if (isExpired(wm) && wm.status !== WorkingMemoryStatus.CLEARED) {
    wm.status = WorkingMemoryStatus.CLEARED;
    wm.clearedReason = 'ttl_expired';
    wm.clearedAt = Date.now();
    markDirty();
    return null;
  }
  
  return formatWorkingMemory(wm);
}

/**
 * Update context window for a working memory
 * @param {string} workingMemoryId
 * @param {string} contextWindow
 * @returns {{success: boolean, workingMemory: object|null, error: string|null}}
 */
export function updateContext(workingMemoryId, contextWindow) {
  try {
    const store = getStore();
    const wm = store.find(w => w.id === workingMemoryId);

    if (!wm) {
      return { success: false, workingMemory: null, error: 'Working memory not found' };
    }
    if (wm.status === WorkingMemoryStatus.CLEARED) {
      return { success: false, workingMemory: null, error: 'Cannot update cleared working memory' };
    }

    wm.contextWindow = contextWindow;
    wm.updatedAt = Date.now();
    markDirty();

    return { success: true, workingMemory: formatWorkingMemory(wm), error: null };
  } catch (err) {
    return { success: false, workingMemory: null, error: err.message };
  }
}

/**
 * Clear all working memories
 * @param {string} [reason]
 * @returns {{cleared: number}}
 */
export function clearAll(reason = 'clear_all') {
  const store = getStore();
  let cleared = 0;

  for (const wm of store) {
    if (wm.status !== WorkingMemoryStatus.CLEARED) {
      wm.status = WorkingMemoryStatus.CLEARED;
      wm.clearedReason = reason;
      wm.clearedAt = Date.now();
      cleared++;
    }
  }

  if (cleared > 0) markDirty();
  return { cleared };
}
