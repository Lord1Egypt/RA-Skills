#!/usr/bin/env node
'use strict';

const path = require('path');
const { undoSteps, undoToCheckpoint, undoToTimestamp, isTracked } = require('../lib/git');

const args = process.argv.slice(2);
const projectPath = args[0];

let steps = 1;
let toCheckpoint = null;
let toTimestamp = null;

for (let i = 1; i < args.length; i++) {
  if (args[i] === '--steps' && args[i + 1]) {
    steps = parseInt(args[++i], 10);
  } else if (args[i] === '--to' && args[i + 1]) {
    toCheckpoint = args[++i];
  } else if (args[i] === '--timestamp' && args[i + 1]) {
    toTimestamp = args[++i];
  }
}

if (!projectPath) {
  console.log(JSON.stringify({
    action: 'undo',
    status: 'error',
    error: 'missing_project_path',
    usage: 'node undo.js <project-path> [--steps N] [--to <checkpoint>] [--timestamp <ISO>]'
  }));
  process.exit(1);
}

const absPath = path.resolve(projectPath);

if (!isTracked(absPath)) {
  console.log(JSON.stringify({
    action: 'undo',
    status: 'error',
    error: 'not_tracked',
    project: absPath
  }));
  process.exit(1);
}

try {
  let result;
  let mode;

  if (toCheckpoint) {
    mode = 'checkpoint';
    result = undoToCheckpoint(absPath, toCheckpoint);
  } else if (toTimestamp) {
    mode = 'timestamp';
    result = undoToTimestamp(absPath, toTimestamp);
  } else {
    mode = 'steps';
    result = undoSteps(absPath, steps);
  }

  if (!result.success || !result.undone) {
    console.log(JSON.stringify({
      action: 'undo',
      status: 'error',
      error: result.message,
      mode,
      project: absPath,
      requested: toCheckpoint || toTimestamp || steps
    }));
    process.exit(1);
  }

  console.log(JSON.stringify({
    action: 'undo',
    status: 'success',
    undone: true,
    mode,
    project: absPath,
    targetHash: result.data?.targetHash || '',
    checkpointBranch: result.data?.checkpointBranch || '',
    ...(result.data || {})
  }));

} catch (err) {
  console.log(JSON.stringify({
    action: 'undo',
    status: 'error',
    error: err.message,
    project: absPath
  }));
  process.exit(1);
}
