#!/usr/bin/env node
import { runScript } from './lib/cli.js';
import { execute } from './lib/wait.js';

const HELP = `Submit a video generation task and poll until completion.

Usage:
  node scripts/wait-video.js --json '{"prompt":"A drone shot over mountains","duration":5}'
  node scripts/wait-video.js --json '{"prompt":"Animate this image","image":"https://example.com/input.png","duration":5}'
  node scripts/wait-video.js --json '{"prompt":"Create a transition","images":["https://example.com/1.png","https://example.com/2.png"],"duration":5}'
  node scripts/wait-video.js --json '{"prompt":"Bridge the first frame to the last frame","first_frame":"https://example.com/start.png","last_frame":"https://example.com/end.png","duration":5}'

Options:
  --json <data>  Pass parameters as JSON string (use "-" for stdin)
  --dry-run      Preview the request without calling the API
  --verbose      Print debug info to stderr
  --help         Show this help message
`;

runScript(process.argv.slice(2), execute, HELP);
