/**
 * shipment-store.js - 物流状态管理（JSON 持久化）
 *
 * 功能：
 *  - getShipment(trackingNumber)              查询单条运单
 *  - upsertShipment(data, opts)               创建或更新运单
 *  - addEvents(trackingNumber, events, opts)   追加物流事件（eventId 去重）
 *  - transitionStatus(trackingNumber, newStatus, opts)  状态机流转
 *  - getAllShipments()                          获取全部运单
 *  - getShipmentsByStatus(status)              按状态过滤运单
 *
 * 特性：
 *  - 原子写入（write .tmp → rename）防并发损坏
 *  - 完整状态机（从 config.state_machine 读取转换规则）
 *  - 事件 eventId 去重（hash(timestamp+description)）
 *  - 赔偿流程提醒（lost / returning 自动告警）
 *  - dry-run 模式（不写入文件）
 *
 * 配置文件：../config/logistics-config.json
 *
 * @module shipment-store
 */

'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

const CONFIG_PATH = path.resolve(__dirname, '../config/logistics-config.json');

let _configCache = null;

/**
 * Load config (cached).
 * @returns {object} logistics-config
 */
function loadConfig() {
  if (_configCache) return _configCache;
  const raw = fs.readFileSync(CONFIG_PATH, 'utf-8');
  _configCache = JSON.parse(raw);
  return _configCache;
}

/**
 * Force reload config.
 * @returns {object} logistics-config
 */
function reloadConfig() {
  _configCache = null;
  return loadConfig();
}

// ---------------------------------------------------------------------------
// Storage path helpers
// ---------------------------------------------------------------------------

/**
 * Resolve the shipments data file path from config.
 * Falls back to data/shipments.json relative to the skill root.
 * @returns {string} absolute path
 */
function _resolveShipmentsPath() {
  const cfg = loadConfig();
  const rel = (cfg.storage && cfg.storage.shipments_file) || 'data/shipments.json';
  return path.resolve(__dirname, '..', rel);
}

/**
 * Ensure the directory for a file exists.
 * @param {string} filePath
 */
function _ensureDir(filePath) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

// ---------------------------------------------------------------------------
// Atomic read / write
// ---------------------------------------------------------------------------

/**
 * Load shipments store from disk.
 * Returns { shipments: { [trackingNumber]: shipmentObj } }.
 * @returns {object}
 */
function _loadStore() {
  const fp = _resolveShipmentsPath();
  if (!fs.existsSync(fp)) {
    return { shipments: {} };
  }
  try {
    const raw = fs.readFileSync(fp, 'utf-8');
    const data = JSON.parse(raw);
    if (!data.shipments || typeof data.shipments !== 'object') {
      return { shipments: {} };
    }
    return data;
  } catch {
    console.error('[shipment-store] Failed to parse shipments file, starting fresh');
    return { shipments: {} };
  }
}

/**
 * Persist the store to disk using atomic write (write .tmp → rename).
 * @param {object} store
 */
function _saveStore(store) {
  const fp = _resolveShipmentsPath();
  _ensureDir(fp);
  const tmp = fp + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(store, null, 2), 'utf-8');
  fs.renameSync(tmp, fp);
}

// ---------------------------------------------------------------------------
// Event ID generation & dedup
// ---------------------------------------------------------------------------

/**
 * Generate a deterministic eventId from timestamp + description.
 * Uses sha256 truncated to 16 hex chars for compact uniqueness.
 *
 * @param {string} timestamp
 * @param {string} description
 * @returns {string} eventId
 */
function generateEventId(timestamp, description) {
  const input = `${timestamp || ''}|${description || ''}`;
  return crypto.createHash('sha256').update(input).digest('hex').slice(0, 16);
}

/**
 * Check if an event has already been processed for a shipment.
 *
 * @param {object} shipment
 * @param {string} eventId
 * @returns {boolean}
 */
function _isEventProcessed(shipment, eventId) {
  if (!shipment.processedEventIds) return false;
  return shipment.processedEventIds.includes(eventId);
}

// ---------------------------------------------------------------------------
// State machine
// ---------------------------------------------------------------------------

/**
 * Load allowed transitions from config.state_machine.
 * Returns { [state]: [allowedNextStates] }.
 * @returns {object}
 */
function _loadTransitions() {
  const cfg = loadConfig();
  const sm = cfg.state_machine;
  if (!sm || !sm.states) {
    throw new Error('[shipment-store] config.state_machine.states is missing');
  }
  const transitions = {};
  for (const [state, def] of Object.entries(sm.states)) {
    transitions[state] = def.transitions || [];
  }
  return transitions;
}

/**
 * Validate whether a status transition is allowed.
 *
 * @param {string} currentStatus
 * @param {string} newStatus
 * @returns {{ valid: boolean, reason?: string }}
 */
function validateTransition(currentStatus, newStatus) {
  const transitions = _loadTransitions();

  if (!transitions[currentStatus]) {
    return { valid: false, reason: `Unknown current status: ${currentStatus}` };
  }

  const cfg = loadConfig();
  if (!cfg.state_machine.states[newStatus]) {
    return { valid: false, reason: `Unknown target status: ${newStatus}` };
  }

  if (cfg.state_machine.states[currentStatus].terminal) {
    return { valid: false, reason: `Current status "${currentStatus}" is terminal, no transitions allowed` };
  }

  const allowed = transitions[currentStatus];
  if (!allowed.includes(newStatus)) {
    return {
      valid: false,
      reason: `Transition "${currentStatus}" → "${newStatus}" is not allowed. Allowed: [${allowed.join(', ')}]`
    };
  }

  return { valid: true };
}

/**
 * Get the human-readable label for a status from config.
 *
 * @param {string} statusKey
 * @returns {string}
 */
function getStatusLabel(statusKey) {
  const cfg = loadConfig();
  const sm = cfg.state_machine;
  if (sm && sm.states && sm.states[statusKey]) {
    return sm.states[statusKey].label || statusKey;
  }
  return statusKey;
}

// ---------------------------------------------------------------------------
// Compensation reminder
// ---------------------------------------------------------------------------

/**
 * Check if a status triggers compensation reminder.
 * If so, returns a reminder object and logs an alert.
 *
 * @param {string} trackingNumber
 * @param {string} newStatus
 * @param {object} shipment
 * @returns {object|null} compensation reminder or null
 */
function _checkCompensation(trackingNumber, newStatus, shipment) {
  const cfg = loadConfig();
  const comp = cfg.anomaly && cfg.anomaly.compensation_reminder;
  if (!comp || !comp.enabled) return null;

  const triggerStatuses = comp.trigger_status || ['lost', 'returned'];
  // Also trigger on 'returning' per subtask requirements
  const allTriggers = [...triggerStatuses, 'returning'];

  if (!allTriggers.includes(newStatus)) return null;

  const carrier = shipment.carrier || 'unknown';
  const statusLabel = getStatusLabel(newStatus);
  const message = (comp.message || '')
    .replace('{tracking_number}', trackingNumber)
    .replace('{status_label}', statusLabel)
    .replace('{carrier}', carrier);

  const reminder = {
    triggered_at: new Date().toISOString(),
    status: newStatus,
    status_label: statusLabel,
    carrier: carrier,
    message: message
  };

  console.warn(`[shipment-store] 🚨 COMPENSATION REMINDER: ${message}`);

  return reminder;
}

// ---------------------------------------------------------------------------
// Core public functions
// ---------------------------------------------------------------------------

/**
 * Get a single shipment by tracking number.
 *
 * @param {string} trackingNumber
 * @returns {object|null} shipment object or null
 */
function getShipment(trackingNumber) {
  const store = _loadStore();
  return store.shipments[trackingNumber] || null;
}

/**
 * Get all shipments.
 *
 * @returns {object} { [trackingNumber]: shipmentObj }
 */
function getAllShipments() {
  const store = _loadStore();
  return store.shipments;
}

/**
 * Get shipments filtered by status.
 *
 * @param {string} status
 * @returns {object[]} array of shipment objects with trackingNumber attached
 */
function getShipmentsByStatus(status) {
  const store = _loadStore();
  const results = [];
  for (const [tn, shipment] of Object.entries(store.shipments)) {
    if (shipment.status === status) {
      results.push({ ...shipment, trackingNumber: tn });
    }
  }
  return results;
}

/**
 * Create or update a shipment record.
 *
 * Required fields in `data`:
 *  - trackingNumber {string}
 *
 * Optional fields:
 *  - carrier {string}
 *  - orderId {string}
 *  - customerName {string}
 *  - customerEmail {string}
 *  - status {string} (defaults to config initial_state)
 *  - shippedAt {string} ISO timestamp
 *  - metadata {object} any extra data
 *
 * @param {object} data
 * @param {object} [opts]
 * @param {boolean} [opts.dryRun=false] if true, skip writing to disk
 * @returns {object} the upserted shipment
 */
function upsertShipment(data, opts = {}) {
  if (!data || !data.trackingNumber) {
    throw new Error('[shipment-store] upsertShipment requires data.trackingNumber');
  }

  const cfg = loadConfig();
  const store = _loadStore();
  const tn = data.trackingNumber;
  const now = new Date().toISOString();

  const existing = store.shipments[tn];

  if (existing) {
    // Update: merge fields, preserve events and processedEventIds
    const updated = {
      ...existing,
      carrier: data.carrier !== undefined ? data.carrier : existing.carrier,
      orderId: data.orderId !== undefined ? data.orderId : existing.orderId,
      customerName: data.customerName !== undefined ? data.customerName : existing.customerName,
      customerEmail: data.customerEmail !== undefined ? data.customerEmail : existing.customerEmail,
      metadata: data.metadata !== undefined ? { ...(existing.metadata || {}), ...data.metadata } : existing.metadata,
      updatedAt: now
    };

    // Status change via upsert is not allowed; use transitionStatus() instead
    if (data.status && data.status !== existing.status) {
      console.warn(`[shipment-store] upsertShipment ignores status change. Use transitionStatus() for "${existing.status}" → "${data.status}"`);
    }

    store.shipments[tn] = updated;

    if (opts.dryRun) {
      console.log(`[shipment-store][DRY-RUN] Would update shipment ${tn}`);
    } else {
      _saveStore(store);
    }

    return updated;
  }

  // Create new shipment
  const initialStatus = (cfg.state_machine && cfg.state_machine.initial_state) || 'pending_shipment';

  const shipment = {
    trackingNumber: tn,
    carrier: data.carrier || null,
    orderId: data.orderId || null,
    customerName: data.customerName || null,
    customerEmail: data.customerEmail || null,
    status: data.status || initialStatus,
    shippedAt: data.shippedAt || null,
    createdAt: now,
    updatedAt: now,
    events: [],
    processedEventIds: [],
    statusHistory: [
      {
        from: null,
        to: data.status || initialStatus,
        at: now,
        reason: 'initial creation'
      }
    ],
    compensation_reminder: null,
    metadata: data.metadata || {}
  };

  store.shipments[tn] = shipment;

  if (opts.dryRun) {
    console.log(`[shipment-store][DRY-RUN] Would create shipment ${tn} with status "${shipment.status}"`);
  } else {
    _saveStore(store);
  }

  return shipment;
}

/**
 * Add tracking events to a shipment with eventId dedup.
 *
 * Each event should have:
 *  - timestamp {string}
 *  - description {string}
 *  - location {string} (optional)
 *  - status {string} (optional, mapped 17Track status)
 *  - eventId {string} (optional, auto-generated if missing)
 *
 * @param {string} trackingNumber
 * @param {object[]} events
 * @param {object} [opts]
 * @param {boolean} [opts.dryRun=false]
 * @returns {{ added: number, skipped: number, shipment: object }}
 */
function addEvents(trackingNumber, events, opts = {}) {
  if (!trackingNumber) {
    throw new Error('[shipment-store] addEvents requires trackingNumber');
  }
  if (!Array.isArray(events)) {
    throw new Error('[shipment-store] addEvents requires events array');
  }

  const store = _loadStore();
  const shipment = store.shipments[trackingNumber];

  if (!shipment) {
    throw new Error(`[shipment-store] Shipment not found: ${trackingNumber}`);
  }

  let added = 0;
  let skipped = 0;

  for (const evt of events) {
    const eventId = evt.eventId || generateEventId(evt.timestamp, evt.description);

    if (_isEventProcessed(shipment, eventId)) {
      skipped++;
      continue;
    }

    const enrichedEvent = {
      eventId: eventId,
      timestamp: evt.timestamp || new Date().toISOString(),
      description: evt.description || '',
      location: evt.location || null,
      status: evt.status || null,
      rawData: evt.rawData || null,
      addedAt: new Date().toISOString()
    };

    shipment.events.push(enrichedEvent);
    shipment.processedEventIds.push(eventId);
    added++;
  }

  shipment.updatedAt = new Date().toISOString();

  if (opts.dryRun) {
    console.log(`[shipment-store][DRY-RUN] Would add ${added} events to ${trackingNumber} (${skipped} skipped as duplicates)`);
  } else {
    _saveStore(store);
  }

  return { added, skipped, shipment };
}

/**
 * Transition a shipment to a new status via the state machine.
 *
 * Validates the transition against config.state_machine rules.
 * Triggers compensation reminder when entering lost/returning/returned.
 *
 * @param {string} trackingNumber
 * @param {string} newStatus
 * @param {object} [opts]
 * @param {string} [opts.reason] reason for the transition
 * @param {boolean} [opts.force=false] bypass state machine validation
 * @param {boolean} [opts.dryRun=false]
 * @returns {{ success: boolean, shipment?: object, error?: string, compensation?: object }}
 */
function transitionStatus(trackingNumber, newStatus, opts = {}) {
  if (!trackingNumber) {
    throw new Error('[shipment-store] transitionStatus requires trackingNumber');
  }
  if (!newStatus) {
    throw new Error('[shipment-store] transitionStatus requires newStatus');
  }

  const store = _loadStore();
  const shipment = store.shipments[trackingNumber];

  if (!shipment) {
    return { success: false, error: `Shipment not found: ${trackingNumber}` };
  }

  const currentStatus = shipment.status;

  // Same status, no-op
  if (currentStatus === newStatus) {
    return { success: true, shipment, compensation: null };
  }

  // Validate transition (unless forced)
  if (!opts.force) {
    const validation = validateTransition(currentStatus, newStatus);
    if (!validation.valid) {
      return { success: false, error: validation.reason };
    }
  }

  const now = new Date().toISOString();
  const previousStatus = currentStatus;

  // Apply transition
  shipment.status = newStatus;
  shipment.updatedAt = now;

  // Record in statusHistory
  if (!shipment.statusHistory) {
    shipment.statusHistory = [];
  }
  shipment.statusHistory.push({
    from: previousStatus,
    to: newStatus,
    at: now,
    reason: opts.reason || null
  });

  // Check compensation reminder
  const compensation = _checkCompensation(trackingNumber, newStatus, shipment);
  if (compensation) {
    shipment.compensation_reminder = compensation;
  }

  if (opts.dryRun) {
    console.log(`[shipment-store][DRY-RUN] Would transition ${trackingNumber}: "${previousStatus}" → "${newStatus}"`);
    if (compensation) {
      console.log(`[shipment-store][DRY-RUN] Would set compensation reminder: ${compensation.message}`);
    }
  } else {
    _saveStore(store);
  }

  console.log(`[shipment-store] Transitioned ${trackingNumber}: "${previousStatus}" → "${newStatus}"`);

  return { success: true, shipment, compensation };
}

// ---------------------------------------------------------------------------
// Utility functions
// ---------------------------------------------------------------------------

/**
 * Get shipment count summary grouped by status.
 * @returns {object} { [status]: count }
 */
function getStatusSummary() {
  const store = _loadStore();
  const summary = {};
  for (const shipment of Object.values(store.shipments)) {
    const st = shipment.status || 'unknown';
    summary[st] = (summary[st] || 0) + 1;
  }
  return summary;
}

/**
 * Get shipments that have not been updated for more than `days` days.
 *
 * @param {number} days
 * @returns {object[]}
 */
function getStaleShipments(days) {
  const store = _loadStore();
  const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;
  const results = [];

  for (const [tn, shipment] of Object.entries(store.shipments)) {
    // Skip terminal states
    const cfg = loadConfig();
    const terminalStates = (cfg.state_machine && cfg.state_machine.terminal_states) || [];
    if (terminalStates.includes(shipment.status)) continue;

    const lastUpdate = shipment.events && shipment.events.length > 0
      ? new Date(shipment.events[shipment.events.length - 1].timestamp).getTime()
      : new Date(shipment.updatedAt || shipment.createdAt).getTime();

    if (lastUpdate < cutoff) {
      results.push({ ...shipment, trackingNumber: tn, daysSinceUpdate: Math.floor((Date.now() - lastUpdate) / (24 * 60 * 60 * 1000)) });
    }
  }

  return results;
}

/**
 * Remove a shipment from the store.
 * Use with caution; intended for cleanup of test/cancelled shipments.
 *
 * @param {string} trackingNumber
 * @param {object} [opts]
 * @param {boolean} [opts.dryRun=false]
 * @returns {boolean} true if removed
 */
function removeShipment(trackingNumber, opts = {}) {
  const store = _loadStore();
  if (!store.shipments[trackingNumber]) {
    return false;
  }

  if (opts.dryRun) {
    console.log(`[shipment-store][DRY-RUN] Would remove shipment ${trackingNumber}`);
    return true;
  }

  delete store.shipments[trackingNumber];
  _saveStore(store);
  console.log(`[shipment-store] Removed shipment ${trackingNumber}`);
  return true;
}

/**
 * Get the total number of shipments.
 * @returns {number}
 */
function getShipmentCount() {
  const store = _loadStore();
  return Object.keys(store.shipments).length;
}

/**
 * Check if a tracking number exists in the store.
 * @param {string} trackingNumber
 * @returns {boolean}
 */
function hasShipment(trackingNumber) {
  const store = _loadStore();
  return !!store.shipments[trackingNumber];
}

// ---------------------------------------------------------------------------
// Module exports
// ---------------------------------------------------------------------------

module.exports = {
  // Core functions (6 required)
  getShipment,
  upsertShipment,
  addEvents,
  transitionStatus,
  getAllShipments,
  getShipmentsByStatus,

  // Utility functions
  getStatusSummary,
  getStaleShipments,
  removeShipment,
  getShipmentCount,
  hasShipment,

  // State machine helpers
  validateTransition,
  getStatusLabel,

  // Event ID helper
  generateEventId,

  // Config
  loadConfig,
  reloadConfig,

  // Internal (exposed for testing)
  _resolveShipmentsPath,
  _loadStore,
  _saveStore,
  _checkCompensation
};
