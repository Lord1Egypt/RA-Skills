#!/usr/bin/env node

import { runScript } from './vendor/weryai-podcast/cli.js';
import { execute } from './vendor/weryai-podcast/generate-audio.js';

const HELP = `Usage: node {baseDir}/scripts/generate-audio.js [options]

Options:
  --task-id <id>    Required podcast task ID
  --json <data>     Optional JSON body (use "-" for stdin)
  --dry-run         Preview the request without calling the API
  --verbose         Print debug info to stderr
  --help            Show this help message

Examples:
  node {baseDir}/scripts/generate-audio.js --task-id <task-id>
  node {baseDir}/scripts/generate-audio.js --task-id <task-id> --json '{"scripts":[{"speakerId":"travel-girl-english","speakerName":"Mia","content":"Welcome back."}]}'
`;

runScript(process.argv.slice(2), execute, HELP).catch(err => { console.error(err); process.exit(1); });
