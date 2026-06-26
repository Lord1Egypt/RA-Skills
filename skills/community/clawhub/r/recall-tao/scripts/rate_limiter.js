/**
 * 频率限制管理器 - 回复频率控制
 * 支持：分钟/小时/日限制、随机延迟、突发保护
 * 
 * 版本：v1.0
 * 更新日期：2026-04-02
 */

const fs = require('fs');
const path = require('path');

// ==================== 配置加载 ====================

let rateLimitConfig = null;
const CONFIG_PATH = path.join(__dirname, '../config/rate_limit_config.json');

// 运行时状态
const runtimeState = {
  replyHistory: [], // { timestamp, commentId }
  lastReplyTime: null,
  consecutiveCount: 0,
  isPaused: false,
  pauseUntil: null
};

function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_PATH)) {
      const content = fs.readFileSync(CONFIG_PATH, 'utf-8');
      rateLimitConfig = JSON.parse(content);
    }
  } catch (error) {
    console.error('加载频率限制配置失败:', error.message);
    rateLimitConfig = getDefaultConfig();
  }
  return rateLimitConfig;
}

function getDefaultConfig() {
  return {
    enabled: true,
    limits: {
      perMinute: { max: 5, windowMs: 60000 },
      perHour: { max: 50, windowMs: 3600000 },
      perDay: { max: 500, windowMs: 86400000 }
    },
    randomDelay: {
      enabled: true,
      minMs: 3000,
      maxMs: 10000
    },
    burstProtection: {
      enabled: true,
      maxConsecutive: 3,
      cooldownMs: 30000
    }
  };
}

// ==================== 核心函数 ====================

/**
 * 检查是否可以发送回复
 * @returns {{ allowed: boolean, reason: string, waitMs: number }}
 */
function canSendReply() {
  if (!rateLimitConfig) {
    loadConfig();
  }
  
  const now = Date.now();
  
  // 检查是否暂停中
  if (runtimeState.isPaused && runtimeState.pauseUntil) {
    if (now < runtimeState.pauseUntil) {
      return {
        allowed: false,
        reason: '频率限制触发，暂停中',
        waitMs: runtimeState.pauseUntil - now,
        limitType: 'pause'
      };
    } else {
      // 暂停结束，重置状态
      runtimeState.isPaused = false;
      runtimeState.pauseUntil = null;
    }
  }
  
  // 清理过期记录
  cleanHistory(now);
  
  // 检查分钟限制
  const minuteCheck = checkLimit('perMinute', now);
  if (!minuteCheck.allowed) {
    return minuteCheck;
  }
  
  // 检查小时限制
  const hourCheck = checkLimit('perHour', now);
  if (!hourCheck.allowed) {
    return hourCheck;
  }
  
  // 检查日限制
  const dayCheck = checkLimit('perDay', now);
  if (!dayCheck.allowed) {
    return dayCheck;
  }
  
  // 检查突发保护
  const burstCheck = checkBurstProtection(now);
  if (!burstCheck.allowed) {
    return burstCheck;
  }
  
  return {
    allowed: true,
    reason: '频率检查通过'
  };
}

/**
 * 检查特定时间窗口的限制
 * @param {string} limitType 限制类型
 * @param {number} now 当前时间戳
 */
function checkLimit(limitType, now) {
  const limit = rateLimitConfig.limits[limitType];
  if (!limit) return { allowed: true };
  
  const windowStart = now - limit.windowMs;
  const countInWindow = runtimeState.replyHistory.filter(r => r.timestamp > windowStart).length;
  
  if (countInWindow >= limit.max) {
    const oldestInWindow = runtimeState.replyHistory.find(r => r.timestamp > windowStart);
    const waitMs = oldestInWindow ? (oldestInWindow.timestamp + limit.windowMs - now) : limit.windowMs;
    
    // 触发限制，是否需要暂停
    if (rateLimitConfig.strategy?.onLimitReached === 'pause') {
      triggerPause(rateLimitConfig.strategy.pauseDurationMs || 60000);
    }
    
    return {
      allowed: false,
      reason: `${limitType} 限制触发 (${countInWindow}/${limit.max})`,
      waitMs,
      limitType,
      current: countInWindow,
      max: limit.max
    };
  }
  
  return { allowed: true };
}

/**
 * 检查突发保护
 * @param {number} now 当前时间戳
 */
function checkBurstProtection(now) {
  const burst = rateLimitConfig.burstProtection;
  if (!burst || !burst.enabled) {
    return { allowed: true };
  }
  
  // 检查最近是否有连续快速回复
  if (runtimeState.consecutiveCount >= burst.maxConsecutive) {
    const timeSinceLastReply = now - (runtimeState.lastReplyTime || 0);
    
    if (timeSinceLastReply < burst.cooldownMs) {
      return {
        allowed: false,
        reason: `突发保护触发，连续回复 ${runtimeState.consecutiveCount} 次，冷却中`,
        waitMs: burst.cooldownMs - timeSinceLastReply,
        limitType: 'burst'
      };
    } else {
      // 冷却结束，重置连续计数
      runtimeState.consecutiveCount = 0;
    }
  }
  
  return { allowed: true };
}

/**
 * 记录一次回复
 * @param {string} commentId 评论ID
 */
function recordReply(commentId) {
  const now = Date.now();
  
  runtimeState.replyHistory.push({
    timestamp: now,
    commentId
  });
  
  // 更新连续计数
  if (runtimeState.lastReplyTime && (now - runtimeState.lastReplyTime) < 10000) {
    runtimeState.consecutiveCount++;
  } else {
    runtimeState.consecutiveCount = 1;
  }
  
  runtimeState.lastReplyTime = now;
  
  return {
    timestamp: now,
    consecutiveCount: runtimeState.consecutiveCount
  };
}

/**
 * 获取随机延迟时间
 * @returns {number} 延迟毫秒数
 */
function getRandomDelay() {
  const delay = rateLimitConfig?.randomDelay;
  if (!delay || !delay.enabled) {
    return 0;
  }
  
  const { minMs, maxMs } = delay;
  return Math.floor(Math.random() * (maxMs - minMs + 1)) + minMs;
}

/**
 * 触发暂停
 * @param {number} durationMs 暂停时长（毫秒）
 */
function triggerPause(durationMs) {
  runtimeState.isPaused = true;
  runtimeState.pauseUntil = Date.now() + durationMs;
  
  console.warn(`[频率限制] 触发暂停，${durationMs / 1000}秒后恢复`);
  
  return {
    paused: true,
    until: new Date(runtimeState.pauseUntil).toISOString()
  };
}

/**
 * 清理过期的历史记录
 * @param {number} now 当前时间戳
 */
function cleanHistory(now) {
  // 保留最近24小时的记录
  const cutoff = now - 86400000;
  runtimeState.replyHistory = runtimeState.replyHistory.filter(r => r.timestamp > cutoff);
}

/**
 * 获取当前频率状态
 * @returns {object}
 */
function getRateLimitStatus() {
  const now = Date.now();
  cleanHistory(now);
  
  return {
    enabled: rateLimitConfig?.enabled || false,
    currentMinute: {
      count: runtimeState.replyHistory.filter(r => r.timestamp > now - 60000).length,
      max: rateLimitConfig?.limits?.perMinute?.max || 5
    },
    currentHour: {
      count: runtimeState.replyHistory.filter(r => r.timestamp > now - 3600000).length,
      max: rateLimitConfig?.limits?.perHour?.max || 50
    },
    currentDay: {
      count: runtimeState.replyHistory.filter(r => r.timestamp > now - 86400000).length,
      max: rateLimitConfig?.limits?.perDay?.max || 500
    },
    isPaused: runtimeState.isPaused,
    pauseUntil: runtimeState.pauseUntil ? new Date(runtimeState.pauseUntil).toISOString() : null,
    consecutiveCount: runtimeState.consecutiveCount
  };
}

/**
 * 重置频率限制状态
 */
function resetState() {
  runtimeState.replyHistory = [];
  runtimeState.lastReplyTime = null;
  runtimeState.consecutiveCount = 0;
  runtimeState.isPaused = false;
  runtimeState.pauseUntil = null;
  
  return { reset: true, timestamp: new Date().toISOString() };
}

// ==================== 配置更新 ====================

/**
 * 更新频率限制配置
 * @param {object} newConfig 新配置
 */
function updateConfig(newConfig) {
  rateLimitConfig = {
    ...rateLimitConfig,
    ...newConfig,
    lastUpdated: new Date().toISOString()
  };
  
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(rateLimitConfig, null, 2), 'utf-8');
  return rateLimitConfig;
}

// ==================== 导出 ====================

module.exports = {
  // 核心函数
  canSendReply,
  recordReply,
  getRandomDelay,
  getRateLimitStatus,
  
  // 暂停控制
  triggerPause,
  resetState,
  
  // 配置管理
  loadConfig,
  updateConfig
};

// 初始化加载配置
loadConfig();
