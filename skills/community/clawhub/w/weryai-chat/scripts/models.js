#!/usr/bin/env node

import { runScript } from './vendor/weryai-text/cli.js';
import { executeModels } from './vendor/weryai-text/models.js';

const HELP = `Usage: node {baseDir}/scripts/models.js [options]

Options:
  --query <text>   Filter chat models by name or description
  --verbose        Print debug info to stderr
  --help           Show this help message

Examples:
  node {baseDir}/scripts/models.js
  node {baseDir}/scripts/models.js --query gpt
`;

await runScript(process.argv.slice(2), executeModels, HELP);
