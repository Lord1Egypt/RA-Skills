#!/usr/bin/env node
'use strict';

const path = require('path');
const fs = require('fs');
const { createSnapshot, isTracked, initProject } = require('../lib/git');

const args = process.argv.slice(2);
const projectPath = args[0];

const DEBOUNCE_MS = parseInt(process.env.UNDO_WATCHER_DEBOUNCE || '5000', 10);
const POLL_INTERVAL_MS = parseInt(process.env.UNDO_WATCHER_POLL || '2000', 10);

if (!projectPath) {
  console.log(JSON.stringify({
    action: 'watcher-start',
    status: 'error',
    error: 'missing_project_path',
    usage: 'node watcher.js <project-path>'
  }));
  process.exit(1);
}

const absPath = path.resolve(projectPath);

const IGNORE_DIRS = new Set(['node_modules', '.git', '.DS_Store', 'dist', 'build', '.next', 'coverage', '.venv', 'venv']);
const IGNORE_EXTS = new Set(['.log', '.tmp', '.swp', '.swo', '.pyc', '.pid']);

function shouldIgnore(filePath) {
  const parts = filePath.split(path.sep);
  for (const part of parts) {
    if (IGNORE_DIRS.has(part)) return true;
  }
  const ext = path.extname(filePath);
  if (IGNORE_EXTS.has(ext)) return true;
  return false;
}

function buildFileMap(dir, baseDir = '') {
  const files = {};
  if (!fs.existsSync(dir)) return files;
  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (IGNORE_DIRS.has(entry.name)) continue;
      const fullPath = path.join(dir, entry.name);
      const relativePath = path.join(baseDir, entry.name);
      if (shouldIgnore(relativePath)) continue;
      if (entry.isDirectory()) {
        Object.assign(files, buildFileMap(fullPath, relativePath));
      } else if (entry.isFile()) {
        try {
          const stat = fs.statSync(fullPath);
          files[relativePath] = { mtime: stat.mtimeMs, size: stat.size };
        } catch {}
      }
    }
  } catch {}
  return files;
}

let lastFileMap = buildFileMap(absPath);
let changeTimer = null;
let lastSnapshotTime = 0;

function detectChanges() {
  const currentFileMap = buildFileMap(absPath);
  const changed = [];
  const deleted = [];
  const added = [];

  for (const [file, info] of Object.entries(lastFileMap)) {
    if (!currentFileMap[file]) {
      deleted.push(file);
    } else if (currentFileMap[file].mtime !== info.mtime || currentFileMap[file].size !== info.size) {
      changed.push(file);
    }
  }
  for (const file of Object.keys(currentFileMap)) {
    if (!lastFileMap[file]) added.push(file);
  }

  lastFileMap = currentFileMap;

  const totalChanges = changed.length + deleted.length + added.length;
  if (totalChanges > 0) {
    if (changeTimer) clearTimeout(changeTimer);
    changeTimer = setTimeout(() => {
      const now = Date.now();
      if (now - lastSnapshotTime < DEBOUNCE_MS) return;

      const description = `[watcher] added: ${added.length}, modified: ${changed.length}, deleted: ${deleted.length}`;

      try {
        const result = createSnapshot(absPath, description);
        if (result.committed) {
          lastSnapshotTime = Date.now();
          console.log(JSON.stringify({
            action: 'watcher-snapshot',
            status: 'success',
            committed: true,
            project: absPath,
            hash: result.data?.hash || '',
            description,
            timestamp: new Date().toISOString(),
            files: {
              added: added.slice(0, 10),
              changed: changed.slice(0, 10),
              deleted: deleted.slice(0, 10)
            }
          }));
        }
      } catch (err) {
        console.log(JSON.stringify({
          action: 'watcher-snapshot',
          status: 'error',
          project: absPath,
          error: err.message
        }));
      }
    }, DEBOUNCE_MS);
  }
}

if (!isTracked(absPath)) {
  const result = initProject(absPath);
  if (!result.success) {
    console.log(JSON.stringify({
      action: 'watcher-start',
      status: 'error',
      error: 'init_failed',
      project: absPath,
      detail: result.message
    }));
    process.exit(1);
  }
}

console.log(JSON.stringify({
  action: 'watcher-start',
  status: 'success',
  project: absPath,
  pid: process.pid,
  debounceMs: DEBOUNCE_MS,
  pollMs: POLL_INTERVAL_MS
}));

setInterval(detectChanges, POLL_INTERVAL_MS);

process.on('SIGINT', () => {
  console.log(JSON.stringify({ action: 'watcher-stop', status: 'stopped', project: absPath }));
  if (changeTimer) clearTimeout(changeTimer);
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log(JSON.stringify({ action: 'watcher-stop', status: 'stopped', project: absPath }));
  if (changeTimer) clearTimeout(changeTimer);
  process.exit(0);
});
