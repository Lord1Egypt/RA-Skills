/**
 * Intent Router - classify query type and routing strategy
 * Returns null → skip retrieval; returns strategy object → proceed
 */
export const INTENT_TYPES = {
  FACT: 'fact',       // who/when/where/what questions
  PREFERENCE: 'preference', // likes/dislikes
  DECISION: 'decision',   // why/why not/why chose
  ENTITY: 'entity',      // tell me about X
  REFLECTION: 'reflection', // lessons/learned/growth
  RECALL: 'recall',       // remember/past/earlier
  METRIC: 'metric',       // stats/numbers/counts
  SKIP: 'skip',           // non-retrieval
};

const ROUTING_RULES = [
  // FACT patterns
  { pattern: /^(who|what|when|where|which)\s+(is|are|was|were|do|does|did|have|has)\s+/i, intent: 'fact' },
  { pattern: /\?$/, intent: 'fact' },
  // PREFERENCE patterns
  { pattern: /(prefer|like|hate|dislike|enjoy|avoid|love|cannot\s+stand)/i, intent: 'preference' },
  // DECISION patterns
  { pattern: /(decide|chose|choose|decision|reason|because|why\s+(did|didn|not))/i, intent: 'decision' },
  // ENTITY patterns
  { pattern: /^tell\s+me\s+about/i, intent: 'entity' },
  { pattern: /^(who\s+is|what\s+is|explain|describe)\s+.{0,30}$/i, intent: 'entity' },
  // REFLECTION patterns
  { pattern: /(learn|lesson|reflect|realize|discover|understand bett)/i, intent: 'reflection' },
  // RECALL patterns (force retrieval)
  { pattern: /(remember|recall|earlier|before|previously|once|曾|记得|之前)/i, intent: 'recall' },
  // METRIC patterns
  { pattern: /(how\s+many|how\s+much|count|total|number\s+of|stats?)/i, intent: 'metric' },
  // SKIP patterns
  { pattern: /^(ok|okay|thanks?|bye|good|great|yes|no|好|好的|再见)/i, intent: 'skip' },
  { pattern: /^[\p{Emoji_Presentation}\p{Extended_Pictographic}]$/u, intent: 'skip' },
];

/**
 * Route a search query to appropriate retrieval strategy
 * @param {string} query
 * @returns {{ intent: string, categories: string[], skip: boolean, strategy: object } | null}
 */
export function routeSearch(query) {
  const q = String(query || '').trim();
  if (!q) return { intent: 'skip', skip: true, categories: [], strategy: {} };

  // Check skip patterns first
  for (const rule of ROUTING_RULES) {
    if (rule.pattern.test(q) && rule.intent === 'skip') {
      return { intent: 'skip', skip: true, categories: [], strategy: {} };
    }
  }

  // Determine primary intent
  let primaryIntent = 'other';
  const matchedCategories = [];

  for (const rule of ROUTING_RULES) {
    if (rule.pattern.test(q)) {
      if (rule.intent !== 'skip') {
        primaryIntent = rule.intent;
        matchedCategories.push(rule.intent);
      }
    }
  }

  // Force recall always needs retrieval
  if (primaryIntent === 'skip' && /(remember|recall|earlier|曾|记得)/i.test(q)) {
    return {
      intent: 'recall',
      skip: false,
      categories: ['preference', 'fact', 'decision', 'entity', 'reflection'],
      strategy: { boostRecent: true, expandScope: true },
    };
  }

  if (primaryIntent === 'skip') {
    return { intent: 'skip', skip: true, categories: [], strategy: {} };
  }

  // Build category filter based on intent
  const categoryMap = {
    fact: ['fact', 'entity'],
    preference: ['preference'],
    decision: ['decision', 'fact'],
    entity: ['entity', 'fact'],
    reflection: ['reflection', 'decision'],
    recall: ['preference', 'fact', 'decision', 'entity', 'reflection'],
    metric: ['fact', 'preference'],
    other: ['preference', 'fact', 'decision', 'entity', 'reflection', 'other'],
  };

  return {
    intent: primaryIntent,
    skip: false,
    categories: categoryMap[primaryIntent] || categoryMap.other,
    strategy: {
      boostRecent: primaryIntent === 'recall',
      expandScope: primaryIntent === 'recall',
    },
  };
}

export default { routeSearch, getCategoryWeights, INTENT_TYPES };

export function getCategoryWeights(intent) {
  const defaults = { preference: 0.3, decision: 0.25, entity: 0.2, fact: 0.15, recent: 0.2, project: 0.25 };
  const map = new Map();
  if (intent === 'general' || !intent) {
    Object.entries(defaults).forEach(([k, v]) => map.set(k, v));
  } else {
    Object.entries(defaults).forEach(([k, v]) => map.set(k, v * 0.5));
    map.set(intent, 0.8);
  }
  return map;
}
