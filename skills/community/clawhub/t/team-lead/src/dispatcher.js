/**
 * Team Lead - Task Dispatcher
 * 将子任务分派给合适的 Agent 并跟踪执行
 */

export class TaskDispatcher {
  constructor(registry, options = {}) {
    this.registry = registry;
    this.options = {
      defaultTimeout: 300,
      retryAttempts: 2,
      ...options
    };
    this.activeDispatches = new Map();
    this.dispatchHistory = [];
  }

  /**
   * 分发单个子任务
   */
  async dispatch(subtask, options = {}) {
    const dispatchId = `dispatch-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    const dispatch = {
      id: dispatchId,
      subtask,
      status: 'pending',
      createdAt: Date.now(),
      timeout: options.timeout || this.options.defaultTimeout,
      retryAttempts: options.retryAttempts || this.options.retryAttempts,
      retriesLeft: options.retryAttempts || this.options.retryAttempts
    };

    console.log(`[TaskDispatcher] Creating dispatch ${dispatchId} for subtask ${subtask.id}`);
    this.activeDispatches.set(dispatchId, dispatch);

    try {
      // 1. 寻找合适的 Agent
      const candidates = this.registry.findAgents([subtask.suggestedAgentType, subtask.type]);
      
      let result;
      if (candidates.length > 0) {
        // 有匹配的 Agent，选择最佳
        const selectedAgent = this.selectBestAgent(candidates);
        console.log(`[TaskDispatcher] Selected agent: ${selectedAgent.id} (score: ${selectedAgent.score.toFixed(2)})`);
        result = await this.sendToExistingAgent(subtask, selectedAgent, dispatch);
      } else {
        // 无匹配 Agent，动态创建
        console.log('[TaskDispatcher] No matching agent, spawning new agent');
        result = await this.spawnNewAgent(subtask, dispatch);
      }

      // 更新 dispatch 状态
      dispatch.status = 'completed';
      dispatch.completedAt = Date.now();
      dispatch.result = result;
      dispatch.responseTime = dispatch.completedAt - dispatch.createdAt;

      // 更新 Agent 性能
      if (result.agentId) {
        this.registry.updatePerformance(result.agentId, {
          responseTime: dispatch.responseTime,
          success: true,
          quality: result.quality || 0.8
        });
      }

      // 记录历史
      this.dispatchHistory.push({
        ...dispatch,
        result: null // 不存储完整结果以节省内存
      });

      return result;

    } catch (error) {
      console.error(`[TaskDispatcher] Dispatch ${dispatchId} failed:`, error.message);
      dispatch.status = 'failed';
      dispatch.error = error.message;

      // 重试逻辑
      if (dispatch.retriesLeft > 0) {
        dispatch.retriesLeft--;
        console.log(`[TaskDispatcher] Retrying dispatch ${dispatchId}, ${dispatch.retriesLeft} attempts left`);
        return this.retry(subtask, dispatch, error);
      }

      throw error;
    } finally {
      // 清理活跃 dispatch
      setTimeout(() => {
        this.activeDispatches.delete(dispatchId);
      }, 60000); // 1 分钟后清理
    }
  }

  /**
   * 选择最佳 Agent
   */
  selectBestAgent(candidates) {
    if (candidates.length === 1) return candidates[0];

    // 综合评分：能力匹配 (50%) + 历史表现 (50%)
    return candidates.reduce((best, current) => {
      const currentScore = this.calculateAgentScore(current);
      const bestScore = this.calculateAgentScore(best);
      return currentScore > bestScore ? current : best;
    });
  }

  /**
   * 计算 Agent 综合评分
   */
  calculateAgentScore(agent) {
    const health = agent.health || this.registry.getHealth(agent.id);
    
    return (
      agent.score * 0.5 +                    // 能力匹配度 50%
      (health.successRate || 0.8) * 0.3 +    // 成功率 30%
      (1 - Math.min(1, (health.avgResponseTime || 60) / 120)) * 0.2  // 响应速度 20%
    );
  }

  /**
   * 发送到已有 Agent
   */
  async sendToExistingAgent(subtask, agent, dispatch) {
    const startTime = Date.now();
    
    // 这里需要调用 OpenClaw 的 sessions_send 工具
    // 由于这是在 skill 中，我们通过返回指令让主 Agent 执行
    const instruction = this.buildAgentInstruction(subtask, agent);

    // 模拟执行（实际由主 Agent 调用 sessions_send）
    console.log(`[TaskDispatcher] Sending to agent ${agent.sessionKey || agent.id}`);
    console.log(`[TaskDispatcher] Instruction: ${instruction.substring(0, 100)}...`);

    // 在实际使用中，这里会调用 sessions_send
    // const result = await sessions_send({
    //   sessionKey: agent.sessionKey,
    //   message: instruction
    // });

    // 返回 dispatch 指令
    return {
      type: 'dispatch',
      agentId: agent.id,
      sessionKey: agent.sessionKey,
      instruction,
      subtaskId: subtask.id,
      dispatchId: dispatch.id,
      estimatedTime: subtask.estimatedTime
    };
  }

  /**
   * 构建给 Agent 的指令
   */
  buildAgentInstruction(subtask, agent) {
    const { input, label, type } = subtask;
    
    return `## 任务：${label}

**任务类型**: ${type}
**执行 Agent**: ${agent.id}

### 指令
${input.instruction}

### 上下文
${JSON.stringify(input.context, null, 2)}

### 输出格式
请使用 ${input.outputFormat} 格式输出结果。

### 要求
- 确保内容准确、完整
- 提供必要的来源和依据
- 如有不确定之处，明确标注

请开始执行任务。`;
  }

  /**
   * 动态创建新 Agent
   */
  async spawnNewAgent(subtask, dispatch) {
    const agentConfig = this.getAgentConfigForTask(subtask);
    const agentId = `dynamic-${subtask.type}-${Date.now()}`;

    // 注册新 Agent
    this.registry.register(agentId, [subtask.type, subtask.suggestedAgentType], {
      sessionKey: agentId,
      type: 'dynamic',
      metadata: {
        model: agentConfig.model,
        systemPrompt: agentConfig.systemPrompt
      }
    });

    // 返回 spawn 指令
    return {
      type: 'spawn',
      agentId,
      subtaskId: subtask.id,
      dispatchId: dispatch.id,
      config: agentConfig,
      instruction: this.buildAgentInstruction(subtask, { id: agentId, sessionKey: agentId })
    };
  }

  /**
   * 获取动态 Agent 配置
   */
  getAgentConfigForTask(subtask) {
    const configs = {
      search: {
        model: 'bailian/qwen3.5-plus',
        systemPrompt: '你是专业研究助手，擅长信息搜索和整理。提供准确、有来源的信息。'
      },
      analysis: {
        model: 'bailian/qwen3.5-plus',
        systemPrompt: '你是专业分析师，擅长从数据中提取洞察。提供深入、有见地的分析。'
      },
      writing: {
        model: 'bailian/qwen3.5-plus',
        systemPrompt: '你是专业写作者，擅长清晰、有吸引力的表达。产出结构化、易读的内容。'
      },
      coding: {
        model: 'bailian/qwen3.5-plus',
        systemPrompt: '你是资深工程师，擅长编写高质量代码。遵循最佳实践，提供完整解决方案。'
      },
      review: {
        model: 'bailian/qwen3.5-plus',
        systemPrompt: '你是专业审查员，擅长发现问题和改进机会。提供具体、可操作的反馈。'
      },
      planning: {
        model: 'bailian/qwen3.5-plus',
        systemPrompt: '你是专业规划师，擅长制定清晰、可执行的计划。考虑全面，步骤明确。'
      }
    };

    return configs[subtask.type] || configs.writing;
  }

  /**
   * 重试分发
   */
  async retry(subtask, originalDispatch, error) {
    // 尝试选择不同的 Agent
    const candidates = this.registry.findAgents([subtask.suggestedAgentType])
      .filter(c => c.id !== originalDispatch.result?.agentId);

    if (candidates.length > 0) {
      const selectedAgent = this.selectBestAgent(candidates);
      return this.sendToExistingAgent(subtask, selectedAgent, originalDispatch);
    }

    // 没有备选 Agent，抛出错误
    throw new Error(`Retry failed: ${error.message}`);
  }

  /**
   * 批量分发子任务
   */
  async dispatchBatch(subtasks, options = {}) {
    const { concurrency = 3 } = options;
    const results = new Map();
    const errors = [];

    // 按照执行计划分组执行
    const executionPlan = this.buildBatchExecutionPlan(subtasks);

    for (const group of executionPlan) {
      console.log(`[TaskDispatcher] Executing batch group: ${group.type} with ${group.subtasks.length} tasks`);
      
      const groupPromises = group.subtasks.map(async (subtask) => {
        try {
          const result = await this.dispatch(subtask, options);
          results.set(subtask.id, result);
        } catch (error) {
          errors.push({ subtaskId: subtask.id, error: error.message });
        }
      });

      // 控制并发
      await Promise.allSettled(groupPromises);

      // 检查是否有失败
      if (errors.length > 0 && group.type === 'sequential') {
        throw new Error(`Batch execution failed: ${errors.map(e => e.error).join(', ')}`);
      }
    }

    return {
      results: Object.fromEntries(results),
      errors,
      successRate: (subtasks.length - errors.length) / subtasks.length
    };
  }

  /**
   * 构建批量执行计划
   */
  buildBatchExecutionPlan(subtasks) {
    const groups = [];
    const visited = new Set();
    const remaining = [...subtasks];

    while (remaining.length > 0) {
      const ready = remaining.filter(s => 
        s.dependsOn.every(dep => visited.has(dep))
      );

      if (ready.length === 0) break;

      groups.push({
        type: ready[0].parallel ? 'parallel' : 'sequential',
        subtasks: ready
      });

      ready.forEach(s => {
        visited.add(s.id);
        const idx = remaining.findIndex(r => r.id === s.id);
        if (idx > -1) remaining.splice(idx, 1);
      });
    }

    return groups;
  }

  /**
   * 获取活跃分发统计
   */
  getActiveStats() {
    const now = Date.now();
    const active = [...this.activeDispatches.values()].filter(d => d.status === 'pending');
    
    return {
      totalActive: active.length,
      avgWaitTime: active.reduce((sum, d) => sum + (now - d.createdAt), 0) / (active.length || 1),
      byStatus: {
        pending: active.filter(d => d.status === 'pending').length,
        completed: this.dispatchHistory.filter(d => d.status === 'completed').length,
        failed: this.dispatchHistory.filter(d => d.status === 'failed').length
      }
    };
  }

  /**
   * 导出历史记录
   */
  exportHistory(limit = 100) {
    return this.dispatchHistory.slice(-limit);
  }
}
