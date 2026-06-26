/**
 * Memory Pipeline - 分层记忆处理管道
 * 借鉴 OpenViking 架构：L0→L1→L2→L3 渐进式处理
 */

import { logger } from './logger.js';
import { transcript_first } from './transcript_first.js';
import { extract } from './extract.js';
import { scene_block } from './scene_block.js';
import { profile } from './profile.js';
import { persona_generator } from './persona/index.js';

export class MemoryPipeline {
  constructor(options = {}) {
    this.options = {
      enableL0: true,    // 对话录制
      enableL1: true,    // 记忆提取
      enableL2: true,    // 场景归纳
      enableL3: true,    // 用户画像
      batchSize: 10,
      asyncProcessing: true,
      ...options
    };
    
    this.stages = {
      L0: this.options.enableL0 ? transcript_first : null,
      L1: this.options.enableL1 ? extract : null,
      L2: this.options.enableL2 ? scene_block : null,
      L3: this.options.enableL3 ? profile : null
    };
    
    this.status = {
      totalProcessed: 0,
      lastProcessed: null,
      errors: [],
      queueStats: {
        pending: 0,
        inProgress: 0,
        processed: 0,
        failed: 0
      }
    };
    
    this.queue = [];
    this.isProcessing = false;
  }
  
  /**
   * 处理新的对话数据
   */
  async processConversation(conversationData, context = {}) {
    const taskId = `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    const task = {
      id: taskId,
      data: conversationData,
      context,
      timestamp: Date.now(),
      stage: 'L0',
      results: {},
      status: 'pending'
    };
    
    this.queue.push(task);
    this.status.queueStats.pending++;
    
    logger.info(`[MemoryPipeline] 新任务入队: ${taskId}, 当前队列: ${this.queue.length}`);
    
    if (this.options.asyncProcessing && !this.isProcessing) {
      this.startProcessing();
    }
    
    return taskId;
  }
  
  /**
   * 启动异步处理
   */
  async startProcessing() {
    if (this.isProcessing) {
      return;
    }
    
    this.isProcessing = true;
    
    while (this.queue.length > 0 && this.isProcessing) {
      const batch = this.queue.splice(0, this.options.batchSize);
      this.status.queueStats.pending -= batch.length;
      this.status.queueStats.inProgress += batch.length;
      
      await Promise.all(
        batch.map(task => this.processTask(task))
      );
      
      this.status.queueStats.inProgress -= batch.length;
      this.status.queueStats.processed += batch.length;
    }
    
    this.isProcessing = false;
  }
  
  /**
   * 处理单个任务
   */
  async processTask(task) {
    try {
      task.status = 'processing';
      
      // L0: 对话录制
      if (this.stages.L0) {
        logger.debug(`[MemoryPipeline] 处理任务 ${task.id}: L0 对话录制`);
        task.results.L0 = await this.stages.L0.process(task.data, task.context);
        task.stage = 'L1';
      }
      
      // L1: 记忆提取
      if (this.stages.L1) {
        logger.debug(`[MemoryPipeline] 处理任务 ${task.id}: L1 记忆提取`);
        task.results.L1 = await this.stages.L1.extractFromText(
          task.results.L0?.transcript || task.data.text,
          task.context
        );
        task.stage = 'L2';
      }
      
      // L2: 场景归纳
      if (this.stages.L2) {
        logger.debug(`[MemoryPipeline] 处理任务 ${task.id}: L2 场景归纳`);
        task.results.L2 = await this.stages.L2.inductFromMemories(
          task.results.L1?.memories || [],
          task.context
        );
        task.stage = 'L3';
      }
      
      // L3: 用户画像
      if (this.stages.L3) {
        logger.debug(`[MemoryPipeline] 处理任务 ${task.id}: L3 用户画像`);
        task.results.L3 = await this.stages.L3.generateProfile(
          task.results.L2?.scenes || [],
          task.results.L1?.memories || [],
          task.context
        );
      }
      
      task.status = 'completed';
      task.completedAt = Date.now();
      
      this.status.totalProcessed++;
      this.status.lastProcessed = task.id;
      
      logger.info(`[MemoryPipeline] 任务完成: ${task.id}, 耗时: ${task.completedAt - task.timestamp}ms`);
      
    } catch (error) {
      logger.error(`[MemoryPipeline] 任务失败 ${task.id}:`, error);
      task.status = 'failed';
      task.error = error.message;
      task.failedAt = Date.now();
      
      this.status.queueStats.failed++;
      this.status.errors.push({
        taskId: task.id,
        error: error.message,
        timestamp: Date.now()
      });
    }
  }
  
  /**
   * 获取管道状态
   */
  getStatus() {
    return {
      ...this.status,
      queueLength: this.queue.length,
      isProcessing: this.isProcessing,
      stagesEnabled: {
        L0: !!this.stages.L0,
        L1: !!this.stages.L1,
        L2: !!this.stages.L2,
        L3: !!this.stages.L3
      }
    };
  }
  
  /**
   * 获取任务结果
   */
  getTaskResult(taskId) {
    const task = this.queue.find(t => t.id === taskId) || 
                 this.status.lastProcessed === taskId ? 
                 { id: taskId, status: 'completed' } : null;
    
    if (!task) {
      return { error: `任务 ${taskId} 不存在` };
    }
    
    return {
      taskId: task.id,
      status: task.status,
      stage: task.stage,
      results: task.results || {},
      timestamp: task.timestamp,
      completedAt: task.completedAt,
      error: task.error
    };
  }
  
  /**
   * 手动触发特定阶段
   */
  async triggerStage(stage, data, context = {}) {
    const validStages = ['L0', 'L1', 'L2', 'L3'];
    
    if (!validStages.includes(stage)) {
      throw new Error(`无效的阶段: ${stage}, 有效值: ${validStages.join(', ')}`);
    }
    
    if (!this.stages[stage]) {
      throw new Error(`阶段 ${stage} 未启用`);
    }
    
    logger.info(`[MemoryPipeline] 手动触发阶段: ${stage}`);
    
    switch (stage) {
      case 'L0':
        return await this.stages.L0.process(data, context);
      case 'L1':
        return await this.stages.L1.extractFromText(data, context);
      case 'L2':
        return await this.stages.L2.inductFromMemories(data, context);
      case 'L3':
        return await this.stages.L3.generateProfile(data, context);
    }
  }
  
  /**
   * 清理错误记录
   */
  clearErrors(maxAgeHours = 24) {
    const cutoff = Date.now() - (maxAgeHours * 60 * 60 * 1000);
    const initialCount = this.status.errors.length;
    
    this.status.errors = this.status.errors.filter(
      error => error.timestamp > cutoff
    );
    
    const removed = initialCount - this.status.errors.length;
    logger.info(`[MemoryPipeline] 清理了 ${removed} 条错误记录`);
    
    return { removed, remaining: this.status.errors.length };
  }
  
  /**
   * 停止处理
   */
  stop() {
    this.isProcessing = false;
    logger.info('[MemoryPipeline] 处理已停止');
  }
}

// 导出单例
let pipelineInstance = null;

export function getMemoryPipeline(options = {}) {
  if (!pipelineInstance) {
    pipelineInstance = new MemoryPipeline(options);
  }
  return pipelineInstance;
}

export default MemoryPipeline;