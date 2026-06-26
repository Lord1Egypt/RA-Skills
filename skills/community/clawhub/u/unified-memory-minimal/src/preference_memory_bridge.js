/**
 * preference_memory_bridge.js — Bidirectional Sync Between Slots and PREFERENCE Memories
 * Part of Feature #10: Structured Preference Slots
 * 
 * Syncs preference slots to/from PREFERENCE category memories for persistence
 * and cross-feature compatibility with the existing memory system.
 */
import { loadPreferences, getSlotValue, updateSlotValue, createSlotEntry, SOURCE_TYPES, persistPreferences } from './preference_slots_schema.js';
import { getAllMemories, addMemory, updateMemory, deleteMemory } from './storage.js';

/**
 * Memory type constant for preference memories
 */
const PREFERENCE_MEMORY_TYPE = 'preference';

/**
 * Extract slot name from memory ID
 */
function memoryIdToSlot(memoryId) {
  return memoryId.replace(/^preference_/, '');
}

/**
 * Create memory ID from slot name
 */
function slotToMemoryId(slotName) {
  return `preference_${slotName}`;
}

/**
 * Convert a slot entry to a memory object
 */
function slotToMemory(slotName, entry) {
  return {
    id: slotToMemoryId(slotName),
    text: formatSlotAsMemoryText(slotName, entry),
    category: PREFERENCE_MEMORY_TYPE,
    importance: entry.confidence,
    tags: [entry.source, slotName],
    created_at: entry.lastUpdated,
  };
}

/**
 * Format slot entry as searchable memory text
 */
function formatSlotAsMemoryText(slotName, entry) {
  const value = entry.value;
  
  if (Array.isArray(value)) {
    return `Preference ${slotName}: ${value.join(', ')} (source: ${entry.source}, confidence: ${entry.confidence})`;
  }
  
  if (typeof value === 'object' && value !== null) {
    return `Preference ${slotName}: ${JSON.stringify(value)} (source: ${entry.source}, confidence: ${entry.confidence})`;
  }
  
  return `Preference ${slotName}: ${value} (source: ${entry.source}, confidence: ${entry.confidence})`;
}

/**
 * Parse memory text back to slot entry
 */
function memoryTextToEntry(text) {
  // Pattern: "Preference slotname: value (source: x, confidence: 0.x)"
  const match = text.match(/^Preference (\w+): (.+?) \(source: (\w+), confidence: ([\d.]+)\)$/);
  if (!match) return null;
  
  const [, slotName, valueStr, source, confidenceStr] = match;
  let value = valueStr;
  
  // Try to parse as JSON array/object
  if (valueStr.startsWith('[') || valueStr.startsWith('{')) {
    try { value = JSON.parse(valueStr); } catch { /* use raw string */ }
  }
  
  return createSlotEntry(value, source, parseFloat(confidenceStr));
}

/**
 * Push all current slot values as PREFERENCE memories
 */
export async function syncSlotsToMemories() {
  const preferences = loadPreferences();
  const results = { synced: 0, failed: 0 };
  
  for (const [slotName, entry] of Object.entries(preferences)) {
    try {
      const memory = slotToMemory(slotName, entry);
      const existing = getAllMemories().find(m => m.id === memory.id);
      
      if (existing) {
        // Update existing
        const { updateMemory: um } = await import('./storage.js');
        // We need the storage module's functions - check if update supports partial
        existing.text = memory.text;
        existing.importance = memory.importance;
        existing.tags = memory.tags;
        existing.updated_at = Date.now();
        um(existing); // storage.updateMemory might need full object
      } else {
        await addMemory(memory);
      }
      results.synced++;
    } catch (err) {
      console.error(`[bridge] Failed to sync slot ${slotName}:`, err.message);
      results.failed++;
    }
  }
  
  return results;
}

/**
 * Pull PREFERENCE memories and update slots
 */
export async function syncMemoriesToSlots() {
  const allMemories = getAllMemories();
  const prefMemories = allMemories.filter(m => m.category === PREFERENCE_MEMORY_TYPE);
  
  const preferences = loadPreferences();
  let updated = 0;
  
  for (const mem of prefMemories) {
    const slotName = memoryIdToSlot(mem.id);
    if (!slotName) continue;
    
    const entry = memoryTextToEntry(mem.text);
    if (!entry) continue;
    
    // Only update if newer (higher lastUpdated)
    const existing = preferences[slotName];
    if (!existing || entry.lastUpdated > existing.lastUpdated) {
      preferences[slotName] = entry;
      updated++;
    }
  }
  
  if (updated > 0) {
    persistPreferences(preferences);
  }
  
  return { updated, total: prefMemories.length };
}

/**
 * Bidirectional sync: merge both directions, highest confidence wins
 */
export async function bidirectionalSync() {
  // First pull from memories to detect any newer values
  const pullResult = await syncMemoriesToSlots();
  
  // Then push current state back to memories
  const pushResult = await syncSlotsToMemories();
  
  return {
    pulled: pullResult,
    pushed: pushResult,
  };
}

/**
 * Get a preference as a memory-compatible object
 */
export function getPreferenceAsMemory(slotName) {
  const preferences = loadPreferences();
  const entry = preferences[slotName];
  if (!entry) return null;
  return slotToMemory(slotName, entry);
}

/**
 * Check if a memory is a preference memory
 */
export function isPreferenceMemory(memory) {
  return memory?.category === PREFERENCE_MEMORY_TYPE || memory?.id?.startsWith('preference_');
}

/**
 * Export all preferences as memories array
 */
export function exportAllAsMemories() {
  const preferences = loadPreferences();
  const memories = [];
  
  for (const [slotName, entry] of Object.entries(preferences)) {
    memories.push(slotToMemory(slotName, entry));
  }
  
  return memories;
}

/**
 * Get sync status between slots and memories
 */
export function getSyncStatus() {
  const preferences = loadPreferences();
  const allMemories = getAllMemories();
  const prefMemories = allMemories.filter(m => isPreferenceMemory(m));
  
  const slotNames = Object.keys(preferences);
  const memoryIds = new Set(prefMemories.map(m => m.id));
  
  const inSync = slotNames.filter(s => memoryIds.has(slotToMemoryId(s))).length;
  const missingInMemory = slotNames.filter(s => !memoryIds.has(slotToMemoryId(s))).length;
  const orphanedInMemory = prefMemories.filter(m => !slotNames.includes(memoryIdToSlot(m.id))).length;
  
  return {
    totalSlots: slotNames.length,
    totalPrefMemories: prefMemories.length,
    inSync,
    missingInMemory,
    orphanedInMemory,
    needsSync: missingInMemory > 0 || orphanedInMemory > 0,
  };
}

export default {
  syncSlotsToMemories,
  syncMemoriesToSlots,
  bidirectionalSync,
  getPreferenceAsMemory,
  isPreferenceMemory,
  exportAllAsMemories,
  getSyncStatus,
  slotToMemoryId,
  memoryIdToSlot,
};
