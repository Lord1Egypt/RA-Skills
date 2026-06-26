#!/usr/bin/env node
'use strict';

const path = require('path');
const { getHistory, getCheckpoints, isTracked } = require('../lib/git');

const args = process.argv.slice(2);
const projectPath = args[0];

let limit = 20;

for (let i = 1; i < args.length; i++) {
  if (args[i] === '--limit' && args[i + 1]) {
    limit = parseInt(args[++i], 10);
  }
}

if (!projectPath) {
  console.log(JSON.stringify({
    action: 'list',
    status: 'error',
    error: 'missing_project_path',
    usage: 'node list.js <project-path> [--limit N]'
  }));
  process.exit(1);
}

const absPath = path.resolve(projectPath);

if (!isTracked(absPath)) {
  console.log(JSON.stringify({
    action: 'list',
    status: 'error',
    error: 'not_tracked',
    project: absPath
  }));
  process.exit(1);
}

try {
  const historyResult = getHistory(absPath, limit);
  const checkpointsResult = getCheckpoints(absPath);

  if (!historyResult.success) {
    console.log(JSON.stringify({
      action: 'list',
      status: 'error',
      error: historyResult.message,
      project: absPath
    }));
    process.exit(1);
  }

  const commits = historyResult.commits.map(c => ({
    hash: c.hash,
    date: c.date,
    timestamp: c.timestamp,
    description: c.description,
    files: c.files,
    isCheckpoint: c.isCheckpoint,
    isInitial: c.isInitial
  }));

  const checkpoints = (checkpointsResult.checkpoints || []).map(cp => ({
    name: cp.name,
    hash: cp.hash
  }));

  console.log(JSON.stringify({
    action: 'list',
    status: 'success',
    project: absPath,
    count: commits.length,
    commits,
    checkpoints
  }));

} catch (err) {
  console.log(JSON.stringify({
    action: 'list',
    status: 'error',
    error: err.message,
    project: absPath
  }));
  process.exit(1);
}
