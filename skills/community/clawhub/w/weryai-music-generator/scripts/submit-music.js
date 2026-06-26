#!/usr/bin/env node

import { runScript } from './lib/cli.js';
import { execute } from './lib/submit.js';

const HELP = `Usage: node {baseDir}/scripts/submit-music.js [options]

Options:
  --json <data>    Pass parameters as a JSON string (use "-" for stdin)
  --dry-run        Preview the request without calling the API
  --verbose        Print debug info to stderr
  --help           Show this help message

Examples:
  node {baseDir}/scripts/submit-music.js --json '{"type":"VOCAL_SONG","description":"A warm pop song","gender":"f"}'
  node {baseDir}/scripts/submit-music.js --json '{"type":"ONLY_MUSIC","styles":{"CLASSIC":"classical","PIANO":"piano"}}' --dry-run
`;

await runScript(process.argv.slice(2), execute, HELP);
