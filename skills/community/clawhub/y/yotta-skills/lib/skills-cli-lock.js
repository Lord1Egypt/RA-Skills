'use strict';

/**
 * Read-only bridge for the official Vercel Labs `skills` CLI lock file.
 *
 * The lock is optional. When present, its source metadata is merged into the
 * YottaSkills Hub ledger so the Hub can show where a skill came from without
 * owning or rewriting the upstream lock.
 */

const fs = require('fs');
const os = require('os');
const path = require('path');

const LOCK_FILE = '.skill-lock.json';
const CURRENT_VERSION = 3;

function lockPath(options) {
  const opts = options || {};
  const home = opts.homeDir || os.homedir();
  const env = opts.env || process.env;
  if (env.XDG_STATE_HOME) return path.join(env.XDG_STATE_HOME, 'skills', LOCK_FILE);
  return path.join(home, '.agents', LOCK_FILE);
}

function readLock(options) {
  const file = lockPath(options);
  let value;
  try {
    value = JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (_) {
    return { available: false, path: file, version: null, skills: {} };
  }
  if (!value || typeof value !== 'object' || !value.skills || typeof value.skills !== 'object') {
    return { available: false, path: file, version: null, skills: {} };
  }
  return {
    available: true,
    path: file,
    version: Number(value.version || 0),
    compatible: Number(value.version || 0) >= CURRENT_VERSION,
    skills: value.skills,
    lastSelectedAgents: Array.isArray(value.lastSelectedAgents) ? value.lastSelectedAgents : [],
  };
}

module.exports = {
  LOCK_FILE,
  CURRENT_VERSION,
  lockPath,
  readLock,
};
