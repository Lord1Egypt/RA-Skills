/**
 * Token Budget Manager
 * 
 * Implements adaptive token budgeting with TurboQuant-inspired efficiency.
 * Dynamically allocates tokens between context and response based on task complexity.
 */

class TokenBudgetManager {
  constructor(config = {}) {
    this.config = {
      maxTokens: config.maxTokens || 8000,
      reserveTokens: config.reserveTokens || 1000,
      safetyMargin: config.safetyMargin || 0.95,
      ...config
    };
    
    this.budgetHistory = [];
    this.taskProfiles = new Map();
  }

  /**
   * Calculate optimal token budget for a task
   * @param {Object} context - Task context
   * @param {Array} messages - Current messages
   * @returns {Object} Budget allocation
   */
  calculateBudget(context, messages) {
    const taskType = this._classifyTask(context);
    const complexity = this._assessComplexity(context, messages);
    const availableTokens = (this.config.maxTokens - this.config.reserveTokens) * this.config.safetyMargin;
    
    // Base allocation by task type
    const baseAllocation = this._getBaseAllocation(taskType);
    
    // Adjust for complexity
    const adjustedAllocation = this._adjustForComplexity(baseAllocation, complexity);
    
    // Calculate actual token limits
    const budget = {
      taskType,
      complexity,
      totalAvailable: Math.floor(availableTokens),
      context: Math.floor(availableTokens * adjustedAllocation.context),
      response: Math.floor(availableTokens * adjustedAllocation.response),
      overhead: Math.floor(availableTokens * adjustedAllocation.overhead),
      metadata: {
        confidence: this._calculateConfidence(context),
        estimatedTurns: complexity.estimatedTurns,
        reasoning: adjustedAllocation.reasoning
      }
    };
    
    // Record for learning
    this._recordBudget(budget);
    
    return budget;
  }

  /**
   * Classify task type from context
   * @private
   */
  _classifyTask(context) {
    const indicators = {
      coding: /\b(code|function|script|program|implement|debug|error|compile|build|deploy)\b/i,
      analysis: /\b(analyze|compare|evaluate|assess|review|research|study|investigate)\b/i,
      creative: /\b(write|create|design|draft|compose|generate|story|poem|article)\b/i,
      reasoning: /\b(explain|why|how does|what if|reason|logic|prove|deduce)\b/i,
      planning: /\b(plan|schedule|organize|workflow|process|steps|timeline|roadmap)\b/i,
      data: /\b(data|csv|json|table|calculate|compute|statistics|metrics|report)\b/i,
      conversation: /\b(chat|talk|discuss|opinion|thoughts|feel|think|believe)\b/i
    };
    
    const text = `${context.query || ''} ${context.recentMessages?.join(' ') || ''}`;
    const scores = {};
    
    for (const [type, pattern] of Object.entries(indicators)) {
      const matches = (text.match(pattern) || []).length;
      scores[type] = matches;
    }
    
    // Get highest scoring type
    const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1]);
    return sorted[0][1] > 0 ? sorted[0][0] : 'general';
  }

  /**
   * Assess task complexity
   * @private
   */
  _assessComplexity(context, messages) {
    const text = `${context.query || ''} ${JSON.stringify(messages)}`;
    
    const factors = {
      // Length factor
      length: Math.min(1, text.length / 5000),
      
      // Vocabulary complexity
      vocabulary: this._calculateVocabularyComplexity(text),
      
      // Structural complexity
      structure: this._calculateStructuralComplexity(context),
      
      // Historical complexity (from past similar tasks)
      historical: this._getHistoricalComplexity(context)
    };
    
    const score = (factors.length * 0.2 + 
                   factors.vocabulary * 0.2 + 
                   factors.structure * 0.3 + 
                   factors.historical * 0.3);
    
    return {
      score: Math.min(1, score),
      level: score < 0.3 ? 'simple' : score < 0.6 ? 'moderate' : 'complex',
      estimatedTurns: score < 0.3 ? 1 : score < 0.6 ? 2 : 3,
      factors
    };
  }

  /**
   * Get base allocation for task type
   * @private
   */
  _getBaseAllocation(taskType) {
    const allocations = {
      coding: { context: 0.4, response: 0.5, overhead: 0.1, reasoning: 'Code needs balanced context for understanding and space for output' },
      analysis: { context: 0.6, response: 0.3, overhead: 0.1, reasoning: 'Analysis requires more context for comprehensive evaluation' },
      creative: { context: 0.3, response: 0.6, overhead: 0.1, reasoning: 'Creative tasks need maximum space for generated content' },
      reasoning: { context: 0.5, response: 0.4, overhead: 0.1, reasoning: 'Reasoning tasks need context for premises and space for explanation' },
      planning: { context: 0.55, response: 0.35, overhead: 0.1, reasoning: 'Planning requires context for constraints and space for plans' },
      data: { context: 0.5, response: 0.4, overhead: 0.1, reasoning: 'Data tasks need context for datasets and space for analysis' },
      conversation: { context: 0.35, response: 0.55, overhead: 0.1, reasoning: 'Conversations prioritize natural flow over context depth' },
      general: { context: 0.45, response: 0.45, overhead: 0.1, reasoning: 'Balanced allocation for general tasks' }
    };
    
    return allocations[taskType] || allocations.general;
  }

  /**
   * Adjust allocation based on complexity
   * @private
   */
  _adjustForComplexity(base, complexity) {
    const adjusted = { ...base };
    
    if (complexity.level === 'complex') {
      // Complex tasks need more context
      adjusted.context = Math.min(0.7, base.context + 0.15);
      adjusted.response = 1 - adjusted.context - base.overhead;
      adjusted.reasoning += ' | Increased context for complexity';
    } else if (complexity.level === 'simple') {
      // Simple tasks can have more response space
      adjusted.context = Math.max(0.2, base.context - 0.1);
      adjusted.response = 1 - adjusted.context - base.overhead;
      adjusted.reasoning += ' | Decreased context for simplicity';
    }
    
    return adjusted;
  }

  /**
   * Calculate vocabulary complexity
   * @private
   */
  _calculateVocabularyComplexity(text) {
    const words = text.toLowerCase().match(/\b\w+\b/g) || [];
    const uniqueWords = new Set(words);
    
    // Technical terms indicate complexity
    const technicalTerms = /\b(algorithm|implementation|architecture|framework|protocol|infrastructure|optimization|asynchronous|parallel|distributed)\b/gi;
    const technicalCount = (text.match(technicalTerms) || []).length;
    
    // Long words indicate complexity
    const longWords = words.filter(w => w.length > 8).length;
    
    return Math.min(1, (technicalCount * 0.1) + (longWords / words.length));
  }

  /**
   * Calculate structural complexity
   * @private
   */
  _calculateStructuralComplexity(context) {
    let score = 0;
    
    // Multi-step indicators
    if (/\b(step|first|then|next|finally|after|before)\b/i.test(context.query || '')) {
      score += 0.3;
    }
    
    // Conditional logic
    if (/\b(if|when|unless|while|during|depending)\b/i.test(context.query || '')) {
      score += 0.2;
    }
    
    // Multiple questions
    const questionCount = (context.query || '').match(/\?/g)?.length || 0;
    score += Math.min(0.3, questionCount * 0.1);
    
    return Math.min(1, score);
  }

  /**
   * Get historical complexity for similar tasks
   * @private
   */
  _getHistoricalComplexity(context) {
    const taskKey = this._generateTaskKey(context);
    const history = this.taskProfiles.get(taskKey);
    
    if (!history || history.length < 3) {
      return 0.5; // Default moderate complexity
    }
    
    // Calculate average from history
    const avgComplexity = history.reduce((sum, h) => sum + h.complexity, 0) / history.length;
    return avgComplexity;
  }

  /**
   * Calculate confidence in budget allocation
   * @private
   */
  _calculateConfidence(context) {
    let confidence = 0.7; // Base confidence
    
    // More confident with more context
    if (context.recentMessages && context.recentMessages.length > 5) {
      confidence += 0.15;
    }
    
    // Less confident with very short queries
    if ((context.query || '').length < 20) {
      confidence -= 0.1;
    }
    
    return Math.min(0.95, confidence);
  }

  /**
   * Generate task key for history tracking
   * @private
   */
  _generateTaskKey(context) {
    const normalized = (context.query || '')
      .toLowerCase()
      .replace(/[^\w\s]/g, '')
      .split(/\s+/)
      .slice(0, 5)
      .join('_');
    return normalized || 'general';
  }

  /**
   * Record budget for learning
   * @private
   */
  _recordBudget(budget) {
    this.budgetHistory.push({
      timestamp: Date.now(),
      ...budget
    });
    
    // Keep history manageable
    if (this.budgetHistory.length > 100) {
      this.budgetHistory.shift();
    }
    
    // Update task profile
    const taskKey = budget.taskType;
    if (!this.taskProfiles.has(taskKey)) {
      this.taskProfiles.set(taskKey, []);
    }
    this.taskProfiles.get(taskKey).push({
      complexity: budget.complexity.score,
      timestamp: Date.now()
    });
  }

  /**
   * Get budget statistics
   * @returns {Object} Statistics
   */
  getStats() {
    if (this.budgetHistory.length === 0) {
      return { message: 'No budget history yet' };
    }
    
    const recent = this.budgetHistory.slice(-20);
    
    return {
      totalBudgets: this.budgetHistory.length,
      avgContextAllocation: recent.reduce((sum, b) => sum + b.context, 0) / recent.length,
      avgResponseAllocation: recent.reduce((sum, b) => sum + b.response, 0) / recent.length,
      taskTypeDistribution: this._getTaskDistribution(),
      complexityDistribution: this._getComplexityDistribution()
    };
  }

  _getTaskDistribution() {
    const counts = {};
    for (const budget of this.budgetHistory) {
      counts[budget.taskType] = (counts[budget.taskType] || 0) + 1;
    }
    return counts;
  }

  _getComplexityDistribution() {
    const counts = { simple: 0, moderate: 0, complex: 0 };
    for (const budget of this.budgetHistory) {
      counts[budget.complexity.level]++;
    }
    return counts;
  }
}

module.exports = { TokenBudgetManager };
