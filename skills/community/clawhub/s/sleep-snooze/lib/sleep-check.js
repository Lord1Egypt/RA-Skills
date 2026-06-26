/**
 * sleep-check.js
 * Shared module: computes sleep state from CURRENT TIME + schedule.
 * Does NOT rely on the isSleeping flag in state.json (which requires
 * the cron job to have run correctly). Works even if cron is broken.
 */

const fs   = require('fs');
const path = require('path');

const STATE_FILE = path.join(
  process.env.HOME, '.openclaw', 'skills', 'sleep-snooze', 'data', 'state.json'
);

// ── Helpers ───────────────────────────────────────────────────────────────────

function parseHHMM(hhmm) {
  const [h, m] = hhmm.split(':').map(Number);
  return h * 60 + m; // minutes since midnight
}

function getCurrentMinutes(timezone) {
  const now = new Date();
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone: timezone,
    hour:     'numeric',
    minute:   'numeric',
    hour12:   false,
  }).formatToParts(now);

  // hour12:false returns "24" for midnight in some implementations
  const hour   = parseInt(parts.find(p => p.type === 'hour').value)   % 24;
  const minute = parseInt(parts.find(p => p.type === 'minute').value);
  return hour * 60 + minute;
}

function inWindow(currentMins, startMins, endMins) {
  if (startMins > endMins) {
    // Crosses midnight — e.g. 22:00 (1320) → 06:00 (360)
    return currentMins >= startMins || currentMins < endMins;
  }
  return currentMins >= startMins && currentMins < endMins;
}

// ── Public API ────────────────────────────────────────────────────────────────

/**
 * Load state from disk and compute whether sleep mode is currently active.
 * Returns { isSleeping, state } or throws if not configured.
 */
function loadSleepState() {
  const state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));

  // Manual override takes precedence (set by /sleep or /wake commands)
  if (state.manualOverride) {
    return { isSleeping: state.isSleeping, state };
  }

  // Compute from current time — cron-independent
  const currentMins    = getCurrentMinutes(state.timezone);
  const sleepStartMins = parseHHMM(state.sleepStart);
  const wakeMins       = parseHHMM(state.wakeTime);
  const isSleeping     = inWindow(currentMins, sleepStartMins, wakeMins);

  return { isSleeping, state };
}

module.exports = { loadSleepState, getCurrentMinutes, inWindow, parseHHMM };
