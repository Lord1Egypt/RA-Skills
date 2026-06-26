/**
 * MCP Tools Monitor - MCP 工具调用监控
 * 
 * 功能:
 * - 工具调用统计（按工具名、按 Server）
 * - 执行时间追踪
 * - 成功率监控
 * - 参数大小统计
 * - 结果大小统计
 * 
 * @version 0.1.0
 * @author 小蒲萄 (Clawd)
 * @date 2026-03-19
 */

class MCPToolsMonitor {
  constructor(metricsCollector, logger) {
    this.metrics = metricsCollector;
    this.logger = logger;
    
    // 工具调用历史（内存缓存，最近 1000 次）
    this.callHistory = [];
    this.maxHistorySize = 1000;
    
    // 按 Server 分组统计
    this.serverStats = new Map(); // serverName -> stats
    
    // 活跃调用（用于存储调用开始时的信息）
    this.activeCalls = new Map(); // callId -> callMeta
    
    // 初始化指标
    this._initMetrics();
  }

  /**
   * 初始化 MCP 工具指标
   */
  _initMetrics() {
    // 调用次数
    this.metrics.counter('mcp.calls.total', 'Total MCP tool calls', {
      tool: 'string',
      server: 'string',
      status: 'success|error'
    });
    
    // 执行时间
    this.metrics.histogram('mcp.execution.time', 'MCP tool execution time (ms)', {
      buckets: [1, 5, 10, 50, 100, 500, 1000, 5000]
    });
    
    // 参数大小
    this.metrics.histogram('mcp.params.size', 'MCP tool params size (bytes)', {
      buckets: [10, 100, 500, 1000, 5000, 10000]
    });
    
    // 结果大小
    this.metrics.histogram('mcp.result.size', 'MCP tool result size (bytes)', {
      buckets: [10, 100, 1000, 5000, 10000, 50000, 100000]
    });
    
    // 错误统计
    this.metrics.counter('mcp.errors.total', 'MCP tool errors', {
      tool: 'string',
      error_type: 'string'
    });
    
    // Server 健康度
    this.metrics.gauge('mcp.server.health', 'MCP server health score', {
      server: 'string'
    });
    
    // 活跃工具数
    this.metrics.gauge('mcp.tools.active', 'Number of active MCP tools');
  }

  /**
   * 记录工具调用开始
   */
  startCall(serverName, toolName, params = {}) {
    const callId = `mcp-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const startTime = Date.now();
    const paramsSize = JSON.stringify(params).length;
    
    // 初始化 Server 统计
    if (!this.serverStats.has(serverName)) {
      this.serverStats.set(serverName, {
        totalCalls: 0,
        successfulCalls: 0,
        failedCalls: 0,
        totalExecutionTime: 0,
        lastCall: null,
        tools: new Set()
      });
    }
    
    const serverStats = this.serverStats.get(serverName);
    serverStats.totalCalls++;
    serverStats.lastCall = startTime;
    serverStats.tools.add(toolName);
    
    // 记录调用开始
    const callMeta = {
      callId,
      serverName,
      toolName,
      startTime,
      paramsSize
    };
    
    // 存储活跃调用
    this.activeCalls.set(callId, callMeta);
    
    this.logger.debug(`[MCP CALL START] ${serverName}/${toolName}`, {
      callId,
      paramsSize
    });
    
    // 记录指标
    this.metrics.histogram('mcp.params.size').observe(paramsSize);
    
    return {
      callId,
      serverName,
      toolName,
      startTime,
      paramsSize: paramsSize,
      end: (result) => this.endCall(callId, serverName, toolName, startTime, result)
    };
  }

  /**
   * 记录工具调用结束
   */
  endCall(callId, serverName, toolName, startTime, result = null) {
    const endTime = Date.now();
    const executionTime = endTime - startTime;
    
    // 获取调用开始时的信息
    const callMeta = this.activeCalls.get(callId);
    const paramsSize = callMeta ? callMeta.paramsSize : 0;
    
    // 清理活跃调用
    this.activeCalls.delete(callId);
    
    const resultSize = result ? JSON.stringify(result).length : 0;
    const isSuccess = !(result?.error || result?.isError);
    
    // 记录指标
    this.metrics.histogram('mcp.execution.time').observe(executionTime);
    this.metrics.histogram('mcp.result.size').observe(resultSize);
    
    const status = isSuccess ? 'success' : 'error';
    this.metrics.counter('mcp.calls.total').inc(1, { tool: toolName, server: serverName, status });
    
    // 更新 Server 统计
    const serverStats = this.serverStats.get(serverName);
    if (serverStats) {
      serverStats.successfulCalls += isSuccess ? 1 : 0;
      serverStats.failedCalls += isSuccess ? 0 : 1;
      serverStats.totalExecutionTime += executionTime;
      
      // 计算健康度（成功率 * 100）
      const healthScore = serverStats.totalCalls > 0
        ? (serverStats.successfulCalls / serverStats.totalCalls) * 100
        : 100;
      this.metrics.gauge('mcp.server.health').set(healthScore, { server: serverName });
    }
    
    // 更新活跃工具数
    const activeTools = new Set();
    for (const stats of this.serverStats.values()) {
      for (const tool of stats.tools) {
        activeTools.add(`${stats.serverName}/${tool}`);
      }
    }
    this.metrics.gauge('mcp.tools.active').set(activeTools.size);
    
    // 记录错误
    if (!isSuccess) {
      const errorType = result?.error?.code || result?.error?.type || 'unknown';
      this.metrics.counter('mcp.errors.total').inc(1, { tool: toolName, error_type: errorType });
      
      this.logger.error(`[MCP CALL ERROR] ${serverName}/${toolName}`, {
        callId,
        executionTime,
        error: result?.error
      });
    } else {
      this.logger.debug(`[MCP CALL END] ${serverName}/${toolName}`, {
        callId,
        executionTime,
        resultSize,
        status
      });
    }
    
    // 添加到历史记录
    this._addToHistory({
      callId,
      timestamp: startTime,
      serverName,
      toolName,
      executionTime,
      paramsSize,
      resultSize,
      status,
      error: result?.error
    });
    
    return {
      callId,
      executionTime,
      resultSize,
      status,
      success: isSuccess
    };
  }

  /**
   * 添加到历史记录
   */
  _addToHistory(callRecord) {
    this.callHistory.push(callRecord);
    
    // 保持历史记录大小
    if (this.callHistory.length > this.maxHistorySize) {
      this.callHistory.shift();
    }
  }

  /**
   * 获取 Server 统计
   */
  getServerStats(serverName) {
    const stats = this.serverStats.get(serverName);
    if (!stats) return null;
    
    return {
      ...stats,
      tools: Array.from(stats.tools),
      avgExecutionTime: stats.totalCalls > 0
        ? stats.totalExecutionTime / stats.totalCalls
        : 0,
      successRate: stats.totalCalls > 0
        ? (stats.successfulCalls / stats.totalCalls) * 100
        : 100
    };
  }

  /**
   * 获取所有 Server 汇总
   */
  getAggregateStats() {
    const aggregate = {
      totalCalls: 0,
      successfulCalls: 0,
      failedCalls: 0,
      totalExecutionTime: 0,
      servers: [],
      tools: new Set()
    };
    
    for (const [serverName, stats] of this.serverStats.entries()) {
      aggregate.totalCalls += stats.totalCalls;
      aggregate.successfulCalls += stats.successfulCalls;
      aggregate.failedCalls += stats.failedCalls;
      aggregate.totalExecutionTime += stats.totalExecutionTime;
      aggregate.servers.push(serverName);
      for (const tool of stats.tools) {
        aggregate.tools.add(`${serverName}/${tool}`);
      }
    }
    
    return {
      ...aggregate,
      tools: Array.from(aggregate.tools),
      avgExecutionTime: aggregate.totalCalls > 0
        ? aggregate.totalExecutionTime / aggregate.totalCalls
        : 0,
      overallSuccessRate: aggregate.totalCalls > 0
        ? (aggregate.successfulCalls / aggregate.totalCalls) * 100
        : 100
    };
  }

  /**
   * 获取最近调用历史
   */
  getRecentHistory(limit = 50) {
    return this.callHistory.slice(-limit);
  }

  /**
   * 查询调用历史（按条件过滤）
   */
  queryHistory(filters = {}) {
    let results = [...this.callHistory];
    
    if (filters.serverName) {
      results = results.filter(r => r.serverName === filters.serverName);
    }
    
    if (filters.toolName) {
      results = results.filter(r => r.toolName === filters.toolName);
    }
    
    if (filters.status) {
      results = results.filter(r => r.status === filters.status);
    }
    
    if (filters.minExecutionTime) {
      results = results.filter(r => r.executionTime >= filters.minExecutionTime);
    }
    
    if (filters.since) {
      results = results.filter(r => r.timestamp >= filters.since);
    }
    
    return results;
  }

  /**
   * 导出 Prometheus 格式指标
   */
  exportPrometheus() {
    const lines = [];
    
    lines.push('# HELP agent_mcp_calls_total Total MCP tool calls');
    lines.push('# TYPE agent_mcp_calls_total counter');
    
    lines.push('# HELP agent_mcp_execution_time MCP tool execution time (ms)');
    lines.push('# TYPE agent_mcp_execution_time histogram');
    
    lines.push('# HELP agent_mcp_server_health MCP server health score');
    lines.push('# TYPE agent_mcp_server_health gauge');
    
    // 添加实际值
    for (const [serverName, stats] of this.serverStats.entries()) {
      const healthScore = stats.totalCalls > 0
        ? (stats.successfulCalls / stats.totalCalls) * 100
        : 100;
      lines.push(`agent_mcp_server_health{server="${serverName}"} ${healthScore.toFixed(2)}`);
    }
    
    return lines.join('\n');
  }

  /**
   * 重置统计
   */
  reset() {
    this.logger.info('[MCP MONITOR] Resetting stats');
    
    this.serverStats.clear();
    this.callHistory = [];
  }
}

module.exports = { MCPToolsMonitor };
