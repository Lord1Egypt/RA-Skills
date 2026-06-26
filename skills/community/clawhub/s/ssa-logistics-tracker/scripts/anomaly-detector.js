/**
 * anomaly-detector.js - 物流异常检测模块
 *
 * 功能：
 *  - detectAnomalies(shipments, opts)          批量异常检测（超时/清关/退回/丢失）
 *  - detectNoUpdateAnomaly(shipment)           单运单无更新检测
 *  - detectCustomsHoldAnomaly(shipment)        清关滞留检测
 *  - detectReturnAnomaly(shipment)             退回检测
 *  - detectLostAnomaly(shipment)               丢失检测
 *  - sendAnomalyAlerts(anomalies, opts)        双渠道告警（Discord + 邮件）
 *  - syncShippedOrders(opts)                   从 order-tracker 同步已发货订单并创建跟踪任务
 *  - runFullDetection(opts)                    完整检测流程（同步 + 检测 + 告警）
 *
 * 特性：
 *  - 双渠道告警（Discord 消息 + 邮件通知 Wilson）
 *  - 自动重试机制（告警发送失败指数退避重试）
 *  - 从 order-tracker 读取已发货订单，自动创建 shipment-store 跟踪记录
 *  - 完整状态机联动（检测到退回/丢失自动流转状态）
 *  - dry-run 模式
 *  - 可通过 require() 导入
 *
 * 配置文件：../config/logistics-config.json
 *
 * @module anomaly-detector
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

// ---------------------------------------------------------------------------
// Module imports
// ---------------------------------------------------------------------------

const shipmentStore = require('./shipment-store');
const trackingApi = require('./tracking-api');

// ---------------------------------------------------------------------------
// Paths
// ---------------------------------------------------------------------------

const CONFIG_PATH = path.resolve(__dirname, '../config/logistics-config.json');
const ALERT_HISTORY_PATH = path.resolve(__dirname, '../data/alert-history.json');
const ORDER_TRACKER_ORDERS_PATH = path.resolve(
  __dirname,
  '../../order-tracker/data/orders.json'
);
const SMTP_SCRIPT = path.resolve(
  __dirname,
  '../../imap-smtp-email/scripts/smtp.js'
);

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

let _configCache = null;

/**
 * Load logistics config (cached).
 * @returns {object}
 */
function loadConfig() {
  if (_configCache) return _configCache;
  const raw = fs.readFileSync(CONFIG_PATH, 'utf-8');
  _configCache = JSON.parse(raw);
  return _configCache;
}

/**
 * Force reload config.
 * @returns {object}
 */
function reloadConfig() {
  _configCache = null;
  return loadConfig();
}

// ---------------------------------------------------------------------------
// Alert history (dedup + persistence)
// ---------------------------------------------------------------------------

/**
 * Load alert history from disk.
 * Structure: { [trackingNumber]: { alerts: [ { type, sentAt, channels } ] } }
 * @returns {object}
 */
function _loadAlertHistory() {
  try {
    const raw = fs.readFileSync(ALERT_HISTORY_PATH, 'utf-8');
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

/**
 * Save alert history with atomic write.
 * @param {object} history
 */
function _saveAlertHistory(history) {
  const dir = path.dirname(ALERT_HISTORY_PATH);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  const tmp = ALERT_HISTORY_PATH + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(history, null, 2), 'utf-8');
  fs.renameSync(tmp, ALERT_HISTORY_PATH);
}

/**
 * Record a sent alert.
 * @param {string} trackingNumber
 * @param {object} record - { type, sentAt, channels, message }
 */
function _recordAlert(trackingNumber, record) {
  const history = _loadAlertHistory();
  if (!history[trackingNumber]) {
    history[trackingNumber] = { alerts: [] };
  }
  history[trackingNumber].alerts.push(record);
  _saveAlertHistory(history);
}

/**
 * Check if an alert of a given type was already sent today for a tracking number.
 * Prevents duplicate alerts for the same anomaly within 24h.
 * @param {string} trackingNumber
 * @param {string} alertType
 * @returns {boolean}
 */
function _isAlertedToday(trackingNumber, alertType) {
  const history = _loadAlertHistory();
  const record = history[trackingNumber];
  if (!record || !record.alerts) return false;

  const oneDayAgo = Date.now() - 24 * 60 * 60 * 1000;
  return record.alerts.some(
    (a) => a.type === alertType && new Date(a.sentAt).getTime() > oneDayAgo
  );
}

// ---------------------------------------------------------------------------
// Retry helper
// ---------------------------------------------------------------------------

/**
 * Execute a function with exponential backoff retry.
 * Uses delays from config.retry or defaults to [1, 5, 15] minutes.
 *
 * @param {Function} fn - Synchronous or async function to execute
 * @param {object} [opts]
 * @param {number} [opts.maxAttempts=3]
 * @param {number[]} [opts.delaysMs] - Delay schedule in ms
 * @returns {Promise<any>} Result of fn
 */
async function withRetry(fn, opts) {
  opts = opts || {};
  const config = loadConfig();
  const retryConf = config.retry || {};
  const maxAttempts = opts.maxAttempts || retryConf.max_attempts || 3;
  const delaysMin = retryConf.delays_minutes || [1, 5, 15];
  const delaysMs = opts.delaysMs || delaysMin.map((m) => m * 60 * 1000);

  let lastErr;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastErr = err;
      if (attempt >= maxAttempts - 1) throw err;
      const delay = delaysMs[attempt] || delaysMs[delaysMs.length - 1];
      console.log(
        `[anomaly-detector] Attempt ${attempt + 1} failed: ${err.message}. Retrying in ${delay / 1000}s...`
      );
      await new Promise((r) => setTimeout(r, delay));
    }
  }
  throw lastErr;
}

// ---------------------------------------------------------------------------
// Anomaly detection: individual checks
// ---------------------------------------------------------------------------

/**
 * Check a single shipment for "no update" anomaly.
 * Triggers when no tracking event for N days (but less than lost threshold).
 *
 * @param {object} shipment - Shipment from shipment-store (with tracking_number attached)
 * @returns {object|null} Anomaly object or null
 */
function detectNoUpdateAnomaly(shipment) {
  const config = loadConfig();
  const anomalyConf = config.anomaly || {};
  const noUpdateDays = anomalyConf.no_update_threshold_days || 7;
  const lostDays = (anomalyConf.lost_detection || {}).no_update_days || 30;
  const terminalStates = (config.state_machine || {}).terminal_states || [
    'delivered',
    'returned',
    'lost',
  ];

  const tn = shipment.tracking_number || shipment.trackingNumber;
  if (terminalStates.includes(shipment.status)) return null;

  const daysSince = _daysSinceLastEvent(shipment);
  if (daysSince >= noUpdateDays && daysSince < lostDays) {
    const template = (anomalyConf.alert_templates || {}).no_update || '';
    return {
      type: 'no_update',
      trackingNumber: tn,
      daysSinceUpdate: daysSince,
      severity: 'warning',
      customerName: shipment.customerName || shipment.customer_name || 'Unknown',
      carrier: shipment.carrier || 'Unknown',
      message: template
        .replace('{tracking_number}', tn)
        .replace('{customer_name}', shipment.customerName || shipment.customer_name || 'Unknown')
        .replace('{days}', String(daysSince)),
    };
  }
  return null;
}

/**
 * Check a single shipment for customs hold anomaly.
 * Triggers when status is customs_clearance for longer than threshold.
 *
 * @param {object} shipment
 * @returns {object|null}
 */
function detectCustomsHoldAnomaly(shipment) {
  const config = loadConfig();
  const anomalyConf = config.anomaly || {};
  const customsHoldDays = anomalyConf.customs_hold_threshold_days || 5;

  if (shipment.status !== 'customs_clearance') return null;

  const tn = shipment.tracking_number || shipment.trackingNumber;
  const customsEntryTime = _findCustomsEntryTime(shipment);
  if (!customsEntryTime) return null;

  const customsDays = Math.floor(
    (Date.now() - customsEntryTime) / (24 * 60 * 60 * 1000)
  );
  if (customsDays < customsHoldDays) return null;

  const template = (anomalyConf.alert_templates || {}).customs_hold || '';
  return {
    type: 'customs_hold',
    trackingNumber: tn,
    daysSinceUpdate: customsDays,
    severity: 'warning',
    customerName: shipment.customerName || shipment.customer_name || 'Unknown',
    carrier: shipment.carrier || 'Unknown',
    message: template
      .replace('{tracking_number}', tn)
      .replace('{days}', String(customsDays)),
  };
}

/**
 * Check a single shipment for return anomaly (keyword-based).
 *
 * @param {object} shipment
 * @returns {object|null}
 */
function detectReturnAnomaly(shipment) {
  const config = loadConfig();
  const anomalyConf = config.anomaly || {};
  const returnConf = anomalyConf.return_detection || {};

  if (!returnConf.enabled) return null;
  if (shipment.status === 'returning' || shipment.status === 'returned') return null;

  const tn = shipment.tracking_number || shipment.trackingNumber;
  const events = shipment.events || [];
  const keywords = (returnConf.keywords || []).map((k) => k.toLowerCase());

  const recentEvents = events.slice(-5);
  for (const evt of recentEvents) {
    const desc = (evt.description || '').toLowerCase();
    if (keywords.some((kw) => desc.includes(kw))) {
      const template = (anomalyConf.alert_templates || {}).returned || '';
      return {
        type: 'return_detected',
        trackingNumber: tn,
        severity: 'warning',
        customerName: shipment.customerName || shipment.customer_name || 'Unknown',
        carrier: shipment.carrier || 'Unknown',
        triggerEvent: evt.description,
        message: template.replace('{tracking_number}', tn),
      };
    }
  }
  return null;
}

/**
 * Check a single shipment for lost anomaly (extended no-update).
 *
 * @param {object} shipment
 * @returns {object|null}
 */
function detectLostAnomaly(shipment) {
  const config = loadConfig();
  const anomalyConf = config.anomaly || {};
  const lostConf = anomalyConf.lost_detection || {};
  const lostDays = lostConf.no_update_days || 30;
  const terminalStates = (config.state_machine || {}).terminal_states || [
    'delivered',
    'returned',
    'lost',
  ];

  if (!lostConf.enabled) return null;
  if (terminalStates.includes(shipment.status)) return null;

  const tn = shipment.tracking_number || shipment.trackingNumber;
  const daysSince = _daysSinceLastEvent(shipment);

  if (daysSince >= lostDays) {
    const template = (anomalyConf.alert_templates || {}).lost || '';
    return {
      type: 'lost_suspect',
      trackingNumber: tn,
      daysSinceUpdate: daysSince,
      severity: 'critical',
      customerName: shipment.customerName || shipment.customer_name || 'Unknown',
      carrier: shipment.carrier || 'Unknown',
      message: template
        .replace('{tracking_number}', tn)
        .replace('{days}', String(daysSince)),
    };
  }
  return null;
}

// ---------------------------------------------------------------------------
// Batch anomaly detection
// ---------------------------------------------------------------------------

/**
 * Run all anomaly checks on a list of shipments.
 * Optionally auto-transitions status for return/lost anomalies.
 *
 * @param {object[]} shipments - Array of shipment objects (with tracking_number)
 * @param {object} [opts]
 * @param {boolean} [opts.dryRun=false]
 * @param {boolean} [opts.autoTransition=true] - Auto-transition status on return/lost
 * @returns {{
 *   anomalies: object[],
 *   transitioned: { trackingNumber: string, from: string, to: string }[],
 *   checked: number
 * }}
 */
function detectAnomalies(shipments, opts) {
  opts = opts || {};
  const autoTransition =
    opts.autoTransition !== undefined ? opts.autoTransition : true;
  const dryRun = opts.dryRun || false;

  const anomalies = [];
  const transitioned = [];

  for (const shipment of shipments) {
    const tn = shipment.tracking_number || shipment.trackingNumber;
    if (!tn) continue;

    // 1. No-update check
    const noUpdate = detectNoUpdateAnomaly(shipment);
    if (noUpdate) anomalies.push(noUpdate);

    // 2. Customs hold check
    const customs = detectCustomsHoldAnomaly(shipment);
    if (customs) anomalies.push(customs);

    // 3. Return check
    const returnAnomaly = detectReturnAnomaly(shipment);
    if (returnAnomaly) {
      anomalies.push(returnAnomaly);
      if (autoTransition && !dryRun) {
        const result = shipmentStore.transitionStatus(tn, 'returning', {
          reason: `Return detected in event: "${returnAnomaly.triggerEvent}"`,
        });
        if (result.success) {
          transitioned.push({
            trackingNumber: tn,
            from: shipment.status,
            to: 'returning',
          });
        }
      }
    }

    // 4. Lost check
    const lost = detectLostAnomaly(shipment);
    if (lost) {
      anomalies.push(lost);
      if (autoTransition && !dryRun) {
        const result = shipmentStore.transitionStatus(tn, 'lost', {
          reason: `No update for ${lost.daysSinceUpdate} days (auto-detected)`,
          force: true,
        });
        if (result.success) {
          transitioned.push({
            trackingNumber: tn,
            from: shipment.status,
            to: 'lost',
          });
        }
      }
    }
  }

  return { anomalies, transitioned, checked: shipments.length };
}

// ---------------------------------------------------------------------------
// Alert sending: Discord + Email
// ---------------------------------------------------------------------------

/**
 * Send anomaly alerts through both Discord and email channels.
 * Deduplicates: same anomaly type + tracking number won't re-alert within 24h.
 * Retries on failure with exponential backoff.
 *
 * @param {object[]} anomalies - Array of anomaly objects from detectAnomalies()
 * @param {object} [opts]
 * @param {boolean} [opts.dryRun=false]
 * @param {boolean} [opts.skipDedup=false] - Skip 24h dedup check
 * @returns {Promise<{
 *   sent: number,
 *   skipped: number,
 *   failed: number,
 *   details: object[]
 * }>}
 */
async function sendAnomalyAlerts(anomalies, opts) {
  opts = opts || {};
  const dryRun = opts.dryRun || false;
  const skipDedup = opts.skipDedup || false;
  const results = { sent: 0, skipped: 0, failed: 0, details: [] };

  if (!anomalies || anomalies.length === 0) return results;

  for (const anomaly of anomalies) {
    const tn = anomaly.trackingNumber;

    // Dedup check
    if (!skipDedup && _isAlertedToday(tn, anomaly.type)) {
      results.skipped++;
      results.details.push({
        trackingNumber: tn,
        type: anomaly.type,
        status: 'skipped',
        reason: 'Already alerted in last 24h',
      });
      continue;
    }

    if (dryRun) {
      console.log(
        `[anomaly-detector][DRY-RUN] Would send alert: [${anomaly.severity}] ${anomaly.message}`
      );
      results.sent++;
      results.details.push({
        trackingNumber: tn,
        type: anomaly.type,
        status: 'dry-run',
      });
      continue;
    }

    // Send to both channels
    const channelResults = { discord: false, email: false };

    // Channel 1: Discord
    try {
      await withRetry(
        () => _sendDiscordAlert(anomaly),
        { maxAttempts: 3, delaysMs: [5000, 15000, 30000] }
      );
      channelResults.discord = true;
    } catch (err) {
      console.error(
        `[anomaly-detector] Discord alert failed for ${tn}: ${err.message}`
      );
    }

    // Channel 2: Email
    try {
      await withRetry(
        () => _sendEmailAlert(anomaly),
        { maxAttempts: 3, delaysMs: [5000, 15000, 30000] }
      );
      channelResults.email = true;
    } catch (err) {
      console.error(
        `[anomaly-detector] Email alert failed for ${tn}: ${err.message}`
      );
    }

    const anySent = channelResults.discord || channelResults.email;

    if (anySent) {
      _recordAlert(tn, {
        type: anomaly.type,
        sentAt: new Date().toISOString(),
        channels: channelResults,
        message: anomaly.message,
        severity: anomaly.severity,
      });
      results.sent++;
    } else {
      results.failed++;
    }

    results.details.push({
      trackingNumber: tn,
      type: anomaly.type,
      status: anySent ? 'sent' : 'failed',
      channels: channelResults,
    });
  }

  return results;
}

/**
 * Send a single anomaly alert to Discord via stdout (picked up by OpenClaw).
 * Uses console.log with structured prefix for Discord delivery.
 *
 * @param {object} anomaly
 */
function _sendDiscordAlert(anomaly) {
  const severityIcon =
    anomaly.severity === 'critical' ? '🚨' : '⚠️';
  const message = `${severityIcon} **物流异常告警** [${anomaly.type}]\n${anomaly.message}\nCarrier: ${anomaly.carrier || 'N/A'} | Customer: ${anomaly.customerName || 'N/A'}`;

  // Write structured alert to a file for Discord bot pickup
  const alertDir = path.resolve(__dirname, '../data/discord-alerts');
  if (!fs.existsSync(alertDir)) {
    fs.mkdirSync(alertDir, { recursive: true });
  }
  const alertFile = path.join(
    alertDir,
    `alert-${Date.now()}-${anomaly.trackingNumber}.json`
  );
  fs.writeFileSync(
    alertFile,
    JSON.stringify(
      {
        channel: 'logistics-alerts',
        message: message,
        severity: anomaly.severity,
        trackingNumber: anomaly.trackingNumber,
        type: anomaly.type,
        createdAt: new Date().toISOString(),
      },
      null,
      2
    ),
    'utf-8'
  );

  console.log(`[anomaly-detector] Discord alert queued: ${anomaly.trackingNumber} (${anomaly.type})`);
}

/**
 * Send a single anomaly alert via email (SMTP) to Wilson.
 *
 * @param {object} anomaly
 */
function _sendEmailAlert(anomaly) {
  const config = loadConfig();
  const emailRecipient =
    (config.anomaly.alert_channels || {}).email_recipient || 'wilson';

  const severityLabel =
    anomaly.severity === 'critical' ? 'CRITICAL' : 'WARNING';
  const subject = `[${severityLabel}] 物流异常: ${anomaly.trackingNumber} (${anomaly.type})`;

  const html = _buildAlertEmailHtml(anomaly);

  // Write HTML to temp file
  const tmpDir = path.resolve(__dirname, '../data/tmp');
  if (!fs.existsSync(tmpDir)) {
    fs.mkdirSync(tmpDir, { recursive: true });
  }
  const tmpFile = path.join(tmpDir, `alert-${Date.now()}.html`);

  try {
    fs.writeFileSync(tmpFile, html, 'utf-8');

    const args = [
      SMTP_SCRIPT,
      'send',
      '--to',
      emailRecipient,
      '--subject',
      subject,
      '--html-file',
      tmpFile,
    ];

    execFileSync('node', args, {
      encoding: 'utf-8',
      timeout: 30000,
      env: process.env,
    });

    console.log(
      `[anomaly-detector] Email alert sent to ${emailRecipient}: ${anomaly.trackingNumber}`
    );
  } finally {
    try {
      fs.unlinkSync(tmpFile);
    } catch {
      /* ignore */
    }
  }
}

/**
 * Build HTML email body for an anomaly alert.
 * @param {object} anomaly
 * @returns {string} HTML
 */
function _buildAlertEmailHtml(anomaly) {
  const severityColor =
    anomaly.severity === 'critical' ? '#dc2626' : '#ea580c';
  const severityLabel =
    anomaly.severity === 'critical' ? 'CRITICAL' : 'WARNING';
  const typeLabels = {
    no_update: 'No Tracking Update',
    customs_hold: 'Customs Hold',
    return_detected: 'Return Detected',
    lost_suspect: 'Suspected Lost',
  };
  const typeLabel = typeLabels[anomaly.type] || anomaly.type;

  const trackingLink = `https://t.17track.net/en#nums=${encodeURIComponent(anomaly.trackingNumber)}`;

  return `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { font-family: Arial, sans-serif; color: #333; line-height: 1.6; margin: 0; padding: 0; }
  .container { max-width: 600px; margin: 0 auto; padding: 20px; }
  .header { background-color: ${severityColor}; color: #fff; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }
  .header h1 { margin: 0; font-size: 20px; }
  .content { background-color: #f9fafb; padding: 24px; border: 1px solid #e5e7eb; }
  .alert-box { background: #fff; border: 2px solid ${severityColor}; border-radius: 8px; padding: 16px; margin: 16px 0; }
  .info-table { width: 100%; border-collapse: collapse; margin: 12px 0; }
  .info-table td { padding: 8px 12px; border-bottom: 1px solid #e5e7eb; }
  .info-table td:first-child { color: #6b7280; width: 140px; }
  .btn { display: inline-block; background: ${severityColor}; color: #fff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; margin: 12px 0; }
  .footer { text-align: center; color: #9ca3af; font-size: 12px; padding: 16px; border-top: 1px solid #e5e7eb; }
</style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>${anomaly.severity === 'critical' ? '🚨' : '⚠️'} Logistics Anomaly Alert [${severityLabel}]</h1>
    </div>
    <div class="content">
      <div class="alert-box">
        <p style="margin:0 0 8px 0; color:${severityColor}; font-weight:bold; font-size:16px;">${typeLabel}</p>
        <p style="margin:0;">${anomaly.message}</p>
      </div>

      <table class="info-table">
        <tr><td>Tracking Number</td><td><strong>${anomaly.trackingNumber}</strong></td></tr>
        <tr><td>Alert Type</td><td><strong>${typeLabel}</strong></td></tr>
        <tr><td>Severity</td><td><strong style="color:${severityColor};">${severityLabel}</strong></td></tr>
        <tr><td>Carrier</td><td>${anomaly.carrier || 'N/A'}</td></tr>
        <tr><td>Customer</td><td>${anomaly.customerName || 'N/A'}</td></tr>
        ${anomaly.daysSinceUpdate ? `<tr><td>Days Since Update</td><td><strong>${anomaly.daysSinceUpdate}</strong> days</td></tr>` : ''}
      </table>

      <p style="text-align:center;">
        <a href="${trackingLink}" class="btn">Check on 17Track</a>
      </p>

      <p style="color:#6b7280; font-size:13px;">
        This is an automated alert from the logistics-tracker skill.
        Please review and take appropriate action.
      </p>
    </div>
    <div class="footer">
      <p>Farreach Electronic Co., Ltd</p>
      <p>Generated at ${new Date().toISOString()}</p>
    </div>
  </div>
</body>
</html>`;
}

// ---------------------------------------------------------------------------
// Order-tracker integration: sync shipped orders
// ---------------------------------------------------------------------------

/**
 * Read shipped orders from order-tracker and create tracking tasks
 * in shipment-store for orders not yet tracked.
 *
 * Reads: /Users/wilson/.openclaw/workspace/skills/order-tracker/data/orders.json
 * Filters: status === 'shipped' with tracking info in status_history notes
 *
 * @param {object} [opts]
 * @param {boolean} [opts.dryRun=false]
 * @returns {{
 *   synced: number,
 *   skipped: number,
 *   errors: string[],
 *   details: object[]
 * }}
 */
function syncShippedOrders(opts) {
  opts = opts || {};
  const result = { synced: 0, skipped: 0, errors: [], details: [] };

  // Load order-tracker orders
  let ordersData;
  try {
    if (!fs.existsSync(ORDER_TRACKER_ORDERS_PATH)) {
      console.log('[anomaly-detector] order-tracker orders.json not found, skipping sync');
      return result;
    }
    const raw = fs.readFileSync(ORDER_TRACKER_ORDERS_PATH, 'utf-8');
    ordersData = JSON.parse(raw);
  } catch (err) {
    result.errors.push(`Failed to read order-tracker data: ${err.message}`);
    return result;
  }

  const orders = ordersData.orders || [];
  const shippedOrders = orders.filter((o) => o.status === 'shipped');

  if (shippedOrders.length === 0) {
    console.log('[anomaly-detector] No shipped orders in order-tracker');
    return result;
  }

  for (const order of shippedOrders) {
    const orderId = order.order_id;
    const trackingInfo = _extractTrackingFromOrder(order);

    if (!trackingInfo.trackingNumber) {
      result.skipped++;
      result.details.push({
        orderId,
        status: 'skipped',
        reason: 'No tracking number found in order notes',
      });
      continue;
    }

    // Check if already tracked
    if (shipmentStore.hasShipment(trackingInfo.trackingNumber)) {
      result.skipped++;
      result.details.push({
        orderId,
        trackingNumber: trackingInfo.trackingNumber,
        status: 'skipped',
        reason: 'Already tracked in shipment-store',
      });
      continue;
    }

    // Create shipment record
    if (opts.dryRun) {
      console.log(
        `[anomaly-detector][DRY-RUN] Would create shipment for order ${orderId}: ${trackingInfo.trackingNumber}`
      );
      result.synced++;
      result.details.push({
        orderId,
        trackingNumber: trackingInfo.trackingNumber,
        status: 'dry-run',
      });
      continue;
    }

    try {
      shipmentStore.upsertShipment({
        trackingNumber: trackingInfo.trackingNumber,
        carrier: trackingInfo.carrier || null,
        orderId: orderId,
        customerName: order.customer_name || null,
        customerEmail: order.customer_email || null,
        status: 'in_transit',
        shippedAt: _getShippedTimestamp(order),
        metadata: {
          source: 'order-tracker-sync',
          syncedAt: new Date().toISOString(),
          customerCompany: order.customer_company || null,
          eta: trackingInfo.eta || null,
        },
      });

      // Transition from initial pending_shipment to in_transit
      const shipment = shipmentStore.getShipment(trackingInfo.trackingNumber);
      if (shipment && shipment.status === 'pending_shipment') {
        shipmentStore.transitionStatus(
          trackingInfo.trackingNumber,
          'in_transit',
          { reason: 'Synced from order-tracker (shipped)' }
        );
      }

      result.synced++;
      result.details.push({
        orderId,
        trackingNumber: trackingInfo.trackingNumber,
        carrier: trackingInfo.carrier,
        status: 'created',
      });

      console.log(
        `[anomaly-detector] Created tracking for order ${orderId}: ${trackingInfo.trackingNumber} (${trackingInfo.carrier || 'auto'})`
      );
    } catch (err) {
      result.errors.push(`Order ${orderId}: ${err.message}`);
      result.details.push({
        orderId,
        trackingNumber: trackingInfo.trackingNumber,
        status: 'error',
        error: err.message,
      });
    }
  }

  return result;
}

/**
 * Extract tracking number and carrier from an order's status_history notes.
 * Supports common patterns:
 *  - "DHL Express, 单号: 1234567890"
 *  - "已发货，DHL 快递"
 *  - "Tracking: SF1234567890123"
 *
 * @param {object} order
 * @returns {{ trackingNumber: string|null, carrier: string|null, eta: string|null }}
 */
function _extractTrackingFromOrder(order) {
  const result = { trackingNumber: null, carrier: null, eta: null };

  // Collect all notes from shipped status entries
  const history = order.status_history || [];
  const shippedEntries = history.filter(
    (h) => h.status === 'shipped' || h.status === 'ready_to_ship'
  );

  let allNotes = '';
  for (const entry of shippedEntries) {
    if (entry.notes) allNotes += ' ' + entry.notes;
  }
  if (order.notes) allNotes += ' ' + order.notes;
  if (order.shipping_notes) allNotes += ' ' + order.shipping_notes;

  if (!allNotes.trim()) return result;

  // Extract carrier
  const carrierPatterns = [
    { regex: /\b(DHL)\b/i, code: 'dhl' },
    { regex: /\b(FedEx)\b/i, code: 'fedex' },
    { regex: /\b(UPS)\b/i, code: 'ups' },
    { regex: /\b(SF|顺丰)\b/i, code: 'sf' },
    { regex: /\b(EMS)\b/i, code: 'ems' },
    { regex: /\b(Yanwen|燕文)\b/i, code: 'yanwen' },
    { regex: /\b(4PX)\b/i, code: '4px' },
    { regex: /\b(CNE)\b/i, code: 'cne' },
  ];

  for (const cp of carrierPatterns) {
    if (cp.regex.test(allNotes)) {
      result.carrier = cp.code;
      break;
    }
  }

  // Extract tracking number patterns
  const trackingPatterns = [
    // Explicit labels: "单号:", "Tracking:", "运单号:"
    /(?:单号|tracking|运单号|tracking\s*(?:no|number|#))\s*[:：]\s*([A-Z0-9]{8,30})/i,
    // DHL: 10-11 digits
    /\b(\d{10,11})\b/,
    // FedEx: 12-22 digits
    /\b(\d{12,22})\b/,
    // UPS: 1Z...
    /\b(1Z[A-Z0-9]{16})\b/,
    // SF: SF + 13 digits
    /\b(SF\d{13})\b/i,
    // EMS: 2 letters + 9 digits + 2 letters
    /\b([A-Z]{2}\d{9}[A-Z]{2})\b/,
  ];

  for (const tp of trackingPatterns) {
    const match = allNotes.match(tp);
    if (match && match[1]) {
      result.trackingNumber = match[1].toUpperCase();
      break;
    }
  }

  // Extract ETA
  const etaMatch = allNotes.match(
    /(?:ETA|预计到达|到达时间)\s*[:：]?\s*(\d{1,2}月\d{1,2}日|\d{4}-\d{2}-\d{2})/i
  );
  if (etaMatch) {
    result.eta = etaMatch[1];
  }

  return result;
}

/**
 * Get the timestamp when an order was shipped from status_history.
 * @param {object} order
 * @returns {string|null} ISO timestamp
 */
function _getShippedTimestamp(order) {
  const history = order.status_history || [];
  for (let i = history.length - 1; i >= 0; i--) {
    if (history[i].status === 'shipped') {
      return history[i].changed_at || null;
    }
  }
  return order.updated_at || null;
}

// ---------------------------------------------------------------------------
// Full detection cycle
// ---------------------------------------------------------------------------

/**
 * Run the complete anomaly detection cycle:
 *  1. Sync shipped orders from order-tracker
 *  2. Load all active shipments
 *  3. Run anomaly detection (no-update, customs, return, lost)
 *  4. Send alerts (Discord + email, with retry)
 *
 * @param {object} [opts]
 * @param {boolean} [opts.dryRun=false]
 * @param {boolean} [opts.skipSync=false] - Skip order-tracker sync
 * @param {boolean} [opts.skipAlerts=false] - Skip alert sending
 * @param {boolean} [opts.autoTransition=true]
 * @returns {Promise<{
 *   sync: object,
 *   detection: object,
 *   alerts: object,
 *   summary: string
 * }>}
 */
async function runFullDetection(opts) {
  opts = opts || {};
  const dryRun = opts.dryRun || false;

  console.log(
    `[anomaly-detector] Starting full detection (dryRun=${dryRun})`
  );

  // Step 1: Sync shipped orders
  let syncResult = { synced: 0, skipped: 0, errors: [] };
  if (!opts.skipSync) {
    syncResult = syncShippedOrders({ dryRun });
    console.log(
      `[anomaly-detector] Order sync: ${syncResult.synced} synced, ${syncResult.skipped} skipped`
    );
  }

  // Step 2: Load active shipments
  const config = loadConfig();
  const terminalStates = (config.state_machine || {}).terminal_states || [
    'delivered',
    'returned',
    'lost',
  ];
  const allShipments = shipmentStore.getAllShipments();
  const activeShipments = [];
  for (const [tn, shipment] of Object.entries(allShipments)) {
    if (!terminalStates.includes(shipment.status)) {
      activeShipments.push({ ...shipment, tracking_number: tn, trackingNumber: tn });
    }
  }

  console.log(`[anomaly-detector] Active shipments: ${activeShipments.length}`);

  // Step 3: Detect anomalies
  const detectionResult = detectAnomalies(activeShipments, {
    dryRun,
    autoTransition: opts.autoTransition !== false,
  });
  console.log(
    `[anomaly-detector] Anomalies found: ${detectionResult.anomalies.length}, transitions: ${detectionResult.transitioned.length}`
  );

  // Step 4: Send alerts
  let alertResult = { sent: 0, skipped: 0, failed: 0, details: [] };
  if (!opts.skipAlerts && detectionResult.anomalies.length > 0) {
    alertResult = await sendAnomalyAlerts(detectionResult.anomalies, { dryRun });
    console.log(
      `[anomaly-detector] Alerts: ${alertResult.sent} sent, ${alertResult.skipped} skipped, ${alertResult.failed} failed`
    );
  }

  // Build summary
  const summary = _buildSummary(syncResult, detectionResult, alertResult);

  return {
    sync: syncResult,
    detection: detectionResult,
    alerts: alertResult,
    summary,
  };
}

/**
 * Build a human-readable summary.
 * @param {object} sync
 * @param {object} detection
 * @param {object} alerts
 * @returns {string}
 */
function _buildSummary(sync, detection, alerts) {
  const lines = [];
  lines.push('🔍 Anomaly Detection Report');
  lines.push('');

  if (sync.synced > 0 || sync.errors.length > 0) {
    lines.push(`Order Sync: ${sync.synced} new, ${sync.skipped} existing`);
    if (sync.errors.length > 0) {
      lines.push(`  Sync errors: ${sync.errors.join('; ')}`);
    }
  }

  lines.push(`Checked: ${detection.checked} active shipments`);
  lines.push(`Anomalies: ${detection.anomalies.length}`);

  if (detection.anomalies.length > 0) {
    const byType = {};
    for (const a of detection.anomalies) {
      byType[a.type] = (byType[a.type] || 0) + 1;
    }
    for (const [type, count] of Object.entries(byType)) {
      lines.push(`  ${type}: ${count}`);
    }
  }

  if (detection.transitioned.length > 0) {
    lines.push(`Auto-transitioned: ${detection.transitioned.length}`);
    for (const t of detection.transitioned) {
      lines.push(`  ${t.trackingNumber}: ${t.from} → ${t.to}`);
    }
  }

  if (alerts.sent > 0 || alerts.failed > 0) {
    lines.push(
      `Alerts: ${alerts.sent} sent, ${alerts.skipped} deduped, ${alerts.failed} failed`
    );
  }

  return lines.join('\n');
}

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

/**
 * Calculate days since the last tracking event for a shipment.
 * @param {object} shipment
 * @returns {number}
 */
function _daysSinceLastEvent(shipment) {
  const events = shipment.events || [];
  let lastTime;

  if (events.length > 0) {
    lastTime = new Date(
      events[events.length - 1].timestamp
    ).getTime();
  } else {
    lastTime = new Date(
      shipment.updatedAt || shipment.createdAt || shipment.updated_at || shipment.created_at
    ).getTime();
  }

  return Math.floor((Date.now() - lastTime) / (24 * 60 * 60 * 1000));
}

/**
 * Find when a shipment entered customs_clearance status.
 * @param {object} shipment
 * @returns {number|null} timestamp in ms
 */
function _findCustomsEntryTime(shipment) {
  const history = shipment.statusHistory || shipment.status_history || [];
  for (let i = history.length - 1; i >= 0; i--) {
    if (history[i].to === 'customs_clearance') {
      return new Date(history[i].at || history[i].changed_at).getTime();
    }
  }
  return null;
}

// ---------------------------------------------------------------------------
// CLI entry point
// ---------------------------------------------------------------------------

if (require.main === module) {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run') || args.includes('-n');
  const skipSync = args.includes('--skip-sync');
  const skipAlerts = args.includes('--skip-alerts');

  runFullDetection({ dryRun, skipSync, skipAlerts })
    .then((result) => {
      console.log('\n' + result.summary);
      process.exit(0);
    })
    .catch((err) => {
      console.error('[anomaly-detector] Fatal error:', err);
      process.exit(1);
    });
}

// ---------------------------------------------------------------------------
// Module exports
// ---------------------------------------------------------------------------

module.exports = {
  // Individual detection functions
  detectNoUpdateAnomaly,
  detectCustomsHoldAnomaly,
  detectReturnAnomaly,
  detectLostAnomaly,

  // Batch detection
  detectAnomalies,

  // Alert sending
  sendAnomalyAlerts,

  // Order-tracker integration
  syncShippedOrders,

  // Full cycle
  runFullDetection,

  // Retry utility
  withRetry,

  // Config
  loadConfig,
  reloadConfig,

  // Internal (exposed for testing)
  _loadAlertHistory,
  _saveAlertHistory,
  _isAlertedToday,
  _recordAlert,
  _sendDiscordAlert,
  _sendEmailAlert,
  _buildAlertEmailHtml,
  _extractTrackingFromOrder,
  _getShippedTimestamp,
  _daysSinceLastEvent,
  _findCustomsEntryTime,
  _buildSummary,
};
