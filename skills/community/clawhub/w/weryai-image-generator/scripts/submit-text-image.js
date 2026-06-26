#!/usr/bin/env node
import { runScript } from './lib/cli.js';
import { execute } from './lib/submit-text.js';

const HELP = `Submit a text-to-image generation task.

Usage:
  node {baseDir}/scripts/submit-text-image.js --json '{"prompt":"A sunset over the ocean"}'

Options:
  --json <data>  Pass parameters as JSON string (use "-" for stdin)
  --dry-run      Preview the request without calling the API
  --verbose      Print debug info to stderr
  --help         Show this help message
`;

runScript(process.argv.slice(2), execute, HELP);
