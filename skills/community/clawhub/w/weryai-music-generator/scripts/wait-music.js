#!/usr/bin/env node

import { runScript } from './lib/cli.js';
import { execute } from './lib/wait.js';

const HELP = `Usage: node {baseDir}/scripts/wait-music.js [options]

Options:
  --json <data>    Pass parameters as a JSON string (use "-" for stdin)
  --dry-run        Preview the request without calling the API
  --verbose        Print debug info to stderr
  --help           Show this help message

Examples:
  node {baseDir}/scripts/wait-music.js --json '{"type":"VOCAL_SONG","description":"An energetic rock anthem","styles":{"ROCK":"rock","EXCITED":"excited"}}'
  node {baseDir}/scripts/wait-music.js --json '{"type":"ONLY_MUSIC","description":"A calm ambient track"}' --dry-run
`;

await runScript(process.argv.slice(2), execute, HELP);
