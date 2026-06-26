#!/usr/bin/env node
import { runScript } from './lib/cli.js';
import { execute } from './lib/wait.js';

const HELP = `Submit an image generation task and poll until completion.

Usage:
  node {baseDir}/scripts/wait-image.js --json '{"prompt":"A futuristic city"}'
  node {baseDir}/scripts/wait-image.js --json '{"prompt":"Restyle this portrait","image":"https://example.com/input.png"}'
  node {baseDir}/scripts/wait-image.js --json '{"prompt":"Stylize it","images":["https://example.com/input.png"]}'

Options:
  --json <data>  Pass parameters as JSON string (use "-" for stdin)
  --dry-run      Preview the request without calling the API
  --verbose      Print debug info to stderr
  --help         Show this help message
`;

runScript(process.argv.slice(2), execute, HELP);
