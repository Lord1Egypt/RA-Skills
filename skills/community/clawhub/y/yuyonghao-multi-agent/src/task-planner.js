/**
 * task-planner.js - 任务分解和分发
 * 
 * 核心功能：
 * - 分解复杂任务为子任务
 * - 识别任务依赖关系
 * - 分配最优执行者
 * - 监控执行进度
 */

/**
 * TaskPlanner 类 - 任务规划器
 */
class TaskPlanner {
  /**
   * 创建任务规划器
   * @param {object} options - 配置选项
   */
  constructor(options = {}) {
    this.options = {
      maxDepth: options.maxDepth || 5,  // 最大分解深度
      minTaskDuration: options.minTaskDuration || 5,  // 最小任务时长（分钟）
      ...options
    };
    
    // 任务模板库
    this.taskTemplates = new Map();
    
    // 执行历史（用于学习优化）
    this.executionHistory = [];
    
    console.log('[TaskPlanner] 初始化完成');
  }
  
  /**
   * 分解复杂任务为子任务
   * @param {string} task - 复杂任务描述
   * @param {object} context - 上下文信息
   * @returns {Promise<Array>} 子任务列表
   */
  async decompose(task, context = {}) {
    console.log(`[TaskPlanner] 分解任务：${task}`);
    
    const decomposition = {
      originalTask: task,
      subtasks: [],
      dependencies: [],
      estimatedTime: 0,
      complexity: 'unknown',
      decomposedAt: new Date().toISOString()
    };
    
    // 分析任务类型和复杂度
    const analysis = await this._analyzeTask(task, context);
    decomposition.complexity = analysis.complexity;
    
    // 根据复杂度和任务类型决定分解策略
    // 开发类任务总是需要分解
    if (analysis.complexity === 'simple' && analysis.type !== 'development') {
      // 简单任务不需要分解（开发任务除外）
      decomposition.subtasks = [{
        id: 'subtask-1',
        description: task,
        type: analysis.type,
        estimatedTime: analysis.estimatedTime,
        dependencies: []
      }];
      decomposition.estimatedTime = analysis.estimatedTime;
    } else {
      // 复杂任务或开发任务需要分解
      const subtasks = await this._generateSubtasks(task, analysis, context);
      decomposition.subtasks = subtasks;
      decomposition.dependencies = this._identifyDependencies(subtasks);
      decomposition.estimatedTime = subtasks.reduce((sum, t) => sum + t.estimatedTime, 0);
    }
    
    console.log(`[TaskPlanner] 分解完成：${decomposition.subtasks.length} 个子任务`);
    return decomposition;
  }
  
  /**
   * 分析任务类型和复杂度
   * @private
   * @param {string} task - 任务描述
   * @param {object} context - 上下文
   * @returns {Promise<object>} 分析结果
   */
  async _analyzeTask(task, context) {
    // 关键词分析
    const keywords = {
      research: ['调研', '研究', '搜索', '分析', '调查', 'research', 'analyze'],
      development: ['开发', '编写', '代码', '实现', '编程', 'code', 'develop'],
      review: ['审核', '审查', '检查', '评估', 'review', 'audit'],
      writing: ['写作', '撰写', '文档', '报告', 'write', 'document'],
      planning: ['规划', '计划', '设计', '策略', 'plan', 'design']
    };
    
    const taskLower = task.toLowerCase();
    const typeScores = {};
    
    for (const [type, words] of Object.entries(keywords)) {
      typeScores[type] = words.filter(word => taskLower.includes(word)).length;
    }
    
    // 确定主要类型
    const type = Object.entries(typeScores)
      .sort((a, b) => b[1] - a[1])[0]?.[0] || 'general';
    
    // 估算复杂度（基于任务描述长度和关键词）
    const lengthScore = Math.min(task.length / 100, 1);
    const keywordScore = Object.values(typeScores).reduce((a, b) => a + b, 0) / 10;
    const complexityScore = (lengthScore + keywordScore) / 2;
    
    let complexity = 'medium';
    if (complexityScore < 0.3) complexity = 'simple';
    if (complexityScore > 0.7) complexity = 'complex';
    
    // 估算时间（分钟）
    const baseTime = { simple: 10, medium: 30, complex: 60 };
    const estimatedTime = baseTime[complexity];
    
    return {
      type,
      complexity,
      estimatedTime,
      keywords: typeScores
    };
  }
  
  /**
   * 生成子任务列表
   * @private
   * @param {string} task - 原始任务
   * @param {object} analysis - 任务分析结果
   * @param {object} context - 上下文
   * @returns {Promise<Array>} 子任务列表
   */
  async _generateSubtasks(task, analysis, context) {
    const subtasks = [];
    let taskId = 1;
    
    // 根据任务类型生成不同的分解模板
    switch (analysis.type) {
      case 'research':
        subtasks.push(
          {
            id: `subtask-${taskId++}`,
            description: `搜索和收集"${task}"相关信息`,
            type: 'research',
            estimatedTime: 20,
            dependencies: []
          },
          {
            id: `subtask-${taskId++}`,
            description: `分析和整理收集到的信息`,
            type: 'analysis',
            estimatedTime: 15,
            dependencies: [`subtask-${taskId - 2}`]
          },
          {
            id: `subtask-${taskId++}`,
            description: `撰写研究总结和报告`,
            type: 'writing',
            estimatedTime: 15,
            dependencies: [`subtask-${taskId - 2}`]
          }
        );
        break;
        
      case 'development':
        subtasks.push(
          {
            id: `subtask-${taskId++}`,
            description: `分析"${task}"的需求和技术方案`,
            type: 'planning',
            estimatedTime: 15,
            dependencies: []
          },
          {
            id: `subtask-${taskId++}`,
            description: `编写核心代码实现`,
            type: 'development',
            estimatedTime: 40,
            dependencies: [`subtask-${taskId - 2}`]
          },
          {
            id: `subtask-${taskId++}`,
            description: `编写测试用例并测试`,
            type: 'testing',
            estimatedTime: 20,
            dependencies: [`subtask-${taskId - 2}`]
          },
          {
            id: `subtask-${taskId++}`,
            description: `代码审查和优化`,
            type: 'review',
            estimatedTime: 15,
            dependencies: [`subtask-${taskId - 2}`]
          }
        );
        break;
        
      case 'writing':
        subtasks.push(
          {
            id: `subtask-${taskId++}`,
            description: `收集"${task}"相关素材和参考资料`,
            type: 'research',
            estimatedTime: 15,
            dependencies: []
          },
          {
            id: `subtask-${taskId++}`,
            description: `撰写文档大纲和结构`,
            type: 'planning',
            estimatedTime: 10,
            dependencies: [`subtask-${taskId - 2}`]
          },
          {
            id: `subtask-${taskId++}`,
            description: `撰写文档内容`,
            type: 'writing',
            estimatedTime: 30,
            dependencies: [`subtask-${taskId - 2}`]
          },
          {
            id: `subtask-${taskId++}`,
            description: `编辑和校对文档`,
            type: 'review',
            estimatedTime: 15,
            dependencies: [`subtask-${taskId - 2}`]
          }
        );
        break;
        
      default:
        // 通用分解
        subtasks.push(
          {
            id: `subtask-${taskId++}`,
            description: `分析任务：${task}`,
            type: 'planning',
            estimatedTime: 10,
            dependencies: []
          },
          {
            id: `subtask-${taskId++}`,
            description: `执行任务：${task}`,
            type: 'general',
            estimatedTime: 30,
            dependencies: [`subtask-${taskId - 2}`]
          },
          {
            id: `subtask-${taskId++}`,
            description: `验证和总结`,
            type: 'review',
            estimatedTime: 10,
            dependencies: [`subtask-${taskId - 2}`]
          }
        );
    }
    
    return subtasks;
  }
  
  /**
   * 识别子任务间的依赖关系
   * @private
   * @param {Array} subtasks - 子任务列表
   * @returns {Array} 依赖关系列表
   */
  _identifyDependencies(subtasks) {
    const dependencies = [];
    
    for (const task of subtasks) {
      if (task.dependencies) {
        for (const depId of task.dependencies) {
          dependencies.push({
            from: depId,
            to: task.id,
            type: 'sequential'
          });
        }
      }
    }
    
    return dependencies;
  }
  
  /**
   * 为任务分配最优执行者
   * @param {object} task - 任务对象
   * @param {Array} availableAgents - 可用智能体列表
   * @returns {string|null} 最优智能体 ID
   */
  assignAgent(task, availableAgents) {
    if (!availableAgents || availableAgents.length === 0) {
      return null;
    }
    
    // 任务类型到角色类型的映射
    const typeMapping = {
      research: ['Researcher', 'Coordinator'],
      development: ['Developer'],
      review: ['Reviewer'],
      writing: ['Writer'],
      planning: ['Planner', 'Coordinator'],
      testing: ['Developer', 'Reviewer'],
      analysis: ['Researcher', 'Planner'],
      general: ['Coordinator']
    };
    
    const preferredRoles = typeMapping[task.type] || ['Coordinator'];
    
    // 评分每个智能体
    const scores = availableAgents.map(agent => {
      let score = 0;
      
      // 角色匹配度（最高 50 分）
      if (preferredRoles.includes(agent.role)) {
        score += 50;
      }
      
      // 工作负载（最高 30 分，空闲的得分高）
      const workloadScore = 30 * (1 - (agent.completedTasks / 10));
      score += Math.max(0, workloadScore);
      
      // 历史表现（最高 20 分）
      const historyScore = this._getAgentHistoryScore(agent.id, task.type);
      score += historyScore;
      
      return { agentId: agent.id, score };
    });
    
    // 选择得分最高的智能体
    scores.sort((a, b) => b.score - a.score);
    const bestAgent = scores[0];
    
    console.log(`[TaskPlanner] 分配任务 "${task.description}" 给 ${bestAgent.agentId} (得分：${bestAgent.score})`);
    
    return bestAgent.agentId;
  }
  
  /**
   * 获取智能体在特定任务类型的历史表现分数
   * @private
   * @param {string} agentId - 智能体 ID
   * @param {string} taskType - 任务类型
   * @returns {number} 分数 (0-20)
   */
  _getAgentHistoryScore(agentId, taskType) {
    const relevantHistory = this.executionHistory.filter(
      h => h.agentId === agentId && h.taskType === taskType
    );
    
    if (relevantHistory.length === 0) {
      return 10; // 默认中等分数
    }
    
    const successRate = relevantHistory.filter(h => h.success).length / relevantHistory.length;
    return Math.round(successRate * 20);
  }
  
  /**
   * 监控任务执行进度
   * @param {Array} tasks - 任务列表
   * @returns {object} 进度信息
   */
  monitorProgress(tasks) {
    const progress = {
      total: tasks.length,
      completed: 0,
      running: 0,
      pending: 0,
      failed: 0,
      percentage: 0,
      estimatedRemaining: 0,
      tasks: []
    };
    
    for (const task of tasks) {
      const taskInfo = {
        id: task.id,
        description: task.description,
        status: task.status,
        agentId: task.agentId
      };
      
      progress.tasks.push(taskInfo);
      
      switch (task.status) {
        case 'completed':
          progress.completed++;
          break;
        case 'running':
          progress.running++;
          break;
        case 'failed':
          progress.failed++;
          break;
        default:
          progress.pending++;
      }
    }
    
    progress.percentage = progress.total > 0 
      ? Math.round((progress.completed / progress.total) * 100) 
      : 0;
    
    // 估算剩余时间
    const pendingTasks = tasks.filter(t => t.status === 'pending' || t.status === 'running');
    progress.estimatedRemaining = pendingTasks.reduce((sum, t) => sum + (t.estimatedTime || 10), 0);
    
    return progress;
  }
  
  /**
   * 记录执行历史（用于优化）
   * @param {object} execution - 执行记录
   */
  recordExecution(execution) {
    this.executionHistory.push({
      taskId: execution.taskId,
      agentId: execution.agentId,
      taskType: execution.taskType,
      success: execution.success,
      duration: execution.duration,
      timestamp: new Date().toISOString()
    });
    
    // 保持历史记录在合理大小
    if (this.executionHistory.length > 1000) {
      this.executionHistory = this.executionHistory.slice(-500);
    }
  }
  
  /**
   * 重新规划失败的任务
   * @param {object} failedTask - 失败的任务
   * @returns {object} 新的任务计划
   */
  replan(failedTask) {
    console.log(`[TaskPlanner] 重新规划失败任务：${failedTask.id}`);
    
    return {
      originalTask: failedTask,
      newStrategy: 'retry_with_adjustments',
      adjustments: [
        '增加执行时间预算',
        '更换执行智能体',
        '进一步分解任务'
      ],
      replannedAt: new Date().toISOString()
    };
  }
}

module.exports = {
  TaskPlanner
};
