/**
 * Notification Router
 * 
 * Routes notifications to the appropriate Discord channel based on
 * notification type, priority, and configuration.
 */

const path = require('path');
const fs = require('fs');
const {
  sendMessage,
  sendEmbed,
  sendApprovalRequest,
  sendAlert,
  sendRecoveryNotification,
  sendEscalationRequest
} = require('./discord-notifier');

/**
 * Load approval rules config
 */
function loadConfig() {
  const configPath = path.join(__dirname, '../config/approval-rules.json');
  const configData = fs.readFileSync(configPath, 'utf8');
  return JSON.parse(configData);
}

/**
 * Get channel ID for notification type and priority
 * @param {String} notificationType - Type of notification
 * @param {String} priority - Priority level (critical/high/normal/low)
 * @returns {String} Discord channel ID
 */
function getChannel(notificationType, priority = 'normal') {
  const config = loadConfig();
  const channels = config.notification_channels?.discord?.channels || {};
  
  // Route based on notification type
  switch (notificationType) {
    case 'approval_request':
      return channels['approval-requests'] || channels['admin-alerts'];
    
    case 'alert':
      // Critical alerts go to admin, others to alerts channel
      if (priority === 'critical' || priority === 'high') {
        return channels['admin-alerts'] || channels['alerts'];
      }
      return channels['order-alerts'] || channels['alerts'];
    
    case 'escalation':
      // All escalations go to admin
      return channels['admin-alerts'];
    
    case 'recovery_status':
      // Recovery notifications go to admin
      return channels['admin-alerts'];
    
    case 'exception':
      // Exceptions based on severity
      if (priority === 'critical') {
        return channels['admin-alerts'];
      }
      return channels['order-alerts'] || channels['alerts'];
    
    default:
      // Default to admin alerts
      return channels['admin-alerts'];
  }
}

/**
 * Route notification to appropriate channel
 * @param {Object} notification - Notification object
 * @returns {Promise<Object>} Send result
 */
async function route(notification) {
  const type = notification.type;
  const priority = notification.priority || notification.severity || 'normal';
  const channelId = getChannel(type, priority);
  
  console.log(`[notification-router] Routing ${type} notification (priority: ${priority}) to channel ${channelId}`);
  
  try {
    switch (type) {
      case 'approval_request':
        return await sendApprovalRequest(notification.data);
      
      case 'alert':
        return await sendAlert(notification.data);
      
      case 'escalation':
        return await sendEscalationRequest(notification.data);
      
      case 'recovery_status':
        return await sendRecoveryNotification(notification.data);
      
      case 'message':
        // Plain text message
        return await sendMessage(channelId, notification.content);
      
      case 'embed':
        // Raw embed
        return await sendEmbed(channelId, notification.embed, notification.components);
      
      default:
        console.warn(`[notification-router] Unknown notification type: ${type}, sending as message`);
        return await sendMessage(channelId, JSON.stringify(notification));
    }
  } catch (error) {
    console.error(`[notification-router] Failed to route notification: ${error.message}`);
    return { success: false, error: error.message };
  }
}

/**
 * Batch route multiple notifications
 * @param {Array} notifications - Array of notification objects
 * @returns {Promise<Array>} Array of send results
 */
async function routeBatch(notifications) {
  const results = [];
  
  for (const notification of notifications) {
    const result = await route(notification);
    results.push(result);
    
    // Small delay between notifications to avoid rate limiting
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  return results;
}

/**
 * Get routing rules summary
 * @returns {Object} Routing configuration summary
 */
function getRoutingRules() {
  const config = loadConfig();
  const channels = config.notification_channels?.discord?.channels || {};
  
  return {
    notification_types: ['approval_request', 'alert', 'escalation', 'recovery_status', 'exception', 'message', 'embed'],
    priority_levels: ['critical', 'high', 'normal', 'low'],
    channels: {
      'approval-requests': channels['approval-requests'] || 'Not configured',
      'order-alerts': channels['order-alerts'] || 'Not configured',
      'customer-service': channels['customer-service'] || 'Not configured',
      'admin-alerts': channels['admin-alerts'] || 'Not configured'
    },
    routing_logic: {
      approval_request: '→ approval-requests channel',
      'alert (critical/high)': '→ admin-alerts channel',
      'alert (normal/low)': '→ order-alerts channel',
      escalation: '→ admin-alerts channel',
      recovery_status: '→ admin-alerts channel',
      'exception (critical)': '→ admin-alerts channel',
      'exception (normal)': '→ order-alerts channel'
    }
  };
}

module.exports = {
  route,
  routeBatch,
  getChannel,
  getRoutingRules
};
