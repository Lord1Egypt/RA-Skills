#!/usr/bin/env node

import { runScript } from './vendor/weryai-podcast/cli.js';
import { execute } from './vendor/weryai-podcast/speakers.js';

const HELP = `Usage: node {baseDir}/scripts/speakers.js [options]

Options:
  --language <code>  Required language code such as en, zh, or ja
  --verbose          Print debug info to stderr
  --help             Show this help message

Examples:
  node {baseDir}/scripts/speakers.js --language en
  node {baseDir}/scripts/speakers.js --language zh
`;

runScript(process.argv.slice(2), execute, HELP).catch(err => { console.error(err); process.exit(1); });
