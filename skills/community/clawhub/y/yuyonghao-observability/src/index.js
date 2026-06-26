/**
 * Observability System - 可观测性系统主入口
 * 
 * 功能:
 * - 结构化日志（logger.js）
 * - 性能指标（metrics.js）
 * - 链路追踪（tracer.js）
 * - Dashboard（dashboard.js）
 * - 告警管理（alert-manager.js）
 * - LLM监控（llm-monitor.js）
 * - MCP监控（mcp-monitor.js）
 * - A2A监控（a2a-monitor.js）
 * 
 * @version 0.2.0
 * @author 小蒲萄 (Clawd)
 */

const { ObservabilityLogger } = require('./logger');
const { MetricsCollector } = require('./metrics');
const { Tracer } = require('./tracer');
const { AlertManager } = require('./alert-manager');
const { LLMMonitor } = require('./llm-monitor');
const { MCPToolsMonitor } = require('./mcp-monitor');
const { A2AMonitor } = require('./a2a-monitor');

class ObservabilitySystem {
  constructor(options = {}) {
    this.options = {
      // 日志配置
      logging: {
        level: 'info',
        console: true,
        file: true,
        ...options.logging
      },
      // 指标配置
      metrics: {
        enabled: true,
        prefix: 'agent',
        autoReport: false,
        ...options.metrics
      },
      // 追踪配置
      tracing: {
        enabled: true,
        sampleRate: 1.0,
        maxTraces: 1000,
        ...options.tracing
      },
      // 告警配置
      alerts: {
        enabled: true,
        checkInterval: 30000,
        createDefaultRules: true,
        ...options.alerts
      },
      // LLM监控配置
      llm: {
        enabled: true,
        ...options.llm
      },
      // MCP监控配置
      mcp: {
        enabled: true,
        ...options.mcp
      },
      // A2A监控配置
      a2a: {
        enabled: true,
        ...options.a2a
      }
    };

    // 初始化日志
    this.logger = new ObservabilityLogger(this.options.logging);

    // 初始化指标
    this.metrics = new MetricsCollector(this.options.metrics);

    // 初始化追踪器
    this.tracer = new Tracer({
      logger: this.logger,
      sampleRate: this.options.tracing.sampleRate,
      maxTraces: this.options.tracing.maxTraces
    });

    // 初始化告警管理器
    if (this.options.alerts.enabled) {
      this.alertManager = new AlertManager({
        metricsCollector: this.metrics,
        logger: this.logger,
        checkInterval: this.options.alerts.checkInterval
      });
      
      if (this.options.alerts.createDefaultRules) {
        this.alertManager.createDefaultRules();
      }
    }

    // 初始化 LLM 监控
    if (this.options.llm.enabled) {
      this.llmMonitor = new LLMMonitor(this.metrics, this.logger);
    }

    // 初始化 MCP 监控
    if (this.options.mcp.enabled) {
      this.mcpMonitor = new MCPToolsMonitor(this.metrics, this.logger);
    }

    // 初始化 A2A 监控
    if (this.options.a2a.enabled) {
      this.a2aMonitor = new A2AMonitor(this.metrics, this.logger);
    }

    // 当前追踪
    this.activeTraces = new Map();

    this.logger.info('可观测性系统初始化完成', {
      logging: this.options.logging,
      metrics: this.options.metrics,
      tracing: this.options.tracing,
      alerts: this.options.alerts.enabled,
      llm: this.options.llm.enabled,
      mcp: this.options.mcp.enabled,
      a2a: this.options.a2a.enabled
    });
  }

  /**
   * 开始追踪
   */
  startTrace(operation, meta = {}) {
    const traceId = `trace-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const spanId = `span-${Math.random().toString(36).substr(2, 9)}`;
    const startTime = Date.now();

    const trace = {
      traceId,
      spanId,
      operation,
      startTime,
      meta,
      spans: []
    };

    this.activeTraces.set(traceId, trace);
    this.logger.info(`[TRACE START] ${operation}`, { traceId, spanId, ...meta });

    // 同时记录到 tracer
    if (this.options.tracing.enabled) {
      this.tracer.startTrace(operation, { traceId, ...meta });
    }

    return {
      traceId,
      spanId,
      end: (result = null) => this.endTrace(traceId, result),
      addSpan: (op, spanMeta = {}) => this.addSpan(traceId, op, spanMeta)
    };
  }

  /**
   * 添加子 span
   */
  addSpan(traceId, operation, meta = {}) {
    const trace = this.activeTraces.get(traceId);
    if (!trace) {
      this.logger.warn(`Trace not found: ${traceId}`);
      return null;
    }

    const spanId = `span-${Math.random().toString(36).substr(2, 9)}`;
    const startTime = Date.now();

    const span = {
      spanId,
      operation,
      startTime,
      meta
    };

    trace.spans.push(span);
    this.logger.debug(`[SPAN START] ${operation}`, { traceId, spanId, ...meta });

    return {
      spanId,
      end: (result = null) => {
        span.endTime = Date.now();
        span.duration = span.endTime - span.startTime;
        span.result = result;
        this.logger.debug(`[SPAN END] ${operation}`, {
          traceId,
          spanId,
          duration: span.duration,
          ...meta
        });
        return span;
      }
    };
  }

  /**
   * 结束追踪
   */
  endTrace(traceId, result = null) {
    const trace = this.activeTraces.get(traceId);
    if (!trace) {
      this.logger.warn(`Trace not found: ${traceId}`);
      return null;
    }

    const endTime = Date.now();
    const duration = endTime - trace.startTime;

    trace.endTime = endTime;
    trace.duration = duration;
    trace.result = result;

    this.logger.info(`[TRACE END] ${trace.operation}`, {
      traceId,
      duration,
      spans: trace.spans.length,
      ...trace.meta
    });

    // 记录指标
    this.metrics.histogram('calls.latency').observe(duration);
    this.metrics.counter('calls.total').inc();

    // 从活跃追踪中移除
    this.activeTraces.delete(traceId);

    return {
      traceId,
      duration,
      spans: trace.spans.length,
      operation: trace.operation
    };
  }

  /**
   * 记录错误
   */
  recordError(error, context = {}) {
    this.logger.error('Error occurred', {
      error: error.message,
      stack: error.stack,
      ...context
    });

    this.metrics.counter('errors.total').inc();
  }

  /**
   * 包装函数（自动追踪）
   */
  wrap(fn, operation) {
    const self = this;
    return async function(...args) {
      const trace = self.startTrace(operation);
      
      try {
        const result = await fn.apply(this, args);
        trace.end(result);
        return result;
      } catch (error) {
        self.recordError(error, {
          traceId: trace.traceId,
          operation
        });
        trace.end({ error: error.message });
        throw error;
      }
    };
  }

  /**
   * 获取系统状态
   */
  getStatus() {
    const status = {
      activeTraces: this.activeTraces.size,
      metrics: this.metrics.getSummary(),
      logDir: this.logger.getLogDir()
    };

    // 添加追踪器统计
    if (this.tracer) {
      status.tracing = this.tracer.getStats();
    }

    // 添加告警统计
    if (this.alertManager) {
      status.alerts = this.alertManager.getStats();
    }

    // 添加 LLM 统计
    if (this.llmMonitor) {
      status.llm = this.llmMonitor.getAggregateStats();
    }

    // 添加 MCP 统计
    if (this.mcpMonitor) {
      status.mcp = this.mcpMonitor.getAggregateStats();
    }

    // 添加 A2A 统计
    if (this.a2aMonitor) {
      status.a2a = this.a2aMonitor.getAggregateStats();
    }

    return status;
  }

  /**
   * 导出指标
   */
  exportMetrics(format = 'json') {
    if (format === 'prometheus') {
      let output = this.metrics.toPrometheus();
      
      // 添加各模块的 Prometheus 指标
      if (this.llmMonitor) {
        output += '\n' + this.llmMonitor.exportPrometheus();
      }
      if (this.mcpMonitor) {
        output += '\n' + this.mcpMonitor.exportPrometheus();
      }
      if (this.a2aMonitor) {
        output += '\n' + this.a2aMonitor.exportPrometheus();
      }
      
      return output;
    }
    return this.metrics.getMetrics();
  }

  /**
   * 导出日志
   */
  exportLogs(options = {}) {
    return this.logger.exportLogs(options);
  }

  /**
   * 获取追踪
   */
  getTrace(traceId) {
    return this.tracer?.getTrace(traceId);
  }

  /**
   * 获取最近追踪
   */
  getRecentTraces(limit = 10) {
    return this.tracer?.getRecentTraces(limit);
  }

  /**
   * 导出追踪
   */
  exportTrace(traceId) {
    return this.tracer?.exportTrace(traceId);
  }

  /**
   * 记录 LLM 调用开始
   */
  startLLMCall(sessionId, model, options = {}) {
    return this.llmMonitor?.startCall(sessionId, model, options);
  }

  /**
   * 记录 MCP 工具调用开始
   */
  startMCPCall(serverName, toolName, params = {}) {
    return this.mcpMonitor?.startCall(serverName, toolName, params);
  }

  /**
   * 记录 A2A 消息发送
   */
  sendA2AMessage(message) {
    return this.a2aMonitor?.sendMessage(message);
  }

  /**
   * 记录 A2A 事件
   */
  recordA2AEvent(event) {
    return this.a2aMonitor?.recordEvent(event);
  }

  /**
   * 添加告警规则
   */
  addAlertRule(config) {
    return this.alertManager?.addRule(config);
  }

  /**
   * 手动触发告警
   */
  fireAlert(ruleId, value, message) {
    return this.alertManager?.fireAlert(ruleId, value, message);
  }

  /**
   * 获取告警历史
   */
  getAlertHistory(options = {}) {
    return this.alertManager?.getHistory(options);
  }

  /**
   * 关闭系统
   */
  shutdown() {
    this.logger.info('可观测性系统关闭中...');
    
    this.alertManager?.stop();
    this.metrics.stopAutoReport?.();
    
    this.logger.info('可观测性系统已关闭');
  }
}

// 导出所有模块
module.exports = {
  ObservabilitySystem,
  ObservabilityLogger,
  MetricsCollector,
  Tracer,
  AlertManager,
  LLMMonitor,
  MCPToolsMonitor,
  A2AMonitor
};