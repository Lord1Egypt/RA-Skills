'use strict';
const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');
const scanLib = require('./skills-scan');

function nowTag() {
  return new Date().toISOString().replace(/[:.]/g, '-');
}

function snapshotRoot(homeDir, slug) {
  return path.join(homeDir || os.homedir(), '.yottaskills', 'snapshots', slug);
}

function copyTree(src, dst) {
  fs.rmSync(dst, { recursive: true, force: true });
  fs.mkdirSync(dst, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const from = path.join(src, entry.name);
    const to = path.join(dst, entry.name);
    if (entry.isDirectory()) copyTree(from, to);
    else if (entry.isFile()) fs.copyFileSync(from, to);
  }
}

function renameWithRetry(from, to, options) {
  const rename = (options && options.rename) || fs.renameSync;
  let lastError;
  for (let attempt = 0; attempt < 5; attempt++) {
    try {
      return rename(from, to);
    } catch (error) {
      lastError = error;
      if (!['EPERM', 'EACCES', 'EBUSY'].includes(error.code) || attempt === 4) throw error;
    }
  }
  throw lastError;
}

function walkFiles(root, current, output) {
  const dir = current || root;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walkFiles(root, full, output);
    else if (entry.isFile()) output.push(full);
  }
}

function computeTreeDigest(root) {
  const files = [];
  walkFiles(path.resolve(root), null, files);
  files.sort((a, b) => path.relative(root, a).localeCompare(path.relative(root, b)));
  const hash = crypto.createHash('sha256');
  for (const file of files) {
    const relative = path.relative(root, file).replace(/\\/g, '/');
    hash.update(relative, 'utf8');
    hash.update('\0', 'utf8');
    hash.update(fs.readFileSync(file));
    hash.update('\0', 'utf8');
  }
  return { digest: hash.digest('hex'), files };
}

function writeJsonAtomic(file, value) {
  const tmp = file + '.tmp-' + process.pid;
  fs.writeFileSync(tmp, JSON.stringify(value, null, 2) + '\n', 'utf8');
  fs.renameSync(tmp, file);
}

function readVersion(root) {
  try {
    const fm = scanLib.parseFrontmatter(fs.readFileSync(path.join(root, 'SKILL.md'), 'utf8'));
    return fm && fm.version ? String(fm.version).trim() : null;
  } catch (_) {
    return null;
  }
}

function validateSnapshot(snapshot) {
  const root = path.resolve(snapshot || '');
  if (!snapshot || !fs.existsSync(root)) {
    return { ok: false, version: null, digest: null, legacy: false, reason: '快照目录不存在', source: null, createdAt: null };
  }
  if (!fs.statSync(root).isDirectory()) {
    return { ok: false, version: null, digest: null, legacy: false, reason: '快照不是目录', source: null, createdAt: null };
  }
  const metaFile = root + '.meta.json';
  if (fs.existsSync(metaFile)) {
    let metadata;
    try {
      metadata = JSON.parse(fs.readFileSync(metaFile, 'utf8'));
    } catch (error) {
      return { ok: false, version: null, digest: null, legacy: false, reason: '快照元数据无法解析: ' + error.message, source: null, createdAt: null };
    }
    let current;
    try {
      current = computeTreeDigest(root);
    } catch (error) {
      return {
        ok: false,
        version: metadata.version || null,
        digest: metadata.digest || null,
        legacy: false,
        reason: '快照不可读: ' + error.message,
        source: metadata.source || null,
        createdAt: metadata.created_at || null,
      };
    }
    if (!metadata.digest || current.digest !== metadata.digest) {
      return {
        ok: false,
        version: metadata.version || readVersion(root),
        digest: metadata.digest || null,
        legacy: false,
        reason: '快照摘要不一致，可能已被修改',
        source: metadata.source || null,
        createdAt: metadata.created_at || null,
      };
    }
    return {
      ok: true,
      version: metadata.version || readVersion(root),
      digest: metadata.digest,
      legacy: false,
      reason: null,
      source: metadata.source || null,
      createdAt: metadata.created_at || null,
    };
  }

  const version = readVersion(root);
  if (!fs.existsSync(path.join(root, 'SKILL.md'))) {
    return { ok: false, version, digest: null, legacy: true, reason: '旧快照缺少 SKILL.md', source: null, createdAt: null };
  }
  return { ok: true, version, digest: null, legacy: true, reason: null, source: null, createdAt: null };
}

function createSnapshot(target, options) {
  const opts = options || {};
  if (!target || !fs.existsSync(target) || !fs.statSync(target).isDirectory()) {
    throw new Error('无法创建快照：目标目录不存在');
  }
  const slug = opts.slug || path.basename(target);
  const root = snapshotRoot(opts.homeDir, slug);
  fs.mkdirSync(root, { recursive: true });
  const version = opts.version || readVersion(target) || 'unknown';
  const snapshot = fs.mkdtempSync(path.join(root, nowTag() + '-' + version + '-'));
  const copyDir = opts.copyDir || copyTree;
  try {
    copyDir(target, snapshot);
    const integrity = computeTreeDigest(snapshot);
    const metadata = {
      schema: 1,
      slug,
      version,
      created_at: new Date().toISOString(),
      source: path.resolve(target),
      digest: integrity.digest,
      files: integrity.files.length,
    };
    writeJsonAtomic(snapshot + '.meta.json', metadata);
    return {
      path: snapshot,
      version,
      digest: integrity.digest,
      files: integrity.files.length,
      metadata,
    };
  } catch (error) {
    fs.rmSync(snapshot, { recursive: true, force: true });
    throw error;
  }
}

function listSnapshots(homeDir, slug) {
  const roots = [];
  if (slug) {
    roots.push({ slug, dir: snapshotRoot(homeDir, slug) });
  } else {
    const base = path.join(homeDir || os.homedir(), '.yottaskills', 'snapshots');
    if (fs.existsSync(base)) {
      for (const entry of fs.readdirSync(base, { withFileTypes: true })) {
        if (entry.isDirectory()) roots.push({ slug: entry.name, dir: path.join(base, entry.name) });
      }
    }
  }

  const rows = [];
  for (const root of roots) {
    if (!fs.existsSync(root.dir)) continue;
    for (const entry of fs.readdirSync(root.dir, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const snapshot = path.join(root.dir, entry.name);
      const validation = validateSnapshot(snapshot);
      let mtimeMs = 0;
      try { mtimeMs = fs.statSync(snapshot).mtimeMs; } catch (_) { /* keep 0 */ }
      rows.push({
        path: snapshot,
        name: entry.name,
        slug: root.slug,
        valid: validation.ok,
        version: validation.version,
        legacy: validation.legacy,
        reason: validation.reason,
        source: validation.source || null,
        createdAt: validation.createdAt || null,
        mtime_ms: mtimeMs,
      });
    }
  }
  rows.sort((a, b) => (b.mtime_ms - a.mtime_ms) || b.name.localeCompare(a.name));
  return rows;
}

function restoreSnapshot(snapshot, target, options) {
  const validation = validateSnapshot(snapshot);
  if (!validation.ok) {
    return { ok: false, version: validation.version, error: validation.reason || '快照校验失败' };
  }
  const opts = options || {};
  const destination = path.dirname(path.resolve(target));
  const base = path.basename(path.resolve(target));
  const copyDir = opts.copyDir || copyTree;
  const staging = path.join(destination, '.yottaskills-rollback-' + base + '-' + process.pid + '-' + Date.now());
  const backup = path.join(destination, '.yottaskills-rollback-backup-' + base + '-' + process.pid + '-' + Date.now());
  let movedCurrent = false;
  try {
    fs.mkdirSync(destination, { recursive: true });
    copyDir(snapshot, staging);
    if (fs.existsSync(target)) {
      renameWithRetry(target, backup, opts);
      movedCurrent = true;
    }
    renameWithRetry(staging, target, opts);
    if (movedCurrent && fs.existsSync(backup)) fs.rmSync(backup, { recursive: true, force: true });
    return { ok: true, version: validation.version, error: null, snapshot };
  } catch (error) {
    try {
      if (fs.existsSync(target) && movedCurrent) fs.rmSync(target, { recursive: true, force: true });
      if (movedCurrent && fs.existsSync(backup)) renameWithRetry(backup, target, opts);
    } catch (_) {
      // Preserve both the failure and any recovered tree for manual inspection.
    }
    if (fs.existsSync(staging)) fs.rmSync(staging, { recursive: true, force: true });
    return { ok: false, version: validation.version, error: error.message, snapshot };
  }
}

module.exports = {
  snapshotRoot,
  copyTree,
  computeTreeDigest,
  createSnapshot,
  validateSnapshot,
  listSnapshots,
  restoreSnapshot,
  renameWithRetry,
};
