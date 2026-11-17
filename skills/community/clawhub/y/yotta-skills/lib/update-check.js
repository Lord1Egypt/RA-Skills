'use strict';

const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');

const CACHE_VERSION = 1;
const CHECK_INTERVAL_MS = 7 * 24 * 60 * 60 * 1000;
const MAX_JITTER_MS = 24 * 60 * 60 * 1000;

function emptyCache() {
  return { version: CACHE_VERSION, targets: {} };
}

function cachePath(homeDir) {
  return path.join(homeDir || os.homedir(), '.yottaskills', 'update-check.json');
}

function targetKey(dest) {
  return crypto.createHash('sha256').update(path.resolve(dest)).digest('hex').slice(0, 24);
}

function readCache(homeDir) {
  try {
    const parsed = JSON.parse(fs.readFileSync(cachePath(homeDir), 'utf8'));
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) return emptyCache();
    if (!parsed.targets || typeof parsed.targets !== 'object' || Array.isArray(parsed.targets)) {
      return emptyCache();
    }
    return {
      version: CACHE_VERSION,
      targets: { ...parsed.targets },
    };
  } catch (_) {
    return emptyCache();
  }
}

function writeCache(homeDir, cache) {
  const file = cachePath(homeDir);
  const dir = path.dirname(file);
  fs.mkdirSync(dir, { recursive: true });
  const tmp = file + '.tmp-' + process.pid + '-' + Date.now();
  fs.writeFileSync(tmp, JSON.stringify(cache, null, 2) + '\n', 'utf8');
  try {
    fs.renameSync(tmp, file);
  } catch (_) {
    fs.rmSync(file, { force: true });
    fs.renameSync(tmp, file);
  }
  return file;
}

function isDue(record, now) {
  if (!record || typeof record.next_check !== 'string') return true;
  const dueAt = Date.parse(record.next_check);
  if (!Number.isFinite(dueAt)) return true;
  return dueAt <= Number(now);
}

function nextCheckAt(now, random) {
  const base = now instanceof Date ? now.getTime() : Number(now);
  const value = Math.min(1, Math.max(0, Number(typeof random === 'function' ? random() : random)));
  const jitter = Math.floor((Number.isFinite(value) ? value : 0) * MAX_JITTER_MS);
  return new Date(base + CHECK_INTERVAL_MS + jitter).toISOString();
}

function recordCheck(homeDir, dest, options) {
  const opts = options || {};
  const now = opts.now === undefined ? Date.now() : opts.now;
  const checkedAt = new Date(now).toISOString();
  const cache = readCache(homeDir);
  const key = targetKey(dest);
  const record = {
    dest: path.resolve(dest),
    last_checked: checkedAt,
    next_check: nextCheckAt(now, opts.random),
    last_result: opts.result || null,
    last_error: opts.error ? String(opts.error) : null,
  };
  cache.targets[key] = record;
  writeCache(homeDir, cache);
  return record;
}

module.exports = {
  CACHE_VERSION,
  CHECK_INTERVAL_MS,
  MAX_JITTER_MS,
  cachePath,
  emptyCache,
  isDue,
  nextCheckAt,
  readCache,
  recordCheck,
  targetKey,
  writeCache,
};
