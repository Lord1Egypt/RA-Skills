#!/usr/bin/env node
'use strict';

const path = require('path');
const { createCheckpoint, isTracked } = require('../lib/git');

const args = process.argv.slice(2);
const projectPath = args[0];
const checkpointName = args.slice(1).join('-').replace(/\s+/g, '-').toLowerCase() || null;

if (!projectPath || !checkpointName) {
  console.log(JSON.stringify({
    action: 'checkpoint',
    status: 'error',
    error: 'missing_args',
    usage: 'node checkpoint.js <project-path> <checkpoint-name>'
  }));
  process.exit(1);
}

const absPath = path.resolve(projectPath);

if (!isTracked(absPath)) {
  console.log(JSON.stringify({
    action: 'checkpoint',
    status: 'error',
    error: 'not_tracked',
    project: absPath
  }));
  process.exit(1);
}

try {
  const result = createCheckpoint(absPath, checkpointName);

  if (!result.success) {
    console.log(JSON.stringify({
      action: 'checkpoint',
      status: 'error',
      error: result.message,
      project: absPath,
      checkpoint: checkpointName
    }));
    process.exit(1);
  }

  console.log(JSON.stringify({
    action: 'checkpoint',
    status: 'success',
    project: absPath,
    checkpoint: checkpointName,
    branch: result.data?.branch || ''
  }));

} catch (err) {
  console.log(JSON.stringify({
    action: 'checkpoint',
    status: 'error',
    error: err.message,
    project: absPath
  }));
  process.exit(1);
}
