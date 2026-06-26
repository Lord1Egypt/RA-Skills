/**
 * working_memory.js - Working Memory Data Model
 * 
 * Short-term, task-focused context that evaporates after task completion.
 * Unlike episodic memory (sessions), working memory is for "currently working on X".
 * 
 * Key characteristics:
 * - Auto-expires after TTL (default 2 hours)
 * - Max 5 active working memories (oldest auto-archived on limit)
 * - States: ACTIVE | HELD | CLEARED
 * - Context window for current task details
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import crypto from 'crypto';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const WORKING_MEMORY_FILE = join(MEMORY_DIR, 'working_memory.json');

// Ensure memory directory exists
if (!existsSync(MEMORY_DIR)) {
  mkdirSync(MEMORY_DIR, { recursive: true });
}

// ============================================================================
// Constants
// ============================================================================

/** @type {Readonly<{ACTIVE: 'ACTIVE', HELD: 'HELD', CLEARED: 'CLEARED'}>} */
export const WorkingMemoryStatus = Object.freeze({
  ACTIVE: 'ACTIVE',
  HELD: 'HELD',
  CLEARED: 'CLEARED',
});

/** Default TTL: 2 hours in milliseconds */
export const DEFAULT_WORKING_MEMORY_TTL = 2 * 60 * 60 * 1000; // 7200000ms

/** Maximum active working memories */
export const MAX_ACTIVE_WORKING_MEMORIES = 5;

/** Default context window size (in tokens, approximate) */
export const DEFAULT_CONTEXT_WINDOW = 4000;

// ============================================================================
// Working Memory Factory
// ============================================================================

/**
 * Generate a unique working memory ID
 * @returns {string}
 */
export function generateWorkingMemoryId() {
  return `wm_${crypto.randomUUID().slice(0, 8)}_${Date.now().toString(36)}`;
}

/**
 * Create a new working memory object
 * @param {object} options
 * @param {string} options.taskId - Unique task identifier
 * @param {string} options.description - Task description
 * @param {string} [options.contextWindow] - Current context/details of the task
 * @param {number} [options.ttlMs] - TTL in milliseconds
 * @param {string} [options.episodeId] - Optional episode ID to link with
 * @param {string} [options.parentTaskId] - Optional parent task ID for hierarchy
 * @returns {WorkingMemory}
 */
export function createWorkingMemory({ taskId, description, contextWindow = '', ttlMs = DEFAULT_WORKING_MEMORY_TTL, episodeId = null, parentTaskId = null }) {
  const now = Date.now();
  return {
    id: generateWorkingMemoryId(),
    taskId: taskId || `task_${Date.now().toString(36)}`,
    description,
    status: WorkingMemoryStatus.ACTIVE,
    contextWindow,
    createdAt: now,
    updatedAt: now,
    expiresAt: now + ttlMs,
    heldAt: null,
    episodeId,           // Link to episodic memory (session/conversation)
    parentTaskId,        // Parent task ID for hierarchy
    subtaskIds: [],      // Child task IDs
    metadata: {},        // Arbitrary metadata
  };
}

// ============================================================================
// Working Memory Store (Persistence)
// ============================================================================

/**
 * Load all working memories from disk
 * @returns {WorkingMemory[]}
 */
export function loadWorkingMemories() {
  if (!existsSync(WORKING_MEMORY_FILE)) {
    return [];
  }
  try {
    const data = JSON.parse(readFileSync(WORKING_MEMORY_FILE, 'utf-8'));
    return Array.isArray(data) ? data : [];
  } catch {
    return [];
  }
}

/**
 * Save all working memories to disk
 * @param {WorkingMemory[]} memories
 */
export function saveWorkingMemories(memories) {
  try {
    writeFileSync(WORKING_MEMORY_FILE, JSON.stringify(memories, null, 2), 'utf-8');
  } catch (err) {
    console.error(`[working_memory] Failed to save: ${err.message}`);
  }
}

/**
 * Persist working memories (alias for saveWorkingMemories)
 * @param {WorkingMemory[]} memories
 */
export function persistWorkingMemories(memories) {
  saveWorkingMemories(memories);
}

// ============================================================================
// Working Memory Queries
// ============================================================================

/**
 * Check if a working memory is expired
 * @param {WorkingMemory} wm
 * @returns {boolean}
 */
export function isExpired(wm) {
  return Date.now() > wm.expiresAt;
}

/**
 * Check if a working memory is active
 * @param {WorkingMemory} wm
 * @returns {boolean}
 */
export function isActive(wm) {
  return wm.status === WorkingMemoryStatus.ACTIVE && !isExpired(wm);
}

/**
 * Check if a working memory is held
 * @param {WorkingMemory} wm
 * @returns {boolean}
 */
export function isHeld(wm) {
  return wm.status === WorkingMemoryStatus.HELD;
}

/**
 * Filter working memories by status and expiration
 * @param {WorkingMemory[]} memories
 * @returns {{active: WorkingMemory[], held: WorkingMemory[], expired: WorkingMemory[]}}
 */
export function categorizeWorkingMemories(memories) {
  const now = Date.now();
  const active = [];
  const held = [];
  const expired = [];

  for (const wm of memories) {
    if (wm.status === WorkingMemoryStatus.CLEARED) continue;
    if (now > wm.expiresAt) {
      expired.push(wm);
    } else if (wm.status === WorkingMemoryStatus.HELD) {
      held.push(wm);
    } else {
      active.push(wm);
    }
  }

  return { active, held, expired };
}

/**
 * Get all valid (non-cleared, non-expired) working memories
 * @param {WorkingMemory[]} [memories]
 * @returns {WorkingMemory[]}
 */
export function getValidWorkingMemories(memories = null) {
  const all = memories || loadWorkingMemories();
  const now = Date.now();
  return all.filter(wm =>
    wm.status !== WorkingMemoryStatus.CLEARED && now <= wm.expiresAt
  );
}

/**
 * Find a working memory by ID
 * @param {string} id
 * @param {WorkingMemory[]} [memories]
 * @returns {WorkingMemory|null}
 */
export function findWorkingMemoryById(id, memories = null) {
  const all = memories || loadWorkingMemories();
  return all.find(wm => wm.id === id) || null;
}

/**
 * Format working memory for display
 * @param {WorkingMemory} wm
 * @returns {object}
 */
export function formatWorkingMemory(wm) {
  const now = Date.now();
  const isExpired_ = now > wm.expiresAt;
  const remainingMs = wm.expiresAt - now;

  return {
    id: wm.id,
    taskId: wm.taskId,
    description: wm.description,
    status: wm.status,
    contextWindow: wm.contextWindow,
    createdAt: new Date(wm.createdAt).toISOString(),
    updatedAt: new Date(wm.updatedAt).toISOString(),
    expiresAt: new Date(wm.expiresAt).toISOString(),
    remainingMs: Math.max(0, remainingMs),
    isExpired: isExpired_,
    episodeId: wm.episodeId,
    parentTaskId: wm.parentTaskId,
    subtaskCount: wm.subtaskIds?.length || 0,
  };
}

/**
 * Prune expired and cleared working memories from storage
 * @returns {{pruned: number, remaining: number}}
 */
export function pruneWorkingMemories() {
  const all = loadWorkingMemories();
  const now = Date.now();
  const before = all.length;

  const remaining = all.filter(wm => {
    // Keep if not cleared AND not expired
    if (wm.status === WorkingMemoryStatus.CLEARED) return false;
    if (now > wm.expiresAt) return false;
    return true;
  });

  if (remaining.length < all.length) {
    saveWorkingMemories(remaining);
  }

  return { pruned: before - remaining.length, remaining: remaining.length };
}

/**
 * @typedef {Object} WorkingMemory
 * @property {string} id
 * @property {string} taskId
 * @property {string} description
 * @property {'ACTIVE'|'HELD'|'CLEARED'} status
 * @property {string} contextWindow
 * @property {number} createdAt
 * @property {number} updatedAt
 * @property {number} expiresAt
 * @property {number|null} heldAt
 * @property {string|null} episodeId
 * @property {string|null} parentTaskId
 * @property {string[]} subtaskIds
 * @property {object} metadata
 */
