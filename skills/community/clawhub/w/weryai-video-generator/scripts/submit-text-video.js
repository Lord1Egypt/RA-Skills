#!/usr/bin/env node
import { runScript } from './lib/cli.js';
import { execute } from './lib/submit-text.js';

const HELP = `Submit a text-to-video generation task.

Usage:
  node scripts/submit-text-video.js --json '{"prompt":"A cat walking in a garden","duration":5}'

Options:
  --json <data>  Pass parameters as JSON string (use "-" for stdin)
  --dry-run      Preview the request without calling the API
  --verbose      Print debug info to stderr
  --help         Show this help message
`;

runScript(process.argv.slice(2), execute, HELP);
