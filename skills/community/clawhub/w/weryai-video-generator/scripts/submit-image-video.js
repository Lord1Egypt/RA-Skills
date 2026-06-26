#!/usr/bin/env node
import { runScript } from './lib/cli.js';
import { execute } from './lib/submit-image.js';

const HELP = `Submit an image-to-video generation task.

Usage:
  node scripts/submit-image-video.js --json '{"prompt":"Add motion","image":"https://example.com/input.png","duration":5}'

Options:
  --json <data>  Pass parameters as JSON string (use "-" for stdin)
  --dry-run      Preview the request without calling the API
  --verbose      Print debug info to stderr
  --help         Show this help message
`;

runScript(process.argv.slice(2), execute, HELP);
