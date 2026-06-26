/**
 * Team Lead - Main Entry Point
 * 多 Agent 协作主管 - 主入口
 */

import { AgentRegistry } from './agent-registry.js';
import { TaskDecomposer } from './task-decomposer.js';
import { TaskDispatcher } from './dispatcher.js';
import { ResultAggregator } from './result-aggregator.js';
import { QualityChecker } from './quality-checker.js';

/**
 * Team Lead 主类
 */
export class TeamLead {
  constructor(options = {}) {
    console.log('[TeamLead] Initializing...');
    
    this.options = {
      maxParallelAgents: 5,
      defaultTimeout: 300,
      retryAttempts: 2,
      qualityThreshold: 0.75,
      enableCaching: true,
      ...options
    };

    // 初始化核心组件
    this.registry = new AgentRegistry();
    this.decomposer = new TaskDecomposer();
    this.dispatcher = new TaskDispatcher(this.registry, {
      defaultTimeout: this.options.defaultTimeout,
      retryAttempts: this.options.retryAttempts
    });
    this.aggregator = new ResultAggregator();
    this.qualityChecker = new QualityChecker({
      qualityThreshold: this.options.qualityThreshold
    });

    // 任务历史
    this.taskHistory = [];
    this.activeTasks = new Map();

    console.log('[TeamLead] Initialized with options:', this.options);
  }

  /**
   * 执行复杂任务
   */
  async execute(task, context = {}) {
    const taskId = `task-${Date.now()}`;
    console.log(`\n[TeamLead] === Starting Task: ${taskId} ===`);
    console.log(`[TeamLead] Task: ${task.substring(0, 100)}...`);

    const taskRecord = {
      id: taskId,
      originalTask: task,
      context,
      startedAt: Date.now(),
      status: 'running'
    };

    this.activeTasks.set(taskId, taskRecord);

    try {
      // Step 1: 任务分解
      console.log('\n[TeamLead] Step 1: Decomposing task...');
      const decomposition = this.decomposer.decompose(task, context);
      taskRecord.decomposition = decomposition;
      
      console.log(`[TeamLead] Template: ${decomposition.template}`);
      console.log(`[TeamLead] Subtasks: ${decomposition.subtasks.length}`);
      console.log(`[TeamLead] Estimated time: ${decomposition.estimatedTotalTime}s`);

      // Step 2: 任务分发与执行
      console.log('\n[TeamLead] Step 2: Dispatching subtasks...');
      const dispatchResults = await this.executeSubtasks(decomposition.subtasks);
      taskRecord.dispatchResults = dispatchResults;

      // Step 3: 质量检查
      console.log('\n[TeamLead] Step 3: Quality check...');
      const qualityReports = await this.qualityChecker.checkBatch(
        dispatchResults.results,
        {
          taskType: decomposition.template,
          keywords: this.extractKeywords(task)
        }
      );
      taskRecord.qualityReports = qualityReports;

      console.log(`[TeamLead] Quality summary: ${qualityReports.summary.passed}/${qualityReports.summary.total} passed`);

      // Step 4: 结果聚合
      console.log('\n[TeamLead] Step 4: Aggregating results...');
      const strategy = this.selectAggregationStrategy(decomposition);
      const aggregated = await this.aggregator.aggregate(
        dispatchResults.results,
        strategy,
        context
      );
      taskRecord.aggregated = aggregated;

      // Step 5: 最终质量评估
      const finalQuality = this.calculateFinalQuality(qualityReports, aggregated);
      taskRecord.finalQuality = finalQuality;

      // 完成任务
      taskRecord.status = 'completed';
      taskRecord.completedAt = Date.now();
      taskRecord.duration = taskRecord.completedAt - taskRecord.startedAt;

      console.log(`\n[TeamLead] === Task Completed: ${taskId} ===`);
      console.log(`[TeamLead] Duration: ${Math.round(taskRecord.duration / 1000)}s`);
      console.log(`[TeamLead] Final Quality: ${Math.round(finalQuality * 100)}%`);

      // 记录历史
      this.taskHistory.push(taskRecord);

      return {
        taskId,
        result: aggregated,
        quality: finalQuality,
        duration: taskRecord.duration,
        stats: this.getTaskStats(taskRecord)
      };

    } catch (error) {
      console.error(`[TeamLead] Task failed: ${error.message}`);
      taskRecord.status = 'failed';
      taskRecord.error = error.message;
      taskRecord.failedAt = Date.now();

      this.activeTasks.delete(taskId);
      throw error;
    }
  }

  /**
   * 执行子任务
   */
  async executeSubtasks(subtasks) {
    const results = [];
    const errors = [];
    const completed = new Set();

    // 按照执行计划分组执行
    const groups = this.groupByExecutionOrder(subtasks);

    for (const group of groups) {
      console.log(`\n[TeamLead] Executing group (${group.type}): ${group.subtasks.length} subtasks`);

      const groupPromises = group.subtasks.map(async (subtask) => {
        // 等待依赖完成
        if (subtask.dependsOn.length > 0) {
          await this.waitForDependencies(subtask.dependsOn, completed);
        }

        try {
          const result = await this.dispatcher.dispatch(subtask);
          results.push({
            ...result,
            subtaskId: subtask.id,
            completedAt: Date.now()
          });
          completed.add(subtask.id);
          return result;
        } catch (error) {
          errors.push({
            subtaskId: subtask.id,
            error: error.message
          });
          throw error;
        }
      });

      await Promise.allSettled(groupPromises);

      // 如果是串行组且有错误，停止执行
      if (group.type === 'sequential' && errors.length > 0) {
        console.warn(`[TeamLead] Stopping sequential execution due to errors`);
        break;
      }
    }

    return {
      results,
      errors,
      successRate: (subtasks.length - errors.length) / subtasks.length,
      completedCount: completed.size,
      totalCount: subtasks.length
    };
  }

  /**
   * 按执行顺序分组
   */
  groupByExecutionOrder(subtasks) {
    const groups = [];
    const visited = new Set();
    const remaining = [...subtasks];

    while (remaining.length > 0) {
      const ready = remaining.filter(s =>
        s.dependsOn.every(dep => visited.has(dep))
      );

      if (ready.length === 0) {
        console.warn('[TeamLead] Circular dependency detected, breaking...');
        break;
      }

      const isParallel = ready[0].parallel;
      groups.push({
        type: isParallel ? 'parallel' : 'sequential',
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
   * 等待依赖完成
   */
  async waitForDependencies(deps, completed) {
    const checkInterval = 100;
    const timeout = 30000;
    const startTime = Date.now();

    while (Date.now() - startTime < timeout) {
      const allCompleted = deps.every(dep => completed.has(dep));
      if (allCompleted) return;
      
      await new Promise(resolve => setTimeout(resolve, checkInterval));
    }

    throw new Error(`Timeout waiting for dependencies: ${deps.join(', ')}`);
  }

  /**
   * 选择聚合策略
   */
  selectAggregationStrategy(decomposition) {
    // 根据任务类型选择聚合策略
    const strategyMap = {
      research: 'merge',
      coding: 'chain',
      content: 'merge',
      translation: 'merge',
      design: 'select-best',
      learning: 'chain',
      heuristic: 'merge'
    };

    return strategyMap[decomposition.template] || 'merge';
  }

  /**
   * 提取任务关键词
   */
  extractKeywords(task) {
    // 简单提取：移除停用词，保留名词性词汇
    const stopwords = new Set(['的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个']);
    const words = task.split(/[\s,，.。?!？！]+/).filter(w => w.length > 1 && !stopwords.has(w));
    return words.slice(0, 10);
  }

  /**
   * 计算最终质量
   */
  calculateFinalQuality(qualityReports, aggregated) {
    const avgQuality = qualityReports.summary.avgScore;
    const completeness = qualityReports.summary.passed / qualityReports.summary.total;
    
    // 聚合结果质量调整
    let adjustment = 0;
    if (aggregated.type === 'consensus' && aggregated.hasConflicts) {
      adjustment = -0.05; // 有冲突，略微降分
    }
    if (aggregated.avgQuality && aggregated.avgQuality > 0.9) {
      adjustment = 0.05; // 高质量，略微加分
    }

    return Math.max(0, Math.min(1, (avgQuality + completeness) / 2 + adjustment));
  }

  /**
   * 获取任务统计
   */
  getTaskStats(taskRecord) {
    return {
      subtasksCompleted: taskRecord.dispatchResults?.completedCount || 0,
      subtasksTotal: taskRecord.dispatchResults?.totalCount || 0,
      qualityPassed: taskRecord.qualityReports?.summary.passed || 0,
      qualityTotal: taskRecord.qualityReports?.summary.total || 0,
      aggregationStrategy: taskRecord.aggregated?.strategy,
      finalQuality: Math.round(taskRecord.finalQuality * 100)
    };
  }

  /**
   * 获取系统状态
   */
  getStatus() {
    return {
      activeTasks: this.activeTasks.size,
      totalTasksCompleted: this.taskHistory.length,
      registryStats: this.registry.getStats(),
      dispatcherStats: this.dispatcher.getActiveStats(),
      qualityStats: this.qualityChecker.getStats()
    };
  }

  /**
   * 导出任务历史
   */
  exportHistory(limit = 50) {
    return this.taskHistory.slice(-limit).map(task => ({
      id: task.id,
      task: task.originalTask,
      status: task.status,
      duration: task.duration,
      quality: task.finalQuality,
      completedAt: task.completedAt
    }));
  }

  /**
   * 清除历史
   */
  clearHistory(olderThan = 3600000) {
    const cutoff = Date.now() - olderThan;
    const initialCount = this.taskHistory.length;
    
    this.taskHistory = this.taskHistory.filter(task => 
      task.completedAt > cutoff || task.status === 'running'
    );

    console.log(`[TeamLead] Cleared ${initialCount - this.taskHistory.length} old task records`);
  }
}

// 导出默认实例
export default TeamLead;
