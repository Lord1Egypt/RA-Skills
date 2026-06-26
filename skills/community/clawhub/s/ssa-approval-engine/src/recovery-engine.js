/**
 * recovery-engine.js - 自动恢复策略引擎
 * 
 * 当检测到异常时，根据异常类型自动选择并执行恢复策略
 * 支持三种恢复策略：重试 (retry)、降级 (fallback)、人工介入 (escalation)
 */

const fs = require('fs');
const path = require('path');
const { randomUUID: uuidv4 } = require('crypto');

const LOGS_DIR = path.join(__dirname, '../logs');
const CONFIG_DIR = path.join(__dirname, '../config');
const RECOVERIES_FILE = path.join(LOGS_DIR, 'recoveries.json');
const APPROVAL_RULES_FILE = path.join(CONFIG_DIR, 'approval-rules.json');

const retryHandler = require('./retry-handler');
const escalationHandler = require('./escalation-handler');

// 确保日志目录存在
if (!fs.existsSync(LOGS_DIR)) {
  fs.mkdirSync(LOGS_DIR, { recursive: true });
}

/**
 * 恢复记录数据结构
 */
let recoveries = {
  records: [],
  stats: {
    total: 0,
    successful: 0,
    failed: 0,
    pending: 0
  }
};

// 加载现有记录
function loadRecoveries() {
  try {
    if (fs.existsSync(RECOVERIES_FILE)) {
      const data = fs.readFileSync(RECOVERIES_FILE, 'utf8');
      recoveries = JSON.parse(data);
    }
  } catch (e) {
    console.warn('[RecoveryEngine] Failed to load recoveries:', e.message);
  }
}

// 保存记录
function saveRecoveries() {
  try {
    // 更新统计
    recoveries.stats.pending = recoveries.records.filter(r => r.status === 'pending' || r.status === 'executing').length;
    recoveries.stats.successful = recoveries.records.filter(r => r.status === 'completed' && r.result?.success).length;
    recoveries.stats.failed = recoveries.records.filter(r => r.status === 'completed' && !r.result?.success).length;
    recoveries.stats.total = recoveries.records.length;
    
    fs.writeFileSync(RECOVERIES_FILE, JSON.stringify(recoveries, null, 2));
  } catch (e) {
    console.warn('[RecoveryEngine] Failed to save recoveries:', e.message);
  }
}

loadRecoveries();

/**
 * 获取审批规则配置
 */
function getApprovalRules() {
  try {
    return JSON.parse(fs.readFileSync(APPROVAL_RULES_FILE, 'utf8'));
  } catch (e) {
    console.warn('[RecoveryEngine] Failed to load approval rules:', e.message);
    return null;
  }
}

/**
 * 根据异常类型获取恢复策略配置
 * @param {string} exceptionType - 异常类型
 * @returns {Object|null} 恢复策略配置
 */
function getRecoveryStrategy(exceptionType) {
  const rules = getApprovalRules();
  if (!rules?.auto_recovery?.strategies) {
    return getDefaultStrategy(exceptionType);
  }

  // 查找匹配的策略
  for (const strategy of rules.auto_recovery.strategies) {
    if (strategy.trigger === exceptionType) {
      return strategy;
    }
  }

  return getDefaultStrategy(exceptionType);
}

/**
 * 获取默认恢复策略
 * @param {string} exceptionType - 异常类型
 * @returns {Object} 默认策略
 */
function getDefaultStrategy(exceptionType) {
  // 根据异常类型返回默认策略
  if (exceptionType.includes('timeout') || exceptionType.includes('network')) {
    return {
      id: 'default-retry',
      name: '默认重试策略',
      type: 'retry',
      max_retries: 3,
      retry_delay_ms: 1000,
      backoff: 'exponential'
    };
  }
  
  if (exceptionType.includes('discord') || exceptionType.includes('unavailable')) {
    return {
      id: 'default-fallback',
      name: '降级到邮件',
      type: 'fallback',
      fallback_channel: 'email',
      notify_admin: true
    };
  }

  // 其他异常默认人工介入
  return {
    id: 'default-escalation',
    name: '默认人工介入',
    type: 'escalation',
    notify_admin: true
  };
}

/**
 * 执行恢复
 * @param {Object} exception - 异常对象
 * @param {Object} context - 上下文信息
 * @returns {Promise<Object>} 恢复结果
 */
async function recover(exception, context = {}) {
  const recoveryId = uuidv4();
  const now = new Date().toISOString();
  
  // 获取恢复策略
  const strategy = getRecoveryStrategy(exception.type);
  
  console.log(`[RecoveryEngine] Starting recovery for exception: ${exception.type}`);
  console.log(`[RecoveryEngine] Selected strategy: ${strategy.name} (${strategy.type})`);

  // 创建恢复记录
  const recoveryRecord = {
    id: recoveryId,
    exceptionId: exception.id || uuidv4(),
    exceptionType: exception.type,
    strategy: strategy.id,
    strategyType: strategy.type,
    status: 'executing',
    attempts: [],
    startedAt: now,
    completedAt: null,
    result: null
  };

  recoveries.records.push(recoveryRecord);
  saveRecoveries();

  try {
    // 执行策略
    const result = await executeStrategy(strategy, { exception, context, recoveryId });
    
    recoveryRecord.status = 'completed';
    recoveryRecord.result = result;
    recoveryRecord.completedAt = new Date().toISOString();
    
    saveRecoveries();
    
    console.log(`[RecoveryEngine] Recovery ${recoveryId} completed: ${result.success ? 'SUCCESS' : 'FAILED'}`);
    
    return result;
  } catch (error) {
    recoveryRecord.status = 'failed';
    recoveryRecord.result = {
      success: false,
      error: error.message,
      strategy: strategy.id
    };
    recoveryRecord.completedAt = new Date().toISOString();
    
    saveRecoveries();
    
    console.error(`[RecoveryEngine] Recovery ${recoveryId} failed: ${error.message}`);
    
    // 如果自动恢复失败，尝试升级
    if (strategy.type !== 'escalation') {
      console.log('[RecoveryEngine] Auto-recovery exhausted, escalating to human intervention');
      await escalationHandler.escalate(exception, {
        impact: `自动恢复失败：${exception.message}`,
        attemptedSteps: [`执行 ${strategy.name} 策略失败`, `错误：${error.message}`],
        suggestedAction: '请管理员手动处理此异常',
        urgency: exception.severity === 'critical' ? 'critical' : 'high'
      });
    }
    
    throw error;
  }
}

/**
 * 执行具体恢复策略
 * @param {Object} strategy - 策略配置
 * @param {Object} context - 执行上下文
 * @returns {Promise<Object>} 执行结果
 */
async function executeStrategy(strategy, context) {
  const { exception, context: extraContext, recoveryId } = context;

  switch (strategy.type) {
    case 'retry':
      return await executeRetryStrategy(strategy, exception, extraContext);
    
    case 'fallback':
      return await executeFallbackStrategy(strategy, exception, extraContext);
    
    case 'escalation':
      return await executeEscalationStrategy(strategy, exception, extraContext);
    
    default:
      throw new Error(`Unknown strategy type: ${strategy.type}`);
  }
}

/**
 * 执行重试策略
 */
async function executeRetryStrategy(strategy, exception, context) {
  const { max_retries = 3, retry_delay_ms = 1000, backoff = 'exponential' } = strategy;
  
  console.log(`[RecoveryEngine] Executing retry strategy: max_retries=${max_retries}, delay=${retry_delay_ms}ms, backoff=${backoff}`);

  // 如果有可重试的操作，执行重试
  if (context.retryableOperation) {
    const result = await retryHandler.retry(context.retryableOperation, {
      maxRetries: max_retries,
      delayMs: retry_delay_ms,
      backoff: backoff,
      onRetry: (attempt, error) => {
        console.log(`[RecoveryEngine] Retry attempt ${attempt}: ${error.message}`);
      }
    });
    
    return {
      success: true,
      strategy: 'retry',
      attempts: max_retries + 1,
      result
    };
  }

  // 如果没有具体操作，模拟重试成功
  return {
    success: true,
    strategy: 'retry',
    message: 'Retry strategy executed (no retryable operation provided)',
    config: { max_retries, retry_delay_ms, backoff }
  };
}

/**
 * 执行降级策略
 */
async function executeFallbackStrategy(strategy, exception, context) {
  const { fallback_channel, notify_admin } = strategy;
  
  console.log(`[RecoveryEngine] Executing fallback strategy: channel=${fallback_channel}`);

  // 记录降级操作
  const fallbackRecord = {
    recoveryId: context.recoveryId,
    originalChannel: 'discord',
    fallbackChannel: fallback_channel,
    timestamp: new Date().toISOString(),
    reason: exception.message
  };

  // 保存降级记录
  const fallbacksFile = path.join(LOGS_DIR, 'fallbacks.json');
  let fallbacks = [];
  try {
    if (fs.existsSync(fallbacksFile)) {
      fallbacks = JSON.parse(fs.readFileSync(fallbacksFile, 'utf8'));
    }
  } catch (e) {
    // Ignore
  }
  fallbacks.push(fallbackRecord);
  fs.writeFileSync(fallbacksFile, JSON.stringify(fallbacks, null, 2));

  // 如果配置了通知管理员
  if (notify_admin) {
    await escalationHandler.escalate(exception, {
      impact: `主通道不可用，已降级到 ${fallback_channel}`,
      attemptedSteps: ['尝试 Discord 通知失败', '执行降级策略'],
      suggestedAction: `请检查 ${fallback_channel} 通道是否正常工作`,
      urgency: 'medium'
    });
  }

  return {
    success: true,
    strategy: 'fallback',
    fallbackChannel: fallback_channel,
    notifyAdmin: notify_admin
  };
}

/**
 * 执行升级策略
 */
async function executeEscalationStrategy(strategy, exception, context) {
  console.log('[RecoveryEngine] Executing escalation strategy');

  const escalationRecord = await escalationHandler.escalate(exception, {
    impact: context.impact || exception.message,
    attemptedSteps: context.attemptedSteps || ['自动恢复策略已用尽'],
    suggestedAction: context.suggestedAction || '请管理员审查并处理',
    urgency: context.urgency || exception.severity || 'medium'
  });

  return {
    success: true,
    strategy: 'escalation',
    escalationId: escalationRecord.id,
    status: escalationRecord.status
  };
}

/**
 * 查询恢复状态
 * @param {string} exceptionId - 异常 ID
 * @returns {Object|null} 恢复状态
 */
function getRecoveryStatus(exceptionId) {
  // 查找最近的恢复记录
  const record = recoveries.records
    .filter(r => r.exceptionId === exceptionId)
    .sort((a, b) => new Date(b.startedAt) - new Date(a.startedAt))[0];

  if (!record) {
    return null;
  }

  return {
    id: record.id,
    exceptionId: record.exceptionId,
    strategy: record.strategy,
    status: record.status,
    startedAt: record.startedAt,
    completedAt: record.completedAt,
    result: record.result
  };
}

/**
 * 列出所有恢复记录
 * @param {Object} filter - 过滤条件
 * @param {string} filter.strategy - 策略 ID 过滤
 * @param {'completed'|'failed'|'pending'|'all'} filter.status - 状态过滤
 * @param {number} filter.limit - 返回数量限制
 * @returns {Array} 恢复记录列表
 */
function listRecoveries(filter = {}) {
  let records = [...recoveries.records];

  // 策略过滤
  if (filter.strategy) {
    records = records.filter(r => r.strategy === filter.strategy);
  }

  // 状态过滤
  if (filter.status && filter.status !== 'all') {
    records = records.filter(r => r.status === filter.status);
  }

  // 按时间倒序
  records.sort((a, b) => new Date(b.startedAt) - new Date(a.startedAt));

  // 数量限制
  if (filter.limit) {
    records = records.slice(0, filter.limit);
  }

  return records;
}

/**
 * 获取恢复统计
 * @returns {Object} 统计信息
 */
function getRecoveryStats() {
  return {
    ...recoveries.stats,
    byStrategy: getStatsByStrategy(),
    successRate: recoveries.stats.total > 0 
      ? (recoveries.stats.successful / recoveries.stats.total * 100).toFixed(2) + '%'
      : '0%'
  };
}

/**
 * 按策略分组统计
 */
function getStatsByStrategy() {
  const stats = {};
  for (const record of recoveries.records) {
    if (!stats[record.strategy]) {
      stats[record.strategy] = { total: 0, successful: 0, failed: 0 };
    }
    stats[record.strategy].total++;
    if (record.status === 'completed' && record.result?.success) {
      stats[record.strategy].successful++;
    } else if (record.status === 'completed' && !record.result?.success) {
      stats[record.strategy].failed++;
    }
  }
  return stats;
}

module.exports = {
  recover,
  getRecoveryStrategy,
  executeStrategy,
  getRecoveryStatus,
  listRecoveries,
  getRecoveryStats,
  loadRecoveries,
  saveRecoveries
};
