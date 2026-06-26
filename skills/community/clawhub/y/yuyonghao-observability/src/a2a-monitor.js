/**
 * A2A Monitor - Agent-to-Agent 通信监控
 * 
 * 功能:
 * - A2A 消息延迟追踪
 * - 消息成功率监控
 * - 消息大小统计
 * - 会话链路追踪
 * - 消息类型分析
 * 
 * @version 0.1.0
 * @author 小蒲萄 (Clawd)
 * @date 2026-03-20
 */

class A2AMonitor {
  constructor(metricsCollector, logger) {
    this.metrics = metricsCollector;
    this.logger = logger;
    
    // 活跃会话
    this.activeSessions = new Map(); // sessionId -> session info
    
    // 消息历史（内存缓存）
    this.messageHistory = [];
    this.maxHistorySize = 1000;
    
    // Agent 统计
    this.agentStats = new Map(); // agentId -> stats
    
    // 初始化指标
    this._initMetrics();
  }

  /**
   * 初始化 A2A 专用指标
   */
  _initMetrics() {
    // 消息计数
    this.metrics.counter('a2a.messages.total', 'Total A2A messages', {
      type: 'request|response|event',
      status: 'success|error|timeout'
    });
    
    // 消息延迟
    this.metrics.histogram('a2a.latency', 'A2A message latency (ms)', {
      buckets: [1, 5, 10, 50, 100, 500, 1000, 5000]
    });
    
    // 消息大小
    this.metrics.histogram('a2a.message.size', 'A2A message size (bytes)', {
      buckets: [100, 500, 1000, 5000, 10000, 50000, 100000]
    });
    
    // 活跃会话数
    this.metrics.gauge('a2a.sessions.active', 'Number of active A2A sessions');
    
    // Agent 连接数
    this.metrics.gauge('a2a.agents.connected', 'Number of connected agents');
    
    // 错误统计
    this.metrics.counter('a2a.errors.total', 'A2A errors', {
      error_type: 'timeout|network|parse|auth|other'
    });
    
    // 重试次数
    this.metrics.counter('a2a.retries.total', 'A2A message retries');
    
    // 消息队列深度
    this.metrics.gauge('a2a.queue.depth', 'A2A message queue depth');
  }

  /**
   * 记录消息发送
   */
  sendMessage(message) {
    const messageId = message.id || `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const timestamp = Date.now();
    const size = JSON.stringify(message).length;
    
    const messageMeta = {
      messageId,
      timestamp,
      type: message.type || 'unknown',
      from: message.from,
      to: message.to,
      sessionId: message.sessionId,
      size,
      status: 'sent'
    };

    // 记录指标
    this.metrics.histogram('a2a.message.size').observe(size);
    this.metrics.counter('a2a.messages.total').inc(1, { 
      type: message.type || 'unknown', 
      status: 'pending' 
    });

    // 初始化会话
    if (message.sessionId && !this.activeSessions.has(message.sessionId)) {
      this.activeSessions.set(message.sessionId, {
        sessionId: message.sessionId,
        createdAt: timestamp,
        messages: [],
        participants: new Set([message.from, message.to])
      });
      this.metrics.gauge('a2a.sessions.active').set(this.activeSessions.size);
    }

    // 添加到会话
    if (message.sessionId) {
      const session = this.activeSessions.get(message.sessionId);
      if (session) {
        session.messages.push(messageMeta);
      }
    }

    // 更新 Agent 统计
    this._updateAgentStats(message.from, 'sent');

    this.logger?.debug(`[A2A SEND] ${message.from} -> ${message.to}`, {
      messageId,
      type: message.type,
      size,
      sessionId: message.sessionId
    });

    return {
      ...messageMeta,
      end: (result) => this.receiveResponse(messageId, message, result)
    };
  }

  /**
   * 记录消息接收/响应
   */
  receiveResponse(messageId, originalMessage, result = null) {
    const endTime = Date.now();
    const startTime = originalMessage.timestamp || endTime;
    const latency = endTime - startTime;
    
    const isSuccess = !(result?.error || result?.isError);
    const status = isSuccess ? 'success' : 'error';
    const errorType = result?.error?.type || 'unknown';
    
    // 记录延迟
    this.metrics.histogram('a2a.latency').observe(latency);
    
    // 更新消息计数
    this.metrics.counter('a2a.messages.total').inc(1, {
      type: originalMessage.type || 'unknown',
      status
    });

    // 记录错误
    if (!isSuccess) {
      this.metrics.counter('a2a.errors.total').inc(1, { error_type: errorType });
    }

    // 更新 Agent 统计
    this._updateAgentStats(originalMessage.to, 'received', isSuccess);

    const responseMeta = {
      messageId,
      originalMessageId: originalMessage.id,
      latency,
      status,
      errorType: isSuccess ? null : errorType,
      timestamp: endTime
    };

    // 添加到历史
    this._addToHistory({
      ...responseMeta,
      from: originalMessage.from,
      to: originalMessage.to,
      type: originalMessage.type,
      sessionId: originalMessage.sessionId
    });

    this.logger?.debug(`[A2A RECEIVE] ${originalMessage.to} <- ${originalMessage.from}`, {
      messageId,
      latency,
      status,
      errorType: isSuccess ? null : errorType
    });

    // 记录性能日志
    if (latency > 1000) {
      this.logger?.warn(`[A2A SLOW] High latency detected: ${latency}ms`, {
        messageId,
        from: originalMessage.from,
        to: originalMessage.to,
        type: originalMessage.type
      });
    }

    return responseMeta;
  }

  /**
   * 记录消息事件（广播、通知等）
   */
  recordEvent(event) {
    const eventId = event.id || `evt-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const timestamp = Date.now();
    const size = JSON.stringify(event).length;
    
    this.metrics.counter('a2a.messages.total').inc(1, {
      type: 'event',
      status: 'success'
    });
    
    this.metrics.histogram('a2a.message.size').observe(size);

    this.logger?.debug(`[A2A EVENT] ${event.type}`, {
      eventId,
      from: event.from,
      size,
      timestamp
    });

    return {
      eventId,
      timestamp,
      size
    };
  }

  /**
   * 记录超时
   */
  recordTimeout(message, timeoutMs) {
    this.metrics.counter('a2a.errors.total').inc(1, { error_type: 'timeout' });
    this.metrics.counter('a2a.messages.total').inc(1, {
      type: message.type || 'unknown',
      status: 'timeout'
    });

    this.logger?.warn(`[A2A TIMEOUT] Message timeout after ${timeoutMs}ms`, {
      messageId: message.id,
      from: message.from,
      to: message.to,
      type: message.type
    });
  }

  /**
   * 记录重试
   */
  recordRetry(message, attemptNumber) {
    this.metrics.counter('a2a.retries.total').inc(1);
    
    this.logger?.debug(`[A2A RETRY] Retry attempt ${attemptNumber}`, {
      messageId: message.id,
      from: message.from,
      to: message.to,
      attempt: attemptNumber
    });
  }

  /**
   * 更新 Agent 统计
   */
  _updateAgentStats(agentId, action, success = true) {
    if (!this.agentStats.has(agentId)) {
      this.agentStats.set(agentId, {
        agentId,
        messagesSent: 0,
        messagesReceived: 0,
        errors: 0,
        lastActivity: Date.now()
      });
    }

    const stats = this.agentStats.get(agentId);
    stats.lastActivity = Date.now();

    if (action === 'sent') {
      stats.messagesSent++;
    } else if (action === 'received') {
      stats.messagesReceived++;
      if (!success) {
        stats.errors++;
      }
    }

    // 更新连接数
    this.metrics.gauge('a2a.agents.connected').set(this.agentStats.size);
  }

  /**
   * 添加到历史记录
   */
  _addToHistory(record) {
    this.messageHistory.push(record);
    
    if (this.messageHistory.length > this.maxHistorySize) {
      this.messageHistory.shift();
    }
  }

  /**
   * 结束会话
   */
  endSession(sessionId) {
    const session = this.activeSessions.get(sessionId);
    if (session) {
      session.endedAt = Date.now();
      session.duration = session.endedAt - session.createdAt;
      
      this.activeSessions.delete(sessionId);
      this.metrics.gauge('a2a.sessions.active').set(this.activeSessions.size);

      this.logger?.debug(`[A2A SESSION END] ${sessionId}`, {
        duration: session.duration,
        messageCount: session.messages.length
      });

      return session;
    }
    return null;
  }

  /**
   * 获取会话信息
   */
  getSession(sessionId) {
    return this.activeSessions.get(sessionId);
  }

  /**
   * 获取 Agent 统计
   */
  getAgentStats(agentId) {
    return this.agentStats.get(agentId);
  }

  /**
   * 获取所有 Agent 统计
   */
  getAllAgentStats() {
    return Array.from(this.agentStats.values());
  }

  /**
   * 获取消息历史
   */
  getMessageHistory(options = {}) {
    let history = [...this.messageHistory];
    
    if (options.sessionId) {
      history = history.filter(h => h.sessionId === options.sessionId);
    }
    
    if (options.agentId) {
      history = history.filter(h => h.from === options.agentId || h.to === options.agentId);
    }
    
    if (options.type) {
      history = history.filter(h => h.type === options.type);
    }
    
    if (options.status) {
      history = history.filter(h => h.status === options.status);
    }
    
    if (options.since) {
      history = history.filter(h => h.timestamp >= options.since);
    }
    
    if (options.limit) {
      history = history.slice(-options.limit);
    }
    
    return history;
  }

  /**
   * 获取聚合统计
   */
  getAggregateStats() {
    const now = Date.now();
    const last24h = now - 24 * 60 * 60 * 1000;
    
    const recentMessages = this.messageHistory.filter(m => m.timestamp >= last24h);
    
    const successCount = recentMessages.filter(m => m.status === 'success').length;
    const errorCount = recentMessages.filter(m => m.status === 'error').length;
    const timeoutCount = recentMessages.filter(m => m.status === 'timeout').length;
    const totalCount = recentMessages.length;
    
    const avgLatency = totalCount > 0
      ? recentMessages.reduce((sum, m) => sum + (m.latency || 0), 0) / totalCount
      : 0;
    
    const successRate = totalCount > 0
      ? (successCount / totalCount) * 100
      : 100;

    return {
      totalMessages24h: totalCount,
      successCount,
      errorCount,
      timeoutCount,
      successRate,
      avgLatency,
      activeSessions: this.activeSessions.size,
      connectedAgents: this.agentStats.size
    };
  }

  /**
   * 导出 Prometheus 格式指标
   */
  exportPrometheus() {
    const lines = [];
    const stats = this.getAggregateStats();
    
    lines.push('# HELP agent_a2a_messages_total Total A2A messages');
    lines.push('# TYPE agent_a2a_messages_total counter');
    lines.push(`agent_a2a_messages_total ${stats.totalMessages24h}`);
    
    lines.push('# HELP agent_a2a_latency A2A message latency (ms)');
    lines.push('# TYPE agent_a2a_latency histogram');
    
    lines.push('# HELP agent_a2a_success_rate A2A message success rate');
    lines.push('# TYPE agent_a2a_success_rate gauge');
    lines.push(`agent_a2a_success_rate ${stats.successRate.toFixed(2)}`);
    
    lines.push('# HELP agent_a2a_sessions_active Active A2A sessions');
    lines.push('# TYPE agent_a2a_sessions_active gauge');
    lines.push(`agent_a2a_sessions_active ${stats.activeSessions}`);
    
    lines.push('# HELP agent_a2a_agents_connected Connected agents');
    lines.push('# TYPE agent_a2a_agents_connected gauge');
    lines.push(`agent_a2a_agents_connected ${stats.connectedAgents}`);
    
    return lines.join('\n');
  }

  /**
   * 重置统计
   */
  reset() {
    this.activeSessions.clear();
    this.messageHistory = [];
    this.agentStats.clear();
    
    this.logger?.info('[A2A MONITOR] Stats reset');
  }
}

module.exports = { A2AMonitor };