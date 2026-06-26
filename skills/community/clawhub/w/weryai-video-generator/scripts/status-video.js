#!/usr/bin/env node
import { runScript } from './lib/cli.js';
import { execute } from './lib/status.js';

const HELP = `Query a video generation task or batch.

Usage:
  node scripts/status-video.js --task-id <task-id>
  node scripts/status-video.js --batch-id <batch-id>

Options:
  --task-id <id>   Query a single task
  --batch-id <id>  Query a batch
  --verbose        Print debug info to stderr
  --help           Show this help message
`;

runScript(process.argv.slice(2), execute, HELP);
