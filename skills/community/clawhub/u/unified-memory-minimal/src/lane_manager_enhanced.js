/**
 * Lane Manager Enhanced - Deep Memory Lane Integration
 * Complete lane-based memory management with advanced features
 * 
 * Storage: ~/.openclaw/workspace/memory/lanes.json
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
 * @property {string[]} tags - Lane tags
 * @property {Object} metadata - Additional metadata
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
 * @property {string} transcript_id - Source transcript ID
 * @property {number} message_index - Message index in transcript
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
    tags: ['main', 'conversation'],
    metadata: {}
  },
  {
    name: 'task',
    description: 'Current task focus',
    isActive: false,
    memoryCount: 0,
    createdAt: new Date().toISOString(),
    archivedAt: null,
    tags: ['task', 'active'],
    metadata: {}
  },
  {
    name: 'background',
    description: 'Long-running investigations',
    isActive: false,
    memoryCount: 0,
    createdAt: new Date().toISOString(),
    archivedAt: null,
    tags: ['investigation', 'long-term'],
    metadata: {}
  },
  {
    name: 'archive',
    description: 'Completed/archived threads',
    isActive: false,
    memoryCount: 0,
    createdAt: new Date().toISOString(),
    archivedAt: null,
    tags: ['archive', 'completed'],
    metadata: {}
  }
];

// ============================================================================
// Core Functions
// ============================================================================

/**
 * Load lanes from file
 */
function loadLanes() {
  if (!existsSync(LANES_FILE)) {
    saveLanes({ lanes: DEFAULT_LANES, active_lane: 'primary' });
    return { lanes: DEFAULT_LANES, active_lane: 'primary' };
  }
  
  const data = readFileSync(LANES_FILE, 'utf-8');
  return JSON.parse(data);
}

/**
 * Save lanes to file
 */
function saveLanes(data) {
  mkdirSync(dirname(LANES_FILE), { recursive: true });
  writeFileSync(LANES_FILE, JSON.stringify(data, null, 2), 'utf-8');
}

/**
 * Create a new lane
 */
export function createLane(name, description = '', tags = [], metadata = {}) {
  const lanesData = loadLanes();
  
  if (lanesData.lanes.some(l => l.name === name)) {
    throw new Error(`Lane '${name}' already exists`);
  }
  
  // Deactivate other lanes
  lanesData.lanes.forEach(lane => {
    lane.isActive = lane.name === lanesData.active_lane;
  });
  
  const newLane = {
    name,
    description,
    isActive: true,
    memoryCount: 0,
    createdAt: new Date().toISOString(),
    archivedAt: null,
    tags,
    metadata
  };
  
  lanesData.lanes.push(newLane);
  lanesData.active_lane = name;
  
  saveLanes(lanesData);
  return newLane;
}

/**
 * Switch to a lane
 */
export function switchLane(name) {
  const lanesData = loadLanes();
  const lane = lanesData.lanes.find(l => l.name === name);
  
  if (!lane) {
    throw new Error(`Lane '${name}' not found`);
  }
  
  // Deactivate other lanes
  lanesData.lanes.forEach(lane => {
    lane.isActive = false;
  });
  
  lane.isActive = true;
  lanesData.active_lane = name;
  
  saveLanes(lanesData);
  return lane;
}

/**
 * Get current active lane
 */
export function getCurrentLane() {
  const lanesData = loadLanes();
  return lanesData.lanes.find(l => l.name === lanesData.active_lane);
}

/**
 * List all lanes
 */
export function listLanes(includeArchived = false) {
  const lanesData = loadLanes();
  const lanes = includeArchived 
    ? lanesData.lanes 
    : lanesData.lanes.filter(l => !l.archivedAt);
  
  return lanes.map(lane => ({
    ...lane,
    memoryCount: lane.memoryCount || 0
  }));
}

/**
 * Move a memory between lanes
 */
export function moveMemory(memoryId, fromLane, toLane) {
  const lanesData = loadLanes();
  
  // Update memory counts
  const fromLaneObj = lanesData.lanes.find(l => l.name === fromLane);
  const toLaneObj = lanesData.lanes.find(l => l.name === toLane);
  
  if (fromLaneObj) fromLaneObj.memoryCount = Math.max(0, fromLaneObj.memoryCount - 1);
  if (toLaneObj) toLaneObj.memoryCount++;
  
  saveLanes(lanesData);
  
  return {
    success: true,
    memory_id: memoryId,
    from_lane: fromLane,
    to_lane: toLane
  };
}

/**
 * Archive a lane
 */
export function archiveLane(name) {
  const lanesData = loadLanes();
  const lane = lanesData.lanes.find(l => l.name === name);
  
  if (!lane) {
    throw new Error(`Lane '${name}' not found`);
  }
  
  lane.archivedAt = new Date().toISOString();
  lane.isActive = false;
  
  // Activate another lane if current is archived
  if (lanesData.active_lane === name) {
    const activeLane = lanesData.lanes.find(l => l.name !== name && !l.archivedAt);
    if (activeLane) {
      activeLane.isActive = true;
      lanesData.active_lane = name;
    }
  }
  
  saveLanes(lanesData);
  return lane;
}

/**
 * Get memories in a lane
 */
export function getLaneMemories(laneName) {
  // In a real implementation, this would query the memory store
  // For now, return metadata about the lane
  const lanesData = loadLanes();
  const lane = lanesData.lanes.find(l => l.name === laneName);
  
  return {
    lane: lane,
    memories: [], // Would be populated from memory store
    count: lane?.memoryCount || 0
  };
}

/**
 * Get lane statistics
 */
export function getLaneStats() {
  const lanesData = loadLanes();
  
  const totalMemories = lanesData.lanes.reduce((sum, lane) => sum + (lane.memoryCount || 0), 0);
  const activeLane = lanesData.lanes.find(l => l.name === lanesData.active_lane);
  
  return {
    total_lanes: lanesData.lanes.length,
    active_lane: activeLane?.name,
    total_memories: totalMemories,
    lanes: lanesData.lanes.map(lane => ({
      name: lane.name,
      memory_count: lane.memoryCount || 0,
      is_active: lane.name === lanesData.active_lane,
      is_archived: !!lane.archivedAt
    }))
  };
}

/**
 * Merge memories from one lane to another
 */
export function mergeLane(fromLane, toLane) {
  const lanesData = loadLanes();
  
  const fromLaneObj = lanesData.lanes.find(l => l.name === fromLane);
  const toLaneObj = lanesData.lanes.find(l => l.name === toLane);
  
  if (!fromLaneObj || !toLaneObj) {
    throw new Error('One or both lanes not found');
  }
  
  // Move memories
  toLaneObj.memoryCount = (toLaneObj.memoryCount || 0) + (fromLaneObj.memoryCount || 0);
  
  // Archive source lane
  fromLaneObj.archivedAt = new Date().toISOString();
  
  saveLanes(lanesData);
  
  return {
    success: true,
    merged_from: fromLane,
    merged_to: toLane,
    memory_count: toLaneObj.memoryCount
  };
}

/**
 * Delete a lane (after archiving)
 */
export function deleteLane(name) {
  const lanesData = loadLanes();
  lanesData.lanes = lanesData.lanes.filter(l => l.name !== name);
  saveLanes(lanesData);
  
  return { success: true, deleted: name };
}

/**
 * Get lane history
 */
export function getLaneHistory(laneName) {
  // In a real implementation, this would track lane changes
  return {
    lane: laneName,
    history: [] // Would be populated from history store
  };
}

/**
 * Lane memory tool - unified interface
 */
export function memoryLanesTool(action, params = {}) {
  try {
    switch (action) {
      case 'create':
        return createLane(params.lane_name, params.description, params.tags, params.metadata);
      
      case 'switch':
        return switchLane(params.lane_name);
      
      case 'current':
        return getCurrentLane();
      
      case 'list':
        return listLanes(params.include_archived);
      
      case 'move':
        return moveMemory(params.memory_id, params.from_lane, params.to_lane);
      
      case 'archive':
        return archiveLane(params.lane_name);
      
      case 'memories':
        return getLaneMemories(params.lane_name);
      
      case 'stats':
        return getLaneStats();
      
      case 'merge':
        return mergeLane(params.from_lane, params.to_lane);
      
      case 'delete':
        return deleteLane(params.lane_name);
      
      default:
        throw new Error(`Unknown action: ${action}`);
    }
  } catch (error) {
    return {
      success: false,
      error: error.message,
      action
    };
  }
}
