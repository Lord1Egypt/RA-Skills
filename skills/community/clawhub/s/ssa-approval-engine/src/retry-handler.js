/**
 * retry-handler.js - 重试处理器
 * 
 * 实现自动重试机制，支持固定延迟和指数退避策略
 * 用于处理临时性失败（网络抖动、API 限流等）
 */

const fs = require('fs');
const path = require('path');

const LOGS_DIR = path.join(__dirname, '../logs');
const STATS_FILE = path.join(LOGS_DIR, 'retry-stats.json');

// 确保日志目录存在
if (!fs.existsSync(LOGS_DIR)) {
  fs.mkdirSync(LOGS_DIR, { recursive: true });
}

/**
 * 重试统计数据结构
 */
let retryStats = {
  totalAttempts: 0,
  successfulRetries: 0,
  failedRetries: 0,
  byOperation: {},
  lastReset: new Date().toISOString()
};

// 加载现有统计
function loadStats() {
  try {
    if (fs.existsSync(STATS_FILE)) {
      const data = fs.readFileSync(STATS_FILE, 'utf8');
      retryStats = JSON.parse(data);
    }
  } catch (e) {
    console.warn('[RetryHandler] Failed to load stats:', e.message);
  }
}

// 保存统计
function saveStats() {
  try {
    fs.writeFileSync(STATS_FILE, JSON.stringify(retryStats, null, 2));
  } catch (e) {
    console.warn('[RetryHandler] Failed to save stats:', e.message);
  }
}

loadStats();

/**
 * 计算延迟时间
 * @param {number} attempt - 当前重试次数 (从 1 开始)
 * @param {number} baseDelayMs - 基础延迟 (毫秒)
 * @param {'fixed'|'exponential'} backoff - 退避策略
 * @returns {number} 延迟时间 (毫秒)
 */
function calculateDelay(attempt, baseDelayMs, backoff) {
  if (backoff === 'exponential') {
    // 指数退避：delay * 2^(attempt-1)
    return baseDelayMs * Math.pow(2, attempt - 1);
  }
  // 固定延迟
  return baseDelayMs;
}

/**
 * 执行重试
 * @param {Function} operation - 异步操作函数 (返回 Promise)
 * @param {Object} options - 重试配置
 * @param {number} options.maxRetries - 最大重试次数 (默认 3)
 * @param {number} options.delayMs - 基础延迟毫秒数 (默认 1000)
 * @param {'fixed'|'exponential'} options.backoff - 退避策略 (默认 'exponential')
 * @param {Function} options.onRetry - 每次重试时的回调 (attempt, error) => void
 * @returns {Promise<any>} 操作结果
 */
async function retry(operation, options = {}) {
  const {
    maxRetries = 3,
    delayMs = 1000,
    backoff = 'exponential',
    onRetry = null
  } = options;

  const operationName = operation.name || 'anonymous';
  let lastError = null;

  for (let attempt = 1; attempt <= maxRetries + 1; attempt++) {
    retryStats.totalAttempts++;
    
    // 初始化操作统计
    if (!retryStats.byOperation[operationName]) {
      retryStats.byOperation[operationName] = {
        attempts: 0,
        successes: 0,
        failures: 0
      };
    }
    retryStats.byOperation[operationName].attempts++;

    try {
      const result = await operation();
      
      // 成功
      retryStats.successfulRetries++;
      retryStats.byOperation[operationName].successes++;
      saveStats();
      
      return result;
    } catch (error) {
      lastError = error;
      retryStats.failedRetries++;
      retryStats.byOperation[operationName].failures++;
      
      if (attempt <= maxRetries) {
        // 还有重试机会
        const delay = calculateDelay(attempt, delayMs, backoff);
        
        console.log(
          `[RetryHandler] Operation "${operationName}" failed (attempt ${attempt}/${maxRetries + 1}). ` +
          `Retrying in ${delay}ms. Error: ${error.message}`
        );
        
        if (onRetry) {
          onRetry(attempt, error);
        }
        
        await sleep(delay);
      } else {
        // 所有重试已用尽
        console.error(
          `[RetryHandler] Operation "${operationName}" failed after ${maxRetries + 1} attempts. ` +
          `Final error: ${error.message}`
        );
      }
    }
  }

  saveStats();
  throw lastError;
}

/**
 * 包装函数使其支持自动重试
 * @param {Function} fn - 要包装的异步函数
 * @param {Object} options - 重试配置 (同 retry)
 * @returns {Function} 包装后的函数
 */
function withRetry(fn, options = {}) {
  return async function(...args) {
    return retry(() => fn(...args), options);
  };
}

/**
 * 获取重试统计
 * @returns {Object} 统计信息
 */
function getRetryStats() {
  return {
    ...retryStats,
    successRate: retryStats.totalAttempts > 0 
      ? (retryStats.successfulRetries / retryStats.totalAttempts * 100).toFixed(2) + '%'
      : '0%'
  };
}

/**
 * 重置统计
 */
function resetStats() {
  retryStats = {
    totalAttempts: 0,
    successfulRetries: 0,
    failedRetries: 0,
    byOperation: {},
    lastReset: new Date().toISOString()
  };
  saveStats();
}

/**
 * 睡眠指定时间
 * @param {number} ms - 毫秒数
 * @returns {Promise<void>}
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 带重试的 Discord 消息发送示例
 * @param {Object} webhookConfig - webhook 配置
 * @param {Object} payload - 消息内容
 * @param {Object} options - 重试配置
 */
async function sendWithRetry(webhookConfig, payload, options = {}) {
  const retryOptions = {
    maxRetries: 3,
    delayMs: 1000,
    backoff: 'exponential',
    onRetry: (attempt, error) => {
      console.log(`[Discord] Retry attempt ${attempt} failed: ${error.message}`);
    }
  };

  return retry(async () => {
    const response = await fetch(webhookConfig.url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`Discord API returned ${response.status}: ${response.statusText}`);
    }

    return response;
  }, { ...retryOptions, ...options });
}

module.exports = {
  retry,
  withRetry,
  getRetryStats,
  resetStats,
  sendWithRetry,
  calculateDelay,
  sleep
};
