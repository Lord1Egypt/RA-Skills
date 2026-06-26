/**
 * preference_slots_schema.js — Preference Slots Schema Definition
 * Part of Feature #10: Structured Preference Slots for unified-memory
 * 
 * Defines standard preference slots with typed schemas, confidence scoring,
 * and source attribution (explicit/inferred/historical).
 */
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WORKSPACE = process.env.OPENCLAW_WORKSPACE_DIR ?? join(process.env.HOME ?? '/root', '.openclaw', 'workspace');
const PREFERENCES_FILE = join(WORKSPACE, 'memory', 'preferences.json');

/**
 * Standard slot definitions with type, default, and validation
 */
export const SLOT_DEFINITIONS = {
  communication_style: {
    type: 'string',
    default: 'balanced',
    options: ['concise', 'balanced', 'detailed', 'verbose'],
    description: 'How verbose and structured should responses be',
  },
  language: {
    type: 'string',
    default: 'zh',
    options: ['zh', 'en', 'zh-CN', 'en-US', 'bilingual'],
    description: 'Preferred language for responses',
  },
  timezone: {
    type: 'string',
    default: 'Asia/Shanghai',
    description: 'User timezone for time-aware features',
  },
  response_length: {
    type: 'string',
    default: 'medium',
    options: ['short', 'medium', 'long', 'comprehensive'],
    description: 'Preferred response length',
  },
  working_hours: {
    type: 'object',
    default: { start: '09:00', end: '18:00', days: [1, 2, 3, 4, 5] },
    description: 'User working hours (24h format, 0=Sunday)',
  },
  interests: {
    type: 'array',
    default: [],
    itemType: 'string',
    description: 'User interest topics',
  },
  goals: {
    type: 'array',
    default: [],
    itemType: 'string',
    description: 'User goals and objectives',
  },
  constraints: {
    type: 'array',
    default: [],
    itemType: 'string',
    description: 'User constraints and limitations',
  },
  preferred_tools: {
    type: 'array',
    default: [],
    itemType: 'string',
    description: 'Preferred tools and platforms',
  },
  notification_preference: {
    type: 'string',
    default: 'normal',
    options: ['silent', 'minimal', 'normal', 'detailed'],
    description: 'How much notification detail is preferred',
  },
  formality_level: {
    type: 'string',
    default: 'semi-formal',
    options: ['formal', 'semi-formal', 'casual', 'friendly'],
    description: 'Formality level of communication',
  },
};

/**
 * Source types for slot attribution
 */
export const SOURCE_TYPES = {
  EXPLICIT: 'explicit',      // User directly stated
  INFERRED: 'inferred',      // Derived from behavior patterns
  HISTORICAL: 'historical',  // From past memory content
};

/**
 * Create an empty slot entry with metadata
 */
export function createSlotEntry(value, source = SOURCE_TYPES.INFERRED, confidence = 0.5) {
  return {
    value,
    confidence: Math.min(1, Math.max(0, confidence)),
    source,
    lastUpdated: Date.now(),
  };
}

/**
 * Load all preferences from disk
 */
export function loadPreferences() {
  if (!existsSync(PREFERENCES_FILE)) {
    const defaults = getDefaultPreferences();
    persistPreferences(defaults);
    return defaults;
  }
  try {
    const data = JSON.parse(readFileSync(PREFERENCES_FILE, 'utf8'));
    return validateAndMerge(data);
  } catch (err) {
    console.error('[preference_slots_schema] Load error:', err.message);
    return getDefaultPreferences();
  }
}

/**
 * Validate and merge loaded data with schema defaults
 */
export function validateAndMerge(data) {
  const defaults = getDefaultPreferences();
  const validated = {};
  
  for (const [slotName, def] of Object.entries(SLOT_DEFINITIONS)) {
    if (data[slotName] !== undefined) {
      validated[slotName] = {
        ...createSlotEntry(def.default),
        ...data[slotName],
      };
      // Type coercion
      if (def.type === 'array' && !Array.isArray(validated[slotName].value)) {
        validated[slotName].value = def.default;
      }
    } else {
      validated[slotName] = createSlotEntry(def.default, SOURCE_TYPES.HISTORICAL, 0.5);
    }
  }
  return validated;
}

/**
 * Get default preferences from slot definitions
 */
export function getDefaultPreferences() {
  const prefs = {};
  for (const [slotName, def] of Object.entries(SLOT_DEFINITIONS)) {
    prefs[slotName] = createSlotEntry(def.default, SOURCE_TYPES.HISTORICAL, 0.5);
  }
  return prefs;
}

/**
 * Persist preferences to disk
 */
export function persistPreferences(prefs) {
  try {
    const dir = join(WORKSPACE, 'memory');
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
    }
    writeFileSync(PREFERENCES_FILE, JSON.stringify(prefs, null, 2), 'utf8');
  } catch (err) {
    console.error('[preference_slots_schema] Persist error:', err.message);
  }
}

/**
 * Get a single slot value (unpacked from slot entry)
 */
export function getSlotValue(preferences, slotName) {
  return preferences[slotName]?.value ?? null;
}

/**
 * Get slot entry with full metadata
 */
export function getSlotEntry(preferences, slotName) {
  return preferences[slotName] ?? null;
}

/**
 * Update a single slot
 */
export function updateSlotValue(preferences, slotName, value, source = SOURCE_TYPES.EXPLICIT, confidence = 0.9) {
  const def = SLOT_DEFINITIONS[slotName];
  if (!def) throw new Error(`Unknown slot: ${slotName}`);
  
  // Validate value
  if (def.options && !def.options.includes(value)) {
    throw new Error(`Invalid value for ${slotName}: ${value}. Options: ${def.options.join(', ')}`);
  }
  
  preferences[slotName] = createSlotEntry(value, source, confidence);
  return preferences[slotName];
}

/**
 * Get all slot names
 */
export function getSlotNames() {
  return Object.keys(SLOT_DEFINITIONS);
}

/**
 * Get slot definition
 */
export function getSlotDefinition(slotName) {
  return SLOT_DEFINITIONS[slotName] ?? null;
}

/**
 * Get preferences as simple key-value map (for injection)
 */
export function getPreferencesFlat(preferences) {
  const flat = {};
  for (const [slotName, entry] of Object.entries(preferences)) {
    flat[slotName] = entry.value;
  }
  return flat;
}

export default {
  SLOT_DEFINITIONS,
  SOURCE_TYPES,
  createSlotEntry,
  loadPreferences,
  validateAndMerge,
  getDefaultPreferences,
  persistPreferences,
  getSlotValue,
  getSlotEntry,
  updateSlotValue,
  getSlotNames,
  getSlotDefinition,
  getPreferencesFlat,
};
