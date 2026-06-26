/**
 * Alert Manager - 告警管理器
 * 
 * 负责发送告警到 Discord 和本地日志，支持告警节流、历史记录查询等功能
 */

const https = require('https');
const http = require('http');
const { logException, getExceptions, getStats } = require('./exception-logger');

// Discord 配置
const DISCORD_BOT_TOKEN = process.env.DISCORD_BOT_TOKEN || 'your-discord-bot-token-here';
const DISCORD_CHANNELS = {
  'approval-requests': '1234567890123456789',
  'order-alerts': '1234567890123456790',
  'customer-service': '1234567890123456791',
  'admin-alerts': '1234567890123456792',
  'alerts': '1234567890123456792' // 默认告警频道
};

// 告警节流配置（毫秒）
const ALERT_THROTTLE = {
  'approval_timeout': 5 * 60 * 1000,      // 5 分钟
  'system_error': 1 * 60 * 1000,          // 1 分钟
  'order_amount_anomaly': 10 * 60 * 1000, // 10 分钟
  'duplicate_order_suspect': 15 * 60 * 1000,
  'order_status_anomaly': 10 * 60 * 1000,
  'order_overdue': 30 * 60 * 1000,        // 30 分钟
  'order_quantity_anomaly': 10 * 60 * 1000,
  'rule_evaluation_error': 5 * 60 * 1000,
  'default': 5 * 60 * 1000                // 默认 5 分钟
};

// 严重级别颜色
const SEVERITY_COLORS = {
  'critical': 15158332,  // 红色
  'warning': 15105570,   // 黄色/橙色
  'info': 3447003        // 蓝色
};

// 告警历史记录（内存缓存）
const alertHistory = [];
const lastAlertTime = {}; // 用于节流：{ type: timestamp }

/**
 * 获取告警节流冷却时间
 */
function getThrottleMs(type) {
  return ALERT_THROTTLE[type] || ALERT_THROTTLE.default;
}

/**
 * 检查是否可以发送告警（节流检查）
 */
function canSendAlert(type) {
  const now = Date.now();
  const lastTime = lastAlertTime[type] || 0;
  const throttleMs = getThrottleMs(type);
  return (now - lastTime) >= throttleMs;
}

/**
 * 更新告警时间记录
 */
function updateAlertTime(type) {
  lastAlertTime[type] = Date.now();
}

/**
 * 发送 Discord webhook 通知
 */
function sendDiscordWebhook(channelId, payload) {
  return new Promise((resolve, reject) => {
    const url = `https://discord.com/api/v10/channels/${channelId}/messages`;
    
    const data = JSON.stringify(payload);
    
    const options = {
      hostname: 'discord.com',
      port: 443,
      path: `/api/v10/channels/${channelId}/messages`,
      method: 'POST',
      headers: {
        'Authorization': `Bot ${DISCORD_BOT_TOKEN}`,
        'Content-Type': 'application/json',
        'Content-Length': data.length
      }
    };
    
    const req = https.request(options, (res) => {
      let responseData = '';
      res.on('data', chunk => responseData += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve({ success: true, statusCode: res.statusCode, data: responseData });
        } else {
          reject(new Error(`Discord API error: ${res.statusCode} - ${responseData}`));
        }
      });
    });
    
    req.on('error', (error) => {
      reject(error);
    });
    
    req.write(data);
    req.end();
  });
}

/**
 * 构建 Discord embed 消息
 */
function buildDiscordEmbed(exception) {
  const color = SEVERITY_COLORS[exception.severity] || SEVERITY_COLORS.info;
  
  const fields = [
    {
      name: '类型',
      value: exception.type,
      inline: true
    },
    {
      name: '严重级别',
      value: exception.severity.toUpperCase(),
      inline: true
    },
    {
      name: '时间',
      value: new Date(exception.timestamp).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' }),
      inline: true
    }
  ];
  
  // 添加上下文字段
  if (exception.context) {
    const contextEntries = Object.entries(exception.context).slice(0, 5);
    contextEntries.forEach(([key, value]) => {
      const displayValue = typeof value === 'object' ? JSON.stringify(value) : String(value);
      if (displayValue.length < 1024) {
        fields.push({
          name: key.replace(/_/g, ' '),
          value: displayValue,
          inline: displayValue.length < 50
        });
      }
    });
  }
  
  // 添加建议操作
  const suggestedActions = getSuggestedActions(exception);
  if (suggestedActions) {
    fields.push({
      name: '建议操作',
      value: suggestedActions,
      inline: false
    });
  }
  
  return {
    embeds: [{
      title: getAlertTitle(exception),
      color: color,
      description: exception.message,
      fields: fields,
      footer: {
        text: `Exception ID: ${exception.id || 'N/A'}`
      },
      timestamp: exception.timestamp || new Date().toISOString()
    }]
  };
}

/**
 * 获取告警标题
 */
function getAlertTitle(exception) {
  const icons = {
    'critical': '🔴',
    'warning': '⚠️',
    'info': 'ℹ️'
  };
  
  const typeLabels = {
    'approval_timeout': '审批超时',
    'system_error': '系统错误',
    'order_amount_anomaly': '订单金额异常',
    'duplicate_order_suspect': '重复订单嫌疑',
    'order_status_anomaly': '订单状态异常',
    'order_overdue': '订单逾期',
    'order_quantity_anomaly': '订单数量异常',
    'rule_evaluation_error': '规则评估错误'
  };
  
  const icon = icons[exception.severity] || 'ℹ️';
  const label = typeLabels[exception.type] || exception.type;
  return `${icon} ${label}`;
}

/**
 * 获取建议操作
 */
function getSuggestedActions(exception) {
  const actions = {
    'approval_timeout': '• 检查审批人是否在线\n• 手动升级审批\n• 联系审批人',
    'system_error': '• 检查系统日志\n• 重启相关服务\n• 联系技术支持',
    'order_amount_anomaly': '• 核实订单金额\n• 联系客户确认\n• 检查是否有欺诈风险',
    'order_overdue': '• 联系生产部门\n• 通知客户延期\n• 安排加急处理',
    'order_status_anomaly': '• 检查状态流转逻辑\n• 手动修正状态\n• 审查相关代码',
    'duplicate_order_suspect': '• 联系客户确认需求\n• 检查是否为重复下单\n• 核实库存情况'
  };
  
  return actions[exception.type] || '• 检查异常详情\n• 根据上下文处理\n• 记录解决方案';
}

/**
 * 发送告警（Discord + 本地日志）
 * @param {Object} exception - 异常对象
 * @param {Object} options - 发送选项
 * @returns {Object} 发送结果
 */
async function sendAlert(exception, options = {}) {
  const result = {
    success: false,
    discord_sent: false,
    logged: false,
    throttled: false,
    error: null
  };
  
  // 节流检查
  if (options.skip_throttle !== true && !canSendAlert(exception.type)) {
    result.throttled = true;
    console.log(`[AlertManager] Alert throttled: ${exception.type}`);
    return result;
  }
  
  // 记录到本地日志
  const exceptionId = logException({
    ...exception,
    alert_sent: true,
    alert_channels: ['discord', 'local_log']
  });
  result.logged = true;
  
  // 发送 Discord 告警
  if (options.skip_discord !== true) {
    try {
      const channelId = options.channel_id || DISCORD_CHANNELS.alerts;
      const payload = buildDiscordEmbed(exception);
      
      await sendDiscordWebhook(channelId, payload);
      result.discord_sent = true;
      result.success = true;
      
      // 更新节流时间
      updateAlertTime(exception.type);
      
      // 记录到内存历史
      alertHistory.push({
        exception_id: exceptionId,
        type: exception.type,
        severity: exception.severity,
        sent_at: new Date().toISOString(),
        channel: channelId,
        discord_sent: true
      });
      
      console.log(`[AlertManager] Alert sent: ${exception.type} (${exception.severity})`);
    } catch (error) {
      result.error = error.message;
      console.error('[AlertManager] Failed to send Discord alert:', error.message);
      
      // Discord 失败时尝试降级到邮件（TODO: 实现邮件发送）
      // 这里先记录错误
      logException({
        type: 'alert_send_failure',
        severity: 'warning',
        message: `Discord 告警发送失败：${error.message}`,
        context: {
          original_exception: exception.type,
          error: error.message
        }
      });
    }
  } else {
    result.success = true; // 只记录日志也算成功
  }
  
  return result;
}

/**
 * 发送 Discord webhook 通知（直接调用）
 * @param {Object} exception - 异常对象
 * @param {string} channelId - 频道 ID
 * @returns {Object} 发送结果
 */
async function sendDiscordAlert(exception, channelId = null) {
  return sendAlert(exception, {
    channel_id: channelId,
    skip_throttle: true
  });
}

/**
 * 告警节流（同类型告警冷却时间内不重复发送）
 * @param {string} type - 异常类型
 * @param {number} cooldownMs - 冷却时间（毫秒）
 * @returns {boolean} 是否可以发送
 */
function throttleAlert(type, cooldownMs = null) {
  if (cooldownMs !== null) {
    // 自定义冷却时间
    ALERT_THROTTLE[type] = cooldownMs;
  }
  return canSendAlert(type);
}

/**
 * 查询告警历史
 * @param {string} type - 异常类型（可选）
 * @param {number} limit - 限制数量
 * @returns {Array} 告警历史记录
 */
function getAlertHistory(type = null, limit = 50) {
  let history = alertHistory;
  
  if (type) {
    history = history.filter(h => h.type === type);
  }
  
  return history.slice(-limit);
}

/**
 * 获取告警统计
 * @returns {Object} 统计信息
 */
function getAlertStats() {
  const now = Date.now();
  const last24h = now - (24 * 60 * 60 * 1000);
  const last1h = now - (60 * 60 * 1000);
  
  const recentAlerts = alertHistory.filter(a => new Date(a.sent_at).getTime() >= last24h);
  
  const stats = {
    total_sent: alertHistory.length,
    last_24h: recentAlerts.length,
    last_1h: alertHistory.filter(a => new Date(a.sent_at).getTime() >= last1h).length,
    by_severity: {
      critical: recentAlerts.filter(a => a.severity === 'critical').length,
      warning: recentAlerts.filter(a => a.severity === 'warning').length,
      info: recentAlerts.filter(a => a.severity === 'info').length
    },
    by_type: {},
    discord_sent: recentAlerts.filter(a => a.discord_sent).length,
    throttled_count: Object.keys(lastAlertTime).length
  };
  
  // 按类型统计
  recentAlerts.forEach(alert => {
    if (!stats.by_type[alert.type]) {
      stats.by_type[alert.type] = 0;
    }
    stats.by_type[alert.type]++;
  });
  
  return stats;
}

/**
 * 批量发送告警
 * @param {Array} exceptions - 异常对象列表
 * @returns {Object} 批量发送结果
 */
async function sendBulkAlerts(exceptions) {
  const results = {
    total: exceptions.length,
    sent: 0,
    throttled: 0,
    failed: 0,
    details: []
  };
  
  for (const exception of exceptions) {
    const result = await sendAlert(exception);
    results.details.push({
      type: exception.type,
      ...result
    });
    
    if (result.success) results.sent++;
    else if (result.throttled) results.throttled++;
    else results.failed++;
  }
  
  return results;
}

module.exports = {
  sendAlert,
  sendDiscordAlert,
  throttleAlert,
  getAlertHistory,
  getAlertStats,
  sendBulkAlerts,
  canSendAlert,
  updateAlertTime,
  DISCORD_CHANNELS,
  SEVERITY_COLORS
};
