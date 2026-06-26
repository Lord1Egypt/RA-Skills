/**
 * tracking-api.js - 17Track REST 批量查询适配器
 *
 * 功能：
 *  - registerTracking(numbers)   批量注册运单号到 17Track
 *  - getTrackingInfo(numbers)    批量查询物流信息（batchSize≤40）
 *  - shouldRefresh(shipment)     智能刷新调度（根据运单阶段过滤）
 *  - getQuotaStatus()            配额监控
 *
 * 环境变量：TRACK17_API_KEY
 * 配置文件：../config/logistics-config.json
 *
 * @module tracking-api
 */

'use strict';

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const { URL } = require('url');

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

const CONFIG_PATH = path.resolve(__dirname, '../config/logistics-config.json');

let _configCache = null;

function loadConfig() {
  if (_configCache) return _configCache;
  const raw = fs.readFileSync(CONFIG_PATH, 'utf-8');
  _configCache = JSON.parse(raw);
  return _configCache;
}

/** Force reload config (useful after external edits). */
function reloadConfig() {
  _configCache = null;
  return loadConfig();
}

// ---------------------------------------------------------------------------
// Quota tracking (in-memory + file-backed)
// ---------------------------------------------------------------------------

const QUOTA_FILE = path.resolve(__dirname, '../data/quota-usage.json');

function _ensureDataDir() {
  const dir = path.dirname(QUOTA_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function _todayKey() {
  return new Date().toISOString().slice(0, 10); // YYYY-MM-DD
}

function _loadQuota() {
  _ensureDataDir();
  if (!fs.existsSync(QUOTA_FILE)) return {};
  try {
    return JSON.parse(fs.readFileSync(QUOTA_FILE, 'utf-8'));
  } catch {
    return {};
  }
}

function _saveQuota(data) {
  _ensureDataDir();
  const tmp = QUOTA_FILE + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2));
  fs.renameSync(tmp, QUOTA_FILE);
}

/**
 * Increment today's API call count by `n`.
 * Returns updated today count.
 */
function _incrementQuota(n) {
  const data = _loadQuota();
  const key = _todayKey();
  data[key] = (data[key] || 0) + n;
  _saveQuota(data);
  return data[key];
}

/**
 * Get current quota status.
 * @returns {{ used: number, limit: number, remaining: number, percent: number, level: 'ok'|'warning'|'critical'|'exhausted' }}
 */
function getQuotaStatus() {
  const config = loadConfig();
  const quota = config.quota || {};
  const limit = quota.daily_limit || 100;
  const data = _loadQuota();
  const used = data[_todayKey()] || 0;
  const remaining = Math.max(0, limit - used);
  const percent = used / limit;

  let level = 'ok';
  if (percent >= 1) level = 'exhausted';
  else if (percent >= (quota.critical_threshold || 0.95)) level = 'critical';
  else if (percent >= (quota.warning_threshold || 0.8)) level = 'warning';

  return { used, limit, remaining, percent: Math.round(percent * 100), level };
}

// ---------------------------------------------------------------------------
// Retry with exponential backoff
// ---------------------------------------------------------------------------

/**
 * Sleep helper.
 * @param {number} ms
 */
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Execute `fn` with exponential backoff retries.
 * @param {Function} fn          async function to execute
 * @param {object}   [opts]
 * @param {number[]} [opts.delays]            delay schedule in ms
 * @param {string[]} [opts.retryableErrors]   error codes that allow retry
 * @param {string[]} [opts.nonRetryableErrors] error codes that abort immediately
 */
async function withRetry(fn, opts = {}) {
  const config = loadConfig();
  const retryConf = config.retry || {};
  const maxAttempts = retryConf.max_attempts || 3;
  const delaysMin = retryConf.delays_minutes || [1, 5, 15];
  const delays = opts.delays || delaysMin.map((m) => m * 60 * 1000);
  const retryable = new Set(opts.retryableErrors || retryConf.retryable_errors || []);
  const nonRetryable = new Set(opts.nonRetryableErrors || retryConf.non_retryable_errors || []);

  let lastError;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err;
      const code = err.code || err.errorCode || '';

      // Non-retryable: abort immediately
      if (nonRetryable.has(code)) {
        throw err;
      }

      // If retryable set is defined, only retry matching codes
      if (retryable.size > 0 && !retryable.has(code)) {
        throw err;
      }

      // If this was the last attempt, throw
      if (attempt >= maxAttempts - 1) {
        throw err;
      }

      const delayMs = delays[attempt] || delays[delays.length - 1];
      console.log(
        `[tracking-api] Attempt ${attempt + 1} failed (${code || err.message}), retrying in ${delayMs / 1000}s...`
      );
      await sleep(delayMs);
    }
  }
  throw lastError;
}

// ---------------------------------------------------------------------------
// HTTP helper
// ---------------------------------------------------------------------------

/**
 * Make an HTTPS/HTTP request.
 * @param {string} url
 * @param {object} options   { method, headers, body }
 * @returns {Promise<{ statusCode: number, headers: object, body: string, json: any }>}
 */
function httpRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const mod = parsed.protocol === 'https:' ? https : http;
    const reqOpts = {
      hostname: parsed.hostname,
      port: parsed.port || (parsed.protocol === 'https:' ? 443 : 80),
      path: parsed.pathname + parsed.search,
      method: options.method || 'POST',
      headers: options.headers || {},
    };

    const req = mod.request(reqOpts, (res) => {
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => {
        const body = Buffer.concat(chunks).toString('utf-8');
        let json = null;
        try {
          json = JSON.parse(body);
        } catch {
          // not JSON
        }
        resolve({ statusCode: res.statusCode, headers: res.headers, body, json });
      });
    });

    req.on('error', (err) => reject(err));
    req.setTimeout(30000, () => {
      req.destroy(new Error('ETIMEDOUT'));
    });

    if (options.body) {
      req.write(typeof options.body === 'string' ? options.body : JSON.stringify(options.body));
    }
    req.end();
  });
}

// ---------------------------------------------------------------------------
// 17Track API helpers
// ---------------------------------------------------------------------------

function _getApiKey() {
  const key = process.env.TRACK17_API_KEY;
  if (!key) {
    const err = new Error('Missing TRACK17_API_KEY environment variable');
    err.code = 'MISSING_API_KEY';
    throw err;
  }
  return key;
}

function _buildUrl(endpoint) {
  const config = loadConfig();
  const base = config.api.primary.endpoint; // https://api.17track.net/track/v2.2
  return base + endpoint;
}

function _buildHeaders() {
  return {
    'Content-Type': 'application/json',
    '17token': _getApiKey(),
  };
}

/**
 * Split an array into chunks of `size`.
 */
function chunk(arr, size) {
  const result = [];
  for (let i = 0; i < arr.length; i += size) {
    result.push(arr.slice(i, i + size));
  }
  return result;
}

// ---------------------------------------------------------------------------
// Core API functions
// ---------------------------------------------------------------------------

/**
 * Register tracking numbers with 17Track.
 *
 * @param {string[]} numbers    Array of tracking number strings
 * @param {object}   [opts]
 * @param {boolean}  [opts.dryRun=false]  If true, log request but don't send
 * @returns {Promise<{ accepted: object[], rejected: object[], raw: object[] }>}
 */
async function registerTracking(numbers, opts = {}) {
  if (!numbers || numbers.length === 0) {
    return { accepted: [], rejected: [], raw: [] };
  }

  const config = loadConfig();
  const batchSize = config.api.primary.batch_size || 40;
  const batches = chunk(numbers, batchSize);
  const url = _buildUrl(config.api.primary.register_endpoint || '/register');
  const headers = opts.dryRun ? {} : _buildHeaders();

  const allAccepted = [];
  const allRejected = [];
  const allRaw = [];

  for (const batch of batches) {
    const body = batch.map((num) => ({
      number: num,
      carrier: 0, // auto-detect
    }));

    if (opts.dryRun) {
      console.log(`[tracking-api][DRY-RUN] registerTracking POST ${url}`);
      console.log(`[tracking-api][DRY-RUN] Body: ${JSON.stringify(body, null, 2)}`);
      allRaw.push({ dryRun: true, url, body });
      continue;
    }

    // Check quota before calling
    const quotaBefore = getQuotaStatus();
    if (quotaBefore.level === 'exhausted') {
      console.log('[tracking-api] Quota exhausted, skipping register call');
      allRejected.push(
        ...batch.map((num) => ({ number: num, error: 'QUOTA_EXHAUSTED' }))
      );
      continue;
    }

    const res = await withRetry(async () => {
      const r = await httpRequest(url, { method: 'POST', headers, body: JSON.stringify(body) });

      // Map HTTP errors to retryable codes
      if (r.statusCode === 429) {
        const err = new Error('Rate limited');
        err.code = 'HTTP_429';
        throw err;
      }
      if (r.statusCode >= 500) {
        const err = new Error(`Server error ${r.statusCode}`);
        err.code = `HTTP_${r.statusCode}`;
        throw err;
      }
      if (r.statusCode === 401 || r.statusCode === 403) {
        const err = new Error(`Auth error ${r.statusCode}`);
        err.code = `HTTP_${r.statusCode}`;
        throw err;
      }

      return r;
    });

    _incrementQuota(1);

    const data = res.json && res.json.data ? res.json.data : {};
    if (Array.isArray(data.accepted)) allAccepted.push(...data.accepted);
    if (Array.isArray(data.rejected)) allRejected.push(...data.rejected);
    allRaw.push(res.json);
  }

  return { accepted: allAccepted, rejected: allRejected, raw: allRaw };
}

/**
 * Batch query tracking info from 17Track.
 *
 * @param {string[]} numbers    Array of tracking number strings
 * @param {object}   [opts]
 * @param {boolean}  [opts.dryRun=false]  If true, log request but don't send
 * @returns {Promise<{ accepted: object[], rejected: object[], events: Map<string, object[]>, raw: object[] }>}
 *
 * `events` is a Map: trackingNumber -> array of tracking event objects
 */
async function getTrackingInfo(numbers, opts = {}) {
  if (!numbers || numbers.length === 0) {
    return { accepted: [], rejected: [], events: new Map(), raw: [] };
  }

  const config = loadConfig();
  const batchSize = config.api.primary.batch_size || 40;
  const batches = chunk(numbers, batchSize);
  const url = _buildUrl(config.api.primary.batch_endpoint || '/gettrackinfo');
  const headers = opts.dryRun ? {} : _buildHeaders();

  const allAccepted = [];
  const allRejected = [];
  const eventsMap = new Map();
  const allRaw = [];

  for (const batch of batches) {
    const body = batch.map((num) => ({
      number: num,
      carrier: 0,
    }));

    if (opts.dryRun) {
      console.log(`[tracking-api][DRY-RUN] getTrackingInfo POST ${url}`);
      console.log(`[tracking-api][DRY-RUN] Body (${batch.length} numbers): ${JSON.stringify(body, null, 2)}`);
      allRaw.push({ dryRun: true, url, body });
      continue;
    }

    // Quota check
    const quotaBefore = getQuotaStatus();
    if (quotaBefore.level === 'exhausted') {
      console.log('[tracking-api] Quota exhausted, skipping getTrackingInfo call');
      allRejected.push(
        ...batch.map((num) => ({ number: num, error: 'QUOTA_EXHAUSTED' }))
      );
      continue;
    }

    const res = await withRetry(async () => {
      const r = await httpRequest(url, { method: 'POST', headers, body: JSON.stringify(body) });

      if (r.statusCode === 429) {
        const err = new Error('Rate limited');
        err.code = 'HTTP_429';
        throw err;
      }
      if (r.statusCode >= 500) {
        const err = new Error(`Server error ${r.statusCode}`);
        err.code = `HTTP_${r.statusCode}`;
        throw err;
      }
      if (r.statusCode === 401 || r.statusCode === 403) {
        const err = new Error(`Auth error ${r.statusCode}`);
        err.code = `HTTP_${r.statusCode}`;
        throw err;
      }

      return r;
    });

    _incrementQuota(1);

    const data = res.json && res.json.data ? res.json.data : {};
    const accepted = Array.isArray(data.accepted) ? data.accepted : [];
    const rejected = Array.isArray(data.rejected) ? data.rejected : [];

    allAccepted.push(...accepted);
    allRejected.push(...rejected);
    allRaw.push(res.json);

    // Parse tracking events from accepted items
    for (const item of accepted) {
      const trackNum = item.number || '';
      const events = _extractEvents(item);
      if (events.length > 0) {
        eventsMap.set(trackNum, events);
      }
    }
  }

  return { accepted: allAccepted, rejected: allRejected, events: eventsMap, raw: allRaw };
}

/**
 * Extract tracking events from a 17Track accepted item.
 * Navigates: track_info.tracking.providers[0].events
 * Falls back to: track.z0.z (v2.2 format variations)
 *
 * @param {object} item  A single accepted tracking item from 17Track
 * @returns {object[]}   Array of event objects { date, description, location, status }
 */
function _extractEvents(item) {
  // Path 1: track_info.tracking.providers[0].events (documented in config)
  try {
    const providers = item.track_info?.tracking?.providers;
    if (Array.isArray(providers) && providers.length > 0) {
      const events = providers[0].events;
      if (Array.isArray(events)) {
        return events.map((e) => ({
          date: e.date || e.time_iso || e.a || null,
          description: e.description || e.z || '',
          location: e.location || e.c || '',
          status: e.status || null,
        }));
      }
    }
  } catch {
    // fallthrough
  }

  // Path 2: v2.2 flat format (track.z0.z for events)
  try {
    const z0 = item.track?.z0;
    if (z0 && Array.isArray(z0.z)) {
      return z0.z.map((e) => ({
        date: e.a || null,
        description: e.z || '',
        location: e.c || '',
        status: null,
      }));
    }
  } catch {
    // fallthrough
  }

  // Path 3: direct .tracking_events or .events array
  const direct = item.tracking_events || item.events;
  if (Array.isArray(direct)) {
    return direct.map((e) => ({
      date: e.date || e.time || null,
      description: e.description || e.content || '',
      location: e.location || '',
      status: e.status || null,
    }));
  }

  return [];
}

// ---------------------------------------------------------------------------
// Smart refresh scheduling
// ---------------------------------------------------------------------------

/**
 * Determine if a shipment should be refreshed now, based on its stage and
 * the configured refresh strategy.
 *
 * @param {object} shipment  Shipment record from shipment-store
 *   Expected fields: { status, shipped_at, last_refreshed_at, last_event_description }
 * @returns {{ shouldRefresh: boolean, stage: string, reason: string }}
 */
function shouldRefresh(shipment) {
  const config = loadConfig();
  const strategy = config.refresh_strategy || {};
  const stages = strategy.stages || {};

  const status = shipment.status || 'pending_shipment';
  const now = Date.now();

  // Terminal states: no refresh
  const stateMachine = config.state_machine || {};
  const terminalStates = stateMachine.terminal_states || ['delivered', 'returned', 'lost'];
  if (terminalStates.includes(status)) {
    return { shouldRefresh: false, stage: 'terminal', reason: `Terminal state: ${status}` };
  }

  // Determine stage
  const stage = _classifyStage(shipment, strategy);

  // Get interval for this stage
  const stageConf = stages[stage];
  if (!stageConf || stageConf.interval_hours === null) {
    return { shouldRefresh: false, stage, reason: 'No refresh interval for this stage' };
  }

  const intervalMs = stageConf.interval_hours * 3600 * 1000;
  const lastRefresh = shipment.last_refreshed_at
    ? new Date(shipment.last_refreshed_at).getTime()
    : 0;

  if (now - lastRefresh >= intervalMs) {
    return { shouldRefresh: true, stage, reason: `${stageConf.interval_hours}h interval elapsed` };
  }

  return {
    shouldRefresh: false,
    stage,
    reason: `Next refresh in ${Math.ceil((intervalMs - (now - lastRefresh)) / 60000)} min`,
  };
}

/**
 * Classify a shipment into a refresh stage.
 * Priority: near_delivery > exception > new_shipment > in_transit
 */
function _classifyStage(shipment, strategy) {
  const status = shipment.status || '';

  // Exception states
  const exceptionStatuses = ['returning', 'returned', 'lost', 'refused'];
  if (exceptionStatuses.includes(status)) {
    return 'exception';
  }

  // Check near_delivery trigger
  if (_isNearDelivery(shipment, strategy)) {
    return 'near_delivery';
  }

  // New shipment (within max_age_days of shipping)
  const newConf = (strategy.stages || {}).new_shipment || {};
  const maxAgeDays = newConf.max_age_days || 3;
  if (shipment.shipped_at) {
    const shippedAt = new Date(shipment.shipped_at).getTime();
    const daysSinceShip = (Date.now() - shippedAt) / (86400 * 1000);
    if (daysSinceShip <= maxAgeDays) {
      return 'new_shipment';
    }
  }

  // Default: in_transit
  return 'in_transit';
}

/**
 * Check if a shipment matches near-delivery trigger conditions.
 */
function _isNearDelivery(shipment, strategy) {
  const trigger = strategy.near_delivery_trigger || {};
  const conditions = trigger.conditions || [];

  for (const cond of conditions) {
    if (cond.type === 'status_keyword') {
      const keywords = (cond.keywords || []).map((k) => k.toLowerCase());
      const lastDesc = (shipment.last_event_description || '').toLowerCase();
      if (keywords.some((kw) => lastDesc.includes(kw))) {
        return true;
      }
    }

    if (cond.type === 'last_mile_carrier_scan') {
      // Status-based: near_delivery status from state machine
      if (shipment.status === 'near_delivery') {
        return true;
      }
    }
  }

  return false;
}

/**
 * Filter a list of shipments to those needing refresh, grouped by priority.
 *
 * @param {object[]} shipments  Array of shipment records
 * @returns {{ toRefresh: object[], skipped: object[], groups: object }}
 *
 * `groups` is { [stage]: trackingNumber[] } ordered by priority
 */
function filterForRefresh(shipments) {
  const config = loadConfig();
  const strategy = config.refresh_strategy || {};
  const priorityOrder = (strategy.batch_grouping || {}).priority_order || [
    'near_delivery',
    'new_shipment',
    'exception',
    'in_transit',
  ];

  const toRefresh = [];
  const skipped = [];
  const groups = {};

  for (const s of shipments) {
    const result = shouldRefresh(s);
    if (result.shouldRefresh) {
      toRefresh.push(s);
      const stage = result.stage;
      if (!groups[stage]) groups[stage] = [];
      groups[stage].push(s.tracking_number);
    } else {
      skipped.push({ ...s, _skipReason: result.reason });
    }
  }

  // Sort groups by priority
  const orderedGroups = {};
  for (const stage of priorityOrder) {
    if (groups[stage] && groups[stage].length > 0) {
      orderedGroups[stage] = groups[stage];
    }
  }
  // Add any remaining stages not in priority list
  for (const [stage, nums] of Object.entries(groups)) {
    if (!orderedGroups[stage]) {
      orderedGroups[stage] = nums;
    }
  }

  return { toRefresh, skipped, groups: orderedGroups };
}

/**
 * Check if a specific stage is allowed under current quota constraints.
 * When quota is exhausted with pause_non_critical behavior, only
 * near_delivery and exception stages remain active.
 *
 * @param {string} stage
 * @returns {boolean}
 */
function isStageAllowedByQuota(stage) {
  const quotaStatus = getQuotaStatus();
  if (quotaStatus.level !== 'exhausted') return true;

  const config = loadConfig();
  const rules = (config.quota || {}).pause_non_critical_rules || {};
  const keepActive = rules.keep_active || ['near_delivery', 'exception'];
  return keepActive.includes(stage);
}

/**
 * Build a prioritized list of tracking numbers to query, respecting quota.
 * Returns numbers in priority order, capped by remaining quota (each batch = 1 API call).
 *
 * @param {object[]} shipments
 * @returns {{ numbers: string[], quotaStatus: object, filtered: { stage: string, numbers: string[] }[] }}
 */
function buildRefreshQueue(shipments) {
  const config = loadConfig();
  const batchSize = config.api.primary.batch_size || 40;
  const { groups } = filterForRefresh(shipments);
  const quotaStatus = getQuotaStatus();

  const filtered = [];
  const allNumbers = [];

  for (const [stage, nums] of Object.entries(groups)) {
    if (!isStageAllowedByQuota(stage)) {
      console.log(
        `[tracking-api] Stage "${stage}" paused due to quota degradation (${nums.length} shipments skipped)`
      );
      continue;
    }
    filtered.push({ stage, numbers: nums });
    allNumbers.push(...nums);
  }

  // Cap by remaining API calls (each call handles up to batchSize numbers)
  const maxCalls = quotaStatus.remaining;
  const maxNumbers = maxCalls * batchSize;
  const cappedNumbers = allNumbers.slice(0, maxNumbers);

  return { numbers: cappedNumbers, quotaStatus, filtered };
}

// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------

module.exports = {
  // Config
  loadConfig,
  reloadConfig,

  // Core API
  registerTracking,
  getTrackingInfo,

  // Refresh scheduling
  shouldRefresh,
  filterForRefresh,
  isStageAllowedByQuota,
  buildRefreshQueue,

  // Quota
  getQuotaStatus,

  // Utilities (exposed for testing)
  chunk,
  withRetry,
  sleep,
  _extractEvents,
};
