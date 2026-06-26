#!/usr/bin/env node
import { runScript } from './lib/cli.js';
import { execute } from './lib/balance.js';

const HELP = `Query the remaining WeryAI video balance.

Usage:
  node scripts/balance-video.js

Options:
  --verbose  Print debug info to stderr
  --help     Show this help message
`;

runScript(process.argv.slice(2), execute, HELP);
