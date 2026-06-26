/**
 * preference_extractor.js — Auto-extract Preferences from Conversation History
 * Part of Feature #10: Structured Preference Slots
 * 
 * Analyzes conversation history to infer user preferences with confidence scoring.
 * Signals: explicit statements ("I prefer..."), implicit patterns, behavioral signals.
 */
import { getPreferencesFlat, createSlotEntry, SOURCE_TYPES, SLOT_DEFINITIONS } from './preference_slots_schema.js';

/**
 * Explicit preference patterns (regex-based signal detection)
 */
const EXPLICIT_PATTERNS = {
  language: [
    /\b(please?\s+)?(speak|write|respond|answer)\s+(in\s+)?(english|chinese|中文|英文)\b/gi,
    /\b(i\s+prefer|i\s+like|i\s+want)\s+.*\s+(english|chinese|中文|英文)\b/gi,
    /\b(用|用中文|英文|中文说)\b/gi,
  ],
  communication_style: [
    /\b(i\s+prefer|i\s+like)\s+(concise|brief|short|detailed|verbose|comprehensive)\b/gi,
    /\b(简明|简洁|详细|简短|扼要)\b/gi,
    /\b(can\s+you\s+)?(keep\s+it\s+)?(short|brief|concise|detailed)\b/gi,
    /\b不要\s+(太\s+)?(长|详细|啰嗦)/gi,
  ],
  response_length: [
    /\b(keep\s+it\s+)?(short|brief|quick|one\s+liner|two\s+liner)\b/gi,
    /\b(详细|全面|深入|简略|简短)\s+(说明|介绍|回答)/gi,
    /\b(give\s+me\s+)?(a\s+brief|a\s+short|a\s+detailed)\b/gi,
  ],
  timezone: [
    /\b(i'm\s+in|i\s+am\s+in|位于|在)([\w\/]+)\b/gi,
    /\b(my\s+timezone|time\s+zone)\s*[:\-]?\s*([\w\/+0-9:]+)/gi,
    /\bUTC([+\-]?\d{1,2})/gi,
  ],
  notification_preference: [
    /\b(don't\s+)?notify?\s+(me\s+)?(too\s+much|every|all|unless|important)\b/gi,
    /\b(少|不要|别)\s+(打扰|通知|提醒)/gi,
    /\bonly\s+(important|critical|urgent)\s+(alerts|notifications|reminders)\b/gi,
  ],
  formality_level: [
    /\b(i\s+prefer|i\s+like)\s+(formal|casual|friendly|professional)\b/gi,
    /\b(正式|随意|专业|朋友式)\s+(交流|对话|沟通)/gi,
  ],
};

/**
 * Implicit behavioral signals
 */
const BEHAVIORAL_SIGNALS = {
  interests: {
    pattern: /\b(project|code|build|develop|test|deploy|api|database|frontend|backend)\b/gi,
    boost: 0.1,
  },
  goals: {
    pattern: /\b(finish|complete|achieve|goal|target|deadline|launch|release)\b/gi,
    boost: 0.1,
  },
};

/**
 * Language detection helpers
 */
function detectLanguage(text) {
  const chineseChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
  const englishWords = (text.match(/[a-zA-Z]{3,}/g) || []).length;
  const total = chineseChars + englishWords;
  if (total === 0) return 'en';
  return chineseChars / total > 0.3 ? 'zh' : 'en';
}

/**
 * Extract explicit preferences from a single message
 */
function extractExplicitFromMessage(text) {
  const results = {};
  
  for (const [slotName, patterns] of Object.entries(EXPLICIT_PATTERNS)) {
    for (const pattern of patterns) {
      const match = text.match(pattern);
      if (match) {
        let value = null;
        // Extract value from pattern groups or keyword
        const matched = match[0];
        if (slotName === 'language') {
          if (/chinese|中文|中文说/.test(matched)) value = 'zh';
          else if (/english|英文/.test(matched)) value = 'en';
        } else if (slotName === 'communication_style') {
          if (/concise|brief|short|简明|简洁|简短/.test(matched)) value = 'concise';
          else if (/detailed|verbose|详细/.test(matched)) value = 'detailed';
        } else if (slotName === 'response_length') {
          if (/short|brief|quick|简略|简短/.test(matched)) value = 'short';
          else if (/detailed|comprehensive|详细|全面/.test(matched)) value = 'long';
        } else if (slotName === 'timezone') {
          const tzMatch = matched.match(/(UTC)?([+\-]?\d{1,2})/);
          if (tzMatch) {
            const offset = parseInt(tzMatch[2]);
            value = `UTC${offset >= 0 ? '+' : ''}${offset}`;
          }
        } else if (slotName === 'notification_preference') {
          if (/don't\s+notify|少|不要|别.*提醒|别.*打扰/.test(matched)) value = 'minimal';
          else if (/only\s+important|仅.*重要/.test(matched)) value = 'minimal';
        } else if (slotName === 'formality_level') {
          if (/formal|正式/.test(matched)) value = 'formal';
          else if (/casual|随意|朋友/.test(matched)) value = 'casual';
        }
        
        if (value) {
          results[slotName] = {
            value,
            confidence: 0.9,
            source: SOURCE_TYPES.EXPLICIT,
            signal: matched,
          };
          break;
        }
      }
    }
  }
  
  return results;
}

/**
 * Detect implicit patterns from message
 */
function detectImplicitPatterns(text) {
  const results = {};
  const lang = detectLanguage(text);
  
  // Language implicit signal
  if (lang === 'zh') {
    results.language = { value: 'zh', confidence: 0.7, source: SOURCE_TYPES.INFERRED };
  } else {
    results.language = { value: 'en', confidence: 0.6, source: SOURCE_TYPES.INFERRED };
  }
  
  // Message length signal
  const wordCount = text.split(/\s+/).length;
  if (wordCount < 20) {
    results.communication_style = { value: 'concise', confidence: 0.6, source: SOURCE_TYPES.INFERRED };
  } else if (wordCount > 100) {
    results.communication_style = { value: 'detailed', confidence: 0.6, source: SOURCE_TYPES.INFERRED };
    results.response_length = { value: 'long', confidence: 0.6, source: SOURCE_TYPES.INFERRED };
  }
  
  // Behavioral signals
  for (const [slotName, signal] of Object.entries(BEHAVIORAL_SIGNALS)) {
    const matches = text.match(signal.pattern);
    if (matches && matches.length >= 2) {
      if (!results[slotName]) {
        results[slotName] = {
          value: [],
          confidence: Math.min(0.9, signal.boost * matches.length),
          source: SOURCE_TYPES.INFERRED,
        };
      }
      if (Array.isArray(results[slotName].value)) {
        results[slotName].value.push(...matches.slice(0, 3));
      }
    }
  }
  
  return results;
}

/**
 * Extract preferences from a batch of messages (conversation history)
 * @param {Array<{text: string, role?: string, timestamp?: number}>} messages
 * @returns {Object} Extracted preferences with confidence scores
 */
export function extractPreferencesFromHistory(messages) {
  const extracted = {};
  const messageCount = messages.length;
  
  for (const msg of messages) {
    const text = msg.text || msg.content || '';
    if (!text || text.length < 3) continue;
    
    // Explicit extraction (highest priority)
    const explicit = extractExplicitFromMessage(text);
    for (const [slotName, data] of Object.entries(explicit)) {
      if (!extracted[slotName] || data.confidence > (extracted[slotName].confidence || 0)) {
        extracted[slotName] = createSlotEntry(data.value, data.source, data.confidence);
      }
    }
    
    // Implicit extraction
    const implicit = detectImplicitPatterns(text);
    for (const [slotName, data] of Object.entries(implicit)) {
      if (!extracted[slotName] || data.confidence > (extracted[slotName].confidence || 0)) {
        // For arrays, merge values
        if (Array.isArray(data.value) && Array.isArray(extracted[slotName]?.value)) {
          const merged = [...new Set([...extracted[slotName].value, ...data.value])];
          extracted[slotName] = createSlotEntry(merged, data.source, data.confidence);
        } else if (!extracted[slotName]) {
          extracted[slotName] = createSlotEntry(data.value, data.source, data.confidence);
        }
      }
    }
  }
  
  // Boost confidence if multiple signals across messages
  for (const [slotName, entry] of Object.entries(extracted)) {
    if (entry.confidence < 0.9 && messageCount > 3) {
      entry.confidence = Math.min(0.85, entry.confidence + 0.05 * Math.log(messageCount));
    }
    entry.lastUpdated = Date.now();
  }
  
  return extracted;
}

/**
 * Merge extracted preferences with existing preferences
 * Higher confidence wins, explicit > inferred > historical
 */
export function mergeExtractedPreferences(existing, extracted) {
  const merged = { ...existing };
  
  for (const [slotName, newEntry] of Object.entries(extracted)) {
    const existingEntry = merged[slotName];
    
    // Higher confidence wins
    if (!existingEntry || newEntry.confidence > existingEntry.confidence) {
      merged[slotName] = newEntry;
    }
    // Same confidence: explicit > inferred > historical
    else if (newEntry.confidence === existingEntry.confidence) {
      const sourcePriority = { explicit: 3, inferred: 2, historical: 1 };
      if ((sourcePriority[newEntry.source] || 0) > (sourcePriority[existingEntry.source] || 0)) {
        merged[slotName] = newEntry;
      }
    }
  }
  
  return merged;
}

export default {
  extractExplicitFromMessage,
  detectImplicitPatterns,
  extractPreferencesFromHistory,
  mergeExtractedPreferences,
  detectLanguage,
};
