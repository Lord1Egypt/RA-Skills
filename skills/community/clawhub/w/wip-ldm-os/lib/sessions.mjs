/**
 * lib/sessions.mjs
 * File-based session registration with PID liveness checks.
 * Enables multi-session awareness: agents can see who else is running.
 * Zero external dependencies.
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync, readdirSync, unlinkSync } from 'node:fs';
import { join, basename } from 'node:path';

const HOME = process.env.HOME || '';
const LDM_ROOT = join(HOME, '.ldm');
const SESSIONS_DIR = join(LDM_ROOT, 'sessions');

// ── Helpers ──

function readJSON(path) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return null;
  }
}

function writeJSON(path, data) {
  mkdirSync(join(path, '..'), { recursive: true });
  writeFileSync(path, JSON.stringify(data, null, 2) + '\n');
}

// ── PID liveness ──

/**
 * Check if a process with the given PID is still alive.
 * Uses signal 0 (no-op signal) to probe without affecting the process.
 */
export function isPidAlive(pid) {
  if (!pid || typeof pid !== 'number') return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

// ── Session management ──

/**
 * Register a session. Writes a JSON file to ~/.ldm/sessions/{name}.json.
 * @param {Object} opts
 * @param {string} opts.name - Session name (unique identifier)
 * @param {string} opts.agentId - Agent identifier (e.g. "cc-mini")
 * @param {number} opts.pid - Process ID of the session
 * @param {Object} [opts.meta] - Additional metadata
 */
export function registerSession({ name, agentId, pid, meta = {} }) {
  try {
    mkdirSync(SESSIONS_DIR, { recursive: true });
    const sessionPath = join(SESSIONS_DIR, `${name}.json`);
    const data = {
      name,
      agentId: agentId || 'unknown',
      pid: pid || process.pid,
      startTime: new Date().toISOString(),
      cwd: meta?.cwd || process.cwd(),
      meta: meta || {},
    };
    writeJSON(sessionPath, data);
    return data;
  } catch {
    return null;
  }
}

/**
 * Deregister a session. Removes the session file.
 * @param {string} name - Session name
 */
export function deregisterSession(name) {
  try {
    const sessionPath = join(SESSIONS_DIR, `${name}.json`);
    if (existsSync(sessionPath)) {
      unlinkSync(sessionPath);
      return true;
    }
    return false;
  } catch {
    return false;
  }
}

/**
 * List all sessions. Validates PID liveness and optionally cleans stale entries.
 * @param {Object} [opts]
 * @param {string} [opts.agentId] - Filter by agent ID
 * @param {boolean} [opts.includeStale] - Include sessions with dead PIDs
 * @returns {Array} Array of session objects with `alive` field
 */
export function listSessions({ agentId, includeStale } = {}) {
  try {
    if (!existsSync(SESSIONS_DIR)) return [];

    const files = readdirSync(SESSIONS_DIR).filter(f => f.endsWith('.json'));
    const sessions = [];

    for (const file of files) {
      const sessionPath = join(SESSIONS_DIR, file);
      const data = readJSON(sessionPath);
      if (!data) continue;

      const alive = isPidAlive(data.pid);

      // Clean stale entries unless asked to include them
      if (!alive && !includeStale) {
        try { unlinkSync(sessionPath); } catch {}
        continue;
      }

      const session = { ...data, alive };

      // Filter by agentId if specified
      if (agentId && data.agentId !== agentId) continue;

      sessions.push(session);
    }

    return sessions;
  } catch {
    return [];
  }
}

/**
 * Count live sessions for a given agent.
 * @param {string} [agentId] - Agent ID to count. If omitted, counts all.
 * @returns {number}
 */
export function sessionCount(agentId) {
  try {
    const sessions = listSessions({ agentId });
    return sessions.filter(s => s.alive).length;
  } catch {
    return 0;
  }
}
