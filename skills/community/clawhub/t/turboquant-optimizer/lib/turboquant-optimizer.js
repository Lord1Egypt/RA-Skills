/**
 * TurboQuant Optimizer for OpenClaw
 * 
 * Implements advanced compression techniques inspired by Google's TurboQuant:
 * - Two-stage compression (PolarQuant + QJL)
 * - Semantic deduplication
 * - Adaptive token budgeting
 * - Conversation checkpointing
 * 
 * @module turboquant-optimizer
 * @version 2.0.0
 * @author MincoSoft Technologies
 */

const crypto = require('crypto');
const EventEmitter = require('events');

/**
 * TurboQuant Optimizer - Main Class
 */
class TurboQuantOptimizer extends EventEmitter {
  /**
   * Create a new TurboQuantOptimizer instance
   * @param {Object} config - Configuration options
   */
  constructor(config = {}) {
    super();
    
    this.config = {
      // Session-level config
      maxTokens: config.maxTokens || 8000,
      compressionThreshold: config.compressionThreshold || 0.7,
      preserveRecent: config.preserveRecent || 4,
      enableCheckpointing: config.enableCheckpointing !== false,
      
      // Message-level config
      deduplication: config.deduplication !== false,
      similarityThreshold: config.similarityThreshold || 0.85,
      compressToolResults: config.compressToolResults !== false,
      
      // Token-level config
      adaptiveBudget: config.adaptiveBudget !== false,
      budgetStrategy: config.budgetStrategy || 'task_complexity',
      reserveTokens: config.reserveTokens || 1000,
      
      // Advanced features
      twoStageCompression: config.twoStageCompression !== false,
      polarQuantization: config.polarQuantization !== false,
      qjltEncoding: config.qjltEncoding || false,
      
      ...config
    };
    
    // Initialize caches and state
    this.toolResultCache = new Map();
    this.checkpoints = [];
    this.semanticIndex = new Map();
    
    // Statistics
    this.stats = {
      totalOptimizations: 0,
      totalTokensSaved: 0,
      totalOriginalTokens: 0,
      compressionRatio: 0,
      deduplicationHits: 0,
      checkpointSaves: 0,
      cacheHits: 0,
      avgResponseTime: 0
    };
    
    // Task complexity detection patterns
    this.taskPatterns = {
      simpleQA: /^(what|who|when|where|why|how|is|are|can|do|does)/i,
      codeGen: /\b(code|function|script|program|implement|write)\b/i,
      analysis: /\b(analyze|compare|evaluate|assess|review|explain)\b/i,
      multiStep: /\b(step|first|then|next|finally|workflow|process)\b/i
    };
  }

  /**
   * Main optimization entry point
   * Applies all optimization strategies in sequence
   * 
   * @param {Array} messages - Original message array
   * @param {Object} context - Additional context (task type, model, etc.)
   * @returns {Promise<Object>} Optimized result with metadata
   */
  async optimize(messages, context = {}) {
    const startTime = Date.now();
    const originalTokens = this.estimateTokens(messages);
    
    this.emit('optimization:start', { originalTokens, messageCount: messages.length });
    
    let optimized = [...messages];
    const stages = [];
    
    // Stage 1: Semantic deduplication
    if (this.config.deduplication) {
      const beforeCount = optimized.length;
      optimized = await this._deduplicateMessages(optimized);
      stages.push({
        name: 'deduplication',
        messagesBefore: beforeCount,
        messagesAfter: optimized.length,
        tokensSaved: this.estimateTokens(messages) - this.estimateTokens(optimized)
      });
    }
    
    // Stage 2: Tool result compression
    if (this.config.compressToolResults) {
      const beforeTokens = this.estimateTokens(optimized);
      optimized = await this._compressToolResults(optimized);
      stages.push({
        name: 'tool_compression',
        tokensBefore: beforeTokens,
        tokensAfter: this.estimateTokens(optimized),
        tokensSaved: beforeTokens - this.estimateTokens(optimized)
      });
    }
    
    // Stage 3: Two-stage compression (TurboQuant-inspired)
    if (this.config.twoStageCompression && 
        this.estimateTokens(optimized) > this.config.maxTokens * this.config.compressionThreshold) {
      const beforeTokens = this.estimateTokens(optimized);
      optimized = await this._twoStageCompress(optimized, context);
      stages.push({
        name: 'turboquant_compression',
        tokensBefore: beforeTokens,
        tokensAfter: this.estimateTokens(optimized),
        tokensSaved: beforeTokens - this.estimateTokens(optimized)
      });
    }
    
    // Stage 4: Adaptive token budgeting
    if (this.config.adaptiveBudget) {
      optimized = await this._applyAdaptiveBudget(optimized, context);
      stages.push({
        name: 'adaptive_budget',
        strategy: this._detectTaskType(context),
        allocation: this._calculateBudgetAllocation(context)
      });
    }
    
    // Update statistics
    const finalTokens = this.estimateTokens(optimized);
    const tokensSaved = originalTokens - finalTokens;
    const duration = Date.now() - startTime;
    
    this.stats.totalOptimizations++;
    this.stats.totalTokensSaved += tokensSaved;
    this.stats.totalOriginalTokens += originalTokens;
    this.stats.compressionRatio = this.stats.totalOriginalTokens > 0 
      ? (this.stats.totalTokensSaved / this.stats.totalOriginalTokens)
      : 0;
    this.stats.avgResponseTime = 
      (this.stats.avgResponseTime * (this.stats.totalOptimizations - 1) + duration) 
      / this.stats.totalOptimizations;
    
    // Create checkpoint if enabled
    if (this.config.enableCheckpointing) {
      this._createCheckpoint(optimized, stages);
    }
    
    const result = {
      messages: optimized,
      metadata: {
        originalTokens,
        finalTokens,
        tokensSaved,
        savingsPercent: originalTokens > 0 ? (tokensSaved / originalTokens * 100).toFixed(2) : 0,
        compressionRatio: finalTokens / originalTokens,
        duration,
        stages,
        checkpointId: this.checkpoints.length > 0 ? this.checkpoints[this.checkpoints.length - 1].id : null
      }
    };
    
    this.emit('optimization:complete', result.metadata);
    
    return result;
  }

  /**
   * Two-stage compression (TurboQuant-inspired)
   * Stage 1: PolarQuant-style primary compression
   * Stage 2: QJL-style residual error correction
   * 
   * @private
   */
  async _twoStageCompress(messages, context) {
    const currentTokens = this.estimateTokens(messages);
    
    if (currentTokens <= this.config.maxTokens * this.config.compressionThreshold) {
      return messages;
    }
    
    // Split messages
    const splitIndex = Math.max(0, messages.length - this.config.preserveRecent);
    const olderMessages = messages.slice(0, splitIndex);
    const recentMessages = messages.slice(splitIndex);
    
    // Stage 1: Primary compression (PolarQuant-inspired)
    // Rotate and quantize to capture main concepts
    const primarySummary = await this._polarQuantCompress(olderMessages);
    
    // Stage 2: Residual correction (QJL-inspired)
    // Encode residuals to sign bits
    const residualCorrection = this.config.qjltEncoding 
      ? await this._qjltEncode(olderMessages, primarySummary)
      : null;
    
    // Build compressed context
    const compressedContext = [
      {
        role: 'system',
        name: 'turboquant_optimizer',
        content: this._buildCompressedContext(primarySummary, residualCorrection)
      },
      ...recentMessages
    ];
    
    return compressedContext;
  }

  /**
   * PolarQuant-inspired compression
   * Converts message "vectors" to polar coordinates (magnitude + direction)
   * 
   * @private
   */
  async _polarQuantCompress(messages) {
    // Extract key concepts and their "magnitudes" (importance)
    const concepts = [];
    
    for (const msg of messages) {
      const text = this._extractText(msg.content);
      const importance = this._calculateImportance(msg);
      
      // Extract key facts and decisions
      if (msg.role === 'user') {
        const requests = this._extractRequests(text);
        concepts.push(...requests.map(r => ({ 
          type: 'request', 
          content: r, 
          magnitude: importance,
          angle: this._semanticHash(r) // "direction" in concept space
        })));
      } else if (msg.role === 'assistant') {
        const actions = this._extractActions(text);
        concepts.push(...actions.map(a => ({ 
          type: 'action', 
          content: a, 
          magnitude: importance,
          angle: this._semanticHash(a)
        })));
      }
    }
    
    // Cluster similar concepts (quantize by angle)
    const clusters = this._clusterByAngle(concepts);
    
    // Build summary from cluster representatives
    return {
      conceptCount: concepts.length,
      clusterCount: clusters.length,
      clusters: clusters.slice(0, 10).map(c => ({
        representative: c.representative,
        magnitude: c.totalMagnitude,
        count: c.items.length
      })),
      totalMessages: messages.length
    };
  }

  /**
   * QJL-inspired encoding (simplified)
   * Encodes residuals to sign bits
   * 
   * @private
   */
  async _qjltEncode(originalMessages, primarySummary) {
    // Simplified QJL: Identify what's missing from primary summary
    const originalText = originalMessages.map(m => this._extractText(m.content)).join(' ');
    const summaryText = JSON.stringify(primarySummary);
    
    // Calculate "residual" information
    const residualTokens = this._extractResidualTokens(originalText, summaryText);
    
    // Encode to sign bits (+1 for present, -1 for absent in context)
    return {
      residualCount: residualTokens.length,
      signBits: residualTokens.map(t => this._semanticHash(t) % 2 === 0 ? 1 : -1),
      coverage: 1 - (residualTokens.length / originalText.split(' ').length)
    };
  }

  /**
   * Semantic deduplication of messages
   * Groups similar messages and keeps representatives
   * 
   * @private
   */
  async _deduplicateMessages(messages) {
    const groups = [];
    const processed = new Set();
    
    for (let i = 0; i < messages.length; i++) {
      if (processed.has(i)) continue;
      
      const group = [messages[i]];
      processed.add(i);
      
      // Find similar messages
      for (let j = i + 1; j < messages.length; j++) {
        if (processed.has(j)) continue;
        
        const similarity = this._calculateSimilarity(messages[i], messages[j]);
        if (similarity >= this.config.similarityThreshold) {
          group.push(messages[j]);
          processed.add(j);
          this.stats.deduplicationHits++;
        }
      }
      
      groups.push(group);
    }
    
    // Return representative from each group
    return groups.map(g => this._selectRepresentative(g));
  }

  /**
   * Compress tool results through caching and summarization
   * 
   * @private
   */
  async _compressToolResults(messages) {
    return messages.map(msg => {
      // Check if this is a tool result message
      if (msg.role === 'tool' || msg.tool_calls || msg.name === 'tool') {
        const content = this._extractText(msg.content);
        const hash = this._hashContent(content);
        
        // Check cache
        if (this.toolResultCache.has(hash)) {
          this.stats.cacheHits++;
          return {
            ...msg,
            content: `[Cached result: ${this.toolResultCache.get(hash).summary}]`
          };
        }
        
        // Compress and cache
        const compressed = this._compressToolContent(content);
        this.toolResultCache.set(hash, { summary: compressed, timestamp: Date.now() });
        
        // Evict old entries if cache too large
        this._evictCacheIfNeeded();
        
        return { ...msg, content: compressed };
      }
      
      return msg;
    });
  }

  /**
   * Apply adaptive token budgeting based on task type
   * 
   * @private
   */
  async _applyAdaptiveBudget(messages, context) {
    const taskType = this._detectTaskType(context);
    const allocation = this._calculateBudgetAllocation(taskType);
    
    const maxContextTokens = (this.config.maxTokens - this.config.reserveTokens) * allocation.context;
    const currentTokens = this.estimateTokens(messages);
    
    if (currentTokens <= maxContextTokens) {
      return messages;
    }
    
    // Progressive compression until within budget
    let compressed = messages;
    let iterations = 0;
    const maxIterations = 3;
    
    while (this.estimateTokens(compressed) > maxContextTokens && iterations < maxIterations) {
      compressed = await this._twoStageCompress(compressed, context);
      iterations++;
    }
    
    return compressed;
  }

  /**
   * Detect task type from context
   * @private
   */
  _detectTaskType(context) {
    const text = context.query || context.lastMessage || '';
    
    if (this.taskPatterns.multiStep.test(text)) return 'multiStep';
    if (this.taskPatterns.codeGen.test(text)) return 'codeGen';
    if (this.taskPatterns.analysis.test(text)) return 'analysis';
    if (this.taskPatterns.simpleQA.test(text)) return 'simpleQA';
    
    return 'general';
  }

  /**
   * Calculate budget allocation for task type
   * @private
   */
  _calculateBudgetAllocation(taskType) {
    const allocations = {
      simpleQA: { context: 0.3, response: 0.7 },
      codeGen: { context: 0.5, response: 0.5 },
      analysis: { context: 0.7, response: 0.3 },
      multiStep: { context: 0.6, response: 0.4 },
      general: { context: 0.5, response: 0.5 }
    };
    
    return allocations[taskType] || allocations.general;
  }

  /**
   * Create a conversation checkpoint
   * @private
   */
  _createCheckpoint(messages, stages) {
    const checkpoint = {
      id: crypto.randomUUID(),
      timestamp: Date.now(),
      messageCount: messages.length,
      tokenCount: this.estimateTokens(messages),
      stages,
      hash: this._hashContent(JSON.stringify(messages))
    };
    
    this.checkpoints.push(checkpoint);
    this.stats.checkpointSaves++;
    
    // Limit checkpoints
    if (this.checkpoints.length > 10) {
      this.checkpoints.shift();
    }
    
    this.emit('checkpoint:created', checkpoint);
  }

  /**
   * Restore from checkpoint
   * @param {string} checkpointId - Checkpoint ID to restore
   * @returns {Array|null} Restored messages or null
   */
  restoreCheckpoint(checkpointId) {
    const checkpoint = this.checkpoints.find(c => c.id === checkpointId);
    if (!checkpoint) return null;
    
    this.emit('checkpoint:restored', checkpoint);
    return checkpoint;
  }

  /**
   * Estimate token count from messages
   * @param {Array} messages - Message array
   * @returns {number} Estimated tokens
   */
  estimateTokens(messages) {
    if (!Array.isArray(messages)) return 0;
    
    return messages.reduce((sum, msg) => {
      const content = this._extractText(msg.content);
      // Industry standard: ~4 chars per token
      return sum + Math.ceil(content.length / 4) + 4; // +4 for message overhead
    }, 0);
  }

  /**
   * Get detailed statistics
   * @returns {Object} Statistics object
   */
  getDetailedStats() {
    const efficiencyScore = Math.min(100, 
      (this.stats.compressionRatio * 100) + 
      (this.stats.cacheHits * 2) +
      (this.stats.deduplicationHits)
    );
    
    return {
      ...this.stats,
      efficiencyScore: efficiencyScore.toFixed(2),
      cacheSize: this.toolResultCache.size,
      checkpointCount: this.checkpoints.length,
      config: this.config
    };
  }

  // Helper methods...
  
  _extractText(content) {
    if (typeof content === 'string') return content;
    if (Array.isArray(content)) {
      return content.filter(c => c.type === 'text').map(c => c.text).join(' ');
    }
    return JSON.stringify(content);
  }
  
  _hashContent(content) {
    return crypto.createHash('sha256').update(content).digest('hex').slice(0, 16);
  }
  
  _semanticHash(text) {
    return text.split('').reduce((hash, char) => {
      return ((hash << 5) - hash) + char.charCodeAt(0) | 0;
    }, 0);
  }
  
  _calculateImportance(msg) {
    let importance = 1.0;
    
    // Recent messages more important
    importance *= 1.0;
    
    // Tool results slightly less important
    if (msg.role === 'tool') importance *= 0.8;
    
    // User questions high importance
    if (msg.role === 'user' && /\?/.test(this._extractText(msg.content))) {
      importance *= 1.2;
    }
    
    return importance;
  }
  
  _calculateSimilarity(msg1, msg2) {
    const text1 = this._extractText(msg1.content).toLowerCase();
    const text2 = this._extractText(msg2.content).toLowerCase();
    
    // Simple Jaccard similarity
    const set1 = new Set(text1.split(/\s+/));
    const set2 = new Set(text2.split(/\s+/));
    
    const intersection = new Set([...set1].filter(x => set2.has(x)));
    const union = new Set([...set1, ...set2]);
    
    return intersection.size / union.size;
  }
  
  _selectRepresentative(group) {
    // Select most informative message from group
    return group.reduce((best, msg) => {
      const score = this._extractText(msg.content).length;
      return score > this._extractText(best.content).length ? msg : best;
    });
  }
  
  _extractRequests(text) {
    const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
    return sentences.filter(s => 
      /\b(need|want|help|create|make|build|write|generate)\b/i.test(s)
    );
  }
  
  _extractActions(text) {
    const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
    return sentences.filter(s => 
      /\b(created|done|completed|finished|built|wrote|generated)\b/i.test(s) ||
      s.includes('✅')
    );
  }
  
  _clusterByAngle(concepts) {
    const clusters = [];
    const processed = new Set();
    
    for (const concept of concepts) {
      if (processed.has(concept)) continue;
      
      const cluster = {
        items: [concept],
        representative: concept,
        totalMagnitude: concept.magnitude
      };
      processed.add(concept);
      
      // Find similar angles
      for (const other of concepts) {
        if (processed.has(other)) continue;
        
        const angleDiff = Math.abs(concept.angle - other.angle);
        if (angleDiff < 1000) { // Similar direction
          cluster.items.push(other);
          cluster.totalMagnitude += other.magnitude;
          processed.add(other);
        }
      }
      
      clusters.push(cluster);
    }
    
    return clusters.sort((a, b) => b.totalMagnitude - a.totalMagnitude);
  }
  
  _buildCompressedContext(primarySummary, residualCorrection) {
    let context = `📋 [Context: ${primarySummary.totalMessages} messages → ${primarySummary.clusterCount} concept clusters]`;
    
    context += '\n\nKey Concepts:\n';
    primarySummary.clusters.forEach((c, i) => {
      context += `  ${i + 1}. ${c.representative.content.slice(0, 100)}`;
      if (c.count > 1) context += ` (${c.count} similar)`;
      context += '\n';
    });
    
    if (residualCorrection) {
      context += `\n[Residual coverage: ${(residualCorrection.coverage * 100).toFixed(1)}%]`;
    }
    
    return context;
  }
  
  _extractResidualTokens(original, summary) {
    const originalWords = new Set(original.toLowerCase().split(/\s+/));
    const summaryWords = new Set(summary.toLowerCase().split(/\s+/));
    return [...originalWords].filter(w => !summaryWords.has(w) && w.length > 3);
  }
  
  _compressToolContent(content) {
    if (content.length < 500) return content;
    
    // Truncate with summary
    const lines = content.split('\n');
    const summary = lines.slice(0, 10).join('\n');
    return `${summary}\n\n... [${lines.length - 10} more lines, ${content.length} chars total] ...`;
  }
  
  _evictCacheIfNeeded() {
    if (this.toolResultCache.size > 100) {
      const oldest = [...this.toolResultCache.entries()]
        .sort((a, b) => a[1].timestamp - b[1].timestamp)[0];
      this.toolResultCache.delete(oldest[0]);
    }
  }
}

module.exports = { TurboQuantOptimizer };
