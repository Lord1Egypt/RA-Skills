/**
 * Reminder Scheduler v1.0
 * Proactive reminder mechanism
 * Supports: one-time reminders, recurring reminders, memory TTL-based auto reminders
 */

import { getAllMemories } from './storage.js';

let log = console;
try {
  const { log: importedLog } = await import('./logger.js');
  log = importedLog;
} catch {
  // Use console if logger not available
}

export class ReminderScheduler {
  constructor() {
    this.reminders = new Map(); // id -> { id, text, dueAt, repeat, callback, type }
    this.timer = null;
    this.tickMs = 30000; // Check every 30 seconds
  }

  add(reminder) {
    const id = `rem_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`;
    this.reminders.set(id, { id, ...reminder, createdAt: Date.now() });
    return id;
  }

  addTTLReminder(memoryId, text, ttlHours = 24) {
    // TTL-based auto reminder for memories
    return this.add({
      type: 'ttl',
      memoryId,
      text,
      dueAt: Date.now() + ttlHours * 3600 * 1000,
      repeat: null,
    });
  }

  addRecurringReminder(text, intervalHours = 24) {
    // Recurring reminder (e.g., daily review)
    return this.add({
      type: 'recurring',
      text,
      dueAt: Date.now() + intervalHours * 3600 * 1000,
      repeat: intervalHours * 3600 * 1000,
    });
  }

  due() {
    const now = Date.now();
    return [...this.reminders.values()].filter(r => r.dueAt <= now);
  }

  async tick() {
    const due = this.due();
    for (const reminder of due) {
      try {
        // Trigger callback if registered
        if (reminder.callback) {
          await reminder.callback(reminder);
        }
        // Re-schedule if recurring
        if (reminder.repeat) {
          reminder.dueAt = Date.now() + reminder.repeat;
        } else {
          this.reminders.delete(reminder.id);
        }
      } catch (e) {
        console.error('[ReminderScheduler] trigger error:', e.message);
      }
    }
  }

  start() {
    if (this.timer) return;
    this.timer = setInterval(() => this.tick(), this.tickMs);
  }

  stop() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }

  list() {
    return [...this.reminders.values()];
  }

  cancel(id) {
    return this.reminders.delete(id);
  }
}

let globalScheduler = null;

export function getReminderScheduler() {
  if (!globalScheduler) {
    globalScheduler = new ReminderScheduler();
  }
  return globalScheduler;
}
