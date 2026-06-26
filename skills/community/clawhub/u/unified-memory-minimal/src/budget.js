/**
 * budget.js - Memory Budget Calculator & Token Allocator
 *
 * Calculates how many memories can fit within a given context window budget.
 * This enables dynamic top-K selection based on actual token limits rather
 * than a fixed number.
 *
 * Also provides precise token allocation control for different memory types
 * (transcript, memory, episode, working, system) with priority-based allocation
 * and auto-compaction when budgets are exceeded.
 *
 * Formula:
 *   maxMemories = floor((contextBudget - queryTokens - responseReserved) / avgMemoryTokens)
 *
 * Usage:
 *   const budget = calculateBudget({ query, contextBudget: 120000 });
 *   const results = await search(query, { topK: budget.limit, ... });
 *
 * Token Allocator Usage:
 *   const allocator = new TokenAllocator(8000);
 *   const tokens = allocator.allocate('transcript', 'high');
 *   const status = getBudgetStatus();
 */

import { estimateTokensSimple, estimateQueryTokens } from './utils/token_estimator.js';
import { config } from './config.js';

// Default budget configuration
const DEFAULT_CONTEXT_BUDGET = 120000;   // 120k tokens (e.g., GPT-4 Turbo context)
const DEFAULT_RESPONSE_RESERVED = 20000; // Reserve 20k tokens for response generation
const DEFAULT_AVG_MEMORY_TOKENS = 500;    // Average memory size in tokens

// ============ Token Allocator for Memory Types ============

/**
 * Memory type budget allocations (percentages of total budget)
 * @type {Object<string, number>}
 */
const MEMORY_TYPE_BUDGETS = {
  transcript: 0.30,  // 30% - main conversation transcript
  memory: 0.40,       // 40% - persistent memories
  episode: 0.15,      // 15% - session episodes
  working: 0.10,      // 10% - current task working memory
  system: 0.05,       // 5%  - system context
};

/**
 * Priority level multipliers
 * @type {Object<string, number>}
 */
const PRIORITY_LEVELS = {
  critical: 1.0,
  high: 0.8,
  medium: 0.5,
  low: 0.3,
};

/**
 * Singleton TokenAllocator instance
 * @type {TokenAllocator | null}
 */
let _allocatorInstance = null;

/**
 * TokenAllocator class - manages token budgets across different memory types
 *
 * Provides precise token allocation control with:
 * - Percentage-based memory type budgets
 * - Priority-based allocation
 * - Auto-compaction when budgets exceeded
 * - Dynamic recalculation
 */
export class TokenAllocator {
  /**
   * Create a new TokenAllocator
   * @param {number} maxBudget - Total context budget in tokens (default 8000)
   */
  constructor(maxBudget = 8000) {
    this.maxBudget = maxBudget;
    this.memoryTypes = Object.keys(MEMORY_TYPE_BUDGETS);

    // Initialize allocations for each memory type
    this.allocations = {};
    this.usage = {};

    for (const type of this.memoryTypes) {
      const budget = Math.floor(maxBudget * MEMORY_TYPE_BUDGETS[type]);
      this.allocations[type] = budget;
      this.usage[type] = 0;
    }

    // Ensure allocations sum to maxBudget
    this._normalize();
  }

  /**
   * Ensure allocations sum to maxBudget (adjust proportionally)
   * @private
   */
  _normalize() {
    const total = Object.values(this.allocations).reduce((a, b) => a + b, 0);
    if (total !== this.maxBudget) {
      const diff = this.maxBudget - total;
      // Distribute difference proportionally
      const scale = this.maxBudget / total;
      for (const type of this.memoryTypes) {
        this.allocations[type] = Math.floor(this.allocations[type] * scale);
      }
      // Fix rounding by adjusting the largest
      const currentTotal = Object.values(this.allocations).reduce((a, b) => a + b, 0);
      const remainder = this.maxBudget - currentTotal;
      const largest = this.memoryTypes.reduce((a, b) =>
        this.allocations[a] > this.allocations[b] ? a : b
      );
      this.allocations[largest] += remainder;
    }
  }

  /**
   * Allocate tokens to a memory type based on priority
   * @param {string} memoryType - Memory type (transcript, memory, episode, working, system)
   * @param {string|number} priority - Priority level (critical, high, medium, low) or multiplier (0-1)
   * @returns {number} Allocated token count
   */
  allocate(memoryType, priority = 'medium') {
    if (!this.memoryTypes.includes(memoryType)) {
      throw new Error(`Unknown memory type: ${memoryType}. Valid types: ${this.memoryTypes.join(', ')}`);
    }

    // Resolve priority multiplier
    let multiplier;
    if (typeof priority === 'number') {
      multiplier = Math.max(0, Math.min(1, priority));
    } else {
      multiplier = PRIORITY_LEVELS[priority] ?? 0.5;
    }

    const budget = this.allocations[memoryType];
    const allocated = Math.floor(budget * multiplier);

    return allocated;
  }

  /**
   * Get remaining tokens for a memory type
   * @param {string} memoryType - Memory type
   * @returns {number} Remaining token count
   */
  getRemaining(memoryType) {
    if (!this.memoryTypes.includes(memoryType)) {
      throw new Error(`Unknown memory type: ${memoryType}`);
    }
    return Math.max(0, this.allocations[memoryType] - this.usage[memoryType]);
  }

  /**
   * Record token usage for a memory type
   * @param {string} memoryType - Memory type
   * @param {number} tokens - Token count to add to usage
   */
  addUsage(memoryType, tokens) {
    if (!this.memoryTypes.includes(memoryType)) {
      throw new Error(`Unknown memory type: ${memoryType}`);
    }
    this.usage[memoryType] = (this.usage[memoryType] || 0) + tokens;
  }

  /**
   * Check if a memory type is over budget
   * @param {string} memoryType - Memory type
   * @returns {boolean} True if over budget
   */
  isOverBudget(memoryType) {
    return this.usage[memoryType] > this.allocations[memoryType];
  }

  /**
   * Get the compaction ratio (how much over budget)
   * @param {string} memoryType - Memory type
   * @returns {number} Ratio of usage to allocation (1.0 = at budget, 1.5 = 50% over)
   */
  getCompactionRatio(memoryType) {
    if (!this.memoryTypes.includes(memoryType)) {
      throw new Error(`Unknown memory type: ${memoryType}`);
    }
    if (this.allocations[memoryType] === 0) return Infinity;
    return this.usage[memoryType] / this.allocations[memoryType];
  }

  /**
   * Auto-compress content when memory type exceeds budget
   * Uses simple truncation with preservation of key information
   * @param {string} memoryType - Memory type
   * @param {string} content - Content to potentially compress
   * @returns {Object} { compressed: boolean, content: string, ratio: number, savedTokens: number }
   */
  compress(memoryType, content) {
    if (!this.memoryTypes.includes(memoryType)) {
      throw new Error(`Unknown memory type: ${memoryType}`);
    }

    const ratio = this.getCompactionRatio(memoryType);

    if (ratio <= 1.0) {
      return { compressed: false, content, ratio, savedTokens: 0 };
    }

    // Calculate target tokens (80% of allocation to leave buffer)
    const targetTokens = Math.floor(this.allocations[memoryType] * 0.8);

    // Simple compression: truncate to target with ellipsis for significant overages
    // Estimate characters from tokens (rough: 4 chars per token)
    const targetChars = targetTokens * 4;
    const currentChars = content.length;

    if (currentChars <= targetChars) {
      return { compressed: false, content, ratio, savedTokens: 0 };
    }

    // Truncate with ellipsis, preserving beginning and key info
    const truncated = content.slice(0, Math.max(0, targetChars - 3)) + '...';
    const savedTokens = Math.ceil((currentChars - truncated.length) / 4);

    return {
      compressed: true,
      content: truncated,
      ratio,
      savedTokens,
    };
  }

  /**
   * Recalculate all allocations based on current usage and priorities
   * Redistributes unused budget from under-utilized types to over-utilized ones
   * @returns {Object} Updated allocation info
   */
  recalculate() {
    // Find underutilized and overutilized types
    const underutilized = [];
    const overutilized = [];

    for (const type of this.memoryTypes) {
      const ratio = this.usage[type] / this.allocations[type];
      if (ratio < 0.5) {
        underutilized.push({ type, slack: this.allocations[type] - this.usage[type] });
      } else if (ratio > 1.0) {
        overutilized.push({ type, overage: this.usage[type] - this.allocations[type] });
      }
    }

    // Redistribute from underutilized to overutilized
    let totalSlack = underutilized.reduce((sum, u) => sum + u.slack, 0);
    let totalOverage = overutilized.reduce((sum, o) => sum + o.overage, 0);

    // Proportional redistribution
    for (const item of overutilized) {
      const share = totalSlack > 0 ? Math.floor((item.overage / totalOverage) * totalSlack) : 0;
      this.allocations[item.type] += share;
    }

    // Mark unused (below threshold) types
    const result = {
      redistributed: totalSlack > 0,
      slackDistributed: Math.min(totalSlack, totalOverage),
      adjustments: {},
    };

    for (const type of this.memoryTypes) {
      result.adjustments[type] = {
        allocation: this.allocations[type],
        usage: this.usage[type],
        remaining: this.getRemaining(type),
        percentUsed: this.allocations[type] > 0
          ? Math.round((this.usage[type] / this.allocations[type]) * 100)
          : 0,
      };
    }

    return result;
  }

  /**
   * Reset usage counters for all memory types
   */
  resetUsage() {
    for (const type of this.memoryTypes) {
      this.usage[type] = 0;
    }
  }

  /**
   * Get full status of the allocator
   * @returns {Object} Complete budget status
   */
  getStatus() {
    const totalAllocated = Object.values(this.allocations).reduce((a, b) => a + b, 0);
    const totalUsage = Object.values(this.usage).reduce((a, b) => a + b, 0);

    const types = {};
    for (const type of this.memoryTypes) {
      types[type] = {
        allocation: this.allocations[type],
        usage: this.usage[type],
        remaining: this.getRemaining(type),
        percentUsed: this.allocations[type] > 0
          ? Math.round((this.usage[type] / this.allocations[type]) * 100)
          : 0,
        percentOfTotal: this.maxBudget > 0
          ? Math.round((this.allocations[type] / this.maxBudget) * 100)
          : 0,
        isOverBudget: this.isOverBudget(type),
      };
    }

    return {
      maxBudget: this.maxBudget,
      totalAllocated,
      totalUsage,
      totalRemaining: this.maxBudget - totalUsage,
      percentUsed: this.maxBudget > 0
        ? Math.round((totalUsage / this.maxBudget) * 100)
        : 0,
      types,
      priorityLevels: PRIORITY_LEVELS,
      memoryTypeBudgets: MEMORY_TYPE_BUDGETS,
    };
  }
}

/**
 * Get or create the singleton TokenAllocator instance
 * @param {number} [maxBudget] - Optional max budget to set (only used on first call)
 * @returns {TokenAllocator}
 */
export function getAllocator(maxBudget) {
  if (!_allocatorInstance) {
    _allocatorInstance = new TokenAllocator(maxBudget ?? 8000);
  } else if (maxBudget !== undefined && maxBudget !== _allocatorInstance.maxBudget) {
    // Update max budget if specified and different
    _allocatorInstance.maxBudget = maxBudget;
    // Recalculate allocations
    for (const type of _allocatorInstance.memoryTypes) {
      _allocatorInstance.allocations[type] = Math.floor(maxBudget * MEMORY_TYPE_BUDGETS[type]);
    }
    _allocatorInstance._normalize();
  }
  return _allocatorInstance;
}

/**
 * Allocate tokens for a memory type
 * @param {string} memoryType - Memory type (transcript, memory, episode, working, system)
 * @param {string|number} priority - Priority (critical, high, medium, low) or multiplier
 * @returns {number} Allocated token count
 */
export function allocateTokens(memoryType, priority = 'medium') {
  const allocator = getAllocator();
  return allocator.allocate(memoryType, priority);
}

/**
 * Get complete budget status
 * @returns {Object} Budget status for all memory types
 */
export function getBudgetStatus() {
  const allocator = getAllocator();
  return allocator.getStatus();
}

/**
 * Compress content if memory type is over budget
 * @param {string} memoryType - Memory type
 * @param {string} content - Content to compress
 * @returns {Object} { compressed, content, ratio, savedTokens }
 */
export function compressIfNeeded(memoryType, content) {
  const allocator = getAllocator();
  return allocator.compress(memoryType, content);
}

/**
 * Recalculate budgets after context changes
 * @returns {Object} Recalculation result
 */
export function recalculateBudgets() {
  const allocator = getAllocator();
  return allocator.recalculate();
}

// Standard context budgets for various models
export const CONTEXT_BUDGETS = {
  '32k': 32000,
  '64k': 64000,
  '128k': 128000,
  '200k': 200000,
  '1M': 1000000,
};

/**
 * Memory budget calculation result
 * @typedef {Object} BudgetResult
 * @property {number} limit - maximum number of memories to retrieve
 * @property {number} contextBudget - total context window size
 * @property {number} queryTokens - tokens used by the query
 * @property {number} responseReserved - tokens reserved for response
 * @property {number} availableForMemories - tokens available for memory content
 * @property {number} avgMemoryTokens - assumed average tokens per memory
 * @property {number} estimatedTotalTokens - estimated total if all memories used
 */

/**
 * Calculate how many memories can fit within a context budget
 * 
 * @param {Object} params
 * @param {string} params.query - search query text
 * @param {number} [params.contextBudget] - total available tokens (default: from config or 120k)
 * @param {number} [params.responseReserved] - tokens to reserve for response (default: 20k)
 * @param {number} [params.avgMemoryTokens] - average tokens per memory (default: 500)
 * @param {number} [params.topK] - optional fixed upper bound (limit won't exceed this)
 * @returns {BudgetResult}
 */
export function calculateBudget({
  query = '',
  contextBudget = null,
  responseReserved = null,
  avgMemoryTokens = null,
  topK = null,
}) {
  // Resolve defaults from config or constants
  const effectiveBudget = contextBudget ?? config.contextBudget ?? DEFAULT_CONTEXT_BUDGET;
  const effectiveResponseReserved = responseReserved ?? config.responseReserved ?? DEFAULT_RESPONSE_RESERVED;
  const effectiveAvgMemoryTokens = avgMemoryTokens ?? config.avgMemoryTokens ?? DEFAULT_AVG_MEMORY_TOKENS;

  // Estimate query token cost
  const queryTokens = estimateQueryTokens(query);

  // Calculate available space for memory content
  const availableForMemories = Math.max(0, effectiveBudget - queryTokens - effectiveResponseReserved);

  // Calculate max memories that can fit
  let limit = Math.floor(availableForMemories / effectiveAvgMemoryTokens);

  // Apply upper bound if specified
  if (topK !== null && topK > 0) {
    limit = Math.min(limit, topK);
  }

  // Ensure at least 1 if budget allows
  limit = Math.max(0, limit);

  return {
    limit,
    contextBudget: effectiveBudget,
    queryTokens,
    responseReserved: effectiveResponseReserved,
    availableForMemories,
    avgMemoryTokens: effectiveAvgMemoryTokens,
    estimatedTotalTokens: queryTokens + (limit * effectiveAvgMemoryTokens),
  };
}

/**
 * Calculate budget and estimate how many memories fit for multiple context sizes
 * Useful for providing users with budget recommendations
 * 
 * @param {string} query - search query
 * @param {number} [topK] - optional upper bound
 * @returns {Object} budget estimates for standard context sizes
 */
export function estimateBudgets(query, topK = null) {
  const budgets = {};
  for (const [name, budget] of Object.entries(CONTEXT_BUDGETS)) {
    budgets[name] = calculateBudget({ query, contextBudget: budget, topK });
  }
  return budgets;
}

/**
 * Budget-aware result trimmer
 * 
 * Takes search results and trims them if they exceed the token budget.
 * Trims lowest-scoring memories first.
 * 
 * @param {Array} results - search results with memory and score fields
 * @param {number} budget - token budget for memories
 * @param {number} [minResults=3] - minimum results to keep if budget allows
 * @returns {Array} trimmed results
 */
export function trimResultsByBudget(results, budget, minResults = 3) {
  if (!Array.isArray(results) || results.length === 0) return results;
  if (!budget || budget <= 0) return results;

  // Sort by score descending (keep highest scoring)
  const sorted = [...results].sort((a, b) => (b.score ?? 0) - (a.score ?? 0));

  let totalTokens = 0;
  const kept = [];

  for (const result of sorted) {
    const text = result.memory?.text || result.memory?.content || '';
    const tokens = estimateTokensSimple(text);

    if (kept.length < minResults || totalTokens + tokens <= budget) {
      kept.push(result);
      totalTokens += tokens;
    } else {
      break; // Budget exhausted
    }
  }

  return kept;
}
