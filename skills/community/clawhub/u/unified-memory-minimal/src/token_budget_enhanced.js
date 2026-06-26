/**
 * Token Budget Manager Enhanced - Hard Token Budget Enforcement
 * Implements strict token budget limits with automatic enforcement
 * 
 * Storage: ~/.openclaw/workspace/memory/token_budget.json
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = process.env.HOME || '/root';
const MEMORY_DIR = join(HOME, '.openclaw', 'workspace', 'memory');
const BUDGET_FILE = join(MEMORY_DIR, 'token_budget.json');

// Ensure memory directory exists
if (!existsSync(MEMORY_DIR)) {
  mkdirSync(MEMORY_DIR, { recursive: true });
}

// ============================================================================
// Configuration
// ============================================================================

const DEFAULT_CONFIG = {
  // Total context budget (tokens)
  totalBudget: 120000,
  
  // Reserved tokens for response generation
  responseReserved: 20000,
  
  // Available budget for memories
  availableBudget: 100000,
  
  // Memory type allocations (percentages)
  memoryTypeBudgets: {
    transcript: 0.30,  // 30% - main conversation transcript
    memory: 0.40,       // 40% - persistent memories
    episode: 0.15,      // 15% - session episodes
    working: 0.10,      // 10% - current task working memory
    system: 0.05,       // 5%  - system context
  },
  
  // Priority multipliers
  priorityMultipliers: {
    critical: 1.0,
    high: 0.8,
    medium: 0.5,
    low: 0.3,
  },
  
  // Hard limits
  hardLimits: {
    maxMemoriesPerType: 100,
    maxMemorySize: 2000,  // tokens per memory
    maxQueryTokens: 5000,
  },
  
  // Auto-compaction thresholds
  compactionThresholds: {
    warn: 0.70,   // 70% - warning
    compact: 0.85, // 85% - auto-compaction
    hardLimit: 0.95 // 95% - hard limit, reject new memories
  }
};

// ============================================================================
// Token Budget Manager Class
// ============================================================================

export class TokenBudgetManager {
  constructor(config = DEFAULT_CONFIG) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.usage = {
      transcript: 0,
      memory: 0,
      episode: 0,
      working: 0,
      system: 0,
      query: 0,
      total: 0
    };
    this.history = [];
  }

  /**
   * Calculate available budget
   */
  getAvailableBudget() {
    return this.config.totalBudget - this.config.responseReserved - this.usage.total;
  }

  /**
   * Calculate budget usage percentage
   */
  getUsagePercentage() {
    return this.usage.total / this.config.totalBudget;
  }

  /**
   * Check if budget is exceeded
   */
  isBudgetExceeded() {
    return this.getUsagePercentage() >= this.config.compactionThresholds.hardLimit;
  }

  /**
   * Check if auto-compaction needed
   */
  needsCompaction() {
    return this.getUsagePercentage() >= this.config.compactionThresholds.compact;
  }

  /**
   * Check if warning should be shown
   */
  shouldWarn() {
    return this.getUsagePercentage() >= this.config.compactionThresholds.warn;
  }

  /**
   * Allocate tokens for a memory type
   */
  allocate(memoryType, priority = 'medium') {
    const baseBudget = this.config.availableBudget * this.config.memoryTypeBudgets[memoryType];
    const priorityMultiplier = this.config.priorityMultipliers[priority] || 0.5;
    const allocated = baseBudget * priorityMultiplier;
    
    return {
      memoryType,
      priority,
      allocated,
      remaining: this.getAvailableBudget() - allocated
    };
  }

  /**
   * Record token usage
   */
  recordUsage(memoryType, tokens) {
    if (!this.usage[memoryType]) {
      this.usage[memoryType] = 0;
    }
    this.usage[memoryType] += tokens;
    this.usage.total += tokens;
    
    // Record history
    this.history.push({
      timestamp: new Date().toISOString(),
      memoryType,
      tokens,
      totalUsage: this.usage.total,
      usagePercentage: this.getUsagePercentage()
    });
    
    // Keep only last 100 history entries
    if (this.history.length > 100) {
      this.history.shift();
    }
  }

  /**
   * Get budget status
   */
  getStatus() {
    return {
      totalBudget: this.config.totalBudget,
      responseReserved: this.config.responseReserved,
      availableBudget: this.getAvailableBudget(),
      usage: { ...this.usage },
      usagePercentage: this.getUsagePercentage(),
      isExceeded: this.isBudgetExceeded(),
      needsCompaction: this.needsCompaction(),
      shouldWarn: this.shouldWarn(),
      hardLimits: this.config.hardLimits
    };
  }

  /**
   * Enforce hard limits
   */
  enforceHardLimits() {
    const status = this.getStatus();
    
    if (status.isExceeded) {
      return {
        success: false,
        action: 'reject',
        reason: 'Budget exceeded hard limit',
        usage: status.usagePercentage
      };
    }
    
    if (status.needsCompaction) {
      return {
        success: true,
        action: 'compact',
        reason: 'Auto-compaction needed',
        usage: status.usagePercentage
      };
    }
    
    return {
      success: true,
      action: 'none',
      reason: 'Budget OK',
      usage: status.usagePercentage
    };
  }

  /**
   * Compress memories to fit budget
   */
  compressMemories(targetBudget) {
    const currentUsage = this.usage.total;
    const budgetGap = currentUsage - targetBudget;
    
    if (budgetGap <= 0) {
      return { success: true, compressed: 0 };
    }
    
    // Strategy: compress lowest priority memories first
    // In a real implementation, this would query the memory store
    const compressed = Math.floor(budgetGap / 500); // Assume 500 tokens per memory
    
    this.usage.total -= compressed * 500;
    
    return {
      success: true,
      compressed,
      bytesFreed: compressed * 500
    };
  }

  /**
   * Get budget history
   */
  getHistory(limit = 10) {
    return this.history.slice(-limit);
  }

  /**
   * Reset usage
   */
  resetUsage() {
    this.usage = {
      transcript: 0,
      memory: 0,
      episode: 0,
      working: 0,
      system: 0,
      query: 0,
      total: 0
    };
    this.history = [];
  }

  /**
   * Save state to file
   */
  save() {
    const data = {
      config: this.config,
      usage: this.usage,
      history: this.history,
      savedAt: new Date().toISOString()
    };
    
    mkdirSync(dirname(BUDGET_FILE), { recursive: true });
    writeFileSync(BUDGET_FILE, JSON.stringify(data, null, 2), 'utf-8');
  }

  /**
   * Load state from file
   */
  static load() {
    if (!existsSync(BUDGET_FILE)) {
      return new TokenBudgetManager();
    }
    
    const data = JSON.parse(readFileSync(BUDGET_FILE, 'utf-8'));
    const manager = new TokenBudgetManager(data.config);
    manager.usage = data.usage || manager.usage;
    manager.history = data.history || [];
    return manager;
  }
}

// ============================================================================
// Singleton Instance
// ============================================================================

let _budgetManagerInstance = null;

export function getBudgetManager() {
  if (!_budgetManagerInstance) {
    _budgetManagerInstance = TokenBudgetManager.load();
  }
  return _budgetManagerInstance;
}

// ============================================================================
// Helper Functions
// ============================================================================

/**
 * Calculate memory budget for a query
 */
export function calculateBudget({ query, topK = 10, contextBudget = 120000 }) {
  const queryTokens = estimateQueryTokens(query);
  const availableBudget = contextBudget - 20000; // Reserve 20k for response
  const avgMemoryTokens = 500;
  
  const maxMemories = Math.floor((availableBudget - queryTokens) / avgMemoryTokens);
  const limit = Math.min(topK, maxMemories);
  
  return {
    queryTokens,
    contextBudget,
    availableBudget,
    maxMemories,
    limit,
    avgMemoryTokens
  };
}

/**
 * Estimate query tokens
 */
function estimateQueryTokens(query) {
  // Simple estimation: 1 character ≈ 0.25 tokens
  return Math.floor(query.length * 0.25);
}

/**
 * Get budget status
 */
export function getBudgetStatus() {
  const manager = getBudgetManager();
  return manager.getStatus();
}

/**
 * Compress if needed
 */
export function compressIfNeeded(manager) {
  if (manager.needsCompaction()) {
    return manager.compressMemories(manager.config.totalBudget * 0.8);
  }
  return { success: true, compressed: 0 };
}

/**
 * Recalculate budgets
 */
export function recalculateBudgets(manager, newConfig) {
  manager.config = { ...manager.config, ...newConfig };
  manager.save();
  return manager.getStatus();
}

// ============================================================================
// Tool Functions
// ============================================================================

/**
 * memory_token_budget_status - Get current token budget status
 */
export function memory_token_budget_status() {
  const manager = getBudgetManager();
  return manager.getStatus();
}

/**
 * memory_token_budget_enforce - Enforce hard limits
 */
export function memory_token_budget_enforce() {
  const manager = getBudgetManager();
  return manager.enforceHardLimits();
}

/**
 * memory_token_budget_allocate - Allocate tokens for memory type
 */
export function memory_token_budget_allocate(memoryType, priority = 'medium') {
  const manager = getBudgetManager();
  return manager.allocate(memoryType, priority);
}

/**
 * memory_token_budget_record - Record token usage
 */
export function memory_token_budget_record(memoryType, tokens) {
  const manager = getBudgetManager();
  manager.recordUsage(memoryType, tokens);
  manager.save();
  return { success: true, usage: manager.getStatus() };
}

/**
 * memory_token_budget_compress - Compress memories to fit budget
 */
export function memory_token_budget_compress(targetBudget) {
  const manager = getBudgetManager();
  return manager.compressMemories(targetBudget);
}

/**
 * memory_token_budget_history - Get budget history
 */
export function memory_token_budget_history(limit = 10) {
  const manager = getBudgetManager();
  return manager.getHistory(limit);
}

/**
 * memory_token_budget_reset - Reset budget usage
 */
export function memory_token_budget_reset() {
  const manager = getBudgetManager();
  manager.resetUsage();
  manager.save();
  return { success: true };
}

/**
 * memory_token_budget_config - Get or update budget configuration
 */
export function memory_token_budget_config(newConfig = null) {
  const manager = getBudgetManager();
  
  if (newConfig) {
    manager.config = { ...manager.config, ...newConfig };
    manager.save();
    return { success: true, config: manager.config };
  }
  
  return { success: true, config: manager.config };
}
