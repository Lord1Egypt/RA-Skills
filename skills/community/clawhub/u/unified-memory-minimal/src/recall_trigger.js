/**
 * Recall Trigger v1.0
 * Evaluates schedules and fires recall events
 */

import { getAllMemories } from './storage.js';
import { predictRecall } from './core/proactive_recall.js';
import { getLogger } from './logger.js';

const log = getLogger('recall_trigger');

/**
 * @typedef {Object} RecallPayload
 * @property {string} scheduleId
 * @property {string} scheduleName
 * @property {string} type
 * @property {object[]} memories
 * @property {string} summary
 * @property {string} triggeredAt
 */

/**
 * @typedef {Object} Schedule
 * @property {string} id
 * @property {string} name
 * @property {string} type
 * @property {object} config
 */

export class RecallTrigger {
  constructor() {
    /** @type {Map<string,string>} scheduleId -> lastNotificationHHMM */
    this._firedToday = new Map();
  }

  /**
   * Evaluate all active schedules (for heartbeat or manual trigger)
   * @param {object} [context] - optional context string
   * @returns {Promise<RecallPayload[]>}
   */
  async checkRecalls(context = '') {
    const results = [];
    // event_based are evaluated by the scheduler's onHeartbeat
    // This method is for a full manual sweep
    return results;
  }

  /**
   * Fire a single recall schedule
   * @param {Schedule} schedule
   * @returns {Promise<RecallPayload>}
   */
  async fireRecall(schedule) {
    const memories = getAllMemories();
    const recallResults = predictRecall(schedule.config.query || schedule.name || 'general');

    const topMemories = recallResults.slice(0, 5).map(r => ({
      id: r.memory?.id || r.memory?.id || 'unknown',
      text: r.memory?.text || '',
      category: r.memory?.category || 'unknown',
      importance: r.memory?.importance || 0.5,
      relevance: r.relevance || 0,
      reason: r.reason || '',
    }));

    const summary = this._summarize(topMemories, schedule);

    /** @type {RecallPayload} */
    const payload = {
      scheduleId: schedule.id,
      scheduleName: schedule.name,
      type: schedule.type,
      memories: topMemories,
      summary,
      triggeredAt: new Date().toISOString(),
    };

    log.info(`[RecallTrigger] fired schedule=${schedule.name} type=${schedule.type} count=${topMemories.length}`);

    return payload;
  }

  /**
   * Check if a schedule already fired today at the same time slot
   * Prevents duplicate firings for time_based schedules
   * @param {string} scheduleId
   * @returns {boolean}
   */
  hasFiredToday(scheduleId) {
    const today = new Date().toDateString();
    const last = this._firedToday.get(scheduleId);
    if (last !== today) {
      this._firedToday.set(scheduleId, today);
      return false;
    }
    return true;
  }

  _summarize(memories, schedule) {
    if (!memories.length) {
      return `Proactive recall "${schedule.name}" triggered — no matching memories found.`;
    }

    const categoryGroups = {};
    for (const m of memories) {
      const cat = m.category || 'unknown';
      if (!categoryGroups[cat]) categoryGroups[cat] = [];
      categoryGroups[cat].push(m);
    }

    const parts = [];
    for (const [cat, items] of Object.entries(categoryGroups)) {
      const count = items.length;
      const total = memories.length;
      const pct = Math.round((count / total) * 100);
      parts.push(`${count} ${cat} (${pct}%)`);
    }

    const avgImportance = memories.reduce((s, m) => s + (m.importance || 0), 0) / memories.length;

    return (
      `Recall "${schedule.name}" [${schedule.type}] → ` +
      `${memories.length} memories: ${parts.join(', ')}. ` +
      `Avg importance: ${avgImportance.toFixed(2)}.`
    );
  }

  /**
   * Build notification text from a recall payload
   * @param {RecallPayload} payload
   * @returns {string}
   */
  static formatNotification(payload) {
    const lines = [
      `🔔 **Proactive Recall: ${payload.scheduleName}**`,
      `Type: ${payload.type} | Triggered: ${new Date(payload.triggeredAt).toLocaleString()}`,
      '',
      `**Summary:** ${payload.summary}`,
      '',
      `**Top Memories (${payload.memories.length}):**`,
    ];

    for (const m of payload.memories.slice(0, 5)) {
      const snippet = (m.text || '').substring(0, 80).replace(/\n/g, ' ');
      lines.push(`• [${m.category}] ${snippet}… (imp: ${(m.importance || 0).toFixed(2)})`);
    }

    return lines.join('\n');
  }
}

// Singleton
let _trigger = null;

export function getRecallTrigger() {
  if (!_trigger) _trigger = new RecallTrigger();
  return _trigger;
}
