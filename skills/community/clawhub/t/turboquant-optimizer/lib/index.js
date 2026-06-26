/**
 * TurboQuant Optimizer - Main Entry Point
 * 
 * Provides comprehensive token and memory optimization for OpenClaw
 * Inspired by Google's TurboQuant research
 */

const { TurboQuantOptimizer } = require('./turboquant-optimizer');
const { TokenBudgetManager } = require('./token-budget-manager');

// Default configuration
const DEFAULT_CONFIG = {
  maxTokens: 8000,
  compressionThreshold: 0.7,
  preserveRecent: 4,
  enableCheckpointing: true,
  deduplication: true,
  similarityThreshold: 0.85,
  compressToolResults: true,
  adaptiveBudget: true,
  budgetStrategy: 'task_complexity',
  reserveTokens: 1000,
  twoStageCompression: true,
  polarQuantization: true,
  qjltEncoding: false
};

/**
 * Create optimizer from OpenClaw config
 * @param {Object} openclawConfig - OpenClaw configuration
 * @returns {TurboQuantOptimizer} Configured optimizer
 */
function createFromConfig(openclawConfig = {}) {
  const skillConfig = openclawConfig.skills?.['turboquant-optimizer'] || {};
  return new TurboQuantOptimizer({
    ...DEFAULT_CONFIG,
    ...skillConfig
  });
}

/**
 * Quick optimize function
 * @param {Array} messages - Messages to optimize
 * @param {Object} options - Optimization options
 * @returns {Promise<Object>} Optimized result
 */
async function optimize(messages, options = {}) {
  const optimizer = new TurboQuantOptimizer(options);
  return optimizer.optimize(messages, options.context);
}

/**
 * Create token budget for a task
 * @param {Object} context - Task context
 * @param {Array} messages - Current messages
 * @param {Object} config - Budget configuration
 * @returns {Object} Token budget
 */
function createBudget(context, messages, config = {}) {
  const manager = new TokenBudgetManager(config);
  return manager.calculateBudget(context, messages);
}

/**
 * Analyze optimization potential
 * @param {Array} messages - Messages to analyze
 * @returns {Object} Analysis results
 */
function analyze(messages) {
  const optimizer = new TurboQuantOptimizer();
  
  const originalTokens = optimizer.estimateTokens(messages);
  
  // Simulate optimization
  const potentialSavings = {
    deduplication: Math.floor(originalTokens * 0.15),
    compression: Math.floor(originalTokens * 0.60),
    toolCaching: Math.floor(originalTokens * 0.10)
  };
  
  const totalPotential = Object.values(potentialSavings).reduce((a, b) => a + b, 0);
  
  return {
    originalTokens,
    potentialTokens: originalTokens - totalPotential,
    potentialSavings: totalPotential,
    savingsPercent: ((totalPotential / originalTokens) * 100).toFixed(1),
    breakdown: potentialSavings,
    recommendation: totalPotential / originalTokens > 0.5 
      ? 'High optimization potential - run turboquant-optimizer'
      : 'Moderate optimization potential'
  };
}

module.exports = {
  TurboQuantOptimizer,
  TokenBudgetManager,
  createFromConfig,
  optimize,
  createBudget,
  analyze,
  DEFAULT_CONFIG
};
