#!/usr/bin/env node

import { runScript } from './vendor/weryai-podcast/cli.js';
import { execute } from './vendor/weryai-podcast/wait.js';

const HELP = `Usage: node {baseDir}/scripts/wait.js [options]

Options:
  --json <data>    Pass parameters as a JSON string (use "-" for stdin)
  --dry-run        Preview the request flow without calling the API
  --verbose        Print debug info to stderr
  --help           Show this help message

Examples:
  node {baseDir}/scripts/wait.js --json '{"query":"What is retrieval augmented generation?","speakers":["travel-girl-english","leo-9328b6d2"],"language":"en","mode":"quick"}'
  node {baseDir}/scripts/wait.js --json '{"query":"Debate the tradeoffs of remote work","speakers":["travel-girl-english","leo-9328b6d2"],"language":"en","mode":"debate"}' --dry-run
`;

runScript(process.argv.slice(2), execute, HELP).catch(err => { console.error(err); process.exit(1); });
