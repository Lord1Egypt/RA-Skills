/**
 * Proactive Scheduler v1.0
 * Cron-based scheduler for proactive recall using setInterval
 * Schedule types: periodic (every N minutes), time_based (HH:MM), event_based (keywords)
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const SCHEDULE_FILE = join(WORKSPACE, 'memory', 'proactive_schedules.json');

// ─── Storage ──────────────────────────────────────────────────────────────────

function ensureDir() {
  const dir = join(WORKSPACE, 'memory');
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

export function loadSchedules() {
  ensureDir();
  if (!existsSync(SCHEDULE_FILE)) return [];
  try { return JSON.parse(readFileSync(SCHEDULE_FILE, 'utf-8')); }
  catch { return []; }
}

export function saveSchedules(schedules) {
  ensureDir();
  writeFileSync(SCHEDULE_FILE, JSON.stringify(schedules, null, 2), 'utf-8');
}

export function addSchedule(schedule) {
  const schedules = loadSchedules();
  schedules.push(schedule);
  saveSchedules(schedules);
  return schedule;
}

export function removeSchedule(id) {
  const schedules = loadSchedules();
  const idx = schedules.findIndex(s => s.id === id);
  if (idx === -1) return false;
  schedules.splice(idx, 1);
  saveSchedules(schedules);
  return true;
}

export function updateSchedule(id, patch) {
  const schedules = loadSchedules();
  const idx = schedules.findIndex(s => s.id === id);
  if (idx === -1) return null;
  schedules[idx] = { ...schedules[idx], ...patch };
  saveSchedules(schedules);
  return schedules[idx];
}

// ─── Time Helpers ─────────────────────────────────────────────────────────────

function getCurrentHHMM() {
  const now = new Date();
  return `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
}

// ─── Scheduler Engine ─────────────────────────────────────────────────────────

export class ProactiveScheduler {
  constructor() {
    this.timers = new Map(); // scheduleId -> intervalId
    this.enabled = false;
    this._tickInterval = null;
    /** @type {import('./recall_trigger.js')} */
    this.recallTrigger = null;
  }

  setRecallTrigger(rt) {
    this.recallTrigger = rt;
  }

  start() {
    if (this.enabled) return;
    this.enabled = true;

    // Master tick every 60 seconds for time-based checks
    this._tickInterval = setInterval(() => this._onTick(), 60_000);
    this._onTick(); // immediate first run

    // Setup periodic schedules
    const schedules = loadSchedules();
    for (const sched of schedules) {
      if (sched.enabled) this._startSchedule(sched);
    }

    console.log('[ProactiveScheduler] started');
  }

  stop() {
    if (!this.enabled) return;
    this.enabled = false;
    if (this._tickInterval) {
      clearInterval(this._tickInterval);
      this._tickInterval = null;
    }
    for (const tid of this.timers.values()) {
      clearInterval(tid);
    }
    this.timers.clear();
    console.log('[ProactiveScheduler] stopped');
  }

  _startSchedule(sched) {
    if (this.timers.has(sched.id)) return;

    if (sched.type === 'periodic') {
      const ms = (sched.config.intervalMinutes || 30) * 60_000;
      const tid = setInterval(() => this._firePeriodic(sched), ms);
      this.timers.set(sched.id, tid);
    }
    // time_based and event_based handled in _onTick
  }

  _stopSchedule(schedId) {
    const tid = this.timers.get(schedId);
    if (tid !== undefined) {
      clearInterval(tid);
      this.timers.delete(schedId);
    }
  }

  _firePeriodic(sched) {
    if (!this.recallTrigger) return;
    try {
      this.recallTrigger.fireRecall(sched);
    } catch (e) {
      console.error(`[ProactiveScheduler] fire error for ${sched.id}:`, e.message);
    }
  }

  async _onTick() {
    if (!this.recallTrigger) return;
    const now = new Date();
    const schedules = loadSchedules();

    for (const sched of schedules) {
      if (!sched.enabled) continue;

      if (sched.type === 'time_based') {
        const currentHHMM = getCurrentHHMM();
        const lastFired = sched.lastFired
          ? new Date(sched.lastFired).toTimeString().slice(0, 5)
          : '';

        for (const t of sched.config.times || []) {
          if (t === currentHHMM && t !== lastFired) {
            try {
              await this.recallTrigger.fireRecall(sched);
              updateSchedule(sched.id, { lastFired: now.toISOString() });
            } catch (e) {
              console.error(`[ProactiveScheduler] time_based fire error:`, e.message);
            }
            break;
          }
        }
      }
    }
  }

  /** Called by heartbeat hook */
  async onHeartbeat(context) {
    if (!this.recallTrigger) return [];
    const schedules = loadSchedules();
    const results = [];

    for (const sched of schedules) {
      if (!sched.enabled || sched.type !== 'event_based') continue;
      const { keywords = [], categories = [] } = sched.config;

      let matched = false;
      const ctxLower = (context || '').toLowerCase();

      if (keywords.length > 0) {
        matched = keywords.some(k => ctxLower.includes(k.toLowerCase()));
      }
      if (!matched && categories.length > 0) {
        // categories checked against memory context
        matched = categories.some(c => ctxLower.includes(c.toLowerCase()));
      }

      if (matched) {
        try {
          const result = await this.recallTrigger.fireRecall(sched);
          results.push(result);
        } catch (e) {
          console.error(`[ProactiveScheduler] event_based fire error:`, e.message);
        }
      }
    }

    return results;
  }

  add(sched) {
    addSchedule(sched);
    if (sched.enabled && sched.type === 'periodic') {
      this._startSchedule(sched);
    }
  }

  remove(id) {
    this._stopSchedule(id);
    removeSchedule(id);
  }

  list() {
    return loadSchedules();
  }

  enable(id) {
    const sched = updateSchedule(id, { enabled: true });
    if (sched) this._startSchedule(sched);
    return sched;
  }

  disable(id) {
    this._stopSchedule(id);
    return updateSchedule(id, { enabled: false });
  }
}

// Singleton
let _scheduler = null;

export function getProactiveScheduler() {
  if (!_scheduler) _scheduler = new ProactiveScheduler();
  return _scheduler;
}
