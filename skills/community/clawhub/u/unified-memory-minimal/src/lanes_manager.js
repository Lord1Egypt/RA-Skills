/**
 * lanes_manager.js - Parallel Memory Lanes
 *
 * Multiple parallel "swim lanes" for different memory contexts.
 * Inspired by Smart Memory's memory lanes concept.
 *
 * Lanes:
 *   - primary: Main conversation lane
 *   - task: Current task focus
 *   - background: Long-running investigations
 *   - archive: Completed/archived threads
 *   - Custom lanes are configurable
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = process.env.HOME || '/root';
const MEMORY_DIR = join(HOME, '.openclaw', 'workspace', 'memory');
const LANES_FILE = join(MEMORY_DIR, 'lanes.json');

// Ensure memory directory exists
if (!existsSync(MEMORY_DIR)) {
  mkdirSync(MEMORY_DIR, { recursive: true });
}

// ============================================================================
// Types
// ============================================================================

/**
 * @typedef {Object} Lane
 * @property {string} name - Lane name (unique identifier)
 * @property {string} description - Lane description
 * @property {boolean} isActive - Whether this is the current active lane
 * @property {number} memoryCount - Number of memories in this lane
 * @property {string} createdAt - ISO timestamp of creation
 * @property {string|null} archivedAt - ISO timestamp when archived, null if not archived
 */

/**
 * @typedef {Object} Memory
 * @property {string} id - Memory unique ID
 * @property {string} text - Memory content
 * @property {string} lane - Lane this memory belongs to
 * @property {string} category - Memory category
 * @property {number} importance - Importance score 0-1
 * @property {string[]} tags - Tags
 * @property {string} created_at - ISO timestamp
 */

// ============================================================================
// Default Lanes
// ============================================================================

const DEFAULT_LANES = [
  {
    name: 'primary',
    description: 'Main conversation lane',
    isActive: true,
    memoryCount: 0,
    createdAt: new Date().toISOString(),
    archivedAt: null,
  },
  {
    name: 'task',
    description: 'Current task focus',
    isActive: false,
    memoryCount: 0,
    createdAt: new Date().toISOString(),
    archivedAt: null,
  },
  {
    name: 'background',
    description: 'Long-running investigations',
    isActive: false,
    memoryCount: 0,
    createdAt: new Date().toISOString(),
    archivedAt: null,
  },
  {
    name: 'archive',
    description: 'Completed/archived threads',
    isActive: false,
    memoryCount: 0,
    createdAt: new Date().toISOString(),
    archivedAt: null,
  },
];

// ============================================================================
// Storage Helpers
// ============================================================================

/**
 * Load lanes data from lanes.json
 * @returns {object}
 */
function loadLanesData() {
  try {
    if (!existsSync(LANES_FILE)) {
      return getDefaultLanesData();
    }
    const content = readFileSync(LANES_FILE, 'utf-8');
    const data = JSON.parse(content);
    return data;
  } catch (err) {
    console.error(`[lanes] Failed to load: ${err.message}`);
    return getDefaultLanesData();
  }
}

/**
 * Save lanes data to lanes.json
 * @param {object} data
 */
function saveLanesData(data) {
  try {
    writeFileSync(LANES_FILE, JSON.stringify(data, null, 2), 'utf-8');
  } catch (err) {
    console.error(`[lanes] Failed to save: ${err.message}`);
  }
}

/**
 * Get default lanes data structure
 * @returns {object}
 */
function getDefaultLanesData() {
  return {
    lanes: DEFAULT_LANES.map(l => ({ ...l })),
    memories: {},  // memoryId -> { lane, memoryId, addedAt }
    version: '1.0.0',
    updatedAt: new Date().toISOString(),
  };
}

/**
 * Recalculate memoryCount for all lanes based on memories map
 * @param {object} data
 */
function recalcMemoryCounts(data) {
  const counts = {};
  for (const [memId, memInfo] of Object.entries(data.memories || {})) {
    const lane = memInfo.lane;
    counts[lane] = (counts[lane] || 0) + 1;
  }
  for (const lane of data.lanes) {
    lane.memoryCount = counts[lane.name] || 0;
  }
}

// ============================================================================
// Lane Operations
// ============================================================================

/**
 * Create a new lane
 * @param {string} name - Lane name
 * @param {string} [description] - Lane description
 * @returns {Promise<Lane>}
 */
export async function createLane(name, description = '') {
  const data = loadLanesData();

  // Check if lane already exists
  const existing = data.lanes.find(l => l.name === name);
  if (existing) {
    throw new Error(`Lane '${name}' already exists`);
  }

  const lane = {
    name,
    description,
    isActive: false,
    memoryCount: 0,
    createdAt: new Date().toISOString(),
    archivedAt: null,
  };

  data.lanes.push(lane);
  data.updatedAt = new Date().toISOString();
  saveLanesData(data);

  return lane;
}

/**
 * Switch active lane
 * @param {string} laneName - Lane to switch to
 * @returns {Promise<void>}
 */
export async function switchLane(laneName) {
  const data = loadLanesData();

  const targetLane = data.lanes.find(l => l.name === laneName);
  if (!targetLane) {
    throw new Error(`Lane '${laneName}' not found`);
  }

  if (targetLane.archivedAt) {
    throw new Error(`Cannot switch to archived lane '${laneName}'`);
  }

  // Deactivate all lanes, activate target
  for (const lane of data.lanes) {
    lane.isActive = lane.name === laneName;
  }

  data.updatedAt = new Date().toISOString();
  saveLanesData(data);
}

/**
 * Get the current active lane
 * @returns {Promise<Lane|null>}
 */
export async function getCurrentLane() {
  const data = loadLanesData();
  recalcMemoryCounts(data);
  const active = data.lanes.find(l => l.isActive) || null;
  return active;
}

/**
 * List all lanes
 * @returns {Promise<Lane[]>}
 */
export async function listLanes() {
  const data = loadLanesData();
  recalcMemoryCounts(data);
  return data.lanes;
}

/**
 * Move a memory to a different lane
 * @param {string} memoryId - Memory ID to move
 * @param {string} laneName - Target lane name
 * @returns {Promise<void>}
 */
export async function moveToLane(memoryId, laneName) {
  const data = loadLanesData();

  // Verify target lane exists and is not archived
  const targetLane = data.lanes.find(l => l.name === laneName);
  if (!targetLane) {
    throw new Error(`Lane '${laneName}' not found`);
  }
  if (targetLane.archivedAt) {
    throw new Error(`Cannot move memory to archived lane '${laneName}'`);
  }

  // Check if memory exists in memories map
  const memInfo = data.memories[memoryId];
  if (!memInfo) {
    throw new Error(`Memory '${memoryId}' not found in any lane`);
  }

  // Update the memory's lane
  const oldLane = memInfo.lane;
  memInfo.lane = laneName;
  memInfo.movedAt = new Date().toISOString();

  data.updatedAt = new Date().toISOString();
  saveLanesData(data);
}

/**
 * Archive a lane and all its contents
 * @param {string} laneName - Lane to archive
 * @returns {Promise<void>}
 */
export async function archiveLane(laneName) {
  const data = loadLanesData();

  const lane = data.lanes.find(l => l.name === laneName);
  if (!lane) {
    throw new Error(`Lane '${laneName}' not found`);
  }

  if (lane.name === 'primary') {
    throw new Error(`Cannot archive the primary lane`);
  }

  if (lane.archivedAt) {
    throw new Error(`Lane '${laneName}' is already archived`);
  }

  // Archive the lane
  lane.archivedAt = new Date().toISOString();
  lane.isActive = false;

  // If this was the active lane, switch to primary
  if (lane.isActive) {
    const primaryLane = data.lanes.find(l => l.name === 'primary');
    if (primaryLane) {
      for (const l of data.lanes) {
        l.isActive = l.name === 'primary';
      }
    }
  }

  data.updatedAt = new Date().toISOString();
  saveLanesData(data);
}

/**
 * Get memories in a specific lane
 * @param {string} laneName - Lane name
 * @returns {Promise<Memory[]>}
 */
export async function getLaneMemories(laneName) {
  const data = loadLanesData();

  const lane = data.lanes.find(l => l.name === laneName);
  if (!lane) {
    throw new Error(`Lane '${laneName}' not found`);
  }

  // Get memory IDs in this lane
  const memoryIds = [];
  for (const [memId, memInfo] of Object.entries(data.memories || {})) {
    if (memInfo.lane === laneName) {
      memoryIds.push(memId);
    }
  }

  return memoryIds;
}

// ============================================================================
// Memory-Lane Association (for use by storage.js / other modules)
// ============================================================================

/**
 * Add a memory to a lane (called when storing new memory)
 * @param {string} memoryId - Memory ID
 * @param {string} [laneName] - Lane name (defaults to current active lane)
 * @returns {Promise<void>}
 */
export async function addMemoryToLane(memoryId, laneName = null) {
  const data = loadLanesData();

  // Default to current active lane if not specified
  if (!laneName) {
    const active = data.lanes.find(l => l.isActive);
    laneName = active ? active.name : 'primary';
  }

  // Verify lane exists
  const lane = data.lanes.find(l => l.name === laneName);
  if (!lane) {
    throw new Error(`Lane '${laneName}' not found`);
  }

  // Add memory to lane
  data.memories[memoryId] = {
    lane: laneName,
    memoryId,
    addedAt: new Date().toISOString(),
  };

  data.updatedAt = new Date().toISOString();
  saveLanesData(data);
}

/**
 * Remove a memory from its lane (called when deleting memory)
 * @param {string} memoryId - Memory ID to remove
 * @returns {Promise<void>}
 */
export async function removeMemoryFromLane(memoryId) {
  const data = loadLanesData();

  if (data.memories[memoryId]) {
    delete data.memories[memoryId];
    data.updatedAt = new Date().toISOString();
    saveLanesData(data);
  }
}

/**
 * Get which lane a memory belongs to
 * @param {string} memoryId - Memory ID
 * @returns {Promise<string|null>} Lane name or null if not found
 */
export async function getMemoryLane(memoryId) {
  const data = loadLanesData();
  const memInfo = data.memories[memoryId];
  return memInfo ? memInfo.lane : null;
}

/**
 * Get the lane assignment data (for inspection/debugging)
 * @returns {Promise<object>}
 */
export async function getLanesData() {
  return loadLanesData();
}

// ============================================================================
// MCP Tool Handler
// ============================================================================

/**
 * Handle memory_lanes MCP tool calls
 * @param {object} args
 * @param {string} [args.action]
 * @param {string} [args.name]
 * @param {string} [args.description]
 * @param {string} [args.lane_name]
 * @param {string} [args.memory_id]
 * @returns {Promise<{content: Array<{type: string, text: string}>, isError?: boolean}>}
 */
export async function memoryLanesTool(args) {
  const { action } = args;

  try {
    switch (action) {
      case 'create': {
        if (!args.name) {
          return { content: [{ type: 'text', text: 'Error: name is required' }], isError: true };
        }
        const lane = await createLane(args.name, args.description || '');
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({ success: true, lane }),
          }],
        };
      }

      case 'switch': {
        const laneName = args.name || args.lane_name;
        if (!laneName) {
          return { content: [{ type: 'text', text: 'Error: lane_name is required' }], isError: true };
        }
        await switchLane(laneName);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({ success: true, message: `Switched to lane '${laneName}'` }),
          }],
        };
      }

      case 'current': {
        const lane = await getCurrentLane();
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({ current: lane }),
          }],
        };
      }

      case 'list': {
        const lanes = await listLanes();
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({ count: lanes.length, lanes }),
          }],
        };
      }

      case 'move': {
        if (!args.memory_id) {
          return { content: [{ type: 'text', text: 'Error: memory_id is required' }], isError: true };
        }
        const moveToLaneName = args.name || args.lane_name;
        if (!moveToLaneName) {
          return { content: [{ type: 'text', text: 'Error: lane_name is required' }], isError: true };
        }
        await moveToLane(args.memory_id, moveToLaneName);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({ success: true, message: `Memory '${args.memory_id}' moved to lane '${moveToLaneName}'` }),
          }],
        };
      }

      case 'archive': {
        const archiveLaneName = args.name || args.lane_name;
        if (!archiveLaneName) {
          return { content: [{ type: 'text', text: 'Error: lane_name is required' }], isError: true };
        }
        await archiveLane(archiveLaneName);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({ success: true, message: `Lane '${archiveLaneName}' archived` }),
          }],
        };
      }

      case 'memories': {
        const memLaneName = args.name || args.lane_name;
        if (!memLaneName) {
          return { content: [{ type: 'text', text: 'Error: lane_name is required' }], isError: true };
        }
        const memoryIds = await getLaneMemories(memLaneName);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({ lane: memLaneName, count: memoryIds.length, memoryIds }),
          }],
        };
      }

      case 'data': {
        // Debug: return raw lanes data
        const data = await getLanesData();
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(data, null, 2),
          }],
        };
      }

      default:
        return {
          content: [{ type: 'text', text: `Error: Unknown action '${action}'. Valid actions: create, switch, current, list, move, archive, memories, data` }],
          isError: true,
        };
    }
  } catch (err) {
    return { content: [{ type: 'text', text: `Lanes error: ${err.message}` }], isError: true };
  }
}

export default { memoryLanesTool };
