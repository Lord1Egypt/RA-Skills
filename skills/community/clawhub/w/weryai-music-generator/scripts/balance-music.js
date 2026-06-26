#!/usr/bin/env node

import { runScript } from './lib/cli.js';
import { execute } from './lib/balance.js';

const HELP = `Usage: node {baseDir}/scripts/balance-music.js [options]

Options:
  --verbose        Print debug info to stderr
  --help           Show this help message

Examples:
  node {baseDir}/scripts/balance-music.js
`;

await runScript(process.argv.slice(2), execute, HELP);
