/**
 * pipeline_scheduler.js — 自动调度管线
 * 
 * 实现 memory-tencentdb 风格的自动调度：
 * - L0 → L1: 每 N 轮对话后触发
 * - L1 → L2: L1 完成后延迟触发
 * - L2 → L3: 每 M 条新记忆触发
 * 
 * 四层管线架构：
 * L0 (对话录制) → transcript_first.js
 * L1 (记忆提取) → extract.js
 * L2 (场景归纳) → scene_block.js
 * L3 (用户画像) → profile.js
 */

import { log } from './logger.js';
import { config } from './config.js';

// ─── 配置 ───────────────────────────────────────────────────────────────────

const DEFAULT_CONFIG = {
  enabled: true,
  everyNConversations: 5,      // 每 N 轮对话触发 L1
  enableWarmup: true,          // Warm-up 模式: 1→2→4→8→...→N
  l1IdleTimeoutSeconds: 60,    // 用户停止对话后多久触发 L1
  l2DelayAfterL1Seconds: 90,   // L1 完成后延迟多久触发 L2
  l2MinIntervalSeconds: 300,   // 同一 session 两次 L2 的最小间隔
  l2MaxIntervalSeconds: 1800,  // 活跃 session 的 L2 最大轮询间隔
  sessionActiveWindowHours: 24, // 超过此时间不活跃的 session 停止 L2 轮询
  l3TriggerEveryN: 50,         // 每 N 条新记忆触发 L3
};

// ─── 管线调度器 ─────────────────────────────────────────────────────────────

class PipelineScheduler {
  constructor(options = {}) {
    this.config = { ...DEFAULT_CONFIG, ...options };
    
    // Session 状态
    this.sessionCounters = new Map();      // sessionId -> counter
    this.sessionLastActive = new Map();    // sessionId -> timestamp
    this.sessionL1Pending = new Map();     // sessionId -> timeoutId
    this.sessionL2Pending = new Map();     // sessionId -> timeoutId
    
    // L3 计数器
    this.l3Counter = 0;
    
    // L2 时间追踪
    this.lastL2Time = 0;
    
    // 统计
    this.stats = {
      l1Executions: 0,
      l2Executions: 0,
      l3Executions: 0,
      memoriesExtracted: 0,
      scenesGenerated: 0,
    };
    
    log.info('[PipelineScheduler] Initialized with config:', this.config);
  }
  
  // ─── 对话结束处理 ─────────────────────────────────────────────────────────
  
  /**
   * 记录对话结束，触发管线检查
   * @param {string} sessionId - 会话 ID
   * @param {string} [scope='USER'] - 范围
   */
  async onConversationEnd(sessionId, scope = 'USER') {
    if (!this.config.enabled) {
      log.debug('[PipelineScheduler] Pipeline disabled, skipping');
      return;
    }
    
    // 更新计数器
    const counter = (this.sessionCounters.get(sessionId) || 0) + 1;
    this.sessionCounters.set(sessionId, counter);
    this.sessionLastActive.set(sessionId, Date.now());
    
    log.info(`[PipelineScheduler] Conversation end for session ${sessionId}, counter: ${counter}`);
    
    // 检查是否触发 L1
    const effectiveN = this.getEffectiveN(sessionId);
    if (counter % effectiveN === 0) {
      log.info(`[PipelineScheduler] Triggering L1 for session ${sessionId} (counter ${counter} % ${effectiveN} = 0)`);
      await this.scheduleL1(sessionId, scope);
    }
  }
  
  /**
   * 获取有效的 N 值（Warm-up 模式）
   */
  getEffectiveN(sessionId) {
    if (!this.config.enableWarmup) {
      return this.config.everyNConversations;
    }
    
    // Warm-up: 1 → 2 → 4 → 8 → ... → N
    const counter = this.sessionCounters.get(sessionId) || 0;
    const maxN = this.config.everyNConversations;
    
    // 找到最大的 2^k <= counter 且 2^k <= maxN
    let effectiveN = 1;
    while (effectiveN * 2 <= counter && effectiveN * 2 <= maxN) {
      effectiveN *= 2;
    }
    
    return Math.max(1, Math.min(effectiveN, maxN));
  }
  
  // ─── L1 调度 ───────────────────────────────────────────────────────────────
  
  /**
   * 调度 L1 提取
   */
  async scheduleL1(sessionId, scope = 'USER') {
    // 取消之前的待处理 L1
    const existingTimeout = this.sessionL1Pending.get(sessionId);
    if (existingTimeout) {
      clearTimeout(existingTimeout);
    }
    
    log.info(`[PipelineScheduler] Scheduling L1 for session ${sessionId} in ${this.config.l1IdleTimeoutSeconds}s`);
    
    // 延迟执行（等待用户停止对话）
    const timeoutId = setTimeout(async () => {
      await this.executeL1WithRetry(sessionId, scope);
    }, this.config.l1IdleTimeoutSeconds * 1000);
    
    this.sessionL1Pending.set(sessionId, timeoutId);
  }
  
  /**
   * 执行 L1（带重试）
   */
  async executeL1WithRetry(sessionId, scope, retries = 3) {
    // 检查是否仍在活跃
    const lastActive = this.sessionLastActive.get(sessionId) || 0;
    const idleTime = Date.now() - lastActive;
    
    if (idleTime < this.config.l1IdleTimeoutSeconds * 1000) {
      log.info(`[PipelineScheduler] Session ${sessionId} still active, rescheduling L1`);
      await this.scheduleL1(sessionId, scope);
      return;
    }
    
    try {
      await this.executeL1(sessionId, scope);
    } catch (err) {
      log.error(`[PipelineScheduler] L1 execution failed:`, err);
      
      if (retries > 0) {
        log.info(`[PipelineScheduler] Retrying L1 (${retries} retries left)`);
        await new Promise(resolve => setTimeout(resolve, 5000));
        await this.executeL1WithRetry(sessionId, scope, retries - 1);
      }
    }
  }
  
  /**
   * 执行 L1 提取
   */
  async executeL1(sessionId, scope = 'USER') {
    log.info(`[PipelineScheduler] Executing L1 for session ${sessionId}`);
    
    try {
      // 动态导入避免循环依赖
      const { extractMemories } = await import('./extract.js');
      const memories = await extractMemories({ sessionId, scope });
      
      this.stats.l1Executions++;
      this.stats.memoriesExtracted += memories?.length || 0;
      
      // 更新 L3 计数器
      this.l3Counter += memories?.length || 0;
      
      log.info(`[PipelineScheduler] L1 completed: ${memories?.length || 0} memories extracted`);
      
      // 调度 L2
      setTimeout(() => this.scheduleL2(sessionId, scope), 
        this.config.l2DelayAfterL1Seconds * 1000);
      
      // 检查是否触发 L3
      if (this.l3Counter >= this.config.l3TriggerEveryN) {
        log.info(`[PipelineScheduler] L3 threshold reached (${this.l3Counter} >= ${this.config.l3TriggerEveryN})`);
        await this.scheduleL3(scope);
        this.l3Counter = 0;
      }
      
      return memories;
    } catch (err) {
      log.error(`[PipelineScheduler] L1 execution error:`, err);
      throw err;
    }
  }
  
  // ─── L2 调度 ───────────────────────────────────────────────────────────────
  
  /**
   * 调度 L2 场景归纳
   */
  async scheduleL2(sessionId, scope = 'USER') {
    // 检查最小间隔
    const elapsed = Date.now() - this.lastL2Time;
    
    if (elapsed < this.config.l2MinIntervalSeconds * 1000) {
      log.info(`[PipelineScheduler] L2 skipped: too soon (${Math.round(elapsed / 1000)}s < ${this.config.l2MinIntervalSeconds}s)`);
      return;
    }
    
    // 检查 session 是否仍活跃
    const lastActive = this.sessionLastActive.get(sessionId) || 0;
    const sessionAge = Date.now() - lastActive;
    
    if (sessionAge > this.config.sessionActiveWindowHours * 60 * 60 * 1000) {
      log.info(`[PipelineScheduler] L2 skipped: session inactive for ${Math.round(sessionAge / 1000 / 60)} minutes`);
      return;
    }
    
    log.info(`[PipelineScheduler] Executing L2 for session ${sessionId}`);
    
    try {
      await this.executeL2(scope);
    } catch (err) {
      log.error(`[PipelineScheduler] L2 execution error:`, err);
    }
  }
  
  /**
   * 执行 L2 场景归纳
   */
  async executeL2(scope = 'USER') {
    log.info(`[PipelineScheduler] Executing L2 for scope ${scope}`);
    
    try {
      const { inductScenes } = await import('./scene_block.js');
      const scenes = await inductScenes({ scope });
      
      this.stats.l2Executions++;
      this.stats.scenesGenerated += scenes?.length || 0;
      this.lastL2Time = Date.now();
      
      log.info(`[PipelineScheduler] L2 completed: ${scenes?.length || 0} scenes generated`);
      
      return scenes;
    } catch (err) {
      log.error(`[PipelineScheduler] L2 execution error:`, err);
      throw err;
    }
  }
  
  // ─── L3 调度 ───────────────────────────────────────────────────────────────
  
  /**
   * 调度 L3 用户画像更新
   */
  async scheduleL3(scope = 'USER') {
    log.info(`[PipelineScheduler] Scheduling L3 for scope ${scope}`);
    await this.executeL3(scope);
  }
  
  /**
   * 执行 L3 用户画像更新
   */
  async executeL3(scope = 'USER') {
    log.info(`[PipelineScheduler] Executing L3 for scope ${scope}`);
    
    try {
      const { getProfile, updateProfile } = await import('./profile.js');
      
      // 获取并更新画像
      const profile = await getProfile({ scope });
      
      this.stats.l3Executions++;
      
      log.info(`[PipelineScheduler] L3 completed: profile updated`);
      
      return profile;
    } catch (err) {
      log.error(`[PipelineScheduler] L3 execution error:`, err);
      throw err;
    }
  }
  
  // ─── 手动触发 ─────────────────────────────────────────────────────────────
  
  /**
   * 手动触发管线阶段
   */
  async trigger(stage, sessionId, scope = 'USER') {
    switch (stage) {
      case 'L1':
        return await this.executeL1(sessionId, scope);
      case 'L2':
        return await this.executeL2(scope);
      case 'L3':
        return await this.executeL3(scope);
      default:
        throw new Error(`Unknown stage: ${stage}`);
    }
  }
  
  // ─── 状态查询 ─────────────────────────────────────────────────────────────
  
  /**
   * 获取调度器状态
   */
  getStatus() {
    return {
      enabled: this.config.enabled,
      config: this.config,
      sessions: {
        active: this.sessionCounters.size,
        counters: Object.fromEntries(this.sessionCounters),
      },
      l3Counter: this.l3Counter,
      lastL2Time: this.lastL2Time,
      stats: this.stats,
    };
  }
  
  /**
   * 重置统计
   */
  resetStats() {
    this.stats = {
      l1Executions: 0,
      l2Executions: 0,
      l3Executions: 0,
      memoriesExtracted: 0,
      scenesGenerated: 0,
    };
  }
  
  /**
   * 更新配置
   */
  updateConfig(newConfig) {
    this.config = { ...this.config, ...newConfig };
    log.info('[PipelineScheduler] Config updated:', this.config);
  }
}

// ─── 单例实例 ───────────────────────────────────────────────────────────────

export const scheduler = new PipelineScheduler();

// ─── 便捷函数 ───────────────────────────────────────────────────────────────

export async function onConversationEnd(sessionId, scope = 'USER') {
  return await scheduler.onConversationEnd(sessionId, scope);
}

export async function triggerPipeline(stage, sessionId, scope = 'USER') {
  return await scheduler.trigger(stage, sessionId, scope);
}

export function getPipelineStatus() {
  return scheduler.getStatus();
}

export default scheduler;
