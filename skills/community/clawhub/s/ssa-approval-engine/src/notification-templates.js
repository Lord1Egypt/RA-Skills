/**
 * Notification Templates Library
 * 
 * Generates Discord embed templates for various notification types.
 * Color coding: critical=#FF0000(red) / warning=#FFA500(orange) / info=#0099FF(blue) / success=#00FF00(green)
 */

const path = require('path');
const fs = require('fs');

// Color constants
const COLORS = {
  critical: 0xFF0000,    // Red
  warning: 0xFFA500,     // Orange
  info: 0x0099FF,        // Blue
  success: 0x00FF00,     // Green
  default: 0x3447003     // Default blue
};

/**
 * Load approval rules config
 */
function loadConfig() {
  const configPath = path.join(__dirname, '../config/approval-rules.json');
  const configData = fs.readFileSync(configPath, 'utf8');
  return JSON.parse(configData);
}

/**
 * Generate approval request embed
 * @param {Object} approval - Approval object
 * @returns {Object} Discord embed object
 */
function getApprovalTemplate(approval) {
  const config = loadConfig();
  const rule = config.rules.find(r => r.id === approval.rule_id);
  
  if (!rule) {
    console.warn(`[notification-templates] Rule not found: ${approval.rule_id}`);
    return getDefaultApprovalTemplate(approval);
  }
  
  const template = config.templates.discord[rule.templates.discord];
  if (!template) {
    return getDefaultApprovalTemplate(approval);
  }
  
  // Build embed with template variables replaced
  const embed = {
    title: replaceTemplateVars(template.embed.title, approval),
    color: template.embed.color || COLORS.default,
    fields: [],
    footer: {
      text: replaceTemplateVars(template.embed.footer?.text || 'Please review within {{timeout_hours}} hours', approval),
      timestamp: new Date().toISOString()
    }
  };
  
  // Process fields
  template.embed.fields.forEach(field => {
    embed.fields.push({
      name: field.name,
      value: replaceTemplateVars(field.value, approval),
      inline: field.inline !== false
    });
  });
  
  // Add components (buttons) if present
  const components = [];
  if (template.components?.buttons) {
    components.push({
      type: 1, // Action row
      components: template.components.buttons.map((btn, idx) => ({
        type: 2, // Button
        style: btn.style === 'success' ? 3 : btn.style === 'danger' ? 4 : 2,
        label: btn.label,
        custom_id: `${btn.action}_${approval.id}`
      }))
    });
  }
  
  return { embed, components };
}

/**
 * Default approval template fallback
 */
function getDefaultApprovalTemplate(approval) {
  return {
    embed: {
      title: '📋 Approval Request',
      color: COLORS.info,
      fields: [
        { name: 'Type', value: approval.type || 'Unknown', inline: true },
        { name: 'ID', value: approval.id, inline: true },
        { name: 'Status', value: approval.status, inline: true },
        { name: 'Requester', value: approval.requester || 'Unknown', inline: true },
        { name: 'Created', value: new Date(approval.created_at).toLocaleString(), inline: true }
      ],
      footer: {
        text: `Timeout: ${approval.timeout_hours || 24} hours`,
        timestamp: new Date().toISOString()
      }
    },
    components: [{
      type: 1,
      components: [
        { type: 2, style: 3, label: '✅ Approve', custom_id: `approve_${approval.id}` },
        { type: 2, style: 4, label: '❌ Reject', custom_id: `reject_${approval.id}` }
      ]
    }]
  };
}

/**
 * Generate alert embed based on severity
 * @param {Object} alert - Alert object
 * @param {String} severity - Severity level (critical/warning/info)
 * @returns {Object} Discord embed object
 */
function getAlertTemplate(alert, severity = 'info') {
  const colorMap = {
    critical: COLORS.critical,
    warning: COLORS.warning,
    info: COLORS.info
  };
  
  const emojiMap = {
    critical: '🔴',
    warning: '⚠️',
    info: 'ℹ️'
  };
  
  const emoji = emojiMap[severity] || emojiMap.info;
  const color = colorMap[severity] || COLORS.info;
  
  return {
    embed: {
      title: `${emoji} ${alert.title || 'System Alert'}`,
      color: color,
      fields: [],
      footer: {
        text: `Severity: ${severity.toUpperCase()} | Generated: ${new Date().toLocaleString()}`,
        timestamp: new Date().toISOString()
      }
    }
  };
}

/**
 * Generate escalation request embed
 * @param {Object} escalation - Escalation object
 * @returns {Object} Discord embed object
 */
function getEscalationTemplate(escalation) {
  const severityColor = escalation.severity === 'critical' ? COLORS.critical :
                        escalation.severity === 'high' ? COLORS.warning : COLORS.info;
  
  const severityEmoji = escalation.severity === 'critical' ? '🔴' :
                        escalation.severity === 'high' ? '⚠️' : '📋';
  
  return {
    embed: {
      title: `${severityEmoji} Human Intervention Required`,
      color: severityColor,
      fields: [
        { name: 'Escalation ID', value: escalation.id, inline: true },
        { name: 'Severity', value: escalation.severity?.toUpperCase() || 'NORMAL', inline: true },
        { name: 'Status', value: escalation.status || 'PENDING', inline: true },
        { name: 'Source', value: escalation.source || 'System', inline: true },
        { name: 'Assigned To', value: escalation.assigned_to || 'Unassigned', inline: true },
        { name: 'Created', value: new Date(escalation.created_at).toLocaleString(), inline: true },
        { name: 'Problem Description', value: escalation.description || 'No description provided', inline: false },
        { name: 'Suggested Actions', value: escalation.suggested_actions?.join('\n') || 'Use your best judgment', inline: false }
      ],
      footer: {
        text: 'Please acknowledge or resolve this escalation',
        timestamp: new Date().toISOString()
      }
    },
    components: [{
      type: 1,
      components: [
        { type: 2, style: 3, label: '✅ Acknowledge', custom_id: `ack_${escalation.id}` },
        { type: 2, style: 1, label: '📝 Resolve', custom_id: `resolve_${escalation.id}` }
      ]
    }]
  };
}

/**
 * Generate recovery status embed
 * @param {Object} recovery - Recovery object
 * @returns {Object} Discord embed object
 */
function getRecoveryTemplate(recovery) {
  const statusColor = recovery.status === 'success' ? COLORS.success :
                      recovery.status === 'failed' ? COLORS.critical :
                      recovery.status === 'in_progress' ? COLORS.warning : COLORS.info;
  
  const statusEmoji = recovery.status === 'success' ? '✅' :
                      recovery.status === 'failed' ? '❌' :
                      recovery.status === 'in_progress' ? '⏳' : '📋';
  
  return {
    embed: {
      title: `${statusEmoji} Recovery Status: ${recovery.id}`,
      color: statusColor,
      fields: [
        { name: 'Exception Type', value: recovery.exception_type || 'Unknown', inline: true },
        { name: 'Strategy', value: recovery.strategy || 'Unknown', inline: true },
        { name: 'Status', value: recovery.status?.toUpperCase() || 'UNKNOWN', inline: true },
        { name: 'Attempts', value: String(recovery.attempts || 0), inline: true },
        { name: 'Last Attempt', value: recovery.last_attempt_at ? new Date(recovery.last_attempt_at).toLocaleString() : 'N/A', inline: true },
        { name: 'Created', value: new Date(recovery.created_at).toLocaleString(), inline: true },
        { name: 'Description', value: recovery.description || 'No description', inline: false }
      ],
      footer: {
        text: `Auto-recovery ${recovery.status === 'success' ? 'succeeded' : recovery.status === 'failed' ? 'failed' : 'in progress'}`,
        timestamp: new Date().toISOString()
      }
    }
  };
}

/**
 * Replace template variables with actual values
 * @param {String} template - Template string with {{var}} placeholders
 * @param {Object} data - Data object containing values
 * @returns {String} Replaced string
 */
function replaceTemplateVars(template, data) {
  if (!template) return '';
  
  return template.replace(/\{\{([^}]+)\}\}/g, (match, key) => {
    const keys = key.split('.');
    let value = data;
    
    for (const k of keys) {
      if (value && typeof value === 'object') {
        value = value[k];
      } else {
        value = undefined;
        break;
      }
    }
    
    return value !== undefined ? String(value) : match;
  });
}

module.exports = {
  getApprovalTemplate,
  getAlertTemplate,
  getEscalationTemplate,
  getRecoveryTemplate,
  COLORS
};
