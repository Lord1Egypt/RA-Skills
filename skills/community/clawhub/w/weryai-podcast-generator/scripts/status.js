#!/usr/bin/env node

import { runScript } from './vendor/weryai-podcast/cli.js';
import { execute } from './vendor/weryai-podcast/status.js';

const HELP = `Usage: node {baseDir}/scripts/status.js [options]

Options:
  --task-id <id>  Required podcast task ID
  --verbose       Print debug info to stderr
  --help          Show this help message

Examples:
  node {baseDir}/scripts/status.js --task-id <task-id>
`;

runScript(process.argv.slice(2), execute, HELP).catch(err => { console.error(err); process.exit(1); });
