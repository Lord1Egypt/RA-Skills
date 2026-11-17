'use strict';

// Session state is a reversible instruction overlay used by the analyzer and
// lifecycle hooks; it never mutates the installed skill files.
const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');

function stateDir() {
  if (process.env.SKILL_GUARD_STATE_DIR) return process.env.SKILL_GUARD_STATE_DIR;
  const base = process.env.XDG_STATE_HOME || (process.platform === 'win32'
    ? (process.env.LOCALAPPDATA || path.join(os.homedir(), 'AppData', 'Local'))
    : path.join(os.homedir(), '.local', 'state'));
  return path.join(base, 'skill-collision-guard');
}

function safeSessionId(value) {
  const source = String(value || 'default');
  return crypto.createHash('sha256').update(source).digest('hex').slice(0, 24);
}

function statePath(sessionId) {
  return path.join(stateDir(), 'sessions', `${safeSessionId(sessionId)}.json`);
}

function readSession(sessionId) {
  try {
    const value = JSON.parse(fs.readFileSync(statePath(sessionId), 'utf8'));
    return value && Array.isArray(value.suppressed) ? value : { suppressed: [] };
  } catch (_) {
    return { suppressed: [] };
  }
}

function writeSession(sessionId, value) {
  const file = statePath(sessionId);
  // Session suppression is intentionally persisted locally so lifecycle hooks
  // and the CLI share one reversible overlay. Only the hashed session filename
  // and selected skill names/paths are stored; no skill contents are written.
  const directory = path.dirname(file);
  fs.mkdirSync(directory, { recursive: true, mode: 0o700 });
  try { fs.chmodSync(directory, 0o700); } catch (_) {}
  const next = { session: safeSessionId(sessionId), updatedAt: new Date().toISOString(), suppressed: value.suppressed || [] };
  fs.writeFileSync(file, `${JSON.stringify(next, null, 2)}\n`, { encoding: 'utf8', mode: 0o600 });
  try { fs.chmodSync(file, 0o600); } catch (_) {}
  return next;
}

function suppress(sessionId, selectors) {
  const current = readSession(sessionId);
  current.suppressed = [...new Set([...current.suppressed, ...selectors.map(String)])].sort();
  return writeSession(sessionId, current);
}

function restore(sessionId, selectors = []) {
  const current = readSession(sessionId);
  if (!selectors.length) current.suppressed = [];
  else {
    const remove = new Set(selectors.map(String));
    current.suppressed = current.suppressed.filter((item) => !remove.has(item));
  }
  return writeSession(sessionId, current);
}

function clearSession(sessionId) {
  // SessionEnd removes exactly the hashed state file for this session. It does
  // not remove a skill, its directory, or any other user data.
  try { fs.unlinkSync(statePath(sessionId)); } catch (_) {}
}

module.exports = { clearSession, readSession, restore, safeSessionId, stateDir, statePath, suppress };
