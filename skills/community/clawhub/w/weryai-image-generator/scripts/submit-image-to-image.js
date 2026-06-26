#!/usr/bin/env node
import { runScript } from './lib/cli.js';
import { execute } from './lib/submit-image.js';

const HELP = `Submit an image-to-image generation task.

Usage:
  node {baseDir}/scripts/submit-image-to-image.js --json '{"prompt":"Make it cinematic","images":["https://example.com/input.png"]}'

Options:
  --json <data>  Pass parameters as JSON string (use "-" for stdin)
  --dry-run      Preview the request without calling the API
  --verbose      Print debug info to stderr
  --help         Show this help message
`;

runScript(process.argv.slice(2), execute, HELP);
