/**
 * customer-notify.js - 客户物流通知模块
 *
 * 功能：
 *  - sendShippedNotification(shipment, opts)     发送发货通知
 *  - sendDeliveredNotification(shipment, opts)    发送签收通知
 *  - sendEventNotification(shipment, event, opts) 发送中间节点通知（opt-in）
 *  - shouldNotify(shipment, eventType, opts)      判断是否应发送通知
 *  - buildEmailHtml(templateName, data)           构建 HTML 邮件内容
 *  - getNotificationHistory(trackingNumber)       获取通知历史
 *  - sendNotification(shipment, eventType, data, opts) 通用通知入口
 *
 * 特性：
 *  - eventId 幂等性检查（同一事件不重复通知）
 *  - 通知频率控制（每日上限 + 冷却时间）
 *  - HTML 邮件模板（含 17track.net 自助查询链接）
 *  - 与 imap-smtp-email SMTP 集成
 *  - dry-run 模式（不实际发送）
 *  - 通知历史持久化
 *
 * 配置文件：../config/logistics-config.json
 *
 * @module customer-notify
 */

'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFileSync } = require('child_process');

// ---------------------------------------------------------------------------
// Paths
// ---------------------------------------------------------------------------

const CONFIG_PATH = path.resolve(__dirname, '../config/logistics-config.json');
const NOTIFY_HISTORY_PATH = path.resolve(__dirname, '../data/notification-history.json');
const SMTP_SCRIPT = path.resolve(__dirname, '../../imap-smtp-email/scripts/smtp.js');

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

let _configCache = null;

/**
 * Load logistics config. Caches after first read.
 * @returns {object}
 */
function loadConfig() {
  if (_configCache) return _configCache;
  const raw = fs.readFileSync(CONFIG_PATH, 'utf8');
  _configCache = JSON.parse(raw);
  return _configCache;
}

/**
 * Force reload config (clear cache).
 * @returns {object}
 */
function reloadConfig() {
  _configCache = null;
  return loadConfig();
}

// ---------------------------------------------------------------------------
// Notification History (persistence + dedup)
// ---------------------------------------------------------------------------

/**
 * Load notification history from disk.
 * Structure: { [trackingNumber]: { events: [ { eventId, eventType, sentAt, recipient } ] } }
 * @returns {object}
 */
function _loadHistory() {
  try {
    const raw = fs.readFileSync(NOTIFY_HISTORY_PATH, 'utf8');
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

/**
 * Save notification history with atomic write.
 * @param {object} history
 */
function _saveHistory(history) {
  const dir = path.dirname(NOTIFY_HISTORY_PATH);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  const tmpPath = NOTIFY_HISTORY_PATH + '.tmp';
  fs.writeFileSync(tmpPath, JSON.stringify(history, null, 2), 'utf8');
  fs.renameSync(tmpPath, NOTIFY_HISTORY_PATH);
}

/**
 * Record a sent notification in history.
 * @param {string} trackingNumber
 * @param {object} record - { eventId, eventType, sentAt, recipient, subject }
 */
function _recordNotification(trackingNumber, record) {
  const history = _loadHistory();
  if (!history[trackingNumber]) {
    history[trackingNumber] = { events: [] };
  }
  history[trackingNumber].events.push(record);
  _saveHistory(history);
}

/**
 * Get notification history for a tracking number.
 * @param {string} trackingNumber
 * @returns {object|null} - { events: [...] } or null
 */
function getNotificationHistory(trackingNumber) {
  const history = _loadHistory();
  return history[trackingNumber] || null;
}

// ---------------------------------------------------------------------------
// Event ID Generation
// ---------------------------------------------------------------------------

/**
 * Generate a unique event ID for notification dedup.
 * Based on trackingNumber + eventType + timestamp/description.
 * @param {string} trackingNumber
 * @param {string} eventType - shipped/delivered/customs_cleared/out_for_delivery/exception
 * @param {string} [extra] - Additional differentiator (e.g., event description or timestamp)
 * @returns {string} - 16-char hex hash
 */
function generateNotifyEventId(trackingNumber, eventType, extra) {
  const input = `${trackingNumber}|${eventType}|${extra || ''}`;
  return crypto.createHash('sha256').update(input).digest('hex').substring(0, 16);
}

// ---------------------------------------------------------------------------
// Dedup Check
// ---------------------------------------------------------------------------

/**
 * Check if an event notification has already been sent (idempotency).
 * @param {string} trackingNumber
 * @param {string} eventId
 * @returns {boolean} - true if already sent
 */
function isAlreadyNotified(trackingNumber, eventId) {
  const record = getNotificationHistory(trackingNumber);
  if (!record || !record.events) return false;
  return record.events.some(e => e.eventId === eventId);
}

// ---------------------------------------------------------------------------
// Frequency Control
// ---------------------------------------------------------------------------

/**
 * Check if sending a notification would violate frequency limits.
 * Uses config.notification.frequency_control settings.
 * @param {string} trackingNumber
 * @returns {{ allowed: boolean, reason?: string }}
 */
function checkFrequencyLimit(trackingNumber) {
  const config = loadConfig();
  const freqCtrl = config.notification.frequency_control;
  const maxPerDay = freqCtrl.max_notifications_per_shipment_per_day;
  const cooldownMin = freqCtrl.cooldown_minutes;

  const record = getNotificationHistory(trackingNumber);
  if (!record || !record.events || record.events.length === 0) {
    return { allowed: true };
  }

  const now = Date.now();
  const oneDayAgo = now - 24 * 60 * 60 * 1000;

  // Count notifications in last 24h
  const recentEvents = record.events.filter(e => {
    const ts = new Date(e.sentAt).getTime();
    return ts > oneDayAgo;
  });

  if (recentEvents.length >= maxPerDay) {
    return {
      allowed: false,
      reason: `Daily limit reached (${recentEvents.length}/${maxPerDay} in last 24h)`
    };
  }

  // Check cooldown since last notification
  const lastEvent = record.events[record.events.length - 1];
  const lastSentAt = new Date(lastEvent.sentAt).getTime();
  const cooldownMs = cooldownMin * 60 * 1000;

  if (now - lastSentAt < cooldownMs) {
    const remainMin = Math.ceil((cooldownMs - (now - lastSentAt)) / 60000);
    return {
      allowed: false,
      reason: `Cooldown active (${remainMin} minutes remaining)`
    };
  }

  return { allowed: true };
}

// ---------------------------------------------------------------------------
// Should Notify Decision
// ---------------------------------------------------------------------------

/**
 * Determine whether a notification should be sent for a given event type.
 * Considers: default events, opt-in events, dedup, frequency limits.
 * @param {object} shipment - Shipment object from shipment-store
 * @param {string} eventType - shipped/delivered/customs_cleared/out_for_delivery/exception
 * @param {object} [opts]
 * @param {string} [opts.eventId] - Pre-computed event ID
 * @param {boolean} [opts.forceOptIn] - Force opt-in events to send
 * @returns {{ should: boolean, reason?: string }}
 */
function shouldNotify(shipment, eventType, opts) {
  opts = opts || {};
  const config = loadConfig();
  const notifConfig = config.notification;
  const trackingNumber = shipment.tracking_number;

  // 1. Check if eventType is in default or opt-in list
  const isDefault = notifConfig.default_events.includes(eventType);
  const isOptIn = notifConfig.opt_in_events.includes(eventType);

  if (!isDefault && !isOptIn) {
    return { should: false, reason: `Event type "${eventType}" is not configured for notifications` };
  }

  if (isOptIn && !opts.forceOptIn) {
    // Check if customer has opted in (via shipment.notification_preferences)
    const prefs = shipment.notification_preferences || {};
    const optedIn = prefs.opt_in_events && prefs.opt_in_events.includes(eventType);
    if (!optedIn) {
      return { should: false, reason: `Event type "${eventType}" requires opt-in (customer not opted in)` };
    }
  }

  // 2. Dedup check
  const eventId = opts.eventId || generateNotifyEventId(trackingNumber, eventType, opts.extra || '');
  if (isAlreadyNotified(trackingNumber, eventId)) {
    return { should: false, reason: `Already notified (eventId: ${eventId})` };
  }

  // 3. Frequency limit check
  const freqCheck = checkFrequencyLimit(trackingNumber);
  if (!freqCheck.allowed) {
    return { should: false, reason: freqCheck.reason };
  }

  return { should: true, eventId };
}

// ---------------------------------------------------------------------------
// HTML Email Templates
// ---------------------------------------------------------------------------

/**
 * Build 17track self-service tracking link.
 * @param {string} trackingNumber
 * @returns {string} URL
 */
function buildTrackingLink(trackingNumber) {
  const config = loadConfig();
  const template = config.notification.self_track_link.template;
  return template.replace('{tracking_number}', encodeURIComponent(trackingNumber));
}

/**
 * Build HTML email content for a notification.
 * @param {string} templateName - shipped/delivered/exception
 * @param {object} data
 * @param {string} data.tracking_number
 * @param {string} [data.customer_name]
 * @param {string} [data.carrier_name]
 * @param {string} [data.order_id]
 * @param {string} [data.event_description]
 * @param {string} [data.event_time]
 * @returns {string} HTML string
 */
function buildEmailHtml(templateName, data) {
  const trackingLink = buildTrackingLink(data.tracking_number);
  const customerName = data.customer_name || 'Valued Customer';
  const carrierName = data.carrier_name || 'the carrier';
  const trackingNumber = data.tracking_number;
  const orderId = data.order_id || '';

  const baseStyle = `
    <style>
      body { font-family: Arial, Helvetica, sans-serif; color: #333; line-height: 1.6; margin: 0; padding: 0; }
      .container { max-width: 600px; margin: 0 auto; padding: 20px; }
      .header { background-color: #2563eb; color: #fff; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }
      .header h1 { margin: 0; font-size: 22px; }
      .content { background-color: #f9fafb; padding: 24px; border: 1px solid #e5e7eb; }
      .tracking-box { background: #fff; border: 2px solid #2563eb; border-radius: 8px; padding: 16px; text-align: center; margin: 16px 0; }
      .tracking-number { font-size: 20px; font-weight: bold; color: #2563eb; letter-spacing: 1px; }
      .btn { display: inline-block; background: #2563eb; color: #fff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; margin: 12px 0; }
      .footer { text-align: center; color: #9ca3af; font-size: 12px; padding: 16px; border-top: 1px solid #e5e7eb; }
      .info-table { width: 100%; border-collapse: collapse; margin: 12px 0; }
      .info-table td { padding: 8px 12px; border-bottom: 1px solid #e5e7eb; }
      .info-table td:first-child { color: #6b7280; width: 120px; }
    </style>
  `;

  if (templateName === 'shipped') {
    return `<!DOCTYPE html>
<html>
<head><meta charset="utf-8">${baseStyle}</head>
<body>
  <div class="container">
    <div class="header">
      <h1>📦 Your Order Has Been Shipped!</h1>
    </div>
    <div class="content">
      <p>Dear ${customerName},</p>
      <p>Great news! Your order${orderId ? ' <strong>' + orderId + '</strong>' : ''} has been shipped via <strong>${carrierName}</strong>.</p>

      <div class="tracking-box">
        <p style="margin:0 0 8px 0; color:#6b7280;">Tracking Number</p>
        <div class="tracking-number">${trackingNumber}</div>
      </div>

      <table class="info-table">
        ${orderId ? '<tr><td>Order ID</td><td><strong>' + orderId + '</strong></td></tr>' : ''}
        <tr><td>Carrier</td><td><strong>${carrierName}</strong></td></tr>
        <tr><td>Tracking No.</td><td><strong>${trackingNumber}</strong></td></tr>
      </table>

      <p style="text-align:center;">
        <a href="${trackingLink}" class="btn">Track Your Shipment</a>
      </p>
      <p style="text-align:center; color:#6b7280; font-size:13px;">
        Click the button above or visit <a href="${trackingLink}">${trackingLink}</a> to check your delivery status anytime.
      </p>
    </div>
    <div class="footer">
      <p>Thank you for your business!</p>
      <p>Farreach Electronic Co., Ltd (SKW)</p>
    </div>
  </div>
</body>
</html>`;
  }

  if (templateName === 'delivered') {
    return `<!DOCTYPE html>
<html>
<head><meta charset="utf-8">${baseStyle}</head>
<body>
  <div class="container">
    <div class="header" style="background-color:#16a34a;">
      <h1>✅ Your Order Has Been Delivered!</h1>
    </div>
    <div class="content">
      <p>Dear ${customerName},</p>
      <p>Your order${orderId ? ' <strong>' + orderId + '</strong>' : ''} has been successfully delivered.</p>

      <div class="tracking-box" style="border-color:#16a34a;">
        <p style="margin:0 0 8px 0; color:#6b7280;">Tracking Number</p>
        <div class="tracking-number" style="color:#16a34a;">${trackingNumber}</div>
      </div>

      <table class="info-table">
        ${orderId ? '<tr><td>Order ID</td><td><strong>' + orderId + '</strong></td></tr>' : ''}
        <tr><td>Carrier</td><td><strong>${carrierName}</strong></td></tr>
        <tr><td>Status</td><td><strong style="color:#16a34a;">Delivered</strong></td></tr>
      </table>

      <p>If you have any questions about your order, please don't hesitate to contact us.</p>

      <p style="text-align:center;">
        <a href="${trackingLink}" class="btn" style="background:#16a34a;">View Delivery Details</a>
      </p>
    </div>
    <div class="footer">
      <p>Thank you for choosing us!</p>
      <p>Farreach Electronic Co., Ltd (SKW)</p>
    </div>
  </div>
</body>
</html>`;
  }

  if (templateName === 'exception') {
    const eventDesc = data.event_description || 'There is an update regarding your shipment.';
    const eventTime = data.event_time || '';
    return `<!DOCTYPE html>
<html>
<head><meta charset="utf-8">${baseStyle}</head>
<body>
  <div class="container">
    <div class="header" style="background-color:#ea580c;">
      <h1>⚠️ Shipping Update</h1>
    </div>
    <div class="content">
      <p>Dear ${customerName},</p>
      <p>We have an update regarding your shipment${orderId ? ' for order <strong>' + orderId + '</strong>' : ''}:</p>

      <div class="tracking-box" style="border-color:#ea580c;">
        <p style="margin:0 0 8px 0; color:#6b7280;">Tracking Number</p>
        <div class="tracking-number" style="color:#ea580c;">${trackingNumber}</div>
        ${eventTime ? '<p style="margin:8px 0 0 0; color:#6b7280; font-size:13px;">' + eventTime + '</p>' : ''}
      </div>

      <p><strong>Update:</strong> ${eventDesc}</p>

      <p>We are monitoring this closely. If you need assistance, please contact us directly.</p>

      <p style="text-align:center;">
        <a href="${trackingLink}" class="btn" style="background:#ea580c;">Track Your Shipment</a>
      </p>
    </div>
    <div class="footer">
      <p>We appreciate your patience.</p>
      <p>Farreach Electronic Co., Ltd (SKW)</p>
    </div>
  </div>
</body>
</html>`;
  }

  // Generic fallback for opt-in events (customs_cleared, out_for_delivery, etc.)
  const eventDesc = data.event_description || `Status update: ${templateName}`;
  return `<!DOCTYPE html>
<html>
<head><meta charset="utf-8">${baseStyle}</head>
<body>
  <div class="container">
    <div class="header">
      <h1>📦 Shipping Update</h1>
    </div>
    <div class="content">
      <p>Dear ${customerName},</p>
      <p>Here's an update on your shipment${orderId ? ' for order <strong>' + orderId + '</strong>' : ''}:</p>

      <div class="tracking-box">
        <p style="margin:0 0 8px 0; color:#6b7280;">Tracking Number</p>
        <div class="tracking-number">${trackingNumber}</div>
      </div>

      <p><strong>Update:</strong> ${eventDesc}</p>

      <p style="text-align:center;">
        <a href="${trackingLink}" class="btn">Track Your Shipment</a>
      </p>
    </div>
    <div class="footer">
      <p>Thank you for your business!</p>
      <p>Farreach Electronic Co., Ltd (SKW)</p>
    </div>
  </div>
</body>
</html>`;
}

// ---------------------------------------------------------------------------
// Email Subject Builder
// ---------------------------------------------------------------------------

/**
 * Build email subject from config templates.
 * @param {string} eventType - shipped/delivered/exception
 * @param {object} data - { tracking_number, ... }
 * @returns {string}
 */
function buildSubject(eventType, data) {
  const config = loadConfig();
  const templates = config.notification.templates;
  const tpl = templates[eventType];

  if (tpl && tpl.subject) {
    return tpl.subject
      .replace('{tracking_number}', data.tracking_number)
      .replace('#{tracking_number}', data.tracking_number);
  }

  // Fallback subjects
  const fallbacks = {
    shipped: `Your order has been shipped - Tracking #${data.tracking_number}`,
    delivered: `Your order has been delivered - #${data.tracking_number}`,
    customs_cleared: `Customs cleared - Tracking #${data.tracking_number}`,
    out_for_delivery: `Out for delivery - Tracking #${data.tracking_number}`,
    exception: `Shipping update for your order - #${data.tracking_number}`
  };

  return fallbacks[eventType] || `Shipping update - #${data.tracking_number}`;
}

// ---------------------------------------------------------------------------
// SMTP Integration
// ---------------------------------------------------------------------------

/**
 * Send an email via imap-smtp-email SMTP script.
 * @param {object} params
 * @param {string} params.to - Recipient email
 * @param {string} params.subject - Email subject
 * @param {string} params.html - HTML body
 * @param {boolean} [params.dryRun] - If true, skip actual sending
 * @returns {{ success: boolean, message: string, dryRun?: boolean }}
 */
function _sendEmail(params) {
  if (params.dryRun) {
    return {
      success: true,
      message: `[DRY-RUN] Would send to: ${params.to}, subject: "${params.subject}"`,
      dryRun: true
    };
  }

  // Write HTML to temp file for smtp.js --html-file
  const tmpDir = path.resolve(__dirname, '../data/tmp');
  if (!fs.existsSync(tmpDir)) {
    fs.mkdirSync(tmpDir, { recursive: true });
  }
  const tmpFile = path.join(tmpDir, `notify-${Date.now()}.html`);

  try {
    fs.writeFileSync(tmpFile, params.html, 'utf8');

    const args = [
      SMTP_SCRIPT,
      'send',
      '--to', params.to,
      '--subject', params.subject,
      '--html-file', tmpFile
    ];

    const result = execFileSync('node', args, {
      encoding: 'utf8',
      timeout: 30000,
      env: process.env
    });

    return {
      success: true,
      message: result.trim() || 'Email sent successfully'
    };
  } catch (err) {
    return {
      success: false,
      message: `Failed to send email: ${err.message}`
    };
  } finally {
    // Clean up temp file
    try { fs.unlinkSync(tmpFile); } catch { /* ignore */ }
  }
}

// ---------------------------------------------------------------------------
// Core Notification Functions
// ---------------------------------------------------------------------------

/**
 * Send a notification for a specific event type.
 * Performs all checks (dedup, frequency, opt-in) before sending.
 *
 * @param {object} shipment - Shipment object from shipment-store
 * @param {string} eventType - shipped/delivered/customs_cleared/out_for_delivery/exception
 * @param {object} [data] - Additional data for template rendering
 * @param {string} [data.event_description] - Description for exception/update events
 * @param {string} [data.event_time] - Timestamp for the event
 * @param {object} [opts]
 * @param {boolean} [opts.dryRun] - Skip actual sending
 * @param {boolean} [opts.forceOptIn] - Force opt-in events to send
 * @param {string} [opts.eventId] - Pre-computed event ID for dedup
 * @param {string} [opts.extra] - Extra differentiator for eventId generation
 * @returns {{ sent: boolean, reason?: string, eventId?: string, dryRun?: boolean }}
 */
function sendNotification(shipment, eventType, data, opts) {
  data = data || {};
  opts = opts || {};

  const trackingNumber = shipment.tracking_number;
  const recipient = shipment.customer_email;

  // Validate recipient
  if (!recipient) {
    return { sent: false, reason: 'No customer email on shipment record' };
  }

  // Check if notification should be sent
  const check = shouldNotify(shipment, eventType, {
    eventId: opts.eventId,
    forceOptIn: opts.forceOptIn,
    extra: opts.extra
  });

  if (!check.should) {
    return { sent: false, reason: check.reason };
  }

  const eventId = check.eventId;

  // Determine template name (map eventType to template)
  let templateName = eventType;
  if (!['shipped', 'delivered', 'exception'].includes(eventType)) {
    // opt-in events use generic template or exception template
    templateName = eventType;
  }

  // Build email content
  const templateData = {
    tracking_number: trackingNumber,
    customer_name: shipment.customer_name || data.customer_name,
    carrier_name: shipment.carrier_name || data.carrier_name,
    order_id: shipment.order_id || data.order_id,
    event_description: data.event_description,
    event_time: data.event_time
  };

  const subject = buildSubject(eventType, templateData);
  const html = buildEmailHtml(templateName, templateData);

  // Send email
  const result = _sendEmail({
    to: recipient,
    subject,
    html,
    dryRun: opts.dryRun
  });

  if (result.success) {
    // Record in history (even dry-run, for testing)
    if (!opts.dryRun) {
      _recordNotification(trackingNumber, {
        eventId,
        eventType,
        sentAt: new Date().toISOString(),
        recipient,
        subject
      });
    }

    return {
      sent: true,
      eventId,
      dryRun: opts.dryRun || false,
      message: result.message
    };
  }

  return {
    sent: false,
    reason: result.message,
    eventId
  };
}

/**
 * Send a "shipped" notification.
 * Convenience wrapper for sendNotification with eventType="shipped".
 * @param {object} shipment
 * @param {object} [opts] - { dryRun }
 * @returns {{ sent: boolean, reason?: string, eventId?: string }}
 */
function sendShippedNotification(shipment, opts) {
  return sendNotification(shipment, 'shipped', {}, opts);
}

/**
 * Send a "delivered" notification.
 * @param {object} shipment
 * @param {object} [opts] - { dryRun }
 * @returns {{ sent: boolean, reason?: string, eventId?: string }}
 */
function sendDeliveredNotification(shipment, opts) {
  return sendNotification(shipment, 'delivered', {}, opts);
}

/**
 * Send a notification for a specific tracking event (opt-in mid-transit events).
 * @param {object} shipment
 * @param {object} event - Tracking event object { description, timestamp, ... }
 * @param {object} [opts] - { dryRun, forceOptIn }
 * @returns {{ sent: boolean, reason?: string, eventId?: string }}
 */
function sendEventNotification(shipment, event, opts) {
  opts = opts || {};
  const eventType = _mapEventToType(event);
  return sendNotification(shipment, eventType, {
    event_description: event.description,
    event_time: event.timestamp
  }, {
    ...opts,
    extra: event.timestamp + '|' + (event.description || '')
  });
}

/**
 * Process a batch of shipments and send notifications for eligible events.
 * Useful for scheduler integration.
 * @param {object[]} shipments - Array of shipment objects
 * @param {object} [opts] - { dryRun }
 * @returns {{ total: number, sent: number, skipped: number, failed: number, details: object[] }}
 */
function processBatchNotifications(shipments, opts) {
  opts = opts || {};
  const results = { total: 0, sent: 0, skipped: 0, failed: 0, details: [] };

  for (const shipment of shipments) {
    if (!shipment || !shipment.tracking_number) continue;

    const status = shipment.status;
    let eventType = null;

    // Determine what notification to send based on current status
    if (status === 'in_transit' && !_hasBeenNotified(shipment.tracking_number, 'shipped')) {
      eventType = 'shipped';
    } else if (status === 'delivered' && !_hasBeenNotified(shipment.tracking_number, 'delivered')) {
      eventType = 'delivered';
    }

    if (!eventType) {
      results.skipped++;
      continue;
    }

    results.total++;
    const result = sendNotification(shipment, eventType, {}, opts);

    results.details.push({
      tracking_number: shipment.tracking_number,
      eventType,
      ...result
    });

    if (result.sent) {
      results.sent++;
    } else if (result.reason && result.reason.includes('Failed')) {
      results.failed++;
    } else {
      results.skipped++;
    }
  }

  return results;
}

// ---------------------------------------------------------------------------
// Internal Helpers
// ---------------------------------------------------------------------------

/**
 * Check if a specific event type notification has been sent for a tracking number.
 * @param {string} trackingNumber
 * @param {string} eventType
 * @returns {boolean}
 */
function _hasBeenNotified(trackingNumber, eventType) {
  const record = getNotificationHistory(trackingNumber);
  if (!record || !record.events) return false;
  return record.events.some(e => e.eventType === eventType);
}

/**
 * Map a tracking event to a notification event type.
 * @param {object} event - { description, status, ... }
 * @returns {string} - Event type for notification config
 */
function _mapEventToType(event) {
  const desc = (event.description || '').toLowerCase();
  const status = (event.status || '').toLowerCase();

  if (desc.includes('customs cleared') || desc.includes('released from customs') || status === 'customs_cleared') {
    return 'customs_cleared';
  }
  if (desc.includes('out for delivery') || desc.includes('delivering') || status === 'out_for_delivery') {
    return 'out_for_delivery';
  }
  if (desc.includes('delivered') || status === 'delivered') {
    return 'delivered';
  }
  if (desc.includes('shipped') || desc.includes('picked up') || status === 'shipped') {
    return 'shipped';
  }

  return 'exception';
}

// ---------------------------------------------------------------------------
// Module Exports
// ---------------------------------------------------------------------------

module.exports = {
  // Core notification functions
  sendNotification,
  sendShippedNotification,
  sendDeliveredNotification,
  sendEventNotification,
  processBatchNotifications,

  // Decision & checking
  shouldNotify,
  isAlreadyNotified,
  checkFrequencyLimit,

  // Template building
  buildEmailHtml,
  buildSubject,
  buildTrackingLink,

  // History
  getNotificationHistory,

  // Event ID
  generateNotifyEventId,

  // Config
  loadConfig,
  reloadConfig,

  // Internal (exposed for testing)
  _sendEmail,
  _loadHistory,
  _saveHistory,
  _recordNotification,
  _hasBeenNotified,
  _mapEventToType
};
