/**
 * escalation-handler.js - 人工介入升级处理器
 * 
 * 当自动恢复策略无法处理异常时，触发人工介入流程
 * 通过 Discord 发送介入通知，并记录升级请求状态
 */

const fs = require('fs');
const path = require('path');
const { randomUUID: uuidv4 } = require('crypto');

const LOGS_DIR = path.join(__dirname, '../logs');
const CONFIG_DIR = path.join(__dirname, '../config');
const ESCALATIONS_FILE = path.join(LOGS_DIR, 'escalations.json');
const APPROVAL_RULES_FILE = path.join(CONFIG_DIR, 'approval-rules.json');

// 确保日志目录存在
if (!fs.existsSync(LOGS_DIR)) {
  fs.mkdirSync(LOGS_DIR, { recursive: true });
}

/**
 * 升级记录数据结构
 */
let escalations = {
  records: [],
  stats: {
    total: 0,
    pending: 0,
    acknowledged: 0,
    resolved: 0
  }
};

// 加载现有记录
function loadEscalations() {
  try {
    if (fs.existsSync(ESCALATIONS_FILE)) {
      const data = fs.readFileSync(ESCALATIONS_FILE, 'utf8');
      escalations = JSON.parse(data);
    }
  } catch (e) {
    console.warn('[EscalationHandler] Failed to load escalations:', e.message);
  }
}

// 保存记录
function saveEscalations() {
  try {
    // 更新统计
    escalations.stats.pending = escalations.records.filter(r => r.status === 'pending').length;
    escalations.stats.acknowledged = escalations.records.filter(r => r.status === 'acknowledged').length;
    escalations.stats.resolved = escalations.records.filter(r => r.status === 'resolved').length;
    escalations.stats.total = escalations.records.length;
    
    fs.writeFileSync(ESCALATIONS_FILE, JSON.stringify(escalations, null, 2));
  } catch (e) {
    console.warn('[EscalationHandler] Failed to save escalations:', e.message);
  }
}

loadEscalations();

/**
 * 获取 Discord 配置
 */
function getDiscordConfig() {
  try {
    const config = JSON.parse(fs.readFileSync(APPROVAL_RULES_FILE, 'utf8'));
    return config.notification_channels?.discord || null;
  } catch (e) {
    console.warn('[EscalationHandler] Failed to load Discord config:', e.message);
    return null;
  }
}

/**
 * 发起人工介入请求
 * @param {Object} exception - 异常对象
 * @param {Object} context - 上下文信息
 * @param {string} context.impact - 影响范围描述
 * @param {string[]} context.attemptedSteps - 已尝试的恢复步骤
 * @param {string} context.suggestedAction - 建议操作
 * @param {'low'|'medium'|'high'|'critical'} context.urgency - 紧急程度
 * @returns {Promise<Object>} 升级记录
 */
async function escalate(exception, context = {}) {
  const escalationId = uuidv4();
  const now = new Date().toISOString();
  
  const escalationRecord = {
    id: escalationId,
    exceptionId: exception.id || uuidv4(),
    severity: exception.severity || 'high',
    type: exception.type || 'unknown',
    message: exception.message || 'Unknown exception',
    context: {
      impact: context.impact || '未指定',
      attemptedSteps: context.attemptedSteps || [],
      suggestedAction: context.suggestedAction || '请管理员审查并决定后续操作',
      urgency: context.urgency || 'medium'
    },
    status: 'pending',
    escalatedAt: now,
    acknowledgedAt: null,
    acknowledgedBy: null,
    resolvedAt: null,
    resolution: null
  };

  // 保存记录
  escalations.records.push(escalationRecord);
  saveEscalations();

  // 发送 Discord 通知
  try {
    await sendDiscordEscalation(escalationRecord);
  } catch (e) {
    console.error('[EscalationHandler] Failed to send Discord notification:', e.message);
    // 不抛出错误，升级记录已保存
  }

  console.log(`[EscalationHandler] Escalation created: ${escalationId} (severity: ${escalationRecord.severity})`);
  
  return escalationRecord;
}

/**
 * 发送 Discord 升级通知
 * @param {Object} escalation - 升级记录
 */
async function sendDiscordEscalation(escalation) {
  const discordConfig = getDiscordConfig();
  if (!discordConfig?.enabled) {
    console.warn('[EscalationHandler] Discord notifications disabled');
    return;
  }

  const channelId = discordConfig.channels?.['admin-alerts'] || discordConfig.channels?.['alerts'];
  if (!channelId) {
    console.warn('[EscalationHandler] No admin-alerts channel configured');
    return;
  }

  // 根据紧急程度设置颜色
  const urgencyColors = {
    low: 3447003,      // 蓝色
    medium: 15105570,  // 橙色
    high: 15158332,    // 红色
    critical: 10038562 // 深红色
  };

  const urgencyEmojis = {
    low: '🟢',
    medium: '🟡',
    high: '🟠',
    critical: '🔴'
  };

  const embed = {
    title: `${urgencyEmojis[escalation.context.urgency] || '🔴'} 人工介入请求`,
    color: urgencyColors[escalation.context.urgency] || urgencyColors.high,
    fields: [
      {
        name: '📋 升级 ID',
        value: `\`${escalation.id}\``,
        inline: true
      },
      {
        name: '⚠️ 异常类型',
        value: escalation.type,
        inline: true
      },
      {
        name: '🔥 严重性',
        value: escalation.severity.toUpperCase(),
        inline: true
      },
      {
        name: '📝 问题描述',
        value: escalation.message,
        inline: false
      },
      {
        name: '💥 影响范围',
        value: escalation.context.impact,
        inline: false
      },
      {
        name: '🔄 已尝试步骤',
        value: escalation.context.attemptedSteps.length > 0 
          ? escalation.context.attemptedSteps.map((s, i) => `${i + 1}. ${s}`).join('\n')
          : '无',
        inline: false
      },
      {
        name: '💡 建议操作',
        value: escalation.context.suggestedAction,
        inline: false
      },
      {
        name: '⏰ 升级时间',
        value: new Date(escalation.escalatedAt).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' }),
        inline: true
      },
      {
        name: '🎯 紧急程度',
        value: escalation.context.urgency.toUpperCase(),
        inline: true
      }
    ],
    footer: {
      text: '请使用 /acknowledge 或 /resolve 命令处理此升级请求'
    }
  };

  const payload = {
    content: `🚨 **人工介入请求** - 需要管理员处理`,
    embeds: [embed]
  };

  // 如果有 webhook URL，发送通知
  if (discordConfig.webhook_url_env) {
    const webhookUrl = process.env[discordConfig.webhook_url_env];
    if (webhookUrl) {
      const response = await fetch(webhookUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      if (!response.ok) {
        throw new Error(`Discord API returned ${response.status}`);
      }
    }
  }
}

/**
 * 确认已收到介入请求
 * @param {string} escalationId - 升级 ID
 * @param {string} acknowledgedBy - 确认人
 * @returns {Object|null} 更新后的记录
 */
function acknowledge(escalationId, acknowledgedBy) {
  const record = escalations.records.find(r => r.id === escalationId);
  if (!record) {
    console.warn(`[EscalationHandler] Escalation not found: ${escalationId}`);
    return null;
  }

  if (record.status !== 'pending') {
    console.warn(`[EscalationHandler] Escalation ${escalationId} is not pending (current: ${record.status})`);
    return null;
  }

  record.status = 'acknowledged';
  record.acknowledgedAt = new Date().toISOString();
  record.acknowledgedBy = acknowledgedBy;
  
  saveEscalations();
  console.log(`[EscalationHandler] Escalation ${escalationId} acknowledged by ${acknowledgedBy}`);
  
  return record;
}

/**
 * 标记介入请求已解决
 * @param {string} escalationId - 升级 ID
 * @param {Object} resolution - 解决方案
 * @param {string} resolution.summary - 解决摘要
 * @param {string} resolution.actions - 已执行的操作
 * @param {string} resolution.resolvedBy - 解决人
 * @returns {Object|null} 更新后的记录
 */
function resolve(escalationId, resolution) {
  const record = escalations.records.find(r => r.id === escalationId);
  if (!record) {
    console.warn(`[EscalationHandler] Escalation not found: ${escalationId}`);
    return null;
  }

  record.status = 'resolved';
  record.resolvedAt = new Date().toISOString();
  record.resolution = {
    summary: resolution.summary || '已解决',
    actions: resolution.actions || '未指定',
    resolvedBy: resolution.resolvedBy || 'unknown',
    resolvedAt: record.resolvedAt
  };
  
  saveEscalations();
  console.log(`[EscalationHandler] Escalation ${escalationId} resolved by ${resolution.resolvedBy || 'unknown'}`);
  
  return record;
}

/**
 * 列出升级请求
 * @param {Object} filter - 过滤条件
 * @param {'pending'|'acknowledged'|'resolved'|'all'} filter.status - 状态过滤
 * @param {string} filter.severity - 严重性过滤
 * @param {number} filter.limit - 返回数量限制
 * @returns {Array} 升级记录列表
 */
function listEscalations(filter = {}) {
  let records = [...escalations.records];

  // 状态过滤
  if (filter.status && filter.status !== 'all') {
    records = records.filter(r => r.status === filter.status);
  }

  // 严重性过滤
  if (filter.severity) {
    records = records.filter(r => r.severity === filter.severity);
  }

  // 按时间倒序
  records.sort((a, b) => new Date(b.escalatedAt) - new Date(a.escalatedAt));

  // 数量限制
  if (filter.limit) {
    records = records.slice(0, filter.limit);
  }

  return records;
}

/**
 * 获取升级统计
 * @returns {Object} 统计信息
 */
function getEscalationStats() {
  return {
    ...escalations.stats,
    pendingIds: escalations.records.filter(r => r.status === 'pending').map(r => r.id),
    avgResolutionTime: calculateAvgResolutionTime()
  };
}

/**
 * 计算平均解决时间 (毫秒)
 */
function calculateAvgResolutionTime() {
  const resolved = escalations.records.filter(r => r.status === 'resolved' && r.resolvedAt);
  if (resolved.length === 0) return 0;

  const totalMs = resolved.reduce((sum, r) => {
    const escalated = new Date(r.escalatedAt).getTime();
    const resolved = new Date(r.resolvedAt).getTime();
    return sum + (resolved - escalated);
  }, 0);

  return totalMs / resolved.length;
}

module.exports = {
  escalate,
  acknowledge,
  resolve,
  listEscalations,
  getEscalationStats,
  loadEscalations,
  saveEscalations
};
