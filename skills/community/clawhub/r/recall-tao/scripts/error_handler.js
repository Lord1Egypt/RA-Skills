/**
 * 异常处理器
 * 职责：捕获异常、分类处理、自动恢复
 */

const logger = require('./logger.js');

// 异常类型枚举
const ErrorTypes = {
  // 网络类
  NETWORK_TIMEOUT: 'NETWORK_TIMEOUT',
  NETWORK_ERROR: 'NETWORK_ERROR',
  CONNECTION_LOST: 'CONNECTION_LOST',
  
  // 登录类
  LOGIN_EXPIRED: 'LOGIN_EXPIRED',
  LOGIN_REQUIRED: 'LOGIN_REQUIRED',
  SESSION_INVALID: 'SESSION_INVALID',
  
  // 页面类
  PAGE_NOT_FOUND: 'PAGE_NOT_FOUND',
  ELEMENT_NOT_FOUND: 'ELEMENT_NOT_FOUND',
  PAGE_LOAD_ERROR: 'PAGE_LOAD_ERROR',
  
  // 操作类
  REPLY_FAILED: 'REPLY_FAILED',
  COMMENT_LOAD_FAILED: 'COMMENT_LOAD_FAILED',
  RATE_LIMITED: 'RATE_LIMITED',
  
  // 浏览器类
  BROWSER_CRASH: 'BROWSER_CRASH',
  BROWSER_CLOSED: 'BROWSER_CLOSED',
  
  // 未知
  UNKNOWN: 'UNKNOWN'
};

// 异常严重级别
const Severity = {
  LOW: 'low',       // 可忽略，继续运行
  MEDIUM: 'medium', // 需要处理，但可恢复
  HIGH: 'high',     // 需要人工介入
  CRITICAL: 'critical' // 系统级错误
};

// 异常处理策略
const handlers = {
  [ErrorTypes.NETWORK_TIMEOUT]: {
    severity: Severity.MEDIUM,
    retryable: true,
    maxRetries: 3,
    retryDelayMs: 5000,
    recoveryAction: 'retry_with_backoff'
  },
  [ErrorTypes.NETWORK_ERROR]: {
    severity: Severity.MEDIUM,
    retryable: true,
    maxRetries: 3,
    retryDelayMs: 10000,
    recoveryAction: 'retry_with_backoff'
  },
  [ErrorTypes.CONNECTION_LOST]: {
    severity: Severity.HIGH,
    retryable: true,
    maxRetries: 5,
    retryDelayMs: 30000,
    recoveryAction: 'reconnect'
  },
  [ErrorTypes.LOGIN_EXPIRED]: {
    severity: Severity.HIGH,
    retryable: false,
    recoveryAction: 'require_login'
  },
  [ErrorTypes.LOGIN_REQUIRED]: {
    severity: Severity.HIGH,
    retryable: false,
    recoveryAction: 'require_login'
  },
  [ErrorTypes.SESSION_INVALID]: {
    severity: Severity.HIGH,
    retryable: true,
    maxRetries: 2,
    retryDelayMs: 5000,
    recoveryAction: 'refresh_session'
  },
  [ErrorTypes.PAGE_NOT_FOUND]: {
    severity: Severity.MEDIUM,
    retryable: false,
    recoveryAction: 'navigate_home'
  },
  [ErrorTypes.ELEMENT_NOT_FOUND]: {
    severity: Severity.LOW,
    retryable: true,
    maxRetries: 3,
    retryDelayMs: 2000,
    recoveryAction: 'retry_with_refresh'
  },
  [ErrorTypes.PAGE_LOAD_ERROR]: {
    severity: Severity.MEDIUM,
    retryable: true,
    maxRetries: 3,
    retryDelayMs: 5000,
    recoveryAction: 'reload_page'
  },
  [ErrorTypes.REPLY_FAILED]: {
    severity: Severity.LOW,
    retryable: true,
    maxRetries: 2,
    retryDelayMs: 3000,
    recoveryAction: 'retry_reply'
  },
  [ErrorTypes.COMMENT_LOAD_FAILED]: {
    severity: Severity.MEDIUM,
    retryable: true,
    maxRetries: 3,
    retryDelayMs: 5000,
    recoveryAction: 'reload_comments'
  },
  [ErrorTypes.RATE_LIMITED]: {
    severity: Severity.LOW,
    retryable: true,
    maxRetries: 1,
    retryDelayMs: 60000,
    recoveryAction: 'wait_and_retry'
  },
  [ErrorTypes.BROWSER_CRASH]: {
    severity: Severity.CRITICAL,
    retryable: true,
    maxRetries: 2,
    retryDelayMs: 10000,
    recoveryAction: 'restart_browser'
  },
  [ErrorTypes.BROWSER_CLOSED]: {
    severity: Severity.HIGH,
    retryable: true,
    maxRetries: 1,
    retryDelayMs: 5000,
    recoveryAction: 'restart_browser'
  },
  [ErrorTypes.UNKNOWN]: {
    severity: Severity.MEDIUM,
    retryable: true,
    maxRetries: 1,
    retryDelayMs: 5000,
    recoveryAction: 'log_and_continue'
  }
};

// 异常统计
let stats = {
  totalErrors: 0,
  byType: {},
  bySeverity: {},
  lastError: null,
  recoverySuccess: 0,
  recoveryFailed: 0
};

/**
 * 分类异常
 * @param {Error} error - 错误对象
 * @param {Object} context - 上下文信息
 * @returns {Object} 分类结果
 */
function classifyError(error, context = {}) {
  const message = error.message?.toLowerCase() || '';
  const name = error.name?.toLowerCase() || '';
  
  // 网络类
  if (message.includes('timeout') || name.includes('timeout')) {
    return { type: ErrorTypes.NETWORK_TIMEOUT, severity: Severity.MEDIUM };
  }
  if (message.includes('network') || message.includes('enetunreach') || message.includes('econnrefused')) {
    return { type: ErrorTypes.NETWORK_ERROR, severity: Severity.MEDIUM };
  }
  if (message.includes('connection') && (message.includes('lost') || message.includes('closed'))) {
    return { type: ErrorTypes.CONNECTION_LOST, severity: Severity.HIGH };
  }
  
  // 登录类
  if (message.includes('login') && (message.includes('expired') || message.includes('required'))) {
    return { type: ErrorTypes.LOGIN_REQUIRED, severity: Severity.HIGH };
  }
  if (message.includes('session') && (message.includes('invalid') || message.includes('expired'))) {
    return { type: ErrorTypes.SESSION_INVALID, severity: Severity.HIGH };
  }
  if (message.includes('unauthorized') || message.includes('401')) {
    return { type: ErrorTypes.LOGIN_REQUIRED, severity: Severity.HIGH };
  }
  
  // 页面类 - 注意顺序，element not found 要在 404/not found 之前
  if (message.includes('element') && message.includes('not found')) {
    return { type: ErrorTypes.ELEMENT_NOT_FOUND, severity: Severity.LOW };
  }
  if (message.includes('404') || (message.includes('not found') && !message.includes('element'))) {
    return { type: ErrorTypes.PAGE_NOT_FOUND, severity: Severity.MEDIUM };
  }
  if (message.includes('page') && message.includes('load')) {
    return { type: ErrorTypes.PAGE_LOAD_ERROR, severity: Severity.MEDIUM };
  }
  
  // 操作类
  if (context.operation === 'reply' && message.includes('failed')) {
    return { type: ErrorTypes.REPLY_FAILED, severity: Severity.LOW };
  }
  if (context.operation === 'load_comments') {
    return { type: ErrorTypes.COMMENT_LOAD_FAILED, severity: Severity.MEDIUM };
  }
  if (message.includes('rate limit') || message.includes('too many')) {
    return { type: ErrorTypes.RATE_LIMITED, severity: Severity.LOW };
  }
  
  // 浏览器类
  if (message.includes('browser') && (message.includes('crash') || message.includes('disconnect'))) {
    return { type: ErrorTypes.BROWSER_CRASH, severity: Severity.CRITICAL };
  }
  if (message.includes('target closed') || message.includes('browser closed')) {
    return { type: ErrorTypes.BROWSER_CLOSED, severity: Severity.HIGH };
  }
  
  return { type: ErrorTypes.UNKNOWN, severity: Severity.MEDIUM };
}

/**
 * 获取处理策略
 * @param {string} errorType - 错误类型
 * @returns {Object} 处理策略
 */
function getHandler(errorType) {
  return handlers[errorType] || handlers[ErrorTypes.UNKNOWN];
}

/**
 * 记录异常
 * @param {Error} error - 错误对象
 * @param {Object} classification - 分类结果
 * @param {Object} context - 上下文
 */
function recordError(error, classification, context) {
  stats.totalErrors++;
  
  // 按类型统计
  if (!stats.byType[classification.type]) {
    stats.byType[classification.type] = 0;
  }
  stats.byType[classification.type]++;
  
  // 按严重级别统计
  if (!stats.bySeverity[classification.severity]) {
    stats.bySeverity[classification.severity] = 0;
  }
  stats.bySeverity[classification.severity]++;
  
  // 记录最后一次错误
  stats.lastError = {
    type: classification.type,
    severity: classification.severity,
    message: error.message,
    timestamp: new Date().toISOString(),
    context
  };
  
  // 写入日志
  logger.error(`[${classification.type}] ${error.message}`, {
    severity: classification.severity,
    context
  });
}

/**
 * 异常处理器主函数
 * @param {Error} error - 错误对象
 * @param {Object} context - 上下文信息
 * @param {Object} options - 处理选项
 * @returns {Promise<Object>} 处理结果
 */
async function handle(error, context = {}, options = {}) {
  // 分类
  const classification = classifyError(error, context);
  const handler = getHandler(classification.type);
  
  // 记录
  recordError(error, classification, context);
  
  console.log(`[ErrorHandler] 处理异常: ${classification.type} (${classification.severity})`);
  
  // 构建结果
  const result = {
    type: classification.type,
    severity: classification.severity,
    retryable: handler.retryable,
    recoveryAction: handler.recoveryAction,
    handled: false,
    retryCount: 0,
    message: error.message
  };
  
  // 根据严重级别决定是否继续
  if (classification.severity === Severity.CRITICAL) {
    result.handled = false;
    result.requiresHumanIntervention = true;
    return result;
  }
  
  // 可重试的处理
  if (handler.retryable && options.retryFn) {
    const maxRetries = handler.maxRetries || 3;
    
    for (let i = 0; i < maxRetries; i++) {
      result.retryCount = i + 1;
      console.log(`[ErrorHandler] 重试 ${i + 1}/${maxRetries}...`);
      
      try {
        // 等待后重试
        await sleep(handler.retryDelayMs * (i + 1)); // 指数退避
        
        const retryResult = await options.retryFn();
        
        if (retryResult) {
          result.handled = true;
          stats.recoverySuccess++;
          console.log(`[ErrorHandler] ✅ 重试成功`);
          return result;
        }
      } catch (retryError) {
        console.log(`[ErrorHandler] 重试失败: ${retryError.message}`);
      }
    }
    
    stats.recoveryFailed++;
    result.handled = false;
  }
  
  // 特殊恢复动作
  if (handler.recoveryAction && options.recoveryActions) {
    const action = options.recoveryActions[handler.recoveryAction];
    if (action) {
      try {
        await action();
        result.handled = true;
      } catch (recoveryError) {
        console.error(`[ErrorHandler] 恢复动作失败: ${recoveryError.message}`);
        result.handled = false;
      }
    }
  }
  
  return result;
}

/**
 * 包装异步函数，自动处理异常
 * @param {Function} fn - 异步函数
 * @param {Object} context - 上下文
 * @param {Object} options - 处理选项
 * @returns {Promise<any>}
 */
async function wrapAsync(fn, context = {}, options = {}) {
  try {
    return await fn();
  } catch (error) {
    const result = await handle(error, context, {
      ...options,
      retryFn: options.autoRetry ? fn : undefined
    });
    
    if (!result.handled) {
      throw new Error(`异常未被处理: ${result.type} - ${result.message}`);
    }
    
    return result;
  }
}

/**
 * 创建重试包装器
 * @param {Function} fn - 要包装的函数
 * @param {Object} options - 重试选项
 * @returns {Function}
 */
function withRetry(fn, options = {}) {
  const { maxRetries = 3, delayMs = 5000, backoff = true } = options;
  
  return async (...args) => {
    let lastError;
    
    for (let i = 0; i < maxRetries; i++) {
      try {
        return await fn(...args);
      } catch (error) {
        lastError = error;
        
        if (i < maxRetries - 1) {
          const delay = backoff ? delayMs * (i + 1) : delayMs;
          console.log(`[Retry] 第${i + 1}次失败，${delay}ms后重试...`);
          await sleep(delay);
        }
      }
    }
    
    throw lastError;
  };
}

/**
 * 获取统计信息
 */
function getStats() {
  return { ...stats };
}

/**
 * 重置统计
 */
function resetStats() {
  stats = {
    totalErrors: 0,
    byType: {},
    bySeverity: {},
    lastError: null,
    recoverySuccess: 0,
    recoveryFailed: 0
  };
}

// 辅助函数
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

module.exports = {
  ErrorTypes,
  Severity,
  classifyError,
  getHandler,
  handle,
  wrapAsync,
  withRetry,
  getStats,
  resetStats
};
