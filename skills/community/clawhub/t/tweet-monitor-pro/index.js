#!/usr/bin/env node
/**
 * Tweet Monitor Pro - OpenClaw Skill
 * 商业化版 X 推文抓取工具
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 配额数据库文件路径
const QUOTA_DB = process.env.QUOTA_DB || path.join(__dirname, 'quotas.json');

// 默认配额配置
const PLANS = {
  free: { limit: 10, features: ['fetchTweet'] },
  pro: { limit: 1000, features: ['fetchTweet', 'fetchThread', 'fetchTimeline', 'monitorUser'] },
  business: { limit: -1, features: ['fetchTweet', 'fetchThread', 'fetchTimeline', 'monitorUser', 'getQuota'] }
};

// 加载配额数据库
function loadQuotas() {
  try {
    if (fs.existsSync(QUOTA_DB)) {
      const data = fs.readFileSync(QUOTA_DB, 'utf-8');
      return JSON.parse(data);
    }
  } catch (error) {
    console.error('配额数据库损坏，创建新的');
  }
  return {}; // userId -> { plan, used }
}

// 保存配额数据库
function saveQuotas(quotas) {
  try {
    fs.writeFileSync(QUOTA_DB, JSON.stringify(quotas, null, 2));
  } catch (error) {
    console.error('保存配额失败:', error.message);
  }
}

// 初始化配额数据库（第一次运行）
function initQuotaIfNeeded(userId, plan = 'free') {
  const quotas = loadQuotas();
  if (!quotas[userId]) {
    quotas[userId] = {
      plan,
      used: 0,
      limit: PLANS[plan].limit,
      createdAt: new Date().toISOString()
    };
    saveQuotas(quotas);
  }
  return quotas;
}

// 获取用户计划
function getUserPlan(userId) {
  const quotas = loadQuotas();
  const user = quotas[userId] || { plan: 'free', used: 0, limit: PLANS.free.limit };
  return user;
}

// 检查并扣减配额
function consumeQuota(userId, feature) {
  const quotas = loadQuotas();
  let user = quotas[userId];
  
  if (!user) {
    user = { plan: 'free', used: 0, limit: PLANS.free.limit };
    quotas[userId] = user;
  }
  
  // 检查功能是否允许
  const allowedFeatures = PLANS[user.plan].features;
  if (!allowedFeatures.includes(feature)) {
    throw new Error(`功能 "${feature}" 需要 ${user.plan === 'free' ? 'Pro 或 Business' : user.plan.toUpperCase()} 计划。`);
  }
  
  // 检查次数限制
  if (user.limit !== -1 && user.used >= user.limit) {
    throw new Error(`配额用尽！当前计划：${user.plan}（${user.limit}次/月）。请升级。`);
  }
  
  // 扣减
  user.used++;
  quotas[userId] = user;
  saveQuotas(quotas);
  
  return {
    plan: user.plan,
    used: user.used,
    limit: user.limit === -1 ? '无限' : user.limit,
    remaining: user.limit === -1 ? '无限' : (user.limit - user.used)
  };
}

// 主工具：抓取推文（基础功能，只依赖 FxTwitter）
function fetchTweet(url, options = {}) {
  const scriptPath = '/root/.openclaw/workspace/skills/x-tweet-fetcher/scripts/fetch_tweet.py';
  const args = ['python3', scriptPath, '--url', url];
  
  if (options.replies) args.push('--replies');
  if (options.textOnly) args.push('--text-only');
  if (options.pretty) args.push('--pretty');
  
  try {
    const output = execSync(args.join(' '), { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] });
    return JSON.parse(output);
  } catch (error) {
    throw new Error(`抓取失败: ${error.message}`);
  }
}

// 工具：抓取用户时间线（需要 Camofox）
function fetchTimeline(username, limit = 50) {
  // 先检查是否支持
  const quotas = loadQuotas();
  // 这里简化，不按用户检查
  
  const scriptPath = '/root/.openclaw/workspace/skills/x-tweet-fetcher/scripts/fetch_tweet.py';
  const args = ['python3', scriptPath, '--user', username, '--limit', String(limit)];
  
  try {
    const output = execSync(args.join(' '), { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] });
    return JSON.parse(output);
  } catch (error) {
    throw new Error(`抓取时间线失败: ${error.message}`);
  }
}

// 工具：监控用户（增量）
function monitorUser(username, baselineFile) {
  const scriptPath = '/root/.openclaw/workspace/skills/x-tweet-fetcher/scripts/fetch_tweet.py';
  const args = ['python3', scriptPath, '--monitor', username];
  
  if (baselineFile) {
    args.push('--baseline', baselineFile);
  }
  
  try {
    const output = execSync(args.join(' '), { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] });
    return JSON.parse(output);
  } catch (error) {
    throw new Error(`监控失败: ${error.message}`);
  }
}

// 升级用户计划
function upgradePlan(userId, newPlan) {
  if (!PLANS[newPlan]) {
    throw new Error(`无效的计划: ${newPlan}。可用: ${Object.keys(PLANS).join(', ')}`);
  }
  
  const quotas = loadQuotas();
  if (!quotas[userId]) {
    quotas[userId] = { plan: 'free', used: 0 };
  }
  
  quotas[userId].plan = newPlan;
  quotas[userId].limit = PLANS[newPlan].limit;
  saveQuotas(quotas);
  
  return getUserPlan(userId);
}

// 导出工具函数（OpenClaw 技能接口）
module.exports = {
  name: 'tweet-monitor-pro',
  version: '1.0.0',
  
  // 初始化用户（OpenClaw 会自动调用？）
  init: async (userId) => {
    const quotas = loadQuotas();
    if (!quotas[userId]) {
      quotas[userId] = { plan: 'free', used: 0, limit: PLANS.free.limit };
      saveQuotas(quotas);
    }
    return { success: true, message: '用户已初始化' };
  },
  
  // 抓取单条推文
  fetchTweet: {
    description: '抓取单条 X/Twitter 推文内容、统计和媒体',
    parameters: {
      url: { type: 'string', required: true, description: '推文 URL' },
      textOnly: { type: 'boolean', default: false, description: '仅返回文本' }
    },
    async execute(params, context) {
      const userId = context.userId || 'anonymous';
      try {
        const quota = consumeQuota(userId, 'fetchTweet');
        const result = fetchTweet(params.url, {
          textOnly: params.textOnly,
          replies: false
        });
        
        return {
          success: true,
          data: result,
          quota
        };
      } catch (error) {
        return {
          success: false,
          error: error.message,
          quota: getUserPlan(userId)
        };
      }
    }
  },
  
  // 查询配额
  getQuota: {
    description: '查询当前账户剩余调用次数',
    parameters: {},
    async execute(params, context) {
      const userId = context.userId || 'anonymous';
      const user = getUserPlan(userId);
      return {
        success: true,
        data: {
          plan: user.plan,
          used: user.used,
          limit: user.limit === -1 ? '无限' : user.limit,
          remaining: user.limit === -1 ? '无限' : Math.max(0, user.limit - user.used),
          plans: Object.keys(PLANS)
        }
      };
    }
  },
  
  // 管理：升级计划
  upgradePlan: {
    description: '升级用户订阅计划',
    parameters: {
      plan: { type: 'string', required: true, enum: ['pro', 'business'], description: '新计划' }
    },
    async execute(params, context) {
      const userId = context.userId || 'anonymous';
      try {
        const newPlan = upgradePlan(userId, params.plan);
        return {
          success: true,
          data: {
            message: `已升级到 ${newPlan.plan} 计划`,
            plan: newPlan.plan,
            limit: newPlan.limit,
            used: newPlan.used
          }
        };
      } catch (error) {
        return {
          success: false,
          error: error.message
        };
      }
    }
  },
  
  // 🔒 Pro/Business 功能（需要高级计划）
  
  fetchThread: {
    description: '抓取推文及其所有回复（包括嵌套）- 仅 Pro/Business',
    parameters: {
      url: { type: 'string', required: true, description: '推文 URL' }
    },
    async execute(params, context) {
      const userId = context.userId || 'anonymous';
      try {
        const quota = consumeQuota(userId, 'fetchThread');
        
        // 检查 Camofox 是否可用（可选）
        try {
          const result = fetchTweet(params.url, { replies: true, textOnly: false });
          return { success: true, data: result, quota };
        } catch (error) {
          if (error.message.includes('Camofox')) {
            return {
              success: false,
              error: '高级功能需要 Camofox 服务。请先启动 Camofox 或升级到支持的基础功能。'
            };
          }
          throw error;
        }
      } catch (error) {
        return {
          success: false,
          error: error.message,
          quota: getUserPlan(userId)
        };
      }
    }
  },
  
  fetchTimeline: {
    description: '抓取用户的最近推文 - 仅 Pro/Business',
    parameters: {
      username: { type: 'string', required: true, description: '用户名' },
      limit: { type: 'number', default: 50, description: '最大数量' }
    },
    async execute(params, context) {
      const userId = context.userId || 'anonymous';
      try {
        const quota = consumeQuota(userId, 'fetchTimeline');
        const result = fetchTimeline(params.username, params.limit);
        return { success: true, data: result, quota };
      } catch (error) {
        return {
          success: false,
          error: error.message,
          quota: getUserPlan(userId)
        };
      }
    }
  },
  
  monitorUser: {
    description: '监控用户新推文（增量）- 仅 Pro/Business',
    parameters: {
      username: { type: 'string', required: true, description: '用户名' },
      baselineFile: { type: 'string', description: '基线文件路径' }
    },
    async execute(params, context) {
      const userId = context.userId || 'anonymous';
      try {
        const quota = consumeQuota(userId, 'monitorUser');
        const result = monitorUser(params.username, params.baselineFile);
        return { success: true, data: result, quota };
      } catch (error) {
        return {
          success: false,
          error: error.message,
          quota: getUserPlan(userId)
        };
      }
    }
  }
};
