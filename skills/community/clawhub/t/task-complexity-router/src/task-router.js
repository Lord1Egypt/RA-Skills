/**
 * Task Router — Public version
 * Detects task complexity and routes to appropriate model
 * Basic scaffolding — no self-learning (that's private)
 */

class TaskRouter {
  constructor(config = {}) {
    this.config = {
      defaultModel: config.defaultModel || 'local',
      escalationModel: config.escalationModel || 'sonnet',
      heavyModel: config.heavyModel || 'opus',
      ...config
    };

    // Complexity patterns — users can add their own
    this.rules = [
      // Simple — stays local
      { 
        name: 'greeting',
        pattern: /^(hi|hey|hello|mhmm|yeah|ok|thanks|good|nice)\.?$/i,
        model: 'local',
        reason: 'Simple acknowledgment'
      },
      { 
        name: 'short_question',
        pattern: /^(what|where|when|who|how)\b.{0,30}\?$/i,
        model: 'local',
        reason: 'Short question'
      },
      {
        name: 'status_check',
        pattern: /\b(status|check|list|show|count|time)\b/i,
        model: 'local',
        reason: 'Status or listing request'
      },

      // Moderate — escalate to mid-tier
      {
        name: 'analysis',
        pattern: /\b(analyze|compare|research|investigate|evaluate|review)\b/i,
        model: 'sonnet',
        reason: 'Analysis task'
      },
      {
        name: 'creation',
        pattern: /\b(create|build|generate|design|write|draft)\b/i,
        model: 'sonnet',
        reason: 'Creation task'
      },
      {
        name: 'explanation',
        pattern: /\b(explain|describe|summarize|break down|walk me through)\b/i,
        model: 'sonnet',
        reason: 'Explanation request'
      },

      // Complex — escalate to heavy model
      {
        name: 'architecture',
        pattern: /\b(architect|system design|framework|infrastructure|refactor)\b/i,
        model: 'opus',
        reason: 'Architecture task'
      },
      {
        name: 'long_writing',
        pattern: /\b(write.{0,20}(book|chapter|article|guide|report))\b/i,
        model: 'opus',
        reason: 'Long-form writing'
      },
      {
        name: 'financial',
        pattern: /\b(trade|trading|invest|financial|budget|revenue|profit)\b/i,
        model: 'opus',
        reason: 'Financial decision'
      },
      {
        name: 'security',
        pattern: /\b(security|vulnerability|encrypt|auth|permission|delete|destroy)\b/i,
        model: 'opus',
        reason: 'Security-sensitive task'
      }
    ];

    // User-defined custom rules (loaded from config)
    if (config.customRules) {
      for (const rule of config.customRules) {
        this.addRule(rule.name, new RegExp(rule.pattern, rule.flags || 'i'), rule.model, rule.reason);
      }
    }
  }

  /**
   * Route a message to the appropriate model
   * @param {string} message - User message
   * @param {object} context - Optional context (e.g., current conversation topic)
   * @returns {object} Routing decision
   */
  route(message, context = {}) {
    const matched = [];

    // Check all rules
    for (const rule of this.rules) {
      if (rule.pattern.test(message)) {
        matched.push(rule);
      }
    }

    // No rules matched — use default
    if (matched.length === 0) {
      // Fallback: short messages go local, long messages escalate
      if (message.split(/\s+/).length <= 5) {
        return {
          model: this.config.defaultModel,
          reason: 'Short message, default model',
          confidence: 0.5,
          matched: []
        };
      } else {
        return {
          model: this.config.escalationModel,
          reason: 'Longer message, escalated to mid-tier',
          confidence: 0.4,
          matched: []
        };
      }
    }

    // Multiple rules matched — use highest tier
    const modelPriority = { 'opus': 3, 'sonnet': 2, 'local': 1 };
    const bestMatch = matched.reduce((best, current) => {
      const currentPriority = modelPriority[current.model] || 0;
      const bestPriority = modelPriority[best.model] || 0;
      return currentPriority > bestPriority ? current : best;
    });

    // Context overrides
    if (context.forceModel) {
      return {
        model: context.forceModel,
        reason: `User override: ${context.forceModel}`,
        confidence: 1.0,
        matched: matched.map(m => m.name)
      };
    }

    return {
      model: bestMatch.model,
      reason: bestMatch.reason,
      confidence: Math.min(0.9, 0.5 + (matched.length * 0.1)),
      matched: matched.map(m => m.name)
    };
  }

  /**
   * Add a custom routing rule
   */
  addRule(name, pattern, model, reason) {
    this.rules.push({ name, pattern, model, reason });
  }

  /**
   * Remove a routing rule by name
   */
  removeRule(name) {
    this.rules = this.rules.filter(r => r.name !== name);
  }

  /**
   * Get all current rules (for UI display)
   */
  getRules() {
    return this.rules.map(r => ({
      name: r.name,
      pattern: r.pattern.source,
      model: r.model,
      reason: r.reason
    }));
  }

  /**
   * Export rules to JSON (for saving config)
   */
  exportRules() {
    return this.rules.map(r => ({
      name: r.name,
      pattern: r.pattern.source,
      flags: r.pattern.flags,
      model: r.model,
      reason: r.reason
    }));
  }
}

module.exports = { TaskRouter };
