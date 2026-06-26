#!/usr/bin/env node

import { runScript } from './lib/cli.js';
import { execute } from './lib/status.js';

const HELP = `Usage: node {baseDir}/scripts/status-music.js --task-id <task-id> [options]

Options:
  --task-id <id>   Query an existing WeryAI music task
  --verbose        Print debug info to stderr
  --help           Show this help message

Examples:
  node {baseDir}/scripts/status-music.js --task-id task_abc123
`;

await runScript(process.argv.slice(2), execute, HELP);
