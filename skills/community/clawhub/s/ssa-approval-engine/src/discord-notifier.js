/**
 * Discord Notifier - Unified Discord Notification Sender
 * 
 * Provides a consistent interface for sending Discord notifications
 * across all approval-engine modules.
 * 
 * Bot Token: From approval-rules.json or environment
 */

const path = require('path');
const fs = require('fs');
const https = require('https');

// Load templates
const {
  getApprovalTemplate,
  getAlertTemplate,
  getEscalationTemplate,
  getRecoveryTemplate,
  COLORS
} = require('./notification-templates');

/**
 * Load approval rules config
 */
function loadConfig() {
  const configPath = path.join(__dirname, '../config/approval-rules.json');
  const configData = fs.readFileSync(configPath, 'utf8');
  return JSON.parse(configData);
}

/**
 * Get Discord channel ID from config
 */
function getChannelId(channelName) {
  const config = loadConfig();
  return config.notification_channels?.discord?.channels?.[channelName] || 
         config.notification_channels?.discord?.channels?.['admin-alerts'];
}

/**
 * Make HTTP request to Discord API
 */
function discordRequest(endpoint, data, token) {
  return new Promise((resolve, reject) => {
    const url = `https://discord.com/api/v10/${endpoint}`;
    const body = JSON.stringify(data);
    
    const options = {
      method: 'POST',
      hostname: 'discord.com',
      path: `/api/v10${endpoint}`,
      headers: {
        'Authorization': `Bot ${token}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body)
      }
    };
    
    const req = https.request(options, (res) => {
      let responseData = '';
      res.on('data', chunk => responseData += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(JSON.parse(responseData));
        } else {
          reject(new Error(`Discord API error: ${res.statusCode} - ${responseData}`));
        }
      });
    });
    
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

/**
 * Send message to Discord channel
 * @param {String} channelId - Discord channel ID
 * @param {String} message - Plain text message
 * @returns {Promise<Object>} Discord message object
 */
async function sendMessage(channelId, message) {
  const config = loadConfig();
  const token = process.env.DISCORD_BOT_TOKEN || config.notification_channels?.discord?.bot_token;
  
  if (!token) {
    console.warn('[discord-notifier] Discord bot token not configured, skipping message');
    return { skipped: true, reason: 'no_token' };
  }
  
  try {
    const result = await discordRequest(`/channels/${channelId}/messages`, {
      content: message
    }, token);
    
    console.log(`[discord-notifier] Message sent to channel ${channelId}`);
    return { success: true, message_id: result.id };
  } catch (error) {
    console.error(`[discord-notifier] Failed to send message: ${error.message}`);
    return { success: false, error: error.message };
  }
}

/**
 * Send embed message to Discord channel
 * @param {String} channelId - Discord channel ID
 * @param {Object} embed - Discord embed object
 * @param {Array} components - Optional components (buttons, etc)
 * @returns {Promise<Object>} Discord message object
 */
async function sendEmbed(channelId, embed, components = []) {
  const config = loadConfig();
  const token = process.env.DISCORD_BOT_TOKEN || config.notification_channels?.discord?.bot_token;
  
  if (!token) {
    console.warn('[discord-notifier] Discord bot token not configured, skipping embed');
    return { skipped: true, reason: 'no_token' };
  }
  
  try {
    const payload = { embeds: [embed] };
    if (components.length > 0) {
      payload.components = components;
    }
    
    const result = await discordRequest(`/channels/${channelId}/messages`, payload, token);
    
    console.log(`[discord-notifier] Embed sent to channel ${channelId}`);
    return { success: true, message_id: result.id };
  } catch (error) {
    console.error(`[discord-notifier] Failed to send embed: ${error.message}`);
    return { success: false, error: error.message };
  }
}

/**
 * Send approval request notification
 * @param {Object} approval - Approval object
 * @returns {Promise<Object>} Send result
 */
async function sendApprovalRequest(approval) {
  const config = loadConfig();
  const channelId = getChannelId('approval-requests');
  const { embed, components } = getApprovalTemplate(approval);
  
  console.log(`[discord-notifier] Sending approval request for ${approval.id}`);
  return sendEmbed(channelId, embed, components);
}

/**
 * Send alert notification
 * @param {Object} alert - Alert object
 * @returns {Promise<Object>} Send result
 */
async function sendAlert(alert) {
  const config = loadConfig();
  const severity = alert.severity || 'info';
  const channelId = getChannelId(severity === 'critical' ? 'admin-alerts' : 'order-alerts');
  const { embed } = getAlertTemplate(alert, severity);
  
  console.log(`[discord-notifier] Sending ${severity} alert: ${alert.title}`);
  return sendEmbed(channelId, embed);
}

/**
 * Send recovery status notification
 * @param {Object} recovery - Recovery object
 * @returns {Promise<Object>} Send result
 */
async function sendRecoveryNotification(recovery) {
  const config = loadConfig();
  const channelId = getChannelId('admin-alerts');
  const { embed } = getRecoveryTemplate(recovery);
  
  console.log(`[discord-notifier] Sending recovery notification for ${recovery.id}`);
  return sendEmbed(channelId, embed);
}

/**
 * Send escalation request notification
 * @param {Object} escalation - Escalation object
 * @returns {Promise<Object>} Send result
 */
async function sendEscalationRequest(escalation) {
  const config = loadConfig();
  const channelId = getChannelId('admin-alerts');
  const { embed, components } = getEscalationTemplate(escalation);
  
  console.log(`[discord-notifier] Sending escalation request for ${escalation.id}`);
  return sendEmbed(channelId, embed, components);
}

/**
 * Send notification with retry logic
 * @param {Function} sendFn - Send function to retry
 * @param {Object} options - Retry options
 * @returns {Promise<Object>} Send result
 */
async function sendWithRetry(sendFn, options = {}) {
  const maxRetries = options.maxRetries || 3;
  const delayMs = options.delayMs || 5000;
  
  let lastError;
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const result = await sendFn();
      if (result.success || result.skipped) {
        return result;
      }
      lastError = result.error;
    } catch (error) {
      lastError = error.message;
    }
    
    if (attempt < maxRetries) {
      console.log(`[discord-notifier] Retry ${attempt}/${maxRetries} after ${delayMs}ms`);
      await new Promise(resolve => setTimeout(resolve, delayMs));
    }
  }
  
  return { success: false, error: `Failed after ${maxRetries} attempts: ${lastError}` };
}

module.exports = {
  sendMessage,
  sendEmbed,
  sendApprovalRequest,
  sendAlert,
  sendRecoveryNotification,
  sendEscalationRequest,
  sendWithRetry,
  getChannelId
};
