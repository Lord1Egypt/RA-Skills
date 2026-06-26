/**
 * agent-team.js - 智能体团队管理
 * 
 * 核心类：AgentTeam
 * 负责管理多智能体团队的创建、配置和任务执行
 */

const { createRole } = require('./roles');

/**
 * AgentTeam 类 - 智能体团队管理
 * 
 * 提供多智能体协作的核心功能：
 * - 添加角色智能体
 * - 分配任务给指定智能体
 * - 广播任务给所有智能体
 * - 收集各智能体结果
 * - 编排多智能体协作流程
 */
class AgentTeam {
  /**
   * 创建智能体团队
   * @param {string} name - 团队名称
   * @param {object} options - 配置选项
   */
  constructor(name, options = {}) {
    this.name = name || 'unnamed-team';
    this.options = {
      maxConcurrency: options.maxConcurrency || 5,
      timeout: options.timeout || 30000,
      retryAttempts: options.retryAttempts || 3,
      ...options
    };
    
    // 已添加的角色智能体
    this.agents = new Map();
    
    // 任务队列
    this.taskQueue = [];
    
    // 执行结果
    this.results = new Map();
    
    // 执行历史
    this.history = [];
    
    console.log(`[AgentTeam] 创建团队：${this.name}`);
  }
  
  /**
   * 添加角色智能体到团队
   * @param {string} agentId - 智能体标识符
   * @param {object} roleConfig - 角色配置（可以是预定义角色或自定义配置）
   * @returns {AgentTeam} 返回 this 以支持链式调用
   */
  addRole(agentId, roleConfig) {
    if (!agentId) {
      throw new Error('agentId 不能为空');
    }
    
    if (this.agents.has(agentId)) {
      console.warn(`[AgentTeam] 智能体 ${agentId} 已存在，将被覆盖`);
    }
    
    // 如果是配置对象，创建自定义角色
    const role = typeof roleConfig === 'function' || roleConfig.execute 
      ? roleConfig 
      : createRole(roleConfig);
    
    const agent = {
      id: agentId,
      role: role,
      status: 'idle',
      currentTask: null,
      completedTasks: 0,
      createdAt: new Date().toISOString()
    };
    
    this.agents.set(agentId, agent);
    console.log(`[AgentTeam] 添加智能体：${agentId} (${role.name || 'Custom'})`);
    
    return this;
  }
  
  /**
   * 从团队移除智能体
   * @param {string} agentId - 智能体标识符
   * @returns {boolean} 是否成功移除
   */
  removeRole(agentId) {
    const removed = this.agents.delete(agentId);
    if (removed) {
      console.log(`[AgentTeam] 移除智能体：${agentId}`);
    }
    return removed;
  }
  
  /**
   * 获取智能体信息
   * @param {string} agentId - 智能体标识符
   * @returns {object|null} 智能体信息
   */
  getAgent(agentId) {
    return this.agents.get(agentId) || null;
  }
  
  /**
   * 列出所有智能体
   * @returns {Array} 智能体列表
   */
  listAgents() {
    return Array.from(this.agents.values()).map(agent => ({
      id: agent.id,
      role: agent.role.name,
      status: agent.status,
      completedTasks: agent.completedTasks
    }));
  }
  
  /**
   * 分配任务给指定智能体
   * @param {string} task - 任务描述
   * @param {string} agentId - 目标智能体 ID
   * @param {object} options - 任务选项
   * @returns {object} 任务对象
   */
  assignTask(task, agentId, options = {}) {
    if (!this.agents.has(agentId)) {
      throw new Error(`智能体 ${agentId} 不存在`);
    }
    
    const taskObj = {
      id: `task-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      description: task,
      agentId: agentId,
      status: 'pending',
      priority: options.priority || 'normal',
      context: options.context || {},
      dependsOn: options.dependsOn || [],
      createdAt: new Date().toISOString(),
      startedAt: null,
      completedAt: null,
      result: null,
      error: null
    };
    
    this.taskQueue.push(taskObj);
    console.log(`[AgentTeam] 分配任务：${taskObj.id} -> ${agentId}`);
    
    return taskObj;
  }
  
  /**
   * 广播任务给所有智能体
   * @param {string} task - 任务描述
   * @param {object} options - 任务选项
   * @returns {Array} 创建的任务列表
   */
  broadcast(task, options = {}) {
    const tasks = [];
    const agentIds = options.toAgents || Array.from(this.agents.keys());
    
    for (const agentId of agentIds) {
      if (this.agents.has(agentId)) {
        const taskObj = this.assignTask(task, agentId, options);
        tasks.push(taskObj);
      }
    }
    
    console.log(`[AgentTeam] 广播任务给 ${tasks.length} 个智能体`);
    return tasks;
  }
  
  /**
   * 收集各智能体的执行结果
   * @param {object} options - 收集选项
   * @returns {object} 聚合结果
   */
  collectResults(options = {}) {
    const results = {
      teamName: this.name,
      totalTasks: this.taskQueue.length,
      completedTasks: 0,
      failedTasks: 0,
      pendingTasks: 0,
      results: [],
      errors: [],
      summary: {},
      collectedAt: new Date().toISOString()
    };
    
    for (const task of this.taskQueue) {
      if (task.status === 'completed' && task.result) {
        results.completedTasks++;
        results.results.push({
          taskId: task.id,
          agentId: task.agentId,
          result: task.result
        });
      } else if (task.status === 'failed') {
        results.failedTasks++;
        results.errors.push({
          taskId: task.id,
          agentId: task.agentId,
          error: task.error
        });
      } else {
        results.pendingTasks++;
      }
    }
    
    // 生成摘要
    results.summary = this._generateSummary(results);
    
    console.log(`[AgentTeam] 收集结果：完成 ${results.completedTasks}/${results.totalTasks}`);
    return results;
  }
  
  /**
   * 生成结果摘要
   * @private
   * @param {object} results - 结果对象
   * @returns {object} 摘要信息
   */
  _generateSummary(results) {
    const summary = {
      successRate: results.totalTasks > 0 
        ? (results.completedTasks / results.totalTasks * 100).toFixed(2) + '%'
        : '0%',
      agentStats: {},
      taskTypes: {}
    };
    
    // 统计每个智能体的表现
    for (const result of results.results) {
      if (!summary.agentStats[result.agentId]) {
        summary.agentStats[result.agentId] = { completed: 0, failed: 0 };
      }
      summary.agentStats[result.agentId].completed++;
      
      const type = result.result?.type || 'unknown';
      summary.taskTypes[type] = (summary.taskTypes[type] || 0) + 1;
    }
    
    // 统计失败
    for (const error of results.errors) {
      if (!summary.agentStats[error.agentId]) {
        summary.agentStats[error.agentId] = { completed: 0, failed: 0 };
      }
      summary.agentStats[error.agentId].failed++;
    }
    
    return summary;
  }
  
  /**
   * 执行单个任务
   * @private
   * @param {object} task - 任务对象
   * @returns {Promise<object>} 执行结果
   */
  async _executeTask(task) {
    const agent = this.agents.get(task.agentId);
    if (!agent) {
      throw new Error(`智能体 ${task.agentId} 不存在`);
    }
    
    task.status = 'running';
    task.startedAt = new Date().toISOString();
    agent.status = 'busy';
    agent.currentTask = task.id;
    
    try {
      console.log(`[AgentTeam] 执行任务：${task.id} by ${task.agentId}`);
      
      // 设置超时
      const timeout = this.options.timeout;
      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error(`任务超时 (${timeout}ms)`)), timeout);
      });
      
      // 执行任务
      const executePromise = agent.role.execute(task.description, {
        ...task.context,
        teamName: this.name,
        taskId: task.id
      });
      
      const result = await Promise.race([executePromise, timeoutPromise]);
      
      task.status = 'completed';
      task.result = result;
      task.completedAt = new Date().toISOString();
      
      agent.status = 'idle';
      agent.currentTask = null;
      agent.completedTasks++;
      
      // 记录历史
      this.history.push({
        taskId: task.id,
        agentId: task.agentId,
        status: 'completed',
        timestamp: task.completedAt
      });
      
      return { success: true, result };
    } catch (error) {
      task.status = 'failed';
      task.error = error.message;
      task.completedAt = new Date().toISOString();
      
      agent.status = 'idle';
      agent.currentTask = null;
      
      // 记录历史
      this.history.push({
        taskId: task.id,
        agentId: task.agentId,
        status: 'failed',
        error: error.message,
        timestamp: task.completedAt
      });
      
      console.error(`[AgentTeam] 任务失败：${task.id} - ${error.message}`);
      return { success: false, error };
    }
  }
  
  /**
   * 编排多智能体协作流程
   * 自动处理任务依赖和执行顺序
   * @param {object} options - 编排选项
   * @returns {Promise<object>} 最终结果
   */
  async orchestrate(options = {}) {
    console.log(`[AgentTeam] 开始编排：${this.taskQueue.length} 个任务`);
    
    const startTime = Date.now();
    const processedTasks = new Set();
    const failedTasks = new Set();
    
    // 构建任务依赖图
    const taskGraph = this._buildTaskGraph();
    
    // 执行任务直到所有任务完成或失败
    while (processedTasks.size + failedTasks.size < this.taskQueue.length) {
      // 找出可执行的任务（依赖已满足）
      const readyTasks = this.taskQueue.filter(task => {
        if (processedTasks.has(task.id) || failedTasks.has(task.id)) {
          return false;
        }
        
        // 检查依赖
        const dependencies = task.dependsOn || [];
        const depsMet = dependencies.every(depId => {
          const depTask = this.taskQueue.find(t => t.id === depId);
          return depTask && depTask.status === 'completed';
        });
        
        // 检查是否有依赖失败
        const depsFailed = dependencies.some(depId => failedTasks.has(depId));
        if (depsFailed) {
          task.status = 'skipped';
          task.error = '依赖任务失败';
          failedTasks.add(task.id);
          return false;
        }
        
        return depsMet;
      });
      
      if (readyTasks.length === 0) {
        // 没有可执行的任务，但有未完成的任务
        const remaining = this.taskQueue.filter(t => 
          !processedTasks.has(t.id) && !failedTasks.has(t.id)
        );
        if (remaining.length > 0) {
          console.warn('[AgentTeam] 检测到循环依赖或无法执行的任务');
          remaining.forEach(t => {
            t.status = 'skipped';
            t.error = '无法执行（可能是循环依赖）';
            failedTasks.add(t.id);
          });
        }
        break;
      }
      
      // 并发执行就绪任务（受最大并发数限制）
      const batchSize = Math.min(readyTasks.length, this.options.maxConcurrency);
      const batch = readyTasks.slice(0, batchSize);
      
      const executionPromises = batch.map(task => this._executeTask(task));
      const results = await Promise.all(executionPromises);
      
      // 更新处理状态
      results.forEach((result, index) => {
        const task = batch[index];
        if (result.success) {
          processedTasks.add(task.id);
        } else {
          failedTasks.add(task.id);
        }
      });
    }
    
    const executionTime = Date.now() - startTime;
    console.log(`[AgentTeam] 编排完成，耗时：${executionTime}ms`);
    
    // 收集并返回结果
    const finalResults = this.collectResults();
    finalResults.executionTime = executionTime;
    finalResults.options = options;
    
    return finalResults;
  }
  
  /**
   * 构建任务依赖图
   * @private
   * @returns {object} 任务图
   */
  _buildTaskGraph() {
    const graph = {
      nodes: new Map(),
      edges: []
    };
    
    // 添加节点
    for (const task of this.taskQueue) {
      graph.nodes.set(task.id, {
        task: task,
        inDegree: task.dependsOn?.length || 0,
        outEdges: []
      });
    }
    
    // 添加边
    for (const task of this.taskQueue) {
      if (task.dependsOn) {
        for (const depId of task.dependsOn) {
          const depNode = graph.nodes.get(depId);
          if (depNode) {
            depNode.outEdges.push(task.id);
            graph.edges.push({ from: depId, to: task.id });
          }
        }
      }
    }
    
    return graph;
  }
  
  /**
   * 重置团队状态
   * @param {boolean} clearHistory - 是否清除历史
   */
  reset(clearHistory = false) {
    this.taskQueue = [];
    this.results.clear();
    
    for (const agent of this.agents.values()) {
      agent.status = 'idle';
      agent.currentTask = null;
    }
    
    if (clearHistory) {
      this.history = [];
    }
    
    console.log(`[AgentTeam] 团队已重置`);
  }
  
  /**
   * 导出团队配置
   * @returns {object} 配置对象
   */
  export() {
    return {
      name: this.name,
      options: this.options,
      agents: this.listAgents(),
      taskCount: this.taskQueue.length,
      historySize: this.history.length
    };
  }
}

module.exports = {
  AgentTeam,
  // 导出预定义角色以便直接使用
  roles: require('./roles')
};
