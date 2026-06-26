/**
 * scheduler.js - 物流跟踪主调度器
 *
 * 功能：
 *  - runScheduledCycle(opts)     执行一次完整调度周期
 *  - getSchedulerStatus()        获取调度器运行状态
 *  - planQuotaBudget()           规划每日配额预算
 *  - buildCycleReport(result)    生成调度周期报告
 *
 * 完整流程：
 *  1. 加载所有活跃运单
 *  2. 按运单阶段分组 + 优先级排序
 *  3. 配额预算检查 + 降级策略
 *  4. 批量查询 17Track API
 *  5. 更新运单状态（状态机流转）
 *  6. 异常检测（超时无更新、清关滞留等）
 *  7. 客户通知（发货/签收/opt-in 事件）
 *  8. 写入调度历史
 *
 * 集成模块：
 *  - tracking-api.js     (API 查询 + 智能刷新 + 配额)
 *  - shipment-store.js   (状态管理 + 事件去重 + 状态机)
 *  - customer-notify.js  (通知决策 + 邮件发送 + 幂等)
 *
 * 配置文件：../config/logistics-config.json
 *
 * @module scheduler
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ---------------------------------------------------------------------------
// Module imports
// ---------------------------------------------------------------------------

const trackingApi = require('./tracking-api');
const shipmentStore = require('./shipment-store');
const customerNotify = require('./customer-notify');

// ---------------------------------------------------------------------------
// Paths & Constants
// ---------------------------------------------------------------------------

const CONFIG_PATH = path.resolve(__dirname, '../config/logistics-config.json');
const SCHEDULER_STATE_PATH = path.resolve(__dirname, '../data/scheduler-state.json');
const SCHEDULER_LOG_DIR = path.resolve(__dirname, '../data/scheduler-logs');

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
// Scheduler state persistence
// ---------------------------------------------------------------------------

/**
 * Ensure a directory exists.
 * @param {string} dirPath
 */
function _ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

/**
 * Load scheduler state from disk.
 * @returns {object} { lastRunAt, lastRunResult, totalRuns, totalApiCalls, ... }
 */
function _loadState() {
  if (!fs.existsSync(SCHEDULER_STATE_PATH)) {
    return {
      lastRunAt: null,
      lastRunResult: null,
      totalRuns: 0,
      totalApiCalls: 0,
      totalEventsProcessed: 0,
      totalNotificationsSent: 0,
      consecutiveErrors: 0
    };
  }
  try {
    return JSON.parse(fs.readFileSync(SCHEDULER_STATE_PATH, 'utf-8'));
  } catch {
    return {
      lastRunAt: null,
      lastRunResult: null,
      totalRuns: 0,
      totalApiCalls: 0,
      totalEventsProcessed: 0,
      totalNotificationsSent: 0,
      consecutiveErrors: 0
    };
  }
}

/**
 * Save scheduler state with atomic write.
 * @param {object} state
 */
function _saveState(state) {
  _ensureDir(path.dirname(SCHEDULER_STATE_PATH));
  const tmp = SCHEDULER_STATE_PATH + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(state, null, 2), 'utf-8');
  fs.renameSync(tmp, SCHEDULER_STATE_PATH);
}

/**
 * Write a scheduler cycle log entry.
 * @param {object} report
 */
function _writeCycleLog(report) {
  _ensureDir(SCHEDULER_LOG_DIR);
  const ts = new Date().toISOString().replace(/[:.]/g, '-');
  const logFile = path.join(SCHEDULER_LOG_DIR, `cycle-${ts}.json`);
  fs.writeFileSync(logFile, JSON.stringify(report, null, 2), 'utf-8');

  // Prune old logs (keep last 50)
  try {
    const files = fs.readdirSync(SCHEDULER_LOG_DIR)
      .filter(f => f.startsWith('cycle-') && f.endsWith('.json'))
      .sort();
    if (files.length > 50) {
      const toDelete = files.slice(0, files.length - 50);
      for (const f of toDelete) {
        fs.unlinkSync(path.join(SCHEDULER_LOG_DIR, f));
      }
    }
  } catch { /* ignore pruning errors */ }
}

// ---------------------------------------------------------------------------
// Quota budget planning
// ---------------------------------------------------------------------------

/**
 * Plan how to distribute the remaining daily quota across refresh stages.
 * Returns a budget object with max API calls per stage.
 *
 * Strategy:
 *  - near_delivery + exception get priority allocation (40% of remaining)
 *  - new_shipment gets 35%
 *  - in_transit gets 25%
 *  - If total shipments in a stage are fewer than allocation, surplus is redistributed
 *
 * @param {object} [opts]
 * @param {object[]} [opts.shipments] - Pre-loaded shipments (avoids re-loading)
 * @returns {{
 *   totalRemaining: number,
 *   allocation: { [stage]: { maxCalls: number, shipmentCount: number } },
 *   quotaStatus: object,
 *   degraded: boolean
 * }}
 */
function planQuotaBudget(opts) {
  opts = opts || {};
  const config = loadConfig();
  const batchSize = config.api.primary.batch_size || 40;
  const quotaStatus = trackingApi.getQuotaStatus();

  const allShipments = opts.shipments || _getAllActiveShipments();
  const { groups } = trackingApi.filterForRefresh(allShipments);

  const degraded = quotaStatus.level === 'exhausted';
  const remaining = quotaStatus.remaining;

  // Weights per stage (proportional allocation)
  const weights = {
    near_delivery: 0.25,
    exception: 0.15,
    new_shipment: 0.35,
    in_transit: 0.25
  };

  const allocation = {};
  let surplus = 0;

  // First pass: compute base allocation
  for (const [stage, weight] of Object.entries(weights)) {
    const stageNums = groups[stage] || [];
    const neededCalls = Math.ceil(stageNums.length / batchSize);
    const baseCalls = Math.floor(remaining * weight);
    const actualCalls = Math.min(baseCalls, neededCalls);
    surplus += baseCalls - actualCalls;

    allocation[stage] = {
      maxCalls: actualCalls,
      shipmentCount: stageNums.length,
      neededCalls: neededCalls,
      numbers: stageNums
    };
  }

  // Second pass: redistribute surplus to stages that need more
  if (surplus > 0) {
    const priorityOrder = ['near_delivery', 'exception', 'new_shipment', 'in_transit'];
    for (const stage of priorityOrder) {
      if (surplus <= 0) break;
      const alloc = allocation[stage];
      if (!alloc) continue;
      const deficit = alloc.neededCalls - alloc.maxCalls;
      if (deficit > 0) {
        const give = Math.min(deficit, surplus);
        alloc.maxCalls += give;
        surplus -= give;
      }
    }
  }

  // Apply degradation: pause non-critical stages
  if (degraded) {
    const keepActive = (config.quota.pause_non_critical_rules || {}).keep_active || ['near_delivery', 'exception'];
    for (const stage of Object.keys(allocation)) {
      if (!keepActive.includes(stage)) {
        allocation[stage].maxCalls = 0;
        allocation[stage].paused = true;
      }
    }
  }

  return {
    totalRemaining: remaining,
    allocation,
    quotaStatus,
    degraded
  };
}

// ---------------------------------------------------------------------------
// Active shipments helper
// ---------------------------------------------------------------------------

/**
 * Get all non-terminal shipments from the store.
 * Attaches tracking_number as a top-level field for module compatibility.
 * @returns {object[]}
 */
function _getAllActiveShipments() {
  const config = loadConfig();
  const terminalStates = (config.state_machine && config.state_machine.terminal_states) || ['delivered', 'returned', 'lost'];
  const all = shipmentStore.getAllShipments();
  const active = [];

  for (const [tn, shipment] of Object.entries(all)) {
    if (!terminalStates.includes(shipment.status)) {
      active.push({
        ...shipment,
        tracking_number: tn
      });
    }
  }
  return active;
}

// ---------------------------------------------------------------------------
// Status mapping (17Track status code to internal state)
// ---------------------------------------------------------------------------

/**
 * Map a 17Track API status to an internal state_machine status.
 * Uses config.state_machine.status_mapping.
 * @param {string} apiStatus - 17Track status string (e.g., "InTransit", "Delivered")
 * @returns {string|null} - Internal status or null if no mapping
 */
function _mapApiStatus(apiStatus) {
  if (!apiStatus) return null;
  const config = loadConfig();
  const mapping = (config.state_machine.status_mapping || {}).mapping || {};
  return mapping[apiStatus] || null;
}

/**
 * Infer internal status from tracking events (keyword-based).
 * Examines the latest event description for stage-related keywords.
 * @param {object[]} events - Array of { description, status, ... }
 * @returns {string|null}
 */
function _inferStatusFromEvents(events) {
  if (!events || events.length === 0) return null;

  const latest = events[0]; // Events are typically newest-first from 17Track
  const desc = (latest.description || '').toLowerCase();

  if (desc.includes('delivered') || desc.includes('签收')) return 'delivered';
  if (desc.includes('out for delivery') || desc.includes('派送中')) return 'near_delivery';
  if (desc.includes('customs') || desc.includes('清关') || desc.includes('海关')) return 'customs_clearance';
  if (desc.includes('returned') || desc.includes('return to sender') || desc.includes('退回')) return 'returning';
  if (desc.includes('refused') || desc.includes('拒收')) return 'refused';

  return null;
}

// ---------------------------------------------------------------------------
// Core: process a single shipment's API response
// ---------------------------------------------------------------------------

/**
 * Process the tracking API response for a single shipment.
 * Updates events, transitions status, and queues notifications.
 *
 * @param {string} trackingNumber
 * @param {object[]} apiEvents - Events from 17Track API response
 * @param {object} [opts]
 * @param {boolean} [opts.dryRun]
 * @returns {{
 *   trackingNumber: string,
 *   eventsAdded: number,
 *   eventsSkipped: number,
 *   statusChanged: boolean,
 *   previousStatus: string,
 *   newStatus: string,
 *   notificationQueued: string|null,
 *   error: string|null
 * }}
 */
function _processShipmentResponse(trackingNumber, apiEvents, opts) {
  opts = opts || {};

  const result = {
    trackingNumber,
    eventsAdded: 0,
    eventsSkipped: 0,
    statusChanged: false,
    previousStatus: null,
    newStatus: null,
    notificationQueued: null,
    error: null
  };

  try {
    const shipment = shipmentStore.getShipment(trackingNumber);
    if (!shipment) {
      result.error = `Shipment not found: ${trackingNumber}`;
      return result;
    }

    result.previousStatus = shipment.status;

    // 1. Add events to store (with dedup)
    if (apiEvents && apiEvents.length > 0) {
      const storeEvents = apiEvents.map(e => ({
        timestamp: e.date || new Date().toISOString(),
        description: e.description || '',
        location: e.location || '',
        status: e.status || null
      }));

      const addResult = shipmentStore.addEvents(trackingNumber, storeEvents, { dryRun: opts.dryRun });
      result.eventsAdded = addResult.added;
      result.eventsSkipped = addResult.skipped;
    }

    // 2. Update last_refreshed_at and last_event_description
    const updatedShipment = shipmentStore.getShipment(trackingNumber);
    if (updatedShipment) {
      shipmentStore.upsertShipment({
        trackingNumber,
        metadata: {
          last_refreshed_at: new Date().toISOString(),
          last_event_description: apiEvents && apiEvents.length > 0
            ? apiEvents[0].description || ''
            : (updatedShipment.metadata || {}).last_event_description || ''
        }
      }, { dryRun: opts.dryRun });
    }

    // 3. Determine if status should change
    const inferredStatus = _inferStatusFromEvents(apiEvents);
    if (inferredStatus && inferredStatus !== shipment.status) {
      const transResult = shipmentStore.transitionStatus(trackingNumber, inferredStatus, {
        reason: `Auto-inferred from tracking events`,
        dryRun: opts.dryRun
      });

      if (transResult.success) {
        result.statusChanged = true;
        result.newStatus = inferredStatus;

        // 4. Queue notification based on new status
        if (inferredStatus === 'delivered') {
          result.notificationQueued = 'delivered';
        }
      }
      // If transition failed (invalid state path), log but don't error
      if (!transResult.success && transResult.error) {
        console.log(`[scheduler] Status transition skipped for ${trackingNumber}: ${transResult.error}`);
      }
    }

    // Check for shipped notification (in_transit and not yet notified)
    if (shipment.status === 'pending_shipment' && result.newStatus === 'in_transit') {
      result.notificationQueued = 'shipped';
    }

  } catch (err) {
    result.error = err.message;
  }

  return result;
}

// ---------------------------------------------------------------------------
// Core: anomaly detection pass
// ---------------------------------------------------------------------------

/**
 * Run anomaly detection on all active shipments.
 * Checks: no-update threshold, customs hold, return/lost keywords.
 *
 * @param {object[]} activeShipments
 * @param {object} [opts]
 * @param {boolean} [opts.dryRun]
 * @returns {{ anomalies: object[] }}
 */
function _runAnomalyDetection(activeShipments, opts) {
  opts = opts || {};
  const config = loadConfig();
  const anomalyConf = config.anomaly || {};
  const noUpdateDays = anomalyConf.no_update_threshold_days || 7;
  const customsHoldDays = anomalyConf.customs_hold_threshold_days || 5;
  const lostDays = (anomalyConf.lost_detection || {}).no_update_days || 30;

  const anomalies = [];
  const now = Date.now();

  for (const shipment of activeShipments) {
    const tn = shipment.tracking_number;
    const events = shipment.events || [];
    const lastEventTime = events.length > 0
      ? new Date(events[events.length - 1].timestamp).getTime()
      : new Date(shipment.updatedAt || shipment.createdAt).getTime();

    const daysSinceUpdate = Math.floor((now - lastEventTime) / (24 * 60 * 60 * 1000));

    // 1. No update threshold
    if (daysSinceUpdate >= noUpdateDays && daysSinceUpdate < lostDays) {
      const template = (anomalyConf.alert_templates || {}).no_update || '';
      anomalies.push({
        type: 'no_update',
        trackingNumber: tn,
        daysSinceUpdate,
        severity: 'warning',
        message: template
          .replace('{tracking_number}', tn)
          .replace('{customer_name}', shipment.customerName || 'Unknown')
          .replace('{days}', String(daysSinceUpdate))
      });
    }

    // 2. Lost detection (extended no-update)
    if (daysSinceUpdate >= lostDays && shipment.status !== 'lost') {
      const template = (anomalyConf.alert_templates || {}).lost || '';
      anomalies.push({
        type: 'lost_suspect',
        trackingNumber: tn,
        daysSinceUpdate,
        severity: 'critical',
        message: template
          .replace('{tracking_number}', tn)
          .replace('{days}', String(daysSinceUpdate))
      });

      // Auto-transition to lost
      if (!opts.dryRun) {
        shipmentStore.transitionStatus(tn, 'lost', {
          reason: `No update for ${daysSinceUpdate} days (auto-detected)`,
          force: true
        });
      }
    }

    // 3. Customs hold detection
    if (shipment.status === 'customs_clearance') {
      const customsEntryTime = _findCustomsEntryTime(shipment);
      if (customsEntryTime) {
        const customsDays = Math.floor((now - customsEntryTime) / (24 * 60 * 60 * 1000));
        if (customsDays >= customsHoldDays) {
          const template = (anomalyConf.alert_templates || {}).customs_hold || '';
          anomalies.push({
            type: 'customs_hold',
            trackingNumber: tn,
            daysSinceUpdate: customsDays,
            severity: 'warning',
            message: template
              .replace('{tracking_number}', tn)
              .replace('{days}', String(customsDays))
          });
        }
      }
    }

    // 4. Return detection (keyword-based in recent events)
    const returnConf = anomalyConf.return_detection || {};
    if (returnConf.enabled && shipment.status !== 'returning' && shipment.status !== 'returned') {
      const keywords = (returnConf.keywords || []).map(k => k.toLowerCase());
      const recentEvents = events.slice(-5);
      for (const evt of recentEvents) {
        const desc = (evt.description || '').toLowerCase();
        if (keywords.some(kw => desc.includes(kw))) {
          const template = (anomalyConf.alert_templates || {}).returned || '';
          anomalies.push({
            type: 'return_detected',
            trackingNumber: tn,
            severity: 'warning',
            message: template.replace('{tracking_number}', tn)
          });

          if (!opts.dryRun) {
            shipmentStore.transitionStatus(tn, 'returning', {
              reason: `Return detected in event: "${evt.description}"`,
              force: false
            });
          }
          break;
        }
      }
    }
  }

  return { anomalies };
}

/**
 * Find when a shipment entered customs_clearance status.
 * @param {object} shipment
 * @returns {number|null} timestamp in ms, or null
 */
function _findCustomsEntryTime(shipment) {
  const history = shipment.statusHistory || [];
  for (let i = history.length - 1; i >= 0; i--) {
    if (history[i].to === 'customs_clearance') {
      return new Date(history[i].at).getTime();
    }
  }
  return null;
}

// ---------------------------------------------------------------------------
// Core: notification pass
// ---------------------------------------------------------------------------

/**
 * Send notifications for shipments that have pending notification triggers.
 *
 * @param {object[]} processResults - Results from _processShipmentResponse calls
 * @param {object} [opts]
 * @param {boolean} [opts.dryRun]
 * @returns {{ sent: number, skipped: number, failed: number, details: object[] }}
 */
function _runNotifications(processResults, opts) {
  opts = opts || {};
  const stats = { sent: 0, skipped: 0, failed: 0, details: [] };

  for (const pr of processResults) {
    if (!pr.notificationQueued) continue;

    const shipment = shipmentStore.getShipment(pr.trackingNumber);
    if (!shipment) continue;

    // Adapt shipment fields to customer-notify expected format
    const notifyShipment = {
      tracking_number: pr.trackingNumber,
      customer_email: shipment.customerEmail,
      customer_name: shipment.customerName,
      carrier_name: shipment.carrier,
      order_id: shipment.orderId,
      status: shipment.status,
      notification_preferences: (shipment.metadata || {}).notification_preferences || {}
    };

    const result = customerNotify.sendNotification(
      notifyShipment,
      pr.notificationQueued,
      {},
      { dryRun: opts.dryRun }
    );

    stats.details.push({
      trackingNumber: pr.trackingNumber,
      eventType: pr.notificationQueued,
      ...result
    });

    if (result.sent) {
      stats.sent++;
    } else if (result.reason && result.reason.toLowerCase().includes('fail')) {
      stats.failed++;
    } else {
      stats.skipped++;
    }
  }

  return stats;
}

// ---------------------------------------------------------------------------
// Main entry: runScheduledCycle
// ---------------------------------------------------------------------------

/**
 * Execute a complete scheduler cycle.
 *
 * Flow:
 *  1. Load active shipments
 *  2. Plan quota budget
 *  3. Build refresh queue (prioritized by stage)
 *  4. Batch query 17Track API
 *  5. Process responses (events + status updates)
 *  6. Run anomaly detection
 *  7. Send notifications
 *  8. Save state + write cycle log
 *
 * @param {object} [opts]
 * @param {boolean} [opts.dryRun=false]  Skip API calls and writes
 * @returns {Promise<{
 *   success: boolean,
 *   startedAt: string,
 *   completedAt: string,
 *   dryRun: boolean,
 *   shipments: { total: number, active: number, refreshed: number },
 *   api: { callsMade: number, quotaBefore: object, quotaAfter: object },
 *   events: { added: number, skipped: number },
 *   statusChanges: { changed: number, details: object[] },
 *   anomalies: { count: number, details: object[] },
 *   notifications: { sent: number, skipped: number, failed: number },
 *   errors: string[]
 * }>}
 */
async function runScheduledCycle(opts) {
  opts = opts || {};
  const dryRun = opts.dryRun || false;
  const startedAt = new Date().toISOString();
  const errors = [];

  console.log(`[scheduler] Starting cycle at ${startedAt} (dryRun=${dryRun})`);

  // --------------- Step 1: Load active shipments ---------------
  const activeShipments = _getAllActiveShipments();
  const totalShipments = shipmentStore.getShipmentCount();
  console.log(`[scheduler] Active shipments: ${activeShipments.length} / ${totalShipments} total`);

  if (activeShipments.length === 0) {
    const report = _buildEmptyReport(startedAt, dryRun, totalShipments);
    if (!dryRun) {
      _updateState(report);
      _writeCycleLog(report);
    }
    console.log('[scheduler] No active shipments, cycle complete.');
    return report;
  }

  // --------------- Step 2: Plan quota budget ---------------
  const budget = planQuotaBudget({ shipments: activeShipments });
  const quotaBefore = { ...budget.quotaStatus };
  console.log(`[scheduler] Quota: ${budget.quotaStatus.used}/${budget.quotaStatus.limit} used (${budget.quotaStatus.level}), degraded=${budget.degraded}`);

  // --------------- Step 3: Build refresh queue ---------------
  const refreshQueue = trackingApi.buildRefreshQueue(activeShipments);
  const numbersToQuery = refreshQueue.numbers;
  console.log(`[scheduler] Refresh queue: ${numbersToQuery.length} numbers across ${refreshQueue.filtered.length} stage groups`);

  if (numbersToQuery.length === 0) {
    const report = _buildNoRefreshReport(startedAt, dryRun, totalShipments, activeShipments.length, quotaBefore);
    if (!dryRun) {
      _updateState(report);
      _writeCycleLog(report);
    }
    console.log('[scheduler] No shipments need refresh, cycle complete.');
    return report;
  }

  // --------------- Step 4: Batch query 17Track ---------------
  let apiResult = { accepted: [], rejected: [], events: new Map(), raw: [] };
  let callsMade = 0;

  if (!dryRun) {
    try {
      apiResult = await trackingApi.getTrackingInfo(numbersToQuery, { dryRun: false });
      const batchSize = loadConfig().api.primary.batch_size || 40;
      callsMade = Math.ceil(numbersToQuery.length / batchSize);
      console.log(`[scheduler] API query complete: ${apiResult.accepted.length} accepted, ${apiResult.rejected.length} rejected`);
    } catch (err) {
      const errMsg = `API query failed: ${err.message}`;
      errors.push(errMsg);
      console.error(`[scheduler] ${errMsg}`);
    }
  } else {
    console.log(`[scheduler][DRY-RUN] Would query ${numbersToQuery.length} numbers`);
    // Simulate dry-run: set callsMade for reporting
    const batchSize = loadConfig().api.primary.batch_size || 40;
    callsMade = Math.ceil(numbersToQuery.length / batchSize);
  }

  // --------------- Step 5: Process responses ---------------
  const processResults = [];
  let totalEventsAdded = 0;
  let totalEventsSkipped = 0;
  const statusChanges = [];

  for (const tn of numbersToQuery) {
    const events = apiResult.events.get(tn) || [];
    const pr = _processShipmentResponse(tn, events, { dryRun });
    processResults.push(pr);

    totalEventsAdded += pr.eventsAdded;
    totalEventsSkipped += pr.eventsSkipped;

    if (pr.statusChanged) {
      statusChanges.push({
        trackingNumber: tn,
        from: pr.previousStatus,
        to: pr.newStatus
      });
    }

    if (pr.error) {
      errors.push(`${tn}: ${pr.error}`);
    }
  }

  console.log(`[scheduler] Processed ${processResults.length} shipments: ${totalEventsAdded} events added, ${statusChanges.length} status changes`);

  // --------------- Step 6: Anomaly detection ---------------
  // Run on ALL active shipments (not just queried ones)
  const anomalyResult = _runAnomalyDetection(activeShipments, { dryRun });
  console.log(`[scheduler] Anomalies detected: ${anomalyResult.anomalies.length}`);

  // --------------- Step 7: Notifications ---------------
  const notifyResult = _runNotifications(processResults, { dryRun });
  console.log(`[scheduler] Notifications: ${notifyResult.sent} sent, ${notifyResult.skipped} skipped, ${notifyResult.failed} failed`);

  // --------------- Step 8: Build report & save ---------------
  const quotaAfter = trackingApi.getQuotaStatus();
  const completedAt = new Date().toISOString();

  const report = {
    success: errors.length === 0,
    startedAt,
    completedAt,
    durationMs: new Date(completedAt).getTime() - new Date(startedAt).getTime(),
    dryRun,
    shipments: {
      total: totalShipments,
      active: activeShipments.length,
      refreshed: numbersToQuery.length
    },
    api: {
      callsMade,
      quotaBefore,
      quotaAfter
    },
    events: {
      added: totalEventsAdded,
      skipped: totalEventsSkipped
    },
    statusChanges: {
      changed: statusChanges.length,
      details: statusChanges
    },
    anomalies: {
      count: anomalyResult.anomalies.length,
      details: anomalyResult.anomalies
    },
    notifications: {
      sent: notifyResult.sent,
      skipped: notifyResult.skipped,
      failed: notifyResult.failed
    },
    errors
  };

  if (!dryRun) {
    _updateState(report);
    _writeCycleLog(report);
  }

  console.log(`[scheduler] Cycle complete in ${report.durationMs}ms. Success=${report.success}`);

  return report;
}

// ---------------------------------------------------------------------------
// Report builders
// ---------------------------------------------------------------------------

/**
 * Build a report for when there are no active shipments.
 */
function _buildEmptyReport(startedAt, dryRun, totalShipments) {
  return {
    success: true,
    startedAt,
    completedAt: new Date().toISOString(),
    durationMs: 0,
    dryRun,
    shipments: { total: totalShipments, active: 0, refreshed: 0 },
    api: { callsMade: 0, quotaBefore: trackingApi.getQuotaStatus(), quotaAfter: trackingApi.getQuotaStatus() },
    events: { added: 0, skipped: 0 },
    statusChanges: { changed: 0, details: [] },
    anomalies: { count: 0, details: [] },
    notifications: { sent: 0, skipped: 0, failed: 0 },
    errors: []
  };
}

/**
 * Build a report for when no shipments need refresh.
 */
function _buildNoRefreshReport(startedAt, dryRun, totalShipments, activeCount, quotaBefore) {
  return {
    success: true,
    startedAt,
    completedAt: new Date().toISOString(),
    durationMs: 0,
    dryRun,
    shipments: { total: totalShipments, active: activeCount, refreshed: 0 },
    api: { callsMade: 0, quotaBefore, quotaAfter: trackingApi.getQuotaStatus() },
    events: { added: 0, skipped: 0 },
    statusChanges: { changed: 0, details: [] },
    anomalies: { count: 0, details: [] },
    notifications: { sent: 0, skipped: 0, failed: 0 },
    errors: []
  };
}

/**
 * Update scheduler persistent state after a cycle.
 * @param {object} report
 */
function _updateState(report) {
  const state = _loadState();
  state.lastRunAt = report.completedAt;
  state.lastRunResult = report.success ? 'success' : 'error';
  state.totalRuns = (state.totalRuns || 0) + 1;
  state.totalApiCalls = (state.totalApiCalls || 0) + report.api.callsMade;
  state.totalEventsProcessed = (state.totalEventsProcessed || 0) + report.events.added;
  state.totalNotificationsSent = (state.totalNotificationsSent || 0) + report.notifications.sent;
  state.consecutiveErrors = report.success ? 0 : (state.consecutiveErrors || 0) + 1;
  _saveState(state);
}

// ---------------------------------------------------------------------------
// Status & reporting
// ---------------------------------------------------------------------------

/**
 * Get current scheduler status.
 * @returns {{
 *   lastRunAt: string|null,
 *   lastRunResult: string|null,
 *   totalRuns: number,
 *   totalApiCalls: number,
 *   consecutiveErrors: number,
 *   quotaStatus: object,
 *   activeShipments: number,
 *   statusSummary: object
 * }}
 */
function getSchedulerStatus() {
  const state = _loadState();
  const quotaStatus = trackingApi.getQuotaStatus();
  const statusSummary = shipmentStore.getStatusSummary();
  const activeShipments = _getAllActiveShipments().length;

  return {
    ...state,
    quotaStatus,
    activeShipments,
    statusSummary
  };
}

/**
 * Build a human-readable summary from a cycle report.
 * @param {object} report - Result from runScheduledCycle()
 * @returns {string}
 */
function buildCycleReport(report) {
  const lines = [];
  lines.push(`📦 Logistics Scheduler Cycle Report`);
  lines.push(`Time: ${report.startedAt} (${report.durationMs}ms)`);
  lines.push(`Mode: ${report.dryRun ? 'DRY-RUN' : 'LIVE'}`);
  lines.push('');
  lines.push(`Shipments: ${report.shipments.active} active / ${report.shipments.total} total, ${report.shipments.refreshed} refreshed`);
  lines.push(`API: ${report.api.callsMade} calls (quota: ${report.api.quotaAfter.used}/${report.api.quotaAfter.limit})`);
  lines.push(`Events: ${report.events.added} added, ${report.events.skipped} deduped`);
  lines.push(`Status changes: ${report.statusChanges.changed}`);

  if (report.statusChanges.details.length > 0) {
    for (const sc of report.statusChanges.details) {
      lines.push(`  ${sc.trackingNumber}: ${sc.from} → ${sc.to}`);
    }
  }

  lines.push(`Anomalies: ${report.anomalies.count}`);
  if (report.anomalies.details.length > 0) {
    for (const a of report.anomalies.details) {
      lines.push(`  ${a.message}`);
    }
  }

  lines.push(`Notifications: ${report.notifications.sent} sent, ${report.notifications.skipped} skipped, ${report.notifications.failed} failed`);

  if (report.errors.length > 0) {
    lines.push('');
    lines.push(`⚠️ Errors (${report.errors.length}):`);
    for (const e of report.errors) {
      lines.push(`  ${e}`);
    }
  }

  return lines.join('\n');
}

// ---------------------------------------------------------------------------
// CLI entry point
// ---------------------------------------------------------------------------

/**
 * Run as CLI if executed directly: node scheduler.js [--dry-run]
 */
if (require.main === module) {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run') || args.includes('-n');

  runScheduledCycle({ dryRun })
    .then(report => {
      console.log('\n' + buildCycleReport(report));
      process.exit(report.success ? 0 : 1);
    })
    .catch(err => {
      console.error('[scheduler] Fatal error:', err);
      process.exit(2);
    });
}

// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------

module.exports = {
  // Main entry
  runScheduledCycle,

  // Planning & status
  planQuotaBudget,
  getSchedulerStatus,

  // Reporting
  buildCycleReport,

  // Config
  loadConfig,
  reloadConfig,

  // Internal (exposed for testing)
  _getAllActiveShipments,
  _processShipmentResponse,
  _runAnomalyDetection,
  _runNotifications,
  _mapApiStatus,
  _inferStatusFromEvents,
  _loadState,
  _saveState,
  _writeCycleLog
};
