/**
 * Routine Manager — Public version
 * Scheduled checks, triggers, and periodic tasks
 * Basic scaffolding — no self-learning (that's private)
 */

class RoutineManager {
  constructor(config = {}) {
    this.config = {
      tickInterval: config.tickInterval || 60000, // check every 60s
      timezone: config.timezone || Intl.DateTimeFormat().resolvedOptions().timeZone,
      ...config
    };

    this.routines = new Map();
    this.history = [];       // last N executions
    this.maxHistory = config.maxHistory || 200;
    this.ticker = null;
    this.listeners = [];     // event callbacks
  }

  // --- Routine CRUD ---

  /**
   * Add a routine
   * @param {object} routine
   * @param {string} routine.id - unique identifier
   * @param {string} routine.name - display name
   * @param {string} routine.schedule - cron-like: "every 30m", "daily 09:00", "hourly", "every 5m"
   * @param {function} routine.action - async function to execute
   * @param {string} [routine.model] - preferred model for this routine (passed to task router)
   * @param {boolean} [routine.enabled=true]
   * @param {object} [routine.conditions] - optional conditions (see _checkConditions)
   */
  add(routine) {
    if (!routine.id || !routine.schedule || !routine.action) {
      throw new Error('Routine requires id, schedule, and action');
    }

    this.routines.set(routine.id, {
      id: routine.id,
      name: routine.name || routine.id,
      schedule: routine.schedule,
      action: routine.action,
      model: routine.model || null,
      enabled: routine.enabled !== false,
      conditions: routine.conditions || {},
      lastRun: null,
      nextRun: null,
      runCount: 0,
      errors: 0,
      createdAt: Date.now()
    });

    this._calcNextRun(routine.id);
    this._emit('routine:added', { id: routine.id });
    return this;
  }

  remove(id) {
    this.routines.delete(id);
    this._emit('routine:removed', { id });
    return this;
  }

  enable(id) {
    const r = this.routines.get(id);
    if (r) { r.enabled = true; this._calcNextRun(id); }
    return this;
  }

  disable(id) {
    const r = this.routines.get(id);
    if (r) { r.enabled = false; r.nextRun = null; }
    return this;
  }

  get(id) {
    return this.routines.get(id);
  }

  list() {
    return Array.from(this.routines.values()).map(r => ({
      id: r.id,
      name: r.name,
      schedule: r.schedule,
      enabled: r.enabled,
      model: r.model,
      lastRun: r.lastRun,
      nextRun: r.nextRun,
      runCount: r.runCount,
      errors: r.errors
    }));
  }

  // --- Lifecycle ---

  start() {
    if (this.ticker) return this;
    this.ticker = setInterval(() => this._tick(), this.config.tickInterval);
    this._emit('manager:started', {});
    // Run first tick immediately
    this._tick();
    return this;
  }

  stop() {
    if (this.ticker) {
      clearInterval(this.ticker);
      this.ticker = null;
    }
    this._emit('manager:stopped', {});
    return this;
  }

  isRunning() {
    return this.ticker !== null;
  }

  // --- Event system ---

  on(callback) {
    this.listeners.push(callback);
    return this;
  }

  off(callback) {
    this.listeners = this.listeners.filter(l => l !== callback);
    return this;
  }

  _emit(event, data) {
    for (const listener of this.listeners) {
      try { listener(event, data); } catch (e) { /* don't break loop */ }
    }
  }

  // --- Schedule parsing ---

  /**
   * Parse schedule string into interval milliseconds
   * Supports: "every Nm", "every Nh", "hourly", "daily HH:MM", "every Ns"
   */
  _parseInterval(schedule) {
    const s = schedule.trim().toLowerCase();

    if (s === 'hourly') return { type: 'interval', ms: 3600000 };

    // "every Xm", "every Xh", "every Xs"
    const everyMatch = s.match(/^every\s+(\d+)\s*(s|m|h)$/);
    if (everyMatch) {
      const val = parseInt(everyMatch[1]);
      const unit = everyMatch[2];
      const multiplier = { s: 1000, m: 60000, h: 3600000 };
      return { type: 'interval', ms: val * multiplier[unit] };
    }

    // "daily HH:MM"
    const dailyMatch = s.match(/^daily\s+(\d{1,2}):(\d{2})$/);
    if (dailyMatch) {
      return {
        type: 'daily',
        hour: parseInt(dailyMatch[1]),
        minute: parseInt(dailyMatch[2])
      };
    }

    // fallback: treat as interval in minutes
    const numMatch = s.match(/^(\d+)$/);
    if (numMatch) {
      return { type: 'interval', ms: parseInt(numMatch[1]) * 60000 };
    }

    return null;
  }

  _calcNextRun(id) {
    const r = this.routines.get(id);
    if (!r || !r.enabled) return;

    const parsed = this._parseInterval(r.schedule);
    if (!parsed) {
      r.nextRun = null;
      return;
    }

    const now = Date.now();

    if (parsed.type === 'interval') {
      r.nextRun = (r.lastRun || now) + parsed.ms;
      // If nextRun is in the past (first run or long pause), set to now
      if (r.nextRun < now) r.nextRun = now;
    } else if (parsed.type === 'daily') {
      const d = new Date();
      d.setHours(parsed.hour, parsed.minute, 0, 0);
      if (d.getTime() <= now) d.setDate(d.getDate() + 1);
      r.nextRun = d.getTime();
    }
  }

  // --- Conditions ---

  /**
   * Check optional conditions before running
   * conditions.quietHours: { start: 23, end: 8 } — skip during these hours
   * conditions.minInterval: ms — don't run more often than this
   * conditions.custom: function returning boolean
   */
  _checkConditions(routine) {
    const c = routine.conditions;
    if (!c) return true;

    const now = new Date();

    // Quiet hours
    if (c.quietHours) {
      const hour = now.getHours();
      const { start, end } = c.quietHours;
      if (start > end) {
        // Wraps midnight: e.g. 23-8
        if (hour >= start || hour < end) return false;
      } else {
        if (hour >= start && hour < end) return false;
      }
    }

    // Min interval
    if (c.minInterval && routine.lastRun) {
      if (Date.now() - routine.lastRun < c.minInterval) return false;
    }

    // Custom check
    if (typeof c.custom === 'function') {
      try { return c.custom(routine); } catch { return false; }
    }

    return true;
  }

  // --- Tick ---

  async _tick() {
    const now = Date.now();

    for (const [id, routine] of this.routines) {
      if (!routine.enabled) continue;
      if (!routine.nextRun || routine.nextRun > now) continue;
      if (!this._checkConditions(routine)) {
        this._calcNextRun(id);
        continue;
      }

      // Execute
      const entry = {
        id: routine.id,
        startedAt: now,
        status: 'running',
        error: null,
        result: null,
        duration: 0
      };

      try {
        this._emit('routine:start', { id });
        const result = await routine.action(routine);
        entry.status = 'ok';
        entry.result = result;
      } catch (err) {
        entry.status = 'error';
        entry.error = err.message || String(err);
        routine.errors++;
        this._emit('routine:error', { id, error: entry.error });
      }

      entry.duration = Date.now() - now;
      routine.lastRun = Date.now();
      routine.runCount++;
      this._calcNextRun(id);

      // History
      this.history.push(entry);
      if (this.history.length > this.maxHistory) {
        this.history = this.history.slice(-this.maxHistory);
      }

      this._emit('routine:done', { id, status: entry.status, duration: entry.duration });
    }
  }

  // --- Persistence ---

  /**
   * Export state to JSON (for saving to disk)
   */
  exportState() {
    const routines = {};
    for (const [id, r] of this.routines) {
      routines[id] = {
        id: r.id,
        name: r.name,
        schedule: r.schedule,
        model: r.model,
        enabled: r.enabled,
        conditions: r.conditions && r.conditions.quietHours ? { quietHours: r.conditions.quietHours } : {},
        lastRun: r.lastRun,
        runCount: r.runCount,
        errors: r.errors
      };
    }
    return { routines, history: this.history.slice(-50) };
  }

  /**
   * Restore timing state from saved data (call after re-adding routines)
   */
  restoreState(state) {
    if (!state || !state.routines) return;
    for (const [id, saved] of Object.entries(state.routines)) {
      const r = this.routines.get(id);
      if (r) {
        r.lastRun = saved.lastRun;
        r.runCount = saved.runCount || 0;
        r.errors = saved.errors || 0;
        this._calcNextRun(id);
      }
    }
    if (state.history) {
      this.history = state.history;
    }
  }

  /**
   * Get execution history
   */
  getHistory(limit = 20) {
    return this.history.slice(-limit);
  }
}

module.exports = { RoutineManager };
