/**
 * preference_tools.js — MCP Tools for Preference Slots
 * Part of Feature #10: Structured Preference Slots
 * 
 * Implements MCP tools:
 * - memory_preference_get: Get one or all preferences
 * - memory_preference_set: Set a preference value (with history tracking)
 * - memory_preference_infer: Infer preferences from recent conversation
 * - memory_preference_explain: Explain a preference's source and confidence
 * 
 * Preference Slot structure:
 * {
 *   slot: "language",       // slot name
 *   value: "Chinese",       // current value
 *   confidence: 0.95,      // confidence 0-1
 *   source: "explicit",    // explicit | inferred | historical
 *   since: "2026-03-01",   // when the preference formed (ISO date)
 *   updated: "2026-03-29", // last update (ISO date)
 *   history: [{value, from, to, at}] // change history
 * }
 */
import { loadPreferences, getSlotValue, getSlotEntry, updateSlotValue, persistPreferences, getSlotDefinition, getSlotNames } from '../preference_slots_schema.js';
import { extractPreferencesFromHistory, mergeExtractedPreferences } from '../preference_extractor.js';
import { getAllMemories } from '../storage.js';

/**
 * Format a timestamp to ISO date string (YYYY-MM-DD)
 */
function toDateStr(ts) {
  if (!ts) return new Date().toISOString().slice(0, 10);
  const d = typeof ts === 'number' ? new Date(ts) : new Date(ts);
  return d.toISOString().slice(0, 10);
}

// ============================================================
// Tool: memory_preference_get
// ============================================================
export function memoryPreferenceGetTool({ key, context } = {}) {
  try {
    const preferences = loadPreferences();

    if (key) {
      // Return single slot with full metadata
      const entry = preferences[key];
      if (!entry) {
        return { content: [{ type: 'text', text: JSON.stringify({ error: `Unknown slot: ${key}` }, null, 2) }], isError: true };
      }
      const def = getSlotDefinition(key);
      const now = new Date().toISOString();

      // Context-aware filtering: if since is older than a recent context window,
      // return "historical" flag to let caller know this is stale
      let isHistorical = false;
      if (context?.currentTime && entry.since) {
        const sinceDate = new Date(entry.since);
        const ctxDate = new Date(context.currentTime);
        // If the preference was formed more than 90 days ago, mark as historical
        isHistorical = (ctxDate - sinceDate) > 90 * 24 * 60 * 60 * 1000;
      }

      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            success: true,
            slot: key,
            value: entry.value,
            confidence: entry.confidence,
            source: entry.source,
            since: entry.since || toDateStr(entry.lastUpdated),
            updated: toDateStr(entry.lastUpdated),
            history: entry.history || [],
            definition: def,
            isHistorical,
          }, null, 2),
        }],
      };
    }

    // Return all slots
    const all = {};
    for (const [slotName, entry] of Object.entries(preferences)) {
      const def = getSlotDefinition(slotName);
      all[slotName] = {
        value: entry.value,
        confidence: entry.confidence,
        source: entry.source,
        since: entry.since || toDateStr(entry.lastUpdated),
        updated: toDateStr(entry.lastUpdated),
        history: entry.history || [],
        definition: { description: def?.description, type: def?.type, options: def?.options },
      };
    }
    return { content: [{ type: 'text', text: JSON.stringify({ success: true, count: Object.keys(all).length, preferences: all }, null, 2) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
  }
}

// ============================================================
// Tool: memory_preference_set
// ============================================================
export function memoryPreferenceSetTool({ key, value, confidence, source, since } = {}) {
  try {
    if (!key) throw new Error('key is required');
    if (value === undefined || value === null) throw new Error('value is required');

    const preferences = loadPreferences();
    const def = getSlotDefinition(key);

    // Validate options if defined
    if (def?.options && !def.options.includes(value)) {
      return {
        content: [{ type: 'text', text: JSON.stringify({ error: `Invalid value '${value}'. Options: ${def.options.join(', ')}` }, null, 2) }],
        isError: true,
      };
    }

    // Validate array type
    if (def?.type === 'array') {
      if (!Array.isArray(value)) {
        return { content: [{ type: 'text', text: JSON.stringify({ error: `Value for '${key}' must be an array` }, null, 2) }], isError: true };
      }
    }

    const conf = confidence !== undefined ? parseFloat(confidence) : 0.9;
    const src = source || 'explicit';
    const now = Date.now();
    const nowDate = toDateStr(now);

    // Build history entry if value is changing
    const existing = preferences[key];
    const historyEntry = {
      value,
      from: existing?.value ?? null,
      to: value,
      at: nowDate,
      source: src,
    };

    // Build full slot entry with history tracking
    const newEntry = {
      value,
      confidence: Math.min(1, Math.max(0, conf)),
      source: src,
      lastUpdated: now,
      since: since ? String(since).slice(0, 10) : (existing?.since || nowDate),
      history: existing?.history ? [...existing.history, historyEntry] : [historyEntry],
    };

    preferences[key] = newEntry;
    persistPreferences(preferences);

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          success: true,
          slot: key,
          value,
          confidence: conf,
          source: src,
          since: newEntry.since,
          updated: nowDate,
          historyLength: newEntry.history.length,
          changedFrom: historyEntry.from,
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
  }
}

// ============================================================
// Tool: memory_preference_infer
// ============================================================
export function memoryPreferenceInferTool({ messageCount = 20, since } = {}) {
  try {
    // Optionally filter to recent memories by since date
    let allMemories = getAllMemories();
    
    if (since) {
      const sinceTs = new Date(String(since)).getTime();
      allMemories = allMemories.filter(m => (m.created_at || 0) >= sinceTs);
    }

    const recentMemories = allMemories
      .filter(m => m.category === 'conversation' || m.text)
      .sort((a, b) => (b.updated_at || 0) - (a.updated_at || 0))
      .slice(0, messageCount);

    if (recentMemories.length === 0) {
      return {
        content: [{ type: 'text', text: JSON.stringify({ message: 'No conversation history found to analyze', inferred: {} }, null, 2) }],
      };
    }

    const extracted = extractPreferencesFromHistory(recentMemories);
    const currentPrefs = loadPreferences();
    const merged = mergeExtractedPreferences(currentPrefs, extracted);

    // Format results with since tracking
    const inferred = {};
    for (const [slotName, entry] of Object.entries(extracted)) {
      const nowDate = toDateStr();
      // If this is a new inference or confidence improved, set since to now
      const isNew = entry.confidence > (currentPrefs[slotName]?.confidence || 0);
      inferred[slotName] = {
        value: entry.value,
        confidence: Math.round(entry.confidence * 100) / 100,
        source: entry.source,
        since: isNew ? nowDate : (currentPrefs[slotName]?.since || nowDate),
        updated: nowDate,
        isNew,
        isUpgrade: isNew && currentPrefs[slotName] !== undefined,
      };
    }

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          success: true,
          messagesAnalyzed: recentMemories.length,
          inferred,
          merged: Object.keys(extracted).length,
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
  }
}

// ============================================================
// Tool: memory_preference_explain
// ============================================================
export function memoryPreferenceExplainTool({ key } = {}) {
  try {
    if (!key) throw new Error('key is required');

    const preferences = loadPreferences();
    const entry = preferences[key];
    if (!entry) {
      return { content: [{ type: 'text', text: JSON.stringify({ error: `Unknown slot: ${key}` }, null, 2) }], isError: true };
    }

    const def = getSlotDefinition(key);

    // Build explanation
    const explanations = [];

    explanations.push(`**Slot**: ${key}`);
    explanations.push(`**Current Value**: ${JSON.stringify(entry.value)}`);
    explanations.push(`**Confidence**: ${Math.round(entry.confidence * 100)}%`);
    explanations.push(`**Source**: ${entry.source}`);
    explanations.push(`**Since**: ${entry.since || toDateStr(entry.lastUpdated)}`);
    explanations.push(`**Last Updated**: ${toDateStr(entry.lastUpdated)}`);
    explanations.push(`**Change History**: ${(entry.history || []).length} change(s)`);

    if (def) {
      explanations.push(`**Description**: ${def.description || 'No description'}`);
      if (def.options) {
        explanations.push(`**Valid Options**: ${def.options.join(', ')}`);
      }
    }

    // Confidence interpretation
    if (entry.confidence >= 0.8) {
      explanations.push(`**Interpretation**: High confidence — this preference is well-established.`);
    } else if (entry.confidence >= 0.6) {
      explanations.push(`**Interpretation**: Moderate confidence — derived from multiple observations.`);
    } else {
      explanations.push(`**Interpretation**: Low confidence — consider confirming with the user.`);
    }

    // Source interpretation
    if (entry.source === 'explicit') {
      explanations.push(`**Source Note**: User directly stated this preference.`);
    } else if (entry.source === 'inferred') {
      explanations.push(`**Source Note**: Automatically inferred from conversation patterns.`);
    } else {
      explanations.push(`**Source Note**: Set from historical defaults.`);
    }

    // Temporal note
    if (entry.since) {
      const ageDays = Math.floor((Date.now() - new Date(entry.since).getTime()) / (1000 * 60 * 60 * 24));
      if (ageDays <= 7) {
        explanations.push(`**Temporal**: This preference was formed recently (${ageDays} day(s) ago).`);
      } else if (ageDays <= 30) {
        explanations.push(`**Temporal**: This preference is ${ageDays} days old.`);
      } else {
        explanations.push(`**Temporal**: This preference is ${ageDays} days old — consider if it may have changed.`);
      }
    }

    // Show recent history
    const recentHistory = (entry.history || []).slice(-3);
    if (recentHistory.length > 0) {
      explanations.push(`**Recent Changes**: ${recentHistory.map(h => `${h.from}→${h.to} (${h.at})`).join(', ')}`);
    }

    return {
      content: [{
        type: 'text',
        text: explanations.join('\n'),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
  }
}

export default {
  memoryPreferenceGetTool,
  memoryPreferenceSetTool,
  memoryPreferenceInferTool,
  memoryPreferenceExplainTool,
};
