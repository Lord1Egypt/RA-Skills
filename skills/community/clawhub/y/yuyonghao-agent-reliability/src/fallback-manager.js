/**
 * FallbackManager - 回退管理模块
 * 失败检测触发、回退策略配置、状态恢复和优雅降级
 */

const EventEmitter = require('events');

class FallbackManager extends EventEmitter {
  /**
   * @param {Object} options - 配置选项
   * @param {number} options.maxRetries - 最大重试次数 (默认 3)
   * @param {string} options.backoffStrategy - 退避策略: 'exponential' | 'linear' | 'fixed' (默认 'exponential')
   * @param {number} options.initialDelay - 初始延迟(ms) (默认 1000)
   * @param {number} options.maxDelay - 最大延迟(ms) (默认 30000)
   * @param {number} options.timeout - 操作超时(ms) (默认 30000)
   * @param {boolean} options.enableLogging - 是否启用日志 (默认 true)
   */
  constructor(options = {}) {
    super();
    
    this.maxRetries = options.maxRetries ?? 3;
    this.backoffStrategy = options.backoffStrategy ?? 'exponential';
    this.initialDelay = options.initialDelay ?? 1000;
    this.maxDelay = options.maxDelay ?? 30000;
    this.timeout = options.timeout ?? 30000;
    this.enableLogging = options.enableLogging ?? true;
    
    // 执行状态
    this.executionState = new Map();
    
    // 回退策略注册表
    this.fallbackStrategies = new Map();
    
    // 统计
    this.stats = {
      totalExecutions: 0,
      successfulExecutions: 0,
      fallbackExecutions: 0,
      failedExecutions: 0,
      totalRetries: 0
    };
    
    this._log('FallbackManager initialized', {
      maxRetries: this.maxRetries,
      backoffStrategy: this.backoffStrategy,
      initialDelay: this.initialDelay
    });
  }
  
  /**
   * 执行带回退的操作
   * @param {Function} primaryOperation - 主操作 (async function)
   * @param {Object} options - 执行选项
   * @param {Function} options.fallback - 回退操作 (async function)
   * @param {Function} options.onFailure - 失败回调
   * @param {Function} options.onRetry - 重试回调
   * @param {Function} options.onSuccess - 成功回调
   * @param {Function} options.stateRecovery - 状态恢复函数
   * @param {number} options.customMaxRetries - 自定义最大重试次数
   * @param {string} options.executionId - 执行ID
   * @returns {Promise} 执行结果
   */
  async execute(primaryOperation, options = {}) {
    const executionId = options.executionId || `exec-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const maxRetries = options.customMaxRetries ?? this.maxRetries;
    
    this.stats.totalExecutions++;
    
    // 初始化执行状态
    const state = {
      id: executionId,
      startTime: Date.now(),
      attempts: 0,
      lastError: null,
      fallbackUsed: false,
      recovered: false
    };
    this.executionState.set(executionId, state);
    
    this._log(`Starting execution ${executionId}`);
    this.emit('execution:start', { executionId });
    
    try {
      // 尝试主操作
      const result = await this._tryPrimary(primaryOperation, state, maxRetries, options);
      
      state.endTime = Date.now();
      state.duration = state.endTime - state.startTime;
      state.success = true;
      
      this.stats.successfulExecutions++;
      
      if (options.onSuccess) {
        await options.onSuccess(result, state);
      }
      
      this._log(`Execution ${executionId} succeeded`, { duration: state.duration, attempts: state.attempts });
      this.emit('execution:success', { executionId, result, state });
      
      return {
        success: true,
        result,
        executionId,
        state: this._sanitizeState(state)
      };
      
    } catch (primaryError) {
      this._log(`Primary operation failed after ${state.attempts} attempts`, { error: primaryError.message });
      
      // 尝试回退操作
      if (options.fallback) {
        try {
          this._log(`Attempting fallback for ${executionId}`);
          this.emit('fallback:start', { executionId, error: primaryError });
          
          // 状态恢复
          if (options.stateRecovery) {
            await options.stateRecovery(state);
            state.recovered = true;
          }
          
          const fallbackResult = await this._executeWithTimeout(options.fallback, this.timeout);
          
          state.fallbackUsed = true;
          state.endTime = Date.now();
          state.duration = state.endTime - state.startTime;
          state.success = true;
          
          this.stats.fallbackExecutions++;
          
          this._log(`Fallback succeeded for ${executionId}`);
          this.emit('fallback:success', { executionId, result: fallbackResult, state });
          
          return {
            success: true,
            result: fallbackResult,
            executionId,
            fallbackUsed: true,
            state: this._sanitizeState(state)
          };
          
        } catch (fallbackError) {
          this._log(`Fallback failed for ${executionId}`, { error: fallbackError.message });
          this.emit('fallback:failure', { executionId, error: fallbackError });
        }
      }
      
      // 全部失败
      state.endTime = Date.now();
      state.duration = state.endTime - state.startTime;
      state.success = false;
      state.lastError = primaryError;
      
      this.stats.failedExecutions++;
      
      if (options.onFailure) {
        await options.onFailure(primaryError, state);
      }
      
      this._log(`Execution ${executionId} failed`, { duration: state.duration, error: primaryError.message });
      this.emit('execution:failure', { executionId, error: primaryError, state });
      
      throw new FallbackExecutionError(
        `Execution failed after ${state.attempts} attempts`,
        primaryError,
        this._sanitizeState(state)
      );
    }
  }
  
  /**
   * 尝试主操作
   * @private
   */
  async _tryPrimary(operation, state, maxRetries, options) {
    let lastError = null;
    
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      state.attempts = attempt + 1;
      
      if (attempt > 0) {
        this.stats.totalRetries++;
        const delay = this._calculateDelay(attempt);
        
        this._log(`Retry ${attempt}/${maxRetries} for ${state.id} after ${delay}ms`);
        
        if (options.onRetry) {
          await options.onRetry(attempt, delay, lastError);
        }
        
        this.emit('execution:retry', { executionId: state.id, attempt, delay });
        await this._sleep(delay);
      }
      
      try {
        const result = await this._executeWithTimeout(operation, this.timeout);
        return result;
      } catch (error) {
        lastError = error;
        state.lastError = error;
        
        this._log(`Attempt ${attempt + 1} failed`, { error: error.message });
        
        // 如果是不可恢复的错误，立即停止
        if (this._isNonRecoverableError(error)) {
          throw error;
        }
      }
    }
    
    throw lastError;
  }
  
  /**
   * 计算退避延迟
   * @private
   */
  _calculateDelay(attempt) {
    let delay;
    
    switch (this.backoffStrategy) {
      case 'exponential':
        delay = this.initialDelay * Math.pow(2, attempt - 1);
        break;
      case 'linear':
        delay = this.initialDelay * attempt;
        break;
      case 'fixed':
      default:
        delay = this.initialDelay;
    }
    
    // 添加抖动 (±20%)
    const jitter = delay * 0.2 * (Math.random() * 2 - 1);
    delay = delay + jitter;
    
    return Math.min(delay, this.maxDelay);
  }
  
  /**
   * 带超时执行
   * @private
   */
  async _executeWithTimeout(operation, timeout) {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        reject(new Error(`Operation timed out after ${timeout}ms`));
      }, timeout);
      
      Promise.resolve(operation())
        .then(result => {
          clearTimeout(timer);
          resolve(result);
        })
        .catch(error => {
          clearTimeout(timer);
          reject(error);
        });
    });
  }
  
  /**
   * 判断是否不可恢复的错误
   * @private
   */
  _isNonRecoverableError(error) {
    const nonRecoverablePatterns = [
      /ENOTFOUND/,
      /EACCES/,
      /EPERM/,
      /EINVAL/,
      /SyntaxError/,
      /TypeError/,
      /ReferenceError/
    ];
    
    const errorMessage = error.message || error.toString();
    return nonRecoverablePatterns.some(pattern => pattern.test(errorMessage));
  }
  
  /**
   * 注册回退策略
   * @param {string} name - 策略名称
   * @param {Function} strategy - 策略函数
   */
  registerStrategy(name, strategy) {
    this.fallbackStrategies.set(name, strategy);
    this._log(`Registered fallback strategy: ${name}`);
  }
  
  /**
   * 使用命名策略执行
   * @param {string} strategyName - 策略名称
   * @param {Function} primaryOperation - 主操作
   * @param {Object} options - 选项
   */
  async executeWithStrategy(strategyName, primaryOperation, options = {}) {
    const strategy = this.fallbackStrategies.get(strategyName);
    if (!strategy) {
      throw new Error(`Unknown fallback strategy: ${strategyName}`);
    }
    
    return this.execute(primaryOperation, {
      ...options,
      fallback: strategy
    });
  }
  
  /**
   * 获取执行状态
   * @param {string} executionId - 执行ID
   * @returns {Object|null} 执行状态
   */
  getExecutionState(executionId) {
    const state = this.executionState.get(executionId);
    return state ? this._sanitizeState(state) : null;
  }
  
  /**
   * 获取统计信息
   * @returns {Object} 统计信息
   */
  getStats() {
    return {
      ...this.stats,
      successRate: this.stats.totalExecutions > 0 
        ? this.stats.successfulExecutions / this.stats.totalExecutions 
        : 0,
      fallbackRate: this.stats.totalExecutions > 0 
        ? this.stats.fallbackExecutions / this.stats.totalExecutions 
        : 0,
      failureRate: this.stats.totalExecutions > 0 
        ? this.stats.failedExecutions / this.stats.totalExecutions 
        : 0,
      averageRetries: this.stats.totalExecutions > 0 
        ? this.stats.totalRetries / this.stats.totalExecutions 
        : 0
    };
  }
  
  /**
   * 重置统计
   */
  resetStats() {
    this.stats = {
      totalExecutions: 0,
      successfulExecutions: 0,
      fallbackExecutions: 0,
      failedExecutions: 0,
      totalRetries: 0
    };
    this.executionState.clear();
    this._log('Stats reset');
  }
  
  /**
   * 清理旧状态
   * @param {number} olderThan - 清理多久前的状态(ms)
   */
  cleanup(olderThan) {
    const cutoff = Date.now() - olderThan;
    let removed = 0;
    
    for (const [id, state] of this.executionState.entries()) {
      if (state.endTime && state.endTime < cutoff) {
        this.executionState.delete(id);
        removed++;
      }
    }
    
    this._log('Cleanup completed', { removed, remaining: this.executionState.size });
    return { removed, remaining: this.executionState.size };
  }
  
  /**
   * 清理状态对象 (移除敏感信息)
   * @private
   */
  _sanitizeState(state) {
    return {
      id: state.id,
      startTime: state.startTime,
      endTime: state.endTime,
      duration: state.duration,
      attempts: state.attempts,
      success: state.success,
      fallbackUsed: state.fallbackUsed,
      recovered: state.recovered,
      lastError: state.lastError ? state.lastError.message : null
    };
  }
  
  /**
   * 睡眠
   * @private
   */
  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  /**
   * 日志记录
   * @private
   */
  _log(message, data = null) {
    if (!this.enableLogging) return;
    
    const timestamp = new Date().toISOString();
    if (data) {
      console.log(`[${timestamp}] [FallbackManager] ${message}:`, data);
    } else {
      console.log(`[${timestamp}] [FallbackManager] ${message}`);
    }
  }
}

/**
 * 回退执行错误
 */
class FallbackExecutionError extends Error {
  constructor(message, originalError, state) {
    super(message);
    this.name = 'FallbackExecutionError';
    this.originalError = originalError;
    this.state = state;
  }
}

module.exports = FallbackManager;
module.exports.FallbackExecutionError = FallbackExecutionError;