#!/usr/bin/env node
'use strict';

const path = require('path');
const { createSnapshot } = require('../lib/git');

const args = process.argv.slice(2);
const projectPath = args[0];
const description = args.slice(1).join(' ') || 'Auto snapshot';

if (!projectPath) {
  console.log(JSON.stringify({
    action: 'snapshot',
    status: 'error',
    error: 'missing_project_path',
    usage: 'node snapshot.js <project-path> [description]'
  }));
  process.exit(1);
}

const absPath = path.resolve(projectPath);

try {
  const result = createSnapshot(absPath, description);

  if (!result.success) {
    console.log(JSON.stringify({
      action: 'snapshot',
      status: 'error',
      error: result.message,
      project: absPath,
      description
    }));
    process.exit(1);
  }

  const output = {
    action: 'snapshot',
    status: 'success',
    committed: result.committed,
    project: absPath,
    description
  };
  if (result.data && result.data.hash) output.hash = result.data.hash;
  if (result.data && result.data.changedFiles) output.changedFiles = result.data.changedFiles;
  if (result.data && result.data.fileCount) output.fileCount = result.data.fileCount;

  console.log(JSON.stringify(output));

} catch (err) {
  console.log(JSON.stringify({
    action: 'snapshot',
    status: 'error',
    error: err.message,
    project: absPath
  }));
  process.exit(1);
}
