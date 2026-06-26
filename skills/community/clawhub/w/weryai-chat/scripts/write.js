#!/usr/bin/env node

import { runScript } from './vendor/weryai-text/cli.js';
import { createWriteExecutor } from './vendor/weryai-text/write.js';

const HELP = `Usage: node {baseDir}/scripts/write.js [options]

Options:
  --json <data>    Pass parameters as a JSON string (use "-" for stdin)
  --dry-run        Preview the request without calling the API
  --verbose        Print debug info to stderr
  --help           Show this help message

Examples:
  node {baseDir}/scripts/write.js --json '{"prompt":"Explain retrieval augmented generation in plain English","temperature":0.7}'
  node {baseDir}/scripts/write.js --json '{"model":"GPT_5_4","messages":[{"role":"system","content":"You are concise."},{"role":"user","content":"Compare RAG and long-context prompting."}]}'
`;

await runScript(process.argv.slice(2), createWriteExecutor('chat'), HELP);
