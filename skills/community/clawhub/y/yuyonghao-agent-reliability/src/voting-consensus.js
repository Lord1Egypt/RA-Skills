/**
 * VotingConsensus - 投票共识模块
 * 多Agent投票策略、冲突解决、共识达成判定和dissent记录
 */

const EventEmitter = require('events');

class VotingConsensus extends EventEmitter {
  /**
   * @param {Object} options - 配置选项
   * @param {string} options.strategy - 投票策略: 'simple-majority' | 'weighted-majority' | 'unanimous' | 'super-majority' (默认 'simple-majority')
   * @param {number} options.minAgreement - 最小同意比例 (默认 0.5)
   * @param {number} options.minVoters - 最小投票人数 (默认 1)
   * @param {number} options.timeout - 投票超时(ms) (默认 30000)
   * @param {boolean} options.enableDissentRecording - 是否记录异议 (默认 true)
   * @param {boolean} options.enableLogging - 是否启用日志 (默认 true)
   */
  constructor(options = {}) {
    super();
    
    this.strategy = options.strategy ?? 'simple-majority';
    this.minAgreement = options.minAgreement ?? 0.5;
    this.minVoters = options.minVoters ?? 1;
    this.timeout = options.timeout ?? 30000;
    this.enableDissentRecording = options.enableDissentRecording ?? true;
    this.enableLogging = options.enableLogging ?? true;
    
    // 投票记录
    this.votes = new Map();
    
    // 投票会话
    this.sessions = new Map();
    
    // 异议记录
    this.dissentRecords = [];
    
    // 统计
    this.stats = {
      totalVotes: 0,
      totalSessions: 0,
      consensusReached: 0,
      consensusFailed: 0,
      avgAgreement: 0
    };
    
    this._log('VotingConsensus initialized', {
      strategy: this.strategy,
      minAgreement: this.minAgreement,
      minVoters: this.minVoters
    });
  }
  
  /**
   * 创建投票会话
   * @param {string} sessionId - 会话ID (可选)
   * @param {Object} options - 会话选项
   * @returns {string} 会话ID
   */
  createSession(sessionId = null, options = {}) {
    const id = sessionId || `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    const session = {
      id,
      createdAt: Date.now(),
      votes: new Map(),
      status: 'open',
      result: null,
      options: {
        strategy: options.strategy || this.strategy,
        minAgreement: options.minAgreement ?? this.minAgreement,
        minVoters: options.minVoters ?? this.minVoters,
        timeout: options.timeout || this.timeout,
        ...options
      }
    };
    
    this.sessions.set(id, session);
    this.stats.totalSessions++;
    
    this._log(`Session created: ${id}`);
    this.emit('session:created', { sessionId: id, session });
    
    // 设置超时
    if (session.options.timeout > 0) {
      setTimeout(() => {
        if (session.status === 'open') {
          this._finalizeSession(id);
        }
      }, session.options.timeout);
    }
    
    return id;
  }
  
  /**
   * 投票
   * @param {string} voterId - 投票者ID
   * @param {Object} vote - 投票内容
   * @param {string} vote.decision - 决策: 'approve' | 'reject' | 'abstain'
   * @param {number} vote.confidence - 置信度 (0-1)
   * @param {number} vote.weight - 权重 (默认 1)
   * @param {string} vote.reason - 理由
   * @param {Object} vote.metadata - 元数据
   * @param {string} sessionId - 会话ID (可选，使用默认会话)
   */
  vote(voterId, vote, sessionId = null) {
    // 如果没有指定会话，使用第一个开放会话或创建新会话
    let targetSessionId = sessionId;
    if (!targetSessionId) {
      const openSession = this._getFirstOpenSession();
      if (openSession) {
        targetSessionId = openSession.id;
      } else {
        targetSessionId = this.createSession();
      }
    }
    
    const session = this.sessions.get(targetSessionId);
    if (!session) {
      throw new Error(`Session not found: ${targetSessionId}`);
    }
    
    if (session.status !== 'open') {
      throw new Error(`Session ${targetSessionId} is not open`);
    }
    
    // 记录投票
    const voteRecord = {
      voterId,
      decision: vote.decision || 'abstain',
      confidence: vote.confidence ?? 0.5,
      weight: vote.weight ?? 1,
      reason: vote.reason || '',
      metadata: vote.metadata || {},
      timestamp: Date.now()
    };
    
    session.votes.set(voterId, voteRecord);
    this.stats.totalVotes++;
    
    this._log(`Vote recorded: ${voterId} -> ${voteRecord.decision} (weight: ${voteRecord.weight})`);
    this.emit('vote:recorded', { sessionId: targetSessionId, voterId, vote: voteRecord });
    
    // 检查是否达到共识
    this._checkConsensus(targetSessionId);
    
    return voteRecord;
  }
  
  /**
   * 获取第一个开放会话
   * @private
   */
  _getFirstOpenSession() {
    for (const session of this.sessions.values()) {
      if (session.status === 'open') {
        return session;
      }
    }
    return null;
  }
  
  /**
   * 检查是否达到共识
   * @private
   */
  _checkConsensus(sessionId) {
    const session = this.sessions.get(sessionId);
    if (!session || session.status !== 'open') return;
    
    const voteCount = session.votes.size;
    if (voteCount < session.options.minVoters) return;
    
    // 计算投票结果
    const result = this._calculateResult(session);
    
    // 根据策略判断是否达到共识
    const consensusReached = this._isConsensusReached(result, session.options);
    
    if (consensusReached) {
      this._finalizeSession(sessionId, result);
    }
    
    return result;
  }
  
  /**
   * 计算投票结果
   * @private
   */
  _calculateResult(session) {
    const votes = Array.from(session.votes.values());
    
    // 统计各决策的票数
    const counts = {
      approve: { count: 0, weight: 0, confidence: 0, voters: [] },
      reject: { count: 0, weight: 0, confidence: 0, voters: [] },
      abstain: { count: 0, weight: 0, confidence: 0, voters: [] }
    };
    
    let totalWeight = 0;
    let totalConfidence = 0;
    
    for (const vote of votes) {
      if (counts[vote.decision]) {
        counts[vote.decision].count++;
        counts[vote.decision].weight += vote.weight;
        counts[vote.decision].confidence += vote.confidence * vote.weight;
        counts[vote.decision].voters.push({
          voterId: vote.voterId,
          confidence: vote.confidence,
          reason: vote.reason
        });
      }
      totalWeight += vote.weight;
      totalConfidence += vote.confidence * vote.weight;
    }
    
    // 计算加权平均置信度
    const avgConfidence = totalWeight > 0 ? totalConfidence / totalWeight : 0;
    
    // 找出获胜决策
    let winningDecision = 'abstain';
    let maxWeight = 0;
    
    for (const [decision, data] of Object.entries(counts)) {
      if (decision !== 'abstain' && data.weight > maxWeight) {
        maxWeight = data.weight;
        winningDecision = decision;
      }
    }
    
    // 计算同意比例
    const winningWeight = counts[winningDecision].weight;
    const agreement = totalWeight > 0 ? winningWeight / totalWeight : 0;
    
    // 计算获胜决策的平均置信度
    const winningConfidence = winningWeight > 0 
      ? counts[winningDecision].confidence / winningWeight 
      : 0;
    
    return {
      decision: winningDecision,
      confidence: winningConfidence,
      agreement,
      totalVotes: votes.length,
      totalWeight,
      counts: {
        approve: counts.approve,
        reject: counts.reject,
        abstain: counts.abstain
      },
      dissenters: winningDecision === 'approve' 
        ? counts.reject.voters 
        : counts.approve.voters
    };
  }
  
  /**
   * 判断是否达到共识
   * @private
   */
  _isConsensusReached(result, options) {
    const { strategy, minAgreement } = options;
    
    switch (strategy) {
      case 'simple-majority':
        return result.agreement > 0.5;
        
      case 'weighted-majority':
        return result.agreement >= minAgreement;
        
      case 'unanimous':
        return result.agreement === 1.0;
        
      case 'super-majority':
        return result.agreement >= 0.67;
        
      default:
        return result.agreement >= minAgreement;
    }
  }
  
  /**
   * 结束会话
   * @private
   */
  _finalizeSession(sessionId, result = null) {
    const session = this.sessions.get(sessionId);
    if (!session || session.status !== 'open') return;
    
    session.status = 'closed';
    session.closedAt = Date.now();
    
    // 如果没有提供结果，重新计算
    if (!result) {
      result = this._calculateResult(session);
    }
    
    session.result = result;
    
    // 检查是否达到共识
    const consensusReached = this._isConsensusReached(result, session.options);
    
    if (consensusReached) {
      this.stats.consensusReached++;
      this._log(`Consensus reached in session ${sessionId}: ${result.decision}`);
      this.emit('consensus:reached', { sessionId, result });
    } else {
      this.stats.consensusFailed++;
      this._log(`Consensus failed in session ${sessionId}`);
      this.emit('consensus:failed', { sessionId, result });
    }
    
    // 记录异议
    if (this.enableDissentRecording && result.dissenters.length > 0) {
      for (const dissenter of result.dissenters) {
        this.dissentRecords.push({
          sessionId,
          timestamp: Date.now(),
          voterId: dissenter.voterId,
          decision: result.decision,
          confidence: dissenter.confidence,
          reason: dissenter.reason
        });
      }
    }
    
    // 更新统计
    this._updateStats(result);
  }
  
  /**
   * 更新统计
   * @private
   */
  _updateStats(result) {
    const totalConsensus = this.stats.consensusReached + this.stats.consensusFailed;
    this.stats.avgAgreement = totalConsensus > 0 
      ? (this.stats.avgAgreement * (totalConsensus - 1) + result.agreement) / totalConsensus
      : result.agreement;
  }
  
  /**
   * 解决冲突
   * @param {string} sessionId - 会话ID
   * @param {Object} resolution - 解决方案
   * @returns {Object} 解决结果
   */
  resolveConflict(sessionId, resolution = {}) {
    const session = this.sessions.get(sessionId);
    if (!session) {
      throw new Error(`Session not found: ${sessionId}`);
    }
    
    // 如果已有结果，返回结果
    if (session.result) {
      return session.result;
    }
    
    // 强制结束会话
    this._finalizeSession(sessionId);
    
    const result = session.result;
    
    // 应用解决方案
    if (resolution.overrideDecision) {
      result.decision = resolution.overrideDecision;
      result.overridden = true;
      result.overrideReason = resolution.reason || 'Manual override';
    }
    
    if (resolution.tieBreaker) {
      // 平票时使用决胜规则
      const approveWeight = result.counts.approve.weight;
      const rejectWeight = result.counts.reject.weight;
      
      if (approveWeight === rejectWeight) {
        result.decision = resolution.tieBreaker;
        result.tieBroken = true;
      }
    }
    
    this._log(`Conflict resolved for session ${sessionId}`, { decision: result.decision });
    this.emit('conflict:resolved', { sessionId, result, resolution });
    
    return result;
  }
  
  /**
   * 获取会话结果
   * @param {string} sessionId - 会话ID
   * @returns {Object|null} 会话结果
   */
  getResult(sessionId) {
    const session = this.sessions.get(sessionId);
    return session ? session.result : null;
  }
  
  /**
   * 获取会话状态
   * @param {string} sessionId - 会话ID
   * @returns {Object|null} 会话状态
   */
  getSession(sessionId) {
    const session = this.sessions.get(sessionId);
    if (!session) return null;
    
    return {
      id: session.id,
      status: session.status,
      createdAt: session.createdAt,
      closedAt: session.closedAt,
      voteCount: session.votes.size,
      options: session.options,
      result: session.result
    };
  }
  
  /**
   * 获取所有会话
   * @param {string} status - 状态过滤: 'open' | 'closed' | 'all'
   * @returns {Array} 会话列表
   */
  getSessions(status = 'all') {
    const sessions = [];
    for (const session of this.sessions.values()) {
      if (status === 'all' || session.status === status) {
        sessions.push(this.getSession(session.id));
      }
    }
    return sessions;
  }
  
  /**
   * 获取异议记录
   * @param {Object} options - 选项
   * @returns {Array} 异议记录
   */
  getDissentRecords(options = {}) {
    let records = [...this.dissentRecords];
    
    if (options.sessionId) {
      records = records.filter(r => r.sessionId === options.sessionId);
    }
    
    if (options.voterId) {
      records = records.filter(r => r.voterId === options.voterId);
    }
    
    if (options.limit) {
      records = records.slice(-options.limit);
    }
    
    return records;
  }
  
  /**
   * 获取统计信息
   * @returns {Object} 统计信息
   */
  getStats() {
    return {
      ...this.stats,
      consensusRate: this.stats.totalSessions > 0 
        ? this.stats.consensusReached / this.stats.totalSessions 
        : 0,
      openSessions: this.getSessions('open').length,
      closedSessions: this.getSessions('closed').length,
      totalDissents: this.dissentRecords.length
    };
  }
  
  /**
   * 重置
   */
  reset() {
    this.votes.clear();
    this.sessions.clear();
    this.dissentRecords = [];
    this.stats = {
      totalVotes: 0,
      totalSessions: 0,
      consensusReached: 0,
      consensusFailed: 0,
      avgAgreement: 0
    };
    
    this._log('VotingConsensus reset');
    this.emit('reset');
  }
  
  /**
   * 清理旧会话
   * @param {number} olderThan - 清理多久前的会话(ms)
   */
  cleanup(olderThan) {
    const cutoff = Date.now() - olderThan;
    let removed = 0;
    
    for (const [id, session] of this.sessions.entries()) {
      if (session.status === 'closed' && session.closedAt && session.closedAt < cutoff) {
        this.sessions.delete(id);
        removed++;
      }
    }
    
    // 清理旧异议记录
    this.dissentRecords = this.dissentRecords.filter(r => r.timestamp >= cutoff);
    
    this._log('Cleanup completed', { 
      removedSessions: removed, 
      remainingSessions: this.sessions.size,
      remainingDissents: this.dissentRecords.length
    });
    
    return { 
      removedSessions: removed, 
      remainingSessions: this.sessions.size,
      remainingDissents: this.dissentRecords.length
    };
  }
  
  /**
   * 日志记录
   * @private
   */
  _log(message, data = null) {
    if (!this.enableLogging) return;
    
    const timestamp = new Date().toISOString();
    if (data) {
      console.log(`[${timestamp}] [VotingConsensus] ${message}:`, data);
    } else {
      console.log(`[${timestamp}] [VotingConsensus] ${message}`);
    }
  }
}

module.exports = VotingConsensus;