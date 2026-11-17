// @ts-check

/**
 * Session recovery module for SPM v4.
 *
 * Reads heartbeat logs produced by the heartbeat manager and generates
 * structured recovery reports that allow a halted or resumed session to
 * reconstruct its execution state: the active task, the last checkpoint,
 * completed tasks, and accumulated context.
 *
 * @module session/index
 */

import { readAll, getBySession } from './heartbeat.js';

/**
 * @typedef {import('./heartbeat.js').Heartbeat} Heartbeat
 */

/**
 * @typedef {Object} RecoveryReport
 * @property {string}          sessionId     – The session being recovered
 * @property {Heartbeat|null}  activeTask    – The most recently active task (or null)
 * @property {Heartbeat|null}  lastCheckpoint– The most recent checkpoint heartbeat (or null)
 * @property {Heartbeat[]}     completedTasks– Heartbeats whose status is "completed"
 * @property {number}          totalHeartbeats– Total heartbeats processed
 * @property {string[]}        contextNotes  – Accumulated notes from all heartbeats
 */

/**
 * Determine whether a heartbeat qualifies as a checkpoint.
 *
 * A heartbeat is considered a checkpoint when its status is one of the
 * recognised stable states, or when the note explicitly mentions
 * "checkpoint", "save", or "snapshot".
 *
 * @param {Heartbeat} hb – A heartbeat entry
 * @returns {boolean} True when the heartbeat is a checkpoint
 */
function isCheckpoint(hb) {
  const stableStatuses = ['completed', 'paused', 'checkpoint'];
  if (stableStatuses.includes(hb.status)) {
    return true;
  }
  if (hb.note) {
    const lower = hb.note.toLowerCase();
    return (
      lower.includes('checkpoint') ||
      lower.includes('save') ||
      lower.includes('snapshot')
    );
  }
  return false;
}

/**
 * Generate a recovery report from a heartbeat log file.
 *
 * The report is derived solely from the persisted heartbeat entries.
 * It identifies:
 * - The currently active task (latest heartbeat overall)
 * - The most recent checkpoint
 * - All tasks that reached a "completed" status
 * - Accumulated context notes for continuity
 *
 * @param {string} [heartbeatFile] – Path to the heartbeat JSON-lines file.
 *        Defaults to the same default used by the heartbeat module.
 * @returns {RecoveryReport} Structured recovery report
 */
export function generateRecoveryReport(heartbeatFile) {
  const all = readAll(heartbeatFile);

  if (all.length === 0) {
    return {
      sessionId: '',
      activeTask: null,
      lastCheckpoint: null,
      completedTasks: [],
      totalHeartbeats: 0,
      contextNotes: [],
    };
  }

  const latest = all[all.length - 1];
  const sessionId = latest.sessionId;

  // Walk backwards to find the most recent checkpoint before (or at) the end.
  let lastCheckpoint = null;
  for (let i = all.length - 1; i >= 0; i--) {
    if (isCheckpoint(all[i])) {
      lastCheckpoint = all[i];
      break;
    }
  }

  const completedTasks = all.filter((hb) => hb.status === 'completed');
  const contextNotes = all
    .filter((hb) => hb.note)
    .map((hb) => `[${hb.timestamp}] ${hb.note}`);

  return {
    sessionId,
    activeTask: latest,
    lastCheckpoint,
    completedTasks,
    totalHeartbeats: all.length,
    contextNotes,
  };
}

/**
 * Retrieve the heartbeat that falls nearest to (or exactly at) a given
 * timestamp.
 *
 * The function searches the entire log and returns the heartbeat whose
 * timestamp is closest to the target **without exceeding it** (i.e. the
 * latest heartbeat ≤ `timestamp`).  If all heartbeats are *after* the
 * target, the earliest entry is returned.
 *
 * @param {string}       timestamp      – ISO-8601 timestamp to look up
 * @param {string}       [heartbeatFile]– Path to the heartbeat log file
 * @returns {Heartbeat | null} The matching heartbeat, or null if the log is empty
 */
export function getCheckpoint(timestamp, heartbeatFile) {
  const all = readAll(heartbeatFile);
  if (all.length === 0) {
    return null;
  }

  const target = new Date(timestamp).getTime();

  // Walk backwards returning the first entry ≤ target.
  for (let i = all.length - 1; i >= 0; i--) {
    if (new Date(all[i].timestamp).getTime() <= target) {
      return all[i];
    }
  }

  // All heartbeats are after the target; return the earliest.
  return all[0];
}