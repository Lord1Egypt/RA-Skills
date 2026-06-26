#!/usr/bin/env node
import { runScript } from './lib/cli.js';
import { execute } from './lib/status.js';

const HELP = `Query an image generation task or batch.

Usage:
  node {baseDir}/scripts/status-image.js --task-id <task-id>
  node {baseDir}/scripts/status-image.js --batch-id <batch-id>

Options:
  --task-id <id>   Query a single task
  --batch-id <id>  Query a batch
  --verbose        Print debug info to stderr
  --help           Show this help message
`;

runScript(process.argv.slice(2), execute, HELP);
