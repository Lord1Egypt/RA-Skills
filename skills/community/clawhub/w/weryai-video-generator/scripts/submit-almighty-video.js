#!/usr/bin/env node
import { runScript } from './lib/cli.js';
import { execute } from './lib/submit-almighty.js';

const HELP = `Submit an almighty-reference-to-video generation task.

Usage:
  node {baseDir}/scripts/submit-almighty-video.js --json '{"model":"SEEDANCE_2_0","prompt":"Use image and video refs","images":["https://example.com/1.png"],"videos":["https://example.com/1.mp4"],"duration":5}'

Options:
  --json <data>  Pass parameters as JSON string (use "-" for stdin)
  --dry-run      Preview the request without calling the API
  --verbose      Print debug info to stderr
  --help         Show this help message
`;

runScript(process.argv.slice(2), execute, HELP);
