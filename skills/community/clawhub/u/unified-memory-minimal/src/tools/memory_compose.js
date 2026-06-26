/**
 * memory_compose - Prompt Composition API
 *
 * Composes a memory context block for injection into prompts.
 * Inputs:
 *   - messages: current conversation context (last N messages)
 *   - targetTokens: target token count (e.g. 2000)
 *   - categories: filter to specific categories (e.g. ['preference', 'decision'])
 *   - query: optional search query to bias selection
 *
 * Output:
 *   - composed: concatenated memory context string
 *   - tokens: actual token count used
 *   - memories: selected memories with metadata
 *   - remaining: available tokens still within budget
 *
 * Priority order: PIN > HOT > WARM > COLD
 *
 * This is an MCP tool registered via index.js
 */

import { getAllMemories } from '../storage.js';
import { partitionByTier, TIER_CONFIG } from '../tier.js';
import { hybridSearch } from '../fusion.js';

/**
 * Estimate token count (rough: ~4 chars per token for Chinese+English mixed)
 * @param {string} text
 * @returns {number}
 */
function estimateTokens(text) {
  if (!text) return 0;
  // Rough: 1 token ≈ 4 chars for Chinese/English mix
  return Math.ceil(text.length / 4);
}

/**
 * Memory to compact string representation
 * @param {object} mem
 * @returns {string}
 */
function memoryToString(mem) {
  const cat = mem.category || 'general';
  const imp = mem.importance != null ? Math.round(mem.importance * 100) / 100 : 0.5;
  const pin = mem.pinned ? '📌 ' : '';
  const text = mem.text || mem.content || '';
  return `${pin}[${cat}|${imp}] ${text}`;
}

/**
 * Select memories to fill token budget, respecting priority tiers.
 * Priority: PIN > HOT > WARM > COLD
 *
 * @param {object[]} memories - all memories
 * @param {number} targetTokens - target token budget
 * @param {string[]} [categories] - optional category filter
 * @param {string} [query] - optional search query to bias
 * @returns {{ selected: object[], usedTokens: number, fillRate: number }}
 */
function selectMemoriesByPriority(memories, targetTokens, categories, query) {
  // Partition into tiers
  const tiers = partitionByTier(memories);

  // Apply category filter
  const filterByCategory = (arr) => {
    if (!categories || categories.length === 0) return arr;
    return arr.filter(m => categories.includes(m.category));
  };

  const pinned = filterByCategory(memories.filter(m => m.pinned));
  const hot = filterByCategory(tiers.HOT || []);
  const warm = filterByCategory(tiers.WARM || []);
  const cold = filterByCategory(tiers.COLD || []);

  // Priority order
  const priorityBuckets = [
    { label: 'PIN', items: pinned },
    { label: 'HOT', items: hot },
    { label: 'WARM', items: warm },
    { label: 'COLD', items: cold },
  ];

  // Sort each bucket: higher importance first, then more recent
  const sortBucket = (arr) => {
    return [...arr].sort((a, b) => {
      // Pinned always first (already separated)
      if (a.importance !== b.importance) return (b.importance || 0.5) - (a.importance || 0.5);
      return (b.created_at || 0) - (a.created_at || 0);
    });
  };

  const selected = [];
  let usedTokens = 0;

  for (const bucket of priorityBuckets) {
    if (usedTokens >= targetTokens) break;

    const sorted = sortBucket(bucket.items);
    for (const mem of sorted) {
      if (usedTokens >= targetTokens) break;
      const text = memoryToString(mem);
      const tokens = estimateTokens(text);
      if (usedTokens + tokens <= targetTokens) {
        selected.push({ ...mem, _tier: bucket.label, _tokens: tokens });
        usedTokens += tokens;
      }
    }
  }

  const fillRate = targetTokens > 0 ? Math.round((usedTokens / targetTokens) * 1000) / 10 : 0;

  return { selected, usedTokens, fillRate };
}

/**
 * Search for relevant memories and blend with priority selection.
 * When query is provided, use hybrid search to boost relevance.
 *
 * @param {object[]} memories
 * @param {number} targetTokens
 * @param {string[]} [categories]
 * @param {string} [query]
 * @returns {{ selected: object[], usedTokens: number, fillRate: number }}
 */
async function searchAndBlend(memories, targetTokens, categories, query) {
  if (!query || query.length < 2) {
    return selectMemoriesByPriority(memories, targetTokens, categories, query);
  }

  try {
    // Hybrid search to find top memories for query
    const searchResults = await hybridSearch(query, Math.min(20, memories.length), 'hybrid');

    // Build a relevance-boosted pool
    // Memories not in search results get base importance; search results get boosted score
    const scoreMap = new Map();
    for (const r of searchResults) {
      const mem = r.memory;
      scoreMap.set(mem.id, {
        ...mem,
        _relevanceBoost: r.fusionScore || 0,
        _tier: mem.pinned ? 'PIN' : undefined, // will be recalculated
      });
    }

    // Add remaining memories not in search results
    for (const mem of memories) {
      if (!scoreMap.has(mem.id)) {
        scoreMap.set(mem.id, { ...mem, _relevanceBoost: 0 });
      }
    }

    // Re-partition with relevance boost
    const tiers = partitionByTier([...scoreMap.values()]);
    const allSelected = [
      ...(categories && categories.length > 0 ? memories.filter(m => categories.includes(m.category)) : memories),
    ];

    const filterByCategory = (arr) => {
      if (!categories || categories.length === 0) return arr;
      return arr.filter(m => categories.includes(m.category));
    };

    const pinned = filterByCategory(allSelected.filter(m => m.pinned));
    const hot = filterByCategory(tiers.HOT || []);
    const warm = filterByCategory(tiers.WARM || []);
    const cold = filterByCategory(tiers.COLD || []);

    const priorityBuckets = [
      { label: 'PIN', items: pinned },
      { label: 'HOT', items: hot },
      { label: 'WARM', items: warm },
      { label: 'COLD', items: cold },
    ];

    // Sort by: importance * (1 + relevanceBoost)
    const sortBucket = (arr) => {
      return [...arr].sort((a, b) => {
        const scoreA = (a.importance || 0.5) * (1 + (a._relevanceBoost || 0));
        const scoreB = (b.importance || 0.5) * (1 + (b._relevanceBoost || 0));
        return scoreB - scoreA;
      });
    };

    const selected = [];
    let usedTokens = 0;

    for (const bucket of priorityBuckets) {
      if (usedTokens >= targetTokens) break;
      const sorted = sortBucket(bucket.items);
      for (const mem of sorted) {
        if (usedTokens >= targetTokens) break;
        const text = memoryToString(mem);
        const tokens = estimateTokens(text);
        if (usedTokens + tokens <= targetTokens) {
          selected.push({ ...mem, _tier: bucket.label, _tokens: tokens });
          usedTokens += tokens;
        }
      }
    }

    const fillRate = targetTokens > 0 ? Math.round((usedTokens / targetTokens) * 1000) / 10 : 0;
    return { selected, usedTokens, fillRate };

  } catch {
    // Fallback: use priority-based selection without search
    return selectMemoriesByPriority(memories, targetTokens, categories, query);
  }
}

/**
 * Compose memory context block from messages.
 *
 * @param {object} params
 * @param {Array<{role?: string, content: string}>} params.messages - conversation messages
 * @param {number} [params.targetTokens=2000] - target token budget
 * @param {string[]} [params.categories] - category filter
 * @param {string} [params.query] - search query to bias selection
 * @param {number} [params.messageWindow=10] - how many recent messages to use for context
 * @returns {Promise<object>}
 */
export async function memoryCompose({
  messages = [],
  targetTokens = 2000,
  categories = [],
  query,
  messageWindow = 10,
}) {
  // 1. Build context string from recent messages
  const recentMessages = messages.slice(-messageWindow);
  const contextStr = recentMessages
    .map(m => {
      const role = m.role || 'user';
      const text = typeof m.content === 'string' ? m.content : JSON.stringify(m.content || '');
      return `[${role}]: ${text}`;
    })
    .join('\n');

  const contextTokens = estimateTokens(contextStr);

  // 2. Determine effective query (use provided or derive from messages)
  const effectiveQuery = query && query.length >= 2
    ? query
    : recentMessages.map(m => typeof m.content === 'string' ? m.content : '').join(' ').slice(0, 100);

  // 3. Load all memories
  const allMemories = await getAllMemories();

  // 4. Select memories within remaining token budget
  // Reserve some tokens for the context header
  const budgetAfterContext = Math.max(100, targetTokens - contextTokens);
  const { selected, usedTokens, fillRate } = await searchAndBlend(
    allMemories,
    budgetAfterContext,
    categories,
    effectiveQuery
  );

  // 5. Build composed output
  const blocks = selected.map((mem) => {
    const text = mem.text || mem.content || '';
    const tier = mem._tier || 'COLD';
    const pin = mem.pinned ? '📌 ' : '';
    const imp = mem.importance != null ? Math.round(mem.importance * 100) / 100 : 0.5;
    return {
      id: mem.id,
      text,
      category: mem.category,
      importance: imp,
      pinned: !!mem.pinned,
      tier,
      tokens: mem._tokens || estimateTokens(text),
    };
  });

  // 6. Format as readable context block
  const composedLines = blocks.map((b) => {
    const pin = b.pinned ? '📌 ' : '';
    const imp = b.importance != null ? ` imp=${b.importance}` : '';
    const text = b.text.length > 300 ? b.text.slice(0, 300) + '...' : b.text;
    return `${pin}[${b.category}${imp}|${b.tier}] ${text}`;
  });

  const header = `== Memory Context (${blocks.length} memories, ~${usedTokens} tokens, ${fillRate}% fill) ==`;
  const footer = '== End Memory Context ==';
  const composed = [
    header,
    ...composedLines,
    footer,
    contextStr ? `\n[Recent conversation context]\n${contextStr}` : '',
  ].filter(Boolean).join('\n');

  const totalTokens = usedTokens + contextTokens;

  return {
    composed,
    total_tokens: totalTokens,
    memory_tokens: usedTokens,
    context_tokens: contextTokens,
    target_tokens: targetTokens,
    remaining: Math.max(0, targetTokens - totalTokens),
    fill_rate: fillRate,
    count: blocks.length,
    memories: blocks,
    tier_breakdown: {
      PIN: blocks.filter(b => b.tier === 'PIN').length,
      HOT: blocks.filter(b => b.tier === 'HOT').length,
      WARM: blocks.filter(b => b.tier === 'WARM').length,
      COLD: blocks.filter(b => b.tier === 'COLD').length,
    },
  };
}

export default { memoryCompose };
