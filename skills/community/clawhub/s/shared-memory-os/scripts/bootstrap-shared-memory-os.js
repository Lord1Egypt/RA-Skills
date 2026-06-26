#!/usr/bin/env node
const { execFileSync } = require('child_process');
const ROOT = '/home/zqh2333/.openclaw/workspace';

function run(cmd, args) {
  execFileSync(cmd, args, { cwd: ROOT, stdio: 'inherit' });
}

run('node', ['skills/shared-memory-os/scripts/init-shared-memory-os.js']);
run('node', ['skills/shared-memory-os/scripts/ensure-shared-memory-crons.js']);
run('node', ['skills/shared-memory-os/scripts/run-shared-memory-maintenance.js']);
