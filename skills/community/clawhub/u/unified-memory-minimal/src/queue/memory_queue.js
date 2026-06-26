/**
 * Memory Queue System - 记忆队列系统
 * 借鉴 OpenViking 的队列设计
 */

import { logger } from '../logger.js';
import { EventEmitter } from 'events';

export class MemoryQueue extends EventEmitter {
  constructor(options = {}) {
    super();
    
    this.options = {
      maxQueueSize: options.maxQueueSize || 1000,
      maxConcurrent: options.maxConcurrent || 5,
      retryAttempts: options.retryAttempts || 3,
      retryDelay: options.retryDelay || 1000,
      processInterval: options.processInterval || 100,
      ...options
    };
    
    // 队列分类
    this.queues = {
      embedding: [],      // Embedding 任务队列
      semantic: [],       // 语义分析队列
      deduplication: [],  // 去重队列
      archiving: [],      // 归档队列
      indexing: []        // 索引队列
    };
    
    // 处理器映射
    this.processors = new Map();
    
    // 统计信息
    this.stats = {
      embedding: { pending: 0, inProgress: 0, processed: 0, failed: 0, total: 0 },
      semantic: { pending: 0, inProgress: 0, processed: 0, failed: 0, total: 0 },
      deduplication: { pending: 0, inProgress: 0, processed: 0, failed: 0, total: 0 },
      archiving: { pending: 0, inProgress: 0, processed: 0, failed: 0, total: 0 },
      indexing: { pending: 0, inProgress: 0, processed: 0, failed: 0, total: 0 }
    };
    
    // 正在处理的任务
    this.activeTasks = new Map();
    
    // 是否正在处理
    this.isProcessing = false;
    
    // 处理定时器
    this.processTimer = null;
    
    // 错误历史
    this.errorHistory = [];
    this.maxErrorHistory = 100;
    
    logger.info('[MemoryQueue] 队列系统初始化完成');
  }
  
  /**
   * 注册处理器
   */
  registerProcessor(queueName, processor) {
    if (!this.queues[queueName]) {
      throw new Error(`未知的队列类型: ${queueName}`);
    }
    
    this.processors.set(queueName, processor);
    logger.info(`[MemoryQueue] 注册处理器: ${queueName}`);
    
    return true;
  }
  
  /**
   * 入队任务
   */
  enqueue(queueName, task) {
    if (!this.queues[queueName]) {
      throw new Error(`未知的队列类型: ${queueName}`);
    }
    
    if (this.queues[queueName].length >= this.options.maxQueueSize) {
      throw new Error(`队列 ${queueName} 已满`);
    }
    
    const taskItem = {
      id: `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      queueName: queueName,
      data: task,
      priority: task.priority || 'normal',
      attempts: 0,
      maxAttempts: this.options.retryAttempts,
      createdAt: Date.now(),
      status: 'pending'
    };
    
    // 根据优先级插入
    if (taskItem.priority === 'high') {
      this.queues[queueName].unshift(taskItem);
    } else {
      this.queues[queueName].push(taskItem);
    }
    
    this.stats[queueName].pending++;
    this.stats[queueName].total++;
    
    logger.debug(`[MemoryQueue] 任务入队: ${taskItem.id} -> ${queueName}`);
    
    // 触发事件
    this.emit('task:enqueued', {
      queueName,
      taskId: taskItem.id,
      stats: this.stats[queueName]
    });
    
    // 启动处理
    if (!this.isProcessing) {
      this.startProcessing();
    }
    
    return taskItem.id;
  }
  
  /**
   * 批量入队
   */
  enqueueBatch(queueName, tasks) {
    const taskIds = [];
    
    for (const task of tasks) {
      const taskId = this.enqueue(queueName, task);
      taskIds.push(taskId);
    }
    
    logger.info(`[MemoryQueue] 批量入队: ${taskIds.length} 个任务 -> ${queueName}`);
    
    return taskIds;
  }
  
  /**
   * 启动处理
   */
  startProcessing() {
    if (this.isProcessing) {
      return;
    }
    
    this.isProcessing = true;
    
    logger.info('[MemoryQueue] 启动队列处理');
    
    // 启动定时处理
    this.processTimer = setInterval(() => {
      this.processQueues();
    }, this.options.processInterval);
    
    // 立即处理一次
    this.processQueues();
  }
  
  /**
   * 停止处理
   */
  stopProcessing() {
    this.isProcessing = false;
    
    if (this.processTimer) {
      clearInterval(this.processTimer);
      this.processTimer = null;
    }
    
    logger.info('[MemoryQueue] 停止队列处理');
  }
  
  /**
   * 处理所有队列
   */
  async processQueues() {
    for (const [queueName, queue] of Object.entries(this.queues)) {
      await this.processQueue(queueName);
    }
  }
  
  /**
   * 处理单个队列
   */
  async processQueue(queueName) {
    const queue = this.queues[queueName];
    const stats = this.stats[queueName];
    
    // 检查是否有可用槽位
    if (stats.inProgress >= this.options.maxConcurrent) {
      return;
    }
    
    // 检查是否有待处理任务
    if (queue.length === 0) {
      return;
    }
    
    // 取出任务
    const task = queue.shift();
    if (!task) {
      return;
    }
    
    // 更新统计
    stats.pending--;
    stats.inProgress++;
    task.status = 'processing';
    task.startedAt = Date.now();
    
    // 记录活动任务
    this.activeTasks.set(task.id, task);
    
    logger.debug(`[MemoryQueue] 开始处理任务: ${task.id} (${queueName})`);
    
    // 触发事件
    this.emit('task:started', {
      queueName,
      taskId: task.id,
      stats: stats
    });
    
    try {
      // 获取处理器
      const processor = this.processors.get(queueName);
      
      if (!processor) {
        throw new Error(`队列 ${queueName} 没有注册处理器`);
      }
      
      // 执行处理
      const result = await processor(task.data, task);
      
      // 处理成功
      task.status = 'completed';
      task.completedAt = Date.now();
      task.result = result;
      
      stats.inProgress--;
      stats.processed++;
      
      logger.debug(`[MemoryQueue] 任务完成: ${task.id} (${queueName}), 耗时: ${task.completedAt - task.startedAt}ms`);
      
      // 触发事件
      this.emit('task:completed', {
        queueName,
        taskId: task.id,
        result: result,
        duration: task.completedAt - task.startedAt
      });
      
    } catch (error) {
      // 处理失败
      task.attempts++;
      
      logger.error(`[MemoryQueue] 任务失败: ${task.id} (${queueName}), 尝试 ${task.attempts}/${task.maxAttempts}`, error);
      
      // 记录错误
      this.recordError(queueName, task, error);
      
      // 检查是否需要重试
      if (task.attempts < task.maxAttempts) {
        // 重新入队
        task.status = 'retrying';
        
        setTimeout(() => {
          if (task.priority === 'high') {
            this.queues[queueName].unshift(task);
          } else {
            this.queues[queueName].push(task);
          }
          
          stats.pending++;
          stats.inProgress--;
          
          logger.debug(`[MemoryQueue] 任务重试: ${task.id} (${queueName})`);
        }, this.options.retryDelay * task.attempts);
        
      } else {
        // 达到最大重试次数，标记为失败
        task.status = 'failed';
        task.failedAt = Date.now();
        task.error = error.message;
        
        stats.inProgress--;
        stats.failed++;
        
        logger.error(`[MemoryQueue] 任务最终失败: ${task.id} (${queueName})`);
        
        // 触发事件
        this.emit('task:failed', {
          queueName,
          taskId: task.id,
          error: error.message,
          attempts: task.attempts
        });
      }
    } finally {
      // 移除活动任务
      this.activeTasks.delete(task.id);
    }
  }
  
  /**
   * 记录错误
   */
  recordError(queueName, task, error) {
    const errorRecord = {
      queueName: queueName,
      taskId: task.id,
      error: error.message,
      stack: error.stack,
      timestamp: Date.now(),
      attempts: task.attempts
    };
    
    this.errorHistory.push(errorRecord);
    
    // 限制错误历史大小
    if (this.errorHistory.length > this.maxErrorHistory) {
      this.errorHistory.shift();
    }
  }
  
  /**
   * 获取队列状态
   */
  getQueueStats(queueName) {
    if (queueName) {
      return {
        name: queueName,
        ...this.stats[queueName],
        queueLength: this.queues[queueName].length
      };
    }
    
    // 返回所有队列状态
    const allStats = {};
    
    for (const [name, stats] of Object.entries(this.stats)) {
      allStats[name] = {
        name: name,
        ...stats,
        queueLength: this.queues[name].length
      };
    }
    
    return allStats;
  }
  
  /**
   * 获取任务状态
   */
  getTaskStatus(taskId) {
    // 检查活动任务
    if (this.activeTasks.has(taskId)) {
      return {
        ...this.activeTasks.get(taskId),
        isActive: true
      };
    }
    
    // 检查队列中的任务
    for (const [queueName, queue] of Object.entries(this.queues)) {
      const task = queue.find(t => t.id === taskId);
      if (task) {
        return {
          ...task,
          isActive: false,
          queueName: queueName
        };
      }
    }
    
    return null;
  }
  
  /**
   * 取消任务
   */
  cancelTask(taskId) {
    // 检查活动任务
    if (this.activeTasks.has(taskId)) {
      const task = this.activeTasks.get(taskId);
      task.status = 'cancelled';
      this.activeTasks.delete(taskId);
      
      this.stats[task.queueName].inProgress--;
      
      logger.info(`[MemoryQueue] 取消活动任务: ${taskId}`);
      
      this.emit('task:cancelled', {
        taskId: taskId,
        queueName: task.queueName
      });
      
      return true;
    }
    
    // 检查队列中的任务
    for (const [queueName, queue] of Object.entries(this.queues)) {
      const index = queue.findIndex(t => t.id === taskId);
      if (index !== -1) {
        const task = queue.splice(index, 1)[0];
        task.status = 'cancelled';
        
        this.stats[queueName].pending--;
        
        logger.info(`[MemoryQueue] 取消排队任务: ${taskId}`);
        
        this.emit('task:cancelled', {
          taskId: taskId,
          queueName: queueName
        });
        
        return true;
      }
    }
    
    return false;
  }
  
  /**
   * 清空队列
   */
  clearQueue(queueName) {
    if (!queueName) {
      // 清空所有队列
      for (const [name, queue] of Object.entries(this.queues)) {
        const cleared = queue.length;
        queue.length = 0;
        this.stats[name].pending = 0;
        
        logger.info(`[MemoryQueue] 清空队列 ${name}: ${cleared} 个任务`);
      }
    } else {
      // 清空指定队列
      const cleared = this.queues[queueName].length;
      this.queues[queueName].length = 0;
      this.stats[queueName].pending = 0;
      
      logger.info(`[MemoryQueue] 清空队列 ${queueName}: ${cleared} 个任务`);
    }
  }
  
  /**
   * 获取错误历史
   */
  getErrorHistory(limit = 20) {
    return this.errorHistory.slice(-limit);
  }
  
  /**
   * 清理错误历史
   */
  clearErrorHistory() {
    const cleared = this.errorHistory.length;
    this.errorHistory = [];
    
    logger.info(`[MemoryQueue] 清理错误历史: ${cleared} 条`);
    
    return cleared;
  }
  
  /**
   * 健康检查
   */
  healthCheck() {
    const health = {
      status: 'healthy',
      isProcessing: this.isProcessing,
      queues: {},
      activeTasks: this.activeTasks.size,
      errorCount: this.errorHistory.length
    };
    
    // 检查每个队列
    for (const [name, stats] of Object.entries(this.stats)) {
      health.queues[name] = {
        pending: stats.pending,
        inProgress: stats.inProgress,
        processed: stats.processed,
        failed: stats.failed,
        status: stats.failed > stats.processed * 0.1 ? 'degraded' : 'healthy'
      };
      
      if (health.queues[name].status === 'degraded') {
        health.status = 'degraded';
      }
    }
    
    // 检查错误率
    const totalProcessed = Object.values(this.stats).reduce((sum, s) => sum + s.processed, 0);
    const totalFailed = Object.values(this.stats).reduce((sum, s) => sum + s.failed, 0);
    
    if (totalProcessed > 0 && totalFailed / totalProcessed > 0.1) {
      health.status = 'degraded';
    }
    
    return health;
  }
  
  /**
   * 重置统计
   */
  resetStats(queueName) {
    if (queueName) {
      this.stats[queueName] = {
        pending: 0,
        inProgress: 0,
        processed: 0,
        failed: 0,
        total: 0
      };
    } else {
      for (const name of Object.keys(this.stats)) {
        this.stats[name] = {
          pending: 0,
          inProgress: 0,
          processed: 0,
          failed: 0,
          total: 0
        };
      }
    }
    
    logger.info(`[MemoryQueue] 重置统计: ${queueName || 'all'}`);
  }
}

// 导出单例
let queueInstance = null;

export function getMemoryQueue(options = {}) {
  if (!queueInstance) {
    queueInstance = new MemoryQueue(options);
  }
  return queueInstance;
}

export default MemoryQueue;