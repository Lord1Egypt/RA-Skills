// Token Tracker Hook - 集成到 OpenClaw 主程序

import { tokenTracker } from './token-tracker';

// 会话信息
let currentSession = {
  startTime: Date.now(),
  model: process.env.OPENCLAW_MODEL || 'unknown',
  sessionKey: process.env.SESSION_KEY || undefined
};

// 记录开始
export function recordSessionStart() {
  console.log('📝 记录会话开始...');
  console.log(`模型: ${currentSession.model}`);
  console.log(`开始时间: ${new Date(currentSession.startTime).toLocaleString('zh-CN')}`);
  console.log('');

  // 记录到 token tracker
  try {
    tokenTracker.record({
      model: currentSession.model,
      tokens: 0,
      sessionKey: currentSession.sessionKey
    });

    console.log('✅ 会话已记录到 token tracker');
    console.log('');
  } catch (error) {
    console.error('❌ 记录会话失败:', error);
    console.log('');
  }
}

// 记录结束
export function recordSessionEnd() {
  // 计算会话持续时间（毫秒）
  const duration = Date.now() - currentSession.startTime;

  // 估算 token 消耗（假设平均 0.5 token/ms）
  // 这个值可能需要根据实际情况调整
  const estimatedTokens = Math.round(duration * 0.5);

  console.log(`\n📝 记录会话结束...`);
  console.log(`持续时间: ${Math.round(duration / 1000)} 秒`);
  console.log(`估算 token 消耗: ${estimatedTokens} tokens`);
  console.log('');

  // 记录到 token tracker
  try {
    tokenTracker.record({
      model: currentSession.model,
      tokens: estimatedTokens,
      sessionKey: currentSession.sessionKey
    });

    console.log('✅ 会话已记录到 token tracker');
    console.log('');
  } catch (error) {
    console.error('❌ 记录会话失败:', error);
    console.log('');
  }

  // 重置会话信息
  currentSession = {
    startTime: Date.now(),
    model: process.env.OPENCLAW_MODEL || 'unknown',
    sessionKey: process.env.SESSION_KEY || undefined
  };
}

// 获取当前会话信息
export function getCurrentSession() {
  return {
    ...currentSession,
    duration: Date.now() - currentSession.startTime
  };
}

// 获取今日统计
export function getTodayStats() {
  return tokenTracker.getTodayStats();
}

// 获取本周统计
export function getWeekStats() {
  return tokenTracker.getWeekStats();
}

// 获取累计统计
export function getTotalStats() {
  return tokenTracker.getTotalStats();
}

// 获取节省建议
export function getSavingSuggestions() {
  return tokenTracker.getSavingSuggestions();
}
