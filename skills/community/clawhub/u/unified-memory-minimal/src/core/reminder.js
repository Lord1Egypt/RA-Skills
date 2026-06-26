/**
 * Memory Reminder System
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const REMINDER_DIR = join(MEMORY_DIR, 'reminders');

function getReminderFile() {
  mkdirSync(REMINDER_DIR, { recursive: true });
  return join(REMINDER_DIR, 'reminders.json');
}

function loadReminders() {
  const file = getReminderFile();
  if (!existsSync(file)) return [];
  try { return JSON.parse(readFileSync(file, 'utf-8')); }
  catch { return []; }
}

function saveReminders(reminders) {
  writeFileSync(getReminderFile(), JSON.stringify(reminders, null, 2), 'utf-8');
}

export function createReminder(data) {
  const reminders = loadReminders();
  const reminder = {
    id: `remind_${Date.now()}_${Math.random().toString(36).substring(2, 6)}`,
    memoryId: data.memoryId,
    text: data.text,
    remindAt: data.remindAt,
    repeatInterval: data.repeatInterval,
    triggered: false,
    createdAt: new Date().toISOString(),
  };
  reminders.push(reminder);
  saveReminders(reminders);
  return reminder;
}

export function getPendingReminders() {
  const reminders = loadReminders();
  const now = new Date().toISOString();
  return reminders.filter(r => !r.triggered && r.remindAt <= now);
}

export function getAllReminders() {
  return loadReminders();
}

export function triggerReminder(id) {
  const reminders = loadReminders();
  const reminder = reminders.find(r => r.id === id);
  if (!reminder) return false;
  reminder.triggered = true;
  saveReminders(reminders);
  return true;
}

export function getReminderStats() {
  const reminders = loadReminders();
  return { total: reminders.length, pending: reminders.filter(r => !r.triggered).length, triggered: reminders.filter(r => r.triggered).length };
}

export function printReminderStatus() {
  const stats = getReminderStats();
  const pending = getPendingReminders();
  console.log('\n⏰ Memory Reminder Status\n');
  console.log(`  Total: ${stats.total}`);
  console.log(`  Pending: ${stats.pending}`);
  console.log(`  Triggered: ${stats.triggered}\n`);
  if (pending.length > 0) {
    console.log('  📋 Pending Reminders:');
    for (const r of pending.slice(0, 5)) console.log(`    - ${r.text} at ${r.remindAt}`);
  }
  console.log('');
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === 'check') { const pending = getPendingReminders(); pending.forEach(r => triggerReminder(r.id)); console.log(`🔔 Triggered ${pending.length} reminders`); }
  else printReminderStatus();
}
