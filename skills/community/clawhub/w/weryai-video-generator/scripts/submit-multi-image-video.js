#!/usr/bin/env node
import { runScript } from './lib/cli.js';
import { execute } from './lib/submit-multi-image.js';

const HELP = `Submit a multi-image-to-video generation task.

Usage:
  node scripts/submit-multi-image-video.js --json '{"prompt":"Create a transition","images":["https://example.com/1.png","https://example.com/2.png"],"duration":5}'

Options:
  --json <data>  Pass parameters as JSON string (use "-" for stdin)
  --dry-run      Preview the request without calling the API
  --verbose      Print debug info to stderr
  --help         Show this help message
`;

runScript(process.argv.slice(2), execute, HELP);
