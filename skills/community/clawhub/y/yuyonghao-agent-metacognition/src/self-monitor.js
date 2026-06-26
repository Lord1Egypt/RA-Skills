/**
 * 自我监控模块
 * 负责执行状态监控、决策过程追踪、置信度评估和异常检测
 */

const EventEmitter = require('events');

/**
 * 决策记录类
 */
class DecisionRecord {
  constructor(data) {
    this.id = data.id || `decision-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    this.decision = data.decision;
    this.confidence = data.confidence || 0.5;
    this.reasoning = data.reasoning || '';
    this.timestamp = data.timestamp || Date.now();
    this.context = data.context || {};
    this.alternatives = data.alternatives || [];
    this.outcome = null;
    this.outcomeTimestamp = null;
  }

  setOutcome(outcome) {
    this.outcome = outcome;
    this.outcomeTimestamp = Date.now();
  }

  getDuration() {
    if (!this.outcomeTimestamp) return null;
    return this.outcomeTimestamp - this.timestamp;
  }
}

/**
 * 会话监控类
 */
class MonitoringSession {
  constructor(sessionId, options = {}) {
    this.sessionId = sessionId;
    this.startTime = Date.now();
    this.endTime = null;
    this.decisions = [];
    this.events = [];
    this.metrics = {
      totalDecisions: 0,
      avgConfidence: 0,
      successCount: 0,
      failureCount: 0,
      anomalyCount: 0
    };
    this.status = 'active'; // active, paused, completed, error
    this.options = {
      maxDecisions: options.maxDecisions || 1000,
      anomalyThreshold: options.anomalyThreshold || 0.1,
      ...options
    };
  }

  addDecision(decisionData) {
    if (this.decisions.length >= this.options.maxDecisions) {
      this.decisions.shift(); // 移除最旧的决策
    }
    
    const decision = new DecisionRecord(decisionData);
    this.decisions.push(decision);
    this.metrics.totalDecisions++;
    this._updateMetrics();
    
    return decision;
  }

  addEvent(eventType, data) {
    this.events.push({
      type: eventType,
      data,
      timestamp: Date.now()
    });
  }

  _updateMetrics() {
    if (this.decisions.length === 0) return;
    
    const totalConfidence = this.decisions.reduce((sum, d) => sum + d.confidence, 0);
    this.metrics.avgConfidence = totalConfidence / this.decisions.length;
  }

  recordOutcome(decisionId, outcome) {
    const decision = this.decisions.find(d => d.id === decisionId);
    if (decision) {
      decision.setOutcome(outcome);
      if (outcome === 'success') {
        this.metrics.successCount++;
      } else if (outcome === 'failure') {
        this.metrics.failureCount++;
      }
    }
  }

  detectAnomaly() {
    const anomalies = [];
    
    // 检测低置信度决策
    const lowConfidenceDecisions = this.decisions.filter(d => d.confidence < this.options.anomalyThreshold);
    if (lowConfidenceDecisions.length > 0) {
      anomalies.push({
        type: 'low_confidence',
        count: lowConfidenceDecisions.length,
        decisions: lowConfidenceDecisions.slice(-5)
      });
    }
    
    // 检测决策模式异常
    if (this.decisions.length >= 5) {
      const recentDecisions = this.decisions.slice(-5);
      const avgRecentConfidence = recentDecisions.reduce((sum, d) => sum + d.confidence, 0) / 5;
      
      if (avgRecentConfidence < 0.3) {
        anomalies.push({
          type: 'confidence_decline',
          message: 'Recent decisions show consistently low confidence',
          avgConfidence: avgRecentConfidence
        });
      }
    }
    
    // 检测失败率异常
    const totalOutcomes = this.metrics.successCount + this.metrics.failureCount;
    if (totalOutcomes > 5) {
      const failureRate = this.metrics.failureCount / totalOutcomes;
      if (failureRate > 0.5) {
        anomalies.push({
          type: 'high_failure_rate',
          message: 'Failure rate exceeds 50%',
          failureRate
        });
      }
    }
    
    this.metrics.anomalyCount = anomalies.length;
    return anomalies;
  }

  complete() {
    this.endTime = Date.now();
    this.status = 'completed';
  }

  getDuration() {
    const end = this.endTime || Date.now();
    return end - this.startTime;
  }

  getReport() {
    return {
      sessionId: this.sessionId,
      status: this.status,
      duration: this.getDuration(),
      decisionCount: this.decisions.length,
      metrics: { ...this.metrics },
      anomalies: this.detectAnomaly(),
      recentDecisions: this.decisions.slice(-10).map(d => ({
        id: d.id,
        decision: d.decision,
        confidence: d.confidence,
        outcome: d.outcome,
        timestamp: d.timestamp
      }))
    };
  }
}

/**
 * 自我监控主类
 */
class SelfMonitor extends EventEmitter {
  constructor(options = {}) {
    super();
    this.sessions = new Map();
    this.activeSession = null;
    this.options = {
      autoDetectAnomalies: options.autoDetectAnomalies !== false,
      anomalyCheckInterval: options.anomalyCheckInterval || 5000,
      ...options
    };
    this.anomalyCheckTimer = null;
  }

  /**
   * 监控函数执行
   */
  async monitor(fn, context = {}) {
    const sessionId = context.sessionId || `monitor-${Date.now()}`;
    this.startMonitoring(sessionId, context);
    
    try {
      const result = await fn();
      this.stopMonitoring(sessionId);
      return result;
    } catch (error) {
      this.stopMonitoring(sessionId);
      throw error;
    }
  }

  /**
   * 开始监控会话
   */
  startMonitoring(sessionId, options = {}) {
    if (this.sessions.has(sessionId)) {
      throw new Error(`Session ${sessionId} already exists`);
    }

    const session = new MonitoringSession(sessionId, options);
    this.sessions.set(sessionId, session);
    this.activeSession = sessionId;

    this.emit('sessionStarted', { sessionId, timestamp: Date.now() });

    // 启动异常检测
    if (this.options.autoDetectAnomalies) {
      this._startAnomalyDetection(sessionId);
    }

    return session;
  }

  /**
   * 停止监控会话
   */
  stopMonitoring(sessionId) {
    const session = this.sessions.get(sessionId);
    if (!session) {
      throw new Error(`Session ${sessionId} not found`);
    }

    session.complete();
    this._stopAnomalyDetection(sessionId);
    
    if (this.activeSession === sessionId) {
      this.activeSession = null;
    }

    this.emit('sessionStopped', { sessionId, report: session.getReport() });
    return session.getReport();
  }

  /**
   * 记录决策
   */
  recordDecision(decisionData, sessionId = null) {
    const targetSessionId = sessionId || this.activeSession;
    if (!targetSessionId) {
      throw new Error('No active session. Call startMonitoring() first or provide sessionId.');
    }

    const session = this.sessions.get(targetSessionId);
    if (!session) {
      throw new Error(`Session ${targetSessionId} not found`);
    }

    const decision = session.addDecision(decisionData);
    this.emit('decisionRecorded', { sessionId: targetSessionId, decision });

    // 实时异常检测
    if (decision.confidence < 0.2) {
      this.emit('anomalyDetected', {
        sessionId: targetSessionId,
        type: 'critical_low_confidence',
        decision
      });
    }

    return decision;
  }

  /**
   * 记录事件
   */
  recordEvent(eventType, data, sessionId = null) {
    const targetSessionId = sessionId || this.activeSession;
    if (!targetSessionId) return;

    const session = this.sessions.get(targetSessionId);
    if (session) {
      session.addEvent(eventType, data);
      this.emit('eventRecorded', { sessionId: targetSessionId, eventType, data });
    }
  }

  /**
   * 记录决策结果
   */
  recordOutcome(decisionId, outcome, sessionId = null) {
    const targetSessionId = sessionId || this.activeSession;
    if (!targetSessionId) return;

    const session = this.sessions.get(targetSessionId);
    if (session) {
      session.recordOutcome(decisionId, outcome);
      this.emit('outcomeRecorded', { sessionId: targetSessionId, decisionId, outcome });
    }
  }

  /**
   * 获取监控报告
   */
  getReport(sessionId = null) {
    const targetSessionId = sessionId || this.activeSession;
    if (!targetSessionId) {
      throw new Error('No active session. Provide sessionId or start a monitoring session.');
    }

    const session = this.sessions.get(targetSessionId);
    if (!session) {
      throw new Error(`Session ${targetSessionId} not found`);
    }

    return session.getReport();
  }

  /**
   * 获取所有会话报告
   */
  getAllReports() {
    const reports = {};
    for (const [sessionId, session] of this.sessions) {
      reports[sessionId] = session.getReport();
    }
    return reports;
  }

  /**
   * 获取当前活跃会话ID
   */
  getActiveSession() {
    return this.activeSession;
  }

  /**
   * 设置活跃会话
   */
  setActiveSession(sessionId) {
    if (!this.sessions.has(sessionId)) {
      throw new Error(`Session ${sessionId} not found`);
    }
    this.activeSession = sessionId;
  }

  /**
   * 获取会话统计信息
   */
  getStatistics() {
    const allReports = this.getAllReports();
    const sessionIds = Object.keys(allReports);
    
    let totalDecisions = 0;
    let totalSuccesses = 0;
    let totalFailures = 0;
    let totalAnomalies = 0;
    
    for (const report of Object.values(allReports)) {
      totalDecisions += report.decisionCount;
      totalSuccesses += report.metrics.successCount;
      totalFailures += report.metrics.failureCount;
      totalAnomalies += report.metrics.anomalyCount;
    }

    return {
      totalSessions: sessionIds.length,
      activeSession: this.activeSession,
      totalDecisions,
      totalSuccesses,
      totalFailures,
      totalAnomalies,
      successRate: totalSuccesses + totalFailures > 0 
        ? totalSuccesses / (totalSuccesses + totalFailures) 
        : 0
    };
  }

  /**
   * 清理已完成的会话
   */
  cleanupCompletedSessions(keepLast = 10) {
    const completedSessions = [];
    
    for (const [sessionId, session] of this.sessions) {
      if (session.status === 'completed') {
        completedSessions.push({ sessionId, endTime: session.endTime });
      }
    }
    
    // 按结束时间排序，保留最近的
    completedSessions.sort((a, b) => b.endTime - a.endTime);
    const sessionsToRemove = completedSessions.slice(keepLast);
    
    for (const { sessionId } of sessionsToRemove) {
      this.sessions.delete(sessionId);
    }
    
    return sessionsToRemove.length;
  }

  /**
   * 启动异常检测定时器
   */
  _startAnomalyDetection(sessionId) {
    if (this.anomalyCheckTimer) {
      clearInterval(this.anomalyCheckTimer);
    }
    
    this.anomalyCheckTimer = setInterval(() => {
      const session = this.sessions.get(sessionId);
      if (session && session.status === 'active') {
        const anomalies = session.detectAnomaly();
        if (anomalies.length > 0) {
          this.emit('anomaliesDetected', { sessionId, anomalies });
        }
      }
    }, this.options.anomalyCheckInterval);
  }

  /**
   * 停止异常检测定时器
   */
  _stopAnomalyDetection(sessionId) {
    if (this.anomalyCheckTimer) {
      clearInterval(this.anomalyCheckTimer);
      this.anomalyCheckTimer = null;
    }
  }

  /**
   * 销毁监控器
   */
  destroy() {
    if (this.anomalyCheckTimer) {
      clearInterval(this.anomalyCheckTimer);
    }
    this.sessions.clear();
    this.activeSession = null;
    this.removeAllListeners();
  }
}

module.exports = {
  SelfMonitor,
  MonitoringSession,
  DecisionRecord
};