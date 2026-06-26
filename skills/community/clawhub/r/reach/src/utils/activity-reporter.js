import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const LOG_PATH = path.join(__dirname, '..', '..', 'data', 'activity-log.json');

/**
 * Activity Reporter.
 *
 * Logs significant Reach actions to data/activity-log.json.
 * Future: report to ReputationOracle via keeper.
 */

/**
 * Load existing activity log.
 * @returns {object[]}
 */
function loadLog() {
  try {
    if (fs.existsSync(LOG_PATH)) {
      return JSON.parse(fs.readFileSync(LOG_PATH, 'utf-8'));
    }
  } catch {}
  return [];
}

/**
 * Save activity log.
 * @param {object[]} entries
 */
function saveLog(entries) {
  const dir = path.dirname(LOG_PATH);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(LOG_PATH, JSON.stringify(entries, null, 2));
}

/**
 * Log a completed action.
 *
 * @param {object} action
 * @param {string} action.type - Action type: 'submit_finding', 'send_email', 'complete_form', 'authenticate', 'pay', 'custom'
 * @param {string} action.site - Site or service name
 * @param {string} [action.description] - Human-readable description
 * @param {object} [action.metadata] - Additional data
 * @param {string} [action.identity] - Exo identity name if available
 * @returns {object} The logged entry
 */
export function logActivity(action) {
  const entry = {
    id: `act-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    timestamp: new Date().toISOString(),
    type: action.type,
    site: action.site,
    description: action.description || '',
    metadata: action.metadata || {},
    identity: action.identity || null,
  };

  const log = loadLog();
  log.push(entry);

  // Keep last 1000 entries
  const trimmed = log.length > 1000 ? log.slice(-1000) : log;
  saveLog(trimmed);

  return entry;
}

/**
 * Get recent activity entries.
 *
 * @param {number} [limit=50] - Max entries to return
 * @param {string} [type] - Filter by action type
 * @returns {object[]}
 */
export function getActivity(limit = 50, type) {
  const log = loadLog();
  const filtered = type ? log.filter(e => e.type === type) : log;
  return filtered.slice(-limit);
}

/**
 * Get activity summary (counts by type).
 * @returns {object}
 */
export function getActivitySummary() {
  const log = loadLog();
  const summary = {};
  for (const entry of log) {
    summary[entry.type] = (summary[entry.type] || 0) + 1;
  }
  summary.total = log.length;
  return summary;
}

/**
 * Clear the activity log.
 */
export function clearActivity() {
  saveLog([]);
}

export default { logActivity, getActivity, getActivitySummary, clearActivity };
