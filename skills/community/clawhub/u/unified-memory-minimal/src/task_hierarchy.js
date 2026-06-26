/**
 * task_hierarchy.js - Task Hierarchy for Working Memory
 * 
 * Supports task trees (parent → subtasks).
 * When parent task is completed/cleared, subtasks are auto-held.
 * Cross-references with episodic memory (sessions/conversations).
 */

import {
  loadWorkingMemories,
  saveWorkingMemories,
  persistWorkingMemories,
  WorkingMemoryStatus,
  formatWorkingMemory,
} from './working_memory.js';
import { config } from './config.js';

// ============================================================================
// Task Hierarchy
// ============================================================================

/**
 * Build the task tree from working memories
 * @returns {{roots: object[], tree: Map<string, object[]>}}
 */
export function buildTaskTree() {
  const memories = loadWorkingMemories().filter(
    wm => wm.status !== WorkingMemoryStatus.CLEARED
  );

  const tree = new Map(); // parentId → children[]
  const roots = [];

  for (const wm of memories) {
    if (!wm.parentTaskId || wm.status === WorkingMemoryStatus.CLEARED) {
      roots.push(wm);
    }
  }

  // Build children map
  for (const wm of memories) {
    if (wm.parentTaskId) {
      if (!tree.has(wm.parentTaskId)) {
        tree.set(wm.parentTaskId, []);
      }
      tree.get(wm.parentTaskId).push(wm);
    }
  }

  return { roots, tree };
}

/**
 * Get subtasks of a working memory
 * @param {string} workingMemoryId
 * @returns {object[]}
 */
export function getSubtasks(workingMemoryId) {
  const memories = loadWorkingMemories();
  const wm = memories.find(w => w.id === workingMemoryId);

  if (!wm) return [];

  return (wm.subtaskIds || [])
    .map(id => memories.find(w => w.id === id))
    .filter(Boolean)
    .map(formatWorkingMemory);
}

/**
 * Add a subtask to a working memory
 * @param {string} parentId - Parent working memory ID
 * @param {string} childId - Child working memory ID
 * @returns {{success: boolean, error: string|null}}
 */
export function addSubtask(parentId, childId) {
  const memories = loadWorkingMemories();
  const parent = memories.find(w => w.id === parentId);
  const child = memories.find(w => w.id === childId);

  if (!parent) return { success: false, error: 'Parent working memory not found' };
  if (!child) return { success: false, error: 'Child working memory not found' };

  if (!parent.subtaskIds) parent.subtaskIds = [];
  if (!parent.subtaskIds.includes(childId)) {
    parent.subtaskIds.push(childId);
  }

  child.parentTaskId = parentId;
  persistWorkingMemories(memories);

  return { success: true, error: null };
}

/**
 * Remove a subtask from a parent
 * @param {string} parentId
 * @param {string} childId
 * @returns {{success: boolean}}
 */
export function removeSubtask(parentId, childId) {
  const memories = loadWorkingMemories();
  const parent = memories.find(w => w.id === parentId);
  const child = memories.find(w => w.id === childId);

  if (parent && parent.subtaskIds) {
    parent.subtaskIds = parent.subtaskIds.filter(id => id !== childId);
  }
  if (child) {
    child.parentTaskId = null;
  }

  persistWorkingMemories(memories);
  return { success: true };
}

/**
 * Complete a parent task and auto-hold all its subtasks
 * @param {string} workingMemoryId
 * @param {string} [reason]
 * @returns {{parent: object, subtasksHeld: number, error: string|null}}
 */
export function completeTask(workingMemoryId, reason = 'parent_completed') {
  const memories = loadWorkingMemories();
  const wm = memories.find(w => w.id === workingMemoryId);

  if (!wm) return { parent: null, subtasksHeld: 0, error: 'Working memory not found' };

  let subtasksHeld = 0;

  // Auto-hold all active subtasks
  if (wm.subtaskIds && wm.subtaskIds.length > 0) {
    for (const subtaskId of wm.subtaskIds) {
      const subtask = memories.find(w => w.id === subtaskId);
      if (subtask && subtask.status === WorkingMemoryStatus.ACTIVE) {
        subtask.status = WorkingMemoryStatus.HELD;
        subtask.heldAt = Date.now();
        subtask.heldReason = reason;
        subtask.updatedAt = Date.now();
        subtasksHeld++;
      }
    }
  }

  persistWorkingMemories(memories);

  return {
    parent: formatWorkingMemory(wm),
    subtasksHeld,
    error: null,
  };
}

/**
 * Get the full ancestry chain (root → ... → parent → current)
 * @param {string} workingMemoryId
 * @returns {object[]}
 */
export function getAncestry(workingMemoryId) {
  const memories = loadWorkingMemories();
  const chain = [];
  let current = memories.find(w => w.id === workingMemoryId);

  while (current) {
    chain.unshift(formatWorkingMemory(current));
    if (!current.parentTaskId) break;
    current = memories.find(w => w.taskId === current.parentTaskId);
  }

  return chain;
}

/**
 * Get all descendant working memories
 * @param {string} workingMemoryId
 * @returns {object[]}
 */
export function getDescendants(workingMemoryId) {
  const memories = loadWorkingMemories();
  const wm = memories.find(w => w.id === workingMemoryId);
  if (!wm || !wm.subtaskIds || wm.subtaskIds.length === 0) return [];

  const descendants = [];
  const queue = [...wm.subtaskIds];

  while (queue.length > 0) {
    const id = queue.shift();
    const child = memories.find(w => w.id === id);
    if (child) {
      descendants.push(formatWorkingMemory(child));
      if (child.subtaskIds) {
        queue.push(...child.subtaskIds);
      }
    }
  }

  return descendants;
}

/**
 * Link a working memory to an episode (session/conversation)
 * @param {string} workingMemoryId
 * @param {string} episodeId
 * @returns {{success: boolean}}
 */
export function linkToEpisode(workingMemoryId, episodeId) {
  const memories = loadWorkingMemories();
  const wm = memories.find(w => w.id === workingMemoryId);

  if (!wm) return { success: false };

  wm.episodeId = episodeId;
  wm.updatedAt = Date.now();
  persistWorkingMemories(memories);

  return { success: true };
}

/**
 * Get working memories linked to a specific episode
 * @param {string} episodeId
 * @returns {object[]}
 */
export function getWorkingMemoriesByEpisode(episodeId) {
  const memories = loadWorkingMemories();
  return memories
    .filter(wm => wm.episodeId === episodeId && wm.status !== WorkingMemoryStatus.CLEARED)
    .map(formatWorkingMemory);
}

/**
 * Check if a working memory has active subtasks
 * @param {string} workingMemoryId
 * @returns {{hasActiveSubtasks: boolean, activeSubtaskCount: number}}
 */
export function hasActiveSubtasks(workingMemoryId) {
  const memories = loadWorkingMemories();
  const wm = memories.find(w => w.id === workingMemoryId);

  if (!wm || !wm.subtaskIds || wm.subtaskIds.length === 0) {
    return { hasActiveSubtasks: false, activeSubtaskCount: 0 };
  }

  const activeSubtasks = wm.subtaskIds
    .map(id => memories.find(w => w.id === id))
    .filter(child => child && child.status === WorkingMemoryStatus.ACTIVE);

  return {
    hasActiveSubtasks: activeSubtasks.length > 0,
    activeSubtaskCount: activeSubtasks.length,
  };
}

/**
 * Get task tree visualization
 * @returns {string}
 */
export function visualizeTaskTree() {
  const { roots, tree } = buildTaskTree();
  const lines = ['Task Hierarchy'];

  function render(wm, indent = 0) {
    const prefix = '  '.repeat(indent);
    const statusIcon = wm.status === WorkingMemoryStatus.ACTIVE ? '●' :
                       wm.status === WorkingMemoryStatus.HELD ? '○' : '✗';
    lines.push(`${prefix}${statusIcon} [${wm.taskId}] ${wm.description}`);
    
    const children = tree.get(wm.taskId) || [];
    for (const child of children) {
      render(child, indent + 1);
    }
  }

  for (const root of roots) {
    render(root);
  }

  return lines.join('\n');
}
