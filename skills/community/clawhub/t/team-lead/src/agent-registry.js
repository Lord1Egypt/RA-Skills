/**
 * Team Lead - Agent Registry
 * 维护可用 Agent 及其能力、性能指标
 */

export class AgentRegistry {
  constructor() {
    this.agents = new Map();
    this.performanceHistory = new Map();
    this.loadKnownAgents();
  }

  /**
   * 加载已知 Agent（从配置或记忆中）
   */
  loadKnownAgents() {
    // 预注册的常见 Agent
    const knownAgents = {
      'stock': {
        capabilities: ['股票分析', '投资组合', '市场数据', '风险评估', 'trading'],
        sessionKey: 'stock',
        type: 'specialized'
      },
      'coding': {
        capabilities: ['代码开发', '代码审查', 'GitHub', '调试', 'programming'],
        sessionKey: 'coding',
        type: 'specialized'
      },
      'main': {
        capabilities: ['通用任务', '协调', '研究', '分析', 'general'],
        sessionKey: 'main',
        type: 'general'
      }
    };

    for (const [id, config] of Object.entries(knownAgents)) {
      this.register(id, config.capabilities, { sessionKey: config.sessionKey, type: config.type });
    }
  }

  /**
   * 注册 Agent
   */
  register(agentId, capabilities, config = {}) {
    const agent = {
      id: agentId,
      capabilities: capabilities.map(c => c.toLowerCase()),
      status: config.status || 'active',
      sessionKey: config.sessionKey || agentId,
      type: config.type || 'dynamic',
      registeredAt: Date.now(),
      metadata: config.metadata || {}
    };

    this.agents.set(agentId, agent);
    console.log(`[AgentRegistry] Registered: ${agentId} with capabilities: ${capabilities.join(', ')}`);
    return agent;
  }

  /**
   * 注销 Agent
   */
  unregister(agentId) {
    const agent = this.agents.get(agentId);
    if (agent) {
      agent.status = 'inactive';
      console.log(`[AgentRegistry] Unregistered: ${agentId}`);
    }
  }

  /**
   * 发现匹配能力的 Agent
   */
  findAgents(requiredCapabilities) {
    const matches = [];
    const requiredSet = new Set(requiredCapabilities.map(c => c.toLowerCase()));

    for (const [id, agent] of this.agents) {
      if (agent.status !== 'active') continue;

      const score = this.calculateMatchScore(agent.capabilities, requiredSet);
      if (score > 0.3) {
        const health = this.getHealth(id);
        matches.push({
          id,
          score,
          ...agent,
          health
        });
      }
    }

    // 按综合评分排序
    return matches.sort((a, b) => {
      const scoreA = a.score * 0.6 + (a.health?.qualityScore || 0.8) * 0.4;
      const scoreB = b.score * 0.6 + (b.health?.qualityScore || 0.8) * 0.4;
      return scoreB - scoreA;
    });
  }

  /**
   * 计算能力匹配度
   */
  calculateMatchScore(agentCaps, requiredSet) {
    const agentSet = new Set(agentCaps);
    const intersection = [...requiredSet].filter(c => agentSet.has(c));
    
    if (requiredSet.size === 0) return 0;
    
    // Jaccard 相似度
    const union = new Set([...agentCaps, ...requiredSet]);
    return intersection.length / union.size;
  }

  /**
   * 更新 Agent 性能指标
   */
  updatePerformance(agentId, metrics) {
    if (!this.performanceHistory.has(agentId)) {
      this.performanceHistory.set(agentId, []);
    }

    const history = this.performanceHistory.get(agentId);
    history.push({
      ...metrics,
      timestamp: Date.now()
    });

    // 保留最近 50 条记录
    if (history.length > 50) {
      history.shift();
    }

    console.log(`[AgentRegistry] Updated performance for ${agentId}:`, metrics);
  }

  /**
   * 获取 Agent 健康状态
   */
  getHealth(agentId) {
    const history = this.performanceHistory.get(agentId) || [];
    const recent = history.slice(-10);

    if (recent.length === 0) {
      return {
        avgResponseTime: 0,
        successRate: 1.0,
        qualityScore: 0.8,
        totalTasks: 0
      };
    }

    return {
      avgResponseTime: recent.reduce((a, b) => a + (b.responseTime || 0), 0) / recent.length,
      successRate: recent.filter(r => r.success !== false).length / recent.length,
      qualityScore: recent.reduce((a, b) => a + (b.quality || 0.8), 0) / recent.length,
      totalTasks: history.length
    };
  }

  /**
   * 获取所有活跃 Agent
   */
  getActiveAgents() {
    return [...this.agents.values()].filter(a => a.status === 'active');
  }

  /**
   * 导出注册表（用于持久化）
   */
  export() {
    return {
      agents: Object.fromEntries(this.agents),
      performanceHistory: Object.fromEntries(
        [...this.performanceHistory.entries()].map(([k, v]) => [k, v.slice(-20)])
      )
    };
  }

  /**
   * 导入注册表（从持久化）
   */
  import(data) {
    if (data.agents) {
      for (const [id, agent] of Object.entries(data.agents)) {
        this.agents.set(id, agent);
      }
    }
    if (data.performanceHistory) {
      for (const [id, history] of Object.entries(data.performanceHistory)) {
        this.performanceHistory.set(id, history);
      }
    }
  }

  /**
   * 获取 Agent 统计信息
   */
  getStats() {
    const active = this.getActiveAgents();
    return {
      totalAgents: this.agents.size,
      activeAgents: active.length,
      totalTasksTracked: [...this.performanceHistory.values()].reduce((sum, h) => sum + h.length, 0),
      topPerformers: this.getTopPerformers(5)
    };
  }

  /**
   * 获取表现最好的 Agent
   */
  getTopPerformers(limit = 5) {
    const healthScores = [...this.agents.keys()].map(id => ({
      id,
      health: this.getHealth(id)
    }));

    return healthScores
      .sort((a, b) => b.health.qualityScore - a.health.qualityScore)
      .slice(0, limit);
  }
}
