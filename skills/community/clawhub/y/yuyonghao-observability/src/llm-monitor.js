/**
 * LLM Monitor - LLM 调用监控模块
 * 
 * 功能:
 * - Token 使用统计（按模型、按用户）
 * - 延迟追踪（首 token 时间、总延迟）
 * - 错误率监控
 * - 成本估算
 * - 速率限制追踪
 * 
 * @version 0.1.0
 * @author 小蒲萄 (Clawd)
 * @date 2026-03-19
 */

class LLMMonitor {
  constructor(metricsCollector, logger) {
    this.metrics = metricsCollector;
    this.logger = logger;
    
    // 模型成本配置（每 1M tokens，USD）
    this.modelCosts = {
      // 阿里云
      'qwen3.5-plus': { input: 0.002, output: 0.006 },
      'qwen-max': { input: 0.004, output: 0.012 },
      // 小米摩塔
      'mimo-v2-pro': { input: 0.005, output: 0.015 },
      'mimo-v2-flash': { input: 0.001, output: 0.003 },
      // OpenAI
      'gpt-4': { input: 0.03, output: 0.06 },
      'gpt-3.5-turbo': { input: 0.0005, output: 0.0015 },
      // Anthropic
      'claude-sonnet-4': { input: 0.003, output: 0.015 },
      'claude-opus-4': { input: 0.015, output: 0.075 },
    };

    // 会话级统计
    this.sessionStats = new Map(); // sessionId -> stats
    
    // 初始化指标
    this._initMetrics();
  }

  /**
   * 初始化 LLM 专用指标
   */
  _initMetrics() {
    // Token 使用（分模型）
    this.metrics.counter('llm.tokens.input', 'LLM input tokens by model', {
      model: 'string'
    });
    
    this.metrics.counter('llm.tokens.output', 'LLM output tokens by model', {
      model: 'string'
    });
    
    this.metrics.counter('llm.tokens.total', 'LLM total tokens by model', {
      model: 'string'
    });
    
    // 延迟指标
    this.metrics.histogram('llm.latency.first_token', 'Time to first token (ms)', {
      buckets: [10, 50, 100, 200, 500, 1000, 2000]
    });
    
    this.metrics.histogram('llm.latency.total', 'Total LLM latency (ms)', {
      buckets: [100, 500, 1000, 2000, 5000, 10000, 30000]
    });
    
    // 调用指标
    this.metrics.counter('llm.calls.total', 'Total LLM calls by model', {
      model: 'string',
      status: 'success|error'
    });
    
    this.metrics.counter('llm.errors.total', 'LLM errors by type', {
      error_type: 'string',
      model: 'string'
    });
    
    // 成本指标
    this.metrics.gauge('llm.cost.total', 'Total estimated cost (USD)');
    
    // 速率限制
    this.metrics.gauge('llm.rate_limit.remaining', 'Rate limit remaining requests');
    this.metrics.gauge('llm.rate_limit.reset', 'Rate limit reset timestamp');
    
    // 模型使用分布
    this.metrics.gauge('llm.models.active', 'Number of active models in use');
  }

  /**
   * 记录 LLM 调用开始
   */
  startCall(sessionId, model, options = {}) {
    const callId = `llm-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const startTime = Date.now();
    
    // 初始化会话统计
    if (!this.sessionStats.has(sessionId)) {
      this.sessionStats.set(sessionId, {
        totalCalls: 0,
        totalTokens: 0,
        totalCost: 0,
        errors: 0,
        lastCall: null
      });
    }
    
    const stats = this.sessionStats.get(sessionId);
    stats.totalCalls++;
    stats.lastCall = startTime;
    
    // 记录调用开始时间
    const callMeta = {
      callId,
      sessionId,
      model,
      startTime,
      options
    };
    
    this.logger.debug(`[LLM START] ${model}`, { callId, sessionId, ...options });
    
    return {
      callId,
      sessionId,
      model,
      startTime,
      end: (result) => this.endCall(callId, sessionId, model, startTime, result)
    };
  }

  /**
   * 记录 LLM 调用结束
   */
  endCall(callId, sessionId, model, startTime, result = null) {
    const endTime = Date.now();
    const duration = endTime - startTime;
    
    // 提取 token 信息
    const usage = result?.usage || {
      prompt_tokens: 0,
      completion_tokens: 0,
      total_tokens: 0
    };
    
    const inputTokens = usage.prompt_tokens || usage.input_tokens || 0;
    const outputTokens = usage.completion_tokens || usage.output_tokens || 0;
    const totalTokens = usage.total_tokens || (inputTokens + outputTokens);
    
    // 记录指标
    this.metrics.counter('llm.tokens.input').inc(inputTokens, { model });
    this.metrics.counter('llm.tokens.output').inc(outputTokens, { model });
    this.metrics.counter('llm.tokens.total').inc(totalTokens, { model });
    
    this.metrics.histogram('llm.latency.total').observe(duration);
    
    // 记录调用结果
    const status = result?.error ? 'error' : 'success';
    this.metrics.counter('llm.calls.total').inc(1, { model, status });
    
    // 更新会话统计
    const sessionStats = this.sessionStats.get(sessionId);
    if (sessionStats) {
      sessionStats.totalTokens += totalTokens;
      if (result?.error) {
        sessionStats.errors++;
        this.metrics.counter('llm.errors.total').inc(1, {
          error_type: result.error.type || 'unknown',
          model
        });
      }
    }
    
    // 计算成本
    const cost = this._calculateCost(model, inputTokens, outputTokens);
    if (sessionStats) {
      sessionStats.totalCost += cost;
    }
    this.metrics.gauge('llm.cost.total').set(sessionStats?.totalCost || 0);
    
    // 日志记录
    const logData = {
      callId,
      model,
      duration,
      inputTokens,
      outputTokens,
      totalTokens,
      cost,
      status
    };
    
    if (result?.error) {
      this.logger.error(`[LLM ERROR] ${model}`, { ...logData, error: result.error });
    } else {
      this.logger.info(`[LLM END] ${model}`, logData);
    }
    
    return logData;
  }

  /**
   * 记录首 token 时间（流式响应）
   */
  recordFirstToken(callId, model, timeToFirstToken) {
    this.metrics.histogram('llm.latency.first_token').observe(timeToFirstToken);
    this.logger.debug(`[LLM FIRST TOKEN] ${model}: ${timeToFirstToken}ms`, { callId });
  }

  /**
   * 记录速率限制
   */
  recordRateLimit(remaining, resetTimestamp) {
    this.metrics.gauge('llm.rate_limit.remaining').set(remaining);
    this.metrics.gauge('llm.rate_limit.reset').set(resetTimestamp);
    
    if (remaining < 10) {
      this.logger.warn(`[LLM RATE LIMIT] Low remaining: ${remaining}`, {
        remaining,
        resetTimestamp
      });
    }
  }

  /**
   * 计算成本
   */
  _calculateCost(model, inputTokens, outputTokens) {
    const costConfig = this.modelCosts[model];
    if (!costConfig) {
      // 默认成本（未知模型）
      return (inputTokens + outputTokens) * 0.000002; // $0.002 / 1M tokens
    }
    
    const inputCost = (inputTokens / 1000000) * costConfig.input;
    const outputCost = (outputTokens / 1000000) * costConfig.output;
    
    return inputCost + outputCost;
  }

  /**
   * 获取会话统计
   */
  getSessionStats(sessionId) {
    return this.sessionStats.get(sessionId) || null;
  }

  /**
   * 获取所有会话汇总统计
   */
  getAggregateStats() {
    const aggregate = {
      totalCalls: 0,
      totalTokens: 0,
      totalCost: 0,
      totalErrors: 0,
      activeModels: new Set()
    };
    
    for (const [sessionId, stats] of this.sessionStats.entries()) {
      aggregate.totalCalls += stats.totalCalls;
      aggregate.totalTokens += stats.totalTokens;
      aggregate.totalCost += stats.totalCost;
      aggregate.totalErrors += stats.errors;
    }
    
    // 统计活跃模型
    for (const counter of this.metrics.counters.values()) {
      if (counter.name.includes('llm.calls.total')) {
        for (const label of Object.keys(counter.labels)) {
          aggregate.activeModels.add(label);
        }
      }
    }
    
    return {
      ...aggregate,
      activeModels: Array.from(aggregate.activeModels)
    };
  }

  /**
   * 导出 Prometheus 格式指标
   */
  exportPrometheus() {
    const lines = [];
    
    lines.push('# HELP agent_llm_tokens_input LLM input tokens by model');
    lines.push('# TYPE agent_llm_tokens_input counter');
    
    lines.push('# HELP agent_llm_tokens_output LLM output tokens by model');
    lines.push('# TYPE agent_llm_tokens_output counter');
    
    lines.push('# HELP agent_llm_latency_total Total LLM latency (ms)');
    lines.push('# TYPE agent_llm_latency_total histogram');
    
    lines.push('# HELP agent_llm_cost_total Total estimated cost (USD)');
    lines.push('# TYPE agent_llm_cost_total gauge');
    
    // 添加实际值
    const cost = this.metrics.gauges.get('agent.llm.cost.total');
    if (cost) {
      lines.push(`agent_llm_cost_total ${cost.value.toFixed(6)}`);
    }
    
    return lines.join('\n');
  }

  /**
   * 重置统计（用于每日清零）
   */
  resetDaily() {
    this.logger.info('[LLM MONITOR] Resetting daily stats');
    
    // 保留历史数据，只重置计数器
    for (const counter of this.metrics.counters.values()) {
      if (counter.name.includes('llm.')) {
        counter.value = 0;
      }
    }
  }
}

module.exports = { LLMMonitor };
