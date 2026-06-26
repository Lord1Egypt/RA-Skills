#!/usr/bin/env node
// LDM OS Boot Hook Installer CLI
// Usage:
//   node install-cli.js           # install or update
//   node install-cli.js --status  # show current state
//   node install-cli.js --dry-run # preview without changes

import { detectInstallState, runInstallOrUpdate, formatStatus, formatResult } from './installer.mjs';

const args = process.argv.slice(2);

if (args.includes('--status')) {
  const state = detectInstallState();
  console.log(formatStatus(state));
  process.exit(0);
}

if (args.includes('--dry-run')) {
  const result = runInstallOrUpdate({ dryRun: true });
  console.log(formatResult(result));
  process.exit(0);
}

// Run install/update
const result = runInstallOrUpdate();
console.log(formatResult(result));
process.exit(0);
