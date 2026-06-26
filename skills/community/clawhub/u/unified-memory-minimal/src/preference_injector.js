/**
 * preference_injector.js — Inject Preferences as Search Context
 * Part of Feature #10: Structured Preference Slots
 * 
 * Loads relevant preferences before search and formats them as context additions.
 */
import { loadPreferences, getPreferencesFlat, getSlotValue, SOURCE_TYPES } from './preference_slots_schema.js';

/**
 * Query context relevance mapping
 * Maps query keywords to relevant preference slots
 */
const QUERY_SLOT_RELEVANCE = {
  // Time-related queries need timezone
  time: ['timezone', 'working_hours'],
  schedule: ['timezone', 'working_hours'],
  meeting: ['timezone', 'working_hours'],
  when: ['timezone', 'working_hours'],
  // Language/communication queries
  language: ['language', 'communication_style'],
  write: ['language', 'communication_style', 'formality_level'],
  explain: ['communication_style', 'response_length'],
  describe: ['communication_style', 'response_length'],
  // Detail/complexity queries
  detail: ['response_length', 'communication_style'],
  brief: ['response_length', 'communication_style'],
  short: ['response_length', 'communication_style'],
  comprehensive: ['response_length'],
  // Tool/platform queries
  tool: ['preferred_tools'],
  platform: ['preferred_tools'],
  use: ['preferred_tools', 'interests'],
  // Goal-oriented queries
  goal: ['goals'],
  achieve: ['goals'],
  finish: ['goals'],
  project: ['goals', 'interests'],
  deadline: ['goals', 'working_hours'],
};

/**
 * Determine which slots are relevant to a query
 */
function getRelevantSlots(query) {
  const q = query.toLowerCase();
  const relevant = new Set();
  
  for (const [keyword, slots] of Object.entries(QUERY_SLOT_RELEVANCE)) {
    if (q.includes(keyword)) {
      slots.forEach(s => relevant.add(s));
    }
  }
  
  // Always include some general slots
  relevant.add('language');
  relevant.add('communication_style');
  
  return Array.from(relevant);
}

/**
 * Format a single preference as context text
 */
function formatSlotContext(slotName, entry) {
  if (entry.value === null || entry.value === undefined) return null;
  
  const def = getSlotDefinition(slotName);
  const confidence = Math.round(entry.confidence * 100);
  const source = entry.source;
  
  if (Array.isArray(entry.value) && entry.value.length === 0) return null;
  
  if (slotName === 'working_hours') {
    const { start, end, days } = entry.value;
    const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const activeDays = Array.isArray(days) ? days.map(d => dayNames[d] || d).join(', ') : ' weekdays';
    return `[Preference] Working hours: ${start}–${end} on ${activeDays} (confidence: ${confidence}%, source: ${source})`;
  }
  
  if (Array.isArray(entry.value)) {
    if (entry.value.length === 0) return null;
    return `[Preference] ${slotName}: ${entry.value.slice(0, 5).join(', ')} (confidence: ${confidence}%, source: ${source})`;
  }
  
  return `[Preference] ${slotName}: ${entry.value} (confidence: ${confidence}%, source: ${source})`;
}

/**
 * Get slot definition by name
 */
function getSlotDefinition(slotName) {
  const defs = {
    communication_style: { options: ['concise', 'balanced', 'detailed', 'verbose'] },
    language: { options: ['zh', 'en', 'zh-CN', 'en-US', 'bilingual'] },
    timezone: {},
    response_length: { options: ['short', 'medium', 'long', 'comprehensive'] },
    working_hours: {},
    interests: {},
    goals: {},
    constraints: {},
    preferred_tools: {},
    notification_preference: { options: ['silent', 'minimal', 'normal', 'detailed'] },
    formality_level: { options: ['formal', 'semi-formal', 'casual', 'friendly'] },
  };
  return defs[slotName] || {};
}

/**
 * Main injection function: load relevant preferences for a query
 * @param {string} query - The search query
 * @returns {{ preferences: Object, contextAdditions: string[], relevantSlots: string[] }}
 */
export function injectPreferences(query) {
  const preferences = loadPreferences();
  const relevantSlots = getRelevantSlots(query);
  const contextAdditions = [];
  
  const relevantPrefs = {};
  
  for (const slotName of relevantSlots) {
    const entry = preferences[slotName];
    if (!entry) continue;
    
    const value = entry.value;
    if (value === null || value === undefined) continue;
    if (Array.isArray(value) && value.length === 0) continue;
    
    relevantPrefs[slotName] = entry;
    
    const contextText = formatSlotContext(slotName, entry);
    if (contextText) {
      contextAdditions.push(contextText);
    }
  }
  
  return {
    preferences: relevantPrefs,
    contextAdditions,
    relevantSlots,
    allPreferences: getPreferencesFlat(preferences),
  };
}

/**
 * Build a full context string from all preferences
 */
export function buildFullContextString(preferences) {
  const lines = [];
  lines.push('## User Preferences');
  
  const prioritySlots = ['language', 'communication_style', 'timezone', 'response_length', 'formality_level'];
  
  for (const slotName of prioritySlots) {
    const entry = preferences[slotName];
    if (entry && entry.value !== null && entry.value !== undefined) {
      const ctx = formatSlotContext(slotName, entry);
      if (ctx) lines.push(ctx.replace(/^\[Preference\]\s*/, ''));
    }
  }
  
  // Add arrays
  const arraySlots = ['interests', 'goals', 'constraints', 'preferred_tools'];
  for (const slotName of arraySlots) {
    const entry = preferences[slotName];
    if (entry && Array.isArray(entry.value) && entry.value.length > 0) {
      lines.push(`${slotName}: ${entry.value.slice(0, 5).join(', ')}`);
    }
  }
  
  if (lines.length === 1) return '';
  return lines.join('\n');
}

/**
 * Calculate a preference-based boost multiplier for search results
 */
export function getPreferenceBoostFactor(preferences, category) {
  let boost = 1.0;
  
  const language = preferences.language?.value;
  const style = preferences.communication_style?.value;
  
  // Language alignment
  if (language === 'zh' && category === 'fact') boost *= 1.1;
  if (language === 'en' && category === 'fact') boost *= 1.05;
  
  // Style alignment
  if (style === 'concise' && category === 'fact') boost *= 1.1;
  if (style === 'detailed' && category === 'learning') boost *= 1.1;
  
  return Math.min(boost, 1.5);
}

export default {
  injectPreferences,
  buildFullContextString,
  getPreferenceBoostFactor,
  getRelevantSlots,
};
